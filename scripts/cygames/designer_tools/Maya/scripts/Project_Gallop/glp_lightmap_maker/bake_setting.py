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
from . import tool_utility

reload(tool_define)
reload(tool_utility)


def init_bake_layer(bake_layer):
    """ベイクレイヤーの設定を初期化

    Args:
        bake_layer (str): 初期化するベイクレイヤー
    """

    for setting in tool_define.DEFAULT_SETTING_LIST:
        __set_attr(setting, bake_layer)

    add_extra_attr(bake_layer)


def add_extra_attr(bake_layer):
    """ツール用のアトリビュートを追加する

    Args:
        bake_layer (str): アトリビュートを追加するベイクレイヤー
    """

    # ライトセット保持用
    attr_list = cmds.listAttr(bake_layer)

    if tool_define.GLP_LIGHT_SET_ATTR not in attr_list:
        cmds.addAttr(bake_layer, longName=tool_define.GLP_LIGHT_SET_ATTR, dataType='string')

    # textureテストサイズ保持用
    if tool_define.GLP_TEST_RES_X_ATTR not in attr_list:
        cmds.addAttr(bake_layer, longName=tool_define.GLP_TEST_RES_X_ATTR, defaultValue=tool_define.TEST_TEX_RES_X)
    if tool_define.GLP_TEST_RES_Y_ATTR not in attr_list:
        cmds.addAttr(bake_layer, longName=tool_define.GLP_TEST_RES_Y_ATTR, defaultValue=tool_define.TEST_TEX_RES_X)

    # Rayのテストmin, max保持用
    if tool_define.GLP_TEST_RAY_MIN_ATTR not in attr_list:
        cmds.addAttr(bake_layer, longName=tool_define.GLP_TEST_RAY_MIN_ATTR, defaultValue=tool_define.TEST_RAY_MIN_VAL)
    if tool_define.GLP_TEST_RAY_MAX_ATTR not in attr_list:
        cmds.addAttr(bake_layer, longName=tool_define.GLP_TEST_RAY_MAX_ATTR, defaultValue=tool_define.TEST_RAY_MAX_VAL)


def init_custom_shader(custom_shader):
    """カスタムシェーダーの初期化

    Args:
        custom_shader (str): 初期化するカスタムシェーダー
    """

    if not cmds.objExists(custom_shader):
        return

    __set_attr({'attr': 'minColor', 'type': 'double3', 'value': [0, 0, 0]}, custom_shader)
    __set_attr({'attr': 'maxColor', 'type': 'double3', 'value': [1, 1, 1]}, custom_shader)

    __set_attr({'attr': 'minSamples', 'type': 'int', 'value': tool_define.RAY_MIN}, custom_shader)
    __set_attr({'attr': 'maxSamples', 'type': 'int', 'value': tool_define.RAY_MAX}, custom_shader)


def create_custom_shader(bake_layer):
    """カスタムシェーダーの作成

    Args:
        bake_layer (str): このカスタムシェーダーを使用するベイクレイヤー

    Returns:
        str: 作成したカスタムシェーダー
    """

    sampler_name = bake_layer + tool_define.AO_SAMPLER_SUFFIX
    return cmds.shadingNode('ilrOccSampler', asShader=True, name=sampler_name)


def get_custom_shader(bake_layer):
    """カスタムシェーダーの取得

    Args:
        bake_layer (str): 対象のベイクレイヤー

    Returns:
        str: カスタムシェーダーノード
    """

    sampler_name = bake_layer + tool_define.AO_SAMPLER_SUFFIX
    if cmds.objExists(sampler_name):
        return sampler_name
    else:
        return None


def set_custom_shader(bake_layer):
    """カスタムシェーダーをベイクレイヤーにセット
    対応するカスタムシェーダーが存在ない場合は新規作成してセット

    Args:
        bake_layer (_type_): _description_
    """

    shader = get_custom_shader(bake_layer)

    if not shader:
        shader = create_custom_shader(bake_layer)
        init_custom_shader(shader)

    sampler_connections = cmds.listConnections(bake_layer + '.customShader')
    if not sampler_connections or shader not in sampler_connections:
        cmds.connectAttr(shader + '.outColor', bake_layer + '.customShader', f=True)


def get_bake_type(bake_layer):
    """ベイクタイプの取得

    Args:
        bake_layer (str): ベイクレイヤー

    Returns:
        int: 1=BakeToTexture, 2=BakeToVertices
    """
    return cmds.getAttr('{}.renderType'.format(bake_layer))


def set_bake_type(bake_layer, bake_typ_num):
    """ベイクタイプをセット

    Args:
        bake_layer (str): 操作するベイクレイヤー
        bake_typ_num (int): 1=BakeToTexture, 2=BakeToVertices
    """

    # 1=BakeToTexture, 2=BakeToVertices
    if bake_typ_num == 1 or bake_typ_num == 2:
        __set_attr({'attr': 'renderType', 'type': 'int', 'value': bake_typ_num}, bake_layer)


def get_bake_texture_dir(bake_layer):
    """出力先ディレクトリを取得

    Args:
        bake_layer (str): 対象ベイクレイヤー

    Returns:
        str: 出力先ディレクトリパス
    """

    return cmds.getAttr('{}.tbDirectory'.format(bake_layer))


def set_bake_texture_dir(bake_layer, output_dir):
    """出力先ディレクトリの設定

    Args:
        bake_layer (str): 対象ベイクレイヤー
        output_dir (str): 出力先ディレクトリパス
    """

    __set_attr({'attr': 'tbDirectory', 'type': 'string', 'value': output_dir}, bake_layer)


def get_bake_texture_name(bake_layer):
    """ベイクテクスチャ名を取得
    turtleのベイク用の添え字が付いたままの名前が取れる

    Args:
        bake_layer (str): 対象ベイクレイヤー

    Returns:
        str: ベイクテクスチャ名
    """

    return cmds.getAttr('{}.tbFileName'.format(bake_layer))


def set_bake_texture_name(bake_layer, output_name):
    """ベイクテクスチャ名の設定
    設定するのはturtleのベイク用の添え字が付いた名前

    Args:
        bake_layer (str): 対象ベイクレイヤー
        output_name (str): 設定するベイクテクスチャ名
    """

    __set_attr({'attr': 'tbFileName', 'type': 'string', 'value': output_name}, bake_layer)


def set_texture_bake_uv(bake_layer, uv_set):
    """テクスチャベイクで使うUVセットを指定

    Args:
        bake_layer (str): 操作するベイクレイヤー
        uv_set (str): セットするUVセット名
    """

    __set_attr({'attr': 'tbUvSet', 'type': 'string', 'value': uv_set}, bake_layer)


def get_texture_bake_uv(bake_layer):
    """テクスチャベイクで使うUVセットを取得

    Args:
        bake_layer (str): ベイクレイヤー
    """

    return cmds.getAttr('{}.tbUvSet'.format(bake_layer))


def set_texture_bake_res(bake_layer, res_x, res_y):
    """テクスチャベイクの解像度を指定

    Args:
        bake_layer (str): 操作するベイクレイヤー
        res_x (int): ベイクテクスチャの幅
        res_y (int): ベイクテクスチャの高さ
    """

    if res_x < 1:
        res_x = 1
    if res_y < 1:
        res_y = 1

    __set_attr({'attr': 'tbResX', 'type': None, 'value': res_x}, bake_layer)
    __set_attr({'attr': 'tbResY', 'type': None, 'value': res_y}, bake_layer)


def get_texture_bake_res(bake_layer):
    """テクスチャベイクの解像度を取得

    Args:
        bake_layer (str): ベイクレイヤー

    Returns:
        list: [ベイクテクスチャの幅, ベイクテクスチャの高さ]
    """

    res_x = cmds.getAttr('{}.tbResX'.format(bake_layer))
    res_y = cmds.getAttr('{}.tbResY'.format(bake_layer))
    return [res_x, res_y]


def set_texture_bake_test_res(bake_layer, test_res_x, test_res_y):
    """テクスチャベイクのテスト解像度を指定

    Args:
        bake_layer (str): 操作するベイクレイヤー
        test_res_x (int): ベイクテクスチャの幅
        test_res_y (int): ベイクテクスチャの高さ
    """

    if test_res_x < 1:
        test_res_x = 1
    if test_res_y < 1:
        test_res_y = 1

    attr_list = cmds.listAttr(bake_layer)

    if tool_define.GLP_TEST_RES_X_ATTR in attr_list:
        __set_attr({'attr': tool_define.GLP_TEST_RES_X_ATTR, 'type': None, 'value': test_res_x}, bake_layer)
    if tool_define.GLP_TEST_RES_Y_ATTR in attr_list:
        __set_attr({'attr': tool_define.GLP_TEST_RES_Y_ATTR, 'type': None, 'value': test_res_y}, bake_layer)


def get_texture_bake_test_res(bake_layer):
    """テクスチャベイクのテスト解像度を取得

    Args:
        bake_layer (str): ベイクレイヤー

    Returns:
        list: [ベイクテクスチャの幅, ベイクテクスチャの高さ]
    """

    attr_list = cmds.listAttr(bake_layer)

    test_res_x = cmds.getAttr('{}.tbResX'.format(bake_layer))
    test_res_y = cmds.getAttr('{}.tbResY'.format(bake_layer))

    if tool_define.GLP_TEST_RES_X_ATTR in attr_list:
        test_res_x = int(cmds.getAttr('{}.{}'.format(bake_layer, tool_define.GLP_TEST_RES_X_ATTR)))
    if tool_define.GLP_TEST_RES_Y_ATTR in attr_list:
        test_res_y = int(cmds.getAttr('{}.{}'.format(bake_layer, tool_define.GLP_TEST_RES_Y_ATTR)))

    return [test_res_x, test_res_y]


def set_must_bake_part(bake_layer, use_gi=False):
    """最低限必要なベイク要素を有効化

    Args:
        bake_layer (str): 操作するベイクレイヤー
        use_gi (bool): ベイク時にGIを計算するか
    """

    # indirectIllumination=gi, illumination=ライティングのみ, custom=aoSampler
    if use_gi:
        __set_attr({'attr': 'indirectIllumination', 'type': 'bool', 'value': True}, bake_layer)
    else:
        __set_attr({'attr': 'indirectIllumination', 'type': 'bool', 'value': False}, bake_layer)

    __set_attr({'attr': 'illumination', 'type': 'bool', 'value': True}, bake_layer)
    __set_attr({'attr': 'custom', 'type': 'bool', 'value': True}, bake_layer)


def set_bake_color_set(bake_layer):
    """頂点カラーベイクで使うカラーセットをセット
    セットされるカラーセット名は (bake_layer)_(tool_define.BAKE_ELM_STR)

    Args:
        bake_layer (str): 操作するベイクレイヤー
    """

    __set_attr({'attr': 'vbColorSet', 'type': 'string', 'value': '{}_{}'.format(bake_layer, tool_define.BAKE_ELM_STR)}, bake_layer)


def get_bake_color_set(bake_layer):
    """頂点カラーベイクで使うカラーセットを取得

    Args:
        bake_layer (str): ベイクレイヤー

    Returns:
        str: 頂点カラーベイクで使うカラーセット名
    """

    return cmds.getAttr('{}.{}'.format(bake_layer, 'vbColorSet'))


def set_light_set(bake_layer, light_set):
    """ベイクに使用するライトセットを指定

    Args:
        bake_layer (str): 操作するベイクレイヤー
        light_set (str): ベイクに使用するライトセット
    """

    __set_attr({'attr': tool_define.GLP_LIGHT_SET_ATTR, 'type': 'string', 'value': light_set}, bake_layer)


def get_light_set(bake_layer):
    """ベイクに使用するライトセットを取得

    Args:
        bake_layer (str): ベイクレイヤー

    Returns:
        str: ベイクに使用するライトセット
    """

    return cmds.getAttr('{}.{}'.format(bake_layer, tool_define.GLP_LIGHT_SET_ATTR))


def set_ray_min_max_value(bake_layer, ray_min_max):
    """カスタムシェーダーのMin/MaxSampleRaysをセット

    Args:
        bake_layer (str): 操作するベイクレイヤー
        ray_min_max (list): [MinSampleRays, MaxSampleRays]
    """

    custom_shader = get_custom_shader(bake_layer)

    if custom_shader:
        __set_attr({'attr': 'minSamples', 'type': 'int', 'value': ray_min_max[0]}, custom_shader)
        __set_attr({'attr': 'maxSamples', 'type': 'int', 'value': ray_min_max[1]}, custom_shader)


def get_ray_min_max_value(bake_layer):
    """カスタムシェーダーのMin/MaxSampleRaysを取得

    Args:
        bake_layer (str): ベイクレイヤー

    Returns:
        list: [MinSampleRays, MaxSampleRays]
    """

    custom_shader = get_custom_shader(bake_layer)

    ray_min_max = [1, 1]

    if custom_shader:
        ray_min_max[0] = cmds.getAttr('{}.minSamples'.format(custom_shader))
        ray_min_max[1] = cmds.getAttr('{}.maxSamples'.format(custom_shader))

    return ray_min_max


def set_test_ray_min_max_value(bake_layer, test_ray_min_max):
    """カスタムシェーダーのテストMin/MaxSampleRaysをセット

    Args:
        bake_layer (str): 操作するベイクレイヤー
        ray_min_max (list): [MinSampleRays, MaxSampleRays]
    """

    attr_list = cmds.listAttr(bake_layer)

    if tool_define.GLP_TEST_RAY_MIN_ATTR in attr_list:
        __set_attr({'attr': tool_define.GLP_TEST_RAY_MIN_ATTR, 'type': 'int', 'value': test_ray_min_max[0]}, bake_layer)
    if tool_define.GLP_TEST_RAY_MAX_ATTR in attr_list:
        __set_attr({'attr': tool_define.GLP_TEST_RAY_MAX_ATTR, 'type': 'int', 'value': test_ray_min_max[1]}, bake_layer)


def get_test_ray_min_max_value(bake_layer):
    """カスタムシェーダーのテストMin/MaxSampleRaysを取得

    Args:
        bake_layer (str): ベイクレイヤー

    Returns:
        list: [MinSampleRays, MaxSampleRays]
    """

    attr_list = cmds.listAttr(bake_layer)

    ray_min_max = [1, 1]

    if tool_define.GLP_TEST_RAY_MIN_ATTR in attr_list:
        ray_min_max[0] = int(cmds.getAttr('{}.{}'.format(bake_layer, tool_define.GLP_TEST_RAY_MIN_ATTR)))
    if tool_define.GLP_TEST_RAY_MAX_ATTR in attr_list:
        ray_min_max[1] = int(cmds.getAttr('{}.{}'.format(bake_layer, tool_define.GLP_TEST_RAY_MAX_ATTR)))

    return ray_min_max


def __set_attr(setting_dict, root_node):
    """cmds.setAttrのラッパー
    defineの設定をまとめてセットするのに使用

    Args:
        setting_dict (dict): {'attr': (str), 'type': 'str', 'value': any}
        root_node (str): 設定するnode
    """

    arg_no_need_types = ['int', 'float', 'long', 'short', 'bool', 'enum']
    unpack_types = ['float2', 'float3', 'double2', 'double3']

    if not setting_dict['type'] or setting_dict['type'] in arg_no_need_types:
        cmds.setAttr('{}.{}'.format(root_node, setting_dict['attr']), setting_dict['value'])
    elif setting_dict['type'] in unpack_types:
        cmds.setAttr('{}.{}'.format(root_node, setting_dict['attr']), *(setting_dict['value']), type=setting_dict['type'])
    else:
        cmds.setAttr('{}.{}'.format(root_node, setting_dict['attr']), setting_dict['value'], type=setting_dict['type'])
