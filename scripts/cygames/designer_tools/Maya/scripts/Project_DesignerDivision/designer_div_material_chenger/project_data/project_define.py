# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os


# ------------------------------------------------------------
# path
# ------------------------------------------------------------

script_dir_path = os.path.dirname(__file__)
resources_dir_path = '{}/resources'.format(script_dir_path)
shader_dir_path = '{}/shader'.format(resources_dir_path)
texture_dir_path = '{}/sample_texture'.format(shader_dir_path)


# ------------------------------------------------------------
# shader_file
# ------------------------------------------------------------

# shader_file_name
FX_FILE_TOON_DEFAULT = 'CharacterToonTSERDefault.fx'
FX_FILE_TOON_FACE = 'CharacterToonFaceTSERDefault.fx'
FX_FILE_TOON_HAIR = 'CharacterToonHairTSERDefault.fx'
FX_FILE_TOON_EYE = 'CharacterToonEyeT.fx'
FX_FILE_OUTLINE = 'CharacterOutline.fx'


# ------------------------------------------------------------
# material_type
# ------------------------------------------------------------

# material_type
MTL_TYP_DEFAULT = 'tga_default'
MTL_TYP_PSD = 'psd_default'
MTL_TYP_PSD_OPT = 'psd_option'
MTL_TYP_TOON = 'toon_default'
MTL_TYP_OUTLINE = 'outline_default'
# prefix
MTL_TYP_TOON_PFX = 'toon_'
MTL_TYP_OUTLINE_PFX = 'outline_'

# ツールで使用するmaterial_typeのリスト
MTL_TYP_LIST = [
    MTL_TYP_DEFAULT,
    MTL_TYP_PSD,
    MTL_TYP_TOON,
    MTL_TYP_OUTLINE,
]


# ------------------------------------------------------------
# mesh
# ------------------------------------------------------------

MSH_PFX = 'M_'
MSH_SFX_OUTLINE = '_Outline'
MSH_FACE_STR = 'Face'
MSH_HAIR_STR = 'Hair'
MSH_BODY_STR = 'Body'
MSH_MAYU_STR = 'Mayu'
MSH_CHEEK_STR = 'Cheek'
MSH_TEAR_STR = 'Tear'
MSH_LINE_STR = 'Line'


# ------------------------------------------------------------
# material_name
# ------------------------------------------------------------

# prefix
MTL_PFX = 'mtl_'
MTL_PFX_BODY = '_bdy'
MTL_PFX_TAIL = '_tail'
# suffix
MTL_SFX_FACE = '_face'
MTL_SFX_MAYU = '_mayu'
MTL_SFX_HAIR = '_hair'
MTL_SFX_EYE = '_eye'
MTL_SFX_ALPHA = '_Alpha'
MTL_SFX_CHEEK = '_Cheek'


# ------------------------------------------------------------
# texture
# ------------------------------------------------------------

# prefix
TEX_PFX = 'tex_'
# suffix
TEX_SFX_MAIN = '_diff'
TEX_SFX_TOON = '_shad_c'
TEX_SFX_TRIPLE_MASK = '_base'
TEX_SFX_OPTION_MASK = '_ctrl'
TEX_SFX_DIRT = '_dirt'
TEX_SFX_EMISSIVE = '_emi'
TEX_SFX_MASK_COL = '_area'

TEX_SFX_EYE_MAIN = '0'
TEX_SFX_EYE_HI0 = 'hi00'
TEX_SFX_EYE_HI1 = 'hi01'
TEX_SFX_EYE_HI2 = 'hi02'

TEX_SFX_CHEEK_FOR_MAYA0 = '_cheek_for_maya0'
TEX_SFX_CHEEK_FOR_MAYA1 = '_cheek_for_maya1'

TEX_SFX_PSD_DEFAULT = '_diff'
TEX_SFX_PSD_OPTION = '_opt'


# ------------------------------------------------------------
# プロジェクト処理呼び出しキー
# ------------------------------------------------------------

CMD_CHARA_LIGHT_CONNECTION = 'CHARA_LIGHT_CONNECTION'
CMD_SPEC_LOC_CONNECTION = 'SPEC_LOC_CONNECTION'
CMD_HEAD_LOCATOR_CONNECTION = 'HEAD_LOCATOR_CONNECTION'
CMD_OUTLINE_MESH_VISIBLE = 'OUTLINE_MESH_VISIBLE'


# ------------------------------------------------------------
# light
# ------------------------------------------------------------

CHARA_LIGHT_NAME = 'charaLight0'


# ------------------------------------------------------------
# locator
# ------------------------------------------------------------

# Head_center系
LOC_FACE_CENTER = 'Head_tube_center_offset'
LOC_HAIR_CENTER = 'Head_center_offset'
# SpecInfo
LOC_FACE_SPEC = 'Face_spec_info'
LOC_HAIR_SPEC = 'Hair_spec_info'
LOC_BODY_SPEC = 'Body_spec_info'
