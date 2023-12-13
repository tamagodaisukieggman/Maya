# -*- coding: utf-8 -*-
"""パネル回りの機能"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function


from maya import cmds


class ModelPanelSelector(object):
    """Maya用のモデルパネルセレクター

    現在のアクティブのモデルパネル取得などの機能を提供
    """
    pass


def get_camera_from_focus_model_panel():
    model_panel = get_focus_model_panel()
    return cmds.modelPanel(model_panel, query=True, camera=True)


def get_focus_panel():
    """フォーカスしているPanelを取得する

    :return: パネルリスト
    :rtype: list[str]
    """
    return cmds.getPanel(withFocus=True)


def get_focus_model_panel():
    """フォーカスしてるモデルパネルを取得する

    :return: モデルパネル名
    :rtype: str
    """
    focus_panel = get_focus_panel()

    panel_list = cmds.getPanel(visiblePanels=True)
    model_panel_list = [_ for _ in panel_list if cmds.modelPanel(_, exists=True)]

    for model_panel in model_panel_list:
        if focus_panel == model_panel:
            return focus_panel

    return model_panel_list[0]


def get_camera_from_model_panel(panel_name):
    return cmds.modelPanel(panel_name, query=True, camera=True)


def is_active_panel(target_panel_name):
    """パネルが表示されているか

    :param target_panel_name: 件tの宇すｒ
    :type target_panel_name: [type]
    :return: [description]
    :rtype: [type]
    """
    for panel in cmds.getPanel(visiblePanels=True):
        if panel == target_panel_name:
            return True

    return False
