# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds

from . import common


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Window(object):

    # ===============================================
    def __init__(self, id, title, size):

        self.ui_id = id

        self.title = title
        self.size = size

        self.__create_ui()

    # ===============================================
    def __create_ui(self):

        common.Method.check_window(self.ui_id)

        cmds.window(
            self.ui_id,
            title=self.title,
            widthHeight=(self.size[0], self.size[1]),
            s=1,
            mnb=True,
            mxb=False,
            rtf=True,
        )

    # ===============================================
    def show(self):

        cmds.showWindow(self.ui_id)
