# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except:
    pass

import os

import maya.cmds as cmds
import maya.mel as mel

from ....base_common import utility as base_utility
from ....priari_common.utility import model_define


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TransferNormal(object):

    # ===============================================
    def __init__(self):

        self.template_path = model_define.SVN_PATH + '/common/normal_template/bakeNormalTemplate.ma'
        self.template_mesh_suffix = '_normal_template'
        self.tmplate_name_space = '__normal_tmp__'

        self.adjust_ref_node_name = 'C_head'
        self.adjust_offset = [0, 0, 0]

        self.src_dst_mesh_pair_list = None

        self.is_ready = False

    # ===============================================
    def initialize(self, mesh_list):

        self.src_dst_mesh_pair_list = []

        # メッシュ合わせのオフセットを取得
        adjust_ref_list = cmds.ls(self.adjust_ref_node_name, l=True)
        if adjust_ref_list:
            adjust_ref_node = adjust_ref_list[0]
            self.adjust_offset = cmds.xform(adjust_ref_node, q=True, ws=True, t=True)

        for mesh in mesh_list:

            if not cmds.objExists(mesh):
                continue

            src_mesh_name = '{0}:{1}{2}'.format(self.tmplate_name_space, mesh.split('|')[-1], self.template_mesh_suffix)

            self.src_dst_mesh_pair_list.append([src_mesh_name, mesh])

        if not self.src_dst_mesh_pair_list:
            return

        if not os.path.exists(self.template_path):
            return

        self.is_ready = True

    # ===============================================
    def import_template_mesh(self):

        selection = cmds.ls(sl=True, l=True, et='transform')

        if not selection:
            return

        self.initialize(selection)

        if not self.is_ready:
            return

        self._load_reference()

        for src_dst_mesh in self.src_dst_mesh_pair_list:

            src_template_mesh = src_dst_mesh[0]

            if cmds.objExists(src_template_mesh):
                dup_obj_list = cmds.duplicate(src_template_mesh)
                cmds.xform(dup_obj_list, r=True, t=self.adjust_offset)

        self._unload_reference()

    # ===============================================
    def tarnsfer_normal(self):

        selection = cmds.ls(sl=True, l=True, et='transform')

        if not selection:
            return

        self.initialize(selection)

        if not self.is_ready:
            return

        self._load_reference()

        for src_dst_mesh in self.src_dst_mesh_pair_list:

            src_template_mesh = src_dst_mesh[0]
            dst_original_mesh = src_dst_mesh[1]

            if cmds.objExists(src_template_mesh):
                cmds.xform(src_template_mesh, r=True, t=self.adjust_offset)
                cmds.transferAttributes(src_template_mesh, dst_original_mesh, pos=0, nml=1, uvs=0, col=0, spa=0, sm=3, fuv=0, clb=0)

                cmds.delete(dst_original_mesh, ch=True)

                cmds.select(dst_original_mesh)
                mel.eval('ToggleDisplayColorsAttr')

        self._unload_reference()

    # ===============================================
    def _load_reference(self):

        if base_utility.reference.exists(self.template_path, self.tmplate_name_space):
            return

        base_utility.reference.load(self.template_path, self.tmplate_name_space)

    # ===============================================
    def _unload_reference(self):

        if not base_utility.reference.exists(self.template_path, self.tmplate_name_space):
            return

        base_utility.reference.unload(self.template_path, self.tmplate_name_space)
