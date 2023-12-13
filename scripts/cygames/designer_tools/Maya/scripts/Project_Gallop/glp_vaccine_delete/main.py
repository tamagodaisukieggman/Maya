# -*- coding: utf-8 -*-
"""MVCでいうControllerを担う
"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from PySide2.QtCore import Qt
from PySide2.QtCore import QSettings
from PySide2 import QtGui, QtWidgets
from maya import OpenMayaUI

from . import view
from . import vaccine_vaccine

import os

import maya.cmds as cmds
import shiboken2


class Main(object):

    def __init__(self):
        """コンストラクタ
        """

        self.view = view.View()
        self.vaccine_vaccine = vaccine_vaccine

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        for widget in main_window.children():
            if type(target) == type(widget):
                widget.deleteLater()

    def show_ui(self):
        """UI描画
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)

        self.setup_view_event()
        self.view.show()

    def setup_view_event(self):
        """UIのevent設定
        """

        # パスセットボタン
        self.view.ui.pathSetButton.clicked.connect(lambda: self.clicked_pathSetButton_event())

        # 実行ボタン
        self.view.ui.execButton.clicked.connect(lambda: self.clicked_execButton_event())

    def clicked_pathSetButton_event(self):
        """
        """

        paths = cmds.fileDialog2(fileMode=3)
        if not paths:
            return

        path = paths[0]
        if not os.path.exists(path) or not os.path.isdir(path):
            return

        self.view.ui.filePathEdit.setText(path)

    def clicked_execButton_event(self):
        """
        """

        path = self.view.ui.filePathEdit.text()
        if not os.path.exists(path) or not os.path.isdir(path):
            return

        treated_list = self.vaccine_vaccine.treat_patient(path)

        if treated_list:
            print('*' * 20)
            for treated in treated_list:
                print(treated)
            print('*' * 20)

        cmds.confirmDialog(title="End", message=u"終了しました", button=['OK'])
