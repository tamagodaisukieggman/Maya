# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from PySide2 import QtCore

from maya import cmds

from .. import utility


class CameraSequencerRangeSliderSyncer(object):
    def __init__(self):
        self.__camera_sequencer = cmds.getPanel(withLabel="Camera Sequencer")
        self.__camera_sequencer_ed = self.__camera_sequencer + "SequenceEditor"

        self.__time_editor = cmds.getPanel(withLabel="Time Editor")
        self.__time_editor_ed = self.__time_editor + "TimeEd"

        self.__graph_editor = cmds.getPanel(withLabel="Graph Editor")
        self.__graph_editor_ed = self.__graph_editor + "GraphEd"

        self.__dop_sheet = cmds.getPanel(withLabel="Dope Sheet")
        self.__dop_sheet_ed = self.__dop_sheet + "DopeSheetEd"

    def __is_showed(self, panel_name):
        """表示されているか

        :param panel_name: 確認したPanel名
        :type panel_name: str
        :return: 表示されているか
        :rtype: bool
        """
        is_control = cmds.panel(panel_name, query=True, control=True)

        return is_control

    def __get_shotnode_time_range(self):
        shot_list = cmds.ls(type="shot")

        if shot_list == []:
            min_time = cmds.playbackOptions(query=True, minTime=True)
            max_time = cmds.playbackOptions(query=True, maxTime=True)
            return min_time, max_time

        time_list = []
        for shot_node in shot_list:
            time_list.append(cmds.shot(shot_node, query=True, startTime=True))
            time_list.append(cmds.shot(shot_node, query=True, endTime=True))

        return min(time_list), max(time_list)

    def sync__time_editor_time_range__from_camera_sequencer(self):
        if not self.__is_showed(self.__camera_sequencer):
            # カメラシーケンサーメインで実質カメラシーケンサーが表示されてないと無意味なので、スキップ
            return

        camera_sequencer_view_time_range = cmds.clipEditor(self.__camera_sequencer_ed, query=True, frameRange=True)

        camera_sequencer_view_start_time = camera_sequencer_view_time_range[0]
        camera_sequencer_view_end_time = camera_sequencer_view_time_range[1]

        if self.__is_showed(self.__time_editor):
            cmds.animView(self.__time_editor_ed, edit=True, startTime=camera_sequencer_view_start_time, endTime=camera_sequencer_view_end_time)

        if self.__is_showed(self.__graph_editor):
            cmds.animView(self.__graph_editor_ed, edit=True, startTime=camera_sequencer_view_start_time, endTime=camera_sequencer_view_end_time)

        if self.__is_showed(self.__dop_sheet):
            cmds.animView(self.__dop_sheet_ed, edit=True, startTime=camera_sequencer_view_start_time, endTime=camera_sequencer_view_end_time)

        clip_start_time, clip_end_time = self.__get_shotnode_time_range()
        cmds.playbackOptions(edit=True, animationStartTime=clip_start_time)
        cmds.playbackOptions(edit=True, animationEndTime=clip_end_time)
