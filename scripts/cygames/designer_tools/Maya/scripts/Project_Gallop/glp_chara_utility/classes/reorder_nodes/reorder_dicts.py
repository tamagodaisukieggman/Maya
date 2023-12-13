# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import copy

from .condition_methods import base as base_method
from .condition_methods import glp as glp_method

reload(base_method)
reload(glp_method)


"""
並び替えを指定するorder_dicts
reorder_list()に並び変えたいリストと以下のorder_dictsを渡すことで意図した並び替えを行う
並び変えたいリストの各要素をorder_dictsの先頭のdictから判定していき、判定に通ったdictのmembersに格納される

order_dictの要素は以下の通り
'desc': このdictの説明
'func': このdictのメンバーかの判定を行うメソッド. Noneのときは無条件でメンバーとなる
'targat_return': funcからこの値が返ってきたときdictのメンバーと判定する
'order_dicts': メンバーに対して更に特殊な並び替えがあるときに用いるorder_dicts
'sort_key_funcs': メンバーを並び変える際に用いるsort()のkeyを取得するメソッドを優先度順に記載したリスト
"""

# デフォルトの並び替え
default_order_dicts = [

    {
        'desc': 'ジョイント',
        'func': base_method.is_joint,
        'targat_return': True,
        'members': [],
        'order_dicts': [

            {
                'desc': '通常骨',
                'func': glp_method.is_special_joint,
                'targat_return': False,
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': '特別骨',
                'func': glp_method.is_special_joint,
                'targat_return': True,
                'members': [],
                'order_dicts': None,
                'sort_key_funcs': [
                    glp_method.get_body_special_joint_attach_point_sort_key,  # まずアタッチポイント順
                    glp_method.get_special_joint_prefix_sort_key,  # まず接頭辞のオーダー順
                    glp_method.get_special_joint_part,  # 次にpart名
                    glp_method.get_direction_sort_key,  # 次に方向前から
                ],
            },

            {
                'desc': 'default',
                'func': None,
                'members': [],
                'order_dicts': None,
            },
        ]
    },

    {
        'desc': 'ロケーター',
        'func': base_method.is_locator,
        'targat_return': True,
        'members': [],
        'order_dicts': None
    },

    {
        'desc': 'メッシュ',
        'func': base_method.is_mesh,
        'targat_return': True,
        'members': [],
        'order_dicts': None,
    },

    {
        'desc': 'default',
        'func': None,
        'members': [],
        'order_dicts': None,
    },
]

# 基本的なルートノード内の並び替え
root_order_dicts = [

    {
        'desc': 'ジョイント',
        'func': base_method.is_joint,
        'targat_return': True,
        'members': [],
        'order_dicts': [

            {
                'desc': '通常骨',
                'func': glp_method.is_special_joint,
                'targat_return': False,
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': '特別骨',
                'func': glp_method.is_special_joint,
                'targat_return': True,
                'members': [],
                'order_dicts': None,
                'sort_key_funcs': [
                    glp_method.get_body_special_joint_attach_point_sort_key,  # まずアタッチポイント順
                    glp_method.get_special_joint_prefix_sort_key,  # まず接頭辞のオーダー順
                    glp_method.get_special_joint_part,  # 次にpart名
                    glp_method.get_direction_sort_key,  # 次に方向前から
                ],
            },

            {
                'desc': 'default',
                'func': None,
                'members': [],
                'order_dicts': None,
            },
        ]
    },

    {
        'desc': 'ロケーター',
        'func': base_method.is_locator,
        'targat_return': True,
        'members': [],
        'order_dicts': [

            {
                'desc': 'ポジション',
                'func': base_method.get_short_name,
                'targat_return': 'Position',
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': 'default',
                'func': None,
                'members': [],
                'order_dicts': None,
            },
        ]
    },

    {
        'desc': 'メッシュ',
        'func': base_method.is_mesh,
        'targat_return': True,
        'members': [],
        'order_dicts': [

            {
                'desc': '通常メッシュ',
                'func': glp_method.is_outline_mesh,
                'targat_return': False,
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': 'アウトラインメッシュ',
                'func': glp_method.is_outline_mesh,
                'targat_return': True,
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': 'default',
                'func': None,
                'members': [],
                'order_dicts': None,
            },
        ],
    },
]

# 頭部ルートモデル内の並び替え
head_model_root_order_dicts = [

    {
        'desc': 'ジョイント',
        'func': base_method.is_joint,
        'targat_return': True,
        'members': [],
        'order_dicts': None
    },

    {
        'desc': 'ロケーター',
        'func': base_method.is_locator,
        'targat_return': True,
        'members': [],
        'order_dicts': [

            {
                'desc': '髪ロケーター',
                'func': glp_method.get_locator_part,
                'targat_return': 'Hair',
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': '顔ロケーター',
                'func': glp_method.get_locator_part,
                'targat_return': 'Face',
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': '目ロケーター',
                'func': glp_method.get_locator_part,
                'targat_return': 'Eye',
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': 'default',
                'func': None,
                'members': [],
                'order_dicts': None,
            },
        ]
    },

    {
        'desc': 'メッシュ',
        'func': base_method.is_mesh,
        'targat_return': True,
        'members': [],
        'order_dicts': [

            {
                'desc': '通常メッシュ',
                'func': glp_method.is_outline_mesh,
                'targat_return': False,
                'members': [],
                'order_dicts': None,
                'sort_key_funcs': [
                    glp_method.get_head_mesh_part_order,  # パーツ名ソート
                ]
            },

            {
                'desc': 'アウトラインメッシュ',
                'func': glp_method.is_outline_mesh,
                'targat_return': True,
                'members': [],
                'order_dicts': None,
                'sort_key_funcs': [
                    glp_method.get_head_mesh_part_order,  # パーツ名ソート
                ]
            },

            {
                'desc': 'default',
                'func': None,
                'members': [],
                'order_dicts': None,
            },
        ],
    },

]

# Headノード内の並び替え
head_order_dicts = [

    {
        'desc': 'ジョイント',
        'func': base_method.is_joint,
        'targat_return': True,
        'members': [],
        'order_dicts': [

            {
                'desc': '鼻',
                'func': glp_method.is_nose_joint,
                'targat_return': True,
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': '顎',
                'func': glp_method.is_chin_joint,
                'targat_return': True,
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': '目',
                'func': glp_method.is_eye_joint,
                'targat_return': True,
                'members': [],
                'order_dicts': [

                    {
                        'desc': '左',
                        'func': glp_method.get_eye_joint_side,
                        'targat_return': 'L',
                        'members': [],
                        'order_dicts': [

                            {
                                'desc': 'トップ',
                                'func': glp_method.is_eye_top,
                                'targat_return': True,
                                'members': [],
                                'order_dicts': None,
                            },

                            {
                                'desc': 'まつ毛',
                                'func': glp_method.is_eyelash,
                                'targat_return': True,
                                'members': [],
                                'order_dicts': None,
                            },

                            {
                                'desc': 'default',
                                'func': None,
                                'members': [],
                                'order_dicts': None,
                                'sort_key_funcs': [
                                    glp_method.get_eye_part_sort_key,  # up, buttomなどパーツの位置でソート
                                ]
                            },
                        ],
                    },

                    {
                        'desc': '右',
                        'func': glp_method.get_eye_joint_side,
                        'targat_return': 'R',
                        'members': [],
                        'order_dicts': [

                            {
                                'desc': 'トップ',
                                'func': glp_method.is_eye_top,
                                'targat_return': True,
                                'members': [],
                                'order_dicts': None,
                            },

                            {
                                'desc': 'まつ毛',
                                'func': glp_method.is_eyelash,
                                'targat_return': True,
                                'members': [],
                                'order_dicts': None,
                            },

                            {
                                'desc': 'default',
                                'func': None,
                                'members': [],
                                'order_dicts': None,
                                'sort_key_funcs': [
                                    glp_method.get_eye_part_sort_key,  # up, buttomなどパーツの位置でソート
                                ]
                            },
                        ],
                    },

                    {
                        'desc': 'default',
                        'func': None,
                        'members': [],
                        'order_dicts': None,
                    },
                ]
            },

            {
                'desc': '特別骨',
                'func': glp_method.is_special_joint,
                'targat_return': True,
                'members': [],
                'order_dicts': None,
                'sort_key_funcs': [
                    glp_method.get_special_joint_prefix_sort_key,  # まず接頭辞のオーダー順
                    glp_method.get_head_special_joint_part_sort_key,  # 次にpart名の優先度が高いもの
                    glp_method.get_special_joint_part,  # 次にpart名
                    glp_method.get_direction_sort_key,  # 次に方向前から
                ],
            },

            {
                'desc': 'default',
                'func': None,
                'members': [],
                'order_dicts': None,
            },
        ]
    },

    {
        'desc': 'ロケーター',
        'func': base_method.is_locator,
        'targat_return': True,
        'members': [],
        'order_dicts': [

            {
                'desc': 'ヘッドロケーター',
                'func': glp_method.get_locator_part,
                'targat_return': 'Head',
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': '眉毛ロケーター',
                'func': glp_method.get_locator_part,
                'targat_return': 'Eyebrow',
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': '目ロケーター',
                'func': glp_method.get_locator_part,
                'targat_return': 'Eye',
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': 'default',
                'func': None,
                'members': [],
                'order_dicts': None,
            },
        ]
    },

    {
        'desc': 'メッシュ',
        'func': base_method.is_mesh,
        'targat_return': True,
        'members': [],
        'order_dicts': None,
    }
]

# Hip内の並び替え
hip_order_dicts = [

    {
        'desc': 'ロケーター',
        'func': base_method.is_locator,
        'targat_return': True,
        'members': [],
        'order_dicts': [

            {
                'desc': '上半身',
                'func': base_method.get_short_name,
                'targat_return': 'UpBody_Ctrl',
                'members': [],
                'order_dicts': None,
            },

            {
                'desc': '尻尾',
                'func': base_method.get_short_name,
                'targat_return': 'Tail_Ctrl',
                'members': [],
                'order_dicts': None,
            },
        ]
    },

    {
        'desc': 'ウェスト（ミニはヒップ直下にWaistが来る）',
        'func': base_method.get_short_name,
        'targat_return': 'Waist',
        'members': [],
        'order_dicts': None
    },

]

# Wrist内の並び替え
wrist_order_dicts = [

    {
        'desc': '手のジョイント',
        'func': glp_method.is_hand_joint,
        'targat_return': True,
        'members': [],
        'order_dicts': None,
        'sort_key_funcs': [
            glp_method.get_hand_part_sort_key,  # 指の順
        ],
    },

]


def get_sorted_order_dicts(target_list, order_dicts):
    """振り分けを行ったorder_dictsを取得

    Args:
        target_list (list): 振り分けるリスト
        order_dicts (list): 振り分ける情報が入ったdictのlist

    Returns:
        list: 振り分け後のorder_dicts
    """

    result_dicts = copy.deepcopy(order_dicts)  # 元のorder_dictsは触らないようにする
    __sort_into_order_dicts(target_list, result_dicts)

    return result_dicts


def __sort_into_order_dicts(target_list, order_dicts):
    """listの中身をreorder_dictsに振り分ける

    Args:
        target_list (list): 振り分けるリスト
        reorder_dicts (list): 振り分ける情報が入ったdictのlist
    """

    used_targets = []

    for order_dict in order_dicts:

        # このreorder_dictのメンバーか判定
        for target in target_list:

            if target in used_targets:
                continue

            # 振り分けメソッドがなければメンバーに入れる
            if not order_dict.get('func'):
                order_dict['members'].append(target)
                used_targets.append(target)

            # 振り分けメソッドがあれば戻り値がtargat_returnならメンバーにいれる
            elif order_dict['func'](target) == order_dict['targat_return']:
                order_dict['members'].append(target)
                used_targets.append(target)

        # メンバーの並び替え
        if 'members' in order_dict:

            # ソート用のkeyを求めるメソッドがあれば、得られるkeyを使ってsort
            sort_key_funcs = order_dict.get('sort_key_funcs')

            if sort_key_funcs:
                order_dict['members'].sort(key=lambda x: [func(x) for func in sort_key_funcs])

            else:
                order_dict['members'].sort()

        if 'members' in order_dict and 'order_dicts' in order_dict and order_dict['order_dicts']:
            __sort_into_order_dicts(order_dict['members'], order_dict['order_dicts'])


def get_list_from_order_dicts(order_dicts):
    """reorder_dictsから並び変わったリストを取得する

    Args:
        reorder_dicts (list): 振りわけが行われたorder_dicts

    Returns:
        list: 並び替え後のリスト
    """

    results = []

    if not order_dicts:
        return results

    for reorder_dict in order_dicts:
        if not reorder_dict.get('order_dicts') and reorder_dict.get('members'):
            # order_dictsがなければメンバーを取得
            results.extend(reorder_dict.get('members'))
        else:
            # order_dictsがあれば更に振り分けられているので、再帰
            results.extend(get_list_from_order_dicts(reorder_dict.get('order_dicts')))

    return results
