# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
except Exception:
    pass

import maya.cmds as cmds


# べ浮く用の値
TEX_RES_X = 4096
TEX_RES_Y = 4096
RAY_MIN = 5000
RAY_MAX = 5000

# テストベイク用の値
TEST_TEX_RES_SCALE = 1 / 4  # testは1/4サイズでベイクする
TEST_TEX_RES_X = 1024
TEST_TEX_RES_Y = 1024
TEST_RAY_MIN_VAL = 64
TEST_RAY_MAX_VAL = 256

# テストベイクの値を保持するための追加アトリビュート
GLP_TEST_RES_X_ATTR = 'GlpLmmTestResX'
GLP_TEST_RES_Y_ATTR = 'GlpLmmTestResY'
GLP_TEST_RAY_MIN_ATTR = 'GlpLmmTestRayMin'
GLP_TEST_RAY_MAX_ATTR = 'GlpLmmTestRayMax'

# ツール定義のプレフィックス・サフィックス
BAKE_LAYER_PREFIX = 'GlpBl_'
PREVIEW_MATERIAL_SUFFIX = '_GlpLmMtr_'
RESULT_COLORSET_SUFFIX = '_FINAL_COLOR'
AO_SAMPLER_SUFFIX = '_AoSampler'

# ベイク時に使用するライトを指定するためにbake_layerノードに追加するアトリビュート
GLP_LIGHT_SET_ATTR = 'glpLmmLightSet'

# turtleの定数
BAKE_ELM_STR = '$p'
BAKE_EXT_STR = '$e'
FULL_SHADING_STR = 'beauty'
ILLUMINATION_STR = 'tpIllumination'
INDIRECTION_STR = 'tpIndirectIllumination'

# gallopの仕様
MODEL_PREFIX = 'mdl_'
TEX_PREFIX = 'tex_'
TEX_OUTPUT_PATH = '/sourceimages/bake'
FBX_OUTPUT_DIRNAME = 'fbx'


# ベイク設定の初期値
# 旧ツールのデフォ値をcreate_setting_dict_str_by_bake_layer()で取得して作成
DEFAULT_SETTING_LIST = [
    {
        'attr': 'renderSelection',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'shadows',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'orthoRefl',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'alpha',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'viewDependent',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'backgroundColor',
        'type': 'float3',
        'value': [0.5, 0.5, 0.5],
    },
    {
        'attr': 'frontRange',
        'type': 'float',
        'value': 0.0,
    },
    {
        'attr': 'backRange',
        'type': 'float',
        'value': 200.0,
    },
    {
        'attr': 'frontBias',
        'type': 'float',
        'value': 0.0,
    },
    {
        'attr': 'backBias',
        'type': 'float',
        'value': -100.0,
    },
    {
        'attr': 'ignoreInconsistentNormals',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'considerTransparency',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'transparencyThreshold',
        'type': 'float',
        'value': 0.001,
    },
    {
        'attr': 'vbClamp',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'vbRgbMin',
        'type': 'float3',
        'value': [0.0, 0.0, 0.0],
    },
    {
        'attr': 'vbRgbMax',
        'type': 'float3',
        'value': [1.0, 1.0, 1.0],
    },
    {
        'attr': 'vbRgbScale',
        'type': 'float',
        'value': 1.0,
    },
    {
        'attr': 'vbAlphaScale',
        'type': 'float',
        'value': 1.0,
    },
    {
        'attr': 'vbAlphaMax',
        'type': 'float',
        'value': 1.0,
    },
    {
        'attr': 'vbVertexBias',
        'type': None,
        'value': 0.01,
    },
    {
        'attr': 'vbMinSamples',
        'type': 'long',
        'value': 2,
    },
    {
        'attr': 'vbMaxSamples',
        'type': 'long',
        'value': 16,
    },
    {
        'attr': 'vbFilter',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'vbFilterSize',
        'type': 'float',
        'value': 0.05,
    },
    {
        'attr': 'vbFilterShape',
        'type': 'float',
        'value': 1.1,
    },
    {
        'attr': 'vbFilterNormalDev',
        'type': 'float',
        'value': 6.0,
    },
    {
        'attr': 'vbSaveToColorSet',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'vbOverwriteColorSet',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'vbSaveToFile',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'tbUMin',
        'type': 'float',
        'value': 0.0,
    },
    {
        'attr': 'tbVMin',
        'type': 'float',
        'value': 0.0,
    },
    {
        'attr': 'tbUMax',
        'type': 'float',
        'value': 1.0,
    },
    {
        'attr': 'tbVMax',
        'type': 'float',
        'value': 1.0,
    },
    {
        'attr': 'tbResX',
        'type': None,
        'value': TEX_RES_X,
    },
    {
        'attr': 'tbResY',
        'type': None,
        'value': TEX_RES_Y,
    },
    {
        'attr': 'tbEdgeDilation',
        'type': None,
        'value': 16,
    },
    {
        'attr': 'tbBilinearFilter',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'tbConservative',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'tbSaveToRenderView',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'tbSaveToFile',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'tbMerge',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'tbVisualize',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'fullShading',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'illumination',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'indirectIllumination',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'diffuse',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'specular',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'ambient',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'incandescence',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'albedo',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'sss',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'reflections',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'refractions',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'custom',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'rnm',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'rnmSampleType',
        'type': 'long',
        'value': 0,
    },
    {
        'attr': 'rnmAdjustIntensity',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'rnmSamples',
        'type': 'long',
        'value': 100,
    },
    {
        'attr': 'lua',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'dirOcc',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'dirOccSamples',
        'type': 'long',
        'value': 100,
    },
    {
        'attr': 'dirOccExponent',
        'type': 'float',
        'value': 1.0,
    },
    {
        'attr': 'dirOccVector1',
        'type': 'float3',
        'value': [0.8164966106414795, 0.0, 0.5773502588272095],
    },
    {
        'attr': 'dirOccVector2',
        'type': 'float3',
        'value': [-0.40824827551841736, 0.7071067690849304, 0.5773502588272095],
    },
    {
        'attr': 'dirOccVector3',
        'type': 'float3',
        'value': [-0.40824827551841736, -0.7071067690849304, 0.5773502588272095],
    },
    {
        'attr': 'dirOccVector4',
        'type': 'float3',
        'value': [0.0, 0.0, 1.0],
    },
    {
        'attr': 'ptm',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'ptmSampleType',
        'type': 'long',
        'value': 2,
    },
    {
        'attr': 'ptmOutput',
        'type': 'long',
        'value': 0,
    },
    {
        'attr': 'ptmSamples',
        'type': 'long',
        'value': 100,
    },
    {
        'attr': 'sph',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'sphSignLess',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'sphSampleType',
        'type': 'long',
        'value': 2,
    },
    {
        'attr': 'sphSpaceType',
        'type': 'long',
        'value': 1,
    },
    {
        'attr': 'sphOutput',
        'type': 'long',
        'value': 0,
    },
    {
        'attr': 'sphSamples',
        'type': 'long',
        'value': 100,
    },
    {
        'attr': 'sphBands',
        'type': 'long',
        'value': 3,
    },
    {
        'attr': 'sphConeAngle',
        'type': 'float',
        'value': 360.0,
    },
    {
        'attr': 'normals',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'normalsFaceTangents',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'normalsUseBump',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'displacementAlpha',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'stencilBake',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'displacement',
        'type': 'bool',
        'value': False,
    },
    {
        'attr': 'displacementRemap',
        'type': 'bool',
        'value': True,
    },
    {
        'attr': 'displacementScale',
        'type': 'float',
        'value': 1.0,
    },
    {
        'attr': 'displacementOffset',
        'type': 'float',
        'value': 0.0,
    },
    {
        'attr': 'renderType',
        'type': 'enum',
        'value': 1,
    },
    {
        'attr': 'normalDirection',
        'type': 'enum',
        'value': 0,
    },
    {
        'attr': 'rangePreset',
        'type': 'enum',
        'value': 1,
    },
    {
        'attr': 'selectionMode',
        'type': 'enum',
        'value': 0,
    },
    {
        'attr': 'mismatchMode',
        'type': 'enum',
        'value': 0,
    },
    {
        'attr': 'envelopeMode',
        'type': 'enum',
        'value': 0,
    },
    {
        'attr': 'transferSpace',
        'type': 'enum',
        'value': 1,
    },
    {
        'attr': 'vbUseBlending',
        'type': 'enum',
        'value': 0,
    },
    {
        'attr': 'vbRgbBlend',
        'type': 'enum',
        'value': 0,
    },
    {
        'attr': 'vbAlphaBlend',
        'type': 'enum',
        'value': 0,
    },
    {
        'attr': 'vbSamplingMode',
        'type': 'enum',
        'value': 1,
    },
    {
        'attr': 'tbUvRange',
        'type': 'enum',
        'value': 0,
    },
    {
        'attr': 'tbImageFormat',
        'type': 'enum',
        'value': 0,
    },
    {
        'attr': 'tbWindingOrder',
        'type': 'enum',
        'value': 1,
    },
    {
        'attr': 'normalsCoordSys',
        'type': 'enum',
        'value': 0,
    },
    {
        'attr': 'normalsFlipChannel',
        'type': 'enum',
        'value': 0,
    },
    {
        'attr': 'camera',
        'type': 'string',
        'value': 'persp',
    },
    {
        'attr': 'vbDirectory',
        'type': 'string',
        'value': 'turtle/bakedTextures/',
    },
]


def create_setting_dict_by_bake_layer(bake_layer_node):
    """
    """

    attr_list = cmds.listAttr(bake_layer_node)
    result_list = []
    for attr in attr_list:
        try:
            type = cmds.getAttr('{}.'.format(bake_layer_node) + attr, type=True)
            value = cmds.getAttr('{}.'.format(bake_layer_node) + attr)
            result_list.append({'attr': attr, 'type': str(type), 'value': value})

        except Exception as e:
            print('skip: {} {}'.format(attr, e))

    return result_list


# def create_setting_dict_str_by_bake_layer(bake_layer_node):
#     """DEFAULT_SETTING_LISTを作成時に使用したメソッド
#     """

#     attr_list = cmds.listAttr(bake_layer_node)
#     result_list = []
#     for attr in attr_list:
#         try:
#             type = cmds.getAttr('{}.'.format(bake_layer_node) + attr, type=True)
#             value = cmds.getAttr('{}.'.format(bake_layer_node) + attr)

#             this_result = "{\n"
#             this_result += "    'attr': '{}',\n".format(attr)
#             this_result += "    'type': '{}',\n".format(type)
#             this_result += "    'value': {},\n".format(value)
#             this_result += "},"
#             result_list.append(this_result)

#         except Exception as e:
#             print('skip: {} {}'.format(attr, e))

#     return '\n'.join(result_list)
