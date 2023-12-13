# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import re

import maya.cmds as cmds


# ==================================================
def get_short_name(name):
    """
    ショート名取得

    :param name: 対象となる名前
    """

    if not name:
        return name

    if name.find('|') == -1:
        return name

    return name.split('|')[-1]


# ==================================================
def get_long_name(name, sub_filter=None):
    """
    ロング名取得

    :param name: 対象となる名前
    :param sub_filter: 複数対象となった場合のフィルタ

    :return: ロング名 ※取得できない場合はnameを返します
    """

    if not name:
        return name

    long_name_list = cmds.ls(name, l=True)

    if not long_name_list:
        return name

    if len(long_name_list) == 1:
        return long_name_list[0]

    if not sub_filter:
        return long_name_list[0]

    re_obj = re.compile(sub_filter)

    for long_name in long_name_list:

        if re_obj.search(long_name):
            return long_name

    return long_name_list[0]
