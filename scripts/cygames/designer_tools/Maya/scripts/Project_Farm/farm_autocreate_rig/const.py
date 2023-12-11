# -*- coding=utf-8 -*-
u"""
name: autocreate_rig/constant.py
data: 2021/8/31
ussage: priari 用 Rig 自動作成ツールの定数
version: 2.72
​
"""
from collections import OrderedDict
import os
import traceback
import re
from glob import glob
import csv
import codecs
from collections import OrderedDict
from logging import getLogger

import maya.api.OpenMaya as om
import maya.cmds as cmds

logger = getLogger(__name__)

PRIMARYJOINTNAME_LIST = ['root']
IGNOREJOINTNAME_LIST = ['root', 'twistarm']
ARMJOINTNAME_LIST = ['clavicle', 'upperarm', 'forearm', 'hand']
HANDJOINTNAME_LIST = ['ringroot']
HANDJOINTNAME_LIST.extend(['ring_00', 'ring_01', 'ring_02', 'ring_End'])
HANDJOINTNAME_LIST.extend(['pinky_00', 'pinky_01', 'pinky_02', 'pinky_End'])
HANDJOINTNAME_LIST.extend(['middle_00', 'middle_01', 'middle_02', 'middle_End'])
HANDJOINTNAME_LIST.extend(['index_00', 'index_01', 'index_02', 'index_End'])
HANDJOINTNAME_LIST.extend(['thumb_00', 'thumb_01', 'thumb_02', 'thumb_End'])
LEGJOINTNAME_LIST = ['upperleg', 'foreleg', 'foot', 'toe', 'toe_End']
C_JOINTNAME_LIST = ['pelvis', 'hip', 'spine', 'chest', 'neck', 'head', 'head_End']
PRIMARYJOINTNAME_LIST.extend(ARMJOINTNAME_LIST)
PRIMARYJOINTNAME_LIST.extend(['ringroot', 'ring', 'pinky', 'middle', 'index', 'thumb'])
PRIMARYJOINTNAME_LIST.extend(LEGJOINTNAME_LIST)
PRIMARYJOINTNAME_LIST.extend(C_JOINTNAME_LIST)
SECONDARYJOINTNAME_LIST = ['tail', 'skirt', 'hair', 'mant', 'wing', 'sleeve', 'bust']
SIKIGNOREJOINTNAME_LIST = ['upperarm', 'forearm', 'hand', 'upperleg', 'foreleg']
SIKIGNOREJOINTNAME_LIST.extend(SECONDARYJOINTNAME_LIST)
SIKIGNOREJOINTNAME_LIST.extend(HANDJOINTNAME_LIST)
SIKIGNOREJOINTNAME_LIST.extend(IGNOREJOINTNAME_LIST)

# pin_type = ['ringroot', 'ring', 'pinky', 'middle', 'index', 'thumb']
# octahedron_type = ['forearm', 'foreleg']
# vcroos_type = ['hand']
# hcroos_type = ['foot', 'pelvis']

SIZE_DICT = {
    'M': {'value': 1.0, 'index': 0},
    'XS': {'value': 0.9, 'index': 1},
    'S': {'value': 0.95, 'index': 2},
    'L': {'value': 1.04, 'index': 3},
    'S_farm': {'value': 0.89, 'index': 4},
    'L_farm': {'value': 1.07, 'index': 5},
}
SIZE_ENUM_STR = ':'.join(sorted(SIZE_DICT, key=lambda k: SIZE_DICT[k]['index']))

# v2.1~: DUMMY_SECONDARY_LISTに bust を追加
DUMMY_SECONDARY_LIST = ['tail', 'skirt', 'hair', 'mant', 'wing', 'bust']
DUMMY_LIST = ['chest', 'hip', 'head', 'spine', 'neck']

WIRE_GRP = None
FILE_PATH = 'template/template_ctrl_wire.mb'
WIRE_NAMESPACE = 'Template_create_wire'
WIRE_TYPE = dict(
    ROOT='root_wire',
    OCTAHEDRON='octahedron_wire',
    IKFK='ikfk_wire',
    PIN='pin_wire',
    H_CROSS='h_cross_wire',
    V_CROSS='v_cross_wire',
    CUBE='cube_wire',
    TAIL='tail_wire',
    SPHERE='sphere_wire',
)

SUFFIX_CTRL = "_CTRL"
SUFFIX_NULL = "_null"
SUFFIX_OFFSET = "_offset"
PREFIX_WEAPON = "wpn_"
PREFIX_SIM = "SIM"

ROOTJOINTNAME = 'root'
ROOTCTRLNAME = ROOTJOINTNAME + SUFFIX_CTRL
ROOTNULLNAME = ROOTJOINTNAME + SUFFIX_NULL
GROUPJOINTNAME = 'grp_joint'
GROUPMESHNAME = 'grp_mesh'
GROUPRIGNAME = 'grp_rig'
GROUPSIKNAME = 'grp_SplineIK'
GROUPDUMNAME = 'grp_Dummy'
GROUPCTRLNAME = 'grp' + SUFFIX_CTRL

L_MANTLENAME = 'L_mant_00'
R_MANTLENAME = 'R_mant_00'

L_SLEEVENAME = 'L_sleeve'
R_SLEEVENAME = 'R_sleeve'

HEADJOINTNAME = 'C_head'
CHESTJOINTNAME = 'C_chest'
HIPJOINTNAME = 'C_hip'

# Extra Attribute dict
ATTR_BODYSCALE = "body_scale"
ATTR_CHARSIZE = "character_size"
ATTR_SCALEFACTOR = "scaleFactor"
SCALEFACTOR_DICT = {"default": [1.0, 1.0, 1.0], "1.5": [1.5, 1.5, 1.5]}
ENUM_STRINGS = ":".join(list(SCALEFACTOR_DICT.keys()))
ATTR_ORIGNAME = "origName"

ATTR_DICT = OrderedDict()
min_scale = SIZE_DICT['S_farm']['value']
max_scale = SIZE_DICT['L_farm']['value']
ATTR_DICT.update({ATTR_BODYSCALE: dict(ln=ATTR_BODYSCALE, at="float", dv=1, min=min_scale, max=max_scale, k=False)})
ATTR_DICT.update({ATTR_CHARSIZE: dict(ln=ATTR_CHARSIZE, at="enum", en=SIZE_ENUM_STR, dv=0, k=False)})
ATTR_DICT.update({ATTR_SCALEFACTOR: dict(ln=ATTR_SCALEFACTOR, at="enum", en=ENUM_STRINGS, dv=0, k=False)})
ATTR_DICT.update({ATTR_ORIGNAME: dict(ln=ATTR_ORIGNAME, dt="string", k=False)})

# Set DrivenKey list : bow_CTRL 武器、FIX@3/11 弓のドリブンキーの向きにつきまして にて変更
DRIVEN_KEY_LIST = [[10, 0], [22, 1], [40, 5]]

# 正規表現
ID_PATTERN = r"(mdl)_(unt|avt)_.*"
WPN_ID_PATTERN = r"(mdl)_(wpn|prp)_.*"
WPN_GROUP_PATTERN = r"(wpn|prp)[0-9]?"

DUMMY = 'Dummy_'
RIG_LAYERNAME = "unit_rig"
UI_SELECTION_DICT = {}

DEBUG_DICT = OrderedDict()