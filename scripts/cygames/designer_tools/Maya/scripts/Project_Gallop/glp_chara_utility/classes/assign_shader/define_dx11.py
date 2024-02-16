# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

script_dir_path = os.path.dirname(__file__)
classes_dir_path = os.path.dirname(script_dir_path)
root_dir_path = os.path.dirname(classes_dir_path).replace('\\', '/')
resource_dir_path = '{0}/_resource'.format(root_dir_path)

DIVIDE_FLAG = '____'
DX11_MATERIAL_SUFFIX = DIVIDE_FLAG + "dx11"
DX11_OUTLINE_MATERIAL_SUFFIX = DIVIDE_FLAG + "outlineDx11"
MAP_MATERIAL_SUFFIX = DIVIDE_FLAG + "map"
CHARA_LIGHT0 = 'charaLight0'
CHARA_LIGHT0_DX11_VECTOR = 'charaLight0_dx11Vector'

DX11_DIR_PATH = '{}/{}'.format(resource_dir_path, 'Dx11')
TEXTURE_DIR_PATH = '{}/{}'.format(resource_dir_path, 'Textures')
DX11_TMP_PATH = '{}/{}'.format(DX11_DIR_PATH, '_tmp')
DX11_OUTLINE_TMP_PATH = '{}/{}'.format(DX11_DIR_PATH, '_outline_tmp')

# ダミーテクスチャ群
ENV_TEXTURE_PATH = resource_dir_path + '/Textures/tex_chr_env000.tga'
BLACK_TEXTURE_PATH = resource_dir_path + '/Textures/tex_chr_black.tga'
GRAY_TEXTURE_PATH = resource_dir_path + '/Textures/tex_chr_gray.tga'
WHITE_TEXTURE_PATH = resource_dir_path + '/Textures/tex_chr_white.tga'
BASE_BLEND_TEXTURE_PATH = resource_dir_path + '/Textures/tex_chr_base_blend.tga'

# fileNodeのアトリビュート
DIFF_TEX_ATTR = 'mainTextureMap'
SHAD_TEX_ATTR = 'toonTextureMap'
BASE_TEX_ATTR = 'tripleMaskMap'
CTRL_TEX_ATTR = 'optionMaskMap'
DIRT_TEX_ATTR = 'dirtTextureMap'
EMI_TEX_ATTR = 'emissiveTextureMap'
ENV_TEX_ATTR = 'envTextureMap'
AREA_TEX_ATTR = 'maskColorTextureMap'
RFL_TEX_ATTR = 'reflectionTextureMap'
DITHER_TEX_ATTR = 'ditherTextureMap'

# DX11のデフォルトアトリビュートと値の初期値
DX11_DEFAULT_ATTR_DICT = {
    'xSpecularPower': 0.15,
    'xEnvRate': 1,
    'xEnvBias': 5,
    'xReflectionRate': 1,
    'xReflectionBias': 1,
    'xToonStep': 0.4,
    'xToonFeather': 0.001,
    'xUseOptionMaskMap': 1,
    'xRimStep': 0.15,
    'xRimFeather': 0.001,
    'xRimColorRGB': [89 / 255, 65 / 255, 55 / 255],
    'xRimColorA': 100 / 255,
    'xRimShadow': 2,
    'xRimSpecRate': 1,
    'xGlobalDirtColor': [89 / 255, 65 / 255, 55 / 255],
    'xGlobalDirtRimSpecularColor': [154 / 255, 115 / 255, 98 / 255],
    'xCutoff': 0.0,
    'xEmissiveColor': [1, 1, 1],
    'xDirtRate1': None,  # assign_dx11_shader側のuiの値を代入する
    'xDirtRate2': None,  # assign_dx11_shader側のuiの値を代入する
    'xDirtRate3': None  # assign_dx11_shader側のuiの値を代入する
}

# DX11のアトリビュートに刺さるテクスチャパス
DX11_DEFAULT_ATTR_PATH_INFO_DICT = {
    DIFF_TEX_ATTR: [WHITE_TEXTURE_PATH, None],
    SHAD_TEX_ATTR: [GRAY_TEXTURE_PATH, None],
    BASE_TEX_ATTR: [BLACK_TEXTURE_PATH, None],
    CTRL_TEX_ATTR: [BLACK_TEXTURE_PATH, None],
    DIRT_TEX_ATTR: [BLACK_TEXTURE_PATH, None],
    EMI_TEX_ATTR: [BLACK_TEXTURE_PATH, None],
    AREA_TEX_ATTR: [GRAY_TEXTURE_PATH, None],
    DITHER_TEX_ATTR: [BLACK_TEXTURE_PATH, None],
    ENV_TEX_ATTR: [ENV_TEXTURE_PATH, None]
}

# OUTLINE
OUTLINE_DX11_DEFAULT_ATTR_DICT = {
    'xOutlineWidth': 0.325,
    'xOutlineColorRGB': [0.125, 0.047, 0],
    'xOutlineColorA': 0.09803922,
    'xGlobalOutlineOffset': 1.0,
    'xGlobalOutlineWidth': 1.0,
    'xGlobalCameraFov': 15.0,
}

OUTLINE_DX11_DEFAULT_ATTR_PATH_INFO_DICT = {
    DIFF_TEX_ATTR: [None, None]
}

HAIR_MASK_COLOR_PARAM_DICT = {
    'xMaskColor': {
        'R1': [0.86, 0.7, 0.54], 'R2': [0.44, 1.0, 0.57],
        'G1': [0.93, 0.9, 1.0], 'G2': [0.0, 0.0, 0.0],
        'B1': [1.00, 0.439, 0.639], 'B2': [0.961, 0.788, 0.476]
    },
    'xMaskToonColor': {
        'R1': [0.81, 0.63, 0.52], 'R2': [0.26, 0.64, 0.61],
        'G1': [0.68, 0.59, 1.0], 'G2': [0.0, 0.0, 0.0],
        'B1': [0.698, 0.129, 0.412], 'B2': [0.839, 0.62, 0.302]
    }
}

EYE_MASK_COLOR_PARAM_DICT = {
    'xMaskColor': {
        'R1': [0.36, 0.17, 0.0], 'R2': [0.933, 0.753, 0.404],
        'G1': [1.0, 0.91, 0.73], 'G2': [0.64, 0.39, 0.11],
        'B1': [0.533, 0.278, 0.071], 'B2': [1.0, 0.82, 0.52]
    },
    'xMaskToonColor': {
        'R1': [1.0, 1.0, 1.0], 'R2': [1.0, 1.0, 1.0],
        'G1': [1.0, 1.0, 1.0], 'G2': [1.0, 1.0, 1.0],
        'B1': [1.0, 1.0, 1.0], 'B2': [1.0, 1.0, 1.0]
    }
}

FACE_MASK_COLOR_PARAM_DICT = {
    'xMaskColor': {
        'R1': [1.0, 1.0, 1.0], 'R2': [1.0, 1.0, 1.0],
        'G1': [1.0, 1.0, 1.0], 'G2': [0.357, 0.184, 0.141],
        'B1': [0.78, 0.533, 0.29], 'B2': [0.62, 0.322, 0.133]
    },
    'xMaskToonColor': {
        'R1': [1.0, 1.0, 1.0], 'R2': [1.0, 1.0, 1.0],
        'G1': [1.0, 1.0, 1.0], 'G2': [0.357, 0.184, 0.141],
        'B1': [0.78, 0.533, 0.29], 'B2': [0.62, 0.322, 0.133]
    }
}

BODY_MASK_COLOR_PARAM_DICT = {
    'xMaskColor': {
        'R1': [0.463, 1.0, 0.373], 'R2': [0.902, 0.745, 0.933],
        'G1': [1.0, 0.702, 0.608], 'G2': [0.569, 0.694, 1.0],
        'B1': [1.0, 0.325, 0.263], 'B2': [1.0, 0.950, 0.686]
    },
    'xMaskToonColor': {
        'R1': [0.251, 0.576, 0.259], 'R2': [0.514, 0.416, 0.839],
        'G1': [0.816, 0.388, 0.369], 'G2': [0.2, 0.431, 1.0],
        'B1': [0.525, 0.176, 0.145], 'B2': [0.957, 0.808, 0.482]
    }
}
