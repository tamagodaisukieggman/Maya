# -*- coding: utf-8 -*-
import maya.cmds as cmds

import datetime
from imp import reload
import os

import tkgRigBuild.libs.aim as tkgAim
import tkgRigBuild.libs.modifyJoints as tkgMJ
import tkgRigBuild.libs.control.ctrl as tkgCtrl
import tkgRigBuild.libs.common as tkgCommon
import tkgRigBuild.libs.maths as tkgMath
import tkgRigBuild.build.guides as tkgGuides
reload(tkgAim)
reload(tkgMJ)
reload(tkgCtrl)
reload(tkgCommon)
reload(tkgMath)
reload(tkgGuides)

GUIDE_PATH = os.path.dirname(tkgGuides.__file__.replace('\\', '/'))

"""
import maya.cmds as cmds
import maya.mel as mel

import tkgRigBuild.build.embedJoints as tkgEJ
reload(tkgEJ)

sel = cmds.ls(os=True)

embed = tkgEJ.EmbedJoints(mesh=sel[0],
                 root_count=1,
                 spine_count=3,
                 neck_count=1,
                 knee_count=1,
                 type='biped')

# embed.create_biped_joints()

embed.set_arm_axis_pv_up(shoulder_aim_axis='x', shoulder_up_axis='-y',
                     arm_aim_axis='x', arm_up_axis='z')

embed.set_leg_axis_pv_up(leg_aim_axis='x', leg_up_axis='z',
                ball_aim_axis='-x', ball_up_axis='z')
"""

class EmbedJoints:
    def __init__(self,
                 mesh=None,
                 root_count=1,
                 spine_count=3,
                 neck_count=1,
                 knee_count=1,
                 type=None,
                 create=None):

        self.mesh = mesh
        self.root_count = root_count
        self.spine_count = spine_count
        self.neck_count = neck_count
        self.knee_count = knee_count
        self.type = type
        self.create = create

        if self.create:
            if self.type == 'biped':
                self.create_biped_joints()

    def create_biped_joints(self):
        # First select the shape, not the transform.
        if not self.mesh:
            sel = cmds.ls(os=True)
            if sel:
                self.mesh = sel[0]
            else:
                return

        # GEO grp
        self.geo_grp = 'guide_geo_GRP'
        if not cmds.objExists(self.geo_grp):
            cmds.createNode('transform', n=self.geo_grp, ss=True)

        cmds.setAttr(self.geo_grp + '.overrideEnabled', 1)
        cmds.setAttr(self.geo_grp + '.overrideDisplayType', 2)

        cmds.parent(self.mesh, self.geo_grp)

        segments = tkgMJ.embed_biped_joints(self.mesh,
                                            self.root_count,
                                            self.spine_count,
                                            self.neck_count,
                                            self.knee_count)
        self.root_segments = segments[0]
        self.spine_segments = segments[1]
        self.neck_segments = segments[2]
        self.left_knee_segments = segments[3]
        self.right_knee_segments = segments[4]

        self.mirror = ['left_', 'right_']

        # Mirror Joints
        mirror_joints = self.simple_duplicate(root_jnt='root', prefix='mirror_')

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
            'head',
            'shoulder',
            'arm',
            'elbow',
            'hand',

            'thigh',
            'ankle',
            'ball'
        ]

        [side_pos_connect.append('_'.join(n.split('_')[1::])) for n in self.left_knee_segments.seg_joints]
        [side_pos_connect.append(n) for n in self.spine_segments.seg_joints]
        [side_pos_connect.append(n) for n in self.neck_segments.seg_joints]

        for part in side_pos_connect:
            if ('spine' in part
                or 'neck' in part
                or 'head' in part):
                cmds.connectAttr(part+'.t', 'mirror_'+part+'.t', f=True)
                cmds.connectAttr(part+'.r', 'mirror_'+part+'.r', f=True)

                # cmds.pointConstraint('mirror_'+part, part, w=True)
                # cmds.orientConstraint('mirror_'+part, part, w=True, mo=True)

            else:
                cmds.connectAttr(self.mirror[0]+part+'.t', 'mirror_'+self.mirror[0]+part+'.t', f=True)
                cmds.connectAttr(self.mirror[0]+part+'.r', 'mirror_'+self.mirror[0]+part+'.r', f=True)

                cmds.pointConstraint('mirror_'+self.mirror[0]+part, self.mirror[1]+part, w=True)
                cmds.orientConstraint('mirror_'+self.mirror[0]+part, self.mirror[1]+part, w=True, mo=True)

        # Controllers Const
        self.left_arms = cmds.ls('left_shoulder', dag=True, type='joint')
        self.left_legs = cmds.ls('left_thigh', dag=True, type='joint')

        self.left_arm_pos_grp, self.left_arm_rot_grp, self.left_arm_pos_locs, self.left_arm_rot_locs = self.create_pos_rot_locs(self.left_arms)
        self.left_leg_pos_grp, self.left_leg_rot_grp, self.left_leg_pos_locs, self.left_leg_rot_locs = self.create_pos_rot_locs(self.left_legs)

        self.spine_pos_grp, self.spine_rot_grp, self.spine_pos_locs, self.spine_rot_locs = self.create_pos_rot_locs(self.spine_segments.seg_joints)
        self.neck_pos_grp, self.neck_rot_grp, self.neck_pos_locs, self.neck_rot_locs = self.create_pos_rot_locs(self.neck_segments.seg_joints)
        self.head_pos_grp, self.head_rot_grp, self.head_pos_locs, self.head_rot_locs = self.create_pos_rot_locs(['head'])

        cmds.parent('left_hand_POS_LOC_GRP', 'left_arm_POS_LOC')
        # cmds.parent('left_knee_POS_LOC_GRP', 'left_thigh_POS_LOC')
        cmds.parent('left_ankle_POS_LOC_GRP', 'left_thigh_POS_LOC')
        cmds.parent('left_ball_POS_LOC_GRP', 'left_thigh_POS_LOC')

        # # Aim
        left_arm_aim_loc = self.left_arm_pos_locs[0]+'_AIM'
        cmds.spaceLocator(n=left_arm_aim_loc)
        aim_loc_grp = self.create_offset_grp(left_arm_aim_loc)
        cmds.matchTransform(aim_loc_grp, self.left_arm_pos_locs[-1])
        cmds.aimConstraint(
            left_arm_aim_loc,
            self.left_arm_pos_locs[1]+'_OFFSET_GRP',
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
        self.add_scale_tweak_attr(grp=self.left_arm_pos_grp,
                             pos_ctrls=self.left_arm_pos_locs,
                             rot_ctrls=self.left_arm_rot_locs)

        # leg
        self.add_scale_tweak_attr(grp=self.left_leg_pos_grp,
                             pos_ctrls=self.left_leg_pos_locs,
                             rot_ctrls=self.left_leg_rot_locs)

        # Spine
        self.add_scale_tweak_attr(grp=self.spine_pos_grp,
                             pos_ctrls=self.spine_pos_locs,
                             rot_ctrls=self.spine_rot_locs)

        # Neck
        self.add_scale_tweak_attr(grp=self.neck_pos_grp,
                             pos_ctrls=self.neck_pos_locs,
                             rot_ctrls=self.neck_rot_locs)

        # Head
        self.add_scale_tweak_attr(grp=self.head_pos_grp,
                             pos_ctrls=self.head_pos_locs,
                             rot_ctrls=self.head_rot_locs)

        # Foot Roll Pivs
        self.foot_roll_piv_locs = []
        for ball, ankle in zip(['left_ball', 'right_ball'], ['left_ankle', 'right_ankle']):
            locs = self.create_foot_roll_pivots(ball=ball, ankle=ankle)
            [self.foot_roll_piv_locs.append(loc) for loc in locs]

        self.foot_roll_piv_grp = 'foot_roll_piv_GRP'
        cmds.createNode('transform', n=self.foot_roll_piv_grp, ss=True)
        [cmds.parent(loc, self.foot_roll_piv_grp) for loc in self.foot_roll_piv_locs]
        self.simple_set_overrideColorRGB(obj=self.foot_roll_piv_grp, color=[0, 1, 1])

        self.mirror_foot_piv = self.simple_duplicate(root_jnt=self.foot_roll_piv_grp, prefix='mirror_', type='transform')
        cmds.parent(self.mirror_foot_piv[0], self.foot_roll_piv_grp)
        cmds.setAttr(self.mirror_foot_piv[0]+'.sx', -1)
        cmds.setAttr(self.mirror_foot_piv[0]+'.v', 0)

        side_pos_connect = [
            'toe_piv_loc',
            'heel_piv_loc',
            'in_piv_loc',
            'out_piv_loc'
        ]
        for part in side_pos_connect:
            cmds.connectAttr(self.mirror[0]+part+'.t', 'mirror_'+self.mirror[0]+part+'.t', f=True)
            cmds.connectAttr(self.mirror[0]+part+'.r', 'mirror_'+self.mirror[0]+part+'.r', f=True)

            cmds.pointConstraint('mirror_'+self.mirror[0]+part, self.mirror[1]+part, w=True)
            cmds.orientConstraint('mirror_'+self.mirror[0]+part, self.mirror[1]+part, w=True, mo=True)

        # Adjustment Grp
        self.adjustment_grp = 'adjustment_GRP'
        cmds.createNode('transform', n=self.adjustment_grp, ss=True)
        cmds.parent(mirror_grp, self.adjustment_grp)
        cmds.parent(aim_loc_grp, self.adjustment_grp)
        # cmds.parent(self.foot_roll_piv_grp, self.adjustment_grp)
        self.simple_set_overrideColorRGB(obj=self.adjustment_grp, color=[1, 1, 0])

        self.add_all_scale_tweak_attr(self.adjustment_grp, self.left_arm_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.left_leg_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.spine_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.neck_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.head_pos_grp)

        self.create_finger_guides()
        print('self.finger_tip', self.finger_tip)

    def create_finger_guides(self):
        self.finger_tip = tkgCommon.get_finger_tip(mesh=self.mesh)

    def add_all_scale_tweak_attr(self, all_grp=None, grp=None):
        if ('spine' in grp
            or 'neck' in grp
            or 'head' in grp):
            part = grp.split('_')[0]
        else:
            part = grp.split('_')[1]
        part_dict = {
            'shoulder':'arm',
            'thigh':'leg',
            'spine':'spine',
            'neck':'neck',
            'head':'head'
        }
        pos_scale_at = '{}PosLocsScale'.format(part_dict[part])
        rot_scale_at = '{}RotLocsScale'.format(part_dict[part])
        if not cmds.objExists(all_grp + '.' + pos_scale_at):
            cmds.addAttr(all_grp, ln=pos_scale_at, at='double', dv=1, k=True)
        if not cmds.objExists(all_grp + '.' + rot_scale_at):
            cmds.addAttr(all_grp, ln=rot_scale_at, at='double', dv=1, k=True)

        cmds.connectAttr(all_grp + '.' + pos_scale_at, grp+'.posLocsScale', f=True)
        cmds.connectAttr(all_grp + '.' + rot_scale_at, grp+'.rotLocsScale', f=True)

        cmds.parent(grp, all_grp)

    def add_scale_tweak_attr(self, grp=None, pos_ctrls=None, rot_ctrls=None):
        cmds.addAttr(grp, ln='posLocsScale', at='double', dv=1, k=True)
        cmds.addAttr(grp, ln='rotLocsScale', at='double', dv=1, k=True)

        for lapl, larl in zip(pos_ctrls, rot_ctrls):
            cmds.connectAttr(grp+'.posLocsScale', lapl+'.localScaleX', f=True)
            cmds.connectAttr(grp+'.posLocsScale', lapl+'.localScaleY', f=True)
            cmds.connectAttr(grp+'.posLocsScale', lapl+'.localScaleZ', f=True)

            cmds.connectAttr(grp+'.rotLocsScale', larl+'.sx', f=True)
            cmds.connectAttr(grp+'.rotLocsScale', larl+'.sy', f=True)
            cmds.connectAttr(grp+'.rotLocsScale', larl+'.sz', f=True)

    def simple_set_overrideColorRGB(self, obj=None, color=[1, 1, 0]):
        cmds.setAttr(obj + '.overrideEnabled', True)
        cmds.setAttr(obj + '.overrideRGBColors', 1)
        cmds.setAttr(obj + '.overrideColorRGB', *color)

    def simple_duplicate(self, root_jnt='root', prefix='mirror_', type='joint'):
        dup_joints = []
        base_joints = cmds.ls(root_jnt, dag=True, type=type)
        for jnt in base_joints:
            new_name = prefix+jnt
            dup_joints.append(new_name)
            dup = cmds.duplicate(jnt, po=True, n=new_name)
            pa = cmds.listRelatives(jnt, p=True) or None
            if pa:
                parent_name = prefix+pa[0]
                if cmds.objExists(parent_name):
                    cmds.parent(new_name, parent_name)

        return dup_joints

    #--------------------------
    # Adjusting Axis
    #--------------------------
    def set_arm_axis_pv_up(self, shoulder_aim_axis='x', shoulder_up_axis='-y',
                     arm_aim_axis='x', arm_up_axis='z'):
        left_shoulder = self.left_arms[0]
        left_arm = self.left_arms[1]
        left_elbow = self.left_arms[2]
        left_hand = self.left_arms[3]

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
        tkgAim.aim_nodes(base=left_arm_loc, target=self.left_arm_rot_locs[0]+'_OFFSET_GRP',
                         aim_axis=shoulder_aim_axis, up_axis=shoulder_up_axis,
                         worldUpType='scene')
        tkgAim.aim_nodes(base=left_arm_loc, target=self.left_arm_rot_locs[0],
                         aim_axis=shoulder_aim_axis, up_axis=shoulder_up_axis,
                         worldUpType='scene')

        # Arm
        tkgAim.aim_nodes(base=left_elbow_loc, target=self.left_arm_rot_locs[1]+'_OFFSET_GRP',
                         aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                         worldUpType='object', worldUpObject=left_elbow_pvloc)
        tkgAim.aim_nodes(base=left_elbow_loc, target=self.left_arm_rot_locs[1],
                         aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                         worldUpType='object', worldUpObject=left_elbow_pvloc)

        tkgAim.aim_nodes(base=left_hand_loc, target=self.left_arm_rot_locs[2]+'_OFFSET_GRP',
                         aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                         worldUpType='object', worldUpObject=left_elbow_pvloc)
        tkgAim.aim_nodes(base=left_hand_loc, target=self.left_arm_rot_locs[2],
                         aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                         worldUpType='object', worldUpObject=left_elbow_pvloc)

        cmds.delete(left_shoulder_loc)
        cmds.delete(left_arm_loc)
        cmds.delete(left_elbow_loc)
        cmds.delete(left_hand_loc)
        cmds.delete(left_elbow_pvloc)


    def set_leg_axis_pv_up(self, leg_aim_axis='x', leg_up_axis='z',
                ball_aim_axis='-x', ball_up_axis='z'):

        buf_self_left_legs = [n for n in self.left_legs]
        buf_self_left_leg_rot_locs = [n for n in self.left_leg_rot_locs]
        buf_left_knee_rot_locs = [n for n in self.left_leg_rot_locs
                                    if 'knee' in '_'.join(n.split('_')[:2:])]

        [buf_self_left_legs.remove(n) for n in self.left_knee_segments.seg_joints]
        [buf_self_left_leg_rot_locs.remove(n)
            for n in self.left_leg_rot_locs if not '_'.join(n.split('_')[:2:]) in self.left_legs]

        left_thigh = buf_self_left_legs[0]
        left_ankle = buf_self_left_legs[1]
        left_ball = buf_self_left_legs[2]

        left_thigh_loc = cmds.spaceLocator(n=left_thigh+'_LOC')[0]
        left_ankle_loc = cmds.spaceLocator(n=left_ankle+'_LOC')[0]
        left_ball_loc = cmds.spaceLocator(n=left_ball+'_LOC')[0]

        cmds.matchTransform(left_thigh_loc, left_thigh)
        cmds.matchTransform(left_ankle_loc, left_ankle)
        cmds.matchTransform(left_ball_loc, left_ball)

        if 1 < len(buf_left_knee_rot_locs):
            # Ball Rot Loc
            left_ball_rot_loc = buf_self_left_leg_rot_locs[2]

            # Knee PV obj
            left_knee_pvlocs = []
            for i, leg_obj in enumerate(self.left_legs):
                # i == 0
                if i+2 == len(self.left_legs)-1:
                    break
                start_obj = leg_obj
                mid_obj = self.left_legs[i+1]
                end_obj = self.left_legs[i+2]
                left_knee_pvloc = cmds.spaceLocator(n=leg_obj+'_PV_LOC')[0]
                tkgAim.set_pole_vec(start=start_obj,
                                    mid=mid_obj,
                                    end=end_obj,
                                    move=10,
                                    obj=left_knee_pvloc)

                left_knee_pvlocs.append(left_knee_pvloc)

            # Knee
            for i, (left_knee, left_knee_rot_ctrl) in enumerate(zip(self.left_knee_segments.seg_joints, buf_left_knee_rot_locs)):
                left_knee_loc = cmds.spaceLocator(n=left_knee+'_LOC')[0]
                cmds.matchTransform(left_knee_loc, left_knee)

                if i == len(self.left_knee_segments.seg_joints)-1:
                    base_loc = buf_self_left_leg_rot_locs[1]
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

            if left_knee_pvlocs:
                cmds.delete(left_knee_pvlocs)

            # Ankle
            left_knee = self.left_legs[1]
            left_ankle_rot_ctrl = buf_self_left_leg_rot_locs[1]
            left_knee_pvloc = cmds.spaceLocator(n=left_knee+'_PV_LOC')[0]
            tkgAim.set_pole_vec(start=left_thigh,
                                mid=left_knee,
                                end=left_ankle,
                                move=10,
                                obj=left_knee_pvloc)

            tkgAim.aim_nodes(base=left_ball_loc, target=left_ankle_rot_ctrl+'_OFFSET_GRP',
                             aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc)
            tkgAim.aim_nodes(base=left_ball_loc, target=left_ankle_rot_ctrl,
                             aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc)

            cmds.delete(left_knee_pvloc)

        else:
            # Ball Rot Loc
            left_ball_rot_loc = self.left_leg_rot_locs[3]

            left_knee = self.left_legs[1]
            left_knee_rot_ctrl = self.left_leg_rot_locs[1]
            left_ankle_rot_ctrl = self.left_leg_rot_locs[2]
            left_knee_pvloc = cmds.spaceLocator(n=left_knee+'_PV_LOC')[0]
            tkgAim.set_pole_vec(start=left_thigh,
                                mid=left_knee,
                                end=left_ankle,
                                move=10,
                                obj=left_knee_pvloc)

            # Leg
            tkgAim.aim_nodes(base=left_ankle_loc, target=left_knee_rot_ctrl+'_OFFSET_GRP',
                             aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc)
            tkgAim.aim_nodes(base=left_ankle_loc, target=left_knee_rot_ctrl,
                             aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc)

            # Ankle
            tkgAim.aim_nodes(base=left_ball_loc, target=left_ankle_rot_ctrl+'_OFFSET_GRP',
                             aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc)
            tkgAim.aim_nodes(base=left_ball_loc, target=left_ankle_rot_ctrl,
                             aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc)

            cmds.delete(left_knee_pvloc)

        # Thigh
        left_knee_pvloc = cmds.spaceLocator(n=self.left_knee_segments.top+'_PV_LOC')[0]
        tkgAim.set_pole_vec(start=left_thigh_loc,
                            mid=self.left_knee_segments.top,
                            end=left_ankle,
                            move=10,
                            obj=left_knee_pvloc)

        tkgAim.aim_nodes(base=buf_left_knee_rot_locs[0], target=buf_self_left_leg_rot_locs[0]+'_OFFSET_GRP',
                         aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                         worldUpType='object', worldUpObject=left_knee_pvloc)
        tkgAim.aim_nodes(base=buf_left_knee_rot_locs[0], target=buf_self_left_leg_rot_locs[0],
                         aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                         worldUpType='object', worldUpObject=left_knee_pvloc)
        cmds.delete(left_knee_pvloc)

        # tkgAim.aim_nodes(base=left_ball_loc, target=buf_self_left_leg_rot_locs[1]+'_OFFSET_GRP',
        #                  aim_axis=leg_aim_axis, up_axis=leg_up_axis,
        #                  worldUpType='object', worldUpObject=left_knee_pvloc)
        # tkgAim.aim_nodes(base=left_ball_loc, target=buf_self_left_leg_rot_locs[1],
        #                  aim_axis=leg_aim_axis, up_axis=leg_up_axis,
        #                  worldUpType='object', worldUpObject=left_knee_pvloc)

        # Ball
        tkgAim.aim_nodes(base=left_ankle_loc, target=left_ball_rot_loc+'_OFFSET_GRP',
                         aim_axis=ball_aim_axis, up_axis=ball_up_axis,
                         worldUpType='object', worldSpace=True, world_axis='y')
        tkgAim.aim_nodes(base=left_ankle_loc, target=left_ball_rot_loc,
                         aim_axis=ball_aim_axis, up_axis=ball_up_axis,
                         worldUpType='object', worldSpace=True, world_axis='y')

        cmds.delete(left_thigh_loc)
        cmds.delete(left_ankle_loc)
        cmds.delete(left_ball_loc)

    def delete_adjust_rig(self):
        # Temp Save
        cmds.viewFit()
        now = datetime.datetime.now()
        file_name = now.strftime("guide_%Y%m%d%H%M.ma")
        cmds.file(rn=GUIDE_PATH + '/' + file_name)
        cmds.file(s=True, f=True)

        # delete guides
        cnsts = [n for n in cmds.ls('root', dag=True) if 'Constraint' in n]
        [cmds.delete(cn) for cn in cnsts]
        cmds.delete('adjustment_GRP')

        # delete guides
        cnsts = [n for n in cmds.ls('foot_roll_piv_GRP', dag=True) if 'Constraint' in n]
        [cmds.delete(cn) for cn in cnsts]
        cmds.delete('mirror_foot_roll_piv_GRP')

    def publish_adjust_joints(self):
        self.delete_adjust_rig()

        cmds.viewFit()
        now = datetime.datetime.now()
        file_name = now.strftime("adjust_joints_%Y%m%d%H%M.ma")
        cmds.file(rn=GUIDE_PATH + '/' + file_name)

        mesh = cmds.listRelatives('guide_geo_GRP')[0]
        cmds.parent(mesh, w=True)
        cmds.delete('guide_geo_GRP')

        foot_roll_piv_locs = cmds.listRelatives('foot_roll_piv_GRP')
        [cmds.parent(n, w=True) for n in foot_roll_piv_locs]
        cmds.delete('foot_roll_piv_GRP')

        cmds.file(s=True, f=True)

    def create_offset_grp(self, obj=None):
        obj_grp = cmds.createNode('transform', n=obj+'_GRP', ss=True)
        obj_oft_grp = cmds.createNode('transform', n=obj+'_OFFSET_GRP', ss=True)
        obj_sdk_grp = cmds.createNode('transform', n=obj+'_SDK_GRP', ss=True)

        cmds.parent(obj, obj_sdk_grp)
        cmds.parent(obj_sdk_grp, obj_oft_grp)
        cmds.parent(obj_oft_grp, obj_grp)
        return obj_grp

    def create_pos_rot_locs(self, objects=None):
        pos_locs = []
        rot_locs = []
        first_pos_grp = None
        first_rot_grp = None
        pa = None
        for i, obj in enumerate(objects):
            pos_loc = obj+'_POS_LOC'
            cmds.spaceLocator(n=pos_loc)
            cmds.setAttr(pos_loc+'Shape.localPositionX', 2)
            cmds.setAttr(pos_loc+'Shape.localPositionY', 2)
            cmds.setAttr(pos_loc+'Shape.localPositionZ', 2)
            pos_locs.append(pos_loc)
            pos_grp = self.create_offset_grp(obj=pos_loc)
            if i == 0:
                first_pos_grp = pos_grp
            cmds.matchTransform(pos_grp, obj)

            rot_loc = obj+'_ROT_LOC'
            tkgCtrl.create_manip_ctrl(rot_loc)
            rot_locs.append(rot_loc)
            rot_grp = self.create_offset_grp(obj=rot_loc)
            if i == 0:
                first_rot_grp = rot_grp
            cmds.matchTransform(rot_grp, obj)

            cmds.parent(rot_grp, pos_loc)

            cmds.pointConstraint(rot_loc, obj, w=True)
            cmds.orientConstraint(rot_loc, obj, w=True)

            if pa:
                cmds.parent(pos_grp, pa)

            pa = pos_loc

        return first_pos_grp, first_rot_grp, pos_locs, rot_locs

    def create_foot_roll_pivots(self, ball=None, ankle=None):
        if 'left_' in ball and 'left_' in ankle:
            in_axis = '-x'
            out_axis = 'x'
            prefix = 'left_'
        elif 'right_' in ball and 'right_' in ankle:
            in_axis = 'x'
            out_axis = '-x'
            prefix = 'right_'

        toe_point = cmds.xform(ball, q=True, t=True, ws=True)
        toe_hit_point = tkgCommon.closest_hit_point_on_mesh(point=toe_point, mesh=self.mesh, axis='z')
        toe_loc = cmds.spaceLocator(n=prefix+'toe_piv_loc')[0]
        cmds.xform(toe_loc, t=[toe_hit_point[0],
                               0,
                               toe_hit_point[2]])

        heel_point = cmds.xform(ankle, q=True, t=True, ws=True)
        heel_hit_point = tkgCommon.closest_hit_point_on_mesh(point=heel_point, mesh=self.mesh, axis='-z')
        heel_loc = cmds.spaceLocator(n=prefix+'heel_piv_loc')[0]
        cmds.xform(heel_loc, t=[heel_hit_point[0],
                               0,
                               heel_hit_point[2]])

        toe_heel_mid_point = tkgCommon.get_mid_point(toe_point, heel_point)
        in_hit_point = tkgCommon.closest_hit_point_on_mesh(point=toe_heel_mid_point, mesh=self.mesh, axis=in_axis)
        in_loc = cmds.spaceLocator(n=prefix+'in_piv_loc')[0]
        cmds.xform(in_loc, t=[in_hit_point[0],
                               0,
                               in_hit_point[2]])

        out_hit_point = tkgCommon.closest_hit_point_on_mesh(point=toe_heel_mid_point, mesh=self.mesh, axis=out_axis)
        out_loc = cmds.spaceLocator(n=prefix+'out_piv_loc')[0]
        cmds.xform(out_loc, t=[out_hit_point[0],
                               0,
                               out_hit_point[2]])

        return [loc for loc in [toe_loc, heel_loc, in_loc, out_loc]]
