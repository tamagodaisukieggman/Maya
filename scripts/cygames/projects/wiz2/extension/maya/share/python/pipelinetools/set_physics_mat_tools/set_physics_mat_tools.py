# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import random
import glob
import pymel.core as pm
    
class setPhysicsTools():
    u"""
    jsonから物理マテリアルの設定、コリジョンの設定をする
    """
    def __init__(self):
        self.parentWidget = None
        self.selectedObjects = None
        self.json_path = ""
        self.attributeName = ""
        self.materialName = ""
        self.physMatPath = r"W:\client\world\Content\res\dl\environment\physmaterial"

    def setMaterialName(self,materialName):
        self.materialName = materialName
        return self.materialName

    def getAttributeName(self):
        rtn = ""
        attributeNames = self.parentWidget.getAttributeCheckedNames()
        if len(attributeNames) is not 0:
            rtn = "_".join(attributeNames)
        else:
            rtn = ""
        return rtn

    def checkPhysMaterialNameExists(self,checkName):
        phxUassetPaths = glob.glob(self.physMatPath+"\\phx*")
        for lp in phxUassetPaths:
            fileName = os.path.splitext(os.path.basename(lp))[0]
            if checkName == fileName:
                return 1
        return 0

    def getPhysMaterialNames(self,getType = "surfaceType"):
        phxUassetPaths = glob.glob(self.physMatPath+"\\phx*")
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

    def getEnumStrings(self,StringArray):
        if len(StringArray) == 0:
            pm.warning(u"物理マテリアルの設定が存在していません")
        for i,lp in enumerate(StringArray):
            if i == 0:
                rtnAttributeName = StringArray[0]+":"
                continue
            rtnAttributeName = "{0}{1}:".format(rtnAttributeName,lp)
        return rtnAttributeName

    def id_to_random_color(self,number):
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

    def getColor(self,attributeNames,materialName,colorType ="material"):
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
            currentColor = self.id_to_random_color(currentSeedNum)
            return currentColor

        colorType = colorType.lower()
        currentColor = []
        if colorType == "material":
            currentColor = self.id_to_random_color(stringToNum(materialName))
        elif colorType == "attribute":
            currentColor = getCurrentAttributeColor()

        elif colorType == "blend":
            colorA = self.id_to_random_color(stringToNum(materialName))
            colorB = getCurrentAttributeColor()
            currentColor = colorblender(colorA,colorB,0.4)
        return currentColor

    def setEnums(self,objects,dataType,setEnumParam = -1):
        enumNames = []
        if dataType == "materialNames":
            enumNames = self.getPhysMaterialNames("surfaceType")
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
            pm.addAttr(object, ln = dataType, en=self.getEnumStrings(enumNames), at="enum")
            pm.setAttr("{0}.{1}".format(object,dataType), index, channelBox=True,l=True)
        return 
    
    def setAttributeFlagsToStringProperty(self,objects):
        attributes = self.parentWidget.getAttributeCheckedNames()
        
        attrStr = ",".join(attributes)
        for object in objects:
            pm.addAttr(object, ln="attributeFlags", dt="string")
            pm.setAttr("{0}.attributeFlags".format(object), attrStr, channelBox=True,l=True)

    def checkMaterialAlreadyExists(self):
        #materialNameが存在するか判定
        name = self.getLambertName()
        if pm.objExists(name):
            #lambertマテリアルかどうか判定
            if pm.objectType(pm.ls(name)[0]) == "lambert":
                return 1
        return 0
    
    def createMaterial(self,name = ""):
        if name == "":
            name = self.getLambertName()
        material = pm.shadingNode("lambert", name=name, asShader=True)
        sg = pm.sets(name="%sSG" % name, empty=True, renderable=True, noSurfaceShader=True)
        pm.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
        
        if self.parentWidget != None:
            colorType = self.parentWidget.getCurrentCheckedColorType()
        else:
            colorType = "material"
        if self.getAttributeName() == u"":
            currentAttributeNames = []
        else:
            currentAttributeNames = self.getAttributeName().split("_")
        material.setColor(self.getColor(currentAttributeNames,self.materialName,colorType))
        #プロパティの設定の設定
        self.setAttributeFlagsToStringProperty([material])
        self.setEnums([material],"materialNames",self.materialName)
        return material

    def get_selectedObjs(self):
        self.selectedObjects = pm.ls(sl=True)
        return self.selectedObjects

    def getLambertName(self):
        if self.getAttributeName() == "":
            rtnname = "phx_{0}".format(self.materialName).lower()
        else:
            rtnname = "phx_{0}_{1}".format(self.materialName,self.getAttributeName()).lower()
        return rtnname

    def assignMaterial(self):
        assignMaterial = None

        if not self.checkPhysMaterialNameExists(self.getLambertName()):
            rtn = pm.confirmDialog( title='Confirm', message=u'この物理マテリアルは現在ue4に存在しません。処理を続行しますか？', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            if rtn == "No":
                return

        #マテリアルがなければ新規作成
        if self.checkMaterialAlreadyExists() == 0:
            assignMaterial = self.createMaterial()
        #存在していればそのマテリアルを取得
        else:
            assignMaterial = pm.ls(self.getLambertName())[0]

        #マテリアルのアサイン処理
        pm.select(self.selectedObjects,r=True)
        pm.hyperShade(assign = assignMaterial)

        self.deleteUnusedColMaterial()
        return assignMaterial

    def getAssignedMaterials(self,transform):
        u"""
        transformに使用しているマテリアルをすべて返す
        """
        mtl_list = []
        shapes = pm.listRelatives(transform, shapes=True)
        if not shapes:
            return mtl_list
        SGs = pm.listConnections(shapes[0], source=False, type='shadingEngine')
        if not SGs:
            return mtl_list
        mtl_list = pm.ls(pm.listConnections(SGs[0], destination=False), materials=True)
        return mtl_list

    def createSets(self,setName):
        u"""
        セットの作成
        """
        rtnSet = pm.sets(name=setName)
        self.setEnums([rtnSet],"collisionNames",setName.replace("col_",""))  
        return rtnSet

    def checkHasSets(self,setsName):
        u"""
        setsNameと同名のsetが存在しているか確認
        """
        #setが存在するか判定
        if pm.objExists(setsName):
            #objectSetかどうか判定
            if pm.objectType(pm.ls(setsName)[0]) == "objectSet":
                return 1
        return 0

    def getAllSets(self):
        u"""
        すべてのコリジョン用setを取得
        """
        sets = pm.ls(type = "objectSet")
        rtnSets = []
        for set in sets:
            #enumのプロパティがあれば対象として追加
            if "collisionNames" in pm.listAttr(set):
                rtnSets.append(set)
        return rtnSets

    def assignCollisionSets(self,setName):
        u"""
        コリジョンのアサイン。すでに存在していればそのセットを使用
        """
        rtnSets = None
        transforms = pm.ls(sl=True,type="transform")
        if self.checkHasSets(setName):
            rtnSets = pm.ls(setName,type="objectSet")[0]
            rtnSets.addMembers(transforms)
        else:
            rtnSets = self.createSets(setName)
        return rtnSets
    
    #mainで使用しているものとは別にコリジョンプリセットを変更するための関数を用意
    def changeColSet(self,transforms,newColSet):
        u"""
        コリジョンの設定を変更する処理。
        """
        collisionSets = self.getAllSets()
        for transform in transforms:
            assignedColSet = None
            for transform in transforms:
                for collisionSet in collisionSets:
                    if transform in collisionSet.members():
                        assignedColSet = collisionSet
                        if assignedColSet != None:
                            assignedColSet.remove(transform)    
                        break
            self.assignCollisionSets(newColSet)

        for collisionSet in collisionSets:
            if len(collisionSet.members()) == 0:
                pm.delete(collisionSet)

        return newColSet                

    def getAllColMaterial(self):
        u"""
        すべてのcolマテリアルを取得
        """
        materials = pm.ls(type="lambert")
        colMaterials = []
        for material in materials:
            if "attributeFlags" in pm.listAttr(material):
                colMaterials.append(material)
        return colMaterials

    def covertEnumToStringArray(self,enums):
        u"""
        文字列の配列をenumの文字列に変換
        """
        rtnArray = []
        for enum in enums:
            rtnArray.extend(enum.split(":"))
        
        return rtnArray
    
    def updateColMaterial(self,colorType = "material"):
        u"""
        すべてのマテリアルを最新のJsonファイルに同期する
        """
        materials = self.getAllColMaterial()
        if len(materials) == 0:
            pm.warning(u"コリジョン用マテリアル >> 存在しません >> 更新を終了")
        currentAttributeNames = None
        currentMaterialName = None
        for material in materials:         
            AttributeNamesString = pm.getAttr("{0}.{1}".format(material,'attributeFlags'))
            if AttributeNamesString == u"":
                currentAttributeNames = []
            else:
                currentAttributeNames = AttributeNamesString.split(",")
            MaterialNamesArray = self.covertEnumToStringArray(pm.attributeQuery( 'materialNames', node=material, listEnum=True ))
            currentMaterialName = MaterialNamesArray[pm.getAttr("{0}.{1}".format(material,"materialNames"))]
            
            pm.setAttr("{}.attributeFlags".format(material), l=False)
            pm.setAttr("{}.materialNames".format(material), l=False)
            
            pm.deleteAttr( material , at='materialNames')
            pm.deleteAttr( material , at='attributeFlags')
            
            self.setAttributeFlagsToStringProperty([material])
            self.setEnums([material],"materialNames",currentMaterialName)
            #ColorをJsonから設定
            currentColor = self.getColor(currentAttributeNames,currentMaterialName,colorType)
            material.setColor(currentColor)
        print(u"コリジョン用マテリアル >> 更新を終了")
        
        return

    def deleteUnusedColMaterial(self):
        u"""
        使用していなマテリアルをすべて削除
        """
        pm.mel.source('cleanUpScene.mel')
        defaultSetting = pm.util.getEnv("MAYA_TESTING_CLEANUP")
        pm.util.putEnv("MAYA_TESTING_CLEANUP","1")
        pm.mel.scOpt_performOneCleanup(["shaderOption"])
        if defaultSetting == None:
            pm.util.putEnv("MAYA_TESTING_CLEANUP","0")
        else:
            pm.util.putEnv("MAYA_TESTING_CLEANUP",defaultSetting)
        
        return

    def apply(self):
        u"""
        マテリアルを適応させるボタンを押した時に実行される処理
        """
        self.get_selectedObjs()
        selectedType = pm.objectType(self.selectedObjects[0])

        collisionPreset = "BlockAll"
        setName = "col_"+collisionPreset

        #faceを選択していた場合
        if selectedType == "mesh":
            currentMesh = self.selectedObjects
            #フェースからオブジェクトを選択
            shapes = pm.listRelatives(self.selectedObjects,p=True)
            transforms = set(pm.listRelatives(shapes,p=True))#重複防止
            
            #複数のメッシュを選択していた場合は中断
            if len(transforms) >= 2:
                pm.warning(u"フェースに対してApplyする場合、単体のオブジェクトに対してのみ実行してください。")
                return 0

            #オブジェクトが入っているセットを検索
            collisionSets = self.getAllSets()

            assignedColSet = None
            for transform in transforms:
                for collisionSet in collisionSets:
                    if transform in collisionSet.members():
                        assignedColSet = collisionSet
                        break            
            
            #コリジョンに属していない、もしくは同じコリジョンプリセットである場合
            if assignedColSet == None or assignedColSet == setName:
                self.assignMaterial()
                pm.select(transforms,r=True)
                sets = self.assignCollisionSets(setName)

            else:
                #collision preset選択用dialogを表示
                slectedCmd = pm.confirmDialog( title='Confirm', 
                                    message=u"""collision presetが重複しています。
                                    どちらのcollision presetを使用しますか？""", 
                                    button=[assignedColSet,setName,"cancel"], 
                                    defaultButton = assignedColSet, 
                                    cancelButton='cancel', 
                                    dismissString='cancel' 
                                )
                
                fixedSet = None
                if slectedCmd == assignedColSet:
                    fixedSet = assignedColSet
                
                #現在のコリジョンと相違があれば一度remove
                elif slectedCmd == setName:
                    assignedColSet.removeMembers(transforms)
                    if len(assignedColSet.members()) == 0:
                        pm.delete(assignedColSet)
                    fixedSet = setName
                else:
                    pm.warning(u"処理をキャンセルしました。")
                    return 0

                print((u"選択フェース >> 物理マテリアルをアサイン >> {}\n".format(setName)))

                self.assignMaterial()
                pm.select(transforms,r=True)
                sets = self.assignCollisionSets(fixedSet)

            pm.select(currentMesh,r=True)

        #transformを選択していた場合
        elif selectedType == "transform":
            mat = self.assignMaterial()
            self.changeColSet(self.selectedObjects,setName)
            print((u"選択オブジェクト >> 物理マテリアルをアサイン >> materialName:{0} >> collisionName:{1}\n".format(mat,setName)))
            for lp in self.selectedObjects:
                print((u"対象オブジェクト >> {}".format(lp)))

        return 1

        