# -*- coding: utf-8 -*-
"""description"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function


import abc

import six
from enum import Enum

from maya import cmds

from mtk.cutscene import utility


class ShotPlacementType(Enum):
    NotCreate = 0
    CurrentFrame = 1
    EndFrame = 2


@six.add_metaclass(abc.ABCMeta)
class SequencerController(object):
    @classmethod
    @abc.abstractmethod
    def set_shot(cls, cutscene_object, settings):
        pass


class CameraSequencerController(SequencerController):
    """
    現状はCameraSequencerで処理してるが、未来的にはcustomEditorに移行予定
    """

    @classmethod
    def set_shot(cls, cutscene_object, settings):
        """ショットを適用する
        :param cutscene_object: カットシーン用のカメラ
        :type cutscene_object: CutsceneCamera
        """
        if settings["shotPlacement"] == ShotPlacementType.NotCreate.value:
            return cls.create_unique_shot_name(settings["shotName"], settings["shotNumber"])

        current_sequencer = cmds.sequenceManager(query=True, writableSequencer=True)
        shot_list = cmds.ls(type="shot")
        if shot_list and settings["shotPlacement"] != ShotPlacementType.CurrentFrame.value:
            start_frame = cmds.getAttr(current_sequencer + ".maxFrame") + 1
        else:
            start_frame = cmds.sequenceManager(query=True, currentTime=True)

        end_frame = start_frame + settings["endTime"]

        unique_name = cls.create_unique_shot_name(settings["shotName"], settings["shotNumber"])

        shot_object_name = cmds.shot(startTime=start_frame,
                                     endTime=end_frame,
                                     sequenceStartTime=start_frame,
                                     sequenceEndTime=end_frame,
                                     currentCamera=cutscene_object.get_name(),
                                     shotName=unique_name)

        cmds.rename(shot_object_name, unique_name)
        return unique_name

    @classmethod
    def create_unique_shot_name(cls, base_name, target_number):
        """固有のShot名を作成する

        :param base_name: 生成する名前のベース名
        :type base_name: str
        :return: 存在しなければ、base_name, 存在していれば、[base_name]_[1, 2 ,3etc]
        :rtype: str
        """
        similar_object_list = cmds.ls(type="shot")
        similar_shot_name_list = [cmds.shot(_, query=True, shotName=True) for _ in similar_object_list]
        count_up_number = cls.__count_up_name(base_name, target_number, similar_shot_name_list)

        return base_name + count_up_number

    @classmethod
    def __count_up_name(cls, name, number, target_list):
        number_identifyer = utility.NumberIdentifyer(name, number)
        count_up_number = number_identifyer.identify__max_number_from_file_name(target_list)
        return count_up_number
