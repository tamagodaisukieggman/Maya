# -*- coding: utf-8 -*-
"""カメラシーケンサーのショットカーソル移動機能"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import numpy as np

from maya import cmds


class CameraSequencerShotCursorMover(object):
    """カメラシーケンサーのショットカーソル移動ツール
    """
    CAMERASEQUENCER_START_TIME = ".sequenceStartFrame"
    CAMERASEQUENCER_END_TIME = ".sequenceEndFrame"

    @classmethod
    def next_key_event(cls):
        """キーの進むイベント
        """
        shot_list = cmds.ls(type="shot")
        cls.__sort_shot_list(shot_list)

        time_list = cls.__create_time_list(shot_list)

        curret_time = cmds.sequenceManager(query=True, ct=True)
        nearest_index = cls.__get_index_nearest(time_list, curret_time)

        target_index = nearest_index
        if curret_time >= time_list[nearest_index]:
            target_index = nearest_index + 1

        if len(time_list) <= nearest_index + 1:
            target_index = 0

        cmds.sequenceManager(ct=time_list[target_index])

    @classmethod
    def previous_key_event(cls):
        """キーの戻るイベント
        """
        shot_list = cmds.ls(type="shot")
        cls.__sort_shot_list(shot_list)

        time_list = cls.__create_time_list(shot_list)

        curret_time = cmds.sequenceManager(query=True, ct=True)
        nearest_index = cls.__get_index_nearest(time_list, curret_time)
        if curret_time <= time_list[nearest_index]:
            cmds.sequenceManager(ct=time_list[nearest_index - 1])
            return

        cmds.sequenceManager(ct=time_list[nearest_index])

    @classmethod
    def __sort_shot_list(cls, shot_list):
        """ショットリストをソートする

        :param shot_list: camera Sequencerのショットリスト
        :type shot_list: list
        """
        max_index = len(shot_list) - 1
        cls.__sort_shot_sublist(shot_list, 0, max_index)

    @classmethod
    def __sort_shot_sublist(cls, shot_list, left, right):
        """ショットのサブリストをソートする

        :param shot_list: camera sequencerのショットリスト
        :type shot_list: list
        :param left: 左側のindex
        :type left: int
        :param right: 右index
        :type right: int
        """
        if right > left:
            pivot_index = left
            pivot_new_index = cls.__partition_shot_list(shot_list, left, right, pivot_index)
            cls.__sort_shot_sublist(shot_list, left, pivot_new_index - 1)
            cls.__sort_shot_sublist(shot_list, pivot_new_index + 1, right)

    @classmethod
    def __partition_shot_list(cls, shot_list, left, right, pivot_index):
        pivot_name = shot_list[pivot_index]
        pivot_value = cmds.getAttr(pivot_name + cls.CAMERASEQUENCER_START_TIME)

        tmp_name = shot_list[right]
        shot_list[pivot_index] = tmp_name
        shot_list[right] = pivot_name

        store_index = left

        for index in range(left, right):
            index_value = cmds.getAttr(shot_list[index] + cls.CAMERASEQUENCER_START_TIME)
            if index_value <= pivot_value:
                tmp_name = shot_list[index]
                shot_list[index] = shot_list[store_index]
                shot_list[store_index] = tmp_name
                store_index += 1

        tmp_name = shot_list[right]
        shot_list[right] = shot_list[store_index]
        shot_list[store_index] = tmp_name
        return store_index

    @classmethod
    def __create_time_list(cls, shot_list):
        time_list = []
        for shot_name in shot_list:
            time_list.append(cmds.getAttr(shot_name + cls.CAMERASEQUENCER_START_TIME))
            time_list.append(cmds.getAttr(shot_name + cls.CAMERASEQUENCER_END_TIME))

        time_list.sort()
        return time_list

    @classmethod
    def __get_index_nearest(cls, data, value):
        """配列の中の値に近いindexを取得する
        """
        idx = np.argmin(np.abs(np.array(data) - value))
        return idx
