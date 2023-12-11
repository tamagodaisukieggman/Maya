# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
from functools import partial

import maya.cmds as cmds

from ....base_common import classes as base_class
from ....priari_common.classes.info import chara_info

from . import add_chara_info_obj
from .. import main_template


class Main(main_template.Main):

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'PriariAddCharaInfoObj'
        self.tool_label = 'オブジェクトの追加'
        self.tool_version = '19112201'

        self.parts_count_field = None

    def ui_body(self):
        """
        UI要素のみ
        """

        cmds.columnLayout(adj=True, rs=5)
        cmds.button(label='エフェクト用ロケーターの初期化', command=self.init_ik_locator)
        cmds.button(label='顔トゥーン用ロケーターの初期化', command=self.init_face_toon_locator)
        cmds.rowLayout(nc=2)
        self.parts_count_field = cmds.intFieldGrp(l='武器パーツ数')
        cmds.button(label='武器モデルから取得', command=self.update_ui)
        cmds.setParent('..')
        cmds.button(label='アタッチ用ロケーターの初期化', command=self.init_attach_locator)
        cmds.setParent('..')
        cmds.button(label='視線ロケーターの初期化', command=self.init_eye_origin_locator)

        self.update_ui()

    def update_ui(self, arg):
        """UIの更新
        """

        if not self.parts_count_field:
            return

        cmds.intFieldGrp(self.parts_count_field,
                         e=True,
                         v1=self.get_weapon_parts_count())

    def get_weapon_parts_count(self):
        """武器モデルからパーツ数を取得する
        """

        default_parts_count = 2

        info = chara_info.CharaInfo()
        info.create_info(is_create_all_info=True)

        if not info.exists:
            return default_parts_count

        if not info.data_info.exists:
            return default_parts_count

        if info.data_info.has_weapon is None:
            return default_parts_count

        if not info.data_info.has_weapon:
            return 0

        if info.data_info.weapon_parts_count is None:
            return default_parts_count

        return info.data_info.weapon_parts_count

    def init_ik_locator(self, arg):
        """
        """

        result_list = []
        add_obj = add_chara_info_obj.AddCharaInfoObj()
        # 以下のロケーター名はchara_infoに記載されている必要がある
        result_list.append(add_obj.add_obj('locator', 'FX_root', is_world=True, should_init=True))
        result_list.append(add_obj.add_obj('locator', 'FX_center', [3, -1, 0], [89.7, 90, 0], should_init=True))
        result_list.append(add_obj.add_obj('locator', 'FX_pos_center', should_init=True))
        result_list.append(add_obj.add_obj('locator', 'FX_head', [9, 0, 0], [85.1, 90, 0], should_init=True))
        result_list.append(add_obj.add_obj('locator', 'FX_L_hand', [2.5, -1, 0], should_init=True))
        result_list.append(add_obj.add_obj('locator', 'FX_R_hand', [2.5, -1, 0], should_init=True))
        result_list.append(add_obj.add_obj('locator', 'FX_L_foot', [5, 0, 0], [144.5, -90, 0], should_init=True))
        result_list.append(add_obj.add_obj('locator', 'FX_R_foot', [5, 0, 0], [144.5, -90, 0], should_init=True))

        print(result_list)
        return result_list

    def init_face_toon_locator(self, arg):
        """
        """

        result_list = []
        add_obj = add_chara_info_obj.AddCharaInfoObj()
        # 以下のロケーター名はchara_infoに記載されている必要がある
        result_list.append(add_obj.add_obj('locator', 'Head_tube_center_offset', [3, 0, 0], should_init=True))
        result_list.append(add_obj.add_obj('locator', 'Head_center_offset', [13, -2.8, 0], should_init=True))
        result_list.append(add_obj.add_obj('locator', 'Head_direction', [0, 0, 0], [85.1, 90, 0.0], should_init=True))

        print(result_list)
        return result_list

    def init_attach_locator(self, arg):
        """
        """

        weapon_parts_count = 2

        if self.parts_count_field:
            weapon_parts_count = \
                cmds.intFieldGrp(self.parts_count_field, q=True, v1=True)

        option = {'weapon_parts_count': weapon_parts_count}

        info = chara_info.CharaInfo()
        info.create_info(data_option=option)

        if not info.exists:
            return

        if not info.part_info.exists:
            return

        root_locator_list = []
        part_locator_list = []

        for locator in info.part_info.locator_list:
            short_name = locator.split('|')[-1]

            if short_name.startswith('AT_'):
                root_locator_list.append(short_name)

            if short_name.startswith('ATCL_'):
                part_locator_list.append(short_name)

        result_list = []
        add_obj = add_chara_info_obj.AddCharaInfoObj(data_option=option)

        for locator in root_locator_list:
            result_obj = add_obj.add_obj('locator', locator, should_init=True)
            if result_obj is not None:
                result_list.append(result_obj)

        for locator in part_locator_list:
            result_obj = add_obj.add_obj('locator', locator, should_init=True)
            if result_obj is not None:
                result_list.append(result_obj)
                cmds.xform(result_obj, s=[0, 1, 1])

        print(result_list)
        return result_list

    def init_eye_origin_locator(self, arg):
        """
        """

        # ペコリーヌ基準
        default_pos = [0, 83.4463005065918, 4.29632736576928]

        info = chara_info.CharaInfo()
        info.create_info()
        if not info.exists or not info.part_info.exists:
            return

        # 目のマテリアルからEye_originのワールド座標を取得
        eye_material = None
        for mtl in info.part_info.material_list:
            if mtl.endswith('_eye'):
                eye_material = mtl
                break

        if not eye_material:
            return

        eye_origin_pos = self.__get_eye_origin_pos(eye_material)
        if not eye_origin_pos:
            print('cannot get position from eye material')
            eye_origin_pos = default_pos

        # ロケーターのセット
        # 一度ワールドでセットした後ローカルでHead_directionと同じ回転値を入れる
        result_list = []
        add_obj = add_chara_info_obj.AddCharaInfoObj()
        # 以下のロケーター名はchara_infoに記載されている必要がある
        eye_origin_locator = add_obj.add_obj('locator', 'Eye_origin', eye_origin_pos, is_world=True, should_reset_scale=False, should_init=True)
        look_target_locator = add_obj.add_obj('locator', 'Look_target', eye_origin_pos, is_world=True, should_reset_scale=False, should_init=True)
        if eye_origin_locator:
            cmds.xform(eye_origin_locator, ro=[85.1, 90, 0.0])
            result_list.append(eye_origin_locator)
        if look_target_locator:
            cmds.xform(look_target_locator, ro=[85.1, 90, 0.0])
            result_list.append(look_target_locator)

        print(result_list)
        return result_list

    def __get_eye_origin_pos(self, eye_material):
        """
        """

        if not cmds.objExists(eye_material):
            return None

        # materialからフェイスを選択
        target_shading_group = cmds.listConnections(eye_material, type='shadingEngine')
        if not target_shading_group:
            return None
        face_list = cmds.sets(target_shading_group, q=True)
        if not face_list:
            return None

        vtx_list = cmds.ls(cmds.polyListComponentConversion(face_list, tv=True), l=True, fl=True)

        if not vtx_list:
            return None

        # 頂点のY,Zの重心を計算
        vtx_count = 0
        result_pos = [0, 0, 0]
        for vtx in vtx_list:
            vtx_pos = cmds.xform(vtx, q=True, t=True, ws=True)
            result_pos[1] += vtx_pos[1]
            result_pos[2] += vtx_pos[2]
            vtx_count += 1

        result_pos[1] = result_pos[1] / vtx_count
        result_pos[2] = result_pos[2] / vtx_count

        return result_pos