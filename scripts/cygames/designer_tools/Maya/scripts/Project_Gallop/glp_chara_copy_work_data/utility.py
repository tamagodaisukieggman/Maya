# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import subprocess

import maya.cmds as cmds

from PySide2 import QtWidgets

from . import const

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

reload(const)


def show_in_explorer(paths):
    """エクスプローラーで表示

    Args:
        paths ([str]): 表示したいパスリスト
    """

    for path in paths:

        if not os.path.exists(path):
            return

        try:
            subprocess.Popen(u'explorer /select,"%s"' % path.replace('/', '\\'))
        except Exception:
            return


def create_qt_context_menu(parent, pos, action_dict_list):
    """コンテキストメニューを作成

    Args:
        parent (QWidget): 親となるウィジェット
        pos (Qpoint): シグナルで送られてくるポジション
        action_dict_list ([{'label': str, 'function': function, 'arg': any, 'enable': bool}]): ラベル名、処理、引数、有効か？の辞書リスト.ラベルが'Separator'の時はセパレータ
    """

    context_menu = QtWidgets.QMenu(parent)
    actions = []

    for action_dict in action_dict_list:
        if action_dict['label'] == 'Separator':
            context_menu.addSeparator()
        else:
            q_action = context_menu.addAction(action_dict['label'])
            q_action.setEnabled(action_dict['enable'])
            actions.append(q_action)

    exec_action = context_menu.exec_(parent.mapToGlobal(pos))

    for action in actions:

        if action != exec_action:
            continue

        for action_dict in action_dict_list:

            if action.text() == action_dict['label'] and action_dict['function']:
                if action_dict['function'] and action_dict['arg']:
                    action_dict['function'](action_dict['arg'])
                elif action_dict['function'] and action_dict['arg'] is None:
                    action_dict['function']()


def get_icon_path(file_name):
    """iconパスの取得

    Args:
        file_name (str): 取得したいアイコンのファイル名

    Returns:
        str: アイコンのパス
    """

    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui', 'icon', file_name)


def normalize_path(path, sep_with_slash=True):
    """パス区切りを標準化

    Args:
        path (str): 元パス
        sep_with_slash(bool): /区切りか\\区切りか

    Returns:
        str: 変換後のパス
    """

    if sep_with_slash:
        return path.replace('\\', '/')
    else:
        return path.replace('/', '\\')


def load_need_plugin(open_file_path):
    """開く際に必要なプラグインのロード
    現状FBXのみ

    Args:
        open_file_path (str): 開くシーンのパス
    """

    ext = os.path.splitext(open_file_path)[-1].lower()

    if ext == '.fbx':
        load_fbx_plugin()


def load_fbx_plugin():
    """fbxプラグインのロード
    """

    if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
        cmds.loadPlugin('fbxmaya.mll')
