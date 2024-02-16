# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


# ツール情報
TOOL_NAME = 'CySceneExplorer'
TOOL_VERSION = '23112101'

TOOL_COLLECTION_LABEL = 'CySceneCollection'
TOOL_COLLECTION_VERSION = 23102001  # jsonに記録する現バージョン
TOOL_MIN_VALID_COLLECTION_VERSION = 23102001  # 最低保証バージョン

# 対応する拡張子
EXTENT_LIST = ['ma', 'mb', 'fbx']
INIT_ON_EXTENT_LIST = ['ma']
EXTENT_PATTERN = '\.({})$'.format('|'.join(EXTENT_LIST))

# デフォルトの設定値
DEFAULT_WALK_LIMIT = 100000
DEFAULT_SET_ROOT_ON_DOUBLE_CLICK = False
DEFAULT_SEP_WITH_SLASH = True
DEFAULT_COL_OBJ_DEL_CONFIRM = True
DEFAULT_EXEC_SCRIPT_NODE = False
DEFAULT_USE_NAMESPACE = True
DEFAULT_EXEC_SET_PROJECT = True
DEFAULT_EXEC_FIX_TEX_PATH = True
DEFAULT_PROJECT_SETTING_FILE_PATH = ''

# 検索ワードのフラグ
AND_FLAG = '(?<!OR) (?!OR)'
OR_FLAG = ' OR '
EXCLUDE_FLAG = '-'
RE_FLAG = '!'

#
MENU_TYPE_EXPLORER = 'Explorer'
MENU_TYPE_BOOKMARK = 'Bookmark'
MENU_TYPE_COLLECTION = 'Collection'

# 右クリックメニューのラベル
MENU_OPEN = 'シーンを開く'
MENU_SHOW_IN_EXP = 'フォルダを開く'
MENU_SET_ROOT = 'ルートディレクトリに指定'
MENU_BOOKMARK = 'ブックマークに追加'
MENU_REM_BOOKMARK = 'ブックマークから削除'
MENU_SEPARATOR = 'Separator'
MENU_COPY_PAHT = 'パスをコピー'
MENU_ADD_COLLECTION_PAHT = 'コレクションに追加'
MENU_OPEN_ALL_ITEMS = 'コレクションの全シーンを開く'
MENU_CHANGE_COLLECTION_NAME = 'コレクション名を編集'

# 実行時ボタンラベル
EXEC_BUTTON_OPEN_NEW = '新しいシーン'
EXEC_BUTTON_REFERENCE = 'リファレンス'
EXEC_BUTTON_IMPORT = 'インポート'
EXEC_BUTTON_CANCEL = 'キャンセル'

# 設定ファイル周り
CY_SCENE_OPENER_NAME = 'CySceneOpener'  # ブックマークの初期ロードに使用
SETTING_GEOMETRY = 'Geometry'
SETTING_MAIN_SPLITTER = 'MainSplitter'
SETTING_SUB_SPLITTER = 'SubSplitter'
SETTING_WALK_FILE_LIMIT_LABEL = 'WalkFileLimit'
SETTING_DOUBLE_CLICK_ROOT_OP_LABEL = 'DoubleClickRootOp'
SETTING_SEP_WITH_SLASH = 'SeparatePathWithSlash'
SETTING_COL_OBJ_DEL_CONFIRM = 'ColObjDelConfirm'
SETTING_EXEC_SCRIPT_NODE_LABEL = 'ExecScriptNode'
SETTING_USE_NAMESPACE_LABEL = 'UseNamespace'
SETTING_ROOT_PATH = 'RootPath'
SETTING_SEARCH_STR = 'SearchStr'
SETTING_EXT_FILTER = 'ExtFilter'
SETTING_EXEC_SET_PROJECT = 'ExecSetProject'
SETTING_EXEC_FIX_TEXTURE_PATH = 'ExecFixTexturePath'
SETTING_IS_PREVIOUS_INCOMPLETE = 'IsPreviousIncomplete'
SETTING_PROJECT_SETTING_FILE_PATH = 'ProjectSettingFilePath'
SETTING_MAIN_TAB_INDEX = 'MainTabIndex'
SETTING_COLLECTION_SPLITTER = 'CollectionSplitter'
SETTING_COLLECTION_JSON_PATH = 'CollectionJsonPath'
SETTING_COLLECTION_COL_SEL = 'CollectionSelection'
SETTING_COLLECTION_COL_ITEM_SEL = 'CollectionItemSelection'
