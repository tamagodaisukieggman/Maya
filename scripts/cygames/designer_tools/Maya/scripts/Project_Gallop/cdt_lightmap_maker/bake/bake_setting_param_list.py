# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass

__key_list = (
    index,
    name,
    lock,
    link,
    visible_link,
    export_link,
) = list(range(0, 6))

__value_list = (
    ("Index", "int", 0, None, None),
    ("Name", "string", "", "Name", None),
    ("Lock", "bool", True, None, None),
    ("Link", "message", None, None, None),
    ("VisibleLink", "message", None, None, None),
    ("ExportLink", "message", None, None, None),
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
