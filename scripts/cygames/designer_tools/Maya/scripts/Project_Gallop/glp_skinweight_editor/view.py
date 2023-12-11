# -*- coding: utf-8 -*-
"""MVCでいうViewを担う
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

from maya.app.general import mayaMixin
from PySide2 import QtWidgets
import shiboken2

from .ui import main_window
reload(main_window)


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)
        # 子ウィンドーなどの連動させてcloseしたいウィンドーのリスト
        self.linked_window = []

    def set_enable_components(self, is_enable):
        self.ui.centralwidget.setEnabled(is_enable)

    def add_linked_window(self, window):
        if window is None:
            return
        if window not in self.linked_window:
            self.linked_window.append(window)

    def remove_linked_window(self, window):
        if window in self.linked_window:
            self.linked_window.remove(window)

    def closeEvent(self, event):
        self.dispose_linked_window()
        return super(self.__class__, self).closeEvent(event)

    def custom_delete(self):
        """自身をdeleteする前にリンクしているウィンドーを閉じる機能を追加したclose
        """
        self.dispose_linked_window()
        self.deleteLater()

    def dispose_linked_window(self):
        """関連付けされているウィンドーも合わせて破棄する
        """
        if self.linked_window:
            for window in self.linked_window:
                # 削除済みインスタンスを踏まないようにvalidateする
                if window is None or not shiboken2.isValid(window):
                    continue
                window.close()
