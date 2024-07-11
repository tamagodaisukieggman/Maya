# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import re
import subprocess
import csv
import sys

import maya.cmds as cmds

from PySide2 import QtWidgets

from . import const

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

reload(const)


def is_hit_text(text, search_word, replace_dict={}):
    """テキストが検索ワードに引っかかるかの判定を行う

    Args:
        text (str): 検索対象
        search_word (str): 検索ワード
        replace_dict (dict): 検索用辞書 search_wordが一致した時、置換した値も一緒に検索ワードに加える
                             search_word="hoge"でreplace_dict={"hogehoge": "fugafuga"}の場合、
                             最終的な検索ワードは["hoge", "hogehoge", "fugafuga"]とする
    Returns:
        bool: ヒットしたか
    """

    search_word = search_word.replace('　', ' ')  # 全角スペースを半角に
    search_word = re.sub(' +', ' ', search_word)  # スペースの繰り返しを除去

    # ANDリストに分割
    and_list = re.split(const.AND_FLAG, search_word)
    and_list = [x for x in and_list if x]

    and_result = True

    for and_str in and_list:

        or_result = False

        # ORリストに分割
        or_list = re.split(const.OR_FLAG, and_str)

        for or_str in or_list:

            target_str = or_str

            # 検索ワード先頭に除外フラグがあるかどうか
            is_exclude = target_str.startswith(const.EXCLUDE_FLAG) and target_str != const.EXCLUDE_FLAG
            if is_exclude:
                target_str = re.sub(r'^{}'.format(const.EXCLUDE_FLAG), '', target_str)
            # 検索ワード先頭に正規表現フラグがあるかどうか
            is_pattern = target_str.startswith(const.RE_FLAG) and target_str != const.RE_FLAG
            if is_pattern:
                target_str = re.sub(r'^{}'.format(const.RE_FLAG), '', target_str)

            target_str_list = [target_str]

            if replace_dict:
                for k, v in replace_dict.items():
                    if k.find(target_str) >= 0:
                        value = v
                        if v.startswith(const.RE_FLAG) and target_str != const.RE_FLAG:
                            is_pattern = True
                            value = re.sub(r'^{}'.format(const.RE_FLAG), '', value)
                        target_str_list.extend([k, value])

            # 除外フラグがある場合は、textに全て検索ワードが一致しなければhit
            if is_exclude:
                for target_str in target_str_list:
                    if (is_pattern and re.search(target_str, text)) or text.find(target_str) >= 0:
                        break
                else:
                    or_result = True
            # 除外フラグがない場合は、textに何れか一致でhit
            else:
                for target_str in target_str_list:
                    if (is_pattern and re.search(target_str, text)) or text.find(target_str) >= 0:
                        or_result = True
                        break

        if not or_result:
            and_result = False
            break

    return and_result


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


def copy_to_clipboard(text):

    byte_text = text.encode('cp932')

    try:
        p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
        p.stdin.write(byte_text)
        p.stdin.close()

        return True
    except Exception:
        return False


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


def get_setting_path():
    """設定ファイルのパスを取得

    Returns:
        str: 設定ファイルのパス
    """

    tool_dir = cmds.internalVar(userAppDir=True) + 'TKG/' + const.TOOL_NAME + '/'
    setting_file_path = tool_dir + const.TOOL_NAME + '.ini'
    return setting_file_path


def get_bookmark_file_path():
    """ブックマークファイルのパスを取得

    Returns:
        str: ブックマークファイルのパス
    """

    tool_dir = cmds.internalVar(userAppDir=True) + 'TKG/' + const.TOOL_NAME + '/'
    bookmark_file_path = tool_dir + const.TOOL_NAME + '_bookmark.txt'
    return bookmark_file_path


def get_tkg_scene_opener_bookmark_file_path():
    """TkgSceneOpenerのブックマークファイルパスを取得

    Returns:
        str: TkgSceneOpenerのブックマークファイルパス
    """

    toolDir = cmds.internalVar(userAppDir=True) + 'TKG/' + const.CY_SCENE_OPENER_NAME + '/'
    bookmark_file_path = toolDir + const.CY_SCENE_OPENER_NAME + '_bookmark.txt'
    return bookmark_file_path


def str_setting_to_bool(str_setting):
    """stringで帰ってくる設定の文字列をboolに変換する

    Args:
        str_setting (str): 設定の文字列

    Returns:
        bool: 変換したbool値
    """

    if str_setting.lower() == 'true':
        return True
    else:
        return False


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


def create_csv_dict_list(csv_path):
    """csvから1行をDictにした全ての行が入ったlistを取得
    Python2でcsv.dictReader()で取得する時にheaderが日本語だと問題になるため
    csv.readerでまずheaderと本体を分離、decodeしてcsv.DictReader()で取得するのと同じ状態の
    辞書のリストを取得する

    Args:
        csv_path (str): 読み込むCSVのパス

    Returns:
        list: CSVから読み込んだそれぞれの行を{'<header>': <value>}の辞書形式にしたlist
    """

    csv_dict_list = []
    if sys.version_info.major == 2:
        with open(csv_path) as f:
            reader = csv.reader(f)
            header = next(reader)
            header = [h.decode('utf-8-sig') for h in header]
            for r in reader:
                csv_dict = {}
                for index, key in enumerate(header):
                    value = r[index]
                    value = value.decode('utf-8-sig')
                    csv_dict[key] = value
                csv_dict_list.append(csv_dict)
    else:
        with open(csv_path, encoding='utf-8_sig') as f:
            reader = csv.DictReader(f)
            for r in reader:
                csv_dict_list.append(r)

    return csv_dict_list
