from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

import maya.api.OpenMaya as om

from ..utility import common as utility_common
from ..utility import attribute as utility_attribute
from ..utility import uvset as utility_uvset
from ..utility import colorset as utility_colorset
from ..utility import material as utility_material
from ..utility import node as utility_node
from ..utility import value as utility_value
from ..utility import vector as utility_vector

from . import param_item_group

from . import bake_group_param_list as gp
from . import bake_override_param_list as ovp
from . import bake_object_param_list as obp
from . import bake_common_param_list as cp

reload(utility_value)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Method(object):

    # ===========================================
    @staticmethod
    def set_colorset(target_transform, bake_group, colorset_type):

        colorset_name = None
        default_color = [0, 0, 0, 1]

        if colorset_type == cp.colorset_common_multiply:
            colorset_name = bake_group.common_colorset_multi_name
            default_color = [1, 1, 1, 1]

        elif colorset_type == cp.colorset_common_add:
            colorset_name = bake_group.common_colorset_add_name
            default_color = [0, 0, 0, 1]

        elif colorset_type == cp.colorset_common_overlay:
            colorset_name = bake_group.common_colorset_overlay_name
            default_color = [0.5, 0.5, 0.5, 1]

        elif colorset_type == cp.colorset_common_alpha:
            colorset_name = bake_group.common_colorset_alpha_name
            default_color = [0.5, 0.5, 0.5, 1]

        elif colorset_type == cp.colorset_common_gray:
            colorset_name = bake_group.common_colorset_gray_name
            default_color = [0.5, 0.5, 0.5, 1]

        elif colorset_type == cp.colorset_multiply:
            colorset_name = bake_group.colorset_multi_name
            default_color = [1, 1, 1, 1]

        elif colorset_type == cp.colorset_add:
            colorset_name = bake_group.colorset_add_name
            default_color = [0, 0, 0, 1]

        elif colorset_type == cp.colorset_overlay:
            colorset_name = bake_group.colorset_overlay_name
            default_color = [0.5, 0.5, 0.5, 1]

        elif colorset_type == cp.colorset_result:
            colorset_name = bake_group.colorset_result_name
            default_color = [0.5, 0.5, 0.5, 1]

        if colorset_name is None:
            return

        if utility_colorset.Method.exist_colorset(
                target_transform, colorset_name):
            utility_colorset.Method.set_current_colorset(
                target_transform, colorset_name)
            return

        utility_colorset.Method.create_new_colorset(
            target_transform, colorset_name, default_color)
        utility_colorset.Method.set_current_colorset(
            target_transform, colorset_name)

    # ===========================================
    @staticmethod
    def assign_base_material(target_transform, bake_group):

        material_list = \
            utility_common.NodeMethod.get_material_list(target_transform)

        if material_list is None:
            return

        if len(material_list) == 0:
            return

        if len(material_list) == 1:

            replace_mat_name = \
                bake_group.get_base_material(material_list[0])

            if replace_mat_name is None:
                return

            if not cmds.objExists(replace_mat_name):
                return

            if material_list[0] == replace_mat_name:
                return

            utility_material.Method.assign_material(
                replace_mat_name, [target_transform])

            return

        for this_mat in material_list:

            replace_mat_name = \
                bake_group.get_base_material(this_mat)

            if replace_mat_name is None:
                return

            if not cmds.objExists(replace_mat_name):
                continue

            if this_mat == replace_mat_name:
                continue

            target_node_list = \
                utility_material.Method.get_node_list_with_material(
                    this_mat, [target_transform])

            utility_material.Method.assign_material(
                replace_mat_name, target_node_list
            )

    # ===========================================
    @staticmethod
    def assign_bake_material(target_transform, bake_group):

        if bake_group.group_root.param_item_group.get_attr("BakeVertexColor"):
            return

        material_list = \
            utility_common.NodeMethod.get_material_list(target_transform)

        if material_list is None:
            return

        if len(material_list) == 0:
            return

        if len(material_list) == 1:

            replace_mat_name = bake_group.get_bake_material_name(material_list[0])

            if not cmds.objExists(replace_mat_name):
                return

            if material_list[0] == replace_mat_name:
                return

            utility_material.Method.assign_material(
                replace_mat_name, [target_transform])

            return

        for this_mat in material_list:

            replace_mat_name = \
                bake_group.get_bake_material_name(this_mat)

            if not cmds.objExists(replace_mat_name):
                return

            if this_mat == replace_mat_name:
                continue

            target_node_list = \
                utility_material.Method.get_node_list_with_material(
                    this_mat, [target_transform])

            utility_material.Method.assign_material(
                replace_mat_name, target_node_list
            )

    # ===========================================
    @staticmethod
    def create_bake_lightmap_uv(target_transform, bake_group):

        bake_lightmap_uv_name = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_lightmapuv)
        custom_lightmap_uv_name = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_customlightmapuv)

        auto_projection_mel = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_unwrapuvmel)

        if not utility_uvset.Method.exist_uvset(
                target_transform, bake_lightmap_uv_name):
            utility_uvset.Method.create_new_uvset(
                target_transform, bake_lightmap_uv_name)

        utility_uvset.Method.set_current_uvset(
            target_transform, bake_lightmap_uv_name)

        if utility_uvset.Method.exist_uvset(
                target_transform, custom_lightmap_uv_name):

            cmds.select(target_transform, r=True)
            cmds.polyCopyUV(target_transform, uvs=bake_lightmap_uv_name,
                            uvi=custom_lightmap_uv_name)

        else:

            cmds.select(target_transform, r=True)
            utility_common.OtherMethod.execute_mel(auto_projection_mel)

        utility_uvset.Method.set_current_uvset(
            target_transform, bake_lightmap_uv_name)

    # ===========================================
    @staticmethod
    def change_bake_lightmap_uv(target_transform, bake_group):

        bake_lightmap_uv_name = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_lightmapuv)

        utility_uvset.Method.set_current_uvset(
            target_transform, bake_lightmap_uv_name)

    # ===========================================
    @staticmethod
    def change_custom_lightmap_uv(target_transform, bake_group):

        custom_lightmap_uv_name = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_customlightmapuv)

        utility_uvset.Method.set_current_uvset(
            target_transform, custom_lightmap_uv_name)

    # ===========================================
    @staticmethod
    def change_first_uv(target_transform):

        utility_uvset.Method.set_current_uvset_from_index(target_transform, 0)

    # ===========================================
    @staticmethod
    def set_bake_colorset_result(target_transform, bake_group):

        if not utility_colorset.Method.exist_colorset(
                target_transform, bake_group.colorset_result_name):
            return

        utility_colorset.Method.set_current_colorset(
            target_transform, bake_group.colorset_result_name)

    # ===========================================
    @staticmethod
    def calculate_result_vertex_color(target_transform, bake_group):

        bake_type = bake_group.group_root.param_item_group.get_attr_value(
            gp.get_name(gp.bake_type))

        colorset_light_name = bake_group.colorset_light_name
        colorset_ao_name = bake_group.colorset_ao_name
        colorset_indirect_name = bake_group.colorset_indirect_name

        colorset_multi_name = bake_group.colorset_multi_name
        colorset_add_name = bake_group.colorset_add_name
        colorset_overlay_name = bake_group.colorset_overlay_name

        common_colorset_multi_name = bake_group.common_colorset_multi_name
        common_colorset_add_name = bake_group.common_colorset_add_name
        common_colorset_overlay_name = bake_group.common_colorset_overlay_name
        common_colorset_alpha_name = bake_group.common_colorset_alpha_name

        light_enable = bake_group.light_enable
        ao_enable = bake_group.ao_enable
        indirect_enable = bake_group.indirect_enable

        light_alpha = bake_group.light_alpha
        ao_alpha = bake_group.ao_alpha
        indirect_alpha = bake_group.indirect_alpha

        if not light_enable:
            light_alpha = 0

        if not ao_enable:
            ao_alpha = 0

        if not indirect_enable:
            indirect_alpha = 0

        colorset_result_name = bake_group.colorset_result_name

        om_mesh = utility_common.OmMethod.get_om_mesh(target_transform)

        om_vtxface_color_light_list = \
            Method.get_om_color_list(
                target_transform,
                om_mesh, [0.5, 0.5, 0.5, 1], colorset_light_name)

        om_vtxface_color_indirect_list = \
            Method.get_om_color_list(
                target_transform,
                om_mesh, [0, 0, 0, 1], colorset_indirect_name)

        om_vtxface_color_ao_list = \
            Method.get_om_color_list(
                target_transform,
                om_mesh, [1, 1, 1, 1], colorset_ao_name)

        om_vtxface_color_multi_list = \
            Method.get_om_color_list(
                target_transform,
                om_mesh, [1, 1, 1, 1], colorset_multi_name)

        om_vtxface_color_add_list = \
            Method.get_om_color_list(
                target_transform,
                om_mesh, [0, 0, 0, 1], colorset_add_name)

        om_vtxface_color_overlay_list = \
            Method.get_om_color_list(
                target_transform,
                om_mesh, [0.5, 0.5, 0.5, 1], colorset_overlay_name)

        om_common_vtxface_color_multi_list = \
            Method.get_om_color_list(
                target_transform,
                om_mesh, [1, 1, 1, 1], common_colorset_multi_name)

        om_common_vtxface_color_add_list = \
            Method.get_om_color_list(
                target_transform,
                om_mesh, [0, 0, 0, 1], common_colorset_add_name)

        om_common_vtxface_color_overlay_list = \
            Method.get_om_color_list(
                target_transform,
                om_mesh, [0.5, 0.5, 0.5, 1], common_colorset_overlay_name)

        om_common_vtxface_color_alpha_list = \
            Method.get_om_color_list(
                target_transform,
                om_mesh, [0.5, 0.5, 0.5, 1], common_colorset_alpha_name)

        om_vtxface_color_result_list = om.MColorArray()

        utility_colorset.Method.create_new_colorset(
            target_transform, colorset_result_name)

        utility_colorset.Method.set_current_colorset(
            target_transform, colorset_result_name)

        om_face_id_list = om.MIntArray()
        om_vertex_id_list = om.MIntArray()
        om_vtxface_color_fix_list = om.MColorArray()

        vtxface_list = \
            cmds.polyListComponentConversion(target_transform, tvf=True)

        vtxface_list = cmds.ls(vtxface_list, l=True, fl=True)

        this_shape = utility_common.NodeMethod.get_mesh_shape(target_transform)

        for p in range(len(vtxface_list)):

            this_vtxface = vtxface_list[p]

            this_transform = this_vtxface.split('.')[0]

            if this_transform != target_transform and \
                    this_shape != this_transform:
                continue

            this_vtx_and_face_index = \
                utility_common.NameMethod.get_vertex_and_face_index(
                    this_vtxface)

            this_vertex_index = this_vtx_and_face_index[0]
            this_face_index = this_vtx_and_face_index[1]

            this_vtxface_index = \
                om_mesh.getFaceVertexIndex(
                    this_face_index, this_vertex_index, False)

            this_light_color = om_vtxface_color_light_list[this_vtxface_index]
            this_indirect_color = om_vtxface_color_indirect_list[this_vtxface_index]
            this_ao_color = om_vtxface_color_ao_list[this_vtxface_index]

            this_multi_color = om_vtxface_color_multi_list[this_vtxface_index]
            this_add_color = om_vtxface_color_add_list[this_vtxface_index]
            this_overlay_color = om_vtxface_color_overlay_list[this_vtxface_index]

            this_common_multi_color = om_common_vtxface_color_multi_list[this_vtxface_index]
            this_common_add_color = om_common_vtxface_color_add_list[this_vtxface_index]
            this_common_overlay_color = om_common_vtxface_color_overlay_list[this_vtxface_index]

            this_common_alpha_color = om_common_vtxface_color_alpha_list[this_vtxface_index]

            this_light_color = utility_common.OmMethod.get_color(
                this_light_color)

            this_ao_color = utility_common.OmMethod.get_color(
                this_ao_color)

            this_indirect_color = utility_common.OmMethod.get_color(
                this_indirect_color)

            this_light_color = utility_vector.Method.multiply_vector(
                this_light_color, bake_group.light_color_multi
            )

            this_light_color = utility_vector.Method.add_vector(
                this_light_color, bake_group.light_color_offset
            )

            this_ao_color = utility_vector.Method.multiply_vector(
                this_ao_color, bake_group.ao_color_multi
            )

            this_ao_color = utility_vector.Method.add_vector(
                this_ao_color, bake_group.ao_color_offset
            )

            this_indirect_color = utility_vector.Method.multiply_vector(
                this_indirect_color, bake_group.indirect_color_multi
            )

            this_indirect_color = utility_vector.Method.add_vector(
                this_indirect_color, bake_group.indirect_color_offset
            )

            this_result_color = [0, 0, 0, 1]

            max_bright_value = 0

            if bake_type == 'Vertex':

                for q in range(3):

                    blend_light_color = \
                        utility_value.Method.lerp(
                            0.71, this_light_color[q], light_alpha)

                    blend_ao_color = \
                        utility_value.Method.lerp(
                            1, this_ao_color[q], ao_alpha)

                    this_bright_value = \
                        blend_light_color * blend_ao_color

                    if this_bright_value > max_bright_value:
                        max_bright_value = this_bright_value

            for q in range(3):

                if bake_type == 'Vertex':

                    blend_indirect_color = \
                        utility_value.Method.lerp(
                            0, this_indirect_color[q], indirect_alpha)

                    blend_light_color = \
                        utility_value.Method.lerp(
                            0.71, this_light_color[q], light_alpha)

                    blend_ao_color = \
                        utility_value.Method.lerp(
                            1, this_ao_color[q], ao_alpha)

                    this_result_color[q] = \
                        utility_value.Method.lerp(
                            blend_indirect_color,
                            blend_light_color,
                            max_bright_value
                    )

                elif bake_type == "Texture":

                    this_result_color[q] = 0.5

                else:

                    this_result_color[q] = 0.5

                this_result_color[q] = \
                    this_result_color[q] * this_multi_color[q] + \
                    this_add_color[q]

                if this_overlay_color[q] > 0.5:

                    this_result_color[q] += \
                        (this_overlay_color[q] - 0.5) * 2

                else:

                    this_result_color[q] *= this_overlay_color[q] * 2

                this_result_color[q] = \
                    this_result_color[q] * this_common_multi_color[q] + \
                    this_common_add_color[q]

                if this_common_overlay_color[q] > 0.5:

                    this_result_color[q] += \
                        (this_common_overlay_color[q] - 0.5) * 2

                else:

                    this_result_color[q] *= this_common_overlay_color[q] * 2

            this_result_color[3] = this_common_alpha_color[3]

            om_result_color = \
                utility_common.OmMethod.get_om_color(this_result_color)

            om_vtxface_color_result_list.append(om_result_color)

            om_vtxface_color_fix_list.append(om_result_color)
            om_face_id_list.append(this_face_index)
            om_vertex_id_list.append(this_vertex_index)

        om_mesh.setFaceVertexColors(
            om_vtxface_color_fix_list, om_face_id_list, om_vertex_id_list)

    # ===========================================
    @staticmethod
    def get_om_color_list(
            target_transform, om_mesh, defalut_color, colorset_name):

        vtx_face_count = om_mesh.numFaceVertices

        result_om_color_list = \
            [utility_common.OmMethod.get_om_color(defalut_color)] * \
            vtx_face_count

        if utility_colorset.Method.exist_colorset(
                target_transform, colorset_name):

            result_om_color_list = \
                om_mesh.getFaceVertexColors(colorset_name)

        return result_om_color_list

    # ===========================================
    @staticmethod
    def change_uv_link(target_transform, bake_group, chooser_node_list):

        shape = utility_node.Method.get_mesh_shape(target_transform)

        if shape is None:
            return

        bake_lightmap_uv_name = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_lightmapuv)

        uvset_index_list = cmds.getAttr(shape + ".uvSet", mi=True)

        for uvset_index in uvset_index_list:

            this_uvset_name_attr = shape + \
                ".uvSet[" + str(uvset_index) + "].uvSetName"

            this_uvset_name = cmds.getAttr(this_uvset_name_attr)

            if this_uvset_name is None:
                continue

            if this_uvset_name == "":
                continue

            if this_uvset_name != bake_lightmap_uv_name:
                continue

            for chooser in chooser_node_list:

                if not cmds.objExists(chooser):
                    continue

                this_chooser_uvset_index_list = cmds.getAttr(
                    chooser + ".uvSets", mi=True)

                is_connected = False
                if this_chooser_uvset_index_list is not None:

                    for this_chooser_uvset_index in \
                            this_chooser_uvset_index_list:

                        this_chooser_uvset_attr = chooser + \
                            ".uvSets[" + str(this_chooser_uvset_index) + "]"

                        if cmds.isConnected(this_uvset_name_attr,
                                            this_chooser_uvset_attr):
                            is_connected = True
                            break

                if is_connected:
                    continue

                this_chooser_uvset_insert_index = 0

                if this_chooser_uvset_index_list is not None:
                    this_chooser_uvset_insert_index = len(
                        this_chooser_uvset_index_list)

                this_chooser_new_uvset_attr = chooser + \
                    ".uvSets[" + str(this_chooser_uvset_insert_index) + "]"

                try:
                    cmds.connectAttr(this_uvset_name_attr,
                                     this_chooser_new_uvset_attr, force=True)
                except Exception:
                    pass

    # ===========================================
    @staticmethod
    def set_vertex_color_blend(target_transform, vertex_blend_type):

        this_mesh = utility_node.Method.get_mesh_shape(
            target_transform
        )

        if this_mesh is None:
            return

        display_color = True
        display_color_channel = 'Ambient+Diffuse'
        material_blend = 0

        if vertex_blend_type == cp.vertex_blend_normal:
            material_blend = 3
        elif vertex_blend_type == cp.vertex_blend_lightmap:
            material_blend = 6

        utility_attribute.Method.set_attr(
            this_mesh, 'displayColors', 'bool', display_color
        )

        utility_attribute.Method.set_attr(
            this_mesh, 'displayColorChannel', 'string', display_color_channel
        )

        utility_attribute.Method.set_attr(
            this_mesh, 'materialBlend', 'int', material_blend
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeObject(object):

    # ===========================================
    def __init__(self):

        self.main = None

        self.target = None

        self.param_item_group = None

        self.param_key_list = None

    # ===========================================
    def initialize(self):

        if not cmds.objExists(self.target):
            return

        self.param_item_group = param_item_group.ParamItemGroup()

        self.param_item_group = param_item_group.ParamItemGroup()
        self.param_item_group.target = self.target
        self.param_item_group.attr_prefix = self.main.attr_prefix + "obj_"
        self.param_item_group.ui_prefix = self.main.ui_prefix + "obj_"

        self.param_key_list = []

        self.param_key_list.append(obp.group_link)
        self.param_key_list.append(obp.lock)

        for key in self.param_key_list:

            self.param_item_group.add_item(
                obp.get_name(key),
                obp.get_type(key),
                obp.get_value(key),
                obp.get_ui_label(key),
                obp.get_ui_type(key)
            )

    # ===========================================
    def get_bake_group(self):

        attr_name = self.param_item_group.get_attr_name(
            obp.get_name(obp.group_link))

        connect_list = cmds.listConnections(self.target + "." + attr_name)

        if connect_list is None:
            return

        if len(connect_list) == 0:
            return

        group_index = cmds.getAttr(
            connect_list[0] + "." + self.main.attr_prefix + "grp_Index")

        return self.main.bake_group_root.group_list[group_index]

    # ===========================================
    def link_bake_group(self, bake_group):

        utility_attribute.Method.connect_attr(
            bake_group.target,
            bake_group.group_root.param_item_group.get_attr_name(
                gp.get_name(gp.group_link)),
            self.target,
            self.param_item_group.get_attr_name(obp.get_name(obp.group_link))
        )

    # ===========================================
    def unlink_bake_group(self):

        bake_group = self.get_bake_group()

        utility_attribute.Method.disconnect_attr(
            bake_group.target,
            bake_group.group_root.param_item_group.get_attr_name(
                gp.get_name(gp.group_link)),
            self.target,
            self.param_item_group.get_attr_name(obp.get_name(obp.group_link))
        )

    # ===========================================
    def remove_attr(self):

        self.root.clean_attr(self.target, [], self.root.attr_prefix)

    # ===========================================
    def is_lock(self):

        this_setting = self.main.bake_setting_root.setting_list[
            self.main.bake_setting_root.current_index
        ]

        return False

        self.param_group.set_attr_prefix(
            self.target,
            self.root.attr_prefix + "obj_set" + str(this_setting.index) + "_"
        )

        is_lock = self.param_group.get_attr_value(obp.get_name(obp.lock))

        self.param_group.set_attr_prefix(
            self.target, self.root.attr_prefix + "obj_")

        return is_lock

    # ===========================================
    def set_lock(self, arg):

        this_setting = self.main.bake_setting_root.setting_list[
            self.main.bake_setting_root.current_index
        ]

        self.param_group.set_attr_prefix(
            self.target,
            self.root.attr_prefix + "obj_set" + str(this_setting.index) + "_"
        )

        if arg:
            self.param_group.set_attr_value(obp.get_name(obp.lock), True)

        else:
            self.param_group.set_attr_value(obp.get_name(obp.lock), False)

        self.param_group.set_attr_prefix(
            self.target, self.root.attr_prefix + "obj_")

    # ===========================================
    def create_temp_colorset(self):

        bake_group = self.get_bake_group()

        if bake_group is None:
            return

        bake_type = bake_group.group_root.param_item_group.get_attr_value(
            gp.get_name(gp.bake_type))

        utility_colorset.Method.create_new_colorset(
            self.target, cp.temp_colorset)
        utility_colorset.Method.set_current_colorset(
            self.target, cp.temp_colorset)

        utility_common.OtherMethod.reset_display_mode_for_lightmap(self.target)
        utility_common.OtherMethod.reset_vtxcolor_for_lightmap(self.target)

        utility_colorset.Method.set_current_colorset(
            self.target, cp.temp_colorset)

    # ===========================================
    def set_default_colorset(self):

        bake_group = self.get_bake_group()

        colorset_name = bake_group.get_bake_colorset_prefix()

        return

        if utility.colorset.exist_colorset(self.target, colorset_name):
            utility.colorset.set_current_colorset(self.target, colorset_name)

    # ===========================================
    def set_bake_colorset(self):

        bake_group = self.get_bake_group()

        if bake_group is None:
            return

        colorset_light_name = bake_group.get_colorset_light()

        if utility_colorset.Method.exist_colorset(
                self.target, colorset_light_name):
            utility_colorset.Method.set_current_colorset(
                self.target, colorset_light_name)

    # ===========================================
    def set_colorset(self, colorset_type):

        bake_group = self.get_bake_group()

        if bake_group is None:
            return

        colorset_name = None
        default_color = [0, 0, 0, 1]

        if colorset_type == cp.colorset_common_multiply:
            colorset_name = bake_group.get_common_colorset_multi()
            default_color = [1, 1, 1, 1]

        elif colorset_type == cp.colorset_common_add:
            colorset_name = bake_group.get_common_colorset_add()
            default_color = [0, 0, 0, 1]

        elif colorset_type == cp.colorset_common_overlay:
            colorset_name = bake_group.get_common_colorset_overlay()
            default_color = [0.5, 0.5, 0.5, 1]

        if colorset_type == cp.colorset_multiply:
            colorset_name = bake_group.get_colorset_multi()
            default_color = [1, 1, 1, 1]

        elif colorset_type == cp.colorset_add:
            colorset_name = bake_group.get_colorset_add()
            default_color = [0, 0, 0, 1]

        elif colorset_type == cp.colorset_overlay:
            colorset_name = bake_group.get_colorset_overlay()
            default_color = [0.5, 0.5, 0.5, 1]

        if colorset_name is None:
            return

        if utility_colorset.Method.exist_colorset(
                self.target, colorset_name):
            utility_colorset.Method.set_current_colorset(
                self.target, colorset_name)
            return

        utility_colorset.Method.create_new_colorset(
            self.target, colorset_name, default_color)
        utility_colorset.Method.set_current_colorset(
            self.target, colorset_name)

    # ===========================================
    def update_colorset_result(self):

        bake_group = self.get_bake_group()

        return

        if bake_group is None:
            return

        bake_type = bake_group.group_root.param_item_group.get_attr_value(
            gp.get_name(gp.bake_type))

        colorset_light_name = bake_group.get_colorset_light()
        colorset_ao_name = bake_group.get_colorset_ao()
        colorset_indirect_name = bake_group.get_colorset_indirect()

        colorset_multi_name = bake_group.get_colorset_multi()
        colorset_add_name = bake_group.get_colorset_add()
        colorset_overlay_name = bake_group.get_colorset_overlay()

        common_colorset_multi_name = bake_group.get_common_colorset_multi()
        common_colorset_add_name = bake_group.get_common_colorset_add()
        common_colorset_overlay_name = bake_group.get_common_colorset_overlay()

        colorset_result_name = bake_group.get_colorset_result()

        om_mesh = utility_common.OmMethod.get_om_mesh(self.target)

        vtx_face_count = om_mesh.numFaceVertices

        om_vtxface_color_light_list = \
            self.get_om_color_list(
                om_mesh, [0.5, 0.5, 0.5, 1], colorset_light_name)

        om_vtxface_color_indirect_list = \
            self.get_om_color_list(
                om_mesh, [0, 0, 0, 1], colorset_indirect_name)

        om_vtxface_color_ao_list = \
            self.get_om_color_list(
                om_mesh, [1, 1, 1, 1], colorset_ao_name)

        om_vtxface_color_multi_list = \
            self.get_om_color_list(
                om_mesh, [1, 1, 1, 1], colorset_multi_name)

        om_vtxface_color_add_list = \
            self.get_om_color_list(
                om_mesh, [0, 0, 0, 1], colorset_add_name)

        om_vtxface_color_overlay_list = \
            self.get_om_color_list(
                om_mesh, [0.5, 0.5, 0.5, 1], colorset_overlay_name)

        om_common_vtxface_color_multi_list = \
            self.get_om_color_list(
                om_mesh, [1, 1, 1, 1], common_colorset_multi_name)

        om_common_vtxface_color_add_list = \
            self.get_om_color_list(
                om_mesh, [0, 0, 0, 1], common_colorset_add_name)

        om_common_vtxface_color_overlay_list = \
            self.get_om_color_list(
                om_mesh, [0.5, 0.5, 0.5, 1], common_colorset_overlay_name)

        om_vtxface_color_result_list = om.MColorArray()

        for p in range(vtx_face_count):

            this_light_color = \
                utility_common.OmMethod.get_color(
                    om_vtxface_color_light_list[p])

            this_indirect_color = \
                utility_common.OmMethod.get_color(
                    om_vtxface_color_indirect_list[p])

            this_ao_color = \
                utility_common.OmMethod.get_color(
                    om_vtxface_color_ao_list[p])

            this_multi_color = \
                utility_common.OmMethod.get_color(
                    om_vtxface_color_multi_list[p])

            this_add_color = \
                utility_common.OmMethod.get_color(
                    om_vtxface_color_add_list[p])

            this_overlay_color = \
                utility_common.OmMethod.get_color(
                    om_vtxface_color_overlay_list[p])

            this_common_multi_color = \
                utility_common.OmMethod.get_color(
                    om_common_vtxface_color_multi_list[p])

            this_common_add_color = \
                utility_common.OmMethod.get_color(
                    om_common_vtxface_color_add_list[p])

            this_common_overlay_color = \
                utility_common.OmMethod.get_color(
                    om_common_vtxface_color_overlay_list[p])

            this_result_color = [0, 0, 0, 1]

            max_bright_value = 0
            for q in range(3):

                this_bright_value = this_light_color[q] * this_ao_color[q]

                if this_bright_value > max_bright_value:
                    max_bright_value = this_bright_value

            for q in range(3):

                if bake_type == 'Vertex':

                    this_result_color[q] = \
                        this_indirect_color[q] * (1 - max_bright_value) \
                        + this_light_color[q] * max_bright_value

                elif bake_type == "Texture":

                    this_result_color[q] = 0.5

                this_result_color[q] *= this_multi_color[q]
                this_result_color[q] += this_add_color[q]

                if this_overlay_color[q] > 0.5:
                    this_result_color[q] += \
                        (this_overlay_color[q] - 0.5) * 2
                else:
                    this_result_color[q] *= this_overlay_color[q] * 2

                this_result_color[q] *= this_common_multi_color[q]
                this_result_color[q] += this_common_add_color[q]

                if this_common_overlay_color[q] > 0.5:
                    this_result_color[q] += \
                        (this_common_overlay_color[q] - 0.5) * 2
                else:
                    this_result_color[q] *= this_common_overlay_color[q] * 2

            this_result_color[3] = this_common_multi_color[3]

            om_result_color = \
                utility_common.OmMethod.get_om_color(this_result_color)

            om_vtxface_color_result_list.append(om_result_color)

        utility_colorset.Method.create_new_colorset(
            self.target, colorset_result_name)
        utility_colorset.Method.set_current_colorset(
            self.target, colorset_result_name)

        om_face_id_list = om.MIntArray()
        om_vertex_id_list = om.MIntArray()
        om_vtxface_color_fix_list = om.MColorArray()

        vtxface_list = cmds.polyListComponentConversion(self.target, tvf=True)
        vtxface_list = cmds.ls(vtxface_list, l=True, fl=True)

        this_shape = utility_common.NodeMethod.get_mesh_shape(self.target)

        for p in range(len(vtxface_list)):

            this_vtxface = vtxface_list[p]

            this_transform = this_vtxface.split('.')[0]

            if this_transform != self.target and this_shape != this_transform:
                continue

            this_vtx_and_face_index = \
                utility_common.NameMethod.get_vertex_and_face_index(
                    this_vtxface)

            this_vertex_index = this_vtx_and_face_index[0]
            this_face_index = this_vtx_and_face_index[1]

            this_vtxface_index = \
                om_mesh.getFaceVertexIndex(
                    this_face_index, this_vertex_index, False)

            om_vtxface_color_fix_list.append(
                om_vtxface_color_result_list[this_vtxface_index])

            om_face_id_list.append(this_face_index)
            om_vertex_id_list.append(this_vertex_index)

        om_mesh.setFaceVertexColors(
            om_vtxface_color_fix_list, om_face_id_list, om_vertex_id_list)

    # ===========================================
    def get_om_color_list(self, om_mesh, defalut_color, colorset_name):

        vtx_face_count = om_mesh.numFaceVertices

        result_om_color_list = \
            [utility_common.OmMethod.get_om_color(defalut_color)] * \
            vtx_face_count

        if utility_colorset.Method.exist_colorset(
                self.target, colorset_name):
            result_om_color_list = \
                om_mesh.getFaceVertexColors(colorset_name)

        return result_om_color_list

    # ===========================================
    def create_bake_lightmap_uv(self):

        bake_group = self.get_bake_group()

        if bake_group is None:
            return

        cmds.delete(self.target, ch=True)

        bake_lightmap_uv_name = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_lightmapuv)
        custom_lightmap_uv_name = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_customlightmapuv)

        auto_projection_mel = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_unwrapuvmel)

        if not utility_uvset.Method.exist_uvset(
                self.target, bake_lightmap_uv_name):
            utility_uvset.Method.create_new_uvset(
                self.target, bake_lightmap_uv_name)

        utility_uvset.Method.set_current_uvset(
            self.target, bake_lightmap_uv_name)

        if utility_uvset.Method.exist_uvset(
                self.target, custom_lightmap_uv_name):
            cmds.select(self.target, r=True)
            cmds.polyCopyUV(self.target, uvs=bake_lightmap_uv_name,
                            uvi=custom_lightmap_uv_name)

        else:
            cmds.select(self.target, r=True)
            utility_common.OtherMethod.execute_mel(auto_projection_mel)

        utility_uvset.Method.set_current_uvset(
            self.target, bake_lightmap_uv_name)

    # ===========================================
    def change_bake_lightmap_uv(self):

        bake_group = self.get_bake_group()

        if bake_group is None:
            return

        bake_lightmap_uv_name = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_lightmapuv)

        utility_uvset.Method.set_current_uvset(
            self.target, bake_lightmap_uv_name)

    # ===========================================
    def change_custom_lightmap_uv(self):

        bake_group = self.get_bake_group()

        if bake_group is None:
            return

        custom_lightmap_uv_name = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_customlightmapuv)

        utility_uvset.Method.set_current_uvset(
            self.target, custom_lightmap_uv_name)

    # ===========================================
    def change_first_uv(self):

        utility_uvset.Method.set_current_uvset_from_index(self.target, 0)

    # ===========================================
    def assign_bake_material(self, group_index):

        bake_group = self.get_bake_group()

        if bake_group is None:
            return

        if bake_group.group_root.param_item_group.get_attr("BakeVertexColor"):
            return

        material_list = \
            utility_common.NodeMethod.get_material_list(self.target)

        if material_list is None:
            return

        if len(material_list) == 0:
            return

        if len(material_list) == 1:

            replace_mat_name = self.get_bake_group(
            ).get_bake_material_name(material_list[0])

            if not cmds.objExists(replace_mat_name):
                return

            if material_list[0] == replace_mat_name:
                return

            utility_material.Method.assign_material(
                replace_mat_name, [self.target])

            return

        for this_mat in material_list:

            replace_mat_name = \
                self.get_bake_group().get_bake_material_name(this_mat)

            if not cmds.objExists(replace_mat_name):
                return

            if this_mat == replace_mat_name:
                continue

            target_node_list = \
                utility_material.Method.get_node_list_with_material(
                    this_mat, [self.target])

            utility_material.Method.assign_material(
                replace_mat_name, target_node_list
            )

    # ===========================================
    def assign_base_material(self, group_index):

        material_list = \
            utility_common.NodeMethod.get_material_list(self.target)

        if material_list is None:
            return

        if len(material_list) == 0:
            return

        if len(material_list) == 1:

            replace_mat_name = self.get_bake_group(
            ).get_base_node_name(material_list[0])

            if not cmds.objExists(replace_mat_name):
                return

            if material_list[0] == replace_mat_name:
                return

            utility_material.Method.assign_material(
                replace_mat_name, [self.target])

            return

        for this_mat in material_list:

            replace_mat_name = \
                self.get_bake_group().get_base_node_name(this_mat)

            if not cmds.objExists(replace_mat_name):
                continue

            if this_mat == replace_mat_name:
                continue

            target_node_list = \
                utility_material.Method.get_node_list_with_material(
                    this_mat, [self.target])

            utility_material.Method.assign_material(
                replace_mat_name, target_node_list
            )

    # ===========================================
    def change_uv_link(self, chooser_node_list):

        shape = utility_common.NodeMethod.get_mesh_shape(self.target)

        if shape is None:
            return

        bake_group = self.get_bake_group()

        if bake_group is None:
            return

        bake_lightmap_uv_name = \
            bake_group.group_root.override_param.get_attr_value(
                ovp.com_bt_lightmapuv)

        uvset_index_list = cmds.getAttr(shape + ".uvSet", mi=True)

        for uvset_index in uvset_index_list:

            this_uvset_name_attr = shape + \
                ".uvSet[" + str(uvset_index) + "].uvSetName"

            this_uvset_name = cmds.getAttr(this_uvset_name_attr)

            if this_uvset_name is None:
                continue

            if this_uvset_name == "":
                continue

            if this_uvset_name != bake_lightmap_uv_name:
                continue

            for chooser in chooser_node_list:

                if not cmds.objExists(chooser):
                    continue

                this_chooser_uvset_index_list = cmds.getAttr(
                    chooser + ".uvSets", mi=True)

                is_connected = False
                if this_chooser_uvset_index_list is not None:

                    for this_chooser_uvset_index in \
                            this_chooser_uvset_index_list:

                        this_chooser_uvset_attr = chooser + \
                            ".uvSets[" + str(this_chooser_uvset_index) + "]"

                        if cmds.isConnected(this_uvset_name_attr,
                                            this_chooser_uvset_attr):
                            is_connected = True
                            break

                if is_connected:
                    continue

                this_chooser_uvset_insert_index = 0

                if this_chooser_uvset_index_list is not None:
                    this_chooser_uvset_insert_index = len(
                        this_chooser_uvset_index_list)

                this_chooser_new_uvset_attr = chooser + \
                    ".uvSets[" + str(this_chooser_uvset_insert_index) + "]"

                try:
                    cmds.connectAttr(this_uvset_name_attr,
                                     this_chooser_new_uvset_attr, force=True)
                except:
                    self.root.tempValue = 0
