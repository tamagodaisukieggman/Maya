# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
except Exception:
    pass

import maya.cmds as cmds
from PySide2 import QtCore, QtGui, QtWidgets
from maya import OpenMayaUI
from maya.app.general import mayaMixin
from . import glp_compress_playblast_pyside2


class GUI(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)

        self.GEO_OPTION_VAR = 'GlpCompressPlayblastGeoVar'

        self.titleName = 'GlpCompressPlayblast'
        self.ui = glp_compress_playblast_pyside2.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(self.titleName)

        # UIにジョブを紐づけているので同名のウインドウが複数存在するのを避ける
        objcet_name = 'GlpCompressPlayblastMainWindow'
        if OpenMayaUI.MQtUtil.findControl(objcet_name):
            self.setObjectName(objcet_name + '__')
        else:
            self.setObjectName(objcet_name)

        # サイズの復元
        if cmds.optionVar(ex=self.GEO_OPTION_VAR):
            geo_str = cmds.optionVar(q=self.GEO_OPTION_VAR)
            geo_list = geo_str.split(',')
            self.setGeometry(int(geo_list[0]), int(geo_list[1]), int(geo_list[2]), int(geo_list[3]))

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def closeEvent(self, event):
        geo = self.geometry()
        geo_str = ','.join([str(geo.left()), str(geo.top()), str(geo.width()), str(geo.height())])
        cmds.optionVar(sv=[self.GEO_OPTION_VAR, str(geo_str)])
        super(GUI, self).closeEvent(event)