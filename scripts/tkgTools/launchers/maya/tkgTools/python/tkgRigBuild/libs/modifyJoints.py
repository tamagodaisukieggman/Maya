# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload
import math

import tkgRigBuild.libs.aim as tkgAim
reload(tkgAim)

def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

def round_attrs(obj=None, attrs=None):
    for at in attrs:
        set_at = '{}.{}'.format(obj, at)
        val = cmds.getAttr(set_at)
        if not val == 0.0:
            if 'e' in str(val):
                cmds.setAttr(set_at, 0.0)
                continue

            try:
                cmds.setAttr(set_at, truncate(round(val, 3), 3))
            except Exception as e:
                print(traceback.format_exc())

def round_transform_attrs(transforms=None):
    attrs = ['tx', 'ty', 'tz',
             'rx', 'ry', 'rz',
             'sx', 'sy', 'sz']

    joint_attrs = ['pax', 'pay', 'paz',
                   'jox', 'joy', 'joz',
                   'radius']

    for obj in transforms:
        round_attrs(obj, attrs)
        if cmds.objectType(obj) == 'joint':
            round_attrs(obj, joint_attrs)


def merge_joints(joints):
    for obj in joints:
        set_wr = cmds.xform(obj, q=1, ro=1, ws=1)
        cmds.setAttr('{}.jo'.format(obj), *(0, 0, 0))
        cmds.xform(obj, ro=set_wr, ws=1, a=1)

def freeze_rotate(joints):
    [cmds.makeIdentity(obj, n=False, s=False, r=True, t=False, apply=True, pn=True)
        for obj in joints]

def set_preferred_angle(joints=None):
    if not joints: return
    [cmds.joint(jnt, e=True, spa=True, ch=True) for jnt in joints]

def adjust_mirrors(force_values=[180, 0, 0], joints=None):
    # ジョイントを選択して実行
    if not joints: return

    for obj in joints:
        pa = cmds.listRelatives(obj, p=True) or None
        if pa: cmds.parent(obj, w=True)
        children = cmds.listRelatives(obj, c=True) or None
        if children: [cmds.parent(ch, w=True) for ch in children]

        cmds.xform(obj, ro=force_values, p=True, os=True, r=True)

        if pa: cmds.parent(obj, pa[0])
        if children: [cmds.parent(ch, obj) for ch in children]

def set_segmentScaleCompensate(joints=None, ssc_sts=False):
    [cmds.setAttr(jnt+'.ssc', ssc_sts) for jnt in joints]

# Aim Joints
sel = cmds.ls(os=True, type='joint')
for obj in sel:
    tkgAim.aim_nodes_from_root(root_jnt=obj,
                               type='joint',
                               aim_axis='z',
                               up_axis='y',
                               worldUpType='object')

# Merge Joints
sel = cmds.ls(os=True, dag=True, type='joint')
freeze_rotate(sel)
merge_joints(sel)
round_transform_attrs(sel)

# Mirror Joints
mirror = ['_L', '_R']
sel = cmds.ls(os=True, type='joint')
for obj in sel:
    mirror_joints = cmds.mirrorJoint(obj,
                 mirrorYZ=True,
                 mirrorBehavior=True,
                 searchReplace=mirror)
    adjust_mirrors(force_values=[180, 0, 0],
                   joints=mirror_joints)

    freeze_rotate(mirror_joints)
    merge_joints(mirror_joints)
    round_transform_attrs(mirror_joints)

# Set Preferred Angle
joints = cmds.ls('UJ_*', type='joint')
set_preferred_angle(joints=joints)

# Set segmentScaleCompensate
set_segmentScaleCompensate(joints=joints, ssc_sts=False)
