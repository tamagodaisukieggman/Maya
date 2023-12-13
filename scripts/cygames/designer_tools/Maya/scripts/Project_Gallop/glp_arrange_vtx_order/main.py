# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import sys

import maya.cmds as cmds
from maya import OpenMayaUI

import shiboken2
from PySide2 import QtWidgets
from . import glp_arrange_vtx_order_gui
from . import glp_arrange_vtx_order

reload(glp_arrange_vtx_order)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main:

    # ===============================================
    def __init__(self):

        self.MESH_PRESET_LIST = [
            'スカート外側',
            'スカート内側',
            '右そで外側',
            '右そで内側',
            '左そで外側',
            '左そで内側',
        ]

        self.OREDERED_BY_LIST = [
            '位置が近い順',
            'UVが近い順',
        ]

        self.main_window = glp_arrange_vtx_order_gui.GUI()
        self.arrenger = glp_arrange_vtx_order.GlpArrangeVtxOrder()

        self.foward_direction = [0, 0, 0]
        self.mesh_direction = [0, 0, 0]
        self.mesh_unite_direction = [0, 0, 0]
        self.order_source = None
        self.is_ready = False

    # ===============================================
    def show_ui(self):
        '''UIの呼び出し
        '''

        self.deleteOverlappingWindow(self.main_window)
        self.__setup_view_event()
        self.main_window.show()

        self.__initialize_ui()

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
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if type(target) == type(widget):
                widget.close()
                widget.deleteLater()

    # ===============================================
    def __setup_view_event(self):

        for preset in self.MESH_PRESET_LIST:
            self.main_window.ui.mesh_preset.addItem(preset)
        for preset in self.OREDERED_BY_LIST:
            self.main_window.ui.ordered_by.addItem(preset)

        self.main_window.ui.mesh_preset.currentIndexChanged.connect(self.__change_mesh_preset_event)
        self.main_window.ui.ordered_by.currentIndexChanged.connect(self.__change_ordered_by_event)

        self.main_window.ui.foward_x.textChanged.connect(self.__check_input)
        self.main_window.ui.foward_y.textChanged.connect(self.__check_input)
        self.main_window.ui.foward_z.textChanged.connect(self.__check_input)
        self.main_window.ui.mesh_direction_x.textChanged.connect(self.__check_input)
        self.main_window.ui.mesh_direction_y.textChanged.connect(self.__check_input)
        self.main_window.ui.mesh_direction_z.textChanged.connect(self.__check_input)
        self.main_window.ui.unite_direction_x.textChanged.connect(self.__check_input)
        self.main_window.ui.unite_direction_y.textChanged.connect(self.__check_input)
        self.main_window.ui.unite_direction_z.textChanged.connect(self.__check_input)

        self.main_window.ui.auto_button.clicked.connect(self.__auto_button_event)
        self.main_window.ui.create_reorder_mesh.clicked.connect(self.__create_reorder_mesh_event)
        self.main_window.ui.create_reorder_meshes.clicked.connect(self.__create_reorder_meshs_event)
        self.main_window.ui.combine_meshes.clicked.connect(self.__combine_meshes_event)

    # ===============================================
    def __initialize_ui(self, arg=None):

        self.main_window.ui.mesh_preset.setCurrentIndex(0)
        self.main_window.ui.ordered_by.setCurrentIndex(0)
        self.__change_mesh_preset_event()
        self.__change_ordered_by_event()
        self.__check_input()

    # ===============================================
    def __change_mesh_preset_event(self, arg=None):

        current_index = self.main_window.ui.mesh_preset.currentIndex()
        current_text = self.main_window.ui.mesh_preset.itemText(current_index)

        foward_direction = [0, 0, 1]
        mesh_direction = [0, -1, 0]
        mesh_unite_direction = [0, 0, -1]

        if current_text == self.MESH_PRESET_LIST[0]:
            foward_direction = [0, 0, 1]
            mesh_direction = [0, -1, 0]
            mesh_unite_direction = [0, 0, -1]
        elif current_text == self.MESH_PRESET_LIST[1]:
            foward_direction = [0, 0, 1]
            mesh_direction = [0, -1, 0]
            mesh_unite_direction = [0, 0, 1]
        elif current_text == self.MESH_PRESET_LIST[2]:
            foward_direction = [0, 0, 1]
            mesh_direction = [1, 0, 0]
            mesh_unite_direction = [0, 0, -1]
        elif current_text == self.MESH_PRESET_LIST[3]:
            foward_direction = [0, 0, 1]
            mesh_direction = [1, 0, 0]
            mesh_unite_direction = [0, 0, 1]
        elif current_text == self.MESH_PRESET_LIST[4]:
            foward_direction = [0, 0, 1]
            mesh_direction = [-1, 0, 0]
            mesh_unite_direction = [0, 0, -1]
        elif current_text == self.MESH_PRESET_LIST[5]:
            foward_direction = [0, 0, 1]
            mesh_direction = [-1, 0, 0]
            mesh_unite_direction = [0, 0, 1]

        self.main_window.ui.foward_x.setText(str(foward_direction[0]))
        self.main_window.ui.foward_y.setText(str(foward_direction[1]))
        self.main_window.ui.foward_z.setText(str(foward_direction[2]))
        self.main_window.ui.mesh_direction_x.setText(str(mesh_direction[0]))
        self.main_window.ui.mesh_direction_y.setText(str(mesh_direction[1]))
        self.main_window.ui.mesh_direction_z.setText(str(mesh_direction[2]))
        self.main_window.ui.unite_direction_x.setText(str(mesh_unite_direction[0]))
        self.main_window.ui.unite_direction_y.setText(str(mesh_unite_direction[1]))
        self.main_window.ui.unite_direction_z.setText(str(mesh_unite_direction[2]))

        self.__check_input()

    # ===============================================
    def __change_ordered_by_event(self, arg=None):

        current_index = self.main_window.ui.ordered_by.currentIndex()
        current_text = self.main_window.ui.ordered_by.itemText(current_index)

        if current_text == self.OREDERED_BY_LIST[0]:
            self.order_source = 'pos'
        elif current_text == self.OREDERED_BY_LIST[1]:
            self.order_source = 'uv'

        self.__check_input()

    # ===============================================
    def __check_input(self, arg=None):

        self.is_ready = False

        foward_x = self.main_window.ui.foward_x.text()
        foward_y = self.main_window.ui.foward_y.text()
        foward_z = self.main_window.ui.foward_z.text()
        mesh_direction_x = self.main_window.ui.mesh_direction_x.text()
        mesh_direction_y = self.main_window.ui.mesh_direction_y.text()
        mesh_direction_z = self.main_window.ui.mesh_direction_z.text()
        unite_direction_x = self.main_window.ui.unite_direction_x.text()
        unite_direction_y = self.main_window.ui.unite_direction_y.text()
        unite_direction_z = self.main_window.ui.unite_direction_z.text()

        try:
            self.foward_direction = [int(foward_x), int(foward_y), int(foward_z)]
            self.mesh_direction = [int(mesh_direction_x), int(mesh_direction_y), int(mesh_direction_z)]
            self.mesh_unite_direction = [int(unite_direction_x), int(unite_direction_y), int(unite_direction_z)]
        except Exception as e:
            return

        if self.foward_direction[0] == self.foward_direction[1] == self.foward_direction[2] == 0:
            return
        if self.mesh_direction[0] == self.mesh_direction[1] == self.mesh_direction[2] == 0:
            return
        if self.mesh_unite_direction[0] == self.mesh_unite_direction[1] == self.mesh_unite_direction[2] == 0:
            return

        if not self.order_source == 'pos' and not self.order_source == 'uv':
            return

        self.is_ready = True

    # ===============================================
    def __auto_button_event(self, arg=None):

        self.__check_input()
        if not self.is_ready:
            return

        select_list = cmds.ls(sl=True, fl=True, l=True)

        if not select_list:
            return

        org_obj = select_list[0].split('.')[0]
        dup_obj_name = org_obj.split('|')[-1] + '_reoder_vtx'
        dup_obj = cmds.duplicate(org_obj, n=dup_obj_name)[0]
        select_face_list = cmds.ls(cmds.polyListComponentConversion(select_list, tf=True), fl=True, l=True)

        if not select_face_list:
            return

        self.arrenger.foward_direction = self.foward_direction
        self.arrenger.mesh_direction = self.mesh_direction
        self.arrenger.mesh_unite_direction = self.mesh_unite_direction

        target_face_list = [face.replace(org_obj, dup_obj) for face in select_face_list]
        face_chain_list = self.arrenger.get_face_chain_list(target_face_list)
        mesh_list = self.arrenger.separate_mesh(dup_obj, face_chain_list)

        self.arrenger.reorder_vtx(mesh_list)
        result_mesh = self.arrenger.unite_mesh(mesh_list, self.order_source)
        cmds.rename(result_mesh, dup_obj_name)

    # ===============================================
    def __create_reorder_mesh_event(self, arg=None):

        self.__check_input()
        if not self.is_ready:
            return

        select_list = cmds.ls(sl=True, fl=True, l=True)

        if not select_list:
            return

        select_face_list = cmds.ls(cmds.polyListComponentConversion(select_list, tf=True), fl=True, l=True)

        if not select_face_list:
            return

        self.arrenger.foward_direction = self.foward_direction
        self.arrenger.mesh_direction = self.mesh_direction
        self.arrenger.mesh_unite_direction = self.mesh_unite_direction

        obj = select_face_list[0].split('.')[0]
        mesh_list = self.arrenger.separate_mesh(obj, [select_face_list])
        self.arrenger.reorder_vtx(mesh_list)

    # ===============================================
    def __create_reorder_meshs_event(self, arg=None):

        self.__check_input()
        if not self.is_ready:
            return

        select_list = cmds.ls(sl=True, fl=True, l=True)

        if not select_list:
            return

        obj = select_list[0].split('.')[0]
        select_face_list = cmds.ls(cmds.polyListComponentConversion(select_list, tf=True), fl=True, l=True)

        if not select_face_list:
            return

        self.arrenger.foward_direction = self.foward_direction
        self.arrenger.mesh_direction = self.mesh_direction
        self.arrenger.mesh_unite_direction = self.mesh_unite_direction

        face_chain_list = self.arrenger.get_face_chain_list(select_face_list)
        mesh_list = self.arrenger.separate_mesh(obj, face_chain_list)

        self.arrenger.reorder_vtx(mesh_list)

    # ===============================================
    def __combine_meshes_event(self, arg=None):

        mesh_list = cmds.ls(sl=True, l=True)

        result = cmds.polyUnite(mesh_list, op=True)

        if not result:
            return

        unite_mesh = result[0]
        vtx_list = cmds.ls(cmds.polyListComponentConversion(unite_mesh, tv=True), l=True, fl=True)
        cmds.polyMergeVertex(vtx_list, d=0.0001)

        uv_list = cmds.ls(cmds.polyListComponentConversion(unite_mesh, tuv=True), l=True, fl=True)
        cmds.polyMergeUV(uv_list, d=0.0001)

        cmds.delete(unite_mesh, ch=True)


