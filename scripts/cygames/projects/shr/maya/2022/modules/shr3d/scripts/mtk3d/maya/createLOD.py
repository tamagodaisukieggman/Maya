# -*- coding: utf-8 -*-
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.cmds as cmds
import maya.mel as mel
import math


#---------------------------------------------
#createMaterial
#---------------------------------------------
def createMaterial(matName):
    retHash = {}
    lambertObj = cmds.shadingNode('lambert', asShader=True, name=matName)
    setObj = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    cmds.connectAttr( lambertObj+".outColor", setObj+".surfaceShader", force=True)
    retHash["lambertObj"] = lambertObj
    retHash["setObj"] = setObj
    return retHash
    
#---------------------------------------------
#connectMaterial
#---------------------------------------------
def connectMaterial(targetObj,lambertObj, setObj):
    #mel.eval('assignCreatedShader "'+lambertObj+'" "" '+setObj+' "'+targetObj+'";')
    cmds.select(targetObj) 
    mel.eval('sets -e -forceElement '+setObj+';')
    return lambertObj

def getMaterial(targetMat):
    retHash = {}
    retHash["lambertObj"] = targetMat
    retHash["setObj"] = cmds.listConnections( targetMat, destination=True, type="shadingEngine")[0]
    
    #print cmds.objectType( targetMat)
    print retHash
    return retHash


#---------------------------------------------
#existObject
#---------------------------------------------
def existObject(targetObj):
    return cmds.objExists(targetObj)


#---------------------------------------------
#createExportAssetTree
#---------------------------------------------
def createExportAssetTree(dataName, lodCount, lodValue, targetObj, keep_normal, materialFlag):
    lodObjArry = []
    
    matName_def = materialFlag + dataName 
    matName_low = materialFlag + dataName + "_low"
    
    #--------------------
    if existObject(matName_def) == True:
        mat_hi = getMaterial(matName_def)
    else:
        mat_hi = createMaterial(matName_def)
    
    if existObject(matName_low)== True:
        mat_low = getMaterial(matName_low)
    else:
        mat_low = createMaterial(matName_low)
        
        
    nTarget = ""
    
    keepQuadsWeight_value = cmds.floatSliderGrp("keepQuadsWeight", q=True, value=True)
    sharpness_value = cmds.floatSliderGrp("sharpness", q=True, value=True)

    for dupObjIndex in range(lodCount):
        newdataName = "mesh_"+dataName+"_"+str(dupObjIndex)
        dupObj = cmds.duplicate(targetObj, name=newdataName)
        cmds.showHidden(dupObj[0])
        reduceParam = lodValue[dupObjIndex]
        
        cmds.polyReduce(dupObj[0], ver=1, p=reduceParam, vct=0, tct=0, keepBorder=1, keepMapBorder=1, keepColorBorder=1, keepFaceGroupBorder=1, keepHardEdge=1, keepCreaseEdge=1, keepQuadsWeight=keepQuadsWeight_value, sharpness=sharpness_value, keepBorderWeight=0.5, keepMapBorderWeight=0.5, keepColorBorderWeight=0.5, keepFaceGroupBorderWeight=0.5, keepHardEdgeWeight=0.5 , keepCreaseEdgeWeight=0.5)
        
        if keep_normal:
            if dupObjIndex == 0:
                cmds.transferAttributes(targetObj, dupObj[0], transferPositions=0, transferNormals=1, transferUVs=0, transferColors=0, sampleSpace=0, sourceUvSpace="map1", targetUvSpace="map1", searchMethod=3, flipUVs=0, colorBorders=1)
            else:
                cmds.transferAttributes(targetObj, nTarget, transferPositions=0, transferNormals=1, transferUVs=0, transferColors=0, sampleSpace=0, sourceUvSpace="map1", targetUvSpace="map1", searchMethod=3, flipUVs=0, colorBorders=1)
        nTarget = dupObj[0]
        
        parentCheck = cmds.listRelatives(dupObj[0], parent=True)
        if parentCheck != None:
            cmds.parent(dupObj[0], w=True)
        #--------------------
        #print dupObj[0], mat_hi["lambertObj"], mat_hi["setObj"]
        #--------------------
        
  
        if dupObjIndex == lodCount -1:
            print "LowMat----"+dupObj[0]+"----"+str(dupObjIndex) + "----------" + str(lodCount -1)
            connectMaterial(dupObj[0], mat_low["lambertObj"], mat_low["setObj"])
            if (lodCount -1) == 0:
                print "HighMat----"+dupObj[0]+"----"+str(dupObjIndex) + "----------" + str(lodCount -1)
                connectMaterial(dupObj[0], mat_hi["lambertObj"], mat_hi["setObj"])

        else:
            print "HighMat----"+dupObj[0]+"----"+str(dupObjIndex) + "----------" + str(lodCount -1)
            connectMaterial(dupObj[0], mat_hi["lambertObj"], mat_hi["setObj"])
        lodObjArry.append(dupObj[0])
    #--------------------
    #print lodObjArry
    #--------------------
    cmds.select(lodObjArry)
    cmds.LevelOfDetailGroup()
    lodRoot = cmds.ls(selection=True)[0]
    cmds.rename(lodRoot, dataName)
    mel.eval('DeleteHistory;')
    

#----------------------------------------------------------
#
#----------------------------------------------------------  
def getLodValHash():
    retHash = {}
    retHash[0]= cmds.intSliderGrp("LOD_0", q=True, value=True)
    retHash[1]= cmds.intSliderGrp("LOD_1", q=True, value=True)
    retHash[2]= cmds.intSliderGrp("LOD_2", q=True, value=True)
    retHash[3]= cmds.intSliderGrp("LOD_3", q=True, value=True)
    retHash[4]= cmds.intSliderGrp("LOD_4", q=True, value=True)
    return retHash
    
def targetName():
    return cmds.textFieldButtonGrp("targetName", q=True, text=True)
    
    
def rootName():
    return cmds.textFieldButtonGrp("rootName", q=True, text=True)
    
def setSelName():
    selObj = cmds.ls(selection=True)[0]
    print selObj
    cmds.textFieldButtonGrp("targetName", e=True, text=selObj)
    
def setRoot():
    selObj = cmds.ls(selection=True)[0]
    print selObj
    cmds.textFieldButtonGrp("rootName", e=True, text=selObj)
    
def getCopyNormalValue():
    copyNormalVal = cmds.checkBox("copyOriginalNormal", q=True, value=True)
    return copyNormalVal

    
def getLodCount():
    return cmds.intSliderGrp ("LOD_Count", q=True, value=True)

def activeSlider():
    nowValue = cmds.intSliderGrp ("LOD_Count", q=True, value=True) - 1
    print nowValue
    if nowValue == 0:
        cmds.intSliderGrp ("LOD_0", e=True, enable=True)
        cmds.intSliderGrp ("LOD_1", e=True, enable=False)
        cmds.intSliderGrp ("LOD_2", e=True, enable=False)
        cmds.intSliderGrp ("LOD_3", e=True, enable=False)
        cmds.intSliderGrp ("LOD_4", e=True, enable=False)
    if nowValue == 1:
        cmds.intSliderGrp ("LOD_0", e=True, enable=True)
        cmds.intSliderGrp ("LOD_1", e=True, enable=True)
        cmds.intSliderGrp ("LOD_2", e=True, enable=False)
        cmds.intSliderGrp ("LOD_3", e=True, enable=False)
        cmds.intSliderGrp ("LOD_4", e=True, enable=False)
    if nowValue == 2:
        cmds.intSliderGrp ("LOD_0", e=True, enable=True)
        cmds.intSliderGrp ("LOD_1", e=True, enable=True)
        cmds.intSliderGrp ("LOD_2", e=True, enable=True)
        cmds.intSliderGrp ("LOD_3", e=True, enable=False)
        cmds.intSliderGrp ("LOD_4", e=True, enable=False)        
    if nowValue == 3:
        cmds.intSliderGrp ("LOD_0", e=True, enable=True)
        cmds.intSliderGrp ("LOD_1", e=True, enable=True)
        cmds.intSliderGrp ("LOD_2", e=True, enable=True)
        cmds.intSliderGrp ("LOD_3", e=True, enable=True)
        cmds.intSliderGrp ("LOD_4", e=True, enable=False)        
    if nowValue == 4:
        cmds.intSliderGrp ("LOD_0", e=True, enable=True)
        cmds.intSliderGrp ("LOD_1", e=True, enable=True)
        cmds.intSliderGrp ("LOD_2", e=True, enable=True)
        cmds.intSliderGrp ("LOD_3", e=True, enable=True)
        cmds.intSliderGrp ("LOD_4", e=True, enable=True)

        
#----------------------------------------------------------
#dataName = "smesh02_046_a"
#lodCount = 5
#keep_normal = True
#materialFlag = "mtl_"
#targetObj = cmds.ls(selection=True)
#lodValue = {0:0, 1:50, 2:75, 3:80, 4:95, 5:95}

#createExportAssetTree(dataName, lodCount, lodValue, targetObj, keep_normal, materialFlag)
#----------------------------------------------------------
def selTarget():
    selValue = cmds.ls(selection=True)
    selValueLen = len(selValue)
    if selValueLen != 0:
        cmds.textFieldButtonGrp("targetName", e=True, text=selValue[0])





def createLOD_Window():
    cmds.window(title='mutsunokami_env_structure_tool')
    cmds.columnLayout()
    cmds.intSliderGrp ("LOD_Count", field=True, label="LOD_Count", min=1, max=5, step=1, value=1, changeCommand='createLOD.activeSlider()')
    cmds.textFieldButtonGrp("targetName", label="target Mesh Name", text="targetObjectName", buttonLabel="set", buttonCommand='createLOD.setSelName()')
    cmds.textFieldButtonGrp("rootName", label="New Tree Name", text="rootName", buttonLabel="set", buttonCommand='createLOD.setRoot()')
    cmds.intSliderGrp ("LOD_0", field=True, label="LOD_0", min=0, max=99, step=1, value=0, enable=True)
    cmds.intSliderGrp ("LOD_1", field=True, label="LOD_1", min=0, max=99, step=1, value=50, enable=False)
    cmds.intSliderGrp ("LOD_2", field=True, label="LOD_2", min=0, max=99, step=1, value=80, enable=False)
    cmds.intSliderGrp ("LOD_3", field=True, label="LOD_3", min=0, max=99, step=1, value=90, enable=False)
    cmds.intSliderGrp ("LOD_4", field=True, label="LOD_4", min=0, max=99, step=1, value=95, enable=False)

    cmds.floatSliderGrp("keepQuadsWeight", field=True, label="keepQuadsWeight", min=0, max=1, step=0.01, value=0.0, enable=True)
    cmds.floatSliderGrp("sharpness", field=True, label="sharpness", min=0, max=1, step=0.01, value=1.0, enable=True)
    cmds.checkBox("copyOriginalNormal", label="copyOriginalNormal", value=False) 
    cmds.button(label='createLOD', command='dataName = createLOD.rootName();lodCountVal = createLOD.getLodCount(); lodCount = lodCountVal;materialFlag = "mtl_";targetObj = createLOD.targetName();lodValue = createLOD.getLodValHash(); keep_normal=createLOD.getCopyNormalValue();createLOD.createExportAssetTree(dataName, lodCount, lodValue, targetObj, keep_normal, materialFlag)')
    cmds.showWindow()
    selTarget()




