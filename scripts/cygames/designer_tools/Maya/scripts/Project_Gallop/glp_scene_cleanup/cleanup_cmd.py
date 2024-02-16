# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import re

import maya.cmds as cmds
import maya.mel as mel


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

    # _UNKNOWN_REF_NODE_の削除
    unknown_ref_nodes = cmds.ls('*_UNKNOWN_REF_NODE_*')
    if unknown_ref_nodes:
        for node in unknown_ref_nodes:
            try:
                cmds.delete(node)
            except Exception:
                print('can`t delete unknown ref node: ' + node)

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

    if unknown_nodes or unknown_ref_nodes or unknown_plugins:

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


def fix_irregular_lock_node():
    """
    通常lambert1に接続されているinitialShadingGroupとinitialParticleSEの状態が正常かチェックし、問題があれば修復する

    Returns:
        bool: 処理を実行したかどうか
    """

    current_path = cmds.file(q=True, sn=True)
    if not current_path:
        cmds.warning('シーンを保存してから実行して下さい')
        return False

    # initialShadingGroup系
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

    # defaultTextureList系
    default_textures = cmds.ls('defaultTextureList*')
    if default_textures:
        for texture in default_textures:
            cmds.lockNode(texture, l=False, lockUnpublished=False)
            cmds.warning('defaultTextureListのロックを解除しました: {}'.format(current_path))

    return True


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


def has_reference_unknown_nodes_or_plugins():
    """unknownノード、プラグインがリファレンスシーンに含まれるかを取得する

    Returns:
        bool: unknownノード、プラグインがリファレンスシーンに含まれるか
    """

    unknown_nodes = get_reference_unknown_nodes()
    unknown_plugins = get_reference_unknown_plugins()

    if unknown_nodes or unknown_plugins:
        return True

    return False


def get_reference_unknown_nodes():
    """リファレンスシーンに含まれるunknownノードを取得する

    Returns:
        list[str]: リファレンスシーンに含まれるunknownノード
    """

    return [node for node in cmds.ls(type='unknown') if cmds.referenceQuery(node, inr=True)]


def get_reference_unknown_plugins():
    """リファレンスシーンに含まれるunknownプラグインを取得する

    Returns:
        list[str]: リファレンスシーンに含まれるunknownプラグイン
    """

    reference_unknown_plugins = []

    initial_unknown_plugins = cmds.unknownPlugin(q=True, l=True)
    unknown_plugins = []
    if initial_unknown_plugins:

        for plugin in initial_unknown_plugins:

            # ロードできているのにUnknownPluginとしてリストされるものがあるのでダブルチェック
            if cmds.pluginInfo(plugin, q=True, loaded=True):
                continue
            else:
                unknown_plugins.append(plugin)

    if not unknown_plugins:
        return reference_unknown_plugins

    ref_nodes = cmds.ls(rf=True)

    for ref_node in ref_nodes:
        # cmds.referenceQuery(ref_node, il=True)で
        # Reference node '***' is not associated with a reference file.
        # というエラーが出る.これはcmds.referenceQuery(ref_node, inr=True)などでも判定しきれないためtry/exceptする.
        try:
            if cmds.referenceQuery(ref_node, il=True):
                ref_path = cmds.referenceQuery(ref_node, f=True)
                included_plugins = get_included_plugins(ref_path, unknown_plugins)
                reference_unknown_plugins = list(set(reference_unknown_plugins + included_plugins))
        except Exception:
            print('{} is not associated with a reference file'.format(ref_node))

    return reference_unknown_plugins


def get_included_plugins(path, plugins):
    """シーンに含まれている指定プラグインを返す

    Args:
        path (str): シーンパス
        plugins (list[str]): チェックするプラグイン名のリスト

    Returns:
        list[str]: シーンに含まれるプラグイン
    """

    included_plugins = []

    try:
        with open(path) as f:
            data = f.read()
            for plugin in plugins:
                if re.search('requires.*{}'.format(plugin), data):
                    included_plugins.append(plugin)
    except Exception:
        pass

    return included_plugins


def delete_script_nodes():
    """規定以外のScriptノードを全て削除する

    現在の規定されているScriptノードは以下の通り
    - 'sceneConfigurationScriptNode'
    - 'uiConfigurationScriptNode'
    - 'MayaMelUIConfigurationFile'
    - '_dwpicker_data'
    - 'GLP_SCRIPT_'
    """

    clear_flag = False

    ignore_target_script_nodes = [
        'sceneConfigurationScriptNode',
        'uiConfigurationScriptNode',
        'MayaMelUIConfigurationFile',
        '_dwpicker_data',
        'GLP_SCRIPT_'
    ]

    script_nodes = cmds.ls(typ="script")
    for script_node in script_nodes:
        if (any([re.search(x, script_node) for x in ignore_target_script_nodes])):
            continue

        try:
            cmds.delete(script_node)
            clear_flag = True
        except Exception:
            pass

    return clear_flag


def delete_outliner_panel_select_command():
    """uiConfigurationNode内に設定されている-selectCommandの設定をクリアする

    cmds.outlinerEditor("outlinerPanel1", e=True, selectCommand="")だと
    原因不明のsyntax errorが発生するので、mel.evalで実行
    """

    # cmdsコマンドだとsyntax errorが発生するのでmel.evalで実行
    mel.eval('outlinerEditor -edit -selectCommand "" "outlinerPanel1";')

    return True
