# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import sys
import subprocess
import threading

mayapy_exe_path = os.path.abspath(os.path.join(os.path.dirname(sys.executable), 'mayapy.exe'))


def exec_mayapy(module_name, options, on_complete=None, show_window=True):
    """mayapyを別プロセスで実行

    Args:
        module_name (str): 実行するモジュール名
        options (list[str]): モジュールに渡すオプション
        on_complete(function): サブプロセス完了後に実行する関数
        show_window(bool): ウィンドウを表示するか
    """

    args = [mayapy_exe_path, '-m', module_name] + options

    startup_info = subprocess.STARTUPINFO()

    if not show_window:
        startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup_info.wShowWindow = subprocess.SW_HIDE

    proc = subprocess.Popen(args, startupinfo=startup_info)

    def wait_for_completion():

        # 終了まで待機
        success = proc.wait() == 0

        if on_complete:
            on_complete(success)

    thread = threading.Thread(target=wait_for_completion)
    thread.start()


def get_options_from_dict(options):
    """辞書からコマンドライン引数のリストを取得する

    Args:
        options (dict): 元になる辞書

    Returns:
        list(str): コマンドライン引数のリスト
    """

    return [option for item in options.items() for option in _get_option_strings(*item)]


def _get_option_strings(key, value):
    """引数の値の型に応じたコマンドライン引数のリストを返す

    Args:
        key (str): キー
        value (Any): 値

    Returns:
        list(str): コマンドライン引数のリスト
    """

    result = ['--{}'.format(key)]

    if type(value) is bool:
        if not value:
            return []

    elif type(value) is list:
        if not value:
            return []

        result.extend(value)

    else:
        result.append(value)

    return result
