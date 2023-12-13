# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   OdinCharaTool
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.mel as mel

import os
import math

import CyCommon.CyUtility
import CyCommon.CySetting

from CyCommon.CyUtility import CyUtility
from CyCommon.CySetting import CySetting

#-------------------------------------------------------------------------------------------
#   更新
#-------------------------------------------------------------------------------------------
def Execute():

    main = Main()
    main.CreateUI()

#*****************************************************************
# メイン
#*****************************************************************
class Main():

    #===========================================
    # __init__
    #===========================================
    def __init__(self):

        self.version = "0.1.0"
        self.toolName = "OdinCharaTool"
        self.scriptPrefix = self.toolName + "."
        self.uiPrefix = self.toolName + "UI_"
        self.windowName = self.toolName + "Win"

        self.setting = CySetting(self.toolName)

        self.currentSelect = None

        self.color00 = [0.5,0.5,0.5]
        self.color01 = [0.5,0.7,0.5]
        self.color02 = [0.5,0.6,0.8]

    #===========================================
    # UI作成
    #===========================================
    def CreateUI(self):

        width=200
        height=1
        formWidth=width-5

        CyUtility.CheckWindow(self.windowName)

        cmds.window( self.windowName, title=self.toolName, wh=(width, height) ,s=True,mnb=True,mxb=True,rtf=False)

        cmds.columnLayout(adjustableColumn=True)
        cmds.scrollLayout(self.uiPrefix + "LayerScrollList",verticalScrollBarThickness=5, cr=True)

        cmds.frameLayout(l=u"ロケーター配置",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
        cmds.columnLayout(adjustableColumn=True)

        cmds.button( label=u"root_point配置", bgc=self.color01 , h=30, command=self.SetLocator00)

        cmds.separator( h=20, style="in" )
        
        cmds.button( label=u"男の子 武器ロケータ配置", bgc=self.color02 , h=30, command=self.SetLocator10)
        cmds.button( label=u"女の子 武器ロケータ配置", bgc=self.color02 , h=30, command=self.SetLocator11)
        cmds.button( label=u"おっさん 武器ロケータ配置", bgc=self.color02 , h=30, command=self.SetLocator12)
        cmds.button( label=u"子供 武器ロケータ配置", bgc=self.color02 , h=30, command=self.SetLocator13)
        cmds.button( label=u"ゴリ 武器ロケータ配置", bgc=self.color02 , h=30, command=self.SetLocator14)

        cmds.setParent( ".." )
        cmds.setParent( ".." )

        cmds.setParent( ".." )
        cmds.setParent( ".." )
     
        cmds.showWindow(self.windowName)

    #===========================================
    # ロケータセット root_point
    #===========================================
    def SetLocator00(self,tmp):

        self.SetLocator("root_point","position",[0,0,0],[0,0,0],[1,1,1])

    #===========================================
    # ロケータセット 男の子
    #===========================================
    def SetLocator10(self,tmp):

        self.SetLocator("L_weapon","L_hand",[10.418,-1.186,0],[0,0,0],[1,1,1])
        self.SetLocator("R_weapon","R_hand",[-10.418,-1.186,0],[0,0,0],[1,1,1])

    #===========================================
    # ロケータセット 女の子
    #===========================================
    def SetLocator11(self,tmp):

        self.SetLocator("L_weapon","L_hand",[10.96,-1.768,0],[0,0,0],[1,1,1])
        self.SetLocator("R_weapon","R_hand",[-10.96,-1.768,0],[0,0,0],[1,1,1])

    #===========================================
    # ロケータセット おっさん
    #===========================================
    def SetLocator12(self,tmp):

        self.SetLocator("L_weapon","L_hand",[12.877,-1.156,0],[0,0,0],[1,1,1])
        self.SetLocator("R_weapon","R_hand",[-12.877,-1.156,0],[0,0,0],[1,1,1])

    #===========================================
    # ロケータセット 子供
    #===========================================
    def SetLocator13(self,tmp):

        self.SetLocator("L_weapon","L_hand",[6.42,-0.918,-0.001],[0,0,0],[1,1,1])
        self.SetLocator("R_weapon","R_hand",[-6.42,-0.918,-0.001],[0,0,0],[1,1,1])

    #===========================================
    # ロケータセット ゴリ
    #===========================================
    def SetLocator14(self,tmp):

        self.SetLocator("L_weapon","L_hand",[12.482,0.277,0],[0,0,0],[1,1,1])
        self.SetLocator("R_weapon","R_hand",[-12.482,0.277,0],[0,0,0],[1,1,1])
        
    #===========================================
    # ロケータセット
    #===========================================
    def SetLocator(self, locatorName, parentName, position, rotate, scale):

        self.currentSelect = cmds.ls(sl=True, fl=True, l=True)

        if self.currentSelect == None:
            print u"親となるオブジェクトを選択して下さい"
            return

        if len(self.currentSelect) == 0:
            print u"親となるオブジェクトを選択して下さい"
            return

        cmds.select(self.currentSelect, hi=True)

        targetList = cmds.ls(sl=True, fl=True, l=True, tr=True)

        if targetList == None:
            print u"親となるオブジェクトを選択して下さい"
            self.Reselect()
            return

        if len(targetList) == 0:
            print u"親となるオブジェクトを選択して下さい"
            self.Reselect()
            return

        if self.ExistObject(parentName, targetList) == False:
            print locatorName + u" の親となる " + parentName + u" が選択しているオブジェクト内に見つかりませんでした"
            self.Reselect()
            return

        parentObject = self.GetObject(parentName, targetList)

        if self.ExistObject(locatorName, targetList) == False:
            self.CreateLocator(locatorName,parentObject)
            self.Reselect()
            cmds.select(self.currentSelect, hi=True)
            targetList = cmds.ls(sl=True, fl=True, l=True, tr=True)
            print locatorName + u" が存在しなかったので " + parentName + u" の下に作成しました"

        targetObject = self.GetObject(locatorName, targetList)

        if targetObject == None:
            print locatorName + u" が見つかりませんでした"
            self.Reselect()
            return

        self.FixLocator(targetObject)

        cmds.setAttr(targetObject + ".translate", position[0], position[1], position[2], type="double3")
        cmds.setAttr(targetObject + ".rotate", rotate[0], rotate[1], rotate[2], type="double3")
        cmds.setAttr(targetObject + ".scale", scale[0], scale[1], scale[2], type="double3")

        print locatorName + self.GetPrintString(u"の位置を ",position,u" ") + self.GetPrintString(u"回転を ",rotate,u" ") + self.GetPrintString(u"スケールを ",scale,u" に設定しました") 

        self.Reselect()

    #===========================================
    # オブジェクトの存在確認
    #===========================================
    def ExistObject(self, objectName, targetList):

        for target in targetList:

            thisShortName = self.GetShortName(target)

            if thisShortName == objectName:
                return True

        return False

    #===========================================
    # オブジェクトの存在確認
    #===========================================
    def CreateLocator(self, locatorName, parentObject):

        targetLocator = cmds.spaceLocator(n=locatorName);
        cmds.parent( targetLocator, parentObject, r=True )

    #===========================================
    # ロケータの値を修正
    #===========================================
    def FixLocator(self, locatorName):

        shapeNodeList = cmds.listRelatives(locatorName,s=True)

        if shapeNodeList == None:
            return

        if len(shapeNodeList) == 0:
            return

        shapeNode = shapeNodeList[0]

        if cmds.objectType(shapeNode) != "locator":
            return

        cmds.makeIdentity(locatorName,apply=True,t=True,r=True,s=True,n=False,pn=True)
        cmds.makeIdentity(locatorName,apply=False,t=True,r=True,s=True)

        cmds.setAttr(shapeNode + ".localPositionX", 0)
        cmds.setAttr(shapeNode + ".localPositionY", 0)
        cmds.setAttr(shapeNode + ".localPositionZ", 0)

        cmds.setAttr(shapeNode + ".localScaleX", 1)
        cmds.setAttr(shapeNode + ".localScaleY", 1)
        cmds.setAttr(shapeNode + ".localScaleZ", 1)
        
    #===========================================
    # オブジェクトの取得
    #===========================================
    def GetObject(self, objectName, targetList):

        for target in targetList:

            thisShortName = self.GetShortName(target)

            if thisShortName == objectName:
                return target

        return None

    #===========================================
    # オブジェクト名を取得
    #===========================================
    def GetShortName(self, longName):

        splitString = longName.split("|")

        if len(splitString) == 0:
            return longName

        return splitString[len(splitString) - 1]

    #===========================================
    # 表示用文字列取得
    #===========================================
    def GetPrintString(self, prifix, listData ,suffix):

        result = prifix

        for cnt in range(0,len(listData)):
            
            result += str(listData[cnt])

            if cnt < len(listData) -1:
                result += ","

        result += suffix

        return result

    #===========================================
    # 再選択
    #===========================================
    def Reselect(self):

        if self.currentSelect == None:
            return

        if len(self.currentSelect) == 0:
            return

        cmds.select(self.currentSelect, r=True)
