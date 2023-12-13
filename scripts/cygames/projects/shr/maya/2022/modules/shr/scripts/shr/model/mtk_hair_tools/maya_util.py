# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import OrderedDict
from distutils.util import strtobool

import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import maya.cmds as cmds
import maya.mel
from mtk.utils import getCurrentSceneFilePath

from . import TOOL_NAME

from . import FILE_IMFO_DATA


def keep_selections(func):
    u"""選択を保持するdecorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return _keep_selections_wrapper(func, *args, **kwargs)
    return wrapper


def _keep_selections_wrapper(func, *args, **kwargs):
    u"""選択を保持"""
    selection = cmds.ls(sl=True, type="tansform")
    result = func(*args, **kwargs)
    if selection:
        cmds.select(selection, ne=True)
    else:
        cmds.select(cl=True)
    return result


def get_scene_name():
    """シーン名を取得
    cmds で取得できないシーンがあったのでOpenMayaでも取得を試みる
    ただし、OpenMayaの場合は開いていなくても文字列は空にならないので
    そのための対処
    """
    scene_name = getCurrentSceneFilePath()
    if not scene_name:
        scene_name = om.MFileIO.currentFile()

    if len(scene_name.split(".")) < 2:
        scene_name = ""

    return scene_name


def get_parents(node=""):
    """ルートノード取得

    Args:
        node (str)): Maya ノードの文字列

    Yields:
        [type]: [description]
    """

    if isinstance(node, list):
        node = node[0]

    if not node:
        return

    parent = cmds.listRelatives(node, parent=True, fullPath=True)
    if parent:
        yield parent[0]
        for p in get_parents(parent):
            yield p


def get_file_infos():
    file_info_datas = OrderedDict()
    for info in FILE_IMFO_DATA:
        _ = cmds.fileInfo("{}_{}".format(TOOL_NAME, info), q=True)
        if _:
            _ = _[0]
            _data_type = info.rsplit("_", 1)[-1]
            if _data_type == "value":
                file_info_datas[info] = int(_)
            elif _data_type == "check":
                file_info_datas[info] = _
            elif _data_type == "fvalue":
                file_info_datas[info] = float(_)
            elif _data_type == "text":
                file_info_datas[info] = _
            elif _data_type == "txint":
                file_info_datas[info] = _
        else:
            file_info_datas[info] = None
    return file_info_datas
