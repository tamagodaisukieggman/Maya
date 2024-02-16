# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

from PySide2 import QtWidgets

from ....base_common import utility as base_utility

from ....glp_common.classes import neck_normal
from ....glp_common.classes import neck_pos

from .. import main_template
from .. import ui as chara_util_ui


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpCharaUtilityNeckEdgeSet'
        self.tool_label = '首のエッジセット(NeckEdgeSet)の設定'
        self.tool_version = '21082501'

        self.neck_normal = neck_normal.NeckNormalInfo()
        self.neck_pos = neck_pos.NeckPositionInfo()

    def ui_body(self):
        """
        UI要素のみ
        """

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('設定', self.add_selected_edge_to_neck_edge_set)
        _button_row_layout.set_button('選択', self.select_edge_from_neck_edge_set)
        _button_row_layout.set_button('規定位置へ', self.move_to_default_value)
        _button_row_layout.set_button('更新', self.update_neck_edge_set)
        _button_row_layout.set_button('除去', self.remove_selected_edge_from_neck_edge_set)
        _button_row_layout.set_button('削除', self.delete_neck_edge_set)
        _button_row_layout.show_layout()

    def add_selected_edge_to_neck_edge_set(self):
        """
        """

        text = '選択しているエッジをNeckEdgeSetに登録し、\n首の法線設定をしますか?'
        buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        result_button = QtWidgets.QMessageBox.question(None, '確認', text, buttons, QtWidgets.QMessageBox.Ok)
        if result_button != QtWidgets.QMessageBox.Ok:
            return

        self.neck_normal.add_neck_edge_set()

    def update_neck_edge_set(self):
        """
        """

        text = 'NeckEdgeSet内のエッジの法線を更新しますか?'
        buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        result_button = QtWidgets.QMessageBox.question(None, '確認', text, buttons, QtWidgets.QMessageBox.Ok)
        if result_button != QtWidgets.QMessageBox.Ok:
            return

        self.neck_normal.update_neck_edge_set()

    def remove_selected_edge_from_neck_edge_set(self):
        """
        """

        text = '選択しているエッジをNeckEdgeSetから除去しますか?'
        buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        result_button = QtWidgets.QMessageBox.question(None, '確認', text, buttons, QtWidgets.QMessageBox.Ok)
        if result_button != QtWidgets.QMessageBox.Ok:
            return

        self.neck_normal.remove_selected_edge_from_neck_edge_set()

    def select_edge_from_neck_edge_set(self):
        """
        """

        self.neck_normal.select_neck_edge_set()

    def move_to_default_value(self):
        """
        """

        text = 'NeckEdgeを規定位置にセットする'
        buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        result_button = QtWidgets.QMessageBox.question(None, '確認', text, buttons, QtWidgets.QMessageBox.Ok)
        if result_button != QtWidgets.QMessageBox.Ok:
            return

        self.neck_pos.move_to_default_value()

    def delete_neck_edge_set(self):
        """
        """

        text = 'NeckEdgeSetを削除しますか?'
        buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        result_button = QtWidgets.QMessageBox.question(None, '確認', text, buttons, QtWidgets.QMessageBox.Ok)
        if result_button != QtWidgets.QMessageBox.Ok:
            return

        self.neck_normal.delete_neck_edge_set()
