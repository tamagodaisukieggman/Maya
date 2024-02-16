# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


# ツール情報
TOOL_NAME = 'GlpCharaCopyWorkData'
TOOL_VERSION = '23032801'

# 規定パス
FOLDER_SELECT_ROOT = 'D:\\work\\gallop\\svn\\svn_gallop\\80_3D\\01_character\\01_model'

# チェック
REG_ID_FOLDER_PATTERN = '\d{4}_\d{2}'
REG_FOLDER_NG_RULE = '[\\\/\:\*\?\"\>\<\|]'
REG_PATH_NG_RULE = '[\*\?\"\>\<\|]'
FILE_COUNT_LIMIT = 10000

# 対応する拡張子
EXT_SCENE_LIST = ['.ma', '.fbx', '.mb']  # 内部のマテリアル等の変更も行うシーンファイル
EXT_TEXT_LIST = ['.asset', '.prefab']  # 内部の文字置換も行う
EXT_DEFAULT_BLACK_LIST = ['.mel', '.swatch', '.meta']  # デフォルトではコピー対象にしないファイル

# ステータス
STATUS_ALREADY_EXISTS = 'コピー先に同名のファイルが存在します'
STATUS_NO_EXISTS = '新規のコピーファイルを作成します'
STATUS_IS_SAME = 'コピー元とコピー先が同じファイルです'

WARNING_STATUSES = [STATUS_ALREADY_EXISTS]
ERROR_STATUSES = [STATUS_IS_SAME]

# 右クリックメニューのラベル
MENU_OPEN_SRC = 'コピー元を開く'
MENU_OPEN_DST = 'コピー先を開く'
