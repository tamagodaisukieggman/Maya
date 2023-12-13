# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import sys
import shiboken2
import maya.cmds as cmds

from PySide2 import QtWidgets
from maya.app.general import mayaMixin
from maya import OpenMayaUI

from . import view_uv_alpha_mask

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

reload(view_uv_alpha_mask)


class Main(object):

    def __init__(self):
        """初期化
        """

        self.ui = GUI()

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.close()          # クローズイベントを呼んでウインドウを閉じる
                widget.deleteLater()    # Mayaウインドウの子からインスタンスを削除

    def show_ui(self):
        """UI表示
        """

        self.deleteOverlappingWindow(self.ui)
        self.setup_view_event()
        self.ui.show()

    def setup_view_event(self):
        """イベント設定
        """

        self.ui.uv_alpha_mask_button.clicked.connect(self.uv_alpha_mask_button_event)
        self.ui.lambert_button.clicked.connect(self.lambert_button_event)

    def uv_alpha_mask_button_event(self):
        """UVAlphaMask表示ボタンのイベント
        """

        mats = cmds.ls(sl=True, type='lambert')
        cmds.select(cl=True)

        if not mats:
            cmds.warning('マテリアルが選択されていません')
            return

        message = '以下のマテリアルをUVAlphaMask確認用マテリアルに変換します\n'
        message += '\n'.join(mats)

        confirm = cmds.confirmDialog(
            m=message,
            button=['Yes', 'No'],
            defaultButton='Yes',
            cancelButton='No',
            dismissString='No',)

        if confirm == 'No':
            return

        for mat in mats:
            if view_uv_alpha_mask.replace_to_uv_alpha_mask_material(mat):
                print('SUCCESS: ' + mat)
            else:
                print('FAILED: ' + mat)

    def lambert_button_event(self):
        """lambertに戻すボタンのイベント
        """

        mats = cmds.ls(sl=True, type='dx11Shader')
        cmds.select(cl=True)

        if not mats:
            cmds.warning('マテリアルが選択されていません')
            return

        message = '以下のマテリアルをlambertマテリアルに戻します\n'
        message += '\n'.join(mats)

        confirm = cmds.confirmDialog(
            m=message,
            button=['Yes', 'No'],
            defaultButton='Yes',
            cancelButton='No',
            dismissString='No',)

        if confirm == 'No':
            return

        for mat in mats:
            if view_uv_alpha_mask.replace_to_lambert_material(mat):
                print('SUCCESS: ' + mat)
            else:
                print('FAILED: ' + mat)


class GUI(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)

        self.titleName = 'GlpViewUVAlphaMask'
        self.setupUi()

    def setupUi(self):

        self.resize(200, 150)
        self.setWindowTitle(self.titleName)

        central_widget = QtWidgets.QWidget(self)
        central_v_layout = QtWidgets.QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        label = QtWidgets.QLabel()
        label.setText('【UVAlphaMask確認用マテリアル変換】\n選択しているマテリアルを変換します')
        central_v_layout.addWidget(label)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.uv_alpha_mask_button = QtWidgets.QPushButton()
        self.uv_alpha_mask_button.setText('UV Alpha Maskマテリアルに変換')
        self.uv_alpha_mask_button.setSizePolicy(sizePolicy)
        central_v_layout.addWidget(self.uv_alpha_mask_button)

        self.lambert_button = QtWidgets.QPushButton()
        self.lambert_button.setText('lambertマテリアルに戻す')
        self.lambert_button.setSizePolicy(sizePolicy)
        central_v_layout.addWidget(self.lambert_button)
