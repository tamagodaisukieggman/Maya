# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload
import json
import math

import tkgRigBuild.libs.aim as tkgAim
import tkgRigBuild.libs.common as tkgCommon
reload(tkgAim)
reload(tkgCommon)

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

def aim_joints(sel=None, aim_axis='x', up_axis='y', worldUpType='object', worldUpObject=None, worldSpace=False, world_axis='y'):
    # Aim Joints
    before_sel = cmds.ls(os=True)
    if not sel:
        sel = cmds.ls(os=True, type='joint')
    for obj in sel:
        tkgAim.aim_nodes_from_root(root_jnt=obj,
                                   type='joint',
                                   aim_axis=aim_axis,
                                   up_axis=up_axis,
                                   worldUpType=worldUpType,
                                   worldUpObject=worldUpObject,
                                   worldSpace=worldSpace,
                                   world_axis=world_axis)

    if before_sel:
        cmds.select(before_sel, r=True)

def correct_joints(sel=None, ssc_sts=False):
    before_sel = cmds.ls(os=True)
    if not sel:
        sel = cmds.ls(os=True, dag=True, type='joint')
    freeze_rotate(sel)
    merge_joints(sel)
    round_transform_attrs(sel)
    set_preferred_angle(sel)
    set_segmentScaleCompensate(joints=sel, ssc_sts=False)
    if before_sel:
        cmds.select(before_sel, r=True)

def mirror_correct_joints(sel=None, mirror=['_L', '_R'], force_values=[180, 0, 0]):
    # Mirror Joints
    before_sel = cmds.ls(os=True)
    if not sel:
        sel = cmds.ls(os=True, type='joint')
    for obj in sel:
        mirror_joints = cmds.mirrorJoint(obj,
                     mirrorYZ=True,
                     mirrorBehavior=True,
                     searchReplace=mirror)
        adjust_mirrors(force_values=force_values,
                       joints=mirror_joints)

        correct_joints(mirror_joints)
    if before_sel:
        cmds.select(before_sel, r=True)

def aim_correct_joints(sel=None,
                       aim_axis='x',
                       up_axis='y',
                       worldUpType='object',
                       worldUpObject=None,
                       ssc_sts=False,
                       worldSpace=False,
                       world_axis='y'):
    aim_joints(sel=sel,
                 aim_axis=aim_axis,
                 up_axis=up_axis,
                 worldUpType=worldUpType,
                 worldUpObject=worldUpObject,
                 worldSpace=worldSpace,
                 world_axis=world_axis)
    correct_joints(sel=cmds.ls(os=True, dag=True),
                     ssc_sts=ssc_sts)

def create_joint(name=None, position=None):
    joint = cmds.createNode('joint' , name=name)
    cmds.xform(joint ,worldSpace=True, translation=position)
    return joint

def create_joints_from_embedding(embedding):
    embedded_joints = [create_joint(name=name, position=position)
                        for name , position in embedding['joints'].items()]
    return embedded_joints

def add_segments(start_position=None, end_position=None, base_name=None, count=3, embedding=None):
    # base_name = 'spine'
    # count = 3
    seg_joints = []
    step = 1.0 / count
    max_rate = 1 - step
    rate = 0
    for i in range(count):
        mid_point = tkgCommon.get_mid_point(start_position, end_position, rate)
        seg_jnt = '{}_{}'.format(base_name, str(i+1).zfill(2))
        seg_joints.append(seg_jnt)
        embedding['joints'][seg_jnt] = mid_point
        rate += step

    return seg_joints

class Segments:
    def __init__(self,
                 start=None,
                 end=None,
                 base_name=None,
                 count=None,
                 embedding=None,
                 parent=None):
        self.start = start
        self.end = end
        self.base_name = base_name
        self.count = count
        self.embedding = embedding
        self.parent = parent

        self.top = None
        self.bottom = None
        self.parent_dict = {}

        self.insert()

    def insert(self):
        if self.count != 1:
            start_position = self.embedding['joints'][self.start]
            end_position = self.embedding['joints'][self.end]
            seg_joints = add_segments(start_position=start_position,
                                     end_position=end_position,
                                     base_name=self.base_name,
                                     count=self.count,
                                     embedding=self.embedding)
            self.embedding['joints'].pop(self.base_name)

            self.top = seg_joints[0]
            self.bottom = seg_joints[-1]

            # set parent
            if self.parent:
                self.parent_dict[self.top] = self.parent
            for i, seg_j in enumerate(seg_joints):
                if i == 0:
                    pass
                else:
                    self.parent_dict[seg_j] = seg_joints[i-1]

        else:
            if self.parent:
                self.parent_dict[self.start] = self.parent

            self.top = self.base_name
            self.bottom = self.base_name


def embed_biped_joints(mesh=None, root_count=1, spine_count=3, neck_count=1, knee_count=1):
    shape = tkgCommon.get_shapes(mesh)[0]

    result = cmds.skeletonEmbed(shape)
    embedding = json.loads(result)

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

    left_arm_mid_point = tkgCommon.get_mid_point(shoulders_position, left_arm_position)
    right_arm_mid_point = tkgCommon.get_mid_point(shoulders_position, right_arm_position)

    embedding['joints'].update({'left_shoulder':left_arm_mid_point})
    embedding['joints'].update({'right_shoulder':right_arm_mid_point})

    # Fixing neck
    embedding['joints']['neck'] = embedding['joints'].pop('shoulders')
    neck_position = embedding['joints']['neck']
    head_position = embedding['joints']['head']

    neck_head_mid_point = tkgCommon.get_mid_point(neck_position, head_position, 0.3)
    embedding['joints']['neck'] = neck_head_mid_point

    # Fixing head
    fix_head_mid_point = tkgCommon.get_mid_point(neck_position, head_position, 0.7)
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
            if 'thigh' in p:
                percentage = 0.5
            elif 'arm' in p:
                percentage = 0.4
            embedding['joints'][s+p[1]] = tkgCommon.get_mid_point(start_position, end_position, percentage)

    # Fix Hand Ankle
    for s in ['left_', 'right_']:
        start_position = embedding['joints'][s+'hand']
        end_position = embedding['joints'][s+'arm']
        embedding['joints'][s+'hand'] = tkgCommon.get_mid_point(start_position, end_position, 0.25)

        start_position = embedding['joints'][s+'ankle']
        end_position = embedding['joints'][s+'thigh']
        embedding['joints'][s+'ankle'] = tkgCommon.get_mid_point(start_position, end_position, 0.07)

    # Fix Elbow Knee
    for s in ['left_', 'right_']:
        start_position = embedding['joints'][s+'hand']
        mid_position = embedding['joints'][s+'elbow']
        end_position = embedding['joints'][s+'arm']
        mid_point = tkgCommon.get_mid_point(start_position, end_position, 0.8)
        embedding['joints'][s+'elbow'] = [mid_position[0], mid_position[1], mid_point[2]]

        # start_position = embedding['joints'][s+'ankle']
        # mid_position = embedding['joints'][s+'knee']
        # end_position = embedding['joints'][s+'thigh']
        # mid_point = tkgCommon.get_mid_point(start_position, end_position, 1.000005)
        # embedding['joints'][s+'knee'] = [mid_position[0], mid_position[1], mid_point[2]]


    for joint in ['hips', 'spine', 'neck', 'head']:
        old_pos = embedding['joints'][joint]
        new_pos = []
        new_pos.append(old_pos[0]*0)
        new_pos.append(old_pos[1])
        new_pos.append(old_pos[2])
        embedding['joints'][joint] = new_pos

    # Add Root Joint
    embedding['joints']['root'] = [0, 0, 0]

    # Add Root Segments
    # root_count=1
    # if root_count != 1:
    #     start_position = embedding['joints']['root']
    #     end_position = embedding['joints']['root']
    #     add_segments(start_position=start_position,
    #                  end_position=end_position,
    #                  base_name='root',
    #                  count=root_count,
    #                  embedding=embedding)
    #     embedding['joints'].pop('root')

    root_segments = Segments(start='root',
                        end='root',
                        base_name='root',
                        count=root_count,
                        embedding=embedding,
                        parent=None)

    # Add Spine Segments
    # spine_count=3
    # if spine_count != 1:
    #     start_position = embedding['joints']['hips']
    #     end_position = embedding['joints']['neck']
    #     add_segments(start_position=start_position,
    #                  end_position=end_position,
    #                  base_name='spine',
    #                  count=spine_count,
    #                  embedding=embedding)
    #     embedding['joints'].pop('spine')

    spine_segments = Segments(start='hips',
                        end='neck',
                        base_name='spine',
                        count=spine_count,
                        embedding=embedding,
                        parent='hips')

    # Add Neck Segments
    # neck_count=2
    # if neck_count != 1:
    #     start_position = embedding['joints']['neck']
    #     end_position = embedding['joints']['head']
    #     add_segments(start_position=start_position,
    #                  end_position=end_position,
    #                  base_name='neck',
    #                  count=neck_count,
    #                  embedding=embedding)
    #     embedding['joints'].pop('neck')

    neck_segments = Segments(start='neck',
                        end='head',
                        base_name='neck',
                        count=neck_count,
                        embedding=embedding,
                        parent=spine_segments.bottom)

    # Add Knee Segments
    left_knee_segments = Segments(start='left_knee',
                        end='left_ankle',
                        base_name='left_knee',
                        count=knee_count,
                        embedding=embedding,
                        parent='left_thigh')

    right_knee_segments = Segments(start='right_knee',
                        end='right_ankle',
                        base_name='right_knee',
                        count=knee_count,
                        embedding=embedding,
                        parent='right_thigh')


    # Connect Joints
    mirror = ['left_', 'right_']
    parent_hierarchy = {
        'hips':root_segments.bottom,
        'head':neck_segments.bottom,
        spine_segments.top:'hips',

        'left_hand':'left_elbow',
        'left_elbow':'left_arm',
        'left_arm':'left_shoulder',
        'left_shoulder':spine_segments.bottom,

        'right_hand':'right_elbow',
        'right_elbow':'right_arm',
        'right_arm':'right_shoulder',
        'right_shoulder':spine_segments.bottom,

        'left_thigh':'hips',
        left_knee_segments.top:'left_thigh',
        'left_ankle':left_knee_segments.bottom,
        'left_ball':'left_ankle',

        'right_thigh':'hips',
        right_knee_segments.top:'right_thigh',
        'right_ankle':right_knee_segments.bottom,
        'right_ball':'right_ankle',

    }

    for child, parent in root_segments.parent_dict.items():
        parent_hierarchy[child] = parent

    for child, parent in spine_segments.parent_dict.items():
        parent_hierarchy[child] = parent

    for child, parent in neck_segments.parent_dict.items():
        parent_hierarchy[child] = parent

    for child, parent in left_knee_segments.parent_dict.items():
        parent_hierarchy[child] = parent

    for child, parent in right_knee_segments.parent_dict.items():
        parent_hierarchy[child] = parent

    # create joints
    # 実際に作成するのはembeddingに格納した値を確認してから
    embedded_joints = create_joints_from_embedding( embedding )

    for child, parent in parent_hierarchy.items():
        if child and parent:
            cmds.parent(child, parent)


    # Aiming Spine
    spine_01 = 'spine_01'
    aim_correct_joints(sel=[spine_01],
                           aim_axis='y',
                           up_axis='y',
                           worldUpType='object',
                           ssc_sts=False,
                           worldSpace=True,
                           world_axis='y')

    # Aiming shoulder
    left_shoulder = 'left_shoulder'
    aim_correct_joints(sel=[left_shoulder],
                           aim_axis='x',
                           up_axis='-y',
                           worldUpType='object',
                           ssc_sts=False,
                           worldSpace=True,
                           world_axis='y')

    # Aiming arm
    left_arm = 'left_arm'
    aim_correct_joints(sel=[left_arm],
                           aim_axis='x',
                           up_axis='-y',
                           worldUpType='object',
                           ssc_sts=False,
                           worldSpace=True,
                           world_axis='x')

    # Aiming arm
    left_thigh = 'left_thigh'
    aim_correct_joints(sel=[left_thigh],
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

    return root_segments, spine_segments, neck_segments, left_knee_segments, right_knee_segments

# wizard2仕様
def joint_labeling():
    joints = cmds.ls(os=True, type='joint', dag=True)
    if not joints: return

    for obj in joints:
        if obj.endswith('_L') or obj.endswith('_R'):
            spl_obj = '_'.join(obj.split('_')[:-1])
            if obj.endswith('_L'):
                cmds.setAttr(obj+'.side', 1)
            if obj.endswith('_R'):
                cmds.setAttr(obj+'.side', 2)
        else:
            spl_obj = obj

        cmds.setAttr(obj+'.type', 18)
        cmds.setAttr(obj+'.otherType', spl_obj, type='string')
