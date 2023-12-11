# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except:
    pass

import os
import re

import maya.cmds as cmds
import maya.mel as mel
from ..add_chara_info_obj import add_chara_info_obj

from ....base_common import utility as base_utility

from ....farm_common.classes.info import chara_info
from ....farm_common.utility import model_define
from ....farm_common.utility import model_mesh_finder
from ....farm_common.utility import model_texture_finder

reload(add_chara_info_obj)
reload(model_define)
reload(model_mesh_finder)
reload(model_texture_finder)


# ==================================================
def get_original_cgfx_file_name(cgfx_material_name):

    if cgfx_material_name.find('outline') >= 0:
        return 'CharacterOutline.cgfx'

    original_file_name = ''

    if cgfx_material_name.find('face') >= 0:
        original_file_name = 'CharacterToonFaceTSERDefault.cgfx'
    elif cgfx_material_name.find('brow') >= 0:
        original_file_name = 'CharacterToonFaceTSERDefault.cgfx'
    elif cgfx_material_name.find('eye') >= 0:
        original_file_name = 'CharacterToonEyeT.cgfx'
    elif cgfx_material_name.find('hair') >= 0:
        if cgfx_material_name.find('Alpha') > -1:
            original_file_name = 'CharacterAlphaToonHairTSERDefault0.cgfx'
        else:
            original_file_name = 'CharacterToonHairTSERDefault.cgfx'
    else:
        if cgfx_material_name.find('Alpha') > -1:
            original_file_name = 'CharacterAlphaToonTSERDefault0.cgfx'
        else:
            original_file_name = 'CharacterToonTSERDefault.cgfx'

    if original_file_name == '':
        return ''
    else:
        return original_file_name


# ==================================================
def get_default_texture_dict(default_texture_path):

    env_texture_name = 'tex_chr_env000.tga'
    black_texture_name = 'tex_chr_black.tga'
    gray_texture_name = 'tex_chr_gray.tga'
    white_texture_name = 'tex_chr_white.tga'
    base_blend_texture_name = 'tex_chr_base_blend.tga'

    attr_tex_dict = {
        '_MainTex': os.path.join(default_texture_path, white_texture_name),
        '_TripleMaskMap': os.path.join(default_texture_path, black_texture_name),
        '_ToonMap': os.path.join(default_texture_path, gray_texture_name),
        '_OptionMaskMap': os.path.join(default_texture_path, black_texture_name),
        '_DirtTex': os.path.join(default_texture_path, black_texture_name),
        '_EmissiveTex': os.path.join(default_texture_path, black_texture_name),
        '_MaskColorTex': os.path.join(default_texture_path, gray_texture_name),
        '_DitherTex': os.path.join(default_texture_path, black_texture_name),
        '_EnvMap': os.path.join(default_texture_path, env_texture_name),
    }

    return attr_tex_dict


# ==================================================
def get_texture_dict(default_material, texture_root_path):

    texture_list = model_texture_finder.get_texture_list_from_material(default_material)
    attr_tex_dict = {}
    for texture in texture_list:

        tex_path = os.path.join(texture_root_path, texture)

        if not os.path.exists(tex_path):
            continue

        attr = ''
        if tex_path.find(model_define.DIFF_SUFFIX) >= 0:
            attr = '_MainTex'
        elif tex_path.find(model_define.BASE_SUFFIX) >= 0:
            attr = '_TripleMaskMap'
        elif tex_path.find(model_define.CTRL_SUFFIX) >= 0:
            attr = '_OptionMaskMap'
        elif tex_path.find(model_define.SHAD_SUFFIX) >= 0:
            attr = '_ToonMap'

        if not attr:
            continue

        attr_tex_dict[attr] = tex_path

    return attr_tex_dict


# ==================================================
def get_default_value_dict(cgfx_material):

    attr_val_dict = {
        '_SpecularPower': 0.15,
        '_EnvRate': 1,
        '_EnvBias': 5,
        '_ToonStep': 0.4,
        '_ToonFeather': 0.001,
        '_UseOptionMaskMap': 1,
        '_RimStep': 0.15,
        '_RimFeather': 0.001,
        '_RimColor': [1] * 3,
        '_RimColorAlpha': 100 / 255,
        '_RimShadow': 2,
        '_RimSpecRate': 1,
        '_GlobalDirtColor': [89 / 255, 65 / 255, 55 / 255],
        '_GlobalDirtRimSpecularColor': [154 / 255, 115 / 255, 98 / 255],
        '_Cutoff': 0.0,
        '_EmissiveColor': [1, 1, 1],
        '_DirtRate1': 0.0,
        '_DirtRate2': 0.0,
        '_DirtRate3': 0.0,
        '_SpecularColor': [1.0, 1.0, 1.0],
        '_FaceCenterPos': [0, 0, 0],
    }

    if cgfx_material.find('_head') >= 0:

        opt_dict = {
            '_FaceCenterPos': [0, 0.1292 * 100, 0.01289 * 100],
            '_RimColorAlpha': 50 / 255,
            '_Cutoff': 0.5,
        }
        attr_val_dict.update(opt_dict)

    elif cgfx_material.find('_hair') >= 0:

        opt_dict = {
            '_RimColorAlpha': 50 / 255,
            '_Cutoff': 0.5,
            '_ToonStep': 0.3,
        }
        attr_val_dict.update(opt_dict)

    elif cgfx_material.find('_eye') >= 0:

        opt_dict = {
            '_RepeatUV': 1.0
        }
        attr_val_dict.update(opt_dict)

    if cgfx_material.find('Alpha') >= 0:

        opt_dict = {
            '_Cutoff': 0.2,
        }
        attr_val_dict.update(opt_dict)

    return attr_val_dict


# ==================================================
def get_outline_default_value_dict():

    attr_val_dict = {
        '_OutlineWidth': 1.0,
        '_OutlineColor': [0.811, 0.586, 0.586],
        '_OutlineColorW': 1.0,
        '_GlobalOutlineOffset': 1.0,
        '_GlobalOutlineWidth': 0.6,
        '_GlobalCameraFov': 15.0,
    }

    return attr_val_dict


# ==================================================
def get_spec_color_locator(cgfx_material):

    target_locater_name = ''

    if cgfx_material.find('face') >= 0:
        target_locater_name = 'Face_spec_info'
    elif cgfx_material.find('hair') >= 0:
        target_locater_name = 'Hair_spec_info'
    elif cgfx_material.find('mtl_bdy') >= 0:
        target_locater_name = 'Body_spec_info'

    target_locator = cmds.ls(target_locater_name, type='Transform', l=True)

    if not target_locator:
        return ''
    else:
        return target_locator[0]


# ==================================================
def get_current_spec_color_dict(spec_locator):

    specular_color = [1.0, 1.0, 1.0]
    if cmds.objExists(spec_locator):
        specular_color = cmds.getAttr(spec_color_locater + '.scale')[0]

    spec_color_dict = {
        '_SpecularColor': specular_color
    }


# ==================================================
def get_spec_color_connect_dict(cgfx_material, spec_locator):

    spec_color_connect_dict = {
        cgfx_material + '._SpecularColor._SpecularColorR': spec_locator + '.scale.scaleX',
        cgfx_material + '._SpecularColor._SpecularColorG': spec_locator + '.scale.scaleY',
        cgfx_material + '._SpecularColor._SpecularColorB': spec_locator + '.scale.scaleZ',
    }
    return spec_color_connect_dict


# ==================================================
def get_head_center_locator(cgfx_material):

    target_locater_name = ''

    if cgfx_material.find('_face') >= 0:
        target_locater_name = 'Head_tube_center_offset'
    elif cgfx_material.find('_eye') >= 0:
        target_locater_name = 'Head_tube_center_offset'
    elif cgfx_material.find('_brow') >= 0:
        target_locater_name = 'Head_tube_center_offset'
    elif cgfx_material.find('_hair') >= 0:
        target_locater_name = 'Head_center_offset'
    else:
        return

    target_locator = cmds.ls(target_locater_name, type='transform', l=True)

    if not target_locator:
        return ''
    else:
        return target_locator[0]
