# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass

__key_list = (
    group_link,
    lock,
) = list(range(0, 2))

__value_list = (
    ("GroupLink", "message", None, None, None),
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
