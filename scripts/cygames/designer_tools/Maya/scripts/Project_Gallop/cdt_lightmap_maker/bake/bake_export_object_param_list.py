# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass

__key_list = (
    link,
    transform_replace_key,
    transform_replace_value,
    material_replace_key,
    material_replace_value,
    texture_replace_key,
    texture_replace_value,
    export_item_enable,
    export_item_name,
    export_item_start_frame,
    export_item_end_frame,
) = list(range(0, 11))

__value_list = (
    ("Link", "message", None, None, None),
    ("TransformReplaceKey", "string", '', 'Transform Replace Key', None),
    ("TransformReplaceValue", "string", '', 'Transform Replace Value', None),
    ("MaterialReplaceKey", "string", '', 'Material Replace Key', None),
    ("MaterialReplaceValue", "string", '', 'Material Replace Value', None),
    ("TextureReplaceKey", "string", '', 'Texture Replace Key', None),
    ("TextureReplaceValue", "string", '', 'Texture Replace Value', None),
    ("ExportItemEnable", "bool", False, 'Export Enable', None),
    ("ExportItemName", "string", '', 'Export Name', None),
    ("ExportItemStartFrame", "int", -1, 'Start Frame', None),
    ("ExportItemEndFrame", "int", -1, 'End Frame', None),
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
