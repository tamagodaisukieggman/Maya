# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import re
import subprocess


# ==================================================
def open_directory(target_path):

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

    if not os.path.isfile(target_file_path):
        return

    subprocess.Popen('notepad "' + target_file_path + '"')


# ===============================================
def get_target_data_path_list(
        target_data_path,
        is_directory,
        name_filter,
        name_notfilter,
        extension_filter,
        contain_lower=True,
):

    target_data_path_list = []

    if not target_data_path:
        return target_data_path_list

    temp_data_path_list = []

    if os.path.isdir(target_data_path):

        target_dir_path = target_data_path.replace('\\', ' / ')

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

    fix_filter_list = []
    fix_notfilter_list = []
    fix_extfilter_list = []

    if name_filter:
        fix_filter_list = name_filter.split(' ')

    if name_notfilter:
        fix_notfilter_list = name_notfilter.split(' ')

    if extension_filter:
        fix_extfilter_list = extension_filter.split(' ')

    print(fix_extfilter_list)

    for data_path in temp_data_path_list:

        this_dir_path = os.path.dirname(data_path)
        this_data_name = os.path.basename(data_path)
        this_data_name_noext, this_data_ext = \
            os.path.splitext(data_path)

        this_data_ext = this_data_ext.lower()

        if this_dir_path.find('/.') >= 0:
            continue

        is_target = True

        if not is_directory:

            if fix_extfilter_list:

                is_target = False

                for this_filter in fix_extfilter_list:

                    if not this_filter:
                        continue

                    if re.search(this_filter.lower(), this_data_ext):
                        is_target = True
                        break
            else:
                is_target = True

        if not is_target:
            continue

        if fix_filter_list:

            is_target = False

            for this_filter in fix_filter_list:

                if re.search(this_filter, this_data_name):
                    is_target = True
                    break
        else:
            is_target = True

        if not is_target:
            continue

        if fix_notfilter_list:

            is_target = True

            for this_filter in fix_notfilter_list:

                if re.search(this_filter, this_data_name):
                    is_target = False
                    break
        else:
            is_target = True

        if not is_target:
            continue

        target_data_path_list.append(data_path)

    return target_data_path_list
