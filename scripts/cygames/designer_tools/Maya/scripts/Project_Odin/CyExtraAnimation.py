# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   CyExtraAnimation
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.mel as mel
import math

g_main = None

#-------------------------------------------------------------------------------------------
#   更新
#-------------------------------------------------------------------------------------------
def Update():

    global g_main

    if g_main == None:
        g_main = Main()

    g_main.Update()

#*****************************************************************
# メイン
#*****************************************************************
class Main():

    #===========================================
    # __init__
    #===========================================
    def __init__(self):

        self.extraGroupName = "CyExtraAnimation"
        self.divideString = "xxx"

        self.customValueAttrPrefix = "CyExValue"
        self.customVectorAttrPrefix = "CyExVector"

        self.attrFilterList = ["color","transparency","ambientColor","bumpMapping","bumpValue","diffuse","layeredTexture","inputs","input","uvCoord","normalCamera"]
        self.notTargetMaterialList = ["lambert1","particleCloud1","shaderGlow1"]

        self.currentSelectList = []

        self.rootItemList = []

        self.progressBar = ProgressBar()

    #===========================================
    # 更新
    #===========================================
    def Update(self):

        self.UpdateCurrentSelectList()

        if len(self.currentSelectList) == 0:
            self.SelectCurrentSelectList()
            return

        maxProgCount = 0
        for select in self.currentSelectList:

            if cmds.objectType(select) != "transform":
                continue

            if select.find(self.extraGroupName) != -1:
                continue

            rootItem = RootItem(self, select)
            rootItem.UpdateList()

            maxProgCount += len(rootItem.transformList) + len(rootItem.materialList)

            self.rootItemList.append(rootItem)

        if len(self.rootItemList) == 0:
            self.SelectCurrentSelectList()
            return

        self.progressBar.Start("Extra Animation ...", maxProgCount)        

        for rootItem in self.rootItemList:

            rootItem.Update()

        self.SelectCurrentSelectList()

    #===========================================
    # 現在の選択リストを更新
    #===========================================
    def UpdateCurrentSelectList(self):
        
        self.currentSelectList = cmds.ls(sl=True,l=True)

        if self.currentSelectList == None:
            self.currentSelectList = []

    #===========================================
    # 現在選択したものを選択
    #===========================================
    def SelectCurrentSelectList(self):

        self.progressBar.End()

        cmds.select(self.currentSelectList,r=True)

    #===========================================
    # タイプでノード取得
    #===========================================
    def GetAllNode(self, rootNode, targetType):

        resultList = []

        self.GetAllNodeLoop(rootNode,targetType,resultList)

        fixResultList = []
        for node in resultList:

            exist = False
            for fixNode in fixResultList:

                if node == fixNode:
                    exist = True
                    break

            if exist == True:
                continue

            fixResultList.append(node)

        return fixResultList

    #===========================================
    # タイプでノード取得
    #===========================================
    def GetAllNodeLoop(self, rootNode, targetType, resultList):

        attrList = cmds.listAttr(rootNode)

        if rootNode.find(".") != -1:
            rootNode = rootNode.split(".")[0]

        if attrList == None:
            return

        for attr in attrList:

            if self.IsFilterAttr(attr) == False:
                continue

            connectList = None

            try:
                connectList = cmds.listConnections(rootNode + "." + attr)
            except:
                continue
            
            if connectList == None:
                continue

            for connect in connectList:

                if cmds.objectType(connect) == targetType:
                    resultList.append(connect)

                self.GetAllNodeLoop(connect, targetType, resultList)

    #===========================================
    # 選択しているオブジェクトフルパスで返す
    #===========================================
    def IsFilterAttr(self, attr):

        for attrFilter in self.attrFilterList:

            if attrFilter == attr:
                return True

        return False

    #===========================================
    # コネクションを切る
    #===========================================
    def BreakConnection(self, targetAttr):

        connectList = cmds.listConnections(targetAttr,s=True,p=True)

        if connectList == None:
            return

        if len(connectList) == 0:
            return

        for connect in connectList:

            cmds.disconnectAttr(connect,targetAttr)

    #===========================================
    # キーの焼き付け
    #===========================================
    def BakeKey(self, srcTarget, dstTarget, defaultValue, cutValue, invert):

        cmds.setAttr(dstTarget, defaultValue)

        if srcTarget == "":
            return False

        srcNode = srcTarget.split(".")[0]
        srcAttr = srcTarget.split(".")[1]
        
        dstNode = dstTarget.split(".")[0]        
        dstAttr = dstTarget.split(".")[1]

        self.BreakConnection(dstNode + "." + dstAttr)

        minFrame = int(cmds.playbackOptions(q=True,minTime=True))
        maxFrame = int(cmds.playbackOptions(q=True,maxTime=True))

        firstValue = cmds.getAttr(srcNode + "." + srcAttr, t=minFrame)

        if invert == True:
            firstValue = 1 - firstValue;
        
        existAnimation = False

        for cnt in range(3,0,-1):
            
            currentStep = pow(5,cnt)
            existAnimation = self.ExistAnimation(srcNode + "." + srcAttr, invert, currentStep)

            if existAnimation == True:
                break

        if existAnimation == False:

            cmds.setAttr(dstNode + "." + dstAttr, firstValue)

            if defaultValue != firstValue:
                existAnimation = True

            return existAnimation

        prevValue = -10000000
        for cnt in range(minFrame, maxFrame + 1):

            nextFrame = cnt + 1

            srcValue = cmds.getAttr(srcNode + "." + srcAttr, t=cnt)
            srcNextValue = cmds.getAttr(srcNode + "." + srcAttr, t=nextFrame)

            thisDiffer = math.fabs(srcNextValue - srcValue)

            isCut = False
            if thisDiffer > cutValue:
                isCut = True

            if invert == True:
                srcValue = 1 - srcValue

            if prevValue != srcValue:
                cmds.setKeyframe( dstNode, v=srcValue, at=dstAttr, t=cnt )

            prevValue = srcValue

            if isCut == False:
                continue

            cmds.setKeyframe( dstNode, v=srcValue, at=dstAttr, t=cnt )
            cmds.setKeyframe( dstNode, v=srcValue, at=dstAttr, t=cnt + 0.995 )

        return existAnimation

    #===========================================
    # アニメーションの存在確認
    #===========================================
    def ExistAnimation(self, targetAttr, invert, checkStep):

        minFrame = int(cmds.playbackOptions(q=True,minTime=True))
        maxFrame = int(cmds.playbackOptions(q=True,maxTime=True))

        firstValue = cmds.getAttr(targetAttr, t=minFrame)

        if invert == True:
            firstValue = 1 - firstValue;
        
        existAnimation = False
        
        for cnt in range(minFrame, maxFrame + 1, checkStep):
            srcValue = cmds.getAttr(targetAttr, t=cnt)

            if invert == True:
                srcValue = 1 - srcValue;

            if firstValue != srcValue:
                existAnimation = True
                break

        return existAnimation

    #===========================================
    # オブジェクトの存在確認
    #===========================================
    def GetTransform(self, objectName, targetList):

        resultList = []

        for target in targetList:

            thisShortName = self.GetShortName(target)

            if thisShortName == objectName:
                resultList.append(target)

        resultList.sort()

        return resultList

    #===========================================
    # 子トランスフォームリスト取得
    #===========================================
    def GetChildTransformList(self, target):

        cmds.select(target,r=True)

        cmds.select(hi=True)

        childTransformList = cmds.ls(sl=True, l=True, tr=True)

        if childTransformList== None:
            childTransformList = []

        return childTransformList

    #===========================================
    # ショート名を取得
    #===========================================
    def GetShortName(self, targetName):

        if targetName.find("|") == -1:
            return targetName

        splitNameList = targetName.split("|")

        return splitNameList[len(splitNameList) - 1]

    #===========================================
    # シェープノード取得
    #===========================================
    def GetShapeNode(self, targetName):

        thisShapeList = cmds.listRelatives(targetName,shapes=True)
        
        if thisShapeList == None:
            return ""

        if len(thisShapeList) == 0:
            return ""

        return thisShapeList[0]

    #===========================================
    # シェープノードタイプ
    #===========================================
    def GetShapeNodeType(self, targetName):

        thisShape = self.GetShapeNode(targetName)

        if thisShape == "":
            return

        return cmds.objectType(targetName + "|" + thisShape)

    #===========================================
    # トランスフォームリスト取得
    #===========================================
    def GetTransformList(self, target):

        resultList = []

        childTransformList = self.GetChildTransformList(target)

        for childTransform in childTransformList:

            if childTransform.find(self.extraGroupName) != -1:
                continue

            if childTransform.find(self.divideString) != -1:
                continue

            resultList.append(childTransform)

        return resultList

    #===========================================
    # マテリアルリスト取得
    #===========================================
    def GetMaterialList(self, target):

        resultMatList = []

        childTransformList = self.GetTransformList(target)

        for childTransform in childTransformList:

            matList = self.GetMaterialListFromTransform(childTransform)

            resultMatList.extend(matList)

        fixResultMatList = []
        for mat in resultMatList:

            exist = False
            for fixMat in fixResultMatList:

                if mat == fixMat:
                    exist=True
                    break

            if exist == True:
                continue

            fixResultMatList.append(mat)

        fixResultMatList.sort()

        return fixResultMatList
            
    #===========================================
    # トランスフォームからマテリアルリストを取得
    #===========================================
    def GetMaterialListFromTransform(self, target):

        resultMatList =[]

        if cmds.objectType(target) != "transform":
            return resultMatList

        shapeList = cmds.listRelatives(target, shapes=True, f=True)

        if shapeList == None:
            return resultMatList

        for shape in shapeList:

            shadingList = cmds.listConnections(shape, t="shadingEngine")

            if shadingList == None:
                continue

            for shading in shadingList:

                materialList = cmds.listConnections(shading, t="lambert")

                if materialList == None:
                    continue

                resultMatList.extend(materialList)

        fixResultMatList = []
        for mat in resultMatList:

            exist = False
            for fixMat in fixResultMatList:

                if mat == fixMat:
                    exist=True
                    break

            if exist == True:
                continue

            fixResultMatList.append(mat)

        return fixResultMatList

#*****************************************************************
# プログレスバー
#*****************************************************************
class ProgressBar():

    #===========================================
    # 初期化
    #===========================================
    def __init__(self):

        self.title = ""

        self.maxValue = 100
        self.currentValue = 0

        self.isCancel = False

    #===========================================
    # 開始
    #===========================================
    def Start(self, title, maxValue):

        self.title = title;
        
        self.currentValue = 0
        self.maxValue = maxValue

        self.isCancel= False

        self.End()

        cmds.progressWindow(title=self.title,status="",isInterruptable=True, min=0, max=self.maxValue )

    #===========================================
    # 更新
    #===========================================
    def Update(self, addValue, info):

        self.currentValue += addValue

        cmds.progressWindow( edit=True, progress=self.currentValue, status=str(self.currentValue) + "/" + str(self.maxValue) + "    " + info)

        if self.isCancel == True:
            return False

        if cmds.progressWindow( query=True, isCancelled=True ) == True:

            self.isCancel= True
            
            return False

        return True

    #===========================================
    # 終了
    #===========================================
    def End(self):

        cmds.progressWindow(endProgress=1)

#*****************************************************************
# ルート
#*****************************************************************
class RootItem():

    #===========================================
    # 初期化
    #===========================================
    def __init__(self, main, rootTransform):

        self.main = main

        self.rootTransform = rootTransform

        self.extraGroup = ""
        
        self.childTransformList = []

        self.materialList = []
        self.transformList = []

        self.extraGroupList = []

    #===========================================
    # リスト更新
    #===========================================
    def UpdateList(self):

        self.UpadateExtraRoot()

        self.transformList = self.main.GetTransformList(self.rootTransform)
        self.materialList = self.main.GetMaterialList(self.rootTransform)

    #===========================================
    # 更新
    #===========================================
    def Update(self):

        self.UpdateMaterial()
        
        self.UpdateTransform()

        
        
        self.Finalize()

    #===========================================
    # マテリアル更新
    #===========================================
    def UpdateMaterial(self):

        for material in self.materialList:

            if self.main.progressBar.Update(1, self.main.GetShortName(material)) == False:
                break

            exist = False
            for notTargetMat in self.main.notTargetMaterialList:

                if material == notTargetMat:
                    exist = True
                    break

            if exist == True:
                continue

            newMat = MaterialItem(self, material)
            newMat.Update()

    #===========================================
    # マテリアル更新
    #===========================================
    def UpdateTransform(self):

        for transform in self.transformList:

            if self.main.progressBar.Update(1, self.main.GetShortName(transform)) == False:
                break

            newTrans = TransformItem(self, transform)
            newTrans.Update()

    #===========================================
    # ルート作成
    #===========================================
    def UpadateExtraRoot(self):

        self.childTransformList = self.main.GetChildTransformList(self.rootTransform)

        extraGroupList = self.main.GetTransform(self.main.extraGroupName, self.childTransformList)

        if len(extraGroupList) == 1:

            self.extraGroup = extraGroupList[0]
            return

        elif len(extraGroupList) > 1:
            
            for cnt in range(1,len(extraGroupList)):
                cmds.delete(extraGroupList[cnt])

            self.extraGroup = extraGroupList[0]
            return
        
        self.extraGroup = cmds.group( em=True, name=self.main.extraGroupName )
        
        self.extraGroup = cmds.parent( self.extraGroup, self.rootTransform )
        
        self.extraGroup = cmds.ls(self.extraGroup, l=True)[0]

    #===========================================
    # 追加オブジェクトを取得
    #=========================================== 
    def GetExtraObject(self, prefix):

        childList = cmds.listRelatives(self.extraGroup ,c=True, f=True)

        if childList == None:
            return None

        if len(childList) == 0:
            return None

        for child in childList:

            if child.find(prefix) != -1:
                return child

        return None

    #===========================================
    # 追加オブジェクトを作成
    #=========================================== 
    def CreateExtraObject(self, objectName):

        newObject = cmds.group( em=True, name=objectName )

        newObject = cmds.parent( newObject, self.extraGroup )

        newObject = cmds.ls(newObject, l=True)[0]

        return newObject

    #===========================================
    # 追加オブジェクトの接頭語を取得
    #=========================================== 
    def GetPrefixNameFromExtraObject(self, target):

        targetShortName = self.main.GetShortName(target)

        if targetShortName.find(self.main.divideString) == -1:
            return ""

        splitNameList = targetShortName.split(self.main.divideString)

        if len(splitNameList) < 3:
            return ""
        
        return splitNameList[0] + self.main.divideString + splitNameList[1] + self.main.divideString + splitNameList[2]

    #===========================================
    # 終了処理
    #===========================================
    def Finalize(self):

        if self.main.progressBar.Update(0, "Finalize") == False:
            return

        if self.extraGroup == "":
            return

        if len(self.extraGroupList) == 0:
            cmds.delete(self.extraGroup)
            return

        childList = cmds.listRelatives(self.extraGroup ,c=True, f=True)

        if childList == None:
            return

        if len(childList) == 0:
            return

        deleteList = []

        for child in childList:

            thisChildPrefix = self.GetPrefixNameFromExtraObject(child)

            if thisChildPrefix == "":
                deleteList.append(child)
                continue

            exist = False
            for current in self.extraGroupList:

                currentPrefix = self.GetPrefixNameFromExtraObject(current)

                if currentPrefix == thisChildPrefix:
                    exist = True
                    break

            if exist == True:
                continue

            deleteList.append(child)

        if len(deleteList) > 0:
            cmds.delete(deleteList)
    
            
#*****************************************************************
# マテリアル
#*****************************************************************
class MaterialItem():

    #===========================================
    # 初期化
    #===========================================
    def __init__(self, rootItem, materialName):

        self.rootItem = rootItem
        self.main = self.rootItem.main
        self.materialName = materialName

    #===========================================
    # 更新
    #===========================================
    def Update(self):

        self.UpdateTexAnim()

        self.UpdateMainColorAnim()
        self.UpdateMainColorOffsetAnim()

        self.UpdateSubTexColorAnim()
        self.UpdateSubTexColorOffsetAnim();

        self.UpdateCustomValue()
        self.UpdateCustomVector()

    #===========================================
    # テクスチャアニメーションの更新
    #===========================================
    def UpdateTexAnim(self):
        
        fileNodeList = self.main.GetAllNode(self.materialName, "file")
        fileNodeList.sort()

        for cnt in range(0, len(fileNodeList)):

            placedTextureList = self.main.GetAllNode(fileNodeList[cnt], "place2dTexture")

            if len(placedTextureList) == 0:
                continue

            thisObjectPrefix = self.materialName + self.main.divideString + "Material" + self.main.divideString + "Tex" + str(cnt)

            targetObject = self.rootItem.GetExtraObject(thisObjectPrefix)

            if targetObject == None:
                if cnt == 0:
                    targetObject = self.rootItem.CreateExtraObject(thisObjectPrefix + self.main.divideString + "_MainTex")
                elif cnt == 1:
                    targetObject = self.rootItem.CreateExtraObject(thisObjectPrefix + self.main.divideString + "_SubTex")
                else:
                    targetObject = self.rootItem.CreateExtraObject(thisObjectPrefix + self.main.divideString + "_SubTex" + str(cnt))

            hasAnimTransX = self.main.BakeKey(placedTextureList[0] + ".offsetU", targetObject + ".translateX", 0, 0.1, False)
            hasAnimTransY = self.main.BakeKey(placedTextureList[0] + ".offsetV", targetObject + ".translateY", 0, 0.1, False)

            hasAnimScaleX = self.main.BakeKey(placedTextureList[0] + ".repeatU", targetObject + ".scaleX", 1, 0.1, False)
            hasAnimScaleY = self.main.BakeKey(placedTextureList[0] + ".repeatV", targetObject + ".scaleY", 1, 0.1, False)

            if hasAnimTransX == False and hasAnimTransY == False and hasAnimScaleX == False and hasAnimScaleY == False:
                cmds.delete(targetObject)
                continue

            self.rootItem.extraGroupList.append(targetObject)

    #===========================================
    # カラーアニメーションの更新
    #===========================================
    def UpdateMainColorAnim(self):

        colorRAttr = self.materialName + ".colorR"
        colorGAttr = self.materialName + ".colorG"
        colorBAttr = self.materialName + ".colorB"
        
        alphaAttr = self.materialName + ".transparencyR"
        alphaInvert = True

        colorFileNodeList = self.main.GetAllNode(self.materialName + ".color", "file")
        colorFileNodeList.sort()

        if len(colorFileNodeList) != 0:
            
            colorRAttr = colorFileNodeList[0] + ".colorGainR"
            colorGAttr = colorFileNodeList[0] + ".colorGainG"
            colorBAttr = colorFileNodeList[0] + ".colorGainB"

        alphaFileNodeList = self.main.GetAllNode(self.materialName + ".transparency", "file")
        alphaFileNodeList.sort()

        if len(alphaFileNodeList) != 0:
            alphaAttr = alphaFileNodeList[0] + ".alphaGain"
            alphaInvert = False

        thisObjectPrefix = self.materialName + self.main.divideString + "Material" + self.main.divideString + "Color" + str(0)

        targetObject = self.rootItem.GetExtraObject(thisObjectPrefix)

        if targetObject == None:
            targetObject = self.rootItem.CreateExtraObject(thisObjectPrefix + self.main.divideString + "_Color")

        hasAnimColorR = self.main.BakeKey(colorRAttr, targetObject + ".translateX", 1, 0.5, False)
        hasAnimColorG = self.main.BakeKey(colorGAttr, targetObject + ".translateY", 1, 0.5, False)
        hasAnimColorB = self.main.BakeKey(colorBAttr, targetObject + ".translateZ", 1, 0.5, False)
        hasAnimColorA = self.main.BakeKey(alphaAttr, targetObject + ".scaleX", 1, 0.5, alphaInvert)

        if hasAnimColorR == False and hasAnimColorG == False and hasAnimColorB == False and hasAnimColorA == False:
            cmds.delete(targetObject)
            return

        self.rootItem.extraGroupList.append(targetObject)

    #===========================================
    # テクスチャカラーアニメーションの更新
    #===========================================
    def UpdateSubTexColorAnim(self):

        colorFileNodeList = self.main.GetAllNode(self.materialName + ".color", "file")
        colorFileNodeList.sort()

        if len(colorFileNodeList) == 0:
            return

        mainColorFileNode = colorFileNodeList[0]

        fileNodeList = self.main.GetAllNode(self.materialName, "file")
        fileNodeList.sort()

        thisIndex = 1
        for cnt in range(0, len(fileNodeList)):

            if fileNodeList[cnt] == mainColorFileNode:
                continue

            colorRAttr = fileNodeList[cnt] + ".colorGainR"
            colorGAttr = fileNodeList[cnt] + ".colorGainG"
            colorBAttr = fileNodeList[cnt] + ".colorGainB"
            alphaAttr = fileNodeList[cnt] + ".alphaGain"

            thisObjectPrefix = self.materialName + self.main.divideString + "Material" + self.main.divideString + "Color" + str(thisIndex)

            targetObject = self.rootItem.GetExtraObject(thisObjectPrefix)

            if targetObject == None:
                if thisIndex == 1:
                    targetObject = self.rootItem.CreateExtraObject(thisObjectPrefix + self.main.divideString + "_SubTexColor")
                else:
                    targetObject = self.rootItem.CreateExtraObject(thisObjectPrefix + self.main.divideString + "_SubTexColor" + str(thisIndex))

            hasAnimColorR = self.main.BakeKey(colorRAttr, targetObject + ".translateX", 1, 0.5, False)
            hasAnimColorG = self.main.BakeKey(colorGAttr, targetObject + ".translateY", 1, 0.5, False)
            hasAnimColorB = self.main.BakeKey(colorBAttr, targetObject + ".translateZ", 1, 0.5, False)
            hasAnimColorA = self.main.BakeKey(alphaAttr, targetObject + ".scaleX", 1, 0.5, False)

            if hasAnimColorR == False and hasAnimColorG == False and hasAnimColorB == False and hasAnimColorA == False:
                cmds.delete(targetObject)
                continue

            self.rootItem.extraGroupList.append(targetObject)

            thisIndex+=1

    #===========================================
    # カラーオフセットアニメーションの更新
    #===========================================
    def UpdateMainColorOffsetAnim(self):

        colorRAttr = self.materialName + ".incandescenceR"
        colorGAttr = self.materialName + ".incandescenceG"
        colorBAttr = self.materialName + ".incandescenceB"
        alphaAttr = ""

        colorFileNodeList = self.main.GetAllNode(self.materialName + ".color", "file")
        colorFileNodeList.sort()

        if len(colorFileNodeList) != 0:
            
            colorRAttr = colorFileNodeList[0] + ".colorOffsetR"
            colorGAttr = colorFileNodeList[0] + ".colorOffsetG"
            colorBAttr = colorFileNodeList[0] + ".colorOffsetB"

        alphaFileNodeList = self.main.GetAllNode(self.materialName + ".transparency", "file")
        alphaFileNodeList.sort()

        if len(alphaFileNodeList) != 0:
            alphaAttr = alphaFileNodeList[0] + ".alphaOffset"

        thisObjectPrefix = self.materialName + self.main.divideString + "Material" + self.main.divideString + "ColorOffset" + str(0)

        targetObject = self.rootItem.GetExtraObject(thisObjectPrefix)

        if targetObject == None:
            targetObject = self.rootItem.CreateExtraObject(thisObjectPrefix + self.main.divideString + "_ColorOffset")

        hasAnimColorR = self.main.BakeKey(colorRAttr, targetObject + ".translateX", 0, 0.5, False)
        hasAnimColorG = self.main.BakeKey(colorGAttr, targetObject + ".translateY", 0, 0.5, False)
        hasAnimColorB = self.main.BakeKey(colorBAttr, targetObject + ".translateZ", 0, 0.5, False)
        hasAnimColorA = self.main.BakeKey(alphaAttr, targetObject + ".scaleX", 0, 0.5, False)

        if hasAnimColorR == False and hasAnimColorG == False and hasAnimColorB == False and hasAnimColorA == False:
            cmds.delete(targetObject)
            return

        self.rootItem.extraGroupList.append(targetObject)

    #===========================================
    # テクスチャカラーオフセットアニメーションの更新
    #===========================================
    def UpdateSubTexColorOffsetAnim(self):

        colorFileNodeList = self.main.GetAllNode(self.materialName + ".color", "file")
        colorFileNodeList.sort()

        if len(colorFileNodeList) == 0:
            return

        mainColorFileNode = colorFileNodeList[0]

        fileNodeList = self.main.GetAllNode(self.materialName, "file")
        fileNodeList.sort()

        thisIndex = 1
        for cnt in range(0, len(fileNodeList)):

            if fileNodeList[cnt] == mainColorFileNode:
                continue

            colorRAttr = fileNodeList[cnt] + ".colorOffsetR"
            colorGAttr = fileNodeList[cnt] + ".colorOffsetG"
            colorBAttr = fileNodeList[cnt] + ".colorOffsetB"
            alphaAttr = fileNodeList[cnt] + ".alphaOffset"
            
            thisObjectPrefix = self.materialName + self.main.divideString + "Material" + self.main.divideString + "ColorOffset" + str(thisIndex)

            targetObject = self.rootItem.GetExtraObject(thisObjectPrefix)

            if targetObject == None:
                if thisIndex == 1:
                    targetObject = self.rootItem.CreateExtraObject(thisObjectPrefix + self.main.divideString + "_SubTexColorOffset")
                else:
                    targetObject = self.rootItem.CreateExtraObject(thisObjectPrefix + self.main.divideString + "_SubTexColorOffset" + str(thisIndex))

            hasAnimColorR = self.main.BakeKey(colorRAttr, targetObject + ".translateX", 0, 0.5, False)
            hasAnimColorG = self.main.BakeKey(colorGAttr, targetObject + ".translateY", 0, 0.5, False)
            hasAnimColorB = self.main.BakeKey(colorBAttr, targetObject + ".translateZ", 0, 0.5, False)
            hasAnimColorA = self.main.BakeKey(alphaAttr, targetObject + ".scaleX", 0, 0.5, False)

            if hasAnimColorR == False and hasAnimColorG == False and hasAnimColorB == False and hasAnimColorA == False:
                cmds.delete(targetObject)
                continue

            self.rootItem.extraGroupList.append(targetObject)

            thisIndex+=1

    #===========================================
    # カスタムアニメーション値更新
    #===========================================
    def UpdateCustomValue(self):

        attrList = cmds.listAttr(self.materialName)

        thisIndex = 0
        for cnt in range(0, 10):

            targetAttrPrefix = self.main.customValueAttrPrefix + str(thisIndex)
            targetAttr = None
            
            for attr in attrList:

                if attr.find(targetAttrPrefix) == -1:
                    continue

                targetAttr = attr
                break

            if targetAttr == None:
                continue

            targetAttr = self.materialName + "." + targetAttr
            thisType = cmds.getAttr(targetAttr,typ=True)

            if thisType != "double":
                continue

            thisObjectPrefix = self.materialName + self.main.divideString + "Material" + self.main.divideString + "CustomValue" + str(thisIndex)
            targetObject = self.rootItem.GetExtraObject(thisObjectPrefix)
            targetObjectNewName = thisObjectPrefix + self.main.divideString + "_CustomValue" + str(thisIndex)

            if targetObject == None:
                targetObject = self.rootItem.CreateExtraObject(targetObjectNewName)
                
            self.main.BakeKey(targetAttr, targetObject + ".translateX", 10000000, 0.5, False)

            self.rootItem.extraGroupList.append(targetObject)

            thisIndex +=1

    #===========================================
    # カスタムアニメーションベクトル更新
    #===========================================
    def UpdateCustomVector(self):

        attrList = cmds.listAttr(self.materialName)

        thisIndex = 0
        for cnt in range(0, 10):

            targetAttrPrefix = self.main.customVectorAttrPrefix + str(thisIndex)
            targetAttr = None
            
            for attr in attrList:

                if attr.find(targetAttrPrefix) == -1:
                    continue

                targetAttr = attr
                break

            if targetAttr == None:
                continue

            targetAttr = self.materialName + "." + targetAttr
            thisType = cmds.getAttr(targetAttr,typ=True)

            if thisType != "double3":
                continue

            thisObjectPrefix = self.materialName + self.main.divideString + "Material" + self.main.divideString + "CustomVector" + str(thisIndex)
            targetObject = self.rootItem.GetExtraObject(thisObjectPrefix)
            targetObjectNewName = thisObjectPrefix + self.main.divideString + "_CustomVector" + str(thisIndex)

            if targetObject == None:
                targetObject = self.rootItem.CreateExtraObject(targetObjectNewName)
                
            self.main.BakeKey(targetAttr + "X", targetObject + ".translateX", 10000000, 0.5, False)
            self.main.BakeKey(targetAttr + "Y", targetObject + ".translateY", 10000000, 0.5, False)
            self.main.BakeKey(targetAttr + "Z", targetObject + ".translateZ", 10000000, 0.5, False)

            self.rootItem.extraGroupList.append(targetObject)

            thisIndex +=1

#*****************************************************************
# トランスフォーム
#*****************************************************************
class TransformItem():

    #===========================================
    # 初期化
    #===========================================
    def __init__(self, rootItem, transformName):

        self.rootItem = rootItem
        self.main = self.rootItem.main
        self.transformName = transformName

    #===========================================
    # 更新
    #===========================================
    def Update(self):

        self.UpdateVisible()

    #===========================================
    # テクスチャアニメーションの更新
    #===========================================
    def UpdateVisible(self):

        targetType = "Object"
        animType = "Visibility"

        thisShortName = self.main.GetShortName(self.transformName)

        thisObjectPrefix = thisShortName + self.main.divideString + targetType + self.main.divideString + animType + str(0)
        targetObject = self.rootItem.GetExtraObject(thisObjectPrefix)

        if targetObject == None:
            targetObject = self.rootItem.CreateExtraObject(thisObjectPrefix + self.main.divideString + "None")
            
        hasAnimValue = self.main.BakeKey(self.transformName + ".visibility", targetObject + ".translateX", 1, 0.5, False)

        if hasAnimValue == False:
            cmds.delete(targetObject)
            return

        self.rootItem.extraGroupList.append(targetObject)       
