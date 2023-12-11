# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

from PySide2 import QtCore, QtGui

from .. import utility
from .. import const

try:
    # Maya2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(utility)
reload(const)


class CopyInfo(object):
    """コピー情報"""

    headers = ['コピー元', 'コピー先', 'ステータス']
    row_count = len(headers)

    def __init__(self, copy_data_info):
        """_summary_

        Args:
            path (_type_): _description_
        """

        self.copy_data_info = copy_data_info

        self.info_dict = {
            'コピー元': self.copy_data_info.src_relative,
            'コピー先': self.copy_data_info.dst_relative,
            'ステータス': self.copy_data_info.status,
        }

        self.is_enable = True
        ext = os.path.splitext(self.copy_data_info.src_path)[-1]

        self.path_icon_pixmap = None

        if not ext:
            self.path_icon_pixmap = QtGui.QPixmap(utility.get_icon_path('folder.png'))
        if ext == '.ma' or ext == '.mb':
            self.path_icon_pixmap = QtGui.QPixmap(utility.get_icon_path('maya.png'))
        elif ext == '.fbx':
            self.path_icon_pixmap = QtGui.QPixmap(utility.get_icon_path('fbx.png'))
        else:
            self.path_icon_pixmap = QtGui.QPixmap(utility.get_icon_path('file.png'))

        self.status_icon_pixmap = None

        if copy_data_info.status in const.WARNING_STATUSES:
            self.status_icon_pixmap = QtGui.QPixmap(utility.get_icon_path('caution.png'))
        elif copy_data_info.status in const.ERROR_STATUSES:
            self.status_icon_pixmap = QtGui.QPixmap(utility.get_icon_path('ng.png'))
        else:
            self.status_icon_pixmap = QtGui.QPixmap(utility.get_icon_path('ok.png'))


class InfoTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        """初期化

        Args:
            parent (_type_, optional): _description_. Defaults to None.
        """
        super(InfoTableModel, self).__init__(parent)
        self.items = []

    def refresh(self, copy_data_infos):
        """情報を更新

        Args:
            itemPaths ([str]): ファイルパスのリスト
        """

        self.layoutAboutToBeChanged.emit()
        self.setItems(copy_data_infos)
        self.modelAboutToBeReset.emit()
        self.modelReset.emit()
        self.layoutChanged.emit()

    def setItems(self, copy_data_infos):
        """itemsを更新

        Args:
            itemPaths ([str]): ファイルパスのリスト
        """

        self.items = []
        for copy_data_info in copy_data_infos:
            this_info = CopyInfo(copy_data_info)
            self.items.append(this_info)

    def headerData(self, col, orientation, role):
        """見出しを返す
        """

        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return CopyInfo.headers[col]
        return None

    def flags(self, index):

        return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def rowCount(self, parent):
        """行数を返す
        """
        return len(self.items)

    def columnCount(self, parent):
        """カラム数を返す
        """
        return CopyInfo.row_count

    def data(self, index, role):
        """データを返す
        """
        if not index.isValid():
            return None

        item = self.items[index.row()]

        if role == QtCore.Qt.DisplayRole:

            return item.info_dict[item.headers[index.column()]]

        elif role == QtCore.Qt.TextAlignmentRole:

            return int(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        elif role == QtCore.Qt.DecorationRole:

            if index.column() == item.headers.index('コピー元') and item.path_icon_pixmap:
                return item.path_icon_pixmap
            elif index.column() == item.headers.index('ステータス') and item.status_icon_pixmap:
                return item.status_icon_pixmap

        elif role == QtCore.Qt.CheckStateRole:

            if index.column() == item.headers.index('コピー元'):
                return QtCore.Qt.Checked if item.is_enable else QtCore.Qt.Unchecked

        return None

    def setData(self, index, value, role):
        """データをセット
        """

        if not index.isValid():
            return None

        if role == QtCore.Qt.CheckStateRole and index.column() == self.items[index.row()].headers.index('コピー元'):
            if value == QtCore.Qt.Checked:
                self.items[index.row()].is_enable = True
            else:
                self.items[index.row()].is_enable = False
            self.dataChanged.emit(index, index)

        return True

    def setCheckState(self, row, is_enable):
        """チェックボックスのステート変更

        Args:
            row (int): 変更したい行
            is_enable (bool): 値
        """

        index = self.index(row, self.items[row].headers.index('コピー元'))
        value = QtCore.Qt.Checked if is_enable else QtCore.Qt.Unchecked
        self.setData(index, value, QtCore.Qt.CheckStateRole)
