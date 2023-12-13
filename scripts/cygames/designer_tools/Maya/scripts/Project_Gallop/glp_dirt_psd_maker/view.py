# -*- coding: utf-8 -*-
"""MVCでいうViewを担う
"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general import mayaMixin

from .ui import dirtPSDMakerWindow


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, *args, **kwargs):

        super(View, self).__init__(*args, **kwargs)
        self.ui = dirtPSDMakerWindow.Ui_MainWindow()
        self.ui.setupUi(self)
