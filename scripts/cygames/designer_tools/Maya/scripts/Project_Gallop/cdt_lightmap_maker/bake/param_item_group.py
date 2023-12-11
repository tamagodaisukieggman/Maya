# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

from . import param_item


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ParamItemGroup(object):

    # ===========================================
    def __init__(self):

        self.target = None

        self.attr_prefix = None

        self.ui_prefix = None

        self.function = None

        self.function_arg = None

        self.param_item_list = None

    # ===========================================
    def add_item(self, name, type, value, ui_label, ui_type):

        new_param_item = param_item.ParamItem()

        new_param_item.parent = self
        new_param_item.target = self.target

        new_param_item.attr_prefix = self.attr_prefix
        new_param_item.ui_prefix = self.ui_prefix

        new_param_item.function = self.function
        new_param_item.function_arg = self.function_arg

        new_param_item.name = name
        new_param_item.type = type
        new_param_item.value = value
        new_param_item.ui_label = ui_label
        new_param_item.ui_type = ui_type

        new_param_item.initialize()

        if self.param_item_list is None:
            self.param_item_list = []

        self.param_item_list.append(new_param_item)

    # ===========================================
    def set_target(self, target):

        self.target = target

        for param_item in self.param_item_list:
            param_item.set_target(target)

    # ===========================================
    def set_attr_prefix(self, target_name, attr_prefix):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        target_param.set_attr_prefix(attr_prefix)

    # ===========================================
    def set_attr_prefix_all(self, attr_prefix):

        self.attr_prefix = attr_prefix

        for param_item in self.param_item_list:
            param_item.set_attr_prefix(self.attr_prefix)

    # ===========================================
    def get_param_item(self, target_name):

        for param_item in self.param_item_list:

            if param_item.name != target_name:
                continue

            return param_item

    # ===========================================
    def exist_attr(self, target_name):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return False

        return target_param.exist_attr()

    # ===========================================
    def add_attr(self):

        for param_item in self.param_item_list:
            param_item.add_attr()

    # ===========================================
    def get_attr_value(self, target_name):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        return target_param.get_attr_value()

    # ===========================================
    def set_attr_value(self, target_name, value):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        target_param.set_attr_value(value)

    # ===========================================
    def get_attr_name(self, target_name):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        return target_param.get_attr_name()

    # ===========================================
    def draw_ui(self, target_name):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        target_param.draw_ui()

    # ===========================================
    def set_attr_from_ui_all(self):

        for param_item in self.param_item_list:
            param_item.set_attr_from_ui()

    # ===========================================
    def set_attr_from_ui(self, target_name):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        target_param.set_attr_from_ui()

    # ===========================================
    def set_ui_from_attr(self):

        for param_item in self.param_item_list:
            param_item.set_ui_from_attr()

    # ===========================================
    def set_ui_from_attr_all(self):

        for param_item in self.param_item_list:
            param_item.set_ui_from_attr()

    # ===========================================
    def get_ui_value(self, target_name):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        return target_param.get_ui_value()

    # ===========================================
    def enable_ui(self, target_name, enable):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        target_param.enable_ui(enable)

    # ===========================================
    def visible_ui(self, target_name, visible):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        target_param.visible_ui(visible)

    # ===========================================
    def set_ui_from_custom_value(self, target_name, custom_value):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        target_param.set_ui_from_custom_value(custom_value)

    # ===========================================
    def get_attr(self, target_name):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        return target_param.get_attr()

    # ===========================================
    def set_attr(self, target_name, value):

        target_param = self.get_param_item(target_name)

        if target_param is None:
            return

        target_param.set_attr(value)
