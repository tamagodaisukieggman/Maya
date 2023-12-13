# -*- coding: utf-8 -*-
import os
import subprocess
from sys import exec_prefix
import maya.cmds as cmds
import maya.mel as mel
import tool_log

EST_RIG_NAME = {"ankle": "ankle_{}", "toe": "toe_{}", "leg": "leg_{}"}
LR = ["L", "R"]

def send_logger() -> None:
    """ログ送信用"""
    version = "v2023.03.24"
    logger_type = "create_reverse_foot"

    logger = tool_log.get_logger(logger_type, version)
    logger.send_launch("")

def check_exist_rf_rig(side):
    """リバースフットリグの存在確認

    Args:
        side (str): L,Rのどれかが文字列で入る

    Returns:
        bool: rf用リグが存在していたらTrue
    """
    return cmds.objExists("*_{}_rf_ctl".format(side))


def create_rf_rig(side, rot_order):
    """リバースフットリグの作成

    Args:
        side (string): LR,L,Rのどれかが文字列で入る
        rot_order(int):enumのindexを入力
    """
    for current_side in LR:
        # 既に存在していれば作成しない
        if check_exist_rf_rig(current_side):
            cmds.warning(
                "already exists >> side {} reverse foot rig.".format(current_side)
            )
            continue

        # sideにはLR,L,Rのどれかが入る
        if current_side not in side:
            continue

        try:
            ankle = cmds.ls(EST_RIG_NAME["ankle"].format(current_side))[0]
            toe = cmds.ls(EST_RIG_NAME["toe"].format(current_side))[0]
            leg = cmds.ls(EST_RIG_NAME["leg"].format(current_side))[0]
        except IndexError:
            cmds.warning(
                "not exists >> {} >> eST rig setup may be incomplete".format(
                    EST_RIG_NAME["ankle"].format(current_side)
                )
            )
            continue

        current_ctl = create_cube_curve(toe + "_rf_ctl", 8)

        # rotation_orderの指定
        cmds.setAttr("{}.rotateOrder".format(current_ctl), rot_order)

        pos = cmds.xform(toe, q=True, ws=True, t=True)
        cmds.setAttr("{}.translate".format(current_ctl), *pos, type="double3")

        test = cmds.orientConstraint([ankle, current_ctl], mo=True, weight=1)
        cmds.delete(test)
        parent_const = cmds.parentConstraint([ankle, current_ctl], mo=True, weight=1)

        # アニメーションのベイク
        bake_animation(current_ctl)

        # ベイクに使用したコンストレインの削除
        cmds.delete(parent_const)
        dummy_loc = cmds.spaceLocator(n="leg_ik_pos_" + current_side)[0]
        cmds.parent(dummy_loc, current_ctl)
        pos = cmds.xform(ankle, q=True, ws=True, t=True)
        cmds.xform(dummy_loc, ws=True, t=pos)
        cmds.orientConstraint([current_ctl, ankle], mo=True, weight=1)
        cmds.pointConstraint([dummy_loc, leg], offset=[0, 0, 0], weight=1)

    return 0


def bake_and_delete_anim():
    """アニメーションをベイクしてリグを削除する"""
    for current_side in LR:
        if check_exist_rf_rig(current_side) == False:
            cmds.warning("not exists >> side {} reverse foot rig.".format(current_side))
            continue
        ankle = cmds.ls(EST_RIG_NAME["ankle"].format(current_side))[0]
        toe = cmds.ls(EST_RIG_NAME["toe"].format(current_side))[0]
        leg = cmds.ls(EST_RIG_NAME["leg"].format(current_side))[0]

        root_rig = toe + "_rf_ctl"
        bake_target = [ankle, leg]
        bake_animation(bake_target)
        for lp in bake_target:
            print("animation bake >> {} ".format(lp))

        cmds.delete(root_rig)


def bake_animation(nodes):
    """アニメーションをベイク

    Args:
        joints (strings): アニメーションのベイクターゲットとなるnodeの文字列の配列

    Returns:
        joints (strings): ベイクされたnode
    """
    start = cmds.playbackOptions(q=True, minTime=True)
    end = cmds.playbackOptions(q=True, maxTime=True)
    # Bake Animation
    cmds.bakeResults(
        nodes,
        simulation=True,
        t=(start, end),
        sampleBy=1,
        disableImplicitControl=True,
        preserveOutsideKeys=False,
        sparseAnimCurveBake=False,
        removeBakedAttributeFromLayer=False,
        bakeOnOverrideLayer=False,
        minimizeRotation=False,
        at=["tx", "ty", "tz", "rx", "ry", "rz"],
    )
    # Return Result
    return nodes


def create_cube_curve(name, scaler=1):
    """cubeのコントローラーを作成

    Args:
        name (str): 作成するコントローラーの名前

    Returns:
        str: 作成したコントローラーの名前
    """
    box_point_array = [
        (0.5, 0.5, 0.5),
        (0.5, 0.5, -0.5),
        (-0.5, 0.5, -0.5),
        (-0.5, -0.5, -0.5),
        (0.5, -0.5, -0.5),
        (0.5, 0.5, -0.5),
        (-0.5, 0.5, -0.5),
        (-0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5),
        (0.5, -0.5, 0.5),
        (0.5, -0.5, -0.5),
        (-0.5, -0.5, -0.5),
        (-0.5, -0.5, 0.5),
        (0.5, -0.5, 0.5),
        (-0.5, -0.5, 0.5),
        (-0.5, 0.5, 0.5),
    ]

    # scaler計算
    new_box_point_array = []
    for vec in box_point_array:
        new_vec = []
        for lp in vec:
            new_vec.append(lp * scaler)
        new_box_point_array.append(new_vec)

    controller = cmds.curve(
        d=1,
        p=new_box_point_array,
        k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        n=name,
    )
    return controller
