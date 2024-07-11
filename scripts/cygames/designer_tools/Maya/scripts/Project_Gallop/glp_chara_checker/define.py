# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


BODY_DEFFERENCE_TARGET_SUFFIX_LIST = [
    '_Height_SS',
    '_Height_L',
    '_Height_LL',
    '_Shape_1',
    '_Shape_2',
    '_Bust_SS',
    '_Bust_S',
    '_Bust_L',
    '_Bust_LL',
]

CLOTH_JOINT_PREFIX_LIST = ['Sp_', 'Ex_', 'Tp_', 'Pc_']
CLOTH_JOINT_LIST = ['Tail'] + CLOTH_JOINT_PREFIX_LIST
CLOTH_JOINT_PARENT_DICT = {
    'Ne': 'Neck',
    'Ch': 'Chest',
    'Wa': 'Waist',
    'Hi': 'Hip',
    'Th': 'Thigh',
    'Kn': 'Knee',
    'An': 'Ankle',
    'Sh': 'Shoulder',
    'Ar': 'Arm',
    'El': 'Elbow',
    'Wr': 'Wrist',
    'Si': 'Spine',
    'So': 'ShoulderRoll',
    'Ao': 'ArmRoll',
    'He': 'Head',
}

EYE_UV_SET_SHELL_COUNT = 2

# Mini faceのパス
MINI_FACE_PATH = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/mini/head/mchr0001_00/scenes/mdl_mchr0001_00_face0.ma'

# フェイシャル向けデータのCSVパス
FACIAL_CNT_CSV = 'C:/tkgpublic/designer_tools/Maya/scripts/Project_Gallop/glp_chara_facial_tool/resource/facial_controller_info.csv'
FACIAL_TARGET_CSV = 'C:/tkgpublic/designer_tools/Maya/scripts/Project_Gallop/glp_chara_facial_tool/resource/facial_target_info.csv'

# Mayaのアトリビュート上では表示しきれない、微小値などの許容値
TORELANCE = 0.001

# NeckEdgeSet名
NECK_EDGE_SET_NAME = 'NeckEdgeSet'
HEIGHT_SS_SUFFIX = '_Height_SS'
HEIGHT_L_SUFFIX = '_Height_L'

# 目用のロケーター
SPECIFIC_EYE_LOCATOR = [
    "Eye_base_info_L",
    "Eye_base_info_R",
    "Eye_big_info_L",
    "Eye_big_info_R",
    "Eye_small_info_L",
    "Eye_small_info_R",
    "Eye_kira_info"
]

# フェイシャルのシンメトリーなフレーム
FACIAL_SYMMETRY_CHECK_DATA = {
    'eyebrow': {
        'controllers': [
            'Eyebrow_01_L_Ctrl', 'Eyebrow_02_L_Ctrl', 'Eyebrow_03_L_Ctrl', 'Eyebrow_04_L_Ctrl',
            'Eyebrow_sub_01_L_Ctrl'
        ],
        'frames': [
            0, 30, 32, 34, 36, 70, 100, 130, 160, 190, 192, 220, 250, 280, 310, 380, 382, 450, 452, 454, 456
        ]
    },
    'eye': {
        'controllers': [
            'Eye_L_Ctrl', 'Eyelashes_L_Ctrl',
            'Eye_double_01_L_Ctrl', 'Eye_double_02_L_Ctrl',
            'Eye_middle_01_L_Ctrl',
            'Eye_up_01_L_Ctrl', 'Eye_up_02_L_Ctrl', 'Eye_up_03_L_Ctrl', 'Eye_up_04_L_Ctrl', 'Eye_up_05_L_Ctrl',
            'Eye_up_11_L_Ctrl', 'Eye_up_12_L_Ctrl', 'Eye_up_13_L_Ctrl', 'Eye_up_14_L_Ctrl', 'Eye_up_15_L_Ctrl',
            'Eye_sub_01_L_Ctrl', 'Eye_sub_02_L_Ctrl', 'Eye_sub_03_L_Ctrl', 'Eye_sub_04_L_Ctrl',
            'Eye_bottom_01_L_Ctrl', 'Eye_bottom_02_L_Ctrl', 'Eye_bottom_03_L_Ctrl', 'Eye_bottom_04_L_Ctrl',
            'Eye_tear_attach_01_L_Ctrl', 'Eye_bottom_02_L_Ctrl', 'Eye_bottom_03_L_Ctrl'
        ],
        'frames': [
            0, 4, 6, 8, 10, 32, 34, 36, 38, 70, 100, 160, 190, 192, 194, 220, 280, 310, 382, 400, 440, 442, 444, 452
        ]
    },
    'mouth': {
        'controllers': [
            'Mouth_up_01_L_Ctrl', 'Mouth_up_02_L_Ctrl', 'Mouth_up_03_L_Ctrl',
            'Mouth_middle_L_Ctrl',
            'Mouth_bottom_01_L_Ctrl', 'Mouth_bottom_02_L_Ctrl', 'Mouth_bottom_03_L_Ctrl'
        ],
        'frames': [
            0, 2, 30, 32, 34, 38, 40, 70, 72, 100, 130, 160, 190, 192, 220, 250, 310, 340, 342, 344,
            346, 348, 350, 352, 354, 356, 358, 360, 362, 364, 366, 372, 374, 380, 382, 400, 458
        ]
    },
}
