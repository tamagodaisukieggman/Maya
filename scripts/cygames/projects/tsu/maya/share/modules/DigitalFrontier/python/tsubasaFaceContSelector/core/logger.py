# -*- coding: utf-8 -*-
"""
Copyright (C) 2021 Digital Frontier Inc.
"""
import os
import logging
import datetime
TOOL_NAME = 'faceContSelector'
LOG_FORMAT = '[%(asctime)s][%(levelname)s] - %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
SETUPED_LOGGER = False
LEVEL_COLOR = {
    'DEBUG': '#9b9b9b',
    # 'INFO': '#d7d7d7',
    'WARNING': '#b4b400',
    'ERROR': '#dc3b3e',
    'CRITICAL': '#bb20af'}


# tool専用のloggerを取得
def get_logger():
    global SETUPED_LOGGER
    logger = logging.getLogger(TOOL_NAME)
    if not SETUPED_LOGGER:
        SETUPED_LOGGER = SETUPED_LOGGER or setup_logger(logger)
    return logger


# loggerへhandlerなどを追加するsetupを行う
def setup_logger(logger):
    # handlerの初期化
    logger.handlers = []

    # levelの設定
    logger_level = logging.INFO
    file_handler_level = logging.INFO

    # loggerに対しlevelを設定
    logger.setLevel(logger_level)

    # コンソール出力用のHanderを作成し登録
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(sh)
    return True
