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
class FbxExporter(object):

    # ===============================================
    def __init__(self):

        self.fbx_file_path = None
        self.target_list = None

        self.is_ascii = False

    # ===============================================
    def export(self):

        if self.fbx_file_path is None:
            return False

        if self.target_list is None:
            return False

        if len(self.target_list) == 0:
            return False

        fix_target_list = []
        for target in self.target_list:

            if not cmds.objExists(target):
                continue

            fix_target_list.append(target)

        if len(fix_target_list) == 0:
            return

        self.fbx_file_path = self.fbx_file_path.replace('\\', '/')

        cmds.select(fix_target_list, r=True)
        cmds.select(hi=True)

        return self.export_fbx_for_model()

    # ===============================================
    def export_fbx_for_model(self):

        mel.eval('FBXResetExport')

        mel.eval('FBXExportAnimationOnly -v false ;')

        mel.eval('FBXExportCameras -v false ;')

        mel.eval('FBXExportLights -v false ;')

        mel.eval('FBXExportInputConnections  -v false ;')

        mel.eval('FBXExportFileVersion -v FBX201300 ;')

        if self.is_ascii:
            mel.eval('FBXExportInAscii -v true ;')
        else:
            mel.eval('FBXExportInAscii -v false ;')

        mel.eval('FBXExport -f "' + self.fbx_file_path + '" -s')

        return True
