# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel


class Label(object):

    # ===============================================
    def __init__(self, label):

        self.ui_id = None

        self.label = label
        self.align = None

        self.__create_ui()

        self.set_label(label)
        self.set_align("left")

    # ===============================================
    def __create_ui(self):

        self.ui_id = cmds.text()

    # ===============================================
    def set_label(self, label):

        self.label = label

        if self.label is None:
            return

        cmds.text(self.ui_id, e=True, label=self.label)

    # ===============================================F
    def set_align(self, align):

        self.align = align

        if self.align is None:
            return

        cmds.text(self.ui_id, e=True, align=self.align)
