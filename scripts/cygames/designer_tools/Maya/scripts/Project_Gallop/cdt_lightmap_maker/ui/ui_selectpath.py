# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

import os


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class UISelectPath(object):

    # ===============================================
    def __init__(self, label, is_folder=False, function=None, arg=None):

        self.function = function
        self.function_arg = arg

        self.is_folder = is_folder
        self.file_filter = None

        self.ui_id = None
        self.ui_label_id = None

        self.__draw()

        self.set_label(label)
        self.set_file_filter(None)
        self.set_function(self.function, self.function_arg)

    # ===============================================
    def __draw(self):

        cmds.rowLayout(numberOfColumns=2, adj=2)

        self.ui_label_id = cmds.text(label='', align='left')

        self.ui_id = cmds.textFieldButtonGrp(
            label='',
            adj=2,
            buttonLabel=u'選択',
            cal=[1, 'left'],
            cw=[1, 0],
            cc=self.__execute_function,
            bc=self.__on_select_button
        )

        cmds.setParent('..')

    # ===============================================
    def __on_select_button(self):

        if self.is_folder:
            self.__select_folder_path()
        else:
            self.__select_file_path()

        self.__execute_function(None)

    # ===============================================
    def __select_folder_path(self):

        select_dir_path = cmds.fileDialog2(
            dialogStyle=2,
            fileMode=3,
            cap='Select Folder',
            okc='Select'
        )

        if select_dir_path is None:
            return

        if len(select_dir_path) == 0:
            return

        select_dir_path = select_dir_path[0]

        self.set_path(select_dir_path)

    # ===============================================
    def __select_file_path(self):

        select_file_path = cmds.fileDialog2(
            dialogStyle=2,
            fileMode=1,
            cap='Select File',
            okc='Select',
            fileFilter=self.file_filter
        )

        if select_file_path is None:
            return

        if len(select_file_path) == 0:
            return

        select_file_path = select_file_path[0]

        self.set_path(select_file_path)

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
    def set_path(self, path):

        cmds.textFieldButtonGrp(self.ui_id, e=True, text='')

        if self.is_folder:
            if os.path.isdir(path):
                cmds.textFieldButtonGrp(self.ui_id, e=True, text=path)
        else:
            if os.path.isfile(path):
                cmds.textFieldButtonGrp(self.ui_id, e=True, text=path)

    # ===============================================
    def get_path(self):

        target_path = cmds.textFieldButtonGrp(self.ui_id, q=True, text=True)

        return target_path

    # ===============================================
    def set_file_filter(self, file_filter):

        if file_filter is None:
            self.file_filter = 'All Files (*.*)'
            return

        self.file_filter = file_filter
