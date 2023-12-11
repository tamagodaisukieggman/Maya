# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds


def get_short_name(long_name):
    """ショートネーム取得
    """
    return __get_short_name(long_name)


def is_joint(long_name):
    """jointノードか
    """
    return True if cmds.objectType(long_name) == 'joint' else False


def is_locator(long_name):
    """locatorノード（の親のトランスフォーム）か
    """
    return True if cmds.listRelatives(long_name, s=True, ni=True, f=True, type='locator') else False


def is_mesh(long_name):
    """meshノード（の親のトランスフォーム）か
    """
    return True if cmds.listRelatives(long_name, s=True, ni=True, f=True, type='mesh') else False


def __get_short_name(long_name):
    return long_name.split('|')[-1].split(':')[-1]

