# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

import os

from ..utility import common as utility_common
from ..utility import attribute as utility_attribute
from ..utility import list as utility_list
from ..utility import name as utility_name

from ..ui import button as ui_button

from . import param_item_group
from . import bake_override_param
from . import bake_setting_param_list as sp
from . import bake_common_param_list as cop
from . import bake_override_param_list as ovp
from . import bake_export_object_param_list as eop

from .. import export_object


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeSetting(object):

    # ===========================================
    def __init__(self, main, setting_root, index):

        self.main = main

        self.setting_root = setting_root

        self.index = index

        self.target_name = None
        self.target = None

        self.ui_btn_select = None

        self.export_object_dir_path = None

    # ===========================================
    def initialize(self):

        self.target_name = \
            self.setting_root.setting_prefix + '{0:02d}'.format(self.index)

        self.target = self.setting_root.target + '|' + self.target_name

        if not cmds.objExists(self.target):
            utility_common.NodeMethod.create_group(
                self.target_name, self.setting_root.target)

    # ===========================================
    def initialize_later(self):

        self.setting_root.set_target(self.index)

        self.setting_root.param_item_group.set_attr_value(
            sp.get_name(sp.index), self.index)

        if not self.setting_root.param_item_group.exist_attr(sp.get_name(sp.name)):

            self.setting_root.param_item_group.set_attr_value(
                sp.get_name(sp.name),
                "setting{0:02d}".format(self.index)
            )

        self.setting_root.override_param.set_attr_value_once(
            ovp.com_bc_settingcolorsetsuffix,
            "_setting{0:02d}".format(self.index)
        )

        self.setting_root.override_param.set_attr_value_once(
            ovp.com_bt_settingtexturesuffix,
            "_setting{0:02d}".format(self.index)
        )

        self.setting_root.override_param.set_attr_value_once(
            ovp.com_bt_settingmaterialsuffix,
            "_setting{0:02d}".format(self.index)
        )

    # ===========================================
    def create_ui(self):

        cmds.rowLayout(self.main.ui_prefix + "set_List" +
                       str(self.index),
                       numberOfColumns=2, adj=2, cal=[2, "left"])

        self.ui_btn_select = ui_button.Button('Select')
        self.ui_btn_select.set_size([50, None])
        self.ui_btn_select.set_function(
            self.setting_root.change_index, self.index)

        cmds.text(self.main.ui_prefix + "set_Name" + str(self.index))

        cmds.setParent("..")

    # ===========================================
    def update_ui(self):

        self.setting_root.param_item_group.set_target(self.target)

        this_name = self.setting_root.param_item_group.get_attr_value(
            sp.get_name(sp.name))

        cmds.text(self.main.ui_prefix + "set_Name" +
                  str(self.index), e=True, label=this_name)

        if self.index == self.setting_root.current_index:
            self.activate_ui()
        else:
            self.inactivate_ui()

    # ===========================================
    def change_ui(self):

        return

    # ===========================================
    def activate_ui(self):

        cmds.rowLayout(self.main.ui_prefix + "set_List" +
                       str(self.index), e=True, bgc=cop.setting_bg_color)

    # ===========================================
    def inactivate_ui(self):

        cmds.rowLayout(self.main.ui_prefix + "set_List" +
                       str(self.index), e=True, bgc=cop.inactive_bg_color)

    # ===========================================
    def set_target(self):

        self.setting_root.param_item_group.set_target(self.target)
        self.setting_root.override_param.param_item_group.set_target(
            self.target)

    # ===========================================
    def export_model(self):

        self.setting_root.export_object_root.update_target_object_list()

        if not utility_list.Method.exist_list(
                self.setting_root.export_object_root.target_object_list):
            return

        root_dir_path = self.main.bake_common_setting.root_dir_path

        self.export_object_dir_path = \
            root_dir_path + '/' + \
            self.setting_root.override_param.get_attr_value(
                ovp.com_bc_export_object_dir_path)

        if not os.path.isdir(self.export_object_dir_path):
            os.makedirs(self.export_object_dir_path)

        for target_object in \
                self.setting_root.export_object_root.target_object_list:

            self.setting_root.export_object_root.set_target(target_object)

            exporter = export_object.ExportObject(self)

            exporter.export_dir_path = self.export_object_dir_path

            exporter.target_transform = target_object
            exporter.export_name = \
                utility_name.Method.get_short_name(
                    target_object)

            material_replace_key = \
                self.setting_root.export_object_root.\
                param_item_group.get_attr_value(
                    eop.get_name(eop.material_replace_key))

            material_replace_value = \
                self.setting_root.export_object_root.\
                param_item_group.get_attr_value(
                    eop.get_name(eop.material_replace_value))

            exporter.material_replace_name_key_list = \
                material_replace_key.split(',')

            exporter.material_replace_name_value_list = \
                material_replace_value.split(',')

            for p in range(10):

                num_string = str(p)

                this_item_enable = \
                    self.setting_root.export_object_root.\
                    param_item_group.get_attr_value(
                        eop.get_name(eop.export_item_enable) + num_string)

                this_item_name = \
                    self.setting_root.export_object_root.\
                    param_item_group.get_attr_value(
                        eop.get_name(eop.export_item_name) + num_string)

                this_item_start = \
                    self.setting_root.export_object_root.\
                    param_item_group.get_attr_value(
                        eop.get_name(eop.export_item_start_frame) + num_string)

                this_item_end = \
                    self.setting_root.export_object_root.\
                    param_item_group.get_attr_value(
                        eop.get_name(eop.export_item_end_frame) + num_string)

                exporter.add_export_object_item(
                    this_item_enable,
                    this_item_name,
                    this_item_start,
                    this_item_end
                )

            exporter.export()
