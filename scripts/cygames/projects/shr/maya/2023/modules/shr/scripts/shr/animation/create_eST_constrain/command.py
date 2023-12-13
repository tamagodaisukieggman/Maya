# -*- coding: utf-8 -*-
import typing as typ

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

mel.eval("eST3start")
import eST3


def _create_locator(target_ctl: str) -> str:
    """rocator の作成 target_ctlの

    Args:
        target_ctl (str): ターゲットとなるコントローラーの名前

    Returns:
        str: 作成したロケーター
    """
    w_location = cmds.xform(target_ctl, q=True, ws=True, t=True)
    locator = cmds.spaceLocator(n=target_ctl + "_loc")[0]
    cmds.xform(locator, ws=True, t=w_location)
    return locator


def _bake_animation(target: str) -> None:
    """アニメーションのベイク

    Args:
        locator (str): 対象となるロケーター
    """
    sf = cmds.playbackOptions(q=True, min=True)
    ef = cmds.playbackOptions(q=True, max=True)
    cmds.bakeResults(
        target,
        simulation=True,
        t=(sf, ef),
        sampleBy=1,
        oversamplingRate=1,
        disableImplicitControl=True,
        preserveOutsideKeys=True,
        sparseAnimCurveBake=False,
        removeBakedAttributeFromLayer=False,
        removeBakedAnimFromLayer=False,
        bakeOnOverrideLayer=False,
        minimizeRotation=True,
        controlPoints=False,
        shape=True,
    )


def get_namespace_from_nodename(target):
    namespace = target.split(":")[0]
    return namespace


def get_user_constraint_plugs(namespace):
    user_anim_plugs = eST3.mCmds.AnimPlugs_constraint(
        "{}:user_constraintPlugs".format(namespace)
    )
    return user_anim_plugs


def generate_eST_constraint(
    maintain_offset: bool, rotation_order: int, method: str
) -> None:
    """eSTのコンストレインとを生成し、ロケーターに親子付け

    Args:
        maintain_offset(bool): parent_const時のmoの有無
        rotation_order(int): enumのint値
        method(str): constraintのメソッド
    """
    # 選択したコントローラーの取得
    selected_ctrls = cmds.ls(sl=True, type="transform")
    # ループ
    for ctrl in selected_ctrls:
        # ロケーターの作成
        anim_loc = _create_locator(ctrl)
        cmds.setAttr("{}.rotateOrder".format(anim_loc), rotation_order)

        # parent const
        pcon = cmds.parentConstraint([ctrl, anim_loc], mo=maintain_offset, weight=1)
        # ロケーターアニメーションベイク
        _bake_animation(anim_loc)

        cmds.select(ctrl)
        ns = get_namespace_from_nodename(ctrl)
        user_anim_plugs = get_user_constraint_plugs(ns)

        # eSTコンストレインノードの作成
        try:
            eST_const = eST3.rCmds.AttachAnimPlugsConstraint(
                animPlugs=user_anim_plugs,
                method=method,
                useSelection=True,
                maintainOffset=False,
            )

        except RuntimeError:
            cmds.warning('This constraint_type >> "{}" is not allowed.'.format(method))
            cmds.delete(pcon, anim_loc)
            continue

        # parentコンストレインの削除
        cmds.delete(pcon)

        # コンストレイン親子付け
        cmds.parent(eST_const, anim_loc)


def get_selected_ctrl() -> typ.List[str]:
    """選択しているコントローラーをリストで返す

    Returns:
        _type_: _description_
    """
    ctrls = cmds.ls(sl=True, type="transform")
    return ctrls


def get_rotation_order() -> int:
    """選択したコントローラーのrotation orderを返す（複数の場合はpass）"""
    ctrls = get_selected_ctrl()
    if len(ctrls) > 1:
        cmds.warning("Multiple assets selected.Please select only one controller.")
        return False

    elif len(ctrls) == 1:
        try:
            current_rot_order = cmds.getAttr("{}.rotationOrder".format(ctrls[0]))
        except:
            current_rot_order = cmds.getAttr("{}.rotateOrder".format(ctrls[0]))
    else:
        cmds.warning("No controller selected.")
        return False

    return current_rot_order


def delete_locator() -> None:
    """locatorの削除を実行"""
    selected_locators = cmds.ls(sl=True, type="transform")
    for loc in selected_locators:
        if "_loc" not in loc:
            cmds.warning("{} is not eST locator".format(loc))
            continue
        cmds.select(cmds.listRelatives(loc, c=True), r=True)
        ns = get_namespace_from_nodename(loc)
        delete_constraint(ns)
        cmds.delete(loc)


def get_current_constraint(
    anim_plugs: eST3.mCmds.AnimPlugs_constraint,
) -> typ.List[eST3.mCmds.Transform]:
    """_summary_

    Args:
        anim_plugs (eST3.mCmds.AnimPlugs_constraint): 対象となるanimPlug

    Returns:
        _type_: _description_
    """
    constraints = []

    for x in eST3.passList(cmds.ls(sl=1, o=1)):
        for constraint in anim_plugs.listRelatedConstraints(x):
            if constraint not in constraints and anim_plugs.isMember(constraint):
                constraints.append(constraint)
    return constraints


def delete_constraint(namespace):
    """選択したeSTコンストレインの削除"""
    animPlugs = get_user_constraint_plugs(namespace)
    constraints = get_current_constraint(animPlugs)
    ctrls = []
    for constraint in constraints:
        for plug in animPlugs.listDrivens(constraint):
            if plug.getNode() not in ctrls:
                ctrls.append(plug.getNode())

    _bake_animation(ctrls)

    # unparent handles that is parented to handles to be deleted.
    for handle in animPlugs.listAllHandles():
        if not handle.isTransform():
            continue
        for constraint in constraints:
            for node in [constraint] + animPlugs.listRelatedHandles(constraint):
                if node.isTransform() and handle < node:
                    handle.setParent(None)
                    break
            else:
                continue
            break
    # delete.
    for constraint in constraints:
        animPlugs.removeConstraint([constraint])
