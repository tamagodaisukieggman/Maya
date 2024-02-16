# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from . import project_define as pj_define
from .. import tool_define as tool_define

# region メッシュ


def get_target_mesh_list(root_node):

    all_transform_list = cmds.listRelatives(root_node, typ='transform', f=True, ad=True)

    if not all_transform_list:
        return []
    else:
        all_transform_list.append(root_node)

    result_mesh_list = []
    for transform in all_transform_list:
        short_name = transform.split('|')[-1]
        if short_name.startswith(pj_define.MSH_PFX):
            result_mesh_list.append(transform)

    return result_mesh_list


# endregion

# region シェーダー


def get_shader_file(material_base_name, material_type):
    """シェーダーファイル名の取得
    """

    if material_type.find(pj_define.MTL_TYP_TOON_PFX) >= 0:

        shader_file = pj_define.FX_FILE_TOON_DEFAULT

        # suffixでシェーダーファイルを判定
        if material_base_name.find(pj_define.MTL_SFX_FACE) >= 0:
            shader_file = pj_define.FX_FILE_TOON_FACE

        elif material_base_name.find(pj_define.MTL_SFX_MAYU) >= 0:
            shader_file = pj_define.FX_FILE_TOON_FACE

        elif material_base_name.find(pj_define.MTL_SFX_HAIR) >= 0:
            shader_file = pj_define.FX_FILE_TOON_HAIR

        elif material_base_name.find(pj_define.MTL_SFX_EYE) >= 0:
            shader_file = pj_define.FX_FILE_TOON_EYE

        return shader_file

    elif material_type.find(pj_define.MTL_TYP_OUTLINE_PFX) >= 0:

        return pj_define.FX_FILE_OUTLINE

    else:
        return ''


# endregion

# region マテリアルデータ


def get_material_name(material_base_name, material_type):
    """シェーダーファイル名の取得
    """

    if material_type.find(pj_define.MTL_TYP_TOON_PFX) >= 0:
        return '{}{}{}'.format(material_base_name, tool_define.SEPARATE_STR, material_type)
    elif material_type.find(pj_define.MTL_TYP_OUTLINE_PFX) >= 0:
        return '{}{}{}'.format(material_base_name, tool_define.SEPARATE_STR, material_type)
    else:
        return material_base_name


def is_possible_mesh_type_pair(mesh_name, material_type):
    """メッシュに指定したタイプのマテリアルを割り当てる可能性があるか
    """
    # toon時のフィルタ
    if material_type.find(pj_define.MTL_TYP_TOON_PFX) >= 0:
        if mesh_name.find(pj_define.MSH_SFX_OUTLINE) >= 0:
            return False
        elif mesh_name.find(pj_define.MSH_CHEEK_STR) >= 0:
            return False
        elif mesh_name.find(pj_define.MSH_TEAR_STR) >= 0:
            return False
        elif mesh_name.find(pj_define.MSH_LINE_STR) >= 0:
            return False

    # outline時のフィルタ
    if material_type.find(pj_define.MTL_TYP_OUTLINE_PFX) >= 0:
        if not mesh_name.find(pj_define.MSH_SFX_OUTLINE) >= 0:
            return False

    return True


# endregion

# region テクスチャ


def get_texture_connect_dict(material_base_name, material_type):
    """テクスチャを接続するアトリビュートと、テクスチャ名の辞書を作成
    """

    texture_base_name = __get_texture_base_name(material_base_name)
    connect_dict = {}

    if material_type == pj_define.MTL_TYP_DEFAULT:
        # 身体
        if material_base_name.find(pj_define.MTL_PFX_BODY) >= 0:
            connect_dict = __get_body_tga_connect_dict(texture_base_name, '')
        # 頬
        elif material_base_name.find(pj_define.MTL_SFX_CHEEK) >= 0:
            connect_dict = __get_cheek_tga_connect_dict(texture_base_name, '')
        else:
            connect_dict = __get_default_tga_connect_dict(texture_base_name, '')
    elif material_type == pj_define.MTL_TYP_PSD:
        # 身体
        if material_base_name.find(pj_define.MTL_PFX_BODY) >= 0:
            connect_dict = __get_body_psd_connect_dict(texture_base_name, '')
        else:
            connect_dict = __get_default_psd_connect_dict(texture_base_name, '')
    elif material_type == pj_define.MTL_TYP_TOON:
        # 身体
        if material_base_name.find(pj_define.MTL_PFX_BODY) >= 0:
            connect_dict = __get_body_toon_connect_dict(texture_base_name, '')
        # 髪
        elif material_base_name.find(pj_define.MTL_SFX_HAIR) >= 0:
            connect_dict = __get_face_toon_connect_dict(texture_base_name, '')
        # 顔
        elif material_base_name.find(pj_define.MTL_SFX_FACE) >= 0:
            connect_dict = __get_face_toon_connect_dict(texture_base_name, '')
        # まゆ
        elif material_base_name.find(pj_define.MTL_SFX_MAYU) >= 0:
            connect_dict = __get_face_toon_connect_dict(texture_base_name, '')
        # 目
        elif material_base_name.find(pj_define.MTL_SFX_EYE) >= 0:
            connect_dict = __get_eye_toon_connect_dict(texture_base_name, '')
        else:
            connect_dict = __get_default_toon_connect_dict(texture_base_name, '')

    elif material_type == pj_define.MTL_TYP_OUTLINE:
        connect_dict = __get_default_outline_connect_dict(texture_base_name, '')

    return connect_dict


def __get_default_tga_connect_dict(texture_base_name, opt_str):

    return {
        'color': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_MAIN, opt_str, 'tga'),
    }


def __get_body_tga_connect_dict(texture_base_name, opt_str):

    return {
        'color': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_MAIN, opt_str, 'tga'),
    }


def __get_cheek_tga_connect_dict(texture_base_name, opt_str):

    return {
        'color': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_CHEEK_FOR_MAYA0, opt_str, 'tga'),
    }


def __get_default_psd_connect_dict(texture_base_name, opt_str):

    return {
        'color': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_PSD_DEFAULT, opt_str, 'psd'),
    }


def __get_body_psd_connect_dict(texture_base_name, opt_str):

    return {
        'color': '{}_00_0_0{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_PSD_DEFAULT, opt_str, 'psd'),
    }


def __get_default_toon_connect_dict(texture_base_name, opt_str):

    return {
        'mainTextureMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_MAIN, opt_str, 'tga'),
        'tripleMaskMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_TRIPLE_MASK, opt_str, 'tga'),
        'toonTextureMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_TOON, opt_str, 'tga'),
        'optionMaskMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_OPTION_MASK, opt_str, 'tga'),
        '_DirtTex': '{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_DIRT, 'tga'),
        '_EmissiveTex': '{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_EMISSIVE, 'tga'),
        '_MaskColorTex': '{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_MASK_COL, 'tga'),
    }


def __get_body_toon_connect_dict(texture_base_name, opt_str):

    return {
        'mainTextureMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_MAIN, opt_str, 'tga'),
        'tripleMaskMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_TRIPLE_MASK, opt_str, 'tga'),
        'toonTextureMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_TOON, opt_str, 'tga'),
        'optionMaskMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_OPTION_MASK, opt_str, 'tga'),
        '_DirtTex': '{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_DIRT, 'tga'),
        '_EmissiveTex': '{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_EMISSIVE, 'tga'),
        '_MaskColorTex': '{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_MASK_COL, 'tga'),
    }


def __get_face_toon_connect_dict(texture_base_name, opt_str):

    return {
        'mainTextureMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_MAIN, opt_str, 'tga'),
        'tripleMaskMap': '{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_TRIPLE_MASK, 'tga'),
        'toonTextureMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_TOON, opt_str, 'tga'),
        'optionMaskMap': '{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_OPTION_MASK, 'tga'),
        '_DirtTex': '{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_DIRT, 'tga'),
        '_EmissiveTex': '{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_EMISSIVE, 'tga'),
        '_MaskColorTex': '{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_MASK_COL, 'tga'),
    }


def __get_eye_toon_connect_dict(texture_base_name, opt_str):

    return {
        'mainTextureMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_EYE_MAIN, opt_str, 'tga'),
        'high0TexMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_EYE_HI0, opt_str, 'tga'),
        'high1TexMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_EYE_HI1, opt_str, 'tga'),
        'high2TexMap': '{}{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_EYE_HI2, opt_str, 'tga'),
    }


def __get_default_outline_connect_dict(texture_base_name, opt_str):

    return {
        'mainTextureMap': '{}_00_0_0{}{}.{}'.format(texture_base_name, pj_define.TEX_SFX_MAIN, opt_str, 'tga'),
    }


def __get_texture_base_name(material_base_name):

    material_base_name = material_base_name.replace('_Luminous', '')
    # まゆは顔と同じマテリアル
    material_base_name = material_base_name.replace(pj_define.MTL_SFX_MAYU, pj_define.MTL_SFX_FACE)
    # マテリアルの接頭辞を入れ替えるとテクスチャのベース名になる
    texture_base_name = material_base_name.replace(pj_define.MTL_PFX, pj_define.TEX_PFX)

    return texture_base_name


# endregion

# region アトリビュート


def get_attr_dict(material_base_name, material_type):

    if material_type.find(pj_define.MTL_TYP_TOON_PFX) >= 0:
        return __get_toon_attr_dict(material_base_name)
    elif material_type.find(pj_define.MTL_TYP_OUTLINE_PFX) >= 0:
        return __get_outline_attr_dict(material_base_name)
    else:
        return {}


def __get_toon_attr_dict(material_base_name):

    attr_val_dict = {
        'xSpecularPower': 0.15,
        'xEnvRate': 1,
        'xEnvBias': 5,
        'xToonStep': 0.4,
        'xToonFeather': 0.001,
        'xUseOptionMaskMap': 1,
        'xRimStep': 0.15,
        'xRimFeather': 0.001,
        'xRimColorRGB': [89 / 255, 65 / 255, 55 / 255],
        'xRimColorA': 100 / 255,
        'xRimShadow': 2,
        'xRimSpecRate': 1,
        'xGlobalDirtColorRGB': [89 / 255, 65 / 255, 55 / 255],
        'xGlobalDirtRimSpecularColorRGB': [154 / 255, 115 / 255, 98 / 255],
        'xCutoff': 0.0,
        'xEmissiveColor': [1, 1, 1],
        'xDirtRate1': 0.0,
        'xDirtRate2': 0.0,
        'xDirtRate3': 0.0,
        'xSpecularColorRGB': [1.0, 1.0, 1.0],
        'xFaceCenterPos': [0, 0, 0],
    }

    if material_base_name.find(pj_define.MTL_SFX_FACE) >= 0:

        opt_dict = {
            'xFaceCenterPos': [0, 0.1292 * 100, 0.01289 * 100],
            'xRimColorA': 50 / 255,
            'xCutoff': 0.5,
        }
        attr_val_dict.update(opt_dict)

    elif material_base_name.find(pj_define.MTL_SFX_HAIR) >= 0:

        opt_dict = {
            'xRimColorA': 50 / 255,
            'xCutoff': 0.5,
            'xToonStep': 0.3,
        }
        attr_val_dict.update(opt_dict)

    elif material_base_name.find(pj_define.MTL_SFX_EYE) >= 0:

        opt_dict = {
            'xRepeatUV': 0.25,
            '_MainParam0': [0, 0, 0, 0],
            '_MainParam1': [0, 0, 0, 0],
            '_HighParam10': [0, 0, 0, 1],
            '_HighParam11': [0, 0, 0, 1],
            '_HighParam12': [0, 0, 0, 0],
            '_HighParam20': [0, 0, 0, 1],
            '_HighParam21': [0, 0, 0, 1],
        }
        attr_val_dict.update(opt_dict)

    if material_base_name.find(pj_define.MTL_SFX_ALPHA) >= 0:

        opt_dict = {
            'xCutoff': 0.2,
        }
        attr_val_dict.update(opt_dict)

    return attr_val_dict


def __get_outline_attr_dict(material_base_name):

    attr_val_dict = {
        'xOutlineWidth': 0.325,
        'xOutlineColorRGB': [0.125, 0.047, 0],
        'xOutlineColorA': 0.09803922,
        'xGlobalOutlineOffset': 1.0,
        'xGlobalOutlineWidth': 1.0,
        'xGlobalCameraFov': 15.0,
    }

    return attr_val_dict


# endregion

# region プロジェクト処理呼び出しキー


def get_project_command_list(material_base_name, material_type):

    command_list = []

    if material_type.find(pj_define.MTL_TYP_TOON_PFX) >= 0:
        command_list.append(pj_define.CMD_CHARA_LIGHT_CONNECTION)

        if material_base_name.find(pj_define.MTL_SFX_FACE) >= 0:
            command_list.append(pj_define.CMD_SPEC_LOC_CONNECTION)
            command_list.append(pj_define.CMD_HEAD_LOCATOR_CONNECTION)

        elif material_base_name.find(pj_define.MTL_SFX_HAIR) >= 0:
            command_list.append(pj_define.CMD_SPEC_LOC_CONNECTION)
            command_list.append(pj_define.CMD_HEAD_LOCATOR_CONNECTION)

        elif material_base_name.find(pj_define.MTL_PFX_TAIL) >= 0:
            command_list.append(pj_define.CMD_SPEC_LOC_CONNECTION)

        elif material_base_name.find(pj_define.MTL_PFX_BODY) >= 0:
            command_list.append(pj_define.CMD_SPEC_LOC_CONNECTION)

    elif material_type.find(pj_define.MTL_TYP_OUTLINE_PFX) >= 0:
        command_list.append(pj_define.CMD_OUTLINE_MESH_VISIBLE)

    return command_list


# endregion