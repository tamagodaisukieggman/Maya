# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os
import shutil

import maya.cmds as cmds
import maya.mel as mel


# ==================================================
def open(target_file_path):
    """
    ファイルを開く

    :param target_file_path: ファイルパス
    """

    if not os.path.isfile(target_file_path):
        return False

    try:

        cmds.file(
            target_file_path,
            open=True,
            force=True,
            options='v=0;',
            ignoreVersion=True)

    except:
        return False

    return True


# ==================================================
def save(target_file_path=None, save_as=True):
    """
    ファイルを保存
    """

    current_file_path = cmds.file(q=True, sn=True)

    if not current_file_path:
        return

    try:

        if target_file_path:

            target_dir_path = os.path.dirname(target_file_path)

            if not os.path.isdir(target_dir_path):
                os.makedirs(target_dir_path)

            cmds.file(rn=target_file_path)
            cmds.file(save=True)

            if not save_as:
                cmds.file(rn=current_file_path)

        else:
            cmds.file(save=True)

    except:

        return False

    return True


# ==================================================
def open_temp(
        target_file_path, temp_file_name=None, temp_dir_path=None):
    """
    一時ファイルを開く

    :param target_file_path: 対象ファイルパス
    :param temp_file_name: 一時ファイル名
    :param temp_dir_path: 一時ファイルのフォルダ

    :return: 一時ファイルパス 作成できなかった場合はNone
    """

    if not os.path.isfile(target_file_path):
        return

    temp_file_path = create_temp(
        target_file_path, temp_file_name, temp_dir_path
    )

    if temp_file_path is None:
        return

    try:
        cmds.file(
            temp_file_path,
            open=True,
            force=True,
            options='v=0;',
            ignoreVersion=True)
    except:
        pass

    return temp_file_path


# ==================================================
def create_temp(
        target_file_path, temp_file_name=None, temp_dir_path=None):
    """
    一時ファイルを作成

    :param target_file_path: 対象ファイルパス
    :param temp_file_name: 一時ファイル名
    :param temp_dir_path: 一時ファイルのフォルダ

    :return: 一時ファイルパス 作成できなかった場合はNone
    """

    if not target_file_path:
        return

    if not os.path.isfile(target_file_path):
        return

    target_file_path = target_file_path.replace('\\', '/')

    # -----------------------
    # ファイル名などの確定

    if not temp_file_name:
        temp_file_name = '____temp_' + os.path.basename(target_file_path)

    if not temp_dir_path:
        temp_dir_path = os.path.dirname(target_file_path)

    temp_file_path = temp_dir_path + '/' + temp_file_name

    # -----------------------
    # 一時ファイルの削除

    if os.path.isfile(temp_file_path):
        os.remove(temp_file_path)

    # -----------------------
    # 現在のファイルと等しい場合は
    # 現在のファイルから一時ファイルを作成

    is_current_file = False

    current_file_path = cmds.file(q=True, sn=True)

    if current_file_path:

        current_file_path = current_file_path.replace('\\', '/')

        if os.path.isfile(current_file_path):

            if current_file_path.lower() == target_file_path.lower():
                is_current_file = True

    is_copy = False

    if is_current_file:

        is_created = True

        try:

            cmds.file(rn=temp_file_path)
            cmds.file(save=True)
            cmds.file(rn=current_file_path)

        except:

            is_created = False

        finally:

            cmds.file(rn=current_file_path)

        if not is_created:

            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)

            is_copy = True

    else:
        is_copy = True

    # -----------------------
    # 現在のファイルではない場合はベースをコピー
    # またリネームに失敗したときもベースをコピー

    if is_copy:
        shutil.copyfile(target_file_path, temp_file_path)

    return temp_file_path
