# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from importlib import reload
except Exception:
    pass

import sys

import maya.cmds as cmds

from PySide2 import QtWidgets


def main():
    """カラースペースを全部Rawにするツール

    """
    version = cmds.about(v=True)
    if int(version) < 2017:
        QtWidgets.QMessageBox.warning(None, '警告', 'Maya2017以降で実行してください')
        return

    # はい以外が選択された場合は実行しない
    result = QtWidgets.QMessageBox.question(None, '実行確認', 'すべてのカラースペースをRAWに変更しますか?(Enterキーで実行します)', (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No), QtWidgets.QMessageBox.Yes)
    if result != QtWidgets.QMessageBox.Yes:
        return

    modify_color_management()
    modify_tex_color_space()
    modify_imageplane_color_space()


def modify_color_management():
    """カラーマネジメントのカラースペースを全部Rawにする

    """
    main_rule = cmds.colorManagementFileRules(listRules=True)[0]
    cmds.colorManagementFileRules(main_rule, edit=True, colorSpace='Raw')

    if sys.version_info.major == 3:
        # OCIOの設定をMaya2019互換のものに変更
        cmds.colorManagementPrefs(e=True, configFilePath='<MAYA_RESOURCES>/OCIO-configs/Maya-legacy/config.ocio')

        # Maya2024のみで実行
        if str(cmds.about(api=True)).startswith('2024'):
            cmds.setAttr('hardwareRenderingGlobals.defaultLightIntensity', 1.0)

    color_management_pref_transform_names = cmds.colorManagementPrefs(q=True, viewTransformNames=True)

    # preferenceのカラースペースをRawに
    if sys.version_info.major == 2:
        cmds.colorManagementPrefs(e=True, viewTransformName='Raw')
    else:
        # for Maya 2022-
        if 'Raw (legacy)' in color_management_pref_transform_names:
            cmds.colorManagementPrefs(e=True, viewTransformName='Raw (legacy)')
        elif 'Raw (sRGB)' in color_management_pref_transform_names:
            cmds.colorManagementPrefs(e=True, viewTransformName='Raw (sRGB)')
        else:
            cmds.error('カラーモードRawが設定できませんでした')
            return

    # modelPanelを取得してビューパイプラインをRawに
    model_panel_list = cmds.getPanel(type='modelPanel')

    for model_panel in model_panel_list:
        if sys.version_info.major == 2:
            cmds.modelEditor(model_panel, e=True, viewTransformName='Raw')
        else:
            # for Maya 2022-
            if 'Raw (legacy)' in color_management_pref_transform_names:
                cmds.modelEditor(model_panel, e=True, viewTransformName='Raw (legacy)')
            elif 'Raw (sRGB)' in color_management_pref_transform_names:
                cmds.modelEditor(model_panel, e=True, viewTransformName='Raw (sRGB)')
            else:
                cmds.error('カラーモードRawが設定できませんでした')
                return


def modify_tex_color_space():
    """テクスチャのカラースペースを全部Rawにする

    """
    file_node_list = cmds.ls(typ='file')

    if not file_node_list:
        return

    for node in file_node_list:
        cmds.setAttr(str(node) + '.colorSpace', 'Raw', type='string')


def modify_imageplane_color_space():
    """イメージプレーンのカラースペースをRAWにする
    """
    rule_list = cmds.colorManagementFileRules(listRules=True)
    if 'default' in rule_list:
        cmds.colorManagementFileRules('Default', edit=True, colorSpace='Raw')

        # 保存することで影響を永続化できる
        cmds.colorManagementFileRules(save=True)

    # 既存部分に関しては手動で修正しなければならないので合わせる
    imageplane_list = cmds.ls(typ='imagePlane')
    if not imageplane_list:
        return

    for imageplane in imageplane_list:
        cmds.setAttr(str(imageplane) + '.colorSpace', 'Raw', type='string')
