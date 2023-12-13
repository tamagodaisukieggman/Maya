# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import time
import math

from PySide2 import QtCore, QtGui, QtWidgets

from .. import utility

try:
    # Maya2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(utility)


def convert_size(size):
    units = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB')
    i = int(math.floor(math.log(size, 1024)) if size > 0 else 0)
    size = round(size / 1024 ** i, 2)

    return '{} {}'.format(size, units[i])


class FileInfo(object):
    """ファイル情報"""

    headers = ['Name', 'Size', 'Type', 'UpdateDateTime']
    row_count = len(headers)

    def __init__(self, file_path):
        """_summary_

        Args:
            path (_type_): _description_
        """
        self.path = file_path
        self.exists = os.path.exists(self.path)

        size = convert_size(os.path.getsize(file_path)) if self.exists else '0 B'
        type = os.path.splitext(file_path)[-1] if self.exists else ''
        update_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(os.path.getmtime(file_path))) if self.exists else '0000'

        self.info_dict = {
            'Name': os.path.basename(file_path),
            'Size': size,
            'Type': type,
            'UpdateDateTime': update_time
        }

        self.icon_pixmap = None
        if os.path.splitext(file_path)[-1] == '.ma' or os.path.splitext(file_path)[-1] == '.mb':
            self.icon_pixmap = QtGui.QPixmap(utility.get_icon_path('maya.png'))
        elif os.path.splitext(file_path)[-1] == '.fbx':
            self.icon_pixmap = QtGui.QPixmap(utility.get_icon_path('fbx.png'))


class FileTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        """初期化

        Args:
            parent (_type_, optional): _description_. Defaults to None.
        """
        super(FileTableModel, self).__init__(parent)
        self.items = []

    def refresh(self, itemPaths):
        """情報を更新

        Args:
            itemPaths ([str]): ファイルパスのリスト
        """

        self.layoutAboutToBeChanged.emit()
        self.setItems(itemPaths)
        self.modelAboutToBeReset.emit()
        self.modelReset.emit()
        self.layoutChanged.emit()

    def setItems(self, itemPaths):
        """itemsを更新

        Args:
            itemPaths ([str]): ファイルパスのリスト
        """

        self.items = []
        for path in itemPaths:
            self.items.append(FileInfo(path))

    def headerData(self, col, orientation, role):
        """見出しを返す
        """

        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return FileInfo.headers[col]
        return None

    def rowCount(self, parent):
        """行数を返す
        """
        return len(self.items)

    def columnCount(self, parent):
        """カラム数を返す
        """
        return FileInfo.row_count

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
            if index.column() == item.headers.index('Name') and item.icon_pixmap:
                return item.icon_pixmap
        elif role == QtCore.Qt.ToolTipRole:
            return item.path

        return None
