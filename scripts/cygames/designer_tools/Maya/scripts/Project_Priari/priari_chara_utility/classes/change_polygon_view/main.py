# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from ....base_common import classes as base_class

from . import change_polygon_view
from .. import main_template


class Main(main_template.Main):

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'PriariCharaUtilityPolygonViewChange'
        self.tool_label = 'Mayaの描画表示・非表示'
        self.tool_version = '19112201'

        self.button_width = 70
        self.label_width = 100

        self.change_polygon_view = change_polygon_view.ChangePolygonView()

    def ui_body(self):
        """
        UI要素のみ
        """

        cmds.columnLayout(adj=True)
        # 法線表示
        cmds.rowLayout(
            numberOfColumns=4,
            columnWidth4=(self.label_width, self.button_width, self.button_width, self.button_width))

        cmds.text(l='法線表示')
        base_class.ui.button.Button(
            "非表示", self.change_polygon_view.change_normal, ["none"], width=self.button_width)
        base_class.ui.button.Button(
            "頂点", self.change_polygon_view.change_normal, ["vertex"], width=self.button_width)
        base_class.ui.button.Button(
            "フェース", self.change_polygon_view.change_normal, ["face"], width=self.button_width)

        cmds.setParent("..")

        # 法線サイズ
        cmds.rowLayout(
            numberOfColumns=3,
            columnWidth3=(self.label_width, self.button_width, self.button_width))
        cmds.text(l='法線サイズ')
        base_class.ui.button.Button(
            "ダウン", self.change_polygon_view.change_normal, ["sizedown"], width=self.button_width)
        base_class.ui.button.Button(
            "アップ", self.change_polygon_view.change_normal, ["sizeup"], width=self.button_width)
        cmds.setParent("..")

        # エッジ表示
        cmds.rowLayout(
            numberOfColumns=4,
            columnWidth4=(self.label_width, self.button_width, self.button_width, self.button_width))
        cmds.text(l='エッジ表示')
        base_class.ui.button.Button(
            "標準", self.change_polygon_view.change_edge, ["none"], width=self.button_width)
        base_class.ui.button.Button(
            "ソフト", self.change_polygon_view.change_edge, ["soft"], width=self.button_width)
        base_class.ui.button.Button(
            "ハード", self.change_polygon_view.change_edge, ["hard"], width=self.button_width)
        cmds.setParent("..")

        # 頂点カラー
        cmds.rowLayout(
            numberOfColumns=3,
            columnWidth3=(self.label_width, self.button_width, self.button_width))
        cmds.text(l='頂点カラー')
        base_class.ui.button.Button(
            "非表示", self.change_polygon_view.change_vertex_color, ["vertex_color_off"], width=self.button_width)
        base_class.ui.button.Button(
            "表示", self.change_polygon_view.change_vertex_color, ["vertex_color_on"], width=self.button_width)
        cmds.setParent("..")

        # ライティング
        cmds.rowLayout(
            numberOfColumns=3,
            columnWidth3=(self.label_width, self.button_width, self.button_width))
        cmds.text(l='ライティング')
        base_class.ui.button.Button(
            "デフォルト", self.change_polygon_view.change_display, ['default'], width=self.button_width)
        base_class.ui.button.Button(
            "フラット", self.change_polygon_view.change_display, ['flat'], width=self.button_width)
        cmds.setParent("..")

        # テクスチャ
        cmds.rowLayout(
            numberOfColumns=3,
            columnWidth3=(self.label_width, self.button_width, self.button_width))
        cmds.text(l='テクスチャ')
        base_class.ui.button.Button(
            "非表示", self.change_polygon_view.change_display, ['texture_off'], width=self.button_width)
        base_class.ui.button.Button(
            "表示", self.change_polygon_view.change_display, ['texture_on'], width=self.button_width)
        cmds.setParent("..")

        # ワイヤーフレーム
        cmds.rowLayout(
            numberOfColumns=3,
            columnWidth3=(self.label_width, self.button_width, self.button_width))
        cmds.text(l='ワイヤーフレーム')
        base_class.ui.button.Button(
            "非表示", self.change_polygon_view.change_display, ['wire_off'], width=self.button_width)
        base_class.ui.button.Button(
            "表示", self.change_polygon_view.change_display, ['wire_on'], width=self.button_width)
        cmds.setParent("..")
        cmds.setParent("..")
