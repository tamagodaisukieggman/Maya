# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass

__key_list = (
    index,
    name,
    bake_type,
    material_name,
    texture_name,
    colorset_name,
    group_link,
    lock,
    visible_link,
) = list(range(0, 9))

__value_list = (
    ("Index", "int", 0, None, None),
    ("Name", "string", "", "Name", None),
    ("BakeType", "list", "Texture", "Bake Type",
     ("radio", ("Texture", "Vertex", "None"))),
    ("MaterialName", "string", "", "Material Name", None),
    ("TextureName", "string", "", "Texture Name", None),
    ("ColorSetName", "string", "", "Color Set Name", None),
    ("GroupLink", "message", None, None, None),
    ("Lock", "bool", False, None, None),
    ("VisibleLink", "message", None, None, None),
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
