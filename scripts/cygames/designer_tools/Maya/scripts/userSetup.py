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
def AddMenu():
    import CyMenu
    CyMenu.UI()


def AddPaths():
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
        import CyAddMayaScriptPath
        try:
            # Python 2
            reload(CyAddMayaScriptPath)
        except NameError:
            try:
                # Python 3.4+
                from importlib import reload
                reload(CyAddMayaScriptPath)
            except Exception:
                pass
        CyAddMayaScriptPath.add(os.path.dirname(thisFilePath))
    except Exception as e:
        print(u"   Mayaスクリプトパスを追加 : 失敗！")
        print(e)

    # Mayaプラグインパスを追加
    try:
        pluginPaths = [
            r'C:\cygames\designer_tools\Maya\plug-ins',
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


def forceLoadMayaScannerPlugins():
    """MayaScannerPlugin群を強制ロード
    """

    mayaScannerPlugins = ["MayaScanner", "MayaScannerCB"]

    if forceLoadPlugins(mayaScannerPlugins):
        pass
        # コメントアウトすると、MayaScannerをOFFにしようとすると強制的にONになる処理が追加されます
        # cmds.pluginInfo(changedCommand=lambda x=mayaScannerPlugins: forceLoadPlugins(x))
    else:
        cmds.warning(u"MayaScanner(Seculity for Autodesk Maya)がインストールされていません。MayaScannerプラグインをインストールしてください")


def forceLoadPlugins(plugins):
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


# -------------------------------------------------
if __name__ == '__main__':

    # Maya起動後に実行
    maya.utils.executeDeferred(AddPaths)
    maya.utils.executeDeferred(AddMenu)
    maya.utils.executeDeferred(forceLoadMayaScannerPlugins)
