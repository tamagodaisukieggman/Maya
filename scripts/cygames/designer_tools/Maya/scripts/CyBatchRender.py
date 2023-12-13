# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   Author: Hideyo Isayama
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.mel as mel
import os.path
import random, string
import subprocess

#-------------------------------------------------------------------------------------------
#   実行
#-------------------------------------------------------------------------------------------
def Execute(filePath):

        if os.path.exists(filePath) == False:
            print "Info file do not exist !"
            return

        #レンダリング情報の取得
        renderInfoList = ReadFile(filePath)

        if len(renderInfoList) == 0:
            print "Cannot get any Render Info !"
            return

        for renderInfo in renderInfoList:

            if renderInfo == None:
                continue
            
            renderInfo.SaveTempFile()
            renderInfo.CreateRenderString()

            print "To create RenderInfo about " + renderInfo.tempFileName + " succeeded !"

        #レンダリングテキストの作成
        settingInfo = SettingInfo()
        
        renderStrList = []
        renderStrList.append("cd " + settingInfo.mayaBin)

        renderIndex = 0
        for renderInfo in renderInfoList:

            if renderInfo == None:
                continue

            if renderInfo.renderString != "":
                #renderStrList.append("echo " + renderInfo.fileName + " " + renderInfo.id + " Rendering...")
                renderStrList.append(renderInfo.renderString)
                renderIndex += 1
                
            elif renderInfo.renderStringList != []:

                for renderString in renderInfo.renderStringList:
                    renderStrList.append(renderString)
                    renderIndex += 1

        #renderStrList.append("echo Complete !")
        renderStrList.append("pause")

        finalRenderStr = ""
        for renderStr in renderStrList:
            finalRenderStr += renderStr + "\r\n"

        if renderIndex == 0:
            print "Cannot get any Render String !"
            return

        #レンダーファイルの書き込み
        renderTextPath = GetPathWithoutExt(filePath) + "_Render.bat"

        f = open(renderTextPath, 'w')
        f.write(finalRenderStr)
        f.close()

        return renderTextPath

#-------------------------------------------------------------------------------------------
#   ファイルの読み込み
#-------------------------------------------------------------------------------------------
def ReadFile(target):

    #セッティング関連変数設定
    settingStartStr = "****SETTING START****"
    settingEndStr = "****SETTING END****"

    renderStr = "Render:"
    paddingStr = "Padding:"
    formatStr = "Format:"
    useMaskStr = "UseMask:"
    useDepthStr = "UseDepth:"
    animExtStr = "AnimationExt:"

    settingStart = False

    #レンダリング関連変数設定
    startStr = "****RENDER START****"
    endStr = "****RENDER END****"
    inputRootStr = "InputRoot:"
    outputRootStr = "OutputRoot:"
    lightStr = "DefaultLight:"
    defaultFileStr = "DefaultFile:"
    fileStr = "File:"
    
    renderStart = False
    renderInfoIndex = 0
    
    inputRoot = ""
    tempRoot = ""
    outputRoot = ""
    defaultFileName = ""
    
    settingInfo = SettingInfo()
    lightList = []
    renderInfoList = []

    #ファイルの読み込み
    f = open(target)
    data = f.read()
    f.close()
     
    lineList = data.split("\r\n")
    for line in lineList:

        if line[:2] == "//":
            continue

        if line.find(startStr) >= 0:

            renderStart = True
            inputRoot = ""
            outputRoot = ""
            renderInfoIndex = 0
            lightList = []

        elif line.find(inputRootStr) >= 0 and renderStart:

            inputRoot = GetBatchValue(line,inputRootStr)
            inputRoot = inputRoot.replace("\\","/")

            if os.path.exists(inputRoot):

                tempRoot = inputRoot + "/ForCyBatchRender"

                if not os.path.exists(tempRoot):

                    os.mkdir(tempRoot)
                
            else:
                    
                renderStart = False

        elif line.find(outputRootStr) >= 0 and renderStart:

            outputRoot = GetBatchValue(line,outputRootStr)
            outputRoot = outputRoot.replace("\\","/")

            if not os.path.exists(outputRoot):
                    
                renderStart = False

        elif line.find(lightStr) >= 0 and renderStart:

            lightName = GetBatchValue(line,lightStr)

            lightList.append(lightName)

        elif line.find(defaultFileStr) >= 0 and renderStart:

            defaultFileName = GetBatchValue(line,defaultFileStr)

        elif line.find(fileStr) >= 0 and renderStart:

            newRenderInfo = RenderInfo()
            
            newRenderInfo.setting = settingInfo

            newRenderInfo.defaultFileName = defaultFileName
            newRenderInfo.inputRoot = inputRoot
            newRenderInfo.tempRoot = tempRoot
            newRenderInfo.outputRoot = outputRoot

            newRenderInfo.ReadInfo(line,renderInfoIndex)

            if newRenderInfo.enable == True:

                #デフォルトライトの追加
                for light in lightList:
                    newRenderInfo.lightList.append(light)
                
                renderInfoList.append(newRenderInfo)

            renderInfoIndex += 1

        elif line.find(endStr) >= 0:

            renderStart = False
            
        elif line.find(settingStartStr) >= 0:
            settingStart = True

        elif line.find(renderStr) >= 0 and settingStart:
            settingInfo.render = GetBatchValue(line,renderStr)

        elif line.find(paddingStr) >= 0 and settingStart:
            settingInfo.padding = float(GetBatchValue(line,paddingStr))

        elif line.find(formatStr) >= 0 and settingStart:
            settingInfo.format = GetBatchValue(line,formatStr)
            
        elif line.find(useMaskStr) >= 0 and settingStart:
            settingInfo.useMask = float(GetBatchValue(line,useMaskStr))

        elif line.find(useDepthStr) >= 0 and settingStart:
            settingInfo.useDepth = float(GetBatchValue(line,useDepthStr))

        elif line.find(animExtStr) >= 0 and settingStart:
            settingInfo.animExt = float(GetBatchValue(line,animExtStr))

        elif line.find(settingEndStr) >= 0:
            settingStart = False

    return renderInfoList
    

#-------------------------------------------------------------------------------------------
#   シェープノードを取得
#-------------------------------------------------------------------------------------------
def GetShapeNode(target):

    target = GetFirstNode(target)

    if target == None:
        return None

    shapeNodes = cmds.listRelatives( target, s=True, f=True )

    if shapeNodes == None:
        return None

    if len(shapeNodes) == 0:
        return None

    return shapeNodes[0]

#-------------------------------------------------------------------------------------------
#   シェープからトランスフォームを取得
#-------------------------------------------------------------------------------------------
def GetTransformNode( shape ):

    shape = GetFirstNode(shape)

    if shape == None:
        return None

    transform = cmds.listRelatives( shape, p=True, f=True )

    if transform == None:
        return None
    
    if len(transform) == 0: 
        return None
 
    return transform[0]

#-------------------------------------------------------------------------------------------
#   カメラのレンダーを全てOFFにする関数
#-------------------------------------------------------------------------------------------
def DisableCameraRenderable():

    camList = cmds.ls(type = "camera")

    if camList == None:
        return

    if len(camList) == 0:
        return

    for cam in camList:

        cmds.setAttr(cam + ".renderable",0)

#-------------------------------------------------------------------------------------------
#   ライト全てOFFにする関数
#-------------------------------------------------------------------------------------------
def DisableLight():

    lightShapeList = cmds.ls(type = "light")

    if lightShapeList == None:
        return

    if len(lightShapeList) == 0:
        return

    for lightShape in lightShapeList:

        transform = GetTransformNode(lightShape)

        if transform == None:
            continue

        cmds.setAttr(transform + ".visibility",0)

#-------------------------------------------------------------------------------------------
#   親までさかのぼってレイヤーを探す関数
#-------------------------------------------------------------------------------------------
def GetParentLayer(target):

    result = None

    thisTarget = GetFirstNode(target)

    layerList = cmds.listConnections(thisTarget,type = "displayLayer")

    if layerList != None and layerList != []:

        result = layerList[0]

    else:

        transform = cmds.listRelatives( thisTarget, p=True, f=True )

        if transform != None and transform != []:

            thisLayer = GetParentLayer(transform[0])

            if thisLayer != None:

                result = thisLayer

    return result

#-------------------------------------------------------------------------------------------
#   親までさかのぼってレイヤーを探す関数
#-------------------------------------------------------------------------------------------
def GetFirstNode(target):

    result = None

    targetList = cmds.ls(target,fl=True)

    if targetList == None or targetList == []:
        return result

    result = targetList[0]

    return result


#-------------------------------------------------------------------------------------------
#   ランダムな文字列を取得する関数
#-------------------------------------------------------------------------------------------
def GetRandomString(length):
    number = '0123456789'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    result = ''
    for i in range(0,length,2):
        result += random.choice(number)
        result += random.choice(alpha)
    return result

    

#-------------------------------------------------------------------------------------------
#   バッチ用の値を取得する関数
#-------------------------------------------------------------------------------------------
def GetBatchValue(target,replaceStr):

    result = target.replace(replaceStr,"")
    result = result.replace("\t","")
    result = result.replace("\r","")
    result = result.replace("\n","")
    result = result.replace(" ","")

    return result

#-------------------------------------------------------------------------------------------
#   拡張子なしのファイル名を取得
#-------------------------------------------------------------------------------------------
def GetNameWithoutExt(target):

    splitStr = target.split("/")

    baseName = splitStr[len(splitStr) - 1]

    result = baseName.split(".")[0]

    return result

#-------------------------------------------------------------------------------------------
#   拡張子なしのパス名を取得
#-------------------------------------------------------------------------------------------
def GetPathWithoutExt(target):

    baseName = target

    result = baseName.split(".")[0]

    return result


    

#-------------------------------------------------------------------------------------------
#   セッティングクラス
#-------------------------------------------------------------------------------------------
class SettingInfo():

    def __init__(self):

        self.render = "sw"
        self.padding = -1
        self.frameStep = -1
        self.format = ""
        self.useMask = -1
        self.useDepth = -1
        self.animExt = -1

        self.maya2013_64Root = "C:/Program Files/Autodesk/Maya2013"
        self.maya20135_64Root = "C:/Program Files/Autodesk/Maya2013.5"
        self.maya2015 = "C:/Program Files/Autodesk/Maya2015"
        self.maya2017 = "C:/Program Files/Autodesk/Maya2017"
        self.maya2018 = "C:/Program Files/Autodesk/Maya2018"

        self.mayaRoot = ""
        self.mayaBin = ""
        self.mayaExe = ""
        self.mayaRender = ""

        self.Initialize()

    def Initialize(self):

        if os.path.exists(self.maya20135_64Root):

            self.mayaRoot = self.maya20135_64Root
            
        elif os.path.exists(self.maya2013_64Root):

            self.mayaRoot = self.maya2013_64Root

        elif os.path.exists(self.maya2015):
    
            self.mayaRoot = self.maya2015

        elif os.path.exists(self.maya2017):
        
            self.mayaRoot = self.maya2017

        elif os.path.exists(self.maya2018):
        
            self.mayaRoot = self.maya2018

        if self.mayaRoot != "":

            self.mayaBin = self.mayaRoot + "/bin"
            self.mayaExe = self.mayaRoot + "/bin/maya.exe"
            self.mayaRender = self.mayaRoot + "/bin/Render.exe"

#-------------------------------------------------------------------------------------------
#   レンダー情報クラス
#-------------------------------------------------------------------------------------------
class RenderInfo():

    #-------------------------------
    #   コンストラクタ
    #-------------------------------
    def __init__(self):

        self.id = ""

        self.defaultFileName = ""

        self.fileName = ""
        self.fullPath = ""
        self.inputRoot = ""

        self.tempRoot = ""
        self.tempFileName = ""
        self.tempFullPath = ""
        
        self.outputRoot = ""
        self.outputPath = ""

        self.prefix = ""

        self.width = -1
        self.height = -1
        
        self.startFrame = -1
        self.startFrameList = []
        self.endFrame = -1
        self.endFrameList = []
        self.frameStep = -1
        self.startExt = -1
        self.byExt = -1
        
        self.cameraName = ""
        self.lightName = ""

        self.lightList = []

        self.renderString = ""
        self.renderStringList = []

        self.setting = None

        self.enable = False

    #-------------------------------
    #   情報の読み取り
    #-------------------------------
    def ReadInfo(self,info,index):

        idStr = "ID:"
        fileStr = "File:"
        widthStr = "Width:"
        heightStr = "Height:"
        StartStr = "Start:"
        EndStr = "End:"
        stepStr = "Step:"
        startExtStr = "StartExt:"
        byExtStr = "ByExt:"
        CameraStr = "Camera:"
        OutputStr = "Output:"
        prefixStr = "Prefix:"
        lightStr = "Light:"
        self.enable = False

        lineList = info.split("#")
        for line in lineList:

            if line.find(idStr) >= 0:

                self.id = GetBatchValue(line,idStr)

            elif line.find(fileStr) >= 0:

                self.fileName = GetBatchValue(line,fileStr)
                
                thisFullPath = self.inputRoot + "/" + self.fileName

                if os.path.exists(thisFullPath) and self.fileName != "":

                    self.fullPath = thisFullPath
                    self.enable = True

                else:
                    
                    defaultFullPath = self.inputRoot + "/" + self.defaultFileName

                    if os.path.exists(defaultFullPath) and self.defaultFileName != "":
                        self.fileName = self.defaultFileName
                        self.fullPath = defaultFullPath
                        self.enable = True
                    else:
                        print "File " + thisFullPath + " or " + defaultFullPath + " do not exist !"
                        self.enable = False

            elif line.find(widthStr) >= 0:

                self.width = float(GetBatchValue(line,widthStr))

            elif line.find(heightStr) >= 0:

                self.height = float(GetBatchValue(line,heightStr))
                
            elif line.find(StartStr) >= 0:

                startFrameStr = GetBatchValue(line,StartStr);

                if startFrameStr.find(",") >= 0:
                    
                    self.startFrameList = []
                    self.endFrameList = []

                    tempStrip0 = startFrameStr.split(",")

                    for temp0 in tempStrip0:

                        tempStrip1 = temp0.split("-")

                        if len(tempStrip1) >= 2: 
                            self.startFrameList.append(float(tempStrip1[0]))
                            self.endFrameList.append(float(tempStrip1[1]))
                        else:
                            self.startFrameList.append(float(tempStrip1[0]))
                            self.endFrameList.append(float(tempStrip1[0]))
                    
                else:
                    self.startFrame = float(startFrameStr)

            elif line.find(EndStr) >= 0:

                self.endFrame = float(GetBatchValue(line,EndStr))

            elif line.find(stepStr) >= 0:

                self.frameStep = float(GetBatchValue(line,stepStr))

            elif line.find(startExtStr) >= 0:

                self.startExt = float(GetBatchValue(line,startExtStr))

            elif line.find(byExtStr) >= 0:

                self.byExt = float(GetBatchValue(line,byExtStr))

            elif line.find(CameraStr) >= 0:

                self.cameraName = GetBatchValue(line,CameraStr)

            elif line.find(lightStr) >= 0:

                lightName = GetBatchValue(line,lightStr)

                self.lightList.append(lightName)

            elif line.find(OutputStr) >= 0:

                self.outputPath = self.outputRoot + "/" + GetBatchValue(line,OutputStr)

                if not os.path.exists(self.outputRoot):
                    print "Cannot create output path ! " + self.outputPath
                    self.enable = False

            elif line.find(prefixStr) >= 0:
                
                self.prefix = GetBatchValue(line,prefixStr)

        if self.enable == False:
            return

        self.tempFileName = GetNameWithoutExt(self.fileName)

        if self.id == "":
            self.id = str(index)

        self.tempFileName += "_" + self.id + ".mb"
            
        self.tempFullPath = self.tempRoot + "/" + self.tempFileName
        
        if self.prefix == "":
            self.prefix = GetNameWithoutExt(self.fileName)

        #出力フォルダの作成
        if not os.path.exists(self.outputPath):
            os.mkdir(self.outputPath)
            

    #-------------------------------
    #   設定を記録した一時ファイル保存
    #-------------------------------
    def SaveTempFile(self):

        if self.enable == False:
            return

        #if os.path.exists(self.tempFullPath):
            #cmds.file(self.tempFullPath,f=True,o=True)
        #else:
        cmds.file(self.fullPath,f=True,o=True)

        #カメラ、ライトの無効化
        DisableCameraRenderable()
        DisableLight()

        #カメラ設定
        if cmds.objExists(self.cameraName):

            cameraShape = GetShapeNode(self.cameraName)

            if cameraShape == None:
                temp = 0

            cmds.setAttr(cameraShape + ".renderable",1)
            cmds.setAttr(cameraShape + ".image",1)

            if self.setting.useMask == 0 or self.setting.useMask == 1:
                cmds.setAttr(cameraShape + ".mask",self.setting.useMask)

            if self.setting.useDepth == 0 or self.setting.useDepth == 1:
                cmds.setAttr(cameraShape + ".depth",self.setting.useDepth)

        #ライト設定
        if len(self.lightList) != 0:

            for light in self.lightList:

                if not cmds.objExists(light):
                    continue

                cmds.setAttr(light + ".visibility",1)

                #ライトが絡むレイヤーを可視化
                thisLayer = GetParentLayer(light)
                if thisLayer != None:
                    cmds.setAttr(thisLayer + ".visibility",1)

    
        
        #解像度設定
        if self.width != -1:
            cmds.setAttr("defaultResolution.aspectLock",0)
            cmds.setAttr("defaultResolution.width",self.width)

        if self.height != -1:
            cmds.setAttr("defaultResolution.aspectLock",0)
            cmds.setAttr("defaultResolution.height",self.height)


        #アニメーション設定
        cmds.setAttr("defaultRenderGlobals.animation",1);

        if self.startFrame != -1:
            cmds.setAttr("defaultRenderGlobals.startFrame",self.startFrame)
            cmds.playbackOptions(ast=self.startFrame,min=self.startFrame)

        if self.endFrame != -1:
            cmds.setAttr("defaultRenderGlobals.endFrame",self.endFrame)
            cmds.playbackOptions(aet=self.endFrame,max=self.endFrame)

        if self.frameStep != -1:
            cmds.setAttr("defaultRenderGlobals.byFrameStep",self.frameStep)

        
        #連番設定
        if self.setting.padding > 0:
            cmds.setAttr("defaultRenderGlobals.extensionPadding",self.setting.padding)
            
        if self.startExt != -1:
            cmds.setAttr("defaultRenderGlobals.modifyExtension",1)
            cmds.setAttr("defaultRenderGlobals.startExtension",self.startExt)

        if self.byExt != -1:
            cmds.setAttr("defaultRenderGlobals.modifyExtension",1)
            cmds.setAttr("defaultRenderGlobals.byExtension",self.byExt)

        #フォーマット設定
        cmds.setAttr("defaultRenderGlobals.imageFormat",32)

        #プリフィックス設定
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix",self.prefix,type="string")

        #MBファイルの保存
        cmds.file(rename=self.tempFullPath )
        cmds.file(f=True,save=True,options="v=0;",type="mayaBinary")
        cmds.file(f=True,new=True)

    #-------------------------------
    #   レンダリング
    #-------------------------------
    def CreateRenderString(self):

        self.renderString = ""
        self.renderStringList = []

        if not os.path.exists(self.setting.mayaRender):
           return

        if self.enable == False:
            return

        if self.startFrameList == []:

            self.renderString = "Render"

            self.renderString += self.GetDefaultRenderString()

        else:

            sumFrame = 0
            for i in range(0,len(self.startFrameList)):

                startFrame = self.startFrameList[i]
                endFrame = self.endFrameList[i]

                renderString = "Render"

                renderString += " -s " + str(startFrame)
                renderString += " -e " + str(endFrame)
                renderString += " -rfs " + str(i + self.startExt + sumFrame)
                renderString += " -rfb " + str(1)

                renderString += self.GetDefaultRenderString()

                self.renderStringList.append(renderString)

                sumFrame += self.endFrameList[i] - self.startFrameList[i]

                


    #-------------------------------------------------------------------------------------------
    #   共通レンダ文字列を追加
    #-------------------------------------------------------------------------------------------
    def GetDefaultRenderString(self):

        result = ""

        if self.setting.render != "":
            result += " -r " + self.setting.render
        else:
            result += " -r sw"
            
        result += " -rd " + self.outputPath

        if self.setting.animExt != -1:
            result += " -fnc " + str(int(self.setting.animExt))
        else:
            result += " -fnc 6"

        if self.setting.format != "":
            result += " -of " + self.setting.format
        else:
            result += " -of png"
        
        result += " " + self.tempFullPath

        return result
        
    
