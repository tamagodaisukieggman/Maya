# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance

import base64
import codecs
from collections import OrderedDict
import fnmatch
from functools import partial
import glob
from imp import reload
import json
import math
import os
import pickle
import re
import subprocess
import sys
import time
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from timeit import default_timer as timer
import traceback

from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui
import maya.api.OpenMaya as om2
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin

class FileExplorer(MayaQWidgetDockableMixin, QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(self.__class__.__name__)

        # ドライブの取得
        self.drives = [drive.absolutePath() for drive in QDir.drives()]
        self.fileView = FileView(self)

        self.widgets()
        self.addPathInput()
        self.addSearchLineEdit()
        self.addDriveSelection()
        self.addFileView()

    def widgets(self):
        self.setGeometry(10, 10, 960, 540)

        # set widget
        self.top_widget = QWidget(self)
        self.setCentralWidget(self.top_widget)

        # set layout
        self.top_vbox_layout = QVBoxLayout(self)
        self.top_widget.setLayout(self.top_vbox_layout)

        # top horizontal
        self.top_hbox_layout = QHBoxLayout(self)
        self.top_vbox_layout.addLayout(self.top_hbox_layout)

        # vertical A in top horizontal
        self.top_vbox_A_layout = QVBoxLayout(self)
        self.top_hbox_layout.addLayout(self.top_vbox_A_layout)

    def addPathInput(self):
        # パス入力用のテキストフィールドを追加
        self.pathInput = QLineEdit()
        self.pathInput.setPlaceholderText("Enter path to focus...")
        self.pathInput.returnPressed.connect(self.focusOnPath)
        self.top_vbox_layout.addWidget(self.pathInput)

    def focusOnPath(self):
        path = self.pathInput.text()
        self.fileView.focusOnPath(path)

    def addSearchLineEdit(self):
        # 検索用のフィールド
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.fileView.searchFiles)
        self.top_vbox_layout.addWidget(self.searchBar)

    # ドライブの選択
    def addDriveSelection(self):
        # ドライブ選択用のComboBoxを追加
        self.driveComboBox = QComboBox()
        self.driveComboBox.addItems(self.drives)
        self.driveComboBox.currentIndexChanged.connect(self.changeDrive)
        self.top_vbox_layout.addWidget(self.driveComboBox)

    def changeDrive(self, index):
        selectedDrivePath = self.drives[index]
        self.fileView.changeRootPath(selectedDrivePath)

    # Treeを追加
    def addFileView(self):
        self.top_vbox_layout.addWidget(self.fileView)

class FileView(QTreeView):
    def __init__(self, parent=None):
        super(FileView, self).__init__(parent)

        # ファイルシステムモデルの設定
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files)
        self.fileSystemModel.setRootPath(QDir.rootPath())
        self.fileSystemModel.setNameFilterDisables(False)

        # ソート/フィルタリング用のプロキシモデルの設定
        self.proxyModel = QSortFilterProxyModel(self)
        self.proxyModel.sort(3)
        self.proxyModel.setSourceModel(self.fileSystemModel)

        # プロキシモデルをビューに設定
        self.setModel(self.proxyModel)

        # ルートパスを設定（ここではホームディレクトリを例としています）
        self.setRootIndex(self.proxyModel.mapFromSource(self.fileSystemModel.index(QDir.homePath())))

        # sortを有効にする
        self.setSortingEnabled(True)

    # ファイル検索メソッド
    def searchFiles(self, pattern):
        if pattern.strip() == "*":
            return

        if pattern:  # 検索パターンが空ではない場合
            regExp = QRegExp(pattern, Qt.CaseInsensitive, QRegExp.Wildcard)
            self.proxyModel.setFilterRegExp(regExp)
        else:  # 検索バーが空の場合は全て表示
            self.proxyModel.setFilterRegExp(QRegExp())

        self.expandAllMatchedItems()

    def expandAllMatchedItems(self):
        for i in range(self.proxyModel.rowCount()):
            index = self.proxyModel.index(i, 0)
            self.expandAllChildren(index)

    def expandAllChildren(self, index):
        if not index.isValid():
            return

        self.expand(index)  # 親アイテムを展開

        rowCount = self.proxyModel.rowCount(index)
        for i in range(rowCount):
            childIndex = self.proxyModel.index(i, 0, index)
            self.expandAllChildren(childIndex)

    def focusOnPath(self, path):
        index = self.fileSystemModel.index(path)
        if index.isValid():
            # プロキシモデルを介して正しいインデックスを取得
            proxyIndex = self.proxyModel.mapFromSource(index)
            # インデックスにスクロールしてフォーカスを移動
            self.scrollTo(proxyIndex, QTreeView.PositionAtCenter)
            self.setCurrentIndex(proxyIndex)

    def mousePressEvent(self, event):
        # Shiftキーが押されたかどうかをチェック
        if event.modifiers() & Qt.ShiftModifier:
            index = self.indexAt(event.pos())
            if index.isValid():
                # アイテムが展開されているかどうかで、折りたたむまたは展開する
                if self.isExpanded(index):
                    self.collapseRecursively(index)
                else:
                    self.expandRecursively(index)
                return  # 早期リターンしてデフォルトの処理をスキップ

        # Shiftキーが押されていない場合は、デフォルトの処理を実行
        super(FileView, self).mousePressEvent(event)

    def collapseRecursively(self, index):
        # このアイテムとすべての子孫を折りたたむ
        self.collapse(index)
        for row in range(self.model().rowCount(index)):
            childIndex = self.model().index(row, 0, index)
            if self.model().hasChildren(childIndex):
                self.collapseRecursively(childIndex)

    def expandRecursively(self, index):
        # このメソッドは必要に応じて実装してください。Qt 5.13以上ではQTreeViewにexpandRecursivelyが既に存在します。
        pass

    # ドライブ選択用のメソッド
    def changeRootPath(self, path):
        index = self.fileSystemModel.index(path)
        if index.isValid():
            proxyIndex = self.proxyModel.mapFromSource(index)
            self.setRootIndex(proxyIndex)
            self.scrollTo(proxyIndex, QTreeView.PositionAtCenter)

if __name__ == '__main__':
    ui = FileExplorer()
    ui.show(dockable=True)
