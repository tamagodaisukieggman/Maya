# -*- coding: utf-8 -*-
"""MVCでいうViewを担う
"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import os
from PySide2 import QtWidgets
from maya.app.general import mayaMixin

from PySide2.QtUiTools import QUiLoader

g_tool_name = 'CharaNormalTools'
CURRENT_PATH = os.path.dirname(__file__)

class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, *args, **kwargs):

        super(View, self).__init__(*args, **kwargs)
        loader = QUiLoader()
        uiFilePath = os.path.join(CURRENT_PATH, 'ui/normalEditorWindow.ui')
        self.ui = loader.load(uiFilePath)  # QMainWindow
        self.setCentralWidget(self.ui)
        self.setWindowTitle(g_tool_name)
        self.setObjectName(g_tool_name)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

    def closeEvent(self, e):

        if self.save_func:
            self.save_func()

        super(View, self).closeEvent(e)
