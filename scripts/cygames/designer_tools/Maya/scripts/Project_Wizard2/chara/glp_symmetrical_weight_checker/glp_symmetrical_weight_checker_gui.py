# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function


from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general import mayaMixin
import maya.api.OpenMaya as om
from . import glp_symmetrical_weight_checker_ui_pyside2


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class GUI(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUIの本体になるクラス

    このクラスをMayaウインドウの中に含んでいるかどうかでウインドウ重複の判定を行っているため、リロードしてはいけない
    mayaMixin.MayaQWidgetBaseMixinを第一引数に指定することで、Mayaのウインドウとして呼ぶことが出来る
    """

    # ===============================================
    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)

        self.titleName = 'GlpSymmetricalWeightChecker'
        self.ui = glp_symmetrical_weight_checker_ui_pyside2.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(self.titleName)
        self.callback_id_list = []

    # ===============================================
    def closeEvent(self, event):
        super(GUI, self).closeEvent(event)

        if self.callback_id_list:
            om.MMessage.removeCallbacks(self.callback_id_list)

        self.callback_id_list = []

    # ===============================================
    def addCallback(self, event_str, func):
        self.callback_id_list.append(om.MEventMessage.addEventCallback(event_str, func))
