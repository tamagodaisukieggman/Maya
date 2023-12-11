# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import re
import subprocess
import sys


# ==================================================
def open_directory(target_path):
    """
    ディレクトリを開く

    :param target_path: 対象パス ファイル指定可
    """

    if not target_path:
        return

    target_dir_path = None

    if os.path.isfile(target_path):
        target_dir_path = os.path.dirname(target_path)

    elif os.path.isdir(target_path):
        target_dir_path = target_path

    if target_dir_path is None:
        return

    target_dir_path = target_dir_path.replace('/', '\\')
    subprocess.Popen('explorer "' + target_dir_path + '"')


# ==================================================
def open_notepad(target_file_path):
    """
    ノートパッドで開く

    :param target_file_path: 対象ファイルパス
    """

    if not target_file_path:
        return

    if not os.path.isfile(target_file_path):
        return

    subprocess.Popen('notepad "' + target_file_path + '"')


# ===============================================
def get_data_path_list(
        target_data_path,
        is_directory,
        file_name_filter,
        file_name_nofilter,
        extension_filter,
        dir_name_filter,
        dir_name_nofilter,
        contain_lower,
):
    u"""
    対象パス以下のファイルまたはディレクトリをすべて取得

    :param target_data_path: 対象パス ファイル指定可
    :param is_directory: ディレクトリかどうか
    :param file_name_filter: ファイル名フィルタ(含む) 正規表現、カンマ区切りで複数化
    :param file_name_nofilter: ファイル名フィルタ(含まない) 正規表現、カンマ区切りで複数化
    :param extension_filter: 拡張子フィルタ 正規表現、カンマ区切りで複数化
    :param dir_name_filter: フォルダ名フィルタ(含む) 正規表現、カンマ区切りで複数化
    :param dir_name_nofilter: フォルダ名フィルタ(含まない) 正規表現、カンマ区切りで複数化
    :param contain_lower: 下層を対象にするかどうか

    :return: ファイルまたはディレクトリパスリスト
    """

    target_data_path_list = []

    if not target_data_path:
        return

    # --------------------
    # 一時データリストの作成

    temp_data_path_list = []

    if os.path.isdir(target_data_path):

        target_dir_path = target_data_path.replace('\\', '/')

        if is_directory:
            temp_data_path_list.append(target_dir_path)

        for root, dirs, files in os.walk(target_dir_path):

            this_root_path = root.replace('\\', '/')

            if this_root_path.find('/.') >= 0:
                continue

            # ファイル
            if not is_directory:

                for this_file in files:

                    this_file_path = os.path.join(
                        root, this_file).replace('\\', '/')

                    temp_data_path_list.append(this_file_path)

            if not contain_lower:
                break

            # ディレクトリ
            if is_directory:

                for this_dir in dirs:

                    this_dir_path = os.path.join(
                        root, this_dir).replace('\\', '/')

                    temp_data_path_list.append(this_dir_path)

    elif os.path.isfile(target_data_path):

        target_file_path = target_data_path.replace('\\', '/')

        if not is_directory:
            temp_data_path_list.append(target_file_path)

    if not temp_data_path_list:
        return target_data_path_list

    # --------------------
    # フィルタのリスト化

    fix_file_name_filter_list = []
    fix_file_name_nofilter_list = []
    fix_extension_filter_list = []

    fix_dir_name_filter_list = []
    fix_dir_name_nofilter_list = []

    if file_name_filter:
        fix_file_name_filter_list = [x.strip()
                                     for x in file_name_filter.split(',')]

    if file_name_nofilter:
        fix_file_name_nofilter_list = [x.strip()
                                       for x in file_name_nofilter.split(',')]

    if extension_filter:
        fix_extension_filter_list = [x.strip()
                                     for x in extension_filter.split(',')]

    if dir_name_filter:
        fix_dir_name_filter_list = [x.strip()
                                    for x in dir_name_filter.split(',')]

    if dir_name_nofilter:
        fix_dir_name_nofilter_list = [x.strip()
                                      for x in dir_name_nofilter.split(',')]

    # --------------------
    # データパスをフィルタから割り出し
    for data_path in temp_data_path_list:

        if sys.version_info.major == 2:

            # TODO: simple_batchからsimple_batch2に全部移行&各関数での日本語対応ができたらこのチェックを外す
            # 処理ファイルのリストを環境変数に書き込んで渡しているあいだは日本語スルー
            try:
                # utf-8でもshift-jisでも日本語だとUnicodeEncodeErrorになる
                data_path.decode("utf-8")
            except UnicodeEncodeError:
                continue

        this_dir_path = os.path.dirname(data_path)
        this_data_name = os.path.basename(data_path)
        this_data_name_noext, this_data_ext = \
            os.path.splitext(this_data_name)

        this_data_ext = this_data_ext.lower()

        if this_dir_path.find('/.') >= 0:
            continue

        is_target = True

        # --------------------
        # フォルダ(含む)判定

        if fix_dir_name_filter_list:

            is_target = False

            for this_filter in fix_dir_name_filter_list:

                if re.search(this_filter, this_dir_path):
                    is_target = True
                    break
        else:
            is_target = True

        if not is_target:
            continue

        # --------------------
        # フォルダ(含まない)判定

        if fix_dir_name_nofilter_list:

            is_target = True

            for this_filter in fix_dir_name_nofilter_list:

                if re.search(this_filter, this_dir_path):
                    is_target = False
                    break
        else:
            is_target = True

        if not is_target:
            continue

        # --------------------
        # ファイル拡張子(含む)判定

        if not is_directory:

            if fix_extension_filter_list:

                is_target = False

                for this_filter in fix_extension_filter_list:

                    if not this_filter:
                        continue

                    if re.search(this_filter.lower(), this_data_ext):
                        is_target = True
                        break
            else:
                is_target = True

        if not is_target:
            continue

        # --------------------
        # ファイル(含む)判定

        if fix_file_name_filter_list:

            is_target = False

            for this_filter in fix_file_name_filter_list:

                if re.search(this_filter, this_data_name):
                    is_target = True
                    break
        else:
            is_target = True

        if not is_target:
            continue

        # --------------------
        # ファイル(含まない)判定

        if fix_file_name_nofilter_list:

            is_target = True

            for this_filter in fix_file_name_nofilter_list:

                if re.search(this_filter, this_data_name):
                    is_target = False
                    break
        else:
            is_target = True

        if not is_target:
            continue

        # --------------------

        target_data_path_list.append(data_path)

    return target_data_path_list
