﻿# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from maya import cmds, mel, utils

import inspect
import importlib
from imp import reload
import os
import sys
import traceback

maya_version = cmds.about(v=1)

def get_script_path():
    script_path = os.path.abspath(inspect.getsourcefile(lambda:0))
    return script_path

userSetup_path = get_script_path()
script_path = '/'.join(userSetup_path.replace('\\', '/').split('/')[0:-1])

def load_plugins():
    plugins = [
        'fbxmaya',
        'quatNodes',
        'curveWarp',
        '{}/plug-ins/CharcoalEditor/{}/CharcoalEditor2.mll'.format(script_path, maya_version)
    ]
    plugin_results = []
    for plugin in plugins:
        plugin_result = cmds.loadPlugin(plugin) if not cmds.pluginInfo(plugin, q=True, l=True) else False
        plugin_results.append(plugin_result)

try:
    maya.utils.executeDeferred('import tkgTools_menu;reload(tkgTools_menu);create_menu = tkgTools_menu.CreateMenu();create_menu.main()')
except Exception as e:
    print(traceback.format_exc())

try:
    maya.utils.executeDeferred(load_plugins)
except Exception as e:
    print(traceback.format_exc())

# -----------------------------------
#
# -----------------------------------
try:
    import splineIK.install
    utils.executeDeferred(splineIK.install.shelf)
except Exception as e:
    print(traceback.format_exc())

try:
    def reorder_attributes_main():
        from reorder_attributes import install
        install.execute()

    if not cmds.about(batch=True):
        cmds.evalDeferred(reorder_attributes_main)
except Exception as e:
    print(traceback.format_exc())
