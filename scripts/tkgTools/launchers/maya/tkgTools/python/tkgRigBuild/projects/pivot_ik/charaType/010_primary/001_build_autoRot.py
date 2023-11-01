# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload


def add_autoRot(rot_addAttr=None, rot_main=None):
    """
    手首の自動回転
    """
    rot_main_auto_grp = rot_main + '_AUTO_GRP'
    rot_ctrl_cnst_grp = rot_main + '_CNST_GRP'
    if not cmds.objExists(rot_main_auto_grp):
        cmds.createNode('transform', n=rot_main_auto_grp, ss=True)

    cmds.matchTransform(rot_main_auto_grp, rot_main)

    pa = cmds.listRelatives(rot_main, p=True)
    if pa:
        auto_pa = cmds.listRelatives(rot_main_auto_grp, p=True)
        if not auto_pa:
            cmds.parent(rot_main_auto_grp, pa[0])

    cmds.parent(rot_main, rot_main_auto_grp)

    dcmx = cmds.createNode('decomposeMatrix', ss=True)
    pbn = cmds.createNode('pairBlend', ss=True)

    cmds.setAttr(pbn + '.rotInterpolation', 1)

    cmds.connectAttr(rot_ctrl_cnst_grp + '.inverseMatrix', dcmx + '.inputMatrix', f=True)
    cmds.connectAttr(dcmx + '.outputRotate', pbn + '.inRotate1', f=True)
    cmds.connectAttr(pbn + '.outRotate', rot_main_auto_grp + '.r', f=True)

    if not rot_addAttr:
        rot_addAttr = rot_main

    if not cmds.objExists(rot_addAttr + '.autoRot'):
        cmds.addAttr(rot_addAttr, ln='autoRot', sn='ar', dv=0, min=0, max=1, at='double', k=True)

    cmds.connectAttr(rot_addAttr + '.ar', pbn + '.weight', f=True)

def add_autoClavicle(rot_addAttr=None, rot_main=None, ikfk_switch=None, aimVector=[1, 0, 0]):
    """
    鎖骨の自動回転
    ※IKのMainのコントローラのSpaceにClavicleを追加するとフリップする
    """
    rot_main_auto_grp = rot_main + '_AUTO_GRP'
    rot_main_auto_inverse_grp = rot_main + '_AUTO_INVERSE_GRP'
    rot_ctrl_cnst_grp = rot_main + '_CNST_GRP'
    if not cmds.objExists(rot_main_auto_grp):
        cmds.createNode('transform', n=rot_main_auto_grp, ss=True)
    cmds.matchTransform(rot_main_auto_grp, rot_main)

    if not cmds.objExists(rot_main_auto_inverse_grp):
        cmds.createNode('transform', n=rot_main_auto_inverse_grp, ss=True)
    cmds.matchTransform(rot_main_auto_inverse_grp, rot_main)

    cmds.parent(rot_main_auto_inverse_grp, rot_main_auto_grp)

    pa = cmds.listRelatives(rot_main, p=True)
    if pa:
        auto_pa = cmds.listRelatives(rot_main_auto_grp, p=True)
        if not auto_pa:
            cmds.parent(rot_main_auto_grp, pa[0])

    cmds.parent(rot_main, rot_main_auto_inverse_grp)

    obj_up_loc = cmds.spaceLocator(n=rot_main + '_AUTO_AIM_UP_LOC')[0]
    cmds.matchTransform(obj_up_loc, rot_main)
    cmds.parent(obj_up_loc, rot_ctrl_cnst_grp)
    cmds.xform(obj_up_loc, t=[0, 10, 0], r=True)

    cmds.aimConstraint(rot_addAttr, rot_main_auto_grp, offset=[0,0,0], w=1, aimVector=aimVector, upVector=[0,1,0],
                       worldUpType="object", worldUpObject=obj_up_loc)


    dcmx = cmds.createNode('decomposeMatrix', ss=True)
    pbn = cmds.createNode('pairBlend', ss=True)
    mdl = cmds.createNode('multDoubleLinear', ss=True)

    cmds.setAttr(pbn + '.rotInterpolation', 1)

    cmds.connectAttr(rot_main_auto_grp + '.inverseMatrix', dcmx + '.inputMatrix', f=True)
    cmds.connectAttr(dcmx + '.outputRotate', pbn + '.inRotate1', f=True)
    cmds.connectAttr(pbn + '.outRotate', rot_main_auto_inverse_grp + '.r', f=True)

    if not rot_addAttr:
        rot_addAttr = rot_main

    if not cmds.objExists(rot_addAttr + '.autoClavicle'):
        cmds.addAttr(rot_addAttr, ln='autoClavicle', sn='ac', dv=0, min=0, max=1, at='double', k=True)

    cmds.connectAttr(ikfk_switch, mdl + '.input1', f=True)
    cmds.connectAttr(rot_addAttr + '.ac', mdl + '.input2', f=True)

    cmds.connectAttr(mdl + '.output', pbn + '.weight', f=True)



add_autoRot(rot_addAttr=None, rot_main='Lf_hand_01_CTRL')
add_autoRot(rot_addAttr=None, rot_main='Rt_hand_01_CTRL')
# add_autoRot(rot_addAttr=None, rot_main='Lf_foot_01_CTRL')
# add_autoRot(rot_addAttr=None, rot_main='Rt_foot_01_CTRL')

add_autoClavicle(rot_addAttr='Lf_arm_IK_main_CTRL', rot_main='Lf_clavicle_CTRL', ikfk_switch='Lf_arm.switch')
add_autoClavicle(rot_addAttr='Rt_arm_IK_main_CTRL', rot_main='Rt_clavicle_CTRL', ikfk_switch='Rt_arm.switch', aimVector=[-1,0,0])
