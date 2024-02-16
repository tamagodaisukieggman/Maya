# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from ... import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RadioButton(object):

    # ===============================================
    def __init__(self, label, value_info_list, on_label, **layout_edit_param):

        self.ui_layout_id = base_utility.string.get_random_string(16)
        self.ui_label_id = self.ui_layout_id + '_label'
        self.ui_radio_collection_id = self.ui_layout_id + '_radio_collection'
        self.ui_radio_button_id_list = None

        self.__value_info_list = value_info_list

        self.__default_value = on_label

        self.__change_function = None
        self.__change_function_arg = None

        self.__draw()

        if layout_edit_param:
            layout_edit_param['edit'] = True
            self.apply_layout_param(**layout_edit_param)

        self.apply_label_param(e=True, label=label)
        self.set_value(self.__default_value)

    # ===============================================
    def __draw(self):

        if not self.__value_info_list:
            self.__value_info_list = [
                'on', 'off'
            ]

        self.ui_radio_button_id_list = []

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            self.ui_radio_button_id_list.append(
                self.ui_layout_id + '_radioButton' + str(count))

        cmds.rowLayout(
            self.ui_layout_id, numberOfColumns=2, adj=2)

        cmds.text(self.ui_label_id, label='', align='left')

        cmds.rowLayout(
            numberOfColumns=len(self.__value_info_list) + 1, adj=1)

        cmds.text(label='', align='right')

        cmds.radioCollection(self.ui_radio_collection_id)

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            cmds.rowLayout(numberOfColumns=1, adj=1)

            cmds.radioButton(
                self.ui_radio_button_id_list[count], label=value_info,
                cc=self.__execute_change_function
            )

            cmds.setParent('..')

        cmds.setParent('..')

        cmds.setParent('..')

    # ===============================================
    def __execute_change_function(self, value):

        if self.__change_function is None:
            return

        self.__change_function(*self.__change_function_arg)

    # ===============================================
    def set_change_function(self, function, *arg):

        self.__change_function = function
        self.__change_function_arg = arg

    # ===============================================
    def get_index(self):

        ui_radio_button_id = \
            self.apply_radio_collection_param(q=True, select=True)

        count = -1
        for radio_button_id in self.ui_radio_button_id_list:
            count += 1

            if radio_button_id == ui_radio_button_id:
                return count

        return -1

    # ===============================================
    def get_value(self):

        ui_radio_button_id = \
            self.apply_radio_collection_param(q=True, select=True)

        count = -1
        for radio_button_id in self.ui_radio_button_id_list:
            count += 1

            if radio_button_id == ui_radio_button_id:

                this_label = cmds.radioButton(radio_button_id, q=True, l=True)

                return this_label

        return None

    # ===============================================
    def set_index(self, index):

        ui_radio_button_id = self.ui_radio_button_id_list[index]

        self.apply_radio_collection_param(e=True, select=ui_radio_button_id)

    # ===============================================
    def set_value(self, value):

        count = -1
        for radio_button_id in self.ui_radio_button_id_list:
            count += 1

            this_label = cmds.radioButton(radio_button_id, q=True, l=True)

            if this_label != value:
                continue

            self.apply_radio_collection_param(e=True, select=radio_button_id)
            break

    # ===============================================
    def apply_layout_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'rowLayout', self.ui_layout_id, **param)

        return return_value

    # ===============================================
    def apply_label_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'text', self.ui_label_id, **param)

        return return_value

    # ===============================================
    def apply_radio_collection_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'radioCollection', self.ui_radio_collection_id, **param)

        return return_value

    # ===============================================
    def apply_radio_button_param(self, index, **param):

        return_value = base_utility.system.exec_maya_command(
            'radioButton', self.ui_radio_button_id_list[index], **param)

        return return_value

    # ===============================================
    def load_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value = setting.load(
            setting_key + '_value', str, self.__default_value)

        self.set_value(this_value)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value = self.get_value()

        setting.save(setting_key + '_value', this_value)
