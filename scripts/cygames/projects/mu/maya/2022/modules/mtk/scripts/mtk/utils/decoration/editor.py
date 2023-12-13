# -*- coding: utf-8 -*-
u"""decorator"""
from functools import wraps

import maya.cmds as cmds
import maya.mel as mel

import logging
# from mtku.maya.log import MtkDBLog


# logger = MtkDBLog(__name__)
logger = logging.getLogger(__name__)


def hide_uv_editor(func):
    u"""実行中UVテクスチャエディタを非表示にするdecorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        window_list = cmds.lsUI(windows=True)
        is_uv_window = False
        for window in window_list:
            if window == "polyTexturePlacementPanel1Window":
                is_uv_window = True
        if is_uv_window:
            cmds.deleteUI("polyTexturePlacementPanel1Window")
        result = func(*args, **kwargs)
        if is_uv_window:
            mel.eval("TextureViewWindow;")
        return result
    return wrapper


def hide_script_editor(func):
    u"""実行中スクリプトエディタを非表示にするdecorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        window_list = cmds.lsUI(windows=True)
        is_uv_window = False
        for window in window_list:
            if window == "scriptEditorPanel1Window":
                is_uv_window = True
        if is_uv_window:
            cmds.deleteUI("scriptEditorPanel1Window")
        result = func(*args, **kwargs)
        if is_uv_window:
            mel.eval("ScriptEditor;")
        return result
    return wrapper
