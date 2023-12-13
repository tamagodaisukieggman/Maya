# -*- coding: utf-8 -*-
"""シーケンサーのモデル
"""
from __future__ import annotations

import os
import stat
import typing as tp

from maya import cmds
from mtk.utils import getCurrentSceneName

from .api import *


class MayaAnimationClipCalculator(object):
    """Maya用のアニメーションクリップの計算機

    フレームごとに計算を実行し、ScreenWriterのinput_factorの比率を変更していく。
    アニメーションクリップの計算のみ。トランスフォームの直接適用などは別途

    # TODO: きっと重かろう。必要であればOpenMaya, c++化検討
    """

    def calculate(self, screen_writer_list, data: tp.Dict[SequencerGroupTrackData, tp.List[EvaluatedClip]]):
        # 全ScreenWriterのInputFactorをOff
        for screen_writer in screen_writer_list:
            array_size = cmds.getAttr("{}.screen_play_data".format(screen_writer), size=True)
            for array_index in range(array_size):
                cmds.setAttr("{}.screen_play_data[{}].input_factor".format(screen_writer, array_index), 0)

        for group_data, evaluated_clips in data.items():
            factor = 1 / len(evaluated_clips)
            for evaluated_clip in evaluated_clips:
                clip: SequencerClipData = evaluated_clip.clip
                group_property = group_data.get_property()
                clip_property = clip.get_clip_property()
                screen_writer = group_property["screen_writer_path"]
                index = clip_property["event_screen_writer_index"]
                input_factor = f"{screen_writer}.screen_play_data[{index}].input_factor"
                cmds.setAttr(input_factor, factor)


class MayaTimeConfig(object):
    @classmethod
    def get_current_time(cls):
        return cmds.currentTime(query=True)

    @classmethod
    def get_min_frame(cls):
        return cmds.playbackOptions(query=True, minTime=True)

    @classmethod
    def get_start_frame(cls):
        return cmds.playbackOptions(query=True, animationStartTime=True)

    @classmethod
    def get_max_frame(cls):
        return cmds.playbackOptions(query=True, maxTime=True)

    @classmethod
    def get_end_frame(cls):
        return cmds.playbackOptions(query=True, animationEndTime=True)


def should_saving_scene():
    scene_path = getCurrentSceneName()
    if scene_path:
        return True
    else:
        return False


def show_error_dialog(message):
    cmds.confirmDialog(title="シーンを保存している必要があります", message=f"{message}")


def show_import_file_dialog(message, file_filter="*.seq"):
    file_path = cmds.fileDialog2(fileFilter=file_filter, dialogStyle=2, fileMode=1)

    if file_path:
        return file_path[0]
    else:
        return None


def save_scene():
    scene_path = getCurrentSceneName()
    if scene_path:
        cmds.file(save=True)
    else:
        raise ValueError("Not found scene.")
