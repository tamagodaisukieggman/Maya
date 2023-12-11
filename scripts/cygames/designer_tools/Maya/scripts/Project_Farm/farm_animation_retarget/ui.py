# -*- coding: utf-8 -*-
u"""
name: animation_retarget.py
data: 2020/8/19
ussage: priari 用 Rig 自動作成ツール
etc:
"""
try:
    # Maya 2022-
    from builtins import str
except:
    pass

import imp
import logging
from PySide2 import QtWidgets
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from . import command

logger = logging.getLogger(__name__)

TOOL_NAME = 'animation_retarget'
TOOL_VERSION = 'Ver 1.1.5'
TOOL_TITLE = 'Animation Retarget' + '   ' + TOOL_VERSION


def get_maya_win():
    u"""Mayaのメインウィンドウを取得する関数

    """
    try:
        from maya import OpenMayaUI

    except ImportError:
        return None

    try:
        imp.find_module("shiboken2")
        import shiboken2
        return shiboken2.wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QWidget)

    except ImportError:
        import shiboken
        return shiboken.wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QWidget)


class Animation_RetargetUI(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Animation_RetargetUI, self).__init__(parent)

        self.setObjectName(TOOL_NAME)
        self.setWindowTitle(TOOL_TITLE)
        self.resize(400, 80)

        self._initUI()

    def _initUI(self):
        widget = QtWidgets.QWidget()
        main_Layout = QtWidgets.QVBoxLayout()
        path_Layout = QtWidgets.QHBoxLayout()
        check_Layout = QtWidgets.QHBoxLayout()

        self.setCentralWidget(widget)

        # 出力パス の ラベル
        self.file_path_label = QtWidgets.QLabel()
        self.file_path_label.setText('Retarget File')
        self.file_path_label.setFixedWidth(85)

        # 出力パス の ラインエディット
        self.file_path_lineedit = QtWidgets.QLineEdit()

        # 出力パス の 参照ボタン
        self.file_path_button = QtWidgets.QPushButton('...')
        self.file_path_button.setFixedWidth(30)
        self.file_path_button.clicked.connect(self.select_file)

        # プライマリ の チェックボックス
        self.primary_check = QtWidgets.QCheckBox("Retarget Basic Joint Only")
        self.primary_check.setChecked(False)

        # ベイク の チェックボックス
        self.bake_check = QtWidgets.QCheckBox("Animation Key Bake")
        self.bake_check.setChecked(True)

        # 削除 の チェックボックス
        self.delete_check = QtWidgets.QCheckBox("Delete Retarget File From Scene")
        self.delete_check.setChecked(True)

        # 実行ボタン
        self.retarget_button = QtWidgets.QPushButton(u" Animation Retarget ")
        self.retarget_button.clicked.connect(self.retarget)

        path_Layout.addWidget(self.file_path_label)
        path_Layout.addWidget(self.file_path_lineedit)
        path_Layout.addWidget(self.file_path_button)

        check_Layout.addWidget(self.primary_check)
        check_Layout.addWidget(self.bake_check)
        check_Layout.addWidget(self.delete_check)

        main_Layout.addLayout(path_Layout)
        main_Layout.addLayout(check_Layout)
        main_Layout.addWidget(self.retarget_button)
        widget.setLayout(main_Layout)

    def select_file(self):
        # ファイル選択
        directory = command.get_filepath()
        file_path = QtWidgets.QFileDialog.getOpenFileName(
                                    self,
                                    'Select File',
                                    directory,
                                    ("Maya ASCII (*.ma);;Maya Binary (*.mb);;FBX (*.fbx)")
                                    )[0]
        self.file_path_lineedit.setText(str(file_path))

    def retarget(self):
        # リターゲット実行
        file_path = self.file_path_lineedit.text()
        primary = self.primary_check.isChecked()
        bake = self.bake_check.isChecked()
        delete = self.delete_check.isChecked()

        command.main(file_path, bake, delete, primary)


def main():
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.windowTitle() == TOOL_TITLE:
            widget.deleteLater()

    # maya_win = get_maya_win()
    window = Animation_RetargetUI()
    window.show()
