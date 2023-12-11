# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import os

import maya.cmds as cmds
import maya.mel as mel

from . import view
from . import turtle_utility
from . import tool_utility
from . import bake
from . import bake_setting
from . import preview
from . import tool_define

reload(view)
reload(turtle_utility)
reload(tool_utility)
reload(bake)
reload(bake_setting)
reload(preview)
reload(tool_define)


class LightMapMaker(object):

    def __init__(self):
        """コンストラクタ
        """
        pass

    def initialize(self):
        """ライトマップツールの初期化
        タートルのロードと初期化
        """
        turtle_utility.load_turtle()
        turtle_utility.switch_turtle_renderer()

    def import_bake_layers(self):
        """シーン内にあるツールで使用するベイクレイヤーの読み込み

        Returns:
            list: ツールで使用するベイクレイヤーのリスト
        """

        bake_layer_list = cmds.ls('{}*'.format(tool_define.BAKE_LAYER_PREFIX), type='ilrBakeLayer')

        result_list = []

        if not bake_layer_list:
            return result_list

        for bake_layer in bake_layer_list:

            # 追加アトリビュートの付与
            bake_setting.add_extra_attr(bake_layer)

            # カスタムシェーダーのセットを確認
            bake_setting.set_custom_shader(bake_layer)

            # 出力先を設定
            bake_dir_path = bake_setting.get_bake_texture_dir(bake_layer)

            if not bake_dir_path:
                # パスが指定されていなければデフォルトパスを設定
                default_dir_path = tool_utility.generate_bake_texture_dir_path()
                bake_setting.set_bake_texture_dir(bake_layer, default_dir_path)

            if not os.path.exists(bake_dir_path.replace(tool_define.TEX_OUTPUT_PATH, '')):
                # ルートのパスが存在しない場合（=他の人のローカルパスが指定されているなど）デフォルトパスを設定
                default_dir_path = tool_utility.generate_bake_texture_dir_path()
                bake_setting.set_bake_texture_dir(bake_layer, default_dir_path)

            bake_tex_name = bake_setting.get_bake_texture_name(bake_layer)

            if not bake_tex_name:
                default_bake_texture_name = tool_utility.generate_default_bake_texture_name(bake_layer)
                bake_setting.set_bake_texture_name(bake_layer, default_bake_texture_name)

            result_list.append(bake_layer)

        return result_list

    def create_new_bake_layer(self, base_name):
        """ベイクレイヤーの新規作成
        作成されるレイヤー名は (tool_define.BAKE_LAYER_PREFIX) + (base_name)

        Args:
            base_name (str): ユーザー定義のベイクレイヤー名
        Returns:
            str: 作成されたベイクレイヤー名
        """

        name = tool_define.BAKE_LAYER_PREFIX + base_name

        if not cmds.objExists(name):
            turtle_utility.create_turtle_bake_layer(name)
            bake_setting.init_bake_layer(name)
            bake_setting.set_custom_shader(name)
            bake_setting.set_bake_color_set(name)

            default_dir_path = tool_utility.generate_bake_texture_dir_path()
            bake_setting.set_bake_texture_dir(name, default_dir_path)

            default_bake_texture_name = tool_utility.generate_default_bake_texture_name(name)
            bake_setting.set_bake_texture_name(name, default_bake_texture_name)

            return name
        else:
            cmds.warning('already exists')
            return ''

    def delete_bake_layers(self, bake_layer_list):
        """ベイクレイヤーの削除

        Args:
            bake_layer_list (list): 削除するベイクレイヤーのリスト
        """

        for bake_layer in bake_layer_list:
            if cmds.objExists(bake_layer):
                turtle_utility.delete_turtle_bake_layer(bake_layer)

    def add_bake_target(self, bake_layer, target_list):
        """ベイクレイヤーにベイク対象を追加する

        Args:
            bake_layer (str): 対象を追加するベイクレイヤー
            target_list (list): 追加するベイク対象(shape)のリスト
        """

        if not cmds.objExists(bake_layer):
            return

        add_target_list = [x for x in target_list if cmds.objExists(x)]

        if add_target_list:
            turtle_utility.add_target_surface(add_target_list, bake_layer)

    def delete_bake_target(self, bake_layer, target_list):
        """ベイクレイヤーからベイク対象を削除する

        Args:
            bake_layer (str): 対象を削除するベイクレイヤー
            target_list (list): 削除するベイク対象(shape)のリスト
        """

        if not cmds.objExists(bake_layer):
            return

        del_target_list = [x for x in target_list if cmds.objExists(x)]

        if del_target_list:
            turtle_utility.delete_target_surface(del_target_list, bake_layer)

    def apply_bake_layer(self, bake_layer):
        """TURTLEのベイクで用いるベイクレイヤーを設定する
        RenderSetting > TURTLE > Baking > BakeLayer で確認出来る

        Args:
            bake_layer (str): 設定するベイクレイヤー
        """

        if cmds.objExists(bake_layer):
            turtle_utility.set_turtle_bake_layer(bake_layer)

    def set_light_set(self, bake_layer, light_set):
        """ライトセットの指定

        Args:
            bake_layer (str): ライトセットを指定するベイクレイヤー
            light_set (str): ライトセット
        """

        if not cmds.objExists(bake_layer):
            return

        bake_setting.set_light_set(bake_layer, light_set)

    def rename_bake_layer(self, bake_layer, new_name):
        """ベイクレイヤーのリネーム

        Args:
            bake_layer (str): 操作するベイクレイヤー
            new_name (str): 新しいベイクレイヤーのベースネーム

        Returns:
            str: リネーム後のベイクレイヤー名
        """

        if cmds.objExists(new_name):
            cmds.warning('already exists: {}'.format(new_name))
            return bake_layer

        # ベイクレイヤーのリネーム
        result_name = cmds.rename(bake_layer, new_name)

        relative_node_list = tool_utility.fetch_bake_layer_relative_node_list(bake_layer)

        # ベイクレイヤーと関連するノードのリネーム
        for node in relative_node_list:
            src = tool_utility.slice_bake_layer_suffix(bake_layer)
            dst = tool_utility.slice_bake_layer_suffix(result_name)
            new_name = node.replace(src, dst)
            cmds.rename(node, new_name)

        # 旧ベイクレイヤー名を持つカラーセットをリネーム
        shape_list = cmds.sets(result_name, q=True)

        if shape_list:
            for shape in shape_list:

                exist_colorset_list = cmds.polyColorSet(shape, q=True, acs=True)

                if not exist_colorset_list:
                    continue

                for colorset in exist_colorset_list:
                    if colorset.find(bake_layer) < 0:
                        continue
                    new_name = colorset.replace(bake_layer, result_name)
                    if new_name not in exist_colorset_list:
                        cmds.polyColorSet(shape, cs=colorset, nc=new_name, rn=True)

        # ベイクレイヤーの再構築
        mel.eval('ilrRebuildBakeLayerSystem;')

        return result_name

    def set_bake_type(self, bake_layer_list, bake_type_num):
        """ベイクタイプの指定

        Args:
            bake_layer_list (list): ベイクタイプを指定するベイクレイヤーのリスト
            bake_type_num (int): ベイクタイプ（1=BakeToTexture, 2=BakeToVertices）
        """

        if bake_type_num != 1 and bake_type_num != 2:
            return

        for bake_layer in bake_layer_list:
            if cmds.objExists(bake_layer):

                current_bake_type = bake_setting.get_bake_type(bake_layer)

                # 変更する場合はプレビューを切る
                if current_bake_type != bake_type_num:
                    preview.show_default(bake_layer)
                    bake_setting.set_bake_type(bake_layer, bake_type_num)

    def bake_by_bake_layer(self, bake_layer_list, use_legacy_method=True, use_gi=False, is_test=False, progress_ui=None):
        """ベイクレイヤーの設定を使用してベイク実行

        Args:
            bake_layer_list (list): ベイクを実行するベイクレイヤーのリスト
            use_legacy_method (bool, optional): 旧ツールの合成方法を使うか. Defaults to True.
            use_gi (bool, optional): ベイク時にGIを計算するか. Defaults to False.
            is_test (bool, optional): テストベイクか. Defaults to False.
            progress_ui (str, optional): cmds.progressBar作成されるコントロール名. Defaults to None.
        """

        for bake_layer in bake_layer_list:

            if not cmds.objExists(bake_layer):
                if progress_ui:
                    cmds.warning(u'ベイクレイヤーが存在していません')
                    cmds.progressBar(progress_ui, e=True, step=1)
                continue

            if bake_setting.get_bake_type(bake_layer) == 1 and not bake_setting.get_texture_bake_uv(bake_layer):
                if progress_ui:
                    cmds.warning(u'ベイク先のUVセットが指定されていないためスキップします')
                    cmds.progressBar(progress_ui, e=True, step=1)
                continue

            # 二度掛けになってしまうのでプレビューを解除しておく
            preview.show_default(bake_layer)

            bake.bake_lightmap(bake_layer, use_legacy_method, use_gi, is_test)

            if progress_ui:
                cmds.progressBar(progress_ui, e=True, step=1)

    def set_texture_bake_uv(self, bake_layer_list, uv_set):
        """ベイクレイヤーにテクスチャベイクするUVセット名を設定

        Args:
            bake_layer_list (list): セットするベイクレイヤーのリスト
            uv_set (str): セットするUVセット名
        """

        for bake_layer in bake_layer_list:
            if cmds.objExists(bake_layer):
                bake_setting.set_texture_bake_uv(bake_layer, uv_set)

    def set_texture_bake_res(self, bake_layer_list, res_x, res_y):
        """ベイクするテクスチャの解像度を設定

        Args:
            bake_layer_list (list): セットするベイクレイヤーのリスト
            res_x (int): 幅
            res_y (int): 高さ
        """

        for bake_layer in bake_layer_list:
            if cmds.objExists(bake_layer):
                bake_setting.set_texture_bake_res(bake_layer, res_x, res_y)

    def set_texture_bake_test_res(self, bake_layer_list, test_res_x, test_res_y):
        """ベイクするテクスチャの解像度を設定

        Args:
            bake_layer_list (list): セットするベイクレイヤーのリスト
            res_x (int): 幅
            res_y (int): 高さ
        """

        for bake_layer in bake_layer_list:
            if cmds.objExists(bake_layer):
                bake_setting.set_texture_bake_test_res(bake_layer, test_res_x, test_res_y)

    def get_texture_name(self, bake_layer):
        """出力テクスチャ名を取得

        Args:
            bake_layer (str): 対象のベイクレイヤー

        Returns:
            str: 取得したテクスチャ名
        """

        if not cmds.objExists(bake_layer):
            return ''

        bake_tex_name = bake_setting.get_bake_texture_name(bake_layer)
        return tool_utility.slice_base_texture_name(bake_tex_name)

    def set_texture_name(self, bake_layer, base_tex_name):
        """出力テクスチャ名を設定

        Args:
            bake_layer (str): 設定するベイクレイヤー
            base_tex_name (str): 設定するテクスチャ名
        """

        if not cmds.objExists(bake_layer):
            return

        # bake用にturtleの置き換え文字を付与
        bake_tex_name = tool_utility.generate_bake_texture_name(base_tex_name)
        bake_setting.set_bake_texture_name(bake_layer, bake_tex_name)

    def create_uv_set(self, bake_layer_list, uv_set_name):
        """ベイクレイヤーに登録されているシェイプにUVセットを追加

        Args:
            bake_layer_list (list): UVセットを追加するベイクレイヤーのリスト
            uv_set_name (str): 追加するUVセット名
        """

        target_shape_list = []

        for bake_layer in bake_layer_list:
            this_shape_list = cmds.sets(bake_layer, q=True)
            if this_shape_list:
                target_shape_list.extend(this_shape_list)

        for shape in target_shape_list:
            tool_utility.create_uv_set(shape, uv_set_name)

    def projection_uv(self, bake_layer_list, uv_set_name):
        """ベイクレイヤーに登録されているシェイプのUVを再展開

        Args:
            bake_layer_list (list): UVを再展開するベイクレイヤーのリスト
            uv_set_name (str): 再展開するUVセット名
        """

        target_shape_list = []

        for bake_layer in bake_layer_list:
            this_shape_list = cmds.sets(bake_layer, q=True)
            if this_shape_list:
                target_shape_list.extend(this_shape_list)

        for shape in target_shape_list:
            tool_utility.projection_uv(shape, uv_set_name)

    def layout_uvs(self, bake_layer_list, uv_set_name):
        """ベイクレイヤーに登録されているシェイプのUVを再展開

        Args:
            bake_layer_list (list): UVを再展開するベイクレイヤーのリスト
            uv_set_name (str): 再展開するUVセット名
        """

        target_shape_list = []

        for bake_layer in bake_layer_list:
            this_shape_list = cmds.sets(bake_layer, q=True)
            if this_shape_list:
                target_shape_list.extend(this_shape_list)

        if target_shape_list:
            tool_utility.layout_uvs(target_shape_list, uv_set_name)

    def set_ray_min_max_value(self, bake_layer_list, min_max):
        """AOのサンプルレイのmin/maxを設定

        Args:
            bake_layer_list (list): ベイクレイヤー
            value (list): [MinSampleRays, MaxSampleRays]
        """

        for bake_layer in bake_layer_list:
            if cmds.objExists(bake_layer):
                bake_setting.set_ray_min_max_value(bake_layer, min_max)

    def set_test_ray_min_max_value(self, bake_layer_list, test_min_max):
        """AOのサンプルレイのテストmin/maxを設定

        Args:
            bake_layer_list (list): ベイクレイヤー
            value (list): [MinSampleRays, MaxSampleRays]
        """

        for bake_layer in bake_layer_list:
            if cmds.objExists(bake_layer):
                bake_setting.set_test_ray_min_max_value(bake_layer, test_min_max)
