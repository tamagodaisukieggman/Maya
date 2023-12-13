# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

import os
import traceback

# ---
# addRig
# ---
def file_import(char_id):
    mel.eval('file -import -type "mayaAscii"  -ignoreVersion -mergeNamespacesOnClash false -options "v=0;"  -pr  -importFrameRate true  -importTimeRange "override" "C:/perforce/wzdx/data/3d/03_motion/npc/{0}/adv/data/mdl_chr_{0}_01_body_rig_parts.ma";'.format(char_id))

def build_addRig(char_id):
    file_import(char_id)
    success, not_exists, error_log = const_rig(char_id)
    return success, not_exists, error_log

def const_rig(char_id):
    const_types = {0:'parent',
                   1:'point',
                   2:'orient',
                   3:'point/orient',
                   4:'point/orient/scale'}

    if 'npc001' == char_id:
        const_list = {'proxy_L_thigh':['data_L_thigh', 1],
                      'proxy_R_thigh':['data_R_thigh', 1],

                      'proxy_chest':['chest_base', 4],

                      'parker_01_ctrl_c':['proxy_parker_01_dyna', 4],
                      'parker_02_ctrl_c':['proxy_parker_02_dyna', 4],

                      'L_A_cloth_01_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_c':['proxy_L_B_cloth_03_dyna', 4],

                      'R_B_cloth_01_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_c':['proxy_R_B_cloth_03_dyna', 4],

                      'L_C_cloth_01_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_c':['proxy_L_C_cloth_03_dyna', 4],

                      'R_C_cloth_01_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_c':['proxy_R_C_cloth_03_dyna', 4],

                      }

    elif 'npc002' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_waist':['data_waist', 1],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_hip':['dummy_hip', 4],

                      'proxy_neck_Rot':['data_neck_Rot', 1],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_02_dyna_c':['proxy_cloth_02_dyna', 4],

                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],
                      'cloth_back_02_dyna_c':['proxy_cloth_back_02_dyna', 4],

                      }

    elif 'npc003' == char_id:
        const_list = {'proxy_hip':['dummy_hip', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],


                      }

    elif 'npc004' == char_id:
        const_list = {'proxy_hip':['dummy_hip', 4],

                      'R_bag_01_dyna_c':['proxy_R_bag_01_dyna', 4],

                      }

    elif 'npc005' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_waist':['dummy_waist', 4],
                      'proxy_chest':['dummy_chest', 4],

                      'tie_01_dyna_c':['proxy_tie_01_dyna', 4],

                      'L_A_dress_01_dyna_c':['proxy_L_A_dress_01_dyna', 4],
                      'L_A_dress_02_dyna_c':['proxy_L_A_dress_02_dyna', 4],
                      'L_A_dress_03_dyna_c':['proxy_L_A_dress_03_dyna', 4],

                      'R_A_dress_01_dyna_c':['proxy_R_A_dress_01_dyna', 4],
                      'R_A_dress_02_dyna_c':['proxy_R_A_dress_02_dyna', 4],
                      'R_A_dress_03_dyna_c':['proxy_R_A_dress_03_dyna', 4],

                      'L_B_dress_01_dyna_c':['proxy_L_B_dress_01_dyna', 4],
                      'L_B_dress_02_dyna_c':['proxy_L_B_dress_02_dyna', 4],
                      'L_B_dress_03_dyna_c':['proxy_L_B_dress_03_dyna', 4],

                      'R_B_dress_01_dyna_c':['proxy_R_B_dress_01_dyna', 4],
                      'R_B_dress_02_dyna_c':['proxy_R_B_dress_02_dyna', 4],
                      'R_B_dress_03_dyna_c':['proxy_R_B_dress_03_dyna', 4],

                      'L_C_dress_01_dyna_c':['proxy_L_C_dress_01_dyna', 4],
                      'L_C_dress_02_dyna_c':['proxy_L_C_dress_02_dyna', 4],
                      'L_C_dress_03_dyna_c':['proxy_L_C_dress_03_dyna', 4],

                      'R_C_dress_01_dyna_c':['proxy_R_C_dress_01_dyna', 4],
                      'R_C_dress_02_dyna_c':['proxy_R_C_dress_02_dyna', 4],
                      'R_C_dress_03_dyna_c':['proxy_R_C_dress_03_dyna', 4],


                      'dress_01_dyna_c':['proxy_dress_01_dyna', 4],
                      'dress_02_dyna_c':['proxy_dress_02_dyna', 4],
                      'dress_03_dyna_c':['proxy_dress_03_dyna', 4],

                      'dress_back_01_dyna_c':['proxy_dress_back_01_dyna', 4],
                      'dress_back_02_dyna_c':['proxy_dress_back_02_dyna', 4],
                      'dress_back_03_dyna_c':['proxy_dress_back_03_dyna', 4],

                      }

    elif 'npc006' == char_id:
        const_list = {'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],

                      }

    elif 'npc007' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],



                      }

    elif 'npc008' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],


                      }

    elif 'npc009' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 1],
                      'proxy_R_thigh':['data_R_thigh', 1],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_chest':['chest_base', 4],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      }

    elif 'npc010' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_chest':['chest_base', 4],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      }

    elif 'npc011' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_chest':['chest_base', 4],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_D_cloth_01_dyna_c':['proxy_L_D_cloth_01_dyna', 4],
                      'L_D_cloth_02_dyna_c':['proxy_L_D_cloth_02_dyna', 4],
                      'L_D_cloth_03_dyna_c':['proxy_L_D_cloth_03_dyna', 4],
                      'L_D_cloth_04_dyna_c':['proxy_L_D_cloth_04_dyna', 4],

                      'R_D_cloth_01_dyna_c':['proxy_R_D_cloth_01_dyna', 4],
                      'R_D_cloth_02_dyna_c':['proxy_R_D_cloth_02_dyna', 4],
                      'R_D_cloth_03_dyna_c':['proxy_R_D_cloth_03_dyna', 4],
                      'R_D_cloth_04_dyna_c':['proxy_R_D_cloth_04_dyna', 4],

                      'L_E_cloth_01_dyna_c':['proxy_L_E_cloth_01_dyna', 4],
                      'L_E_cloth_02_dyna_c':['proxy_L_E_cloth_02_dyna', 4],
                      'L_E_cloth_03_dyna_c':['proxy_L_E_cloth_03_dyna', 4],
                      'L_E_cloth_04_dyna_c':['proxy_L_E_cloth_04_dyna', 4],

                      'R_E_cloth_01_dyna_c':['proxy_R_E_cloth_01_dyna', 4],
                      'R_E_cloth_02_dyna_c':['proxy_R_E_cloth_02_dyna', 4],
                      'R_E_cloth_03_dyna_c':['proxy_R_E_cloth_03_dyna', 4],
                      'R_E_cloth_04_dyna_c':['proxy_R_E_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      }

    elif 'npc012' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_chest':['chest_base', 4],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_D_cloth_01_dyna_c':['proxy_L_D_cloth_01_dyna', 4],
                      'L_D_cloth_02_dyna_c':['proxy_L_D_cloth_02_dyna', 4],
                      'L_D_cloth_03_dyna_c':['proxy_L_D_cloth_03_dyna', 4],
                      'L_D_cloth_04_dyna_c':['proxy_L_D_cloth_04_dyna', 4],

                      'R_D_cloth_01_dyna_c':['proxy_R_D_cloth_01_dyna', 4],
                      'R_D_cloth_02_dyna_c':['proxy_R_D_cloth_02_dyna', 4],
                      'R_D_cloth_03_dyna_c':['proxy_R_D_cloth_03_dyna', 4],
                      'R_D_cloth_04_dyna_c':['proxy_R_D_cloth_04_dyna', 4],

                      'L_E_cloth_01_dyna_c':['proxy_L_E_cloth_01_dyna', 4],
                      'L_E_cloth_02_dyna_c':['proxy_L_E_cloth_02_dyna', 4],
                      'L_E_cloth_03_dyna_c':['proxy_L_E_cloth_03_dyna', 4],
                      'L_E_cloth_04_dyna_c':['proxy_L_E_cloth_04_dyna', 4],

                      'R_E_cloth_01_dyna_c':['proxy_R_E_cloth_01_dyna', 4],
                      'R_E_cloth_02_dyna_c':['proxy_R_E_cloth_02_dyna', 4],
                      'R_E_cloth_03_dyna_c':['proxy_R_E_cloth_03_dyna', 4],
                      'R_E_cloth_04_dyna_c':['proxy_R_E_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      }

    elif 'npc013' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_chest':['chest_base', 4],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'proxy_L_thigh':['dummy_L_thigh', 4],
                      'proxy_R_thigh':['dummy_R_thigh', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_D_cloth_01_dyna_c':['proxy_L_D_cloth_01_dyna', 4],
                      'L_D_cloth_02_dyna_c':['proxy_L_D_cloth_02_dyna', 4],
                      'L_D_cloth_03_dyna_c':['proxy_L_D_cloth_03_dyna', 4],
                      'L_D_cloth_04_dyna_c':['proxy_L_D_cloth_04_dyna', 4],

                      'R_D_cloth_01_dyna_c':['proxy_R_D_cloth_01_dyna', 4],
                      'R_D_cloth_02_dyna_c':['proxy_R_D_cloth_02_dyna', 4],
                      'R_D_cloth_03_dyna_c':['proxy_R_D_cloth_03_dyna', 4],
                      'R_D_cloth_04_dyna_c':['proxy_R_D_cloth_04_dyna', 4],

                      'L_E_cloth_01_dyna_c':['proxy_L_E_cloth_01_dyna', 4],
                      'L_E_cloth_02_dyna_c':['proxy_L_E_cloth_02_dyna', 4],
                      'L_E_cloth_03_dyna_c':['proxy_L_E_cloth_03_dyna', 4],
                      'L_E_cloth_04_dyna_c':['proxy_L_E_cloth_04_dyna', 4],

                      'R_E_cloth_01_dyna_c':['proxy_R_E_cloth_01_dyna', 4],
                      'R_E_cloth_02_dyna_c':['proxy_R_E_cloth_02_dyna', 4],
                      'R_E_cloth_03_dyna_c':['proxy_R_E_cloth_03_dyna', 4],
                      'R_E_cloth_04_dyna_c':['proxy_R_E_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_02_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_03_dyna', 4],

                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_02_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_03_dyna', 4],

                      'L_A_sleeve_01_dyna_c':['proxy_L_A_sleeve_01_dyna', 4],
                      'L_B_sleeve_01_dyna_c':['proxy_L_B_sleeve_01_dyna', 4],
                      'L_C_sleeve_01_dyna_c':['proxy_L_C_sleeve_01_dyna', 4],
                      'L_D_sleeve_01_dyna_c':['proxy_L_D_sleeve_01_dyna', 4],

                      'R_A_sleeve_01_dyna_c':['proxy_R_A_sleeve_01_dyna', 4],
                      'R_B_sleeve_01_dyna_c':['proxy_R_B_sleeve_01_dyna', 4],
                      'R_C_sleeve_01_dyna_c':['proxy_R_C_sleeve_01_dyna', 4],
                      'R_D_sleeve_01_dyna_c':['proxy_R_D_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'L_A_collar_01_dyna_c':['proxy_L_A_collar_01_dyna', 4],
                      'L_B_collar_01_dyna_c':['proxy_L_B_collar_01_dyna', 4],
                      'L_C_collar_01_dyna_c':['proxy_L_C_collar_01_dyna', 4],

                      'R_A_collar_01_dyna_c':['proxy_R_A_collar_01_dyna', 4],
                      'R_B_collar_01_dyna_c':['proxy_R_B_collar_01_dyna', 4],
                      'R_C_collar_01_dyna_c':['proxy_R_C_collar_01_dyna', 4],

                      'L_collar_front_01_dyna_c':['proxy_L_collar_front_01_dyna', 4],
                      'L_collar_back_01_dyna_c':['proxy_L_collar_back_01_dyna', 4],

                      'R_collar_front_01_dyna_c':['proxy_R_collar_front_01_dyna', 4],
                      'R_collar_back_01_dyna_c':['proxy_R_collar_back_01_dyna', 4],

                      'collar_back_01_dyna_c':['proxy_collar_back_01_dyna_c', 4],



                      }

    elif 'npc014' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_chest':['chest_base', 4],
                      'proxy_spine':['data_spine', 1],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'proxy_L_thigh':['dummy_L_thigh', 4],
                      'proxy_R_thigh':['dummy_R_thigh', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_D_cloth_01_dyna_c':['proxy_L_D_cloth_01_dyna', 4],
                      'L_D_cloth_02_dyna_c':['proxy_L_D_cloth_02_dyna', 4],
                      'L_D_cloth_03_dyna_c':['proxy_L_D_cloth_03_dyna', 4],
                      'L_D_cloth_04_dyna_c':['proxy_L_D_cloth_04_dyna', 4],

                      'R_D_cloth_01_dyna_c':['proxy_R_D_cloth_01_dyna', 4],
                      'R_D_cloth_02_dyna_c':['proxy_R_D_cloth_02_dyna', 4],
                      'R_D_cloth_03_dyna_c':['proxy_R_D_cloth_03_dyna', 4],
                      'R_D_cloth_04_dyna_c':['proxy_R_D_cloth_04_dyna', 4],

                      'L_E_cloth_01_dyna_c':['proxy_L_E_cloth_01_dyna', 4],
                      'L_E_cloth_02_dyna_c':['proxy_L_E_cloth_02_dyna', 4],
                      'L_E_cloth_03_dyna_c':['proxy_L_E_cloth_03_dyna', 4],
                      'L_E_cloth_04_dyna_c':['proxy_L_E_cloth_04_dyna', 4],

                      'R_E_cloth_01_dyna_c':['proxy_R_E_cloth_01_dyna', 4],
                      'R_E_cloth_02_dyna_c':['proxy_R_E_cloth_02_dyna', 4],
                      'R_E_cloth_03_dyna_c':['proxy_R_E_cloth_03_dyna', 4],
                      'R_E_cloth_04_dyna_c':['proxy_R_E_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_02_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_03_dyna', 4],

                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_02_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_03_dyna', 4],

                      'L_A_sleeve_01_dyna_c':['proxy_L_A_sleeve_01_dyna', 4],
                      'L_B_sleeve_01_dyna_c':['proxy_L_B_sleeve_01_dyna', 4],
                      'L_C_sleeve_01_dyna_c':['proxy_L_C_sleeve_01_dyna', 4],
                      'L_D_sleeve_01_dyna_c':['proxy_L_D_sleeve_01_dyna', 4],

                      'R_A_sleeve_01_dyna_c':['proxy_R_A_sleeve_01_dyna', 4],
                      'R_B_sleeve_01_dyna_c':['proxy_R_B_sleeve_01_dyna', 4],
                      'R_C_sleeve_01_dyna_c':['proxy_R_C_sleeve_01_dyna', 4],
                      'R_D_sleeve_01_dyna_c':['proxy_R_D_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'L_A_collar_01_dyna_c':['proxy_L_A_collar_01_dyna', 4],
                      'L_B_collar_01_dyna_c':['proxy_L_B_collar_01_dyna', 4],
                      'L_C_collar_01_dyna_c':['proxy_L_C_collar_01_dyna', 4],

                      'R_A_collar_01_dyna_c':['proxy_R_A_collar_01_dyna', 4],
                      'R_B_collar_01_dyna_c':['proxy_R_B_collar_01_dyna', 4],
                      'R_C_collar_01_dyna_c':['proxy_R_C_collar_01_dyna', 4],

                      'L_collar_front_01_dyna_c':['proxy_L_collar_front_01_dyna', 4],
                      'L_collar_back_01_dyna_c':['proxy_L_collar_back_01_dyna', 4],

                      'R_collar_front_01_dyna_c':['proxy_R_collar_front_01_dyna', 4],
                      'R_collar_back_01_dyna_c':['proxy_R_collar_back_01_dyna', 4],

                      'collar_back_01_dyna_c':['proxy_collar_back_01_dyna_c', 4],

                        'L_bag_01_dyna_c':['proxy_L_bag_01_dyna', 4],
                        'L_bag_02_dyna_c':['proxy_L_bag_02_dyna', 4],

                        'R_bag_01_dyna_c':['proxy_R_bag_01_dyna', 4],
                        'R_bag_02_dyna_c':['proxy_R_bag_02_dyna', 4],


                      }


    elif 'npc015' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_waist':['waist_base', 4],
                      'proxy_chest':['chest_base', 4],
                      'proxy_spine':['data_spine', 1],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'proxy_L_thigh':['dummy_L_thigh', 4],
                      'proxy_R_thigh':['dummy_R_thigh', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_D_cloth_01_dyna_c':['proxy_L_D_cloth_01_dyna', 4],
                      'L_D_cloth_02_dyna_c':['proxy_L_D_cloth_02_dyna', 4],
                      'L_D_cloth_03_dyna_c':['proxy_L_D_cloth_03_dyna', 4],
                      'L_D_cloth_04_dyna_c':['proxy_L_D_cloth_04_dyna', 4],

                      'R_D_cloth_01_dyna_c':['proxy_R_D_cloth_01_dyna', 4],
                      'R_D_cloth_02_dyna_c':['proxy_R_D_cloth_02_dyna', 4],
                      'R_D_cloth_03_dyna_c':['proxy_R_D_cloth_03_dyna', 4],
                      'R_D_cloth_04_dyna_c':['proxy_R_D_cloth_04_dyna', 4],

                      'L_E_cloth_01_dyna_c':['proxy_L_E_cloth_01_dyna', 4],
                      'L_E_cloth_02_dyna_c':['proxy_L_E_cloth_02_dyna', 4],
                      'L_E_cloth_03_dyna_c':['proxy_L_E_cloth_03_dyna', 4],
                      'L_E_cloth_04_dyna_c':['proxy_L_E_cloth_04_dyna', 4],

                      'R_E_cloth_01_dyna_c':['proxy_R_E_cloth_01_dyna', 4],
                      'R_E_cloth_02_dyna_c':['proxy_R_E_cloth_02_dyna', 4],
                      'R_E_cloth_03_dyna_c':['proxy_R_E_cloth_03_dyna', 4],
                      'R_E_cloth_04_dyna_c':['proxy_R_E_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_02_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_03_dyna', 4],

                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_02_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_03_dyna', 4],

                      'L_A_sleeve_01_dyna_c':['proxy_L_A_sleeve_01_dyna', 4],
                      'L_B_sleeve_01_dyna_c':['proxy_L_B_sleeve_01_dyna', 4],
                      'L_C_sleeve_01_dyna_c':['proxy_L_C_sleeve_01_dyna', 4],
                      'L_D_sleeve_01_dyna_c':['proxy_L_D_sleeve_01_dyna', 4],

                      'R_A_sleeve_01_dyna_c':['proxy_R_A_sleeve_01_dyna', 4],
                      'R_B_sleeve_01_dyna_c':['proxy_R_B_sleeve_01_dyna', 4],
                      'R_C_sleeve_01_dyna_c':['proxy_R_C_sleeve_01_dyna', 4],
                      'R_D_sleeve_01_dyna_c':['proxy_R_D_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'L_A_collar_01_dyna_c':['proxy_L_A_collar_01_dyna', 4],
                      'L_B_collar_01_dyna_c':['proxy_L_B_collar_01_dyna', 4],
                      'L_C_collar_01_dyna_c':['proxy_L_C_collar_01_dyna', 4],

                      'R_A_collar_01_dyna_c':['proxy_R_A_collar_01_dyna', 4],
                      'R_B_collar_01_dyna_c':['proxy_R_B_collar_01_dyna', 4],
                      'R_C_collar_01_dyna_c':['proxy_R_C_collar_01_dyna', 4],

                      'L_collar_front_01_dyna_c':['proxy_L_collar_front_01_dyna', 4],
                      'L_collar_back_01_dyna_c':['proxy_L_collar_back_01_dyna', 4],

                      'R_collar_front_01_dyna_c':['proxy_R_collar_front_01_dyna', 4],
                      'R_collar_back_01_dyna_c':['proxy_R_collar_back_01_dyna', 4],

                      'collar_back_01_dyna_c':['proxy_collar_back_01_dyna', 4],

                      'apron_01_dyna_c':['proxy_apron_01_dyna', 4],

                      'scarf_01_dyna_c':['proxy_scarf_01_dyna', 4],
                      'scarf_02_dyna_c':['proxy_scarf_02_dyna', 4],

                      'belly_01_dyna_c':['proxy_belly_01_dyna', 4],


                      }


    elif 'npc016' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_waist':['waist_base', 4],
                      'proxy_chest':['chest_base', 4],
                      'proxy_spine':['data_spine', 1],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'proxy_L_thigh':['dummy_L_thigh', 4],
                      'proxy_R_thigh':['dummy_R_thigh', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_02_dyna_c':['proxy_cloth_02_dyna', 4],

                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],
                      'cloth_back_02_dyna_c':['proxy_cloth_back_02_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_D_cloth_01_dyna_c':['proxy_L_D_cloth_01_dyna', 4],
                      'L_D_cloth_02_dyna_c':['proxy_L_D_cloth_02_dyna', 4],
                      'L_D_cloth_03_dyna_c':['proxy_L_D_cloth_03_dyna', 4],
                      'L_D_cloth_04_dyna_c':['proxy_L_D_cloth_04_dyna', 4],

                      'R_D_cloth_01_dyna_c':['proxy_R_D_cloth_01_dyna', 4],
                      'R_D_cloth_02_dyna_c':['proxy_R_D_cloth_02_dyna', 4],
                      'R_D_cloth_03_dyna_c':['proxy_R_D_cloth_03_dyna', 4],
                      'R_D_cloth_04_dyna_c':['proxy_R_D_cloth_04_dyna', 4],

                      'L_E_cloth_01_dyna_c':['proxy_L_E_cloth_01_dyna', 4],
                      'L_E_cloth_02_dyna_c':['proxy_L_E_cloth_02_dyna', 4],
                      'L_E_cloth_03_dyna_c':['proxy_L_E_cloth_03_dyna', 4],
                      'L_E_cloth_04_dyna_c':['proxy_L_E_cloth_04_dyna', 4],

                      'R_E_cloth_01_dyna_c':['proxy_R_E_cloth_01_dyna', 4],
                      'R_E_cloth_02_dyna_c':['proxy_R_E_cloth_02_dyna', 4],
                      'R_E_cloth_03_dyna_c':['proxy_R_E_cloth_03_dyna', 4],
                      'R_E_cloth_04_dyna_c':['proxy_R_E_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_02_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_03_dyna', 4],

                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_02_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_03_dyna', 4],

                      'L_A_sleeve_01_dyna_c':['proxy_L_A_sleeve_01_dyna', 4],
                      'L_B_sleeve_01_dyna_c':['proxy_L_B_sleeve_01_dyna', 4],
                      'L_C_sleeve_01_dyna_c':['proxy_L_C_sleeve_01_dyna', 4],
                      'L_D_sleeve_01_dyna_c':['proxy_L_D_sleeve_01_dyna', 4],

                      'R_A_sleeve_01_dyna_c':['proxy_R_A_sleeve_01_dyna', 4],
                      'R_B_sleeve_01_dyna_c':['proxy_R_B_sleeve_01_dyna', 4],
                      'R_C_sleeve_01_dyna_c':['proxy_R_C_sleeve_01_dyna', 4],
                      'R_D_sleeve_01_dyna_c':['proxy_R_D_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'L_A_collar_01_dyna_c':['proxy_L_A_collar_01_dyna', 4],
                      'L_B_collar_01_dyna_c':['proxy_L_B_collar_01_dyna', 4],
                      'L_C_collar_01_dyna_c':['proxy_L_C_collar_01_dyna', 4],

                      'R_A_collar_01_dyna_c':['proxy_R_A_collar_01_dyna', 4],
                      'R_B_collar_01_dyna_c':['proxy_R_B_collar_01_dyna', 4],
                      'R_C_collar_01_dyna_c':['proxy_R_C_collar_01_dyna', 4],

                      'L_collar_front_01_dyna_c':['proxy_L_collar_front_01_dyna', 4],
                      'L_collar_back_01_dyna_c':['proxy_L_collar_back_01_dyna', 4],

                      'R_collar_front_01_dyna_c':['proxy_R_collar_front_01_dyna', 4],
                      'R_collar_back_01_dyna_c':['proxy_R_collar_back_01_dyna', 4],

                      'collar_back_01_dyna_c':['proxy_collar_back_01_dyna', 4],

                      'apron_01_dyna_c':['proxy_apron_01_dyna', 4],

                      'scarf_01_dyna_c':['proxy_scarf_01_dyna', 4],
                      'scarf_02_dyna_c':['proxy_scarf_02_dyna', 4],

                      'belly_01_dyna_c':['proxy_belly_01_dyna', 4],

                      'L_bag_01_dyna_c':['proxy_L_bag_01_dyna', 4],
                      'L_bag_02_dyna_c':['proxy_L_bag_02_dyna', 4],

                      'R_bag_01_dyna_c':['proxy_R_bag_01_dyna', 4],
                      'R_bag_02_dyna_c':['proxy_R_bag_02_dyna', 4],

                      'F_brooch_01_dyna_c':['proxy_F_brooch_01_dyna', 4],


                      }


    elif 'npc017' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_waist':['waist_base', 4],
                      'proxy_chest':['chest_base', 4],
                      'proxy_spine':['data_spine', 1],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'proxy_L_thigh':['dummy_L_thigh', 4],
                      'proxy_R_thigh':['dummy_R_thigh', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_02_dyna_c':['proxy_cloth_02_dyna', 4],

                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],
                      'cloth_back_02_dyna_c':['proxy_cloth_back_02_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_D_cloth_01_dyna_c':['proxy_L_D_cloth_01_dyna', 4],
                      'L_D_cloth_02_dyna_c':['proxy_L_D_cloth_02_dyna', 4],
                      'L_D_cloth_03_dyna_c':['proxy_L_D_cloth_03_dyna', 4],
                      'L_D_cloth_04_dyna_c':['proxy_L_D_cloth_04_dyna', 4],

                      'R_D_cloth_01_dyna_c':['proxy_R_D_cloth_01_dyna', 4],
                      'R_D_cloth_02_dyna_c':['proxy_R_D_cloth_02_dyna', 4],
                      'R_D_cloth_03_dyna_c':['proxy_R_D_cloth_03_dyna', 4],
                      'R_D_cloth_04_dyna_c':['proxy_R_D_cloth_04_dyna', 4],

                      'L_E_cloth_01_dyna_c':['proxy_L_E_cloth_01_dyna', 4],
                      'L_E_cloth_02_dyna_c':['proxy_L_E_cloth_02_dyna', 4],
                      'L_E_cloth_03_dyna_c':['proxy_L_E_cloth_03_dyna', 4],
                      'L_E_cloth_04_dyna_c':['proxy_L_E_cloth_04_dyna', 4],

                      'R_E_cloth_01_dyna_c':['proxy_R_E_cloth_01_dyna', 4],
                      'R_E_cloth_02_dyna_c':['proxy_R_E_cloth_02_dyna', 4],
                      'R_E_cloth_03_dyna_c':['proxy_R_E_cloth_03_dyna', 4],
                      'R_E_cloth_04_dyna_c':['proxy_R_E_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_02_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_03_dyna', 4],

                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_02_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_03_dyna', 4],

                      'L_A_sleeve_01_dyna_c':['proxy_L_A_sleeve_01_dyna', 4],
                      'L_B_sleeve_01_dyna_c':['proxy_L_B_sleeve_01_dyna', 4],
                      'L_C_sleeve_01_dyna_c':['proxy_L_C_sleeve_01_dyna', 4],
                      'L_D_sleeve_01_dyna_c':['proxy_L_D_sleeve_01_dyna', 4],

                      'R_A_sleeve_01_dyna_c':['proxy_R_A_sleeve_01_dyna', 4],
                      'R_B_sleeve_01_dyna_c':['proxy_R_B_sleeve_01_dyna', 4],
                      'R_C_sleeve_01_dyna_c':['proxy_R_C_sleeve_01_dyna', 4],
                      'R_D_sleeve_01_dyna_c':['proxy_R_D_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'L_A_collar_01_dyna_c':['proxy_L_A_collar_01_dyna', 4],
                      'L_B_collar_01_dyna_c':['proxy_L_B_collar_01_dyna', 4],
                      'L_C_collar_01_dyna_c':['proxy_L_C_collar_01_dyna', 4],

                      'R_A_collar_01_dyna_c':['proxy_R_A_collar_01_dyna', 4],
                      'R_B_collar_01_dyna_c':['proxy_R_B_collar_01_dyna', 4],
                      'R_C_collar_01_dyna_c':['proxy_R_C_collar_01_dyna', 4],

                      'L_collar_front_01_dyna_c':['proxy_L_collar_front_01_dyna', 4],
                      'L_collar_back_01_dyna_c':['proxy_L_collar_back_01_dyna', 4],

                      'R_collar_front_01_dyna_c':['proxy_R_collar_front_01_dyna', 4],
                      'R_collar_back_01_dyna_c':['proxy_R_collar_back_01_dyna', 4],

                      'collar_back_01_dyna_c':['proxy_collar_back_01_dyna', 4],

                      'apron_01_dyna_c':['proxy_apron_01_dyna', 4],

                      'scarf_01_dyna_c':['proxy_scarf_01_dyna', 4],
                      'scarf_02_dyna_c':['proxy_scarf_02_dyna', 4],

                      'belly_01_dyna_c':['proxy_belly_01_dyna', 4],

                      'L_bag_01_dyna_c':['proxy_L_bag_01_dyna', 4],
                      'L_bag_02_dyna_c':['proxy_L_bag_02_dyna', 4],

                      'R_bag_01_dyna_c':['proxy_R_bag_01_dyna', 4],
                      'R_bag_02_dyna_c':['proxy_R_bag_02_dyna', 4],

                      'F_brooch_01_dyna_c':['proxy_F_brooch_01_dyna', 4],


                      }


    elif 'npc018' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_waist':['waist_base', 4],
                      'proxy_chest':['chest_base', 4],
                      'proxy_spine':['data_spine', 1],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'proxy_L_thigh':['dummy_L_thigh', 4],
                      'proxy_R_thigh':['dummy_R_thigh', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_02_dyna_c':['proxy_cloth_02_dyna', 4],

                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],
                      'cloth_back_02_dyna_c':['proxy_cloth_back_02_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_D_cloth_01_dyna_c':['proxy_L_D_cloth_01_dyna', 4],
                      'L_D_cloth_02_dyna_c':['proxy_L_D_cloth_02_dyna', 4],
                      'L_D_cloth_03_dyna_c':['proxy_L_D_cloth_03_dyna', 4],
                      'L_D_cloth_04_dyna_c':['proxy_L_D_cloth_04_dyna', 4],

                      'R_D_cloth_01_dyna_c':['proxy_R_D_cloth_01_dyna', 4],
                      'R_D_cloth_02_dyna_c':['proxy_R_D_cloth_02_dyna', 4],
                      'R_D_cloth_03_dyna_c':['proxy_R_D_cloth_03_dyna', 4],
                      'R_D_cloth_04_dyna_c':['proxy_R_D_cloth_04_dyna', 4],

                      'L_E_cloth_01_dyna_c':['proxy_L_E_cloth_01_dyna', 4],
                      'L_E_cloth_02_dyna_c':['proxy_L_E_cloth_02_dyna', 4],
                      'L_E_cloth_03_dyna_c':['proxy_L_E_cloth_03_dyna', 4],
                      'L_E_cloth_04_dyna_c':['proxy_L_E_cloth_04_dyna', 4],

                      'R_E_cloth_01_dyna_c':['proxy_R_E_cloth_01_dyna', 4],
                      'R_E_cloth_02_dyna_c':['proxy_R_E_cloth_02_dyna', 4],
                      'R_E_cloth_03_dyna_c':['proxy_R_E_cloth_03_dyna', 4],
                      'R_E_cloth_04_dyna_c':['proxy_R_E_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_02_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_03_dyna', 4],

                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_02_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_03_dyna', 4],

                      'L_A_sleeve_01_dyna_c':['proxy_L_A_sleeve_01_dyna', 4],
                      'L_B_sleeve_01_dyna_c':['proxy_L_B_sleeve_01_dyna', 4],
                      'L_C_sleeve_01_dyna_c':['proxy_L_C_sleeve_01_dyna', 4],
                      'L_D_sleeve_01_dyna_c':['proxy_L_D_sleeve_01_dyna', 4],

                      'R_A_sleeve_01_dyna_c':['proxy_R_A_sleeve_01_dyna', 4],
                      'R_B_sleeve_01_dyna_c':['proxy_R_B_sleeve_01_dyna', 4],
                      'R_C_sleeve_01_dyna_c':['proxy_R_C_sleeve_01_dyna', 4],
                      'R_D_sleeve_01_dyna_c':['proxy_R_D_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'L_A_collar_01_dyna_c':['proxy_L_A_collar_01_dyna', 4],
                      'L_B_collar_01_dyna_c':['proxy_L_B_collar_01_dyna', 4],
                      'L_C_collar_01_dyna_c':['proxy_L_C_collar_01_dyna', 4],

                      'R_A_collar_01_dyna_c':['proxy_R_A_collar_01_dyna', 4],
                      'R_B_collar_01_dyna_c':['proxy_R_B_collar_01_dyna', 4],
                      'R_C_collar_01_dyna_c':['proxy_R_C_collar_01_dyna', 4],

                      'L_collar_front_01_dyna_c':['proxy_L_collar_front_01_dyna', 4],
                      'L_collar_back_01_dyna_c':['proxy_L_collar_back_01_dyna', 4],

                      'R_collar_front_01_dyna_c':['proxy_R_collar_front_01_dyna', 4],
                      'R_collar_back_01_dyna_c':['proxy_R_collar_back_01_dyna', 4],

                      'collar_back_01_dyna_c':['proxy_collar_back_01_dyna', 4],

                      'apron_01_dyna_c':['proxy_apron_01_dyna', 4],

                      'scarf_01_dyna_c':['proxy_scarf_01_dyna', 4],
                      'scarf_02_dyna_c':['proxy_scarf_02_dyna', 4],

                      'belly_01_dyna_c':['proxy_belly_01_dyna', 4],

                      'L_bag_01_dyna_c':['proxy_L_bag_01_dyna', 4],
                      'L_bag_02_dyna_c':['proxy_L_bag_02_dyna', 4],

                      'R_bag_01_dyna_c':['proxy_R_bag_01_dyna', 4],
                      'R_bag_02_dyna_c':['proxy_R_bag_02_dyna', 4],

                      'F_brooch_01_dyna_c':['proxy_F_brooch_01_dyna', 4],

                      'proxy_necklace_01_dyna_c':['proxy_necklace_01_dyna', 4],
                      'proxy_necklace_02_dyna_c':['proxy_necklace_02_dyna', 4],

                      'proxy_center_cloth_01_dyna_c':['proxy_center_cloth_01_dyna', 4],

                      'proxy_L_cloth_01_dyna_c':['proxy_L_cloth_01_dyna', 4],
                      'proxy_center_cloth_01_dyna_c':['proxy_center_cloth_01_dyna', 4],

                      'proxy_belt_01_dyna_c':['proxy_belt_01_dyna', 4],
                      'proxy_belt_02_dyna_c':['proxy_belt_02_dyna', 4],
                      'proxy_belt_03_dyna_c':['proxy_belt_03_dyna', 4],


                      }


    elif 'npc019' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_waist':['waist_base', 4],
                      'proxy_chest':['chest_base', 4],
                      'proxy_spine':['data_spine', 1],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'proxy_L_thigh':['dummy_L_thigh', 4],
                      'proxy_R_thigh':['dummy_R_thigh', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_02_dyna_c':['proxy_cloth_02_dyna', 4],

                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],
                      'cloth_back_02_dyna_c':['proxy_cloth_back_02_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_D_cloth_01_dyna_c':['proxy_L_D_cloth_01_dyna', 4],
                      'L_D_cloth_02_dyna_c':['proxy_L_D_cloth_02_dyna', 4],
                      'L_D_cloth_03_dyna_c':['proxy_L_D_cloth_03_dyna', 4],
                      'L_D_cloth_04_dyna_c':['proxy_L_D_cloth_04_dyna', 4],

                      'R_D_cloth_01_dyna_c':['proxy_R_D_cloth_01_dyna', 4],
                      'R_D_cloth_02_dyna_c':['proxy_R_D_cloth_02_dyna', 4],
                      'R_D_cloth_03_dyna_c':['proxy_R_D_cloth_03_dyna', 4],
                      'R_D_cloth_04_dyna_c':['proxy_R_D_cloth_04_dyna', 4],

                      'L_E_cloth_01_dyna_c':['proxy_L_E_cloth_01_dyna', 4],
                      'L_E_cloth_02_dyna_c':['proxy_L_E_cloth_02_dyna', 4],
                      'L_E_cloth_03_dyna_c':['proxy_L_E_cloth_03_dyna', 4],
                      'L_E_cloth_04_dyna_c':['proxy_L_E_cloth_04_dyna', 4],

                      'R_E_cloth_01_dyna_c':['proxy_R_E_cloth_01_dyna', 4],
                      'R_E_cloth_02_dyna_c':['proxy_R_E_cloth_02_dyna', 4],
                      'R_E_cloth_03_dyna_c':['proxy_R_E_cloth_03_dyna', 4],
                      'R_E_cloth_04_dyna_c':['proxy_R_E_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_02_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_03_dyna', 4],

                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_02_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_03_dyna', 4],

                      'L_A_sleeve_01_dyna_c':['proxy_L_A_sleeve_01_dyna', 4],
                      'L_B_sleeve_01_dyna_c':['proxy_L_B_sleeve_01_dyna', 4],
                      'L_C_sleeve_01_dyna_c':['proxy_L_C_sleeve_01_dyna', 4],
                      'L_D_sleeve_01_dyna_c':['proxy_L_D_sleeve_01_dyna', 4],

                      'R_A_sleeve_01_dyna_c':['proxy_R_A_sleeve_01_dyna', 4],
                      'R_B_sleeve_01_dyna_c':['proxy_R_B_sleeve_01_dyna', 4],
                      'R_C_sleeve_01_dyna_c':['proxy_R_C_sleeve_01_dyna', 4],
                      'R_D_sleeve_01_dyna_c':['proxy_R_D_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'L_A_collar_01_dyna_c':['proxy_L_A_collar_01_dyna', 4],
                      'L_B_collar_01_dyna_c':['proxy_L_B_collar_01_dyna', 4],
                      'L_C_collar_01_dyna_c':['proxy_L_C_collar_01_dyna', 4],

                      'R_A_collar_01_dyna_c':['proxy_R_A_collar_01_dyna', 4],
                      'R_B_collar_01_dyna_c':['proxy_R_B_collar_01_dyna', 4],
                      'R_C_collar_01_dyna_c':['proxy_R_C_collar_01_dyna', 4],

                      'L_collar_front_01_dyna_c':['proxy_L_collar_front_01_dyna', 4],
                      'L_collar_back_01_dyna_c':['proxy_L_collar_back_01_dyna', 4],

                      'R_collar_front_01_dyna_c':['proxy_R_collar_front_01_dyna', 4],
                      'R_collar_back_01_dyna_c':['proxy_R_collar_back_01_dyna', 4],

                      'collar_back_01_dyna_c':['proxy_collar_back_01_dyna', 4],

                      'apron_01_dyna_c':['proxy_apron_01_dyna', 4],

                      'scarf_01_dyna_c':['proxy_scarf_01_dyna', 4],
                      'scarf_02_dyna_c':['proxy_scarf_02_dyna', 4],

                      'belly_01_dyna_c':['proxy_belly_01_dyna', 4],

                      'L_bag_01_dyna_c':['proxy_L_bag_01_dyna', 4],
                      'L_bag_02_dyna_c':['proxy_L_bag_02_dyna', 4],

                      'R_bag_01_dyna_c':['proxy_R_bag_01_dyna', 4],
                      'R_bag_02_dyna_c':['proxy_R_bag_02_dyna', 4],

                      'F_brooch_01_dyna_c':['proxy_F_brooch_01_dyna', 4],

                      'proxy_necklace_01_dyna_c':['proxy_necklace_01_dyna', 4],
                      'proxy_necklace_02_dyna_c':['proxy_necklace_02_dyna', 4],

                      'proxy_center_cloth_01_dyna_c':['proxy_center_cloth_01_dyna', 4],

                      'proxy_L_cloth_01_dyna_c':['proxy_L_cloth_01_dyna', 4],
                      'proxy_center_cloth_01_dyna_c':['proxy_center_cloth_01_dyna', 4],

                      'proxy_belt_01_dyna_c':['proxy_belt_01_dyna', 4],
                      'proxy_belt_02_dyna_c':['proxy_belt_02_dyna', 4],
                      'proxy_belt_03_dyna_c':['proxy_belt_03_dyna', 4],


                      }


    elif 'npc020' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_waist':['waist_base', 4],
                      'proxy_chest':['chest_base', 4],
                      'proxy_spine':['data_spine', 1],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'proxy_L_thigh':['dummy_L_thigh', 4],
                      'proxy_R_thigh':['dummy_R_thigh', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_02_dyna_c':['proxy_cloth_02_dyna', 4],

                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],
                      'cloth_back_02_dyna_c':['proxy_cloth_back_02_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_D_cloth_01_dyna_c':['proxy_L_D_cloth_01_dyna', 4],
                      'L_D_cloth_02_dyna_c':['proxy_L_D_cloth_02_dyna', 4],
                      'L_D_cloth_03_dyna_c':['proxy_L_D_cloth_03_dyna', 4],
                      'L_D_cloth_04_dyna_c':['proxy_L_D_cloth_04_dyna', 4],

                      'R_D_cloth_01_dyna_c':['proxy_R_D_cloth_01_dyna', 4],
                      'R_D_cloth_02_dyna_c':['proxy_R_D_cloth_02_dyna', 4],
                      'R_D_cloth_03_dyna_c':['proxy_R_D_cloth_03_dyna', 4],
                      'R_D_cloth_04_dyna_c':['proxy_R_D_cloth_04_dyna', 4],

                      'L_E_cloth_01_dyna_c':['proxy_L_E_cloth_01_dyna', 4],
                      'L_E_cloth_02_dyna_c':['proxy_L_E_cloth_02_dyna', 4],
                      'L_E_cloth_03_dyna_c':['proxy_L_E_cloth_03_dyna', 4],
                      'L_E_cloth_04_dyna_c':['proxy_L_E_cloth_04_dyna', 4],

                      'R_E_cloth_01_dyna_c':['proxy_R_E_cloth_01_dyna', 4],
                      'R_E_cloth_02_dyna_c':['proxy_R_E_cloth_02_dyna', 4],
                      'R_E_cloth_03_dyna_c':['proxy_R_E_cloth_03_dyna', 4],
                      'R_E_cloth_04_dyna_c':['proxy_R_E_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_02_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_03_dyna', 4],

                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_02_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_03_dyna', 4],

                      'L_A_sleeve_01_dyna_c':['proxy_L_A_sleeve_01_dyna', 4],
                      'L_B_sleeve_01_dyna_c':['proxy_L_B_sleeve_01_dyna', 4],
                      'L_C_sleeve_01_dyna_c':['proxy_L_C_sleeve_01_dyna', 4],
                      'L_D_sleeve_01_dyna_c':['proxy_L_D_sleeve_01_dyna', 4],

                      'R_A_sleeve_01_dyna_c':['proxy_R_A_sleeve_01_dyna', 4],
                      'R_B_sleeve_01_dyna_c':['proxy_R_B_sleeve_01_dyna', 4],
                      'R_C_sleeve_01_dyna_c':['proxy_R_C_sleeve_01_dyna', 4],
                      'R_D_sleeve_01_dyna_c':['proxy_R_D_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'L_A_collar_01_dyna_c':['proxy_L_A_collar_01_dyna', 4],
                      'L_B_collar_01_dyna_c':['proxy_L_B_collar_01_dyna', 4],
                      'L_C_collar_01_dyna_c':['proxy_L_C_collar_01_dyna', 4],

                      'R_A_collar_01_dyna_c':['proxy_R_A_collar_01_dyna', 4],
                      'R_B_collar_01_dyna_c':['proxy_R_B_collar_01_dyna', 4],
                      'R_C_collar_01_dyna_c':['proxy_R_C_collar_01_dyna', 4],

                      'L_collar_front_01_dyna_c':['proxy_L_collar_front_01_dyna', 4],
                      'L_collar_back_01_dyna_c':['proxy_L_collar_back_01_dyna', 4],

                      'R_collar_front_01_dyna_c':['proxy_R_collar_front_01_dyna', 4],
                      'R_collar_back_01_dyna_c':['proxy_R_collar_back_01_dyna', 4],

                      'collar_back_01_dyna_c':['proxy_collar_back_01_dyna', 4],

                      'apron_01_dyna_c':['proxy_apron_01_dyna', 4],

                      'scarf_01_dyna_c':['proxy_scarf_01_dyna', 4],
                      'scarf_02_dyna_c':['proxy_scarf_02_dyna', 4],

                      'belly_01_dyna_c':['proxy_belly_01_dyna', 4],

                      'L_bag_01_dyna_c':['proxy_L_bag_01_dyna', 4],
                      'L_bag_02_dyna_c':['proxy_L_bag_02_dyna', 4],

                      'R_bag_01_dyna_c':['proxy_R_bag_01_dyna', 4],
                      'R_bag_02_dyna_c':['proxy_R_bag_02_dyna', 4],

                      'F_brooch_01_dyna_c':['proxy_F_brooch_01_dyna', 4],

                      'proxy_necklace_01_dyna_c':['proxy_necklace_01_dyna', 4],
                      'proxy_necklace_02_dyna_c':['proxy_necklace_02_dyna', 4],

                      'proxy_center_cloth_01_dyna_c':['proxy_center_cloth_01_dyna', 4],

                      'proxy_L_cloth_01_dyna_c':['proxy_L_cloth_01_dyna', 4],
                      'proxy_center_cloth_01_dyna_c':['proxy_center_cloth_01_dyna', 4],

                      'proxy_belt_01_dyna_c':['proxy_belt_01_dyna', 4],
                      'proxy_belt_02_dyna_c':['proxy_belt_02_dyna', 4],
                      'proxy_belt_03_dyna_c':['proxy_belt_03_dyna', 4],

                      'L_collar_01_dyna_c':['proxy_L_collar_01_dyna', 4],



                      }

    elif 'npc021' == char_id:
        const_list = {'proxy_L_shin':['data_L_shin', 1],
                      'proxy_R_shin':['data_R_shin', 1],
                      'proxy_L_thigh':['data_L_thigh', 2],
                      'proxy_R_thigh':['data_R_thigh', 2],

                      'proxy_hip':['dummy_hip', 4],
                      'proxy_chest':['dummy_chest', 4],
                      'proxy_waist':['data_waist', 4],
                      'proxy_waist':['waist_base', 4],
                      'proxy_chest':['chest_base', 4],
                      'proxy_spine':['data_spine', 1],

                      'proxy_L_lowerarm':['dummy_L_lowerarm', 4],
                      'proxy_R_lowerarm':['dummy_R_lowerarm', 4],

                      'proxy_L_shoulder':['dummy_L_shoulder', 4],
                      'proxy_R_shoulder':['dummy_R_shoulder', 4],

                      'proxy_L_upperarm':['dummy_L_upperarm', 4],
                      'proxy_R_upperarm':['dummy_R_upperarm', 4],

                      'proxy_L_thigh':['dummy_L_thigh', 4],
                      'proxy_R_thigh':['dummy_R_thigh', 4],

                      'L_A_skirt_01_dyna_c':['proxy_L_A_skirt_01_dyna', 4],
                      'L_A_skirt_02_dyna_c':['proxy_L_A_skirt_02_dyna', 4],

                      'L_B_skirt_01_dyna_c':['proxy_L_B_skirt_01_dyna', 4],
                      'L_B_skirt_02_dyna_c':['proxy_L_B_skirt_02_dyna', 4],

                      'L_C_skirt_01_dyna_c':['proxy_L_C_skirt_01_dyna', 4],
                      'L_C_skirt_02_dyna_c':['proxy_L_C_skirt_02_dyna', 4],

                      'R_A_skirt_01_dyna_c':['proxy_R_A_skirt_01_dyna', 4],
                      'R_A_skirt_02_dyna_c':['proxy_R_A_skirt_02_dyna', 4],

                      'R_B_skirt_01_dyna_c':['proxy_R_B_skirt_01_dyna', 4],
                      'R_B_skirt_02_dyna_c':['proxy_R_B_skirt_02_dyna', 4],

                      'R_C_skirt_01_dyna_c':['proxy_R_C_skirt_01_dyna', 4],
                      'R_C_skirt_02_dyna_c':['proxy_R_C_skirt_02_dyna', 4],

                      'skirt_01_dyna_c':['proxy_skirt_01_dyna', 4],
                      'skirt_02_dyna_c':['proxy_skirt_02_dyna', 4],

                      'skirt_back_01_dyna_c':['proxy_skirt_back_01_dyna', 4],
                      'skirt_back_02_dyna_c':['proxy_skirt_back_02_dyna', 4],

                      'waistcloth_01_dyna_c':['proxy_waistcloth_01_dyna', 4],
                      'waistcloth_02_dyna_c':['proxy_waistcloth_02_dyna', 4],

                      'cloth_01_dyna_c':['proxy_cloth_01_dyna', 4],
                      'cloth_02_dyna_c':['proxy_cloth_02_dyna', 4],

                      'cloth_back_01_dyna_c':['proxy_cloth_back_01_dyna', 4],
                      'cloth_back_02_dyna_c':['proxy_cloth_back_02_dyna', 4],

                      'L_A_cloth_01_dyna_c':['proxy_L_A_cloth_01_dyna', 4],
                      'L_A_cloth_02_dyna_c':['proxy_L_A_cloth_02_dyna', 4],
                      'L_A_cloth_03_dyna_c':['proxy_L_A_cloth_03_dyna', 4],
                      'L_A_cloth_04_dyna_c':['proxy_L_A_cloth_04_dyna', 4],

                      'R_A_cloth_01_dyna_c':['proxy_R_A_cloth_01_dyna', 4],
                      'R_A_cloth_02_dyna_c':['proxy_R_A_cloth_02_dyna', 4],
                      'R_A_cloth_03_dyna_c':['proxy_R_A_cloth_03_dyna', 4],
                      'R_A_cloth_04_dyna_c':['proxy_R_A_cloth_04_dyna', 4],

                      'L_B_cloth_01_dyna_c':['proxy_L_B_cloth_01_dyna', 4],
                      'L_B_cloth_02_dyna_c':['proxy_L_B_cloth_02_dyna', 4],
                      'L_B_cloth_03_dyna_c':['proxy_L_B_cloth_03_dyna', 4],
                      'L_B_cloth_04_dyna_c':['proxy_L_B_cloth_04_dyna', 4],

                      'R_B_cloth_01_dyna_c':['proxy_R_B_cloth_01_dyna', 4],
                      'R_B_cloth_02_dyna_c':['proxy_R_B_cloth_02_dyna', 4],
                      'R_B_cloth_03_dyna_c':['proxy_R_B_cloth_03_dyna', 4],
                      'R_B_cloth_04_dyna_c':['proxy_R_B_cloth_04_dyna', 4],

                      'L_C_cloth_01_dyna_c':['proxy_L_C_cloth_01_dyna', 4],
                      'L_C_cloth_02_dyna_c':['proxy_L_C_cloth_02_dyna', 4],
                      'L_C_cloth_03_dyna_c':['proxy_L_C_cloth_03_dyna', 4],
                      'L_C_cloth_04_dyna_c':['proxy_L_C_cloth_04_dyna', 4],

                      'R_C_cloth_01_dyna_c':['proxy_R_C_cloth_01_dyna', 4],
                      'R_C_cloth_02_dyna_c':['proxy_R_C_cloth_02_dyna', 4],
                      'R_C_cloth_03_dyna_c':['proxy_R_C_cloth_03_dyna', 4],
                      'R_C_cloth_04_dyna_c':['proxy_R_C_cloth_04_dyna', 4],

                      'L_D_cloth_01_dyna_c':['proxy_L_D_cloth_01_dyna', 4],
                      'L_D_cloth_02_dyna_c':['proxy_L_D_cloth_02_dyna', 4],
                      'L_D_cloth_03_dyna_c':['proxy_L_D_cloth_03_dyna', 4],
                      'L_D_cloth_04_dyna_c':['proxy_L_D_cloth_04_dyna', 4],

                      'R_D_cloth_01_dyna_c':['proxy_R_D_cloth_01_dyna', 4],
                      'R_D_cloth_02_dyna_c':['proxy_R_D_cloth_02_dyna', 4],
                      'R_D_cloth_03_dyna_c':['proxy_R_D_cloth_03_dyna', 4],
                      'R_D_cloth_04_dyna_c':['proxy_R_D_cloth_04_dyna', 4],

                      'L_E_cloth_01_dyna_c':['proxy_L_E_cloth_01_dyna', 4],
                      'L_E_cloth_02_dyna_c':['proxy_L_E_cloth_02_dyna', 4],
                      'L_E_cloth_03_dyna_c':['proxy_L_E_cloth_03_dyna', 4],
                      'L_E_cloth_04_dyna_c':['proxy_L_E_cloth_04_dyna', 4],

                      'R_E_cloth_01_dyna_c':['proxy_R_E_cloth_01_dyna', 4],
                      'R_E_cloth_02_dyna_c':['proxy_R_E_cloth_02_dyna', 4],
                      'R_E_cloth_03_dyna_c':['proxy_R_E_cloth_03_dyna', 4],
                      'R_E_cloth_04_dyna_c':['proxy_R_E_cloth_04_dyna', 4],

                      'L_sleeve_01_dyna_c':['proxy_L_sleeve_01_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_02_dyna', 4],
                      'L_sleeve_02_dyna_c':['proxy_L_sleeve_03_dyna', 4],

                      'R_sleeve_01_dyna_c':['proxy_R_sleeve_01_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_02_dyna', 4],
                      'R_sleeve_02_dyna_c':['proxy_R_sleeve_03_dyna', 4],

                      'L_A_sleeve_01_dyna_c':['proxy_L_A_sleeve_01_dyna', 4],
                      'L_B_sleeve_01_dyna_c':['proxy_L_B_sleeve_01_dyna', 4],
                      'L_C_sleeve_01_dyna_c':['proxy_L_C_sleeve_01_dyna', 4],
                      'L_D_sleeve_01_dyna_c':['proxy_L_D_sleeve_01_dyna', 4],

                      'R_A_sleeve_01_dyna_c':['proxy_R_A_sleeve_01_dyna', 4],
                      'R_B_sleeve_01_dyna_c':['proxy_R_B_sleeve_01_dyna', 4],
                      'R_C_sleeve_01_dyna_c':['proxy_R_C_sleeve_01_dyna', 4],
                      'R_D_sleeve_01_dyna_c':['proxy_R_D_sleeve_01_dyna', 4],

                      'L_A_jacket_01_dyna_c':['proxy_L_A_jacket_01_dyna', 4],
                      'L_A_jacket_02_dyna_c':['proxy_L_A_jacket_02_dyna', 4],

                      'R_A_jacket_01_dyna_c':['proxy_R_A_jacket_01_dyna', 4],
                      'R_A_jacket_02_dyna_c':['proxy_R_A_jacket_02_dyna', 4],

                      'L_B_jacket_01_dyna_c':['proxy_L_B_jacket_01_dyna', 4],
                      'L_B_jacket_02_dyna_c':['proxy_L_B_jacket_02_dyna', 4],

                      'R_B_jacket_01_dyna_c':['proxy_R_B_jacket_01_dyna', 4],
                      'R_B_jacket_02_dyna_c':['proxy_R_B_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'R_C_jacket_01_dyna_c':['proxy_R_C_jacket_01_dyna', 4],
                      'R_C_jacket_02_dyna_c':['proxy_R_C_jacket_02_dyna', 4],

                      'L_C_jacket_01_dyna_c':['proxy_L_C_jacket_01_dyna', 4],
                      'L_C_jacket_02_dyna_c':['proxy_L_C_jacket_02_dyna', 4],

                      'L_A_collar_01_dyna_c':['proxy_L_A_collar_01_dyna', 4],
                      'L_B_collar_01_dyna_c':['proxy_L_B_collar_01_dyna', 4],
                      'L_C_collar_01_dyna_c':['proxy_L_C_collar_01_dyna', 4],

                      'R_A_collar_01_dyna_c':['proxy_R_A_collar_01_dyna', 4],
                      'R_B_collar_01_dyna_c':['proxy_R_B_collar_01_dyna', 4],
                      'R_C_collar_01_dyna_c':['proxy_R_C_collar_01_dyna', 4],

                      'L_collar_front_01_dyna_c':['proxy_L_collar_front_01_dyna', 4],
                      'L_collar_back_01_dyna_c':['proxy_L_collar_back_01_dyna', 4],

                      'R_collar_front_01_dyna_c':['proxy_R_collar_front_01_dyna', 4],
                      'R_collar_back_01_dyna_c':['proxy_R_collar_back_01_dyna', 4],

                      'collar_back_01_dyna_c':['proxy_collar_back_01_dyna', 4],

                      'apron_01_dyna_c':['proxy_apron_01_dyna', 4],

                      'scarf_01_dyna_c':['proxy_scarf_01_dyna', 4],
                      'scarf_02_dyna_c':['proxy_scarf_02_dyna', 4],

                      'belly_01_dyna_c':['proxy_belly_01_dyna', 4],

                      'L_bag_01_dyna_c':['proxy_L_bag_01_dyna', 4],
                      'L_bag_02_dyna_c':['proxy_L_bag_02_dyna', 4],

                      'R_bag_01_dyna_c':['proxy_R_bag_01_dyna', 4],
                      'R_bag_02_dyna_c':['proxy_R_bag_02_dyna', 4],

                      'F_brooch_01_dyna_c':['proxy_F_brooch_01_dyna', 4],

                      'proxy_necklace_01_dyna_c':['proxy_necklace_01_dyna', 4],
                      'proxy_necklace_02_dyna_c':['proxy_necklace_02_dyna', 4],

                      'proxy_center_cloth_01_dyna_c':['proxy_center_cloth_01_dyna', 4],

                      'proxy_L_cloth_01_dyna_c':['proxy_L_cloth_01_dyna', 4],
                      'proxy_center_cloth_01_dyna_c':['proxy_center_cloth_01_dyna', 4],

                      'proxy_belt_01_dyna_c':['proxy_belt_01_dyna', 4],
                      'proxy_belt_02_dyna_c':['proxy_belt_02_dyna', 4],
                      'proxy_belt_03_dyna_c':['proxy_belt_03_dyna', 4],

                      'L_collar_01_dyna_c':['proxy_L_collar_01_dyna', 4],

                      }


    error_log=[]

    not_exists={}
    success={}
    for ctrl, jnt in const_list.items():
        try:
            if cmds.objExists(ctrl) and cmds.objExists(jnt[0]):
                if jnt[1] == 0:
                    cmds.parentConstraint(ctrl, jnt[0], w=1, mo=1)
                    success[ctrl]=[jnt[0],'parent']
                elif jnt[1] == 1:
                    cmds.pointConstraint(ctrl, jnt[0], w=1, mo=1)
                    success[ctrl]=[jnt[0],'point']
                elif jnt[1] == 2:
                    cmds.orientConstraint(ctrl, jnt[0], w=1, mo=1)
                    success[ctrl]=[jnt[0],'orient']
                elif jnt[1] == 3:
                    cmds.pointConstraint(ctrl, jnt[0], w=1, mo=1)
                    cmds.orientConstraint(ctrl, jnt[0], w=1, mo=1)
                    success[ctrl]=[jnt[0],'point/orient']
                elif jnt[1] == 4:
                    cmds.pointConstraint(ctrl, jnt[0], w=1, mo=1)
                    cmds.orientConstraint(ctrl, jnt[0], w=1, mo=1)
                    cmds.scaleConstraint(ctrl, jnt[0], w=1, mo=1)
                    success[ctrl]=[jnt[0],'point/orient/scale']
            else:
                not_exists[char_id]=[ctrl, jnt[0]]

        except Exception as e:
            error_log.append([e, ctrl, jnt])

    # proxy_chectの不具合対応
    # if cmds.objExists('proxy_chest') and cmds.objExists('dummy_chest'):
    try:
        cmds.pointConstraint('proxy_chest', 'dummy_chest', w=1, mo=1)
        cmds.orientConstraint('proxy_chest', 'dummy_chest', w=1, mo=1)
        cmds.scaleConstraint('proxy_chest', 'dummy_chest', w=1, mo=1)
        success['proxy_chest']=['dummy_chest','point/orient/scale']
    except Exception as e:
        error_log.append([e, ctrl, jnt])

    return success, not_exists, error_log


# success, not_exists, error_log = build_addRig('npc001')
