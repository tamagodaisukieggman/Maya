# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

from ..utility import common as utility_common
from ..utility import attribute as utility_attribute


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ParamItem(object):

    # ===========================================
    def __init__(self):

        self.parent = None

        self.target = None

        self.ui_prefix = None
        self.attr_prefix = None

        self.name = None
        self.type = None
        self.value = None
        self.ui_label = None
        self.ui_type = None

        self.function = None
        self.function_arg = None

        self.create_ui = False

    # ===========================================
    def initialize(self):

        self.create_ui = True

        if self.ui_label is None or self.ui_label == '':
            self.create_ui = False

    # ===========================================
    def set_target(self, target):

        self.target = None

        if target is None:
            return

        if not cmds.objExists(target):
            return

        self.target = target

    # ===========================================
    def exist_attr(self):

        return utility_attribute.Method.exist_attr(
            self.target, self.attr_prefix + self.name)

    # ===========================================
    def add_attr(self):

        if self.type == 'list':

            if self.ui_type is None:
                return

            elif self.ui_type[0] == 'radio':

                utility_attribute.Method.add_attr(
                    self.target,
                    self.attr_prefix + self.name,
                    self.attr_prefix + self.name,
                    'string',
                    self.value
                )

        else:

            utility_attribute.Method.add_attr(
                self.target,
                self.attr_prefix + self.name,
                self.attr_prefix + self.name,
                self.type,
                self.value
            )

    # ===========================================
    def get_attr_value(self):

        self.add_attr()

        return utility_attribute.Method.get_attr(
            self.target,
            self.attr_prefix + self.name,
            self.type)

    # ===========================================
    def set_attr_value(self, value):

        self.add_attr()

        utility_attribute.Method.set_attr(
            self.target,
            self.attr_prefix + self.name,
            self.type,
            value)

    # ===========================================
    def set_attr_prefix(self, attr_prefix):

        self.add_attr()

        self.attr_prefix = attr_prefix

    # ===========================================
    def get_attr_name(self):

        self.add_attr()

        return self.attr_prefix + self.name

    # ===========================================
    def draw_ui(self):

        if self.ui_label is None:
            return

        if self.exist_ui():
            return

        if self.type == 'string':

            cmds.textFieldGrp(self.ui_prefix + self.name,
                              label=self.ui_label,
                              cal=[1, 'left'],
                              adj=2,
                              cc=self.execute_function,
                              fcc=True)

        elif self.type == 'int':

            if self.ui_type is None:

                cmds.intFieldGrp(
                    self.ui_prefix + self.name,
                    label=self.ui_label,
                    cal=[1, 'left'],
                    adj=2,
                    cc=self.execute_function
                )

            elif self.ui_type[0] == 'slider':

                cmds.intSliderGrp(
                    self.ui_prefix + self.name,
                    label=self.ui_label,
                    field=True,
                    cal=[1, 'left'],
                    adj=3,
                    minValue=self.ui_type[1],
                    maxValue=self.ui_type[2],
                    fieldMinValue=self.ui_type[3],
                    fieldMaxValue=self.ui_type[4],
                    cc=self.execute_function
                )

        elif self.type == 'float':

            if self.ui_type is None:

                cmds.floatFieldGrp(
                    self.ui_prefix + self.name,
                    label=self.ui_label,
                    cal=[1, 'left'],
                    adj=2,
                    cc=self.execute_function
                )

            elif self.ui_type[0] == 'slider':

                cmds.floatSliderGrp(
                    self.ui_prefix + self.name,
                    label=self.ui_label,
                    field=True,
                    cal=[1, 'left'],
                    adj=3,
                    precision=4,
                    minValue=self.ui_type[1],
                    maxValue=self.ui_type[2],
                    fieldMinValue=self.ui_type[3],
                    fieldMaxValue=self.ui_type[4],
                    cc=self.execute_function
                )

        elif self.type == 'bool':

            cmds.checkBoxGrp(self.ui_prefix + self.name,
                             label=self.ui_label,
                             cal=[1, 'left'],
                             adj=2,
                             cc=self.execute_function)

            if self.ui_label == '----':

                cmds.checkBoxGrp(self.ui_prefix + self.name,
                                 e=True,
                                 cw=[1, 0])

        elif self.type == 'color':

            cmds.colorSliderGrp(self.ui_prefix + self.name,
                                label=self.ui_label, cal=[1, 'left'], adj=3,
                                cc=self.execute_function)

        elif self.type == 'list':

            if self.ui_type is None:
                return

            elif self.ui_type[0] == 'radio':

                if len(self.ui_type[1]) == 2:

                    cmds.radioButtonGrp(
                        self.ui_prefix + self.name,
                        label=self.ui_label,
                        cal=[1, 'left'],
                        labelArray2=self.ui_type[1],
                        numberOfRadioButtons=len(self.ui_type[1]),
                        cc=self.execute_function
                    )

                if len(self.ui_type[1]) == 3:

                    cmds.radioButtonGrp(
                        self.ui_prefix + self.name,
                        label=self.ui_label,
                        cal=[1, 'left'],
                        labelArray3=self.ui_type[1],
                        numberOfRadioButtons=len(self.ui_type[1]),
                        cc=self.execute_function
                    )

    # ===========================================
    def exist_ui(self):

        if self.type == 'string':

            return cmds.textFieldGrp(self.ui_prefix + self.name, exists=True)

        elif self.type == 'int':

            if self.ui_type is None:
                return cmds.intFieldGrp(self.ui_prefix + self.name,
                                        exists=True)

            elif self.ui_type[0] == 'slider':
                return cmds.intSliderGrp(self.ui_prefix + self.name,
                                         exists=True)

        elif self.type == 'float':

            if self.ui_type is None:
                return cmds.floatFieldGrp(self.ui_prefix + self.name,
                                          exists=True)

            elif self.ui_type[0] == 'slider':
                return cmds.floatSliderGrp(self.ui_prefix + self.name,
                                           exists=True)

        elif self.type == 'bool':

            return cmds.checkBoxGrp(self.ui_prefix + self.name,
                                    exists=True)

        elif self.type == 'color':

            return cmds.colorSliderGrp(self.ui_prefix + self.name,
                                       exists=True)

        elif self.type == 'list':

            if self.ui_type is None:
                return False

            elif self.ui_type[0] == 'radio':

                return cmds.radioButtonGrp(self.ui_prefix + self.name,
                                           exists=True)

    # ===========================================
    def get_ui_value(self):

        if not self.exist_ui():
            return

        this_value = None

        if self.type == 'string':

            this_value = cmds.textFieldGrp(
                self.ui_prefix + self.name, q=True, text=True)

        elif self.type == 'int':

            if self.ui_type is None:
                this_value = cmds.intFieldGrp(
                    self.ui_prefix + self.name, q=True, value1=True)

            elif self.ui_type[0] == 'slider':
                this_value = cmds.intSliderGrp(
                    self.ui_prefix + self.name, q=True, value=True)

        elif self.type == 'float':

            if self.ui_type is None:
                this_value = cmds.floatFieldGrp(
                    self.ui_prefix + self.name, q=True, value1=True)

            elif self.ui_type[0] == 'slider':
                this_value = cmds.floatSliderGrp(
                    self.ui_prefix + self.name, q=True, value=True)

        elif self.type == 'bool':

            this_value = cmds.checkBoxGrp(
                self.ui_prefix + self.name, q=True, value1=True)

        elif self.type == 'color':

            this_value = cmds.colorSliderGrp(
                self.ui_prefix + self.name, q=True, rgb=True)

        elif self.type == 'list':

            if self.ui_type is None:
                this_value = this_value

            elif self.ui_type[0] == 'radio':

                select_index = cmds.radioButtonGrp(
                    self.ui_prefix + self.name, q=True, select=True)
                this_value = self.ui_type[1][select_index]

        return this_value

    # ===========================================
    def enable_ui(self, enable):

        if not self.exist_ui():
            return

        if self.type == 'string':
            cmds.textFieldGrp(self.ui_prefix + self.name,
                              e=True, enable=enable)

        elif self.type == 'int':

            if self.ui_type is None:
                cmds.intFieldGrp(self.ui_prefix + self.name,
                                 e=True, enable=enable)

            elif self.ui_type[0] == 'slider':
                cmds.intSliderGrp(self.ui_prefix + self.name,
                                  e=True, enable=enable)

        elif self.type == 'float':

            if self.ui_type is None:
                cmds.floatFieldGrp(self.ui_prefix + self.name,
                                   e=True, enable=enable)

            elif self.ui_type[0] == 'slider':
                cmds.floatSliderGrp(
                    self.ui_prefix + self.name, e=True, enable=enable)

        elif self.type == 'bool':
            cmds.checkBoxGrp(self.ui_prefix + self.name, e=True, enable=enable)

        elif self.type == 'color':
            cmds.colorSliderGrp(self.ui_prefix + self.name,
                                e=True, enable=enable)

        elif self.type == 'list':

            if self.ui_type is None:
                return

            elif self.ui_type[0] == 'radio':
                cmds.radioButtonGrp(
                    self.ui_prefix + self.name, e=True, enable=enable)

    # ===========================================
    def visible_ui(self, enable):

        if not self.exist_ui():
            return

        if self.type == 'string':
            cmds.textFieldGrp(self.ui_prefix + self.name, e=True, vis=enable)

        elif self.type == 'int':

            if self.ui_type is None:
                cmds.intFieldGrp(self.ui_prefix + self.name,
                                 e=True, vis=enable)

            elif self.ui_type[0] == 'slider':
                cmds.intSliderGrp(self.ui_prefix + self.name,
                                  e=True, vis=enable)

        elif self.type == 'float':

            if self.ui_type is None:
                cmds.floatFieldGrp(
                    self.ui_prefix + self.name, e=True, vis=enable)

            elif self.ui_type[0] == 'slider':
                cmds.floatSliderGrp(
                    self.ui_prefix + self.name, e=True, vis=enable)

        elif self.type == 'bool':
            cmds.checkBoxGrp(self.ui_prefix + self.name, e=True, vis=enable)

        elif self.type == 'color':
            cmds.colorSliderGrp(self.ui_prefix + self.name, e=True, vis=enable)

        elif self.type == 'list':

            if self.ui_type is None:
                return

            elif self.ui_type[0] == 'radio':
                cmds.radioButtonGrp(
                    self.ui_prefix + self.name, e=True, vis=enable)

    # ===========================================
    def execute_function(self, value):

        if self.function is None:
            return

        if self.function_arg is None:
            self.function()
            return

        self.function(self.function_arg)

    # ===========================================
    def set_attr_from_ui(self):

        if self.target is None:
            return

        if not self.create_ui:
            return

        if not self.exist_ui():
            return

        self.add_attr()

        if self.type == 'string':

            this_value = cmds.textFieldGrp(
                self.ui_prefix + self.name, q=True, text=True)

            cmds.setAttr(self.target + '.' + self.attr_prefix +
                         self.name, this_value, type='string')

        elif self.type == 'int':

            this_value = None

            if self.ui_type is None:
                this_value = cmds.intFieldGrp(
                    self.ui_prefix + self.name, q=True, value1=True)

            elif self.ui_type[0] == 'slider':
                this_value = cmds.intSliderGrp(
                    self.ui_prefix + self.name, q=True, value=True)

            if this_value is None:
                return

            cmds.setAttr(self.target + '.' + self.attr_prefix +
                         self.name, this_value)

        elif self.type == 'float':

            this_value = None

            if self.ui_type is None:
                this_value = cmds.floatFieldGrp(
                    self.ui_prefix + self.name, q=True, value1=True)

            elif self.ui_type[0] == 'slider':
                this_value = cmds.floatSliderGrp(
                    self.ui_prefix + self.name, q=True, value=True)

            if this_value is None:
                return

            cmds.setAttr(self.target + '.' + self.attr_prefix +
                         self.name, this_value)

        elif self.type == 'bool':

            this_value = cmds.checkBoxGrp(
                self.ui_prefix + self.name, q=True, value1=True)

            cmds.setAttr(self.target + '.' + self.attr_prefix +
                         self.name, this_value)

        elif self.type == 'color':

            this_value = cmds.colorSliderGrp(
                self.ui_prefix + self.name, q=True, rgb=True)

            cmds.setAttr(self.target + '.' + self.attr_prefix + self.name,
                         this_value[0], this_value[1], this_value[2], type='float3')

        elif self.type == 'list':

            if self.ui_type is None:
                return

            elif self.ui_type[0] == 'radio':

                select_index = cmds.radioButtonGrp(
                    self.ui_prefix + self.name, q=True, select=True)

                this_value = self.ui_type[1][select_index - 1]

                cmds.setAttr(self.target + '.' + self.attr_prefix +
                             self.name, this_value, type='string')

    # ===========================================
    def set_ui_from_attr(self):

        if self.target is None:
            return

        if not self.create_ui:
            return

        if not self.exist_ui():
            return

        self.add_attr()

        if self.type == 'string':

            this_value = cmds.getAttr(
                self.target + '.' + self.attr_prefix + self.name)

            cmds.textFieldGrp(self.ui_prefix + self.name,
                              e=True, text=this_value)

        elif self.type == 'int':

            this_value = cmds.getAttr(
                self.target + '.' + self.attr_prefix + self.name)

            if self.ui_type is None:
                cmds.intFieldGrp(self.ui_prefix + self.name,
                                 e=True, value1=this_value)

            elif self.ui_type[0] == 'slider':
                cmds.intSliderGrp(self.ui_prefix + self.name,
                                  e=True, value=this_value)

        elif self.type == 'float':

            this_value = cmds.getAttr(
                self.target + '.' + self.attr_prefix + self.name)

            if self.ui_type is None:
                cmds.floatFieldGrp(self.ui_prefix + self.name,
                                   e=True, value1=this_value)

            elif self.ui_type[0] == 'slider':
                cmds.floatSliderGrp(
                    self.ui_prefix + self.name, e=True, value=this_value)

        elif self.type == 'bool':

            this_value = cmds.getAttr(
                self.target + '.' + self.attr_prefix + self.name)

            cmds.checkBoxGrp(self.ui_prefix + self.name,
                             e=True, value1=this_value)

        elif self.type == 'color':

            this_value = cmds.getAttr(
                self.target + '.' + self.attr_prefix + self.name)[0]

            cmds.colorSliderGrp(self.ui_prefix + self.name,
                                e=True, rgb=this_value)

        elif self.type == 'list':

            if self.ui_type is None:
                return

            elif self.ui_type[0] == 'radio':

                this_value = cmds.getAttr(
                    self.target + '.' + self.attr_prefix + self.name)

                target_index = 0
                for cnt in range(0, len(self.ui_type[1])):

                    if self.ui_type[1][cnt] == this_value:
                        target_index = cnt
                        break

                cmds.radioButtonGrp(self.ui_prefix + self.name,
                                    e=True, select=target_index + 1)

    # ===========================================
    def set_ui_from_custom_value(self, custom_value):

        if self.target is None:
            return

        if not self.exist_ui():
            return

        self.add_attr()

        if self.type == 'string':
            cmds.textFieldGrp(self.ui_prefix + self.name,
                              e=True, text=custom_value)

        elif self.type == 'int':

            if self.ui_type is None:
                cmds.intFieldGrp(self.ui_prefix + self.name,
                                 e=True, value1=custom_value)

            elif self.ui_type[0] == 'slider':
                cmds.intSliderGrp(self.ui_prefix + self.name,
                                  e=True, value=custom_value)

        elif self.type == 'float':

            if self.ui_type is None:
                cmds.floatFieldGrp(self.ui_prefix + self.name,
                                   e=True, value1=custom_value)

            elif self.ui_type[0] == 'slider':
                cmds.floatSliderGrp(self.ui_prefix + self.name,
                                    e=True, value=custom_value)

        elif self.type == 'bool':
            cmds.checkBoxGrp(self.ui_prefix + self.name,
                             e=True, value1=custom_value)

        elif self.type == 'color':
            cmds.colorSliderGrp(self.ui_prefix + self.name,
                                e=True, rgb=custom_value)

        elif self.type == 'list':

            if self.ui_type is None:
                return

            elif self.ui_type[0] == 'radio':

                target_index = 0
                for cnt in range(0, len(self.ui_type[1])):

                    if self.ui_type[1][cnt] == custom_value:
                        target_index = cnt
                        break

                cmds.radioButtonGrp(self.ui_prefix + self.name,
                                    e=True, select=target_index)

    # ===========================================
    def get_attr(self):

        if self.target is None:
            return

        self.add_attr()

        return utility_attribute.Method.get_attr(
            self.target, self.attr_prefix + self.name, self.type)

    # ===========================================
    def set_attr(self, value):

        if self.target is None:
            return

        self.add_attr()

        utility_attribute.Method.set_attr(
            self.target, self.attr_prefix + self.name, self.type, value)
