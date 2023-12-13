# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

"""
priariのモデルシーンを開く
"""

try:
    # Maya 2022-
    from builtins import str
except:
    pass

import os

import maya.cmds as cmds

from ....priari_common.utility import model_define as define

from .. import main_template
from . import priari_scene_opener


class Main(main_template.Main):
    """
    """

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'PriariSceneOpener'
        self.tool_label = 'モデルシーンを開く'
        self.tool_version = '22080901'

        self.scene_opener = priari_scene_opener.PriariSceneOpener()
        self.root_path_input = None
        self.type_pull_down = None
        self.id_input = None
        self.ext_pull_down = None
        self.search_list = None

        self.type_list = [
            'all',  # 全検索（デフォルト）
            define.AVATAR_DATA_TYPE,
            define.UNIT_DATA_TYPE,
            define.WEAPON_DATA_TYPE,
            define.PROP_DATA_TYPE,
            define.SUMMON_DATA_TYPE,
            define.ENEMY_DATA_TYPE,
            'feedback',
        ]
        self.ext_list = ['.ma', '.fbx', 'all']

    def ui_body(self):
        """UIの構成
        """

        cmds.columnLayout(adjustableColumn=True)

        # モデルルートパス指定。デフォルトでSVNのパスを入れる。
        cmds.rowLayout(numberOfColumns=2, adj=2)
        cmds.text(label='モデルルートパス:', align='left')
        self.root_path_input = cmds.textField(text=define.SVN_PATH, cc=self.refresh_search_from_ui)
        cmds.setParent('..')

        # 検索情報を入れるrowLayout
        cmds.rowLayout(adj=4, numberOfColumns=5)

        cmds.text(label='type:', align='left')
        self.type_pull_down = cmds.optionMenu(cc=self.refresh_search_from_ui)
        for type in self.type_list:
            cmds.menuItem(label=type)

        cmds.text(label='id:', align='left')
        self.id_input = cmds.intField(minValue=0, maxValue=9999, cc=self.refresh_search_from_ui)

        self.ext_pull_down = cmds.optionMenu(cc=self.refresh_search_from_ui)
        for ext in self.ext_list:
            cmds.menuItem(label=ext)

        cmds.setParent('..')

        # 検索結果表示リスト。全検索で少し時間がかかるので、起動時は検索しない。
        self.search_list = cmds.textScrollList(h=80, dcc=self.open_file_from_ui)

        # 実行ボタン
        cmds.button(label='選択ファイルを開く', c=self.open_file_from_ui)

        cmds.setParent('..')

    def refresh_search_from_ui(self, arg=None):
        """UI情報を元に検索結果を更新する

        Args:
            arg (_type_, optional): no using. Defaults to None.
        """

        # 一旦リセット
        cmds.textScrollList(self.search_list, e=True, removeAll=True)

        # 入力情報
        root_path = cmds.textField(self.root_path_input, q=True, text=True)
        data_type = cmds.optionMenu(self.type_pull_down, q=True, value=True)
        id_input_str = str(cmds.intField(self.id_input, q=True, value=True))
        ext_str = cmds.optionMenu(self.ext_pull_down, q=True, value=True)

        # ファイル検索
        search_list = self.scene_opener.search_files(root_path, data_type, id_input_str, ext_str)
        append_list = [p.replace(root_path + '\\', '').replace('\\', '/') for p in search_list]
        cmds.textScrollList(self.search_list, e=True, append=append_list)

    def open_file_from_ui(self, arg=None):
        """UI情報を元にファイルを開く

        Args:
            arg (_type_, optional): no using. Defaults to None.
        """

        selected_item = cmds.textScrollList(self.search_list, q=True, selectItem=True)

        if not selected_item:
            return

        root_path = cmds.textField(self.root_path_input, q=True, text=True)
        target_path = os.path.join(root_path, selected_item[0])

        self.scene_opener.open_file(target_path)
