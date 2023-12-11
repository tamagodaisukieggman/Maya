# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import os

import maya.cmds as cmds
import maya.mel as mel

from ..utility import common as utility_common

from . import bake_override_param_list as ovp
from . import bake_common_param_list as cp

from . import param_item_group
from . import bake_override_param


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeCommonSetting(object):

    # ===========================================
    def __init__(self, main):

        self.main = main

        self.target_name = None
        self.target = None

        self.param_item_group = None
        self.override_param = None

        self.project_dir_path = None
        self.root_dir_path = None

        self.is_init = False

    # ===========================================
    def initialize(self):

        self.is_init = False

        self.target = self.main.target + '|' + self.target_name

        if not cmds.objExists(self.target):
            utility_common.NodeMethod.create_group(
                self.target_name, self.main.target)

        self.param_item_group = param_item_group.ParamItemGroup()
        self.param_item_group.target = self.target
        self.param_item_group.attr_prefix = self.main.attr_prefix + 'com_'
        self.param_item_group.ui_prefix = self.main.ui_prefix + 'com_'
        self.param_item_group.function = self.main.change_ui

        self.param_key_list = []

        self.param_key_list.append(cp.current_setting_index)
        self.param_key_list.append(cp.current_group_index)

        for key in self.param_key_list:

            self.param_item_group.add_item(
                cp.get_name(key),
                cp.get_type(key),
                cp.get_value(key),
                cp.get_ui_label(key),
                cp.get_ui_type(key)
            )

        self.override_param = bake_override_param.BakeOverrideParam()
        self.override_param.main = self.main
        self.override_param.target = self.target
        self.override_param.attr_prefix = self.main.attr_prefix + "com_ovp_"
        self.override_param.ui_prefix = self.main.ui_prefix + "com_ovp_"

        self.override_param.initialize()

        self.initialize_later()

        self.update_root_dir_path()

        self.is_init = True

    # ===========================================
    def initialize_later(self):

        self.override_param.set_attr_value_once(
            ovp.com_bt_settingmaterialsuffix,
            ""
        )

        self.override_param.set_attr_value_once(
            ovp.com_bt_groupmaterialsuffix,
            ""
        )

        self.override_param.set_attr_value_once(
            ovp.com_bt_settingtexturesuffix,
            ""
        )

        self.override_param.set_attr_value_once(
            ovp.com_bt_grouptexturesuffix,
            ""
        )

        self.override_param.set_attr_value_once(
            ovp.com_bc_settingcolorsetsuffix,
            ""
        )

        self.override_param.set_attr_value_once(
            ovp.com_bc_groupcolorsetsuffix,
            ""
        )

    # ===========================================
    def create_ui(self):

        cmds.columnLayout(adj=True, co=['both', 10])

        self.override_param.create_ui()

        cmds.setParent('..')

    # ===========================================
    def create_ui_later(self):

        self.override_param.visible_ui(ovp.com_bc_settingcolorsetsuffix, False)
        self.override_param.visible_ui(ovp.com_bt_settingmaterialsuffix, False)
        self.override_param.visible_ui(ovp.com_bt_settingtexturesuffix, False)

        self.override_param.visible_ui(ovp.com_bc_groupcolorsetsuffix, False)
        self.override_param.visible_ui(ovp.com_bt_groupmaterialsuffix, False)
        self.override_param.visible_ui(ovp.com_bt_grouptexturesuffix, False)

    # ===========================================
    def update_ui(self):

        self.override_param.update_ui()

    # ===========================================
    def change_ui(self):

        self.override_param.change_ui()

    # ===========================================
    def update_root_dir_path(self):

        self.project_dir_path = cmds.workspace(q=True, rootDirectory=True)
        self.root_dir_path = None

        if not os.path.exists(self.project_dir_path):
            self.project_dir_path = None
            return

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

                        parent_dir_path = os.path.abspath(
                            os.path.dirname(parent_dir_path))
                        parent_dir_name = os.path.basename(parent_dir_path)

                        if parent_dir_name.lower() == 'scenes':

                            self.root_dir_path = os.path.dirname(
                                parent_dir_path)
                        else:

                            self.root_dir_path = parent_dir_path

        if not os.path.exists(self.root_dir_path):
            self.root_dir_path = None
