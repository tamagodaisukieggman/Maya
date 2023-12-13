from __future__ import absolute_import

import json
import os
import sys

import pymel.core as pm
import maya.cmds as mc


# -----------------------------------------------------------------------------
# plugin fuction
# -----------------------------------------------------------------------------
def checkLoadPlugin(plugin=''):
    if not pm.pluginInfo(plugin, l=True, q=True):
        pm.loadPlugin(plugin)
        print('Plug-in, "{0}", was loaded successfully.'.format(plugin))
    else:
        print('Plug-in, "{0}", is already loaded. <Skipped>'.format(plugin))


# ---- unload turtle plugin ---------------------------------------------------
def turtleKiller():
    if mc.pluginInfo('Turtle', loaded=True, q=True):
        mc.unloadPlugin('Turtle', f=True)
    for unk in mc.ls('Turtle*'):
        mc.lockNode(unk, l=False)
        mc.delete(unk)
    print('unloaded turtle plugin and deleted related nodes successfully.')


# -----------------------------------------------------------------------------
# json functions
# -----------------------------------------------------------------------------
def exportJson(path=r'', dict={}):
    f = open(path, 'w')
    json.dump(dict, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()


def importJson(path=r''):
    f = open(path, 'r')
    tmp = f.read()
    res = json.loads(tmp)
    f.close()
    return res
