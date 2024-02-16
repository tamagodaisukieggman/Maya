# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets
from maya.app.general import mayaMixin

from .ui import glp_create_union_model, path_list_dialog

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

reload(glp_create_union_model)
reload(path_list_dialog)


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, parent=None):

        super(View, self).__init__(parent)
        self.ui = glp_create_union_model.Ui_MainWindow()
        self.ui.setupUi(self)


class PathListDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):

        super(PathListDialog, self).__init__(parent)
        self.ui = path_list_dialog.Ui_Dialog()
        self.ui.setupUi(self)

    def accept(self):
        return super(PathListDialog, self).accept()

    def reject(self):
        return super(PathListDialog, self).reject()
