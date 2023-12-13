# -*- coding: cp932 -*-
#===============================================
#
# ユーティリティ
#
# Fujita Yukihiro
#
#===============================================

import maya.cmds as cmds
import os
import time
import mtk3d.maya.env.os.functions as envos

#===============================================
#
# テキスト クリップボート
#
# @param      method : set,get
# @param      txt : クリップボードに渡す文字列
# @return     クリップボードの文字列
#
#===============================================
def textClipboard(method, txt=""):
    """ テキストをクリップボードにコピー、クリップボードから取得 """

    # コピーかつtxt 引数が文字列じゃなければ終了
    if method == "set" and not isinstance(txt, str):
        return False

    elif method != "set" and method != "get":
        return False

    # 一時ファイル
    tempFileName = os.path.join(os.getenv("TMP"), "fy_tempClipboard.txt")

    # クリップボードにコピーの場合、一時ファイルに書き込み
    if method == "set":
        tempFile = open(tempFileName, "w")
        tempFile.write(txt)
        tempFile.close()

        # 一時ファイルの内容をクリップボードにコピーするコマンド
        batCmd = "clip < " + tempFileName

    elif method == "get":
        # クリップボードの内容を一時ファイルに書き出すコマンド
        batCmd = 'mshta.exe "vbscript:Execute("str=window.clipboardData.getData(""text""):CreateObject(""Scripting.FileSystemObject"").GetStandardStream(1).Write(str^&""""):close")" > ' + tempFileName

    else:
        return False

    # バッチコマンド実行
    envos.execBatchCmd(batCmd)

    # クリップボードから取得の場合
    if method == "get":
        #ウェイト
        time.sleep(0.3)

        # 一時ファイルから読み込み
        tempFile = open(tempFileName, "r")
        txt = tempFile.read()
        tempFile.close()

        return txt
    else:
        return True


#===============================================
#
# スムーズバインドしてウェイトをコピー
#
# @param      msource_mesh: コピー元のメッシュ
# @param      forward_mesh:  コピー先のメッシュ
#
#===============================================
def bind_and_copy_weights(source_mesh, forward_mesh):
    """ スムーズバインドしてウェイトをコピー """

    # コピー元のメッシュからジョイント、スキンクラスタを取得
    root_joint = get_root_joint(source_mesh)

    skin_cluster = get_skin_cluster(source_mesh)

    # skinning meshではない場合、複製して終了
    if not skin_cluster:
        return

    # スキンクラスタの最大インフルエンス数の取得
    max_influence = cmds.getAttr('{}.maxInfluences'.format(skin_cluster))

    # コピー先のメッシュをスムーズバインド、ウェイトコピー
    cmds.skinCluster(forward_mesh, root_joint, omi=True, bm=1, mi=max_influence)

    # ウェイトコピー
    cmds.select([source_mesh, forward_mesh])
    cmds.copySkinWeights(sa='closestPoint', ia='closestJoint', nm=True)


#===============================================
#
# ルートジョイントの取得
#
# @param      mesh: メッシュ
# @return     ルートジョイント
#
#===============================================
def get_root_joint(mesh):
    """ ルートジョイントの取得 """

    skin_cluster = get_skin_cluster(mesh)
    if not skin_cluster:
        return

    joints = cmds.ls(cmds.skinCluster(skin_cluster, q=True, influence=True), long=True)

    if not joints:
        return

    root_joint = None

    for _node in joints[0].split("|"):
        if _node and cmds.objectType(_node) == "joint":
            root_joint = _node
            break

    return root_joint


#===============================================
#
# skinClusterの取得
#
# @param      mesh: メッシュ
# @return     skinCluster
#
#===============================================
def get_skin_cluster(mesh):
    """ skinClusterの取得 """

    skin_clusters = cmds.ls(cmds.listHistory(mesh), typ='skinCluster')
    if skin_clusters:
        return skin_clusters[0]
    else:
        return []


