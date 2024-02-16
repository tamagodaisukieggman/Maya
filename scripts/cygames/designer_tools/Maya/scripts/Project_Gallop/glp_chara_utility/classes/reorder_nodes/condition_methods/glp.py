# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import re
import maya.cmds as cmds

from . import base as base_methods
from . import decorator as cm_decorator

reload(base_methods)
reload(cm_decorator)


# 顔ジョイント関連

@cm_decorator.deco_safe_bool_method
def is_nose_joint(long_name):
    """鼻のジョイントノードか
    """

    if not base_methods.is_joint(long_name):
        return False

    short_name = base_methods.get_short_name(long_name)
    return True if short_name.startswith('Nose') else False


@cm_decorator.deco_safe_bool_method
def is_chin_joint(long_name):
    """顎のジョイントノードか
    """

    if not base_methods.is_joint(long_name):
        return False

    short_name = base_methods.get_short_name(long_name)
    return True if short_name.startswith('Chin') else False


@cm_decorator.deco_safe_bool_method
def is_ear_joint(long_name):
    """耳のジョイントか
    """

    short_name = base_methods.get_short_name(long_name)
    return True if short_name.find('Ear_') == 0 or re.search('Sp_He_Ear[0-9]_', short_name) else False


# 目ジョイント関連

@cm_decorator.deco_safe_bool_method
def is_eye_joint(long_name):
    """目のジョイントノードか
    """

    if not base_methods.is_joint(long_name):
        return False

    short_name = base_methods.get_short_name(long_name)
    return True if short_name.startswith('Eye') else False


@cm_decorator.deco_safe_bool_method
def is_eye_top(long_name):
    """目のトップジョイントノードか
    """

    if not base_methods.is_joint(long_name) or not is_eye_joint(long_name):
        return False

    short_name = base_methods.get_short_name(long_name)
    return True if re.search('^Eye_[L|R]$', short_name) else False


@cm_decorator.deco_safe_bool_method
def is_eyelash(long_name):
    """まつ毛のジョイントか
    """

    if not base_methods.is_joint(long_name) or not is_eye_joint(long_name):
        return False

    short_name = base_methods.get_short_name(long_name)
    return True if re.search('^Eyelashes_[L|R]$', short_name) else False


@cm_decorator.deco_safe_str_method
def get_eye_part(long_name):
    """目のジョイントのパーツ名を取得
    """

    if not base_methods.is_joint(long_name) or not is_eye_joint(long_name):
        return ''

    eye_joint_short_name = base_methods.get_short_name(long_name)
    return eye_joint_short_name.split('_')[1]


@cm_decorator.deco_safe_int_method
def get_eye_part_sort_key(long_name):
    """目のジョイントのパーツ名ソートkeyを取得
    """

    part_order = ['middle', 'up', 'bottom', 'double', 'sub']
    part_str = get_eye_part(long_name)
    if part_str in part_order:
        return part_order.index(part_str)
    else:
        return len(part_order)


@cm_decorator.deco_safe_str_method
def get_eye_joint_side(long_name):
    """目ジョイントの左右を取得
    """

    if not base_methods.is_joint(long_name) or not is_eye_joint(long_name):
        return ''

    eye_joint_short_name = base_methods.get_short_name(long_name)
    return eye_joint_short_name.split('_')[-1]


# 手ジョイント関連

@cm_decorator.deco_safe_str_method
def get_hand_joint_part_str(long_name):
    """手のジョイントからパーツ名(どの指か)を取得
    """

    if not long_name.split('|')[-2].startswith('Wrist_'):
        return ''

    short_name = base_methods.get_short_name(long_name)
    return short_name.split('_')[0]


@cm_decorator.deco_safe_bool_method
def is_hand_joint(long_name):
    """手のジョイントか
    """

    return True if get_hand_joint_part_str(long_name) else False


@cm_decorator.deco_safe_int_method
def get_hand_part_sort_key(long_name):
    """手のジョイントのパーツ名ソートkeyを取得
    """

    part_order = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']  # 指の順
    part_str = get_hand_joint_part_str(long_name)
    if part_str in part_order:
        return part_order.index(part_str)
    else:
        return len(part_order)


# Spジョイント関連

@cm_decorator.deco_safe_str_method
def get_special_joint_prefix(long_name):
    """特殊ジョイントの接頭辞取得
    """

    if not base_methods.is_joint(long_name):
        return ''

    special_joint_prefixes = ['Sp', 'Ex', 'Tp', 'Pc']
    short_name = base_methods.get_short_name(long_name)
    prefix = short_name.split('_')[0]
    if prefix in special_joint_prefixes:
        return prefix
    else:
        return ''


@cm_decorator.deco_safe_bool_method
def is_special_joint(long_name):
    """特殊ジョイントか
    """

    if not base_methods.is_joint(long_name):
        return False

    return True if get_special_joint_prefix(long_name) else False


@cm_decorator.deco_safe_int_method
def get_special_joint_prefix_sort_key(long_name):
    """特殊ジョイントの接頭辞ソートkeyを取得
    """

    prefix_order = ['Sp', 'Ex', 'Tp', 'Pc']
    prefix = get_special_joint_prefix(long_name)

    if prefix in prefix_order:
        return prefix_order.index(prefix)
    else:
        return len(prefix_order)


@cm_decorator.deco_safe_str_method
def get_special_joint_attach_point(long_name):
    """特殊ジョイントのアタッチ場所を取得
    """

    short_name = base_methods.get_short_name(long_name)
    return short_name.split('_')[1]


@cm_decorator.deco_safe_int_method
def get_body_special_joint_attach_point_sort_key(long_name):
    """身体の特殊ジョイントのアタッチ場所ソートkeyを取得
    """

    attach_point_order = [
        'Ne',  # Neck
        'Ch',  # Chest
        'Si',  # Spine
        'Wa',  # waist
        'Sh',  # Shoulder
        'So',  # Shoulder roll
        'Ar',  # Arm
        'El',  # Elbow
        'Ao',  # Arm roll
        'Wr',  # Wrist
        'Hi',  # Hip
        'Th',  # Thigh
        'Kn',  # Knee
        'An',  # Ankle
    ]

    attach_point = get_special_joint_attach_point(long_name)

    if attach_point in attach_point_order:
        return attach_point_order.index(attach_point)
    else:
        return len(attach_point_order)


@cm_decorator.deco_safe_str_method
def get_special_joint_part(long_name):
    """特殊ジョイントのパーツ名取得
    """

    short_name = base_methods.get_short_name(long_name)
    return short_name.split('_')[2]


@cm_decorator.deco_safe_int_method
def get_head_special_joint_part_sort_key(long_name):
    """頭部の特殊ジョイントのパーツ名ソートkeyを取得
    """

    short_name = base_methods.get_short_name(long_name)
    part_str = get_special_joint_part(short_name)
    if re.search('^Ear[0-9]', part_str):  # Earringがあるので厳密にとる
        return 0
    elif part_str.startswith('Hair'):
        return 1
    else:
        return 2


@cm_decorator.deco_safe_int_method
def get_direction_sort_key(long_name):
    """特殊ジョイントの配置場所ソートkeyを取得
    """

    direction_str = ''
    if get_special_joint_prefix(long_name):
        short_name = base_methods.get_short_name(long_name)
        direction_str = short_name.split('_')[3]
    else:
        short_name = base_methods.get_short_name(long_name)
        direction_str = short_name.split('_')[-1]
    sum = 0.0
    # より前方、より左方が前に来るようにしたい
    # C=centerを0度、F=frontを10度、L=leftを89度、R=rightを91度、その他（B=back）を180度として
    # 仮想の前方からの偏差角度を出す
    for chr in direction_str:
        if chr == 'C':
            sum += 0
        elif chr == 'F':
            sum += 10
        elif chr == 'L':
            sum += 89
        elif chr == 'R':
            sum += 91
        else:
            sum += 180
    return sum / len(direction_str)


# ロケーター関連

@cm_decorator.deco_safe_str_method
def get_locator_part(long_name):
    """ロケーターのパーツ名取得
    """

    if not base_methods.is_locator(long_name):
        return ''

    short_name = base_methods.get_short_name(long_name)
    return short_name.split('_')[0]


# メッシュ関連

@cm_decorator.deco_safe_int_method
def get_head_mesh_part_order(long_name):
    """頭部メッシュのパーツ名ソートkeyを取得
    """

    part_order = ['Mayu', 'Cheek', 'Hair', 'Face']
    part = get_mesh_part(long_name)

    if part in part_order:
        return part_order.index(part)
    else:
        return len(part_order)


@cm_decorator.deco_safe_str_method
def get_mesh_part(long_name):
    """メッシュパーツ名を取得
    """

    short_name = base_methods.get_short_name(long_name)
    return short_name.split('_')[1]  # meshはM_<part>となる


@cm_decorator.deco_safe_bool_method
def is_outline_mesh(long_name):
    """アウトラインメッシュか
    """

    short_name = base_methods.get_short_name(long_name)
    return True if short_name.split('_')[-1] == 'Outline' else False
