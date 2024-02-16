# -*- coding: utf-8 -*-
"""MVCでいうViewを担う
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from PySide2 import QtWidgets
from . import base_widget


class Rotation2HierarchyWidget(base_widget.BaseWidget):

    def __init__(self, parent, param_data_template):
        super(Rotation2HierarchyWidget, self).__init__(parent, param_data_template)

        self.target_line = None

    def create_widget(self):
        """ウィジェットの作成
        """

        lable = QtWidgets.QLabel('対象骨')
        self.target_line = QtWidgets.QLineEdit()
        target_sel_button = QtWidgets.QPushButton('選択')
        target_sel_button.clicked.connect(self.__target_select_event)
        target_set_button = QtWidgets.QPushButton('セット')
        target_set_button.clicked.connect(self.__target_set_event)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(lable)
        layout.addWidget(self.target_line)
        layout.addWidget(target_sel_button)
        layout.addWidget(target_set_button)

        self.main_layout.addLayout(layout)

    def get_target_data(self):
        """UIからプロセスの制御対象となるノードとアトリビュートリストを取得

        Returns:
            str: ノード
            list: アトリビュートリスト
        """

        return self.target_line.text(), ['rotateY']

    def import_param_data(self, target, param_data):
        """パラメーター情報の読み込み

        Args:
            target (str): ターゲットノード
            param_data (dict): プロセスで使用されるパラメーターdict. {attr_name: {'type': type, 'value': value},,,}
        """

        self.target_line.setText(target)

    def __target_set_event(self):
        """ターゲットセットイベント
        """

        sels = cmds.ls(sl=True, typ='transform')

        if sels:
            self.target_line.setText(sels[0])
            self.expression_edit.emit(self)

    def __target_select_event(self):
        """ターゲット選択イベント
        """

        target = self.target_line.text()
        if cmds.objExists(target):
            cmds.select(target, r=True)

