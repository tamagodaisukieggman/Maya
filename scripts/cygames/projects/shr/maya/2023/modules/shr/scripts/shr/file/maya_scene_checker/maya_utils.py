# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial
from maya import cmds
import maya.mel
import webbrowser
from . import settings


def open_help_site():
    _web_site = settings.load_config('WEB_SITE')
    webbrowser.open(_web_site)

def attach_job(object_name="", job=None):
    """GUI にスクリプトジョブを付ける

    Args:
        object_name (str): GUI Object name
        job (function):
    """
    if not object_name or not job:
        return
    cmds.scriptJob(parent=object_name, event=("SceneOpened", partial(job)))
    cmds.scriptJob(parent=object_name, event=("NewSceneOpened", partial(job)))

def iterUpNode(node):
    """ルートノード取得

    Args:
        node (str): maya transform node

    Yields:
        [str]: maya transform node
    """
    parent = cmds.listRelatives(node, parent=True, fullPath=True)
    if parent:
        yield parent[0]
        for p in iterUpNode(parent):
            yield p


def delete_poly_bind_data():
    """poly bind というヒストリを削除する

    Returns:
        [list]: maya node history
    """
    _poly_bind_data = cmds.ls(type="polyBlindData")
    _poly_bind_data_template = cmds.ls(type="blindDataTemplate")
    if _poly_bind_data_template:
        _poly_bind_data.extend(_poly_bind_data_template)
        if _poly_bind_data:
            cmds.delete(_poly_bind_data)
            print(
                f'Delete Poly BindDatas -- [ {", ".join(_poly_bind_data)} ] ')
    return _poly_bind_data


def fit_view():
    """Maya ビューポートをフィット
    """
    _command = 'FrameSelectedWithoutChildren; '
    _command += 'fitPanel -selectedNoChildren;'
    try:
        maya.mel.eval(_command)
    except:
        pass


def show_hidden_nodes(visible_node=""):
    """ノードの表示
    引数ノードのルートをたどって表示をさせる

    Args:
        visible_node (str): maya dag node
    """
    try:
        cmds.setAttr("{}.visibility".format(visible_node), 1)
    except:
        pass

    for n in iterUpNode(visible_node):
        try:
            cmds.setAttr("{}.visibility".format(n), 1)
        except:
            pass

    shape = cmds.listRelatives(visible_node, shapes=True, fullPath=True)
    if shape:
        try:
            cmds.setAttr("{}.visibility".format(shape[0]), 1)
        except:
            pass


def fit_outliner():
    """選択しているノードをアウトライナでフィットさせる
    """
    _outliners = [x for x in cmds.getPanel(type="outlinerPanel")
                  if x in cmds.getPanel(visiblePanels=True)]

    if _outliners:
        [cmds.outlinerEditor(x, edit=True, showSelected=True)
         for x in _outliners]


def select_target(targets=[], selection_flag=True, focus_flag=True, focus_outliner_flag=True):
    """ターゲットの選択
    表示状態を変更、ビューとアウトライナをフィットさせる

    Args:
        targets (list): maya dag nodes
    """
    if not targets:
        return

    target = targets[0]
    if not cmds.objExists(target):
        return

    if selection_flag:
        show_hidden_nodes(target)
        cmds.select(targets, replace=True, noExpand=True)
    if focus_flag:
        fit_view()
    if focus_outliner_flag:
        fit_outliner()
