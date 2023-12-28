# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel

from collections import OrderedDict
import datetime
from imp import reload
import os
import traceback

import buildRig.common as brCommon
import buildRig.node as brNode
import buildRig.aim as brAim
import buildRig.modifyJoints as brMJ
import buildRig.libs.control.draw as brDraw
import buildRig.lock as brLock
reload(brCommon)
reload(brNode)
reload(brAim)
reload(brMJ)
reload(brDraw)
reload(brLock)

GUIDE_PATH = os.path.dirname(__file__.replace('\\', '/')) + '/guides'
if not os.path.isdir(GUIDE_PATH):
    os.makedirs(GUIDE_PATH)

"""
import maya.cmds as cmds
import maya.mel as mel
import traceback

try:
    import buildRig.embedJoints as brEJ
    reload(brEJ)
except:
    print(traceback.format_exc())

sel = cmds.ls(os=True)

embed = brEJ.EmbedJoints(mesh=sel[0],
                 root_count=1,
                 spine_count=3,
                 neck_count=1,
                 knee_count=1,
                 type='biped',
                 create=True,
                 guide_name='HumanBody')

embed.set_arm_axis_pv_up(shoulder_aim_axis='x',
                         shoulder_up_axis='-y',
                         shoulder_worldSpace=False,
                         shoulder_world_axis='y',
                         arm_aim_axis='x',
                         arm_up_axis='z',
                         arm_worldSpace=False,
                         arm_world_axis='y')

embed.set_leg_axis_pv_up(leg_aim_axis='x',
                         leg_up_axis='z',
                         leg_worldSpace=False,
                         leg_world_axis='y',
                         ball_aim_axis='-x',
                         ball_up_axis='z',
                         ball_worldSpace=False,
                         ball_world_axis='y',
                         thigh_aim_axis='x',
                         thigh_up_axis='z',
                         thigh_worldSpace=False,
                         thigh_world_axis='y',
                         ankle_aim_axis='x',
                         ankle_up_axis='z',
                         ankle_worldSpace=False,
                         ankle_world_axis='y')

embed.set_spine_axis_pv_up(spine_aim_axis='y',
                           spine_up_axis='z',
                           offset_aim_rotate=0)

embed.set_thumb_axis_pv_up('x', 'y')
embed.set_index_axis_pv_up('x', 'x')
embed.set_middle_axis_pv_up('x', 'x')
embed.set_ring_axis_pv_up('x', 'x')
embed.set_pinky_axis_pv_up('x', 'x')

embed.publish_adjust_joints()

embed.set_world_aim(obj=None, wld_front_axis='z', wld_left_axis='x')

# select 2 verts and locator
import buildRig.common as brCommon
reload(brCommon)
sel = cmds.ls(os=True, fl=True)
mid_pos = brCommon.set_mid_point(*sel, 0.5)


"""

AXIS_DICT = {
    'x':[1,0,0],
    'y':[0,1,0],
    'z':[0,0,1],
    '-x':[-1,0,0],
    '-y':[0,-1,0],
    '-z':[0,0,-1]
}


class EmbedJoints:
    def __init__(self,
                 mesh=None,
                 root_count=1,
                 spine_count=3,
                 neck_count=1,
                 knee_count=1,
                 thumb_count=3,
                 index_count=3,
                 middle_count=3,
                 ring_count=3,
                 pinky_count=3,
                 type=None,
                 create=None,
                 guide_name=None,
                 set_from_current=None):

        self.mesh = mesh
        self.root_count = root_count
        self.spine_count = spine_count
        self.neck_count = neck_count
        self.knee_count = knee_count
        self.thumb_count = thumb_count
        self.index_count = index_count
        self.middle_count = middle_count
        self.ring_count = ring_count
        self.pinky_count = pinky_count
        self.type = type
        self.create = create
        self.guide_name = guide_name
        self.set_from_current = set_from_current

        self.set_json_file()

        self.guide_cur_adj_json = GUIDE_PATH + '/current_adjustment.json'
        self.guide_cur_footroll_json = GUIDE_PATH + '/current_footroll.json'

        if self.create:
            if self.type == 'biped':
                self.create_biped_joints()
                self.set_adjustment_nodes_values(type='adjustment')
                self.set_adjustment_nodes_values(type='footroll')
                self.match_all_pos_to_rot_locs()
                self.create_all_ctrl()

    def set_json_file(self):
        if self.guide_name:
            self.guide_name_adj_json = GUIDE_PATH + '/{}_adjustment.json'.format(self.guide_name)
            self.guide_name_footroll_json = GUIDE_PATH + '/{}_footroll.json'.format(self.guide_name)
        else:
            self.set_json_file_from_mesh()

    def set_json_file_from_mesh(self):
        self.guide_name_adj_json = GUIDE_PATH + '/{}_adjustment.json'.format(self.mesh)
        self.guide_name_footroll_json = GUIDE_PATH + '/{}_footroll.json'.format(self.mesh)

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

        segments = brMJ.embed_biped_joints(self.mesh,
                                            self.root_count,
                                            self.spine_count,
                                            self.neck_count,
                                            self.knee_count,
                                            self.thumb_count,
                                            self.index_count,
                                            self.middle_count,
                                            self.ring_count,
                                            self.pinky_count)
        self.root_segments = segments[0]
        self.spine_segments = segments[1]
        self.neck_segments = segments[2]
        self.left_knee_segments = segments[3]
        self.right_knee_segments = segments[4]

        # Mirror Joints
        self.mirror = ['left_', 'right_']

        mirror_joints = self.simple_duplicate(root_jnt='root', prefix='mirror_')

        mirror_grp = cmds.createNode('transform', n='mirror_joints_GRP', ss=True)
        cmds.parent('mirror_root', mirror_grp)
        cmds.setAttr(mirror_grp+'.sx', -1)
        cmds.setAttr(mirror_grp+'.v', 0)

        # left to right connection
        # cmds.pointConstraint('hips', 'mirror_hips', w=True)
        # cmds.orientConstraint('hips', 'mirror_hips', w=True, mo=True)

        # cmds.pointConstraint('spine_03', 'mirror_spine_03', w=True)
        # cmds.orientConstraint('spine_03', 'mirror_spine_03', w=True, mo=True)

        side_pos_connect = [
            'head',
            'shoulder',
            'arm',
            'elbow',
            'hand',
            'hips',

            'thigh',
            'ankle',
            'ball'
        ]

        [side_pos_connect.append('_'.join(n.split('_')[1::])) for n in self.left_knee_segments.seg_joints]
        [side_pos_connect.append(n) for n in self.spine_segments.seg_joints]
        [side_pos_connect.append(n) for n in self.neck_segments.seg_joints]

        # Body Mirror Connect
        for part in side_pos_connect:
            if ('spine' in part
                or 'neck' in part
                or 'head' in part
                or 'hips' in part):
                cmds.connectAttr(part+'.t', 'mirror_'+part+'.t', f=True)
                cmds.connectAttr(part+'.r', 'mirror_'+part+'.r', f=True)

                # cmds.pointConstraint(part, 'mirror_'+part, w=True)
                # cmds.orientConstraint(part, 'mirror_'+part, w=True, mo=True)

                pass

            else:
                cmds.connectAttr(self.mirror[0]+part+'.t', 'mirror_'+self.mirror[0]+part+'.t', f=True)
                cmds.connectAttr(self.mirror[0]+part+'.r', 'mirror_'+self.mirror[0]+part+'.r', f=True)

                cmds.pointConstraint('mirror_'+self.mirror[0]+part, self.mirror[1]+part, w=True)
                cmds.orientConstraint('mirror_'+self.mirror[0]+part, self.mirror[1]+part, w=True, mo=True)

        self.base_joints_dict = OrderedDict({})
        # Controllers Const
        self.left_arms = cmds.ls('left_shoulder', dag=True, type='joint')
        self.left_legs = cmds.ls('left_thigh', dag=True, type='joint')
        self.base_joints_dict['arm'] = self.left_arms
        self.base_joints_dict['leg'] = self.left_legs

        self.left_knee_joints = self.left_knee_segments.seg_joints
        self.base_joints_dict['knee'] = self.left_knee_joints
        self.left_knee_segments_top = self.left_knee_segments.top
        self.base_joints_dict['kneeTop'] = self.left_knee_segments_top

        ## Fingers
        self.left_thumb = cmds.ls('left_thumb_01', dag=True, type='joint')
        self.left_index = cmds.ls('left_index_01', dag=True, type='joint')
        self.left_middle = cmds.ls('left_middle_01', dag=True, type='joint')
        self.left_ring = cmds.ls('left_ring_01', dag=True, type='joint')
        self.left_pinky = cmds.ls('left_pinky_01', dag=True, type='joint')
        self.fingers = []
        [self.fingers.append(n) for n in self.left_thumb]
        [self.fingers.append(n) for n in self.left_index]
        [self.fingers.append(n) for n in self.left_middle]
        [self.fingers.append(n) for n in self.left_ring]
        [self.fingers.append(n) for n in self.left_pinky]
        [self.left_arms.remove(n) for n in self.fingers]

        # Fingers Mirror Connect
        for fing in self.fingers:
            cmds.connectAttr(fing+'.t', 'mirror_'+fing+'.t', f=True)
            cmds.connectAttr(fing+'.r', 'mirror_'+fing+'.r', f=True)

            cmds.pointConstraint('mirror_'+fing, fing.replace(self.mirror[0], self.mirror[1]), w=True)
            cmds.orientConstraint('mirror_'+fing, fing.replace(self.mirror[0], self.mirror[1]), w=True, mo=True)


        self.pos_rot_ctrls_dict = OrderedDict({})
        # arm
        self.left_arm_pos_grp, self.left_arm_rot_grp, self.left_arm_pos_locs, self.left_arm_rot_locs = self.create_pos_rot_locs(self.left_arms)
        self.pos_rot_ctrls_dict['arm'] = self.left_arm_pos_grp, self.left_arm_rot_grp, self.left_arm_pos_locs, self.left_arm_rot_locs

        # fingers
        self.left_thumb_pos_grp, self.left_thumb_rot_grp, self.left_thumb_pos_locs, self.left_thumb_rot_locs = self.create_pos_rot_locs(self.left_thumb)
        self.left_index_pos_grp, self.left_index_rot_grp, self.left_index_pos_locs, self.left_index_rot_locs = self.create_pos_rot_locs(self.left_index)
        self.left_middle_pos_grp, self.left_middle_rot_grp, self.left_middle_pos_locs, self.left_middle_rot_locs = self.create_pos_rot_locs(self.left_middle)
        self.left_ring_pos_grp, self.left_ring_rot_grp, self.left_ring_pos_locs, self.left_ring_rot_locs = self.create_pos_rot_locs(self.left_ring)
        self.left_pinky_pos_grp, self.left_pinky_rot_grp, self.left_pinky_pos_locs, self.left_pinky_rot_locs = self.create_pos_rot_locs(self.left_pinky)
        self.pos_rot_ctrls_dict['thumb'] = self.left_thumb_pos_grp, self.left_thumb_rot_grp, self.left_thumb_pos_locs, self.left_thumb_rot_locs
        self.pos_rot_ctrls_dict['index'] = self.left_index_pos_grp, self.left_index_rot_grp, self.left_index_pos_locs, self.left_index_rot_locs
        self.pos_rot_ctrls_dict['middle'] = self.left_middle_pos_grp, self.left_middle_rot_grp, self.left_middle_pos_locs, self.left_middle_rot_locs
        self.pos_rot_ctrls_dict['ring'] = self.left_ring_pos_grp, self.left_ring_rot_grp, self.left_ring_pos_locs, self.left_ring_rot_locs
        self.pos_rot_ctrls_dict['pinky'] = self.left_pinky_pos_grp, self.left_pinky_rot_grp, self.left_pinky_pos_locs, self.left_pinky_rot_locs

        # leg
        self.left_leg_pos_grp, self.left_leg_rot_grp, self.left_leg_pos_locs, self.left_leg_rot_locs = self.create_pos_rot_locs(self.left_legs)
        self.pos_rot_ctrls_dict['leg'] = self.left_leg_pos_grp, self.left_leg_rot_grp, self.left_leg_pos_locs, self.left_leg_rot_locs

        # spines
        self.spine_pos_grp, self.spine_rot_grp, self.spine_pos_locs, self.spine_rot_locs = self.create_pos_rot_locs(self.spine_segments.seg_joints)
        self.neck_pos_grp, self.neck_rot_grp, self.neck_pos_locs, self.neck_rot_locs = self.create_pos_rot_locs(self.neck_segments.seg_joints)
        self.head_pos_grp, self.head_rot_grp, self.head_pos_locs, self.head_rot_locs = self.create_pos_rot_locs(['head'])
        self.hips_pos_grp, self.hips_rot_grp, self.hips_pos_locs, self.hips_rot_locs = self.create_pos_rot_locs(['hips'])
        self.pos_rot_ctrls_dict['spine'] = self.spine_pos_grp, self.spine_rot_grp, self.spine_pos_locs, self.spine_rot_locs
        self.pos_rot_ctrls_dict['neck'] = self.neck_pos_grp, self.neck_rot_grp, self.neck_pos_locs, self.neck_rot_locs
        self.pos_rot_ctrls_dict['head'] = self.head_pos_grp, self.head_rot_grp, self.head_pos_locs, self.head_rot_locs
        self.pos_rot_ctrls_dict['hips'] = self.hips_pos_grp, self.hips_rot_grp, self.hips_pos_locs, self.hips_rot_locs

        # Parent Body
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

        # fingers
        # thumb
        self.add_scale_tweak_attr(grp=self.left_thumb_pos_grp,
                             pos_ctrls=self.left_thumb_pos_locs,
                             rot_ctrls=self.left_thumb_rot_locs)

        # index
        self.add_scale_tweak_attr(grp=self.left_index_pos_grp,
                             pos_ctrls=self.left_index_pos_locs,
                             rot_ctrls=self.left_index_rot_locs)

        # middle
        self.add_scale_tweak_attr(grp=self.left_middle_pos_grp,
                             pos_ctrls=self.left_middle_pos_locs,
                             rot_ctrls=self.left_middle_rot_locs)

        # ring
        self.add_scale_tweak_attr(grp=self.left_ring_pos_grp,
                             pos_ctrls=self.left_ring_pos_locs,
                             rot_ctrls=self.left_ring_rot_locs)

        # pinky
        self.add_scale_tweak_attr(grp=self.left_pinky_pos_grp,
                             pos_ctrls=self.left_pinky_pos_locs,
                             rot_ctrls=self.left_pinky_rot_locs)


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

        # Hips
        self.add_scale_tweak_attr(grp=self.hips_pos_grp,
                             pos_ctrls=self.hips_pos_locs,
                             rot_ctrls=self.hips_rot_locs)

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

        # Body
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.left_arm_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.left_leg_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.spine_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.neck_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.head_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.hips_pos_grp)

        # Fingers
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.left_thumb_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.left_index_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.left_middle_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.left_ring_pos_grp)
        self.add_all_scale_tweak_attr(self.adjustment_grp, self.left_pinky_pos_grp)

        # Parent Fingers
        cmds.parent('left_thumb_01_POS_LOC_GRP', 'left_hand_POS_LOC')
        cmds.parent('left_index_01_POS_LOC_GRP', 'left_hand_POS_LOC')
        cmds.parent('left_middle_01_POS_LOC_GRP', 'left_hand_POS_LOC')
        cmds.parent('left_ring_01_POS_LOC_GRP', 'left_hand_POS_LOC')
        cmds.parent('left_pinky_01_POS_LOC_GRP', 'left_hand_POS_LOC')

        cmds.select(self.mesh, r=True)
        mel.eval('fitPanel -selectedNoChildren;')

        self.lock_guide_locators()

    def add_all_scale_tweak_attr(self, all_grp=None, grp=None):
        if ('spine' in grp
            or 'neck' in grp
            or 'head' in grp
            or 'hips' in grp):
            part = grp.split('_')[0]
        else:
            part = grp.split('_')[1]
        part_dict = {
            'shoulder':'arm',
            'thigh':'leg',
            'spine':'spine',
            'neck':'neck',
            'head':'head',
            'hips':'hips',

            'thumb':'thumb',
            'index':'index',
            'middle':'middle',
            'ring':'ring',
            'pinky':'pinky'

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

    def pa_unparent_mesh(self):
        self.mesh_pa = cmds.listRelatives(self.mesh, p=True) or None
        if self.mesh_pa:
            cmds.parent(self.mesh, w=True)
        else:
            cmds.parent(self.mesh, self.geo_grp)

    def get_current_adjust_axis_values(self):
        if cmds.objExists('all_adjust_ctrl.posRotCtrls'):
            self.pos_rot_ctrls_dict = eval(cmds.getAttr('all_adjust_ctrl.posRotCtrls'))
            self.left_arm_pos_grp, self.left_arm_rot_grp, self.left_arm_pos_locs, self.left_arm_rot_locs = self.pos_rot_ctrls_dict['arm']
            self.left_thumb_pos_grp, self.left_thumb_rot_grp, self.left_thumb_pos_locs, self.left_thumb_rot_locs = self.pos_rot_ctrls_dict['thumb']
            self.left_index_pos_grp, self.left_index_rot_grp, self.left_index_pos_locs, self.left_index_rot_locs = self.pos_rot_ctrls_dict['index']
            self.left_middle_pos_grp, self.left_middle_rot_grp, self.left_middle_pos_locs, self.left_middle_rot_locs = self.pos_rot_ctrls_dict['middle']
            self.left_ring_pos_grp, self.left_ring_rot_grp, self.left_ring_pos_locs, self.left_ring_rot_locs = self.pos_rot_ctrls_dict['ring']
            self.left_pinky_pos_grp, self.left_pinky_rot_grp, self.left_pinky_pos_locs, self.left_pinky_rot_locs = self.pos_rot_ctrls_dict['pinky']
            self.left_leg_pos_grp, self.left_leg_rot_grp, self.left_leg_pos_locs, self.left_leg_rot_locs = self.pos_rot_ctrls_dict['leg']
            self.spine_pos_grp, self.spine_rot_grp, self.spine_pos_locs, self.spine_rot_locs = self.pos_rot_ctrls_dict['spine']
            self.neck_pos_grp, self.neck_rot_grp, self.neck_pos_locs, self.neck_rot_locs = self.pos_rot_ctrls_dict['neck']
            self.head_pos_grp, self.head_rot_grp, self.head_pos_locs, self.head_rot_locs = self.pos_rot_ctrls_dict['head']
            self.hips_pos_grp, self.hips_rot_grp, self.hips_pos_locs, self.hips_rot_locs = self.pos_rot_ctrls_dict['hips']

            self.base_joints_dict = eval(cmds.getAttr('all_adjust_ctrl.baseJoints'))
            self.left_arms = self.base_joints_dict['arm']
            self.left_legs = self.base_joints_dict['leg']
            self.left_knee_joints = self.base_joints_dict['knee']
            self.left_knee_segments_top = self.base_joints_dict['kneeTop']

    #--------------------------
    # Adjusting Axis
    #--------------------------
    def set_arm_axis_pv_up(self, shoulder_aim_axis='x', shoulder_up_axis='-y', shoulder_worldSpace=False, shoulder_world_axis='y',
                     arm_aim_axis='x', arm_up_axis='z', arm_worldSpace=False, arm_world_axis='y'):
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

        brAim.set_pole_vec(start=left_arm_loc,
                            mid=left_elbow_loc,
                            end=left_hand_loc,
                            move=10,
                            obj=left_elbow_pvloc)

        # Shoulder
        brAim.aim_nodes(base=left_arm_loc, target=self.left_arm_rot_locs[0]+'_OFFSET_GRP',
                         aim_axis=shoulder_aim_axis, up_axis=shoulder_up_axis,
                         worldUpType='scene', worldSpace=shoulder_worldSpace, world_axis=shoulder_world_axis)
        brAim.aim_nodes(base=left_arm_loc, target=self.left_arm_rot_locs[0],
                         aim_axis=shoulder_aim_axis, up_axis=shoulder_up_axis,
                         worldUpType='scene', worldSpace=shoulder_worldSpace, world_axis=shoulder_world_axis)

        # Arm
        brAim.aim_nodes(base=left_elbow_loc, target=self.left_arm_rot_locs[1]+'_OFFSET_GRP',
                         aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                         worldUpType='object', worldUpObject=left_elbow_pvloc, worldSpace=arm_worldSpace, world_axis=arm_world_axis)
        brAim.aim_nodes(base=left_elbow_loc, target=self.left_arm_rot_locs[1],
                         aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                         worldUpType='object', worldUpObject=left_elbow_pvloc, worldSpace=arm_worldSpace, world_axis=arm_world_axis)

        brAim.aim_nodes(base=left_hand_loc, target=self.left_arm_rot_locs[2]+'_OFFSET_GRP',
                         aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                         worldUpType='object', worldUpObject=left_elbow_pvloc, worldSpace=arm_worldSpace, world_axis=arm_world_axis)
        brAim.aim_nodes(base=left_hand_loc, target=self.left_arm_rot_locs[2],
                         aim_axis=arm_aim_axis, up_axis=arm_up_axis,
                         worldUpType='object', worldUpObject=left_elbow_pvloc, worldSpace=arm_worldSpace, world_axis=arm_world_axis)

        cmds.delete(left_shoulder_loc)
        cmds.delete(left_arm_loc)
        cmds.delete(left_elbow_loc)
        cmds.delete(left_hand_loc)
        cmds.delete(left_elbow_pvloc)

        cmds.matchTransform(self.left_arm_pos_locs[2], self.left_arm_rot_locs[2], pos=True, rot=False, scl=False)
        cmds.xform(self.left_arm_rot_locs[2]+'_OFFSET_GRP', t=[0,0,0], a=True)

    def set_leg_axis_pv_up(self, leg_aim_axis='x', leg_up_axis='z', leg_worldSpace=False, leg_world_axis='y',
                ball_aim_axis='-x', ball_up_axis='z', ball_worldSpace=False, ball_world_axis='y',
                thigh_aim_axis='x', thigh_up_axis='z', thigh_worldSpace=False, thigh_world_axis='y',
                ankle_aim_axis='x', ankle_up_axis='z', ankle_worldSpace=False, ankle_world_axis='y'):

        buf_self_left_legs = [n for n in self.left_legs]
        buf_self_left_leg_rot_locs = [n for n in self.left_leg_rot_locs]
        buf_left_knee_rot_locs = [n for n in self.left_leg_rot_locs
                                    if 'knee' in '_'.join(n.split('_')[:2:])]

        [buf_self_left_legs.remove(n) for n in self.left_knee_joints]
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
                brAim.set_pole_vec(start=start_obj,
                                    mid=mid_obj,
                                    end=end_obj,
                                    move=10,
                                    obj=left_knee_pvloc)

                left_knee_pvlocs.append(left_knee_pvloc)

            # Knee
            for i, (left_knee, left_knee_rot_ctrl) in enumerate(zip(self.left_knee_joints, buf_left_knee_rot_locs)):
                left_knee_loc = cmds.spaceLocator(n=left_knee+'_LOC')[0]
                cmds.matchTransform(left_knee_loc, left_knee)

                if i == len(self.left_knee_joints)-1:
                    base_loc = buf_self_left_leg_rot_locs[1]
                else:
                    base_loc = buf_left_knee_rot_locs[i+1]

                # Leg
                brAim.aim_nodes(base=base_loc, target=left_knee_rot_ctrl+'_OFFSET_GRP',
                                 aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                                 worldUpType='object', worldUpObject=left_knee_pvlocs[i], worldSpace=leg_worldSpace, world_axis=leg_world_axis)
                brAim.aim_nodes(base=base_loc, target=left_knee_rot_ctrl,
                                 aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                                 worldUpType='object', worldUpObject=left_knee_pvlocs[i], worldSpace=leg_worldSpace, world_axis=leg_world_axis)

                cmds.delete(left_knee_loc)

            if left_knee_pvlocs:
                cmds.delete(left_knee_pvlocs)

            # Ankle
            left_knee = self.left_legs[1]
            left_ankle_rot_ctrl = buf_self_left_leg_rot_locs[1]
            left_knee_pvloc = cmds.spaceLocator(n=left_knee+'_PV_LOC')[0]
            brAim.set_pole_vec(start=left_thigh,
                                mid=left_knee,
                                end=left_ankle,
                                move=10,
                                obj=left_knee_pvloc)

            brAim.aim_nodes(base=left_ball_loc, target=left_ankle_rot_ctrl+'_OFFSET_GRP',
                             aim_axis=ankle_aim_axis, up_axis=ankle_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc, worldSpace=ankle_worldSpace, world_axis=ankle_world_axis)
            brAim.aim_nodes(base=left_ball_loc, target=left_ankle_rot_ctrl,
                             aim_axis=ankle_aim_axis, up_axis=ankle_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc, worldSpace=ankle_worldSpace, world_axis=ankle_world_axis)

            cmds.delete(left_knee_pvloc)

        else:
            # Ball Rot Loc
            left_ball_rot_loc = self.left_leg_rot_locs[3]

            left_knee = self.left_legs[1]
            left_knee_rot_ctrl = self.left_leg_rot_locs[1]
            left_ankle_rot_ctrl = self.left_leg_rot_locs[2]
            left_knee_pvloc = cmds.spaceLocator(n=left_knee+'_PV_LOC')[0]
            brAim.set_pole_vec(start=left_thigh,
                                mid=left_knee,
                                end=left_ankle,
                                move=10,
                                obj=left_knee_pvloc)

            # Leg
            brAim.aim_nodes(base=left_ankle_loc, target=left_knee_rot_ctrl+'_OFFSET_GRP',
                             aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc, worldSpace=leg_worldSpace, world_axis=leg_world_axis)
            brAim.aim_nodes(base=left_ankle_loc, target=left_knee_rot_ctrl,
                             aim_axis=leg_aim_axis, up_axis=leg_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc, worldSpace=leg_worldSpace, world_axis=leg_world_axis)

            # Ankle
            brAim.aim_nodes(base=left_ball_loc, target=left_ankle_rot_ctrl+'_OFFSET_GRP',
                             aim_axis=ankle_aim_axis, up_axis=ankle_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc, worldSpace=ankle_worldSpace, world_axis=ankle_world_axis)
            brAim.aim_nodes(base=left_ball_loc, target=left_ankle_rot_ctrl,
                             aim_axis=ankle_aim_axis, up_axis=ankle_up_axis,
                             worldUpType='object', worldUpObject=left_knee_pvloc, worldSpace=ankle_worldSpace, world_axis=ankle_world_axis)

            cmds.delete(left_knee_pvloc)

        # Thigh
        left_knee_pvloc = cmds.spaceLocator(n=self.left_knee_segments_top+'_PV_LOC')[0]
        brAim.set_pole_vec(start=left_thigh_loc,
                            mid=self.left_knee_segments_top,
                            end=left_ankle,
                            move=10,
                            obj=left_knee_pvloc)

        brAim.aim_nodes(base=buf_left_knee_rot_locs[0], target=buf_self_left_leg_rot_locs[0]+'_OFFSET_GRP',
                         aim_axis=thigh_aim_axis, up_axis=thigh_up_axis,
                         worldUpType='object', worldUpObject=left_knee_pvloc, worldSpace=thigh_worldSpace, world_axis=thigh_world_axis)
        brAim.aim_nodes(base=buf_left_knee_rot_locs[0], target=buf_self_left_leg_rot_locs[0],
                         aim_axis=thigh_aim_axis, up_axis=thigh_up_axis,
                         worldUpType='object', worldUpObject=left_knee_pvloc, worldSpace=thigh_worldSpace, world_axis=thigh_world_axis)
        cmds.delete(left_knee_pvloc)

        # brAim.aim_nodes(base=left_ball_loc, target=buf_self_left_leg_rot_locs[1]+'_OFFSET_GRP',
        #                  aim_axis=leg_aim_axis, up_axis=leg_up_axis,
        #                  worldUpType='object', worldUpObject=left_knee_pvloc)
        # brAim.aim_nodes(base=left_ball_loc, target=buf_self_left_leg_rot_locs[1],
        #                  aim_axis=leg_aim_axis, up_axis=leg_up_axis,
        #                  worldUpType='object', worldUpObject=left_knee_pvloc)

        # Ball
        brAim.aim_nodes(base=left_ankle_loc, target=left_ball_rot_loc+'_OFFSET_GRP',
                         aim_axis=ball_aim_axis, up_axis=ball_up_axis,
                         worldUpType='object', worldSpace=ball_worldSpace, world_axis=ball_world_axis)
        brAim.aim_nodes(base=left_ankle_loc, target=left_ball_rot_loc,
                         aim_axis=ball_aim_axis, up_axis=ball_up_axis,
                         worldUpType='object', worldSpace=ball_worldSpace, world_axis=ball_world_axis)

        cmds.delete(left_thigh_loc)
        cmds.delete(left_ankle_loc)
        cmds.delete(left_ball_loc)

    def set_spine_axis_pv_up(self, spine_aim_axis='y', spine_up_axis='z', offset_aim_rotate=0):
        self.set_rot_ctrls(rot_ctrls=self.spine_rot_locs,
                           aim_axis=spine_aim_axis,
                           up_axis=spine_up_axis,
                           offset_aim_rotate=offset_aim_rotate)

    # thumb
    def set_thumb_axis_pv_up(self, thumb_aim_axis='y', thumb_up_axis='z', offset_aim_rotate=0):
        self.set_rot_ctrls(rot_ctrls=self.left_thumb_rot_locs,
                           aim_axis=thumb_aim_axis,
                           up_axis=thumb_up_axis,
                           offset_aim_rotate=offset_aim_rotate)

    # index
    def set_index_axis_pv_up(self, index_aim_axis='y', index_up_axis='z', offset_aim_rotate=0):
        self.set_rot_ctrls(rot_ctrls=self.left_index_rot_locs,
                           aim_axis=index_aim_axis,
                           up_axis=index_up_axis,
                           offset_aim_rotate=offset_aim_rotate)

    # middle
    def set_middle_axis_pv_up(self, middle_aim_axis='y', middle_up_axis='z', offset_aim_rotate=0):
        self.set_rot_ctrls(rot_ctrls=self.left_middle_rot_locs,
                           aim_axis=middle_aim_axis,
                           up_axis=middle_up_axis,
                           offset_aim_rotate=offset_aim_rotate)

    # ring
    def set_ring_axis_pv_up(self, ring_aim_axis='y', ring_up_axis='z', offset_aim_rotate=0):
        self.set_rot_ctrls(rot_ctrls=self.left_ring_rot_locs,
                           aim_axis=ring_aim_axis,
                           up_axis=ring_up_axis,
                           offset_aim_rotate=offset_aim_rotate)

    # pinky
    def set_pinky_axis_pv_up(self, pinky_aim_axis='y', pinky_up_axis='z', offset_aim_rotate=0):
        self.set_rot_ctrls(rot_ctrls=self.left_pinky_rot_locs,
                           aim_axis=pinky_aim_axis,
                           up_axis=pinky_up_axis,
                           offset_aim_rotate=offset_aim_rotate)


    def set_rot_ctrls(self, rot_ctrls=None, aim_axis='y', up_axis='z', offset_aim_rotate=0):
        aim_joints = []
        pa = None
        for srloc in rot_ctrls:
            aim_jnt = cmds.createNode('joint', ss=True)
            cmds.matchTransform(aim_jnt, srloc, pos=True, rot=True, scl=False)
            if pa:
                cmds.parent(aim_jnt, pa)
            pa = aim_jnt
            aim_joints.append(aim_jnt)

        brMJ.merge_joints(aim_joints)

        up_obj = cmds.spaceLocator()[0]
        cmds.matchTransform(up_obj, aim_joints[0])
        axis_vec = [v*1000 for v in AXIS_DICT[up_axis]]
        cmds.xform(up_obj, t=axis_vec, ws=True, a=True)

        brMJ.aim_joints(sel=aim_joints,
                         aim_axis=aim_axis,
                         up_axis=up_axis,
                         worldUpType='object',
                         worldUpObject=up_obj,
                         worldSpace=False,
                         world_axis='y')

        cmds.delete(up_obj)

        for aim_jnt, srloc in zip(aim_joints, rot_ctrls):
            cmds.matchTransform(srloc, aim_jnt, pos=False, rot=True, scl=False)

        cmds.delete(aim_joints)

        offset_rotate = [v*offset_aim_rotate for v in AXIS_DICT[aim_axis]]
        for obj in rot_ctrls:
            cmds.rotate(*offset_rotate, obj, r=True, os=True, fo=True)

    def set_world_aim(self, obj=None, wld_front_axis='z', wld_left_axis='x'):
        brAim.force_world_aim(obj, wld_front_axis, wld_left_axis)

    def match_all_pos_to_rot_locs(self):
        pos_locs = cmds.ls('*_POS_LOC', type='transform')
        for pos_loc in pos_locs:
            try:
                rot_loc = pos_loc.replace('_POS_', '_ROT_')
                cmds.matchTransform(pos_loc, rot_loc, pos=True, rot=False, scl=False)
                cmds.xform(rot_loc+'_OFFSET_GRP', t=[0,0,0], a=True)
            except:
                print(traceback.format_exc())

    def create_all_ctrl(self):
        self.all_ctrl = brDraw.create_curve_text(name='all_adjust_ctrl', text='All Controller', color=[1, 0.5, 1])
        cmds.xform(self.all_ctrl, ro=[-90, 0, 0], s=[30, 30, 30], r=True)

        cmds.parent(self.all_ctrl, 'adjustment_GRP')

        list_attrs = cmds.listAttr('adjustment_GRP', ud=True)
        for lat in list_attrs:
            if not cmds.objExists(self.all_ctrl+'.'+lat):
                cmds.addAttr(self.all_ctrl, ln=lat, at='double', k=True)

            cmds.connectAttr(self.all_ctrl+'.'+lat, 'adjustment_GRP.'+lat, f=True)

        self.save_adjust_ctrls()

    def lock_guide_locators(self):
        pos_locs = cmds.ls('*_POS_LOC', tr=True)
        pos_ltrs = brLock.LockTransforms(pos_locs)
        pos_ltrs.lock_and_hide(['r', 's', 'v'])

        rot_locs = cmds.ls('*_ROT_LOC', tr=True)
        rot_ltrs = brLock.LockTransforms(rot_locs)
        rot_ltrs.lock_and_hide(['t', 's', 'v'])

        grps = cmds.ls('*_LOC_GRP', tr=True)
        grps_ltrs = brLock.LockTransforms(grps)
        grps_ltrs.lock_and_hide(['t', 'r', 's', 'v'])

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

    def save_adjust_ctrls(self):
        cmds.addAttr('all_adjust_ctrl', ln='posRotCtrls', dt='string')
        cmds.setAttr('all_adjust_ctrl.posRotCtrls', '{}'.format(self.pos_rot_ctrls_dict), type='string')
        cmds.setAttr('all_adjust_ctrl.posRotCtrls', l=True)

        cmds.addAttr('all_adjust_ctrl', ln='baseJoints', dt='string')
        cmds.setAttr('all_adjust_ctrl.baseJoints', '{}'.format(self.base_joints_dict), type='string')
        cmds.setAttr('all_adjust_ctrl.baseJoints', l=True)

    def save_adjustment_nodes_values(self, node='root'):
        # adjustment
        adjustment_nodes = cmds.ls('adjustment_GRP', dag=True, type='transform')
        nodes = brNode.Nodes(adjustment_nodes)
        nodes.store_nodes_values()

        cmds.addAttr(node, ln='adjustmentDict', dt='string')
        cmds.setAttr(node+'.adjustmentDict', '{}'.format(nodes.nodes_values), type='string')
        cmds.setAttr(node+'.adjustmentDict', l=True)

        brCommon.json_transfer(self.guide_cur_adj_json, 'export', nodes.nodes_values)
        brCommon.json_transfer(self.guide_name_adj_json, 'export', nodes.nodes_values)

        # footroll
        footroll_nodes = cmds.ls('foot_roll_piv_GRP', dag=True, type='transform')
        nodes = brNode.Nodes(footroll_nodes)
        nodes.store_nodes_values()

        cmds.addAttr(node, ln='footrollDict', dt='string')
        cmds.setAttr(node+'.footrollDict', '{}'.format(nodes.nodes_values), type='string')
        cmds.setAttr(node+'.footrollDict', l=True)

        brCommon.json_transfer(self.guide_cur_footroll_json, 'export', nodes.nodes_values)
        brCommon.json_transfer(self.guide_name_footroll_json, 'export', nodes.nodes_values)

    def set_adjustment_nodes_values(self, type='adjustment'):
        if type == 'adjustment':
            if self.guide_name:
                json_file = self.guide_name_adj_json
            else:
                if self.set_from_current:
                    json_file = self.guide_cur_adj_json
                else:
                    return
        elif type == 'footroll':
            if self.guide_name:
                json_file = self.guide_name_footroll_json
            else:
                if self.set_from_current:
                    json_file = self.guide_cur_footroll_json
                else:
                    return
        # nodes_values = eval(cmds.getAttr('root.adjustmentDict'))
        if not os.path.isfile(json_file):
            return

        nodes_values = brCommon.json_transfer(json_file, 'import')
        for n, vals in nodes_values.items():
            parent = vals['parent']
            children = vals['children']
            full_path = vals['full_path']
            wld_pos = vals['wld_pos']
            wld_rot = vals['wld_rot']
            jnt_orient = vals['jnt_orient']
            shapes = vals['shapes']
            userDefineAttrs = vals['userDefineAttrs']

            if cmds.objExists(n):
                cmds.xform(n, t=wld_pos, ro=wld_rot, ws=True, a=True, p=True)
                if userDefineAttrs:
                    for udattr, attrval in userDefineAttrs.items():
                        try:
                            if attrval[0] in ['double']:
                                cmds.setAttr(n+'.'+udattr, attrval[1])
                            else:
                                cmds.setAttr(n+'.'+udattr, attrval[1], type=attrval[0])
                        except:
                            print(traceback.format_exc())


    def publish_adjust_joints(self):
        self.save_adjustment_nodes_values('root')
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
            # cmds.setAttr(pos_loc+'Shape.localPositionX', 2)
            # cmds.setAttr(pos_loc+'Shape.localPositionY', 2)
            # cmds.setAttr(pos_loc+'Shape.localPositionZ', 2)
            pos_locs.append(pos_loc)
            pos_grp = self.create_offset_grp(obj=pos_loc)
            if i == 0:
                first_pos_grp = pos_grp
            cmds.matchTransform(pos_grp, obj)

            rot_loc = obj+'_ROT_LOC'
            brDraw.create_manip_ctrl(rot_loc)
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
        toe_hit_point = brCommon.closest_hit_point_on_mesh(point=toe_point, mesh=self.mesh, axis='z')
        toe_loc = cmds.spaceLocator(n=prefix+'toe_piv_loc')[0]
        cmds.xform(toe_loc, t=[toe_hit_point[0],
                               0,
                               toe_hit_point[2]])

        heel_point = cmds.xform(ankle, q=True, t=True, ws=True)
        heel_hit_point = brCommon.closest_hit_point_on_mesh(point=heel_point, mesh=self.mesh, axis='-z')
        heel_loc = cmds.spaceLocator(n=prefix+'heel_piv_loc')[0]
        cmds.xform(heel_loc, t=[heel_hit_point[0],
                               0,
                               heel_hit_point[2]])

        toe_heel_mid_point = brCommon.get_mid_point(toe_point, heel_point)
        in_hit_point = brCommon.closest_hit_point_on_mesh(point=toe_heel_mid_point, mesh=self.mesh, axis=in_axis)
        in_loc = cmds.spaceLocator(n=prefix+'in_piv_loc')[0]
        cmds.xform(in_loc, t=[in_hit_point[0],
                               0,
                               in_hit_point[2]])

        out_hit_point = brCommon.closest_hit_point_on_mesh(point=toe_heel_mid_point, mesh=self.mesh, axis=out_axis)
        out_loc = cmds.spaceLocator(n=prefix+'out_piv_loc')[0]
        cmds.xform(out_loc, t=[out_hit_point[0],
                               0,
                               out_hit_point[2]])

        return [loc for loc in [toe_loc, heel_loc, in_loc, out_loc]]
