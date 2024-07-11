# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

"""
import TkgUVDeformation
reload(TkgUVDeformation)
TkgUVDeformation.UI()
"""
#-------------------------------------------------------------------------------------------
#   設定
#-------------------------------------------------------------------------------------------
import ctypes
import math
import re
import sys

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

#from math import *
#from math import sin,pi

import maya.cmds as cmds
import maya.mel as mel

import TkgCommon.TkgUtility
import TkgCommon.TkgSetting

from TkgCommon.TkgUtility import TkgUtility
from TkgCommon.TkgSetting import TkgSetting

reload(TkgCommon.TkgUtility)
reload(TkgCommon.TkgSetting)

g_version = "0.1.0"
g_toolName = __name__
g_scriptPrefix = g_toolName + "."
g_uiPrefix = g_toolName + "UI_"
g_setting = TkgSetting(g_toolName)

g_save = {}
g_save_key = {}

#-------------------------------------------------------------------------------------------
#   画面
#-------------------------------------------------------------------------------------------
def UI():

    global g_scriptPrefix
    global g_uiPrefix
    global g_toolName

    width=250
    height=1

    windowTitle=g_toolName
    windowName=windowTitle+"Win"

    #ウインドウ重複確認
    TkgUtility.CheckWindow(windowName)

    #ウィンドウ作成
    cmds.window(windowName, title=windowTitle, widthHeight=(width, height),s=1,mnb=True,mxb=False,rtf=True)

    #カラムレイアウト開始
    cmds.columnLayout(adjustableColumn=True)

    #-----------------
    cmds.floatSliderGrp(g_uiPrefix + "waveLength", precision=3, label=u"波長", field=True, minValue=-2.0, maxValue=2.0, fieldMinValue=-100.0, fieldMaxValue=100.0, value=1.0, cw3=[50,50,0], cl3=["left","center","center"], cc=g_scriptPrefix+"SaveSetting()")
    cmds.floatSliderGrp(g_uiPrefix + "waveWidth", precision=3, label=u"振幅", field=True, minValue=-1.0, maxValue=1.0, fieldMinValue=-100.0, fieldMaxValue=100.0, value=0.1, cw3=[50,50,0], cl3=["left","center","center"], cc=g_scriptPrefix+"SaveSetting()")
    cmds.floatSliderGrp(g_uiPrefix + "waveOffset", precision=3, label=u"オフセット", field=True, minValue=-1.0, maxValue=1.0, fieldMinValue=-10.0, fieldMaxValue=10.0, value=0.0, cw3=[50,50,0], cl3=["left","center","center"], cc=g_scriptPrefix+"SaveSetting()")
    cmds.floatSliderGrp(g_uiPrefix + "waveShear", precision=3, label=u"せん断", field=True, minValue=-1.0, maxValue=1.0, fieldMinValue=-10.0, fieldMaxValue=10.0, value=0.0, cw3=[50,50,0], cl3=["left","center","center"], cc=g_scriptPrefix+"SaveSetting()")
    cmds.radioButtonGrp(g_uiPrefix + "waveTar", label=u"方向", cw3=[50,50,0], cl3=["left","center","center"], labelArray2=["X", "Y"], select=1, numberOfRadioButtons=2, cc=g_scriptPrefix+"SaveSetting()")
    cmds.button(label="Deformation", bgc=[0.8,0.5,0.8], command=g_scriptPrefix+"Deformation()")
    cmds.button(label="Back", bgc=[0.5,0.5,0.8], command=g_scriptPrefix+"Back()")

    #カラムレイアウト終了
    cmds.setParent("..")

    #ウィンドウ表示
    cmds.showWindow()

    #再記処理
    LoadSetting()


#-------------------------------------------------------------------------------------------
#   処理
#-------------------------------------------------------------------------------------------
def Deformation():

    global g_uiPrefix
    global g_save
    global g_save_key

    #UIから値取得
    waveLength = cmds.floatSliderGrp(g_uiPrefix + "waveLength", q=True, v=True)
    waveWidth = cmds.floatSliderGrp(g_uiPrefix + "waveWidth", q=True, v=True)
    waveOffset = cmds.floatSliderGrp(g_uiPrefix + "waveOffset", q=True, v=True)
    waveShear = cmds.floatSliderGrp(g_uiPrefix + "waveShear", q=True, v=True)
    waveTar = cmds.radioButtonGrp(g_uiPrefix + "waveTar", q=True, select=True)

    #対象の選択確認
    meshList = cmds.ls(sl=1, o=1)
    if not meshList:
        ctypes.windll.user32.MessageBoxW(0, u"Error: 対象オブジェクトを選択してください。", u"Warning", 0x40 | 0x0)
        sys.exit()
    mesh = meshList[0]

    #初期頂点座標の記録
    n = mesh
    if not n in g_save:
        g_save["%s" % n] = []
        g_save_key["%s" % n] = True

    #UVの選択
    cmds.select(mesh + ".map[*]", r=1)
    cmds.polyUVSet(mesh, q=True, allUVSets=True)

    #サインカーブ
    for uvlist in mel.eval("ls -sl -fl"):
        cmds.select(uvlist, r=1)
        p = mel.eval("polyEditUV -q")
        
        if g_save_key["%s" % n]:
            g_save[n].append(p)

        if waveTar == 1:
            #x
            x = p[0]
            y = waveWidth * math.sin(2 * math.pi * (p[0] + waveOffset)*waveLength) + p[1]
        else:
            #y
            x = waveWidth * math.sin(2 * math.pi * (p[1] + waveOffset)*waveLength) + p[0]
            y = p[1]

        mel.eval("polyEditUV -r false -u %s -v %s" % (x, y))

    g_save_key["%s" % n] = False

    #UVの選択
    cmds.select(mesh + ".map[*]", r=1)
    cmds.polyUVSet(mesh, q=True, allUVSets=True)

    #せん断
    for uvlist in mel.eval("ls -sl -fl"):
        cmds.select(uvlist, r=1)
        p = mel.eval("polyEditUV -q")

        if waveTar == 1:
            #x
            x = p[0] + (waveShear * p[1])
            y = p[1]
        else:
            #y
            x = p[0]
            y = p[1] + (waveShear * p[0])

        mel.eval("polyEditUV -r false -u %s -v %s" % (x, y))

    mel.eval("select -r %s" % mesh)


#-------------------------------------------------------------------------------------------
#   変形前に戻す
#-------------------------------------------------------------------------------------------
"""
オブジェクト名毎に最初の状態を配列に保存
削除や切り取りなどされた場合は戻せない
"""
def Back():

    global g_save

    #対象の選択確認
    meshList = cmds.ls(sl=1, o=1)
    if not meshList:
        ctypes.windll.user32.MessageBoxW(0, u"Error: 対象オブジェクトを選択してください。", u"Warning", 0x40 | 0x0)
        sys.exit()
    mesh = meshList[0]
    cmds.select(mesh + ".map[*]", r=1)
    cmds.polyUVSet(mesh, q=True, allUVSets=True)
    uvlist = mel.eval("ls -sl -fl")
    mel.eval("select -r %s" % mesh)

    #保存確認
    if not mesh in g_save:
        ctypes.windll.user32.MessageBoxW(0, u"Error: 初期状態が記憶されていません。", u"Warning", 0x40 | 0x0)
        sys.exit()

    #整合性確認
    if not len(g_save[mesh]) == len(uvlist):
        ctypes.windll.user32.MessageBoxW(0, u"Error: 保存された頂点数と現在の頂点数が大きく異るため最初の状態に戻すことができません。", u"Warning", 0x40 | 0x0)
        sys.exit()

    #実行確認
    returnValue = ctypes.windll.user32.MessageBoxW(None, u"UV変形を最初の状態に戻します。よろしいですか？", u"Warning", 0x40 | 0x1)
    if returnValue == 2:
        return 0

    #
    cmds.select(mesh + ".map[*]", r=1)
    cmds.polyUVSet(mesh, q=True, allUVSets=True)
    uvlist = mel.eval("ls -sl -fl")
    i = 0
    for uvlist in mel.eval("ls -sl -fl"):
        cmds.select(uvlist, r=1)
        x = g_save[mesh][i][0]
        y = g_save[mesh][i][1]
        mel.eval("polyEditUV -r false -u %s -v %s" % (x, y))
        i = i + 1

    mel.eval("select -r %s" % mesh)


#-------------------------------------------------------------------------------------------
#   Save Setting
#-------------------------------------------------------------------------------------------
def SaveSetting():

    global g_uiPrefix
    global g_setting

    for var in cmds.lsUI(type=["floatSliderGrp"]):
        if re.compile("%s*" % g_uiPrefix).match(var):
            t = cmds.floatSliderGrp(var, q=True, v=True)
            g_setting.Save(var, t)

    for var in cmds.lsUI(type=["radioButtonGrp"]):
        if re.compile("%s*" % g_uiPrefix).match(var):
            t = cmds.radioButtonGrp(var, q=True, sl=True)
            g_setting.Save(var, t)


#-------------------------------------------------------------------------------------------
#   Load Setting
#-------------------------------------------------------------------------------------------
def LoadSetting():

    global g_uiPrefix
    global g_setting

    for var in cmds.lsUI(type=["floatSliderGrp"]):
        if re.compile("%s*" % g_uiPrefix).match(var):
            t = g_setting.Load(var, "float")
            cmds.floatSliderGrp(var, e=True, v=t)

    for var in cmds.lsUI(type=["radioButtonGrp"]):
        if re.compile("%s*" % g_uiPrefix).match(var):
            t = g_setting.Load(var, "float")
            cmds.radioButtonGrp(var, e=True, sl=t)

