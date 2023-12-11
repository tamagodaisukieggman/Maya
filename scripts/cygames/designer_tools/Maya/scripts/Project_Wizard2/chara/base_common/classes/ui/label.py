# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from ... import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Label(object):

    # ===============================================
    def __init__(self, label, **label_edit_param):

        self.ui_label_id = base_utility.string.get_random_string(16)

        self.__draw()

        if label_edit_param:
            label_edit_param['edit'] = True
            self.apply_label_param(**label_edit_param)

        self.apply_label_param(e=True, label=label, align='left')

    # ===============================================
    def __draw(self):

        cmds.text(self.ui_label_id)

    # ===============================================
    def get_value(self, value):

        return self.apply_label_param(q=True, label=True)

    # ===============================================
    def set_value(self, value):

        self.apply_label_param(e=True, label=value)

    # ===============================================
    def apply_label_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'text', self.ui_label_id, **param)

        return return_value
