# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from .. import utility as _base_utility

g_select_list = None


# ==================================================
def save_selection():
    """
    現在の選択を保存
    """

    global g_select_list

    g_select_list = cmds.ls(sl=True, l=True)


# ==================================================
def load_selection():
    """
    現在の選択を読み出し
    """

    select_list = g_select_list
    print(select_list)

    if not select_list:
        select_list = []

    fix_select_list = []

    for select in select_list:

        if not _base_utility.node.exists(select):
            continue

        fix_select_list.append(select)

    cmds.select(fix_select_list, r=True)
