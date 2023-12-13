# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel


class IconButton(object):

    # ===============================================
    def __init__(self,
                 image=None,
                 label=None,
                 annotation=None,
                 size=None,
                 bgcolor=None,
                 function=None,
                 arg=None):

        self.ui_id = None

        self.image = image
        self.label = label
        self.annotation = annotation

        self.size = size
        self.bgcolor = bgcolor
        self.function = function
        self.function_arg = arg

        self.__create_ui()

        self.set_image(self.image)
        self.set_label(self.label)
        self.set_annotation(self.annotation)
        self.set_size(self.size)
        self.set_bgcolor(self.bgcolor)
        self.set_function(self.function, self.function_arg)

    # ===============================================
    def __create_ui(self):

        self.ui_id = cmds.shelfButton(
            style='iconOnly', c=self.__execute_function)

    # ===============================================
    def __execute_function(self):

        if self.function is None:
            return

        if self.function_arg is None:
            self.function()
            return

        self.function(self.function_arg)

    # ===============================================
    def set_function(self, function, arg=None):

        self.function = function
        self.function_arg = arg

    # ===============================================
    def set_image(self, image):

        self.image = image

        if self.image is None:
            return

        cmds.shelfButton(self.ui_id, e=True, image1=self.image)

    # ===============================================
    def set_bgcolor(self, bgcolor):

        self.bgcolor = bgcolor

        if self.bgcolor is None:
            return

        cmds.shelfButton(self.ui_id, e=True, bgc=self.bgcolor)

    # ===============================================
    def set_annotation(self, annotation):

        self.annotation = annotation

        if self.annotation is None:
            return

        cmds.shelfButton(self.ui_id, e=True, ann=self.annotation)

    # ===============================================
    def set_size(self, size):

        self.size = size

        if self.size is None:
            return

        cmds.shelfButton(self.ui_id, e=True,
                         width=self.size[0], height=self.size[1])

    # ===============================================
    def set_label(self, label):

        self.label = label

        if self.label is None:
            cmds.shelfButton(self.ui_id, e=True, style="iconOnly")
            return

        cmds.shelfButton(self.ui_id, e=True, style="iconAndTextHorizontal")

        cmds.shelfButton(self.ui_id, e=True, iol=self.label)
        cmds.shelfButton(self.ui_id, e=True, olc=(1, 1, 1))
        cmds.shelfButton(self.ui_id, e=True, olb=(0.1, 0.1, 0.1, 0.7))
