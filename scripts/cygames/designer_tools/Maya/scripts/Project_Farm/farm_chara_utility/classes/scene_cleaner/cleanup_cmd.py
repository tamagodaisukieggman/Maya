# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

"""
gallop の glp_scene_cleanup/cleanup_cmd をそのまま移植してきたもの
"""

import maya.cmds as cmds


def delete_unknown_nodes_and_plugins():
    """現在開いているmayaシーンのunknownノードとプラグインを削除して上書き保存する

    Returns:
        bool: unknownノード並びにunknownプラグインの削除を行ったかどうか
    """

    current_path = cmds.file(q=True, sn=True)
    if not cmds.file(q=True, sn=True):
        cmds.warning('シーンを保存してから実行して下さい')
        return False

    # unknownノードの削除
    unknown_nodes = cmds.ls(type='unknown')
    if unknown_nodes:
        for node in unknown_nodes:
            try:
                cmds.delete(node)
            except Exception:
                # delete出来ないパターンがある（lockされている等）
                print('can`t delete unknown node: ' + node)

    # unknownプラグインの削除
    initial_unknown_plugins = cmds.unknownPlugin(q=True, list=True)
    unknown_plugins = []
    if initial_unknown_plugins:

        for plugin in initial_unknown_plugins:

            # ロードできているのにUnknownPluginとしてリストされるものがあるのでダブルチェック
            if cmds.pluginInfo(plugin, q=True, loaded=True):
                continue
            else:
                unknown_plugins.append(plugin)

            try:
                cmds.unknownPlugin(plugin, remove=True)
            except Exception:
                cmds.warning('can`t delete unknown plugin: ' + plugin)

    if unknown_nodes or unknown_plugins:

        cmds.file(modified=True)
        cmds.file(rename=cmds.encodeString(current_path))
        cmds.file(save=True, uiConfiguration=cmds.optionVar(q='useSaveScenePanelConfig'))
        cmds.warning('unknownノードとプラグインを削除しました: {}'.format(current_path))

        return True

    return False


def delete_vaccine():
    """vaccine.pyとuserSetup.pyがDocuments/maya/scriptsに作られる不正なスクリプトをシーンを削除

    Returns:
        bool: 処理を実行したかどうか
    """

    current_path = cmds.file(q=True, sn=True)
    if not current_path:
        cmds.warning('シーンを保存してから実行して下さい')
        return False

    found_vaccine_file = False
    if cmds.ls('vaccine_gene') or cmds.ls('breed_gene'):
        found_vaccine_file = True

    if found_vaccine_file:

        cmds.delete(cmds.ls('vaccine_gene'))
        cmds.delete(cmds.ls('breed_gene'))

        cmds.file(modified=True)
        cmds.file(rename=cmds.encodeString(current_path))
        cmds.file(save=True, uiConfiguration=cmds.optionVar(q='useSaveScenePanelConfig'))
        cmds.warning('不正なスクリプトをシーンから削除しました: {}'.format(current_path))

        return True

    return False


def reset_ui_callback():
    """「CgAbBlastPanelOptChangeCallback」等のuiConfigurationNodeに付随しているCallback関数を削除する

    削除するためにシーンを一度scriptNodeを読み込まない設定で読み込み直し保存する

    Returns:
        bool: 処理を実行したかどうか
    """

    current_path = cmds.file(q=True, sn=True)
    if not current_path:
        cmds.warning('シーンを保存してから実行して下さい')
        return False

    found_editor_changed_flag = False

    if cmds.optionVar(q='fileExecuteSN'):
        panels = cmds.getPanel(type='modelPanel')
        if panels:
            for pnl in panels:
                modelEditorName = cmds.modelPanel(pnl, q=True, me=True)
                if cmds.modelEditor(modelEditorName, q=True, editorChanged=True):
                    found_editor_changed_flag = True
                    break

    if found_editor_changed_flag:

        cmds.file(modified=True)
        cmds.file(rename=cmds.encodeString(current_path))
        cmds.file(save=True, uiConfiguration=False)
        cmds.warning('UI関連のCallback(uiConfiguration)をリセットしました: {}'.format(current_path))

        return True

    return False


def fix_initial_node():
    """
    通常lambert1に接続されているinitialShadingGroupとinitialParticleSEの状態が正常かチェックし、問題があれば修復する

    Returns:
        bool: 処理を実行したかどうか
    """

    current_path = cmds.file(q=True, sn=True)
    if not current_path:
        cmds.warning('シーンを保存してから実行して下さい')
        return False

    is_error = False
    for target_node in ['initialShadingGroup', 'initialParticleSE']:

        if cmds.getAttr('{}.ro'.format(target_node)) is False:
            is_error = True
            break

        if cmds.lockNode(target_node, q=True, lockUnpublished=True)[0]:
            is_error = True
            break

        if cmds.lockNode(target_node, q=True, lock=True) is False:
            is_error = True
            break

    if is_error:
        # 実行順が重要
        try:
            cmds.lockNode('initialShadingGroup', lockUnpublished=False)
            cmds.lockNode('initialShadingGroup', lock=False)
            cmds.lockNode('initialParticleSE', lockUnpublished=False)
            cmds.lockNode('initialParticleSE', lock=False)
            cmds.setAttr('initialShadingGroup.ro', True)
            cmds.setAttr('initialParticleSE.ro', True)
            cmds.file(save=True, uiConfiguration=cmds.optionVar(q='useSaveScenePanelConfig'))
            cmds.warning('initialShadingGroupとinitialParticleSEを正常な状態に修復しました: {}'.format(current_path))
        except Exception:
            cmds.warning('fix_initial_nodeを実行出来ませんでした: {}'.format(current_path))

    return is_error


def suggest_maya_scanner():
    """Maya Scannerが未インストールまたはOFFの場合に警告を行う
    """

    if not cmds.pluginInfo('MayaScanner', q=True, registered=True):
        cmds.confirmDialog(
            title='警告',
            message='「Security Tools for Autodesk Maya」がインストールされていません',
            button=['OK']
        )

    else:

        target_plugin_list = ['MayaScanner', 'MayaScannerCB']
        for target_plugin in target_plugin_list:
            if not cmds.pluginInfo(target_plugin, q=True, loaded=True):
                cmds.confirmDialog(
                    title='警告',
                    message='Window > Settings/Preferences > Plug-in Manager で MayaScanner と MayaScannerCB をONにしてください',
                    button=['OK']
                )
