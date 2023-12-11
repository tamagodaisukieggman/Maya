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

import os

from ..utility import common as utility_common
from ..utility import attribute as utility_attribute

from ..ui import icon_button as ui_icon_button
from ..ui import dialog as ui_dialog
from ..ui import radio_button as ui_radio_button

from . import param_item_group

from . import bake_setting

from . import bake_override_param

from . import bake_setting_param_list as sp
from . import bake_common_param_list as cp
from . import bake_override_param_list as ovp

from . import bake_export_object_root
from . import bake_visible_object_root


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeSettingRoot(object):

    # ===========================================
    def __init__(self, main):

        self.main = main

        self.target_name = None

        self.target = None

        self.setting_num = 20
        self.setting_prefix = 'setting_'

        self.current_index = 0

        self.target_index = 0
        self.target_setting = None

        self.setting_list = None

        self.param_item_group = None
        self.override_param = None

        self.param_key_list = None

        self.bake_quality_type = cp.bake_quality_product

        self.export_object_root = None

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
        self.param_item_group.attr_prefix = self.main.attr_prefix + 'set_'
        self.param_item_group.ui_prefix = self.main.ui_prefix + 'set_'
        self.param_item_group.function = self.main.change_ui

        self.param_key_list = []

        self.param_key_list.append(sp.index)
        self.param_key_list.append(sp.name)
        self.param_key_list.append(sp.lock)
        self.param_key_list.append(sp.link)
        self.param_key_list.append(sp.visible_link)
        self.param_key_list.append(sp.export_link)

        for key in self.param_key_list:

            self.param_item_group.add_item(
                sp.get_name(key),
                sp.get_type(key),
                sp.get_value(key),
                sp.get_ui_label(key),
                sp.get_ui_type(key)
            )

        self.override_param = bake_override_param.BakeOverrideParam()

        self.override_param.main = self.main
        self.override_param.target = self.target
        self.override_param.parent_param = \
            self.main.bake_common_setting.override_param

        self.override_param.attr_prefix = self.main.attr_prefix + 'set_ovp_'
        self.override_param.ui_prefix = self.main.ui_prefix + 'set_ovp_'

        self.override_param.initialize()

        self.setting_list = []

        for p in range(0, self.setting_num):

            new_setting = bake_setting.BakeSetting(self.main, self, p)

            new_setting.initialize()

            self.setting_list.append(new_setting)

        for this_setting in self.setting_list:
            this_setting.initialize_later()

        self.export_object_root = \
            bake_export_object_root.BakeExportObjectRoot()

        self.export_object_root.main = self.main
        self.export_object_root.initialize()

        self.visible_object_root = \
            bake_visible_object_root.BakeVisibleObjectRoot()

        self.visible_object_root.main = self.main
        self.visible_object_root.initialize()

    # ===========================================
    def create_ui(self):

        cmds.columnLayout(adj=True, co=['both', 10])

        self.param_item_group.draw_ui(sp.get_name(sp.name))

        cmds.separator(height=10, style='none')

        ui_radio_button.RadioButton(
            cp.setting_tab_label_list, self.change_tab_index)

        self.ui_object_setting = cmds.columnLayout(adj=True)

        self.visible_object_root.create_ui()

        cmds.setParent('..')

        self.ui_export_setting = cmds.columnLayout(adj=True)

        self.export_object_root.create_ui()

        cmds.setParent('..')

        self.ui_bake_setting = cmds.columnLayout(adj=True)

        self.override_param.param_item_group.set_target(
            self.setting_list[self.current_index].target)

        self.override_param.create_ui()

        cmds.setParent('..')

        cmds.setParent('..')

    # ===========================================
    def create_selector_ui(self):

        cmds.frameLayout(
            l=u'ベイク設定リスト',
            cll=0, cl=0, bv=1, mw=1, mh=1,
            p=self.main.ui_current_selector,
            w=self.main.ui_setting_selector_width
        )

        cmds.scrollLayout(verticalScrollBarThickness=5, h=200, cr=True)

        for cnt in range(0, len(self.setting_list)):
            self.setting_list[cnt].create_ui()

        cmds.setParent('..')
        cmds.setParent('..')

    # ===========================================
    def create_ui_later(self):

        self.change_tab_index(0)

    # ===========================================
    def update_ui(self):

        for cnt in range(0, len(self.setting_list)):
            self.setting_list[cnt].update_ui()

        self.set_target(self.current_index)

        self.param_item_group.set_ui_from_attr_all()

        self.update_override_ui()

        self.visible_object_root.update_ui()

        self.export_object_root.update_ui()

    # ===========================================
    def change_tab_index(self, index):

        cmds.columnLayout(
            self.ui_object_setting, e=True, vis=False)

        cmds.columnLayout(
            self.ui_export_setting, e=True, vis=False)

        cmds.columnLayout(
            self.ui_bake_setting, e=True, vis=False)

        if index == cp.setting_tab_object:

            cmds.columnLayout(
                self.ui_object_setting, e=True, vis=True)

        elif index == cp.setting_tab_export:

            cmds.columnLayout(
                self.ui_export_setting, e=True, vis=True)

        elif index == cp.setting_tab_bake:

            cmds.columnLayout(
                self.ui_bake_setting, e=True, vis=True)

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
            ovp.com_bc_settingcolorsetsuffix, False)

        self.override_param.visible_override_ui(
            ovp.com_bt_settingtexturesuffix, False)

        self.override_param.set_override(
            ovp.com_bc_settingcolorsetsuffix, True)

        self.override_param.visible_override_ui(
            ovp.com_bt_settingmaterialsuffix, False)
        self.override_param.set_override(
            ovp.com_bt_settingmaterialsuffix, True)

        self.override_param.set_override(ovp.com_bt_settingtexturesuffix, True)

        self.override_param.visible_ui(ovp.com_bc_groupcolorsetsuffix, False)

        self.override_param.visible_ui(ovp.com_bt_groupmaterialsuffix, False)

        self.override_param.visible_ui(ovp.com_bt_grouptexturesuffix, False)

        self.override_param.update_ui()

    # ===========================================
    def change_ui(self):

        self.set_target(self.current_index)

        self.param_item_group.set_attr_from_ui_all()

        self.override_param.change_ui()

        self.visible_object_root.change_ui()

        self.export_object_root.change_ui()

    # ===========================================
    def change_index(self, index):

        if index == self.current_index:
            return

        if not ui_dialog.open_yes_no(
                u'確認', u'設定を切り替えますか?', self.main.ui_window.ui_id):
            return

        self.current_index = index

        self.change_current_index()

        self.main.save_current()

        self.main.change_tab_index(cp.main_tab_bake_setting)

        self.main.update_ui()

    # ===========================================
    def change_current_index(self):

        self.set_target(self.current_index)

        self.hide_all_visible_object()
        self.show_visible_object()

        self.main.bake_group_root.change_current_index()

        self.reset_material_and_object(
            cp.material_reset_original)

        self.reset_material_and_object(
            cp.material_reset_bake_with_lightmap
        )

    # ===========================================
    def set_target(self, target_setting_index):

        self.target_setting = None

        target_setting = self.__get_setting(target_setting_index)

        if target_setting is None:
            return

        self.target_setting = target_setting

        self.target_setting.set_target()

    # ===========================================
    def __get_setting(self, setting_index):

        setting_list_length = len(self.setting_list)

        if setting_index < 0:
            return

        if setting_index >= setting_list_length:
            return

        return self.setting_list[setting_index]

    # ===========================================
    def get_setting_fix_list(self, setting_index_list):

        setting_fix_list = []

        if setting_index_list is None:
            setting_index_list = []

        for p in range(0, len(self.setting_list)):

            this_setting = self.setting_list[p]

            if len(setting_index_list) == 0:
                setting_fix_list.append(this_setting)
                continue

            for q in range(0, len(setting_index_list)):

                if setting_index_list[q] == this_setting.index:
                    setting_fix_list.append(this_setting)
                    break

        return setting_fix_list

    # ===========================================
    def reset_material_and_object(self, material_reset_type):

        self.main.bake_group_root.reset_material_and_object(
            material_reset_type)

    # ===========================================
    def bake_scene(self, setting_index_list, group_index_list):

        setting_fix_list = self.get_setting_fix_list(setting_index_list)

        for p in range(0, len(setting_fix_list)):

            this_setting = setting_fix_list[p]

            self.set_target(this_setting.index)

            self.reset_material_and_object(
                cp.material_reset_original)

            self.main.bake_group_root.bake_scene(group_index_list)

            self.reset_material_and_object(
                cp.material_reset_bake_with_lightmap)

    # ===========================================
    def create_export_data(self, setting_index_list):

        setting_fix_list = self.get_setting_fix_list(setting_index_list)

        for p in range(0, len(setting_fix_list)):

            this_setting = setting_fix_list[p]

            self.set_target(this_setting)

            self.main.group_root.create_export_data()

    # ===========================================
    def export_object(self, setting_index_list):

        setting_fix_list = self.get_setting_fix_list(setting_index_list)

        if not utility_common.ListMethod.exist_list(setting_fix_list):
            return

        for cnt in range(0, len(setting_fix_list)):

            this_setting = setting_fix_list[cnt]

            self.set_target(this_setting.index)

            self.reset_material_and_object(
                cp.material_reset_bake_without_lightmap
            )

            this_setting.export_model()

        utility_common.IOMethod.open_directory(
            setting_fix_list[-1].export_object_dir_path)

    # ===========================================
    def export_composite_texture(self, setting_index_list):

        setting_fix_list = self.get_setting_fix_list(setting_index_list)

        if not utility_common.ListMethod.exist_list(setting_fix_list):
            return

        for cnt in range(0, len(setting_fix_list)):

            this_setting = setting_fix_list[cnt]

            self.set_target(this_setting.index)

            self.main.bake_group_root.export_composite_texture()

    # ===========================================
    def hide_all_visible_object(self):

        for this_setting in self.setting_list:

            self.set_target(this_setting.index)

            self.visible_object_root.hide_target_object()

            self.main.bake_group_root.hide_all_visible_object()

    # ===========================================
    def show_visible_object(self):

        self.set_target(self.current_index)

        self.visible_object_root.show_target_object()
        self.main.bake_group_root.show_visible_object()
