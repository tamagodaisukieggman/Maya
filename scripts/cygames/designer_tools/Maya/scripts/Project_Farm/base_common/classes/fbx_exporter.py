# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import object
except:
    pass

import maya.cmds as cmds
import maya.mel as mel


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FbxExporter(object):

    # ===============================================
    def __init__(self):

        self.fbx_file_path = None
        self.target_node_list = None

        self.is_ascii = False

        self.animation_info_list = None

    # ===============================================
    def reset(self):

        self.fbx_file_path = None
        self.target_node_list = None

        self.is_ascii = False

        self.animation_info_list = None

    # ===============================================
    def add_animation(self, name, start_frame, end_frame):

        if not name:
            return

        if not self.animation_info_list:
            self.animation_info_list = []

        anim_info_dict = {}
        anim_info_dict['Name'] = name
        anim_info_dict['Start'] = start_frame
        anim_info_dict['End'] = end_frame

        self.animation_info_list.append(anim_info_dict)

    # ===============================================
    def remove_animation(self, name):

        if not self.animation_info_list:
            return

        target_anim_info_list = []

        for anim_info in self.animation_info_list:

            this_name = anim_info['Name']

            if this_name != name:
                continue

            target_anim_info_list.append(anim_info)

        for anim_info in target_anim_info_list:

            self.animation_info_list.remove(anim_info)

    # ===============================================
    def clear_animation(self):

        self.animation_info_list = None

    # ===============================================
    def export(self):

        if not self.fbx_file_path:
            return False

        if not self.target_node_list:
            return False

        cmds.select(self.target_node_list, r=True, hi=True)

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

        if self.animation_info_list:

            for anim_info in self.animation_info_list:

                this_name = anim_info['Name']
                this_start = anim_info['Start']
                this_end = anim_info['End']

                if not this_name:
                    continue

                mel.eval(
                    'FBXExportSplitAnimationIntoTakes -v "{0}" {1} {2} ;'.format(
                        this_name, this_start, this_end)
                )

        mel.eval('FBXExport -f "' + self.fbx_file_path + '" -s')

        return True
