# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

import maya.cmds as cmds


PLUGIN_NAME = u'Turtle'


# Turtle周りのノードを削除する関数
def deleteTurtleNodes(*args):
    dn = cmds.pluginInfo(PLUGIN_NAME, q=True, dn=True)
    turtleNodes = cmds.ls(type=dn)
    if len(turtleNodes) != 0:
        cmds.lockNode(turtleNodes, l=False)
        cmds.delete(turtleNodes)
    return 0


# Turtleをロードする関数
# 一度もロードされていない環境だとpluginInfoが動作しません
def loadTurtlePlugin(*args):
    cmds.loadPlugin(PLUGIN_NAME)
    return 0


# Turtleをアンロードする関数
# アンロード時に警告が出ますが，Turtleの仕組み上不可避です
def unloadTurtlePlugin(*args):
    cmds.unloadPlugin(PLUGIN_NAME, f=True)
    return 0


# main関数
def main(*args):
    loadTurtlePlugin()
    deleteTurtleNodes()
    unloadTurtlePlugin()
    return 0