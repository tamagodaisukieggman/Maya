# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from functools import partial

import maya.cmds as cmds

from ... import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CustomMultiField(object):

    # ===============================================
    def __init__(self, label, value_info_list, **layout_edit_param):

        self.ui_layout_id = base_utility.string.get_random_string(16)
        self.ui_label_id = self.ui_layout_id + '_label'
        self.ui_value_id_list = None
        self.ui_value_label_id_list = None

        self.__value_info_list = value_info_list
        self.__value_info_index_dict = None

        self.__function_list = None
        self.__function_arg_list = None

        self.__draw()

        if layout_edit_param:
            layout_edit_param['edit'] = True
            self.apply_layout_param(**layout_edit_param)

        self.apply_label_param(e=True, label=label)

    # ===============================================
    def __draw(self):

        if not self.__value_info_list:
            self.__value_info_list = [['Text', '', '', 'textField']]

        self.__value_info_index_dict = {}
        self.ui_value_id_list = []
        self.ui_value_label_id_list = []

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_key = value_info[0]

            self.__value_info_index_dict[this_key] = count

            self.ui_value_id_list.append(
                self.ui_layout_id + '_' + this_key)

            self.ui_value_label_id_list.append(
                self.ui_layout_id + '_' + this_key + '_label')

        cmds.rowLayout(
            self.ui_layout_id, numberOfColumns=2, adj=2)

        cmds.text(self.ui_label_id, label='', align='left')

        cmds.rowLayout(
            numberOfColumns=len(self.__value_info_list), adj=1)

        count = -1
        for value_label_info in self.__value_info_list:
            count += 1

            this_key = value_label_info[0]
            this_label = value_label_info[1]
            this_value = value_label_info[2]
            this_command = value_label_info[3]

            this_ui_id = self.ui_value_id_list[count]

            cmds.rowLayout(numberOfColumns=2, adj=1)

            if this_command == 'button':

                self.apply_value_param_by_index(
                    count, label=this_label)

            else:

                cmds.text(
                    self.ui_value_label_id_list[count],
                    label=this_label,
                    align='right'
                )

                if this_command == 'textField' or not this_command:

                    self.apply_value_param_by_index(
                        count, text=this_value
                    )

                elif this_command == 'checkBox':

                    self.apply_value_param_by_index(
                        count, value=this_value, label=''
                    )

                else:

                    self.apply_value_param_by_index(
                        count, value=this_value
                    )

            if this_command == 'button':

                cmds.button(
                    this_ui_id, e=True, c=partial(self.__execute_function, count))

            elif this_command == 'textField':

                cmds.textField(
                    this_ui_id, e=True, tcc=partial(self.__execute_function, count))

            elif this_command == 'intField':

                cmds.intField(
                    this_ui_id, e=True, cc=partial(self.__execute_function, count))

            elif this_command == 'floatField':

                cmds.floatField(
                    this_ui_id, e=True, cc=partial(self.__execute_function, count))

            elif this_command == 'checkBox':

                cmds.checkBox(
                    this_ui_id, e=True, cc=partial(self.__execute_function, count))

            cmds.setParent('..')

        cmds.setParent('..')

        cmds.setParent('..')

    # ===============================================
    def __execute_function(self, index, value):

        if not self.__function_list:
            return

        this_function = self.__function_list[index]
        this_function_arg = self.__function_arg_list[index]

        if not this_function:
            return

        this_function(*this_function_arg)

    # ===============================================
    def set_function_by_key(self, key, function, *arg):

        if key not in self.__value_info_index_dict:
            return

        index = self.__value_info_index_dict[key]

        self.set_function_by_index(index, function, *arg)

    # ===============================================
    def set_function_by_index(self, index, function, *arg):

        if not self.__function_list:

            self.__function_list = [None] * len(self.__value_info_list)
            self.__function_arg_list = [None] * len(self.__value_info_list)

        self.__function_list[index] = function
        self.__function_arg_list[index] = arg

    # ===============================================
    def get_value_by_key(self, key):

        if key not in self.__value_info_index_dict:
            return

        index = self.__value_info_index_dict[key]

        return self.get_value_by_index(index)

    # ===============================================
    def get_value_by_index(self, index):

        this_value_info = self.__value_info_list[index]
        this_command = this_value_info[3]

        if this_command == 'button':
            return
        elif this_command == 'textField':
            return self.apply_value_param_by_index(index, q=True, text=True)

        return self.apply_value_param_by_index(index, q=True, v=True)

    # ===============================================
    def set_value_by_key(self, key, value):

        if key not in self.__value_info_index_dict:
            return

        index = self.__value_info_index_dict[key]

        self.set_value_by_index(index, value)

    # ===============================================
    def set_value_by_index(self, index, value):

        this_value_info = self.__value_info_list[index]
        this_command = this_value_info[3]

        if this_command == 'button':
            return
        elif this_command == 'textField':
            self.apply_value_param_by_index(index, e=True, text=value)
            return

        self.apply_value_param_by_index(index, e=True, v=value)

    # ===============================================
    def get_value_list(self):

        value_list = []

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_command = value_info[3]

            this_value = None
            if this_command == 'button':
                this_value = ''
            elif this_command == 'textField':
                this_value = self.apply_value_param_by_index(
                    count, q=True, text=True)
            else:
                this_value = self.apply_value_param_by_index(
                    count, q=True, v=True)

            value_list.append(this_value)

        return value_list

    # ===============================================
    def set_value_list(self, value_list):

        if not value_list:
            return

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_command = value_info[3]

            if count >= len(value_list):
                break

            if this_command == 'button':
                continue
            elif this_command == 'textField':
                self.apply_value_param_by_index(
                    count, e=True, text=value_list[count])
            else:
                self.apply_value_param_by_index(
                    count, e=True, v=value_list[count])

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
    def apply_value_param_by_key(self, key, **param):

        if key not in self.__value_info_index_dict:
            return

        index = self.__value_info_index_dict[key]

        return self.apply_value_param_by_index(index, **param)

    # ===============================================
    def apply_value_param_by_index(self, index, **param):

        this_value_info = self.__value_info_list[index]
        this_command = this_value_info[3]

        return_value = base_utility.system.exec_maya_command(
            this_command, self.ui_value_id_list[index], **param)

        return return_value

    # ===============================================
    def load_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value_list = []

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_key = value_info[0]
            this_value = value_info[2]
            this_command = value_info[3]
            this_type = str

            if this_command == 'floatField':
                this_type = float
            elif this_command == 'intField':
                this_type = int
            elif this_command == 'checkBox':
                this_type = bool

            this_value = setting.load(
                setting_key + '_' + this_key, this_type, this_value)

            this_value_list.append(this_value)

        self.set_value_list(this_value_list)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value_list = self.get_value_list()

        if not this_value_list:
            return

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_key = value_info[0]

            if count >= len(this_value_list):
                break

            setting.save(
                setting_key + '_' + this_key, this_value_list[count])
