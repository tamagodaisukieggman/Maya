# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import os

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

TOOL_NAME = "Prop_Offset_Tool"
UI_PATH = os.path.dirname(__file__) + "/ui"


class View(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        loader = QUiLoader()
        uiFilePath = os.path.join(UI_PATH, "prop_offset_tools_main.ui")
        self.gui = loader.load(uiFilePath)
        self.setCentralWidget(self.gui)
        self.setWindowTitle(TOOL_NAME)
        self.setObjectName(TOOL_NAME)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
