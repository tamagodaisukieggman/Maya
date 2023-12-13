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

import math
import maya.cmds as cmds

from ...base_common import utility as base_utility
from ..utility import model_id_finder as model_id_finder
from ..utility import model_define as model_define


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class UvFacialPart(object):
    """
    """

    # ===============================================
    def __init__(self):

        self.default_row_col = [0, 0]

        self.part_label = ''
        self.tex_row_count = 0
        self.tex_col_count = 0
        self.cgfx_row_height = 0
        self.cgfx_col_width = 0
        self.index_label_dict_list = []
        self.__is_update_success = False

        self.start_index = 0
        self.final_index = 0

        self.mesh = None

        # ------------------------------
        # update()で更新される系
        self.material = None
        self.file_node_list = None
        self.place2dTexture_node_list = None
        self.current_index = 0
        self.is_using_cgfx = False

    # ===============================================
    def create_info(self, label, target_mesh, row_count, col_count, index_label_dict_list):

        self.part_label = label
        self.tex_row_count = row_count
        self.tex_col_count = col_count
        self.cgfx_row_height = 1.0 / self.tex_row_count
        self.cgfx_col_width = 1.0 / self.tex_col_count
        self.index_label_dict_list = index_label_dict_list

        if self.tex_row_count * self.tex_col_count < len(self.index_label_dict_list):
            self.final_index = self.tex_row_count * self.tex_col_count - 1
        else:
            self.final_index = len(self.index_label_dict_list) - 1

        # ------------------------------
        # mesh
        if not cmds.objExists(target_mesh):
            return

        self.mesh = target_mesh

        self.update()

    # ===============================================
    def update(self):

        materials = base_utility.material.get_material_list(self.mesh)

        # ------------------------------
        # material
        if not materials:
            return

        self.material = materials[0]
        if self.material.find(model_define.CGFX_SUFFIX) >= 0:
            self.is_using_cgfx = True
        else:
            self.is_using_cgfx = False

        # ------------------------------
        # file_node
        file_nodes = cmds.listConnections(self.material, type='file')

        if not file_nodes:
            return

        self.file_node_list = list(set(file_nodes))

        # ------------------------------
        # place2dTexture_node
        place2dTexture_nodes = cmds.listConnections(self.file_node_list, type='place2dTexture')

        if not place2dTexture_nodes:
            return

        self.place2dTexture_node_list = list(set(place2dTexture_nodes))

        self.current_index = self.get_current_index()

        self.__is_update_success = True

    # ===============================================
    def apply_value(self, index):

        self.update()
        self.set_tex_coverage()
        self.adjust_uv_scale()

        if self.is_using_cgfx:
            # CGFXではテクスチャスクロールが効かない、UVを動かす
            self.set_translate_frame([0.0, 0.0])
            self.apply_uv_offset_by_index(index)

        else:
            # 通常はUVデフォルト位置でテクスチャスクロール
            self.apply_tex_coverage_by_index(index)

        # アウトラインを合わせる
        self.adjust_outline_uv_to_base()

    # ===============================================
    def apply_uv_offset_by_index(self, index):

        self.update()

        if index > self.final_index:
            return

        current_row_col = self.get_current_row_col()
        current_row = current_row_col[0]
        current_col = current_row_col[1]

        row_col_offset = self.__get_row_col_offset(self.current_index, index)
        row_offset = row_col_offset[0]
        col_offset = row_col_offset[1]

        final_row = current_row + row_offset
        final_col = current_col + col_offset
        final_row = final_row % self.tex_row_count
        final_col = final_col % self.tex_col_count

        self.set_uv_row_col([final_row, final_col])

        self.update()

    # ===============================================
    def apply_tex_coverage_by_index(self, index):

        self.update()

        if index > self.final_index:
            return

        if not self.place2dTexture_node_list:
            return

        trans_frame_u = (self.tex_col_count - index) % self.tex_col_count
        trans_frame_v = index // self.tex_col_count

        self.set_translate_frame([trans_frame_u, trans_frame_v])

        self.update()

    # ===============================================
    def get_current_translate_frame(self):

        if not self.place2dTexture_node_list:
            return [0, 0]

        translate_frame_u = cmds.getAttr('{}.translateFrameU'.format(self.place2dTexture_node_list[0]))
        translate_frame_v = cmds.getAttr('{}.translateFrameV'.format(self.place2dTexture_node_list[0]))

        return [translate_frame_u, translate_frame_v]

    # ===============================================
    def set_translate_frame(self, trans_frame_uv):

        self.update()

        for place2dTexture_node in self.place2dTexture_node_list:

            if not cmds.objExists(place2dTexture_node):
                continue

            cmds.setAttr('{}.translateFrameU'.format(place2dTexture_node), trans_frame_uv[0])
            cmds.setAttr('{}.translateFrameV'.format(place2dTexture_node), trans_frame_uv[1])

    # ===============================================
    def set_uv_row_col(self, target_row_col):

        self.update()

        uv_list = cmds.polyListComponentConversion(self.mesh, tuv=True)
        uv_list = cmds.ls(uv_list, fl=True, l=True)

        if not uv_list:
            return

        current_row_col = self.get_current_row_col()

        row_offset = target_row_col[0] - current_row_col[0]
        col_offset = target_row_col[1] - current_row_col[1]

        u_offset_value = col_offset * self.cgfx_col_width
        v_offset_value = -1 * row_offset * self.cgfx_row_height

        cmds.polyEditUV(uv_list, u=u_offset_value, v=v_offset_value)

    # ===============================================
    def get_current_row_col(self):

        if not self.mesh:
            return [0, 0]

        uv_list = self.__get_uv_list(self.mesh)
        uv_pos = self.__get_uv_avarage_pos(uv_list)
        row_col = self.__get_row_col_from_uv(uv_pos)

        return row_col

    # ===============================================
    def get_current_index(self):

        result_index = 0

        if self.is_using_cgfx:

            current_row_col = self.get_current_row_col()

            result_index = int(current_row_col[0] * self.tex_col_count + current_row_col[1])

        else:

            current_frans_frame = self.get_current_translate_frame()

            result_index = int(
                current_frans_frame[1] * self.tex_col_count + (self.tex_col_count - current_frans_frame[0]) % self.tex_col_count)

        return result_index

    # ===============================================
    def set_tex_coverage(self):

        self.update()

        coverage_uv_list = [self.tex_col_count, self.tex_row_count]

        if self.is_using_cgfx:
            coverage_uv_list = [1, 1]

        for place2dTexture_node in self.place2dTexture_node_list:

            if not cmds.objExists(place2dTexture_node):
                continue

            cmds.setAttr('{}.coverageU'.format(place2dTexture_node), coverage_uv_list[0])
            cmds.setAttr('{}.coverageV'.format(place2dTexture_node), coverage_uv_list[1])

    # ===============================================
    def adjust_uv_scale(self):

        self.update()

        uv_list = self.__get_uv_list(self.mesh)
        uv_bounds = self.__get_uv_bounds(uv_list)
        u_length = uv_bounds[0] - uv_bounds[1]
        v_length = uv_bounds[2] - uv_bounds[3]

        if self.is_using_cgfx:

            if u_length < self.cgfx_col_width or v_length < self.cgfx_row_height:
                return

            cmds.polyEditUV(uv_list, pivotU=0.0, pivotV=1.0, scaleU=1/self.tex_col_count, scaleV=1/self.tex_row_count)

        else:

            if u_length > self.cgfx_col_width or v_length > self.cgfx_row_height:
                return

            self.set_uv_row_col(self.default_row_col)
            cmds.polyEditUV(uv_list, pivotU=0.0, pivotV=1.0, scaleU=self.tex_col_count, scaleV=self.tex_row_count)

    # ===============================================
    def adjust_outline_uv_to_base(self):

        if not cmds.objExists(self.mesh):
            return

        base_uv_list = self.__get_uv_list(self.mesh)
        outline_uv_list = self.__get_uv_list(self.mesh + model_define.OUTLINE_SUFFIX)

        self.__adjust_outline_uv_to_base_calc(outline_uv_list, base_uv_list)

    # ===============================================
    def __adjust_outline_uv_to_base_calc(self, outline_uv_list, base_uv_list):

        if not outline_uv_list or not base_uv_list:
            return

        outline_uv_bounds = self.__get_uv_bounds(outline_uv_list)
        base_uv_bounds = self.__get_uv_bounds(base_uv_list)

        outline_u_length = outline_uv_bounds[0] - outline_uv_bounds[1]
        outline_v_length = outline_uv_bounds[2] - outline_uv_bounds[3]

        base_u_length = base_uv_bounds[0] - base_uv_bounds[1]
        base_v_length = base_uv_bounds[0] - base_uv_bounds[1]

        adjust_u_scale = base_u_length / outline_u_length
        adjust_v_scale = base_v_length / outline_v_length

        outline_uv_center_pos = [
            outline_uv_bounds[1] + (outline_u_length / 2),
            outline_uv_bounds[3] + (outline_v_length / 2),
        ]

        base_uv_center_pos = [
            base_uv_bounds[1] + (base_u_length / 2),
            base_uv_bounds[3] + (base_v_length / 2),
        ]

        relative_base_pos = [
            base_uv_center_pos[0] - outline_uv_center_pos[0],
            base_uv_center_pos[1] - outline_uv_center_pos[1],
        ]

        cmds.polyEditUV(
            outline_uv_list,
            pivotU=outline_uv_center_pos[0],
            pivotV=outline_uv_center_pos[1],
            scaleU=adjust_u_scale,
            scaleV=adjust_v_scale
        )

        cmds.polyEditUV(
            outline_uv_list,
            r=True,
            u=relative_base_pos[0],
            v=relative_base_pos[1],
        )

    # ===============================================
    def __get_row_col_offset(self, from_index, to_index):

        target_tex_row = to_index // self.tex_col_count
        target_tex_col = to_index % self.tex_col_count

        current_tex_row = from_index // self.tex_col_count
        current_tex_col = from_index % self.tex_col_count

        row_offset = target_tex_row - current_tex_row
        col_offset = target_tex_col - current_tex_col

        return [row_offset, col_offset]

    # ===============================================
    def __get_row_col_from_uv(self, uv_pos):

        u_pos = uv_pos[0]
        v_pos = uv_pos[1]

        this_row = int(math.floor((1.0 - v_pos) / self.cgfx_row_height))
        this_col = int(math.floor(u_pos / self.cgfx_col_width))

        return [this_row, this_col]

    # ===============================================
    def __get_uv_list(self, mesh):

        if not cmds.objExists(mesh):
            return []

        uv_list = cmds.polyListComponentConversion(mesh, tuv=True)
        uv_list = cmds.ls(uv_list, fl=True, l=True)

        return uv_list

    # ===============================================
    def __get_uv_avarage_pos(self, uv_list):

        uv_avarage_pos = [0.0, 0.0]
        uv_count = 0

        if not uv_list:
            return uv_avarage_pos

        for uv_item in uv_list:
            this_uv = cmds.polyEditUV(uv_item, q=True)
            uv_avarage_pos[0] += this_uv[0]
            uv_avarage_pos[1] += this_uv[1]
            uv_count += 1

        uv_avarage_pos[0] = uv_avarage_pos[0] / uv_count
        uv_avarage_pos[1] = uv_avarage_pos[1] / uv_count

        return uv_avarage_pos

    # ===============================================
    def __get_uv_bounds(self, uv_list):

        u_list = []
        v_list = []

        if not uv_list:
            return [0, 0, 0, 0]

        for uv_item in uv_list:
            this_uv = cmds.polyEditUV(uv_item, q=True)
            u_list.append(this_uv[0])
            v_list.append(this_uv[1])

        u_max = max(u_list)
        u_min = min(u_list)
        v_max = max(v_list)
        v_min = min(v_list)

        return [u_max, u_min, v_max, v_min]
