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

from . import texture_animation_creator

reload(base_common)

reload(texture_animation_creator)


# ===============================================
def main():

    main = Main()
    main.create_ui()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main:

    # ==================================================
    def __init__(self):

        self.tool_version = '19070201'
        self.tool_name = 'TextureAnimationCreator'

        self.window_name = self.tool_name + 'Win'

        # スクリプトのパス関連
        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        # 設定関連
        self.setting = base_class.setting.Setting(self.tool_name)
        self.local_setting = base_class.setting.Setting(self.tool_name, True)

        # UI

        self.ui_window = None

        #
        self.current_select = None
        self.prev_select = None

        self.tex_anim = texture_animation_creator.TextureAnimationCreator()

    # ==================================================
    def create_ui(self):

        self.ui_window = base_class.ui.window.Window(
            self.window_name,
            'Glp' + self.tool_name + '  ' + self.tool_version,
            width=520, height=570
        )

        self.ui_window.set_close_function(
            self.__save_setting
        )

        self.ui_window.set_job('SelectionChanged', self.__change_selection)

        this_column = cmds.columnLayout(adj=True, rs=4)

        self.__create_setting_ui()
        self.__create_header_ui()

        cmds.columnLayout(
            this_column,
            e=True, parent=self.ui_window.ui_header_layout_id)

        self.__create_main_ui()

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
    def __create_header_ui(self):

        self.ui_header_layout = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            "モデルとテクスチャを生成", self.__create_texture, bgc=[0.7, 0.5, 0.5], height=40)

        cmds.setParent('..')

    # ==================================================
    def __create_main_ui(self):

        self.ui_main_layout = cmds.columnLayout(adj=True, rs=4)

        self.ui_target_mesh = base_class.ui.text_field.TextField(
            "Target Mesh", '')

        self.ui_root_group_name = base_class.ui.text_field.TextField(
            "Root Group Name", 'textureAnimation')

        self.ui_plane_name = base_class.ui.text_field.TextField(
            "Plane Name", 'plane')

        self.ui_material_name = base_class.ui.text_field.TextField(
            "Material Name", 'mtl_textureAnimation')

        self.ui_joint_name = base_class.ui.text_field.TextField(
            "Joint Name", 'joint')

        self.ui_bound_offset = base_class.ui.value_field.ValueField(
            'Bound Offset', 0.1, False)

        self.ui_plane_y_direction = \
            base_class.ui.radio_button.RadioButton(
                'Plane Y Direction',
                ['+X', '-X', '+Y', '-Y', '+Z', '-Z'],
                '-Y'
            )

        self.ui_plane_z_direction = \
            base_class.ui.radio_button.RadioButton(
                'Plane Z Direction',
                ['+X', '-X', '+Y', '-Y', '+Z', '-Z'],
                '+Z'
            )

        self.ui_plane_x_align = \
            base_class.ui.radio_button.RadioButton(
                'Plane X Align',
                ['Left', 'Center', 'Right'],
                'Center'
            )

        self.ui_plane_y_align = \
            base_class.ui.radio_button.RadioButton(
                'Plane Y Align',
                ['Upper', 'Middle', 'Bottom'],
                'Bottom'
            )

        self.ui_plane_devide = \
            base_class.ui.value_multi_field.ValueMultiField(
                'Plane Divide',
                [
                    {
                        'key': 'x',
                        'label': 'X',
                        'value': 5,
                    },

                    {
                        'key': 'y',
                        'label': 'Y',
                        'value': 10,
                    },
                ],
                True
            )

        self.ui_plane_vertex_offset = \
            base_class.ui.value_multi_field.ValueMultiField(
                'Plane Vertex Offset',
                [
                    {
                        'key': 'xEdge',
                        'label': 'X Edge',
                        'value': 0.1,
                    },

                    {
                        'key': 'yEdge',
                        'label': 'Y Edge',
                        'value': 0,
                    },

                    {
                        'key': 'inner',
                        'label': 'Inner',
                        'value': 0.1,
                    },
                ],
                False
            )

        self.ui_render_frame = \
            base_class.ui.value_multi_field.ValueMultiField(
                'Render Frame',
                [
                    {
                        'key': 'start',
                        'label': 'Start',
                        'value': 0,
                    },

                    {
                        'key': 'end',
                        'label': 'End',
                        'value': 100,
                    },

                    {
                        'key': 'interval',
                        'label': 'Interval',
                        'value': 1,
                    },
                ],
                True
            )

        self.ui_atlas_file_name = base_class.ui.text_field.TextField(
            "Atlas File Name", 'textureAnimation')

        self.ui_atlas_size = \
            base_class.ui.value_multi_field.ValueMultiField(
                'Atlas Size',
                [
                    {
                        'key': 'width',
                        'label': 'Width',
                        'value': 512,
                    },

                    {
                        'key': 'height',
                        'label': 'Height',
                        'value': 512,
                    },
                ],
                True
            )

        self.ui_atlas_part_size = \
            base_class.ui.value_multi_field.ValueMultiField(
                'Atlas Part Size',
                [
                    {
                        'key': 'width',
                        'label': 'Width',
                        'value': 32,
                    },

                    {
                        'key': 'height',
                        'label': 'Height',
                        'value': 64,
                    },
                ],
                True
            )

        self.ui_atlas_multiply_value = base_class.ui.value_field.ValueField(
            'Atlas Multiply Value', 1, False)

        cmds.setParent('..')

        cmds.columnLayout(
            self.ui_main_layout,
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
                self.ui_header_layout, e=True, visible=True)
            cmds.columnLayout(
                self.ui_main_layout, e=True, visible=True)
            cmds.columnLayout(
                self.ui_setting_layout, e=True, visible=False)

            self.__save_local_setting()

            self.__change_setting(self.current_select)

            self.__load_local_setting()

        else:

            cmds.columnLayout(
                self.ui_header_layout, e=True, visible=False)
            cmds.columnLayout(
                self.ui_main_layout, e=True, visible=False)
            cmds.columnLayout(
                self.ui_setting_layout, e=True, visible=True)

        self.prev_select = self.current_select

    # ==================================================
    def __load_setting(self):

        self.ui_window.load_setting(
            self.setting, 'mainWindow')

    # ==================================================
    def __save_setting(self):

        self.ui_window.save_setting(
            self.setting, 'mainWindow')

        self.__save_local_setting()

    # ==================================================
    def __load_local_setting(self):

        if not self.local_setting.setting_group_name:
            return

        if self.local_setting.setting_group_name.find('_setting') >= 0:
            return

        if not cmds.objExists(self.local_setting.setting_group_name):
            return

        self.ui_target_mesh.load_setting(
            self.local_setting, 'targetMesh')

        self.ui_root_group_name.load_setting(
            self.local_setting, 'rootGroupName')

        self.ui_plane_name.load_setting(
            self.local_setting, 'planeName')

        self.ui_material_name.load_setting(
            self.local_setting, 'materialName')

        self.ui_joint_name.load_setting(
            self.local_setting, 'jointName')

        self.ui_bound_offset.load_setting(
            self.local_setting, 'boundOffset')

        self.ui_plane_y_direction.load_setting(
            self.local_setting, 'planeYDirection')

        self.ui_plane_z_direction.load_setting(
            self.local_setting, 'planeZDirection')

        self.ui_plane_y_align.load_setting(
            self.local_setting, 'planeYAlign')

        self.ui_plane_x_align.load_setting(
            self.local_setting, 'planeXAlign')

        self.ui_plane_devide.load_setting(
            self.local_setting, 'planeDivide')

        self.ui_plane_vertex_offset.load_setting(
            self.local_setting, 'planeVertexOffset'
        )

        self.ui_render_frame.load_setting(
            self.local_setting, 'renderFrame')

        self.ui_atlas_file_name.load_setting(
            self.local_setting, 'atlasFileName')

        self.ui_atlas_size.load_setting(
            self.local_setting, 'atlasSize')

        self.ui_atlas_part_size.load_setting(
            self.local_setting, 'atlasPartSize')

        self.ui_atlas_multiply_value.load_setting(
            self.local_setting, 'atlasMultiplyValue')

    # ==================================================
    def __save_local_setting(self):

        if not self.local_setting.setting_group_name:
            return

        if self.local_setting.setting_group_name.find('_setting') >= 0:
            return

        if not cmds.objExists(self.local_setting.setting_group_name):
            return

        self.ui_target_mesh.save_setting(
            self.local_setting, 'targetMesh')

        self.ui_root_group_name.save_setting(
            self.local_setting, 'rootGroupName')

        self.ui_plane_name.save_setting(
            self.local_setting, 'planeName')

        self.ui_material_name.save_setting(
            self.local_setting, 'materialName')

        self.ui_joint_name.save_setting(
            self.local_setting, 'jointName')

        self.ui_bound_offset.save_setting(
            self.local_setting, 'boundOffset')

        self.ui_plane_y_direction.save_setting(
            self.local_setting, 'planeYDirection')

        self.ui_plane_z_direction.save_setting(
            self.local_setting, 'planeZDirection')

        self.ui_plane_y_align.save_setting(
            self.local_setting, 'planeYAlign')

        self.ui_plane_x_align.save_setting(
            self.local_setting, 'planeXAlign')

        self.ui_plane_devide.save_setting(
            self.local_setting, 'planeDivide')

        self.ui_plane_vertex_offset.save_setting(
            self.local_setting, 'planeVertexOffset'
        )

        self.ui_render_frame.save_setting(
            self.local_setting, 'renderFrame')

        self.ui_atlas_file_name.save_setting(
            self.local_setting, 'atlasFileName')

        self.ui_atlas_size.save_setting(
            self.local_setting, 'atlasSize')

        self.ui_atlas_part_size.save_setting(
            self.local_setting, 'atlasPartSize')

        self.ui_atlas_multiply_value.save_setting(
            self.local_setting, 'atlasMultiplyValue')

    # ==================================================
    def __create_texture(self):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'モデルとテクスチャを作成しますか?',
                self.ui_window.ui_window_id):
            return

        base_utility.select.save_selection()

        self.__apply_value_from_ui()

        self.tex_anim.create_texture()

        base_utility.select.load_selection()

    # ==================================================
    def __apply_value_from_ui(self):

        self.tex_anim.root_group_name = self.ui_root_group_name.get_value()

        self.tex_anim.plane_name = self.ui_plane_name.get_value()

        self.tex_anim.material_name = self.ui_material_name.get_value()

        self.tex_anim.plane_joint_name_prefix = self.ui_joint_name.get_value()

        self.tex_anim.target_transform_list = \
            self.ui_target_mesh.get_value().split(',')

        self.tex_anim.bound_size_offset = self.ui_bound_offset.get_value()

        self.tex_anim.plane_devide_x = \
            self.ui_plane_devide.get_value_by_key('x')
        self.tex_anim.plane_devide_y =\
            self.ui_plane_devide.get_value_by_key('y')

        self.tex_anim.plane_y_vector = [0, 0, 0]

        if self.ui_plane_y_direction.get_value() == '+X':
            self.tex_anim.plane_y_vector[0] = 1
        elif self.ui_plane_y_direction.get_value() == '-X':
            self.tex_anim.plane_y_vector[0] = -1
        elif self.ui_plane_y_direction.get_value() == '+Y':
            self.tex_anim.plane_y_vector[1] = 1
        elif self.ui_plane_y_direction.get_value() == '-Y':
            self.tex_anim.plane_y_vector[1] = -1
        elif self.ui_plane_y_direction.get_value() == '+Z':
            self.tex_anim.plane_y_vector[2] = 1
        elif self.ui_plane_y_direction.get_value() == '-Z':
            self.tex_anim.plane_y_vector[2] = -1

        self.tex_anim.plane_z_vector = [0, 0, 0]

        if self.ui_plane_z_direction.get_value() == '+X':
            self.tex_anim.plane_z_vector[0] = 1
        elif self.ui_plane_z_direction.get_value() == '-X':
            self.tex_anim.plane_z_vector[0] = -1
        elif self.ui_plane_z_direction.get_value() == '+Y':
            self.tex_anim.plane_z_vector[1] = 1
        elif self.ui_plane_z_direction.get_value() == '-Y':
            self.tex_anim.plane_z_vector[1] = -1
        elif self.ui_plane_z_direction.get_value() == '+Z':
            self.tex_anim.plane_z_vector[2] = 1
        elif self.ui_plane_z_direction.get_value() == '-Z':
            self.tex_anim.plane_z_vector[2] = -1

        self.tex_anim.plane_align = [0, 0]

        if self.ui_plane_x_align.get_value() == 'Left':
            self.tex_anim.plane_align[0] = -1
        elif self.ui_plane_x_align.get_value() == 'Center':
            self.tex_anim.plane_align[0] = 0
        elif self.ui_plane_x_align.get_value() == 'Right':
            self.tex_anim.plane_align[0] = 1

        if self.ui_plane_y_align.get_value() == 'Upper':
            self.tex_anim.plane_align[1] = 1
        elif self.ui_plane_y_align.get_value() == 'Middle':
            self.tex_anim.plane_align[1] = 0
        elif self.ui_plane_y_align.get_value() == 'Bottom':
            self.tex_anim.plane_align[1] = -1

        self.tex_anim.plane_x_edge_offset = \
            self.ui_plane_vertex_offset.get_value_by_key('xEdge')
        self.tex_anim.plane_y_edge_offset = \
            self.ui_plane_vertex_offset.get_value_by_key('yEdge')
        self.tex_anim.plane_inner_offset = \
            self.ui_plane_vertex_offset.get_value_by_key('inner')

        self.tex_anim.start_frame = \
            self.ui_render_frame.get_value_by_key('start')

        self.tex_anim.end_frame = \
            self.ui_render_frame.get_value_by_key('end')

        self.tex_anim.frame_interval = \
            self.ui_render_frame.get_value_by_key('interval')

        self.tex_anim.atlas_file_name = self.ui_atlas_file_name.get_value()

        self.tex_anim.atlas_texture_width =\
            self.ui_atlas_size.get_value_by_key('width')

        self.tex_anim.atlas_texture_height =\
            self.ui_atlas_size.get_value_by_key('height')

        self.tex_anim.atlas_part_tex_width =\
            self.ui_atlas_part_size.get_value_by_key('width')

        self.tex_anim.atlas_part_tex_height =\
            self.ui_atlas_part_size.get_value_by_key('height')

        self.tex_anim.atlas_texture_multiply_value = \
            self.ui_atlas_multiply_value.get_value()

    # ==================================================
    def __create_setting(self):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', '設定を作成しますか?',
                self.ui_window.ui_window_id):
            return

        this_group_name = cmds.group(name='textureAnimationSetting', em=True)

        self.local_setting.set_group_name(this_group_name)

        self.local_setting.save('isTextureAnimation', True)

    # ==================================================
    def __is_setting(self, target_transform):

        if not target_transform:
            return False

        if not base_utility.attribute.exists(target_transform, 'isTextureAnimation'):
            return False

        return True

    # ==================================================
    def __change_setting(self, target_transform):

        if not self.__is_setting(target_transform):
            return

        short_name = target_transform.split('|')[-1]

        self.local_setting.set_group_name(short_name)
