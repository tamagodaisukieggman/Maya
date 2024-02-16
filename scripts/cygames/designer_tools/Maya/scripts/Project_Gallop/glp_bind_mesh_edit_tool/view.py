# -*- coding: utf-8 -*-
"""MVCでいうViewを担う
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets
from maya.app.general import mayaMixin

from .ui import bind_mesh_edit_window

try:
    from importlib import reload
except Exception:
    pass

reload(bind_mesh_edit_window)


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, *args, **kwargs):

        super(View, self).__init__(*args, **kwargs)
        self.ui = bind_mesh_edit_window.Ui_MainWindow()
        self.ui.setupUi(self)
