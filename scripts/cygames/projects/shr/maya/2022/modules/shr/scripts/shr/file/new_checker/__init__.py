# -*- coding: utf-8 -*-
import sys
# import logging
# from tatool.log import ToolLogging, Stage

import maya.OpenMayaUI as omui

from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

TITLE = "Mutsunokami Export Checker"

# Cylista Exporter ウィンドウのクラス名
EXPORT_WINDOW_CLASS_NAME = "ExportWindow"

CHARACTER_PATHS = [
    "z:/mtk/work/resources/characters",
    "z:/mtk/work/noshipping/characters"
]

ENV_PATHS = [
    "z:/mtk/work/resources/env",
    "z:/mtk/work/noshipping/env"
]

DATA_TYPES = {
        "env": "env",
        "chara": "chara",
        "prop": "prop"
}

EXT_DICT = {
    ".ma": "mayaAscii",
    ".mb": "mayaBinary"
}

# ！！ここ重要パスからモジュールパスを抽出している
# mtk.file.new_checker
PATH = "Z:/mtk/tools/maya/2022/modules/mtk/scripts/mtk/file/new_checker"

PATH = 'C:/cygames/shrdev/shr/tools/in/ext/maya/2022/modules/shr/scripts/shr/file/new_checker'

PACKAGE = ".".join(PATH.split("/")[-3:])

config_node = None
CYLISTA_SCRIPT_PATH = "Z:/cyllista/tools/maya/modules/cyllista/scripts/"


if CYLISTA_SCRIPT_PATH not in sys.path:
    sys.path.append(CYLISTA_SCRIPT_PATH)



CHECKER_GUI_NAME = "CheckerGUI"
CHECKER_RESULT_GUI_NAME = "CheckerResultGUI"
CHECKER_ERROR_GUI_NAME = "ChekerErrorGUI"



project = "mutsunokami"
TOOL_NAME = "{}".format("".join(TITLE.split()))

tool_category = "Maya"


tool_version = 'v2021.12.03'
# バッチ起動対応

# tool_version = 'v2021.08.04'
# col_detailed　がないのに、col_character に設定されているアトリビュートの値が
# object_without_camera でないとエラーになる状態を詳細にエラー記述
# 自動修正でのフォロー
# 法線のロックをLOD では見ないように変更
# model グループ以下のもののみをチェックするようにした
# なので、コリジョンも見ない
# オーダーは背景だけだが、キャラも同じようにした


# tool_version = 'v2021.08.03'
# chara トランスフォームノードに dagPose があるモデルの
# メッシュノードに skinCluster が無ければエラー　追加
# ウェイトの合計値が 1.0 （5桁で丸め）でないものはエラー　追加


# tool_version = 'v2021.05.21'
# Rig シーン、model ノードをチェックする階層を修正


# tool_version = 'v2021.05.18'
# コリジョンアトリビュートのエラー、追加のみの判定にしていたため
# 値の修正では、検出はするが、修正後の確認の表示がされていなかった
# 値の追加と修正を分け、どちらも検出するようにした


# tool_version = 'v2021.04.27'
# CNP のインフルエンスをエラーとして処理を追加


# tool_version = 'v2021.04.13'



# tool_logging = ToolLogging(
#                         projects=project,
#                         toolcategory=tool_category,
#                         target_stage=Stage.dev,
#                         tool_version=tool_version)

# logger = tool_logging.getTemplateLogger(TOOL_NAME)


#logger.setLevel(logging.INFO)