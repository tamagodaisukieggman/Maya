# -*- coding: utf-8 -*-
from imp import reload
import os
import traceback

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
import buildRig.root as brRoot
import buildRig.fk as brFk
import buildRig.file as brFile
reload(brRoot)
reload(brFk)
reload(brCommon)
reload(brFile)

# rig_setup_id = 'bahamut'
# chara_path

namespace = 'chr'
files = brFile.Files(chara_path, namespace, 'reference')
file_objects = files.file_execute()
ref_top_nodes = files.get_top_nodes()

##############
# root setup
# roots
root_joints = ['Global', 'Local', 'Root']

try:
    root = brRoot.Root(module='root',
                 side='Cn',
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 joints=root_joints,
                 namespace=namespace,
                 shapes=['gnomon', 'pacman', 'arrow_one_way_z'],
                 axis=[0,0,0],
                 scale=3000,
                 scale_step=-500,
                 prefix=None)
except:
    print(traceback.format_exc())

root.base_connection()

##############
# FK setup
# hips
hip_joints = ['Hip']
hip_fk = brFk.Fk(module='hip',
             side='Cn',
             rig_joints_parent=None,
             rig_ctrls_parent=None,
             rig_ctrls_parent_const=root.jnt_object.nodes[-1],
             joints=hip_joints,
             namespace=namespace,
             shape='hip',
             axis=[0,0,0],
             scale=2000,
             scale_step=-90,
             prefix='FK_')

hip_fk.base_connection()

##############
# FK setup
# spine
spine_joints = ['Spine1',
 'Spine2',
 'Spine3']
spine_fk = brFk.Fk(module='spine',
             side='Cn',
             rig_joints_parent=None,
             rig_ctrls_parent=None,
             rig_ctrls_parent_const=hip_fk.jnt_object.nodes[-1],
             joints=spine_joints,
             namespace=namespace,
             shape='cube_pointer',
             axis=[90,0,0],
             scale=1000,
             scale_step=-90,
             prefix='FK_')

spine_fk.connect_children()
spine_fk.base_connection()

##############
# FK setup
# neck
neck_joints = ['Neck']
neck_fk = brFk.Fk(module='neck',
             side='Cn',
             rig_joints_parent=None,
             rig_ctrls_parent=None,
             rig_ctrls_parent_const=spine_fk.jnt_object.nodes[-1],
             joints=neck_joints,
             namespace=namespace,
             shape='cube_pointer',
             axis=[180,0,0],
             scale=700,
             scale_step=-90,
             prefix='FK_')

neck_fk.base_connection()

brCommon.create_spaces(
    base_ctrl=neck_fk.trs_objects[-1].nodes[-1],
    base_ctrl_space=neck_fk.trs_objects[-1].nodes[-4],
    space_ctrls=[
        spine_fk.trs_objects[-1].nodes[-1],
        root.trs_objects[-1].nodes[-1],
    ],
    spaces=[
        'Spine',
        'Root',
    ],
    const_type='rot',
    space_type='enum'
)

##############
# FK setup
# head
head_joints = ['Head']
head_fk = brFk.Fk(module='head',
             side='Cn',
             rig_joints_parent=None,
             rig_ctrls_parent=None,
             rig_ctrls_parent_const=neck_fk.jnt_object.nodes[-1],
             joints=head_joints,
             namespace=namespace,
             shape='arrows_on_ball',
             axis=[0,0,0],
             scale=800,
             scale_step=-90,
             prefix='FK_')

head_fk.base_connection()

##############
# FK setup
# jaw
jaw_joints = ['Jaw']
jaw_fk = brFk.Fk(module='jaw',
             side='Cn',
             rig_joints_parent=None,
             rig_ctrls_parent=None,
             rig_ctrls_parent_const=head_fk.jnt_object.nodes[-1],
             joints=jaw_joints,
             namespace=namespace,
             shape='cube',
             axis=[0,0,0],
             scale=600,
             scale_step=-90,
             prefix='FK_')

jaw_fk.base_connection()

##############
# FK setup
# tongue
tongue_joints = ['Tongue_01',
'Tongue_02']
tongue_fk = brFk.Fk(module='tongue',
             side='Cn',
             rig_joints_parent=None,
             rig_ctrls_parent=None,
             rig_ctrls_parent_const=jaw_fk.jnt_object.nodes[-1],
             joints=tongue_joints,
             namespace=namespace,
             shape='dumbell',
             axis=[0,0,0],
             scale=400,
             scale_step=-90,
             prefix='FK_')

tongue_fk.base_connection()

##############
# side fk setup
sides = ['_L', '_R']

arm_joints = ['Shoulder',
 'Arm',
 'Elbow',
 'Wrist']

leg_joints = [
    'Thigh',
    'Knee'
]

wing_joints = ['ArmWing_01',
 'ArmWing_02',
 'ArmWing_03',
 'ArmWing_04',
 'ArmWing_05',
 'ArmWing_06',
 'ArmWing_07',
 'WingA_01',
 'WingA_02',
 'WingA_03',
 'WingB_01',
 'WingB_02',
 'WingB_03',
 'WingC_01',
 'WingC_02',
 'WingC_03',
 'WingD_01',
 'WingD_02',
 'WingD_03',
 'WingE_01',
 'WingE_02',
 'WingE_03',
 'WingF_01',
 'WingF_02']

thumb_joints = [
    'Thumb_01',
    'Thumb_02',
    'Thumb_03'
]

index_joints = [
    'Index_01',
    'Index_02',
    'Index_03'
]

middle_joints = [
    'Middle_01',
    'Middle_02',
    'Middle_03'
]

ring_joints = [
    'Ring_01',
    'Ring_02',
    'Ring_03'
]


for side in sides:
    if side == '_L':
        m_side = 'Lt'
    elif side == '_R':
        m_side = 'Rt'

    # arm
    side_arm_joints = [n+side for n in arm_joints]
    arm_fk = brFk.Fk(module='arm'+side,
                 side=m_side,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 rig_ctrls_parent_const=spine_fk.jnt_object.nodes[-1],
                 joints=side_arm_joints,
                 namespace=namespace,
                 shape='cube',
                 axis=[0,0,0],
                 scale=700,
                 scale_step=-100,
                 prefix='FK_')

    arm_fk.connect_children()
    arm_fk.base_connection()

    brCommon.create_spaces(
        base_ctrl=arm_fk.trs_objects[0].nodes[-1],
        base_ctrl_space=arm_fk.trs_objects[0].nodes[-4],
        space_ctrls=[
            spine_fk.trs_objects[-1].nodes[-1],
            root.trs_objects[-1].nodes[-1],
        ],
        spaces=[
            'Spine',
            'Root',
        ],
        const_type='rot',
        space_type='enum'
    )

    # leg
    side_leg_joints = [n+side for n in leg_joints]
    leg_fk = brFk.Fk(module='leg'+side,
                 side=m_side,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 rig_ctrls_parent_const=hip_fk.jnt_object.nodes[-1],
                 joints=side_leg_joints,
                 namespace=namespace,
                 shape='cube',
                 axis=[0,0,0],
                 scale=700,
                 scale_step=-100,
                 prefix='FK_')

    leg_fk.connect_children()
    leg_fk.base_connection()

    # wing
    side_wing_joints = [n+side for n in wing_joints]
    wing_fk = brFk.Fk(module='wing'+side,
                 side=m_side,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 joints=side_wing_joints,
                 rig_ctrls_parent_const=spine_fk.jnt_object.nodes[-1],
                 namespace=namespace,
                 shape='cube_pointer',
                 axis=[0,0,0],
                 scale=500,
                 scale_step=-10,
                 prefix='FK_')

    wing_fk.connect_children()
    wing_fk.base_connection()

    brCommon.create_spaces(
        base_ctrl=wing_fk.trs_objects[0].nodes[-1],
        base_ctrl_space=wing_fk.trs_objects[0].nodes[-4],
        space_ctrls=[
            spine_fk.trs_objects[-1].nodes[-1],
            root.trs_objects[-1].nodes[-1],
        ],
        spaces=[
            'Spine',
            'Root',
        ],
        const_type='rot',
        space_type='enum'
    )

    # fingers
    # thumb
    side_thumb_joints = [n+side for n in thumb_joints]
    thumb_fk = brFk.Fk(module='thumb'+side,
                 side=m_side,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 rig_ctrls_parent_const=arm_fk.jnt_object.nodes[-1],
                 joints=side_thumb_joints,
                 namespace=namespace,
                 shape='cube_pointer',
                 axis=[0,0,0],
                 scale=200,
                 scale_step=-30,
                 prefix='FK_')

    thumb_fk.connect_children()
    thumb_fk.base_connection()

    # index
    side_index_joints = [n+side for n in index_joints]
    index_fk = brFk.Fk(module='index'+side,
                 side=m_side,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 rig_ctrls_parent_const=arm_fk.jnt_object.nodes[-1],
                 joints=side_index_joints,
                 namespace=namespace,
                 shape='cube_pointer',
                 axis=[0,0,0],
                 scale=200,
                 scale_step=-30,
                 prefix='FK_')

    index_fk.connect_children()
    index_fk.base_connection()

    # middle
    side_middle_joints = [n+side for n in middle_joints]
    middle_fk = brFk.Fk(module='middle'+side,
                 side=m_side,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 rig_ctrls_parent_const=arm_fk.jnt_object.nodes[-1],
                 joints=side_middle_joints,
                 namespace=namespace,
                 shape='cube_pointer',
                 axis=[0,0,0],
                 scale=200,
                 scale_step=-30,
                 prefix='FK_')

    middle_fk.connect_children()
    middle_fk.base_connection()

    # ring
    side_ring_joints = [n+side for n in ring_joints]
    ring_fk = brFk.Fk(module='ring'+side,
                 side=m_side,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 rig_ctrls_parent_const=arm_fk.jnt_object.nodes[-1],
                 joints=side_ring_joints,
                 namespace=namespace,
                 shape='cube_pointer',
                 axis=[0,0,0],
                 scale=200,
                 scale_step=-30,
                 prefix='FK_')

    ring_fk.connect_children()
    ring_fk.base_connection()


##############
# FK setup
# tails
tail_joints = ['Tail_01',
 'Tail_02',
 'Tail_03',
 'Tail_04',
 'Tail_05',
 'Tail_06',
 'Tail_07',
 'Tail_08']
tail_fk = brFk.Fk(module='tail',
             side='Cn',
             rig_joints_parent=None,
             rig_ctrls_parent=None,
             rig_ctrls_parent_const=hip_fk.jnt_object.nodes[-1],
             joints=tail_joints,
             namespace=namespace,
             shape='cube_pointer',
             axis=[0,90,180],
             scale=1000,
             scale_step=-90,
             prefix='FK_')

tail_fk.connect_children()
tail_fk.base_connection()

brCommon.create_spaces(
    base_ctrl=tail_fk.trs_objects[0].nodes[-1],
    base_ctrl_space=tail_fk.trs_objects[0].nodes[-4],
    space_ctrls=[
        hip_fk.trs_objects[-1].nodes[-1],
        root.trs_objects[-1].nodes[-1],
    ],
    spaces=[
        'Hip',
        'Root',
    ],
    const_type='rot',
    space_type='enum'
)

##############
# chr parent MODEL
[cmds.parent(rfn, tail_fk.model_grp) for rfn in ref_top_nodes]
