# -*- coding: utf-8 -*-
"""MVCでいうViewを担う
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya2022-
    from builtins import range
    from importlib import reload
except Exception:
    pass

import os
import maya.api.OpenMaya as om

from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general import mayaMixin

from . import define
from .ui import main_window

reload(main_window)


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):

    def __init__(self, root=None):

        super(View, self).__init__()

        self.__root = root
        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.__items_widget = ScrollWidget(self)
        self.ui.items_widget_area.setWidget(self.__items_widget)

        if os.path.exists(define.ADD_ICON_PATH):
            self.ui.add_item_button.setIcon(QtGui.QIcon(define.ADD_ICON_PATH))
        if os.path.exists(define.RELOAD_ICON_PATH):
            self.ui.update_item_button.setText('')
            self.ui.update_item_button.setIcon(QtGui.QIcon(define.RELOAD_ICON_PATH))

        self.__callback_id_list = []

    def closeEvent(self, event):
        """クローズイベント
        """
        try:
            super(View, self).closeEvent(event)
        except Exception:
            pass

        if self.__root:
            self.__root.close_event()

        if self.__callback_id_list:
            om.MMessage.removeCallbacks(self.__callback_id_list)
            self.__callback_id_list = []

    def addCallback(self, event_str, func):
        """コールバックの追加

        Args:
            event_str (str): イベント文字列
            func (func): コールバック処理
        """
        self.__callback_id_list.append(om.MEventMessage.addEventCallback(event_str, func))

    def add_item_widget(self, widget):
        """アイテムウィジェットの追加

        Args:
            widget (item.Item): アイテムウィジェット
        """

        self.__items_widget.add_item(widget)

    def remove_item_widget(self, widget):
        """アイテムウィジェットの削除

        Args:
            widget (item.Item): 削除するウィジェット
        """

        self.__items_widget.remove_item(widget)

    def clear_item_widgets(self):
        """アイテムウィジェットを全削除
        """

        self.__items_widget.clear_items()

    def widgets(self):
        """全アイテムウィジェットを取得

        Returns:
            [QtWidgets.QWidget]: 全アイテムウィジェットリスト
        """

        return self.__items_widget.widgets()

    def get_index(self, widget):
        """アイテムウィジェットのインデックスを取得

        Args:
            widget (item.Item): アイテムウィジェット

        Returns:
            int: アイテムウィジェットのインデックス
        """

        return self.__items_widget.get_index(widget)


class ScrollWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(ScrollWidget, self).__init__(*args, **kwargs)

        self.__layout = QtWidgets.QFormLayout(self)

    def add_item(self, widget):
        """レイアウトに追加

        Args:
            widget (QtWidgets.QWidget): 追加ウィジェット
        """

        self.__layout.addRow(widget)

    def remove_item(self, widget):
        """レイアウトから削除

        Args:
            widget (QtWidgets.QWidget): 削除ウィジェット
        """
        self.__layout.takeAt(self.get_index(widget))
        widget.deleteLater()

    def clear_items(self):
        """レイアウト内のウィジェットをクリア
        """

        widgets = self.widgets()
        for widget in widgets:
            self.remove_item(widget)

    def widgets(self):
        """レイアウト内のウィジェットを取得

        Returns:
            [QtWidgets.QWidget]: ウィジェットリスト
        """

        item_count = self.__layout.rowCount()
        widgets = []

        for index in range(item_count):
            item = self.__layout.itemAt(index, QtWidgets.QFormLayout.SpanningRole)
            if item:
                widgets.append(item.widget())

        return widgets

    def get_index(self, widget):
        """レイアウト内のウィジェットのインデックスを取得

        Args:
            widget (QtWidgets.QWidget): レイアウト内のウィジェット

        Returns:
            int: レイアウト内のウィジェットのインデックス
        """

        return self.__layout.getItemPosition(self.__layout.indexOf(widget))[0]
