# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   CyVertexColorLayer
#-------------------------------------------------------------------------------------------

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel
import CyCommon.CyUtility

from CyCommon.CyUtility import CyUtility
from CyCommon.CySetting import CySetting

reload(CyCommon.CyUtility)
reload(CyCommon.CySetting)

g_version = "1.0.0"
g_toolName = "CyVertexColorLayer"
g_scriptPrefix= g_toolName + "."
g_uiPrefix= g_toolName + "_UI_"

g_layerManager = None
g_setting = None

g_currentTransformList = []
g_prevTransformList = ["","",""]

g_copyVtxFaceList = []
g_copyVtxColorList = []
g_copyVtxColorInfo = []


#**************************************************************************************************************************
#   UI構築
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   メインUI
#-------------------------------------------------------------------------------------------
def UI():

    global g_toolName
    global g_uiPrefix
    global g_scriptPrefix
    global g_layerManager
    global g_setting

    if g_setting == None:
        g_setting = CySetting(g_toolName)

    if g_layerManager == None:
        g_layerManager = LayerManager()
    
    width=420
    height=5

    windowTitle=g_scriptPrefix.replace(".","")
    windowName=windowTitle+"Win"

    CyUtility.CheckWindow(windowName)

    cmds.window( windowName, title=windowTitle, widthHeight=(width, height),s=False,mnb=True,mxb=False,rtf=True)

    cmds.columnLayout(adjustableColumn=True)

    DrawHeaderUI()
    DrawLayerRootUI()
    DrawFooterUI()

    cmds.separator( style='in',h=15,w=width)

    cmds.button( label="About",w=width,command=g_scriptPrefix + "Test2()")

    cmds.setParent( ".." )
 
    cmds.showWindow(windowName)

    SelectChangeEvent(windowName)

    LoadSetting()

    UpdateUI()

#-------------------------------------------------------------------------------------------
# ヘッダーUI構築
#-------------------------------------------------------------------------------------------
def DrawHeaderUI():

    global g_uiPrefix
    global g_scriptPrefix

    cmds.columnLayout(adjustableColumn=True)

    cmds.button(g_uiPrefix + "StartSystem", label="Start Vertex Color Layer System", c=g_scriptPrefix + "ApplySystem()")

    cmds.setParent( ".." )

#-------------------------------------------------------------------------------------------
# レイヤーリストUI構築
#-------------------------------------------------------------------------------------------
def DrawLayerRootUI():

    global g_uiPrefix
    global g_scriptPrefix
    global g_layerManager

    #レイヤー操作
    cmds.frameLayout(g_uiPrefix + "LayerRoot", l="Layer List",cll=0,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
    cmds.columnLayout(g_uiPrefix + "LayerMain", adjustableColumn = True, rs=5)

    cmds.rowLayout(numberOfColumns=6, columnWidth6=(70, 70, 70, 70, 70, 70))

    cmds.button(label="Add Layer", w=70, c=g_scriptPrefix + "AddLayer()", bgc=g_layerManager.layerAddColor)
    cmds.text(label="")
    cmds.button(label="Up Layer", w=70, c=g_scriptPrefix + "UpLayer()", bgc=g_layerManager.layerMoveColor)
    cmds.button(label="Down Layer", w=70, c=g_scriptPrefix + "DownLayer()", bgc=g_layerManager.layerMoveColor)
    #cmds.button(label="Merge Layer", w=70, c=g_scriptPrefix + "DownLayer()", bgc=g_layerManager.layerMergeColor)
    cmds.text(label="")
    cmds.button(label="Delete Layer", w=70, c=g_scriptPrefix + "DeleteLayer()", bgc=g_layerManager.warningColor)

    cmds.setParent( ".." )

    #レイヤー
    cmds.scrollLayout(g_uiPrefix + "LayerScrollList",verticalScrollBarThickness=5, h=150, cr=True,)
    
    for p in range(0,g_layerManager.layerMaxNum):
        DrawLayerUI(str(g_layerManager.layerMaxNum - 1 - p))

    cmds.setParent( ".." )

    #プログレスバーなど
    cmds.button(label="Culculate Result Color", c=g_scriptPrefix + "MergeAllLayer()", bgc=g_layerManager.warningColor )

    cmds.setParent( ".." )

    #レイヤー編集外
    cmds.rowLayout( numberOfColumns=6, columnWidth6=(200, 120, 10, 10, 10, 10))

    cmds.checkBox(g_uiPrefix + "CheckKeepEdit",label="Keep Editing Layer", cc=g_scriptPrefix + "UpdateKeepEditLayer()")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    cmds.setParent( ".." )
    
    cmds.setParent( ".." )

    UnvisibleAllLayerUI()

#-------------------------------------------------------------------------------------------
# レイヤーUI構築
#-------------------------------------------------------------------------------------------
def DrawLayerUI(layerId):

    global g_uiPrefix
    global g_scriptPrefix
    global g_layerManager

    cmds.rowLayout( g_uiPrefix + "Layer_" + layerId, numberOfColumns=6, columnWidth6=(10, 30, 100, 65, 100, 40), adjustableColumn=3, h=30)

    cmds.text(g_uiPrefix + "LayerIndex_" + layerId, label="")

    cmds.button(g_uiPrefix + "LayerEditButton_" + layerId, w=30, label="Edit", enable=True, c=g_scriptPrefix + "EditLayer(\"" + layerId + "\")")
    
    cmds.textField(g_uiPrefix + "LayerName_" + layerId, text="", en=True, cc=g_scriptPrefix + "UpdateLayerValue(\"" + layerId + "\")" )

    cmds.optionMenu(g_uiPrefix + "LayerBlend_" + layerId, label="", width=65, en=True, cc=g_scriptPrefix + "UpdateLayerValue(\"" + layerId + "\")")
    cmds.menuItem( label="Normal" )
    cmds.menuItem( label="Multiply" )
    cmds.menuItem( label="Add" )
    cmds.menuItem( label="Screen" )
    cmds.menuItem( label="Overlay" )

    cmds.floatSliderGrp(g_uiPrefix + "LayerAlpha_" + layerId, cw3=(0,50,50), label="", field=True, minValue=0, maxValue=1.0, value=1, pre=3, en=True, cc=g_scriptPrefix + "UpdateLayerValue(\"" + layerId + "\")" )

    cmds.button(g_uiPrefix + "LayerVisible_" + layerId, label="Visible", width=40, en=True, c=g_scriptPrefix + "UpdateLayerVisible(\"" + layerId + "\")" )
    
    cmds.setParent( ".." )

#-------------------------------------------------------------------------------------------
# フッターUI構築
#-------------------------------------------------------------------------------------------
def DrawFooterUI():

    global g_uiPrefix
    global g_scriptPrefix

    cmds.frameLayout(l="Other Menu",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
    cmds.columnLayout(adjustableColumn = True, rs=5)

    cmds.rowLayout( numberOfColumns=3, columnWidth3=(140, 140, 140) )
    
    cmds.button(label="Show ColorSet Editor", w=140, c=g_scriptPrefix + "ShowColorSetEditor()")
    cmds.button(label="Rename Result ColorSet", w=140, c=g_scriptPrefix + "ShowRenameResultColorSetDialog()")
    cmds.text(label="")
    
    cmds.setParent( ".." )
    
    cmds.setParent( ".." )
    cmds.setParent( ".." )

#-------------------------------------------------------------------------------------------
# 全てのレイヤーUIを非表示
#-------------------------------------------------------------------------------------------
def UnvisibleAllLayerUI():

    global g_layerManager

    for p in range(0,g_layerManager.layerMaxNum):
        cmds.rowLayout( g_uiPrefix + "Layer_" + str(p), e=True, visible=False)

#-------------------------------------------------------------------------------------------
#   UI更新
#-------------------------------------------------------------------------------------------
def UpdateUI():

    global g_layerManager
    global g_currentTransformList
    global g_prevTransformList

    cmds.undoInfo( swf=False )

    selectList = cmds.ls(sl=True,l=True)

    g_currentTransformList = GetTransformList()

    updateUI = False
    
    if len(g_currentTransformList) != len(g_prevTransformList):
        updateUI = True

    if updateUI == False:

        for p in range(0, len(g_currentTransformList)):

            if g_currentTransformList[p] != g_prevTransformList[p]:
                updateUI = True
                break

    if updateUI == True:
        g_layerManager.LoadFromColorSet()

    g_prevTransformList = g_currentTransformList
    
    cmds.undoInfo( swf=True )

    if selectList == None:
        return

    if len(selectList) == 0:
        return

    cmds.undoInfo( swf=False )
    cmds.select(selectList,r=True)
    cmds.undoInfo( swf=True )

#-------------------------------------------------------------------------------------------
#   ShowRenameResultColorSetDialog
#-------------------------------------------------------------------------------------------
def ShowRenameResultColorSetDialog():

    global g_layerManager

    result = cmds.promptDialog(
        title="Rename Result ColorSet",
        message="Enter Name:",
        button=["OK", "Cancel"],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString="Cancel",
        text=g_layerManager.resultColorSet)

    if result == "Cancel":
        return

    g_layerManager.resultColorSet = cmds.promptDialog(query=True, text=True)

    SaveSetting()

#-------------------------------------------------------------------------------------------
#   ShowColorSetEditor
#-------------------------------------------------------------------------------------------
def ShowColorSetEditor():

    mel.eval("colorSetEditor;")

#-------------------------------------------------------------------------------------------
# 編集中レイヤーをキープするかの更新
#-------------------------------------------------------------------------------------------
def UpdateKeepEditLayer():

    global g_layerManager
    global g_uiPrefix

    g_layerManager.keepEditingLayer = cmds.checkBox(g_uiPrefix + "CheckKeepEdit",q=True,v=True)

    SaveSetting()

#-------------------------------------------------------------------------------------------
#   選択イベント
#-------------------------------------------------------------------------------------------
def SelectChangeEvent(windowName):

    global g_scriptPrefix

    cmds.scriptJob(p=windowName,e=("SelectionChanged",g_scriptPrefix+"UpdateUI()"))
    
#**************************************************************************************************************************
#   セーブロード関連
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   ロード
#-------------------------------------------------------------------------------------------
def LoadSetting():

    global g_setting
    global g_layerManager

    g_layerManager.resultColorSet = g_setting.Load("ResultColorSet")
    g_layerManager.keepEditingLayer = g_setting.Load("KeepEditingLayer","bool")

    if g_layerManager.resultColorSet == "":        
        g_layerManager.resultColorSet = "colorSet1"

    cmds.checkBox(g_uiPrefix + "CheckKeepEdit",e=True,v=g_layerManager.keepEditingLayer)

#-------------------------------------------------------------------------------------------
#   セーブ
#-------------------------------------------------------------------------------------------
def SaveSetting():

    global g_setting
    global g_layerManager

    g_setting.Save("ResultColorSet", g_layerManager.resultColorSet)
    g_setting.Save("KeepEditingLayer",g_layerManager.keepEditingLayer)

#**************************************************************************************************************************
#   プログレスバー関連
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   プログレスバー開始
#-------------------------------------------------------------------------------------------
def StartProgress(titleName):

    cmds.progressWindow(title=titleName,status="",isInterruptable=True, min=0, max=100 )

#-------------------------------------------------------------------------------------------
#   プログレスバー更新
#-------------------------------------------------------------------------------------------
def UpdateProgress(amount,info):

    cmds.progressWindow( edit=True, progress=amount * 100.0, status=info )

    if cmds.progressWindow( query=True, isCancelled=True ) == True:
        return False

    return True

#-------------------------------------------------------------------------------------------
#   プログレスバー終了
#-------------------------------------------------------------------------------------------
def EndProgress():

    cmds.progressWindow(endProgress=1)

#**************************************************************************************************************************
#   ヘッダーでの操作
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   レイヤーシステム割り当て
#-------------------------------------------------------------------------------------------
def ApplySystem():

    global g_layerManager

    if cmds.confirmDialog(t="Confirm", m="Start Vertex Color Layer System ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    cmds.undoInfo( swf=False )

    selectList = cmds.ls(sl=True,l=True)

    g_layerManager.ApplySystem()

    cmds.undoInfo( swf=True )

    if selectList == None:
        return

    if len(selectList) == 0:
        return

    cmds.undoInfo( swf=False )
    cmds.select(selectList,r=True)
    cmds.undoInfo( swf=True )

#-------------------------------------------------------------------------------------------
#   レイヤーシステム削除
#-------------------------------------------------------------------------------------------
def DeleteSystem(layerId):

    global g_layerManager

    g_layerManager.DeleteSystem()

#-------------------------------------------------------------------------------------------
#   レイヤー追加
#-------------------------------------------------------------------------------------------
def AddLayer():

    global g_layerManager

    cmds.undoInfo( swf=False )

    selectList = cmds.ls(sl=True,l=True)

    g_layerManager.AddLayer()

    cmds.undoInfo( swf=True )

    if selectList == None:
        return

    if len(selectList) == 0:
        return

    cmds.undoInfo( swf=False )
    cmds.select(selectList,r=True)
    cmds.undoInfo( swf=True )

#-------------------------------------------------------------------------------------------
#   レイヤー削除
#-------------------------------------------------------------------------------------------
def DeleteLayer():

    global g_layerManager

    cmds.undoInfo( swf=False )
    g_layerManager.DeleteLayer()
    cmds.undoInfo( swf=True )

#-------------------------------------------------------------------------------------------
#   レイヤー移動
#-------------------------------------------------------------------------------------------
def UpLayer():

    global g_layerManager

    cmds.undoInfo( swf=False )
    g_layerManager.MoveLayer(True)
    cmds.undoInfo( swf=True )

#-------------------------------------------------------------------------------------------
#   レイヤー移動
#-------------------------------------------------------------------------------------------
def DownLayer():

    global g_layerManager

    cmds.undoInfo( swf=False )
    g_layerManager.MoveLayer(False)
    cmds.undoInfo( swf=True )

#**************************************************************************************************************************
#   レイヤー個別操作
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   レイヤー切り替え
#-------------------------------------------------------------------------------------------
def EditLayer(layerIndex):

    global g_layerManager

    layer = g_layerManager.GetLayerFromIndex(layerIndex)

    if layer == None:
        return

    if g_layerManager.editLayer == layer:
        layer = None
    
    g_layerManager.editLayer = layer

    cmds.undoInfo( swf=False )
    g_layerManager.EditLayer()
    cmds.undoInfo( swf=True )

#-------------------------------------------------------------------------------------------
#   レイヤー情報変更
#-------------------------------------------------------------------------------------------
def UpdateLayerValue(layerIndex):

    global g_layerManager

    layer = g_layerManager.GetLayerFromIndex(layerIndex)

    if layer == None:
        return

    cmds.undoInfo( swf=False )
    layer.UpdateValue()
    cmds.undoInfo( swf=True )

#-------------------------------------------------------------------------------------------
#   レイヤー可視変更
#-------------------------------------------------------------------------------------------
def UpdateLayerVisible(layerIndex):

    global g_layerManager

    layer = g_layerManager.GetLayerFromIndex(layerIndex)

    if layer == None:
        return

    cmds.undoInfo( swf=False )
    layer.ToggleVisible()
    cmds.undoInfo( swf=True )

#-------------------------------------------------------------------------------------------
#   レイヤー結合
#-------------------------------------------------------------------------------------------
def MergeAllLayer():

    global g_layerManager

    cmds.undoInfo( swf=False )

    selectList = cmds.ls(sl=True,l=True)
        
    g_layerManager.MergeColor();

    cmds.undoInfo( swf=True )

    if selectList == None:
        return

    if len(selectList) == 0:
        return

    cmds.undoInfo( swf=False )
    cmds.select(selectList,r=True)
    cmds.undoInfo( swf=True )

#**************************************************************************************************************************
#   その他
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   トランスフォームリスト取得
#-------------------------------------------------------------------------------------------
def GetTransformList():

    tempTransList = []
    
    selectList = cmds.ls(sl=True,l=True)
    hiliteList = cmds.ls(hl=True,l=True)

    if selectList == None:
        selectList = []

    if hiliteList != None:
        for hilite in hiliteList:
            selectList.append(hilite)

    if len(selectList) == 0:
        return tempTransList

    for select in selectList:

        #メッシュではない場合はShapeを探し登録
        if cmds.objectType( select ) != "transform":
            tempList = cmds.listRelatives( select, ap=True, f=True )

            if tempList == None:
                continue

            if len(tempList) == 0:
                continue

            if cmds.objectType( tempList[0] ) != "mesh":
                continue

            tempList = cmds.listRelatives( tempList[0], ap=True, f=True )

            if len(tempList) == 0:
                continue

            if cmds.objectType( tempList[0] ) != "transform":                
                continue

            tempTransList.append(tempList[0])
            
            continue

        shapeList = cmds.listRelatives( select, s=True, f=True )

        if shapeList == None:
            continue

        if len(shapeList) == 0:
            continue

        if cmds.objectType( shapeList[0] ) != "mesh":
            continue

        tempTransList.append(select)

    #重複回避
    resultTransList = []    
    for tempTrans in tempTransList:
        
        exist = False
        for trans in resultTransList:
            if trans == tempTrans:
                exist=True
                break

        if exist == False:
            resultTransList.append(tempTrans)
    
    return resultTransList

#-------------------------------------------------------------------------------------------
# カラーセットが存在するかどうか
#-------------------------------------------------------------------------------------------
def ExistColorSet(target, searchName):

    if searchName == "":
        return False

    colorSetList = cmds.polyColorSet(target, q=True, allColorSets=True)

    if colorSetList == None:
        return False

    if len(colorSetList) == 0:
        return False

    for colorSet in colorSetList:

        if colorSet == searchName:
            return True

    return False

#-------------------------------------------------------------------------------------------
# カラーセットをリネーム
#-------------------------------------------------------------------------------------------
def RenameColorSet(target, currentName, newName):

    currentColorSetList = cmds.polyColorSet(target, q=True, currentColorSet=True)

    if ExistColorSet(target, currentName) == False:
        return

    if ExistColorSet(target, newName) == True:
        return

    vertexInfo = GetVertexColorInfo(target)

    cmds.polyColorSet(target, colorSet=currentName, rn=True, newColorSet=newName);

    SetVertexColorInfo(target, vertexInfo)

#-------------------------------------------------------------------------------------------
# 頂点番号順で並べ替えた頂点フェースリスト取得
#-------------------------------------------------------------------------------------------
def GetVertexFaceList(target):

    if cmds.objectType(target) != "transform":
        return []
    
    vertexFaceList = cmds.ls(target + ".vtxFace[*][*]",fl=True,l=True)

    if len(vertexFaceList) == []:
        return

    maxDigit = 10

    tempVertexFaceList = []
    for cnt in range(0, len(vertexFaceList)):

        vtxFace = vertexFaceList[cnt]

        startIndex = vtxFace.find("[")
        endIndex = vtxFace.find("]")

        faceStartIndex = vtxFace.rfind("[")
        faceEndIndex = vtxFace.rfind("]")

        thisVtxIndex = vtxFace[startIndex + 1:endIndex]
        thisVtxFaceIndex = vtxFace[faceStartIndex + 1:faceEndIndex]

        thisFixVtxIndex = GetNumWithDigit(thisVtxIndex,maxDigit)
        thisFixVtxFaceIndex = GetNumWithDigit(thisVtxFaceIndex,maxDigit)

        tempVtxFaceName = thisFixVtxIndex + "_" + thisFixVtxFaceIndex + "@" + vtxFace

        tempVertexFaceList.append(tempVtxFaceName)

    tempVertexFaceList.sort()
    vertexFaceList = []
    for tempVtxFace in tempVertexFaceList:
        startIndex = tempVtxFace.find("@")
        endIndex = len(tempVtxFace)

        newVtxFaceName = tempVtxFace[startIndex + 1:endIndex]

        vertexFaceList.append(newVtxFaceName)
    
    return vertexFaceList

#-------------------------------------------------------------------------------------------
# 番号を桁数有りで取得
#-------------------------------------------------------------------------------------------
def GetNumWithDigit(target, digit):

    numStr = str(target)

    if len(numStr) >= digit:
        return numStr

    addDigit = digit - len(numStr)

    addStr = ""
    for cnt in range(0,addDigit):
        addStr += "0"

    return addStr + numStr


#-------------------------------------------------------------------------------------------
# 頂点フェースリストから頂点リストとそのカラーリストを取得
#-------------------------------------------------------------------------------------------
def GetVertexListAndVertexColorList(vtxFaceList, vtxFaceColorList):

    resultList = [[],[]]

    if len(vtxFaceList) == 0:
        return resultList

    if len(vtxFaceColorList) == 0:
        return resultList

    if len(vtxFaceList) != len(vtxFaceColorList):
        return resultList

    dotStartIndex = vtxFaceList[0].find(".")
    transformName = vtxFaceList[0][0:dotStartIndex]

    prevVtxIndex = -100

    startColor = None
    isSameColor = False

    resultVtxList = []
    resultVtxColorList = []
    tempList = []
    tempColorList = []

    for cnt in range(0, len(vtxFaceList)):

        #頂点番号,頂点フェース番号の収集        
        vtxFace = vtxFaceList[cnt]
        vtxFaceColor = vtxFaceColorList[cnt]

        startIndex = vtxFace.find("[")
        endIndex = vtxFace.find("]")

        faceStartIndex = vtxFace.rfind("[")
        faceEndIndex = vtxFace.rfind("]")

        thisVtxIndex = vtxFace[startIndex + 1:endIndex]
        thisVtxFaceIndex = vtxFace[faceStartIndex + 1:faceEndIndex]

        if prevVtxIndex != thisVtxIndex:

            #結果に登録処理
            if isSameColor == True:
                resultVtxList.append(transformName + ".vtx[" + prevVtxIndex + "]")
                resultVtxColorList.append(vtxFaceColorList[cnt - 1])
            else:

                if len(tempList) > 0:
                    resultVtxList.extend(tempList)
                    resultVtxColorList.extend(tempColorList)

            #初期化
            startColor = vtxFaceColor
            isSameColor = True
            tempList = []
            tempColorList = []

        tempList.append(vtxFace)
        tempColorList.append(vtxFaceColor)

        if IsSameColor(startColor, vtxFaceColor) == False:
            isSameColor = False

        if  cnt == len(vtxFaceList) - 1:
            
            if isSameColor == True:
                resultVtxList.append(transformName + ".vtx[" + thisVtxIndex + "]")
                resultVtxColorList.append(vtxFaceColor)
            else:

                if len(tempList) > 0:
                    resultVtxList.extend(tempList)
                    resultVtxColorList.extend(tempColorList)

        prevVtxIndex = thisVtxIndex

    resultList[0] = resultVtxList
    resultList[1] = resultVtxColorList

    return resultList

#-------------------------------------------------------------------------------------------
# 頂点フェースリストから頂点カラーリスト取得
#-------------------------------------------------------------------------------------------
def GetVertexColorList(vtxFaceList):

    tempVtxFaceColorList = []

    existVtxColor = True
    try:        
        tempVtxFaceColorList = cmds.polyColorPerVertex(vtxFaceList, q=True, r=True, g=True, b=True, a=True)
    except:
        existVtxColor = False

    if existVtxColor == False:
        return []
    
    vertexColorList = []
    for q in range(0,len(tempVtxFaceColorList) / 4):

        vtxColor = [0,0,0,0]
        vtxColor[0] = tempVtxFaceColorList[q * 4 + 0]
        vtxColor[1] = tempVtxFaceColorList[q * 4 + 1]
        vtxColor[2] = tempVtxFaceColorList[q * 4 + 2]
        vtxColor[3] = tempVtxFaceColorList[q * 4 + 3]

        vertexColorList.append(FixColor(vtxColor))

    tempVtxFaceColorList = None

    return vertexColorList

#-------------------------------------------------------------------------------------------
# カラーを比較
#-------------------------------------------------------------------------------------------
def IsSameColor(srcColor, dstColor):

    precision = 1000.0

    if srcColor == None:
        return False

    if dstColor == None:
        return False

    if len(srcColor) != 4:
        return False

    if len(dstColor) != 4:
        return False

    tempSrc = []
    tempDst = []

    for cnt in range(0,4):
        tempSrcValue = int(srcColor[cnt] * precision)
        tempdstValue = int(dstColor[cnt] * precision)

        tempSrc.append(tempSrcValue)
        tempDst.append(tempdstValue)

    if IsSameColorValue(tempSrc[0],tempDst[0]) == False:
        return False

    if IsSameColorValue(tempSrc[1],tempDst[1]) == False:
        return False

    if IsSameColorValue(tempSrc[2],tempDst[2]) == False:
        return False

    if IsSameColorValue(tempSrc[3],tempDst[3]) == False:
        return False

    return True

#-------------------------------------------------------------------------------------------
# 同じ値かどうか
#-------------------------------------------------------------------------------------------
def IsSameColorValue(srcValue, dstValue):

    diffValue = srcValue - dstValue
    if diffValue < 0:
        diffValue = -diffValue

    if diffValue <= 1:
        return True

    return False

#-------------------------------------------------------------------------------------------
# カラーを補正
#-------------------------------------------------------------------------------------------
def FixColor(srcColor):

    precision = 1000.0

    for cnt in range(0,4):
        srcColor[cnt] = int(srcColor[cnt] * precision)
        srcColor[cnt] /= precision

    return srcColor


#**************************************************************************************************************************
#   頂点カラーコピーペースト
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
# 頂点カラーをコピー
#-------------------------------------------------------------------------------------------
def CopyVertexColor():

    global g_copyVtxColorInfo

    g_copyVtxFaceList = []
    g_copyVtxColorList = []

    selectList = cmds.ls(sl=True,l=True)

    transList = GetTransformList()

    if len(transList) == 1:

        trans = transList[0]

        cmds.undoInfo( swf=False )
        g_copyVtxColorInfo = GetVertexColorInfo(trans)
        cmds.undoInfo( swf=True )

    if selectList == None:
        return

    if len(selectList) == 0:
        return

    cmds.undoInfo( swf=False )
    cmds.select(selectList,r=True)
    cmds.undoInfo( swf=True )


#-------------------------------------------------------------------------------------------
# 頂点カラーをペースト
#-------------------------------------------------------------------------------------------
def PasteVertexColor():

    global g_copyVtxColorInfo

    if cmds.confirmDialog(t="Confirm", m="Paste Vertex Color ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    selectList = cmds.ls(sl=True,l=True)

    transList = GetTransformList()

    if len(transList) == 1:

        trans = transList[0]

        cmds.undoInfo( swf=False )
        SetVertexColorInfo(trans, g_copyVtxColorInfo)
        cmds.undoInfo( swf=True )

    if selectList == None:
        return

    if len(selectList) == 0:
        return

    cmds.undoInfo( swf=False )
    cmds.select(selectList,r=True)
    cmds.undoInfo( swf=True )

#-------------------------------------------------------------------------------------------
# 頂点カラーコピーリストを取得
#-------------------------------------------------------------------------------------------
def GetVertexColorInfo(target):

    vtxFaceList = GetVertexFaceList(target)

    vtxColorList = GetVertexColorList(vtxFaceList)

    return [vtxFaceList,vtxColorList]

#-------------------------------------------------------------------------------------------
# 頂点カラーコピーリストを取得
#-------------------------------------------------------------------------------------------
def SetVertexColorInfo(target,vtxColorInfo):

    if vtxColorInfo == None:
        return

    if len(vtxColorInfo) != 2:
        return

    if vtxColorInfo[0] == []:
        return

    if vtxColorInfo[1] == []:
        return

    if len(vtxColorInfo[0]) != len(vtxColorInfo[1]):
        return

    currentVtxColorInfo = GetVertexColorInfo(target)

    diffVtxColorInfo = GetDifferentVertexColorInfo(currentVtxColorInfo, vtxColorInfo)

    if len(diffVtxColorInfo[0]) == 0:
        return

    StartProgress("Paset Vertex Color")

    for p in range(0,len(diffVtxColorInfo[0])):

        thisVtxFace = diffVtxColorInfo[0][p]
        thisColor = diffVtxColorInfo[1][p]

        cmds.polyColorPerVertex(thisVtxFace, r=thisColor[0], g=thisColor[1], b=thisColor[2], a=thisColor[3], cla=True, nun=True, cdo=True)

        progress = float(p) / len(diffVtxColorInfo[0])
        progressStr = str(p) + "/" + str(len(diffVtxColorInfo[0]))

        if UpdateProgress(progress,"Pasting Color " + progressStr) == False:
            EndProgress()
            break

    EndProgress()

#-------------------------------------------------------------------------------------------
# 頂点カラーコピーリストを取得
#-------------------------------------------------------------------------------------------
def GetDifferentVertexColorInfo(srcColorInfo, dstColorInfo):

    resultVtxColorInfo = [[],[]]

    for p in range(0,len(srcColorInfo[0])):

        srcVtxFace = srcColorInfo[0][p]
        srcVtxColor = srcColorInfo[1][p]

        if p >= len(dstColorInfo[0]):
            break

        dstVtxFace = dstColorInfo[0][p]
        dstVtxColor = dstColorInfo[1][p]

        if IsSameColor(srcVtxColor, dstVtxColor) == True:
            continue

        resultVtxColorInfo[0].append(dstVtxFace)
        resultVtxColorInfo[1].append(dstVtxColor)

    return resultVtxColorInfo
    
#-------------------------------------------------------------------------------------------
#   レイヤーマネージャー
#-------------------------------------------------------------------------------------------
class LayerManager:

    #===========================================
    # コンストラクタ
    #===========================================
    def __init__(self):

        self.id = CyUtility.GetRandomString(15)

        self.flagPrefix = "____"
        self.colorSetPrefix = "CyVCL_"
        self.baseLayerName = "BaseLayer"
        self.resultColorSet = "colorSet1"

        self.colorLayerList = []

        self.isSingle = False

        self.editLayer = None
        self.keepEditingLayer = False

        self.layerMaxNum = 64

        self.layerInterval = 10

        self.editColor = (0.4,0.8,0.8)
        self.waitColor = (0.7,0.7,0.8)

        self.disableColor = (0.3,0.3,0.3)

        self.warningColor = (0.9,0.5,0.5)

        self.layerAddColor = (0.6,0.6,0.8)
        self.layerMoveColor = (0.7,0.7,0.5)
        self.layerMergeColor = (0.5,0.7,0.5)

        self.copyVtxColorColor = (0.6,0.6,0.8)
        self.pasteVtxColorColor = (0.6,0.8,0.6)

        self.progStart = 0
        self.progCurrent = 0
        self.progEnd = 0
        self.progInfo = ""
        self.progSubInfo = ""

    #===========================================
    # カラーセットからロード
    #===========================================
    def LoadFromColorSet(self):

        global g_currentTransformList

        self.isSingle = False

        self.colorLayerList = []

        self.isSingle = False
        if len(g_currentTransformList) == 1:
            self.isSingle = True

        existLayerColorSet = True
        for trans in g_currentTransformList:

            if self.ExistDefaultColorSet(trans) == False:
                existLayerColorSet = False
                break

        if existLayerColorSet == True:

            self.UpdateLayerListAll()

        if len(self.colorLayerList) != 0:

            if self.keepEditingLayer == True:

                for trans in g_currentTransformList:
                    
                    currentColorSet = cmds.polyColorSet(trans, q=True, currentColorSet=True)[0]

                    for colorLayer in self.colorLayerList:
                        
                        thisColorSetName = colorLayer.GetShortColorSet("")

                        if currentColorSet.find(thisColorSetName) == 0:
                            self.editLayer = colorLayer
                            break
            else:

                for trans in g_currentTransformList:
                    cmds.polyColorSet(trans, currentColorSet=True, colorSet=self.resultColorSet)

                self.editLayer = None

        else:
            
            self.editLayer = None

        self.UpdateUI()

    #===========================================
    # デフォルトカラーセットの存在確認
    #===========================================
    def CheckSameLayer(self, target):

        thisLayerList = self.UpdateLayerList(target)

        if len(thisLayerList) != len(self.colorLayerList):
            return False

        for p in range(0, len(thisLayerList)):

            thisLayer = thisLayerList[p]
            thisOriginalLayer = self.colorLayerList[p]

            if thisLayer.name != thisOriginalLayer.name:
                thisOriginalLayer.sameName = False

            if thisLayer.priority != thisOriginalLayer.priority:
                thisOriginalLayer.samePriority = False

            if thisLayer.blendMode != thisOriginalLayer.blendMode:
                thisOriginalLayer.sameBlendMode = False

            if thisLayer.alpha != thisOriginalLayer.alpha:
                thisOriginalLayer.sameAlpha = False

            if thisLayer.visible != thisOriginalLayer.visible:
                thisOriginalLayer.sameVisible = False

        return True

    #===========================================
    # レイヤーシステムの割り当て
    #===========================================
    def ApplySystem(self):

        global g_currentTransformList

        for trans in g_currentTransformList:

            if self.ExistDefaultColorSet(trans) == True:
                continue

            self.AddDefaultColorSet(trans)

        self.LoadFromColorSet()

    #===========================================
    # デフォルトカラーセットを追加
    #===========================================
    def AddDefaultColorSet(self, target):
        
        if ExistColorSet(target, self.resultColorSet) == False:
            cmds.polyColorSet(target, create=True, clamped=1, rpt="RGBA", colorSet=self.resultColorSet, perInstance=False, unshared=False)

        colorSetList = self.GetFullColorSetList(target)

        if len(colorSetList) != 0:
            return

        #頂点フェースリスト
        vtxFaceList = GetVertexFaceList(target)

        #頂点フェースリストから頂点カラー取得
        vertexColorList = GetVertexColorList(vtxFaceList)

        #重複しているカラーリスト
        fixVtxColorList = self.GetFixColorList(vertexColorList)

        #レイヤーセット作成
        tempLayer = Layer(self)        
        tempLayer.CreateColorSet(target, self.baseLayerName, 0)
        
        for vtxColor in fixVtxColorList:

            targetVtxList = self.GetVtxListFromVtxColor(vtxColor, vtxFaceList, vertexColorList, None, 0)

            if len(targetVtxList) == 0:
                continue

            #リザルトカラーセットに切り替えてカラーコピー
            cmds.polyColorSet(target, currentColorSet=True, colorSet=self.resultColorSet)

            cmds.polyColorPerVertex(targetVtxList, rgb=[vtxColor[0],vtxColor[1],vtxColor[2]],a=vtxColor[3], nun=False, cla=True, cdo=True)

            #デフォルトカラーセットに切り替えてカラーコピー
            self.SetCurrentColorSet(target, tempLayer.GetShortColorSet(""))

            cmds.polyColorPerVertex(targetVtxList, rgb=[vtxColor[0],vtxColor[1],vtxColor[2]],a=vtxColor[3], nun=False, cla=True, cdo=True)

    #===========================================
    # レイヤーシステム削除
    #===========================================
    def DeleteSystem(self):

        return

        self.editLayer = None

        self.MergeColor()

        transList = GetTransformList()

        for trans in transList:

            if self.ExistDefaultColorSet(trans) == F:
                continue

            cmds.polyColorSet(trans, colorSet=colorSet, rn=True, newColorSet=newColorSetName);

        self.adFromColorSet()

    #===========================================
    # カラーセットへ保存
    #===========================================
    def SaveToColorSet(self):

        global g_currentTransformList

        for layer in self.colorLayerList:

            for trans in g_currentTransformList:

                layer.SaveToColorSet(trans)

    #===========================================
    # 現在のカラーセットに設定
    #===========================================
    def SetCurrentColorSet(self, target, shortColorSet):

        fullColorSet = self.GetFullColorSetFromShortColorSet(target, shortColorSet)

        if fullColorSet == "":
            return

        cmds.polyColorSet(target, currentColorSet=True, colorSet=fullColorSet)

    #===========================================
    # 現在のカラーセットに設定
    #===========================================
    def RenameColorSet(self, target, srcFullColorSet, dstShortColorSet):

        thisId  = self.GetLayerId(srcFullColorSet)

        if thisId == "":
            thisId = CyUtility.GetRandomString(5)

        RenameColorSet(target, srcFullColorSet, dstShortColorSet + self.flagPrefix + "id_" + thisId)

    #===========================================
    # フルカラーセットからIDを取得
    #===========================================
    def GetLayerId(self, fullColorSet):

        thisId  = self.GetFlagValue(fullColorSet,"id","")

        return thisId

    #===========================================
    # デフォルトカラーセットの存在確認
    #===========================================
    def ExistDefaultColorSet(self, target):

        if ExistColorSet(target, self.resultColorSet) == False:
            return False

        colorSetList = self.GetFullColorSetList(target)

        if len(colorSetList) == 0:
            return False

        return True

    #===========================================
    # レイヤーカラーセットリスト取得
    #===========================================
    def GetFullColorSetList(self,target):

        colorSetList = cmds.polyColorSet(target, q=True, allColorSets=True)

        if colorSetList == None:
            return []

        if len(colorSetList) == 0:
            return []

        resultList = []
        
        for colorSet in colorSetList:

            if colorSet.find(self.colorSetPrefix) != 0:
                continue

            if colorSet.find(self.resultColorSet) != -1:
                continue

            resultList.append(colorSet)

        return resultList

    #===========================================
    # 全レイヤーリスト更新
    #===========================================
    def UpdateLayerListAll(self):

        global g_currentTransformList

        self.colorLayerList = []

        for p in range(0, len(g_currentTransformList)):

            trans = g_currentTransformList[p]

            tempList = self.UpdateLayerList(trans)

            if p == 0:
                 self.colorLayerList = tempList

        existSame = True
        for p in range(0, len(g_currentTransformList)):

            trans = g_currentTransformList[p]

            if p == 0:
                continue

            if self.CheckSameLayer(trans) == False:
                existSame = False
                break

        if existSame == False:
            self.colorLayerList = []

    #===========================================
    # レイヤーリスト更新
    #===========================================
    def UpdateLayerList(self,target):
                    
        thisFullColorSetList = self.GetFullColorSetList(target)
        thisSortLayerList = []

        for fullColorSet in thisFullColorSetList:

            newLayer = Layer(self)
            newLayer.LoadFromColorSet(fullColorSet)

            thisSortLayerList.append(newLayer)

        sortLayerInfo = self.GetSortedLayerInfo(thisSortLayerList, thisFullColorSetList)

        rewriteColorSet = False
        
        for cnt in range(0,len(sortLayerInfo[0])):

            sortLayer = sortLayerInfo[0][cnt]
            thisFullColorSet = sortLayerInfo[1][cnt]

            sortColorSet = sortLayer.GetShortColorSet("")

            if thisFullColorSet.find(sortColorSet) != 0:
                rewriteColorSet = True
                break

        if rewriteColorSet == True:
            
            for cnt in range(0,len(sortLayerInfo[0])):

                sortLayer = sortLayerInfo[0][cnt]
                thisFullColorSet = sortLayerInfo[1][cnt]
                
                sortColorSet = sortLayer.GetShortColorSet("")

                if thisFullColorSet.find(sortColorSet) == 0:
                    continue

                self.RenameColorSet(target, thisFullColorSet, sortColorSet)

        thisFullColorSetList = None
        thisSortLayerList = None

        return sortLayerInfo[0]

    #===========================================
    # レイヤーリストをソート
    #===========================================
    def GetSortedLayerInfo(self, layerList, layerColorSetList):

        resultLayerList = []
        resultLayerColorSetList = []

        for layer in layerList:

            tempResult = self.GetMaxPriorityLayerInfo(layerList, layerColorSetList, resultLayerList)

            if tempResult != None:
                
                resultLayerList.append(tempResult[0])
                resultLayerColorSetList.append(tempResult[1])

        index=0
        for layer in resultLayerList:

            layer.priority = len(resultLayerList) - 1 - index
            layer.priority *= self.layerInterval

            layer.index = len(resultLayerList) - index - 1
            
            index+=1
        
        return [resultLayerList,resultLayerColorSetList]

    #===========================================
    # レイヤーカラーセットを番号で取得
    #===========================================
    def GetFullColorSetFromIndex(self, target, index):

        layerList = self.UpdateLayerList(target)

        if layerList == None:
            return ""

        if len(layerList) == 0:
            return ""

        tempIndex = int(index)

        shortColorSet = ""

        if tempIndex <= 0:
            shortColorSet = layerList[len(layerList) - 1].GetShortColorSet("")

        if tempIndex >= len(layerList):
            shortColorSet = layerList[0].GetShortColorSet(target)

        if shortColorSet == "":
            shortColorSet = layerList[len(layerList) - 1 - tempIndex].GetShortColorSet("")

        if shortColorSet == "":
            return ""

        return self.GetFullColorSetFromShortColorSet(target, shortColorSet)

    #===========================================
    # レイヤーカラーセット取得
    #===========================================
    def GetFullColorSetFromShortColorSet(self, target, shortColorSet):

        fullColorSetList = self.GetFullColorSetList(target)

        if len(fullColorSetList) == 0:
            return ""

        for fullColorSet in fullColorSetList:

            if fullColorSet.find(shortColorSet) == 0:
                return fullColorSet

        return ""

    #===========================================
    # レイヤーを番号で取得
    #===========================================
    def GetLayerFromIndex(self, index):

        if self.colorLayerList == None:
            return None

        if len(self.colorLayerList) == 0:
            return None

        tempIndex = int(index)

        if tempIndex <= 0:
            return self.colorLayerList[len(self.colorLayerList) - 1]

        if tempIndex >= len(self.colorLayerList):
            return self.colorLayerList[0]

        return self.colorLayerList[len(self.colorLayerList) - 1 - tempIndex]

    #===========================================
    # 最大プライオリティをもつレイヤーを取得
    #===========================================
    def GetMaxPriorityLayerInfo(self, layerList, colorSetList, exceptLayerList):

        maxPriority = -100000
        result = None

        for cnt in range(0, len(layerList)):

            layer = layerList[cnt]
            colorSet = colorSetList[cnt]

            exist = False
            for exceptLayer in exceptLayerList:
                if exceptLayer == layer:
                    exist = True
                    break

            if exist == True:
                continue

            if layer.priority > maxPriority:
                maxPriority = layer.priority
                result = [layer, colorSet]

        return result

    #===========================================
    # フラグ値を取得
    #===========================================
    def GetFlagValue(self, target, flagKey, defaultValue):

        targetFlag = self.flagPrefix + flagKey + "_"

        if target.find(targetFlag) == -1:
            return defaultValue
        
        flagIndex = target.find(targetFlag)
        valueIndex = flagIndex + len(targetFlag)
        nextFlagIndex = target.find(self.flagPrefix, valueIndex)

        if nextFlagIndex == -1:
            nextFlagIndex = len(target)

        result = target[valueIndex:nextFlagIndex]
                
        return result

    #===========================================
    # UI構築
    #===========================================
    def UpdateUI(self):

        global g_uiPrefix
        global g_currentTransformList

        UnvisibleAllLayerUI()

        if len(g_currentTransformList) == 0:
            cmds.button(g_uiPrefix + "StartSystem", e=True, en=False,bgc=self.disableColor)
            cmds.columnLayout(g_uiPrefix + "LayerMain", e=True, en=False)
            return

        if len(self.colorLayerList) == 0:
            cmds.button(g_uiPrefix + "StartSystem", e=True, en=True,bgc=self.warningColor)
            cmds.columnLayout(g_uiPrefix + "LayerMain", e=True, en=False)
            return

        cmds.button(g_uiPrefix + "StartSystem", e=True, en=False,bgc=self.disableColor)
        cmds.columnLayout(g_uiPrefix + "LayerMain", e=True, en=True)

        for layer in self.colorLayerList:

            layer.UpdateUI()

        cmds.checkBox(g_uiPrefix + "CheckKeepEdit", e=True, v=self.keepEditingLayer)

        self.UpdateEditButton()

    #===========================================
    # エディットボタン更新
    #===========================================
    def UpdateEditButton(self):

        for layer in self.colorLayerList:

            layer.EnableEditButton(False)

        if self.editLayer != None:
            self.editLayer.EnableEditButton(True)

    #===========================================
    # 編集レイヤーを変更
    #===========================================
    def EditLayer(self):

        global g_currentTransformList

        if self.editLayer != None:
            for trans in g_currentTransformList:
                self.editLayer.Edit(trans)            
        else:
            for trans in g_currentTransformList:
                cmds.polyColorSet(trans, currentColorSet=True, colorSet=self.resultColorSet)

        self.UpdateUI()

    #===========================================
    # レイヤーを追加
    #===========================================
    def AddLayer(self):

        global g_currentTransformList

        if len(self.colorLayerList) == self.layerMaxNum:
            return

        targetPriority = 10000
        targetIndex = 10000
        if self.editLayer != None:
            targetPriority = self.editLayer.priority + 1;
            targetIndex = self.editLayer.index + 1;
        
        for trans in g_currentTransformList:

            tempLayer = Layer(self)
            tempLayer.CreateColorSet(trans, "NewLayer", targetPriority)
        
        self.UpdateLayerListAll()

        self.editLayer = self.GetLayerFromIndex(targetIndex)
        
        self.EditLayer()
            
    #===========================================
    # レイヤーを削除
    #===========================================
    def DeleteLayer(self):

        global g_currentTransformList

        if self.editLayer == None:
            return

        if self.editLayer.isBase == True:
            return

        if cmds.confirmDialog(t="Confirm", m="Delete layer ? This layer is " + self.editLayer.name, b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
            return

        if len(self.colorLayerList) == 1:
            return
            
        self.colorLayerList.remove(self.editLayer)
        
        for trans in g_currentTransformList:

            self.editLayer.Delete(trans)

        self.UpdateLayerListAll()

        self.editLayer = self.GetLayerFromIndex(10000)

        self.EditLayer()

    #===========================================
    # レイヤーを移動
    #===========================================
    def MoveLayer(self, isUp):

        global g_currentTransformList

        if self.editLayer == None:
            return

        if self.editLayer.isBase == True:
            return

        if isUp == True:
            self.editLayer.priority += self.layerInterval + 1
        else:
            self.editLayer.priority -= self.layerInterval + 1

        if self.editLayer.priority <= 0:
            self.editLayer.priority = 1;

        for trans in g_currentTransformList:

            self.editLayer.SaveToColorSet(trans)
            
        self.UpdateLayerListAll()

        targetIndex = 0
        
        if isUp == True:
            targetIndex = self.editLayer.index + 1
        else:
            targetIndex = self.editLayer.index - 1

        if targetIndex <= 0:
            targetIndex = 1

        self.editLayer = self.GetLayerFromIndex(targetIndex)
        
        self.EditLayer()

    #===========================================
    # カラー情報を結合
    #===========================================
    def MergeColor(self):

        global g_uiPrefix
        global g_currentTransformList

        if len(self.colorLayerList) == 0:
            return

        self.editLayer = None
        self.EditLayer()

        cmds.undoInfo( swf=False )

        for trans in g_currentTransformList:

            StartProgress("Calculate Color...")
            
            vtxFaceList = GetVertexFaceList(trans)

            #現在の結合頂点カラーリスト取得
            self.progStart = 0            
            self.progEnd = 10
            self.progInfo = "Get Current Vertex Color..."
            self.progSubInfo = ""
            
            cmds.polyColorSet(trans, currentColorSet=True, colorSet=self.resultColorSet)
            currentVtxFaceColorList = GetVertexColorList(vtxFaceList)

            if self.UpdateProgress() == False:
                EndProgress()
                return
            
            #新しい結合頂点カラーリスト取得
            self.progStart = 10            
            self.progEnd = 30
            self.progInfo = "Get Result Vertex Color..."
            self.progSubInfo = ""
            
            vtxColorList = self.GetMergedVertexColorList(trans,vtxFaceList)

            #レイヤー切り替え
            self.progStart = 30            
            self.progEnd = 40
            self.progInfo = "Get Target Vertex Color..."
            self.progSubInfo = ""
            
            cmds.polyColorSet(trans, currentColorSet=True, colorSet=self.resultColorSet)

            currentTempList = GetVertexListAndVertexColorList(vtxFaceList,currentVtxFaceColorList)
            newTempList = GetVertexListAndVertexColorList(vtxFaceList,vtxColorList)

            currentVtxList = currentTempList[0]
            currentVtxCList = currentTempList[1]
            
            newVtxList = newTempList[0]
            newVtxCList = newTempList[1]

            targetVtxList = []
            targetVtxCList = []

            for p in range(0,len(newVtxList)):

                self.progCurrent = float(p) / len(newVtxList)
                self.progSubInfo = str(p) + "/" + str(len(newVtxList))
                
                if self.UpdateProgress() == False:
                    break

                newVtx = newVtxList[p]
                newColor = newVtxCList[p]

                existVtx = False

                for q in range(0,len(currentVtxList)):

                    currentVtx = currentVtxList[q]
                    currentColor = currentVtxCList[q]

                    if newVtx == currentVtx and IsSameColor(newColor, currentColor) == True:
                        existVtx = True
                        break

                if existVtx == True:
                    continue

                targetVtxList.append(newVtx)
                targetVtxCList.append(newColor)

            if self.UpdateProgress() == False:
                EndProgress()
                return

            #レイヤー切り替え
            self.progStart = 40            
            self.progEnd = 100
            self.progInfo = "Bake Result Color..."

            for p in range(0,len(targetVtxList)):

                thisVtx = targetVtxList[p]
                thisColor = targetVtxCList[p]

                cmds.polyColorPerVertex(thisVtx, r=thisColor[0], g=thisColor[1], b=thisColor[2], a=thisColor[3], cla=True, nun=True)

                self.progCurrent = float(p) / len(targetVtxList)
                self.progSubInfo = str(p) + "/" + str(len(targetVtxList))

                if self.UpdateProgress() == False:
                    break

            if self.UpdateProgress() == False:
                EndProgress()
                return

        EndProgress()

        cmds.undoInfo( swf=True )

    #===========================================
    # カラー情報を結合
    #===========================================
    def GetMergedVertexColorList(self, target, vtxFaceList):
        
        self.progCurrent = 0

        vertexColorList = []

        layerList = self.UpdateLayerList(target)

        for p in range(0, len(layerList)):

            thisLayer = layerList[len(layerList) - 1 - p]
            thisLayerShortColorSet = thisLayer.GetShortColorSet("")

            thisLayerBlendMode = thisLayer.blendMode
            thisLayerAlpha = thisLayer.alpha * thisLayer.visible

            self.SetCurrentColorSet(target, thisLayerShortColorSet)
            
            vtxFaceColorList = cmds.polyColorPerVertex(vtxFaceList, q=True, r=True, g=True, b=True, a=True)

            for q in range(0,len(vtxFaceColorList) / 4):

                vtxColor = [0,0,0,0]
                vtxColor[0] = vtxFaceColorList[q * 4 + 0]
                vtxColor[1] = vtxFaceColorList[q * 4 + 1]
                vtxColor[2] = vtxFaceColorList[q * 4 + 2]
                vtxColor[3] = vtxFaceColorList[q * 4 + 3]

                if len(vertexColorList) != len(vtxFaceList):
                    vertexColorList.append(vtxColor)
                else:

                    vtxAlpha = vtxColor[3] * thisLayerAlpha

                    if vtxAlpha == 0:
                        continue

                    vertexColorList[q][0] = self.BlendValue(vertexColorList[q][0], vtxColor[0], vtxAlpha, thisLayerBlendMode)
                    vertexColorList[q][1] = self.BlendValue(vertexColorList[q][1], vtxColor[1], vtxAlpha, thisLayerBlendMode)
                    vertexColorList[q][2] = self.BlendValue(vertexColorList[q][2], vtxColor[2], vtxAlpha, thisLayerBlendMode)

                if p == 0:
                    vertexColorList[q][3] = vtxColor[3]
                
                self.progCurrent = ((q + 1.0) * 4.0) / len(vtxFaceColorList) * 1.0 / len(layerList)
                self.progCurrent += float(p) / len(layerList)
                self.progSubInfo = ""

                if self.UpdateProgress() == False:
                    break

        tempVertexColorList = []        
        for vtxColor in vertexColorList:

            tempVertexColorList.append(FixColor(vtxColor))

        vertexColorList = tempVertexColorList

        vtxFaceList = None
        layerColorSetList = None

        return vertexColorList
    
    #===========================================
    # 重複なしの値リスト取得
    #===========================================
    def GetFixValueList(self, valueList):

        resultList = []

        for cnt in range(0, len(valueList)):

            thisValue = valueList[cnt]

            exist = False
            for cnt2 in range(0, len(resultList)):

                thisResult = resultList[cnt2]

                if thisValue == thisResult:
                    exist = True
                    break

            if exist == True:
                continue

            resultList.append(thisValue)

        return resultList

    #===========================================
    # 重複なしの値リスト取得
    #===========================================
    def GetFixColorList(self, colorList):

        resultColorList = []

        for cnt in range(0, len(colorList)):

            thisColor = colorList[cnt]

            exist = False
            for cnt2 in range(0, len(resultColorList)):

                thisResultColor = resultColorList[cnt2]

                if thisColor[0] == thisResultColor[0] and thisColor[1] == thisResultColor[1] and thisColor[2] == thisResultColor[2] and thisColor[3] == thisResultColor[3]:
                    exist = True
                    break

            if exist == True:
                continue

            resultColorList.append(thisColor)

        return resultColorList

    #===========================================
    # 値が一致する頂点フェースを取得
    #===========================================
    def GetVtxListFromVtxColor(self, targetColor, vtxList, vtxColorList, fixVtxColorList, currentFixIndex):

        resultList = []

        for index in range(0,len(vtxList)):

            thisVtxFace = vtxList[index]
            thisVtxColor = vtxColorList[index]

            if fixVtxColorList != None:
                
                self.progCurrent = float(index + 1.0) / float(len(vtxList))
                self.progCurrent *= 1.0 / len(fixVtxColorList)
                self.progCurrent += float(currentFixIndex) / len(fixVtxColorList)

                if self.UpdateProgress() == False:
                    break

            if IsSameColor(thisVtxColor, targetColor) == False:
                continue

            resultList.append(thisVtxFace)

        return resultList

    #===========================================
    # 値をブレンド
    #===========================================
    def BlendValue(self, baseValue, overValue, overValueAlpha, blendMode):

        lerpValue0 = 1 - overValueAlpha
        lerpValue1 = overValueAlpha

        result = overValue * lerpValue1
        
        if blendMode == "Normal":
            
            result = baseValue * lerpValue0 + overValue * lerpValue1
            
        elif blendMode == "Add":
            
            result = baseValue * lerpValue0 + (baseValue + overValue) * lerpValue1
            
        elif blendMode == "Multiply":
            
            result = baseValue * lerpValue0 + (baseValue * overValue) * lerpValue1
            
        elif blendMode == "Overlay":

            if baseValue < 0.5:
                result = baseValue * overValue * 2.0
            else:
                result = 1.0 - 2.0 * (1.0 - baseValue ) * ( 1.0 - overValue )

            result *= lerpValue1
            result += baseValue * lerpValue0
            
        elif blendMode == "Screen":

            result = 1.0 - (1.0 - baseValue ) * ( 1.0 - overValue )
            result *= lerpValue1
            result += baseValue * lerpValue0
            
        return result

    #===========================================
    # プログレスバー更新
    #===========================================
    def UpdateProgress(self):

        global g_uiPrefix

        value = self.progStart + (self.progEnd - self.progStart) * self.progCurrent

        return UpdateProgress(value * 0.01, self.progInfo + " " + self.progSubInfo)

#-------------------------------------------------------------------------------------------
#   レイヤー
#-------------------------------------------------------------------------------------------
class Layer:

    #===========================================
    # コンストラクタ
    #===========================================
    def __init__(self, manager):

        self.index = 0
        self.manager = manager

        self.name = "NoName"
        self.blendMode = "Normal"
        self.visible = 1
        self.alpha = 1
        self.priority = 0

        self.sameName = True
        self.samePriority = True
        self.sameBlendMode = True
        self.sameVisible = True
        self.sameAlpha = True

        self.isBase = False
        
        self.parentLayer = None

    #===========================================
    # カラーセット作成処理
    #===========================================
    def CreateColorSet(self, target, name, priority):

        self.name = name
        self.blendMode = "Normal"
        self.alpha = 1.0
        self.visible = 1
        self.priority = priority

        newFullColorSet = self.GetShortColorSet("") + self.manager.flagPrefix + "id_" + CyUtility.GetRandomString(5)

        cmds.polyColorSet(target, create=True, clamped=True, rpt="RGBA", colorSet=newFullColorSet, perInstance=False, unshared=False)

        cmds.polyColorSet(target, currentColorSet=True, colorSet=newFullColorSet)

        cmds.polyColorPerVertex(target, rgb=[1.0,1.0,1.0], a=1.0, cla=True, nun=True)

    #===========================================
    # カラーセットからロード
    #===========================================
    def LoadFromColorSet(self, colorSet):

        self.colorSet = colorSet

        #名前取得
        if self.colorSet.find(self.manager.flagPrefix) == -1:
            self.name = self.colorSet[len(self.manager.colorSetPrefix):len(self.colorSet)]
        else:
            self.name = self.colorSet[len(self.manager.colorSetPrefix):self.colorSet.find(self.manager.flagPrefix)]

        #ベースレイヤー
        if self.name == self.manager.baseLayerName:
            self.isBase = True
            
        #ブレンド取得
        self.blendMode = "Normal"

        self.blendMode = self.manager.GetFlagValue(self.colorSet,"blend","Normal")
        self.blendMode = self.blendMode.capitalize()

        #アルファ値
        self.alpha = float(self.manager.GetFlagValue(self.colorSet,"alpha","1000"))
        self.alpha /= 1000.0

        #可視
        self.visible = int(self.manager.GetFlagValue(self.colorSet,"visible","1"))

        #優先度
        self.priority = int(self.manager.GetFlagValue(self.colorSet,"priority","0"))

    #===========================================
    # カラーセットへ保存
    #===========================================
    def SaveToColorSet(self, target):

        fullColorSet = self.manager.GetFullColorSetFromIndex(target, self.index)

        if fullColorSet == "":
            return

        newShortColorSet = self.GetShortColorSet(fullColorSet)

        if fullColorSet.find(newShortColorSet) == 0:
            return

        self.manager.RenameColorSet(target, fullColorSet, newShortColorSet)

    #===========================================
    # カラーセット名を取得
    #===========================================
    def GetShortColorSet(self, originalColorSetName):

        resultName = self.manager.colorSetPrefix

        if self.sameName == True or originalColorSetName == "":
            resultName += self.name
        else:
            resultName += self.GetNameFromColorSet(originalColorSetName)

        if self.sameBlendMode == True or originalColorSetName == "":
            resultName += self.manager.flagPrefix + "blend_" + self.blendMode
        else:
            resultName += self.manager.flagPrefix + "blend_" + self.manager.GetFlagValue(originalColorSetName,"blend","Normal")

        if self.sameAlpha == True or originalColorSetName == "":
            resultName += self.manager.flagPrefix + "alpha_" + str(int(self.alpha * 1000))
        else:
            resultName += self.manager.flagPrefix + "alpha_" + self.manager.GetFlagValue(originalColorSetName,"alpha","0")

        if self.sameVisible == True or originalColorSetName == "":
            resultName += self.manager.flagPrefix + "visible_" + str(int(self.visible))
        else:
            resultName += self.manager.flagPrefix + "visible_" + self.manager.GetFlagValue(originalColorSetName,"visible","1")

        if self.samePriority == True or originalColorSetName == "":
            resultName += self.manager.flagPrefix + "priority_" + str(int(self.priority))
        else:
            resultName += self.manager.flagPrefix + "priority_" + self.manager.GetFlagValue(originalColorSetName,"priority","0")

        return resultName

    #===========================================
    # カラーセットから名前取得
    #===========================================
    def GetNameFromColorSet(self,colorSetName):

        if colorSetName.find(self.manager.colorSetPrefix) != 0:
            return self.name

        if colorSetName.find(self.manager.flagPrefix) == -1:
            return self.name
        
        startIndex = len(self.manager.colorSetPrefix)
        endIndex = colorSetName.find(self.manager.flagPrefix)

        return colorSetName[startIndex:endIndex]
    
    #===========================================
    # 削除処理
    #===========================================
    def Delete(self, target):

        if self.isBase == True:
            return

        fullColorSet = self.manager.GetFullColorSetFromIndex(target, self.index)

        if fullColorSet == "":
            return

        cmds.polyColorSet(target, delete=True, colorSet=fullColorSet)

    #===========================================
    # 編集処理
    #===========================================
    def Edit(self, target):

        fullColorSet = self.manager.GetFullColorSetFromIndex(target, self.index)

        if fullColorSet == "":
            return

        cmds.polyColorSet(target, currentColorSet=True, colorSet=fullColorSet)

    #===========================================
    # UI更新
    #===========================================
    def UpdateUI(self):

        global g_uiPrefix

        enable = True
        if self.manager.isSingle == False or self.isBase == True:
            enable = False

        cmds.text(g_uiPrefix + "LayerIndex_" + str(self.index), e=True, label= str(self.index + 1))

        cmds.rowLayout( g_uiPrefix + "Layer_" + str(self.index), e=True, visible=True)

        cmds.textField(g_uiPrefix + "LayerName_" + str(self.index), e=True, text=self.name)
        cmds.optionMenu(g_uiPrefix + "LayerBlend_" + str(self.index), e=True, value=self.blendMode)
        cmds.floatSliderGrp(g_uiPrefix + "LayerAlpha_" + str(self.index), e=True, value=self.alpha)

        self.UpdateVisibleUI()
        self.CheckUI()

    #===========================================
    # 可視状態更新
    #===========================================
    def UpdateVisibleUI(self):

        global g_uiPrefix

        if self.visible == 1:
            cmds.button(g_uiPrefix + "LayerVisible_" + str(self.index), e=True, bgc=self.manager.editColor)
        else:
            cmds.button(g_uiPrefix + "LayerVisible_" + str(self.index), e=True, bgc=self.manager.waitColor)

    #===========================================
    # UIチェック
    #===========================================
    def CheckUI(self):
        
        global g_uiPrefix

        enalbeEdit = False
        enableName = False
        enalbeBlend = False
        enableAlpha = False
        enableVisible = False

        if self.isBase == True:
            
            enalbeEdit = True
            enableName = False
            enalbeBlend = False
            enableAlpha = False
            enableVisible = False
            
        else:
            
            if self.samePriority == True:                
                enalbeEdit = True

            if enalbeEdit == True:

                if self.sameName == True:
                    enableName = True

                if self.sameBlendMode == True:
                    enalbeBlend = True

                if self.sameAlpha == True:
                    enableAlpha = True

                if self.sameVisible == True:
                    enableVisible = True
            
        cmds.button(g_uiPrefix + "LayerEditButton_" + str(self.index), e=True, en=enalbeEdit)
        cmds.textField(g_uiPrefix + "LayerName_" + str(self.index), e=True, en=enableName)
        cmds.optionMenu(g_uiPrefix + "LayerBlend_" + str(self.index), e=True, en=enalbeBlend)
        cmds.floatSliderGrp(g_uiPrefix + "LayerAlpha_" + str(self.index), e=True, en=enableAlpha)
        cmds.button(g_uiPrefix + "LayerVisible_" + str(self.index), e=True, en=enableVisible, vis=enalbeEdit)

        if self.isBase == True:
            cmds.button(g_uiPrefix + "LayerVisible_" + str(self.index), e=True, vis=False)

    #===========================================
    # エディットボタン更新
    #===========================================
    def EnableEditButton(self, edit):

        global g_uiPrefix

        backColor = self.manager.editColor
        if edit == False:
            backColor = self.manager.waitColor
        
        cmds.button(g_uiPrefix + "LayerEditButton_" + str(self.index), e=True, bgc=backColor)

    #===========================================
    # レイヤーの値更新
    #===========================================
    def UpdateValue(self):

        global g_uiPrefix
        global g_currentTransformList

        if self.isBase == True:
            return

        tempName = cmds.textField(g_uiPrefix + "LayerName_" + str(self.index), q=True, text=True)

        if tempName == self.manager.baseLayerName or tempName == "":
            cmds.textField(g_uiPrefix + "LayerName_" + str(self.index), e=True, text=self.name)
            return

        self.alpha = cmds.floatSliderGrp(g_uiPrefix + "LayerAlpha_" + str(self.index), q=True, value=True)
        self.blendMode = cmds.optionMenu(g_uiPrefix + "LayerBlend_" + str(self.index), q=True, value=True)
        self.name = tempName
        
        for trans in g_currentTransformList:
            self.SaveToColorSet(trans)
            
    #===========================================
    # 可視状態変更
    #===========================================
    def ToggleVisible(self):

        global g_uiPrefix
        global g_currentTransformList

        if self.isBase == True:
            return

        visibleColor = cmds.button(g_uiPrefix + "LayerVisible_" + str(self.index), q=True, bgc=True)
        
        if visibleColor[0] == self.manager.editColor[0]:
            self.visible = 0
        else:
            self.visible = 1

        self.UpdateVisibleUI()

        for trans in g_currentTransformList:
            self.SaveToColorSet(trans)

        

    
