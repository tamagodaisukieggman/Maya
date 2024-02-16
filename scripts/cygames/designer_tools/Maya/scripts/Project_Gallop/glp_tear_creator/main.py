# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds
import maya.mel as mel

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

from . import tear_creator

reload(base_common)

reload(tear_creator)


# ===============================================
def main():

    main = Main()
    main.create_ui()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main:

    # ==================================================
    def __init__(self):

        self.tool_version = '19070201'
        self.tool_name = 'TearCreator'

        self.window_name = self.tool_name + 'Win'

        # スクリプトのパス関連
        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        # 設定関連
        self.setting = base_class.setting.Setting(self.tool_name)
        self.local_setting = base_class.setting.Setting('', True)

        # UI
        self.ui_target_curve = None
        self.ui_target_material = None

        self.ui_particle_count = None

        self.ui_frame_info_frame_layout_list = None
        self.ui_frame_info_frame_list = None
        self.ui_frame_info_position_list = None
        self.ui_frame_info_mesh_threshold_list = None
        self.ui_frame_info_mesh_blobby_radius_scale_list = None
        self.ui_frame_info_mesh_triangle_size_list = None
        self.ui_frame_info_delay_list = None
        self.ui_frame_info_delay_power_list = None
        self.ui_frame_info_offset_list = None
        self.ui_frame_info_offset_interval_list = None
        self.ui_frame_info_spread_list = None

        #
        self.current_select = None
        self.prev_select = None

    # ==================================================
    def create_ui(self):

        self.ui_window = base_class.ui.window.Window(
            self.window_name,
            'Glp' + self.tool_name + '  ' + self.tool_version,
            width=400, height=700
        )

        self.ui_window.set_close_function(self.__save_setting)

        self.ui_window.set_job('SelectionChanged', self.__change_selection)

        this_column = cmds.columnLayout(adj=True, rs=4)

        self.__create_tear_header_ui()
        self.__create_setting_ui()

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True, parent=self.ui_window.ui_header_layout_id)

        self.__create_tear_ui()

        self.__load_setting()

        self.__change_selection()

        self.ui_window.show()

    # ==================================================
    def __create_setting_ui(self):

        self.ui_setting_layout = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            "設定作成", self.__create_setting, bgc=[0.5, 0.6, 0.7], height=40)

        cmds.setParent('..')

    # ==================================================
    def __create_tear_header_ui(self):

        self.ui_tear_header_layout = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            "生成", self.__create_tear, bgc=[0.7, 0.5, 0.5], height=40)

        cmds.setParent('..')

    # ==================================================
    def __create_tear_ui(self):

        self.ui_frame_info_frame_layout_list = []
        self.ui_frame_info_frame_list = []
        self.ui_frame_info_position_list = []
        self.ui_frame_info_mesh_threshold_list = []
        self.ui_frame_info_mesh_blobby_radius_scale_list = []
        self.ui_frame_info_mesh_triangle_size_list = []
        self.ui_frame_info_delay_list = []
        self.ui_frame_info_delay_power_list = []
        self.ui_frame_info_offset_list = []
        self.ui_frame_info_offset_interval_list = []
        self.ui_frame_info_spread_list = []

        self.ui_tear_main_layout = cmds.columnLayout(adj=True, rs=4)

        self.ui_root_name = base_class.ui.text_field.TextField(
            "Root Name", 'tear_root')

        self.ui_target_curve = base_class.ui.text_field.TextField(
            "Target Curve", '')

        self.ui_target_material = base_class.ui.text_field.TextField(
            "Target Material", '')

        self.ui_particle_count = base_class.ui.value_field.ValueField(
            'Particle Count', 10, True)

        for p in range(10):

            this_frame_layout = base_class.ui.frame_layout.FrameLayout(
                'Frame Info {0}'.format(p), True)

            color_multiply_value = 1 - float(p) / float(10.0)
            color_multiply_value = color_multiply_value * 0.6 + 0.4

            if p % 2 == 0:
                this_frame_layout.apply_frame_layout_param(
                    e=True, bgc=[0.4 * color_multiply_value, 0.4 * color_multiply_value, 0.6 * color_multiply_value])
            else:
                this_frame_layout.apply_frame_layout_param(
                    e=True, bgc=[0.4 * color_multiply_value, 0.4 * color_multiply_value, 0.5 * color_multiply_value])

            this_column = cmds.columnLayout(adj=True, rs=4)

            this_ui_frame = base_class.ui.value_field.ValueField(
                'Frame', -1, True)

            this_ui_position = base_class.ui.value_field.ValueField(
                'Position', -1, False)

            this_ui_mesh_threshold = base_class.ui.value_field.ValueField(
                'Mesh Threshold', 0.1, False)

            this_ui_mesh_blobby_radius_scale = base_class.ui.value_field.ValueField(
                'Mesh Blobby Radius Scale', 1, False)

            this_ui_mesh_triangle_size = \
                base_class.ui.value_field.ValueField(
                    'Mesh Triangle Size', 0.25, False)

            this_ui_delay = base_class.ui.value_field.ValueField(
                'Delay', 1, False)

            this_ui_delay_power = base_class.ui.value_field.ValueField(
                'Delay Power', 1, False)

            this_ui_offset = \
                base_class.ui.value_multi_field.ValueMultiField(
                    'Offset',
                    [
                        {
                            'key': 'x',
                            'label': 'x',
                            'value': 0,
                        },

                        {
                            'key': 'y',
                            'label': 'y',
                            'value': 0,
                        },

                        {
                            'key': 'z',
                            'label': 'z',
                            'value': 0,
                        },
                    ],
                    False
                )

            this_ui_offset_interval = base_class.ui.value_field.ValueField(
                'Offset Interval', 0, True)

            this_ui_spread = base_class.ui.value_field.ValueField(
                'Spread', 0, False)

            self.ui_frame_info_frame_layout_list.append(
                this_frame_layout)

            self.ui_frame_info_frame_list.append(
                this_ui_frame)

            self.ui_frame_info_position_list.append(
                this_ui_position)

            self.ui_frame_info_mesh_blobby_radius_scale_list.append(
                this_ui_mesh_blobby_radius_scale)

            self.ui_frame_info_mesh_threshold_list.append(
                this_ui_mesh_threshold)

            self.ui_frame_info_mesh_triangle_size_list.append(
                this_ui_mesh_triangle_size)

            self.ui_frame_info_delay_list.append(
                this_ui_delay)

            self.ui_frame_info_delay_power_list.append(
                this_ui_delay_power)

            self.ui_frame_info_offset_list.append(
                this_ui_offset)

            self.ui_frame_info_offset_interval_list.append(
                this_ui_offset_interval)

            self.ui_frame_info_spread_list.append(
                this_ui_spread)

            cmds.setParent('..')

            cmds.columnLayout(
                this_column,
                e=True, parent=this_frame_layout.ui_layout_id)

        cmds.setParent('..')

        cmds.columnLayout(
            self.ui_tear_main_layout,
            e=True, parent=self.ui_window.ui_body_layout_id)

    # ==================================================
    def __change_selection(self):

        select_list = cmds.ls(sl=True, l=True, typ='transform')

        if select_list:
            self.current_select = select_list[0]
        else:
            self.current_select = None

        if self.current_select != self.prev_select:
            self.__save_local_setting()

        if self.__is_setting(self.current_select):

            cmds.columnLayout(
                self.ui_tear_header_layout, e=True, visible=True)
            cmds.columnLayout(
                self.ui_tear_main_layout, e=True, visible=True)
            cmds.columnLayout(
                self.ui_setting_layout, e=True, visible=False)

            self.__save_local_setting()

            self.__change_setting(self.current_select)

            self.__load_local_setting()

        else:

            cmds.columnLayout(
                self.ui_tear_header_layout, e=True, visible=False)
            cmds.columnLayout(
                self.ui_tear_main_layout, e=True, visible=False)
            cmds.columnLayout(
                self.ui_setting_layout, e=True, visible=True)

        self.prev_select = self.current_select

    # ==================================================
    def __load_setting(self):

        self.ui_window.load_setting(
            self.setting, 'MainWindow')

    # ==================================================
    def __save_setting(self):

        self.ui_window.save_setting(
            self.setting, 'MainWindow')

        self.__save_local_setting()

    # ==================================================
    def __load_local_setting(self):

        if not self.local_setting.setting_group_name:
            return

        if self.local_setting.setting_group_name.find('_setting') >= 0:
            return

        if not cmds.objExists(self.local_setting.setting_group_name):
            return

        self.ui_root_name.load_setting(
            self.local_setting, 'rootName'
        )

        self.ui_target_curve.load_setting(
            self.local_setting, 'targetCurve')

        self.ui_target_material.load_setting(
            self.local_setting, 'targetMaterial')

        self.ui_particle_count.load_setting(
            self.local_setting, 'particleCount')

        for p in range(len(self.ui_frame_info_frame_list)):

            this_ui_frame_layout = self.ui_frame_info_frame_layout_list[p]

            this_ui_frame = self.ui_frame_info_frame_list[p]
            this_ui_position = self.ui_frame_info_position_list[p]
            this_ui_mesh_threshold = self.ui_frame_info_mesh_threshold_list[p]
            this_ui_mesh_blobby_radius_scale = self.ui_frame_info_mesh_blobby_radius_scale_list[
                p]
            this_ui_mesh_triangle_size = self.ui_frame_info_mesh_triangle_size_list[p]
            this_ui_delay = self.ui_frame_info_delay_list[p]
            this_ui_delay_power = self.ui_frame_info_delay_power_list[p]
            this_ui_offset = self.ui_frame_info_offset_list[p]
            this_ui_offset_interval = self.ui_frame_info_offset_interval_list[p]
            this_ui_spread = self.ui_frame_info_spread_list[p]

            this_ui_frame_layout.load_setting(
                self.local_setting, 'frameInfo{0}_frameLayout'.format(p))

            this_ui_frame.load_setting(
                self.local_setting, 'frameInfo{0}_frame'.format(p))

            this_ui_position.load_setting(
                self.local_setting, 'frameInfo{0}_position'.format(p))

            this_ui_mesh_threshold.load_setting(
                self.local_setting, 'frameInfo{0}_meshThreshold'.format(p))

            this_ui_mesh_blobby_radius_scale.load_setting(
                self.local_setting, 'frameInfo{0}_meshBlobbyRadiusScale'.format(p))

            this_ui_mesh_triangle_size.load_setting(
                self.local_setting, 'frameInfo{0}_meshTriangleSize'.format(p))

            this_ui_delay.load_setting(
                self.local_setting, 'frameInfo{0}_delay'.format(p))

            this_ui_delay_power.load_setting(
                self.local_setting, 'frameInfo{0}_delayPower'.format(p))

            this_ui_offset.load_setting(
                self.local_setting, 'frameInfo{0}_offset'.format(p))

            this_ui_offset_interval.load_setting(
                self.local_setting, 'frameInfo{0}_offsetInterval'.format(p))

            this_ui_spread.load_setting(
                self.local_setting, 'frameInfo{0}_spread'.format(p))

    # ==================================================
    def __save_local_setting(self):

        if not self.local_setting.setting_group_name:
            return

        if self.local_setting.setting_group_name.find('_setting') >= 0:
            return

        if not cmds.objExists(self.local_setting.setting_group_name):
            return

        self.ui_root_name.save_setting(
            self.local_setting, 'rootName'
        )

        self.ui_target_curve.save_setting(
            self.local_setting, 'targetCurve')

        self.ui_target_material.save_setting(
            self.local_setting, 'targetMaterial')

        self.ui_particle_count.save_setting(
            self.local_setting, 'particleCount')

        for p in range(len(self.ui_frame_info_frame_list)):

            this_ui_frame_layout = self.ui_frame_info_frame_layout_list[p]

            this_ui_frame = self.ui_frame_info_frame_list[p]
            this_ui_position = self.ui_frame_info_position_list[p]
            this_ui_mesh_threshold = self.ui_frame_info_mesh_threshold_list[p]
            this_ui_mesh_blobby_radius_scale = self.ui_frame_info_mesh_blobby_radius_scale_list[
                p]
            this_ui_mesh_triangle_size = self.ui_frame_info_mesh_triangle_size_list[p]
            this_ui_delay = self.ui_frame_info_delay_list[p]
            this_ui_delay_power = self.ui_frame_info_delay_power_list[p]
            this_ui_offset = self.ui_frame_info_offset_list[p]
            this_ui_offset_interval = self.ui_frame_info_offset_interval_list[p]
            this_ui_spread = self.ui_frame_info_spread_list[p]

            this_ui_frame_layout.save_setting(
                self.local_setting, 'frameInfo{0}_frameLayout'.format(p))

            this_ui_frame.save_setting(
                self.local_setting, 'frameInfo{0}_frame'.format(p))

            this_ui_position.save_setting(
                self.local_setting, 'frameInfo{0}_position'.format(p))

            this_ui_mesh_threshold.save_setting(
                self.local_setting, 'frameInfo{0}_meshThreshold'.format(p))

            this_ui_mesh_blobby_radius_scale.save_setting(
                self.local_setting, 'frameInfo{0}_meshBlobbyRadiusScale'.format(p))

            this_ui_mesh_triangle_size.save_setting(
                self.local_setting, 'frameInfo{0}_meshTriangleSize'.format(p))

            this_ui_delay.save_setting(
                self.local_setting, 'frameInfo{0}_delay'.format(p))

            this_ui_delay_power.save_setting(
                self.local_setting, 'frameInfo{0}_delayPower'.format(p))

            this_ui_offset.save_setting(
                self.local_setting, 'frameInfo{0}_offset'.format(p))

            this_ui_offset_interval.save_setting(
                self.local_setting, 'frameInfo{0}_offsetInterval'.format(p))

            this_ui_spread.save_setting(
                self.local_setting, 'frameInfo{0}_spread'.format(p))

    # ==================================================
    def __create_tear(self):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'データを作成しますか?',
                self.ui_window.ui_window_id):
            return

        target_curve = self.ui_target_curve.get_value()

        if not target_curve:
            return

        if not cmds.objExists(target_curve):
            return

        creator = tear_creator.TearCreator()

        creator.root_transform_name = self.ui_root_name.get_value()

        creator.target_curve = target_curve

        creator.particle_count = self.ui_particle_count.get_value()

        creator.material_name = self.ui_target_material.get_value()

        creator.frame_info_list = []

        for p in range(len(self.ui_frame_info_frame_list)):

            this_ui_frame = self.ui_frame_info_frame_list[p]
            this_ui_position = self.ui_frame_info_position_list[p]
            this_ui_mesh_threshold = self.ui_frame_info_mesh_threshold_list[p]
            this_ui_mesh_blobby_radius_scale = self.ui_frame_info_mesh_blobby_radius_scale_list[
                p]
            this_ui_mesh_triangle_size = self.ui_frame_info_mesh_triangle_size_list[p]
            this_ui_delay = self.ui_frame_info_delay_list[p]
            this_ui_delay_power = self.ui_frame_info_delay_power_list[p]
            this_ui_offset = self.ui_frame_info_offset_list[p]
            this_ui_offset_interval = self.ui_frame_info_offset_interval_list[p]
            this_ui_spread = self.ui_frame_info_spread_list[p]

            this_frame_info = {}

            if this_ui_frame.get_value() < 0:
                continue

            if this_ui_position.get_value() < 0:
                continue

            this_frame_info['frame'] = \
                this_ui_frame.get_value()
            this_frame_info['position'] = \
                this_ui_position.get_value()
            this_frame_info['meshThreshold'] = \
                this_ui_mesh_threshold.get_value()
            this_frame_info['meshBlobbyRadiusScale'] = \
                this_ui_mesh_blobby_radius_scale.get_value()
            this_frame_info['meshTriangleSize'] = \
                this_ui_mesh_triangle_size.get_value()
            this_frame_info['delay'] = \
                this_ui_delay.get_value()
            this_frame_info['delayPower'] = \
                this_ui_delay_power.get_value()
            this_frame_info['offset'] = \
                this_ui_offset.get_value_list()
            this_frame_info['offsetInterval'] = \
                this_ui_offset_interval.get_value()
            this_frame_info['spread'] = \
                this_ui_spread.get_value()

            creator.frame_info_list.append(this_frame_info)

        base_utility.select.save_selection()

        creator.create()

        base_utility.select.load_selection()

    # ==================================================
    def __create_setting(self):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', '設定を作成しますか?',
                self.ui_window.ui_window_id):
            return

        this_group_name = cmds.group(name='tearCreatorSetting', em=True)

        self.local_setting.set_group_name(this_group_name)

        self.local_setting.save('isTearCreator', True)

    # ==================================================
    def __is_setting(self, target_transform):

        if not target_transform:
            return False

        if not base_utility.attribute.exists(target_transform, 'isTearCreator'):
            return False

        return True

    # ==================================================
    def __change_setting(self, target_transform):

        if not self.__is_setting(target_transform):
            return

        short_name = target_transform.split('|')[-1]

        self.local_setting.set_group_name(short_name)
