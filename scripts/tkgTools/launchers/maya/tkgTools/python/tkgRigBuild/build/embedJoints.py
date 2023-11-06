# -*- coding: utf-8 -*-
import maya.cmds as cmds
import json

import tkgRigBuild.libs.aim as tkgAim
import tkgRigBuild.libs.control.ctrl as tkgCtrl
reload(tkgAim)
reload(tkgCtrl)


def create_joint(name=None, position=None):
    joint = cmds.createNode( 'joint' , name=name )
    cmds.xform( joint , worldSpace=True , translation=position )
    return joint

# This method creates a few joints to see the embedding.
def create_joints_from_embedding( embedding ):
    embedded_joints = [create_joint(name=name, position=position)
                        for name , position in embedding[ 'joints' ].items( )]
    return embedded_joints

def get_mid_point(pos1, pos2, percentage=0.5):
    mid_point = [pos1[0] + (pos2[0] - pos1[0]) * percentage,
                 pos1[1] + (pos2[1] - pos1[1]) * percentage,
                 pos1[2] + (pos2[2] - pos1[2]) * percentage]
    return mid_point

def add_segments(start_position=None, end_position=None, base_name=None, count=3, embedding=None):
    # base_name = 'spine'
    # count = 3
    step = 1.0 / count
    max_rate = 1 - step
    rate = 0
    for i in range(count):
        mid_point = get_mid_point(start_position, end_position, rate)
        embedding['joints']['{}_{}'.format(base_name, str(i+1).zfill(2))] = mid_point
        rate += step

def merge_joints(joints):
    for obj in joints:
        set_wr = cmds.xform(obj, q=1, ro=1, ws=1)
        cmds.setAttr('{}.jo'.format(obj), *(0, 0, 0))
        cmds.xform(obj, ro=set_wr, ws=1, a=1)

def freeze_rotate(joints):
    [cmds.makeIdentity(obj, n=False, s=False, r=True, t=False, apply=True, pn=True)
        for obj in joints]


# First select the shape, not the transform.
sel = cmds.ls(os=True)
shape = cmds.listRelatives(sel[0], s=True)[0]
cmds.select( shape , r=True )

result = cmds.skeletonEmbed()
embedding = json.loads( result )

# Exchange keys
embedding['joints']['left_arm'] = embedding['joints'].pop('left_shoulder')
embedding['joints']['right_arm'] = embedding['joints'].pop('right_shoulder')

# Fixing spine
embedding['joints']['spine'] = embedding['joints'].pop('back')

# Fixing arm and shoulder
shoulders_position = embedding['joints']['shoulders']
left_arm_position = embedding['joints']['left_arm']
right_arm_position = embedding['joints']['right_arm']

left_arm_mid_point = get_mid_point(shoulders_position, left_arm_position)
right_arm_mid_point = get_mid_point(shoulders_position, right_arm_position)

embedding['joints'].update({'left_shoulder':left_arm_mid_point})
embedding['joints'].update({'right_shoulder':right_arm_mid_point})

# Fixing neck
embedding['joints']['neck'] = embedding['joints'].pop('shoulders')
neck_position = embedding['joints']['neck']
head_position = embedding['joints']['head']

neck_head_mid_point = get_mid_point(neck_position, head_position, 0.3)
embedding['joints']['neck'] = neck_head_mid_point

# Fixing head
fix_head_mid_point = get_mid_point(neck_position, head_position, 0.7)
embedding['joints']['head'] = fix_head_mid_point

# Fixing Side
left_sides = {}
for joint, position in embedding['joints'].items():
    if 'left_' in joint:
        left_sides[joint] = position

for joint, position in embedding['joints'].items():
    if 'left_' in joint:
        l_pos = left_sides[joint]
        r_pos = []
        r_pos.append(l_pos[0]*-1)
        r_pos.append(l_pos[1])
        r_pos.append(l_pos[2])
        embedding['joints'][joint.replace('left_', 'right_')] = r_pos

# Fixing Straight
for s in ['left_', 'right_']:
    for i, p in enumerate([['arm', 'elbow', 'hand'], ['thigh', 'knee', 'ankle']]):
        start_position = embedding['joints'][s+p[0]]
        end_position = embedding['joints'][s+p[2]]
        embedding['joints'][s+p[1]] = get_mid_point(start_position, end_position)

for joint in ['hips', 'spine', 'neck', 'head']:
    old_pos = embedding['joints'][joint]
    new_pos = []
    new_pos.append(old_pos[0]*0)
    new_pos.append(old_pos[1])
    new_pos.append(old_pos[2])
    embedding['joints'][joint] = new_pos

# Add Spine Segments
spine_count=3
if spine_count != 1:
    start_position = embedding['joints']['hips']
    end_position = embedding['joints']['neck']
    add_segments(start_position=start_position,
                 end_position=end_position,
                 base_name='spine',
                 count=spine_count,
                 embedding=embedding)
    embedding['joints'].pop('spine')

# Add Neck Segments
neck_count=2
if neck_count != 1:
    start_position = embedding['joints']['neck']
    end_position = embedding['joints']['head']
    add_segments(start_position=start_position,
                 end_position=end_position,
                 base_name='neck',
                 count=neck_count,
                 embedding=embedding)
    embedding['joints'].pop('neck')

# Add Root Joint
embedding['joints']['root'] = [0, 0, 0]

# Add Neck Segments
root_count=1
if root_count != 1:
    start_position = embedding['joints']['root']
    end_position = embedding['joints']['root']
    add_segments(start_position=start_position,
                 end_position=end_position,
                 base_name='root',
                 count=root_count,
                 embedding=embedding)
    embedding['joints'].pop('root')


# Connect Joints
mirror = ['left_', 'right_']
parent_hierarchy = {
    'hips':'root',
    'spine_01':'hips',
    'spine_02':'spine_01',
    'spine_03':'spine_02',
    'neck_01':'spine_03',
    'neck_02':'neck_01',
    'head':'neck_02',

    'left_hand':'left_elbow',
    'left_elbow':'left_arm',
    'left_arm':'left_shoulder',
    'left_shoulder':'spine_03',

    'right_hand':'right_elbow',
    'right_elbow':'right_arm',
    'right_arm':'right_shoulder',
    'right_shoulder':'spine_03',

    'left_foot':'left_ankle',
    'left_ankle':'left_knee',
    'left_knee':'left_thigh',
    'left_thigh':'hips',

    'right_foot':'right_ankle',
    'right_ankle':'right_knee',
    'right_knee':'right_thigh',
    'right_thigh':'hips',

}

# create joints
# 実際に作成するのはembeddingに格納した値を確認してから
embedded_joints = create_joints_from_embedding( embedding )

for child, parent in parent_hierarchy.items():
    cmds.parent(child, parent)

side_pos_connect = [
    'shoulder',
    'arm',
    'elbow',
    'hand',

    'thigh',
    'knee',
    'ankle',
    'foot'
]

for part in side_pos_connect:
    cmds.connectAttr(mirror[0]+part+'.ty', mirror[1]+part+'.ty', f=True)
    cmds.connectAttr(mirror[0]+part+'.tz', mirror[1]+part+'.tz', f=True)

    mdn = cmds.createNode('multiplyDivide', ss=True)
    cmds.setAttr(mdn+'.input2X', -1)

    cmds.connectAttr(mirror[0]+part+'.tx', mdn+'.input1X', f=True)
    cmds.connectAttr(mdn+'.outputX', mirror[1]+part+'.tx', f=True)

root_jnt = 'root'
rot_joints = []
base_joints = cmds.ls(root_jnt, dag=True, type='joint')
for jnt in base_joints:
    new_name = 'rot_'+jnt
    rot_joints.append(new_name)
    dup = cmds.duplicate(jnt, po=True, n=new_name)
    cmds.setAttr(new_name+'.drawStyle', 3)
    radius_ = cmds.getAttr(jnt+'.radius')
    cmds.setAttr(new_name+'.radius', radius_ * 2)
    pa = cmds.listRelatives(jnt, p=True) or None
    if pa:
        parent_name = 'rot_'+pa[0]
        if cmds.objExists(parent_name):
            cmds.parent(new_name, parent_name)

# Arm Joint Aim
arm_root_jnt = 'rot_left_shoulder'
tkgAim.aim_nodes_from_root(root_jnt=arm_root_jnt,
                           type='joint',
                           aim_axis='x',
                           up_axis='y',
                           worldUpType='object')

right_arm_root_jnt = arm_root_jnt.replace(mirror[0], mirror[1])
cmds.delete(right_arm_root_jnt)

arm_parent = cmds.listRelatives(arm_root_jnt, p=True)[0]
cmds.parent(arm_root_jnt, w=True)

# Leg Joint Aim
leg_root_jnt = 'rot_left_thigh'
tkgAim.aim_nodes_from_root(root_jnt=leg_root_jnt,
                           type='joint',
                           aim_axis='x',
                           up_axis='-z',
                           worldUpType='object')

right_leg_root_jnt = leg_root_jnt.replace(mirror[0], mirror[1])
cmds.delete(right_leg_root_jnt)

# leg_parent = cmds.listRelatives(leg_root_jnt, p=True)[0]
# cmds.parent(leg_root_jnt, w=True)

cmds.mirrorJoint(leg_root_jnt,
                 mirrorYZ=True,
                 mirrorBehavior=True,
                 searchReplace=mirror)

# Spine Joint Aim
spine_root_jnt = 'rot_spine_01'
tkgAim.aim_nodes_from_root(root_jnt=spine_root_jnt,
                           type='joint',
                           aim_axis='y',
                           up_axis='y',
                           worldUpType='scene')

cmds.parent(arm_root_jnt, arm_parent)

cmds.mirrorJoint(arm_root_jnt,
                 mirrorYZ=True,
                 mirrorBehavior=True,
                 searchReplace=mirror)

# Merge Joints
merge_joints(rot_joints)
freeze_rotate(rot_joints)

# Mirror Rot Connect
for arm_rj in cmds.ls(arm_root_jnt, dag=True, type='joint'):
    cmds.connectAttr(arm_rj+'.r', arm_rj.replace(mirror[0], mirror[1])+'.r', f=True)

for leg_rj in cmds.ls(leg_root_jnt, dag=True, type='joint'):
    cmds.connectAttr(leg_rj+'.r', leg_rj.replace(mirror[0], mirror[1])+'.r', f=True)


# tkgAim.aim_nodes_from_root(root_jnt='rot_left_shoulder',
#                            type='joint',
#                            aim_axis='y',
#                            up_axis='x',
#                            worldUpType='object')

# Const pos to rot
for bj in base_joints:
    cmds.pointConstraint(bj, 'rot_'+bj, w=True)
    cmds.orientConstraint('rot_'+bj, bj, w=True, mo=True)


# Create Manip Ctrls
for rj in rot_joints:
    axis_ctrl = rj + '_axis_CTRL'
    grp = cmds.createNode('transform', ss=True, n=axis_ctrl+'_grp')
    tkgCtrl.create_manip_ctrl(axis_ctrl)

    cmds.addAttr(axis_ctrl, ln='aimVector', at='enum', en='x:y:z:-x:-y:-z:', k=True)
    cmds.addAttr(axis_ctrl, ln='upVector', at='enum', en='x:y:z:-x:-y:-z:', k=True)

    cmds.parent(axis_ctrl, grp)
    cmds.matchTransform(grp, rj)

    cmds.pointConstraint(rj.replace('rot_', ''), grp, w=True)
    cmds.orientConstraint(rj, grp, w=True)
