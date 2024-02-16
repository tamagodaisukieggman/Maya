# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
    from builtins import str
    from importlib import reload
except Exception:
    pass

import os
import re
import time

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om

from . import turtle_utility
from . import tool_utility
from . import bake_setting
from . import tool_define

reload(turtle_utility)
reload(tool_utility)
reload(bake_setting)
reload(tool_define)


def bake_lightmap(bake_layer, use_legacy_method=True, use_gi=False, is_test=False):
    """ライトマップをベイクする

    Args:
        bake_layer (str): _description_
        use_legacy_method (bool, optional): 旧ツールの合成方法を使うか. Defaults to True.
        use_gi (bool, optional): ベイク時にGIを計算するか. Defaults to False.
        is_test (bool, optional): テストベイクか. Defaults to False.
    """

    if not cmds.objExists(bake_layer):
        return

    if not cmds.sets(bake_layer, q=True):
        return

    # 受けるライトを切り替えるため全ライトを取得しておく
    all_light_shape_list = cmds.ls(type='light')
    all_light_list = []

    for shape in all_light_shape_list:
        transform_list = cmds.listRelatives(shape, parent=True, type='transform', f=True)
        if transform_list:
            all_light_list.append(transform_list[0])

    # オリジナルのライトのvisibilityを取得
    org_light_visible_list = []

    for light in all_light_list:
        org_light_visible_list.append(cmds.getAttr(light + '.visibility'))

    # ベイクで使用するライト以外は非表示にする
    # 元々ライトの表示を触っている可能性があるのでベイク使用ライトはオンにするのではなく触らない
    bake_light_set = bake_setting.get_light_set(bake_layer)
    if not bake_light_set:
        bake_light_set = 'defaultLightSet'

    bake_light_list = cmds.ls(cmds.sets(bake_light_set, q=True), l=True)

    for light in all_light_list:
        cmds.setAttr(light + '.visibility', l=False)
        if light not in bake_light_list:
            cmds.setAttr(light + '.visibility', False)

    # オリジナルの解像度を保存
    org_tex_w_h = bake_setting.get_texture_bake_res(bake_layer)

    # オリジナルのサンプリング数を保存
    org_ray_min_max = bake_setting.get_ray_min_max_value(bake_layer)

    # テストが指定されていたら、テスト値を設定
    if is_test:
        test_res_x_y = bake_setting.get_texture_bake_test_res(bake_layer)
        bake_setting.set_texture_bake_res(bake_layer, test_res_x_y[0], test_res_x_y[1])

        test_ray_min_max = bake_setting.get_test_ray_min_max_value(bake_layer)
        bake_setting.set_ray_min_max_value(bake_layer, test_ray_min_max)

    # TURTLEの設定
    turtle_utility.load_turtle()
    turtle_utility.switch_turtle_renderer()
    turtle_utility.set_turtle_bake_layer(bake_layer)
    turtle_utility.set_gi_enable(use_gi)

    # BakeTypeに応じてベイク実行
    if cmds.getAttr('{}.renderType'.format(bake_layer)) == 1:  # BakeToTexture
        bake_lightmap_to_textures(bake_layer, use_gi, use_legacy_method)
    elif cmds.getAttr('{}.renderType'.format(bake_layer)) == 2:  # BakeToVertices
        bake_lightmap_to_vertices(bake_layer, use_gi, use_legacy_method)

    # オリジナルのライトの表示状態を戻す
    for light, visible in zip(all_light_list, org_light_visible_list):
        cmds.setAttr(light + '.visibility', l=False)
        cmds.setAttr(light + '.visibility', visible)

    # オリジナルの解像度を戻す
    bake_setting.set_texture_bake_res(bake_layer, org_tex_w_h[0], org_tex_w_h[1])

    # オリジナルのサンプリング数を戻す
    bake_setting.set_ray_min_max_value(bake_layer, org_ray_min_max)


def bake_lightmap_to_textures(bake_layer, use_gi, use_legacy_method=True):
    """テクスチャへライトマップをベイクする

    Args:
        bake_layer (str): ベイクするベイクレイヤー
        use_gi (bool): ベイク時にGIを計算するか
        use_legacy_method (bool, optional): 旧ツールの合成方法を使うか. Defaults to True.
    """

    # 必須な要素のベイクフラグを建てる
    bake_setting.set_must_bake_part(bake_layer, use_gi)

    bake_tex_dir = bake_setting.get_bake_texture_dir(bake_layer)
    bake_tex_name = bake_setting.get_bake_texture_name(bake_layer)

    if not os.path.exists(bake_tex_dir):
        os.makedirs(bake_tex_dir)

    # こちらも最終結果合成用のカラーセット作成
    shape_list = cmds.sets(bake_layer, q=True)
    if shape_list:
        for shape in shape_list:
            tool_utility.create_colorset(shape, tool_utility.generate_bake_colorset_name(bake_layer), [0.5, 0.5, 0.5, 1])

    # ベイクを実行
    # 同一のファイル名でベイクするとこの後の合成（恐らくcmds.convertSolidTx）で結果が反映されない不具合が出るため、時刻を付加
    now = time.localtime()
    d = time.strftime('%Y%m%d%H%M%S', now)
    this_bake_file_name = bake_tex_name.replace(tool_define.BAKE_ELM_STR, tool_define.BAKE_ELM_STR + d)
    bake_mel_command = mel.eval('ilrGetTextureBakeCmdString {} "";'.format(bake_layer))
    bake_mel_command = bake_mel_command.replace(bake_tex_name, this_bake_file_name)
    mel.eval(bake_mel_command)

    # ベイクされたテクスチャのパス
    tex_file_base_name = this_bake_file_name.replace(tool_define.BAKE_EXT_STR, 'tga')
    ill_tex_name = tex_file_base_name.replace(tool_define.BAKE_ELM_STR, tool_define.ILLUMINATION_STR)
    ill_tex_path = os.path.join(bake_tex_dir, ill_tex_name)

    gi_tex_name = tex_file_base_name.replace(tool_define.BAKE_ELM_STR, tool_define.INDIRECTION_STR)
    gi_tex_path = os.path.join(bake_tex_dir, gi_tex_name)

    custom_shader_connections = cmds.listConnections('{}.customShader'.format(bake_layer))
    custom_shader = custom_shader_connections[0] if custom_shader_connections else ''
    ao_tex_name = tex_file_base_name.replace(tool_define.BAKE_ELM_STR, custom_shader)
    ao_tex_path = os.path.join(bake_tex_dir, ao_tex_name)

    # 合成テクスチャのパス
    final_tex_name = tool_utility.generate_conbine_texture_name(bake_layer)
    final_tex_path = os.path.join(bake_tex_dir, final_tex_name)

    # 合成テクスチャの作成
    __conbine_texture(ill_tex_path, ao_tex_path, gi_tex_path, final_tex_path, use_legacy_method)

    # ベイク結果を反映するマテリアルをセットアップ
    setup_bake_material(bake_layer)

    # 中間ファイルの削除
    if os.path.exists(ill_tex_path):
        os.remove(ill_tex_path)
    if os.path.exists(ao_tex_path):
        os.remove(ao_tex_path)
    if os.path.exists(gi_tex_path):
        os.remove(gi_tex_path)


def bake_lightmap_to_vertices(bake_layer, use_gi, use_legacy_method=True):
    """頂点へライトマップをベイクする

    Args:
        bake_layer (str): ベイクするベイクレイヤー
        use_gi (bool): ベイク時にGIを計算するか
        use_legacy_method (bool, optional): 旧ツールの合成方法を使うか. Defaults to True.
    """

    bake_setting.set_must_bake_part(bake_layer, use_gi)

    # 最終結果合成用のカラーセット作成
    shape_list = cmds.sets(bake_layer, q=True)
    if shape_list:
        for shape in shape_list:
            tool_utility.create_colorset(shape, tool_utility.generate_bake_colorset_name(bake_layer))

    # ベイクを実行
    bake_mel_command = mel.eval('ilrGetVertexBakeCmdString {} "";'.format(bake_layer))
    mel.eval(bake_mel_command)

    # 旧ツールと同じ結果になるように最終結果合成用カラーセットを計算 => illumination*illumination*ao
    custom_shader_connections = cmds.listConnections('{}.customShader'.format(bake_layer))
    custom_shader = custom_shader_connections[0] if custom_shader_connections else ''
    bake_colorset_base_name = cmds.getAttr(bake_layer + '.vbColorSet')

    ill_colorset = bake_colorset_base_name.replace(tool_define.BAKE_ELM_STR, tool_define.ILLUMINATION_STR)
    ao_colorset = bake_colorset_base_name.replace(tool_define.BAKE_ELM_STR, custom_shader)
    gi_colorset = bake_colorset_base_name.replace(tool_define.BAKE_ELM_STR, tool_define.INDIRECTION_STR)
    result_colorset = tool_utility.generate_bake_colorset_name(bake_layer)

    for shape in shape_list:
        __conbine_vtx_color(shape, ill_colorset, ao_colorset, gi_colorset, result_colorset, use_legacy_method)

        # 中間カラーセットの削除
        exist_colorset_list = cmds.polyColorSet(shape, q=True, acs=True)
        if ill_colorset in exist_colorset_list:
            cmds.polyColorSet(shape, cs=ill_colorset, delete=True)
        if ao_colorset in exist_colorset_list:
            cmds.polyColorSet(shape, cs=ao_colorset, delete=True)
        if gi_colorset in exist_colorset_list:
            cmds.polyColorSet(shape, cs=gi_colorset, delete=True)


def setup_bake_material(bake_layer):
    """ベイク結果を反映するマテリアルをセットアップする

    Args:
        bake_layer (str): ベイクマテリアルをセットアップするベイクレイヤー
    """

    shape_list = cmds.sets(bake_layer, q=True)

    if not shape_list:
        return

    # マテリアルの取得
    material_list = tool_utility.get_material_list(shape_list)

    # ベイク合成結果テクスチャのファイルノード作成
    # 既存の場合はテクスチャを更新
    tex_dir = bake_setting.get_bake_texture_dir(bake_layer)
    bake_texture_name = tool_utility.generate_conbine_texture_name(bake_layer)
    tex_path = os.path.join(tex_dir, bake_texture_name)

    tex_file_node = bake_layer + '_file'

    if cmds.objExists(tex_file_node):

        # リネームした場合は出力テクスチャ名も変わるのでチェック
        if os.path.exists(tex_path):
            cmds.setAttr('{}.fileTextureName'.format(tex_file_node), tex_path, type='string')

        mel.eval('AEfileTextureReloadCmd {}'.format(tex_file_node + '.fileTextureName'))

    else:

        tex_file_node = tool_utility.create_file_node(tex_path, tex_file_node)[0]

    # uvLinkの設定
    bake_uv_name = bake_setting.get_texture_bake_uv(bake_layer)

    for shape in shape_list:

        uv_name_list = cmds.polyUVSet(shape, q=True, allUVSets=True)
        uv_index_list = cmds.polyUVSet(shape, q=True, allUVSetsIndices=True)

        if not uv_name_list:
            continue

        for name, index in zip(uv_name_list, uv_index_list):
            if name == bake_uv_name:
                uv_attr = '{}.uvSet[{}].uvSetName'.format(shape, str(index))
                cmds.uvLink(make=True, uvSet=uv_attr, texture=tex_file_node)
                break

    # 確認用マテリアルの作成
    for material in material_list:

        # プレビュー用のマテリアルの名前を定義
        bake_material = tool_utility.generate_bake_material_name(bake_layer, material)

        if not cmds.objExists(bake_material):
            bake_material = tool_utility.create_material(bake_material)

        # 元マテリアルのアウトカラーと乗算でブレンドするようにする
        mul_blend_nodes = cmds.listConnections('{}.color'.format(bake_material), type='multiplyDivide')
        mul_blend_node = None
        if mul_blend_nodes:
            mul_blend_node = mul_blend_nodes[0]
        else:
            mul_blend_node = cmds.shadingNode('multiplyDivide', asUtility=True)

        # 元マテリアルとベイクテクスチャの割り当て
        cmds.connectAttr('{}.outColor'.format(tex_file_node), '{}.input1'.format(mul_blend_node), f=True)
        cmds.connectAttr('{}.outColor'.format(material), '{}.input2'.format(mul_blend_node), f=True)
        cmds.connectAttr('{}.output'.format(mul_blend_node), '{}.color'.format(bake_material), f=True)


def __conbine_texture(ill_texture_path, ao_texture_path, gi_texture_path, result_texture_path, use_legacy_method=True):
    """各要素のテクスチャを合成する

    Args:
        ill_texture_path (str): illuminationテクスチャパス. 必ずベイクされているはず.
        ao_texture_path (str): aoテクスチャパス. 必ずベイクされているはず.
        gi_texture_path (str): indirectIlluminationテクスチャパス. giが無効ならベイクされていないはず.
        result_texture_path (str): 合成結果のテクスチャパス
        use_legacy_method (bool, optional): 旧ツールの合成方法を使うか. Defaults to True.
    """

    # シェーディング周りのノードロックがあるとエラーになるため解除する処理を挟む
    __fix_irregular_lock_node()

    # 最後に破棄する一時ノード格納用リスト
    tmp_node_list = []

    # 各ファイルノード
    ill_nodes = tool_utility.create_file_node(ill_texture_path)
    ill_file_node = ill_nodes[0]

    ao_nodes = tool_utility.create_file_node(ao_texture_path)
    ao_file_node = ao_nodes[0]

    gi_nodes = tool_utility.create_file_node(gi_texture_path)
    gi_file_node = gi_nodes[0]

    tmp_node_list.extend(ill_nodes)
    tmp_node_list.extend(ao_nodes)
    tmp_node_list.extend(gi_nodes)

    # 出力用の一時ポリゴンとマテリアル
    tmp_plane_info = cmds.polyPlane()
    tmp_mat = tool_utility.create_material('tmp_mat')
    tmp_sg = tool_utility.get_shading_group(tmp_mat)

    cmds.sets([tmp_plane_info[0]], e=True, fe=tmp_sg)

    tmp_node_list.extend([tmp_plane_info[0], tmp_mat, tmp_sg])

    if use_legacy_method:  # 旧ツールを再現した合成方法（ライトが二度掛けされる）

        ill_pow_node = cmds.shadingNode('multiplyDivide', asUtility=True)
        mul_blend_node = cmds.shadingNode('multiplyDivide', asUtility=True)
        rgb_to_hsv_node = cmds.shadingNode('rgbToHsv', asUtility=True)
        blend_col_node = cmds.shadingNode('blendColors', asUtility=True)
        export_node = cmds.shadingNode('multiplyDivide', asUtility=True)

        cmds.connectAttr('{}.outColor'.format(ao_file_node), '{}.input1'.format(mul_blend_node))
        cmds.connectAttr('{}.outColor'.format(ill_file_node), '{}.input2'.format(mul_blend_node))

        cmds.connectAttr('{}.output'.format(mul_blend_node), '{}.inRgb'.format(rgb_to_hsv_node), f=True)

        cmds.connectAttr('{}.outHsvV'.format(rgb_to_hsv_node), '{}.blender'.format(blend_col_node), f=True)
        cmds.connectAttr('{}.outColor'.format(ill_file_node), '{}.color1'.format(blend_col_node), f=True)
        cmds.connectAttr('{}.outColor'.format(gi_file_node), '{}.color2'.format(blend_col_node), f=True)

        cmds.connectAttr('{}.output'.format(blend_col_node), '{}.input1'.format(export_node))
        cmds.connectAttr('{}.output'.format(export_node), '{}.color'.format(tmp_mat))

        tmp_node_list.extend([ill_pow_node, mul_blend_node, rgb_to_hsv_node, blend_col_node, export_node])

    else:

        mul_blend_node = cmds.shadingNode('multiplyDivide', asUtility=True)
        add_blend_node = cmds.shadingNode('plusMinusAverage', asUtility=True)
        cmds.setAttr('{}.{}'.format(add_blend_node, 'operation'), 1)  # add
        export_node = cmds.shadingNode('multiplyDivide', asUtility=True)

        cmds.connectAttr('{}.outColor'.format(ill_file_node), '{}.input1'.format(mul_blend_node))
        cmds.connectAttr('{}.outColor'.format(ao_file_node), '{}.input2'.format(mul_blend_node))

        cmds.connectAttr('{}.output'.format(mul_blend_node), '{}.input3D[0]'.format(add_blend_node), f=True)
        cmds.connectAttr('{}.outColor'.format(gi_file_node), '{}.input3D[1]'.format(add_blend_node), f=True)

        cmds.connectAttr('{}.output3D'.format(add_blend_node), '{}.input1'.format(export_node))
        cmds.connectAttr('{}.output'.format(export_node), '{}.color'.format(tmp_mat))

        tmp_node_list.extend([mul_blend_node, add_blend_node, export_node])

    size_x_y = [cmds.getAttr('{}.outSizeX'.format(ill_file_node)), cmds.getAttr('{}.outSizeY'.format(ill_file_node))]
    result_nodes = cmds.convertSolidTx('{}.output'.format(export_node),
                                       tmp_plane_info,
                                       f=True,
                                       sp=False,
                                       al=False,
                                       rx=size_x_y[0],
                                       ry=size_x_y[1],
                                       fil='tga',
                                       fin=result_texture_path)

    # 一時ファイルの削除
    tmp_node_list.extend(result_nodes)
    cmds.delete(tmp_node_list)


def __conbine_vtx_color(target, ill_colorset, ao_colorset, gi_colorset, result_colorset, use_legacy_method=True):
    """各要素の頂点カラーを合成する

    Args:
        ill_colorset (str): illuminationカラーセット. 必ずベイクされているはず.
        ao_colorset (str): aoカラーセット. 必ずベイクされているはず.
        gi_colorset (str): indirectIlluminationカラーセット. giが無効ならベイクされていないはず.
        result_colorset (str): 合成結果のカラーセット
        use_legacy_method (bool, optional): 旧ツールの合成方法を使うか. Defaults to True.
    """

    exist_colorset_list = cmds.polyColorSet(target, q=True, acs=True)
    if ill_colorset not in exist_colorset_list:
        return
    if ao_colorset not in exist_colorset_list:
        return
    if result_colorset not in exist_colorset_list:
        return
    # gi_colorset はGIを有効化していない場合は存在しない

    om_select_list = om.MSelectionList()
    om_select_list.add(target)
    om_dag_path = om_select_list.getDagPath(0)
    om_mesh = om.MFnMesh(om_dag_path)

    # カラー配列を取得
    # gi_vtx_color_listはgi_colorsetがない場合は真っ黒にしておく
    ill_vtx_color_list = om_mesh.getFaceVertexColors(ill_colorset)
    ao_vtx_color_list = om_mesh.getFaceVertexColors(ao_colorset)
    gi_vtx_color_list = [om.MColor()] * len(ill_vtx_color_list)
    if gi_colorset in exist_colorset_list:
        gi_vtx_color_list = om_mesh.getFaceVertexColors(gi_colorset)

    # カラー配列に対応するvtx, faceの配列を取得
    raw_vtx_face_list = cmds.ls(cmds.polyListComponentConversion(target, tvf=True), fl=True)
    vtx_face_list = []
    for vtx_face in raw_vtx_face_list:
        m = re.search(r'\.vtxFace\[(\d+)\]\[(\d+)\]$', vtx_face)
        vtx_face_list.append([int(m.group(1)), int(m.group(2))])

    result_color_list = []
    face_id_list = []
    vtx_id_list = []

    # カラーの合成
    # # 以下のやり方はtargetが円柱の時、om_mesh.getFaceAndVertexIndices(i, False)がフリーズを起こしたため使わない（理由は不明）
    # for i, (ill_color, ao_color) in enumerate(zip(ill_vtx_color_list, ao_vtx_color_list)):
    #     result_color_list.append(ill_color * ill_color * ao_color)  # この計算の理由は不明だが元ツールからの仕様
    #     face_and_vtx_ids = om_mesh.getFaceAndVertexIndices(i, False)
    #     face_id_list.append(face_and_vtx_ids[0])
    #     vtx_id_list.append(face_and_vtx_ids[1])
    if use_legacy_method:

        for vtx_and_face, ill_color, ao_color, gi_color in zip(vtx_face_list, ill_vtx_color_list, ao_vtx_color_list, gi_vtx_color_list):
            result_color_list.append(ill_color * ill_color * ao_color + gi_color)  # この計算の理由は不明だが元ツールからの仕様
            face_id_list.append(vtx_and_face[1])
            vtx_id_list.append(vtx_and_face[0])

    else:

        for vtx_and_face, ill_color, ao_color, gi_color in zip(vtx_face_list, ill_vtx_color_list, ao_vtx_color_list, gi_vtx_color_list):
            result_color_list.append(ill_color * ao_color + gi_color)
            face_id_list.append(vtx_and_face[1])
            vtx_id_list.append(vtx_and_face[0])

    # カラーのセット
    cmds.polyColorSet(target, colorSet=result_colorset, currentColorSet=True)
    om_mesh.setFaceVertexColors(result_color_list, face_id_list, vtx_id_list)


def __fix_irregular_lock_node():
    """
    initialShadingGroup等のロック状態を修復する
    """

    # initialShadingGroup系
    try:
        cmds.lockNode('initialShadingGroup', lockUnpublished=False)
        cmds.lockNode('initialShadingGroup', lock=False)
        cmds.lockNode('initialParticleSE', lockUnpublished=False)
        cmds.lockNode('initialParticleSE', lock=False)
        cmds.setAttr('initialShadingGroup.ro', True)
        cmds.setAttr('initialParticleSE.ro', True)
    except Exception:
        cmds.warning('fix_initial_nodeを実行出来ませんでした')

    # defaultTextureList系
    default_textures = cmds.ls('defaultTextureList*')
    if default_textures:
        for texture in default_textures:
            cmds.lockNode(texture, l=False, lockUnpublished=False)
