#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import shutil
import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds
import maya.mel as mel

# https://help.autodesk.com/view/MAYAUL/2017/ENU/?guid=__files_GUID_85B1116E_F0C1_42AD_9CD4_30E936B6C7B8_htm
# https://download.autodesk.com/us/maya/2009help/Nodes/renderGlobals.html
g_showDialog = True

##########################################################
# Plug-in
##########################################################
class GluonMiniMapClass(OpenMaya.MPxCommand):
    kPluginCmdName = 'GluonMiniMapSnapshot'

    def __init__(self):
        ''' Constructor. '''
        OpenMaya.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        ''' Create an instance of our command. '''
        return GluonMiniMapClass()

    def doIt(self, args):
        ''' Command execution. '''
        if not self.validateBeforeDoIt():
            return
        # パースペクティブカメラのモデルビューパネルを取得
        mPanel = getAnyVisibleModelPanel()
        target = cmds.ls(sl=True)
        outputImgName = target[0]
        # cam = cmds.modelPanel(mPanel, q=True, camera=True)
        cam = "top"
        mel.eval("lookThroughModelPanel " + cam + " " + mPanel)
        cmds.setAttr("defaultRenderGlobals.imageFormat", 32)  # 19==tga, 32==png
        cmds.setAttr("defaultRenderGlobals.matteOpacityUsesTransparency", False)
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix", outputImgName, type="string")
        cmds.select(target, r=True)
        cmds.viewSet(t=True)
        cmds.viewFit(fitFactor=1.0)
        self.setupRenderCamera(cam)
        cmds.setAttr(cam + ".renderable", True)
        cmds.render(cam, x=256, y=256) # ここでtmpとrenderDataフォルダが出来る
        curSceneFilePath = cmds.file(q=True, sn=True)
        imgFolderPath = os.path.dirname(os.path.dirname(curSceneFilePath)) + "/images"
        if not os.path.exists(imgFolderPath):
            os.makedirs(imgFolderPath)
        editor = 'renderView'
        saveImgPath = imgFolderPath + "/" + outputImgName + ".png"
        cmds.renderWindowEditor(editor, e=True,
                                writeImage=saveImgPath)
        print("saveImgPath: " + saveImgPath)
        # renderで出来たtmpとrenderDataフォルダを消す
        tmpFolderPath = imgFolderPath + "/tmp"
        renderDataFolderPath = os.path.dirname(imgFolderPath) + "/renderDat"
        try:
            shutil.rmtree(tmpFolderPath)
            shutil.rmtree(renderDataFolderPath)
        except:
            pass
        if g_showDialog:
            cmds.confirmDialog(title="Done", message=u"選択したオブジェクトのレンダリングをimagesフォルダに書き出しました: " +
                                saveImgPath, button=["OK"], defaultButton="OK")
        else:
            print(u"選択したオブジェクトのレンダリングをimagesフォルダに書き出しました。")

    def validateBeforeDoIt(self):
        # シーンが開かれているかチェック
        curSceneFilePath = cmds.file(q=True, sn=True)
        if not curSceneFilePath:
            if g_showDialog:
                cmds.confirmDialog(title="Usage",
                                   message=u"シーンを開いてから実行してください", button=["OK"], defaultButton="OK")
                return False
            else:
                print(u"シーンを開いてから実行してください")
                return False
        # 選択されているパーツが一個かどうか確認
        target = cmds.ls(sl=True)
        if len(target) == 0:
            if g_showDialog:
                cmds.confirmDialog(title="Usage", message=u"MiniMapのアイコン用にレンダリングしたいパーツを選択してから実行してください。", button=["OK"], defaultButton="OK")
            print(u"MiniMapのアイコン用にレンダリングしたいパーツを選択してから実行してください。")
            return False
        outputImgName = target[0]
        if len(target) > 1:
            if g_showDialog:
                userInput = cmds.confirmDialog(title="Confirm",
                                               message=u"""2つ以上のオブジェクトが選択されています。　
                                               書き出される画像の名前は最初に選択された """ +
                                                       outputImgName + u" になります。　よろしいですか？",
                                               button=["Yes", "No"],
                                               defaultButton="Yes", cancelButton="No", dismissString="No")
                if userInput == "No":
                    cmds.confirmDialog(title="Cencelled", message=u"処理をキャンセルしました。",
                                       button=["OK"], defaultButton="OK")
                    return False
            else:
                print(u"2つ以上のオブジェクトが選択されています。　書き出される画像の名前は最初に選択した " +
                                                       outputImgName + u" になります。")
        return True


    def setupRenderCamera(self, camName):
        u"""
        MiniMapのレンダー用に新規のカメラを設定します。
        :return: string 新規のカメラの名前
        """
        pCameras = cmds.listCameras()
        for cam in pCameras:
            if cam == camName:
                cmds.setAttr(camName + ".renderable", True)
                # TODO: topカメラの向きをツールで決めるかシーンで決めるか相談
                cmds.setAttr(camName + ".rotateX", -90)
                cmds.setAttr(camName + ".rotateY", 180)
                cmds.setAttr(camName + ".rotateZ", 0)
                return [camName, camName + "Shape"]
        return None

##########################################################
# functions
##########################################################
def getAnyVisibleModelPanel():
    u"""
    現在開いているViewの内モデルパネルを一つ返します。
    :return: string. VisibleなModelPanelのうち最初の１つ
    """
    visiblePanels = cmds.getPanel(visiblePanels=True)
    modelPanels = cmds.getPanel(type="modelPanel")
    visibleAndModelPanels = [value for value in modelPanels if value in visiblePanels]
    return visibleAndModelPanels[0]


##########################################################
# Plug-in initialization.
##########################################################

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


def initializePlugin(mobject):
    ''' Initialize the plug-in when Maya loads it. '''
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.registerCommand(GluonMiniMapClass.kPluginCmdName,
                                GluonMiniMapClass.cmdCreator)
    except:
        sys.stderr.write('Failed to register command: ' + GluonMiniMapClass.kPluginCmdName)


def uninitializePlugin(mobject):
    ''' Uninitialize the plug-in when Maya un-loads it. '''
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(GluonMiniMapClass.kPluginCmdName)
    except:
        sys.stderr.write('Failed to unregister command: ' + GluonMiniMapClass.kPluginCmdName)


