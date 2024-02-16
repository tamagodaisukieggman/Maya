# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import re

# ツール名
TOOL_NAME = 'GlpBGExporter'

# ツールバージョン（更新日）
TOOL_VERSION = '23090101'

# サイリウム，モブのルートグループ名の正規表現
REGEX_MOB_CYALUME_ROOT = re.compile(r'mdl_env_live_cmn_(cyalume_d|cyalume_r|mob)[0-9]{3}(_.*?[0-9]{3}|)$')

# サイリウム，モブのグループメンバーの正規表現
REGEX_MOB_CYALUME_GROUP = re.compile(r'(cyalume_d|cyalume_r|mob)[0-9]{3}_.*?_([0-1])([0-9])$')

# マニュアルページのURL
HELP_URL = 'https://wisdom.cygames.jp/x/odoCBg'

# ファイルタイプオプションメニューの項目
FILE_TYPES = ['ma', 'mb', 'obj', 'fbx']

DEFAULT_FILE_TYPE = 'fbx'

MAKE_DIR_OPTION_KEY = 'gallopBGExporterMakeDir'
MULTI_DST_MODE_OPTION_KEY = 'gallopBGExporterMultiDstMode'

FOLDER_PATH_ATTR_NAME = 'exportInfo_folderPath'

SETTING_LOCATOR_NAME = 'CygamesTools'

TEMP_NODE_SUFFIX = 'TEMP_TEMP_TEMP'

SUB_NORMAL_SUFFIX = '_outline'

UVSET_FOR_NORMAL_XY = '____normal_xy'
UVSET_FOR_NORMAL_Z = '____normal_z'

OUTPUT_COLORSET = '____output_colorset'

SUB_COLORSET_NAME = 'colorSet_sub'

OUTLINE_PROCESS_TARGET_REGEX_LIST = [
    r'(_outline|_toon)$',
]

NODE_TYPE_BY_CATEGORY = {
    'model': ['mesh', 'nurbsSurface', 'nurbsCurve'],
    'light': ['ambientLight', 'directionalLight', 'pointLight', 'spotLight', 'areaLight', 'volumeLight'],
    'skeleton': ['joint', 'ikEffector', 'ikHandle'],
    'etc': ['camera', 'locator', 'group'],
}

NODE_TYPES = [node_type for category in NODE_TYPE_BY_CATEGORY.values() for node_type in category]
