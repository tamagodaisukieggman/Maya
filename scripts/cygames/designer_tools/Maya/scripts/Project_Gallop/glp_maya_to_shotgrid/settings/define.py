# -*- coding: utf-8 -*-
"""
他プロジェクト等に移植する時などに書き換える定義ファイル
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

TOOL_NAME = 'glp_shotgrid_tool'
SG_URL = "https://tkgpublic.shotgunstudio.com/"
SG_PROJECT_NAME = "gallop"

SG_FIELD_CODE_LIST = [
    'code',
    'sg_glp_chara_name',
    'sg_glp_section',
    'sg_glp_division',
    'sg_glp_part',
    'sg_glp_type',
    'sg_category',
    'sg_sub_category',
    'sg_glp_kind',
    'task_template'
]

# 設定jsonファイルパス
UI_SETTING_JSON_PATH = os.getenv('APPDATA') + '/TKG/' + TOOL_NAME + '_ui_setting.json'
SG_USER_SETTING_JSON_PATH = os.getenv('APPDATA') + '/TKG/' + TOOL_NAME + '_user_setting.json'
