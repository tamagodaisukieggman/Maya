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

from PySide2 import QtWidgets
from maya.app.general import mayaMixin

from .ui import normalEditorWindow
reload(normalEditorWindow)


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, *args, **kwargs):

        super(View, self).__init__(*args, **kwargs)
        self.ui = normalEditorWindow.Ui_GallopNormalEditorWin()
        self.ui.setupUi(self)
        self.save_func = None

    def closeEvent(self, e):

        if self.save_func:
            self.save_func()

        super(View, self).closeEvent(e)
