# -*- coding: utf-8 -*-
from __future__ import print_function
try:
    import maya.cmds as cmds
    import pymel.core as pm
except:
    pass

import json
import os
import re
import glob
import random

# from pipelinetools.set_physics_mat_tools import set_physics_mat_tools_ui as spmtu

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase):
    def application(self):
        return Application.Maya

    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        if asset.assetgroup == 'environment' and asset.task == 'model':
            return True
        else:
            return False

    def order(self):
        return 99

    def execute(self, args):
        # =====================================================================
        # set_physics_mat_toolsクラスをdeadlineで読むことができないので関数を移植
        # =====================================================================
        import sys
        print("maya_version >> "+str(sys.version))
        def getColor(attributeNames,materialName,colorType ="material"):
            def colorblender(colorA,colorB, percent):
                newColor = [0,0,0]
                for lp in range(0,3):
                    newColor[lp] = (colorA[lp]*(1.0 - percent))+(colorB[lp]*percent)
                return newColor
            
            def stringToNum(sourceStr):
                num = 0
                for lp in sourceStr:
                    num += ord(lp)
                return int(num)
            def getCurrentAttributeColor():
                if len(attributeNames) == 0:
                    return [0,0,0]
            
                _stackValue = 0
                for attributeName in attributeNames:
                    _stackValue+=stringToNum(attributeName)
                
                currentSeedNum = _stackValue/len(attributeNames)
                currentColor = id_to_random_color(currentSeedNum)
                return currentColor

            colorType = colorType.lower()
            currentColor = []
            if colorType == "material":
                currentColor = id_to_random_color(stringToNum(materialName))
            elif colorType == "attribute":
                currentColor = getCurrentAttributeColor()

            elif colorType == "blend":
                colorA = id_to_random_color(stringToNum(materialName))
                colorB = getCurrentAttributeColor()
                currentColor = colorblender(colorA,colorB,0.4)
            return currentColor
        
        def id_to_random_color(number):
                random.seed(number)
                numbers = str(random.randrange(999999))
                r_seed = int(numbers[0:2])
                g_seed = int(numbers[2:4])
                b_seed = int(numbers[4:6])
                color = []
                for lp in (r_seed,g_seed,b_seed):
                    random.seed(lp)
                    color.append((random.uniform(0, 1)))
                return color
                
        def setAttributeFlagsToStringProperty(objects,attrbuteFlags):
            attributes = attrbuteFlags
            
            attrStr = ",".join(attributes)
            for object in objects:
                pm.addAttr(object, ln="attributeFlags", dt="string")
                pm.setAttr("{0}.attributeFlags".format(object), attrStr, channelBox=True,l=True)

        def createMaterial(materialName,attributeFlags,name = ""):
            if name == "":
                name = createMaterialName(materialName,attributeFlags)
            material = pm.shadingNode("lambert", name=name, asShader=True)
            sg = pm.sets(name="%sSG" % name, empty=True, renderable=True, noSurfaceShader=True)
            pm.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
            colorType = "material"
            currentAttributeNames = []
            material.setColor(getColor(currentAttributeNames,materialName,colorType))
            #プロパティの設定の設定
            setAttributeFlagsToStringProperty([material],attributeFlags)
            setEnums([material],"materialNames",materialName)
            return material,sg

        def checkMaterialAlreadyExists(materialName,attributeName):
            if attributeName == [u""]:
                name = "phx_{0}".format(materialName).lower()
            else:
                name = "phx_{0}_{1}".format(materialName,attributeName).lower()
            if cmds.objExists(name):
                if cmds.objectType(cmds.ls(name)[0]) == "lambert":
                    return 1
            return 0

        def getLambertName():
            rtnname = "phx_{0}".format("none").lower()
            return rtnname

        def assignMaterial(targetObjs,materialName,attributeFlags):
            name = createMaterialName(materialName,attributeFlags)
            rtnMaterial = None
            if checkMaterialAlreadyExists(materialName,attributeFlags) == 0:
                materialInfo = createMaterial(materialName,attributeFlags)
                rtnMaterial = materialInfo[0]
                assignSG = materialInfo[1]
            else:
                rtnMaterial = cmds.ls(name)[0]
                assignSG = rtnMaterial+"SG"

            pm.select(targetObjs,r=True)
            pm.sets(assignSG, e=1, forceElement=targetObjs)
            return rtnMaterial
        
        #rtnに入れた値に疑似的に参照渡しする
        def quick_parent(obj,parent_group):
            if parent_group == None:
                if pm.listRelatives(obj,p=True,pa=True) != None:
                    pm.parent(obj,w=True)
            else:
                if pm.listRelatives(obj,p=True,pa=True) != [parent_group]:
                    pm.parent(obj,parent_group)

        def separate_enumlist(enumlist):
            return enumlist[0].split(":")

        def assign_group(group_name,parent_group,obj):
            # ワールドにペアレント
            if parent_group == None:
                groupNames = pm.ls("{}".format(group_name),l=True)
                if len(groupNames) != 0:
                    groupName = groupNames[0]
                    if pm.listRelatives(obj,pa=True,p=True)[0] in groupName:
                        pm.warning("{} is already a child of the parent {}".format(obj,groupName))
                    else:
                        pm.parent(obj, groupName)
                        rtn = groupName
                        return 0
                        
                else:
                    pm.group(obj,name=group_name,w=True)
                    return 1

            else:
                groupNames = pm.ls("*{}|{}".format(parent_group,group_name),l=True)
                if len(groupNames) != 0:
                    
                    for groupName in groupNames:
                        parent_group_name = ""
                        if parent_group != None:
                            parent_group_name = parent_group
                        if pm.listRelatives(obj,pa=True,p=True)[0] == groupName:
                            pm.warning("{} is already a child of the parent {}".format(obj,groupName))

                        else:
                            pm.parent(obj, groupName)
                            rtn = groupName
                            return 0
                else:
                    pm.group(obj,parent=parent_group,name=group_name)
                    return 1

        def getPhysMaterialNames(getType = "surfaceType"):
            physMatPath = r"W:\client\world\Content\res\dl\environment\physmaterial"
            phxUassetPaths = glob.glob(physMatPath+"\\phx*")
            surfaceTypes = []
            attributes = []
            rtn = []

            for lp in phxUassetPaths:
                fileName = os.path.splitext(os.path.basename(lp))[0]
                values = fileName.replace("phx_","").split("_")
                for i,value in enumerate(values):
                    if i != 0:
                        attributes.append(value)
                        continue
                    surfaceTypes.append(value)
            
            if getType == "surfaceType":
                if "none" not in surfaceTypes:
                    surfaceTypes.insert(0,"none")
                rtn = surfaceTypes
            
            elif getType == "attribute":
                if "none" not in attributes:
                    attributes.insert(0,"none")
                rtn = attributes
            
            return list(set(rtn))        

        def getEnumStrings(StringArray):
            if len(StringArray) == 0:
                pm.warning(u"物理マテリアルの設定が存在していません")
            for i,lp in enumerate(StringArray):
                if i == 0:
                    rtnAttributeName = StringArray[0]+":"
                    continue
                rtnAttributeName = "{0}{1}:".format(rtnAttributeName,lp)
            return rtnAttributeName
        
        def setEnums(objects,dataType,setEnumParam = -1,setEnumName = ""):
            enumNames = []
            if dataType == "materialNames":
                enumNames = getPhysMaterialNames("surfaceType")
            elif dataType == "collisionNames":
                enumNames = ["None","NoCollision","BlockAll"]
            
            for object in objects:
                #Enumの追加処理（すでにあれば削除して更新）
                if dataType in pm.listAttr(object):
                    pm.deleteAttr(object,at=dataType)
                index = setEnumParam
                #-1であれば初期値は設定されていないので、0に設定
                if setEnumParam == -1:
                    index = 0
                if setEnumName != "":
                    index = enumNames.index(setEnumName)

                pm.addAttr(object, ln = dataType, en=getEnumStrings(enumNames), at="enum")
                pm.setAttr("{0}.{1}".format(object,dataType), index, channelBox=True,l=True)
            return 

        def checkHasSets(setsName):
            #setが存在するか判定
            if pm.objExists(setsName):
                #objectSetかどうか判定
                if pm.objectType(pm.ls(setsName)[0]) == "objectSet":
                    return 1
            return 0
        def createSets(setName):
            rtnSet = pm.sets(name=setName)
            setEnums([rtnSet],"collisionNames",setEnumName = setName.replace("col_",""))  
            return rtnSet

        def assignCollisionSets(objs,setName):
            rtnSets = None
            if checkHasSets(setName):
                rtnSets = pm.ls(setName,type="objectSet")[0]
                rtnSets.addMembers(objs)
            else:
                rtnSets = createSets(setName)
            return rtnSets

        def is_col_sets_member(obj,col_sets):
            for col_set in col_sets:
                if obj in col_set.members():
                    return col_set
            else:
                return False

        def checkHasShape(obj):
            children = pm.listRelatives(obj,pa=True,c=True,type="mesh")
           
            if children != None:
                for lp in children:
                    if pm.objectType(lp) == "mesh":
                        return True
            
            return False
        
        def createMaterialName(materialName,attributeFlags):
            if attributeFlags == [u""]:
                rtn = "phx_{0}".format(materialName).lower()
            else:
                rtn = "phx_{0}_{1}".format(materialName,"_".join(attributeFlags)).lower()

            return rtn

        def create_collision_basename(obj_name,attrbuteName,materialName,suffixIndex):
            if "" != attrbuteName:
                groupName = "{0}{1}".format(obj_name+"_"+materialName+"_"+attrbuteName,format(suffixIndex, '02')).lower()
            else :
                groupName = "{0}{1}".format(obj_name+"_"+materialName,format(suffixIndex, '02')).lower()
            return groupName

        def get_top_parent(obj):
            rtn = pm.PyNode(obj.longName().split("|")[1])
            if obj != rtn:
                return rtn
            return None


        # ------------------------------------------
        # main 
        # ------------------------------------------
        selection = args['global_args']['selection']
        colsets = pm.ls("col_*",type ="objectSet")
        mats    = pm.ls("phx_*",type ="lambert")
        collisionGroup = {}
        for mat in mats:
            colnum = {}
            for colset in colsets:
                colnum[colset] = -1
            else:
                collisionGroup[mat] = colnum
        objs = selection
        objs = pm.listRelatives(objs,ad = True,pa=True,type = "transform")

        default_objects = []
        #check exist transform
        if objs == None:
            return 0

        for obj in objs:
            hasShape = checkHasShape(obj)

            if hasShape == True:
                shape = pm.listRelatives(obj,ad=True,pa=True,type="mesh")
                SG  = pm.listConnections(shape, s=False, d=True, t='shadingEngine')
                mats = pm.ls(pm.listConnections(SG, s=True, d=False), mat=True)

                #get top parent node.
                parent_node = pm.listRelatives(obj,p=True,pa=True)[0]
                pattern = re.compile("(UCX|UBX|COMPLEX)_(.*?)_(\d{1,5})")

                #Check collision assets. 
                if re.search(pattern,str(obj)):
                    if is_col_sets_member(obj,colsets):
                        try:
                            parent_node = pm.listRelatives(pm.listRelatives(obj,pa=True,p=True)[0],pa=True,p=True)[0]
                        except (TypeError,IndexError):
                            parent_node = None

                        if "COMPLEX_" in str(obj):
                            top_parent = [""]
                            top_parent = get_top_parent(obj)
                            if top_parent != None:
                                quick_parent(obj,top_parent)
                                
                        else:
                            col = is_col_sets_member(obj,colsets)
                            collisionName = pm.attributeQuery( 'collisionNames', node=col, listEnum=True )
                            collisionName = separate_enumlist(collisionName)[pm.getAttr("{}.collisionNames".format(col))]
                            
                            materialName = pm.attributeQuery( 'materialNames', node=mats[0], listEnum=True )
                            materialName = separate_enumlist(materialName)[pm.getAttr("{}.materialNames".format(mats[0]))]

                            attrbuteName = pm.getAttr(mats[0]+".attributeFlags").replace(",","_")

                            current_maxnum = max(collisionGroup[mats[0]].values())
                            current_suffix = collisionGroup[mats[0]][col]
                            suffixIndex = current_suffix
                            if current_suffix == -1:
                                suffixIndex = current_maxnum+1
                                collisionGroup[mats[0]][col] = current_maxnum+1

                            pattern = re.compile("(UCX|UBX|COMPLEX)_(.*?)_(\d{1,5})")
                            obj_name = re.search(pattern,str(obj)).group(2)
                            groupName = "col_{0}".format(create_collision_basename(obj_name,attrbuteName,materialName,suffixIndex))
                            is_createGroup = assign_group(groupName,parent_node,obj)                        

                            if parent_node == None:
                                obj = "{0}|{1}".format(groupName,obj.rsplit("|")[-1])
                    
                            else:
                                obj = "{0}|{1}|{2}".format(parent_node,groupName,obj.rsplit("|")[-1])
                            
                            new_name = obj.replace(obj_name,create_collision_basename(obj_name,attrbuteName,materialName,suffixIndex))
                            pm.rename(obj,new_name.split("|")[-1])

                            if is_createGroup:
                                dummy = pm.polyCreateFacet( p=[(0, 0, 0), (10, 0, 0), (10, 10, 0)],n=create_collision_basename(obj_name,attrbuteName,materialName,suffixIndex))[0]
                                materialName = pm.attributeQuery( 'materialNames', node=mats[0], listEnum=True )
                                print("dummy>>",str(dummy))
                                materialName = separate_enumlist(materialName)[pm.getAttr("{}.materialNames".format(mats[0]))]
                                attributeFlags = pm.getAttr(mats[0]+'.attributeFlags').split(",")
                                #ダミーに適切なマテリアルをアサイン
                                assignMaterial(dummy,materialName,attributeFlags)
                                pm.delete(dummy, constructionHistory = True)
                                pm.addAttr(dummy, ln = "simplePhysMat" , dt ="string")
                                pm.setAttr("{0}.simplePhysMat".format(dummy),create_collision_basename(obj_name,attrbuteName,materialName,suffixIndex), type="string") 
                                quick_parent(dummy,parent_node)
                    else:
                        default_objects.append(obj)
                
                #描画用オブジェクト
                else:
                    if "simplePhysMat" in pm.listAttr(obj):
                        pm.deleteAttr(obj,at="simplePhysMat")
                    #描画オブジェクトにsimpleMaterial用のアトリビュート追加
                    if checkHasShape(obj):
                        pm.addAttr(obj, ln = "simplePhysMat",  dt ="string")
                        pm.setAttr("{0}.simplePhysMat".format(obj), createMaterialName("none",[u""]), type="string") 

            else:
                if len(default_objects) != 0:

                    #小文字で設定する必要あり
                    assignMaterial(default_objects,"none",[u""])
                    assignCollisionSets(default_objects,"col_BlockAll")



    def getlabel(self):
        return 'Export organize scene'

    def default_checked(self):
        return True

    def is_editable(self):
        return False