#-------------------------------------------------------------------------------------------
#   TkgUnityCameraImporter
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.mel as mel

import os
import math

import TkgCommon.TkgUtility
import TkgCommon.TkgSetting

from TkgCommon.TkgUtility import TkgUtility
from TkgCommon.TkgSetting import TkgSetting

from xml.dom import minidom, Node

g_main = None

#-------------------------------------------------------------------------------------------
#   更新
#-------------------------------------------------------------------------------------------
def Execute():

    global g_main

    if g_main == None:
        g_main = Main()

    g_main.CreateUI()

#*****************************************************************
# メイン
#*****************************************************************
class Main():

    #===========================================
    # __init__
    #===========================================
    def __init__(self):

        self.version = "0.1.0"
        self.toolName = "TkgUnityCameraImporter"
        self.scriptPrefix = self.toolName + "."
        self.uiPrefix = self.toolName + "UI_"
        self.windowName = self.toolName + "Win"

        self.setting = TkgSetting(self.toolName)

        self.color00 = [0.5,0.5,0.5]
        self.color01 = [0.5,0.7,0.5]
        self.color02 = [0.7,0.5,0.5]

        self.defaultCameraName = "UnityCameraDataGroup"

        self.targetCameraRoot = ""

        self.targetCamera = ""
        self.targetCameraShape = ""

        self.targetCameraAim = ""
        self.targetCameraUp = ""

        self.cameraKeyList = []

        self.fps = 30

        self.multiplyValue = 100
        self.xmlPath = ""

    #===========================================
    # UI作成
    #===========================================
    def CreateUI(self):

        width=300
        height=1
        formWidth=width-5

        TkgUtility.CheckWindow(self.windowName)

        cmds.window( self.windowName, title=self.toolName, wh=(width, height) ,s=True,mnb=True,mxb=True,rtf=False)

        cmds.columnLayout(adjustableColumn=True)
        
        cmds.scrollLayout(self.uiPrefix + "LayerScrollList",verticalScrollBarThickness=5, cr=True)

        cmds.columnLayout(adjustableColumn=True)

        cmds.text(label=u"カメラXmlパス", al="left")
        cmds.textField(self.uiPrefix + "_CameraXml", text="", cc=self.ChangeValue)
        cmds.button( label=u"Unityカメラxml選択", bgc=self.color01 , h=30, command=self.SelectCameraXml)
        
        cmds.separator( h=20, style="in" )

        cmds.text(label=u"移動値倍率", al="left")
        cmds.floatField(self.uiPrefix + "_MultiplyValue", value=100, cc=self.ChangeValue)

        cmds.separator( h=20, style="in" )
        
        cmds.button( label=u"カメラ作成", bgc=self.color02 , h=30, command=self.CreateCamera)

        cmds.setParent( ".." )

        cmds.setParent( ".." )
        cmds.setParent( ".." )
     
        cmds.showWindow(self.windowName)

        self.LoadSetting()

    #===========================================
    # 値変化時
    #===========================================
    def ChangeValue(self,temp):

        self.SaveSetting()

    #===========================================
    # ロード
    #===========================================
    def LoadSetting(self):

        self.xmlPath = self.setting.Load("XmlPath")
        self.multiplyValue = self.setting.Load("MultiplyValue","float")

        if self.multiplyValue == 0:
            self.multiplyValue = 100

        cmds.textField(self.uiPrefix + "_CameraXml", e=True, text=self.xmlPath)
        cmds.floatField(self.uiPrefix + "_MultiplyValue", e=True, v=self.multiplyValue)

    #===========================================
    # 保存
    #===========================================
    def SaveSetting(self):

        self.xmlPath = cmds.textField(self.uiPrefix + "_CameraXml", q=True, text=True)
        self.multiplyValue = cmds.floatField(self.uiPrefix + "_MultiplyValue", q=True, v=True)

        self.setting.Save("XmlPath",self.xmlPath)
        self.setting.Save("MultiplyValue",self.multiplyValue)

        self.LoadSetting()

    #===========================================
    # FPS更新
    #===========================================
    def UpdateFPS(self):

        thisFpsType = cmds.currentUnit(q=True,time=True)

        if thisFpsType == "ntsc":
            self.fps = 30
        elif thisFpsType == "film":
            self.fps = 24
        elif thisFpsType == "ntscf":
            self.fps = 60
        else:
            self.fps = 30

    #===========================================
    # カメラXmlを選択
    #===========================================
    def SelectCameraXml(self, temp):

        targetList = cmds.fileDialog2(fileFilter="*.xml", dialogStyle=2,fileMode=1)

        if len(targetList) == 0:
            return

        cmds.textField(self.uiPrefix + "_CameraXml", e=True, text=targetList[0])

        self.SaveSetting()

    #===========================================
    # カメラ作成
    #===========================================
    def CreateCamera(self, temp):
        self.SaveSetting()

        mel.eval("CreateCameraAimUp")

        cameraList = cmds.ls(sl=True,l=True,fl=True)

        self.targetCamera = cameraList[0]
        self.targetCameraShape = self.targetCamera + "|" + cmds.listRelatives(self.targetCamera ,shapes=True)[0]
        self.targetCameraUp = cameraList[1]
        self.targetCameraAim = cameraList[2]

        self.targetCameraRoot = cmds.listRelatives(self.targetCamera,p=True,f=True)[0]
        
        self.CreaateCameraKeyList()

        self.UpdateCamera()
        
    #===========================================
    # カメラ作成
    #===========================================
    def CreaateCameraKeyList(self):

        self.cameraKeyList = []
        self.UpdateFPS()

        xmlPath = cmds.textField(self.uiPrefix + "_CameraXml", q=True, text=True)

        if os.path.exists(xmlPath) == False:
            return

        doc = minidom.parse(xmlPath)

        rootNode = doc.getElementsByTagName("UnityCameraData")[0]

        parentNode = rootNode.getElementsByTagName("DataList")[0]

        dataList = []
        for node in parentNode.childNodes:

            if node.nodeType != node.ELEMENT_NODE:
                continue

            dataList.append(node)

        for data in dataList:

            thisTime = self.GetAttrValue("Time", data)
            thisPosition = self.GetAttrValue("Position", data)
            thisRotation = self.GetAttrValue("Rotation", data)
            thisTargetPosition = self.GetAttrValue("TargetPosition", data)
            thisUpPosition = self.GetAttrValue("UpPosition", data)
            thisFov = self.GetAttrValue("FOV", data)

            newCameraKey = CameraKey(self)

            newCameraKey.time = float(thisTime)
            newCameraKey.position = self.GetListFromString(thisPosition)
            newCameraKey.rotation = self.GetListFromString(thisRotation)
            newCameraKey.targetPosition = self.GetListFromString(thisTargetPosition)
            newCameraKey.upPosition = self.GetListFromString(thisUpPosition)

            newCameraKey.fov = float(thisFov)
            newCameraKey.focalLength = self.GetFocalLength(newCameraKey.fov)

            newCameraKey.frame = newCameraKey.time * self.fps

            self.cameraKeyList.append(newCameraKey)

    #===========================================
    # カメラ作成
    #===========================================
    def UpdateCamera(self):

        for cameraKey in self.cameraKeyList:

            cameraKey.SetData()

    #===========================================
    # アトリビュート値を取得
    #===========================================
    def GetAttrValue(self, attrName, rootNode):

        for index in range(rootNode.attributes.length):

            item = rootNode.attributes.item(index)

            if item.name == attrName:
                return item.value
            
        return ""

    #===========================================
    # GetListFromString
    #===========================================
    def GetListFromString(self, target):

        target = target.replace("(","")
        target = target.replace(")","")

        splitStr = target.split(",")

        result = [0,0,0]

        result[0] = float(splitStr[0])
        result[1] = float(splitStr[1])
        result[2] = float(splitStr[2])

        return result

    #===========================================
    # GetFocalLength
    #===========================================
    def GetFocalLength(self, unityFov):

        vfa = cmds.getAttr(self.targetCameraShape + '.verticalFilmAperture')
        
        focalLength =(0.5 * vfa) / math.tan(unityFov/(2.0 * 57.29578)) / 0.03937

        return focalLength

#*****************************************************************
# CameraKey
#*****************************************************************
class CameraKey():

    #===========================================
    # __init__
    #===========================================
    def __init__(self, main):

        self.main = main

        self.time = 0

        self.frame = 0
        
        self.position = [0,0,0]
        self.rotation = [0,0,0]
        self.targetPosition = [0,0,0]
        self.upPosition = [0,0,0]

        self.fov = 0
        self.focalLength = 0

    #===========================================
    # SetData
    #===========================================
    def SetData(self):

        cmds.setKeyframe( self.main.targetCamera, v=-self.position[0] * self.main.multiplyValue, at="translateX", t=self.frame )
        cmds.setKeyframe( self.main.targetCamera, v=self.position[1] * self.main.multiplyValue, at="translateY", t=self.frame )
        cmds.setKeyframe( self.main.targetCamera, v=self.position[2] * self.main.multiplyValue, at="translateZ", t=self.frame )

        cmds.setKeyframe( self.main.targetCameraAim, v=-self.targetPosition[0] * self.main.multiplyValue, at="translateX", t=self.frame )
        cmds.setKeyframe( self.main.targetCameraAim, v=self.targetPosition[1] * self.main.multiplyValue, at="translateY", t=self.frame )
        cmds.setKeyframe( self.main.targetCameraAim, v=self.targetPosition[2] * self.main.multiplyValue, at="translateZ", t=self.frame )

        cmds.setKeyframe( self.main.targetCameraUp, v=-self.upPosition[0] * self.main.multiplyValue, at="translateX", t=self.frame )
        cmds.setKeyframe( self.main.targetCameraUp, v=self.upPosition[1] * self.main.multiplyValue, at="translateY", t=self.frame )
        cmds.setKeyframe( self.main.targetCameraUp, v=self.upPosition[2] * self.main.multiplyValue, at="translateZ", t=self.frame )

        cmds.setKeyframe( self.main.targetCameraShape, v=self.focalLength, at="focalLength", t=self.frame )
