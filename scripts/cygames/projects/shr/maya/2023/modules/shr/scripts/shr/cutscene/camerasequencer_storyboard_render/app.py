# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os

from maya import cmds
from shr.utils import getCurrentSceneFilePath


class StorybardRender(object):
    def collect_clip_info_from_camerasequencer(self):
        """カメラシーケンサーのクリップ情報を収集する
        """
        clip_info_list = []
        shot_list = cmds.sequenceManager(listShots=True)
        for shot in shot_list:
            info_dict = dict()
            info_dict["name"] = shot
            info_dict["startTime"] = cmds.shot(shot, query=True, startTime=True)
            info_dict["endTime"] = cmds.shot(shot, query=True, endTime=True)
            clip_info_list.append(info_dict)

        return clip_info_list

    def collect_clip_info_from_camerasequencer_current_frame(self):
        shot_name = cmds.sequenceManager(query=True, currentShot=True)
        if not shot_name:
            return

        shot_info = dict()
        shot_info["name"] = shot_name
        shot_info["startTime"] = cmds.sequenceManager(query=True, currentTime=True)
        shot_info["endTime"] = cmds.sequenceManager(query=True, currentTime=True)

        return shot_info

    def get_scene_name(self):
        scene_base_name = os.path.basename(getCurrentSceneFilePath())
        scene_base_name_no_extension = os.path.splitext(scene_base_name)[0]
        return scene_base_name_no_extension
