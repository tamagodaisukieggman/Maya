# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    # Maya 2022-
    from builtins import zip
    from builtins import str
    from builtins import range
    from builtins import object
except Exception:
    pass

import os
import re
import shutil

import maya.cmds as cmds

from . import define_dx11 as define
from ..add_chara_info_obj import add_chara_info_obj
from ....base_common import utility as base_utility
from ....glp_common.classes.info import chara_info


class AssignShader(object):

    def __init__(self):

        self.chara_info = None
        self.ui_paramator = {}
        self.is_target_reference = False
        self.target_reference_namespace = ''

        self.toon_matrix_nodes_dict = {}

    # ------------------------------------------------------------
    # initialize
    # ------------------------------------------------------------

    def __initialize(self, ui_paramator, current_path='', reference_namespace=''):
        """処理前設定

        Args:
            ui_paramator ([type]): [description]
            current_path (str, optional): [description]. Defaults to ''.
            reference_namespace (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """

        # UIから値が渡されていなければ動作なし
        if not ui_paramator:
            return False
        self.ui_paramator = ui_paramator

        self.__set_chara_info(current_path, reference_namespace)
        if not self.chara_info.exists:
            return False

        if self.chara_info.is_use_alternative_info:
            if not self.chara_info.alternative_info or not self.chara_info.alternative_info.exists:
                return False

        # 必要なプラグインのロード
        if not cmds.pluginInfo('dx11Shader', query=True, loaded=True):
            cmds.loadPlugin('dx11Shader.mll')
        if not cmds.pluginInfo('matrixNodes', query=True, loaded=True):
            cmds.loadPlugin('matrixNodes.mll')

        return True

    def __set_chara_info(self, current_path='', reference_namespace=''):
        """キャラクター情報を取得し、変数にセットする

        Args:
            current_path (str, optional): キャラインフォで読み込むファイルパス
            reference_namespace (str, optional): 入力すると、キャラインフォ内のデータをリファレンス名を付与して取得できる
        """

        _option = {}

        # data_type取得のために一度CharaInfoを作成
        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info(file_path=current_path, reference_namespace=reference_namespace)
        if not self.chara_info.exists:
            return

        general_tail_num = self.ui_paramator.get('general_tail_num')
        skin_num = self.ui_paramator.get('skin_num')
        mini_char_main_id = self.ui_paramator.get('mini_char_main_id')
        mini_char_sub_id = self.ui_paramator.get('mini_char_sub_id')

        # 汎用尻尾の場合、尻尾のテクスチャ番号を指定できる
        # デフォルトは1001
        if self.chara_info.part_info.data_type in ['general_tail', 'mini_general_tail']:
            if general_tail_num is not None:
                _option.update({'extra_value_dict_list': [{'name': 'CHAR_ID', 'value': general_tail_num}]})

        # ミニキャラ顔の頭部指定
        if self.chara_info.part_info.data_type == 'mini_face_head':
            if mini_char_main_id is not None and mini_char_sub_id is not None:
                _option.update({'hair_id': mini_char_main_id, 'hair_sub_id': mini_char_sub_id})

        # モブ系とミニ素体顔は肌色と毛色を見てマテリアルリンクリストを更新
        if self.chara_info.part_info.data_type in ['mini_face_head', 'mob_face_head', 'mob_hair_head']:
            if skin_num is not None:
                _option.update({'extra_value_dict_list': [{'name': 'SKINCOLOR', 'value': skin_num}]})

        self.chara_info.create_info(file_path=current_path, reference_namespace=reference_namespace, option=_option)

    # ------------------------------------------------------------
    # 実行関数
    # ------------------------------------------------------------

    def assign_dx11_shader_material(self, ui_paramator, is_change=False, is_wet=False, current_path='', reference_namespace=''):
        """DX11シェーダーを読み込みアサインする

        Args:
            ui_paramator ([type]): UIから取得してきた各種設定情報
            is_change (bool, optional): 新しくDX11をセットするのではなく、一部テクスチャ等の変更のみ加える場合はTrue
            is_wet (bool, optional): 濡れ汚れを適用するか
            current_path ([type]): キャラインフォで読み込むファイルパス
            reference_namespace ([type]): 入力すると、キャラインフォ内のデータをリファレンス名を付与して取得できる
        """

        if not self.__initialize(ui_paramator, current_path, reference_namespace):
            return

        # 初期セットアップ時にdefaultTextureListがロックされているとエラーになるので解除
        default_textures = cmds.ls('defaultTextureList*')
        if default_textures:
            for texture in default_textures:
                if cmds.lockNode(texture, q=True, l=True)[0] or cmds.lockNode(texture, q=True, lu=True)[0]:
                    cmds.error(u'defaultTextureListがロックされています シーンクリーナーを実行してください: {}'.format(texture))

        # # リファレンスにDX11を適用する際はその前に作成したdx11を破棄しない
        # if not reference_namespace:
        #     self.__remove_tmp_dx11_dir()

        for mesh in self.chara_info.part_info.mesh_list:
            if not cmds.objExists(mesh):
                continue

            material_list = base_utility.material.get_material_list(mesh)

            if not material_list:
                continue

            for material in material_list:
                original_material = material.split(define.DIVIDE_FLAG)[0]

                if original_material not in self.chara_info.part_info.material_list:
                    continue

                material_index = self.chara_info.part_info.material_list.index(original_material)

                dx11_material = original_material + define.DX11_MATERIAL_SUFFIX
                material_link = self.chara_info.part_info.material_link_list[material_index]

                # カラーベイク用のロケーターの値が飛ぶことがあったため、一度値を評価しておく
                self.__evaluate_color_locator_val()

                # 新規適用の際、セットしたいDX11Materialが存在する場合は処理しない
                # 但しDX11→WET、WET→DX11のように状態変更を行う場合は処理を実行する
                if not is_change and cmds.objExists(dx11_material) and dx11_material == material:
                    dx11_material_mainTex_texture = self.__get_texture_from_material_file_node(dx11_material, define.DIFF_TEX_ATTR)
                    in_wet = dx11_material_mainTex_texture.find('_wet') >= 0

                    if is_wet == in_wet:
                        # wetがない場合などテクスチャが取れていない場合はスキップしないようにする
                        if dx11_material_mainTex_texture != define.WHITE_TEXTURE_PATH:
                            continue

                # DX11が読み込まれていない時は一部変更を行わない
                if is_change and not cmds.objExists(dx11_material):
                    continue

                # mobの目と眉はテスト用にテクスチャを乗せる
                is_test_texture = False
                if self.chara_info.part_info.data_type.startswith('mob_'):
                    if dx11_material.find('eye') >= 0 or dx11_material.find('mayu') >= 0:
                        is_test_texture = True

                # Miniとテスト用テクスチャ以外にはbaseテクスチャが必要
                if not self.chara_info.is_mini and not is_test_texture:
                    if 'base' not in material_link:
                        continue

                # ラメ・スパンコール用のrflかどうかテクスチャがあるかで判定する
                has_reflection = False
                reflection_texture_info = self.__get_texture_info_from_material_link(material_link, 'reflection')
                if reflection_texture_info and os.path.exists(reflection_texture_info[2]):
                    has_reflection = True

                # dx11マテリアルの作成
                if not self.__create_dx11_material(dx11_material, has_reflection):
                    continue

                self.__create_info_locators(has_reflection)
                self.__create_chara_light()

                # 部位変更の場合はwetかどうかテクスチャ状況から把握する
                if is_change:
                    result = self.__get_texture_from_material_file_node(dx11_material, define.DIFF_TEX_ATTR)
                    is_wet = result.find('_wet.tga') > -1

                # 各種パラメーターの設定
                self.__set_texture_to_dx11_material(dx11_material, material_link, is_wet, is_test_texture)
                self.__set_dx11_material_specular_color(dx11_material)
                self.__set_dx11_material_rfl_color(dx11_material)
                self.__set_dx11_material_rfl_pow_value(dx11_material)
                self.__set_dx11_material_value(dx11_material)
                self.__set_dx11_material_mask_color_value(dx11_material)

                matrix_nodes = []
                matrix_nodes.extend(self.__connect_dx11_material_head_center_locator(dx11_material))
                matrix_nodes.extend(self.__connect_dx11_material_head_vector(dx11_material))
                if dx11_material in self.toon_matrix_nodes_dict:
                    self.toon_matrix_nodes_dict[dx11_material].extend(matrix_nodes)
                else:
                    self.toon_matrix_nodes_dict[dx11_material] = matrix_nodes

                self.__connect_chara_light_and_dx11_material(dx11_material)
                self.__replace_material(material, dx11_material, mesh)

    def assign_outline_dx11_shader_material(self, ui_paramator):
        """アウトラインDX11シェーダーを読み込みアサインする

        Args:
            ui_paramator ([type]): UIから取得してきた各種設定情報
        """

        if not self.__initialize(ui_paramator):
            return

        self.__change_outline_visible_state(True)
        self.__remove_tmp_outline_dx11_dir()

        for outline_mesh in self.chara_info.part_info.outline_mesh_list:

            if not cmds.objExists(outline_mesh):
                continue

            material_list = base_utility.material.get_material_list(outline_mesh)
            if not material_list:
                continue

            for material in material_list:

                if not cmds.objExists(material):
                    continue

                if material.find(define.DX11_OUTLINE_MATERIAL_SUFFIX) >= 0:
                    continue

                # 目のMaterialにはアウトラインを適用しない
                if material.find('_eye') >= 0:
                    continue

                material_root = material.split(define.DIVIDE_FLAG)[0]
                dx11_material = material_root + define.DX11_OUTLINE_MATERIAL_SUFFIX

                # 存在しない場合はdx11マテリアルを作成
                if not cmds.objExists(dx11_material):
                    self.__create_dx11_material(dx11_material)
                    self.__set_texture_for_outline_dx11_material(dx11_material, outline_mesh)
                    self.__set_outline_dx11_material_value(dx11_material, self.chara_info.part_info.data_type)

                self.__replace_material(material, dx11_material, outline_mesh)

    def remove_outline_dx11_shader_material(self, ui_paramator):
        """アウトラインDX11シェーダーを取り除く

        Args:
            ui_paramator ([type]): UIから取得してきた各種設定情報
        """

        if not self.__initialize(ui_paramator):
            return

        self.__change_outline_visible_state(False)
        self.__adjust_outline_material_to_base_material()
        self.__remove_dx11_material(True)

    def assign_default_material(self, texture_type, ui_paramator, current_path='', reference_namespace=''):
        """モデルデフォルトのマテリアルをアサインする
        DX11マテリアルがある場合は破棄する

        Args:
            texture_type ([type]): デフォルトモデルのMaterialに変更する際適用するテクスチャの種類(diff, shad_c, or psd)
            ui_paramator ([type]): UIから取得してきた各種設定情報
            current_path ([type]): キャラインフォで読み込むファイルパス
            reference_namespace ([type]): 入力すると、キャラインフォ内のデータをリファレンス名を付与して取得できる
        """

        if not self.__initialize(ui_paramator, current_path, reference_namespace):
            return

        self.__revert_to_default_material()
        self.change_default_material_texture(texture_type)

        # リファレンスのオブジェクト処理中はdx11マテリアルを削除しない
        if not reference_namespace:
            self.__remove_dx11_material()
            self.__remove_map_material()

    def change_default_material_texture(self, texture_type):
        """モデルデフォルトのマテリアルのテクスチャを変更・適用する

        Args:
            texture_type ([type]): デフォルトモデルのMaterialに変更する際適用するテクスチャの種類(diff, shad_c, or psd)
        """

        for assign_texture_info in self.__get_assing_texture_info_list_from_chara_info(texture_type):
            self.__apply_texture_to_material_assigned_file_node(
                assign_texture_info.get('target_material'),
                assign_texture_info.get('target_attr'),
                assign_texture_info.get('target_texture_path')
            )

    def assign_map_material(self, texture, channel, ui_paramator, current_path='', reference_namespace=''):
        """各種マップ表示用マテリアルを作成しアサインする

        Args:
            map_type (str): マップの種類
            texture (str): テクスチャ名('base' or 'ctrl')
            channel (str): 出力チャンネル('R' or 'G' or 'B')
            ui_paramator ([type]): UIから取得してきた各種設定情報
            current_path ([type]): キャラインフォで読み込むファイルパス
            reference_namespace ([type]): 入力すると、キャラインフォ内のデータをリファレンス名を付与して取得できる
        """

        if not self.__initialize(ui_paramator, current_path, reference_namespace):
            return

        for mesh in self.chara_info.part_info.mesh_list:
            if not cmds.objExists(mesh):
                continue

            material_list = base_utility.material.get_material_list(mesh)

            if not material_list:
                continue

            for material in material_list:
                original_material = material.split(define.DIVIDE_FLAG)[0]

                if original_material not in self.chara_info.part_info.material_list:
                    continue

                material_index = self.chara_info.part_info.material_list.index(original_material)

                map_material = original_material + define.MAP_MATERIAL_SUFFIX
                material_link = self.chara_info.part_info.material_link_list[material_index]

                if texture not in material_link:
                    continue

                # surfaceマテリアルの作成
                if not self.__create_surface_material(map_material):
                    continue

                is_wet = False

                dx11_material = original_material + define.DX11_MATERIAL_SUFFIX
                if cmds.objExists(dx11_material):
                    result = self.__get_texture_from_material_file_node(dx11_material, define.DIFF_TEX_ATTR)
                    is_wet = result.find('_wet.tga') > -1

                self.__set_texture_to_map_material(map_material, material_link, texture, channel, is_wet)

                # 割り当てなおし前にスペキュラー値などを確実にロケーターに渡す
                self.__reapply_connection_param(material)

                self.__replace_material(material, map_material, mesh)

    def get_material_state(self, ui_parameter):
        """現在メッシュに割り当てられているマテリアルの状態を取得する

        Returns:
            dict[str, str] or None: マテリアルの状態を表す辞書
        """

        if not self.__initialize(ui_parameter):
            return None

        for mesh in self.chara_info.part_info.mesh_list:
            if not cmds.objExists(mesh):
                continue

            material_list = base_utility.material.get_material_list(mesh)

            if not material_list:
                continue

            for material in material_list:
                if cmds.objExists(material):
                    return self.__create_material_state(material)

    # ------------------------------------------------------------
    # その他関数
    # ------------------------------------------------------------

    def __create_dx11_material(self, dx11_material, has_reflection=False):
        """DX11シェーダー付きのマテリアルを作成する

        Args:
            dx11_material ([type]): 作成するDX11マテリアル名

        Returns:
            bool: 作成が正常に行えていたらTrue, 失敗している場合はFalse
        """

        if not cmds.objExists(dx11_material):
            cmds.shadingNode('dx11Shader', name=dx11_material, asShader=True)

        this_dx11_file = self.__get_dx11_file(dx11_material, has_reflection).replace('\\', '/')
        if this_dx11_file:
            cmds.setAttr(dx11_material + '.shader', this_dx11_file, typ='string')
            # dx11で頂点カラーが自動で刺さらないので、setAttrする
            self.__connect_vertex_color_attr_to_dx11_material(dx11_material)
            return True

        return False

    def __create_surface_material(self, surface_material):
        """Surfaceシェーダー付きのマテリアルを作成する

        Args:
            surface_material (str): 作成するマテリアル名

        Returns:
            bool: 作成が正常に行えていたらTrue, 失敗している場合はFalse
        """

        if not cmds.objExists(surface_material):
            cmds.shadingNode('surfaceShader', name=surface_material, asShader=True)

            file_node = cmds.shadingNode('file', asTexture=True)
            p2t_node = cmds.shadingNode('place2dTexture', asUtility=True)

            base_utility.material.connect_p2t_node_to_file_node(p2t_node, file_node)

            for c in ['R', 'G', 'B']:
                self.__connect_node_attr(file_node, 'outColorR', surface_material, 'outColor' + c)

        if not cmds.objExists(surface_material):
            return False

        return True

    def __create_info_locators(self, has_reflection=False):
        """SpecやrflのInfoロケーターを追加する

        Args:
            has_reflection (bool): リフレクション要素があるか
        """

        add_obj = add_chara_info_obj.AddCharaInfoObj()

        if self.chara_info.part_info.data_type.endswith('head'):

            add_obj.add_obj('locator', 'Face_spec_info')
            add_obj.add_obj('locator', 'Hair_spec_info')

            if has_reflection:
                # 顔にrflは無いので髪だけ
                add_obj.add_obj('locator', 'Hair_rfl_add_info')
                add_obj.add_obj('locator', 'Hair_rfl_mul_info')
                add_obj.add_obj('locator', 'Hair_rfl_pow_info')

        elif self.chara_info.part_info.data_type.endswith('body'):

            match_obj = re.match(r'bdy0001_[0-9]{2}', self.chara_info.data_id)

            if match_obj:
                add_obj.add_obj('locator', 'Body_spec_info_0')
                add_obj.add_obj('locator', 'Body_spec_info_1')
                add_obj.add_obj('locator', 'Body_spec_info_2')
            else:
                add_obj.add_obj('locator', 'Body_spec_info')

            if has_reflection:
                add_obj.add_obj('locator', 'Body_rfl_add_info')
                add_obj.add_obj('locator', 'Body_rfl_mul_info')
                add_obj.add_obj('locator', 'Body_rfl_pow_info')

        elif self.chara_info.part_info.data_type.endswith('tail'):

            if has_reflection:
                add_obj.add_obj('locator', 'Tail_rfl_add_info')
                add_obj.add_obj('locator', 'Tail_rfl_mul_info')
                add_obj.add_obj('locator', 'Tail_rfl_pow_info')

        elif self.chara_info.part_info.data_type.endswith('toon_prop'):

            add_obj.add_obj('locator', 'ToonProp_spec_info')

            if has_reflection:
                add_obj.add_obj('locator', 'ToonProp_rfl_add_info')
                add_obj.add_obj('locator', 'ToonProp_rfl_mul_info')
                add_obj.add_obj('locator', 'ToonProp_rfl_pow_info')

    def __create_chara_light(self):
        """キャラライトを作成する
        """

        if not cmds.objExists(define.CHARA_LIGHT0):
            cmds.pointLight(name=define.CHARA_LIGHT0)

        if not cmds.objExists(define.CHARA_LIGHT0_DX11_VECTOR):
            cmds.shadingNode('dx11Vector', name=define.CHARA_LIGHT0_DX11_VECTOR, asShader=True)

        light0_translate_attr = '{}.{}'.format(define.CHARA_LIGHT0, 'translate')
        if cmds.getAttr(light0_translate_attr) == [(0, 0, 0)]:
            cmds.setAttr(light0_translate_attr, 30, 30, 30)

    def __remove_chara_light(self):
        """シーン上のキャラライトを削除する
        DX11を削除しても残ってしまう為
        """

        if cmds.objExists(define.CHARA_LIGHT0):
            cmds.delete(define.CHARA_LIGHT0)

        if cmds.objExists(define.CHARA_LIGHT0_DX11_VECTOR):
            cmds.delete(define.CHARA_LIGHT0_DX11_VECTOR)

    def __get_texture_from_material_file_node(self, material, attr):
        """対象のマテリアルの指定アトリビュートに接続されているfileノードからテクスチャパスを取得する

        Args:
            material ([type]): fileNodeを取得したいマテリアル
            attr_name ([type]): fileNodeを取得したいアトリビュート

        Returns:
            str: テクスチャパス or ''
        """

        if not cmds.objExists(material) or not self.__check_exists_attr(material, attr):
            return ''

        this_file_node_list = cmds.listConnections('{0}.{1}'.format(material, attr), type='file')
        if not this_file_node_list:
            return ''

        return cmds.getAttr('{}.fileTextureName'.format(this_file_node_list[0]))

    def __set_texture_to_dx11_material(self, dx11_material, material_link, is_wet, is_test_texture):
        """テクスチャをマテリアルリンクリストを利用してDX11マテリアルの設定する

        Args:
            dx11_material ([type]): テクスチャをセットするマテリアル
            material_link ([type]): テクスチャ⇔マテリアルの結びつき辞書
            is_wet (bool): 濡れ汚れかどうか
            is_test_texture (bool): テストテクスチャ(Mobの目と眉用のテクスチャ)を載せるかどうか
        """

        dx11_default_attr_path_info_dict = define.DX11_DEFAULT_ATTR_PATH_INFO_DICT.copy()

        base_default_texture = define.BLACK_TEXTURE_PATH
        # テストテクスチャの場合はtex_chr_blackではなくtex_chr_base_blendを使用する
        if is_test_texture:
            base_default_texture = define.BASE_BLEND_TEXTURE_PATH

        # マテリアルリンクから情報の取得
        diff_flag = 'diff' if not is_wet else 'diff_wet'
        base_flag = 'base' if not is_wet else 'base_wet'
        shad_c_flag = 'shad_c' if not is_wet else 'shad_c_wet'
        ctrl_flag = 'ctrl' if not is_wet else 'ctrl_wet'
        emissive_flag = 'emissive' if not is_wet else 'emissive_wet'
        area_flag = 'area' if not is_wet else 'area_wet'
        dirt_flag = 'dirt'
        reflection_flag = 'reflection'

        # マテリアルリンクから該当のテクスチャパスを取得する
        diff_texture_info = self.__get_texture_info_from_material_link(material_link, diff_flag)
        base_texture_info = self.__get_texture_info_from_material_link(material_link, base_flag)
        shad_c_texture_info = self.__get_texture_info_from_material_link(material_link, shad_c_flag)
        ctrl_texture_info = self.__get_texture_info_from_material_link(material_link, ctrl_flag)
        emissive_texture_info = self.__get_texture_info_from_material_link(material_link, emissive_flag)
        area_texture_info = self.__get_texture_info_from_material_link(material_link, area_flag)
        dirt_texture_info = self.__get_texture_info_from_material_link(material_link, dirt_flag)
        reflection_texture_info = self.__get_texture_info_from_material_link(material_link, reflection_flag)

        # diff
        if diff_texture_info is not None:
            diff_texture_path = self.__get_replaced_difference_texture_path_from_ui_param(diff_texture_info[2])
            diff_texture_path = self.__get_replaced_color_texture_path_from_ui_param(diff_texture_path)
            dx11_default_attr_path_info_dict[define.DIFF_TEX_ATTR] = [diff_texture_path, define.WHITE_TEXTURE_PATH]

        # shad_c
        if shad_c_texture_info is not None:
            shad_c_texture_path = self.__get_replaced_difference_texture_path_from_ui_param(shad_c_texture_info[2])
            shad_c_texture_path = self.__get_replaced_color_texture_path_from_ui_param(shad_c_texture_path)
            dx11_default_attr_path_info_dict[define.SHAD_TEX_ATTR] = [shad_c_texture_path, define.GRAY_TEXTURE_PATH]

        # base
        if base_texture_info is not None:
            base_texture_path = self.__get_replaced_difference_texture_path_from_ui_param(base_texture_info[2], is_change_skin=False)
            dx11_default_attr_path_info_dict[define.BASE_TEX_ATTR] = [base_texture_path, base_default_texture]

        # ctrl
        if ctrl_texture_info is not None:
            ctrl_texture_path = self.__get_replaced_difference_texture_path_from_ui_param(ctrl_texture_info[2], is_change_skin=False)
            dx11_default_attr_path_info_dict[define.CTRL_TEX_ATTR] = [ctrl_texture_path, define.BLACK_TEXTURE_PATH]

        # dirt
        if dirt_texture_info is not None:
            dx11_default_attr_path_info_dict[define.DIRT_TEX_ATTR] = [dirt_texture_info[2], define.BLACK_TEXTURE_PATH]

        # emi
        if emissive_texture_info is not None:
            dx11_default_attr_path_info_dict[define.EMI_TEX_ATTR] = [emissive_texture_info[2], define.BLACK_TEXTURE_PATH]

        # area
        if area_texture_info is not None:
            dx11_default_attr_path_info_dict[define.AREA_TEX_ATTR] = [area_texture_info[2], define.GRAY_TEXTURE_PATH]
        # UIParamで値が渡されている場合には強制オーバーライド処理する
        if self.ui_paramator['area_num'] != -1:
            area_texture_path = self.__get_area_texture_path_from_ui_param()
            if area_texture_path:
                dx11_default_attr_path_info_dict[define.AREA_TEX_ATTR] = [area_texture_path, define.GRAY_TEXTURE_PATH]

        # reflection
        if reflection_texture_info is not None:
            dx11_default_attr_path_info_dict[define.RFL_TEX_ATTR] = [reflection_texture_info[2], define.BLACK_TEXTURE_PATH]

        # 設定
        for attr, val in list(dx11_default_attr_path_info_dict.items()):
            self.__apply_texture_to_material_assigned_file_node(dx11_material, attr, val[0], val[1])

    def __set_texture_to_map_material(self, map_material, material_link, texture, channel, is_wet):
        """マテリアルリンクリストを利用してマップマテリアルを設定する

        Args:
            map_material (str): テクスチャをセットするマテリアル
            material_link ([type]): テクスチャ⇔マテリアルの結びつき辞書
            texture (str): テクスチャ名('base' or 'ctrl')
            channel (str): 出力チャンネル('R' or 'G' or 'B')
            is_wet (bool): 濡れ汚れかどうか
        """

        texture_flag = texture

        if is_wet:
            texture_flag += '_wet'

        # マテリアルリンクから該当のテクスチャパスを取得する
        texture_info = self.__get_texture_info_from_material_link(material_link, texture_flag)

        if texture_info is not None:
            texture_path = self.__get_replaced_difference_texture_path_from_ui_param(texture_info[2], is_change_skin=False)
            self.__set_texture_and_channel(map_material, texture_path, channel)

    def __get_texture_info_from_material_link(self, material_link, texture_type):
        """マテリアルとテクスチャの結びつきリストからテクスチャ情報を取得する

        Args:
            material_link ([type]): テクスチャ⇔マテリアルの結びつき辞書
            texture_type ([type]): リンクリストから情報を取得したいテクスチャの属性

        Returns:
            [type]: None or テクスチャリストのindex, テクスチャ名、テクスチャパス(taple)
        """

        texture_index = material_link.get(texture_type)
        if texture_index is None:
            return None

        texture_name = ''
        texture_path = ''

        for texture_param in self.chara_info.part_info.texture_param_list:

            if texture_param['id'] == texture_index:

                texture_name = texture_param['name']
                texture_path = '{0}/{1}'.format(
                    self.chara_info.part_info.maya_sourceimages_dir_path,
                    texture_name
                )
                break

        if texture_name and texture_path:
            return texture_index, texture_name, texture_path

        # Mini顔対応
        if not self.chara_info.is_use_alternative_info:
            return None

        for texture_param in self.chara_info.alternative_info.texture_param_list:

            if texture_param['alternate_id'] == texture_index:

                texture_name = texture_param['name']
                texture_path = '{0}/{1}'.format(
                    self.chara_info.alternative_info.maya_sourceimages_dir_path,
                    texture_name
                )
                return texture_index, texture_name, texture_path

        else:
            return None

    def __get_replaced_color_texture_path_from_ui_param(self, texture_path):
        """UIから渡された肌色とバストの値に応じて置換したテクスチャパスを取得し返す

        Args:
            texture_path ([type]): 肌色とバストの値を置換するテクスチャパス

        Returns:
            [type]: 置換されたテクスチャパス
        """

        change_color_num = self.ui_paramator.get('color_num')
        # change_color_numが設定されていないか、color_numが0より小さい(=初期値)だったら置換せず次へ
        if change_color_num is None or change_color_num < 0:
            return texture_path

        change_color_str = str(change_color_num).zfill(2)
        color_diff_folder_name = ''
        tex_file_name = ''

        tmp_dir_list = texture_path.split('/')
        if len(tmp_dir_list) < 2:
            return texture_path

        color_diff_folder_name = tmp_dir_list[-2]
        tex_file_name = tmp_dir_list[-1]

        match_pattern = r'_([0-9])_([0-9])_[0-9]{2}_'
        match_obj = re.search(match_pattern, tex_file_name)

        if match_obj:

            skin_num = match_obj.group(1)
            bust_num = match_obj.group(2)
            replace_str = '_{0}_{1}_{2}_'.format(skin_num, bust_num, change_color_str)
            new_tex_file_name = re.sub(match_pattern, replace_str, tex_file_name)

            texture_path = texture_path.replace(
                color_diff_folder_name + '/' + tex_file_name,
                change_color_str + '/' + new_tex_file_name
            )

        return texture_path

    def __get_area_texture_path_from_ui_param(self):
        """UIで指定されている値にマッチするテクスチャのパスを返します

        Returns:
            str: テクスチャのパス
        """
        if self.ui_paramator['area_num'] == -1:
            return None

        # 当該パターンにマッチするテクスチャのパスを探す
        source_image_path = self.chara_info.part_info.maya_sourceimages_dir_path
        if not os.path.exists(source_image_path):
            return None

        for target_file in os.listdir(source_image_path):
            current_path = os.path.join(source_image_path, target_file)
            if not os.path.isfile(current_path):
                continue

            if target_file.endswith('_{:0>2}_area.tga'.format(self.ui_paramator['area_num'])):
                return current_path

        return None

    def __apply_texture_to_material_assigned_file_node(self, material, attr, texture_path, default_texture_path=None):
        """テクスチャをマテリアルの特定のAttrにアサインされているfileノードにセットする

        Args:
            material (str): セットするマテリアル名
            attr (str): fileノードを検索するアトリビュート名
            texture_path (str): セットするテクスチャパス
            default_texture_path (str, optional): テクスチャパスがfileではない場合にセットされる
                                                  デフォルトテクスチャ名
        """

        if not cmds.objExists(material) or not self.__check_exists_attr(material, attr):
            return

        target_texture_file_path = default_texture_path
        if os.path.isfile(texture_path):
            target_texture_file_path = texture_path

        if target_texture_file_path is None or not os.path.isfile(target_texture_file_path):
            return

        this_file_node_list = cmds.listConnections('{0}.{1}'.format(material, attr), type='file')
        if not this_file_node_list:
            return

        cmds.setAttr(
            '{}.{}'.format(this_file_node_list[0], 'fileTextureName'),
            target_texture_file_path,
            type='string')

    def __set_dx11_material_specular_color(self, dx11_material):
        """DX11マテリアルのスペキュラカラーの値を設定する

        spec_infoロケーター(=Scale値にスペキュラ値を入れてUnityで呼び出しクライアントに情報を渡す)が
        有れば接続しスペキュラカラーをロケーターから取得する

        Args:
            dx11_material ([type]): specular値を設定するDX11マテリアル名
        """

        # spec_color_locaterがあれば、それのスケールを_SpecularColorにコネクト
        # なければ定義してある初期値をセット
        spec_info_locator = self.__search_spec_info_locator(dx11_material)

        if spec_info_locator:

            self.__clamp_scale_value_in_01range(spec_info_locator)
            specular_color = cmds.getAttr('{}.scale'.format(spec_info_locator))[0]

            self.__connect_loc_scale_to_mtl_color(spec_info_locator, dx11_material, 'xSpecularColor')

        else:
            specular_color = [1.0, 1.0, 1.0]

        if self.__check_exists_attr(dx11_material, 'xSpecularColor'):
            cmds.setAttr('{}.xSpecularColor.xSpecularColorRGB'.format(dx11_material), *specular_color)

    def __evaluate_color_locator_val(self):
        """スケールに色情報をベイクしているロケーターの値を評価する
        スケールアトリビュートが飛ぶ場合があり（Mayaのバグか？）、一度値をgetAttr()で評価することで回避できるためにこのメソッドを使用
        """

        color_locator_suffixes = ['_rfl_add_info', '_rfl_mul_info', '_spec_info']
        color_locators = self.__fetch_chara_locators_with_suffix(color_locator_suffixes)

        if not color_locators:
            return

        for color_locator in color_locators:
            cmds.getAttr('{}.scale'.format(color_locator))[0]

    def __set_dx11_material_rfl_color(self, dx11_material):
        """DX11マテリアルのリフレクション用カラーの値を設定する

        ここでいうリフレクションはラメ・スパンコール用の疑似的なもので、仕組みは環境マップに近い
        rfl_infoロケーター(=Scale値に加算・乗算の色を入れてUnityで呼び出しクライアントに情報を渡す)が
        有れば接続しリフレクションカラーをロケーターから取得する

        Args:
            dx11_material ([type]): リフレクション値を設定するDX11マテリアル名
        """

        add_color_loc_suffix = '_rfl_add_info'
        mul_color_loc_suffix = '_rfl_mul_info'
        add_color_attr = 'xReflectionAddColor'
        mul_color_attr = 'xReflectionMulColor'

        # rfl_color_locaterがあれば、それのスケールを_RflAddColor,_RflMulColorにコネクト
        color_locator_list = self.__fetch_chara_locators_with_suffix([add_color_loc_suffix, mul_color_loc_suffix])

        if not color_locator_list:
            return

        for color_locator in color_locator_list:

            self.__clamp_scale_value_in_01range(color_locator)
            rfl_color = cmds.getAttr('{}.scale'.format(color_locator))[0]

            target_attr = None
            if color_locator.endswith(add_color_loc_suffix):
                target_attr = add_color_attr
            elif color_locator.endswith(mul_color_loc_suffix):
                target_attr = mul_color_attr
            else:
                continue

            self.__connect_loc_scale_to_mtl_color(color_locator, dx11_material, target_attr)

            if self.__check_exists_attr(dx11_material, target_attr):
                cmds.setAttr('{}.{}'.format(dx11_material, target_attr), *rfl_color)

    def __connect_loc_scale_to_mtl_color(self, locator, material, material_color_attr):
        """ロケーターのスケールXYZをマテリアルのカラーRGBに接続する
        """

        if not self.__check_exists_attr(material, material_color_attr):
            return
        if not cmds.objExists(locator):
            return

        for scale_attr, color_attr in zip(['X', 'Y', 'Z'], ['R', 'G', 'B']):

            loc_scale_attr = '{}.scale.scale{}'.format(locator, scale_attr)
            material_rfl_color_attr = '{0}.{1}{2}'.format(material, material_color_attr, color_attr)

            if cmds.listConnections(loc_scale_attr):
                return
            if cmds.isConnected(material_rfl_color_attr, loc_scale_attr):
                return
            cmds.connectAttr(material_rfl_color_attr, loc_scale_attr, f=True)

    def __set_dx11_material_rfl_pow_value(self, dx11_material):
        """DX11マテリアルのリフレクション用カラーの乗数値を設定する

        ここでいうリフレクションはラメ・スパンコール用の疑似的なもので、仕組みは環境マップに近い
        pow_value_locロケーター(=ScaleX値に色の乗数を入れてUnityで呼び出しクライアントに情報を渡す)が
        有れば接続し乗数をロケーターから取得する

        Args:
            dx11_material ([type]): リフレクション値を設定するDX11マテリアル名
        """

        pow_value_loc_sffix = 'rfl_pow_info'
        pow_value_attr = 'xReflectionPowVal'

        # rfl_color_locaterがあれば、それのスケールを_RflAddColor,_RflMulColorにコネクト
        value_locator_list = self.__fetch_chara_locators_with_suffix([pow_value_loc_sffix])

        if not value_locator_list:
            return
        if not self.__check_exists_attr(dx11_material, pow_value_attr):
            return

        loc_scale_x_attr = '{}.scale.scaleX'.format(value_locator_list[0])
        material_pow_val_attr = '{}.{}'.format(dx11_material, pow_value_attr)
        loc_value = cmds.getAttr(loc_scale_x_attr)

        if cmds.listConnections(loc_scale_x_attr):
            return
        if cmds.isConnected(material_pow_val_attr, loc_scale_x_attr):
            return
        cmds.connectAttr(material_pow_val_attr, loc_scale_x_attr, f=True)

        cmds.setAttr('{}.{}'.format(dx11_material, pow_value_attr), loc_value)

    def __set_dx11_material_value(self, dx11_material):
        """DX11マテリアルのアトリビュートに値をセットする

        Args:
            dx11_material ([type]): 値をセットするDX11マテリアル
        """

        dx11_attr_val_dict = define.DX11_DEFAULT_ATTR_DICT.copy()

        # ui要素から引き渡す値は別途追加する
        dx11_attr_val_dict.update({
            'xDirtRate1': self.ui_paramator.get('dirt_rate_list')[0],
            'xDirtRate2': self.ui_paramator.get('dirt_rate_list')[1],
            'xDirtRate3': self.ui_paramator.get('dirt_rate_list')[2]
        })

        data_type = self.chara_info.part_info.data_type

        if data_type.endswith('head') or data_type.endswith('toon_prop'):

            dx11_attr_val_dict['xRimColorA'] = 50 / 255
            dx11_attr_val_dict['xCutoff'] = 0.5

            if dx11_material.find('_hair') > -1:
                dx11_attr_val_dict['xToonStep'] = 0.3

        elif data_type.endswith('body') or data_type.endswith('attach') or data_type.endswith('toon_prop'):

            if dx11_material.find('_tail') < 0:
                dx11_attr_val_dict['xCutoff'] = 0.5

            else:
                dx11_attr_val_dict['xRimColorA'] = 50 / 255

        if dx11_material.find('Alpha') >= 0:
            dx11_attr_val_dict['xCutoff'] = 0.2

        # 値のセット
        for attr, val in list(dx11_attr_val_dict.items()):

            if not self.__check_exists_attr(dx11_material, attr):
                continue

            if type(val) == list:
                cmds.setAttr('{}.{}'.format(dx11_material, attr), *val)
            else:
                cmds.setAttr('{}.{}'.format(dx11_material, attr), val)

    def __set_dx11_material_mask_color_value(self, dx11_material):
        """DX11マテリアルのマスクカラーをセットする

        Args:
            dx11_material ([type]): 値をセットするDX11マテリアル
        """

        target_mask_color_param = None
        if dx11_material.find('hair') >= 0:
            target_mask_color_param = define.HAIR_MASK_COLOR_PARAM_DICT.copy()
        elif dx11_material.find('eye') >= 0:
            target_mask_color_param = define.EYE_MASK_COLOR_PARAM_DICT.copy()
        elif dx11_material.find('face') >= 0 or dx11_material.find('mayu') >= 0:
            target_mask_color_param = define.FACE_MASK_COLOR_PARAM_DICT.copy()
        elif dx11_material.find('bdy') >= 0:
            target_mask_color_param = define.BODY_MASK_COLOR_PARAM_DICT.copy()
        else:
            return

        for attr, color_value_param in list(target_mask_color_param.items()):

            for attr_color_id, color_value in list(color_value_param.items()):

                if not self.__check_exists_attr(dx11_material, attr + attr_color_id):
                    continue

                cmds.setAttr('{}.{}{}'.format(dx11_material, attr, attr_color_id), *color_value)

    def __connect_dx11_material_head_center_locator(self, dx11_material):
        """DX11マテリアルにHeadCenterLocaterを接続する

        Args:
            dx11_material ([str]): HeadCenterLocaterを接続するDX11マテリアル
        Returns:
            [list]: 作成したマトリクスノードリスト
        """

        matrix_nodes = []
        head_center_locator = self.__fetch_head_center_locator(dx11_material)
        if head_center_locator:

            matrix_decomposer = head_center_locator.split('|')[-1] + '_world_matrix_decomposer'
            if not cmds.objExists(matrix_decomposer):
                cmds.shadingNode('decomposeMatrix', au=True, n=matrix_decomposer)

            cmds.connectAttr(head_center_locator + '.worldMatrix[0]', matrix_decomposer + '.inputMatrix', f=True)
            cmds.connectAttr(matrix_decomposer + '.outputTranslate', dx11_material + '.xFaceCenterPos', f=True)
            matrix_nodes = [matrix_decomposer]

        return matrix_nodes

    def __fetch_head_center_locator(self, dx11_material):
        """シーンに存在するHeadCenterLocatorを取得する

        Args:
            dx11_material ([type]): Head_center_locatorを取得するタイプを取得する用のDX11マテリアル名

        Returns:
            [type]: Head_center_locator名
        """

        if not self.chara_info.part_info.data_type.endswith('head'):
            return None

        target_locator_name = 'Head_tube_center_offset'
        if dx11_material.find('_face') < 0:
            target_locator_name = 'Head_center_offset'

        for locater in self.chara_info.part_info.locator_list:
            if locater.find(target_locator_name) > -1 and cmds.objExists(locater):
                return locater

        return None

    def __connect_dx11_material_head_vector(self, dx11_material):
        """Headの姿勢をマテリアルに渡すマトリクスノード群を作成

        Args:
            dx11_material ([str]): HeadCenterLocaterを接続するDX11マテリアル
        Returns:
            [list]: 作成したマトリクスノードリスト
        """

        matrix_nodes = []
        head_joint = self.__fetch_head_joint()
        if head_joint:

            head_world_rot = ''
            if not cmds.objExists(head_world_rot):
                head_world_rot = cmds.shadingNode('decomposeMatrix', au=True, n='headWorldRot_' + dx11_material)

            head_rot_mtx = 'headRotMatrix_' + dx11_material
            if not cmds.objExists(head_rot_mtx):
                head_rot_mtx = cmds.shadingNode('composeMatrix', au=True, n='headRotMatrix_' + dx11_material)

            forward_vector = 'forwardVector_' + dx11_material
            if not cmds.objExists(forward_vector):
                forward_vector = cmds.shadingNode('composeMatrix', au=True, n='forwardVector_' + dx11_material)
                cmds.setAttr(forward_vector + '.inputTranslateZ', 1)

            up_vector = 'upVector_' + dx11_material
            if not cmds.objExists(up_vector):
                up_vector = cmds.shadingNode('composeMatrix', au=True, n='upVector_' + dx11_material)
                cmds.setAttr(up_vector + '.inputTranslateY', 1)

            forward_mult = 'forwardMult_' + dx11_material
            if not cmds.objExists(forward_mult):
                forward_mult = cmds.shadingNode('multMatrix', au=True, n='forwardMult_' + dx11_material)

            up_mult = 'upMult_' + dx11_material
            if not cmds.objExists(up_mult):
                up_mult = cmds.shadingNode('multMatrix', au=True, n='upMult_' + dx11_material)

            forward_decompose = 'forwardDecompose_' + dx11_material
            if not cmds.objExists(forward_decompose):
                forward_decompose = cmds.shadingNode('decomposeMatrix', au=True, n='forwardDecompose_' + dx11_material)

            up_decompose = 'upDecompose_' + dx11_material
            if not cmds.objExists(up_decompose):
                up_decompose = cmds.shadingNode('decomposeMatrix', au=True, n='upDecompose_' + dx11_material)

            matrix_nodes = [
                head_world_rot,
                head_rot_mtx,
                forward_vector,
                up_vector,
                forward_mult,
                up_mult,
                forward_decompose,
                up_decompose,
            ]

            cmds.connectAttr(head_joint + '.worldMatrix', head_world_rot + '.inputMatrix', f=True)
            cmds.connectAttr(head_world_rot + '.outputRotate', head_rot_mtx + '.inputRotate', f=True)
            cmds.connectAttr(forward_vector + '.outputMatrix', forward_mult + '.matrixIn[0]', f=True)
            cmds.connectAttr(head_rot_mtx + '.outputMatrix', forward_mult + '.matrixIn[1]', f=True)
            cmds.connectAttr(up_vector + '.outputMatrix', up_mult + '.matrixIn[0]', f=True)
            cmds.connectAttr(head_rot_mtx + '.outputMatrix', up_mult + '.matrixIn[1]', f=True)
            cmds.connectAttr(forward_mult + '.matrixSum', forward_decompose + '.inputMatrix', f=True)
            cmds.connectAttr(up_mult + '.matrixSum', up_decompose + '.inputMatrix', f=True)

            cmds.connectAttr(forward_decompose + '.outputTranslate', dx11_material + '.xFaceForward', f=True)
            cmds.connectAttr(up_decompose + '.outputTranslate', dx11_material + '.xFaceUp', f=True)

        return matrix_nodes

    def __fetch_head_joint(self):

        if not self.chara_info.part_info.data_type.endswith('head'):
            return None

        for joint in self.chara_info.part_info.joint_list:
            if joint.endswith('Head') and cmds.objExists(joint):
                return joint

    def __connect_chara_light_and_dx11_material(self, dx11_material):
        """DX11マテリアルとキャラライトを接続する

        Args:
            dx11_material ([type]): 接続するDX11マテリアル
        """

        scr_attr = '{}.{}'.format(define.CHARA_LIGHT0, 'translate')
        dst_attr = '{}.{}'.format(dx11_material, 'xWorldSpaceLightPos0')

        # お互いがつながっていない場合のみつなげる
        if not cmds.isConnected(scr_attr, dst_attr):
            cmds.connectAttr(scr_attr, dst_attr, f=True)

    def __set_texture_and_channel(self, material, texture_path, channel):
        """テクスチャをfileノードにセットし、指定チャンネルと接続する

        Args:
            material (str): セットするマテリアル名
            texture_path (str): セットするテクスチャパス
            channel (str): 出力チャンネル
        """

        attr = 'outColor'

        if not cmds.objExists(material) or not self.__check_exists_attr(material, attr):
            return

        if texture_path is None or not os.path.isfile(texture_path):
            return

        this_file_node_list = list(set(cmds.listConnections(material, type='file') or []))
        if not this_file_node_list:
            return

        cmds.setAttr(
            '{}.{}'.format(this_file_node_list[0], 'fileTextureName'),
            texture_path,
            type='string')

        for c in ['R', 'G', 'B']:
            self.__connect_node_attr(this_file_node_list[0], attr + channel, material, attr + c)

    def __connect_node_attr(self, src_obj, src_attr, dst_obj, dst_attr):
        """アトリビュート同士を接続する
        それぞれのオブジェクト、アトリビュートの存在確認も同時に行っている

        Args:
            src_attr ([type]): [description]
            src_obj ([type]): [description]
            dst_attr ([type]): [description]
            dst_obj ([type]): [description]
        """

        if not cmds.objExists(src_obj) or not cmds.objExists(dst_obj):
            return

        src_full_attr = '{}.{}'.format(src_obj, src_attr)
        dst_full_attr = '{}.{}'.format(dst_obj, dst_attr)

        if not self.__check_exists_attr(src_obj, src_attr) or not self.__check_exists_attr(dst_obj, dst_attr):
            return

        if cmds.isConnected(src_full_attr, dst_full_attr):
            cmds.warning('already connected attr {}->{}'.format(src_full_attr, dst_full_attr))
            return

        try:
            cmds.connectAttr(src_full_attr, dst_full_attr, force=True)
        except Exception as e:
            cmds.warning(e)

    def __check_exists_attr(self, obj, attr):
        """対象のオブジェクトにAttributeが存在するか確認する

        Args:
            obj ([type]): アトリビュートの存在確認をするオブジェクト
            attr ([type]): 存在確認するアトリビュート
        """

        attr_list = cmds.listAttr(obj)

        if attr in attr_list:
            return True
        else:
            return False

    def __replace_material(self, src_material, dst_material, target_filter=''):
        """マテリアルを入れ替える

        Args:
            src_material ([type]): 入れ替え元のマテリアル
            dst_material ([type]): 入れ替え先のマテリアル
            target_filter (str, optional): 対象にするメッシュ名のフィルター. Defaults to ''.
        """

        if not cmds.objExists(src_material) or not cmds.objExists(dst_material):
            return

        cmds.hyperShade(objects=src_material)

        target_list = cmds.ls(sl=True, fl=True, l=True)
        if not target_list:
            return

        fix_target_list = []
        if not target_filter:
            fix_target_list = target_list
        else:
            for target in target_list:
                if target.find(target_filter) >= 0:
                    fix_target_list.append(target)

        if not fix_target_list:
            return

        cmds.select(fix_target_list, r=True)
        cmds.hyperShade(assign=dst_material)

        cmds.select(cl=True)

    def __change_outline_visible_state(self, visible):
        """全アウトラインメッシュの表示を切り替え

        Args:
            visible ([bool]): 表示状態
        """

        for outline in self.chara_info.part_info.outline_mesh_list:
            if cmds.objExists(outline):
                cmds.setAttr(outline + '.visibility', visible)

    def __set_texture_for_outline_dx11_material(self, outline_dx11_material, outline_mesh):
        """アウトラインDX11マテリアルのテクスチャを設定する

        Args:
            outline_dx11_material ([type]): テクスチャ設定するアウトライン用DX11マテリアル
            outline_mesh ([type]): アウトラインメッシュ(_Outline)
        """

        if not cmds.objExists(outline_dx11_material) or not cmds.objExists(outline_mesh):
            return

        # アウトラインのメッシュとマテリアル名から元メッシュのマテリアルを特定
        true_base_material = ''
        expected_base_mesh = outline_mesh.replace('_Outline', '')
        expected_base_material = outline_dx11_material.replace(define.DX11_OUTLINE_MATERIAL_SUFFIX, '')

        base_material_list = base_utility.material.get_material_list(expected_base_mesh)
        if not base_material_list:
            return

        for base_material in base_material_list:
            if base_material.find(expected_base_material) >= 0:
                true_base_material = base_material
                break

        if not true_base_material:
            return

        outline_dx11_default_attr_path_info_dict = define.OUTLINE_DX11_DEFAULT_ATTR_PATH_INFO_DICT.copy()

        # 元のマテリアルからテクスチャを取得
        if true_base_material.find(define.DX11_MATERIAL_SUFFIX) >= 0:
            diff_path = self.__get_texture_from_material_file_node(true_base_material, define.DIFF_TEX_ATTR)
            area_path = self.__get_texture_from_material_file_node(true_base_material, define.AREA_TEX_ATTR)
            outline_dx11_default_attr_path_info_dict[define.DIFF_TEX_ATTR] = [diff_path, define.WHITE_TEXTURE_PATH]
            outline_dx11_default_attr_path_info_dict[define.AREA_TEX_ATTR] = [area_path, define.GRAY_TEXTURE_PATH]

        else:
            diff_path = self.__get_texture_from_material_file_node(true_base_material, 'color')
            outline_dx11_default_attr_path_info_dict[define.DIFF_TEX_ATTR] = [diff_path, define.WHITE_TEXTURE_PATH]

        # 設定
        for attr, val in list(outline_dx11_default_attr_path_info_dict.items()):
            if val[0]:
                self.__apply_texture_to_material_assigned_file_node(outline_dx11_material, attr, val[0], val[1])
            else:
                self.__apply_texture_to_material_assigned_file_node(outline_dx11_material, attr, val[1])

    def __set_outline_dx11_material_value(self, dx11_material, data_type):
        """アウトラインDX11マテリアルの値を設定する

        Args:
            dx11_material ([type]): [description]
            data_type ([type]): [description]
        """

        outline_dx11_default_attr_dict = define.OUTLINE_DX11_DEFAULT_ATTR_DICT.copy()

        if data_type.find('mini') >= 0:
            outline_dx11_default_attr_dict['xOutlineWidth'] = 2.0

        # 値のセット
        for attr, val in list(outline_dx11_default_attr_dict.items()):

            if type(val) == list:
                cmds.setAttr('{}.{}'.format(dx11_material, attr), *val)
            else:
                cmds.setAttr('{}.{}'.format(dx11_material, attr), val)

    def __remove_dx11_material(self, is_outline=False):
        """dx11マテリアルの関連ノードやtmpファイルを完全に削除
        change_default_materialでマテリアルをdx11からはずしてから使用

        Args:
            is_outline (bool, optional): 削除対象のDX11がアウトライン用かどうか. Defaults to False.
        """

        target_dx11_material_suffix = define.DX11_MATERIAL_SUFFIX
        if is_outline:
            target_dx11_material_suffix = define.DX11_OUTLINE_MATERIAL_SUFFIX

        for dx11 in cmds.ls(type='dx11Shader'):

            if not dx11.endswith(target_dx11_material_suffix):
                continue

            # ファイルノードの削除
            attr_list = [
                define.DIFF_TEX_ATTR, define.BASE_TEX_ATTR, define.CTRL_TEX_ATTR, define.SHAD_TEX_ATTR,
                define.DIRT_TEX_ATTR, define.EMI_TEX_ATTR, define.DITHER_TEX_ATTR, define.ENV_TEX_ATTR,
                define.AREA_TEX_ATTR, define.RFL_TEX_ATTR,
            ]
            for attr in attr_list:
                self.__remove_file_node_connected_in_material(dx11, attr)

            if not is_outline:
                # マトリックスノードの削除
                self.__remove_matrix_nodes(dx11)

            # シェーディングエンジンの削除
            self.__remove_shading_engine_node_connected_in_material(dx11)

            # dx11マテリアル自身の削除
            cmds.delete(dx11)

        if is_outline:
            self.__remove_tmp_outline_dx11_dir()
        else:
            self.__remove_chara_light()
            self.__remove_tmp_dx11_dir()

    def __remove_map_material(self):
        """マップマテリアルの関連ノードを完全に削除

        """

        for material in cmds.ls(type='surfaceShader'):

            if not material.endswith(define.MAP_MATERIAL_SUFFIX):
                continue

            # ファイルノードの削除
            attr_list = ['outColorR', 'outColorG', 'outColorB']
            for attr in attr_list:
                self.__remove_file_node_connected_in_material(material, attr)

            # シェーディングエンジンの削除
            self.__remove_shading_engine_node_connected_in_material(material)

            # surfaceマテリアル自身の削除
            cmds.delete(material)

    def __remove_file_node_connected_in_material(self, material, attr):
        """マテリアルに接続されているfileノードを削除する
        DX11を削除しても残ってしまう為

        Args:
            material ([type]): 接続されているfileノードを削除したいマテリアル
            attr ([type]): マテリアルとfileノードが接続されているアトリビュート
        """

        if not cmds.objExists(material) or not self.__check_exists_attr(material, attr):
            return

        this_file_node_list = cmds.listConnections('{0}.{1}'.format(material, attr), type='file')
        if not this_file_node_list:
            return

        this_file_node = this_file_node_list[0]
        this_p2d_node_list = cmds.listConnections('{0}.{1}'.format(this_file_node, 'uvCoord'), type='place2dTexture')
        if this_p2d_node_list:
            cmds.delete(this_p2d_node_list[0])

        cmds.delete(this_file_node)

    def __remove_matrix_nodes(self, material):
        """マテリアルに接続されているmatrix_nodeを削除する

        Args:
            material ([type]): matrix_nodeが接続されているマテリアル
        """

        if not cmds.objExists(material):
            return

        if material not in self.toon_matrix_nodes_dict:
            return

        cmds.delete([x for x in self.toon_matrix_nodes_dict[material] if cmds.objExists(x)])
        self.toon_matrix_nodes_dict[material] = []

    def __remove_shading_engine_node_connected_in_material(self, material):
        """マテリアルに接続されているShadingEngineNodeを削除する
        DX11シェーダーを削除してしても残ってしまう為

        Args:
            material (string): 接続されているShadingEngineNodeを削除したいマテリアル
        """

        if not cmds.objExists(material):
            return

        this_shading_engine_list = cmds.listConnections('{0}.{1}'.format(material, 'outColor'), type='shadingEngine')
        if not this_shading_engine_list:
            return

        cmds.delete(this_shading_engine_list[0])

    def __adjust_outline_material_to_base_material(self):
        """アウトラインのマテリアルをベースメッシュに合わせる
        """

        for this_outline in self.chara_info.part_info.outline_mesh_list:

            material_list = base_utility.material.get_material_list(this_outline)
            if not material_list:
                continue

            base_mesh = this_outline.replace('_Outline', '')
            base_material_list = base_utility.material.get_material_list(base_mesh)
            if not base_material_list:
                continue

            for this_material in material_list:

                this_material_base = this_material.replace(define.DX11_OUTLINE_MATERIAL_SUFFIX, '')

                target_material = None

                for base_material in base_material_list:
                    if base_material.find(this_material_base) >= 0:
                        target_material = base_material
                        break
                else:
                    continue

                if this_material == target_material:
                    continue

                self.__replace_material(this_material, target_material)

    def __clamp_scale_value_in_01range(self, color_locater):
        """color_infoのscale値を0-1の範囲にクランプする

        spec_infoのscale値が0-1の範囲を外れていた場合
        set_value時だけではなく、connectAttrするときに不正な値だとエラーが発生する為
        """

        scale_attr_list = ['scaleX', 'scaleY', 'scaleZ']
        for scale_attr in scale_attr_list:

            if not self.__check_exists_attr(color_locater, scale_attr):
                continue

            locator_attr = '{}.{}'.format(color_locater, scale_attr)
            locator_attr_value = cmds.getAttr(locator_attr)

            if locator_attr_value < 0.0:
                locator_attr_value = 0.0
            elif locator_attr_value > 1.0:
                locator_attr_value = 1.0
            else:
                continue

            cmds.setAttr(locator_attr, locator_attr_value)

    def __search_spec_info_locator(self, dx11_material):
        """シーン内からspec_infoのロケーターを検索、取得

        Args:
            dx11_material ([type]): 検索するspec_infoのタイプを区別するためのDX11マテリアル名

        Returns:
            [type]: None or spec_info_locator名
        """

        if not self.chara_info.part_info.locator_list:
            return None

        target_locator_name = None
        if dx11_material.find('face') > -1:
            target_locator_name = 'Face_spec_info'
        elif dx11_material.find('hair') > -1:
            target_locator_name = 'Hair_spec_info'
        elif dx11_material.find('mtl_tail') > -1:
            target_locator_name = 'Tail_spec_info'
        elif dx11_material.find('mtl_bdy') > -1:
            target_locator_name = 'Body_spec_info'
            match_obj = re.match(r'mtl_bdy0001_[0-9]{2}(_[0-9])', dx11_material)
            if match_obj:
                target_locator_name = target_locator_name + match_obj.groups()[0]
        elif dx11_material.find('mtl_toon_prop') > -1:
            target_locator_name = 'ToonProp_spec_info'

        if target_locator_name:
            for locator in self.chara_info.part_info.locator_list:
                if locator.find(target_locator_name) > -1 and cmds.objExists(locator):
                    return locator

        return None

    def __fetch_chara_locators_with_suffix(self, target_suffix_list):
        """シーン内から特定の接尾語を持つchara_info登録ロケーターを検索、取得

        Args:
            target_suffix_list ([type]): 検索するロケーターの接尾語

        Returns:
            [type]: [] or color_info_locatorのリスト
        """

        if not self.chara_info.part_info.locator_list or not target_suffix_list:
            return []

        possible_loc_list = []

        for locator in self.chara_info.part_info.locator_list:
            for suffix in target_suffix_list:
                if locator.endswith(suffix):
                    possible_loc_list.append(locator)

        return [loc for loc in possible_loc_list if cmds.objExists(loc)]

    def __get_replaced_difference_texture_path_from_ui_param(self, texture_path, is_change_skin=True, is_change_bust=True):
        """UIから渡された肌色とバストの値に応じて置換したテクスチャパスを取得し返す

        Args:
            texture_path ([type]): 肌色とバストの値を置換するテクスチャパス名

        Returns:
            [type]: 置換されたテクスチャパス名
        """

        # mobはUIからリンクリストを更新しているのでパスを変更しない
        if self.chara_info.data_type.startswith('mob_'):
            return texture_path

        match_pattern = r'_([0-9])_([0-9])_'
        match_obj = re.search(match_pattern, texture_path)
        if match_obj:

            skin_num = match_obj.groups()[0]
            bust_num = match_obj.groups()[1]
            change_skin_num = self.ui_paramator.get('skin_num')
            change_bust_num = self.ui_paramator.get('bust_num')

            if change_skin_num is not None and is_change_skin:
                skin_num = change_skin_num
            if change_bust_num is not None and is_change_bust:
                bust_num = change_bust_num

            replace_str = '_{0}_{1}_'.format(skin_num, bust_num)
            tmp_texture_path = re.sub(match_pattern, replace_str, texture_path)
            for texture in self.chara_info.part_info.all_texture_list:
                if texture in tmp_texture_path:
                    texture_path = tmp_texture_path
                    break

        return texture_path

    def __connect_vertex_color_attr_to_dx11_material(self, dx11_material):
        """頂点カラーセットをDX11マテリアルに接続

        Args:
            dx11_material ([type]): 接続するDX11マテリアル
        """

        if not self.chara_info.part_info.mesh_list:
            return

        dx11_material_core_name = dx11_material.split(define.DIVIDE_FLAG)[0]

        mesh_type = None
        if dx11_material.find('face') > -1:
            mesh_type = 'M_Face'
        elif dx11_material.find('hair') > -1:
            mesh_type = 'M_Hair'
        elif dx11_material.find('mtl_bdy') > -1 or dx11_material.find('mtl_mbdy') > -1:
            mesh_type = 'M_Body'
        elif dx11_material.find('mtl_tail') > -1 or dx11_material.find('mtl_mtail') > -1:
            mesh_type = 'M_Tail'
        elif dx11_material.find('mtl_chr_prop') > -1:
            mesh_type = 'M_Prop'
        elif dx11_material.find('mtl_toon_prop') > -1:
            mesh_type = 'M_ToonProp'
        elif dx11_material.startswith('mtl_env_') and dx11_material_core_name.endswith('toon'):
            mesh_type = 'M_ToonProp'

        if mesh_type is None:
            return

        # 対象メッシュのカラーセット0があれば、それを適用する
        target_mesh = None
        target_mesh_list = self.chara_info.part_info.mesh_list

        # 対象がOutline用のMaterialであれば、mesh_listはそれ用のmeshリストに差し替え
        if dx11_material.find(define.DX11_OUTLINE_MATERIAL_SUFFIX) > -1:
            target_mesh_list = self.chara_info.part_info.outline_mesh_list

        for mesh in target_mesh_list:

            if mesh.find(mesh_type) > -1:
                target_mesh = mesh
                break

            m_mesh = cmds.ls(mesh, dag=True, type='mesh', long=True)
            shading_eng = cmds.listConnections(m_mesh, type='shadingEngine')
            material_list = cmds.ls(cmds.listConnections(shading_eng), materials=True)

            current_material_core_name = material_list[0].split(define.DIVIDE_FLAG)[0]
            if dx11_material_core_name == current_material_core_name:
                target_mesh = mesh
                break

        else:
            return

        target_color_set_list = base_utility.mesh.colorset.get_colorset_list(target_mesh)
        if not target_color_set_list:
            return

        shader_attr_list = cmds.listAttr(dx11_material)
        if 'Position_Source' in shader_attr_list:
            cmds.setAttr('{}.{}'.format(dx11_material, 'Position_Source'), 'position', type='string')
        if 'TexCoord0_Source' in shader_attr_list:
            cmds.setAttr('{}.{}'.format(dx11_material, 'TexCoord0_Source'), 'uv:map1', type='string')
        if 'Normal_Source' in shader_attr_list:
            cmds.setAttr('{}.{}'.format(dx11_material, 'Normal_Source'), 'normal', type='string')
        if 'Color0_Source' in shader_attr_list:
            cmds.setAttr('{}.{}'.format(dx11_material, 'Color0_Source'), '{}{}'.format('color:', target_color_set_list[0]), type='string')

    def __get_dx11_file(self, dx11_material, has_reflection=False):
        """複製元のDX11ファイルを取得する

        Args:
            dx11_material ([type]): 複製するDX11マテリアルマテリアルの名前

        Returns:
            [type]: 複製する.dx11ファイルの名前
        """

        if dx11_material.find('outline') >= 0:
            return os.path.join(define.DX11_DIR_PATH, 'CharacterOutline.fx')

        if self.chara_info.is_mini:
            return os.path.join(define.DX11_DIR_PATH, 'MiniCharaBody.fx')

        original_file_name = ''

        if dx11_material.find('face') >= 0 or dx11_material.find('brow') >= 0:
            original_file_name = 'CharacterToonFaceTSER.fx'
        elif dx11_material.find('eye') >= 0:
            original_file_name = 'CharacterToonEyeT.fx'
        elif dx11_material.find('hair') >= 0:
            if dx11_material.find('Alpha') > -1:
                if has_reflection:
                    original_file_name = 'CharacterAlphaNolineToonHairTSERRfl.fx'
                else:
                    original_file_name = 'CharacterAlphaNolineToonHairTSER.fx'
            else:
                if has_reflection:
                    original_file_name = 'CharacterToonHairTSERRfl.fx'
                else:
                    original_file_name = 'CharacterToonHairTSER.fx'
        else:
            if dx11_material.find('Alpha') > -1:
                if has_reflection:
                    original_file_name = 'CharacterAlphaNolineToonTSERRfl.fx'
                else:
                    original_file_name = 'CharacterAlphaNolineToonTSER.fx'
            else:
                if has_reflection:
                    original_file_name = 'CharacterToonTSERRfl.fx'
                else:
                    original_file_name = 'CharacterToonTSER.fx'

        org_dx11_file = os.path.join(define.DX11_DIR_PATH, original_file_name)

        if not os.path.exists(org_dx11_file) or not org_dx11_file:
            return ''
        else:
            return org_dx11_file

    def __get_assing_texture_info_list_from_chara_info(self, texture_type):
        """テクスチャタイプからマテリアルにアサインするテクスチャをキャラインフォから取得する

        texture_typeが「diff」(=通常テクスチャ)の場合はmaterial_link_listからdiffテクスチャパスを取得し
        「psd」の場合はmaterial_link_listからpsd_idと同じpsdのパスを取得

        Args:
            texture_type (str): 取得するテクスチャの種類(diff, shad_c, or psd)

        Returns:
            [type]: [description]
        """

        assign_texture_info_list = []

        for p in range(0, len(self.chara_info.part_info.material_param_list)):

            this_material = self.chara_info.part_info.material_param_list[p]['name']
            if not cmds.objExists(this_material):
                continue

            material_param = self.chara_info.part_info.material_param_list[p]
            material_link = self.chara_info.part_info.material_link_list[p]

            if texture_type == 'psd':

                psd_id = material_param.get('psd_id')
                if psd_id is None:
                    continue

                psd_texture_path = self.get_psd_texture_path_from_chara_info(psd_id)
                if psd_texture_path is None:
                    continue

                assign_texture_info_list.append({
                    'target_attr': 'color',
                    'target_material': this_material,
                    'target_texture_path': psd_texture_path
                })

            else:

                diff_texture_info = self.__get_texture_info_from_material_link(material_link, texture_type)
                if diff_texture_info is None:
                    continue

                assign_texture_info_list.append({
                    'target_attr': 'color',
                    'target_material': this_material,
                    'target_texture_path': diff_texture_info[2]
                })

        return assign_texture_info_list

    def get_psd_texture_path_from_chara_info(self, psd_id):
        """chara_infoのpsd_param_listからpsd_idに合致するpsdファイルを取得する

        Args:
            psd_id (string): chara_infoのpsd_param_listでの該当のマテリアルに対応するpsdのid

        Returns:
            psdのテクスチャパス
        """

        psd_texture_path = ''
        psd_param_list = self.chara_info.part_info.psd_param_list
        for psd_param in psd_param_list:

            psd_param_id = psd_param.get('id')
            psd_texture_name = psd_param.get('name')

            if psd_param_id is None or psd_texture_name is None:
                continue

            if psd_param_id != psd_id:
                continue

            psd_texture_path = os.path.join(
                self.chara_info.part_info.maya_sourceimages_dir_path,
                psd_texture_name
            )
            break

        # mini顔対応
        if not psd_texture_path and self.chara_info.is_use_alternative_info:

            psd_alternate_id = psd_param_list.get('alternate_id')
            if psd_alternate_id is None:
                return None

            for psd_param in self.chara_info.alternative_info.psd_param_list:

                if psd_alternate_id != psd_id:
                    continue

                psd_texture_name = psd_param['name']
                psd_texture_path = '{0}/{1}'.format(
                    self.chara_info.alternative_info.maya_sourceimages_dir_path,
                    psd_texture_name
                )
                break

        if not psd_texture_path:
            return None

        if not os.path.exists(psd_texture_path):
            return None

        return psd_texture_path

    def __revert_to_default_material(self):
        """アウトライン以外のメッシュのマテリアルを標準に戻す
        """

        mesh_list = self.chara_info.part_info.mesh_list

        for p in range(len(mesh_list)):

            this_mesh = mesh_list[p]

            material_list = base_utility.material.get_material_list(this_mesh)
            if not material_list:
                continue

            for q in range(len(material_list)):

                material = material_list[q]
                if material.find(define.DIVIDE_FLAG) <= 0:
                    continue

                # マテリアルと接続しているロケーターなどの値がはずれていることがあるので再設定
                self.__reapply_connection_param(material)

                original_material = material.split(define.DIVIDE_FLAG)[0]
                self.__replace_material(material, original_material)

    def __reapply_connection_param(self, target_material):
        """接続しているパラメーターを再設定
        シーンを開きなおした場合など接続先のパラメーターの値が外れることがあるので再設定する
        """

        if not cmds.objExists(target_material):
            return

        attrs = cmds.listAttr(target_material)

        for attr in attrs:

            if not cmds.attributeQuery(attr, node=target_material, ex=True):
                continue
            if not cmds.listConnections('{}.{}'.format(target_material, attr), d=True, s=False):
                continue
            if not cmds.attributeQuery(attr, node=target_material, internal=True):
                continue

            attr_type = cmds.attributeQuery(attr, node=target_material, attributeType=True)
            attr_value = cmds.getAttr('{}.{}'.format(target_material, attr))

            if attr_type in ['short', 'long', 'float', 'double', 'int32']:
                cmds.setAttr('{}.{}'.format(target_material, attr), attr_value)
            else:
                cmds.setAttr('{}.{}'.format(target_material, attr), attr_value, type=attr_type)

    def __remove_tmp_dx11_dir(self):
        """アサイン用に仮で生成しているDX11シェーダーのディレクトリを削除する
        """

        if os.path.exists(define.DX11_TMP_PATH):
            shutil.rmtree(define.DX11_TMP_PATH)

    def __remove_tmp_outline_dx11_dir(self):
        """アサイン用に仮で生成しているアウトライン用のDX11シェーダーのディレクトリを削除する
        """

        if os.path.exists(define.DX11_OUTLINE_TMP_PATH):
            shutil.rmtree(define.DX11_OUTLINE_TMP_PATH)

    def __create_material_state(self, material):
        """マテリアルの状態を表す辞書を作成

        Returns:
            dict[str, str]: マテリアルの状態を表す辞書
        """

        material_state = {
            'shader': 'default',
            'texture': 'diff',
            'channel': 'R'
        }

        if define.DIVIDE_FLAG not in material:
            texture = 'diff'

            texture_path = self.__get_texture_from_material_file_node(material, 'color')
            if os.path.splitext(texture_path)[1] == '.psd':
                texture = 'psd'
            elif 'shad_c' in os.path.basename(texture_path):
                texture = 'shad_c'

            material_state.update({'texture': texture})

        else:
            shader = material.split(define.DIVIDE_FLAG)[1]

            if shader == 'dx11':
                material_state.update({'shader': shader})

            elif shader == 'map':
                material_state.update({'shader': shader})

                texture = 'base'
                texture_path = self.__get_texture_from_material_file_node(material, 'outColorR')
                if 'ctrl' in os.path.basename(texture_path):
                    texture = 'ctrl'
                material_state.update({'texture': texture})

                attributes = cmds.listConnections('{0}.{1}'.format(material, 'outColorR'), s=True, d=False, p=True, t='file')
                for attribute in attributes or []:
                    match = re.search(r'outColor([RGB])', attribute)
                    if match:
                        material_state.update({'channel': match.group(1)})
                        break

        return material_state
