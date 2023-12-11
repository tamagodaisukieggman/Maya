# -*- coding: utf-8 -*-

"""
テクスチャをベイク

"""

toolName = "WizardBakeTexture"
__author__ = "Cygames, Inc. Yuta Kimura"

import os

import maya.mel as mel
import pymel.core as pm

import WizardChangeTextureBakeSetting;reload(WizardChangeTextureBakeSetting)

#-------------------------------------------------
#メイン
def bake(renderTypes, imageWidth, imageHeight, isGI=0, isFG=0):
    for renderType in renderTypes:
        #テクスチャベイク設定の切り替え
        WizardChangeTextureBakeSetting.change(renderType, imageWidth, imageHeight, isGI, isFG)

        #テクスチャをベイク
        mel.eval("mrBakeToTexture false")

        #ベイク後のテクスチャをPhotoshopで開く
        textureFileName = pm.getAttr("textureBakeSet_wizard.prefix") + ".tga"
        textureFilePath = pm.Workspace.getPath() + "/renderData/mentalray/lightMap/" + textureFileName
        textureFilePath = textureFilePath.replace("/", "\\")

        photoshopExeFilePath = '"C:/Program Files/Adobe/Adobe Photoshop CS6 (64 Bit)/Photoshop.exe"'
        command = 'start "" ' + photoshopExeFilePath + " " + textureFilePath
        os.system(command)

    return


#-------------------------------------------------
if __name__ == '__main__':
    bake()
