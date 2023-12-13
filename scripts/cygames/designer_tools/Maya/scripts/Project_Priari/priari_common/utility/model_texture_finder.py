# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except:
    pass

import os
import re

from ...base_common import utility as base_utility
from . import model_define as model_define

import maya.cmds as cmds

reload(model_define)


# ===============================================
def get_texture_list_from_material(material, psd=False):
    """
    material名から予想されるテクスチャ名一覧を返す

    :param material: マテリアル
    :return: テクスチャ名リスト
    """

    if not material.startswith(model_define.MATERIAL_PREFIX):
        return []

    suffix_list = [
        model_define.DIFF_SUFFIX,
        model_define.BASE_SUFFIX,
        model_define.CTRL_SUFFIX,
        model_define.SHAD_SUFFIX,
    ]

    # マテリアルでテクスチャが異なる場合の分岐
    if material.find('_eye') >= 0:
        suffix_list = [
            model_define.DIFF_SUFFIX,
        ]
    if material.find('_face') >= 0 or material.find('_brow') >= 0:
        suffix_list = [
            model_define.DIFF_SUFFIX,
            model_define.BASE_SUFFIX,
            model_define.SHAD_SUFFIX,
        ]

    # マテリアルの接頭辞をテクスチャに入れ替えるだけで使える想定
    if material.find('_brow') >= 0:
        material = material.replace('_brow', '_face')

    if material.find('_Alpha') >= 0:
        material = re.sub('_Alpha[0-9]', '', material)

    texture_base_name = material.replace(model_define.MATERIAL_PREFIX, model_define.TEXTURE_PREFIX)

    if psd:
        return [texture_base_name + model_define.PSD_EXT]

    texture_list = []
    for suffix in suffix_list:
        texture_list.append(texture_base_name + suffix + model_define.TEXTURE_EXT)

    return texture_list


# ===============================================
def get_texture_list_from_assigned_material(mesh):
    """
    meshにアサインされているmaterial名から予想されるテクスチャ名一覧を返す

    :param material: メッシュ
    :return: テクスチャ名リスト
    """

    if not cmds.objExists(mesh):
        return []

    material_list = base_utility.material.get_material_list(mesh)

    if not material_list:
        return []

    texture_list = []

    for material in material_list:
        texture_list.extend(get_texture_list_from_material(material))

    return texture_list


# ===============================================
def get_target_texture_size(texture_name):
    """
    textureの規定サイズを返す

    :param texture_name: ファイル名
    :return: 取りうるテクスチャサイズ[w, h]
    """

    default_size = [1024, 1024]

    result_size = default_size

    if '_eye' in texture_name:
        result_size = [256, 256]

    return result_size


# ===============================================
def get_data_type(texture_name):

    data_type = ''

    if texture_name.find(model_define.AVATAR_SHORT_DATA_TYPE) >= 0:
        data_type = model_define.AVATAR_DATA_TYPE
    elif texture_name.find(model_define.UNIT_SHORT_DATA_TYPE) >= 0:
        data_type = model_define.UNIT_DATA_TYPE
    elif texture_name.find(model_define.ENEMY_SHORT_DATA_TYPE) >= 0:
        data_type = model_define.ENEMY_DATA_TYPE
    elif texture_name.find(model_define.WEAPON_SHORT_DATA_TYPE) >= 0:
        data_type = model_define.WEAPON_DATA_TYPE
    elif texture_name.find(model_define.PROP_SHORT_DATA_TYPE) >= 0:
        data_type = model_define.PROP_DATA_TYPE
    elif texture_name.find(model_define.SUMMON_SHORT_DATA_TYPE) >= 0:
        data_type = model_define.SUMMON_DATA_TYPE

    return data_type
