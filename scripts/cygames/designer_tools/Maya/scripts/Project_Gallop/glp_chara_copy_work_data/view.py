# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets, QtGui
from maya.app.general import mayaMixin

from .ui import glp_copy_work_data_gui
from . import utility

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

reload(glp_copy_work_data_gui)


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, root, parent=None):
        super(View, self).__init__(parent)

        self.root = root
        self.ui = glp_copy_work_data_gui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.src_icon_label.setPixmap(QtGui.QPixmap(utility.get_icon_path('folder.png')))
        self.ui.dst_icon_label.setPixmap(QtGui.QPixmap(utility.get_icon_path('folder.png')))
        self.ui.replace_icon_label.setPixmap(QtGui.QPixmap(utility.get_icon_path('replace.png')))
        self.ui.copy_icon_label.setPixmap(QtGui.QPixmap(utility.get_icon_path('copy.png')))

        self.ui.table_refresh_button.setIcon(QtGui.QPixmap(utility.get_icon_path('reload.png')))
