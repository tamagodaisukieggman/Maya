# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import next
    from builtins import zip
    from importlib import reload
except:
    pass

from maya import cmds
from maya import OpenMayaUI as omui
from maya.app.general import mayaMixin

from PySide2 import QtCore, QtGui, QtWidgets
import shiboken2

from . import command
from . import export_range
from . import main_window_pyside2

reload(command)
reload(export_range)
reload(main_window_pyside2)


class MainWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    connections = [0, 1, 1, 2, 2, 3]
    names = ['st', 'lp', 'ed']
    attr_name = export_range.ExportRange.get_attr_name()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.data = None

        self.ui = main_window_pyside2.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.InitButton.clicked.connect(lambda: self.update(True))

        self.buttons = [
            self.ui.StStartButton,
            self.ui.StEndButton,
            self.ui.LpStartButton,
            self.ui.LpEndButton,
            self.ui.EdStartButton,
            self.ui.EdEndButton,
        ]

        self.texts = [
            self.ui.StStartText,
            self.ui.StEndText,
            self.ui.LpStartText,
            self.ui.LpEndText,
            self.ui.EdStartText,
            self.ui.EdEndText,
        ]

        self.frames = [
            self.ui.StFrame,
            self.ui.LpFrame,
            self.ui.EdFrame,
        ]

        for text in self.texts:
            text.editingFinished.connect(self.update)

        for button, text in zip(self.buttons, self.texts):
            button.clicked.connect(lambda t=text: self.set_current(t))

        self.scene_job_number = cmds.scriptJob(
            event=['SceneOpened', self.update], protected=True)

        self.update()

    def show(self):
        ptr = omui.MQtUtil.mainWindow()
        try:
            main_window = shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)
        except:
            # Maya 2022-
            main_window = shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)

        for widget in main_window.children():
            if type(widget) == self.__class__:
                widget.close()          # クローズイベントを呼んでウインドウを閉じる
                widget.deleteLater()    # Mayaウインドウの子からインスタンスを削除

        super(MainWindow, self).show()

    def closeEvent(self, event):
        if self.scene_job_number is not None:
            cmds.scriptJob(kill=self.scene_job_number, force=True)
            self.scene_job_number = None
        super(MainWindow, self).closeEvent(event)

    def to_frames(self, ranges):
        if ranges is None:
            return None

        frames = []

        for name in self.names:
            r = next((x for x in ranges if x.name == name), None)
            if r is None:
                continue
            frames.append(r.start)
            frames.append(r.end)

        if len(frames) != 6:
            return None

        return frames

    def get_data(self, data):
        diff = [None] * 4

        for data, i in zip(data, self.connections):
            if self.data is None or data != self.data[i]:
                diff[i] = data

        if any(dif is not None for dif in diff):
            if self.data is None:
                return diff
            return sorted([dif or dat for dif, dat in zip(diff, self.data)])
        else:
            return None

    def init(self):
        start = cmds.playbackOptions(q=True, ast=True)
        end = cmds.playbackOptions(q=True, aet=True)
        mid1 = cmds.playbackOptions(q=True, min=True)
        mid2 = cmds.playbackOptions(q=True, max=True)
        mid1 = mid1 if mid1 > start else start + 1
        mid2 = mid2 if mid2 < end else end - 1
        self.data = sorted([start, mid1, mid2, end])

    def update_data(self):
        frames = self.to_frames(export_range.ExportRange.from_node())

        if frames is None:
            self.data = None
            return True

        data = self.get_data(frames)

        if data is not None:
            self.data = data
            return True

        data = self.get_data([text.value() for text in self.texts])

        if data is not None:
            self.data = data
            return True

        return False

    def update_attr(self):
        ranges = [
            export_range.ExportRange(n, self.data[i], self.data[i + 1])
            for i, n in enumerate(self.names)
        ]

        export_range.ExportRange.to_node(ranges)

    def update_ui(self, enabled):
        for frame in self.frames:
            frame.setEnabled(enabled)

        for i, text in enumerate(self.texts):
            text.setValue(self.data[self.connections[i]] if enabled else 0)

    def update(self, init=False):
        if init:
            self.init()
        else:
            updated = self.update_data()
            if not updated:
                return

        if self.data is None:
            self.update_ui(False)
            return

        self.update_attr()
        self.update_ui(True)

    def set_current(self, target):
        target.setValue(cmds.currentTime(q=True))
        self.update()
