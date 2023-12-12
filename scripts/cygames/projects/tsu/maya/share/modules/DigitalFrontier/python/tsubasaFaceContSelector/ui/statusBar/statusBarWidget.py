# -*- coding: utf-8 -*-
"""
Copyright (C) 2021 Digital Frontier Inc.
"""
# default
import os
import sys
import imp
# PySide
try:
    imp.find_module('PySide2')
    # from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import QUiLoader
except ImportError:
    # from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import QUiLoader
# statusbar
from .logBrowser import LogBrowser
from .handler import Handler
import tsubasaFaceContSelector.core as core


class StatusBarWidget(QStatusBar):
    UIFILE = os.path.abspath(__file__).replace('.py', '.ui')

    def __init__(self, parent=None, setup_jumper=False):
        QStatusBar.__init__(self, parent)
        self._show_message_time = 3000
        self._status_bar = QStatusBar()
        self._log_browser = LogBrowser(self)
        self._handler = Handler(
            status_bar=self,
            log_browser=self._log_browser)

        self.setup_ui()

    # =========================================================================
    # Public
    # =========================================================================
    def set_progress_value(self, cur_value, max_value=100):
        """ProgressBarに値をセットする
        """
        self.show_progress_bar()
        value = cur_value / float(max_value)
        self.ui.progress_bar.setValue(min(value, 1) * 100)

    def close_log_browser(self):
        """statusBarのLogBrowserWidgetを閉じる
        """
        self._log_browser.setVisible(0)

    def set_show_message_time(self, time=0):
        """statusBarにmessageが表示される時間を設定する
        """
        self._show_message_time = time

    def show_progress_bar(self):
        """ProgressBarを表示
        """
        self.ui.progress_bar.show()

    def hide_progress_bar(self):
        """ProgressBarを非表示
        """
        self.ui.progress_bar.show()

    # =========================================================================
    # GUI
    # =========================================================================
    def setup_ui(self):
        self.ui = QUiLoader().load(self.UIFILE)
        self.addPermanentWidget(self.ui, stretch=1)
        self.setSizeGripEnabled(0)

        # Status Bar
        self._status_bar.setSizeGripEnabled(False)
        self._status_bar.messageChanged.connect(self._reset_color)
        self.ui.statusBar_layout.addWidget(self._status_bar)

        # Progress Bar
        self.ui.progress_bar.hide()
        self.ui.progress_bar.setRange(0, 100)
        self.ui.progress_bar.setMaximumWidth(150)
        self.ui.progress_bar.setMinimumWidth(150)

        # Log Browser Button
        self.ui.log_button.clicked.connect(self._show_log_browser)

    # =========================================================================
    # Private
    # =========================================================================
    def _reset_color(self):
        """文字が空になったら色を元に戻す
        """
        self.setStyleSheet("")

    def _show_log_browser(self):
        """LogBrowserを表示する
        """
        if self._log_browser.isHidden():
            self._log_browser.setVisible(1)
        else:
            self._log_browser.setVisible(0)

    # =========================================================================
    # Override
    # =========================================================================
    def showMessage(self, text, timeout=None):
        """StatusBarに表示するメッセージを指定する
        """
        if not timeout:
            timeout = self._show_message_time
        self._status_bar.showMessage(text, self._show_message_time)

    def setStyleSheet(self, color):
        """StatusBarの色を設定する
        """
        self._status_bar.setStyleSheet(color)

    def closeEvent(self, event):
        """windowが閉じられたときに実行
        """
        # loggerのhandlerを削除
        logger = core.get_logger()
        logger.removeHandler(self._handler)
        self._log_browser.close()


def main():
    from pysidelib.sampleWindow.mainWindow import SampleWindow
    app = QApplication(sys.argv)
    sw = SampleWindow()
    sw.show()
    sw.statusBar().set_progress_value(1000)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
