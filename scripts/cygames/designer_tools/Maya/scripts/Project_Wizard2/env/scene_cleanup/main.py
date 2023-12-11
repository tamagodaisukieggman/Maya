# -*- coding: utf-8 -*-

import maya.cmds as cmds


def delte_unknown_plugins():
    u"""
    現在開いているmayaシーンのunknownプラグインを削除します。
    :return: bool. Falseならunknownノード・プラグインがあったということ
    """
    # unknownPluginをリスト
    initial_unknown_plugins = cmds.unknownPlugin(q=True, list=True)
    unknown_plugins = []
    could_not_removed = []
    if initial_unknown_plugins:
        for plugin in initial_unknown_plugins:
            # ロードできているのにUnknownPluginとしてリストされるものがあるのでダブルチェック
            if cmds.pluginInfo(plugin, q=True, loaded=True):
                continue
            else:
                unknown_plugins.append(plugin)
            try:
                print(u"Unknownプラグインの削除: " + plugin)
                cmds.unknownPlugin(plugin, remove=True)
            except Exception as ex:
                print(ex)
                cmds.warning(u"Unknownプラグインが削除できませんでした: " + plugin)
                could_not_removed.append(plugin)
    if unknown_plugins:
        if not could_not_removed:
            user_choice = cmds.confirmDialog(title='Confirm',
                                             message='Unknownプラグインを削除しました\n' +
                                             'シーンを保存しますか?',
                                             button=['保存', '保存しない'],
                                             defaultButton='保存しない',
                                             cancelButton='保存しない',
                                             dismissString='保存しない')
            if user_choice == '保存':
                try:
                    cmds.file(modified=True)  # シーンからプラグインが削除されてもMayaはシーンに変更があったと認識しないのでフラグ変更
                    current_path = cmds.file(q=True, sn=True)
                    cmds.file(rename=cmds.encodeString(current_path))
                    cmds.file(save=True, uiConfiguration=cmds.optionVar(q="useSaveScenePanelConfig"))
                except Exception as ex:
                    cmds.warning(ex)
        else:
            cmds.confirmDialog(title='Info',
                               message='Unknownプラグインがありましたが上手く削除できませんでした',
                               button=['OK'])
        return False
    cmds.confirmDialog(title='Info',
                       message='Unknownプラグインはありませんでした',
                       button=['OK'])
    return True # unknownノード・プラグインがなかったという意味

