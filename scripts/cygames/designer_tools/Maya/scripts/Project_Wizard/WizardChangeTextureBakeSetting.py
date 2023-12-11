# -*- coding: utf-8 -*-

"""
テクスチャベイク設定の切り替え

"""

toolName = "WizardChangeTextureBakeSetting"
__author__ = "Cygames, Inc. Yuta Kimura"

import pymel.core as pm


#-------------------------------------------------
#メイン
def change(renderType, imageWidth, imageHeight, isGI=0, isFG=0):
    renderLayerName = ""
    if renderType == "default":
        renderLayerName = "defaultRenderLayer"
    else:
        renderLayerName = renderType + "MapLayer"

    #レンダーレイヤーの切り替え
    pm.editRenderLayerGlobals(currentRenderLayer=renderLayerName)

    #テクスチャベイクセット設定を変更(カラーモード)
    fileNameSuffix = ""
    if renderType == "light":
        pm.setAttr("textureBakeSet_wizard.colorMode", 0)    #Light and Color
        fileNameSuffix += "lightMap"
    elif renderType == "shadow":
        pm.setAttr("textureBakeSet_wizard.colorMode", 1)    #Only Light
        fileNameSuffix += "shadowMap"
    elif renderType == "gi":
        pm.setAttr("textureBakeSet_wizard.colorMode", 2)    #Only Global Illumination
        fileNameSuffix += "giMap"
    elif renderType == "ao":
#       pm.setAttr("textureBakeSet_wizard.colorMode", 3)    #Occlusion
        pm.setAttr("textureBakeSet_wizard.colorMode", 4)    #Custom Shader
        fileNameSuffix += "aoMap"

    bakeFileName = ""

    selNodes = pm.ls(sl=1, transforms=1, flatten=1)
    if len(selNodes) > 0:
        selNodeShortName = selNodes[0].shortName().split("|")[-1]
        bakeFileName = selNodeShortName.split("__")[0] + "_" + fileNameSuffix

    #テクスチャベイクセット設定を変更(保存テクスチャ名)
    pm.setAttr("textureBakeSet_wizard.prefix", bakeFileName, type="string")

    #テクスチャベイクセット設定を変更(ベイク画像サイズ)
    if imageWidth > 0:
        pm.setAttr("textureBakeSet_wizard.xResolution", imageWidth)
    if imageHeight > 0:
        pm.setAttr("textureBakeSet_wizard.yResolution", imageHeight)

    #レンダリング設定を変更(GI)
    pm.setAttr("miDefaultOptions.globalIllum", isGI)

#   if renderType == "light":
#       pm.setAttr("miDefaultOptions.globalIllum", 1)
#   else:
#       pm.setAttr("miDefaultOptions.globalIllum", 0)

    #レンダリング設定を変更(FG)
    pm.setAttr("miDefaultOptions.finalGather", isFG)

#   if renderType == "ao" or renderType == "gi":
#       pm.setAttr("miDefaultOptions.finalGather", 1)
#   else:
#       pm.setAttr("miDefaultOptions.finalGather", 0)

    return


#-------------------------------------------------
if __name__ == '__main__':
    change()
