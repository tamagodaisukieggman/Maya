# -*- coding: utf-8 -*-
import maya.cmds as cmds
import json

import tkgRigBuild.libs.aim as tkgAim
import tkgRigBuild.libs.modifyJoints as tkgMJ
import tkgRigBuild.libs.control.ctrl as tkgCtrl
reload(tkgAim)
reload(tkgMJ)
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

def create_offset_grp(obj=None):
    obj_grp = cmds.createNode('transform', n=obj+'_GRP', ss=True)
    obj_oft_grp = cmds.createNode('transform', n=obj+'_OFFSET_GRP', ss=True)
    obj_sdk_grp = cmds.createNode('transform', n=obj+'_SDK_GRP', ss=True)

    cmds.parent(obj, obj_sdk_grp)
    cmds.parent(obj_sdk_grp, obj_oft_grp)
    cmds.parent(obj_oft_grp, obj_grp)
    return obj_grp

def create_pos_rot_locs(objects=None):
    pos_locs = []
    rot_locs = []
    pa = None
    for obj in objects:
        pos_loc = obj+'_POS_LOC'
        cmds.spaceLocator(n=pos_loc)
        pos_locs.append(pos_loc)
        pos_grp = create_offset_grp(obj=pos_loc)
        cmds.matchTransform(pos_grp, obj)

        rot_loc = obj+'_ROT_LOC'
        tkgCtrl.create_manip_ctrl(rot_loc)
        rot_locs.append(rot_loc)
        rot_grp = create_offset_grp(obj=rot_loc)
        cmds.matchTransform(rot_grp, obj)

        cmds.parent(rot_grp, pos_loc)

        cmds.pointConstraint(rot_loc, obj, w=True)
        cmds.orientConstraint(rot_loc, obj, w=True)

        if pa:
            cmds.parent(pos_grp, pa)

        pa = pos_loc

    return pos_locs, rot_locs

# First select the shape, not the transform.
sel = cmds.ls(os=True)
shape = cmds.listRelatives(sel[0], s=True)[0]
cmds.select( shape , r=True )

result = cmds.skeletonEmbed()
embedding = json.loads( result )

# Exchange keys
embedding['joints']['left_arm'] = embedding['joints'].pop('left_shoulder')
embedding['joints']['right_arm'] = embedding['joints'].pop('right_shoulder')

embedding['joints']['left_ball'] = embedding['joints'].pop('left_foot')
embedding['joints']['right_ball'] = embedding['joints'].pop('right_foot')


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

    'left_ball':'left_ankle',
    'left_ankle':'left_knee',
    'left_knee':'left_thigh',
    'left_thigh':'hips',

    'right_ball':'right_ankle',
    'right_ankle':'right_knee',
    'right_knee':'right_thigh',
    'right_thigh':'hips',

}

# create joints
# 実際に作成するのはembeddingに格納した値を確認してから
embedded_joints = create_joints_from_embedding( embedding )

for child, parent in parent_hierarchy.items():
    cmds.parent(child, parent)

# Aiming Spine
spine_01 = 'spine_01'
tkgMJ.aim_correct_joints(sel=[spine_01],
                       aim_axis='y',
                       up_axis='y',
                       worldUpType='object',
                       ssc_sts=False,
                       worldSpace=True,
                       world_axis='y')

# Aiming shoulder
left_shoulder = 'left_shoulder'
tkgMJ.aim_correct_joints(sel=[left_shoulder],
                       aim_axis='x',
                       up_axis='-y',
                       worldUpType='object',
                       ssc_sts=False,
                       worldSpace=True,
                       world_axis='y')

# Aiming arm
left_arm = 'left_arm'
tkgMJ.aim_correct_joints(sel=[left_arm],
                       aim_axis='x',
                       up_axis='-y',
                       worldUpType='object',
                       ssc_sts=False,
                       worldSpace=True,
                       world_axis='x')

# Aiming arm
left_thigh = 'left_thigh'
tkgMJ.aim_correct_joints(sel=[left_thigh],
                       aim_axis='x',
                       up_axis='y',
                       worldUpType='object',
                       ssc_sts=False,
                       worldSpace=True,
                       world_axis='x')

# Mirror Joints
cmds.delete('right_shoulder')
cmds.delete('right_thigh')

left_parts = [left_shoulder, left_thigh]
for obj in left_parts:
    mirror_joints = cmds.mirrorJoint(obj,
                 mirrorYZ=True,
                 mirrorBehavior=True,
                 searchReplace=mirror)

# Mirror Joints
root_jnt = 'root'
mirror_joints = []
base_joints = cmds.ls(root_jnt, dag=True, type='joint')
for jnt in base_joints:
    new_name = 'mirror_'+jnt
    mirror_joints.append(new_name)
    dup = cmds.duplicate(jnt, po=True, n=new_name)
    pa = cmds.listRelatives(jnt, p=True) or None
    if pa:
        parent_name = 'mirror_'+pa[0]
        if cmds.objExists(parent_name):
            cmds.parent(new_name, parent_name)

mirror_grp = cmds.createNode('transform', n='mirror_joints_GRP', ss=True)
cmds.parent('mirror_root', mirror_grp)
cmds.setAttr(mirror_grp+'.sx', -1)
cmds.setAttr(mirror_grp+'.v', 0)

# left to right connection
cmds.pointConstraint('hips', 'mirror_hips', w=True)
cmds.orientConstraint('hips', 'mirror_hips', w=True, mo=True)

cmds.pointConstraint('spine_03', 'mirror_spine_03', w=True)
cmds.orientConstraint('spine_03', 'mirror_spine_03', w=True, mo=True)


side_pos_connect = [
    'shoulder',
    'arm',
    'elbow',
    'hand',

    'thigh',
    'knee',
    'ankle',
    'ball'
]

for part in side_pos_connect:
    cmds.connectAttr(mirror[0]+part+'.t', 'mirror_'+mirror[0]+part+'.t', f=True)
    cmds.connectAttr(mirror[0]+part+'.r', 'mirror_'+mirror[0]+part+'.r', f=True)

    cmds.pointConstraint('mirror_'+mirror[0]+part, mirror[1]+part, w=True)
    cmds.orientConstraint('mirror_'+mirror[0]+part, mirror[1]+part, w=True, mo=True)

# Controllers Const
left_arms = cmds.ls(left_shoulder, dag=True, type='joint')
left_legs = cmds.ls(left_thigh, dag=True, type='joint')

left_arm_pos_locs, left_arm_rot_locs = create_pos_rot_locs(left_arms)
left_leg_pos_locs, left_leg_rot_locs = create_pos_rot_locs(left_legs)

cmds.parent('left_hand_POS_LOC_GRP', 'left_arm_POS_LOC')
# cmds.parent('left_knee_POS_LOC_GRP', 'left_thigh_POS_LOC')
cmds.parent('left_ankle_POS_LOC_GRP', 'left_thigh_POS_LOC')
cmds.parent('left_ball_POS_LOC_GRP', 'left_thigh_POS_LOC')

# Aim
left_arm_aim_loc = left_arm_pos_locs[0]+'_AIM'
cmds.spaceLocator(n=left_arm_aim_loc)
aim_loc_grp = create_offset_grp(left_arm_aim_loc)
cmds.matchTransform(aim_loc_grp, left_arm_pos_locs[-1])
cmds.aimConstraint(
    left_arm_aim_loc,
    left_arm_pos_locs[1]+'_OFFSET_GRP',
    offset=[0,0,0],
    w=True,
    aimVector=[1,0,0],
    upVector=[0,-1,0],
    worldUpType='scene',
)


# Point Const
cmds.pointConstraint('left_shoulder_POS_LOC_AIM', 'left_hand_POS_LOC_OFFSET_GRP', w=True, mo=True)

cmds.pointConstraint('left_arm_POS_LOC', 'left_elbow_POS_LOC_OFFSET_GRP', w=True, mo=True)
cmds.pointConstraint('left_hand_POS_LOC', 'left_elbow_POS_LOC_OFFSET_GRP', w=True, mo=True)

#--------------------------
# Adjusting Axis
#--------------------------
def set_arm_axis_pv_up(shoulder_aim_axis='x', shoulder_up_axis='-y',
                 arm_aim_axis='x', arm_up_axis='z'):
    left_shoulder = left_arms[0]
    left_arm = left_arms[1]
    left_elbow = left_arms[2]
    left_hand = left_arms[3]

    left_shoulder_loc = cmds.spaceLocator(n=left_shoulder+'_LOC')[0]
    left_arm_loc = cmds.spaceLocator(n=left_arm+'_LOC')[0]
    left_elbow_loc = cmds.spaceLocator(n=left_elbow+'_LOC')[0]
    left_hand_loc = cmds.spaceLocator(n=left_hand+'_LOC')[0]

    left_elbow_pvloc = cmds.spaceLocator(n=left_elbow+'_PV_LOC')[0]

    cmds.matchTransform(left_shoulder_loc, left_shoulder)
    cmds.matchTransform(left_arm_loc, left_arm)
    cmds.matchTransform(left_elbow_loc, left_elbow)
    cmds.matchTransform(left_hand_loc, left_hand)

    tkgAim.set_pole_vec(start=left_arm_loc,
                        mid=left_elbow_loc,
                        end=left_hand_loc,
                        move=10,
                        obj=left_elbow_pvloc)

    # Shoulder
    tkgAim.aim_nodes(base=left_arm_loc, target=left_arm_rot_locs[0]+'_OFFSET_GRP',
                     aim_axis=shoulder_aim_axis, up_axis=shoulder_up_axis,
                     worldUpType='scene')
    tkgAim.aim_nodes(base=left_arm_loc, target=left_arm_rot_locs[0],
                     aim_axis=shoulder_aim_axis, up_axis=shoulder_up_axis,
                     worldUpType='scene')

    # Arm
    tkgAim.aim_nodes(base=left_elbow_loc, target=left_arm_rot_locs[1]+'_OFFSET_GRP',
                     aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                     worldUpType='object', worldUpObject=left_elbow_pvloc)
    tkgAim.aim_nodes(base=left_elbow_loc, target=left_arm_rot_locs[1],
                     aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                     worldUpType='object', worldUpObject=left_elbow_pvloc)

    tkgAim.aim_nodes(base=left_hand_loc, target=left_arm_rot_locs[2]+'_OFFSET_GRP',
                     aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                     worldUpType='object', worldUpObject=left_elbow_pvloc)
    tkgAim.aim_nodes(base=left_hand_loc, target=left_arm_rot_locs[2],
                     aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                     worldUpType='object', worldUpObject=left_elbow_pvloc)

    cmds.delete(left_shoulder_loc)
    cmds.delete(left_arm_loc)
    cmds.delete(left_elbow_loc)
    cmds.delete(left_hand_loc)
    cmds.delete(left_elbow_pvloc)

def set_leg_axis_pv_up(leg_aim_axis='x', leg_up_axis='-z',
            ball_aim_axis='-x', ball_up_axis='-z'):
    left_thigh = left_legs[0]
    left_knee = left_legs[1]
    left_ankle = left_legs[2]
    left_ball = left_legs[3]

    left_thigh_loc = cmds.spaceLocator(n=left_thigh+'_LOC')[0]
    left_knee_loc = cmds.spaceLocator(n=left_knee+'_LOC')[0]
    left_ankle_loc = cmds.spaceLocator(n=left_ankle+'_LOC')[0]
    left_ball_loc = cmds.spaceLocator(n=left_ball+'_LOC')[0]

    left_knee_pvloc = cmds.spaceLocator(n=left_knee+'_PV_LOC')[0]

    cmds.matchTransform(left_thigh_loc, left_thigh)
    cmds.matchTransform(left_knee_loc, left_knee)
    cmds.matchTransform(left_ankle_loc, left_ankle)
    cmds.matchTransform(left_ball_loc, left_ball)

    tkgAim.set_pole_vec(start=left_thigh_loc,
                        mid=left_knee,
                        end=left_ankle,
                        move=10,
                        obj=left_knee_pvloc)

    # Leg
    tkgAim.aim_nodes(base=left_knee_loc, target=left_leg_rot_locs[0]+'_OFFSET_GRP',
                     aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                     worldUpType='object', worldUpObject=left_knee_pvloc)
    tkgAim.aim_nodes(base=left_knee_loc, target=left_leg_rot_locs[0],
                     aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                     worldUpType='object', worldUpObject=left_knee_pvloc)

    tkgAim.aim_nodes(base=left_ankle_loc, target=left_leg_rot_locs[1]+'_OFFSET_GRP',
                     aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                     worldUpType='object', worldUpObject=left_knee_pvloc)
    tkgAim.aim_nodes(base=left_ankle_loc, target=left_leg_rot_locs[1],
                     aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                     worldUpType='object', worldUpObject=left_knee_pvloc)

    tkgAim.aim_nodes(base=left_ball_loc, target=left_leg_rot_locs[2]+'_OFFSET_GRP',
                     aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                     worldUpType='object', worldUpObject=left_knee_pvloc)
    tkgAim.aim_nodes(base=left_ball_loc, target=left_leg_rot_locs[2],
                     aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                     worldUpType='object', worldUpObject=left_knee_pvloc)


    # Ball
    tkgAim.aim_nodes(base=left_ankle_loc, target=left_leg_rot_locs[3]+'_OFFSET_GRP',
                     aim_axis=ball_aim_axis, up_axis=ball_up_axis,
                     worldUpType='object', worldSpace=True, world_axis='y')
    tkgAim.aim_nodes(base=left_ankle_loc, target=left_leg_rot_locs[3],
                     aim_axis=ball_aim_axis, up_axis=ball_up_axis,
                     worldUpType='object', worldSpace=True, world_axis='y')

    cmds.delete(left_thigh_loc)
    cmds.delete(left_knee_loc)
    cmds.delete(left_ankle_loc)
    cmds.delete(left_ball_loc)
    cmds.delete(left_knee_pvloc)

set_arm_axis_pv_up(shoulder_aim_axis='x', shoulder_up_axis='-y',
            arm_aim_axis='x', arm_up_axis='z')


set_leg_axis_pv_up(leg_aim_axis='x', leg_up_axis='z',
            ball_aim_axis='-x', ball_up_axis='z')
