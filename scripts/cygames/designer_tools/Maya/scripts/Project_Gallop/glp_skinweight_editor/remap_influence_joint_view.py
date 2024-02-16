# -*- coding: utf-8 -*-
"""MVCでいうViewを担う
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

from maya.app.general import mayaMixin
from PySide2 import QtWidgets

from .ui import edit_joint_window
reload(edit_joint_window)


class RemapInfluenceJointView(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, parent=None):
        super(RemapInfluenceJointView, self).__init__(parent)
        self.ui = edit_joint_window.Ui_MainWindow()
        self.ui.setupUi(self)
        self.end_process = None

    def closeEvent(self, event):
        if self.end_process:
            try:
                self.end_process()

            # すでに親がけされている場合などにエラーが発生するため抑止
            except RuntimeError:
                pass

        super(self.__class__, self).closeEvent(event)
