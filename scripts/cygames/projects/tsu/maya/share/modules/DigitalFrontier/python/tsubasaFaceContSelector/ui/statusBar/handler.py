# -*- coding: utf-8 -*-
"""
Copyright (C) 2021 Digital Frontier Inc.
"""
import logging
import tsubasaFaceContSelector.core.logger as logger
LEVEL_COLOR = logger.LEVEL_COLOR
LOG_FORMAT = logger.LOG_FORMAT
DATE_FORMAT = logger.DATE_FORMAT


class Handler(logging.StreamHandler):

    def __init__(self, status_bar, log_browser):
        logging.StreamHandler.__init__(self)
        logger.get_logger().addHandler(self)
        self.setFormatter(logging.Formatter(
            LOG_FORMAT, DATE_FORMAT))
        self._status_bar = status_bar
        self._log_browser = log_browser

    # =========================================================================
    # Override
    # =========================================================================
    def emit(self, record):
        # messageとlevelを取得
        msg = self.format(record)
        level = record.levelname

        # StatusBar にメッセージを送る
        color = LEVEL_COLOR.get(level, None)
        self._status_bar.showMessage(msg)
        if color:
            self._status_bar.setStyleSheet('background-color: %s' % color)

        # log browserへメッセージを送る
        self._log_browser.add_message(msg, color)
