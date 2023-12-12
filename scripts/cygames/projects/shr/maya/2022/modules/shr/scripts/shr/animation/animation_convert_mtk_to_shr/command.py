# -*- coding: utf-8 -*-
import os
import subprocess
import maya.cmds as cmds
from maya import OpenMaya as om
from maya import OpenMayaUI as omUI
from PySide2 import QtGui,QtWidgets,QtCore
import shiboken2
#eSTの宣言より後に実行するとエラーになる
import maya.mel as mm;mm.eval('eST3menuBar;')
import eST3 as eST
import shr.model.character_importer.command as character_importer
import shr.model.character_exporter.command as character_exporter


# ------------------------------------------
# 定数
# ------------------------------------------
#fileInfo用
DEV = True

def bake_animation(nodes):
    '''
    アニメーションをベイク
    '''
    # Get Character joints
    start = cmds.playbackOptions(q=True, minTime=True)
    end   = cmds.playbackOptions(q=True, maxTime=True)
    # Bake Animation
    cmds.bakeResults(	nodes,
                    simulation=True,
                    t=(start,end),
                    sampleBy=1,
                    disableImplicitControl=True,
                    preserveOutsideKeys=False,
                    sparseAnimCurveBake=False,
                    removeBakedAttributeFromLayer=False,
                    bakeOnOverrideLayer=False,
                    minimizeRotation=False,
                    at=['tx','ty','tz','rx','ry','rz','sx','sy','sz'] )
    # Return Result
    
    return nodes

def maya_to_pySide(name, toType):
    ptr = omUI.MQtUtil.findControl(name)
    if not ptr:
        ptr = omUI.MQtUtil.findLayout(name)    
         
    if not ptr:
        ptr = omUI.MQtUtil.findMenuItem(name)
         
    if not ptr:
        return None
 
    return shiboken2.wrapInstance(int(ptr), toType)

def getMayaWindow():
    ptr = omUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken2.wrapInstance(int(ptr), QtWidgets.QMainWindow)
        
def select_character_all_rig():
    eST.rCmds.LaunchWidget( ':common_maya.rig.rigViewWidget' )
    #scripteditorからだと選択されないバグあり。menuから実行する分には問題ない。
    for menu in maya_to_pySide("eST3rigViewWidget",QtWidgets.QMainWindow).children():
        if type(menu) == QtWidgets.QMenuBar:
            menu.activateWindow()
            for action in menu.actions():
                if action.text() == "Select":
                    for lp in action.menu().actions():
                        if lp.text() == "All Nodes in the Current Rig":
                            cmds.setFocus("modelPanel4")
                            lp.triggered.emit()
                            return cmds.ls(sl=True) 
    

def animation_convert(fbx_paths = []):
    if len(fbx_paths) == 0:
        _animation_convert()
        return 1
    for fbx_path in fbx_paths:
        _animation_convert(fbx_path)
        return 1

def _animation_convert(fbx_path = ""):
    TYPE = "animation"
    imp = character_importer.importer(TYPE)
    #exp = character_exporter.exporter(TYPE)
    #cmds.file(cmds.file(q=True, sn=True),o=True,f=True)
    imp.exec_import(fbx_path)
    rigs = select_character_all_rig()
    if len(rigs) == 0:
        cmds.warning(u"ベイク対象となるリグが存在しません。処理を終了します。")
        return 0
    bake_animation(rigs)

