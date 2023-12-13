# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import os

import maya.cmds as cmds

from . import tool_define

reload(tool_define)


def create_uv_set(shape, uv_set_name):
    """UVセットを作成

    Args:
        shape (str): UVセットを追加するシェイプ
        uv_set_name (str): 追加するUVセット名
    """

    uvset_list = cmds.polyUVSet(shape, q=True, allUVSets=True)

    if uv_set_name in uvset_list:
        cmds.warning(u'{} には既に {} が存在するためUVセット作成をスキップ'.format(shape, uv_set_name))
        return

    cmds.polyUVSet(shape, uvSet=uv_set_name, create=True)


def projection_uv(shape, uv_set):
    """UVを展開

    Args:
        shape (str): UVを展開するシェイプ
        uv_set (str): 展開するUVセット名
    """

    uvset_list = cmds.polyUVSet(shape, q=True, allUVSets=True)

    if uv_set not in uvset_list:
        return

    cmds.polyUVSet(shape, currentUVSet=True, uvSet=uv_set)
    cmds.polyAutoProjection(
        shape,
        layoutMethod=1,  # シェイプ スタッキング
        layout=2,  # UV ピースは正方シェイプに移動されます
    )


def layout_uvs(shape_list, uv_set):
    """UVを自動配置

    Args:
        shape_list (str): UVを自動配置するシェイプのリスト
        uv_set (str): 配置するUVセット名
    """

    target_list = []

    for shape in shape_list:
        uvset_list = cmds.polyUVSet(shape, q=True, allUVSets=True)
        if uv_set in uvset_list:
            cmds.polyUVSet(shape, currentUVSet=True, uvSet=uv_set)
            target_list.append(shape)

    cmds.polyMultiLayoutUV(
        target_list,
        flipReversed=True,
        scale=1,  # 単位正方形に合わせて均一にスケール
        rotateForBestFit=1,  # 90°回転のみ可能
        layoutMethod=1,  # シェイプ スタッキング
        prescale=2,  # ワールド空間のスケールが適用
        layout=2,  # ピースを四角形にレイアウト
        percentageSpace=0.4
    )


def create_material(material_name):
    """新規ランバートマテリアルの作成

    Args:
        material_name (str): 作成するマテリアル名

    Returns:
        str: 作成されたマテリアル名
    """

    if cmds.objExists(material_name):
        return ''

    shading_engine_name = material_name + 'SG'

    shading_node = cmds.shadingNode('lambert', asShader=True, name=material_name)
    cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shading_engine_name)
    cmds.connectAttr('{}.{}'.format(shading_node, 'outColor'), '{}.{}'.format(shading_engine_name, 'surfaceShader'))

    return material_name


def get_material_list(shape_list):
    """シェイプからマテリアルを取得

    Args:
        shape_list (list): 検索するシェイプのリスト

    Returns:
        list: 割り当てられているマテリアルのリスト
    """

    shading_engine_list = []

    for shape in shape_list:

        shading_engines = cmds.listConnections(shape, type='shadingEngine')

        if not shading_engines:
            continue

        for shading_engine in shading_engines:
            if shading_engine not in shading_engine_list:
                shading_engine_list.append(shading_engine)

    material_list = []

    for shading_engine in shading_engine_list:

        materials = cmds.listConnections(shading_engine + '.surfaceShader')

        if not materials:
            continue

        for material in materials:
            if material not in material_list:
                material_list.append(material)

    return material_list


def get_shading_group(target_material):
    """マテリアルからシェーディンググループを取得

    Args:
        target_material (str): 対象マテリアル

    Returns:
        str: シェーディンググループ
    """

    if not cmds.objExists(target_material):
        return ''

    shading_group_list = cmds.listConnections(target_material, t='shadingEngine')

    if not shading_group_list:
        return ''

    if len(shading_group_list) > 1 and shading_group_list[0] == 'initialParticleSE':
        return shading_group_list[1]  # lambert1の場合
    else:
        return shading_group_list[0]


def get_material_member(target_material, target_transform=''):
    """マテリアルに登録されているシェイプや面を取得

    Args:
        target_material (str): マテリアル
        target_transform (str): シェイプや面を取得したいトランスフォーム

    Returns:
        list: シェイプや面のリスト
    """

    sg = get_shading_group(target_material)

    if not sg:
        return []

    all_members = cmds.ls(cmds.sets(sg, q=True), l=True, fl=True)

    target_transform_fullpath = ''
    if not target_transform:
        return all_members
    elif not cmds.objExists(target_transform):
        return []
    else:
        target_transform_fullpath = cmds.ls(target_transform, l=True)[0]

    shape = ''
    shapes = cmds.listRelatives(target_transform_fullpath, s=True, f=True)
    if shapes:
        shape = shapes[0]

    shape_members = []
    for member in all_members:
        # memberはshapeかtransform.f[*]なので、下記の操作でshapeかtransformのフルパスになるはず
        elm_long_name = member.split('.f')[0]

        if elm_long_name == target_transform_fullpath or elm_long_name == shape:
            shape_members.append(member)

    return shape_members


def create_file_node(texture_path, node_name=None):
    """テクスチャファイルノードを作成する

    Args:
        texture_path (str): テクスチャのパス
        node_name (str): ノード名

    Returns:
        list: 作成されるノードのリスト[ファイルノード, place2dTextureノード, uvChooserノード]
    """

    file_node = ''
    if node_name:
        file_node = cmds.shadingNode('file', asTexture=True, isColorManaged=True, n=node_name)
    else:
        file_node = cmds.shadingNode('file', asTexture=True, isColorManaged=True)

    p2t_node = cmds.shadingNode('place2dTexture', asUtility=True)
    uv_chooser_node = cmds.shadingNode('uvChooser', asUtility=True)

    if os.path.exists(texture_path):
        cmds.setAttr('{}.{}'.format(file_node, 'fileTextureName'), texture_path, type='string')
    else:
        cmds.warning(u'{} が存在していません'.format(texture_path))

    cmds.defaultNavigation(connectToExisting=True, source=p2t_node, destination=file_node)
    cmds.connectAttr('{}.{}'.format(uv_chooser_node, 'outVertexCameraOne'), '{}.{}'.format(p2t_node, 'vertexCameraOne'))
    cmds.connectAttr('{}.{}'.format(uv_chooser_node, 'outVertexUvThree'), '{}.{}'.format(p2t_node, 'vertexUvThree'))
    cmds.connectAttr('{}.{}'.format(uv_chooser_node, 'outVertexUvTwo'), '{}.{}'.format(p2t_node, 'vertexUvTwo'))
    cmds.connectAttr('{}.{}'.format(uv_chooser_node, 'outVertexUvOne'), '{}.{}'.format(p2t_node, 'vertexUvOne'))
    cmds.connectAttr('{}.{}'.format(uv_chooser_node, 'outUv'), '{}.{}'.format(p2t_node, 'uvCoord'))

    return [file_node, p2t_node, uv_chooser_node]


def create_colorset(target, new_colorset_name, default_color=[1, 1, 1, 1]):
    """カラーセットを新規作成
    既存の場合はスキップ
    """

    exist_colorset_list = cmds.polyColorSet(target, q=True, acs=True)

    if exist_colorset_list and new_colorset_name in exist_colorset_list:
        return new_colorset_name

    new_colorset_name = cmds.polyColorSet(target, colorSet=new_colorset_name, cr=True, rpt="RGBA")[0]
    cmds.polyColorSet(target, colorSet=new_colorset_name, currentColorSet=True)
    cmds.polyColorPerVertex(target, r=default_color[0], g=default_color[1], b=default_color[2], a=default_color[3], cdo=True)

    return new_colorset_name


def change_colorset(shape, color_set):
    """カラーセットを変更

    Args:
        shape (str): カラーセットを変更したいシェイプ
        color_set (str): 変更したいカラーセット名

    Returns:
        bool: 変更できたか
    """

    exist_colorset_list = cmds.polyColorSet(shape, q=True, acs=True)

    if not exist_colorset_list or color_set not in exist_colorset_list:
        cmds.warning(u'カラーセットが存在していません: {}({})'.format(color_set, shape))
        return False

    cmds.polyColorSet(shape, colorSet=color_set, currentColorSet=True)
    return True


def fetch_bake_layer_relative_node_list(bake_layer):
    """ベイクレイヤーに関連してツールが作成したノードのリストを取得
    ベイクレイヤーに関連した命名で作成されているので、命名から検索

    Args:
        bake_layer (str): 検索元となるベイクレイヤー

    Returns:
        list: 関連するノードのリスト
    """

    target_str_list = [bake_layer, generate_material_suffix(bake_layer)]
    result_list = []

    for target_str in target_str_list:

        hit_list = cmds.ls('*{}*'.format(target_str))

        if not hit_list:
            continue

        for hit in hit_list:

            # bake_layer自身は除外
            if cmds.objectType(hit) == 'ilrBakeLayer':
                continue
            if hit not in result_list:
                result_list.append(hit)

    return result_list


def slice_bake_layer_suffix(bake_layer_name):
    """ベイクレイヤーのサフィックス（ユーザー指定部分）を取得する

    Args:
        bake_layer_name (str): サフィックスを取得したいベイクレイヤー

    Returns:
        str: サフィックス（ユーザー指定部分）
    """
    return bake_layer_name.replace(tool_define.BAKE_LAYER_PREFIX, '')


def generate_material_suffix(bake_layer_name):
    """テクスチャベイク表示用のマテリアルのサフィックスを取得

    Args:
        bake_layer_name (str): サフィックスを取得したいベイクレイヤー

    Returns:
        str: サフィックス
    """
    return tool_define.PREVIEW_MATERIAL_SUFFIX + slice_bake_layer_suffix(bake_layer_name)


def generate_bake_material_name(bake_layer_name, org_mtr_name):
    """テクスチャベイク表示用のマテリアル名を取得

    Args:
        bake_layer_name (str): このマテリアルを仕様するベイクレイヤー
        org_mtr_name (str): 元々割り当てられていたマテリアル名

    Returns:
        str: テクスチャベイク表示用のマテリアル名
    """

    # ツールがつけたサフィックスがついていたら取り除く
    base_mtr_name = slice_base_material_name(org_mtr_name)
    return base_mtr_name + generate_material_suffix(bake_layer_name)


def slice_base_material_name(preview_mtr_name):
    """元になっているマテリアル名の取得

    Args:
        preview_mtr_name (str): テクスチャベイク表示用のマテリアル名

    Returns:
        str: 元になっているマテリアル名
    """
    return preview_mtr_name.split(tool_define.PREVIEW_MATERIAL_SUFFIX)[0]


def generate_bake_colorset_name(bake_layer_name):
    """頂点ベイク表示用のカラーセット名の取得

    Args:
        bake_layer_name (str): カラーセットを表示するベイクレイヤー

    Returns:
        str: 頂点ベイク表示用のカラーセット名
    """
    return bake_layer_name + tool_define.RESULT_COLORSET_SUFFIX


def generate_bake_texture_dir_path():
    """テクスチャ出力用のパスを作成
    sourceimages内のbakeを指定する

    Returns:
        str: テクスチャ出力用パス
    """

    dir_path = ''
    ma_path = cmds.file(q=True, sn=True)

    if ma_path:
        dir_path = os.path.dirname(os.path.dirname(ma_path)) + tool_define.TEX_OUTPUT_PATH

    return dir_path


def generate_bake_texture_name(bake_layer_name):
    """ベイク用のテクスチャ名の作成
    ベースネーム + turtleが使用する置き換え用の文字列

    Args:
        bake_layer_name (str): ベースとなるテクスチャ名

    Returns:
        str: ベイクレイヤーに設定するテクスチャ名
    """

    return '{}{}.{}'.format(bake_layer_name, tool_define.BAKE_ELM_STR, tool_define.BAKE_EXT_STR)


def generate_default_bake_texture_name(bake_layer_name):
    """デフォルトのベイク用テクスチャ名の作成
    シーン名 + _ベイクレイヤーサフィックス + turtleが使用する置き換え用の文字列

    Args:
        bake_layer (str): ベイクするベイクレイヤー

    Returns:
        str: ベイクレイヤーに設定するテクスチャ名
    """

    scene_path = cmds.file(q=True, sn=True)
    base_name = ''

    if scene_path:
        base_name = os.path.splitext(os.path.basename(scene_path))[0].replace(tool_define.MODEL_PREFIX, tool_define.TEX_PREFIX)
        if not base_name.startswith(tool_define.TEX_PREFIX):
            base_name = tool_define.TEX_PREFIX + base_name
    else:
        base_name = tool_define.TEX_PREFIX + bake_layer_name

    return generate_bake_texture_name('{}_{}'.format(base_name, slice_bake_layer_suffix(bake_layer_name)))


def slice_base_texture_name(bake_tex_name):
    """ベイク用のテクスチャ名から置き換え文字を除いたベース部分を取得

    Args:
        bake_tex_name (str): ベイクレイヤーに設定する置き換え文字を含むテクスチャ名

    Returns:
        str: 置き換え文字を除いたベース部分
    """

    base_name = bake_tex_name.replace('.{}'.format(tool_define.BAKE_EXT_STR), '')
    base_name = base_name.replace(tool_define.BAKE_ELM_STR, '')

    return base_name


def generate_conbine_texture_name(bake_layer):
    """ベイク結果を合成した（最終的に使用する）テクスチャ名を作成

    Args:
        bake_layer (str): ベイクするベイクレイヤー

    Returns:
        _type_: ベイク結果を合成したテクスチャ名
    """

    raw_tex_name = cmds.getAttr('{}.tbFileName'.format(bake_layer))
    conbine_tex_name = raw_tex_name.replace(tool_define.BAKE_EXT_STR, 'tga')
    conbine_tex_name = conbine_tex_name.replace(tool_define.BAKE_ELM_STR, '')

    return conbine_tex_name
