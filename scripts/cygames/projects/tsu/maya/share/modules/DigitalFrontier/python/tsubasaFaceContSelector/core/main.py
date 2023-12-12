# -*- coding: utf-8 -*-
"""
Copyright (C) 2021 Digital Frontier Inc.
"""
import os
import json
SETTING_FILE = os.path.join(os.path.dirname(__file__), 'btn_settings.json')


def get_button_settings_info():
    """jsonファイルを辞書形式で読み込み取得する
    Args:
    　path (str): jsonファイルのパスを指定する
    Return:
    　Dict
    """
    data = {}
    with open(SETTING_FILE, 'r') as jobj:
        data = json.load(jobj)
    return data
