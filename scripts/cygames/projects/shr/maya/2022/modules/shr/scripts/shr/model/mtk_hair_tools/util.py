# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds
import os
from functools import wraps
import time
import sys
import shutil

import importlib

from . import TITLE


from . import gui_util

from . import TEMP_PATH
from . import ROOT_PATH
from . import AUTOMATION_TOOL_KIT
from . import PYSBS
from . import IMAGE_MAGICK_PATH
from . import ARNOLD_PLUGIN_NAME
from . import HOUDINI_ENGINE_PLUGIN_NAME
from . import NEED_PLUGINS
from . import HOUDINI_ENGINE_VERSION
from . import NEED_PATHS
from . import BIN
from . import HOUDINI
from . import HOUDINI_PATH


importlib.reload(gui_util)


# ARNOLD_PLUGIN_NAME = "mtoa"
# HOUDINI_ENGINE_PLUGIN_NAME = "houdiniEngine"

# NEED_PLUGINS = [ARNOLD_PLUGIN_NAME, HOUDINI_ENGINE_PLUGIN_NAME]
# HOUDINI_ENGINE_VERSION = "3.5 (API: 2)"

# NEED_PATHS = [AUTOMATION_TOOL_KIT, PYSBS, IMAGE_MAGICK_PATH, ROOT_PATH, TEMP_PATH]







def timeit(ndigits=2):
    """Print execution time [sec] of function/method
    - message: message to print with time
    - ndigits: precision after the decimal point
    """
    def outer_wrapper(func):
        # @wraps: keep docstring of "func"
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print("[ {} ] Function time for : {sec} [sec]".format(
                func.func_name,
                sec=round(end-start, ndigits))
            )
            return result
        return inner_wrapper
    return outer_wrapper

def keep_selections(func):
    u"""選択を保持するdecorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return _keep_selections_wrapper(func, *args, **kwargs)
    return wrapper


def _keep_selections_wrapper(func, *args, **kwargs):
    u"""選択を保持"""
    selection = cmds.ls(sl=True, type="tansform")
    result = func(*args, **kwargs)
    if selection:
        cmds.select(selection, ne=True)
    else:
        cmds.select(cl=True)
    return result

def path_exists(path):
    if os.path.exists(path):
        return path
    else:
        return None

def _warning_message(message):
    print(message)
    cmds.warning(message)
    _d = gui_util.ConformDialog(title=TITLE,
                    message=message)
    _d.exec_()



def add_path():
    # print("\nadd_path --------------------- ")
    os_env = os.environ["PATH"]
    os_env_list = []

    for x in os_env.split(";"):
        if HOUDINI in x and BIN in x:
            print("{:-<40}  {}".format("Houdini bin Path", x))
            continue
        else:
            os_env_list.append(x)


    os_env_str = ";".join(os_env_list)
    os_env_str = os_env_str + ";" + HOUDINI_PATH
    os.environ["PATH"] = os_env_str
    # print("{:-<40}  [ {} ]\n".format("Houdini Path Exists", HOUDINI_PATH in os.environ["PATH"].split(";")))

def path_check():
    # add_path()
    _message = ""
    _errors = []
    for path in NEED_PATHS:
        if path == TEMP_PATH or path == ROOT_PATH:
            if not os.path.exists(path):
                os.makedirs(path)
        if not os.path.exists(path):
            _errors.append(path.replace(os.sep, '/'))
        elif path == PYSBS and PYSBS not in sys.path:
            sys.path.append(PYSBS)

    if _errors:
        _m = "not found path [ {} ]".format(", ".join(_errors))
        _warning_message(_m)
        _message += _m
    return _message

def check_plugin():
    _errors = []
    _version_errors = ""
    _messages = ""
    for plugin_name in NEED_PLUGINS:
        cmds.loadPlugin(plugin_name, quiet=True)
        if plugin_name not in cmds.pluginInfo(q=True, listPlugins=True):
            _errors.append(plugin_name)
        if HOUDINI_ENGINE_PLUGIN_NAME == plugin_name:
            _version = cmds.pluginInfo(plugin_name, q=True, v=True)
            if _version != HOUDINI_ENGINE_VERSION:
                _version_errors = _version

    if _errors:
        _m = "can not find plugins [ {} ]".format(", ".join(_errors))
        _warning_message(_m)
        _messages += _m

    if _version_errors:
        _m = "not support version [ {} ][ {} ]".format(HOUDINI_ENGINE_PLUGIN_NAME, _version_errors)
        _warning_message(_m)
        _messages += _m

    return _messages


def cleat_directory(path):
    shutil.rmtree(path)


def clear_temp_directory():
    cleat_directory(TEMP_PATH)
    os.makedirs(TEMP_PATH)




