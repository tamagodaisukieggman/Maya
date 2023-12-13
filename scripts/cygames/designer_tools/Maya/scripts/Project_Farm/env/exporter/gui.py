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

from ...base_common import utility as base_utility
from ..common import command as env_command
from ..common import gui as env_gui
from . import command
from . import main_window_pyside2

reload(env_command)
reload(env_gui)
reload(command)
reload(main_window_pyside2)

option_key = 'farmEnvExporterOption'


class MainWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = main_window_pyside2.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.ExecuteButton.clicked.connect(self.export)

        self.scene = None

        if cmds.optionVar(ex=option_key):
            should_trim = cmds.optionVar(q=option_key)
            self.ui.ShouldTrim.setChecked(bool(should_trim))

    def closeEvent(self, event):
        should_trim = self.ui.ShouldTrim.isChecked()
        cmds.optionVar(iv=(option_key, int(should_trim)))
        super(MainWindow, self).closeEvent(event)

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
        widget = env_gui.SceneWidget()
        widget.update(cmds.file(q=True, sn=True), show_path=True)
        self.ui.MainLayout.insertWidget(0, widget)
        self.scene = widget

    def export(self):
        models = self.scene.get_enabled_models()
        nodes = [model.ui.NameLabel.text() for model in models]
        path = self.scene.ui.PathLabel.text()
        paths = [path for _ in models]
        should_trim = self.ui.ShouldTrim.isChecked()
        should_trims = [should_trim for _ in models]
        command.execute_batch(paths, nodes, should_trims)
        base_utility.ui.dialog.open_ok(u'FarmEnvExporter', u'エクスポートが完了しました。')
