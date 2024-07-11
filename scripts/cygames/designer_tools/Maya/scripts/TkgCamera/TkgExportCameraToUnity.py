# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   TkgExportCameraToUnity
#-------------------------------------------------------------------------------------------

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import gc
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

version = "1.0.0"
toolName = "TkgExportCameraToUnity"
scriptPrefix= toolName + "."
uiPrefix= toolName + "UI"

g_setting = TkgSetting(toolName)

#-------------------------------------------------------------------------------------------
#   メインUI
#-------------------------------------------------------------------------------------------
def UI():

    global scriptPrefix
    global uiPrefix
    global toolName
    global g_setting

    if g_setting == None:
        g_setting = TkgSetting(toolName)

    width=250
    height=1
    formWidth=width-5

    windowTitle=scriptPrefix.replace(".","")
    windowName=windowTitle+"Win"
    
    TkgUtility.CheckWindow(windowName)

    cmds.window( windowName, title=windowTitle, widthHeight=(width, height),s=1,mnb=True,mxb=False,rtf=True)

    cmds.columnLayout(adjustableColumn=True)
    
    cmds.textFieldGrp(uiPrefix + "ExportName", label='Export Name', text="md_camera000", cl2=("left","left"), ad2=2, cc=scriptPrefix+"SaveSetting()")
    cmds.textFieldGrp(uiPrefix + "ExportFolder", label='Export Folder', text="c:\Works", cl2=("left","left"), ad2=2, cc=scriptPrefix+"SaveSetting()")

    cmds.separator( style='in',h=15,w=formWidth)

    cmds.checkBox(uiPrefix + "ModelOnly", label="Export Model Only", cc=scriptPrefix+"SaveSetting()" )
    cmds.checkBox(uiPrefix + "ShowResultModel", label="Show Result Model", cc=scriptPrefix+"SaveSetting()", v=False)

    cmds.separator( style='in',h=15,w=formWidth)

    cmds.text( label="Cut Setting",al="left" )

    cmds.separator( style='none',h=10,w=formWidth)

    cmds.floatSliderGrp(uiPrefix + "DistDiffer", label='Distance Difference', field=True, minValue=1, maxValue=1000, fmn=1, fmx=1000, value=1, cw3=[100,50,0], cl3=["left","center","center"], cc=scriptPrefix+"SaveSetting()" )
    cmds.floatSliderGrp(uiPrefix + "AngleDiffer", label='Angle Difference', field=True, minValue=1, maxValue=1000, fmn=1, fmx=1000, value=1, cw3=[100,50,0], cl3=["left","center","center"], cc=scriptPrefix+"SaveSetting()" )
    cmds.floatSliderGrp(uiPrefix + "FovDiffer", label='Fov Difference', field=True, minValue=1, maxValue=1000, fmn=1, fmx=1000, value=1, cw3=[100,50,0], cl3=["left","center","center"], cc=scriptPrefix+"SaveSetting()" )

    cmds.separator( style='in',h=15,w=formWidth)
    
    cmds.button( label="Export",bgc=[0.8,0.5,0.5],command=scriptPrefix+"Export()")

    cmds.separator( style='in',h=15,w=formWidth)
    
    cmds.button( label="About",w=formWidth,command=scriptPrefix + "ShowAbout()")
 
    cmds.showWindow(windowName)

    LoadSetting()

#-------------------------------------------------------------------------------------------
#   Export
#-------------------------------------------------------------------------------------------
def Export():

    selectList = cmds.ls(sl=True);

    if selectList == None:
        return

    if len(selectList) != 1:
        return

    cameraTrans = selectList[0]

    if cmds.objectType( cameraTrans ) != "transform":
        return
    
    cameraShape = None
    nodeList = cmds.listRelatives( cameraTrans )

    for node in nodeList:

        if cmds.objectType( node ) == "camera":
            cameraShape = node
            break

    if cameraShape == None:
        return

    exportName = cmds.textFieldGrp(uiPrefix + "ExportName", q=True, text=True)
    exportFolder = cmds.textFieldGrp(uiPrefix + "ExportFolder", q=True, text=True)
    
    modelOnly = cmds.checkBox(uiPrefix + "ModelOnly", q=True, v=True)
    showModel = cmds.checkBox(uiPrefix + "ShowResultModel", q=True, v=True)

    distDiffer = cmds.floatSliderGrp(uiPrefix + "DistDiffer", q=True, v=True )
    angleDiffer = cmds.floatSliderGrp(uiPrefix + "AngleDiffer", q=True, v=True )
    fovDiffer = cmds.floatSliderGrp(uiPrefix + "FovDiffer", q=True, v=True )

    if os.path.exists(exportFolder) == False:
        return

    exportFullPath = exportFolder + "/" + exportName

    minFrame = int(cmds.playbackOptions(q=True,ast=True))
    maxFrame = int(cmds.playbackOptions(q=True,aet=True))

    if modelOnly == True:
        minFrame = 0
        maxFrame = 0

    if cmds.objExists("CameraRoot"):
        cmds.select("CameraRoot")
        cmds.delete()

    rootLocator = cmds.spaceLocator(n="CameraRoot",p=(0,0,0),a=True)[0];
    attachLocator = cmds.spaceLocator(n="Cam_Attach",p=(0,0,0),a=True)[0];
    fovLocator = cmds.spaceLocator(n="Cam_Fov",p=(0,0,0),a=True)[0];
    transLocator = cmds.spaceLocator(n="Cam_Translate",p=(0,0,0),a=True)[0];
    rotateLocator = cmds.spaceLocator(n="Cam_Rotate",p=(0,0,0),a=True)[0];

    cmds.parent(attachLocator, rootLocator)
    cmds.parent(transLocator, rootLocator)
    cmds.parent(rotateLocator, rootLocator)
    cmds.parent(fovLocator, rootLocator)

    if modelOnly == True:
        return

    for cnt in range(minFrame, maxFrame + 1):

        translate = cmds.getAttr(cameraTrans + '.translate', t=cnt)[0]
        rotate = cmds.getAttr(cameraTrans + '.rotate', t=cnt)[0]
        fov = GetFov(cameraTrans, cnt)
        
        cmds.setAttr( transLocator + ".translateX", translate[0])
        cmds.setAttr( transLocator + ".translateY", translate[1])
        cmds.setAttr( transLocator + ".translateZ", translate[2])

        cmds.setAttr( rotateLocator + ".translateX", rotate[0])
        cmds.setAttr( rotateLocator + ".translateY", rotate[1])
        cmds.setAttr( rotateLocator + ".translateZ", rotate[2])

        cmds.setAttr( fovLocator + ".translateX", fov)

        nextTranslate = cmds.getAttr(cameraTrans + '.translate', t=cnt + 1)[0]
        nextRotate = cmds.getAttr(cameraTrans + '.rotate', t=cnt + 1)[0]
        nextFov = GetFov(cameraTrans, cnt + 1)

        transDistance = GetDistance(translate,nextTranslate)
        rotDistance = GetDistance(rotate,nextRotate)

        rotDistX = math.fabs(nextRotate[0] - rotate[0])
        rotDistY = math.fabs(nextRotate[1] - rotate[1])
        rotDistZ = math.fabs(nextRotate[2] - rotate[2])
        
        fovDistance = math.fabs(nextFov - fov)

        isCut = False
        if transDistance > distDiffer:
            isCut = True

        if  rotDistX > angleDiffer:
            isCut = True

        if  rotDistY > angleDiffer:
            isCut = True

        if  rotDistZ > angleDiffer:
            isCut = True

        if fovDistance > fovDiffer:
            isCut = True

        currentFrame = cnt

        translate = cmds.getAttr(cameraTrans + '.translate', t=currentFrame)[0]
        rotate = cmds.getAttr(cameraTrans + '.rotate', t=currentFrame)[0]
        fov = GetFov(cameraTrans, cnt)

        cmds.setKeyframe( transLocator, v=translate[0], at='translateX', t=currentFrame )
        cmds.setKeyframe( transLocator, v=translate[1], at='translateY', t=currentFrame )
        cmds.setKeyframe( transLocator, v=translate[2], at='translateZ', t=currentFrame )

        cmds.setKeyframe( rotateLocator, v=rotate[0], at='translateX', t=currentFrame )
        cmds.setKeyframe( rotateLocator, v=rotate[1], at='translateY', t=currentFrame )
        cmds.setKeyframe( rotateLocator, v=rotate[2], at='translateZ', t=currentFrame )
        
        cmds.setKeyframe( fovLocator, v=fov, at='translateX', t=currentFrame )

        if isCut == True:

            cutFrame = currentFrame + 0.99

            cmds.setKeyframe( transLocator, v=translate[0], at='translateX', t=cutFrame )
            cmds.setKeyframe( transLocator, v=translate[1], at='translateY', t=cutFrame )
            cmds.setKeyframe( transLocator, v=translate[2], at='translateZ', t=cutFrame )

            cmds.setKeyframe( rotateLocator, v=rotate[0], at='translateX', t=cutFrame )
            cmds.setKeyframe( rotateLocator, v=rotate[1], at='translateY', t=cutFrame )
            cmds.setKeyframe( rotateLocator, v=rotate[2], at='translateZ', t=cutFrame )
            
            cmds.setKeyframe( fovLocator, v=fov, at='translateX', t=cutFrame )
                
        
    cmds.select(clear=True)
    cmds.select(rootLocator, add=True)
    cmds.select(hierarchy=True)

    ExportFbx(exportFullPath)

    if showModel == False:
        cmds.delete(rootLocator)

    cmds.select(cameraTrans,r=True)

#-------------------------------------------------------------------------------------------
#   ExportFBX
#-------------------------------------------------------------------------------------------
def ExportFbx(filePath):

    cmds.file(filePath, force=True,options="v=0;", typ="FBX export", pr=True, es=True)

#-------------------------------------------------------------------------------------------
#   GetFov
#-------------------------------------------------------------------------------------------
def GetFov(cameraShape, time):

    focalLength = cmds.getAttr(cameraShape + '.focalLength', t=time)
    vfa = cmds.getAttr(cameraShape + '.verticalFilmAperture', t=time)
    fov = 2.0 * math.atan((0.5 * vfa) / (focalLength * 0.03937)) * 57.29578

    return fov

#-------------------------------------------------------------------------------------------
#   Get distance
#-------------------------------------------------------------------------------------------
def GetDistance(src, dst):

    dist = math.pow(src[0] - dst[0],2) + math.pow(src[1] - dst[1],2) + math.pow(src[2] - dst[2],2)

    dist = math.sqrt(dist)

    return dist

#-------------------------------------------------------------------------------------------
#   Save Setting
#-------------------------------------------------------------------------------------------
def SaveSetting():

    global uiPrefix
    global g_setting

    exportName = cmds.textFieldGrp(uiPrefix + "ExportName",q=True,text=True)
    exportFolder = cmds.textFieldGrp(uiPrefix + "ExportFolder",q=True,text=True)

    modelOnly = cmds.checkBox(uiPrefix + "ModelOnly", q=True, v=True )

    distDiffer = cmds.floatSliderGrp(uiPrefix + "DistDiffer", q=True, v=True )
    angleDiffer = cmds.floatSliderGrp(uiPrefix + "AngleDiffer", q=True, v=True )
    fovDiffer = cmds.floatSliderGrp(uiPrefix + "FovDiffer", q=True, v=True )

    g_setting.Save("ExportName", exportName)
    g_setting.Save("ExportFolder", exportFolder)

    g_setting.Save("ModelOnly", modelOnly)

    g_setting.Save("DistDiffer",distDiffer)
    g_setting.Save("AngleDiffer",angleDiffer)
    g_setting.Save("FovDiffer",fovDiffer)

#-------------------------------------------------------------------------------------------
#   Load Setting
#-------------------------------------------------------------------------------------------
def LoadSetting():

    global uiPrefix
    global g_setting

    exportName = g_setting.Load("ExportName")
    exportFolder = g_setting.Load("ExportFolder")
    
    modelOnly = g_setting.Load("ModelOnly", "bool")

    distDiffer = g_setting.Load("DistDiffer", "float")
    angleDiffer = g_setting.Load("AngleDiffer", "float")
    fovDiffer = g_setting.Load("FovDiffer", "float")

    if distDiffer == 0:
        distDiffer = 100

    if angleDiffer == 0:
        angleDiffer = 100

    if fovDiffer == 0:
        fovDiffer = 100

    cmds.textFieldGrp(uiPrefix + "ExportName",e=True,text=exportName)
    cmds.textFieldGrp(uiPrefix + "ExportFolder",e=True,text=exportFolder)

    cmds.checkBox(uiPrefix + "ModelOnly", e=True, v=modelOnly )

    cmds.floatSliderGrp(uiPrefix + "DistDiffer", e=True, v=distDiffer )
    cmds.floatSliderGrp(uiPrefix + "AngleDiffer", e=True, v=angleDiffer )
    cmds.floatSliderGrp(uiPrefix + "FovDiffer", e=True, v=fovDiffer )
    
