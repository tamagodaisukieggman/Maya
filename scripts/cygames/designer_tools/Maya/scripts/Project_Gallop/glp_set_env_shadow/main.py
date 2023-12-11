# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import sys
import shiboken2
from PySide2 import QtWidgets

import maya.cmds as cmds
from maya import OpenMayaUI

from ..base_common import utility as base_utility
from . import glp_set_env_shadow_gui
from . import glp_set_env_shadow

try:
    # Maya2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(glp_set_env_shadow)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ===============================================
    def __init__(self):

        self.main_window = glp_set_env_shadow_gui.GUI()

    # ===============================================
    def show_ui(self):
        '''UIの呼び出し
        '''

        self.deleteOverlappingWindow(self.main_window)
        self.__setup_view_event()
        self.main_window.show()

    # ===============================================
    def deleteOverlappingWindow(self, target):
        '''Windowの重複削除処理
        '''

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # Maya2022-
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.close()
                widget.deleteLater()

    # ===============================================
    def __setup_view_event(self):

        self.main_window.ui.pushButton.clicked.connect(self.__set_env_shadow)
        self.main_window.ui.pushButton_2.clicked.connect(self.__set_default)

    # ===============================================
    def __set_env_shadow(self, arg=None):

        target_material = self.__get_lambert_list()

        for material in target_material:
            glp_set_env_shadow.set_env_shadow(material)

    # ===============================================
    def __set_default(self, arg=None):

        target_material = self.__get_lambert_list()

        for material in target_material:
            glp_set_env_shadow.set_default_lambert(material)

    # ===============================================
    def __get_lambert_list(self):

        material_list = []
        sel_list = cmds.ls(sl=True)

        if not sel_list:
            return material_list

        for selection in sel_list:

            if cmds.objectType(selection) == 'lambert':
                material_list.append(selection)

            if cmds.objectType(selection) == 'transform':
                tmp_material_list = base_utility.material.get_material_list(selection)

                if not tmp_material_list:
                    continue

                for material in tmp_material_list:
                    if cmds.objectType(material) == 'lambert':
                        material_list.append(material)

        return material_list
