# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

# userSetup.pyでインポートしたモジュールはMaya全体で使用されるため、このモジュール内で使用しない場合でも記述しておく
import maya.utils
import maya.cmds as cmds
import maya.mel as mel

import sys
import os
import traceback


# -------------------------------------------------
# Maya起動後に実行する処理
def add_menu():
    import TkgMenu
    TkgMenu.UI()


def add_paths():
    # このファイルのパス
    thisFilePath = ""
    try:
        thisFilePath = __file__.replace("\\", "/")
    except NameError:
        tb = traceback.extract_tb(sys.exc_info()[2])
        thisFilePath = tb[0][0].replace("\\", "/")
    print(thisFilePath)

    try:
        # Mayaスクリプトパスを追加
        import TkgAddMayaScriptPath
        try:
            # Python 2
            reload(TkgAddMayaScriptPath)
        except NameError:
            try:
                # Python 3.4+
                from importlib import reload
                reload(TkgAddMayaScriptPath)
            except Exception:
                pass
        TkgAddMayaScriptPath.add(os.path.dirname(thisFilePath))
    except Exception as e:
        print(u"   Mayaスクリプトパスを追加 : 失敗！")
        print(e)

    # Mayaプラグインパスを追加
    try:
        pluginPaths = [
            r'C:\tkgpublic\designer_tools\Maya\plug-ins',
        ]

        if 'MAYA_PLUG_IN_PATH' in os.environ:
            os.environ['MAYA_PLUG_IN_PATH'] = ';'.join(
                ([os.environ['MAYA_PLUG_IN_PATH']] + pluginPaths)
            )
        else:
            os.environ['MAYA_PLUG_IN_PATH'] = ';'.join(pluginPaths)

    except Exception as e:
        print(u"   Mayaプラグインパスを追加 : 失敗！")
        print(e)


def force_load_maya_scanner_plugins():
    """MayaScannerPlugin群を強制ロード
    """

    mayaScannerPlugins = ["MayaScanner", "MayaScannerCB"]

    if force_load_plugins(mayaScannerPlugins):
        pass
        # コメントアウトすると、MayaScannerをOFFにしようとすると強制的にONになる処理が追加されます
        # cmds.pluginInfo(changedCommand=lambda x=mayaScannerPlugins: forceLoadPlugins(x))
    else:
        cmds.warning(u"MayaScanner(Seculity for Autodesk Maya)がインストールされていません。MayaScannerプラグインをインストールしてください")


def force_load_plugins(plugins):
    """該当のプラグインが読まれていない時、プラグインを強制ロードする
    """

    for plugin in plugins:

        if not cmds.pluginInfo(plugin, q=True, loaded=True):
            try:
                cmds.loadPlugin(plugin)
                cmds.pluginInfo(plugin, e=True, autoload=True)
            except RuntimeError:
                # プラグインがインストールされていない時にRuntimeErrorが発生する
                return False

    return True


def disable_move_acceleration():
    """移動の高速化設定を無効化する
    Maya2023/2024ではマウス操作で頂点移動を行う際、
    高速化設定が入っていると法線の再計算が正しく行われないバグ対応 (MAYA-131823 Move tool creates non-normalized normals)
    """
    NEED_FIX_VERSION_LIST = ['2023', '2024']
    current_maya_version = cmds.about(version=True)

    # この問題は、Maya2023, 2024で対応が必要（2025で修正予定）
    if current_maya_version not in NEED_FIX_VERSION_LIST:
        return

    # 高速化設定が有効となっている場合は無効化する
    if str(cmds.performanceOptions(q=True, regionOfEffect=True)) != 'True':
        # performanceOptions コマンドで、regionOfEffect の設定を 1 に変更します
        cmds.performanceOptions(regionOfEffect=1)

        # optionVar コマンドで、regionOfEffect の設定を 1 に変更し、userPrefs.mel に書き込みます (次回起動のMayaでも設定が残ります)
        cmds.optionVar(sv=('performanceSettingRegionOfEffect', '1'))


# -------------------------------------------------
if __name__ == '__main__':

    # Maya起動後に実行
    maya.utils.executeDeferred(add_paths)
    maya.utils.executeDeferred(add_menu)
    maya.utils.executeDeferred(force_load_maya_scanner_plugins)
    maya.utils.executeDeferred(disable_move_acceleration)
