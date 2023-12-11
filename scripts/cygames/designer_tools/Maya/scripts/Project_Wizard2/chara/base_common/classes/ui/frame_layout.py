# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from ... import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FrameLayout(object):

    # ===============================================
    def __init__(self, label, is_close, **frame_layout_edit_param):

        self.ui_layout_id = base_utility.string.get_random_string(16)

        self.__is_close = is_close

        self.__draw()

        if frame_layout_edit_param:
            frame_layout_edit_param['edit'] = True
            self.apply_frame_layout_param(**frame_layout_edit_param)

        self.apply_frame_layout_param(e=True, label=label, cl=self.__is_close)

    # ===============================================
    def __draw(self):

        cmds.frameLayout(
            self.ui_layout_id,
            cll=True, bv=True, mw=10, mh=10)

        cmds.setParent('..')

    # ===============================================
    def apply_frame_layout_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'frameLayout', self.ui_layout_id, **param)

        return return_value

    # ===============================================
    def load_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value = setting.load(
            setting_key + '_Close', bool, self.__is_close)

        self.apply_frame_layout_param(e=True, cl=this_value)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value = self.apply_frame_layout_param(q=True, cl=True)

        setting.save(setting_key + '_Close', this_value)
