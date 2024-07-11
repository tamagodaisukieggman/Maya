# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# UIの保存
OP_VAR_JSON_DIR = 'SnapImporterJsonDir'

# jsonキー
CONTAINER_NAME_KEY = '_containerName'
SNAP_VER_KEY = '_toolVer'
SNAP_LIST_KEY = '_snaps'
GRP_ID_LIST_KEY = '_grpIds'
ROOT_LABEL_LIST_KEY = '_rootLabels'
ROOT_TYPE_LIST_KEY = '_types'

OBJ_DATA_LIST_KEY = '_objDatas'
AXIS_OBJ_DATA_KEY = '_refObjData'
SANP_TIME_KEY = '_time'

OBJ_TYPE_KEY = 'Type'
OBJ_NAME_KEY = 'Name'
OBJ_GRP_ID_KEY = 'GrpId'
OBJ_IS_ROOT_KEY = 'IsRoot'

# データ型
FLOAT_DATA_LIST_KEY = 'Floats'
VEC3_DATA_LIST_KEY = 'Vec3s'
QUAT_DATA_LIST_KEY = 'Quats'
COLOR_DATA_LIST_KEY = 'Cols'
# 全データ型リスト
ALL_DATA_LIST_KEYS = [
    FLOAT_DATA_LIST_KEY,
    VEC3_DATA_LIST_KEY,
    QUAT_DATA_LIST_KEY,
    COLOR_DATA_LIST_KEY,
]

ATTR_LABEL = 'Label'
DATA_LABEL = 'Data'

# 記録アトリビュートキー
ATTR_WORLD_POS_KEY = 'wP'
ATTR_LOCAL_POS_KEY = 'lP'
ATTR_WORLD_ROT_KEY = 'wR'
ATTR_LOCAL_ROT_KEY = 'lR'
ATTR_WORLD_SCALE_KEY = 'wS'
ATTR_LOCAL_SCALE_KEY = 'lS'
ATTR_USE_ORG_LIGHT_KEY = 'UOL'
ATTR_ORG_LIGHT_DIR_KEY = 'OLD'
ATTR_CHEEK_PRETENSE_KEY = 'CPT'
ATTR_NOSE_PRETENSE_KEY = 'NPT'
ATTR_CYLINDER_BLEND_KEY = 'CB'
ATTR_CHARA_COLOR_KEY = 'CC'
ATTR_TOON_BRIGHT_KEY = 'TBC'
ATTR_TOON_DARK_KEY = 'TDC'
ATTR_HAIR_BLEND_KEY = 'HNB'
ATTR_CAM_FOV_KEY = 'FOV'
# 全記録アトリビュートとMayaのアトリビュートのdict
ALL_OBJ_ATTR_DICT = {
    ATTR_WORLD_POS_KEY: 'translate',
    ATTR_LOCAL_POS_KEY: 'translate',
    ATTR_WORLD_ROT_KEY: 'rotate',
    ATTR_LOCAL_ROT_KEY: 'rotate',
    ATTR_WORLD_SCALE_KEY: 'scale',
    ATTR_LOCAL_SCALE_KEY: 'scale',
    ATTR_USE_ORG_LIGHT_KEY: 'xUseOriginalDirectionalLight',
    ATTR_ORG_LIGHT_DIR_KEY: 'xOriginalDirectionalLightDir',
    ATTR_CHEEK_PRETENSE_KEY: 'xCheekPretenseThreshold',
    ATTR_NOSE_PRETENSE_KEY: 'xNosePretenseThreshold',
    ATTR_CYLINDER_BLEND_KEY: 'xTkglinderBlend',
    ATTR_HAIR_BLEND_KEY: 'xHairNormalBlend',
    ATTR_CHARA_COLOR_KEY: 'xCharaColor',
    ATTR_TOON_BRIGHT_KEY: 'xToonBrightColor',
    ATTR_TOON_DARK_KEY: 'xToonDarkColor',
    ATTR_CAM_FOV_KEY: 'focalLength',
}

# UnityとMayaのスケール
MAYA_TRANS_SCALE = 100

# DX11shaderのサフィックス
DX11_MAT_SUFFIX = '____dx11'

# ObjType
TYPE_OBJ = 'Object'
TYPE_LIGHT = 'Light'
TYPE_CAMERA = 'Camera'
TYPE_CHARA_MATERIAL = 'ChrMaterial'
# 全ObjTypeリスト
ALL_TYPES = [
    TYPE_OBJ,
    TYPE_LIGHT,
    TYPE_CAMERA,
    TYPE_CHARA_MATERIAL,
]

# Mayaでどのアトリビュートを再現するかのフラグ
FLAG_ROOT_TRANS = 'RootPosition'
FLAG_ROOT_ROT = 'RootRotation'
FLAG_ROOT_SCALE = 'RootScale'
FLAG_USE_ORG_LIGHT = 'MaterialDirLight'
FLAG_USE_CHAR_LIGHT = 'CharToonLight'

# Rootの再現座標選択
ROOT_ORIENT_AXIS_OBJ = 'RootOrientAxisObj'
ROOT_ORIENT_WORLD = 'RootOrientWorld'
ROOT_ORIENT_LOCAL = 'RootOrientLocal'
