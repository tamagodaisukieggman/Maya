# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

import maya.cmds as cmds


PLUGIN_NAME = u'Turtle'


# Turtle周りのノードを削除する関数
def deleteTurtleNodes():
    dn = cmds.pluginInfo(PLUGIN_NAME, q=True, dn=True)
    turtleNodes = cmds.ls(type=dn)
    if turtleNodes:
        cmds.lockNode(turtleNodes, l=False)
        cmds.delete(turtleNodes)


# Turtleをロードする関数
def loadTurtlePlugin():
    cmds.loadPlugin(PLUGIN_NAME)


# Turtleをアンロードする関数
def unloadTurtlePlugin():
    cmds.unloadPlugin(PLUGIN_NAME, f=True)


# main関数
def main():

    isLoaded = cmds.pluginInfo(PLUGIN_NAME, q=True, loaded=True)
    if not isLoaded:
        loadTurtlePlugin()

    deleteTurtleNodes()

    if not isLoaded:
        unloadTurtlePlugin()

    return True
