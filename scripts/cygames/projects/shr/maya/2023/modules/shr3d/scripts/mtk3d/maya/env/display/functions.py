# -*- coding: cp932 -*-
#===============================================
#
# 表示関連
#
# Fujita Yukihiro
#
#===============================================
import maya.OpenMaya as OM
import maya.OpenMayaUI as OMUI

#-----------------------------------------------
#
# ビューポートをキャプチャ
#
# @param      mPanel : キャプチャするモデルパネル
# @param      filename : キャプチャ画像を保存するファイル名
# @param      extension : 画像フォーマット
#
#-----------------------------------------------
def captureViewport(mPanel, filename, extension):

    img = OM.MImage()

    view = OMUI.M3dView()

    OMUI.M3dView.getM3dViewFromModelPanel(mPanel, view)

    view.beginGL()

    view.readColorBuffer(img, 1)

    view.endGL()

    #img.resize(w, h, aspect)

    img.writeToFile(filename, extension)
