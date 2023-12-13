# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from importlib import reload
except:
    pass

from maya import cmds
from maya import OpenMayaUI as omui
from maya.app.general import mayaMixin
import sys

from PySide2 import QtCore, QtGui, QtWidgets
import shiboken2

from ....base_common import utility as base_utility
from ...common import command as env_cmd
from ...common import gui as env_gui
from . import command
from . import main_window_pyside2

reload(env_cmd)
reload(env_gui)
reload(command)
reload(main_window_pyside2)


class MainWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = main_window_pyside2.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.ExecuteButton.clicked.connect(self.execute)
        self.ui.DefaultViewportButton.clicked.connect(self.show_display)
        self.ui.HideViewportButton.clicked.connect(self.hide_display)

        self.scene = env_gui.SceneWidget()
        self.ui.MainLayout.insertWidget(0, self.scene)

        self.camera_list = self.ui.CameraList

        self.title = self.windowTitle()

    def show(self):
        ptr = omui.MQtUtil.mainWindow()

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)
        else:
            main_window = shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)

        for widget in main_window.children():
            if type(widget) == self.__class__:
                widget.close()          # クローズイベントを呼んでウインドウを閉じる
                widget.deleteLater()    # Mayaウインドウの子からインスタンスを削除

        super(MainWindow, self).show()

    def update(self):
        self.scene.update(cmds.file(q=True, sn=True), show_path=False)

        self.camera_list.clear()
        self.camera_list.addItems(command.get_cameras())

    def execute(self):
        cameras = [item.text() for item in self.ui.CameraList.selectedItems()]

        if not cameras:
            base_utility.ui.dialog.open_ok(
                self.windowTitle(),
                u'カメラを選択してください。')
            return

        pos_list = [command.get_translate_values(cam) for cam in cameras]
        positions = [p for pos in pos_list for p in pos]

        models = self.scene.get_enabled_models()
        nodes = [model.ui.NameLabel.text() for model in models]

        for node in nodes:
            command.set_backface_color(node, positions, add=True, remove=True)

        self.set_display(True)

        self.update()

        base_utility.ui.dialog.open_ok(
            self.windowTitle(),
            u'背面削除設定が完了しました。')

    def set_display(self, state):
        models = self.scene.get_enabled_models()
        nodes = [model.ui.NameLabel.text() for model in models]

        for node in nodes:
            env_cmd.set_display_color(node, state)

        env_cmd.set_alpha_cut(state)

    def show_display(self):
        self.set_display(False)

    def hide_display(self):
        self.set_display(True)
