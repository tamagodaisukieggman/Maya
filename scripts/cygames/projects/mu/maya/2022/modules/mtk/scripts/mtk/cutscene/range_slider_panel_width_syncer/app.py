# -*- coding: utf-8 -*-
"""Panelサイズ同期機能"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya import cmds


class CameraSequencerRangeSliderSyncer(object):
    def __init__(self):
        self.common_width = 50.00

    def __is_showed(self, panel_name):
        """表示されているか

        :param panel_name: 確認したPanel名
        :type panel_name: str
        :return: 表示されているか
        :rtype: bool
        """
        is_control = cmds.panel(panel_name, query=True, control=True)

        return is_control

    def sync(self, src_panel, dist_panel):
        panel_layout = self.__get_pane_layout(src_panel)
        self.common_width = cmds.paneLayout(panel_layout, query=True, paneSize=True)[0]

        self.change_graph_editor_panel_width(src_panel, self.common_width)
        self.change_graph_editor_panel_width(dist_panel, self.common_width)

    def __get_pane_layout(self, panel_name):
        panel_all_layout = [_ for _ in cmds.lsUI(long=True, controlLayouts=True) if panel_name in _]
        panel_target_layout = [_ for _ in panel_all_layout if "paneLayout" in _]
        panel_target_layout.sort()

        if panel_target_layout:
            return panel_target_layout[0]
        else:
            return None

    def __change_panel_kayout_width(self, layout, index, width_size):
        """パネルの横幅を変更する

        :param layout: 対象のpanelLayout
        :type layout: str
        :param index: panelの番号(1~)
        :type index: int
        :param width_size: 横幅. panelLayout以上のサイズを設定できない
        :type width_size: str
        """
        pain_size = cmds.paneLayout(layout, query=True, paneSize=True)[index - 1:(index * 2)]

        cmds.paneLayout(layout, edit=True, paneSize=[1, width_size, pain_size[1]])

    def change_graph_editor_panel_width(self, panel_name, width):
        if not self.__is_showed(panel_name):
            # 同期元となるEditorが表示されてなかったら無意味なので、返却
            return

        graph_editor_panel_layout = self.__get_pane_layout(panel_name)
        self.__change_panel_kayout_width(graph_editor_panel_layout, 1, width)
