# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import maya.cmds as cmds
from PySide2 import QtCore, QtGui, QtWidgets
from maya import OpenMayaUI
from maya.app.general import mayaMixin
from . import glp_arrange_vtx_order_ui_pyside2


class GUI(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)

        self.GEO_OPTION_VAR = 'GlpArrangeVtxOrderGeoVar'

        self.titleName = 'GlpArrangeVtxOrder'
        self.ui = glp_arrange_vtx_order_ui_pyside2.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(self.titleName)

        # サイズの復元
        if cmds.optionVar(ex=self.GEO_OPTION_VAR):
            geo_str = cmds.optionVar(q=self.GEO_OPTION_VAR)
            geo_list = geo_str.split(',')
            self.setGeometry(int(geo_list[0]), int(geo_list[1]), int(geo_list[2]), int(geo_list[3]))

    def closeEvent(self, event):
        geo = self.geometry()
        geo_str = ','.join([str(geo.left()), str(geo.top()), str(geo.width()), str(geo.height())])
        cmds.optionVar(sv=[self.GEO_OPTION_VAR, str(geo_str)])
        super(GUI, self).closeEvent(event)