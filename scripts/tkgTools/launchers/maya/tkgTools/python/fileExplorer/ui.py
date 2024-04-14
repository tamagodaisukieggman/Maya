# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

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
import shutil
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

ver = cmds.about(v=True)

if int(ver) >= 2025:
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from PySide6 import __version__
    from shiboken6 import wrapInstance
else:
    try:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
        from PySide2 import __version__
        from shiboken2 import wrapInstance
    except Exception as e:
        from PySide.QtCore import *
        from PySide.QtGui import *
        from PySide import __version__
        from shiboken import wrapInstance


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
        self.drives = []
        [self.drives.append(drive.absolutePath()) for drive in QDir.drives()]

        # Treeの作成
        self.fileView = FileView(self)
        self.bookmarkView = FileView(self)

        # My Computerの追加
        self.drives.append(self.fileView.fileSystemModel.myComputer())

        # 構築
        self.widgets()
        self.addPathInput()
        self.addSearchLineEdit()
        self.addNamespaceLineEdit()
        self.addDriveSelection()
        self.addBookmarkView()
        self.addFileView()

        # initialize
        self.setDefaultDrive()
        self.pathStock = []
        self.bookmarkData = None

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
        self.pathInput.textChanged.connect(self.focusOnPath)
        self.pathVboxLayout.addWidget(self.pathInput)
        self.fileView.pathInput = self.pathInput

        self.selectedPathLine = QLineEdit()
        self.selectedPathLine.setReadOnly(True)
        self.pathVboxLayout.addWidget(self.selectedPathLine)
        # selectedの受け渡し
        self.fileView.selectedPathLine = self.selectedPathLine

        # コピー先のパス
        self.copyDataPathInput = QLineEdit()
        self.copyDataPathInput.setPlaceholderText('To copy data path from selected...')
        # self.copyDataPathInput.textChanged.connect(self.focusOnPath)
        self.pathVboxLayout.addWidget(self.copyDataPathInput)
        self.fileView.copyDataPathInput = self.copyDataPathInput

    def focusOnPath(self):
        path = self.pathInput.text()
        path = path.replace('\\', '/')
        # self.pathInput.setText(path)
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

    # NameSpace
    def addNamespaceLineEdit(self):
        # 検索用のフィールド
        self.namespaceBar = QLineEdit()
        self.namespaceBar.setPlaceholderText('Namespace...')
        self.namespaceBar.textChanged.connect(self.setNamespace)
        self.pathVboxLayout.addWidget(self.namespaceBar)

    def setNamespace(self):
        sender = self.sender()
        self.fileView.namespace = sender.text()

    # ドライブの選択
    def addDriveSelection(self):
        # ドライブ選択用のComboBoxを追加
        self.driveComboBox = QComboBox()
        self.comboBoxes(self.driveComboBox, self.drives)
        self.driveComboBox.currentIndexChanged.connect(self.changeDrive)
        self.pathVboxLayout.addWidget(self.driveComboBox)

    def comboBoxes(self, comboBox=None, listItems=None):
        comboBox.clear()
        comboBox.addItems(listItems)

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
        # self.bookmarkView.menuActions['Show Bookmark List'] = {'cmd':partial(self.showBookmarkedList)}
        self.bookmarkView.showBookmarkedList = self.showBookmarkedList

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
        self.readBookmark(pop=True)
        # if not self.bookmarkData:
        #     self.bookmarkData = {self.bookmarkKeyNameText.text(): self.fileView.curFilePath}
        #
        # elif self.bookmarkData:
        self.bookmarkData[self.bookmarkKeyNameText.text()] = self.fileView.curFilePath

        sorted_bookmarkData = sorted(self.bookmarkData.items())
        self.bookmarkData = dict((x, y) for x, y in sorted_bookmarkData)

        with open(self.bookmarkFilePath, 'w') as bookmarkFile:
            json.dump(self.bookmarkData, bookmarkFile, indent=4)

    # ブックマークの読み込み
    def readBookmark(self, pop=None):
        if pop:
            bookmarkDir = self.bookmarkView.curFilePath
            if os.path.isfile(bookmarkDir):
                bookmarkDir = '/'.join(bookmarkDir.split('/')[0:-1])
            self.bookmarkFilePath = '{}/{}.json'.format(bookmarkDir, self.bookmarkFileNameText.text())
        else:
            self.bookmarkFilePath = self.bookmarkView.curFilePath

        if os.path.isfile(self.bookmarkFilePath):
            with open(self.bookmarkFilePath, 'r', encoding="utf-8") as f:
                self.bookmarkData = json.load(f, object_pairs_hook=OrderedDict)
        else:
            self.bookmarkData = {}

    def showBookmarkedList(self):
        self.readBookmark()

        _bookmarkData = OrderedDict()
        for keyName, path in self.bookmarkData.items():
            _bookmarkData[keyName] = path

        sorted_bookmarkData = sorted(_bookmarkData.items())
        _bookmarkData = dict((x, y) for x, y in sorted_bookmarkData)

        addedBookmarkActions = OrderedDict()
        if _bookmarkData:
            for keyName, path in _bookmarkData.items():
                actionName = '{} -> {}'.format(keyName, path)
                addedBookmarkActions[actionName] = path
                self.bookmarkView.menuActions[actionName] = {'cmd':partial(self.selectBookmark, path)}

        return addedBookmarkActions

    def selectBookmark(self, path):
        self.pathInput.setText(path)
        self.fileView.curFilePath = path
        if os.path.isdir(path):
            dirname = path
        else:
            dirname = os.path.dirname(path)
        if not dirname in self.drives:
            self.drives.append(dirname)
        self.comboBoxes(self.driveComboBox, self.drives)
        self.driveComboBox.setCurrentText(dirname)

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
        # self.setRootIndex(self.proxyModel.mapFromSource(self.fileSystemModel.index(QDir.homePath())))

        # sortを有効にする
        self.setSortingEnabled(True)

        # showBookmarkedList用
        self.showBookmarkedList = None
        self._bookmarkData = OrderedDict()

        # 右クリックメニューを有効にする
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

        # Namespace用
        self.namespace = None

        # 項目が選択されたとき用
        self.selectedPathLine = None

        # setPathToCopyDataPath用
        self.copyDataPathInput = None
        self.pathInput = None

        # 右クリックメニューに追加する機能
        self.menuActions = OrderedDict()
        self.menuActions['Create New Folder'] = {'cmd':partial(self.showCreateDirDialog)}
        self.menuActions['Show in Explorer'] = {'cmd':partial(self.showInExplorer)}
        self.menuActions['Copy Path in clipboard'] = {'cmd':partial(self.copyPathInClipboard)}
        self.menuActions['Set path to Copy Data Path from selection'] = {'cmd':partial(self.setPathToCopyDataPath)}
        self.menuActions['Go to Copy Data Path'] = {'cmd':partial(self.goToCopyDataPath)}
        self.menuActions['File Open'] = {'cmd':partial(self.fileOpen)}
        self.menuActions['File Import'] = {'cmd':partial(self.fileImport)}
        self.menuActions['File Reference'] = {'cmd':partial(self.fileReference)}
        self.menuActions['File Save'] = {'cmd':partial(self.fileSave)}
        self.menuActions['Text File Viewer'] = {'cmd':partial(self.textFileViewer)}

        # 現在のパスを返す
        self.curFilePath = None
        self.clicked.connect(self.getPath)

        # パスコピー用
        self.clipboard = QClipboard()

    # 選択項目の取得
    def getPath(self, index):
        indexSource = self.proxyModel.mapToSource(index)
        self.curFilePath = self.fileSystemModel.filePath(indexSource)

    # def getPath(self):
    #     sender = self.sender()
    #     indexes = sender.selectionModel().selectedIndexes()
    #     index = indexes[0]
    #     proxyIndex = self.proxyModel.mapFromSource(index)
    #     self.curFilePath = self.fileSystemModel.filePath(proxyIndex)
    #     print(self.curFilePath)

        self.whenGetPath()

    # 選択されたときに実行される
    def whenGetPath(self):
        self.setTextFromPath()

    def setTextFromPath(self):
        if self.selectedPathLine:
            self.selectedPathLine.setText(self.curFilePath)

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
        proxyIndex = self.proxyModel.mapFromSource(self.fileSystemModel.index(path))
        self.setRootIndex(proxyIndex)
        self.scrollTo(proxyIndex, QTreeView.PositionAtCenter)

        # if path == 'My Computer':
        #     self.setRootIndex(self.proxyModel.mapFromSource(self.fileSystemModel.index(path)))
        #     return
        # index = self.fileSystemModel.index(path)
        # if index.isValid():
        #     proxyIndex = self.proxyModel.mapFromSource(index)
        #     self.setRootIndex(proxyIndex)
        #     self.scrollTo(proxyIndex, QTreeView.PositionAtCenter)

    # 右クリック用のメニュー
    def openMenu(self, position):
        sender = self.sender()
        self.contextMenu = QMenu(sender)

        # bookmarksの表示
        if self.showBookmarkedList:
            if self._bookmarkData:
                [self.menuActions.pop(key) for key, value in self._bookmarkData.items()]
            self._bookmarkData = self.showBookmarkedList()

        for menuName, menuCmd in self.menuActions.items():
            action = self.contextMenu.addAction(menuName)
            action.triggered.connect(menuCmd['cmd'])

        # QMenuの表示
        self.contextMenu.exec_(sender.mapToGlobal(position))

    def fileOpen(self):
        file = File(path='{}'.format(self.curFilePath))
        file.fileOpen()

    def fileImport(self):
        file = File(path='{}'.format(self.curFilePath))
        file.fileImport()

    def fileReference(self):
        file = File(path='{}'.format(self.curFilePath), namespace=self.namespace)
        file.fileReference()

    def fileSave(self):
        savePath = self.pathInput.text()
        file = File(path=savePath)
        file.fileSave()

    # テキストファイルを表示
    def textFileViewer(self):
        fileViewer = FileViewer()
        fileViewer.loadFileContent(self.curFilePath)
        fileViewer.show()

    # フォルダ作成
    def showCreateDirDialog(self):
        self.createDirDialog = QDialog(self)
        createDirVBoxLayout = QVBoxLayout()
        self.createDirDialog.setLayout(createDirVBoxLayout)

        self.folderNameText = QLineEdit()
        createDirVBoxLayout.addWidget(self.folderNameText)

        self.createChrDirCheck = QCheckBox('Character Forlder')
        createDirVBoxLayout.addWidget(self.createChrDirCheck)

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

        if self.createChrDirCheck.isChecked():
            chrDirs = ['scenes', 'fbx', 'sourceimages']
            for chrD in chrDirs:
                if not os.path.isdir('{}/{}'.format(newDir, chrD)):
                    os.makedirs('{}/{}'.format(newDir, chrD))

    # エクスプローラで表示
    def showInExplorer(self):
        if os.name == 'nt':
            path = self.curFilePath.replace('/', '\\')
            subprocess.Popen('explorer /select,"{}"'.format(path))
        elif os.name == 'posix':
            subprocess.Popen(['open', '-R', self.curFilePath])

    def copyPathInClipboard(self):
        self.clipboard.setText(self.curFilePath)

    def setPathToCopyDataPath(self):
        self.copyDataPathInput.setText(self.curFilePath)

    def goToCopyDataPath(self):
        copyDataPath = self.copyDataPathInput.text()
        copyPathDir = os.path.dirname(copyDataPath)
        if not os.path.isdir(copyPathDir):
            os.makedirs(copyPathDir)
        if not os.path.isfile(copyDataPath):
            shutil.copy(self.curFilePath, copyDataPath)
        self.pathInput.setText(copyDataPath)

class File:
    def __init__(self, path=None, namespace=None):
        self.path = path
        self.namespace = namespace

        self.settings = None
        self.resetSettings()

    def resetSettings(self):
        self.settings = OrderedDict({
            'ignoreVersion':True,
        })

    def fileOpen(self):
        self.settings['options'] = "v=0;p=17;f=0"
        self.settings['o'] = True
        self.settings['f'] = True
        self.doFileCommand()

    def fileImport(self):
        self.settings['options'] = "v=0;p=17;f=0"
        self.settings['pr'] = True
        self.settings['i'] = True
        self.settings['mergeNamespacesOnClash'] = False
        self.settings['importTimeRange'] = 'combine'
        self.doFileCommand()

    def fileReference(self):
        self.settings['options'] = "v=0;"
        self.settings['namespace'] = self.namespace
        self.settings['r'] = True
        self.settings['gl'] = True
        self.settings['mergeNamespacesOnClash'] = True
        self.doFileCommand()

    def fileSave(self):
        if self.path.endswith('.mb'):
            fileType = 'mayaBinary'
        elif self.path.endswith('.ma'):
            fileType = 'mayaAscii'

        cmds.file(rn=self.path)
        self.settings.pop('ignoreVersion')
        self.settings['type'] = fileType
        self.settings['options'] = "v=0;"
        self.settings['save'] = True
        self.doSaveFileCommand()

    def doFileCommand(self):
        if os.path.isfile(self.path):
            cmds.file(self.path, **self.settings)
        self.resetSettings()

    def doSaveFileCommand(self):
        saveDir = os.path.dirname(self.path)
        if not os.path.isdir(saveDir):
            os.makedirs(saveDir)
        cmds.file(**self.settings)
        self.resetSettings()

class FileViewer(MayaQWidgetDockableMixin, QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ウィンドウタイトルの設定
        self.setWindowTitle(self.__class__.__name__)

        self.widgets()

    def widgets(self):
        # self.setGeometry(10, 10, 960, 540)

        # set widget
        self.topWidget = QWidget(self)
        self.setCentralWidget(self.topWidget)

        # set layout
        self.topHboxLayout = QHBoxLayout(self)
        self.topWidget.setLayout(self.topHboxLayout)

        # テキストエディタの設定
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)  # 編集不可に設定
        self.topHboxLayout.addWidget(self.textEdit)

    def loadFileContent(self, filePath):
        file = QFile(filePath)
        if file.open(QFile.ReadOnly | QFile.Text):
            textStream = QTextStream(file)
            self.textEdit.setText(textStream.readAll())
            file.close()
        else:
            self.textEdit.setText("ファイルを開くことができませんでした。")

if __name__ == '__main__':
    ui = FileExplorer()
    ui.show(dockable=True)
