# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
from PySide2 import QtCore, QtGui, QtWidgets
import maya.cmds as cmds

from tatool.log import ToolLogging, Stage


tool_version = 'v2021.09.01'
# パック後のテクスチャをpsdにして各チャンネルを分解し、レイヤーマスクにする機構を入れた
# しかしその後の打ち合わせで不要なものとなったのでオミット

# tool_version = 'v2021.08.11'
# パッキングテクスチャ以外のアトラステクスチャ名に設定した名前の適用
# アトラステクスチャ生成時にマテリアル生成できない問題の解決
# Ornatrix のスタックオペレータでシンメトリが入っている場合、
# モデルをまとめるときにMaya で鏡面コピーをしてから実行
# HDAでの法線編集時のアルゴリズム変更、四本足対応
# パッキング時のアルゴリズム変更しよりシビアに、オプション追加
# 頂点カラー適用時に頂点カラーのヒストリがあればそれを削除してから適用するようにした


# tool_version = 'v2021.08.05'
# optionVar polyAutoShowColorPerVertex を強制的にオンにするようにしてみた
# プリセットテクスチャ、アトラステクスチャの設定パスLine
# エンターキーでの動作を通常のパス入力のように、セパレータの置き換え
# アトラステクスチャのパス設定ダイアログのデフォルト値、
# 既に入力がある場合はそこを起点とする

# アトラステクスチャの名前を全てのファイル名に設定した名前で生成

# アトラステクスチャ生成時にマテリアルの生成が正しくできていない問題の解決

# 頂点カラー適用時頂点カラーがディスプレイされない問題の解決


# tool_version = 'v2021.07.16'
# リダクション機能をエッジのリダクションに変更


# tool_version = 'v2021.07.15.2'
# PMG と表記されていたものを PNG に変更
# テクスチャからマテリアルを作る際にスペキュラの値をゼロに変更


# tool_version = 'v2021.07.15'
# プリセット生成後に QFileSystemModel のルートパスをリフレッシュしないように変更
# コンフルジャンプ機能追加
# ソースの選択時、ヘアのベースジオメトリの判定追加


# tool_version = 'v2021.07.12'
# 初回リリース


TITLE = "Hair Tool Set"
NAME = "{}".format("_".join(TITLE.lower().split()))

project = "mutsunokami"

TOOL_NAME = "{} {}".format(project, TITLE)


ROOT_PATH = r"\\cgs-str-pri01-m\mutsunokami_storage\30_design\chara\04_common\HairCard\PresetTextures"
ROOT_PATH = r"z:\mtk\work\noshipping\characters\hair_presets"
ROOT_PATH = "z:/mtk/work/noshipping/hair_card"

TEMP_PATH = r"z:\mtk\work\noshipping\characters\temp_hair"


AUTOMATION_TOOL_KIT = "Z:/mtk/tools/standalone/substance_automation_toolkit"
PYSBS = "Z:/mtk/tools/standalone/substance_automation_toolkit/Python API/site-packages"

if PYSBS not in sys.path:
    sys.path.append(PYSBS)

MAYA_PATH = os.environ["MAYA_LOCATION"]
IMAGE_MAGICK_PATH = os.path.join(
    MAYA_PATH, "bin/magick.exe").replace(os.sep, '/')

ARNOLD_PLUGIN_NAME = "mtoa"


CURRENT_HOUDINI_VERSION = "18.5.532"
HOUDINI = "Houdini"
BIN = "bin"
HOUDINI_PATH = "C:/Program Files/Side Effects Software/{} {}/{}".format(
    HOUDINI, CURRENT_HOUDINI_VERSION, BIN)

HOUDINI_PLUGIN_PATH = "Z:/mtk/tools/maya/modules/houdini_engine/plug-ins"
HOUDINI_SCRIPTS_PATH = "Z:/mtk/tools/maya/modules/houdini_engine/scripts/houdini_engine_for_maya"
# PLUGIN_PATH = "Z:/mtk/tools/maya/modules/houdini_engine/plug-ins"

HOUDINI_ENGINE_PLUGIN_NAME = "houdiniEngine"
HOUDINI_ENGINE_PLUGIN_EXT = ".mll"

NEED_PLUGINS = [ARNOLD_PLUGIN_NAME, HOUDINI_ENGINE_PLUGIN_NAME]
HOUDINI_ENGINE_VERSION = "3.5 (API: 2)"

HDA_NAME = "mtk_hair_uv_tool"
REMOVE_HDA_NAME = "mtk_hair_remove"
REMOVE_HDA_NAME = "mtk_hair_edge_remove"
HDA_PATH = "Z:/mtk/tools/maya/share/hda/develop"


NEED_PATHS = [AUTOMATION_TOOL_KIT, PYSBS,
              IMAGE_MAGICK_PATH, HDA_PATH, TEMP_PATH, ROOT_PATH]

TEXTURE_SUFFIX = [
    "alpha",
    "depth",
    "flow",
    "root"
]

EXPORT_MAP_TYPES = [
    "normal",
    "flow",
    "ao",
    "root",
    "depth",
    "alpha",
    "vcolor",
]

VTX_COLOR_SET_NAME = "ar_vtx_color"
DEFAULT_UV_SET = "map1"

RESOLUTIONS_DICT = {
    32: 5,
    64: 6,
    128: 7,
    256: 8,
    512: 9,
    1024: 10,
    2048: 11,
    4096: 12,
    8192: 13,
}

PRESET_TEXTURE_PREFEX = "ph"

HAIR_CARD_NAME = "HairCard"
SHADING_NODE_NAME = "initialShadingGroup"

ONE_CARD = "one_card"
ALL_CARD = "all_card"

BAKE_TARGET_NAME = "bake_target"
BAKE_SOURCE_NAME = "bake_source"
FINAL_NAME = "filal"

MAP_SAMPLING_LIST = ["Preview", "Low", "Medium", "High"]

# text:   string
# txint:  string
# fvalue: float
# value:  int
# check:  bool

FILE_IMFO_DATA = [
    "preset_directory_text",
    "plane_size_fvalue",
    "preset_name_check",
    "preset_name_text",

    "preset_resolution_txint",
    "preset_filter_txint",
    "preset_sampling_value",
    "preset_filter_size_fvalue",

    "normal_map_check",
    "flow_map_check",
    "ao_map_check",
    "root_map_check",
    "depth_map_check",
    "alpha_map_check",
    "vcolor_map_check",

    "delete_unused_check",

    "atlus_resolution_txint",
    "atlus_quality_txint",
    "atlus_file_name_text",
    "atlus_file_type_txint",
    "atlus_create_material_check",
    "atlus_export_directory_text",

    "uv_crop_check",

    "atlus_texture_filter_type_txint",
    "atlus_texture_filter_size_fvalue",
]


tool_category = "Maya"


tool_logging = ToolLogging(
    projects=project,
    toolcategory=tool_category,
    target_stage=Stage.dev,
    tool_version=tool_version)

logger = tool_logging.getTemplateLogger(TOOL_NAME)
