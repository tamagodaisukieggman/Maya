# -*- coding: utf-8 -*-
"""
Copyright (C) 2021 Digital Frontier Inc.
"""
# default
import os
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


class LogBrowser(QMainWindow):
    UIFILE = os.path.join(__file__.rsplit('.', 1)[0] + '.ui')

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = QUiLoader().load(self.UIFILE)
        self._textbrowser = QTextBrowser()

        # message cache
        self._cur_message_cache = str()
        self._all_message_cache = str()

        # UIのセットアップ
        self.setup_ui()
        self.update

    # =========================================================================
    # Public
    # =========================================================================
    def update(self):
        """Viewの更新
        """
        text = '<div style="font-family:sans-serif;font-size:10pt;">%s</div>'
        self._textbrowser.setHtml(text % self._cur_message_cache)

        # 一番下のメッセージに移動
        # self._textbrowser.page().mainFrame().scroll(0, 1000000)
        self._textbrowser.verticalScrollBar().setValue(1000000)

    def add_message(self, message, color=None):
        """Loggerにメッセージを追加
        """
        message = message.replace('\n', '<br>')
        if color:
            message = '<font color="%s">%s</font>' % (color, message)
        message += '<br>'
        self._cur_message_cache += message
        self._all_message_cache += message
        self.update()

    def clear_message(self):
        """メッセージを削除する
        """
        self._cur_message_cache = str()
        self.update()

    def show_all_message(self):
        """すべてのメッセージを表示する
        """
        self._cur_message_cache = self._all_message_cache
        self.update()

    # =========================================================================
    # GUI
    # =========================================================================
    def setup_ui(self):
        """UIの構築
        """
        self.setWindowTitle('Logs')
        self.resize(1000, 400)
        self.setCentralWidget(self.ui)

        # WebViewの作成
        self.ui.webview_layout.addWidget(self._textbrowser)

        # Connectionの構築
        self.ui.clear_btn.clicked.connect(self.clear_message)
        self.ui.show_all_btn.clicked.connect(self.show_all_message)


def main():
    import sys
    app = QApplication(sys.argv)
    lb = LogBrowser()
    lb.add_message('error message', 'ERROR')
    lb.add_message('info message', 'Info')
    lb.add_message('none message', None)
    lb.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
