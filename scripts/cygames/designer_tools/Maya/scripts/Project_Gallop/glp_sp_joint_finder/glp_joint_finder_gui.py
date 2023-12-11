# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets
from maya.app.general import mayaMixin
from . import glp_joint_finder_pyside2

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

reload(glp_joint_finder_pyside2)


class GUI(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)

        self.titleName = 'GlpJointFinder'
        self.ui = glp_joint_finder_pyside2.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(self.titleName)
