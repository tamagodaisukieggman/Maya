# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from operator import attrgetter

from maya import cmds

from shr.cutscene import utility

GROUP_SUFFIX = "_group"
AIM_SUFFIX = "_aim"

CAM_SUFFIX = "_cam"


class CameraSequencerCamera(object):
    def __init__(self, name, group_suffix, aim_suffix):
        self.name = name

        self.group_name = None
        self.group_suffix = group_suffix

        self.aim_name = None
        self.aim_suffix = aim_suffix

        self.correct__camera_property()

    def correct__camera_property(self):
        target_group_name = self.name + self.group_suffix
        if cmds.objExists(target_group_name):
            self.group_name = cmds.ls(target_group_name, type="lookAt")[0]

        target_aim_name = self.name + self.aim_suffix
        if cmds.objExists(target_aim_name):
            self.aim_name = cmds.ls(target_aim_name, type="transform")[0]

    def rename(self, name):
        cmds.rename(self.name, name)
        self.name = name

        if self.group_name:
            target_group_name = name + self.group_suffix
            cmds.rename(self.group_name, target_group_name)
            self.group_name = target_group_name

        if self.aim_name:
            target_aim_name = name + self.aim_suffix
            cmds.rename(self.aim_name, target_aim_name)
            self.aim_name = target_aim_name


class CameraSequencerShotData(object):
    def __init__(self, shot_object_name, group_suffix, aim_suffix, cam_suffix):
        self.shot_object_name = shot_object_name
        self.shot_name = None
        self.start_time = 0
        self.end_time = 0

        self.group_suffix = group_suffix
        self.aim_suffix = aim_suffix
        self.cam_suffix = cam_suffix

        self.bind_camera = None

        self.candidate_count = None
        self.sort_completed = False

        self.correct__shot_property()

    def correct__shot_property(self):
        self.shot_name = cmds.shot(self.shot_object_name, query=True, shotName=True)
        self.start_time = cmds.shot(self.shot_object_name, query=True, sequenceStartTime=True)
        self.end_time = cmds.shot(self.shot_object_name, query=True, sequenceEndTime=True)

        camera_name = cmds.shot(self.shot_object_name, query=True, currentCamera=True)
        self.bind_camera = CameraSequencerCamera(camera_name, self.group_suffix, self.aim_suffix)

    def rename(self, name, is_rename_camera):
        cmds.rename(self.shot_object_name, name)
        self.shot_object_name = name

        cmds.shot(self.shot_object_name, edit=True, shotName=name)
        self.shot_name = name

        if is_rename_camera:
            self.bind_camera.rename(name + self.cam_suffix)

    def check__can_object_rename(self, shot_name):
        if cmds.objExists(shot_name):
            return False

        if cmds.objExists(shot_name + self.cam_suffix):
            return False

        return True


def check_can__object_rename(name):
    return not cmds.objExists(name)


class ShotRenamer(object):
    def __init__(self, name_prefix, number, group_suffix, aim_suffix, cam_suffix, is_rename_camera):
        self.name_prefix = name_prefix
        self.number = int(number)
        self.digits = len(number)
        self.group_suffix = group_suffix
        self.aim_suffix = aim_suffix
        self.cam_suffix = cam_suffix
        self.is_rename_camera = is_rename_camera

    def _exec(self):
        shot_list = cmds.ls(type="shot")

        shot_data_class_list = [CameraSequencerShotData(_, self.group_suffix, self.aim_suffix, self.cam_suffix) for _ in shot_list]
        shot_data_class_list.sort(key=attrgetter("start_time"))

        for count, shot_data in enumerate(shot_data_class_list):
            shot_data.candidate_count = self.number + count

        miss_match_count = len(shot_data_class_list)

        while(miss_match_count > 0):
            for i, shot_data in enumerate(shot_data_class_list):
                # 既にソート済みならスキップ
                if shot_data.sort_completed:
                    continue

                candidate_name = self.name_prefix + utility.zero_fill(self.number + i, self.digits)
                temp_name = self.name_prefix + utility.zero_fill(self.number + i, self.digits) + "_temp"
                can_rename = shot_data.check__can_object_rename(candidate_name)

                if can_rename:
                    shot_data.rename(candidate_name, self.is_rename_camera)
                    shot_data.sort_completed = True
                    miss_match_count -= 1
                else:
                    shot_data.rename(temp_name, self.is_rename_camera)
                    shot_data.sort_completed = False


# from shr.cutscene import camerasequencer_sort_shot
# camerasequencer_sort_shot.app.main()
