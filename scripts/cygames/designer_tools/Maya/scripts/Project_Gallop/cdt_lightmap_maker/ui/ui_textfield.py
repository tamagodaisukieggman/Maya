# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class UITextField(object):

    # ===============================================
    def __init__(self, label, function=None, arg=None):

        self.function = function
        self.function_arg = arg

        self.ui_id = None
        self.ui_label_id = None

        self.__draw()

        self.set_label(label)
        self.set_function(self.function, self.function_arg)

    # ===============================================
    def __draw(self):

        cmds.rowLayout(numberOfColumns=2, adj=2)

        self.ui_label_id = cmds.text(label='', align='left')

        self.ui_id = cmds.textFieldGrp(
            label='',
            adj=2,
            cal=[1, 'left'],
            cw=[1, 0],
            tcc=self.__execute_function
        )

        cmds.setParent('..')

    # ===============================================
    def __execute_function(self, arg):

        if self.function is None:
            return

        if self.function_arg is None:
            self.function()
            return

        self.function(self.function_arg)

    # ===============================================
    def set_label(self, label):

        cmds.text(self.ui_label_id, e=True, label=label)

    # ===============================================
    def set_label_width(self, width):

        if width is None:
            return

        cmds.text(self.ui_label_id, e=True, width=width)

    # ===============================================
    def set_function(self, function, arg=None):

        self.function = function
        self.function_arg = arg

    # ===============================================
    def get_value(self):

        return cmds.textFieldGrp(self.ui_id, q=True, text=True)

    # ===============================================
    def set_value(self, value):

        cmds.textFieldGrp(self.ui_id, e=True, text=value)

    # ===============================================
    def set_editable(self, editable):

        cmds.textFieldGrp(self.ui_id, e=True, editable=editable)
