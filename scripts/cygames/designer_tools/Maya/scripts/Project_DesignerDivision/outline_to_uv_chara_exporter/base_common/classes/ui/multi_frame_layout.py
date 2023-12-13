# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from ... import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MultiFrameLayout(object):

    # ===============================================
    def __init__(self, label, is_close, lower_layout_info_dict, **layout_edit_param):

        self.ui_layout_id = base_utility.string.get_random_string(16)

        self.ui_lower_layout_id_dict = None

        self.__is_close = is_close

        self.__lower_layout_info_dict = lower_layout_info_dict

        self.__draw()

        if layout_edit_param:
            layout_edit_param['edit'] = True
            self.apply_layout_param(**layout_edit_param)

        self.apply_layout_param(e=True, cl=self.__is_close)

        if label:
            self.apply_layout_param(e=True, label=label)
        else:
            self.apply_layout_param(e=True, labelVisible=False)

    # ===============================================
    def __draw(self):

        if not self.__lower_layout_info_dict:
            self.__lower_layout_info_dict = {}

        self.ui_lower_layout_id_dict = {}

        count = -1
        for layout_info in self.__lower_layout_info_dict:
            count += 1

            this_key = None

            if 'key' in layout_info:
                this_key = layout_info['key']

            if not this_key:
                continue

            self.ui_lower_layout_id_dict[this_key] = \
                self.ui_layout_id + '_' + this_key

        cmds.frameLayout(
            self.ui_layout_id,
            cll=True, bv=True, mw=10, mh=10)

        count = -1
        for layout_info in self.__lower_layout_info_dict:
            count += 1

            this_key = None
            this_label = None
            this_close = False
            this_parent_id = None
            this_color = None

            if 'key' in layout_info:
                this_key = layout_info['key']

            if 'label' in layout_info:
                this_label = layout_info['label']

            if 'close' in layout_info:
                this_close = layout_info['close']

            if 'parent' in layout_info:
                this_parent_id = layout_info['parent']

            if 'color' in layout_info:
                this_color = layout_info['color']

            if not this_key:
                continue

            cmds.frameLayout(
                self.ui_lower_layout_id_dict[this_key],
                cll=True, bv=True, mw=10, mh=10, cl=this_close)

            if this_label:
                cmds.frameLayout(
                    self.ui_lower_layout_id_dict[this_key], e=True, label=this_label)
            else:
                cmds.frameLayout(
                    self.ui_lower_layout_id_dict[this_key], e=True, lv=False)

            if this_color:
                cmds.frameLayout(
                    self.ui_lower_layout_id_dict[this_key], e=True, backgroundColor=this_color)

            cmds.setParent('..')

            if this_parent_id:

                cmds.frameLayout(
                    self.ui_lower_layout_id_dict[this_key],
                    e=True, p=self.ui_lower_layout_id_dict[this_parent_id])

        cmds.setParent('..')

    # ===============================================
    def apply_layout_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'frameLayout', self.ui_layout_id, **param)

        return return_value

    # ===============================================
    def apply_lower_layout_param_by_key(self, key, **param):

        if key not in self.ui_lower_layout_id_dict:
            return

        return_value = base_utility.system.exec_maya_command(
            'frameLayout', self.ui_lower_layout_id_dict[key], **param)

        return return_value

    # ===============================================
    def load_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_close = setting.load(
            setting_key + '_close', bool, self.__is_close)

        self.apply_layout_param(e=True, cl=this_close)

        for layout_info in self.__lower_layout_info_dict:

            this_key = None

            if 'key' in layout_info:
                this_key = layout_info['key']

            if not this_key:
                continue

            this_close_defalut = False

            if 'close' in layout_info:
                this_close_defalut = layout_info['close']

            this_close = setting.load(
                setting_key + '_' + this_key + '_close', bool, this_close_defalut)

            this_label = None

            if 'label' in layout_info:
                this_label = layout_info['label']

            if not this_label:
                this_close = False

            self.apply_lower_layout_param_by_key(
                this_key, e=True, cl=this_close)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_close = self.apply_layout_param(q=True, cl=True)

        setting.save(setting_key + '_close', this_close)

        for layout_info in self.__lower_layout_info_dict:

            this_key = None

            if 'key' in layout_info:
                this_key = layout_info['key']

            if not this_key:
                continue

            this_close = \
                self.apply_lower_layout_param_by_key(this_key, q=True, cl=True)

            setting.save(setting_key + '_' + this_key + '_close', this_close)
