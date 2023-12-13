# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import maya.api.OpenMaya as om

from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general import mayaMixin

from .ui import glp_eye_cover_tool_ui_pyside2


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, *args, **kwargs):

        super(View, self).__init__(*args, **kwargs)
        self.ui = glp_eye_cover_tool_ui_pyside2.Ui_MainWindow()
        self.ui.setupUi(self)
        self.callback = None
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理
        
        callbackを破棄
        """

        if self.callback:
            om.MMessage.removeCallback(self.callback)
            print('delete:{}'.format(self.callback))

    def connectCallback(self, func):
        """callback作成
        """

        #callback作成
        self.callback = om.MEventMessage.addEventCallback('SelectionChanged', func)
        print('create:{}'.format(self.callback))
