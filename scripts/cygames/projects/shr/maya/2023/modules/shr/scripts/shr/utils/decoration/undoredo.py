# -*- coding: utf-8 -*-
u"""decorator"""

import traceback
from functools import wraps

import maya.cmds as cmds


import logging
# from mtku.maya.log import MtkDBLog


# logger = MtkDBLog(__name__)
logger = logging.getLogger(__name__)


def undo_redo(can_keep_selections=False):
    u"""Undo/Redoのdecorator

    :param can_keep_selections: 選択を保持するか
    :type can_keep_selections: bool
    """
    def _undo_redo(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            cmds.undoInfo(ock=True)
            try:
                if can_keep_selections:
                    result = _keep_selections_wrapper(func, *args, **kwargs)
                else:
                    result = func(*args, **kwargs)
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
            finally:
                cmds.undoInfo(cck=True)
                return result
        return wrapper
    return _undo_redo


def _keep_selections_wrapper(func, *args, **kwargs):
    u"""選択を保持"""
    selection = cmds.ls(sl=True)
    result = func(*args, **kwargs)
    if selection:
        cmds.select(selection)
    return result
