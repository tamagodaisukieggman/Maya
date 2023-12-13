# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import maya.cmds as cmds

from . import TITLE
from . import gui_util


CURRENT_HOUDINI_VERSION = "18.5.532"
# CURRENT_HOUDINI_VERSION = "18.5.696"
HOUDINI = "Houdini"
BIN = "bin"
HOUDINI_PATH = f'C:/Program Files/Side Effects Software/{HOUDINI} {CURRENT_HOUDINI_VERSION}/{BIN}'

HOUDINI_PLUGIN_PATH = "Z:/mtk/tools/maya/2022/modules/houdini_engine/plug-ins"
# HOUDINI_PLUGIN_PATH = "C:/Program Files/Side Effects Software/Houdini 18.5.696/engine/maya/maya2018/plug-ins"

HOUDINI_ENGINE_PLUGIN_NAME = "houdiniEngine"
HOUDINI_ENGINE_PLUGIN_EXT = ".mll"

HDA_PATH = "Z:/mtk/tools/maya/share/hda/develop"

_SessionType = {"houdiniEngineSessionType": 2}
_SessionPipeCustom = {"houdiniEngineSessionPipeCustom": 0}
_ThriftPipe = {"houdiniEngineThriftPipe": "hapi"}

_SafeModeAllowedlistPaths = "SafeModeAllowedlistPaths"
_TrustCenterPathAction = "TrustCenterPathAction"
_AsynchronousMode = "houdiniEngineAsynchronousMode"

# ENV_PATHS = {
#     "PATH": r"C:\Program Files\Side Effects Software\Houdini 18.5.532\bin",
#     "MAYA_PLUG_IN_PATH": r"Z:\mtk\tools\maya\2022\modules\houdini_engine\plug-ins",
# }


ENV_PATHS = {
    "PATH": HOUDINI_PATH,
    "MAYA_PLUG_IN_PATH": HOUDINI_PLUGIN_PATH,
}


def add_path(env_paths={}):
    if not env_paths:
        env_paths = ENV_PATHS

    for env, env_path in env_paths.items():
        path_string = os.environ.get(env, None)

        if not path_string:
            continue

        _path_exists = env_path in path_string.split(";")
        print(f'[ ENV: {env} ] [ ENV PATH: {env_path} ] [ EXISTS: {_path_exists} ]')

        if not _path_exists:
            os.environ[env] = f'{path_string};{env_path}'

        path_string = os.environ.get(env, None)
        _path_exists = env_path in path_string.split(";")
        print(f'[ ENV: {env} ] [ ENV PATH: {env_path} ] [ EXISTS: {_path_exists} ]')


def set_default_trust():
    """untrust location のデフォルト動作を変更
    ただしこれを行ってもダイアログは表示される
    """
    if cmds.optionVar(q=_TrustCenterPathAction) != 2:
        cmds.optionVar(intValue=[_TrustCenterPathAction, 2])

def set_trust_path():
    """Z ドライブのHoudiniEngine をプラグインとして登録できるように
    trust directory に登録
    """
    paths = cmds.optionVar(q=_SafeModeAllowedlistPaths)
    if not paths:
        cmds.optionVar(stringValueAppend=[_SafeModeAllowedlistPaths, HOUDINI_PLUGIN_PATH])
    elif HOUDINI_PLUGIN_PATH not in paths:
        cmds.optionVar(stringValueAppend=[_SafeModeAllowedlistPaths, HOUDINI_PLUGIN_PATH])

def set_option_var():
    """HoudiniEngine 用のoptionVar 設定
    """
    if cmds.optionVar(q="houdiniEngineSessionType") != 2:
        cmds.optionVar(intValue=["houdiniEngineSessionType", 2])
    if cmds.optionVar(q="houdiniEngineSessionPipeCustom") != 0:
        cmds.optionVar(intValue=["houdiniEngineSessionPipeCustom", 0])
    if cmds.optionVar(q="houdiniEngineThriftPipe") != "hapi":
        cmds.optionVar(stringValue=["houdiniEngineThriftPipe", "hapi"])
    if cmds.optionVar(q="houdiniEngineAsynchronousMode") != 0:
        cmds.optionVar(intValue=["houdiniEngineAsynchronousMode", 0])

def plugin_load_check():
    """HoudiniEngine がすでに読み込まれているか確認

    Returns:
        [bool]: 読み込まれているか否か
    """
    _load_flag = HOUDINI_ENGINE_PLUGIN_NAME in cmds.pluginInfo(query=True, listPlugins=True)
    return _load_flag

def plugin_path_check():
    """読み込まれているHoudiniEngine のパスを確認

    Returns:
        [str]: 読まれているプラグインのパス
    """
    _plugin_path = cmds.pluginInfo(HOUDINI_ENGINE_PLUGIN_NAME,
                                    q=True, path=True).replace(os.sep, '/')
    return _plugin_path

def plugin_version_check():
    """houdiniEngine のバージョン確認

    Returns:
        [type]: [description]
    """
    _current_version = cmds.houdiniEngine(bhv=True)
    return _current_version

def set_z_drive_plugin():

    _flag = True
    _plugin_path = os.path.join(HOUDINI_PLUGIN_PATH,
                HOUDINI_ENGINE_PLUGIN_NAME + HOUDINI_ENGINE_PLUGIN_EXT).replace(os.sep, '/')
    # _plugin_path = HOUDINI_PLUGIN_PATH
    print(f'try load houdini plugin path  --- {_plugin_path}')
    try:
        cmds.loadPlugin(_plugin_path, qt=True)

        # 自動ロードにしているとMaya2022 でarnold が使えなくなる問題がある
        # 自動ロードしなければHoudiniEngine もarnold もどちらも使えることを確認
        cmds.pluginInfo(_plugin_path, edit=True, autoload=False)
    except Exception as e:
        # logger.send_crash('{}-Crash-{}'.format(tool_title, e))
        print("error--- ", e)
        _flag = False
    return _flag

def plugin_unload():
    cmds.unloadPlugin("{}{}".format(HOUDINI_ENGINE_PLUGIN_NAME,
                                HOUDINI_ENGINE_PLUGIN_EXT), force=True)

def main():
    add_path()

    set_default_trust()
    set_trust_path()

    load_flag = plugin_load_check()
    print(load_flag, " ---- load_flag")

    z_drive_flag = True
    version_flag = ""

    set_option_var()

    _houdini_engine_plugin_path = os.path.join(HOUDINI_PLUGIN_PATH,
                HOUDINI_ENGINE_PLUGIN_NAME + HOUDINI_ENGINE_PLUGIN_EXT).replace(os.sep, '/')

    # _houdini_engine_plugin_path = HOUDINI_PLUGIN_PATH

    if load_flag:
        version_flag = plugin_version_check()
        # print(f'current houdini engine version ---- {version_flag}')
        # if version_flag != CURRENT_HOUDINI_VERSION:
        #     error = "version error"
        #     _m = u"インストールされている Houdini のバージョンが違います\n"
        #     _m += u"[ {} ] にバージョンアップしてください\n".format(CURRENT_HOUDINI_VERSION)
        #     _m += u"現在のバージョンは [ {} ] です\n".format(version_flag)
        #     _d = gui_util.ConformDialog(title=TITLE, message=_m)
        #     _d.exec_()
        #     return
        plugin_path = plugin_path_check()
        if plugin_path != _houdini_engine_plugin_path or version_flag != CURRENT_HOUDINI_VERSION:
            plugin_unload()
            z_drive_flag = False

    if not z_drive_flag or not load_flag:
        z_drive_flag = set_z_drive_plugin()

    return z_drive_flag













