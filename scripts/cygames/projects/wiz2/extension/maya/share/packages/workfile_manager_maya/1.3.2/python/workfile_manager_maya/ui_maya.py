# -*- coding: utf-8 -*-

import sys
import os
import re

from Qt import QtCore,QtWidgets


from maya.app.general import mayaMixin


from workfile_manager_maya import assetutils_maya

from workfile_manager.ui import ui_main, uiutils

class MainWindow(mayaMixin.MayaQWidgetBaseMixin, ui_main.MainWindow):
    def dccutils(self):
        return assetutils_maya.MayaUtils
    def parent_func(self, w):
        w.setParent(ui_main.mwin, QtCore.Qt.Window)

def show():
    try:
        #ui_main.mwin.close_without_save_settings()
        ui_main.mwin.close()
    except:
        pass
    ui_main.mwin = MainWindow(toolgroup='Default', toolname='workfile_manager')
    ui_main.mwin.setStyleSheet('QWidget {font-size:14px}')
    
    try:
        if ui_main.mwin.ui_prefs.var['miscellaneous']['display-app-specific-colorbar'] == True:
            ui_main.mwin.add_application_name_bar("Maya",[127,183,188])
    except:
        pass

    ui_main.mwin.show_()
    
    
