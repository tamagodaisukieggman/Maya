# -*- coding: utf-8 -*-
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.cmds as cmds
import maya.mel as mel
import math
import os
import csv



def create_env_tool_launcher():
    cmdHash = {"createSPVcolor":{"col":[0.0, 0.8, 0.9], "cmd":"import mtk3d.maya.createSPVcolor as createSPVcolor;reload(createSPVcolor);createSPVcolor.create_SPMatVcolorWindow()"},
    "create_SPMatVcolorWindow":{"col":[0.0, 0.5, 0.8], "cmd":"import mtk3d.maya.createLOD as createLOD;reload(createLOD);createLOD.createLOD_Window()"}}
    
    
    cmds.window(title='env_tool_launcher')
    cmds.columnLayout()
    for cmdNameStr, counter in cmdHash.items():
        print cmdHash[cmdNameStr]
        cmds.button(cmdNameStr, label=cmdNameStr, width=200, height=50, backgroundColor=cmdHash[cmdNameStr]["col"], annotation="hoge", command='exec("'+cmdHash[cmdNameStr]["cmd"]+'")')
    cmds.showWindow()
