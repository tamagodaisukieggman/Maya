# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass

__material_reset_type_list = (
    material_reset_original,
    material_reset_bake_without_lightmap,
    material_reset_bake_with_lightmap,
    material_reset_bake_with_lightmap_and_calc_vertex_color,
) = list(range(0, 4))

__bake_scene_setting_type_list = (
    bake_scene_setting_all,
    bake_scene_setting_current,
) = list(range(0, 2))

__bake_scene_group_type_list = (
    bake_scene_group_all,
    bake_scene_group_current,
) = list(range(0, 2))

__bake_quality_type_list = (
    bake_quality_product,
    bake_quality_test,
) = list(range(0, 2))

__colorset_type_list = (
    colorset_common_multiply,
    colorset_common_add,
    colorset_common_overlay,
    colorset_common_alpha,
    colorset_common_gray,
    colorset_multiply,
    colorset_add,
    colorset_overlay,
    colorset_result,
) = list(range(0, 9))

__vertex_blend_type_list = (
    vertex_blend_normal,
    vertex_blend_lightmap,
) = list(range(0, 2))

__main_tab_key_list = (
    main_tab_common_setting,
    main_tab_bake_setting,
    main_tab_bake_group,
) = list(range(0, 3))

main_tab_label_list = [
    '共通設定',
    'ベイク設定',
    'グループ設定'
]

__setting_tab_key_list = (
    setting_tab_export,
    setting_tab_object,
    setting_tab_bake,
) = list(range(0, 3))

setting_tab_label_list = [
    '出力設定',
    'オブジェクト設定',
    'ベイク設定'
]

__group_tab_key_list = (
    group_tab_object,
    group_tab_bake,
) = list(range(0, 2))

group_tab_label_list = [
    'オブジェクト設定',
    'ベイク設定'
]

temp_colorset = "____temp_bake_colorset"

temp_export_colorset = "____temp_export_colorset_"

inactive_bg_color = (0.1, 0.1, 0.1)

setting_bg_color = (0.4, 0.6, 0.7)

group_bg_color = (0.7, 0.6, 0.4)

bg_safe_color0 = (0.5, 0.5, 0.6)
bg_safe_color1 = (0.5, 0.5, 0.8)

bg_warn_color0 = (0.6, 0.5, 0.5)
bg_warn_color1 = (0.8, 0.5, 0.5)

__key_list = (
    current_setting_index,
    current_group_index,
) = list(range(0, 2))

__value_list = (
    ("CurrentSettingIndex", "int", 0, '', None),
    ("CurrentGroupIndex", "int", 0, '', None),
)


def get_name(key):

    return __value_list[key][0]


def get_type(key):

    return __value_list[key][1]


def get_value(key):
    return __value_list[key][2]


def get_ui_label(key):

    return __value_list[key][3]


def get_ui_type(key):

    return __value_list[key][4]


def get_main_tab_label(key):

    return __main_tab_value_list[key][0]


def get_setting_tab_label(key):

    return __setting_tab_value_list[key][0]


def get_group_tab_label(key):

    return __group_tab_value_list[key][0]
