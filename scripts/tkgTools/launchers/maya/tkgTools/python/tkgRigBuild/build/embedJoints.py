# -*- coding: utf-8 -*-
import maya.cmds as cmds

import tkgRigBuild.libs.aim as tkgAim
import tkgRigBuild.libs.modifyJoints as tkgMJ
import tkgRigBuild.libs.control.ctrl as tkgCtrl
import tkgRigBuild.libs.common as tkgCommon
reload(tkgAim)
reload(tkgMJ)
reload(tkgCtrl)
reload(tkgCommon)


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
segments = tkgMJ.embed_biped_joints(sel[0], root_count=1, spine_count=3, neck_count=2, knee_count=2)
root_segments = segments[0]
spine_segments = segments[1]
neck_segments = segments[2]
left_knee_segments = segments[3]
right_knee_segments = segments[4]

mirror = ['left_', 'right_']

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
    'ankle',
    'ball'
]

[side_pos_connect.append('_'.join(n.split('_')[1::])) for n in left_knee_segments.seg_joints]

for part in side_pos_connect:
    cmds.connectAttr(mirror[0]+part+'.t', 'mirror_'+mirror[0]+part+'.t', f=True)
    cmds.connectAttr(mirror[0]+part+'.r', 'mirror_'+mirror[0]+part+'.r', f=True)

    cmds.pointConstraint('mirror_'+mirror[0]+part, mirror[1]+part, w=True)
    cmds.orientConstraint('mirror_'+mirror[0]+part, mirror[1]+part, w=True, mo=True)

# Controllers Const
left_arms = cmds.ls('left_shoulder', dag=True, type='joint')
left_legs = cmds.ls('left_thigh', dag=True, type='joint')

left_arm_pos_locs, left_arm_rot_locs = create_pos_rot_locs(left_arms)
left_leg_pos_locs, left_leg_rot_locs = create_pos_rot_locs(left_legs)

cmds.parent('left_hand_POS_LOC_GRP', 'left_arm_POS_LOC')
# cmds.parent('left_knee_POS_LOC_GRP', 'left_thigh_POS_LOC')
cmds.parent('left_ankle_POS_LOC_GRP', 'left_thigh_POS_LOC')
cmds.parent('left_ball_POS_LOC_GRP', 'left_thigh_POS_LOC')

# # Aim
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
cmds.setAttr(left_arm_aim_loc+'.v', 0)

# # # Point Const
cmds.pointConstraint('left_shoulder_POS_LOC_AIM', 'left_hand_POS_LOC_OFFSET_GRP', w=True, mo=True)

cmds.pointConstraint('left_arm_POS_LOC', 'left_elbow_POS_LOC_OFFSET_GRP', w=True, mo=True)
cmds.pointConstraint('left_hand_POS_LOC', 'left_elbow_POS_LOC_OFFSET_GRP', w=True, mo=True)

# Scale Tweak
# arm
cmds.addAttr('left_shoulder_POS_LOC_GRP', ln='posLocsScale', at='double', dv=1, k=True)
cmds.addAttr('left_shoulder_POS_LOC_GRP', ln='rotLocsScale', at='double', dv=1, k=True)

for lapl, larl in zip(left_arm_pos_locs, left_arm_rot_locs):
    cmds.connectAttr('left_shoulder_POS_LOC_GRP.posLocsScale', lapl+'.localScaleX', f=True)
    cmds.connectAttr('left_shoulder_POS_LOC_GRP.posLocsScale', lapl+'.localScaleY', f=True)
    cmds.connectAttr('left_shoulder_POS_LOC_GRP.posLocsScale', lapl+'.localScaleZ', f=True)

    cmds.connectAttr('left_shoulder_POS_LOC_GRP.rotLocsScale', larl+'.sx', f=True)
    cmds.connectAttr('left_shoulder_POS_LOC_GRP.rotLocsScale', larl+'.sy', f=True)
    cmds.connectAttr('left_shoulder_POS_LOC_GRP.rotLocsScale', larl+'.sz', f=True)

# leg
cmds.addAttr('left_thigh_POS_LOC_GRP', ln='posLocsScale', at='double', dv=1, k=True)
cmds.addAttr('left_thigh_POS_LOC_GRP', ln='rotLocsScale', at='double', dv=1, k=True)

for llpl, llrl in zip(left_leg_pos_locs, left_leg_rot_locs):
    cmds.connectAttr('left_thigh_POS_LOC_GRP.posLocsScale', llpl+'.localScaleX', f=True)
    cmds.connectAttr('left_thigh_POS_LOC_GRP.posLocsScale', llpl+'.localScaleY', f=True)
    cmds.connectAttr('left_thigh_POS_LOC_GRP.posLocsScale', llpl+'.localScaleZ', f=True)

    cmds.connectAttr('left_thigh_POS_LOC_GRP.rotLocsScale', llrl+'.sx', f=True)
    cmds.connectAttr('left_thigh_POS_LOC_GRP.rotLocsScale', llrl+'.sy', f=True)
    cmds.connectAttr('left_thigh_POS_LOC_GRP.rotLocsScale', llrl+'.sz', f=True)


# Adjustment Grp
adjustment_grp = 'adjustment_grp'
cmds.createNode('transform', n=adjustment_grp, ss=True)
cmds.parent(mirror_grp, adjustment_grp)
cmds.parent('left_shoulder_POS_LOC_GRP', adjustment_grp)
cmds.parent('left_thigh_POS_LOC_GRP', adjustment_grp)
cmds.parent(aim_loc_grp, adjustment_grp)

cmds.addAttr(adjustment_grp, ln='armPosLocsScale', at='double', dv=1, k=True)
cmds.addAttr(adjustment_grp, ln='armRotLocsScale', at='double', dv=1, k=True)
cmds.connectAttr(adjustment_grp + '.armPosLocsScale', 'left_shoulder_POS_LOC_GRP.posLocsScale', f=True)
cmds.connectAttr(adjustment_grp + '.armRotLocsScale', 'left_shoulder_POS_LOC_GRP.rotLocsScale', f=True)

cmds.addAttr(adjustment_grp, ln='legPosLocsScale', at='double', dv=1, k=True)
cmds.addAttr(adjustment_grp, ln='legRotLocsScale', at='double', dv=1, k=True)
cmds.connectAttr(adjustment_grp + '.legPosLocsScale', 'left_thigh_POS_LOC_GRP.posLocsScale', f=True)
cmds.connectAttr(adjustment_grp + '.legRotLocsScale', 'left_thigh_POS_LOC_GRP.rotLocsScale', f=True)


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

    buf_left_legs = [n for n in left_legs]
    buf_left_leg_rot_locs = [n for n in left_leg_rot_locs]
    buf_left_knee_rot_locs = [n for n in left_leg_rot_locs
                                if 'knee' in '_'.join(n.split('_')[:2:])]

    [buf_left_legs.remove(n) for n in left_knee_segments.seg_joints]
    [buf_left_leg_rot_locs.remove(n)
        for n in left_leg_rot_locs if not '_'.join(n.split('_')[:2:]) in left_legs]

    left_thigh = buf_left_legs[0]
    left_ankle = buf_left_legs[1]
    left_ball = buf_left_legs[2]

    left_thigh_loc = cmds.spaceLocator(n=left_thigh+'_LOC')[0]
    left_ankle_loc = cmds.spaceLocator(n=left_ankle+'_LOC')[0]
    left_ball_loc = cmds.spaceLocator(n=left_ball+'_LOC')[0]

    cmds.matchTransform(left_thigh_loc, left_thigh)
    cmds.matchTransform(left_ankle_loc, left_ankle)
    cmds.matchTransform(left_ball_loc, left_ball)

    # Knee PV obj
    left_knee_pvlocs = []
    for i, leg_obj in enumerate(left_legs):
        # i == 0
        if i+2 == len(left_legs)-1:
            break
        start_obj = leg_obj
        mid_obj = left_legs[i+1]
        end_obj = left_legs[i+2]
        left_knee_pvloc = cmds.spaceLocator(n=leg_obj+'_PV_LOC')[0]
        tkgAim.set_pole_vec(start=start_obj,
                            mid=mid_obj,
                            end=end_obj,
                            move=10,
                            obj=left_knee_pvloc)

        left_knee_pvlocs.append(left_knee_pvloc)

    # Knee
    for i, (left_knee, left_knee_rot_ctrl) in enumerate(zip(left_knee_segments.seg_joints, buf_left_knee_rot_locs)):
        left_knee_loc = cmds.spaceLocator(n=left_knee+'_LOC')[0]
        cmds.matchTransform(left_knee_loc, left_knee)

        if i == len(left_knee_segments.seg_joints)-1:
            base_loc = buf_left_leg_rot_locs[1]
        else:
            base_loc = buf_left_knee_rot_locs[i+1]

        # Leg
        tkgAim.aim_nodes(base=base_loc, target=left_knee_rot_ctrl+'_OFFSET_GRP',
                         aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                         worldUpType='object', worldUpObject=left_knee_pvlocs[i])
        tkgAim.aim_nodes(base=base_loc, target=left_knee_rot_ctrl,
                         aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                         worldUpType='object', worldUpObject=left_knee_pvlocs[i])

        cmds.delete(left_knee_loc)

    cmds.delete(left_knee_pvlocs)

    # Thigh
    left_knee_pvloc = cmds.spaceLocator(n=left_knee_segments.seg_joints[0]+'_PV_LOC')[0]
    tkgAim.set_pole_vec(start=left_thigh_loc,
                        mid=left_knee_segments.seg_joints[0],
                        end=left_ankle,
                        move=10,
                        obj=left_knee_pvloc)

    tkgAim.aim_nodes(base=buf_left_knee_rot_locs[0], target=buf_left_leg_rot_locs[0]+'_OFFSET_GRP',
                     aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                     worldUpType='object', worldUpObject=left_knee_pvloc)
    tkgAim.aim_nodes(base=buf_left_knee_rot_locs[0], target=buf_left_leg_rot_locs[0],
                     aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                     worldUpType='object', worldUpObject=left_knee_pvloc)
    cmds.delete(left_knee_pvloc)

    # tkgAim.aim_nodes(base=left_ball_loc, target=buf_left_leg_rot_locs[1]+'_OFFSET_GRP',
    #                  aim_axis=leg_aim_axis, up_axis=leg_up_axis,
    #                  worldUpType='object', worldUpObject=left_knee_pvloc)
    # tkgAim.aim_nodes(base=left_ball_loc, target=buf_left_leg_rot_locs[1],
    #                  aim_axis=leg_aim_axis, up_axis=leg_up_axis,
    #                  worldUpType='object', worldUpObject=left_knee_pvloc)

    # Ball
    tkgAim.aim_nodes(base=left_ankle_loc, target=buf_left_leg_rot_locs[2]+'_OFFSET_GRP',
                     aim_axis=ball_aim_axis, up_axis=ball_up_axis,
                     worldUpType='object', worldSpace=True, world_axis='y')
    tkgAim.aim_nodes(base=left_ankle_loc, target=buf_left_leg_rot_locs[2],
                     aim_axis=ball_aim_axis, up_axis=ball_up_axis,
                     worldUpType='object', worldSpace=True, world_axis='y')

    cmds.delete(left_thigh_loc)
    cmds.delete(left_ankle_loc)
    cmds.delete(left_ball_loc)



set_arm_axis_pv_up(shoulder_aim_axis='x', shoulder_up_axis='-y',
            arm_aim_axis='x', arm_up_axis='z')


set_leg_axis_pv_up(leg_aim_axis='x', leg_up_axis='z',
            ball_aim_axis='-x', ball_up_axis='z')

# delete guides
# cnsts = [n for n in cmds.ls('root', dag=True) if 'Constraint' in n]
# [cmds.delete(cn) for cn in cnsts]
# grps = cmds.ls('*_GRP', assemblies=True)
# [cmds.delete(gp) for gp in grps]
