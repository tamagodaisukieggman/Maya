# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os
import re
import sys

# ==================================================
def __reimport_directory(target_dir_path, print_log):
    """
    フォルダ以下をリインポート
    """

    if not target_dir_path:
        return

    if not os.path.isdir(target_dir_path):
        return

    if print_log:
        print('-' * 40)
        print('Import Directory\n {0}'.format(target_dir_path))
        print('-' * 40)

    import_reload_str = ""
    if sys.version_info.major != 2:
        import_reload_str = 'from importlib import reload;'

    for root, dirs, files in os.walk(target_dir_path):

        root_dir_name = os.path.basename(root)

        if re.search('^_', root_dir_name):
            continue

        if re.search(r'\.', root_dir_name):
            continue

        relative_path = root.replace(target_dir_path, '').replace('\\', '.')

        if not relative_path:
            relative_path = '.'

        # ファイルのインポート
        for file_name in files:

            if re.search('^_', file_name):
                continue

            is_pyc = False

            if re.search('.pyc$', file_name):
                is_pyc = True

            else:
                if not re.search('.py$', file_name):
                    continue

            file_name_noext = os.path.splitext(file_name)[0]

            if is_pyc:
                exec_string = 'from {0} import {1}'.format(
                    relative_path, file_name_noext)

            else:
                exec_string = 'from {0} import {1};{2}reload({1})'.format(
                    relative_path, file_name_noext, import_reload_str)

            if print_log:
                print('File  ->  {0}'.format(exec_string))

            exec(exec_string)

        # フォルダのインポート
        for dir_name in dirs:

            if re.search('^_', dir_name):
                continue

            if re.search(r'\.', dir_name):
                continue

            exec_string = 'from {0} import {1};{2}reload({1})'.format(
                relative_path, dir_name, import_reload_str)

            if print_log:
                print('Folder  ->  {0}'.format(exec_string))

            exec(exec_string)


__reimport_directory(os.path.dirname(__file__), False)
