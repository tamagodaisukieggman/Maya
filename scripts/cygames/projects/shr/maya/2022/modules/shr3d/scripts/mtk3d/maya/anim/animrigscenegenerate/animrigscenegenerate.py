# -*- coding: utf-8 -*-

import maya.cmds as mc
import os
import re

#ファイル名のキャラカテゴリは省略されているので変換する関数
def idCheck(charSpecificID):

    print(u"渡された値： " + charSpecificID)

    if charSpecificID == "ply":
        charDirectory = "player"

    elif charSpecificID == "bos":
        charDirectory = "boss"

    elif charSpecificID == "cre":
        charDirectory = "creature"

    elif charSpecificID == "mob":
        charDirectory = "mob"

    else :
        charDirectory == u"None"

    print(u"キャラは: " + charDirectory)

    return charDirectory

#ディレクトリ探す処理と無かったら作る処理
def directoryExistsCheck(worksceneDirectory):

    worksceneDirectoryPath = worksceneDirectory
    existsFlag = True

    #無い場合はあるところまでからフォルダを作成していく
    if not os.path.exists(worksceneDirectory):
        os.makedirs(worksceneDirectory)
        existsFlag = False

    return existsFlag

def execute():

    basicFilter = "*.ma"
    rigfullPath = mc.fileDialog2(fileFilter=basicFilter, fileMode=1, dialogStyle=2, cap=u"リグファイルを選択してください")[0]
    #rawにする
    rigPath = repr(rigfullPath)

    charDirectory = "None"

    #接頭辞
    prefix = "anm"

    #ma
    fileFormat = ".ma"

    #アニメーションワークの場所
    animDirectoryBasePath = r"Z:\mtk\work\resources\animations\clips"

    #シーン生成先の末端ディレクトリ名
    workScenes = "workscenes"

    #リグまでのフルパスからキャラIDを取得する
    #
    rigFile = os.path.basename(rigPath).split(".")[0]
    chrID = os.path.basename(rigFile).split("_")[1]
    print(chrID)
    charSpecificID = re.split('[0-999]', chrID)[0]
    print(charSpecificID)

    #IDからキャラカテゴリを検索
    charDir = idCheck(str(charSpecificID))
    print(charDir)

    #キャラカテゴリがplyかmobならIDが特殊なので専用処理
    #rig_ply00_m_000.ma
    if charDir == "player" or charDir == "mob" :
        charaID = os.path.basename(rigFile).split("_")[1] + "_" + os.path.basename(rigFile).split("_")[2] + "_" + os.path.basename(rigFile).split("_")[3]
    else :
        charaID = os.path.basename(rigFile).split("_")[1] + "_" + os.path.basename(rigFile).split("_")[2]

    #workscenesまでのパスを作成
    worksceneDirectory = animDirectoryBasePath + "\\" + charDir + "\\" + workScenes
    generateRigSceneFileName = worksceneDirectory + "\\" + prefix + "_" + charaID + "_rig" + fileFormat

    print(u"workscenesまでのパス： " + worksceneDirectory)
    print(u"Animリグデータ: " + generateRigSceneFileName)

    #フォルダあるかチェック。なかったら作る
    directoryExists = directoryExistsCheck(worksceneDirectory)
    print(u"フォルダがあるか： " + str(directoryExists))

    #animシーン作成
    generateAnimSceneFileName = worksceneDirectory + "\\" + prefix + "_" + charaID + "_anim" + fileFormat
    nameSpaceID =  charaID + "_000"
    print(u"ネームスペース: " + nameSpaceID)
    print(u"Animシーンデータ:" + generateAnimSceneFileName)

    #--referenceCmds--#
    #--rigScene Make--#
    #まずシーンを空に
    mc.file(force=True,new=True)
    #リファレンス作成開始
    mc.file(rigfullPath, reference=True, ns = ":")
    #別名で保存
    mc.file(rename = generateRigSceneFileName)
    mc.file(save=True, type="mayaAscii")

    #--referenceCmds--#
    #--animSceneMake--#
    mc.file(force=True,new=True)
    mc.file(generateRigSceneFileName, reference=True, ns = nameSpaceID)
    mc.file(rename = generateAnimSceneFileName)
    mc.file(save=True, type="mayaAscii")

    mc.confirmDialog(m=u"""%s , %s
を作成しました。
以下を確認してください。
%s"""%(generateRigSceneFileName,generateAnimSceneFileName,worksceneDirectory))
