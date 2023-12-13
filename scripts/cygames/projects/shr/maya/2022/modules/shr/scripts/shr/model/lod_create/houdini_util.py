# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import maya.cmds as cmds

from . import TITLE
from . import gui_util


CURRENT_HOUDINI_VERSION = "18.5.532"
HOUDINI = "Houdini"
BIN = "bin"
HOUDINI_PATH = "C:/Program Files/Side Effects Software/{} {}/{}".format(HOUDINI, CURRENT_HOUDINI_VERSION, BIN)

HOUDINI_PLUGIN_PATH = "Z:/mtk/tools/maya/modules/houdini_engine/plug-ins"
HOUDINI_SCRIPTS_PATH = "Z:/mtk/tools/maya/modules/houdini_engine/scripts/houdini_engine_for_maya"
# PLUGIN_PATH = "Z:/mtk/tools/maya/modules/houdini_engine/plug-ins"

HOUDINI_ENGINE_PLUGIN_NAME = "houdiniEngine"
HOUDINI_ENGINE_PLUGIN_EXT = ".mll"

HOUDINI_ENGINE_VERSION = "3.5 (API: 2)"

HDA_NAME = "mtk_hair_uv_tool"
REMOVE_HDA_NAME = "mtk_hair_remove"
REMOVE_HDA_NAME = "mtk_hair_edge_remove"
HDA_PATH = "Z:/mtk/tools/maya/share/hda/develop"

_SessionType = {"houdiniEngineSessionType": 2}
_SessionPipeCustom = {"houdiniEngineSessionPipeCustom": 0}
_ThriftPipe = {"houdiniEngineThriftPipe": "hapi"}


def check_option_var():
    _type = cmds.optionVar(q=list(_SessionType.keys())[0])
    _session = cmds.optionVar(q=list(_SessionPipeCustom.keys())[0])
    _pipe = cmds.optionVar(q=list(_ThriftPipe.keys())[0])

    _type_default = list(_SessionType.values())[0]
    _session_default = list(_SessionPipeCustom.values())[0]
    _pipe_default = list(_ThriftPipe.values())[0]

    print("{:-<36} idDefault [{}]".format(list(_SessionType.keys())[0], _type == list(_SessionType.values())[0]))
    print("{:-<36} idDefault [{}]".format(list(_SessionPipeCustom.keys())[0],_session == list(_SessionPipeCustom.values())[0]))
    print("{:-<36} idDefault [{}]".format(list(_ThriftPipe.keys())[0], _pipe == list(_ThriftPipe.values())[0]))

    _m = ""
    if _type != _type_default:
        _m += "can not change option var [ {} ]".format(list(_SessionType.keys())[0])
    elif _session != _session_default:
        _m += "can not change option var [ {} ]".format(list(_SessionPipeCustom.keys())[0])
    elif _pipe != _pipe_default:
        _m += "can not change option var [ {} ]".format(list(_ThriftPipe.keys())[0])

    if _m:
        _d = gui_util.ConformDialog(title=u"オプション変更不可",
                        message=_m)
        _d.exec_()
        return False
    else:
        return True


def set_option_var():
        cmds.optionVar(iv=[list(_SessionType.keys())[0],
                            list(_SessionType.values())[0]])
        cmds.optionVar(iv=[list(_SessionPipeCustom.keys())[0],
                            list(_SessionPipeCustom.values())[0]])
        cmds.optionVar(sv=[list(_ThriftPipe.keys())[0],
                            list(_ThriftPipe.values())[0]])


def plugin_load_check():
    _load_flag = HOUDINI_ENGINE_PLUGIN_NAME in cmds.pluginInfo(query=True, listPlugins=True)
    return _load_flag

def plugin_path_check():
    _plugin_path = cmds.pluginInfo(HOUDINI_ENGINE_PLUGIN_NAME,
                                    q=True, path=True).replace(os.sep, '/')
    return _plugin_path


def plugin_version_check():
    _current_version = cmds.houdiniEngine(bhv=True)
    return _current_version


def set_z_drive_plugin():
    _flag = True
    _plugin_path = os.path.join(HOUDINI_PLUGIN_PATH,
                HOUDINI_ENGINE_PLUGIN_NAME + HOUDINI_ENGINE_PLUGIN_EXT).replace(os.sep, '/')
    try:
        cmds.loadPlugin(_plugin_path, qt=True)
        cmds.pluginInfo(_plugin_path, edit=True, autoload=True)
    except Exception as e:
        # logger.send_crash('{}-Crash-{}'.format(tool_title, e))
        print("error--- ", e)
        _flag = False
    return _flag

def plugin_unload():
    cmds.unloadPlugin("{}{}".format(HOUDINI_ENGINE_PLUGIN_NAME,
                                HOUDINI_ENGINE_PLUGIN_EXT), force=True)

def main():
    load_flag = plugin_load_check()
    z_drive_flag = True
    version_flag = ""

    set_option_var()

    # 以前使っていたが、たぶん必要ないのでコメントアウト
    # _option_check = check_option_var()
    # if not _option_check:
    #     return u"Option Var の設定を変更できませんでした"

    _houdini_engine_plugin_path = os.path.join(HOUDINI_PLUGIN_PATH,
                HOUDINI_ENGINE_PLUGIN_NAME + HOUDINI_ENGINE_PLUGIN_EXT).replace(os.sep, '/')

    if load_flag:
        version_flag = plugin_version_check()
        if version_flag != CURRENT_HOUDINI_VERSION:
            error = "version error"
            _m = u"インストールされている Houdini のバージョンが違います\n"
            _m += u"[ {} ] にバージョンアップしてください\n".format(CURRENT_HOUDINI_VERSION)
            _m += u"現在のバージョンは [ {} ] です\n".format(version_flag)
            _d = gui_util.ConformDialog(title=TITLE, message=_m)
            _d.exec_()
            return
        plugin_path = plugin_path_check()
        if plugin_path != _houdini_engine_plugin_path:
            plugin_unload()
            z_drive_flag = False

    if not z_drive_flag:
        z_drive_flag = set_z_drive_plugin()

    return z_drive_flag



def set_active_z_drive_plugin():
    _load_flag = HOUDINI_ENGINE_PLUGIN_NAME in cmds.pluginInfo(query=True, listPlugins=True)
    _plugin_path = ""
    _current_version = ""
    _houdini_engine_plugin_path = os.path.join(HOUDINI_PLUGIN_PATH,
                                                HOUDINI_ENGINE_PLUGIN_NAME + HOUDINI_ENGINE_PLUGIN_EXT).replace(os.sep, '/')

    if _load_flag:
        _current_version = cmds.houdiniEngine(bhv=True)
        _plugin_path = cmds.pluginInfo(HOUDINI_ENGINE_PLUGIN_NAME, q=True, path=True).replace(os.sep, '/')
        if _plugin_path != _houdini_engine_plugin_path:
            cmds.unloadPlugin("{}{}".format(HOUDINI_ENGINE_PLUGIN_NAME, HOUDINI_ENGINE_PLUGIN_EXT), force=True)
            # print("{:-<40}  {}{}".format("unloadPlugin", HOUDINI_ENGINE_PLUGIN_NAME, HOUDINI_ENGINE_PLUGIN_EXT))
            _load_flag = False
    else:
        _load_flag = False

    # print("{:-<40}  {}".format("_plugin_path", _plugin_path))
    # print("{:-<40}  {}\n".format("_load_flag", _load_flag))

    if not _load_flag:
        try:
            cmds.loadPlugin(_houdini_engine_plugin_path, qt=True)
            cmds.pluginInfo(_houdini_engine_plugin_path, edit=True, autoload=True)
        except Exception as e:
            # logger.send_crash('{}-Crash-{}'.format(tool_title, e))
            print("error--- ", e)
            return False

    if HOUDINI_ENGINE_PLUGIN_NAME not in cmds.pluginInfo(query=True, listPlugins=True):
        return False
    else:
        _version = cmds.pluginInfo(_houdini_engine_plugin_path, q=True, v=True)
        _current_version = cmds.houdiniEngine(bhv=True)
        print("{:-<40}  {}\n".format("_version", _current_version))
        return True













