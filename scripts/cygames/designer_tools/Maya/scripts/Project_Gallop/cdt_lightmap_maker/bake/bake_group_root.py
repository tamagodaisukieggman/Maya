# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

from ..utility import common as utility_common
from ..utility import list as utility_list

from ..ui import icon_button as ui_icon_button
from ..ui import button as ui_button
from ..ui import dialog as ui_dialog
from ..ui import radio_button as ui_radio_button

from . import param_item_group
from . import bake_override_param

from . import bake_group

from . import bake_group_param_list as gp
from . import bake_override_param_list as ovp
from . import bake_common_param_list as cp

from . import bake_object_root
from . import bake_visible_object_root


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeGroupRoot(object):

    # ===========================================
    def __init__(self, main):

        self.main = main

        self.target_name = None
        self.target = None

        self.group_num = 50
        self.group_prefix = 'group_'

        self.current_index = 0

        self.target_group = None

        self.group_list = []

        self.param_item_group = None

        self.param_key_list = None

        self.override_param = None

        self.object_root = None

        self.visible_object_root = None

        self.ui_object_setting = None
        self.ui_export_setting = None
        self.ui_bake_setting = None

    # ===========================================
    def initialize(self):

        self.target = self.main.target + '|' + self.target_name

        if not cmds.objExists(self.target):
            utility_common.NodeMethod.create_group(
                self.target_name, self.main.target)

        self.param_item_group = param_item_group.ParamItemGroup()
        self.param_item_group.target = self.target
        self.param_item_group.attr_prefix = self.main.attr_prefix + 'grp_'
        self.param_item_group.ui_prefix = self.main.ui_prefix + 'grp_'
        self.param_item_group.function = self.main.change_ui

        self.param_key_list = []

        self.param_key_list.append(gp.index)
        self.param_key_list.append(gp.name)
        self.param_key_list.append(gp.bake_type)
        self.param_key_list.append(gp.texture_name)
        self.param_key_list.append(gp.material_name)
        self.param_key_list.append(gp.colorset_name)
        self.param_key_list.append(gp.group_link)
        self.param_key_list.append(gp.lock)
        self.param_key_list.append(gp.visible_link)

        for key in self.param_key_list:

            self.param_item_group.add_item(
                gp.get_name(key),
                gp.get_type(key),
                gp.get_value(key),
                gp.get_ui_label(key),
                gp.get_ui_type(key)
            )

        self.override_param = bake_override_param.BakeOverrideParam()
        self.override_param.main = self.main
        self.override_param.target = self.target
        self.override_param.param_item_group = \
            self.main.bake_common_setting.override_param.param_item_group
        self.override_param.attr_prefix = self.main.attr_prefix + 'grp_ovp_'
        self.override_param.ui_prefix = self.main.ui_prefix + 'grp_ovp_'
        self.override_param.initialize()

        self.object_root = bake_object_root.BakeObjectRoot(self.main)
        self.object_root.initialize()

        self.visible_object_root = \
            bake_visible_object_root.BakeVisibleObjectRoot()

        self.visible_object_root.main = self.main
        self.visible_object_root.is_group = True
        self.visible_object_root.initialize()

        self.group_list = []

        for p in range(0, self.group_num):

            new_group = bake_group.BakeGroup(self.main, self, p)

            new_group.initialize()

            self.group_list.append(new_group)

        for this_group in self.group_list:
            this_group.initialize_later()

    # ===========================================
    def create_ui(self):

        icon_size = (40, 40)

        self.set_target(self.current_index)

        cmds.columnLayout(adj=True, co=['both', 10])

        self.param_item_group.draw_ui(gp.get_name(gp.name))

        cmds.separator(height=10, style='none')

        ui_radio_button.RadioButton(
            cp.group_tab_label_list, self.change_tab_index)

        self.ui_object_setting = cmds.columnLayout(adj=True)

        self.object_root.create_ui()

        self.visible_object_root.create_ui()

        cmds.setParent('..')

        self.ui_bake_setting = cmds.columnLayout(adj=True)

        self.param_item_group.draw_ui(gp.get_name(gp.bake_type))

        self.override_param.create_ui()

        cmds.setParent('..')

        cmds.setParent('..')

    # ===========================================
    def create_selector_ui(self):

        cmds.frameLayout(l=u'ベイクグループリスト',
                         cll=0, cl=0, bv=0, mw=1, mh=1,
                         p=self.main.ui_current_selector)
        cmds.scrollLayout(verticalScrollBarThickness=5, h=200, cr=True)

        for cnt in range(0, len(self.group_list)):
            self.group_list[cnt].create_ui()

        cmds.setParent('..')
        cmds.setParent('..')

    # ===========================================
    def create_ui_later(self):

        self.change_tab_index(0)

        cmds.columnLayout(adjustableColumn=True,
                          p=self.override_param.combake_colorset_ui_1)

        self.param_item_group.draw_ui(gp.get_name(gp.colorset_name))
        self.param_item_group.enable_ui(gp.get_name(gp.colorset_name), False)

        cmds.setParent('..')

        cmds.columnLayout(adjustableColumn=True,
                          p=self.override_param.texbake_output_ui_1)

        self.param_item_group.draw_ui(gp.get_name(gp.texture_name))
        self.param_item_group.enable_ui(gp.get_name(gp.texture_name), False)

        self.param_item_group.draw_ui(gp.get_name(gp.material_name))
        self.param_item_group.enable_ui(gp.get_name(gp.material_name), False)

        cmds.setParent('..')

        cmds.columnLayout(adjustableColumn=True,
                          p=self.override_param.texbake_lightmapuv_ui_0)

        ui_button.Button(u'ライトマップUVを更新', self.edit_uv_from_ui, 0)
        ui_button.Button(u'ライトマップUVを参照', self.edit_uv_from_ui, 1)
        ui_button.Button(u'カスタムライトマップUVを参照', self.edit_uv_from_ui, 2)
        ui_button.Button(u'デフォルトUVを参照', self.edit_uv_from_ui, 3)

        cmds.setParent('..')

        cmds.columnLayout(adjustableColumn=True,
                          p=self.override_param.combake_colorset_ui_1)

        self.param_item_group.draw_ui(gp.get_name(gp.colorset_name))
        self.param_item_group.enable_ui(gp.get_name(gp.colorset_name), False)

        cmds.setParent('..')

    # ===========================================
    def update_ui(self):

        for cnt in range(0, len(self.group_list)):
            self.group_list[cnt].update_ui()

        self.set_target(self.current_index)

        self.param_item_group.set_ui_from_attr_all()

        self.update_override_ui()

        self.param_item_group.set_ui_from_custom_value(gp.get_name(
            gp.texture_name),
            self.target_group.get_bake_texture_prefix()
        )

        self.param_item_group.set_ui_from_custom_value(
            gp.get_name(gp.material_name),
            'MATERIAL' + self.target_group.get_bake_material_suffix()
        )

        self.param_item_group.set_ui_from_custom_value(
            gp.get_name(gp.colorset_name),
            self.target_group.get_bake_colorset_prefix()
        )

        this_bake_type = self.param_item_group.get_attr_value(
            gp.get_name(gp.bake_type))

        if this_bake_type == 'Texture':
            cmds.frameLayout(
                self.override_param.texbake_frame_ui, e=True, vis=True)
            cmds.frameLayout(
                self.override_param.vtxbake_frame_ui, e=True, vis=False)
        elif this_bake_type == 'Vertex':
            cmds.frameLayout(
                self.override_param.texbake_frame_ui, e=True, vis=False)
            cmds.frameLayout(
                self.override_param.vtxbake_frame_ui, e=True, vis=True)
        else:
            cmds.frameLayout(
                self.override_param.texbake_frame_ui, e=True, vis=False)
            cmds.frameLayout(
                self.override_param.vtxbake_frame_ui, e=True, vis=False)

        self.object_root.update_ui()

        self.visible_object_root.update_ui()

    # ===========================================
    def update_override_ui(self):

        self.override_param.visible_override_ui(
            ovp.com_bt_customlightmapuv, False)
        self.override_param.visible_override_ui(ovp.com_bt_lightmapuv, False)

        self.override_param.visible_override_ui(
            ovp.com_bc_common_colorset_multi, False)

        self.override_param.visible_override_ui(
            ovp.com_bc_common_colorset_add, False)

        self.override_param.visible_override_ui(
            ovp.com_bc_common_colorset_overlay, False)

        self.override_param.visible_override_ui(
            ovp.com_bc_common_colorset_alpha, False)

        self.override_param.visible_override_ui(
            ovp.com_bc_common_colorset_gray, False)

        self.override_param.visible_override_ui(
            ovp.com_bc_colorsetprefix, False)

        self.override_param.visible_override_ui(
            ovp.com_bc_settingcolorsetsuffix, False)

        self.override_param.visible_override_ui(
            ovp.com_bt_settingtexturesuffix, False)

        self.override_param.visible_override_ui(
            ovp.com_bt_grouptexturesuffix, False)

        self.override_param.visible_override_ui(
            ovp.com_bt_groupmaterialsuffix, False)

        self.override_param.visible_override_ui(
            ovp.com_bt_texouptputpath, False)

        self.override_param.visible_override_ui(
            ovp.com_bt_textureprefix, False)

        self.override_param.visible_override_ui(
            ovp.com_bt_materialsuffix, False)

        self.override_param.visible_override_ui(
            ovp.com_bt_settingmaterialsuffix, False)

        self.override_param.visible_override_ui(
            ovp.com_bc_groupcolorsetsuffix, False)

        self.override_param.visible_ui(ovp.com_bt_settingmaterialsuffix, True)

        self.override_param.set_override(ovp.com_bc_groupcolorsetsuffix, True)
        self.override_param.set_override(ovp.com_bt_grouptexturesuffix, True)
        self.override_param.set_override(ovp.com_bt_groupmaterialsuffix, True)

        self.override_param.update_ui()

    # ===========================================
    def change_ui(self):

        self.set_target(self.current_index)

        self.param_item_group.set_attr_from_ui_all()

        self.override_param.change_ui()

        self.object_root.change_ui()

        self.visible_object_root.change_ui()

    # ===========================================
    def change_index(self, index):

        if index == self.current_index:
            return

        self.current_index = index

        self.change_current_index()

        self.main.save_current()

        self.main.change_tab_index(cp.main_tab_bake_group)

        self.main.update_ui()

    # ===========================================
    def change_current_index(self):

        self.set_target(self.current_index)

    # ===========================================
    def change_tab_index(self, index):

        cmds.columnLayout(
            self.ui_object_setting, e=True, vis=False)

        cmds.columnLayout(
            self.ui_bake_setting, e=True, vis=False)

        if index == cp.group_tab_object:

            cmds.columnLayout(
                self.ui_object_setting, e=True, vis=True)

        elif index == cp.group_tab_bake:

            cmds.columnLayout(
                self.ui_bake_setting, e=True, vis=True)

    # ===========================================
    def set_target(self, target_index):

        self.target_group = None

        target_group = self.__get_group(target_index)

        if target_group is None:
            return

        self.target_group = target_group

        self.target_group.set_target()

    # ===========================================
    def set_target_fast(self, target_index):

        self.target_group = None

        target_group = self.__get_group(target_index)

        if target_group is None:
            return

        self.target_group = target_group

        self.target_group.set_target_fast()

    # ===========================================
    def set_target_completely(self, target_index):

        self.target_group = None

        target_group = self.__get_group(target_index)

        if target_group is None:
            return

        self.target_group = target_group

        self.target_group.set_target_completely()

    # ===========================================
    def __get_group(self, group_index):

        group_list_length = len(self.group_list)

        if group_index < 0:
            return

        if group_index >= group_list_length:
            return

        return self.group_list[group_index]

    # ===========================================
    def edit_uv_from_ui(self, arg):

        self.set_target_completely(self.current_index)

        if arg == 0:

            if not ui_dialog.open_yes_no(
                    u'UV更新',
                    u'ライトマップUVを更新しますか？',
                    self.main.ui_window.ui_id):
                return

            self.target_group.create_bake_lightmap_uv()
            self.target_group.change_bake_lightmap_uv()
            self.target_group.view_uv_editor()

        elif arg == 1:
            self.target_group.change_bake_lightmap_uv()
            self.target_group.view_uv_editor()

        elif arg == 2:
            self.target_group.change_custom_lightmap_uv()
            self.target_group.view_uv_editor()

        elif arg == 3:
            self.target_group.change_first_uv()
            self.target_group.view_uv_editor()

    # ===========================================
    def get_group_fix_list(self, group_index_list):

        group_fix_list = []

        if group_index_list is None:
            group_index_list = []

        for p in range(0, len(self.group_list)):

            this_group = self.group_list[p]

            self.set_target(this_group.index)

            self.object_root.update_target_object_list()

            if not utility_list.Method.exist_list(
                    self.object_root.target_object_list):
                continue

            if len(group_index_list) == 0:
                group_fix_list.append(this_group)
                continue

            for q in range(0, len(group_index_list)):

                if group_index_list[q] == this_group.index:
                    group_fix_list.append(this_group)
                    break

        return group_fix_list

    # ===========================================
    def reset_material_and_object(self, material_reset_type):

        group_fix_list = self.get_group_fix_list(None)

        if not utility_common.ListMethod.exist_list(group_fix_list):
            return

        for p in range(0, len(group_fix_list)):

            this_group = group_fix_list[p]

            self.set_target_completely(this_group.index)

            if material_reset_type == cp.material_reset_original:

                this_group.assign_base_material()
                this_group.set_colorset(cp.colorset_result)

            elif material_reset_type == cp.material_reset_bake_with_lightmap:

                this_group.assign_bake_material_with_lightmap()
                this_group.set_colorset(cp.colorset_result)

            elif material_reset_type == \
                    cp.material_reset_bake_without_lightmap:

                this_group.assign_bake_material()
                this_group.set_colorset(cp.colorset_result)

            elif material_reset_type == \
                    cp.material_reset_bake_with_lightmap_and_calc_vertex_color:

                this_group.calculate_result_vertex_color()
                this_group.assign_bake_material_with_lightmap()
                this_group.set_colorset(cp.colorset_result)

    # ===========================================
    def bake_scene(self, group_index_list):

        group_fix_list = \
            self.get_group_fix_list(group_index_list)

        for p in range(0, len(group_fix_list)):

            this_group = group_fix_list[p]

            self.set_target_completely(this_group.index)

            this_group.bake_scene()

    # ===========================================
    def export_composite_texture(self):

        group_fix_list = self.get_group_fix_list(None)

        if not utility_common.ListMethod.exist_list(group_fix_list):
            return

        for cnt in range(0, len(group_fix_list)):

            this_group = self.group_list[cnt]

            self.set_target_completely(this_group.index)

            this_group.assign_bake_material_with_lightmap()
            this_group.create_composite_texture()

        utility_common.IOMethod.open_directory(
            group_fix_list[-1].export_texture_dir_path)

    # ===========================================
    def set_colorset_all(self, colorset_type):

        for p in range(0, len(self.group_list)):

            this_group = self.group_list[p]

            self.set_target_completely(this_group.index)

            self.target_group.set_colorset(colorset_type)

    # ===========================================
    def hide_all_visible_object(self):

        for this_group in self.group_list:

            self.set_target_fast(this_group.index)

            self.visible_object_root.hide_target_object()

    # ===========================================
    def show_visible_object(self):

        self.set_target_fast(self.current_index)

        self.visible_object_root.show_target_object()
