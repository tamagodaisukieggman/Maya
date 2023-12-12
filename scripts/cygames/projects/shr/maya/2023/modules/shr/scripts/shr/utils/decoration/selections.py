# -*- coding: utf-8 -*-
u"""decorator"""
from functools import wraps

import maya.cmds as cmds

import logging
# from mtku.maya.log import MtkDBLog


# logger = MtkDBLog(__name__)
logger = logging.getLogger(__name__)

def keep_selections(func):
    u"""選択を保持するdecorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return _keep_selections_wrapper(func, *args, **kwargs)
    return wrapper


def _keep_selections_wrapper(func, *args, **kwargs):
    u"""選択を保持"""
    selection = cmds.ls(sl=True)
    result = func(*args, **kwargs)
    if selection:
        cmds.select(selection, ne=True)
    return result
