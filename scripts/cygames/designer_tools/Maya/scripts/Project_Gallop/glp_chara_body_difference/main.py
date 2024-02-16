# -*- coding: utf-8 -*-
u"""GallopCharaBodyDifference: 体型差分作成ツール(UI)"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import os
import sys

from maya import OpenMayaUI

import shiboken2
from PySide2 import QtWidgets

from . import view

from ..glp_chara_body_difference import body_difference

reload(body_difference)


# ==================================================
def main():
    exporter = Main()
    exporter.create_ui()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ==================================================
    def __init__(self):
        self.tool_version = "21070901"
        self.tool_name = "GallopCharaBodyDifference"

        self.window_name = self.tool_name + "Win"
        self.window_width = 240
        self.bust_l_suffix = "_BustL"
        self.bust_m_suffix = "_BustM"

        # スクリプトのパス関連
        self.script_file_path = None
        self.script_dir_path = None

        self.view = view.View()

    # ==================================================
    def initialize(self):

        self.script_file_path = os.path.abspath(__file__)
        self.script_file_path = self.script_file_path.replace("\\", "/")
        self.script_dir_path = os.path.dirname(self.script_file_path)

    # ==================================================
    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if type(target) == type(widget):
                widget.deleteLater()

    # ==================================================
    def create_ui(self):
        """ui作成
        """

        self.initialize()

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)

        self.setup_view_event()
        self.view.show()

    # ==================================================
    def setup_view_event(self):
        """UIのevent設定
        """

        self.view.ui.createBodyDiffBtn.clicked.connect(self.do_body_difference)
        self.view.ui.moveBodyDiffForPosContractBtn.clicked.connect(lambda *args: self.move_body_difference(0))
        self.view.ui.moveBodyDiffForPosExpandBtn.clicked.connect(lambda *args: self.move_body_difference(150))
        self.view.ui.moveBodyDiffForGrpNodeContractBtn.clicked.connect(lambda *args: self.move_body_difference(0, False))
        self.view.ui.moveBodyDiffForGrpNodeExpandBtn.clicked.connect(lambda *args: self.move_body_difference(150, False))
        self.view.ui.changeBodyDiffSkiningStateDetachBtn.clicked.connect(lambda: self.change_skin_status_for_body_difference(False))
        self.view.ui.changeBodyDiffSkiningStateBindBtn.clicked.connect(lambda: self.change_skin_status_for_body_difference(True))

    # ==================================================
    def move_body_difference(self, move_num, is_position=True):
        """
        """

        bd = body_difference.BodyDifference()
        bd.move_body_difference(move_num, is_position)

    # ==================================================
    def change_skin_status_for_body_difference(self, is_bind):
        """体型差分のバインド状態を変更する

        :param is_bind: バインドするかどうか Falseでデタッチ
        """

        bd = body_difference.BodyDifference()
        bd.do_change_skin_status(is_bind)

    # ==================================================
    def do_body_difference(self):
        """
        """

        q_ans = QtWidgets.QMessageBox.question(self.view, "実行確認", "体型差分を作成しますか")
        if not q_ans == QtWidgets.QMessageBox.Yes:
            return

        bd = body_difference.BodyDifference()
        bd.do_create_body_difference()
