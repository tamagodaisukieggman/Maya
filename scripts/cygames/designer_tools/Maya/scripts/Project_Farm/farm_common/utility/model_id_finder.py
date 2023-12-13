# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
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
def get_data_types(file_name):
    """
    ファイル名から各種データタイプのリストを返す

    :param file_name: モデルのファイル名
    :return: [data_type, middle_data_type, short_data_type]
    """

    data_type = ''
    middle_data_type = ''
    short_data_type = ''

    if file_name.find('{}_'.format(model_define.AVATAR_SHORT_DATA_TYPE)) >= 0:
        data_type = model_define.AVATAR_DATA_TYPE
        middle_data_type = model_define.AVATAR_MIDDLE_DATA_TYPE
        short_data_type = model_define.AVATAR_SHORT_DATA_TYPE

    elif file_name.find('{}_'.format(model_define.UNIT_SHORT_DATA_TYPE)) >= 0:
        data_type = model_define.UNIT_DATA_TYPE
        middle_data_type = model_define.UNIT_MIDDLE_DATA_TYPE
        short_data_type = model_define.UNIT_SHORT_DATA_TYPE

    elif file_name.find('{}_'.format(model_define.WEAPON_SHORT_DATA_TYPE)) >= 0:
        data_type = model_define.WEAPON_DATA_TYPE
        middle_data_type = model_define.WEAPON_MIDDLE_DATA_TYPE
        short_data_type = model_define.WEAPON_SHORT_DATA_TYPE

    elif file_name.find('{}_'.format(model_define.PROP_SHORT_DATA_TYPE)) >= 0:
        data_type = model_define.PROP_DATA_TYPE
        middle_data_type = model_define.PROP_MIDDLE_DATA_TYPE
        short_data_type = model_define.PROP_SHORT_DATA_TYPE

    elif file_name.find('{}_'.format(model_define.SUMMON_SHORT_DATA_TYPE)) >= 0:
        data_type = model_define.SUMMON_DATA_TYPE
        middle_data_type = model_define.SUMMON_MIDDLE_DATA_TYPE
        short_data_type = model_define.SUMMON_SHORT_DATA_TYPE

    elif file_name.find('{}_'.format(model_define.ENEMY_SHORT_DATA_TYPE)) >= 0:
        data_type = model_define.ENEMY_DATA_TYPE
        middle_data_type = model_define.ENEMY_MIDDLE_DATA_TYPE
        short_data_type = model_define.ENEMY_SHORT_DATA_TYPE

    elif file_name.find('{}_'.format(model_define.ENEMY_SHORT_DATA_TYPE)) >= 0:
        data_type = model_define.ENEMY_DATA_TYPE
        middle_data_type = model_define.ENEMY_MIDDLE_DATA_TYPE
        short_data_type = model_define.ENEMY_SHORT_DATA_TYPE

    # 旧ID_START
    elif file_name.find('{}_'.format('unit')) >= 0:
        data_type = model_define.UNIT_DATA_TYPE
        middle_data_type = model_define.UNIT_MIDDLE_DATA_TYPE
        short_data_type = 'unit'

    elif file_name.find('{}_'.format('prop')) >= 0:
        data_type = model_define.PROP_DATA_TYPE
        middle_data_type = model_define.PROP_MIDDLE_DATA_TYPE
        short_data_type = 'prop'
    # 旧ID_END

    else:
        print('invalid file_name')

    return [data_type, middle_data_type, short_data_type]


# ===============================================
def get_data_id(file_name, data_type):
    """
    ファイル名からデータidを返す

    :param file_name: モデルのファイル名, data_type: データタイプ
    :return: data_id
    """

    data_id = ''

    if data_type == model_define.AVATAR_DATA_TYPE:

        data_id = base_utility.string.get_string_by_regex(file_name, model_define.AVATAR_SHORT_DATA_TYPE + r'_\d{7}_\d{1}')

    elif data_type == model_define.UNIT_DATA_TYPE:

        data_id = base_utility.string.get_string_by_regex(file_name, model_define.UNIT_SHORT_DATA_TYPE + r'_\d{6}_\d{1}')

    elif data_type == model_define.WEAPON_DATA_TYPE:

        data_id = base_utility.string.get_string_by_regex(file_name, model_define.WEAPON_SHORT_DATA_TYPE + r'_\d{6}_\d{1}')

    elif data_type == model_define.PROP_DATA_TYPE:

        data_id = base_utility.string.get_string_by_regex(file_name, model_define.PROP_SHORT_DATA_TYPE + r'_\d{6}_\d{1}')

    elif data_type == model_define.SUMMON_DATA_TYPE:

        data_id = base_utility.string.get_string_by_regex(file_name, model_define.SUMMON_SHORT_DATA_TYPE + r'_\d{6}_\d{1}')

    elif data_type == model_define.ENEMY_DATA_TYPE:

        data_id = base_utility.string.get_string_by_regex(file_name, model_define.ENEMY_SHORT_DATA_TYPE + r'_\d{6}_\d{1}')

    else:
        print('invalid data_type')

    return data_id


# ===============================================
def get_file_id(file_name, data_type):
    """
    ファイル名からファイルidを返す
    file_id == data_short_name以降

    :param file_name: モデルのファイル名, data_type: データタイプ
    :return: file_id
    """

    file_id = ''

    if data_type == model_define.AVATAR_DATA_TYPE:
        file_id = base_utility.string.get_string_by_regex(file_name, model_define.AVATAR_SHORT_DATA_TYPE + r'_[^.]*')

    elif data_type == model_define.UNIT_DATA_TYPE:
        file_id = base_utility.string.get_string_by_regex(file_name, model_define.UNIT_SHORT_DATA_TYPE + r'_[^.]*')

    elif data_type == model_define.WEAPON_DATA_TYPE:
        file_id = base_utility.string.get_string_by_regex(file_name, model_define.WEAPON_SHORT_DATA_TYPE + r'_[^.]*')

    elif data_type == model_define.PROP_DATA_TYPE:

        file_id = base_utility.string.get_string_by_regex(file_name, model_define.PROP_SHORT_DATA_TYPE + r'_[^.]*')

    elif data_type == model_define.SUMMON_DATA_TYPE:
        file_id = base_utility.string.get_string_by_regex(file_name, model_define.SUMMON_SHORT_DATA_TYPE + r'_[^.]*')

    elif data_type == model_define.ENEMY_DATA_TYPE:
        file_id = base_utility.string.get_string_by_regex(file_name, model_define.ENEMY_SHORT_DATA_TYPE + r'_[^.]*')

    else:
        print('invalid data_type')

    return file_id


# ===============================================
def get_main_sub_ids(data_id, data_type):
    """
    ファイル名からメインid,サブidのリストを返す

    :param file_name: モデルのファイル名, data_type: データタイプ
    :return: [main_id, sub_id]
    """

    main_id = ''
    sub_id = ''

    match_obj = None

    if data_type == model_define.AVATAR_DATA_TYPE:

        match_obj = re.search(r'([0-9]{7})_([0-9]{1})', data_id)

        if match_obj:
            main_id = match_obj.group(1)
            sub_id = match_obj.group(2)

    elif data_type == model_define.PROP_DATA_TYPE:

        match_obj = re.search(r'([0-9]{6})_([0-9]{1})', data_id)

        if match_obj:
            main_id = match_obj.group(1)
            sub_id = match_obj.group(2)

    elif data_type == model_define.SUMMON_DATA_TYPE:

        match_obj = re.search(r'([0-9]{6})_([0-9]{1})', data_id)

        if match_obj:
            main_id = match_obj.group(1)
            sub_id = match_obj.group(2)

    else:

        match_obj = re.search(r'([0-9]{6})_([0-9]{1})', data_id)

        if match_obj:
            main_id = match_obj.group(1)
            sub_id = match_obj.group(2)

    return [main_id, sub_id]


# ===============================================
def create_scene_name(data_type, data_main_id, data_sub_id, extra_suffix=''):
    """
    データタイプとidからmayaシーン名を返す
    別タイプや別idのインフォを作成したいときに用いることを想定

    :param data_type: データタイプ, data_main_id: メインid, data_sub_id: サブid, extra_suffix: 特殊な接尾語がある場合
    :return: シーン名
    """

    if data_type == model_define.AVATAR_DATA_TYPE:
        return '{}{}_{}_{}{}{}'.format(model_define.MODEL_PREFIX, model_define.AVATAR_SHORT_DATA_TYPE, data_main_id, data_sub_id, extra_suffix, model_define.MAYA_EXT)

    elif data_type == model_define.UNIT_DATA_TYPE:
        return '{}{}_{}_{}{}{}'.format(model_define.MODEL_PREFIX, model_define.UNIT_SHORT_DATA_TYPE, data_main_id, data_sub_id, extra_suffix, model_define.MAYA_EXT)

    elif data_type == model_define.WEAPON_DATA_TYPE:
        return '{}{}_{}_{}{}{}'.format(model_define.MODEL_PREFIX, model_define.WEAPON_SHORT_DATA_TYPE, data_main_id, data_sub_id, extra_suffix, model_define.MAYA_EXT)

    elif data_type == model_define.PROP_DATA_TYPE:
        return '{}{}_{}_{}{}{}'.format(model_define.MODEL_PREFIX, model_define.PROP_SHORT_DATA_TYPE, data_main_id, data_sub_id, extra_suffix, model_define.MAYA_EXT)

    elif data_type == model_define.SUMMON_DATA_TYPE:
        return '{}{}_{}_{}{}{}'.format(model_define.MODEL_PREFIX, model_define.SUMMON_SHORT_DATA_TYPE, data_main_id, data_sub_id, extra_suffix, model_define.MAYA_EXT)

    elif data_type == model_define.ENEMY_DATA_TYPE:
        return '{}{}_{}_{}{}{}'.format(model_define.MODEL_PREFIX, model_define.ENEMY_SHORT_DATA_TYPE, data_main_id, data_sub_id, extra_suffix, model_define.MAYA_EXT)


# ===============================================
def get_maya_file_path(file_name, root_dir=''):
    """
    ファイル名から想定されるpathを返す
    root_dirが未入力ならデフォルトのSVNパスを採用

    :param file_name: ファイル名 root_dir: ルートディレクトリパス
    :return: path
    """

    data_types = get_data_types(file_name)

    if data_types[0] == '':
        return ''

    file_id = get_file_id(file_name, data_types[0])
    data_middle_type = data_types[1]

    default_root = ''
    if root_dir:
        default_root = root_dir
    else:
        default_root = model_define.SVN_PATH

    ids = get_main_sub_ids(file_name, data_types[0])
    dir_name = '{}_{}'.format(data_types[2], ids[0])

    return '{}/{}/{}/{}/scenes/{}'.format(default_root, data_middle_type, dir_name, file_id, file_name)


def get_fbx_name(file_name):
    """ファイル名からfbx名を返す
    """

    data_types = get_data_types(file_name)

    data_type = data_types[0]

    if data_type == '':
        return ''

    ids = get_main_sub_ids(file_name, data_type)
    ext = model_define.FBX_EXT

    fbx_name = '{}_{}_{}{}'.format(ids[0], ids[1], data_type, ext)

    # avatar
    if data_type == model_define.AVATAR_DATA_TYPE:
        fbx_name = '{}_{}{}'.format(ids[0], data_type, ext)

    # unit
    elif data_type == model_define.UNIT_DATA_TYPE:
        fbx_name = '{}_{}{}'.format(ids[0], data_type, ext)

    # enemy,summonはunityではunit扱いなので、unitの命名で出力する
    elif data_type == model_define.ENEMY_DATA_TYPE:
        fbx_name = '{}_{}{}'.format(ids[0], model_define.UNIT_DATA_TYPE, ext)
    elif data_type == model_define.SUMMON_DATA_TYPE:
        fbx_name = '{}_{}{}'.format(ids[0], model_define.UNIT_DATA_TYPE, ext)

    # weapon
    elif data_type == model_define.WEAPON_DATA_TYPE:
        fbx_name = '{}_{}{}'.format(ids[0], data_type, ext)

    # 800000番台のguildhousePropは別命名
    elif data_type == model_define.PROP_DATA_TYPE and str(ids[0]).startswith('8'):
        two_digit_sub_id = format(ids[1], '0>2')
        fbx_name = '{}_{}_{}{}'.format(ids[0], data_type, two_digit_sub_id, ext)

    # バトルprop
    elif data_type == model_define.PROP_DATA_TYPE:
        fbx_name = '{}_{}{}'.format(ids[0], data_type, ext)

    return fbx_name
