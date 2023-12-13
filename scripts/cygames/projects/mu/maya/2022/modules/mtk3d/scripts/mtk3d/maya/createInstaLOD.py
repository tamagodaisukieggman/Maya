# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya as maya
import os


def createInstaLODmesh(targetName, newName, percentage):
    maya.cmds.optionVar( q='INSTALOD_ID_OP_PERCENTTRIANGLES' );
    #maya.mel.eval("InstaLOD_ResetSettings(false);");
    maya.cmds.optionVar( sv=('INSTALOD_ID_OPTIMIZE_TYPE', "Optimize") ); 
    maya.cmds.optionVar( fv=('INSTALOD_ID_OP_PERCENTTRIANGLES', percentage) );
    maya.cmds.optionVar( sv=('INSTALOD_ID_OP_SHADINGIMPORTANCE', "Highest") );
    maya.cmds.optionVar( sv=('INSTALOD_ID_OP_SILHOUETTEIMPORTANCE', "High") );
    maya.cmds.optionVar( sv=('INSTALOD_ID_OP_SKINNINGIMPORTANCE', "Off") );
    targetMesh = '\"'+targetName+'\"'
    maya.mel.eval("InstaLOD_OptimizeMesh("+targetMesh+", \"\", false);");
    newMeshObj = cmds.ls(selection=True)
    newMeshObjArry = []
    for newobj in newMeshObj:
        newMeshName = cmds.rename(newobj, newName)
        if cmds.listRelatives( newMeshName, parent=True ) == None:
            thisData = newMeshName
        else:
            thisData = cmds.parent(newMeshName, w=True)[0]

        newMeshObjArry.append(thisData)
        print "lod mesh name is ---------", thisData
    return newMeshObjArry
    

def setRoot():
    selObj = cmds.ls(selection=True)[0]
    print selObj
    cmds.textFieldButtonGrp("target", e=True, text=selObj)

def valueActiv(sliderName):   
    enableValue = cmds.intSliderGrp (sliderName, q=True, enable=True)
    print sliderName, enableValue
    if enableValue == True:
        cmds.intSliderGrp(sliderName, e=True, enable=False)
    else:
        cmds.intSliderGrp(sliderName, e=True, enable=True)
        

def createInstaLODMesh_main(lodHash):
    InstaLodObjHash = {}
    for lodObj in lodHash:
        lodName = lodHash[lodObj]["name"]
        lodMeshName = lodHash[lodObj]["lodMeshName"]
        sliderName = lodName+"_slider"
        enableValue = cmds.intSliderGrp (sliderName, q=True, enable=True)
        sliderValue = cmds.intSliderGrp (sliderName, q=True, value=True)
        if enableValue == True:
            InstaLodObjHash[lodObj] = lodHash[lodObj]
    
    targetName = cmds.textFieldButtonGrp("target", q=True, text=True)
    cmds.select(targetName)
    targetMeshName = cmds.ls(selection=True)[0]
    meshArry = []
    count = 0

    for id in InstaLodObjHash:
        sModel = InstaLodObjHash[id]["name"]
        sPercent = InstaLodObjHash[id]["percent"]
        lodMeshName = InstaLodObjHash[id]["lodMeshName"]
        print sModel, sPercent
        InstaLodMeshArry = createInstaLODmesh(targetMeshName, "mesh_"+lodMeshName, sPercent) 
        newGroupName = cmds.group( em=True, w=True, name=lodMeshName )
        for InstaLodMeshName in InstaLodMeshArry:
            cmds.parent( InstaLodMeshName, newGroupName )
        
        meshArry.append(newGroupName)
        count += 1
    
    LODGroup = cmds.checkBox("LODGroup", q=True, value=True)
    if LODGroup == True:
        meshArry.sort()
        cmds.select(meshArry)
        cmds.LevelOfDetailGroup()
    else:
        cmds.select(meshArry)



def createInstaLOD_Window():
    maya.mel.eval("InstaLOD_MayaIntegration;");
    maya.mel.eval("InstaLOD;");

    lodHash = {2:{"name":"lod1","percent":85.0, "def":True, "lodMeshName":"lod1"},
    3:{"name":"lod2","percent":50.0, "def":True, "lodMeshName":"lod2"},
    4:{"name":"lod3","percent":25.0, "def":False, "lodMeshName":"lod3"},
    5:{"name":"lod4","percent":15.0, "def":False, "lodMeshName":"lod4"},
    6:{"name":"lod5","percent":10.0, "def":False, "lodMeshName":"lod5"},
    7:{"name":"lod6","percent":8.0, "def":False, "lodMeshName":"lod6"},
    8:{"name":"lod7","percent":5.0, "def":False, "lodMeshName":"lod7"}
    }
    
    columnWidthArry = []
    for lodObj in lodHash:
        columnWidthArry.append((1, 60))
    
    cmds.window(title='InstaLodLOD', width=150 )
    cmds.columnLayout()
    cmds.textFieldButtonGrp("target", label="target Name", text="target Name", buttonLabel="set", buttonCommand='createInstaLOD.setRoot()')
    maya.cmds.setParent('..')
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=columnWidthArry)
    
    for lodObj in lodHash:
        lodName = lodHash[lodObj]["name"]
        checkboxName = lodName+"_checkbox"
        sliderName = lodName+"_slider"
        lodPercent = lodHash[lodObj]["percent"]
        defValue = lodHash[lodObj]["def"]
        #print lodName, checkboxName, lodPercent
        cmds.checkBox(checkboxName, label="", value=defValue, changeCommand='createInstaLOD.valueActiv("'+sliderName+'")')
        cmds.intSliderGrp (sliderName, field=True, label=sliderName, min=0.0, max=100.0, step=1, value=lodPercent, enable=defValue)
    
    maya.cmds.setParent('..')
    cmds.columnLayout( adjustableColumn=True )
    cmds.button( label='createInstaLOD', align='left', command="createInstaLOD.createInstaLODMesh_main("+str(lodHash)+")")
    cmds.checkBox("LODGroup", label="LODGroup", value=False)
    maya.cmds.setParent('..')
    cmds.showWindow()
    




    