# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   CyWeightEditor
#-------------------------------------------------------------------------------------------
#
# 変更履歴
# ========================================
# [日付] 2018年10月04日 2回目
# [作業者] 諫山
#
# [内容]
# ツールボックス形式をやめました
#
# ========================================
# [日付] 2018年10月04日
# [作業者] 諫山
#
# [内容]
# ミラーコピー時に同一座標ジョイントが複数ある場合、
# 取り切れていなかったので0.001の値を足すことで判定を緩くしました。
# 
# 上記判定を抜けて複数ある場合にミラー時のLR判定が
# 今までは末尾が_L,_Rだったのを末尾が_L_数値,_L数値も判定するようにしました
#
# XMLでのインポート時にミラーが正しく動作していなかったので、
# パラメータを追加し修正しました。
#
# バージョンを0.1.0から18100401とし日付を基準としました
#
# ウィンドウをツールボックス形式にしました
#
# Maya2013,2015,2017にて動作確認済み
#
# ========================================
# [日付] 2016年06月15日
# [作業者] 阿武 (拡張の許可を諌山さんに確認済み)
#
# [内容]
# 出力ファイルをjsonからxmlに変更してほしいとの諌山さんの修正指示に従って変更
#
# [XML]
# <?xml version="1.0" encoding="UTF-8" ?>
# <VtxWeightInfoList>
#     <VtxWeightInfo name="" index="" meshname="" shortmeshname="" clustername="" jointrootname="" position="">
#         <WeightInfoList>
#             <WeightInfo weight="">
#                 <JointInfo name="" shortname="" position="" />
#             </WeightInfo>
#         </WeightInfoList>
#    </VtxWeightInfo>
# <VtxWeightInfoList>
#
# ========================================
# [日付] 2016年06月14日
# 作業者] 阿武 (拡張の許可を諌山さんに確認済み)
#
# [内容]
# Weight情報の外部ファイル化の機能を追加
#
# [追加した関数]
# AddExpImpWeightFrame
# ExportWeight
# __ImportWeight(decorator)
# ImportWeightByIndex
# ImportWeightBySelectOrder
# ImportWeightByPosition
# ImportWeightByMirror
# Json2List
# Xml2List
# FileDialog


from __future__ import division

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
    from past.utils import old_div
except Exception:
    pass


import gc
import maya.cmds as cmds
import maya.mel as mel
import CyCommon.CyUtility
import math
import re
import sys

# import json　
# import codecs
# from collections import OrderedDict
import xml.etree.ElementTree as ET

from functools import wraps

from CyCommon.CyUtility import CyUtility
from CyCommon.CySetting import CySetting

reload(CyCommon.CyUtility)
reload(CyCommon.CySetting)

g_version = "18100402"
g_toolName = "CyWeightEditor"
g_scriptPrefix= g_toolName + "."
g_uiPrefix= g_toolName + "UI_"
g_setting = None

g_lr_pattern = '_L$|_l$|_R$|_r$|_L_\d*$|_l_\d*$|_R_\d*$|_r_\d*$|_L\d*$|_l\d*$|_R\d*$|_r\d*$'
g_lr_replace_string = 'XXXXXXXX'

g_weightManager = None

#**************************************************************************************************************************
#   UI関連
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   メインUI
#-------------------------------------------------------------------------------------------
def UI():

    global g_toolName
    global g_scriptPrefix
    global g_uiPrefix
    global g_weightManager
    global g_setting
    global g_version

    cmds.selectPref(tso=True)

    if g_weightManager == None:
        g_weightManager = WeightManager()

    if g_setting == None:
        g_setting = CySetting(g_toolName)

    width=250
    height=1
    formWidth=width-5

    windowTitle = g_scriptPrefix.replace(".","") + " " + g_version
    windowName = g_scriptPrefix.replace(".", "") + "Win"

    CyUtility.CheckWindow(windowName)

    cmds.window( windowName, title=windowTitle, widthHeight=(width, height),s=1,mnb=True,mxb=False,rtf=True)

    cmds.columnLayout(adjustableColumn=True)
    
    cmds.frameLayout(l="Copy And Paste Weight",cll=1,cl=0,bv=1,bs="etchedIn",mw=0,mh=0)
    
    tabs = cmds.tabLayout(g_uiPrefix + "TabLayout", cc=g_scriptPrefix+"SaveSetting()")

    copyPasteFrame = cmds.frameLayout(bv=0, lv=0,mw=10,mh=10)
    
    cmds.columnLayout(adjustableColumn = True, rs=5)

    cmds.button( label="Copy Weight",bgc=[0.8,0.5,0.5],command=g_scriptPrefix+"CopyWeight()")
    cmds.separator( style='none',h=5,w=formWidth)
    cmds.button( label="Paste Weight By SelectOrder",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PasteWeightBySelectOrder()")
    cmds.button( label="Paste Weight By Index",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PasteWeightByIndex()")
    cmds.button( label="Paste Weight By Position",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PasteWeightByPosition()")
    cmds.separator( style='none', h=5, w=formWidth)
    cmds.button( label="Paste Weight By MirrorX",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PaseteWeightByMirror(0)")
    cmds.button( label="Paste Weight By MirrorY",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PaseteWeightByMirror(1)")
    cmds.button( label="Paste Weight By MirrorZ",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PaseteWeightByMirror(2)")

    cmds.setParent( ".." )
    cmds.setParent( ".." )
    
    # 追加UI (Export And Import Weight)
    expImpFrame = AddExpImpWeightFrame(formWidth)
    
    cmds.tabLayout(tabs, e=True, 
        tabLabel=((copyPasteFrame, 'Copy And Paste'), (expImpFrame, 'Export And Import'))
    )
    
    cmds.setParent( ".." )
    
    cmds.frameLayout(bv=0, lv=0,mw=10,mh=10)
    
    cmds.floatSliderGrp(g_uiPrefix + "PasteDistance", label='Paste Distance', field=True, minValue=0.0, maxValue=1000, fmn=0.0, fmx=1000, value=5, cw3=[80,50,0], cl3=["left","center","center"], cc=g_scriptPrefix+"SaveSetting()")
    
    cmds.setParent( ".." )
 
    cmds.setParent( ".." )

    cmds.frameLayout(l="Round Weight",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
    cmds.columnLayout(adjustableColumn = True, rs=5)

    cmds.intSliderGrp(g_uiPrefix + "RoundNum", label='Precision', field=True, minValue=1, maxValue=10, fmn=1, fmx=10, value=2, cw3=[80,30,0], cl3=["left","center","center"], cc=g_scriptPrefix+"SaveSetting()")
    cmds.button( label="Round Weight",bgc=[0.8,0.5,0.5],command=g_scriptPrefix+"RoundWeightValue()")
    cmds.button( label="Check Round Weight",bgc=[0.5,0.5,0.8],command=g_scriptPrefix+"CheckRoundWeightValue()")
 
    cmds.setParent( ".." )
    cmds.setParent( ".." )

    cmds.frameLayout(l="Max Influence",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
    cmds.columnLayout(adjustableColumn = True, rs=5)

    cmds.intSliderGrp(g_uiPrefix + "InfluenceNum", label='Influence Num', field=True, minValue=1, maxValue=10, fmn=1, fmx=10, value=2, cw3=[80,30,0], cl3=["left","center","center"], cc=g_scriptPrefix+"SaveSetting()" )
    cmds.button( label="Set Max Influence",bgc=[0.8,0.5,0.5],command=g_scriptPrefix+"SetMaxInfluence()")
    cmds.button( label="Check Max Influence",bgc=[0.5,0.5,0.8],command=g_scriptPrefix+"CheckMaxInfluence()")

    cmds.setParent( ".." )
    cmds.setParent( ".." )

    cmds.separator( style='in',h=15,w=formWidth)
    cmds.button( label="About",w=formWidth,command=g_scriptPrefix + "ShowAbout()")
 
    cmds.showWindow(windowName)

    LoadSetting()

#-------------------------------------------------------------------------------------------
#   追加UI (Export And Import Weight)
#-------------------------------------------------------------------------------------------
def AddExpImpWeightFrame(formWidth):
    
    global g_scriptPrefix
    global g_uiPrefix
    
    frame = cmds.frameLayout(bv=0, lv=0,mw=10,mh=10)
    cmds.columnLayout(adjustableColumn=True, rs=5)

    cmds.button( label="Export Weight",bgc=[0.8,0.5,0.8],command=g_scriptPrefix+"ExportWeight()")
    cmds.separator( style='none',h=5,w=formWidth)
    cmds.button( label="Import Weight By SelectOrder",bgc=[0.8,0.5,0],command=g_scriptPrefix+"ImportWeightBySelectOrder()")
    cmds.button( label="Import Weight By Index",bgc=[0.8,0.5,0],command=g_scriptPrefix+"ImportWeightByIndex()")
    cmds.button( label="Import Weight By Position",bgc=[0.8,0.5,0],command=g_scriptPrefix+"ImportWeightByPosition()")
    cmds.separator( style='none', h=5, w=formWidth)
    cmds.button( label="Import Weight By MirrorX",bgc=[0.8,0.5,0],command=g_scriptPrefix+"ImportWeightByMirror(0)")
    cmds.button( label="Import Weight By MirrorY",bgc=[0.8,0.5,0],command=g_scriptPrefix+"ImportWeightByMirror(1)")
    cmds.button( label="Import Weight By MirrorZ",bgc=[0.8,0.5,0],command=g_scriptPrefix+"ImportWeightByMirror(2)")
 
    cmds.setParent( ".." )
    cmds.setParent( ".." )
    
    return frame
    
#-------------------------------------------------------------------------------------------
#   CopyWeight
#-------------------------------------------------------------------------------------------
def CopyWeight():

    global g_weightManager

    g_weightManager.CreateInfo(True)

#-------------------------------------------------------------------------------------------
#   PasteWeightByIndex
#-------------------------------------------------------------------------------------------
def PasteWeightByIndex():

    global g_weightManager

    if cmds.confirmDialog(t="Confirm", m="Paste Weight By Index ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_weightManager.CreateInfo()
    g_weightManager.PasteWeightByIndex()

#-------------------------------------------------------------------------------------------
#   PasteWeightBySelectOrder
#-------------------------------------------------------------------------------------------
def PasteWeightBySelectOrder():

    global g_weightManager

    if cmds.confirmDialog(t="Confirm", m="Paste Weight By SelectOrder ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_weightManager.CreateInfo()
    g_weightManager.PasteWeightBySelectOrder()

#-------------------------------------------------------------------------------------------
#   PasteWeightByPosition
#-------------------------------------------------------------------------------------------
def PasteWeightByPosition():

    global g_weightManager

    if cmds.confirmDialog(t="Confirm", m="Paste Weight By Position ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_weightManager.CreateInfo()
    g_weightManager.PasteWeightByPosition(True)

#-------------------------------------------------------------------------------------------
#   PaseteWeightByMirror
#-------------------------------------------------------------------------------------------
def PaseteWeightByMirror(typ = 0):

    global g_weightManager

    if cmds.confirmDialog(t="Confirm", m="Pasete Weight By Mirror ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_weightManager.CreateInfo()

    if typ == 0:
        g_weightManager.PaseteWeightByMirror(True,False,False)

    if typ == 1:
        g_weightManager.PaseteWeightByMirror(False,True,False)

    if typ == 2:
        g_weightManager.PaseteWeightByMirror(False,False,True)

#-------------------------------------------------------------------------------------------
#   ExportWeight
#-------------------------------------------------------------------------------------------
'''
def ExportWeight():

    global g_weightManager

    # jsonファイルの出力ダイアログを表示
    jsonFile = FileDialogForJson(0)
    if not(jsonFile):
        return

    # CopyWeightを実行してg_weightManager.copyVtxWeightInfoListに値をセット
    CopyWeight()
    
    # g_weightManager.copyVtxWeightInfoListの値をjsonファイルとして出力
    with codecs.open(jsonFile, 'w', 'utf-8') as f:
        vtxInfoDict = OrderedDict()
        for copyVtxWeightInfo in g_weightManager.copyVtxWeightInfoList:
            weightInfoList = []
            for weightInfo in copyVtxWeightInfo.weightInfoList:
                jointInfoDict = {}
                jointInfo = weightInfo.jointInfo
                jointInfoDict = {
                    'name': jointInfo.name,
                    'shortName': jointInfo.shortName,
                    'position': jointInfo.position,
                }
                weightInfoList.append({
                    'jointInfo': jointInfoDict,
                    'weight': weightInfo.weight,
                })
            vtxInfoDict[copyVtxWeightInfo.name] = {
                'name': copyVtxWeightInfo.name,
                'index': copyVtxWeightInfo.index,
                'meshName': copyVtxWeightInfo.meshName,
                'shortMeshName': copyVtxWeightInfo.shortMeshName,
                'clusterName': copyVtxWeightInfo.clusterName,
                'jointRootName': copyVtxWeightInfo.jointRootName,
                'position': copyVtxWeightInfo.position,
                'weightInfoList': weightInfoList,
            }
        json.dump(vtxInfoDict, f, indent=2)
'''

def ExportWeight():

    global g_weightManager
    
    # xmlファイルの出力ダイアログを表示
    xmlFile = FileDialog(0)
    if not(xmlFile):
        return

    # CopyWeightを実行してg_weightManager.copyVtxWeightInfoListに値をセット
    CopyWeight()
    
    pos2str = lambda pos : '{0},{1},{2}'.format(pos[0], pos[1], pos[2])
    
    # g_weightManager.copyVtxWeightInfoListの値をxmlファイルとして出力
    # <root>
    #root = ET.Element('root')
    #root.text = '\n\t'
    
    # <VtxWeightInfoList>
    vtxWeightInfoListElem = ET.Element('VtxWeightInfoList')
    vtxWeightInfoListElem.text = '\n\t'
    vtxWeightInfoListElem.tail = '\n'
    
    for copyVtxWeightInfo in g_weightManager.copyVtxWeightInfoList:
        # <VtxWeightInfo>
        vtxWeightInfoElem = ET.SubElement(vtxWeightInfoListElem, 'VtxWeightInfo')
        vtxWeightInfoElem.text = '\n\t\t'
        attr_value = {
            'name': copyVtxWeightInfo.name,
            'index': str(copyVtxWeightInfo.index),
            'meshName': copyVtxWeightInfo.meshName,
            'shortMeshName': copyVtxWeightInfo.shortMeshName,
            'clusterName': copyVtxWeightInfo.clusterName,
            'jointRootName': copyVtxWeightInfo.jointRootName,
            'position': pos2str(copyVtxWeightInfo.position),
        }
        for attr, value in list(attr_value.items()):
            vtxWeightInfoElem.set(attr, value)
        vtxWeightInfoElem.tail = '\n\t'
        
        # <WeightInfoList>
        weightInfoListElem = ET.SubElement(vtxWeightInfoElem, 'WeightInfoList')
        weightInfoListElem.text = '\n\t\t\t'
        weightInfoListElem.tail = '\n\t'
        
        for weightInfo in copyVtxWeightInfo.weightInfoList:
            # <WeightInfo>
            weightInfoElem = ET.SubElement(weightInfoListElem, 'WeightInfo')
            weightInfoElem.text = '\n\t\t\t\t'
            attr_value = {
                'weight': str(weightInfo.weight),
            }
            for attr, value in list(attr_value.items()):
                weightInfoElem.set(attr, value)
            weightInfoElem.tail = '\n\t\t'

            # <JointInfo>
            jointInfo = weightInfo.jointInfo
            jointInfoElem = ET.SubElement(weightInfoElem, 'JointInfo')
            attr_value = {
                'name': jointInfo.name,
                'shortName': jointInfo.shortName,
                'position': pos2str(jointInfo.position),
                'removeLRName': jointInfo.removeLRName,
                'lrSuffix': jointInfo.lrSuffix
            }
            for attr, value in list(attr_value.items()):
                jointInfoElem.set(attr, value)
            jointInfoElem.tail = '\n\t\t\t'

    maya_ver = int(cmds.about(v=True)[:4])
    tree = ET.ElementTree(vtxWeightInfoListElem)
    if maya_ver < 2015:
        tree.write(xmlFile, encoding='utf-8')
    else:
        tree.write(xmlFile, xml_declaration=True, encoding='utf-8')
    
    
#-------------------------------------------------------------------------------------------
#   ImportWeight
#-------------------------------------------------------------------------------------------
def __ImportWeight(func, *args):
    
    @wraps(func)
    def WrapperImportWeight(*args):
    
        global g_weightManager
    
        filename = FileDialog(1)
        if not(filename):
            return
        
        g_weightManager.CreateInfo()
        # g_weightManager.copyVtxWeightInfoList = Json2List(filename)
        g_weightManager.copyVtxWeightInfoList = Xml2List(filename)
        func(*args)
            
    return WrapperImportWeight
    
#-------------------------------------------------------------------------------------------
#   ImportWeightByIndex
#-------------------------------------------------------------------------------------------
@__ImportWeight
def ImportWeightByIndex():
    g_weightManager.PasteWeightByIndex()

#-------------------------------------------------------------------------------------------
#   ImportWeightBySelectOrder
#-------------------------------------------------------------------------------------------
@__ImportWeight
def ImportWeightBySelectOrder():
    g_weightManager.PasteWeightBySelectOrder()
    
#-------------------------------------------------------------------------------------------
#   ImportWeightByPosition
#-------------------------------------------------------------------------------------------
@__ImportWeight
def ImportWeightByPosition():
    g_weightManager.PasteWeightByPosition(True)
    
#-------------------------------------------------------------------------------------------
#   ImportWeightByMirror
#-------------------------------------------------------------------------------------------
@__ImportWeight
def ImportWeightByMirror(typ = 0):
    if typ == 0:
        g_weightManager.PaseteWeightByMirror(True,False,False)

    if typ == 1:
        g_weightManager.PaseteWeightByMirror(False,True,False)

    if typ == 2:
        g_weightManager.PaseteWeightByMirror(False,False,True)
     
'''
#-------------------------------------------------------------------------------------------
#   Json2List
#-------------------------------------------------------------------------------------------
def Json2List(jsonFile):
    
    vtxWeightInfoList = []
    
    decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)
    with codecs.open(jsonFile, 'r', 'utf-8') as f:
        data = decoder.decode(f.read())
        for name, vtxInfoDict in data.items():
            weightInfoList = []
            for weightDict in vtxInfoDict['weightInfoList']:
                jointInfoDict = weightDict['jointInfo']
                jointInfo = JointInfo()
                jointInfo.name = jointInfoDict['name']
                jointInfo.shortName = jointInfoDict['shortName']
                jointInfo.position = jointInfoDict['position']
                
                weightInfo = WeightInfo()
                weightInfo.jointInfo = jointInfo
                weightInfo.weight = weightDict['weight']
                weightInfoList.append(weightInfo)
                
            vtxWeightInfo = VertexWeightInfo()        
            vtxWeightInfo.name = name
            vtxWeightInfo.index = vtxInfoDict['index']
            vtxWeightInfo.meshName = vtxInfoDict['meshName']
            vtxWeightInfo.shortMeshName = vtxInfoDict['shortMeshName']
            vtxWeightInfo.clusterName = vtxInfoDict['clusterName']
            vtxWeightInfo.jointRootName = vtxInfoDict['jointRootName']
            vtxWeightInfo.position = vtxInfoDict['position']
            vtxWeightInfo.weightInfoList = weightInfoList
            
            vtxWeightInfoList.append(vtxWeightInfo)

    return vtxWeightInfoList
'''

#-------------------------------------------------------------------------------------------
#   Xml2List
#-------------------------------------------------------------------------------------------
def Xml2List(xmlFile):
    
    vtxWeightInfoList = []
    
    str2pos = lambda s: (
        [float(s.split(',')[0]), float(s.split(',')[1]), float(s.split(',')[2])]
    )
    
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    for e1 in root.findall('.//VtxWeightInfo'):
        # <VtxWeightInfo>
        vtxWeightInfo = VertexWeightInfo()
        vtxWeightInfo.name = e1.get('name')
        vtxWeightInfo.index = int(e1.get('index'))
        vtxWeightInfo.meshName = e1.get('meshName')
        vtxWeightInfo.shortMeshName = e1.get('shortMeshName')
        vtxWeightInfo.clusterName = e1.get('clusterName')
        vtxWeightInfo.jointRootName = e1.get('jointRootName')
        vtxWeightInfo.position = str2pos(e1.get('position'))
        
        weightInfoList = []
        for e2 in e1.findall('.//WeightInfo'):
            # <WeightInfo>
            weightInfo = WeightInfo()
            weightInfo.weight = float(e2.get('weight'))
            
            for e3 in e2.findall('.//JointInfo'):
                # <JointInfo>
                jointInfo = JointInfo()
                jointInfo.name = e3.get('name')
                jointInfo.shortName = e3.get('shortName')
                jointInfo.position = str2pos(e3.get('position'))
                jointInfo.removeLRName = e3.get('removeLRName')
                jointInfo.lrSuffix = e3.get('lrSuffix')
                break
            
            weightInfo.jointInfo = jointInfo
            weightInfoList.append(weightInfo)
            
        vtxWeightInfo.weightInfoList = weightInfoList
        vtxWeightInfoList.append(vtxWeightInfo)

    return vtxWeightInfoList
    
#-------------------------------------------------------------------------------------------
#   jsonファイルの入出力ダイアログを表示
#-------------------------------------------------------------------------------------------
def FileDialog(fileMode):
    # fileMode: fileDialog2の引数fileMode

    if fileMode == 0:
        label = 'Export'
    else:
        label = 'Import'
    outputPath = cmds.file(q=True, sn=True)       
    outputPath = outputPath.split('/scenes')[0] if outputPath else ''
   
    # results = cmds.fileDialog2(cap='Export Weight (JSON)', fm=fileMode, dir=outputPath, okc=label, ff='*.json')
    results = cmds.fileDialog2(cap='Export Weight (XML)', fm=fileMode, dir=outputPath, okc=label, ff='*.xml')
    if results:
        return results[0]
    else:
        return False
     
#-------------------------------------------------------------------------------------------
#   RoundWeightValue
#-------------------------------------------------------------------------------------------
def RoundWeightValue():

    global g_uiPrefix
    global g_weightManager

    if cmds.confirmDialog(t="Confirm", m="Round weight ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    roundNum = cmds.intSliderGrp(g_uiPrefix + "RoundNum",q=True,v=True)

    g_weightManager.CreateInfo()
    g_weightManager.RoundWeight(roundNum)
    g_weightManager.Delete()
    
    gc.collect()

#-------------------------------------------------------------------------------------------
#   CheckRoundWeightValue
#-------------------------------------------------------------------------------------------
def CheckRoundWeightValue():

    global g_uiPrefix
    global g_weightManager

    if cmds.confirmDialog(t="Confirm", m="Check Round weight ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    roundNum = cmds.intSliderGrp(g_uiPrefix + "RoundNum",q=True,v=True)

    g_weightManager.CreateInfo()
    g_weightManager.ExistRoundWeight(roundNum)
    g_weightManager.Delete()
    
    gc.collect()

#-------------------------------------------------------------------------------------------
#   最大影響範囲設定
#-------------------------------------------------------------------------------------------
def SetMaxInfluence():

    global g_uiPrefix
    global g_weightManager

    if cmds.confirmDialog(t="Confirm", m="Set max influence ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    influenceNum = cmds.intSliderGrp(g_uiPrefix + "InfluenceNum",q=True,v=True)

    g_weightManager.CreateInfo()
    g_weightManager.SetMaxInfluence(influenceNum)
    g_weightManager.Delete()

    gc.collect()

#-------------------------------------------------------------------------------------------
#   最大影響範囲設定
#-------------------------------------------------------------------------------------------
def CheckMaxInfluence():

    global g_uiPrefix
    global g_weightManager

    if cmds.confirmDialog(t="Confirm", m="Check max influence ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    influenceNum = cmds.intSliderGrp(g_uiPrefix + "InfluenceNum",q=True,v=True)

    g_weightManager.CreateInfo()
    g_weightManager.ExistOverMaxInfluence(influenceNum)
    g_weightManager.Delete()

    gc.collect()

#-------------------------------------------------------------------------------------------
#   情報
#-------------------------------------------------------------------------------------------
def ShowAbout():

    global g_toolName
    global g_version

    CyUtility.ShowAbout(g_toolName, g_version, "")

#**************************************************************************************************************************
#   セーブロード関連
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   ロード
#-------------------------------------------------------------------------------------------
def LoadSetting():

    global g_setting

    tabLayout = g_setting.Load("TabLayout","int")
    
    pasteDistance = g_setting.Load("PasteDistance","float")
    importDistance = g_setting.Load("ImportDistance","float")

    roundNum = g_setting.Load("RoundNum","int")
    influenceNum = g_setting.Load("InfluenceNum","int")
    
    if tabLayout != 0:
        cmds.tabLayout(g_uiPrefix + "TabLayout",e=True,sti=tabLayout)

    if pasteDistance != 0:
        cmds.floatSliderGrp(g_uiPrefix + "PasteDistance",e=True,v=pasteDistance)
        
    if roundNum != 0:
        cmds.intSliderGrp(g_uiPrefix + "RoundNum",e=True,v=roundNum)

    if influenceNum != 0:
        cmds.intSliderGrp(g_uiPrefix + "InfluenceNum",e=True,v=influenceNum)

#-------------------------------------------------------------------------------------------
#   セーブ
#-------------------------------------------------------------------------------------------
def SaveSetting():

    global g_setting

    tabLayout = cmds.tabLayout(g_uiPrefix + "TabLayout",q=True,sti=True)
    
    pasteDistance = cmds.floatSliderGrp(g_uiPrefix + "PasteDistance",q=True,v=True)

    roundNum = cmds.intSliderGrp(g_uiPrefix + "RoundNum",q=True,v=True)
    influenceNum = cmds.intSliderGrp(g_uiPrefix + "InfluenceNum",q=True,v=True)

    g_setting.Save("TabLayout", tabLayout)
    g_setting.Save("PasteDistance", pasteDistance)
    g_setting.Save("RoundNum", roundNum)
    g_setting.Save("InfluenceNum",influenceNum)

#**************************************************************************************************************************
#   ユーティリティ関連
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   GetSelectList
#-------------------------------------------------------------------------------------------
def GetSelectList():

    selectList=[]
    
    selectList=cmds.ls(os=True,l=True,fl=True)

    if selectList != None:
        if len(selectList) != 0:
            return selectList

    selectList=cmds.ls(sl=True,l=True,fl=True)

    if selectList == None:
        return []

    if len(selectList) == 0:
        return []

    return selectList

#-------------------------------------------------------------------------------------------
#   GetShortName
#-------------------------------------------------------------------------------------------
def GetShortName(name):

    longName = GetLongName(name)

    if longName == "":
        return ""

    if longName.find("|") == -1:
        return longName

    splitStr = longName.split("|")

    return splitStr[len(splitStr) - 1]

#-------------------------------------------------------------------------------------------
#   GetLongName
#-------------------------------------------------------------------------------------------
def GetLongName(name):

    longName = cmds.ls(name,l=True)

    if longName == None:
        return ""

    if len(longName) == 0:
        return ""

    return longName[0]

#-------------------------------------------------------------------------------------------
#   GetRootName
#-------------------------------------------------------------------------------------------
def GetRootName(name):

    longName = GetLongName(name)

    if longName == "":
        return ""

    if longName.find("|") == -1:
        return longName

    splitStr = longName.split("|")

    return splitStr[1]

#-------------------------------------------------------------------------------------------
#   RemoveNamespace
#-------------------------------------------------------------------------------------------
def RemoveNamespace(name):

    if name.find("|") == -1:
        return RemoveNamespaceBase(name)

    splitStrList = name.split("|")
    resultName = ""
    for p in range(0,len(splitStrList)):
        
        fixName = RemoveNamespaceBase(splitStrList[p])

        resultName += fixName

        if p == len(splitStrList) - 1:
            continue

        resultName += "|"

    return resultName

#-------------------------------------------------------------------------------------------
#   RemoveNamespace
#-------------------------------------------------------------------------------------------
def RemoveNamespaceBase(name):

    if name.find(":") == -1:
        return name

    splitStr = name.split(":")

    return splitStr[len(splitStr) - 1]

#-------------------------------------------------------------------------------------------
#   GetRemoveLRName
#-------------------------------------------------------------------------------------------
def GetRemoveLRName(name):

    global g_lr_pattern
    global g_lr_replace_string

    match_obj = re.search(g_lr_pattern, name)

    if match_obj is None:
        return name, ''

    replace_string = match_obj.group()
    replace_name = re.sub(g_lr_pattern, g_lr_replace_string, name)

    return replace_name, replace_string

#-------------------------------------------------------------------------------------------
#   メッシュ名からスキンクラスタ用の名前取得
#-------------------------------------------------------------------------------------------
def GetNameForSkinCluster(meshName):
     
    result=meshName
 
    split=meshName.split("|")
 
    if meshName[0]=="|" and len(split)>2:
        result=meshName.replace("|","",1)
 
    return result

#-------------------------------------------------------------------------------------------
#   頂点からメッシュ取得
#-------------------------------------------------------------------------------------------
def GetMeshNameFromVertex(vertexName):

    if vertexName.find(".") == -1:
        return vertexName

    meshName=vertexName.split(".")[0]
        
    return meshName

#-------------------------------------------------------------------------------------------
#   頂点番号取得
#-------------------------------------------------------------------------------------------
def GetVertexIndex(vertexName):

    if vertexName.find("[") == -1:
        return

    if vertexName.find("]") == -1:
        return

    startIndex = vertexName.find("[") + 1
    endIndex = vertexName.find("]")

    return int(vertexName[startIndex:endIndex])

#-------------------------------------------------------------------------------------------
#   GetDistance
#-------------------------------------------------------------------------------------------
def GetDistance(value0, value1):

    if len(value0) != len(value1):
        return 10000000

    result = 0
    for p in range(len(value0)):

        result += (value1[p] - value0[p]) * (value1[p] - value0[p])

    return result

#-------------------------------------------------------------------------------------------
#   CopyPosition
#-------------------------------------------------------------------------------------------
def CopyPosition(value):

    result = [value[0],value[1],value[2]]

    return result

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
#   クラス群
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   メッシュウェイト情報クラス
#-------------------------------------------------------------------------------------------
class WeightManager(object):

    #===========================================
    # __init__
    #===========================================
    def __init__(self):

        self.targetVtxWeightInfoList = []
        self.copyVtxWeightInfoList = []

        self.pasteDistance = 5.0

    #===========================================
    # GetVertexList
    #===========================================
    def GetVertexList(self):

        selectList=GetSelectList()

        if len(selectList) == 0:
            return []
     
        mel.eval("PolySelectConvert 3")
        vtxList=cmds.ls(os=True,l=True,fl=True)

        cmds.select(selectList, r=True)

        selectList = None

        return vtxList

    #===========================================
    # GetJointInfoList
    #===========================================
    def GetJointInfoList(self):

        jointList=cmds.ls(l=True,typ="joint")

        if jointList == None:
            return []

        if len(jointList) == 0:
            return []

        resultList = []
        for p in range(len(jointList)):

            joint = JointInfo(jointList[p])

            resultList.append(joint)

        jointList = None

        return resultList

    #===========================================
    # GetClosestJointInfoList
    #===========================================
    def GetClosestJointInfo(self, targetPosition, maxDistance = 5):

        jointInfoList = self.GetJointInfoList()

        result = None
        minDistance = 10000000
        
        for p in range(len(jointInfoList)):

            thisDistance = GetDistance(targetPosition, jointInfoList[p].position)

            if thisDistance > maxDistance:
                continue

            if thisDistance < minDistance:
                result = jointInfoList[p]
                minDistance = thisDistance

        if result != None:
            result = result.Clone()

        for p in range(len(jointInfoList)):

            jointInfoList[p].Delete()

        jointInfoList = None

        return result

    #===========================================
    # GetClosestJointInfoList
    #===========================================
    def GetClosestJointInfoList(self, targetPosition, maxDistance = 5):

        jointInfoList = self.GetJointInfoList()

        result = []
        minDistance = 10000000
        
        for p in range(len(jointInfoList)):

            thisDistance = GetDistance(targetPosition, jointInfoList[p].position)

            if thisDistance > maxDistance:
                continue

            if thisDistance <= minDistance + 0.001:
                result.append(jointInfoList[p].Clone())
                minDistance = thisDistance

        for p in range(len(jointInfoList)):
            jointInfoList[p].Delete()

        jointInfoList = None

        return result

    #===========================================
    # GetVtxWeightInfoFromShortMeshName
    #===========================================
    def GetVtxWeightInfoListFromShortMeshName(self, shortMeshName, vtxWeightInfoList):

        result = []

        for p in range(len(vtxWeightInfoList)):

            tempVtxWeightInfo = vtxWeightInfoList[p]
            
            if shortMeshName != tempVtxWeightInfo.shortMeshName:
                continue

            result.append(tempVtxWeightInfo)

        if len(result) == 0:
            return vtxWeightInfoList

        return result

    #===========================================
    # GetClosestVtxWeightInfo
    #===========================================
    def GetClosestVtxWeightInfo(self, targetPosition, vtxWeightInfoList, maxDistance = 5):

        result = None
        minDistance = 10000000

        for p in range(len(vtxWeightInfoList)):

            thisDistance = GetDistance(targetPosition, vtxWeightInfoList[p].position)

            if thisDistance > maxDistance:
                continue

            if thisDistance < minDistance:
                result = vtxWeightInfoList[p]
                minDistance = thisDistance

        if result != None:
            result = result.Clone()

        return result

    #===========================================
    # CreateInfo
    #===========================================
    def CreateInfo(self, useCopyList=False):

        self.GetValueFromUI()

        vtxList = self.GetVertexList()

        if len(vtxList)==0:
            mel.eval("warning \"Cannot get target vertices!\"")
            return

        info = "Create Weight Info"
        if useCopyList == True:
            info = "Copy Weight"
            self.copyVtxWeightInfoList = []
        else:
            self.targetVtxWeightInfoList = []

        StartProgress(info)

        for p in range(len(vtxList)):

            if UpdateProgress(float(p) / float(len(vtxList)), info + "...") == False:
                EndProgress()
                break

            thisVertex = vtxList[p]
            
            newWeightInfo = VertexWeightInfo(thisVertex)

            if newWeightInfo.clusterName == "":
                continue

            if useCopyList == True:
                self.copyVtxWeightInfoList.append(newWeightInfo)
            else:
                self.targetVtxWeightInfoList.append(newWeightInfo)

        EndProgress()

    #===========================================
    # GetValueFromUI
    #===========================================
    def GetValueFromUI(self):

        global g_uiPrefix

        self.pasteDistance = cmds.floatSliderGrp(g_uiPrefix + "PasteDistance",q=True,v=True)

    #===========================================
    # PasteWeightByIndex
    #===========================================
    def PasteWeightByIndex(self):

        if len(self.copyVtxWeightInfoList)==0:
            mel.eval("warning \"Cannot get copy weight info!\"")
            return

        if len(self.targetVtxWeightInfoList)==0:
            mel.eval("warning \"Cannot get paste weight info!\"")
            return

        StartProgress("Paste Weight By Index")

        for p in range(len(self.targetVtxWeightInfoList)):

            if UpdateProgress(float(p) / float(len(self.targetVtxWeightInfoList)), "Pasting...") == False:
                EndProgress()
                break

            thisVtxWeightInfo = self.targetVtxWeightInfoList[p]

            tempVtxWeightInfoList = self.GetVtxWeightInfoListFromShortMeshName(thisVtxWeightInfo.shortMeshName, self.copyVtxWeightInfoList)

            if len(tempVtxWeightInfoList) == 0:
                continue

            targetWeightInfo = None
            for q in range(len(tempVtxWeightInfoList)):

                tempVtxWeightInfo = tempVtxWeightInfoList[q]
                
                if thisVtxWeightInfo.index != tempVtxWeightInfo.index:
                    continue

                targetWeightInfo = tempVtxWeightInfo.Clone()
                break

            if targetWeightInfo == None:
                continue

            thisVtxWeightInfo.weightInfoList = targetWeightInfo.weightInfoList

            thisVtxWeightInfo.UpdateWeight()

        EndProgress()

    #===========================================
    # PasteWeightBySelectOrder
    #===========================================
    def PasteWeightBySelectOrder(self):

        if len(self.copyVtxWeightInfoList)==0:
            mel.eval("warning \"Cannot get copy weight info!\"")
            return

        if len(self.targetVtxWeightInfoList)==0:
            mel.eval("warning \"Cannot get paste weight info!\"")
            return

        StartProgress("Paste Weight By Index")

        for p in range(len(self.targetVtxWeightInfoList)):

            if UpdateProgress(float(p) / float(len(self.targetVtxWeightInfoList)), "Pasting...") == False:
                EndProgress()
                break

            thisVtxWeightInfo = self.targetVtxWeightInfoList[p]

            tempVtxWeightInfoList = self.GetVtxWeightInfoListFromShortMeshName(thisVtxWeightInfo.shortMeshName, self.copyVtxWeightInfoList)

            if len(tempVtxWeightInfoList) == 0:
                continue

            thisIndex = p
            if p >= len(tempVtxWeightInfoList):
                thisIndex = len(tempVtxWeightInfoList) - 1

            targetWeightInfo = tempVtxWeightInfoList[thisIndex].Clone()

            if targetWeightInfo == None:
                continue

            thisVtxWeightInfo.weightInfoList = targetWeightInfo.weightInfoList

            thisVtxWeightInfo.UpdateWeight()

        EndProgress()

    #===========================================
    # PasteWeightByPosition
    #===========================================
    def PasteWeightByPosition(self, isWorld):

        if len(self.copyVtxWeightInfoList)==0:
            mel.eval("warning \"Cannot get copy weight info!\"")
            return

        if len(self.targetVtxWeightInfoList)==0:
            mel.eval("warning \"Cannot get paste weight info!\"")
            return

        StartProgress("Pasete Weight By Position")

        for p in range(len(self.targetVtxWeightInfoList)):

            if UpdateProgress(float(p) / float(len(self.targetVtxWeightInfoList)), "Pasting...") == False:
                EndProgress()
                break

            thisVtxWeightInfo = self.targetVtxWeightInfoList[p]

            tempVtxWeightInfoList = self.GetVtxWeightInfoListFromShortMeshName(thisVtxWeightInfo.shortMeshName, self.copyVtxWeightInfoList)

            if len(tempVtxWeightInfoList) == 0:
                continue

            tempVtxWeightInfo = self.GetClosestVtxWeightInfo(thisVtxWeightInfo.position, tempVtxWeightInfoList, self.pasteDistance)

            if tempVtxWeightInfo == None:
                continue

            targetVtxWeightInfo = tempVtxWeightInfo.Clone()

            thisVtxWeightInfo.weightInfoList = targetVtxWeightInfo.weightInfoList

            thisVtxWeightInfo.UpdateWeight()

        EndProgress()

    #===========================================
    # PaseteWeightByMirror
    #===========================================
    def PaseteWeightByMirror(self, isX, isY, isZ):

        if len(self.copyVtxWeightInfoList)==0:
            mel.eval("warning \"Cannot get copy weight info!\"")
            return

        if len(self.targetVtxWeightInfoList)==0:
            mel.eval("warning \"Cannot get paste weight info!\"")
            return

        StartProgress("Pasete Weight By Mirror")

        for p in range(len(self.targetVtxWeightInfoList)):

            if UpdateProgress(float(p) / float(len(self.targetVtxWeightInfoList)), "Pasting...") == False:
                EndProgress()
                break

            thisVtxWeightInfo = self.targetVtxWeightInfoList[p]

            tempVtxWeightInfoList = self.GetVtxWeightInfoListFromShortMeshName(thisVtxWeightInfo.shortMeshName, self.copyVtxWeightInfoList)

            if len(tempVtxWeightInfoList) == 0:
                continue

            tempPosition = CopyPosition(thisVtxWeightInfo.position)

            if isX == True:
                tempPosition[0] *= -1

            if isY == True:
                tempPosition[1] *= -1

            if isZ == True:
                tempPosition[2] *= -1

            tempVtxWeightInfo = self.GetClosestVtxWeightInfo(tempPosition, tempVtxWeightInfoList, self.pasteDistance)

            if tempVtxWeightInfo == None:
                continue

            targetVtxWeightInfo = tempVtxWeightInfo.Clone()

            for q in range(len(targetVtxWeightInfo.weightInfoList)):

                thisWeightInfo = targetVtxWeightInfo.weightInfoList[q]

                tempPosition = CopyPosition(thisWeightInfo.jointInfo.position)

                if isX == True:
                    tempPosition[0] *= -1

                if isY == True:
                    tempPosition[1] *= -1

                if isZ == True:
                    tempPosition[2] *= -1

                mirrorJointInfoList = self.GetClosestJointInfoList(tempPosition, self.pasteDistance)

                if len(mirrorJointInfoList) == 0:
                    continue

                if len(mirrorJointInfoList) == 1:
                    thisWeightInfo.jointInfo = mirrorJointInfoList[0].Clone()
                    continue

                for r in range(len(mirrorJointInfoList)):
                    
                    if mirrorJointInfoList[r].removeLRName != thisWeightInfo.jointInfo.removeLRName:
                       continue

                    thisWeightInfo.jointInfo = mirrorJointInfoList[r].Clone()

                    break                

            thisVtxWeightInfo.weightInfoList = targetVtxWeightInfo.weightInfoList

            thisVtxWeightInfo.UpdateWeight()

        EndProgress()

    #===========================================
    # RoundWeight
    #===========================================
    def RoundWeight(self,n):        

        if len(self.targetVtxWeightInfoList) == 0:
            return

        StartProgress("Round Weight")
        
        for p in range(len(self.targetVtxWeightInfoList)):

            if UpdateProgress(float(p) / float(len(self.targetVtxWeightInfoList)), "Rounding...") == False:
                EndProgress()
                break

            vtxWeightInfo = self.targetVtxWeightInfoList[p]

            vtxWeightInfo.RoundWeight(n)

        EndProgress()

    #===========================================
    # ExistRoundWeight
    #===========================================
    def ExistRoundWeight(self,n):

        result = []

        for p in range(len(self.targetVtxWeightInfoList)):

            vtxWeightInfo = self.targetVtxWeightInfoList[p]
            
            if vtxWeightInfo.ExistRoundWeight(n):
                result.append(vtxWeightInfo.name)

        if len(result) == 0:
            cmds.select(cl=True);
            return

        cmds.select(result, r=True);

        cmds.warning( "Some vertices have round weight !!!!!!" )

    #===========================================
    # SetMaxInfluence
    #===========================================
    def SetMaxInfluence(self,n):

        if len(self.targetVtxWeightInfoList) == 0:
            return

        StartProgress("Set MaxInfluence")
        
        for p in range(len(self.targetVtxWeightInfoList)):

            if UpdateProgress(float(p) / float(len(self.targetVtxWeightInfoList)), "Seting Influence...") == False:
                EndProgress()
                break

            vtxWeightInfo = self.targetVtxWeightInfoList[p]
            
            vtxWeightInfo.SetMaxInfluence(n)

        EndProgress()

    #===========================================
    # ExistOverMaxInfluence
    #===========================================
    def ExistOverMaxInfluence(self,n):

        result = []

        for p in range(len(self.targetVtxWeightInfoList)):

            vtxWeightInfo = self.targetVtxWeightInfoList[p]
            
            if vtxWeightInfo.ExistOverMaxInfluence(n):
                result.append(vtxWeightInfo.name)

        if len(result) == 0:
            cmds.select(cl=True);
            return

        cmds.select(result, r=True);

        cmds.warning( "Some vertices have over max influence !!!!!!" )

    #===========================================
    # Delete
    #===========================================
    def Delete(self):

        for vtxWeightInfo in self.targetVtxWeightInfoList:
            
            vtxWeightInfo.Delete()

        self.targetVtxWeightInfoList = None

#-------------------------------------------------------------------------------------------
#   頂点ウェイト情報クラス
#-------------------------------------------------------------------------------------------
class VertexWeightInfo(object):

    #===========================================
    # __init__
    #===========================================
    def __init__(self,name=""):

        self.name = name
        self.index = 0
        self.meshName = ""
        self.shortMeshName = ""
        self.clusterName = ""
        self.jointRootName = ""
        
        self.position = [0,0,0]
        
        self.weightInfoList = []

        if self.name == "":
            return

        self.CreateInfo()

    #===========================================
    # Clone
    #===========================================
    def Clone(self):

        cloneVertexWeightInfo = VertexWeightInfo()

        cloneVertexWeightInfo.name = self.name
        cloneVertexWeightInfo.index = self.index
        cloneVertexWeightInfo.meshName = self.meshName
        cloneVertexWeightInfo.shortMeshName = self.shortMeshName
        cloneVertexWeightInfo.clusterName = self.clusterName
        cloneVertexWeightInfo.jointRootName = self.jointRootName
        
        cloneVertexWeightInfo.position = CopyPosition(self.position)

        cloneVertexWeightInfo.weightInfoList = []

        for i in range(len(self.weightInfoList)):

            cloneWeightInfo = self.weightInfoList[i].Clone()

            cloneVertexWeightInfo.weightInfoList.append(cloneWeightInfo)

        return cloneVertexWeightInfo

    #===========================================
    # CreateInfo
    #===========================================
    def CreateInfo(self):

        self.name = GetLongName(self.name)

        if cmds.objExists(self.name) == False:
            return

        self.index = GetVertexIndex(self.name)
        self.meshName = GetMeshNameFromVertex(self.name)
        self.shortMeshName = RemoveNamespace(GetShortName(self.meshName))
        
        meshNameForCluster = GetNameForSkinCluster(self.meshName)
        self.clusterName=mel.eval("findRelatedSkinCluster "+meshNameForCluster)

        if self.clusterName=="":
            return

        jointList=cmds.skinPercent(self.clusterName,self.name, query=True, t=None )
        weightList = cmds.skinPercent(self.clusterName,self.name, query=True, value=True )

        if len(jointList) == 0:
            return

        if len(jointList) != len(weightList):
            return

        self.jointRootName = GetRootName(jointList[0])

        for i in range(len(jointList)):

            if weightList[i] == 0:
                continue

            newWeightInfo = WeightInfo(jointList[i],weightList[i])

            self.weightInfoList.append(newWeightInfo)

        self.SortWeightInfo()

        #Position
        self.position = cmds.pointPosition(self.name,w=True)

        jointList = None
        weightList = None

    #===========================================
    # UpdateWeight
    #===========================================
    def UpdateWeight(self):

        self.FixJointName()

        self.FixWeight()

        transformValue = self.CreateTransformValue()

        try:
            cmds.skinPercent(self.clusterName,self.name,tv=transformValue,nrm=True)
        except:
            test = 0

        transformValue = None

    #===========================================
    # RoundWeight
    #===========================================
    def RoundWeight(self, n):

        for cnt in range(0,2):

            for weightInfo in self.weightInfoList:

                weightInfo.Round(n)

            self.NormalizeWeight(1)

            self.UpdateWeight()

    #===========================================
    # ExistRoundWeight
    #===========================================
    def ExistRoundWeight(self, n):

        for weightInfo in self.weightInfoList:

            if weightInfo.ExistRoundWeight(n):
                return True

        return False

    #===========================================
    # SetMaxInfluence
    #===========================================
    def SetMaxInfluence(self,n):

        self.SortWeightInfo()

        restWeight = 0
        for i in range(len(self.weightInfoList)):

            if i < n:
                continue

            restWeight += self.weightInfoList[i].weight
            self.weightInfoList[i].weight = 0

        weightSum = 0
        for weight in self.weightInfoList:
            weightSum += weight.weight

        for weight in self.weightInfoList:
            if sys.version_info.major == 2:
                weight.weight += restWeight * weight.weight / weightSum
            else:
                # for Maya 2022-
                weight.weight += old_div(restWeight * weight.weight, weightSum)

        self.NormalizeWeight(0)

        self.UpdateWeight()

    #===========================================
    # ExistOverMaxInfluence
    #===========================================
    def ExistOverMaxInfluence(self,n):
                
        weightCount = 0
        for p in range(len(self.weightInfoList)):

            if self.weightInfoList[p].weight == 0:
                continue

            weightCount += 1

        if weightCount <= n:
            return False

        return True

    #===========================================
    # SortWeightInfo
    #===========================================
    def SortWeightInfo(self):

        newWeightInfoList = []

        while len(self.weightInfoList) != 0:

            weightInfo = self.GetMinWeightInfo()

            self.weightInfoList.remove(weightInfo)
            newWeightInfoList.append(weightInfo)

        self.weightInfoList =[]
        for i in range(len(newWeightInfoList)):
            self.weightInfoList.append(newWeightInfoList[len(newWeightInfoList) - 1 - i])

        newWeightInfoList = None

    #===========================================
    # GetMinWeightInfo
    #===========================================
    def GetMinWeightInfo(self):

        result = self.weightInfoList[0]
        minWeight = 10000
        for weightInfo in self.weightInfoList:

            if weightInfo.weight < minWeight:
                result = weightInfo
                minWeight = weightInfo.weight

        return result

    #===========================================
    # CreateInfo
    #===========================================
    def NormalizeWeight(self, typ):

        weightSum = 0

        for weightInfo in self.weightInfoList:
            
            weightSum += weightInfo.weight

        weightDef = weightSum - 1.0;

        if typ == 0:
            
            for weightInfo in self.weightInfoList:

                weightInfo.weight /= weightSum

        elif typ == 1:

            for weightInfo in self.weightInfoList:

                if weightInfo.weight <= 0:
                    continue

                weightInfo.weight -= weightDef
                break

    #===========================================
    # FixWeight
    #===========================================
    def FixWeight(self):

        weightSum = 0

        for weightInfo in self.weightInfoList:
            
            weightSum += weightInfo.weight

        weightDef = weightSum - 1.0;

        if weightDef == 0:
            return

        for weightInfo in self.weightInfoList:

            if weightInfo.weight <= 0:
                continue

            if weightInfo.weight <= weightDef:
                continue

            weightInfo.weight -= weightDef
            break

    #===========================================
    # CreateTransformValue
    #===========================================
    def CreateTransformValue(self):
     
        transformValue=[]

        for weightInfo in self.weightInfoList:
            
            transformValue.append((weightInfo.jointInfo.name,weightInfo.weight))
     
        return transformValue

    #===========================================
    # Delete
    #===========================================
    def Delete(self):

        for weightInfo in self.weightInfoList:

            weightInfo.Delete()

            weight = None

    #===========================================
    # FixJointName
    #===========================================
    def FixJointName(self):

        for weightInfo in self.weightInfoList:

            targetJointNameList = cmds.ls(weightInfo.jointInfo.shortName,l=True,fl=True)

            for jointName in targetJointNameList:

                jointRootName = GetRootName(jointName)

                if self.jointRootName == jointRootName:
                    weightInfo.jointInfo = JointInfo(jointName)
                    break

#-------------------------------------------------------------------------------------------
#   ウェイト情報クラス
#-------------------------------------------------------------------------------------------
class WeightInfo(object):

    #===========================================
    # __init__
    #===========================================
    def __init__(self, jointName="", weight=0):

        self.jointInfo = JointInfo(jointName)
        self.weight = weight

    #===========================================
    # Clone
    #===========================================
    def Clone(self):

        cloneWeightInfo = WeightInfo()

        cloneWeightInfo.jointInfo = self.jointInfo.Clone()
        cloneWeightInfo.weight = self.weight

        return cloneWeightInfo

    #===========================================
    # ExistRoundWeight
    #===========================================
    def ExistRoundWeight(self,n):

        tempFullValue = self.weight * pow(10,n)
        tempValue = math.modf(tempFullValue);

        if tempValue[0] < 0.01 or tempValue[0] > 0.99:
            return False

        return True

    #===========================================
    # Round
    #===========================================
    def Round(self,n):

        self.weight = round(self.weight,n)
        
    #===========================================
    # Delete
    #===========================================
    def Delete(self):

        self.jointInfo = None

#-------------------------------------------------------------------------------------------
#   ジョイント情報クラス
#-------------------------------------------------------------------------------------------
class JointInfo(object):

    #===========================================
    # __init__
    #===========================================
    def __init__(self, name=""):
        
        self.name = name        
        self.shortName = ""
        self.removeLRName = ""
        self.lrSuffix = ""
        self.position = [0,0,0]

        if self.name == "":
            return

        self.CreateInfo()

    #===========================================
    # Clone
    #===========================================
    def Clone(self):

        cloneJointInfo = JointInfo()

        cloneJointInfo.name = self.name
        cloneJointInfo.shortName = self.shortName
        cloneJointInfo.removeLRName = self.removeLRName
        cloneJointInfo.lrSuffix = self.lrSuffix
        cloneJointInfo.position = CopyPosition(self.position)

        return cloneJointInfo

    #===========================================
    # CreateInfo
    #===========================================
    def CreateInfo(self):

        self.name = GetLongName(self.name)

        if cmds.objExists(self.name) == False:
            return

        self.shortName = RemoveNamespace(GetShortName(self.name))
        self.removeLRName, self.lrSuffix = GetRemoveLRName(self.shortName)
        
        self.position = cmds.xform(self.name,q=True,ws=True,t=True)

    #===========================================
    # Delete
    #===========================================
    def Delete(self):

        self.name = None
        self.shortName = None
        self.removeLRName = None
        self.position = None
