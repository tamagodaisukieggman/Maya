from __future__ import absolute_import
from inspect import trace

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
except Exception:
    pass

import subprocess
import time

import maya.cmds as cmds
import maya.mel as mel

from ..utility import common as utility_common
from ..utility import attribute as utility_attribute
from ..utility import colorset as utility_colorset
from ..utility import material as utility_material
from ..utility import list as utility_list
from ..utility import set as utility_set
from ..utility import mesh as utility_mesh
from ..utility import batch_render as utility_batch_render
from ..utility import file as utility_file
from ..utility import vector as utility_vector

from ..ui import button as ui_button

from . import bake_group_param_list as gp
from . import bake_override_param_list as ovp
from . import bake_common_param_list as cp
from . import bake_setting_param_list as stp

from . import bake_object

import shutil
import os


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeGroup(object):

    # ===========================================
    def __init__(self, main, group_root, index):

        self.main = main

        self.group_root = group_root

        self.index = index

        self.target_name = None
        self.target = None

        self.param_item_group = None

        self.override_param = None

        self.ui_btn_select = None
        self.btn_bake = None
        self.btn_bake_test = None

        self.bake_object_list = None
        self.target_transform_list = None
        self.target_mesh_shape_list = None

        self.project_dir_path = None
        self.root_dir_path = None

        self.base_material_list = None
        self.base_file_node_list = None
        self.base_color_list = None

        self.bake_material_list = None
        self.bake_layer_node_list = None
        self.bake_file_node_list = None
        self.bake_p2t_node_list = None
        self.bake_chooser_node_list = None

        self.texture_output_dir_path = None
        self.temp_texture_output_dir_path = None
        self.export_texture_dir_path = None

        self.bake_origin_texture_file_path_list = None
        self.bake_texture_file_path_list = None

        self.bake_blend_list = None

        self.bake_layer_mode_list = None
        self.bake_layer_alpha_list = None
        self.bake_layer_gain_list = None

        self.bake_colorset_list = None

        self.ui_btn_update_bake_lightmap_uv = None
        self.ui_btn_view_bake_lightmap_uv = None
        self.ui_btn_view_custom_lightmap_uv = None
        self.ui_btn_view_first_uv = None

        self.ui_btn_select_all = None
        self.ui_btn_add = None
        self.ui_btn_remove = None
        self.ui_btn_clear = None

        self.material_link_attr = None

        self.colorset_result_name = None
        self.colorset_light_name = None
        self.colorset_ao_name = None
        self.colorset_indirect_name = None
        self.colorset_add_name = None
        self.colorset_multi_name = None
        self.colorset_overlay_name = None

        self.common_colorset_gray_name = None
        self.common_colorset_add_name = None
        self.common_colorset_multi_name = None
        self.common_colorset_overlay_name = None
        self.common_colorset_alpha_name = None

        self.light_enable = False
        self.ao_enable = False
        self.indirect_enable = False

        self.light_alpha = 0
        self.ao_alpha = 0
        self.indirect_alpha = 0

        self.light_color_multi = None
        self.ao_color_multi = None
        self.indirect_color_multi = None

        self.light_color_offset = None
        self.ao_color_offset = None
        self.indirect_color_offset = None

        self.light_fix_color_multi = None
        self.ao_fix_color_multi = None
        self.indirect_fix_color_multi = None

        self.light_fix_color_offset = None
        self.ao_fix_color_offset = None
        self.indirect_fix_color_offset = None

    # ===========================================
    def initialize(self):

        self.target_name = \
            self.group_root.group_prefix + '{0:02d}'.format(self.index)

        self.target = self.group_root.target + '|' + self.target_name

        if not cmds.objExists(self.target):
            utility_common.NodeMethod.create_group(
                self.target_name, self.group_root.target)

        self.material_link_attr = \
            self.main.attr_prefix + 'MaterialLink'

    # ===========================================
    def initialize_later(self):

        self.group_root.set_target(self.index)

        self.group_root.param_item_group.set_attr_value(
            gp.get_name(gp.index), self.index)

        if not self.group_root.param_item_group.exist_attr(
                gp.get_name(gp.name)):

            self.group_root.param_item_group.set_attr_value(
                gp.get_name(gp.name),
                'group{0:02d}'.format(self.index)
            )

        self.group_root.override_param.set_attr_value_once(
            ovp.com_bc_groupcolorsetsuffix,
            ''
        )

        self.group_root.override_param.set_attr_value_once(
            ovp.com_bt_grouptexturesuffix,
            '_group{0:02d}'.format(self.index)
        )

        self.group_root.override_param.set_attr_value_once(
            ovp.com_bt_groupmaterialsuffix,
            '_group{0:02d}'.format(self.index)
        )

    # ===========================================
    def create_ui(self):

        cmds.rowLayout(self.main.ui_prefix + 'grp_List' + str(self.index),
                       numberOfColumns=2, adj=2, cal=[2, 'left'])

        self.ui_btn_select = ui_button.Button('Select')
        self.ui_btn_select.set_size([50, None])
        self.ui_btn_select.set_function(
            self.group_root.change_index, self.index)

        cmds.text(self.main.ui_prefix + 'grp_Name' + str(self.index))

        cmds.setParent('..')

    # ===========================================
    def update_ui(self):

        self.group_root.param_item_group.set_target(self.target)

        this_name = \
            self.group_root.param_item_group.get_attr_value(
                gp.get_name(gp.name))

        cmds.text(self.main.ui_prefix + 'grp_Name' + str(self.index),
                  e=True, label=this_name)

        if self.index == self.group_root.current_index:
            self.activate_ui()
        else:
            self.inactivate_ui()

    # ===========================================
    def activate_ui(self):

        cmds.rowLayout(self.main.ui_prefix + 'grp_List' + str(self.index),
                       e=True, bgc=cp.group_bg_color)

    # ===========================================
    def inactivate_ui(self):

        cmds.rowLayout(self.main.ui_prefix + 'grp_List' + str(self.index),
                       e=True, bgc=cp.inactive_bg_color)

    # ===========================================
    def change_ui(self):

        return

    # ===========================================
    def create_bake_lightmap_uv(self):

        bake_type = \
            self.group_root.param_item_group.get_attr_value(
                gp.get_name(gp.bake_type))

        if bake_type != 'Texture':
            return

        if not utility_list.Method.exist_list(self.target_transform_list):
            return

        for target_transform in self.target_transform_list:

            bake_object.Method.create_bake_lightmap_uv(
                target_transform, self
            )

        cmds.select(self.target_transform_list, r=True)

        layout_uv_mel = \
            self.group_root.override_param.get_attr_value(
                ovp.com_bt_layoutuvmel)

        utility_common.OtherMethod.execute_mel(layout_uv_mel)

    # ===========================================
    def change_bake_lightmap_uv(self):

        for target_transform in self.target_transform_list:
            bake_object.Method.change_bake_lightmap_uv(
                target_transform, self
            )

    # ===========================================
    def change_custom_lightmap_uv(self):

        for target_transform in self.target_transform_list:
            bake_object.Method.change_custom_lightmap_uv(
                target_transform, self
            )

    # ===========================================
    def change_first_uv(self):

        for target_transform in self.target_transform_list:

            bake_object.Method.change_first_uv(target_transform)

    # ===========================================
    def view_uv_editor(self):

        if not utility_list.Method.exist_list(self.target_transform_list):
            return

        cmds.select(self.target_transform_list, r=True)

        mel.eval('TextureViewWindow;')

    # ===========================================
    def set_target(self):

        self.set_target_fast()

        self.group_root.override_param.param_item_group.set_target(self.target)

        self.group_root.override_param.param_item_group.set_attr_prefix_all(
            self.main.attr_prefix + 'grp_ovp_set{0:02d}_'.format(
                self.main.bake_setting_root.target_setting.index)
        )

        self.group_root.override_param.set_attr_prefix(
            ovp.com_bc_groupcolorsetsuffix, self.main.attr_prefix + 'grp_ovp_')
        self.group_root.override_param.set_attr_prefix(
            ovp.com_bt_grouptexturesuffix, self.main.attr_prefix + 'grp_ovp_')
        self.group_root.override_param.set_attr_prefix(
            ovp.com_bt_groupmaterialsuffix, self.main.attr_prefix + 'grp_ovp_')

        self.group_root.override_param.parent_param = self.main.bake_setting_root.override_param

    # ===========================================
    def set_target_fast(self):

        self.group_root.param_item_group.set_target(self.target)

    # ===========================================
    def set_target_completely(self):

        self.set_target()

        if not self.__update_target_list():
            return

        if not self.__update_root_path():
            return

        if not self.__update_node_name():
            return

        if not self.__update_render_setting():
            return

        self.__update_colorset_name()
        self.__update_lightmap_enable_value()

    # ===========================================
    def __update_target_list(self):

        self.target_transform_list = []
        self.target_mesh_shape_list = []

        self.group_root.object_root.update_target_object_list()

        if not utility_list.Method.exist_list(self.group_root.object_root.target_object_list):
            return False

        for target_transform in self.group_root.object_root.target_object_list:

            this_mesh = utility_mesh.Method.get_mesh_shape(
                target_transform
            )

            if this_mesh is None:
                continue

            self.target_transform_list.append(target_transform)
            self.target_mesh_shape_list.append(this_mesh)

        if not utility_list.Method.exist_list(self.target_transform_list):
            return False

        return True

    # ===========================================
    def __update_root_path(self):

        self.project_dir_path = cmds.workspace(q=True, rootDirectory=True)
        self.root_dir_path = None

        if not os.path.exists(self.project_dir_path):
            return False

        self.root_dir_path = self.project_dir_path

        current_scene = cmds.file(q=True, sn=True)

        if current_scene is not None:
            if current_scene != '':
                if os.path.exists(current_scene):

                    parent_dir_path = os.path.abspath(
                        os.path.dirname(current_scene))
                    parent_dir_name = os.path.basename(parent_dir_path)

                    if parent_dir_name.lower() == 'scenes':
                        self.root_dir_path = os.path.dirname(parent_dir_path)

                    else:
                        self.root_dir_path = parent_dir_path

        if not os.path.exists(self.root_dir_path):
            return False

        return True

    # ===========================================
    def __update_node_name(self):

        if len(self.target_transform_list) == 0:
            return False

        self.base_material_list = []
        self.base_file_node_list = []
        self.base_color_list = []

        self.bake_material_list = []
        self.bake_output_multi_node_list = []
        self.bake_layer_node_list = []

        self.bake_file_node_list = []
        self.bake_p2t_node_list = []
        self.bake_chooser_node_list = []

        self.bake_blend_list = ['multiply', 'add', 'multiply']

        self.bake_layer_mode_list = [6, 4, 6]
        self.bake_layer_alpha_list = [1.0, 1.0, 1.0]
        self.bake_layer_gain_list = [2.0, 1.0, 1.0]

        texture_type_list = ['light', 'indirect', 'ao']

        texture_origin_suffix_list = [
            'tpIllumination',
            'tpIndirectIllumination',
            self.group_root.override_param.get_attr_value(
                ovp.ttl_bc_ao_sampler_name)
        ]

        self.bake_origin_texture_file_path_list = []
        self.bake_texture_file_path_list = []

        self.bake_composite_texture_file_path = ''

        self.bake_origin_colorset_list = []
        self.bake_colorset_list = []

        for target_transform in self.target_transform_list:

            this_material_list = utility_material.Method.get_material_list(
                target_transform)

            if not utility_list.Method.exist_list(this_material_list):
                continue

            for this_mat in this_material_list:

                this_base_mat_name = self.get_base_material(this_mat)

                if this_base_mat_name is None:
                    this_base_mat_name = this_mat

                exist = False
                for mat in self.base_material_list:

                    if mat == this_base_mat_name:
                        exist = True
                        break

                if exist:
                    continue

                self.base_material_list.append(this_base_mat_name)

        if not utility_list.Method.exist_list(self.base_material_list):
            return False

        for p in range(0, len(self.base_material_list)):

            this_base_material = self.base_material_list[p]

            this_base_file_node_list = cmds.listConnections(
                this_base_material + '.color', type='file')

            this_base_color = utility_attribute.Method.get_attr(
                this_base_material, 'color', 'color'
            )

            this_base_file_node = None
            if this_base_file_node_list is not None:
                if len(this_base_file_node_list) > 0:
                    this_base_file_node = this_base_file_node_list[0]

            this_bake_mat_name = self.get_bake_material_name(
                this_base_material)

            this_output_multi_node = self.get_bake_node_name_with_index(
                'multiOutput_' + this_base_material)

            self.base_color_list.append(this_base_color)

            self.base_file_node_list.append(this_base_file_node)

            self.bake_material_list.append(this_bake_mat_name)

            self.bake_output_multi_node_list.append(this_output_multi_node)

        self.texture_output_dir_path = self.root_dir_path + '/' + \
            self.group_root.override_param.get_attr_value(
                ovp.com_bt_texouptputpath)

        self.temp_texture_output_dir_path = self.texture_output_dir_path + '/temp'

        self.export_texture_dir_path = \
            self.main.bake_common_setting.root_dir_path + '/' + \
            self.group_root.override_param.get_attr_value(
                ovp.com_bc_export_texture_dir_path
            )

        texture_prefix = self.get_bake_texture_prefix()
        this_colorset_prefix = self.get_bake_colorset_prefix()

        for p in range(0, len(texture_type_list)):

            this_file_node = self.get_bake_node_name_with_index(
                'file') + '_' + texture_type_list[p]
            this_p2t_node = self.get_bake_node_name_with_index(
                'place2dTexture') + '_' + texture_type_list[p]
            this_chooser_node = self.get_bake_node_name_with_index(
                'uvChooser') + '_' + texture_type_list[p]

            this_origin_texture_path = self.temp_texture_output_dir_path + '/' + \
                texture_prefix + '_' + texture_origin_suffix_list[p] + '.tga'
            this_texture_file_path = self.texture_output_dir_path + '/' + \
                texture_prefix + '_' + texture_type_list[p] + '.tga'

            this_origin_colorset_name = this_colorset_prefix + \
                '_' + texture_origin_suffix_list[p]
            this_colorset_name = this_colorset_prefix + \
                '_' + texture_type_list[p]

            self.bake_file_node_list.append(this_file_node)
            self.bake_p2t_node_list.append(this_p2t_node)
            self.bake_chooser_node_list.append(this_chooser_node)

            self.bake_origin_texture_file_path_list.append(
                this_origin_texture_path)
            self.bake_texture_file_path_list.append(this_texture_file_path)

            self.bake_origin_colorset_list.append(this_origin_colorset_name)
            self.bake_colorset_list.append(this_colorset_name)

        self.bake_lt_clamp_node = self.get_bake_node_name_with_index(
            'clampLight')
        self.bake_in_clamp_node = self.get_bake_node_name_with_index(
            'clampIndirect')
        self.bake_ao_clamp_node = self.get_bake_node_name_with_index('clampAo')

        self.bake_lt_ao_multi_node = self.get_bake_node_name_with_index(
            'multiLightAo')

        self.bake_lt_in_rgb_hsv_node = self.get_bake_node_name_with_index(
            'rgbToHsvLightIndirect')

        self.bake_lt_in_blend_node = self.get_bake_node_name_with_index(
            'blendLightIndirect')

        self.bake_lt_multi_node = self.get_bake_node_name_with_index(
            'multiLight')

        self.bake_export_multi_node = self.get_bake_node_name_with_index(
            'multiExport')

        self.bake_2_multi_node = self.get_bake_node_name_with_index('multiTwo')

        self.bake_tx_lt_multi_node = self.get_bake_node_name_with_index(
            'multiTexLight')

        self.bake_composite_texture_file_path = \
            self.export_texture_dir_path + \
            '/' + texture_prefix + '.tga'

        return True

    # ===========================================
    def __update_render_setting(self):

        bake_layer_name = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_bakelayername)
        ao_sampler_name = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_ao_sampler_name)

        if not cmds.objExists(bake_layer_name):

            cmds.select(cl=True)
            eval_string = 'ilrCreateBakeLayer(\"' + bake_layer_name + '\", 1)'
            utility_common.OtherMethod.execute_mel(eval_string)

        bake_type = \
            self.group_root.param_item_group.get_attr_value(
                gp.get_name(gp.bake_type))

        com_orthoreflect = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_orthreflect)
        com_bake_shadow = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_bakeshadows)
        com_bgcolor = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_bgcolor)

        com_ao_mincolor = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_ao_mincolor)

        com_ao_maxcolor = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_ao_maxcolor)

        com_ao_maxdistance = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_ao_maxdistance)

        com_ao_contrast = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_ao_contrast)

        com_ao_scale = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_ao_scale)

        com_ao_accuracy = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_ao_accuracy)

        com_ao_smooth = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_ao_smooth)

        tex_width = self.group_root.override_param.get_attr_value(
            ovp.com_bt_width)
        tex_height = self.group_root.override_param.get_attr_value(
            ovp.com_bt_height)
        tex_test_width = self.group_root.override_param.get_attr_value(
            ovp.com_bt_testwidth)
        tex_test_height = self.group_root.override_param.get_attr_value(
            ovp.com_bt_testheight)

        tex_bilinear = self.group_root.override_param.get_attr_value(
            ovp.ttl_bt_bilinear)
        tex_edge_dilation = self.group_root.override_param.get_attr_value(
            ovp.ttl_bt_edgedilation)

        tex_texture_name = self.get_bake_texture_prefix() + '_$p.$e'

        vtx_sample_mode = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_samplemode)
        vtx_min_sample = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_minsample)
        vtx_max_sample = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_maxsample)
        vtx_vtx_bias = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_vtxbias)

        vtx_rgb_scale = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_rgbscale)
        vtx_clamp = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_clamp)
        vtx_rgb_min = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_rgbmin)
        vtx_rgb_max = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_rgbmax)

        vtx_enable_filter = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_enablefilter)
        vtx_filter_size = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_filtersize)
        vtx_filter_shape = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_filtershape)
        vtx_filter_deviation = self.group_root.override_param.get_attr_value(
            ovp.ttl_bv_filterdeviation)

        light_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_light_enable)

        indirect_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_indirect_enable)

        ao_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_ao_enable)

        cmds.select(cl=True)

        cmds.setAttr(bake_layer_name + '.renderSelection', 0)

        utility_set.Method.clear_member_from_set(bake_layer_name)

        utility_set.Method.add_member_to_set(
            bake_layer_name, self.target_mesh_shape_list)

        if not cmds.objExists(ao_sampler_name):
            cmds.shadingNode('ilrOccSampler', asShader=True,
                             name=ao_sampler_name)

        utility_attribute.Method.connect_attr(
            ao_sampler_name, 'outColor', bake_layer_name, 'customShader')

        cmds.setAttr(ao_sampler_name + '.minColor',
                     com_ao_mincolor[0], com_ao_mincolor[1], com_ao_mincolor[2],
                     type='double3')

        cmds.setAttr(ao_sampler_name + '.maxColor',
                     com_ao_maxcolor[0], com_ao_maxcolor[1], com_ao_maxcolor[2],
                     type='double3')

        cmds.setAttr(ao_sampler_name + '.maxDistance', com_ao_maxdistance)
        cmds.setAttr(ao_sampler_name + '.contrast', com_ao_contrast)
        cmds.setAttr(ao_sampler_name + '.scale', com_ao_scale)

        cmds.setAttr(ao_sampler_name + '.accuracy', com_ao_accuracy)
        cmds.setAttr(ao_sampler_name + '.smooth', com_ao_smooth)

        cmds.setAttr(ao_sampler_name + '.minSamples', 5000)
        cmds.setAttr(ao_sampler_name + '.maxSamples', 5000)

        if bake_type == 'Vertex':
            cmds.setAttr(bake_layer_name + '.renderType', 2)
        elif bake_type == 'Texture':
            cmds.setAttr(bake_layer_name + '.renderType', 1)

        cmds.setAttr(bake_layer_name + '.orthoRefl', com_orthoreflect)
        cmds.setAttr(bake_layer_name + '.normalDirection', 0)
        cmds.setAttr(bake_layer_name + '.orthoRefl', com_orthoreflect)
        cmds.setAttr(bake_layer_name + '.shadows', com_bake_shadow)
        cmds.setAttr(bake_layer_name + '.alpha', 0)
        cmds.setAttr(bake_layer_name + '.viewDependent', 0)
        cmds.setAttr(bake_layer_name + '.backgroundColor',
                     com_bgcolor[0], com_bgcolor[1], com_bgcolor[2],
                     type='double3')

        if self.main.bake_setting_root.bake_quality_type == \
                cp.bake_quality_test:

            cmds.setAttr(bake_layer_name + '.tbResX', tex_test_width)
            cmds.setAttr(bake_layer_name + '.tbResY', tex_test_height)

            cmds.setAttr(bake_layer_name + '.tbEdgeDilation', 0)

        else:
            cmds.setAttr(bake_layer_name + '.tbResX', tex_width)
            cmds.setAttr(bake_layer_name + '.tbResY', tex_height)

            cmds.setAttr(
                bake_layer_name + '.tbEdgeDilation', tex_edge_dilation)

        cmds.setAttr(bake_layer_name + '.tbConservative', 1)
        cmds.setAttr(bake_layer_name + '.tbMerge', 1)
        cmds.setAttr(bake_layer_name + '.tbSaveToRenderView', 0)
        cmds.setAttr(bake_layer_name + '.tbSaveToFile', 1)

        if self.temp_texture_output_dir_path is not None:
            cmds.setAttr(bake_layer_name + '.tbDirectory',
                         self.temp_texture_output_dir_path, typ='string')

        cmds.setAttr(bake_layer_name + '.tbFileName',
                     tex_texture_name, typ='string')

        cmds.setAttr(bake_layer_name + '.tbVisualize', 0)

        cmds.setAttr(bake_layer_name + '.tbBilinearFilter', tex_bilinear)

        cmds.setAttr(bake_layer_name + '.tbUvRange', 0)

        cmds.setAttr(bake_layer_name + '.tbUvSet', '', typ='string')
        cmds.setAttr(bake_layer_name + '.tbTangentUvSet', '', typ='string')

        if vtx_sample_mode == 'Per Vertex':
            cmds.setAttr(bake_layer_name + '.vbSamplingMode', 0)
        elif vtx_sample_mode == 'Triangle Subdiv':
            cmds.setAttr(bake_layer_name + '.vbSamplingMode', 1)

        cmds.setAttr(bake_layer_name + '.vbMinSamples', vtx_min_sample)
        cmds.setAttr(bake_layer_name + '.vbMaxSamples', vtx_max_sample)
        cmds.setAttr(bake_layer_name + '.vbVertexBias', vtx_vtx_bias)

        cmds.setAttr(bake_layer_name + '.vbSaveToColorSet', 1)
        cmds.setAttr(bake_layer_name + '.vbOverwriteColorSet', 1)
        cmds.setAttr(bake_layer_name + '.vbSaveToFile', 0)

        cmds.setAttr(bake_layer_name + '.vbUseBlending', 0)

        cmds.setAttr(bake_layer_name + '.vbRgbScale', vtx_rgb_scale)

        cmds.setAttr(bake_layer_name + '.vbClamp', vtx_clamp)

        cmds.setAttr(bake_layer_name + '.vbRgbMin',
                     vtx_rgb_min[0], vtx_rgb_min[1], vtx_rgb_min[2],
                     type='double3')
        cmds.setAttr(bake_layer_name + '.vbRgbMax',
                     vtx_rgb_max[0], vtx_rgb_max[1], vtx_rgb_max[2],
                     type='double3')

        cmds.setAttr(bake_layer_name + '.vbFilter', vtx_enable_filter)
        cmds.setAttr(bake_layer_name + '.vbFilterSize', vtx_filter_size)
        cmds.setAttr(bake_layer_name + '.vbFilterShape', vtx_filter_shape)
        cmds.setAttr(bake_layer_name + '.vbFilterNormalDev',
                     vtx_filter_deviation)

        colorset_name = self.get_bake_colorset_prefix() + '_$p'

        cmds.setAttr(bake_layer_name + '.vbColorSet',
                     colorset_name, typ='string')

        cmds.setAttr(bake_layer_name + '.fullShading', 0)

        cmds.setAttr(bake_layer_name + '.illumination', 0)
        cmds.setAttr(bake_layer_name + '.indirectIllumination', 0)
        cmds.setAttr(bake_layer_name + '.custom', 0)

        if light_enable:
            cmds.setAttr(bake_layer_name + '.illumination', 1)

        if indirect_enable:
            cmds.setAttr(bake_layer_name + '.indirectIllumination', 1)

        if ao_enable:
            cmds.setAttr(bake_layer_name + '.custom', 1)

        return True

    # ===========================================
    def __update_colorset_name(self):

        self.colorset_light_name = self.get_bake_colorset_prefix() + '_light'
        self.colorset_indirect_name = self.get_bake_colorset_prefix() + '_indirect'
        self.colorset_ao_name = self.get_bake_colorset_prefix() + '_ao'

        self.colorset_multi_name = self.get_bake_colorset_prefix() + '_multi'
        self.colorset_add_name = self.get_bake_colorset_prefix() + '_add'
        self.colorset_overlay_name = self.get_bake_colorset_prefix() + '_overlay'

        self.colorset_result_name = self.get_bake_colorset_prefix()

        self.common_colorset_gray_name = self.group_root.override_param.get_attr_value(
            ovp.com_bc_common_colorset_gray)

        self.common_colorset_multi_name = self.group_root.override_param.get_attr_value(
            ovp.com_bc_common_colorset_multi)

        self.common_colorset_add_name = self.group_root.override_param.get_attr_value(
            ovp.com_bc_common_colorset_add)

        self.common_colorset_overlay_name = self.group_root.override_param.get_attr_value(
            ovp.com_bc_common_colorset_overlay)

        self.common_colorset_alpha_name = self.group_root.override_param.get_attr_value(
            ovp.com_bc_common_colorset_alpha)

    # ===========================================
    def __update_lightmap_enable_value(self):

        self.light_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_light_enable)

        self.ao_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_ao_enable)

        self.indirect_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_indirect_enable)

        self.light_alpha = self.group_root.override_param.get_attr_value(
            ovp.com_bc_light_alpha)

        self.ao_alpha = self.group_root.override_param.get_attr_value(
            ovp.com_bc_ao_alpha)

        self.indirect_alpha = self.group_root.override_param.get_attr_value(
            ovp.com_bc_indirect_alpha)

        self.light_color_multi = self.group_root.override_param.get_attr_value(
            ovp.com_bc_light_color_multi)

        self.ao_color_multi = self.group_root.override_param.get_attr_value(
            ovp.com_bc_ao_color_multi)

        self.indirect_color_multi = self.group_root.override_param.get_attr_value(
            ovp.com_bc_indirect_color_multi)

        self.light_color_offset = self.group_root.override_param.get_attr_value(
            ovp.com_bc_light_color_offset)

        self.ao_color_offset = self.group_root.override_param.get_attr_value(
            ovp.com_bc_ao_color_offset)

        self.indirect_color_offset = self.group_root.override_param.get_attr_value(
            ovp.com_bc_indirect_color_offset)

        if not self.light_enable:
            self.light_alpha = 0

        if not self.ao_enable:
            self.ao_alpha = 0

        if not self.indirect_enable:
            self.indirect_alpha = 0

        self.light_fix_color_multi = utility_vector.Method.lerp(
            [0] * 3, self.light_color_multi, self.light_alpha
        )

        self.ao_fix_color_multi = utility_vector.Method.lerp(
            [0] * 3, self.ao_color_multi, self.ao_alpha
        )

        self.indirect_fix_color_multi = utility_vector.Method.lerp(
            [0] * 3, self.indirect_color_multi, self.indirect_alpha
        )

        self.light_fix_color_offset = utility_vector.Method.lerp(
            [0.71] * 3, self.light_color_offset, self.light_alpha
        )

        self.ao_fix_color_offset = utility_vector.Method.lerp(
            [1] * 3, self.ao_color_offset, self.ao_alpha
        )

        self.indirect_fix_color_offset = utility_vector.Method.lerp(
            [0] * 3, self.indirect_color_offset, self.indirect_alpha
        )

    # ===========================================
    def bake_scene(self):

        if not self.__update_render_setting():
            return

        bake_type = self.group_root.param_item_group.get_attr_value(
            gp.get_name(gp.bake_type))

        cmds.flushUndo()

        self.set_colorset(cp.colorset_common_gray)

        if bake_type == 'Vertex':
            self.render_vertex_color()

        elif bake_type == 'Texture':
            self.render_texture()

        self.calculate_result_vertex_color()

        self.set_colorset(cp.colorset_result)

        cmds.flushUndo()

    # ===========================================
    def render_vertex_color(self):

        self.assign_base_material()

        self.change_first_uv()

        cmds.flushUndo()
        mel.eval('RenderIntoNewWindow;')
        cmds.flushUndo()

        self.rename_lightmap_colorset()

    # ===========================================
    def render_texture(self):

        if not os.path.exists(self.texture_output_dir_path):
            os.makedirs(self.texture_output_dir_path)

        if not os.path.exists(self.temp_texture_output_dir_path):
            os.makedirs(self.temp_texture_output_dir_path)

        self.assign_base_material()

        self.change_bake_lightmap_uv()

        bake_layer_name = self.group_root.override_param.get_attr_value(
            ovp.ttl_bc_bakelayername)

        cmds.setAttr(bake_layer_name + '.illumination', 0)
        cmds.setAttr(bake_layer_name + '.indirectIllumination', 0)
        cmds.setAttr(bake_layer_name + '.custom', 0)

        if self.light_enable:

            cmds.setAttr(bake_layer_name + '.illumination', 1)

            temp_file_path = utility_file.create_temp_file_from_current_file(
                'lmm_', '_bake_light', 'temp')

            if temp_file_path is not None:
                self.main.batch_render_manager.add_target(temp_file_path, None)

            cmds.setAttr(bake_layer_name + '.illumination', 0)

        if self.ao_enable:

            cmds.setAttr(bake_layer_name + '.custom', 1)

            temp_file_path = utility_file.create_temp_file_from_current_file(
                'lmm_', '_bake_ao', 'temp')

            if temp_file_path is not None:
                self.main.batch_render_manager.add_target(temp_file_path, None)

            cmds.setAttr(bake_layer_name + '.custom', 0)

        if self.indirect_enable:

            cmds.setAttr(bake_layer_name + '.indirectIllumination', 1)

            temp_file_path = utility_file.create_temp_file_from_current_file(
                'lmm_', '_bake_indirect', 'temp')

            if temp_file_path is not None:
                self.main.batch_render_manager.add_target(temp_file_path, None)

            cmds.setAttr(bake_layer_name + '.indirectIllumination', 0)

        self.change_first_uv()

        self.update_bake_material()

    # ===========================================
    def create_composite_texture(self):

        bake_type = \
            self.group_root.param_item_group.get_attr_value(
                gp.get_name(gp.bake_type))

        if bake_type == 'Vertex':
            return

        if bake_type == 'None':
            return

        if not cmds.objExists(self.bake_export_multi_node):
            return

        if not cmds.objExists(self.bake_file_node_list[0]):
            return

        if not os.path.exists(self.export_texture_dir_path):
            os.makedirs(self.export_texture_dir_path)

        if os.path.exists(self.bake_texture_file_path_list[0]):
            cmds.setAttr(self.bake_file_node_list[0] + '.fileTextureName',
                         self.bake_texture_file_path_list[0], type='string')

        reso_width = cmds.getAttr(self.bake_file_node_list[0] + '.outSizeX')
        reso_height = cmds.getAttr(self.bake_file_node_list[0] + '.outSizeY')

        composit_mel_arg = str(reso_width) + ' '
        composit_mel_arg += str(reso_height) + ' '
        composit_mel_arg += '\"lmm_temp\"' + ' '
        composit_mel_arg += '\"tga\"' + ' '
        composit_mel_arg += '\"\"' + ' '
        composit_mel_arg += str(0) + ' '
        composit_mel_arg += str(0) + ' '
        composit_mel_arg += str(1) + ' '
        composit_mel_arg += str(0) + ' '
        composit_mel_arg += 'true'

        cmds.select(self.bake_export_multi_node, r=True)

        composite_mel = 'composite ' + composit_mel_arg

        mel.eval(composite_mel)

        temp_texture_file_path = \
            self.main.bake_common_setting.project_dir_path + \
            '/' + 'lmm_temp.0.tga'

        if not os.path.exists(temp_texture_file_path):
            return

        if os.path.exists(self.bake_composite_texture_file_path):
            os.remove(self.bake_composite_texture_file_path)

        shutil.copyfile(temp_texture_file_path,
                        self.bake_composite_texture_file_path)

        if os.path.exists(temp_texture_file_path):
            os.remove(temp_texture_file_path)

    # ===========================================
    def calculate_result_vertex_color(self):

        for target_transform in self.target_transform_list:

            bake_object.Method.calculate_result_vertex_color(
                target_transform, self)

    # ===========================================
    def set_colorset(self, colorset_type):

        for target_transform in self.target_transform_list:

            bake_object.Method.set_colorset(
                target_transform, self, colorset_type)

    # ===========================================
    def rename_lightmap_colorset(self):

        for target_transform in self.target_transform_list:

            for p in range(0, len(self.bake_origin_colorset_list)):

                this_origin_colorset = self.bake_origin_colorset_list[p]
                this_new_colorset = self.bake_colorset_list[p]

                if not utility_colorset.Method.exist_colorset(
                        target_transform, this_origin_colorset):
                    continue

                abc = utility_colorset.Method.get_colorset_list(
                    target_transform)

                utility_colorset.Method.delete_colorset(
                    target_transform, this_new_colorset)

                utility_colorset.Method.rename_colorset(
                    target_transform,
                    this_origin_colorset, this_new_colorset)

    # ===========================================
    def rename_texture(self):

        for cnt in range(0, len(self.bake_origin_texture_file_path_list)):

            this_origin_path = self.bake_origin_texture_file_path_list[cnt]
            this_new_path = self.bake_texture_file_path_list[cnt]

            if not os.path.exists(this_origin_path):
                continue

            shutil.copy(this_origin_path, this_new_path)

            if os.path.exists(this_origin_path):
                os.remove(this_origin_path)

    # ===========================================
    def update_bake_material(self):

        self.create_bake_material()

        self.update_file_p2t_chooser_node()

        self.update_lightmap_node()

        self.update_output_node()

        self.update_uv_link()

        self.rename_texture()

        self.update_base_file_node()

    # ===========================================
    def create_bake_material(self):

        for p in range(0, len(self.bake_material_list)):

            this_bake_material = self.bake_material_list[p]
            this_base_material = self.base_material_list[p]

            utility_material.Method.create_new_material(
                this_bake_material
            )

            utility_attribute.Method.add_attr(
                this_bake_material,
                self.material_link_attr,
                self.material_link_attr,
                'message',
                None
            )

            utility_attribute.Method.add_attr(
                this_base_material,
                self.material_link_attr,
                self.material_link_attr,
                'message',
                None
            )

            utility_attribute.Method.connect_attr(
                this_base_material,
                self.material_link_attr,
                this_bake_material,
                self.material_link_attr
            )

    # ===========================================
    def update_base_file_node(self):

        for cnt in range(0, len(self.base_file_node_list)):

            this_file_node = self.base_file_node_list[cnt]

            if this_file_node is None:
                continue

            utility_attribute.Method.set_attr(
                this_file_node, 'colorSpace', 'string', 'Raw')

    # ===========================================
    def update_lightmap_node(self):

        if not cmds.objExists(self.bake_lt_clamp_node):
            cmds.shadingNode('clamp', asUtility=True,
                             name=self.bake_lt_clamp_node)

        if not cmds.objExists(self.bake_in_clamp_node):
            cmds.shadingNode('clamp', asUtility=True,
                             name=self.bake_in_clamp_node)

        if not cmds.objExists(self.bake_ao_clamp_node):
            cmds.shadingNode('clamp', asUtility=True,
                             name=self.bake_ao_clamp_node)

        if not cmds.objExists(self.bake_lt_in_rgb_hsv_node):
            cmds.shadingNode('rgbToHsv', asUtility=True,
                             name=self.bake_lt_in_rgb_hsv_node)

        if not cmds.objExists(self.bake_lt_in_blend_node):
            cmds.shadingNode('blendColors', asUtility=True,
                             name=self.bake_lt_in_blend_node)

        if not cmds.objExists(self.bake_lt_multi_node):
            cmds.shadingNode('multiplyDivide', asUtility=True,
                             name=self.bake_lt_multi_node)

        if not cmds.objExists(self.bake_lt_ao_multi_node):
            cmds.shadingNode('multiplyDivide', asUtility=True,
                             name=self.bake_lt_ao_multi_node)

        if not cmds.objExists(self.bake_export_multi_node):
            cmds.shadingNode('multiplyDivide', asUtility=True,
                             name=self.bake_export_multi_node)

        if not cmds.objExists(self.bake_2_multi_node):
            cmds.shadingNode('multiplyDivide', asUtility=True,
                             name=self.bake_2_multi_node)

        if not cmds.objExists(self.bake_tx_lt_multi_node):
            cmds.shadingNode('multiplyDivide', asUtility=True,
                             name=self.bake_tx_lt_multi_node)

        light_file_node = self.bake_file_node_list[0]
        indirect_file_node = self.bake_file_node_list[1]
        ao_file_node = self.bake_file_node_list[2]

        light_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_light_enable)

        indirect_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_indirect_enable)

        ao_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_ao_enable)

        light_alpha = self.group_root.override_param.get_attr_value(
            ovp.com_bc_light_alpha)

        indirect_alpha = self.group_root.override_param.get_attr_value(
            ovp.com_bc_indirect_alpha)

        ao_alpha = self.group_root.override_param.get_attr_value(
            ovp.com_bc_ao_alpha)

        if not light_enable:
            light_alpha = 0

        if not ao_enable:
            ao_alpha = 0

        if not indirect_enable:
            indirect_alpha = 0

        utility_attribute.Method.set_attr(
            light_file_node,
            'defaultColor',
            'color',
            [0.71] * 3
        )

        utility_attribute.Method.set_attr(
            light_file_node,
            'colorGain',
            'color',
            self.light_fix_color_multi
        )

        utility_attribute.Method.set_attr(
            light_file_node,
            'colorOffset',
            'color',
            self.light_fix_color_offset
        )

        utility_attribute.Method.set_attr(
            ao_file_node,
            'defaultColor',
            'color',
            [1] * 3
        )

        utility_attribute.Method.set_attr(
            ao_file_node,
            'colorGain',
            'color',
            self.ao_fix_color_multi
        )

        utility_attribute.Method.set_attr(
            ao_file_node,
            'colorOffset',
            'color',
            self.ao_fix_color_offset
        )

        utility_attribute.Method.set_attr(
            indirect_file_node,
            'defaultColor',
            'color',
            [0] * 3
        )

        utility_attribute.Method.set_attr(
            indirect_file_node,
            'colorGain',
            'color',
            self.indirect_fix_color_multi
        )

        utility_attribute.Method.set_attr(
            indirect_file_node,
            'colorOffset',
            'color',
            self.indirect_fix_color_offset
        )

        utility_attribute.Method.connect_attr(
            light_file_node, 'outColor', self.bake_lt_clamp_node, 'input')

        utility_attribute.Method.set_attr(
            self.bake_lt_clamp_node, 'maxR', 'int', 1)
        utility_attribute.Method.set_attr(
            self.bake_lt_clamp_node, 'maxG', 'int', 1)
        utility_attribute.Method.set_attr(
            self.bake_lt_clamp_node, 'maxB', 'int', 1)

        utility_attribute.Method.connect_attr(
            indirect_file_node, 'outColor', self.bake_in_clamp_node, 'input')

        utility_attribute.Method.set_attr(
            self.bake_in_clamp_node, 'maxR', 'int', 1)
        utility_attribute.Method.set_attr(
            self.bake_in_clamp_node, 'maxG', 'int', 1)
        utility_attribute.Method.set_attr(
            self.bake_in_clamp_node, 'maxB', 'int', 1)

        utility_attribute.Method.connect_attr(
            ao_file_node, 'outColor', self.bake_ao_clamp_node, 'input')

        utility_attribute.Method.set_attr(
            self.bake_ao_clamp_node, 'maxR', 'int', 1)
        utility_attribute.Method.set_attr(
            self.bake_ao_clamp_node, 'maxG', 'int', 1)
        utility_attribute.Method.set_attr(
            self.bake_ao_clamp_node, 'maxB', 'int', 1)

        utility_attribute.Method.connect_attr(
            self.bake_lt_clamp_node, 'output',
            self.bake_lt_ao_multi_node, 'input1')
        utility_attribute.Method.connect_attr(
            self.bake_ao_clamp_node, 'output',
            self.bake_lt_ao_multi_node, 'input2')

        utility_attribute.Method.connect_attr(
            self.bake_lt_ao_multi_node, 'output',
            self.bake_lt_in_rgb_hsv_node, 'inRgb')

        utility_attribute.Method.connect_attr(
            self.bake_lt_in_rgb_hsv_node, 'outHsvV',
            self.bake_lt_in_blend_node, 'blender')

        utility_attribute.Method.connect_attr(
            self.bake_lt_clamp_node, 'output',
            self.bake_lt_in_blend_node, 'color1')
        utility_attribute.Method.connect_attr(
            self.bake_in_clamp_node, 'output',
            self.bake_lt_in_blend_node, 'color2')

        utility_attribute.Method.connect_attr(
            self.bake_lt_in_blend_node, 'output',
            self.bake_lt_multi_node, 'input1')

        utility_attribute.Method.connect_attr(
            self.bake_lt_multi_node, 'output',
            self.bake_export_multi_node, 'input1')

        utility_attribute.Method.connect_attr(
            self.bake_export_multi_node, 'output',
            self.bake_2_multi_node, 'input1')

        utility_attribute.Method.set_attr(
            self.bake_2_multi_node, 'input2X', 'float', 2)
        utility_attribute.Method.set_attr(
            self.bake_2_multi_node, 'input2Y', 'float', 2)
        utility_attribute.Method.set_attr(
            self.bake_2_multi_node, 'input2Z', 'float', 2)

        utility_attribute.Method.connect_attr(
            self.bake_2_multi_node, 'output',
            self.bake_tx_lt_multi_node, 'input1')
        utility_attribute.Method.connect_attr(
            self.base_file_node_list[0], 'output',
            self.bake_tx_lt_multi_node, 'input2')

        utility_attribute.Method.connect_attr(
            self.bake_tx_lt_multi_node, 'output',
            self.bake_material_list[0], 'input2')

    # ===========================================
    def update_file_p2t_chooser_node(self):

        for cnt in range(0, len(self.bake_file_node_list)):

            this_file_node = self.bake_file_node_list[cnt]
            this_p2t_node = self.bake_p2t_node_list[cnt]
            this_chooser_node = self.bake_chooser_node_list[cnt]
            this_texture_file_path = self.bake_texture_file_path_list[cnt]

            if not cmds.objExists(this_file_node):
                cmds.shadingNode('file', asTexture=True,
                                 name=this_file_node, isColorManaged=True)

            if not cmds.objExists(this_p2t_node):
                cmds.shadingNode('place2dTexture',
                                 asUtility=True, name=this_p2t_node)

            if not cmds.objExists(this_chooser_node):
                cmds.shadingNode('uvChooser', asUtility=True,
                                 name=this_chooser_node)

            if os.path.exists(this_texture_file_path):
                cmds.setAttr(this_file_node + '.fileTextureName',
                             this_texture_file_path, type='string')

            utility_common.NodeMethod.connect_place2d_to_file(
                this_p2t_node, this_file_node)

            utility_common.NodeMethod.connect_chooser_to_place2d(
                this_chooser_node, this_p2t_node)

    # ===========================================
    def update_output_node(self):

        for cnt in range(0, len(self.bake_material_list)):

            this_file_node = self.base_file_node_list[cnt]
            this_output_multi_node = self.bake_output_multi_node_list[cnt]
            this_base_color = self.base_color_list[cnt]

            if not cmds.objExists(this_output_multi_node):

                cmds.shadingNode('multiplyDivide', asUtility=True,
                                 name=this_output_multi_node)

            try:
                utility_attribute.Method.set_attr(
                    this_output_multi_node, 'input1X', 'float', this_base_color[0])
                utility_attribute.Method.set_attr(
                    this_output_multi_node, 'input1Y', 'float', this_base_color[1])
                utility_attribute.Method.set_attr(
                    this_output_multi_node, 'input1Z', 'float', this_base_color[2])
            except:
                pass

            if this_file_node is not None:
                if cmds.objExists(this_file_node):
                    utility_attribute.Method.connect_attr(
                        this_file_node, 'outColor',
                        this_output_multi_node, 'input1')

            if cmds.objExists(self.bake_2_multi_node):
                utility_attribute.Method.connect_attr(
                    self.bake_2_multi_node, 'output',
                    this_output_multi_node, 'input2')

    # ===========================================
    def update_uv_link(self):

        for target_transform in self.target_transform_list:

            bake_object.Method.change_uv_link(
                target_transform,
                self,
                self.bake_chooser_node_list)

    # ===========================================
    def update_hardware_texture_setting(self):

        if not utility_list.Method.exist_list(self.bake_material_list):
            return

        for cnt in range(0, len(self.bake_material_list)):
            this_bake_material = self.bake_material_list[cnt]

            utility_common.NodeMethod.turn_off_hardware_texture(
                this_bake_material)

    # ===========================================
    def assign_base_material(self):

        for target_transform in self.target_transform_list:

            bake_object.Method.assign_base_material(
                target_transform, self
            )

            bake_object.Method.set_vertex_color_blend(
                target_transform, cp.vertex_blend_lightmap
            )

        self.update_hardware_texture_setting()

    # ===========================================
    def assign_bake_material(self):

        bake_type = \
            self.group_root.param_item_group.get_attr_value(
                gp.get_name(gp.bake_type))

        self.assign_base_material()

        for target_transform in self.target_transform_list:

            bake_object.Method.set_vertex_color_blend(
                target_transform, cp.vertex_blend_lightmap
            )

        if bake_type != 'Texture':
            return

        self.update_bake_material()

        for target_transform in self.target_transform_list:

            bake_object.Method.assign_bake_material(
                target_transform, self
            )

        for cnt in range(0, len(self.bake_material_list)):

            this_bake_material = self.bake_material_list[cnt]
            this_base_file_node = self.base_file_node_list[cnt]

            if this_base_file_node is not None:
                utility_attribute.Method.connect_attr(
                    this_base_file_node, 'outColor',
                    this_bake_material, 'color')

        self.update_hardware_texture_setting()

    # ===========================================
    def assign_bake_material_with_lightmap(self):

        bake_type = self.group_root.param_item_group.get_attr_value(
            gp.get_name(gp.bake_type))

        self.assign_base_material()

        for target_transform in self.target_transform_list:

            bake_object.Method.set_vertex_color_blend(
                target_transform, cp.vertex_blend_lightmap
            )

        if bake_type != 'Texture':
            return

        self.assign_bake_material()

        for cnt in range(0, len(self.bake_material_list)):

            this_bake_material = self.bake_material_list[cnt]
            this_output_multi_node = self.bake_output_multi_node_list[cnt]

            if not cmds.objExists(this_bake_material):
                continue

            if not cmds.objExists(this_output_multi_node):
                continue

            utility_attribute.Method.connect_attr(
                this_output_multi_node, 'output', this_bake_material, 'color')

        self.assign_bake_file_path()

        self.update_hardware_texture_setting()

    # ===========================================
    def assign_bake_file_path(self):

        light_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_light_enable)

        indirect_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_indirect_enable)

        ao_enable = self.group_root.override_param.get_attr_value(
            ovp.com_bc_ao_enable)

        for cnt in range(0, len(self.bake_file_node_list)):

            this_file_node = self.bake_file_node_list[cnt]
            this_texture_file_path = self.bake_texture_file_path_list[cnt]

            if not cmds.objExists(this_file_node):
                continue

            is_assign_texture = False

            if this_file_node.find('_light') > 0 and light_enable:
                is_assign_texture = True
            elif this_file_node.find('_indirect') > 0 and indirect_enable:
                is_assign_texture = True
            elif this_file_node.find('_ao') > 0 and ao_enable:
                is_assign_texture = True

            if is_assign_texture:

                if os.path.exists(this_texture_file_path):
                    cmds.setAttr(this_file_node + '.fileTextureName',
                                 this_texture_file_path, type='string')

            else:

                cmds.setAttr(this_file_node + '.fileTextureName',
                             '', type='string')

            utility_attribute.Method.set_attr(
                this_file_node, 'colorSpace', 'string', 'Raw')

    # ===========================================
    def get_bake_node_name_with_index(self, base_node):

        result_name = \
            '{0}_group{1:02d}'.format(base_node, self.index)

        return result_name

    # ===========================================
    def get_base_material(self, target_material):

        if not utility_attribute.Method.exist_attr(
            target_material, self.material_link_attr
        ):
            return

        connect_list = cmds.listConnections(
            target_material + '.' + self.material_link_attr, d=False, s=True)

        if not utility_list.Method.exist_list(connect_list):
            return

        return connect_list[0]

    # ===========================================
    def get_bake_material_name(self, target_material):

        return target_material + self.get_bake_material_suffix()

    # ===========================================
    def get_base_node_name(self, bake_node):

        material_suffix = self.get_bake_material_suffix()

        if bake_node.find(material_suffix) < 0:
            return bake_node

        find_index = bake_node.find(material_suffix)

        node_name = bake_node[0:find_index]

        return node_name

    # ===========================================
    def get_bake_texture_prefix(self):

        texture_prefix = \
            self.group_root.override_param.get_attr_value(
                ovp.com_bt_textureprefix) + \
            self.group_root.override_param.get_attr_value(
                ovp.com_bt_settingtexturesuffix) + \
            self.group_root.override_param.get_attr_value(
                ovp.com_bt_grouptexturesuffix)

        return texture_prefix

    # ===========================================
    def get_bake_material_suffix(self):

        material_suffix = \
            self.group_root.override_param.get_attr_value(
                ovp.com_bt_materialsuffix) + \
            self.group_root.override_param.get_attr_value(
                ovp.com_bt_settingmaterialsuffix) + \
            self.group_root.override_param.get_attr_value(
                ovp.com_bt_groupmaterialsuffix)

        return material_suffix

    # ===========================================
    def get_bake_colorset_prefix(self):

        colorset_prefix = \
            self.group_root.override_param.get_attr_value(
                ovp.com_bc_colorsetprefix) + \
            self.group_root.override_param.get_attr_value(
                ovp.com_bc_settingcolorsetsuffix) + \
            self.group_root.override_param.get_attr_value(
                ovp.com_bc_groupcolorsetsuffix)

        return colorset_prefix

    # ===========================================
    def get_colorset_light(self):

        return self.get_bake_colorset_prefix() + '_light'

    # ===========================================
    def get_colorset_indirect(self):

        return self.get_bake_colorset_prefix() + '_indirect'

    # ===========================================
    def get_colorset_ao(self):

        return self.get_bake_colorset_prefix() + '_ao'

    # ===========================================
    def get_colorset_multi(self):

        return self.get_bake_colorset_prefix() + '_multi'

    # ===========================================
    def get_colorset_add(self):

        return self.get_bake_colorset_prefix() + '_add'

    # ===========================================
    def get_colorset_overlay(self):

        return self.get_bake_colorset_prefix() + '_overlay'

    # ===========================================
    def get_colorset_result(self):

        return self.get_bake_colorset_prefix()

    # ===========================================
    def get_common_colorset_multi(self):

        return self.group_root.override_param.get_attr_value(
            ovp.com_bc_common_colorset_multi)

    # ===========================================
    def get_common_colorset_add(self):

        return self.group_root.override_param.get_attr_value(
            ovp.com_bc_common_colorset_add)

    # ===========================================
    def get_common_colorset_overlay(self):

        return self.group_root.override_param.get_attr_value(
            ovp.com_bc_common_colorset_overlay)

    # ===========================================
    def get_common_colorset_alpha(self):

        return self.group_root.override_param.get_attr_value(
            ovp.com_bc_common_colorset_alpha)

    # ===========================================
    def get_common_colorset_gray(self):

        return self.group_root.override_param.get_attr_value(
            ovp.com_bc_common_colorset_gray)
