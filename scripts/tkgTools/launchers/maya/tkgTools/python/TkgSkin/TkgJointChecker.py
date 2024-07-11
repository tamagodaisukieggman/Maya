# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   TkgJointChecker
#-------------------------------------------------------------------------------------------


try:
    # Maya 2022-
    from builtins import range
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel
import math
import os.path
import TkgCommon.TkgUtility
import TkgCommon.TkgSetting

from TkgCommon.TkgUtility import TkgUtility
from TkgCommon.TkgSetting import TkgSetting

reload(TkgCommon.TkgUtility)
reload(TkgCommon.TkgSetting)

g_version = "1.0.0"
g_toolName = "TkgJointChecker"
g_scriptPrefix= g_toolName + "."
g_uiPrefix= g_toolName + "UI"

g_setting = TkgSetting(g_toolName)

g_resultStringList = []
g_resultObjectList = []

#-------------------------------------------------------------------------------------------
#   メインUI
#-------------------------------------------------------------------------------------------
def UI():

    global g_scriptPrefix
    global g_uiPrefix
    global g_toolName
    global g_setting
    global g_resultStringList
    global g_resultObjectList

    g_resultStringList = []
    g_resultObjectList = []

    if g_setting == None:
        g_setting = TkgSetting(g_toolName)

    width=250
    height=1
    formWidth=width-5

    windowTitle=g_scriptPrefix.replace(".","")
    windowName=windowTitle+"Win"
    
    TkgUtility.CheckWindow(windowName)

    cmds.window( windowName, title=windowTitle, widthHeight=(width, height),s=False,mnb=True,mxb=False,rtf=True)

    cmds.columnLayout(adjustableColumn=True)

    cmds.checkBox(g_uiPrefix + "CheckRotateZero", label="Check Rotate Zero", cc=g_scriptPrefix+"SaveSetting()", v=True )
    cmds.checkBox(g_uiPrefix + "CheckOrientZero", label="Check Orient Zero", cc=g_scriptPrefix+"SaveSetting()", v=True)
    cmds.checkBox(g_uiPrefix + "CheckScaleOne", label="Check Scale One", cc=g_scriptPrefix+"SaveSetting()", v=True)

    cmds.button( label="Check",bgc=[0.8,0.5,0.5],command=g_scriptPrefix+"CheckJoint()")

    cmds.separator( style='in',h=15,w=formWidth)

    cmds.text(label=" Result List ",al="left")

    cmds.textScrollList(g_uiPrefix + "ResultList", allowMultiSelection=True, h=200, selectCommand=g_scriptPrefix + "SelectTargetJoint()", dcc=g_scriptPrefix + "ShowTargetJointAttr()",)

    cmds.separator( style='in',h=15,w=formWidth)
    
    cmds.button( label="About",w=formWidth,command=g_scriptPrefix + "ShowAbout()")

    cmds.setParent( ".." )
 
    cmds.showWindow(windowName)

    LoadSetting()

#-------------------------------------------------------------------------------------------
#   CheckJoint
#-------------------------------------------------------------------------------------------
def CheckJoint():

    global g_resultStringList
    global g_resultObjectList

    g_resultStringList = []
    g_resultObjectList = []

    selectList = cmds.ls(sl=True, l=True)

    if selectList == None:
        return

    if len(selectList) == 0:
        return

    cmds.select(selectList, r=True, hi=True)

    targetList = cmds.ls(sl=True, l=True)

    for p in range(0, len(targetList)):

        thisSelect = targetList[p]

        if cmds.objectType( thisSelect ) != "joint":
            continue

        thisResult = GetResultString(thisSelect)

        if thisResult == "":
            continue

        g_resultStringList.append(thisResult)
        g_resultObjectList.append(thisSelect)

    cmds.textScrollList(g_uiPrefix + "ResultList", e=True, removeAll=True)
    cmds.textScrollList(g_uiPrefix + "ResultList", e=True, append=g_resultStringList)

    cmds.select(selectList, r=True)

#-------------------------------------------------------------------------------------------
#   GetResultString
#-------------------------------------------------------------------------------------------
def GetResultString(target):

    global g_uiPrefix

    rotateZero = cmds.checkBox(g_uiPrefix + "CheckRotateZero", q=True, v=True )
    orientZero = cmds.checkBox(g_uiPrefix + "CheckOrientZero", q=True, v=True )
    scaleOne = cmds.checkBox(g_uiPrefix + "CheckScaleOne", q=True, v=True )

    result = GetShortNameWithDepth(target) + " : "

    exist = False

    if IsRotateZero(target) == False and rotateZero == True:

        result += " Rotate!"
        exist = True

    if IsOrigentZero(target) == False and orientZero == True:

        result += " Orient!"
        exist = True

    if IsScaleZero(target) == False and scaleOne == True:

        result += " Scale!"
        exist = True

    if exist == False:
        return ""

    return result

#-------------------------------------------------------------------------------------------
#   IsRotateZero
#-------------------------------------------------------------------------------------------
def IsRotateZero(target):

    value = cmds.getAttr(target + ".rotate")[0]

    if value[0] != 0:
        return False

    if value[1] != 0:
        return False

    if value[2] != 0:
        return False

    return True

#-------------------------------------------------------------------------------------------
#   IsOrigentZero
#-------------------------------------------------------------------------------------------
def IsOrigentZero(target):

    value = cmds.getAttr(target + ".jointOrient")[0]

    if value[0] != 0:
        return False

    if value[1] != 0:
        return False

    if value[2] != 0:
        return False

    return True

#-------------------------------------------------------------------------------------------
#   IsScaleZero
#-------------------------------------------------------------------------------------------
def IsScaleZero(target):

    value = cmds.getAttr(target + ".scale")[0]

    if value[0] != 1:
        return False

    if value[1] != 1:
        return False

    if value[2] != 1:
        return False

    return True

#-------------------------------------------------------------------------------------------
#   GetShortName
#-------------------------------------------------------------------------------------------
def GetShortNameWithDepth(target):

    if target.find("|") == -1:
        return target

    splitStr = target.split("|")

    result = ""

    for p in range(0, len(splitStr) - 1):
        result += " "

    result += splitStr[len(splitStr) - 1]

    return result
    

#-------------------------------------------------------------------------------------------
#   SelectTargetJoint
#-------------------------------------------------------------------------------------------
def SelectTargetJoint():

    global g_resultStringList
    global g_resultObjectList

    if len(g_resultStringList) == 0:
        return

    if len(g_resultObjectList) == 0:
        return

    if len(g_resultStringList) != len(g_resultObjectList):
        return

    selectIndexList = cmds.textScrollList(g_uiPrefix + "ResultList", q=True, selectIndexedItem=True)

    resultSelectList = []
    for p in range(0, len(selectIndexList)):

        thisIndex = selectIndexList[p] - 1

        if thisIndex >= len(g_resultStringList):
            continue

        resultSelectList.append(g_resultObjectList[thisIndex])

    cmds.select(resultSelectList,r=True)

#-------------------------------------------------------------------------------------------
#   ShowTargetJointAttr
#-------------------------------------------------------------------------------------------
def ShowTargetJointAttr():

    global g_resultStringList
    global g_resultObjectList

    if len(g_resultStringList) == 0:
        return

    if len(g_resultObjectList) == 0:
        return

    if len(g_resultStringList) != len(g_resultObjectList):
        return

    selectIndexList = cmds.textScrollList(g_uiPrefix + "ResultList", q=True, selectIndexedItem=True)

    if len(selectIndexList) == 0:
        return

    thisIndex = selectIndexList[0] - 1

    if thisIndex >= len(g_resultObjectList):
        return

    cmds.select(g_resultObjectList[thisIndex],r=True)

    mel.eval("ShowAttributeEditorOrChannelBox")

#-------------------------------------------------------------------------------------------
#   Save Setting
#-------------------------------------------------------------------------------------------
def SaveSetting():

    global g_uiPrefix
    global g_setting

    rotateZero = cmds.checkBox(g_uiPrefix + "CheckRotateZero", q=True, v=True )
    orientZero = cmds.checkBox(g_uiPrefix + "CheckOrientZero", q=True, v=True )
    scaleOne = cmds.checkBox(g_uiPrefix + "CheckScaleOne", q=True, v=True )

    g_setting.Save("CheckRotateZero", rotateZero)
    g_setting.Save("CheckOrientZero", orientZero)
    g_setting.Save("CheckScaleOne", scaleOne)

#-------------------------------------------------------------------------------------------
#   Load Setting
#-------------------------------------------------------------------------------------------
def LoadSetting():

    global g_uiPrefix
    global g_setting
    
    rotateZero = g_setting.Load("CheckRotateZero", "bool")
    orientZero = g_setting.Load("CheckOrientZero", "bool")
    scaleOne = g_setting.Load("CheckScaleOne", "bool")

    cmds.checkBox(g_uiPrefix + "CheckRotateZero", e=True, v=rotateZero )
    cmds.checkBox(g_uiPrefix + "CheckOrientZero", e=True, v=orientZero )
    cmds.checkBox(g_uiPrefix + "CheckScaleOne", e=True, v=scaleOne )
    
