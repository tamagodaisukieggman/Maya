# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload

import maya.cmds as cmds
import maya.mel as mel

import buildRig.post.finalize as brFinalize
reload(brFinalize)

namespace = 'chr'

# set environment
brFinalize.set_environment(set_fps=30,
                           set_focalLength=100,
                           set_farClipPlane=240000,
                           set_nearClipPlane=100)

# set ihi
brFinalize.ihi_hides(set_ihi_nodes=None)

#######################################################
# Create Sets
#######################################################
create_sets = {
    'all_sets':None,
    'export_sets':{
        'add':['all_sets'],
        'items':cmds.ls(namespace+':Root', dag=True, type='joint')
    },
    'ctrl_sets':{
        'add':['all_sets']
    },
    'ikfk_ctrl_sets':{
        'add':['all_sets'],
        'items':[]
    },
    'main_ctrl_sets':{
        'add':['ctrl_sets'],
        'items':[
            'Global_ctrl',
            'Local_ctrl',
            'Root_ctrl',
            ]
    },
    'cog_hip_ctrl_sets':{
        'add':['ctrl_sets'],
        'items':[
            'FK_Hip_ctrl'
        ]
    },
    'fk_ctrl_sets':{
        'add':['ctrl_sets'],
    },

    # wing ctrl sets
    'wing_ctrl_sets':{
        'add':['ctrl_sets'],
    },

    'left_wing_ctrl_sets':{
        'add':['wing_ctrl_sets'],
        'items':['FK_ArmWing_01_L_ctrl',
                 'FK_ArmWing_02_L_ctrl',
                 'FK_ArmWing_03_L_ctrl',
                 'FK_ArmWing_04_L_ctrl',
                 'FK_ArmWing_05_L_ctrl',
                 'FK_ArmWing_06_L_ctrl',
                 'FK_ArmWing_07_L_ctrl',
                 'FK_WingA_01_L_ctrl',
                 'FK_WingA_02_L_ctrl',
                 'FK_WingA_03_L_ctrl',
                 'FK_WingB_01_L_ctrl',
                 'FK_WingB_02_L_ctrl',
                 'FK_WingB_03_L_ctrl',
                 'FK_WingC_01_L_ctrl',
                 'FK_WingC_02_L_ctrl',
                 'FK_WingC_03_L_ctrl',
                 'FK_WingD_01_L_ctrl',
                 'FK_WingD_02_L_ctrl',
                 'FK_WingD_03_L_ctrl',
                 'FK_WingE_01_L_ctrl',
                 'FK_WingE_02_L_ctrl',
                 'FK_WingE_03_L_ctrl',
                 'FK_WingF_01_L_ctrl',
                 'FK_WingF_02_L_ctrl']
    },
    'right_wing_ctrl_sets':{
        'add':['wing_ctrl_sets'],
        'items':['FK_ArmWing_01_R_ctrl',
                 'FK_ArmWing_02_R_ctrl',
                 'FK_ArmWing_03_R_ctrl',
                 'FK_ArmWing_04_R_ctrl',
                 'FK_ArmWing_05_R_ctrl',
                 'FK_ArmWing_06_R_ctrl',
                 'FK_ArmWing_07_R_ctrl',
                 'FK_WingA_01_R_ctrl',
                 'FK_WingA_02_R_ctrl',
                 'FK_WingA_03_R_ctrl',
                 'FK_WingB_01_R_ctrl',
                 'FK_WingB_02_R_ctrl',
                 'FK_WingB_03_R_ctrl',
                 'FK_WingC_01_R_ctrl',
                 'FK_WingC_02_R_ctrl',
                 'FK_WingC_03_R_ctrl',
                 'FK_WingD_01_R_ctrl',
                 'FK_WingD_02_R_ctrl',
                 'FK_WingD_03_R_ctrl',
                 'FK_WingE_01_R_ctrl',
                 'FK_WingE_02_R_ctrl',
                 'FK_WingE_03_R_ctrl',
                 'FK_WingF_01_R_ctrl',
                 'FK_WingF_02_R_ctrl']
    },

    # tail ctrl sets
    'tail_ctrl_sets':{
        'add':['ctrl_sets'],
        'items':['FK_Tail_01_ctrl',
                 'FK_Tail_02_ctrl',
                 'FK_Tail_03_ctrl',
                 'FK_Tail_04_ctrl',
                 'FK_Tail_05_ctrl',
                 'FK_Tail_06_ctrl',
                 'FK_Tail_07_ctrl',
                 'FK_Tail_08_ctrl']
    },

    'fk_spine_ctrl_sets':{
        'add':['fk_ctrl_sets'],
        'items':[
            'FK_Spine1_ctrl',
            'FK_Spine2_ctrl',
            'FK_Spine3_ctrl'
        ]
    },
    'fk_neck_head_ctrl_sets':{
        'add':['fk_ctrl_sets'],
        'items':[
            'FK_Neck_ctrl',
            'FK_Head_ctrl'
        ]
    },

    'fk_jaw_ctrl_sets':{
        'add':['fk_ctrl_sets'],
        'items':[
            'FK_Jaw_ctrl',
        ]
    },

    'fk_tongue_ctrl_sets':{
        'add':['fk_ctrl_sets'],
        'items':[
            'FK_Tongue_01_ctrl',
            'FK_Tongue_02_ctrl'
        ]
    },

    'fk_hand_ctrl_sets':{
        'add':['fk_ctrl_sets']
    },
    'fk_left_hand_ctrl_sets':{
        'add':['fk_hand_ctrl_sets', 'left_fk_ctrl_sets'],
        'items':[
            'FK_Shoulder_L_ctrl',
            'FK_Arm_L_ctrl',
            'FK_Elbow_L_ctrl',
            'FK_Wrist_L_ctrl'
        ]
    },
    'fk_right_hand_ctrl_sets':{
        'add':['fk_hand_ctrl_sets', 'right_fk_ctrl_sets'],
        'items':[
            'FK_Shoulder_R_ctrl',
            'FK_Arm_R_ctrl',
            'FK_Elbow_R_ctrl',
            'FK_Wrist_R_ctrl'
        ]
    },
    'fk_foot_ctrl_sets':{
        'add':['fk_ctrl_sets']
    },
    'fk_left_foot_ctrl_sets':{
        'add':['fk_foot_ctrl_sets', 'left_fk_ctrl_sets'],
        'items':[
            'FK_Thigh_L_ctrl',
            'FK_Knee_L_ctrl'
        ]
    },
    'fk_right_foot_ctrl_sets':{
        'add':['fk_foot_ctrl_sets', 'right_fk_ctrl_sets'],
        'items':[
            'FK_Thigh_R_ctrl',
            'FK_Knee_R_ctrl'
        ]
    },

    'ik_ctrl_sets':{
        'add':['ctrl_sets']
    },
    'ik_hand_ctrl_sets':{
        'add':['ik_ctrl_sets']
    },
    'ik_left_hand_ctrl_sets':{
        'add':['ik_hand_ctrl_sets', 'left_ik_ctrl_sets'],
        'items':[]
    },
    'ik_right_hand_ctrl_sets':{
        'add':['ik_hand_ctrl_sets', 'right_ik_ctrl_sets'],
        'items':[]
    },
    'ik_foot_ctrl_sets':{
        'add':['ik_ctrl_sets']
    },
    'ik_left_foot_ctrl_sets':{
        'add':['ik_foot_ctrl_sets', 'left_ik_ctrl_sets'],
        'items':[]
    },
    'ik_right_foot_ctrl_sets':{
        'add':['ik_foot_ctrl_sets', 'right_ik_ctrl_sets'],
        'items':[]
    },

    'finger_ctrl_sets':{
        'add':['ctrl_sets']
    },
    'left_finger_ctrl_sets':{
        'add':['finger_ctrl_sets']
    },
    'left_thumb_finger_ctrl_sets':{
        'add':['left_finger_ctrl_sets'],
        'items':[
            'FK_Thumb_01_L_ctrl',
            'FK_Thumb_02_L_ctrl',
            'FK_Thumb_03_L_ctrl'
        ]
    },
    'left_index_finger_ctrl_sets':{
        'add':['left_finger_ctrl_sets'],
        'items':[
            'FK_Index_01_L_ctrl',
            'FK_Index_02_L_ctrl',
            'FK_Index_03_L_ctrl'
        ]
    },
    'left_middle_finger_ctrl_sets':{
        'add':['left_finger_ctrl_sets'],
        'items':[
            'FK_Middle_01_L_ctrl',
            'FK_Middle_02_L_ctrl',
            'FK_Middle_03_L_ctrl'
        ]
    },
    'left_ring_finger_ctrl_sets':{
        'add':['left_finger_ctrl_sets'],
        'items':[
            'FK_Ring_01_L_ctrl',
            'FK_Ring_02_L_ctrl',
            'FK_Ring_03_L_ctrl'
        ]
    },
    'left_pinky_finger_ctrl_sets':{
        'add':['left_finger_ctrl_sets'],
        'items':[]
    },

    'right_finger_ctrl_sets':{
        'add':['finger_ctrl_sets']
    },
    'right_thumb_finger_ctrl_sets':{
        'add':['right_finger_ctrl_sets'],
        'items':[
            'FK_Thumb_01_R_ctrl',
            'FK_Thumb_02_R_ctrl',
            'FK_Thumb_03_R_ctrl'
        ]
    },
    'right_index_finger_ctrl_sets':{
        'add':['right_finger_ctrl_sets'],
        'items':[
            'FK_Index_01_R_ctrl',
            'FK_Index_02_R_ctrl',
            'FK_Index_03_R_ctrl'
        ]
    },
    'right_middle_finger_ctrl_sets':{
        'add':['right_finger_ctrl_sets'],
        'items':[
            'FK_Middle_01_R_ctrl',
            'FK_Middle_02_R_ctrl',
            'FK_Middle_03_R_ctrl'
        ]
    },
    'right_ring_finger_ctrl_sets':{
        'add':['right_finger_ctrl_sets'],
        'items':[
            'FK_Ring_01_R_ctrl',
            'FK_Ring_02_R_ctrl',
            'FK_Ring_03_R_ctrl'
        ]
    },
    'right_pinky_finger_ctrl_sets':{
        'add':['right_finger_ctrl_sets'],
        'items':[]
    },

    'side_ctrl_sets':{
        'add':['ctrl_sets']
    },

    'left_ctrl_sets':{
        'add':['side_ctrl_sets']
    },
    'left_ik_ctrl_sets':{
        'add':['left_ctrl_sets']
    },
    'left_fk_ctrl_sets':{
        'add':['left_ctrl_sets']
    },


    'right_ctrl_sets':{
        'add':['side_ctrl_sets']
    },
    'right_ik_ctrl_sets':{
        'add':['right_ctrl_sets']
    },
    'right_fk_ctrl_sets':{
        'add':['right_ctrl_sets']
    },

    'attach_ctrl_sets':{
        'add':['ctrl_sets'],
        'items':[]
    },

    # foot roll
    'foot_roll_ctrl_sets':{
        'add':['ctrl_sets'],
    },
    'left_foot_roll_ctrl_sets':{
        'add':['foot_roll_ctrl_sets'],
        'items':[]
    },
    'right_foot_roll_ctrl_sets':{
        'add':['foot_roll_ctrl_sets'],
        'items':[]
    },
    'left_foot_roll_connect_sets':{
        'add':['left_foot_roll_ctrl_sets'],
        'items':[]
    },
    'right_foot_roll_connect_sets':{
        'add':['right_foot_roll_ctrl_sets'],
        'items':[]
    },

}

empty_sets = [sets for sets in create_sets.keys()]
[cmds.sets(em=True, n=sets) for sets in empty_sets if not cmds.objExists(sets)]

for sets in empty_sets:
    sets_settings = create_sets[sets]
    if sets_settings:
        if 'add' in sets_settings.keys():
            [cmds.sets(sets, add=add_item) for add_item in sets_settings['add']]

        if 'items' in sets_settings.keys():
            [cmds.sets(item, add=sets) for item in sets_settings['items'] if cmds.objExists(item)]

################################
# tweak controller shapes
mel.eval("""
select -r FK_Jaw_ctrl.cv[0:16] ;
move -r -os -wd 0 0 1381.101122 ;
scale -r -p 0cm 8882.897316cm 1619.748859cm 0.138988 0.138988 0.138988 ;
""")
