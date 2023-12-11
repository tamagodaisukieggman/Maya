# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets
from maya.app.general import mayaMixin

from .ui import scene_cleanup_window

# maya 2022-
try:
    from importlib import reload
except Exception:
    pass

reload(scene_cleanup_window)


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI生成

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, *args, **kwargs):

        super(View, self).__init__(*args, **kwargs)
        self.ui = scene_cleanup_window.Ui_MainWindow()
        self.ui.setupUi(self)
