# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass

import os
import glob
import re
from functools import partial

from PySide2 import QtWidgets

import maya.api.OpenMaya as om
import maya.cmds as cmds

from . import assign_shader
from .. import main_template
from ..move_chara_light import move_chara_light
from ....base_common import classes as base_class
from ....glp_common.classes.info import chara_info


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpCharaUtilityAssignCgfxShader'
        self.tool_label = 'テクスチャ・シェーダーの切り替え ※リファレンスモデル対応版'
        self.tool_version = '22072801'

        # tailのディレクトリパス
        # Wディレクトリが無いときはgeneral_chara_data_infoから取得する
        self.tail_dir_path = 'W:\\gallop\\svn\\svn_gallop\\80_3D\\01_character\\01_model\\tail'
        self.mini_tail_dir_path = 'W:\\gallop\\svn\\svn_gallop\\80_3D\\01_character\\01_model\\mini\\tail'
        self.mini_head_dir_path = 'W:\\gallop\\svn\\svn_gallop\\80_3D\\01_character\\01_model\\mini\\head'

        self.assign_shader = assign_shader.AssignShader()
        self.move_chara_light_class = move_chara_light.MoveCharaLight()

        self.change_skin_num = 1
        self.change_bust_num = 2
        self.change_color_num = -1
        self.change_area_num = -1
        self.change_general_tail_num = '0001'
        self.mini_char_main_id = '1001'
        self.mini_char_sub_id = '00'

        self.dirt_rate_list = [0, 0, 0]

        self.row_column_margin = 90
        self.column_height = 22

        self.ui_skin_radio_list = ['白肌', '桃肌', '黄肌', '褐色']
        self.ui_bust_radio_list = ['SS', 'S', 'M', 'L', 'LL']
        self.bust_mini_num_comparison_table = {
            0: 0, 1: 0, 2: 1, 3: 2, 4: 2
        }

    def ui_body(self):
        """
        UI要素のみ
        """

        form = cmds.formLayout(numberOfDivisions=100)

        # マテリアルアサイン
        assign_material_layout = cmds.rowLayout(
            numberOfColumns=6, columnWidth6=(50, 50, 50, 50, 50, 100),
            columnAttach6=['left', 'left', 'left', 'left', 'left', 'left'],
            columnOffset6=[0, 0, 0, 0, 0, 25])
        base_class.ui.button.Button('diff', self.__assign_default_material, 'diff', width=50)
        base_class.ui.button.Button('shad_c', self.__assign_default_material, 'shad_c', width=50)
        base_class.ui.button.Button('PSD', self.__assign_default_material, 'psd', width=50)
        base_class.ui.button.Button('TOON', self.__assign_toon_shader_material, False, False, width=50)
        base_class.ui.button.Button('WET', self.__assign_toon_shader_material, False, True, width=50)
        base_class.ui.button.Button('テクスチャリロード', self.__reload_texture, width=100)
        cmds.setParent('..')

        assign_map_layout = cmds.rowLayout(
            numberOfColumns=6, columnWidth6=(50, 50, 50, 50, 50, 50),
            columnAttach6=['left', 'left', 'left', 'left', 'left', 'left'],
            columnOffset6=[0, 0, 0, 0, 0, 0])
        base_class.ui.button.Button('base R', self.__assign_map_material, 'base', 'R', width=50)
        base_class.ui.button.Button('base G', self.__assign_map_material, 'base', 'G', width=50)
        base_class.ui.button.Button('base B', self.__assign_map_material, 'base', 'B', width=50)
        base_class.ui.button.Button('ctrl R', self.__assign_map_material, 'ctrl', 'R', width=50)
        base_class.ui.button.Button('ctrl G', self.__assign_map_material, 'ctrl', 'G', width=50)
        base_class.ui.button.Button('ctrl B', self.__assign_map_material, 'ctrl', 'B', width=50)
        cmds.setParent('..')

        # 表示する肌色
        skin_radio_layout = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, self.row_column_margin)], height=self.column_height)
        cmds.text(l='表示する肌色', align='left')
        cmds.rowColumnLayout(numberOfRows=1)
        self.skin_radio_grp = cmds.radioCollection()
        for i in range(len(self.ui_skin_radio_list)):
            rb_label = self.ui_skin_radio_list[i]
            cmds.radioButton(label=rb_label, width=50, changeCommand=partial(self.__change_toon_skin_texture))
        self.__update_skin_radio_button_ui()
        cmds.scriptJob(event=['SceneOpened', self.__update_skin_radio_button_ui], protected=True, parent=form)
        cmds.setParent('..')
        cmds.setParent('..')

        # 表示する胸差分
        bust_radio_layout = cmds.rowColumnLayout(
            numberOfColumns=2, columnWidth=[(1, self.row_column_margin)], height=self.column_height)
        cmds.text(l='表示する胸差分', align='left')
        cmds.rowColumnLayout(numberOfRows=1)
        self.bust_radio_grp = cmds.radioCollection()
        for i in range(len(self.ui_bust_radio_list)):
            rb_label = self.ui_bust_radio_list[i]
            cmds.radioButton(label=rb_label, width=50, changeCommand=partial(self.__change_toon_bust_texture))
        self.__update_bust_radio_button_ui()
        cmds.scriptJob(event=['SceneOpened', self.__update_bust_radio_button_ui], protected=True, parent=form)
        cmds.setParent('..')
        cmds.setParent('..')

        # 表示するカラー差分
        color_diff_pull_down_layout = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, self.row_column_margin)], height=self.column_height)
        cmds.text(l='表示するカラー差分', align='left')
        self.color_diff_pull_down = cmds.optionMenu(changeCommand=partial(self.__change_toon_color_texture))
        self.__refrash_color_diff_pull_down_ui()
        cmds.scriptJob(event=['SceneOpened', self.__refrash_color_diff_pull_down_ui], protected=True, parent=form)
        cmds.setParent('..')

        # 表示するエリア差分
        area_diff_pull_down_layout = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, self.row_column_margin)], height=self.column_height)
        cmds.text(l='表示するエリア差分', align='left')
        self.area_diff_pull_down = cmds.optionMenu(changeCommand=partial(self.__change_toon_area_texture))
        self.__refresh_area_diff_pull_down_ui()
        cmds.scriptJob(event=['SceneOpened', self.__refresh_area_diff_pull_down_ui], protected=True, parent=form)
        cmds.setParent('..')

        # 汚れの表示
        dirt_box_layout = cmds.columnLayout(adjustableColumn=True, height=self.column_height)
        self.dirt_box_grp = cmds.checkBoxGrp(
            columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'left', 0)],
            columnWidth=[(1, self.row_column_margin), (2, 75), (3, 75)],
            label='汚れの表示', labelArray3=['dirt1', 'dirt2', 'dirt3'], numberOfCheckBoxes=3,
            changeCommand=partial(self.__change_toon_dirt_texture))
        cmds.setParent('..')

        # 汎用尻尾テクスチャ
        tail_pull_down_layout = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, self.row_column_margin)], height=self.column_height)
        cmds.text(l='汎用尻尾テクスチャ', align='left')
        self.tail_pull_down = cmds.optionMenu(changeCommand=partial(self.__change_general_tail_texture))
        self.__update_tail_pull_down_ui()
        cmds.scriptJob(event=['SceneOpened', self.__update_tail_pull_down_ui], protected=True, parent=form)
        cmds.setParent('..')

        # ミニキャラ顔
        mini_char_pull_down_layout = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, self.row_column_margin)], height=self.column_height)
        cmds.text(l='MINIキャラ顔', align='left')
        self.mini_char_pull_down = cmds.optionMenu(changeCommand=partial(self.__change_mini_char_face_texture))
        self.__update_mini_char_pull_down_ui()
        cmds.scriptJob(event=['SceneOpened', self.__update_mini_char_pull_down_ui], protected=True, parent=form)
        cmds.setParent('..')

        # アウトラインToonShaderのアサイン
        outline_check_layout = cmds.rowLayout(numberOfColumns=4)
        cmds.text(label='アウトライン【確認用】', align='left', width=100)
        base_class.ui.button.Button('ON', self.__assign_outline_toon_shader_material, width=50)
        base_class.ui.button.Button('OFF', self.__remove_outline_toon_shader_material, width=50)
        cmds.text(label='※viewport2.0下ではTOON, WETと併用推奨')
        cmds.setParent('..')

        cmds.formLayout(
            form, e=True,
            attachForm=[
                (assign_material_layout, 'top', 0),
                (assign_material_layout, 'left', 0),
                (assign_map_layout, 'left', 0),
                (skin_radio_layout, 'left', 0),
                (bust_radio_layout, 'left', 0),
                (color_diff_pull_down_layout, 'left', 0),
                (area_diff_pull_down_layout, 'left', 0),
                (dirt_box_layout, 'left', 0),
                (tail_pull_down_layout, 'left', 0),
                (mini_char_pull_down_layout, 'left', 0),
                (outline_check_layout, 'left', 0),
            ],
            attachControl=[
                (assign_map_layout, 'top', 5, assign_material_layout),
                (skin_radio_layout, 'top', 5, assign_map_layout),
                (bust_radio_layout, 'top', 5, skin_radio_layout),
                (color_diff_pull_down_layout, 'top', 5, bust_radio_layout),
                (area_diff_pull_down_layout, 'top', 5, color_diff_pull_down_layout),
                (dirt_box_layout, 'top', 0, area_diff_pull_down_layout),
                (tail_pull_down_layout, 'top', 0, dirt_box_layout),
                (mini_char_pull_down_layout, 'top', 0, tail_pull_down_layout),
                (outline_check_layout, 'top', 0, mini_char_pull_down_layout),
            ]
        )
        cmds.setParent('..')

    def __get_scene_reference_info_list(self):
        """[summary]
        """

        scene_reference_info_list = []
        for ref_node in cmds.ls(referencedNodes=True, type='transform'):

            ref_file_path = cmds.referenceQuery(ref_node, filename=True)
            if ref_file_path in [ref_info.get('file_path') for ref_info in scene_reference_info_list]:
                continue

            ref_namespace = cmds.referenceQuery(ref_file_path, namespace=True, shortName=True)
            scene_reference_info_list.append({'file_path': ref_file_path, 'namespace': ref_namespace})

        return scene_reference_info_list

    def __assign_toon_shader_material(self, is_change=False, is_wet=None):
        """表示されている頭・身体にトゥーンシェーダーのマテリアルをアサインする

        Args:
            is_wet (bool): [description]
        """

        if not self.__check_renderer_and_engine():
            return

        self.assign_shader.assign_dx11_shader_material(
            self.__get_ui_paramator_dict(),
            is_change=is_change,
            is_wet=is_wet)

        scene_reference_info_list = self.__get_scene_reference_info_list()
        for scene_reference_info in scene_reference_info_list:
            self.assign_shader.assign_dx11_shader_material(
                self.__get_ui_paramator_dict(),
                is_change,
                is_wet,
                scene_reference_info.get('file_path'),
                scene_reference_info.get('namespace'))

    def __assign_map_material(self, texture, channel):
        """表示している頭・身体にマップ表示マテリアルをアサインする

        Args:
            texture (str): テクスチャ名('base' or 'ctrl')
            channel (str): 出力チャンネル('R' or 'G' or 'B')
        """

        self.assign_shader.assign_map_material(
            texture,
            channel,
            self.__get_ui_paramator_dict())

        scene_reference_info_list = self.__get_scene_reference_info_list()
        for scene_reference_info in scene_reference_info_list:
            self.assign_shader.assign_map_material(
                texture,
                channel,
                self.__get_ui_paramator_dict(),
                scene_reference_info.get('file_path'),
                scene_reference_info.get('namespace'))

    def __assign_default_material(self, texture_type):
        """表示している頭・身体に通常マテリアルをアサインする

        Args:
            texture_type ([type]): [description]
        """

        scene_reference_info_list = self.__get_scene_reference_info_list()
        for scene_reference_info in scene_reference_info_list:
            self.assign_shader.assign_default_material(
                texture_type,
                self.__get_ui_paramator_dict(),
                scene_reference_info.get('file_path'),
                scene_reference_info.get('namespace'))

        self.assign_shader.assign_default_material(
            texture_type,
            self.__get_ui_paramator_dict())

    def __assign_outline_toon_shader_material(self):
        """[summary]
        """

        if not self.__check_renderer_and_engine():
            return

        self.assign_shader.assign_outline_dx11_shader_material(
            self.__get_ui_paramator_dict())

    def __remove_outline_toon_shader_material(self):
        """アウトライントゥーンシェーダーをシーンから取り除く
        """

        self.assign_shader.remove_outline_dx11_shader_material(
            self.__get_ui_paramator_dict())

    def __change_toon_skin_texture(self, *args):
        """トゥーン表示の肌色テクスチャを変更する
        """

        selected_skin_radio_object = cmds.radioCollection(self.skin_radio_grp, q=True, sl=True)
        selected_skin = cmds.radioButton(selected_skin_radio_object, q=True, label=True)
        self.change_skin_num = self.ui_skin_radio_list.index(selected_skin)

        self.__assign_toon_shader_material(True)

    def __change_toon_bust_texture(self, *args):
        """トゥーン表示の胸差分テクスチャを変更する
        """

        selected_bust_radio_object = cmds.radioCollection(self.bust_radio_grp, q=True, sl=True)
        selected_bust = cmds.radioButton(selected_bust_radio_object, q=True, label=True)
        self.change_bust_num = self.ui_bust_radio_list.index(selected_bust)

        self.__assign_toon_shader_material(True)

    def __change_toon_color_texture(self, *args):
        """トゥーン表示の色差分テクスチャを変更する
        """

        self.change_color_num = int(cmds.optionMenu(self.color_diff_pull_down, q=True, value=True))

        self.__assign_toon_shader_material(True)

    def __change_toon_area_texture(self, *args):
        """トゥーン表示のエリアテクスチャを変更する
        """
        self.change_area_num = int(cmds.optionMenu(self.area_diff_pull_down, q=True, value=True))
        self.__assign_toon_shader_material(True)

    def __change_toon_dirt_texture(self, *args):
        """トゥーン表示のダートテクスチャを変更する
        """

        dirt_toggle_list = cmds.checkBoxGrp(self.dirt_box_grp, q=True, va3=True)
        self.dirt_rate_list = []
        for toggle in dirt_toggle_list:
            if toggle:
                self.dirt_rate_list.append(1.0)
            else:
                self.dirt_rate_list.append(0.0)

        self.__assign_toon_shader_material(True)

    def __change_general_tail_texture(self, *args):
        """[summary]
        """

        self.change_general_tail_num = cmds.optionMenu(self.tail_pull_down, q=True, value=True)

        material_state = self.assign_shader.get_material_state(
            self.__get_ui_paramator_dict())

        if not material_state:
            return

        if material_state.get('shader') == 'default':
            self.__assign_default_material(material_state.get('texture'))
        elif material_state.get('shader') == 'dx11':
            self.__assign_toon_shader_material(True)
        elif material_state.get('shader') == 'map':
            self.__assign_map_material(material_state.get('texture'), material_state.get('channel'))

    def __change_mini_char_face_texture(self, *args):
        """[summary]
        """

        mini_char_id = cmds.optionMenu(self.mini_char_pull_down, q=True, value=True)
        self.mini_char_main_id = mini_char_id.split('_')[0]
        self.mini_char_sub_id = mini_char_id.split('_')[1]

        material_state = self.assign_shader.get_material_state(
            self.__get_ui_paramator_dict())

        if not material_state:
            return

        if material_state.get('shader') == 'default':
            self.__assign_default_material(material_state.get('texture'))
        elif material_state.get('shader') == 'dx11':
            self.__assign_toon_shader_material(True)
        elif material_state.get('shader') == 'map':
            self.__assign_map_material(material_state.get('texture'), material_state.get('channel'))

    def __get_ui_paramator_dict(self):
        """UI上の情報(表示する肌色や胸差分、カラー差分など)を全て取得して辞書化
        """

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            return {}

        ui_paramator = {
            'skin_num': self.change_skin_num,
            'bust_num': self.change_bust_num,
            'color_num': self.change_color_num,
            'area_num': self.change_area_num,
            'general_tail_num': self.change_general_tail_num,
            'dirt_rate_list': self.dirt_rate_list,
            'mini_char_main_id': self.mini_char_main_id,
            'mini_char_sub_id': self.mini_char_sub_id
        }

        # Miniの場合は、胸がS/M/Lの3種類しかない
        if _chara_info.part_info.is_mini:
            self.change_bust_num = self.bust_mini_num_comparison_table[self.change_bust_num]

        return ui_paramator

    def __parse_tail_diff_texture_id_list(self):
        """フォルダを検索して、テクスチャファイルが存在する汎用尻尾IDのリストを返す

        Returns:
            list[str]: 汎用尻尾IDのリスト
        """

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()

        if not _chara_info.exists:
            return []

        tail_dir_path = ''
        pattern = None

        if _chara_info.is_mini:
            tail_dir_path = self.mini_tail_dir_path
            pattern = re.compile(r'^tex_mtail\d{4}_\d{2}_(\d{4})_diff.tga$')
        else:
            tail_dir_path = self.tail_dir_path
            pattern = re.compile(r'^tex_tail\d{4}_\d{2}_(\d{4})_diff.tga$')

        return sorted(pattern.match(file).group(1) for _, _, files in os.walk(tail_dir_path) for file in files if pattern.match(file))

    def __parse_mini_char_id(self, *args):
        """[summary]

        Returns:
            [type]: [description]
        """

        mini_char_id_list = []

        if os.path.isdir(self.mini_head_dir_path):

            for mini_head_dir_child_path in glob.glob(self.mini_head_dir_path + '\\*'):
                match_obj = re.search(r'mchr([1-9][0-9]{3}_[0-9]{2})', mini_head_dir_child_path)
                if match_obj:
                    mini_char_id_list.append(match_obj.group(1))

        return sorted(mini_char_id_list)

    def __refrash_color_diff_pull_down_ui(self, *args):
        """色差分プルダウンメニューを更新する
        """

        if not self.color_diff_pull_down:
            return

        color_diff_id_list = self.__parse_color_diff_id_list()
        if color_diff_id_list:

            # 有効にして初期化
            cmds.optionMenu(self.color_diff_pull_down, e=True, enable=True)
            menuItems = cmds.optionMenu(self.color_diff_pull_down, q=True, itemListLong=True)
            if menuItems:
                cmds.deleteUI(menuItems)

            # 項目追加
            for color_diff_id in color_diff_id_list:
                cmds.menuItem(label=color_diff_id, p=self.color_diff_pull_down)

        else:
            # 無効にして初期化
            cmds.optionMenu(self.color_diff_pull_down, e=True, enable=False)
            menuItems = cmds.optionMenu(self.color_diff_pull_down, q=True, itemListLong=True)
            if menuItems:
                cmds.deleteUI(menuItems)

    def __refresh_area_diff_pull_down_ui(self, *args):
        """エリアのプルダウンメニューを更新する
        """

        if not self.area_diff_pull_down:
            return

        area_diff_id_list = self.__parse_area_diff_id_list()
        if area_diff_id_list:
            # 有効にして初期化
            cmds.optionMenu(self.area_diff_pull_down, e=True, enable=True)
            menu_items = cmds.optionMenu(self.area_diff_pull_down, q=True, itemListLong=True)
            if menu_items:
                cmds.deleteUI(menu_items)

            for area_diff_id in area_diff_id_list:
                cmds.menuItem(label=area_diff_id, p=self.area_diff_pull_down)

            # 初期化時に値が入っていないとToonで初回ロード時に無視されてしまう
            self.change_area_num = 0

        else:
            # 無効化して初期化
            cmds.optionMenu(self.area_diff_pull_down, e=True, enable=False)
            menu_items = cmds.optionMenu(self.area_diff_pull_down, q=True, itemListLong=True)
            if menu_items:
                cmds.deleteUI(menu_items)

    def __parse_color_diff_id_list(self):
        """開いているシーンのsourceimagesフォルダの色差分フォルダのリストを取得する

        Returns:
            [list]: 色差分フォルダのリスト
        """

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            return []

        source_image_path = _chara_info.part_info.maya_sourceimages_dir_path
        if not os.path.exists(source_image_path):
            return []

        dir_list = []
        for target_dir in os.listdir(source_image_path):
            if os.path.isdir('{0}/{1}'.format(source_image_path, target_dir)):
                dir_list.append(target_dir)

        color_diff_id_list = []
        # 色差分IDはフォルダ名と一致しているはず
        for target_dir in dir_list:

            match_obj = re.search(r'^[0-9]{2}$', target_dir)
            if not match_obj:
                continue

            color_diff_id_list.append(match_obj.group(0))

        return color_diff_id_list

    def __parse_area_diff_id_list(self):
        """開いているシーンのsourceimagesからエリアテクスチャのリストを取得する
        """
        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            return []

        area_diff_id_list = []
        for tex_file in _chara_info.part_info.all_texture_list:
            if tex_file.endswith('_area.tga'):
                match_obj = re.search(r'_[0-9]{2}_area.tga$', tex_file)
                if not match_obj:
                    continue
                area_diff_id_list.append(match_obj.group(0)[1:3])

        return area_diff_id_list

    def __reload_texture(self):
        """[summary]
        """

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            return

        file_node_list = cmds.ls(type='file', l=True)
        if not file_node_list:
            return

        for file_node in file_node_list:

            texture_file_path = cmds.getAttr('{}.fileTextureName'.format(file_node))
            texture_file_name = os.path.basename(texture_file_path)

            fix_texture_file_path = '{0}/{1}'.format(
                _chara_info.part_info.maya_sourceimages_dir_path,
                texture_file_name)

            if not os.path.isfile(fix_texture_file_path):
                continue

            cmds.setAttr('{}.fileTextureName'.format(file_node), fix_texture_file_path, type='string')

    def __check_renderer_and_engine(self):
        """レンダラーとエンジンの設定をチェック

        Returns:
            bool: レンダラーとエンジンが正しい設定になっているか
        """

        target_renderer = 'vp2Renderer'
        target_engine = 'DirectX11'
        target_engin_var = 'vp2RenderingEngine'

        p1 = cmds.paneLayout('viewPanes', q=True, pane1=True, fpn=True)
        p2 = cmds.paneLayout('viewPanes', q=True, pane2=True, fpn=True)
        p3 = cmds.paneLayout('viewPanes', q=True, pane3=True, fpn=True)
        p4 = cmds.paneLayout('viewPanes', q=True, pane4=True, fpn=True)
        panes = [p1, p2, p3, p4]
        engine = cmds.optionVar(q=target_engin_var)

        is_valid = True
        confirm_text = ''

        for pane in panes:
            renderer = cmds.modelEditor(pane, q=True, rnm=True)
            if renderer != target_renderer:
                cmds.modelEditor(pane, e=True, rnm=target_renderer)
                confirm_text += u'{}をViewport2.0に設定しました\n\n'.format(pane)

        if engine != target_engine:
            cmds.optionVar(sv=(target_engin_var, target_engine))
            confirm_text += u'Viewport2.0のRenderingEngineをDirectX11に設定しました\n'
            confirm_text += u'Mayaを再起動してください'
            is_valid = False

        if confirm_text:
            QtWidgets.QMessageBox.information(None, '設定エラー', confirm_text, QtWidgets.QMessageBox.Ok)

        return is_valid

    def __update_skin_radio_button_ui(self):
        """肌色ラジオボタンを更新する
        """

        if not self.skin_radio_grp:
            return

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()

        if _chara_info.exists and _chara_info.is_unique_chara and _chara_info.data_info.skin_id is not None:
            self.change_skin_num = _chara_info.data_info.skin_id
        else:
            self.change_skin_num = 1

        radio_buttons = cmds.radioCollection(self.skin_radio_grp, q=True, collectionItemArray=True)

        for radio_button in radio_buttons:
            if cmds.radioButton(radio_button, q=True, label=True) == self.ui_skin_radio_list[self.change_skin_num]:
                cmds.radioButton(radio_button, e=True, select=True)

    def __update_bust_radio_button_ui(self):
        """胸差分ラジオボタンを更新する
        """

        if not self.bust_radio_grp:
            return

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()

        if _chara_info.exists and _chara_info.is_unique_chara and _chara_info.data_info.bust_id is not None:
            self.change_bust_num = _chara_info.data_info.bust_id
        else:
            self.change_bust_num = 2

        radio_buttons = cmds.radioCollection(self.bust_radio_grp, q=True, collectionItemArray=True)

        for radio_button in radio_buttons:
            if cmds.radioButton(radio_button, q=True, label=True) == self.ui_bust_radio_list[self.change_bust_num]:
                cmds.radioButton(radio_button, e=True, select=True)

    def __update_tail_pull_down_ui(self):
        """汎用尻尾プルダウンメニューを更新する
        """

        if not self.tail_pull_down:
            return

        # 初期化
        cmds.optionMenu(self.tail_pull_down, e=True, enable=False)
        menu_items = cmds.optionMenu(self.tail_pull_down, q=True, itemListLong=True)
        if menu_items:
            cmds.deleteUI(menu_items)

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()

        if not _chara_info.exists:
            return

        tail_ids = self.__parse_tail_diff_texture_id_list()

        # 項目追加
        for tail_id in tail_ids:
            cmds.menuItem(label=tail_id, p=self.tail_pull_down)
        cmds.optionMenu(self.tail_pull_down, e=True, enable=True)

        tail_id = ''

        if _chara_info.is_unique_chara:
            tail_id = _chara_info.data_main_id
        else:
            tail_id = cmds.optionMenu(self.tail_pull_down, q=True, value=True)

        if tail_id not in tail_ids:
            om.MGlobal.displayWarning('汎用尻尾データが見つかりません ({})'.format(tail_id))
            return

        cmds.optionMenu(self.tail_pull_down, e=True, value=tail_id)

        self.change_general_tail_num = tail_id

    def __update_mini_char_pull_down_ui(self):
        """ミニキャラ顔プルダウンメニューを更新する
        """

        if not self.mini_char_pull_down:
            return

        # 初期化
        cmds.optionMenu(self.mini_char_pull_down, e=True, enable=False)
        menu_items = cmds.optionMenu(self.mini_char_pull_down, q=True, itemListLong=True)
        if menu_items:
            cmds.deleteUI(menu_items)

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()

        if not _chara_info.exists:
            return

        if not _chara_info.is_mini:
            return

        mini_char_ids = self.__parse_mini_char_id()

        if not mini_char_ids:
            return

        # 項目追加
        for mini_char_id in mini_char_ids:
            cmds.menuItem(label=mini_char_id, p=self.mini_char_pull_down)
        cmds.optionMenu(self.mini_char_pull_down, e=True, enable=True)

        mini_char_id = ''

        if _chara_info.is_unique_chara:
            mini_char_id = '{}_{}'.format(_chara_info.data_main_id, _chara_info.data_sub_id)
        else:
            mini_char_id = cmds.optionMenu(self.mini_char_pull_down, q=True, value=True)

        if mini_char_id not in mini_char_ids:
            om.MGlobal.displayWarning('ミニキャラ顔データが見つかりません ({})'.format(mini_char_id))
            return

        cmds.optionMenu(self.mini_char_pull_down, e=True, value=mini_char_id)

        self.mini_char_main_id = mini_char_id.split('_')[0]
        self.mini_char_sub_id = mini_char_id.split('_')[1]
