# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import subprocess

import maya.cmds as cmds

try:
    # Maya2022-
    from builtins import object
except Exception:
    pass


class Util(object):

    @classmethod
    def get_target_type_obj_in_selection(cls, _type):
        """選択したオブジェクトの中で、指定したtypeのオブジェクトを取得する
        複数選択している場合、最初に取得したオブジェクトを返す

        Args:
            _type ([type]): 取得するタイプ

        Returns:
            [type]: 指定したタイプのオブジェクト or ''
        """

        selection = cmds.ls(sl=True)
        if not selection:
            return ''

        target_type_obj = ''
        for sel in selection:

            if cmds.objectType(sel) == _type:
                target_type_obj = sel
                break

            if cmds.listRelatives(selection, type=_type):
                target_type_obj = sel
                break

        return target_type_obj

    @classmethod
    def get_dir(cls):

        target_dir = cmds.fileDialog2(fileMode=3, dialogStyle=2)
        if not target_dir:
            return ''

        return target_dir[0]

    @classmethod
    def open_dir(cls, dir):

        if not os.path.exists(dir):
            return

        subprocess.Popen(
            ['explorer', dir.encode("cp932").replace("/", "\\")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    @classmethod
    def get_scene_name(cls):

        return cmds.file(q=True, sn=True)

    @classmethod
    def set_script_job(cls, event_name, cmd, window):

        cmds.scriptJob(event=[event_name, cmd], protected=True, parent=window)

    @classmethod
    def show_maya_dialog(cls, title='title', message='message'):

        cmds.confirmDialog(title=title, message=message)

    @classmethod
    def get_focus_model_panel(cls):

        focus_panel = cmds.getPanel(withFocus=True)
        if focus_panel not in cmds.getPanel(type='modelPanel'):
            return None
        return focus_panel
