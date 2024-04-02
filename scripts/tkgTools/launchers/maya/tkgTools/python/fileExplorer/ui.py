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

        # ウィンドウタイトルの設定
        self.setWindowTitle(self.__class__.__name__)

        self.dirPath = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
        self.dataPath = '{}/{}'.format(self.dirPath, 'data')
        self.iconsPath = '{}/{}'.format(self.dirPath, 'icons')
        self.bookmarksPath = '{}/{}'.format(self.dataPath, 'bookmarks')

        pathDirs = [self.dataPath, self.iconsPath, self.bookmarksPath]
        for path in pathDirs:
            if not os.path.isdir(path):
                os.makedirs(path)

        # ドライブの取得
        self.drives = [drive.absolutePath() for drive in QDir.drives()]
        self.fileView = FileView(self)
        self.bookmarkView = FileView(self)

        self.widgets()
        self.addPathInput()
        self.addSearchLineEdit()
        self.addDriveSelection()
        self.addBookmarkView()
        self.addFileView()

        # initialize
        self.setDefaultDrive()
        self.pathStock = []

    def widgets(self):
        self.setGeometry(10, 10, 960, 540)

        # set widget
        self.topWidget = QWidget(self)
        self.setCentralWidget(self.topWidget)

        # set layout
        self.topVboxLayout = QVBoxLayout(self)
        self.topWidget.setLayout(self.topVboxLayout)

        # top hori layout
        self.pathVboxLayout = QVBoxLayout(self)
        self.topVboxLayout.addLayout(self.pathVboxLayout)

        # top tree layout
        self.treeHboxLayout = QHBoxLayout(self)
        self.topVboxLayout.addLayout(self.treeHboxLayout)

        # QSplitter
        self.splitterHorizontal = QSplitter(Qt.Horizontal)
        self.treeHboxLayout.addWidget(self.splitterHorizontal)

    def addPathInput(self):
        # パス入力用のテキストフィールドを追加
        self.pathInput = QLineEdit()
        self.pathInput.setPlaceholderText('Enter path to focus...')
        self.pathInput.returnPressed.connect(self.focusOnPath)
        self.pathVboxLayout.addWidget(self.pathInput)

    def focusOnPath(self):
        path = self.pathInput.text()
        path = path.replace('\\', '/')
        self.pathInput.setText(path)
        self.fileView.focusOnPath(path)
        if path in self.pathStock:
            self.pathStock.remove(path)
        self.pathStock.append(path)

    # ファイル検索用
    def addSearchLineEdit(self):
        # 検索用のフィールド
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText('Search...')
        self.searchBar.textChanged.connect(self.fileView.searchFiles)
        self.pathVboxLayout.addWidget(self.searchBar)

    # ドライブの選択
    def addDriveSelection(self):
        # ドライブ選択用のComboBoxを追加
        self.driveComboBox = QComboBox()
        self.driveComboBox.addItems(self.drives)
        self.driveComboBox.currentIndexChanged.connect(self.changeDrive)
        self.pathVboxLayout.addWidget(self.driveComboBox)

    def setDefaultDrive(self):
        selectedDrivePath = self.drives[0]
        self.fileView.changeRootPath(selectedDrivePath)

    def changeDrive(self, index):
        selectedDrivePath = self.drives[index]
        self.fileView.changeRootPath(selectedDrivePath)

    # Treeを追加
    def addFileView(self):
        self.splitterHorizontal.addWidget(self.fileView)

    # ブックマークビューメソッド
    def addBookmarkView(self):
        self.splitterHorizontal.addWidget(self.bookmarkView)
        self.bookmarkView.changeRootPath(self.dataPath)
        self.bookmarkView.menuActions['Add Bookmark'] = {'cmd':partial(self.showBookmarkDialog)}

    def showBookmarkDialog(self):
        self.bookmarkDialog = QDialog(self)
        bookmarkVBoxLayout = QVBoxLayout()
        self.bookmarkDialog.setLayout(bookmarkVBoxLayout)

        bookmarkFile = ''
        if self.bookmarkView.curFilePath.endswith('.json'):
            bookmarkFile = os.path.splitext(os.path.basename(self.bookmarkView.curFilePath))[0]

        self.bookmarkFileNameText = QLineEdit(bookmarkFile)
        self.bookmarkFileNameText.setPlaceholderText('Enter Bookmark File Name...')
        bookmarkVBoxLayout.addWidget(self.bookmarkFileNameText)

        self.bookmarkKeyNameText = QLineEdit()
        self.bookmarkKeyNameText.setPlaceholderText('Enter Bookmark Key Name...')
        bookmarkVBoxLayout.addWidget(self.bookmarkKeyNameText)

        bookmarkOkBtn = QPushButton('OK')
        bookmarkVBoxLayout.addWidget(bookmarkOkBtn)
        bookmarkOkBtn.clicked.connect(self.addBookmark)

        self.bookmarkDialog.setWindowTitle('Add Bookmark')
        self.bookmarkDialog.exec_()

    # ブックマーク追加
    def addBookmark(self):        
        # ブックマークデータをJSONファイルに保存
        bookmarkDir = self.bookmarkView.curFilePath
        if os.path.isfile(self.bookmarkView.curFilePath):
            bookmarkDir = '/'.join(self.bookmarkView.curFilePath.split('/')[0:-1])
        bookmarkFilePath = '{}/{}.json'.format(bookmarkDir, self.bookmarkFileNameText.text())

        bookmarkData = None
        if os.path.isfile(bookmarkFilePath):
            with open(bookmarkFilePath, 'r', encoding="utf-8") as f:
                bookmarkData = json.load(f, object_pairs_hook=OrderedDict)

        if not bookmarkData:
            bookmarkData = {self.bookmarkKeyNameText.text(): self.fileView.curFilePath}

        elif bookmarkData:
            bookmarkData[self.bookmarkKeyNameText.text()] = self.fileView.curFilePath

        with open(bookmarkFilePath, 'w') as bookmarkFile:
            json.dump(bookmarkData, bookmarkFile, indent=4)


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

        # 右クリックメニューを有効にする
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

        # 右クリックメニューに追加する機能
        self.menuActions = OrderedDict()
        self.menuActions['Create New Folder'] = {'cmd':partial(self.showCreateDirDialog)}
        self.menuActions['Show in Explorer'] = {'cmd':partial(self.showInExplorer)}

        # 現在のパスを返す
        self.curFilePath = None
        self.clicked.connect(self.getPath)

    # 選択項目の取得
    def getPath(self, index):
        indexSource = self.proxyModel.mapToSource(index)
        self.curFilePath = self.fileSystemModel.filePath(indexSource)

    # ファイル検索メソッド
    def searchFiles(self, pattern):
        if pattern.strip() == '*':
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

    # 右クリック用のメニュー
    def openMenu(self, position):
        sender = self.sender()
        self.contextMenu = QMenu(sender)

        for menuName, menuCmd in self.menuActions.items():
            action = self.contextMenu.addAction(menuName)
            action.triggered.connect(menuCmd['cmd'])

        # QMenuの表示
        self.contextMenu.exec_(sender.mapToGlobal(position))


    # フォルダ作成
    def showCreateDirDialog(self):
        self.createDirDialog = QDialog(self)
        createDirVBoxLayout = QVBoxLayout()
        self.createDirDialog.setLayout(createDirVBoxLayout)

        self.folderNameText = QLineEdit()
        createDirVBoxLayout.addWidget(self.folderNameText)

        createDirOkBtn = QPushButton('OK')
        createDirVBoxLayout.addWidget(createDirOkBtn)
        createDirOkBtn.clicked.connect(self.createDir)

        self.createDirDialog.setWindowTitle('Create Directory')
        self.createDirDialog.exec_()

    def createDir(self):
        folderName = self.folderNameText.text()
        newDir = '{}/{}'.format(self.curFilePath, folderName)
        if not os.path.isdir(newDir):
            os.makedirs(newDir)
        else:
            print('{} already exists'.format(newDir))
        # self.showCreateDirDialog.close()

    # エクスプローラで表示
    def showInExplorer(self):
        if os.name == 'nt':
            path = self.curFilePath.replace('/', '\\')
            subprocess.Popen('explorer /select,"{}"'.format(path))
        elif os.name == 'posix':
            subprocess.Popen(['open', '-R', self.curFilePath])


if __name__ == '__main__':
    ui = FileExplorer()
    ui.show(dockable=True)
