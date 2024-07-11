#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Qt_TkgSceneOpener.py
#

from __future__ import print_function

import codecs  # python2系でopen関数にencoding引数を実装するため

try:
    # Maya 2022-
    from builtins import object
    from builtins import range
    from builtins import str
    from past.utils import old_div
except Exception:
    pass

try:
    # Maya 2022-
    from urllib.parse import urlencode
    from urllib.request import urlopen
except Exception:
    from urllib import urlencode
    from urllib2 import urlopen

import sys
import os
import re
import time
import datetime
import threading
import subprocess
import json

try:
  from PySide2.QtCore import *
  from PySide2.QtGui import *
  from PySide2.QtWidgets import *
  from PySide2 import __version__
  from shiboken2 import wrapInstance
  print( "Use Pyside2" )

except ImportError:
  from PySide.QtCore import *
  from PySide.QtGui import *
  from PySide import __version__
  from shiboken import wrapInstance
  print( "Use Pyside(1)" )

import pymel.util.path as pmp
import pymel.core as pm

import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as OpenMayaUI


g_toolName = "TkgSceneOpener"
g_toolVersion = "2.1.2"
g_refecrenceOptionVar = "TkgSceneOpenerReferenceOptionVar"


class TkgSceneOpener(QMainWindow):
    syncCurrentPathSignal = Signal(str)
    setPreviewPathSignal = Signal(str)
    addBookmarkSignal = Signal(str)

    def get_maya_window(self):
        #from shiboken import wrapInstance
        if sys.version_info.major == 2:
            return wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QWidget)
        else:
            # for Maya 2022-
            return wrapInstance(int(OpenMayaUI.MQtUtil.mainWindow()), QWidget)

    def __init__(self, parent=None):
        super(TkgSceneOpener, self).__init__(self.get_maya_window())
        self.__ui = Ui_TkgSceneOpener()
        self.__ui.setupUi(self)
        self.setup()

    def setup(self):
        self.currentPath = ""

        self.dialog_Option = Dialog_Option(self)

        self.widget_directory = Widget_Directory(self)
        self.__ui.splitter_left.addWidget(self.widget_directory)

        self.tabWidget = QTabWidget(self.__ui.splitter_left)
        self.tabWidget.setMinimumSize(QSize(1, 1))

        self.widget_bookmark = Widget_Bookmark(self)
        self.tabWidget.addTab(self.widget_bookmark, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget_bookmark), u"ブックマーク")

        self.widget_recentFile = Widget_RecentFile(self)
        self.tabWidget.addTab(self.widget_recentFile, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget_recentFile), u"最近使ったファイル")

        self.widget_file = Widget_File(self)
        self.__ui.verticalLayout_center.addWidget(self.widget_file)

        self.widget_historyButtons = Widget_HistoryButtons(self)
        self.__ui.horizontalLayout_centerTop.addWidget(self.widget_historyButtons)

        self.lineEdit_path = LineEdit_Path(self)
        self.__ui.horizontalLayout_centerTop.addWidget(self.lineEdit_path)

        self.widget_preview = Widget_Preview(self)
        self.__ui.splitter_main.addWidget(self.widget_preview)

        self.setSlot()

        self.readSettings()
        # ツリーの生成が間に合わないと指定したパスにスクロールされないため、１秒待ってパスを再設定する
        QTimer.singleShot(1000, lambda: self.widget_directory.setCurrentPath(self.widget_directory.getCurrentPath()))

    def setSlot(self):
        self.__ui.action_option.triggered.connect(self.openOption)

    def openOption(self):
        self.dialog_Option.show()

    def closeEvent(self, event):
        self.writeSettings()

    def resizeEvent(self, event):
        self.storeWindowGeomery()

    def moveEvent(self, event):
        self.storeWindowGeomery()

    def storeWindowGeomery(self):
        if self.isMaximized() == False:
            self.wpos = self.pos()
            self.wsize = self.size()

    def syncCurrentPath(self, path):
        self.currentPath = path
        self.syncCurrentPathSignal.emit(path)

    def setPreviewPath(self, path):
        self.setPreviewPathSignal.emit(path)

    def addBookmark(self, path):
        self.addBookmarkSignal.emit(path)

    def getPreviewOption(self):
        return self.dialog_Option.getPreviewOption()

    def getSelectOption(self):
        return self.dialog_Option.getSelectOption()

    def getSelectOption_scriptNode(self):
        return self.dialog_Option.getSelectOption_scriptNode()

    def getExpandFolderWhenClickOption(self):
        return self.dialog_Option.getExpandFolderWhenClickOption()

    def readSettings(self):
        settingFilePath = Utility.getSettingFilePath()
        self.settings = QSettings(settingFilePath, QSettings.IniFormat)
        self.settings.beginGroup(g_toolName)
        state = self.settings.value("state")
        if state is not None:
            self.restoreState(state)
        geometry = self.settings.value("geometry")
        if geometry is not None:
            self.restoreGeometry(geometry)
        isMaximized = self.settings.value("maximized")
        if isMaximized == "true":
            self.move(self.settings.value("pos", self.pos()))
            self.resize(self.settings.value("size", self.size()))
            self.wpos = self.pos()
            self.wsize = self.size()
            self.showMaximized()
        splitterSizes = self.settings.value("splitterSizes")
        if splitterSizes is not None:
            self.__ui.splitter_main.restoreState(splitterSizes)
        last_path = self.settings.value("last_path")
        if last_path is not None:
            self.currentPath = last_path
            self.syncCurrentPath(self.currentPath)
        else:
            self.currentPath = Utility.getRootPath()
            self.syncCurrentPath(self.currentPath)
        self.settings.endGroup()

    def writeSettings(self):
        settingFilePath = Utility.getSettingFilePath()
        self.settings = QSettings(settingFilePath, QSettings.IniFormat)
        self.settings.beginGroup(g_toolName)
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("state", self.saveState())
        self.settings.setValue("maximized", self.isMaximized())
        if self.isMaximized() == True:
            self.settings.setValue("pos", self.wpos)
            self.settings.setValue("size", self.wsize)
        self.settings.setValue(
            "splitterSizes", self.__ui.splitter_main.saveState())
        self.settings.setValue("last_path", self.currentPath)
        self.settings.endGroup()


class Ui_TkgSceneOpener(object):
    def setupUi(self, TkgSceneOpener):
        TkgSceneOpener.setObjectName("TkgSceneOpener")
        TkgSceneOpener.resize(788, 391)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TkgSceneOpener.sizePolicy().hasHeightForWidth())
        TkgSceneOpener.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(TkgSceneOpener)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter_main = QSplitter(self.centralwidget)
        self.splitter_main.setOrientation(Qt.Horizontal)
        self.splitter_main.setObjectName("splitter_main")
        self.splitter_left = QSplitter(self.splitter_main)
        self.splitter_left.setOrientation(Qt.Vertical)
        self.splitter_left.setObjectName("splitter_left")
        self.verticalLayoutWidget_2 = QWidget(self.splitter_main)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_center = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_center.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_center.setObjectName("verticalLayout_center")
        self.horizontalLayout_centerTop = QHBoxLayout()
        self.horizontalLayout_centerTop.setObjectName("horizontalLayout_centerTop")
        self.verticalLayout_center.addLayout(self.horizontalLayout_centerTop)
        self.gridLayout.addWidget(self.splitter_main, 0, 0, 1, 1)
        TkgSceneOpener.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(TkgSceneOpener)
        self.menuBar.setGeometry(QRect(0, 0, 788, 24))
        self.menuBar.setObjectName("menuBar")
        self.menu_setting = QMenu(self.menuBar)
        self.menu_setting.setObjectName("menu_setting")
        TkgSceneOpener.setMenuBar(self.menuBar)
        self.action_option = QAction(TkgSceneOpener)
        self.action_option.setObjectName("action_option")
        self.menu_setting.addAction(self.action_option)
        self.menuBar.addAction(self.menu_setting.menuAction())
        self.retranslateUi(TkgSceneOpener)
        #self.tabWidget.setCurrentIndex(1)
        QMetaObject.connectSlotsByName(TkgSceneOpener)

    def retranslateUi(self, TkgSceneOpener):
        try:
            TkgSceneOpener.setWindowTitle(QApplication.translate("TkgSceneOpener", "TkgSceneOpener", None, QApplication.UnicodeUTF8))
            self.menu_setting.setTitle(QApplication.translate("TkgSceneOpener", "設定", None, QApplication.UnicodeUTF8))
            self.action_option.setText(QApplication.translate("TkgSceneOpener", "オプション", None, QApplication.UnicodeUTF8))
        except:
            TkgSceneOpener.setWindowTitle(QApplication.translate("TkgSceneOpener", "TkgSceneOpener", None))
            self.menu_setting.setTitle(QApplication.translate("TkgSceneOpener", "設定", None))
            self.action_option.setText(QApplication.translate("TkgSceneOpener", "オプション", None))



class Widget_Directory(QWidget):

    def __init__(self, parent=None):
        super(Widget_Directory, self).__init__(parent)
        self.widgetName = "Widget_Directory"
        self.parent = parent
        self.__ui = Ui_Widget_Directory()
        self.__ui.setupUi(self)
        self.setup()

    def setup(self):
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.__ui.treeView_directory.setModel(self.model)
        self.__ui.treeView_directory.setRootIndex(QModelIndex())
        self.__ui.treeView_directory.setRootIsDecorated(False)
        self.__ui.treeView_directory.setHeaderHidden(True)
        self.__ui.treeView_directory.hideColumn(1)
        self.__ui.treeView_directory.hideColumn(2)
        self.__ui.treeView_directory.hideColumn(3)

        self.__ui.treeView_directory.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__ui.treeView_directory.customContextMenuRequested.connect(self.setContextMenu)

        self.setSlot()

    def setSlot(self):
        self.parent.syncCurrentPathSignal.connect(self.setCurrentPath)
        self.__ui.treeView_directory.clicked[QModelIndex].connect(self.clickEvent)
        self.__ui.treeView_directory.doubleClicked[QModelIndex].connect(self.doubleClickEvent)

    def clickEvent(self):
        path = self.getCurrentPath()
        self.parent.syncCurrentPath(path)
        self.parent.setPreviewPath(path)

    def doubleClickEvent(self):
        path = self.getCurrentPath()
        if(os.path.isfile(path)):
            if(MayaUtility.isSceneFile(path)):
                MayaUtility.openSceneFile(path, self.parent.getSelectOption_scriptNode())
            else:
                Utility.openFile(path)

    def getCurrentPath(self):
        index = self.__ui.treeView_directory.currentIndex()
        path = self.model.filePath(index)
        return path

    def setCurrentPath(self, path):
        index = self.model.index(path)
        self.__ui.treeView_directory.setCurrentIndex(index)
        self.scrollTarget = path
        if self.parent.getExpandFolderWhenClickOption():
            self.__ui.treeView_directory.expand(index)

        # ツリーの構築を待ってスクロール
        # threading.Timerを使うとUI構築時にエラーになることがあるためQTimerを使用
        QTimer.singleShot(400, lambda: self.scrollDirectory(path))

    def scrollDirectory(self, path):
        index = self.model.index(path)
        self.__ui.treeView_directory.scrollTo(index, QAbstractItemView.EnsureVisible)

    def setContextMenu(self, pos):
        contextMenu = QMenu(self)
        contextMenuLabels = [u"ブックマークへ追加", u"エクスプローラで開く"]
        actionList = []
        for label in contextMenuLabels:
            actionList.append(contextMenu.addAction(label))
        action = contextMenu.exec_(self.mapToGlobal(pos))
        for act in actionList:
            if act == action:
                if(act.text() == u"ブックマークへ追加"):
                    self.parent.addBookmark(self.getCurrentPath())
                if(act.text() == u"エクスプローラで開く"):
                    Utility.openExplorer(self.getCurrentPath())


class Ui_Widget_Directory(object):
    def setupUi(self, Widget_Directory):
        Widget_Directory.setObjectName("Widget_Directory")
        Widget_Directory.resize(252, 480)
        Widget_Directory.setMinimumSize(QSize(1, 1))
        self.gridLayout = QGridLayout(Widget_Directory)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.treeView_directory = QTreeView(Widget_Directory)
        self.treeView_directory.setMinimumSize(QSize(1, 1))
        self.treeView_directory.setObjectName("treeView_directory")
        self.gridLayout.addWidget(self.treeView_directory, 0, 0, 1, 1)

        self.retranslateUi(Widget_Directory)
        QMetaObject.connectSlotsByName(Widget_Directory)

    def retranslateUi(self, Widget_Directory):
        try:
            Widget_Directory.setWindowTitle(
                QApplication.translate("Widget_Directory", "Widget_Directory", None, QApplication.UnicodeUTF8))
        except:
            Widget_Directory.setWindowTitle(
                QApplication.translate("Widget_Directory", "Widget_Directory", None))


class Dialog_Option(QDialog):

    widgetName = "Dialog_Option"

    def __init__(self, parent=None):
        super(Dialog_Option, self).__init__(parent)
        self.parent = parent
        self.__ui = Ui_Dialog_Option()
        self.__ui.setupUi(self)
        self.setup()

    def setup(self):
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.__ui.buttonGroup_previewOption.setId(self.__ui.radioButton_withBoot, 0)
        self.__ui.buttonGroup_previewOption.setId(self.__ui.radioButton_withSelect, 1)
        self.__ui.buttonGroup_previewOption.setId(self.__ui.radioButton_disable, 2)

        self.readSettings()

    def closeEvent(self, event):
        self.writeSettings()

    def getPreviewOption(self):
        return self.__ui.buttonGroup_previewOption.checkedId()

    def getSelectOption(self):
        return self.__ui.checkBox_selectOption.checkState()

    def getExpandFolderWhenClickOption(self):
        return self.__ui.checkBox_expandFolderWhenClickOption.checkState()

    def getSelectOption_scriptNode(self):
        if self.__ui.checkBox_selectOption_scriptNode.checkState() == Qt.CheckState.Checked:
            return True
        else:
            return False

    def readSettings(self):
        settingFilePath = Utility.getSettingFilePath()
        self.settings = QSettings(settingFilePath, QSettings.IniFormat)
        self.settings.beginGroup(self.widgetName)

        selectOption = self.settings.value("selectOption")
        if selectOption is not None:
            if selectOption == "True":
                self.__ui.checkBox_selectOption.setCheckState(Qt.CheckState.Checked)
            else:
                self.__ui.checkBox_selectOption.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.__ui.checkBox_selectOption.setCheckState(Qt.CheckState.Checked)

            self.settings.setValue("previewOption", self.__ui.buttonGroup_previewOption.checkedId())

        selectOption_scriptNode = self.settings.value("selectOption_scriptNode")
        if selectOption_scriptNode is not None:
            if selectOption_scriptNode == "True":
                self.__ui.checkBox_selectOption_scriptNode.setCheckState(Qt.CheckState.Checked)
            else:
                self.__ui.checkBox_selectOption_scriptNode.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.__ui.checkBox_selectOption_scriptNode.setCheckState(Qt.CheckState.Checked)

        previewOption = self.settings.value("previewOption")
        if previewOption is not None:
            if int(previewOption) != -1:
                self.__ui.buttonGroup_previewOption.button(int(previewOption)).setChecked(True)
            else:
                self.__ui.buttonGroup_previewOption.button(0).setChecked(True)
        else:
            self.__ui.buttonGroup_previewOption.button(0).setChecked(True)

        hasReferenceOption = cmds.optionVar(exists=g_refecrenceOptionVar)
        if hasReferenceOption:
            referenceOption = cmds.optionVar(q=g_refecrenceOptionVar)
            if referenceOption:
                self.__ui.checkBox_referenceOption.setCheckState(Qt.CheckState.Checked)
            else:
                self.__ui.checkBox_referenceOption.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.__ui.checkBox_referenceOption.setCheckState(Qt.CheckState.Unchecked)

            cmds.optionVar(iv=(g_refecrenceOptionVar, 0))

        expandFolderWhenClickOption = self.settings.value("expandFolderWhenClickOption")
        if expandFolderWhenClickOption is not None:
            if expandFolderWhenClickOption == "True":
                self.__ui.checkBox_expandFolderWhenClickOption.setCheckState(Qt.CheckState.Checked)
            else:
                self.__ui.checkBox_expandFolderWhenClickOption.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.__ui.checkBox_expandFolderWhenClickOption.setCheckState(Qt.CheckState.Unchecked)

        self.settings.endGroup()

    def writeSettings(self):
        settingFilePath = Utility.getSettingFilePath()
        self.settings = QSettings(settingFilePath, QSettings.IniFormat)
        self.settings.beginGroup(self.widgetName)

        if self.__ui.checkBox_selectOption.checkState() == Qt.CheckState.Checked:
            self.settings.setValue("selectOption", "True")
        else:
            self.settings.setValue("selectOption", "False")

        if self.__ui.checkBox_selectOption_scriptNode.checkState() == Qt.CheckState.Checked:
            self.settings.setValue("selectOption_scriptNode", "True")
        else:
            self.settings.setValue("selectOption_scriptNode", "False")

        self.settings.setValue("previewOption", self.__ui.buttonGroup_previewOption.checkedId())

        if self.__ui.checkBox_referenceOption.checkState() == Qt.CheckState.Checked:
            cmds.optionVar(iv=(g_refecrenceOptionVar, 1))
        else:
            cmds.optionVar(iv=(g_refecrenceOptionVar, 0))

        if self.__ui.checkBox_expandFolderWhenClickOption.checkState() == Qt.CheckState.Checked:
            self.settings.setValue("expandFolderWhenClickOption", "True")
        else:
            self.settings.setValue("expandFolderWhenClickOption", "False")

        self.settings.endGroup()


class Ui_Dialog_Option(object):
    def setupUi(self, Dialog_Option):
        Dialog_Option.setObjectName("Dialog_Option")
        Dialog_Option.resize(318, 150)
        Dialog_Option.setSizeGripEnabled(False)
        Dialog_Option.setModal(True)
        self.gridLayout = QGridLayout(Dialog_Option)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_select = QLabel(Dialog_Option)
        self.label_select.setObjectName("label_select")
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_select)
        self.checkBox_selectOption = QCheckBox(Dialog_Option)
        self.checkBox_selectOption.setObjectName("checkBox_selectOption")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.checkBox_selectOption)
        self.checkBox_selectOption_scriptNode = QCheckBox(Dialog_Option)
        self.checkBox_selectOption_scriptNode.setObjectName("checkBox_selectOption_scriptNode")
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.checkBox_selectOption_scriptNode)
        self.line = QFrame(Dialog_Option)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.line)
        self.label_preview = QLabel(Dialog_Option)
        self.label_preview.setObjectName("label_preview")
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.label_preview)
        self.radioButton_withBoot = QRadioButton(Dialog_Option)
        self.radioButton_withBoot.setObjectName("radioButton_withBoot")
        self.buttonGroup_previewOption = QButtonGroup(Dialog_Option)
        self.buttonGroup_previewOption.setObjectName("buttonGroup_previewOption")
        self.buttonGroup_previewOption.addButton(self.radioButton_withBoot)
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.radioButton_withBoot)
        self.radioButton_withSelect = QRadioButton(Dialog_Option)
        self.radioButton_withSelect.setObjectName("radioButton_withSelect")
        self.buttonGroup_previewOption.addButton(self.radioButton_withSelect)
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.radioButton_withSelect)
        self.radioButton_disable = QRadioButton(Dialog_Option)
        self.radioButton_disable.setObjectName("radioButton_disable")
        self.buttonGroup_previewOption.addButton(self.radioButton_disable)
        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.radioButton_disable)
        self.line2 = QFrame(Dialog_Option)
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setObjectName("line2")
        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.line2)
        self.label_reference = QLabel(Dialog_Option)
        self.label_reference.setObjectName("label_reference")
        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.label_reference)
        self.checkBox_referenceOption = QCheckBox(Dialog_Option)
        self.checkBox_referenceOption.setObjectName("checkBox_referenceOption")
        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.checkBox_referenceOption)
        self.line3 = QFrame(Dialog_Option)
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Sunken)
        self.line3.setObjectName("line3")
        self.formLayout.setWidget(11, QFormLayout.FieldRole, self.line3)
        self.label_expandFolderWhenClickOption = QLabel(Dialog_Option)
        self.label_expandFolderWhenClickOption.setObjectName("label_expandFolderWhenClick")
        self.formLayout.setWidget(12, QFormLayout.FieldRole, self.label_expandFolderWhenClickOption)
        self.checkBox_expandFolderWhenClickOption = QCheckBox(Dialog_Option)
        self.checkBox_expandFolderWhenClickOption.setObjectName("checkBox_expandFolderWhenClick")
        self.formLayout.setWidget(13, QFormLayout.FieldRole, self.checkBox_expandFolderWhenClickOption)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog_Option)
        QMetaObject.connectSlotsByName(Dialog_Option)

    def retranslateUi(self, Dialog_Option):
        try:
            Dialog_Option.setWindowTitle(QApplication.translate("Dialog_Option", "オプション", None, QApplication.UnicodeUTF8))
            self.label_select.setText(QApplication.translate("Dialog_Option", "選択", None, QApplication.UnicodeUTF8))
            self.checkBox_selectOption.setText(QApplication.translate("Dialog_Option", "プロジェクトフォルダ選択時にscenesフォルダ内を表示", None, QApplication.UnicodeUTF8))
            self.checkBox_selectOption_scriptNode.setText(QApplication.translate("Dialog_Option", "スクリプトノードを実行してファイルを開く", None, QApplication.UnicodeUTF8))
            self.label_preview.setText(QApplication.translate("Dialog_Option", "プレビュー用画像自動レンダリング機能", None, QApplication.UnicodeUTF8))
            self.radioButton_withBoot.setText(QApplication.translate("Dialog_Option", "起動時に有効", None, QApplication.UnicodeUTF8))
            self.radioButton_withSelect.setText(QApplication.translate("Dialog_Option", "シーンファイル選択時に有効", None, QApplication.UnicodeUTF8))
            self.radioButton_disable.setText(QApplication.translate("Dialog_Option", "無効", None, QApplication.UnicodeUTF8))
            self.label_reference.setText(QApplication.translate("Dialog_Option", "リファレンス読み込み", None, QApplication.UnicodeUTF8))
            self.checkBox_referenceOption.setText(QApplication.translate("Dialog_Option", "ネームスペースを使用", None, QApplication.UnicodeUTF8))
            self.label_expandFolderWhenClickOption.setText(QApplication.translate("Dialog_Option", "フォルダ選択", None, QApplication.UnicodeUTF8))
            self.checkBox_expandFolderWhenClickOption.setText(QApplication.translate("Dialog_Option", "フォルダ選択時、下層を開く", None, QApplication.UnicodeUTF8))
        except:
            Dialog_Option.setWindowTitle(QApplication.translate("Dialog_Option", "オプション", None))
            self.label_select.setText(QApplication.translate("Dialog_Option", "選択", None))
            self.checkBox_selectOption.setText(QApplication.translate("Dialog_Option", "プロジェクトフォルダ選択時にscenesフォルダ内を表示", None))
            self.checkBox_selectOption_scriptNode.setText(QApplication.translate("Dialog_Option", "スクリプトノードを実行してファイルを開く", None))
            self.label_preview.setText(QApplication.translate("Dialog_Option", "プレビュー用画像自動レンダリング機能", None))
            self.radioButton_withBoot.setText(QApplication.translate("Dialog_Option", "起動時に有効", None))
            self.radioButton_withSelect.setText(QApplication.translate("Dialog_Option", "シーンファイル選択時に有効", None))
            self.radioButton_disable.setText(QApplication.translate("Dialog_Option", "無効", None))
            self.label_reference.setText(QApplication.translate("Dialog_Option", "リファレンス読み込み", None))
            self.checkBox_referenceOption.setText(QApplication.translate("Dialog_Option", "ネームスペースを使用", None))
            self.label_expandFolderWhenClickOption.setText(QApplication.translate("Dialog_Option", "フォルダ選択", None))
            self.checkBox_expandFolderWhenClickOption.setText(QApplication.translate("Dialog_Option", "フォルダ選択時、下層を開く", None))


class Widget_Bookmark(QWidget):

    def __init__(self, parent=None):
        super(Widget_Bookmark, self).__init__(parent)
        self.widgetName = "Widget_Bookmark"
        self.parent = parent
        self.__ui = Ui_Widget_Bookmark()
        self.__ui.setupUi(self)
        self.setup()

    def setup(self):
        self.initVariable()
        self.setSlot()
        self.loadBookmarkFile()
        self.setRightClickMenu()

    def initVariable(self):
        '''
        変数の初期化
        '''
        self.bookmarkDict = {}
        self.bookmarkFilePath = self.getBookmarkFilePath()

    def setSlot(self):
        '''
        スロットの登録
        '''
        self.parent.addBookmarkSignal.connect(self.addBookmark)

        self.__ui.pushButton_up.clicked.connect(self.upBookmark)
        self.__ui.pushButton_down.clicked.connect(self.downBookmark)
        self.__ui.pushButton_add.clicked.connect(self.addBookmark)
        self.__ui.pushButton_remove.clicked.connect(self.removeBookmark)
        self.__ui.pushButton_clear.clicked.connect(self.clearBookmark)

        self.__ui.listWidget_bookmark.doubleClicked[QModelIndex].connect(self.syncCurrentPath)

    def upBookmark(self):
        '''
        選択しているブックマークを上に移動
        '''
        row = self.__ui.listWidget_bookmark.currentRow()
        if row > 0:
            self.__ui.listWidget_bookmark.insertItem(row-1, self.__ui.listWidget_bookmark.currentItem().text())
            self.__ui.listWidget_bookmark.takeItem(row+1)
            self.__ui.listWidget_bookmark.setCurrentRow(row-1)
            self.saveBookmarkFile()

    def downBookmark(self):
        '''
        選択しているブックマークを下に移動
        '''
        row = self.__ui.listWidget_bookmark.currentRow()
        if row < self.__ui.listWidget_bookmark.count()-1:
            self.__ui.listWidget_bookmark.insertItem(row, self.__ui.listWidget_bookmark.item(row+1).text())
            self.__ui.listWidget_bookmark.takeItem(row+2)
            self.__ui.listWidget_bookmark.setCurrentRow(row+1)
            self.saveBookmarkFile()

    def addBookmark(self, path=None):
        '''
        ブックマークを追加する
        '''
        if not path:
            path = self.parent.currentPath

        if os.path.isdir(path):
            if path not in self.bookmarkDict:
                self.bookmarkDict[path] = len(self.bookmarkDict)
                self.__ui.listWidget_bookmark.clear()
                for k, v in sorted(list(self.bookmarkDict.items()), key=lambda x: x[1]):
                    self.__ui.listWidget_bookmark.addItems([k])

                self.saveBookmarkFile()
                QMessageBox.information(
                    self, u"ブックマーク", path + u" \nをブックマークしました。")
            else:
                QMessageBox.warning(
                    self, u"警告", path + u" \nは既にブックマークされています。")
        else:
            QMessageBox.warning(
                self, u"警告", u"ブックマークできるのはディレクトリのみです。\nディレクトリを指定してください。")

    def removeBookmark(self):
        '''
        選択しているブックマークを削除する
        '''
        item = self.__ui.listWidget_bookmark.currentItem()
        if item:
            path = item.text()
            if path in self.bookmarkDict:
                self.bookmarkDict.pop(path)
                self.__ui.listWidget_bookmark.takeItem(self.__ui.listWidget_bookmark.row(item))
                self.saveBookmarkFile()

    def clearBookmark(self):
        '''
        ブックマークをすべて削除する
        '''
        reply = QMessageBox.question(self, u"ブックマークのクリア", u" ブックマークをすべて削除します。\nよろしいですか？",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.__ui.listWidget_bookmark.clear()
            self.bookmarkDict.clear()
            self.saveBookmarkFile()

    def syncCurrentPath(self):
        '''
        ブックマークのパスを他のウィジェットに反映する
        '''
        path = self.getCurrentPath()
        self.parent.syncCurrentPath(path)

    def getCurrentPath(self):
        '''
        選択しているブックマークのパスを返す
        '''
        item = self.__ui.listWidget_bookmark.currentItem()
        path = item.text()
        return path

    def loadBookmarkFile(self):
        '''
        ブックマークファイルを読み込む
        '''
        if os.path.exists(self.bookmarkFilePath):
            for i, path in enumerate(codecs.open(self.bookmarkFilePath, 'r', encoding='utf-8')):
                dirPath = path.rstrip('\n')
                self.bookmarkDict[dirPath] = i
                self.__ui.listWidget_bookmark.addItems([dirPath])

    def saveBookmarkFile(self):
        '''
        ブックマークファイルを保存する
        '''
        file = codecs.open(self.bookmarkFilePath, 'w', encoding='utf-8')
        for i in range(self.__ui.listWidget_bookmark.count()):
            item = self.__ui.listWidget_bookmark.item(i)
            file.write(u"{0}\n".format(item.text()))

    def getBookmarkFilePath(self):
        '''
        ブックマークファイルを保存する場所を取得する
        '''
        toolDir = cmds.internalVar(userAppDir=True) + \
            "TKG/" + g_toolName + "/"
        bookmarkFilePath = toolDir + g_toolName + '_bookmark.txt'
        return bookmarkFilePath

    def setRightClickMenu(self):
        '''
        右クリックメニューの登録
        '''
        self.__ui.listWidget_bookmark.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__ui.listWidget_bookmark.customContextMenuRequested.connect(self.setContextMenu)

    def setContextMenu(self, pos):
        '''
        右クリックメニューの設定
        '''
        contextMenu = QMenu(self)
        contextMenuLabels = [u"ブックマークから削除", u"エクスプローラで開く"]
        actionList = []
        for label in contextMenuLabels:
            actionList.append(contextMenu.addAction(label))
        action = contextMenu.exec_(self.mapToGlobal(pos))
        for act in actionList:
            if act == action:
                if(act.text() == u"ブックマークから削除"):
                    self.removeBookmark()
                if(act.text() == u"エクスプローラで開く"):
                    Utility.openExplorer(self.getCurrentPath())


class Ui_Widget_Bookmark(object):
    def setupUi(self, Widget_Bookmark):
        Widget_Bookmark.setObjectName("Widget_Bookmark")
        Widget_Bookmark.resize(169, 475)
        Widget_Bookmark.setMinimumSize(QSize(1, 1))
        self.gridLayout = QGridLayout(Widget_Bookmark)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget_bookmark = QListWidget(Widget_Bookmark)
        self.listWidget_bookmark.setMinimumSize(QSize(1, 1))
        self.listWidget_bookmark.setObjectName("listWidget_bookmark")
        self.gridLayout.addWidget(self.listWidget_bookmark, 0, 0, 1, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_up = QPushButton(Widget_Bookmark)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_up.sizePolicy().hasHeightForWidth())
        self.pushButton_up.setSizePolicy(sizePolicy)
        self.pushButton_up.setMinimumSize(QSize(25, 25))
        self.pushButton_up.setMaximumSize(QSize(25, 16777215))
        self.pushButton_up.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/up.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_up.setIcon(icon)
        self.pushButton_up.setObjectName("pushButton_up")
        self.horizontalLayout.addWidget(self.pushButton_up)
        self.pushButton_down = QPushButton(Widget_Bookmark)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_down.sizePolicy().hasHeightForWidth())
        self.pushButton_down.setSizePolicy(sizePolicy)
        self.pushButton_down.setMinimumSize(QSize(25, 25))
        self.pushButton_down.setMaximumSize(QSize(25, 16777215))
        self.pushButton_down.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/down.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_down.setIcon(icon1)
        self.pushButton_down.setObjectName("pushButton_down")
        self.horizontalLayout.addWidget(self.pushButton_down)
        self.pushButton_add = QPushButton(Widget_Bookmark)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_add.sizePolicy().hasHeightForWidth())
        self.pushButton_add.setSizePolicy(sizePolicy)
        self.pushButton_add.setMinimumSize(QSize(25, 25))
        self.pushButton_add.setMaximumSize(QSize(25, 16777215))
        self.pushButton_add.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/add.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_add.setIcon(icon2)
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)
        self.pushButton_remove = QPushButton(Widget_Bookmark)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_remove.sizePolicy().hasHeightForWidth())
        self.pushButton_remove.setSizePolicy(sizePolicy)
        self.pushButton_remove.setMinimumSize(QSize(25, 25))
        self.pushButton_remove.setMaximumSize(QSize(25, 16777215))
        self.pushButton_remove.setText("")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(":/remove.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_remove.setIcon(icon3)
        self.pushButton_remove.setObjectName("pushButton_remove")
        self.horizontalLayout.addWidget(self.pushButton_remove)
        self.pushButton_clear = QPushButton(Widget_Bookmark)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_clear.sizePolicy().hasHeightForWidth())
        self.pushButton_clear.setSizePolicy(sizePolicy)
        self.pushButton_clear.setMinimumSize(QSize(25, 25))
        self.pushButton_clear.setMaximumSize(QSize(25, 16777215))
        self.pushButton_clear.setText("")
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(":/clear.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_clear.setIcon(icon4)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.horizontalLayout.addWidget(self.pushButton_clear)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Widget_Bookmark)
        QMetaObject.connectSlotsByName(Widget_Bookmark)

    def retranslateUi(self, Widget_Bookmark):

        try:
            Widget_Bookmark.setWindowTitle(QApplication.translate("Widget_Bookmark", "Widget_Bookmark", None, QApplication.UnicodeUTF8))
            self.pushButton_up.setToolTip(QApplication.translate("Widget_Bookmark", "選択しているブックマークを上に移動", None, QApplication.UnicodeUTF8))
            self.pushButton_down.setToolTip(QApplication.translate("Widget_Bookmark", "選択しているブックマークを下に移動", None, QApplication.UnicodeUTF8))
            self.pushButton_add.setToolTip(QApplication.translate("Widget_Bookmark", "現在のディレクトリをブックマークに追加", None, QApplication.UnicodeUTF8))
            self.pushButton_remove.setToolTip(QApplication.translate("Widget_Bookmark", "選択しているブックマークを削除", None, QApplication.UnicodeUTF8))
            self.pushButton_clear.setToolTip(QApplication.translate("Widget_Bookmark", "ブックマークをすべて削除", None, QApplication.UnicodeUTF8))
        except:
            Widget_Bookmark.setWindowTitle(QApplication.translate("Widget_Bookmark", "Widget_Bookmark", None))
            self.pushButton_up.setToolTip(QApplication.translate("Widget_Bookmark", "選択しているブックマークを上に移動", None))
            self.pushButton_down.setToolTip(QApplication.translate("Widget_Bookmark", "選択しているブックマークを下に移動", None))
            self.pushButton_add.setToolTip(QApplication.translate("Widget_Bookmark", "現在のディレクトリをブックマークに追加", None))
            self.pushButton_remove.setToolTip(QApplication.translate("Widget_Bookmark", "選択しているブックマークを削除", None))
            self.pushButton_clear.setToolTip(QApplication.translate("Widget_Bookmark", "ブックマークをすべて削除", None))



class Widget_RecentFile(QWidget):

    def __init__(self, parent=None):
        super(Widget_RecentFile, self).__init__(parent)
        self.widgetName = "Widget_RecentFile"
        self.parent = parent
        self.__ui = Ui_Widget_RecentFile()
        self.__ui.setupUi(self)
        self.setup()

    def setup(self):
        self.setSlot()
        self.setRightClickMenu()
        self.updateRecentFileList()

    def setSlot(self):
        '''
        スロットの登録
        '''
        self.__ui.listWidget_recentFile.clicked[QModelIndex].connect(self.syncCurrentPath)
        self.__ui.listWidget_recentFile.doubleClicked[QModelIndex].connect(self.doubleClickEvent)

        self.__ui.pushButton_update.clicked.connect(self.updateRecentFileList)


    def updateRecentFileList(self):
        '''
        リストのアップデート
        '''
        recentFiles  = pm.optionVar(q='RecentFilesList')

        self.__ui.listWidget_recentFile.clear()

        if isinstance(recentFiles, int) == False:
            for recentFile in reversed(recentFiles):
              self.__ui.listWidget_recentFile.addItem(recentFile)


    def syncCurrentPath(self):
        '''
        アイテムのパスを他のウィジェットに反映する
        '''
        path = self.getCurrentPath()
        self.parent.setPreviewPath(path)
        self.parent.syncCurrentPath(path)

    def doubleClickEvent(self):
        '''
        シーンを開く
        '''
        path = self.getCurrentPath()
        if(os.path.isfile(path)):
            if(MayaUtility.isSceneFile(path)):
                MayaUtility.openSceneFile(path, self.parent.getSelectOption_scriptNode())
            else:
                Utility.openFile(path)

    def getCurrentPath(self):
        '''
        選択しているアイテムのパスを返す
        '''
        item = self.__ui.listWidget_recentFile.currentItem()
        path = item.text()
        return path


    def setRightClickMenu(self):
        '''
        右クリックメニューの登録
        '''
        self.__ui.listWidget_recentFile.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__ui.listWidget_recentFile.customContextMenuRequested.connect(self.setContextMenu)

    def setContextMenu(self, pos):
        '''
        右クリックメニューの設定
        '''
        contextMenu = QMenu(self)
        contextMenuLabels = [u"エクスプローラで開く"]
        actionList = []
        for label in contextMenuLabels:
            actionList.append(contextMenu.addAction(label))
        action = contextMenu.exec_(self.mapToGlobal(pos))
        for act in actionList:
            if act == action:
                if(act.text() == u"エクスプローラで開く"):
                    Utility.openExplorer(self.getCurrentPath())


class Ui_Widget_RecentFile(object):
    def setupUi(self, Widget_RecentFile):
        Widget_RecentFile.setObjectName("Widget_RecentFile")
        Widget_RecentFile.resize(169, 475)
        Widget_RecentFile.setMinimumSize(QSize(1, 1))
        self.gridLayout = QGridLayout(Widget_RecentFile)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget_recentFile = QListWidget(Widget_RecentFile)
        self.listWidget_recentFile.setMinimumSize(QSize(1, 1))
        self.listWidget_recentFile.setObjectName("listWidget_recentFile")
        self.gridLayout.addWidget(self.listWidget_recentFile, 0, 0, 1, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_update = QPushButton(Widget_RecentFile)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_update.sizePolicy().hasHeightForWidth())
        self.pushButton_update.setSizePolicy(sizePolicy)
        self.pushButton_update.setMinimumSize(QSize(50, 25))
        self.pushButton_update.setMaximumSize(QSize(50, 16777215))
        self.pushButton_update.setObjectName("pushButton_update")
        self.horizontalLayout.addWidget(self.pushButton_update)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Widget_RecentFile)
        QMetaObject.connectSlotsByName(Widget_RecentFile)

    def retranslateUi(self, Widget_RecentFile):
        try:
            Widget_RecentFile.setWindowTitle(QApplication.translate("Widget_RecentFile", "Widget_RecentFile", None, QApplication.UnicodeUTF8))
            self.pushButton_update.setToolTip(QApplication.translate("Widget_RecentFile", "ブックマークをすべて削除", None, QApplication.UnicodeUTF8))
            self.pushButton_update.setText(QApplication.translate("Widget_RecentFile", "更新", None, QApplication.UnicodeUTF8))
        except:
            Widget_RecentFile.setWindowTitle(QApplication.translate("Widget_RecentFile", "Widget_RecentFile", None))
            self.pushButton_update.setToolTip(QApplication.translate("Widget_RecentFile", "ブックマークをすべて削除", None))
            self.pushButton_update.setText(QApplication.translate("Widget_RecentFile", "更新", None))


class Widget_HistoryButtons(QWidget):

    def __init__(self, parent=None):
        super(Widget_HistoryButtons, self).__init__(parent)
        self.parent = parent
        self.__ui = Ui_Widget_HistoryButtons()
        self.__ui.setupUi(self)
        self.setup()

    def setup(self):
        self.currentPath = ""
        self.backPath = []
        self.forwardPath = []

        self.__ui.pushButton_back.clicked.connect(self.back)
        self.__ui.pushButton_forward.clicked.connect(self.forward)
        self.__ui.pushButton_toParent.clicked.connect(self.toParent)

        self.disableButton(self.__ui.pushButton_back)
        self.disableButton(self.__ui.pushButton_forward)

        self.parent.syncCurrentPathSignal.connect(self.storeHistory)

    def back(self):
        if self.backPath:
            self.forwardPath.append(self.backPath.pop())
            self.enableButton(self.__ui.pushButton_forward)
            self.setCurrentPath(self.backPath[-1])
            if len(self.backPath) <= 1:
                self.disableButton(self.__ui.pushButton_back)

    def forward(self):
        self.backPath.append(self.forwardPath.pop())
        self.enableButton(self.__ui.pushButton_back)
        self.setCurrentPath(self.backPath[-1])
        if len(self.forwardPath) <= 0:
            self.disableButton(self.__ui.pushButton_forward)

    def toParent(self):
        if os.path.dirname(self.currentPath):
            dirPath = os.path.dirname(self.currentPath)
            self.setCurrentPath(dirPath)
            self.storeHistory(dirPath)

    def enableButton(self, button):
        button.setEnabled(True)

    def disableButton(self, button):
        button.setEnabled(False)

    def storeHistory(self, path):
        if path != self.currentPath:
            self.backPath.append(path)
            self.currentPath = self.backPath[-1]
            if len(self.backPath) > 1:
                self.enableButton(self.__ui.pushButton_back)
            del self.forwardPath[:]
            self.disableButton(self.__ui.pushButton_forward)

        if path == Utility.getRootPath():
            self.disableButton(self.__ui.pushButton_toParent)
        else:
            self.enableButton(self.__ui.pushButton_toParent)

    def setCurrentPath(self, path):
        self.currentPath = self.backPath[-1]
        self.parent.syncCurrentPath(path)


class Ui_Widget_HistoryButtons(object):
    def setupUi(self, Widget_HistoryButtons):
        Widget_HistoryButtons.setObjectName("Widget_HistoryButtons")
        Widget_HistoryButtons.resize(94, 31)
        Widget_HistoryButtons.setMinimumSize(QSize(1, 1))
        Widget_HistoryButtons.setMaximumSize(QSize(114, 42))
        self.horizontalLayout = QHBoxLayout(Widget_HistoryButtons)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_back = QPushButton(Widget_HistoryButtons)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_back.sizePolicy().hasHeightForWidth())
        self.pushButton_back.setSizePolicy(sizePolicy)
        self.pushButton_back.setMinimumSize(QSize(1, 1))
        self.pushButton_back.setMaximumSize(QSize(25, 25))
        self.pushButton_back.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/back.png"), QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap(":/back_disable.png"), QIcon.Disabled, QIcon.Off)
        self.pushButton_back.setIcon(icon)
        self.pushButton_back.setObjectName("pushButton_back")
        self.horizontalLayout_2.addWidget(self.pushButton_back)
        self.pushButton_forward = QPushButton(Widget_HistoryButtons)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_forward.sizePolicy().hasHeightForWidth())
        self.pushButton_forward.setSizePolicy(sizePolicy)
        self.pushButton_forward.setMinimumSize(QSize(1, 1))
        self.pushButton_forward.setMaximumSize(QSize(25, 25))
        self.pushButton_forward.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/forward.png"), QIcon.Normal, QIcon.Off)
        icon1.addPixmap(QPixmap(":/forward_disable.png"), QIcon.Disabled, QIcon.Off)
        icon1.addPixmap(QPixmap(":/forward_disable.png"), QIcon.Disabled, QIcon.On)
        self.pushButton_forward.setIcon(icon1)
        self.pushButton_forward.setObjectName("pushButton_forward")
        self.horizontalLayout_2.addWidget(self.pushButton_forward)
        self.pushButton_toParent = QPushButton(Widget_HistoryButtons)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_toParent.sizePolicy().hasHeightForWidth())
        self.pushButton_toParent.setSizePolicy(sizePolicy)
        self.pushButton_toParent.setMinimumSize(QSize(1, 1))
        self.pushButton_toParent.setMaximumSize(QSize(25, 25))
        self.pushButton_toParent.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/toParent.png"), QIcon.Normal, QIcon.Off)
        icon2.addPixmap(QPixmap(":/toParent_disable.png"), QIcon.Disabled, QIcon.Off)
        icon2.addPixmap(QPixmap(":/toParent_disable.png"), QIcon.Disabled, QIcon.On)
        self.pushButton_toParent.setIcon(icon2)
        self.pushButton_toParent.setObjectName("pushButton_toParent")
        self.horizontalLayout_2.addWidget(self.pushButton_toParent)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Widget_HistoryButtons)
        QMetaObject.connectSlotsByName(Widget_HistoryButtons)

    def retranslateUi(self, Widget_HistoryButtons):
        try:
            Widget_HistoryButtons.setWindowTitle(QApplication.translate("Widget_HistoryButtons", "Widget_HistoryButtons", None, QApplication.UnicodeUTF8))
            self.pushButton_back.setToolTip(QApplication.translate("Widget_HistoryButtons", "戻る", None, QApplication.UnicodeUTF8))
            self.pushButton_forward.setToolTip(QApplication.translate("Widget_HistoryButtons", "進む", None, QApplication.UnicodeUTF8))
            self.pushButton_toParent.setToolTip(QApplication.translate("Widget_HistoryButtons", "上の階層へ移動", None, QApplication.UnicodeUTF8))
        except:
            Widget_HistoryButtons.setWindowTitle(QApplication.translate("Widget_HistoryButtons", "Widget_HistoryButtons", None))
            self.pushButton_back.setToolTip(QApplication.translate("Widget_HistoryButtons", "戻る", None))
            self.pushButton_forward.setToolTip(QApplication.translate("Widget_HistoryButtons", "進む", None))
            self.pushButton_toParent.setToolTip(QApplication.translate("Widget_HistoryButtons", "上の階層へ移動", None))


class LineEdit_Path(QLineEdit):

    def __init__(self, parent=None):
        super(LineEdit_Path, self).__init__(parent)
        self.parent = parent
        self.setup()

    def setup(self):
        self.returnPressed.connect(self.putText)
        self.parent.syncCurrentPathSignal.connect(self.setCurrentPath)

    def getCurrentPath(self):
        return self.currentPath

    def setCurrentPath(self, path):
        self.currentPath = path
        if os.path.isdir(path):
            self.setText(path)
        else:
            self.setText(os.path.dirname(path))

    def putText(self):
        path = Utility.normalizePath(self.text())
        if os.path.exists(path):
            self.setCurrentPath(path)
            self.parent.syncCurrentPath(path)


class Widget_File(QWidget):

    def __init__(self, parent=None):
        super(Widget_File, self).__init__(parent)
        self.widgetName = "Widget_File"
        self.parent = parent
        self.__ui = Ui_Widget_File()
        self.__ui.setupUi(self)
        self.setup()
        self.readSettings()

    def setup(self):
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.__ui.treeView_file.setModel(self.model)
        self.__ui.treeView_file.setRootIndex(QModelIndex())
        self.installEventFilter(self)
        self.setSlot()

    def setSlot(self):
        self.__ui.treeView_file.clicked[QModelIndex].connect(self.clickEvent)
        self.__ui.treeView_file.doubleClicked[QModelIndex].connect(self.doubleClickEvent)
        self.__ui.treeView_file.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__ui.treeView_file.customContextMenuRequested.connect(self.setContextMenu)
        self.parent.syncCurrentPathSignal.connect(self.setCurrentPath)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Hide:
            self.writeSettings()
            return True
        return False

    def clickEvent(self):
        path = self.getCurrentPath()
        self.parent.setPreviewPath(path)

    def doubleClickEvent(self):
        path = self.getCurrentPath()
        if(os.path.isfile(path)):
            if(MayaUtility.isSceneFile(path)):
                MayaUtility.openSceneFile(path, self.parent.getSelectOption_scriptNode())
            else:
                Utility.openFile(path)
        else:
            self.parent.syncCurrentPath(path)

    def getCurrentPath(self):
        index = self.__ui.treeView_file.currentIndex()
        path = self.model.filePath(index)
        return path

    def setCurrentPath(self, path):
        subPathList = path.split("/")
        for i in range(len(subPathList)):
            subPath = "/".join(subPathList[:i + 1])
            index = self.model.index(subPath)
            self.__ui.treeView_file.setRootIndex(index)

        index = self.model.index(path)
        if os.path.isdir(path):
            self.__ui.treeView_file.setRootIndex(index)
        else:
            self.__ui.treeView_file.setRootIndex(index.parent())
        self.__ui.treeView_file.setCurrentIndex(index)

        if self.getSelectOption() == Qt.CheckState.Checked:
            targetDir = "/scenes"
            if os.path.exists(path + targetDir):
                self.__ui.treeView_file.setRootIndex(self.model.index(path + targetDir))

    def getSelectOption(self):
        return self.parent.getSelectOption()

    def setContextMenu(self, pos):
        contextMenu = QMenu(self)
        contextMenuLabels = [u"ブックマークへ追加", u"エクスプローラで開く"]
        actionList = []
        for label in contextMenuLabels:
            actionList.append(contextMenu.addAction(label))
        action = contextMenu.exec_(self.mapToGlobal(pos))
        for act in actionList:
            if act == action:
                if(act.text() == u"ブックマークへ追加"):
                    self.parent.addBookmark(self.getCurrentPath())
                if(act.text() == u"エクスプローラで開く"):
                    Utility.openExplorer(self.getCurrentPath())

    def writeSettings(self):
        settingFilePath = Utility.getSettingFilePath()
        self.settings = QSettings(settingFilePath, QSettings.IniFormat)
        self.settings.beginGroup(self.widgetName)

        self.settings.setValue("headerState", self.__ui.treeView_file.header().saveState())

        self.settings.endGroup()

    def readSettings(self):
        settingFilePath = Utility.getSettingFilePath()
        self.settings = QSettings(settingFilePath, QSettings.IniFormat)
        self.settings.beginGroup(self.widgetName)

        headerState = self.settings.value("headerState")
        if headerState is not None:
            self.__ui.treeView_file.header().restoreState(headerState)

        self.settings.endGroup()
        self.__ui.treeView_file.hideColumn(2)


class Ui_Widget_File(object):
    def setupUi(self, Widget_File):
        Widget_File.setObjectName("Widget_File")
        Widget_File.resize(503, 387)
        Widget_File.setMinimumSize(QSize(0, 0))
        self.gridLayout = QGridLayout(Widget_File)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.treeView_file = QTreeView(Widget_File)
        self.treeView_file.setMinimumSize(QSize(1, 1))
        self.treeView_file.setRootIsDecorated(False)
        self.treeView_file.setItemsExpandable(False)
        self.treeView_file.setSortingEnabled(True)
        self.treeView_file.setObjectName("treeView_file")
        self.gridLayout.addWidget(self.treeView_file, 0, 0, 1, 1)

        self.retranslateUi(Widget_File)
        QMetaObject.connectSlotsByName(Widget_File)

    def retranslateUi(self, Widget_File):
        try:
            Widget_File.setWindowTitle(QApplication.translate("Widget_File", "Widget_File", None, QApplication.UnicodeUTF8))
        except:
            Widget_File.setWindowTitle(QApplication.translate("Widget_File", "Widget_File", None))


class Widget_Preview(QWidget):

    def __init__(self, parent=None):
        super(Widget_Preview, self).__init__(parent)
        self.widgetName = "Widget_Preview"
        self.__ui = Ui_Widget_Preview()
        self.__ui.setupUi(self)
        self.parent = parent
        self.setup()


    def bootStandaloneMaya(self):
        initializes = True if self.getPreviewOption() == 0 else False
        self.standaloneMaya = StandaloneMaya(initializes)
        self.standaloneMaya.start()

    def setup(self):
        self.initialized = True
        self.imagePath = ""
        self.threadRenderList = []

        self.bootStandaloneMaya()
        self.installEventFilter(self)

        self.parent.setPreviewPathSignal.connect(self.setImagePath)

    def eventFilter(self, widget, event):
        if event.type() == QEvent.Type.Resize:
            self.displayImage(self.imagePath)
            return True
        if event.type() == QEvent.Type.Hide:
            self.standaloneMaya.kill()
            return True
        return False

    def renderFinishedEvent(self, imagePath):
        if self.imagePath == imagePath:
            self.setImagePath(self.imagePath)

    def setImagePath(self, path):
        #if not self.initialized:
        #    self.mayaInit()
        #    self.initialized = True

        self.__ui.graphicsView_preview.setScene(None)

        if(self.isSceneFile(path)):
            self.imagePath = self.getImagePathforSceneFile(path)
            if os.path.exists(self.imagePath):
                if (Utility.diffUpdateTime(path, self.imagePath) > datetime.timedelta(seconds=-1)):
                    if self.getPreviewOption() != 2:
                        self.threadImageRendring(path)
                    else:
                        self.displayImage(self.imagePath)
                else:
                    self.displayImage(self.imagePath)
            else:
                if self.getPreviewOption() != 2:
                    self.threadImageRendring(path)
                else:
                    self.displayImage(self.imagePath)
        else:
            self.imagePath = path
            self.displayImage(self.imagePath)

    def mayaInit(self):
        try:
            cmd = CMD('""')
            StandaloneRPC.send_command(cmd)
        except:
            print("[URLError]")
            StandaloneRPC.send_command(cmd)

    def threadImageRendring(self, path):
        self.threadRenderList.append(ThreadRender(path, self.imagePath))
        self.threadRenderList[-1].renderFinished.connect(
            self.renderFinishedEvent)
        self.threadRenderList[-1].start()

    def displayImage(self, imagePath):
        imageReader = QImageReader(imagePath)
        if imageReader.canRead():
            imageWidth = imageReader.size().width()
            imageHeight = imageReader.size().height()
            imageAspect = float(imageWidth) / imageHeight

            margin = 3
            windowWidth = self.width() - margin * 2
            windowHeight = self.height() - margin * 2
            windowAspect = float(windowWidth) / windowHeight

            if(imageAspect > windowAspect):
                width = windowWidth
                if sys.version_info.major == 2:
                    height = width / imageAspect
                else:
                    height = old_div(width, imageAspect)
            else:
                height = windowHeight
                width = height * imageAspect

            imageReader.setScaledSize(QSize(width, height))
            self.thumbnail = imageReader.read()

            item = QGraphicsPixmapItem(
                QPixmap.fromImage(self.thumbnail))
            self.scene = QGraphicsScene(self)
            self.scene.addItem(item)
            self.__ui.graphicsView_preview.setScene(self.scene)

            imageReader = None
        else:
            self.__ui.graphicsView_preview.setScene(None)

    def isSceneFile(self, path):
        types = {".ma": "mayaAscii", ".mb": "mayaBinary",
                 ".fbx": "FBX", ".obj": "OBJ"}
        fileName = os.path.basename(path)
        name, ext = os.path.splitext(fileName)
        if ext in list(types.keys()):
            return True
        else:
            return False

    def getImagePathforSceneFile(self, path):
        fileName = os.path.basename(path)
        name, ext = os.path.splitext(fileName)

        dirPath = cmds.internalVar(userAppDir=True) + "temp/"

        if ext == ".mb" or ext == ".ma":
            imagePath = dirPath + name + ".jpg"
        else:
            imagePath = dirPath + name + ext + ".jpg"

        return imagePath

    def getPreviewOption(self):
        return self.parent.getPreviewOption()


class Ui_Widget_Preview(object):
    def setupUi(self, Widget_Preview):
        Widget_Preview.setObjectName("Widget_Preview")
        Widget_Preview.resize(273, 480)
        self.gridLayout = QGridLayout(Widget_Preview)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView_preview = QGraphicsView(Widget_Preview)
        self.graphicsView_preview.setMinimumSize(QSize(1, 1))
        self.graphicsView_preview.setObjectName("graphicsView_preview")
        self.gridLayout.addWidget(self.graphicsView_preview, 0, 0, 1, 1)

        self.retranslateUi(Widget_Preview)
        QMetaObject.connectSlotsByName(Widget_Preview)

    def retranslateUi(self, Widget_Preview):
        try:
            Widget_Preview.setWindowTitle(QApplication.translate(
                "Widget_Preview", "Widget_Preview", None, QApplication.UnicodeUTF8))
        except:
            Widget_Preview.setWindowTitle(
                QApplication.translate("Widget_Preview", "Widget_Preview", None))


class ThreadRender(QThread):
    renderFinished = Signal(str)

    def __init__(self, scenePath, imagePath, parent=None):
        super(ThreadRender, self).__init__()
        self.scenePath = scenePath
        self.imagePath = imagePath

    def run(self):
        try:
            cmd = CMD(
                'RenderSettings.main(\"' + self.scenePath + '\")')
            StandaloneRPC.send_command(cmd)

            for i in range(50):
                time.sleep(0.1)
                if os.path.exists(self.imagePath):
                    self.renderFinished.emit(self.imagePath)
                    break
        except:
            print("No connection...")


class StandaloneMaya(threading.Thread):

    def __init__(self, initializes):
        super(StandaloneMaya, self).__init__()
        self.initializes = initializes
        self.process = None

    def run(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        standalone_rpc_path =  u'{0}/{1}'.format(os.path.dirname(os.path.abspath(__file__)), u'StandaloneRPC.py')
        api = str(cmds.about(api=True))
        if api.find("20135") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2013.5/bin/mayapy.exe'
        elif api.find("2013") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2013/bin/mayapy.exe'
        if api.find("2014") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2014/bin/mayapy.exe'
        if api.find("2015") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2015/bin/mayapy.exe'
        if api.find("2016") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2016/bin/mayapy.exe'
        if api.find("2017") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2017/bin/mayapy.exe'
        if api.find("2018") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2018/bin/mayapy.exe'
        if api.find("2019") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2019/bin/mayapy.exe'
        if api.find("2020") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2020/bin/mayapy.exe'
        if api.find("2022") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2022/bin/mayapy.exe'
        if api.find("2023") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2023/bin/mayapy.exe'
        if api.find("2024") > -1:
            mayapy_path = u'C:/Program Files\Autodesk/Maya2024/bin/mayapy.exe'

        self.process = subprocess.Popen(u'\"{0}\" {1}'.format(mayapy_path, standalone_rpc_path), startupinfo=startupinfo)

        from time import sleep

        # wait mayapy
        sleep(2)
        if self.initializes:
            self.mayaInit()
            self.initializes = False

    def mayaInit(self):
        try:
            cmd = CMD('RenderSettings.init()')
            StandaloneRPC.send_command(cmd)
        except:
            print("[URLError]")


    def kill(self):
        if self.process:
            self.process.kill()


class CMD(str):

    def __new__(cls, cmd, *args, **kwargs):
        result = {'command': str(cmd)}
        if args:
            result['args'] = json.dumps(args)
        if kwargs:
            result['kwargs'] = json.dumps(kwargs)
        return urlencode(result)


class StandaloneRPC(object):

    @staticmethod
    def send_command(cmd, address='127.0.0.1', port=8000):
        url = "http://{address}:{port}/?{cmd}".format(
            address=address, port=port, cmd=cmd)

        q = urlopen(url)
        raw = q.read()
        try:
            results = json.loads(raw)
            return results
        except:
            raise ValueError("Could not parse server responss", raw)

class Utility(object):

    @staticmethod
    def getSettingFilePath():
        '''
        設定ファイルを保存する場所を取得する
        '''
        tool_dir = cmds.internalVar(userAppDir=True) + \
            "TKG/" + g_toolName + "/"
        settingFilePath = tool_dir + g_toolName + g_toolVersion + '.ini'
        return settingFilePath

    @staticmethod
    def getBookmarkFilePath():
        '''
        設定ファイルを保存する場所を取得する
        '''
        tool_dir = cmds.internalVar(userAppDir=True) + \
            "TKG/" + g_toolName + "/"
        bookmarkFilePath = tool_dir + g_toolName + '_bookmark.txt'
        return bookmarkFilePath

    @staticmethod
    def getRootPath():
        '''
        ルートパスを取得する
        '''
        rootPath = "C:/"
        return rootPath

    @staticmethod
    def openFile(path):
        '''
        指定したパス(path)を実行する
        '''
        os.popen(('start ' + '\"Hoge\" ' + '\"' + path + '\"').encode('shift-jis'))

    @staticmethod
    def openExplorer(path):
        '''
        指定されたパス(path)をエクスプローラで開く
        '''
        os.popen((u'explorer /select,"%s"' %
                  os.path.normpath(path)).encode('shift-jis'))

    @staticmethod
    def normalizePath(path):
        '''
        指定されたパス(path)の「\」を「/」に変換する
        '''
        return os.path.normpath(path).replace('\\', '/').strip()

    @staticmethod
    def getElapsedTime(file_path):
        '''
        ファイル(file_path)の最終更新日時からの経過時間を取得する
        '''
        stat = os.stat(file_path)
        last_update_time = datetime.datetime.fromtimestamp(stat.st_mtime)
        current_time = datetime.datetime.now()
        elapsed_time = current_time - last_update_time
        return elapsed_time

    @staticmethod
    def isLastUpdateTimeExceeding(file_path, seconds):
        '''
        ファイル(file_path)の最終更新日時から指定秒(seconds)以上経過しているか
        '''
        elapsed_time = getElapsedTime(file_path)
        ten_minutes = datetime.timedelta(seconds=seconds)
        if elapsed_time > ten_minutes:
            return True
        else:
            return False

    @staticmethod
    def diffUpdateTime(file_path1, file_path2):
        '''
        ファイル間(file_path1,file_path2)の最終更新日時の差を求める
        '''
        stat1 = os.stat(file_path1)
        last_update_time1 = datetime.datetime.fromtimestamp(stat1.st_mtime)
        stat2 = os.stat(file_path2)
        last_update_time2 = datetime.datetime.fromtimestamp(stat2.st_mtime)
        diff_time = last_update_time1 - last_update_time2
        return diff_time


class MayaUtility(object):

    @staticmethod
    def openSceneFile(path, executeScriptNodes):
        '''
        シーン読み込む
        '''
        path = pmp(path)
        fbxPlug = "fbxmaya"
        types = {".ma": "mayaAscii", ".mb": "mayaBinary",
                 ".fbx": "FBX", ".obj": "OBJ"}
        options = {".ma": "v=0", ".mb": "v=0",
                   ".fbx": "fbx", ".dae": "dae", ".obj": "obj"}
        sceneName = pm.sceneName()
        fileType = types[path.ext.lower()]
        options[path.ext.lower()]
        scenePath = path.replace("\\", "/")
        prjPath = path.parent.normpath().rsplit("\\scenes", 1)[0]
        io = om.MFileIO()
        nameSpace = os.path.splitext(os.path.basename(scenePath))[0]
        if not sceneName:
            mel.eval('saveChanges("");')
            try:
                pm.loadPlugin("{0:}.mll".format(fbxPlug), qt=1)
                cmds.file(scenePath, o=True, f=True, executeScriptNodes=executeScriptNodes)
            except:
                pass

            MayaUtility.fixTexturePath(path)
            MayaUtility.addRecentFile(scenePath, fileType)
            MayaUtility.setProject(prjPath.replace("\\", "/"))
        else:
            flag = 1
            while flag:
                result = pm.confirmDialog(t=u"開く", m=u"読み込み方を選択してください", b=[
                                          u"新しいシーン", u"リファレンスとして読み込む", u"キャンセル"], db=u"新しいシーン", cb=u"リファレンスとして読み込む", ds=u"キャンセル")
                if result == u"キャンセル":
                    return
                else:
                    flag = 0
                    if result == u"新しいシーン":
                        pm.loadPlugin("{0:}.mll".format(fbxPlug), qt=1)
                        mel.eval('saveChanges("");')
                        cmds.file(scenePath, o=True, f=True, executeScriptNodes=executeScriptNodes)
                        MayaUtility.addRecentFile(scenePath, fileType)
                        MayaUtility.setProject(prjPath.replace("\\", "/"))
                    elif result == u"リファレンスとして読み込む":
                        pm.loadPlugin("{0:}.mll".format(fbxPlug), qt=1)
                        if fbxPlug not in pm.pluginInfo(q=1, ls=1):
                            om.MGlobal.displayError(
                                "{0:} Plugin in not loaded".format(fbxPlug))
                            return
                        if cmds.optionVar(q=g_refecrenceOptionVar):
                            cmds.file(
                                scenePath,
                                ignoreVersion=True,
                                ns=nameSpace,
                                r=True,
                                executeScriptNodes=executeScriptNodes,
                            )
                        else:
                            file_pattern = re.compile(r'\d+$')
                            basename = os.path.basename(scenePath)
                            filename, _ = os.path.splitext(basename)
                            file_pattern_match = file_pattern.match(
                                r'{}'.format(filename),
                            )
                            if file_pattern_match:
                                message = u'数字のみの ma ファイルを指定しています。'
                                message += u'\n\nファイル保存時に参照ファイルが読み'
                                message += u'込めない可能性があるのでリファレンス'
                                message += u'ノード名に\nプレフィックスを追加します。\n\n '
                                message += u'Yes = 文字列 (ref_) を先頭に'
                                message += u'追加して参照ファイルを読み込みます。'
                                message += u'\n\nNo = 処理を中断します。'
                                confirm_dmn = pm.confirmDialog(
                                    t=u"確認",
                                    m=message,
                                    b=["Yes", u"No"],
                                    db="Yes",
                                    ds="No"
                                )
                                if confirm_dmn == 'Yes':
                                    cmds.file(
                                        scenePath,
                                        r=True,
                                        type='mayaAscii',
                                        iv=True,
                                        gl=False,
                                        rpr='ref_',
                                        op='v=0;p=17;f=0',
                                        esn=executeScriptNodes,
                                    )
                                else:
                                    return
                            else:
                                cmds.file(scenePath, r=True, executeScriptNodes=executeScriptNodes)

                    MayaUtility.fixTexturePath(path)

        [cmds.setAttr(x + '.ftn', cmds.getAttr(x + '.ftn'), type='string')
         for x in cmds.ls(typ='file', type='mentalrayTexture')]

    @staticmethod
    def setProject(project):
        '''
        プロジェクト設定する
        '''
        mel.eval('setProject ' + '"' + project + '"')

    @staticmethod
    def addRecentFile(filePath, fileType):
        '''
        最近使ったファイルに追加
        '''
        maxSize = pm.optionVar["RecentFilesMaxSize"]
        if pm.optionVar.get("RecentFilesList") is not None:
            [[pm.optionVar(rfa=["RecentFilesList", i]), pm.optionVar(rfa=["RecentFilesTypeList", i])]
             for i, x in enumerate(pm.optionVar.get("RecentFilesList")) if filePath == x]
        pm.optionVar(sva=["RecentFilesList", filePath])
        pm.optionVar(sva=["RecentFilesTypeList", fileType])

        fileList = pm.optionVar["RecentFilesList"]
        if len(fileList) > maxSize:
            [[pm.optionVar(rfa=["RecentFilesList", 0]), pm.optionVar(
                rfa=["RecentFilesTypeList", 0])] for i, x in enumerate(fileList) if i >= maxSize]

    @staticmethod
    def fixTexturePath(path):
        '''
        テクスチャパス修正する
        '''
        listedNodes = cmds.ls(type="file")

        if len(listedNodes) > 0:
            for currNode in listedNodes:
                if not pmp(cmds.getAttr(currNode + '.fileTextureName')).exists():
                    print("-----------------------")
                    print("NODE: " + currNode)

                    if cmds.referenceQuery(currNode, isNodeReferenced=True) == 1:
                        dir_path = cmds.referenceQuery(currNode, filename=True).split("scenes")[
                            0] + "sourceimages/"
                        print("REFERENCE PATH " + dir_path)
                    else:
                        dir_path = path.split("scenes")[0] + "sourceimages/"
                        print("DIR PATH " + dir_path)

                    path_old = cmds.getAttr(
                        currNode + '.fileTextureName').split("/")
                    tex_name = path_old[len(path_old) - 1]
                    print("TEXTURE NAME: " + tex_name)

                    path_new = pmp(dir_path + tex_name)

                    if path_new.exists():
                        cmds.setAttr(currNode + '.fileTextureName',
                                     path_new, type="string")
                        print("NEW PATH: " + path_new)
                        print("-----------------------")

    @staticmethod
    def isSceneFile(path):
        '''
        シーンファイルであるかの判定を返す
        '''
        types = {".ma": "mayaAscii", ".mb": "mayaBinary",
                 ".fbx": "FBX", ".obj": "OBJ"}
        fileName = os.path.basename(path)
        name, ext = os.path.splitext(fileName)
        if ext in list(types.keys()):
            return True
        else:
            return False


class Resources(object):
    '''
    アイコンリソース
    '''
    qt_resource_data = b"\x00\x00;\xa1\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x11\x00\x00\x00\x18\x08\x04\x00\x00\x00\xb6k\xde\xb9\x00\x00\x00\x09pHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x009\xeciTXtXML:com.adobe.xmp\x00\x00\x00\x00\x00<?xpacket begin=\x22\xef\xbb\xbf\x22 id=\x22W5M0MpCehiHzreSzNTczkc9d\x22?>\x0a<x:xmpmeta xmlns:x=\x22adobe:ns:meta/\x22 x:xmptk=\x22Adobe XMP Core 5.6-c014 79.156797, 2014/08/20-09:53:02        \x22>\x0a   <rdf:RDF xmlns:rdf=\x22http://www.w3.org/1999/02/22-rdf-syntax-ns#\x22>\x0a      <rdf:Description rdf:about=\x22\x22\x0a            xmlns:xmp=\x22http://ns.adobe.com/xap/1.0/\x22\x0a            xmlns:dc=\x22http://purl.org/dc/elements/1.1/\x22\x0a            xmlns:photoshop=\x22http://ns.adobe.com/photoshop/1.0/\x22\x0a            xmlns:xmpMM=\x22http://ns.adobe.com/xap/1.0/mm/\x22\x0a            xmlns:stEvt=\x22http://ns.adobe.com/xap/1.0/sType/ResourceEvent#\x22\x0a            xmlns:tiff=\x22http://ns.adobe.com/tiff/1.0/\x22\x0a            xmlns:exif=\x22http://ns.adobe.com/exif/1.0/\x22>\x0a         <xmp:CreatorTool>Adobe Photoshop CC 2014 (Windows)</xmp:CreatorTool>\x0a         <xmp:CreateDate>2016-01-06T22:30:53+09:00</xmp:CreateDate>\x0a         <xmp:ModifyDate>2016-01-06T23:35:11+09:00</xmp:ModifyDate>\x0a         <xmp:MetadataDate>2016-01-06T23:35:11+09:00</xmp:MetadataDate>\x0a         <dc:format>image/png</dc:format>\x0a         <photoshop:ColorMode>1</photoshop:ColorMode>\x0a         <xmpMM:InstanceID>xmp.iid:27932bbb-8118-a148-973a-c1bd71dedbf2</xmpMM:InstanceID>\x0a         <xmpMM:DocumentID>adobe:docid:photoshop:aa07cd4c-b482-11e5-b313-d3d4949f05fd</xmpMM:DocumentID>\x0a         <xmpMM:OriginalDocumentID>xmp.did:586b4dbd-d2a9-8846-8913-52af9a534cbd</xmpMM:OriginalDocumentID>\x0a         <xmpMM:History>\x0a            <rdf:Seq>\x0a               <rdf:li rdf:parseType=\x22Resource\x22>\x0a                  <stEvt:action>created</stEvt:action>\x0a                  <stEvt:instanceID>xmp.iid:586b4dbd-d2a9-8846-8913-52af9a534cbd</stEvt:instanceID>\x0a                  <stEvt:when>2016-01-06T22:30:53+09:00</stEvt:when>\x0a                  <stEvt:softwareAgent>Adobe Photoshop CC 2014 (Windows)</stEvt:softwareAgent>\x0a               </rdf:li>\x0a               <rdf:li rdf:parseType=\x22Resource\x22>\x0a                  <stEvt:action>saved</stEvt:action>\x0a                  <stEvt:instanceID>xmp.iid:27932bbb-8118-a148-973a-c1bd71dedbf2</stEvt:instanceID>\x0a                  <stEvt:when>2016-01-06T23:35:11+09:00</stEvt:when>\x0a                  <stEvt:softwareAgent>Adobe Photoshop CC 2014 (Windows)</stEvt:softwareAgent>\x0a                  <stEvt:changed>/</stEvt:changed>\x0a               </rdf:li>\x0a            </rdf:Seq>\x0a         </xmpMM:History>\x0a         <tiff:Orientation>1</tiff:Orientation>\x0a         <tiff:XResolution>720000/10000</tiff:XResolution>\x0a         <tiff:YResolution>720000/10000</tiff:YResolution>\x0a         <tiff:ResolutionUnit>2</tiff:ResolutionUnit>\x0a         <exif:ColorSpace>65535</exif:ColorSpace>\x0a         <exif:PixelXDimension>17</exif:PixelXDimension>\x0a         <exif:PixelYDimension>24</exif:PixelYDimension>\x0a      </rdf:Description>\x0a   </rdf:RDF>\x0a</x:xmpmeta>\x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                            \x0a<?xpacket end=\x22w\x22?><f\xe6R\x00\x00\x00 cHRM\x00\x00z%\x00\x00\x80\x83\x00\x00\xf9\xff\x00\x00\x80\xe9\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17o\x92_\xc5F\x00\x00\x01/IDATx\xda\xc4\xd2=K\x1dA\x14\xc6\xf1\xdf\xcc.\xa4\xd1F\xf0\x85\x90\x1b\xc2\xb5\xb8\x85\x86\x5c\x82U\xea\x80\x85]\x0a\x91@>\x8f\x22\xbe\xa1\xdf\xc2F\x02A\xd2\xa4M\x93\xda\xaf\x10\xd3\x85@\xc0(;\xb3\x16\xde\xdd\xf5\xbeX\xe7\xe9\xce\x9cg\xf8?\xe7\xcc\x84\xa1V\x85d\xd3W\xef}SH\xcdql\x0dA2\xef\x10\xc7\xe6$a\xdaR`\xcf\x9a[\xaf\xed\x8e\xea\x87\xbb\xc3\x0e\xb2\xe5\x8b,\xca\xa2-\x97\x0d,\xb6\x90\x05\xa7],g\x16\x1aXlq\xfb\xfa*\x11Q\xa5\xef\xa0\xe9\x16+\x0f\x90\x0f\xf6$e\x9b0y\xeb\xca\x95B\x1d\x86Am\xd9\x0f=\xf9Q\xf8Z\xf0\xd3\x86k!\x8a8\xd2\x1bA\xba\x15T\x9e;A\x8c\x92\x1d\x1f\x1fA\x1a\x95\x92m\x9f\xa40\xec\xf9\xee\x85\xd4\xed\xa1U\x16\xfd\xf2\xaeX\xb9\xf0F\x9ea \xc8\xe6m\x94^\xf9#\xcb\xe6<\x1b3\xdc\xf9+\x08^F\xeb\xfa\x06\x96\x9c\xa3\x1a\xb5+|\xb6h`\xd5\xa0\xf4\xcf\x8dRv7\x81\xb9\x95\xfdV\x09\x11\xa1{\xd5\xb1$\xa3N\xa9Fm\xb6j\xb5\xb1u=\xa1\xff`\xa9\xa7\xa2\xce\xf8\xde\xd3COX\xae',m}?\x00\x17hM8\xe2r\xfb$\x00\x00\x00\x00IEND\xaeB`\x82\x00\x00;\x9d\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x18\x00\x00\x00\x11\x08\x04\x00\x00\x00mq\xa4\xbb\x00\x00\x00\x09pHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x009\xeciTXtXML:com.adobe.xmp\x00\x00\x00\x00\x00<?xpacket begin=\x22\xef\xbb\xbf\x22 id=\x22W5M0MpCehiHzreSzNTczkc9d\x22?>\x0a<x:xmpmeta xmlns:x=\x22adobe:ns:meta/\x22 x:xmptk=\x22Adobe XMP Core 5.6-c014 79.156797, 2014/08/20-09:53:02        \x22>\x0a   <rdf:RDF xmlns:rdf=\x22http://www.w3.org/1999/02/22-rdf-syntax-ns#\x22>\x0a      <rdf:Description rdf:about=\x22\x22\x0a            xmlns:xmp=\x22http://ns.adobe.com/xap/1.0/\x22\x0a            xmlns:dc=\x22http://purl.org/dc/elements/1.1/\x22\x0a            xmlns:photoshop=\x22http://ns.adobe.com/photoshop/1.0/\x22\x0a            xmlns:xmpMM=\x22http://ns.adobe.com/xap/1.0/mm/\x22\x0a            xmlns:stEvt=\x22http://ns.adobe.com/xap/1.0/sType/ResourceEvent#\x22\x0a            xmlns:tiff=\x22http://ns.adobe.com/tiff/1.0/\x22\x0a            xmlns:exif=\x22http://ns.adobe.com/exif/1.0/\x22>\x0a         <xmp:CreatorTool>Adobe Photoshop CC 2014 (Windows)</xmp:CreatorTool>\x0a         <xmp:CreateDate>2016-01-06T22:32:25+09:00</xmp:CreateDate>\x0a         <xmp:ModifyDate>2016-01-06T23:34:22+09:00</xmp:ModifyDate>\x0a         <xmp:MetadataDate>2016-01-06T23:34:22+09:00</xmp:MetadataDate>\x0a         <dc:format>image/png</dc:format>\x0a         <photoshop:ColorMode>1</photoshop:ColorMode>\x0a         <xmpMM:InstanceID>xmp.iid:711372d9-f949-dc41-9ca1-5bcb1ccb2780</xmpMM:InstanceID>\x0a         <xmpMM:DocumentID>adobe:docid:photoshop:8feaed3d-b482-11e5-b313-d3d4949f05fd</xmpMM:DocumentID>\x0a         <xmpMM:OriginalDocumentID>xmp.did:be5430ae-21c4-b445-9212-e8f14aafbb87</xmpMM:OriginalDocumentID>\x0a         <xmpMM:History>\x0a            <rdf:Seq>\x0a               <rdf:li rdf:parseType=\x22Resource\x22>\x0a                  <stEvt:action>created</stEvt:action>\x0a                  <stEvt:instanceID>xmp.iid:be5430ae-21c4-b445-9212-e8f14aafbb87</stEvt:instanceID>\x0a                  <stEvt:when>2016-01-06T22:32:25+09:00</stEvt:when>\x0a                  <stEvt:softwareAgent>Adobe Photoshop CC 2014 (Windows)</stEvt:softwareAgent>\x0a               </rdf:li>\x0a               <rdf:li rdf:parseType=\x22Resource\x22>\x0a                  <stEvt:action>saved</stEvt:action>\x0a                  <stEvt:instanceID>xmp.iid:711372d9-f949-dc41-9ca1-5bcb1ccb2780</stEvt:instanceID>\x0a                  <stEvt:when>2016-01-06T23:34:22+09:00</stEvt:when>\x0a                  <stEvt:softwareAgent>Adobe Photoshop CC 2014 (Windows)</stEvt:softwareAgent>\x0a                  <stEvt:changed>/</stEvt:changed>\x0a               </rdf:li>\x0a            </rdf:Seq>\x0a         </xmpMM:History>\x0a         <tiff:Orientation>1</tiff:Orientation>\x0a         <tiff:XResolution>720000/10000</tiff:XResolution>\x0a         <tiff:YResolution>720000/10000</tiff:YResolution>\x0a         <tiff:ResolutionUnit>2</tiff:ResolutionUnit>\x0a         <exif:ColorSpace>65535</exif:ColorSpace>\x0a         <exif:PixelXDimension>24</exif:PixelXDimension>\x0a         <exif:PixelYDimension>17</exif:PixelYDimension>\x0a      </rdf:Description>\x0a   </rdf:RDF>\x0a</x:xmpmeta>\x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                            \x0a<?xpacket end=\x22w\x22?>\xbfg\x09\x10\x00\x00\x00 cHRM\x00\x00z%\x00\x00\x80\x83\x00\x00\xf9\xff\x00\x00\x80\xe9\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17o\x92_\xc5F\x00\x00\x01+IDATx\xda\x8c\xd2\xbfJ\x5cQ\x10\x06\xf0\xdf\xb9\xe7\xc8Z\x04\x82\x85\xa0\x08>\xc3>\x80O\x10\x92.\x85E\xf0\x11D\x8cV\x82\x0f\x90G0\xa4\x90\x14\x16!\x09\xe4\x1d\xac,le\x9b\xe0\x1fPL\x88\x92N\xbc\xe7\x9e\x14\xbb\xb2\xde\xddK\xf4\x9b\xea0g\xbeo\xe6\x9b\x09}\x13\x08\x98q\xec\x8f5?EE\xf38]\x99F\xd13o\xc5\xa15Y#\xb6\x0bRGD\x8d\xc6\xa2}_,\xc9\xa20.\xa8'\xe2^\xedVQ\xc9\xb2\xb7\x8e\xac\xca\xca\x83N\xb2kY\x193\x80\x19/Q\x09\xb2E\x07^\xd9r-j\x94\xd0/\xfe\x8f\xa2\x11\x9d\xd9\xf0\x1d\xb1\x92\xa7\x9a\xaa\xd5-\xd7\xa2\xda\xb2o>\x9a\x93\x9fV\x18\xa2QD\x03[\xcf-\x80;\xbd\xee=t+d=\x03oR\xab\xdf1R\xebUK\xf8d\xdbM\x9aHu\xbb\x94\x5c\xd8\xf0\x151\xf9\xd0\xb1\x87\xe4\xb5Y\x90E\xd1\x81MW\xa2F\x0e\xfdn\xdeK\x0b#g~y\xef3\xa2<\xe4J\xca\xe8F\xc7x!(*\xfc\xb0\xeet\xc8\xfd ^O\x9dw\x91\x05\xc1o;\xf6&\xfft\x8d\x1c\xdc\xf9\xeb\xdc;'\xa2\xd2\xa6\xfc7\x00\x1b\x8fkh\xfc\x7f\xf2,\x00\x00\x00\x00IEND\xaeB`\x82\x00\x00\x02E\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x11\x00\x00\x00\x18\x08\x04\x00\x00\x00\xb6k\xde\xb9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00 cHRM\x00\x00z&\x00\x00\x80\x84\x00\x00\xfa\x00\x00\x00\x80\xe8\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17p\x9c\xbaQ<\x00\x00\x00\x02bKGD\x00\x00\xaa\x8d#2\x00\x00\x00\xf1IDAT(\xcf\xc5\xd1\xb1J\x03A\x10\xc6\xf1\xdf\xde\x1d\x88\x10\x9b\x93 \x16\x16>\x8b\x85\xa0\x9dX\xd8\xf8Tb'\x16\x82\x85\xbe\x83\x9dO \xb6i\x14Ii\xa1`\x8c\xc9\x8d\x85\x17\xbdl\x22\x96~\xcb\xb23\xec\x9f\xf9fg\xf9Q\x89]a\xa7\x8d\x17\x94\xb0\xe6^\xb8\xd3k\xf3L\x15N\x85\x91p\xd2\xe6s*\xb1/L\xdb\xbd\x97\x9b%\xd4\x06\x1dd\xa0\x9e7+q&|\x08\xd1\x9e\xe7\xdd:%\x0e\x84I\x0bD\x1b\x1f\xce\xa0\x84\x0d\x0f\xad\xc1l5\xc2\x93\xcd\xaf\xfb\x12\x97\x1d\x93\xe8\x98]\xcd\xea\x1ce&]\xb3c\xd8\xf2\xf8\x0b2\x15\x86\xb6\xb9\xc9\xba\xc8\xa1\xdbd`]\xa3\xd1\xb327\xcc\xb1WI\xf2\xc2\xaaZ_\xe1\x22\x9b\xcb\xb5B_m\xb52\xf2\xa6\xd2\x18g_\xf2\xae\xf1l\x22\x15H\xcb~U\x9a\xddT\x02a\xb9BP\xf8S\xff\x80\xe4-\xc7\x22\x92?<-\x22\xc3\x0c\xf9\xce?\x01,\x85\x89\x1a\xbd\x89e\xea\x00\x00\x00%tEXtdate:create\x002015-02-14T11:50:47-06:00\x95\xc21>\x00\x00\x00%tEXtdate:modify\x002015-02-14T11:50:47-06:00\xe4\x9f\x89\x82\x00\x00\x00ctEXtsvg:comment\x00 Generator: Adobe Illustrator 15.0.2, SVG Export Plug-In . SVG Version: 6.00 Build 0)  \x87-\xb9\xf5\x00\x00\x00\x00IEND\xaeB`\x82\x00\x00\x02H\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x18\x00\x00\x00\x11\x08\x04\x00\x00\x00mq\xa4\xbb\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00 cHRM\x00\x00z&\x00\x00\x80\x84\x00\x00\xfa\x00\x00\x00\x80\xe8\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17p\x9c\xbaQ<\x00\x00\x00\x02bKGD\x00\x00\xaa\x8d#2\x00\x00\x00\xf4IDAT(\xcf\x8d\xd2?/\x04Q\x14\x05\xf0\xdf\xec\xec\x86\x10\x0d\xf1'\x11\x95\xaf\xa0\xd3\xa9\x954TZ\x9fD\x22\xbe\x82\xa8%:\x9dZ\xa5R\xe9\x88d\x13\xdb-\xba\xb53\xaebF\xe4\xad\xc9\xec\x9eS\xbd\xdc{O\xde\xb9\xf7\x90\x22\x93c\xd3\x9dg\x0b2\x99V\xe4\xe0\xd0\xab\xf0i\x95\xb6\x81L\x17+\xae\x84P\x1aZ\xd7\xd5\xd3\x9d`\xa2\xbd\xefE(\x14\xc2\xf0\xaf\x98\xeaV\xff.,9s\x8a\xa2n\xfcrm\x94\xf4\x86\xcc\xe0W{\xcf\x93P*\xc5\x14b\xde\xb9\x10\xc6\x13\xa5q#\xedz\x98Q;\x84\xc8\x04F\xe6\xcc\x88\xdc\xa3\x1dk\xca\xf6\x9d\xa7Xv\xd9\xe8\xa1h\xf6Pm\xe9@_(|O\xf7@\xa6\xa3\xb4\xe1\xc2\x11\xcaZb\xec\xf6\xdf\x1d:\xde\xd2K\x1f\x1b\x08\x85R\x18\xea\xb5;\xa9r\xba\xe5\xa6\xce\xd2{\x9d\xa5<\xe1D\x5c\xaa\xe7\x89\x81\xf01-\xad\x15:rl\xbb\xd7\xb7\xd84\xf0\x03\xa1Y\x9dQ\x9e<\xfd\xf7\x00\x00\x00%tEXtdate:create\x002015-02-14T11:50:32-06:00\xcd?\x17\x80\x00\x00\x00%tEXtdate:modify\x002015-02-14T11:50:32-06:00\xbcb\xaf<\x00\x00\x00ctEXtsvg:comment\x00 Generator: Adobe Illustrator 15.0.2, SVG Export Plug-In . SVG Version: 6.00 Build 0)  \x87-\xb9\xf5\x00\x00\x00\x00IEND\xaeB`\x82\x00\x00\x02\x99\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x14\x00\x00\x00\x18\x08\x04\x00\x00\x00PB\x15\xfd\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00 cHRM\x00\x00z&\x00\x00\x80\x84\x00\x00\xfa\x00\x00\x00\x80\xe8\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17p\x9c\xbaQ<\x00\x00\x00\x02bKGD\x00\x00\xaa\x8d#2\x00\x00\x01EIDAT(\xcf\xcd\xd1\xbdjTQ\x14\xc5\xf1\xdf9s\x07\x02\x8a\x0a\x0a\x8a\x95\x9d\x95\x9d\x85\x8f\xa0/amg\xa7mJ\xedR\x06\x93F\x14\xec\xb4\x8a\x95\xda\x04c\x1cP\x08haa\xe5\x0b\x88\x85\x04\xee\xdc,\x8b{s\x9dL\x12k\xd7\xa9\xce^\xff\xf3\xb1\xd7fQ\x13\x5c\xf5\xdd\x0f\xd7\x86\xdd\x89\xaa\xb8\xe8\xb3\x88/\xae\x9c\x86V\x9c7\x13\xadV\xec\xb9t\x12Zq\xc6\xb6\x88\x87\xee\x8b\x98\xb908G\xb0\x15oD<\x06\xab\x22\xb6\x9d]D\xabbjK\xc4\x1a\x1a\x0d\x1e\x89xk\xe5\x10-\xaa\xea\xa5\x88uL\x14E\x835\x11\xafM\x15\xb5\xa7_\x88x:`\xfd\xf1\x06\xeb\x22^\xa9}uS\xc4\xb3\x01\xf8\xab\x82'\x22\x9e\xc3\x86\xd8\xd7\xd9\xf5\xd1\xae\x1b\xa8*\xae{of\xc7\xdc~\x8f\xfe\x96a\xb5bul\xe6\xc1P\x19\xbc\xc6=\xb7\xb5\x8a\xce\x1d\x97\x17\x9e.\xf8iK\xc1\xd4\xbb\xc54?\x1d\xbb\xf1\xabz\xf8\xeff\xec\xb3;\xd2Ho\x97!,\xd2\xe8F+\xc7\xe6\x1f\x9d\x03E\x96&\xf9/\xfdG`\x1d\xe3Yr\x9a%\xf0\x00\xf3!\xaeS\xc1\x82\x9b\xee:\x87_n\xb1\x94\xec\xa8=\xd1\x8d\xd3\xed\xc4\xb7!\xf6\x85\x9fL\xb0\x83Nkn\xae\xd5\xe1\x83\xa8\xfd \xfe\x00e\x0bx%\xb1\xa0H*\x00\x00\x00%tEXtdate:create\x002015-02-14T00:23:46-06:00\xb1 \xac\xf9\x00\x00\x00%tEXtdate:modify\x002015-02-14T00:23:46-06:00\xc0}\x14E\x00\x00\x00ctEXtsvg:comment\x00 Generator: Adobe Illustrator 15.0.2, SVG Export Plug-In . SVG Version: 6.00 Build 0)  \x87-\xb9\xf5\x00\x00\x00\x00IEND\xaeB`\x82\x00\x00\x02\xa4\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x14\x00\x00\x00\x18\x08\x04\x00\x00\x00PB\x15\xfd\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00 cHRM\x00\x00z&\x00\x00\x80\x84\x00\x00\xfa\x00\x00\x00\x80\xe8\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17p\x9c\xbaQ<\x00\x00\x00\x02bKGD\x00\x00\xaa\x8d#2\x00\x00\x01PIDAT(\xcf\xc5\xd3=kTA\x14\xc6\xf1\xdf\xdc\x9d\x0b)\x12H\xb1\x88)\x04\x1b\x0b\x1b{?\x81\xc5\xd6\xf9\x0a\x96\x96\xc12\xe5v\xda\xf8RYY\x0a\xa62M\x82\x85\x82\x90*\x81@\x82\xad\x16\x92B\x05\x11\xe4\xee\xde\x9c\x14\xf7\x85\x9b\xddl\xeds\x8a\x19\xce\xfc\x19\xce<\xe7\x0c\x8dFx&T*33\x95Jx\x8d\xc2\x92N\x84Z\xb4Q\x0b\xe7\x12\x12\xe4\x01X\xe3\xc0\x9e\x0d\xfc11q)\x89\xe6p\x08\x06\xbex%cn\xc3\xa4\x83\xdcPA\x81,\xb7U\x0f\x94\x17\xc0K\xcc\xfb\x9d\xd57\xae\xd4\x7f\x04\xb3Qc\xa8\xba]\x87Jr\x9b\x8f\xac\xbe\xe6\xe3u\x85ygz\xb6\xed\x91\x99\xa4\xb6\xb5\x04\x8e\xbd\x00\xa5\x8f\xfc\xed\xbb;\x13v{\xc3w\xdaL\x13\xd5\xc8}\x0f\xfc\x93\x1c\xfb\xe9\xc2\xd4\x0f\x84\xf0\xdbC\xbf|sK%\xdb\x83\xb7Bx\xc3\xc2s\x12^\x0a\xe1\x9d\x82\xa4\xf0^\xb4\xd3\x97{\xb8\xd4Lh\xd8WJ\x14\x92\xd2\x07!<\xef\xd1\x8c\xa9\x10\x0e\xadu~\x17Xs(\x84)\xb2\x12\xbbB\xf8l}\xd8\x96\x02\xeb>\x89\xf6\xdd<\x15\xc2\x91\xcd\xc5\xee\x15\xd8t$\x84'\x1e\x0b\xe1\xd8\xd8\xd2\x5c6\x89\xb1\x93\xf6\x83\x853[7a\x1dz\xdb\xa9\x10\xbe\xba\xb3\x0a\xeb\xd0\xbb\xbe\xbbp\xcf\xc2\xf4_\x01\x99={\xff\x9fz\xda\xf1\x00\x00\x00%tEXtdate:create\x002015-02-14T00:22:54-06:00\x05\xd7\xd6p\x00\x00\x00%tEXtdate:modify\x002015-02-14T00:22:54-06:00t\x8an\xcc\x00\x00\x00ctEXtsvg:comment\x00 Generator: Adobe Illustrator 15.0.2, SVG Export Plug-In . SVG Version: 6.00 Build 0)  \x87-\xb9\xf5\x00\x00\x00\x00IEND\xaeB`\x82\x00\x00\x02E\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x18\x00\x00\x00\x11\x08\x04\x00\x00\x00mq\xa4\xbb\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00 cHRM\x00\x00z&\x00\x00\x80\x84\x00\x00\xfa\x00\x00\x00\x80\xe8\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17p\x9c\xbaQ<\x00\x00\x00\x02bKGD\x00\x00\xaa\x8d#2\x00\x00\x00\xf1IDAT(\xcf\x8d\xd3\xb1.DA\x18\x05\xe0o\xcc\xdd]\x0a\xc9\xaa%D\xe7al!\x22\xd1Pz\x00Q\xeb=\x03\x9dB\xa1\xf2\x0cZ\xad\x02\x95H\xd6ZO \xee\xbd\xa3\xb8\xbbbo\xae\x8cs\xaaIf\xfe\x93\xf3\x9f3\xb4\x11\x04}\x0f\xeel!Z\x92A\xc0\xaa\xa9d\xec\x08\xc4\xc5\x0bE\x8b=\x85\xa1\x89J\x92\xdcXG\x14r:o\x92R)\x19;\xf8\xad\x13\x9c\xd9\x90Z\x13z\xf6\xadH\x82J\xc4\x95SSQ-\x912\xac\x95\x92\x17\xbbs\x9d\xd2W\x07\x17\x1f5\xe7\x0bk\xe4\x15\x1aVJ\xc9\xa3Q\x90r\xfe\x7f\xf0i \x1f\xcb\x0c\xb5\xca\xc0\x93\x91N\x07\xdd\x1e.\xff\xe7\xa1\xd9\xd2\xab\xbdfK\xc1yG\x0e\x85\x1d\xcb0\xcb\xe1\xda\x89\xc9<\x87\xbf\x93n63u\xb8\xd8\xa8B\x14[}\x1a\x9a\xa8%\xc9\xad\xcd\x5c\x97\x9a\xb6\xbeK>\x1c\xcfFf\xea\x1d\xf4=\xbb\xb7\xad\xe3?|\x03\x1c\x8d\x9e\x8e\x9d\xddJ\x93\x00\x00\x00%tEXtdate:create\x002015-02-14T11:50:40-06:00Pe\x0f\xb0\x00\x00\x00%tEXtdate:modify\x002015-02-14T11:50:40-06:00!8\xb7\x0c\x00\x00\x00ctEXtsvg:comment\x00 Generator: Adobe Illustrator 15.0.2, SVG Export Plug-In . SVG Version: 6.00 Build 0)  \x87-\xb9\xf5\x00\x00\x00\x00IEND\xaeB`\x82\x00\x00\x02\x87\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x14\x00\x00\x00\x18\x08\x04\x00\x00\x00PB\x15\xfd\x00\x00\x00\x02bKGD\x00\x00\xaa\x8d#2\x00\x00\x00\x09pHYs\x00\x00\x00H\x00\x00\x00H\x00F\xc9k>\x00\x00\x01\x95IDAT(\xcf}\xd3=hTA\x14\xc5\xf1\xdf\xfbHd1K$ \x82HPR\x99R[%\x8aM\xc0J\x10\x04\xab\x80`\x1b\x94\x88\x226\x0aZ\xda\x0aA\x9b\x80\x9dm\xc0\xdeR\xb0\x8c\x08&\x1b\xabh\xe5\xc7F]\xcd\xbew-\xf6\xed\xee[\xb3:S\xcd\xcc\x9f3s\xce\xdc\x9bH\x95\x8e\x99\x97\xfa{d\xde\xd8\x91)\xfa\x1bw|\x17\xfbf!l\x9aC\xd6\xc3V\x84r\x0cX\xea\x0a\xdb}4\xf1\xc1\xac\xf7\x96}\x93\x89\xc1\xa5\x9f-[\xf2S\xc3\xb6\x0b\xb6\xe4t\x84\xfb\xc8k\xaf\xcb\xf1\xd8+w\x85\xd0r\x82T\x8a.\xb2\x91\xc9\x0f\x87=\xf2\x00\xc7\xbd4\xc7o\xe1^M1\x91\x99\xc0)\xe16\x9e\x08\xe1\xdd~\xb07R\x5c\x17\xba\xbe\x08\x85b4\xbd\x04\xb9gV%Xu\xc4E\x8b\x9eKuG\x15s\x9c\x15\xc2\x19\x1c\xa8v\x1e\x0a\xbf\xd2\x9aZ*\x06O\xc8\xd1\x95\xc9\xab{\x92!\x18\x123&5A\xd3\xa4\x99*\x8f@\x0c-\x14\xd6\x5c\xd2\xd6\x00k:\x9a^X\xaaG\xdb\x13\x9f\xb2\xe0\xa0FU\x1c\x87\x94R\xe7M\xd9\x95\x0c\xc1@\xdb\x15\x8b\xbe\x9aw\x0dO\xbd5m\xddnuj\xd4u\x86sBX\xa8Vc\x5c\x93\x0e\x22\xea\x87U;\xad\xffGi\x0f-\x1d\x85-\xec)\x87\xe8\xd0LV\xa5\xb8\xe9\xb4\xd0\x92\x0b\x99L\xb7o\xa6\xc4\x04\x8aA\xc9oP%\xd8\x93\x98@\x99\xfbd\xd6U\xafk\x85\x9b\xa2\xac\xb0\xc2\xb4\xcb\xf8\xc8\xcd\x7f\xb4B\xbd)\xc2\x0d\xb8\xa5\xfd_\xb0m\xa5W\x0a\xa5\xa3N\x8ei\xd7~\x16\x1bv\xa4\x7f\x00\xd6:\xb2>j\x8f\xbc\x05\x00\x00\x00%tEXtdate:create\x002015-02-15T20:17:56+00:00Q\xb7\x83\xe1\x00\x00\x00%tEXtdate:modify\x002015-02-15T20:17:56+00:00 \xea;]\x00\x00\x00(tEXtsvg:base-uri\x00file:///tmp/magick-JLDSCIv6\xb9\xec1\xb3\x00\x00\x00\x00IEND\xaeB`\x82\x00\x00;\xa4\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x18\x00\x00\x00\x11\x08\x04\x00\x00\x00mq\xa4\xbb\x00\x00\x00\x09pHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x009\xeciTXtXML:com.adobe.xmp\x00\x00\x00\x00\x00<?xpacket begin=\x22\xef\xbb\xbf\x22 id=\x22W5M0MpCehiHzreSzNTczkc9d\x22?>\x0a<x:xmpmeta xmlns:x=\x22adobe:ns:meta/\x22 x:xmptk=\x22Adobe XMP Core 5.6-c014 79.156797, 2014/08/20-09:53:02        \x22>\x0a   <rdf:RDF xmlns:rdf=\x22http://www.w3.org/1999/02/22-rdf-syntax-ns#\x22>\x0a      <rdf:Description rdf:about=\x22\x22\x0a            xmlns:xmp=\x22http://ns.adobe.com/xap/1.0/\x22\x0a            xmlns:dc=\x22http://purl.org/dc/elements/1.1/\x22\x0a            xmlns:photoshop=\x22http://ns.adobe.com/photoshop/1.0/\x22\x0a            xmlns:xmpMM=\x22http://ns.adobe.com/xap/1.0/mm/\x22\x0a            xmlns:stEvt=\x22http://ns.adobe.com/xap/1.0/sType/ResourceEvent#\x22\x0a            xmlns:tiff=\x22http://ns.adobe.com/tiff/1.0/\x22\x0a            xmlns:exif=\x22http://ns.adobe.com/exif/1.0/\x22>\x0a         <xmp:CreatorTool>Adobe Photoshop CC 2014 (Windows)</xmp:CreatorTool>\x0a         <xmp:CreateDate>2016-01-06T23:14:31+09:00</xmp:CreateDate>\x0a         <xmp:ModifyDate>2016-01-06T23:33:57+09:00</xmp:ModifyDate>\x0a         <xmp:MetadataDate>2016-01-06T23:33:57+09:00</xmp:MetadataDate>\x0a         <dc:format>image/png</dc:format>\x0a         <photoshop:ColorMode>1</photoshop:ColorMode>\x0a         <xmpMM:InstanceID>xmp.iid:13ac7bd7-fb76-0942-916d-c08516564a35</xmpMM:InstanceID>\x0a         <xmpMM:DocumentID>adobe:docid:photoshop:75cc5ae0-b482-11e5-b313-d3d4949f05fd</xmpMM:DocumentID>\x0a         <xmpMM:OriginalDocumentID>xmp.did:cba44650-a2d0-ac45-aeaa-c8222a940052</xmpMM:OriginalDocumentID>\x0a         <xmpMM:History>\x0a            <rdf:Seq>\x0a               <rdf:li rdf:parseType=\x22Resource\x22>\x0a                  <stEvt:action>created</stEvt:action>\x0a                  <stEvt:instanceID>xmp.iid:cba44650-a2d0-ac45-aeaa-c8222a940052</stEvt:instanceID>\x0a                  <stEvt:when>2016-01-06T23:14:31+09:00</stEvt:when>\x0a                  <stEvt:softwareAgent>Adobe Photoshop CC 2014 (Windows)</stEvt:softwareAgent>\x0a               </rdf:li>\x0a               <rdf:li rdf:parseType=\x22Resource\x22>\x0a                  <stEvt:action>saved</stEvt:action>\x0a                  <stEvt:instanceID>xmp.iid:13ac7bd7-fb76-0942-916d-c08516564a35</stEvt:instanceID>\x0a                  <stEvt:when>2016-01-06T23:33:57+09:00</stEvt:when>\x0a                  <stEvt:softwareAgent>Adobe Photoshop CC 2014 (Windows)</stEvt:softwareAgent>\x0a                  <stEvt:changed>/</stEvt:changed>\x0a               </rdf:li>\x0a            </rdf:Seq>\x0a         </xmpMM:History>\x0a         <tiff:Orientation>1</tiff:Orientation>\x0a         <tiff:XResolution>720000/10000</tiff:XResolution>\x0a         <tiff:YResolution>720000/10000</tiff:YResolution>\x0a         <tiff:ResolutionUnit>2</tiff:ResolutionUnit>\x0a         <exif:ColorSpace>65535</exif:ColorSpace>\x0a         <exif:PixelXDimension>24</exif:PixelXDimension>\x0a         <exif:PixelYDimension>17</exif:PixelYDimension>\x0a      </rdf:Description>\x0a   </rdf:RDF>\x0a</x:xmpmeta>\x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                                                                                                    \x0a                            \x0a<?xpacket end=\x22w\x22?>W\x15\x81C\x00\x00\x00 cHRM\x00\x00z%\x00\x00\x80\x83\x00\x00\xf9\xff\x00\x00\x80\xe9\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17o\x92_\xc5F\x00\x00\x012IDATx\xda\x8c\xd21k\x15A\x14\x05\xe0ofV\x12\x0cBPI\x1e\xd8\x086\x16\x16K\xd0\xeau!\xa5M\x10\x9b\xa4\x08\xa4L\xed?\xb0\xb1y\x10\x10\xeb\xd8\xa4\x15\x04\x7fC\xfeA E\xba\x14\x89E@\x10\x22!3\xfb,\xcc3\xbb\xfb\xb6\xc8=\xd5\xc0\xb9\xe7\xdc{\xee\x84Z\xa7\x82\xa8x\xe6\xab\x17^\xf9\x83i\x97\x10;\xafd\xaax\xef\xc8\x86\xa7\x96\xfad\xa8Z\xdaI\xf6\xc4\xc4\x0e\x1aET\x09\xfd\xa6\xea\xbfv\x91\xbd\xf5\xd9s\x05\x09\x97\xf2\xb0\xc3?\xedG>\xd9C\xbe\x15y\xe8\xc0u\x87;\x15\x5c\x84:)X\xf7\xc5K\xcd\xdcV\x03\x0e\xc5\xa2\x8f>\xb4\xb4g\x95\x87\x1b\xc6\xf6\xbd\xd6t\x02\xe8\x07\xd2\xce\xbd\x9e\xe2\xda\x82{V\xb4\xe9\xd4\x82\xa2\xb9_C\x1a\x9d8\xb4bM\x90{\x0b\x17\xcd<\xd2(\xb9\xf2\xdd\xb1\xb1eE\x10Z\xee\x03\x08\xf5\xec\xff\x8cLl\xa1H\xe0\xc6\x8f\xb9;D\xe7\xa1\xbe\xbb4\xdb&V\x15A\xf4\xcb\x8a\x9b\xa1\xa5g\xf3\x06\xc9\xa17\xbeI\xa2F\xf0X\xe5\x81\xd4A\x15[\x86E\xe5\xcc;\xbb~\x8a\x82F\x96\x95\x0er\xec\xdd6J\x0e\x8c\x1d\xf9\xedj(\xd6\xbf\x03\x00/9_$\x050\x9dn\x00\x00\x00\x00IEND\xaeB`\x82\x00\x00\x02\xb0\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x16\x00\x00\x00\x18\x08\x04\x00\x00\x00T\xb7\xc5\xc0\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00 cHRM\x00\x00z&\x00\x00\x80\x84\x00\x00\xfa\x00\x00\x00\x80\xe8\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17p\x9c\xbaQ<\x00\x00\x00\x02bKGD\x00\x00\xaa\x8d#2\x00\x00\x01\x5cIDAT8\xcb\xdd\xd3\xbbjTQ\x14\x06\xe0o_\xce\x19c\x84(&j*\xab\x01\x0b\xb1\xb2\x09X\xa6\xb5\xb4\x10DA\xf0\x05|\x0bk-\x04_@_\xc1\xc6\xc2\xceR\x0bA\xec,\x15\x84\xc08$3\xe7l\x8bs\x99\xc9h\x0a[\xff\x0dk\xef\xbd\xd6\xbf\xae\xb0\x08b\x7f*\xdcS4\x8ab\xa9x\x84z\xb4\x87\x8cV\x87\x88+x\xeaX\x10\xbdp\x0d\xedh\x0f\xd9yW\x15\x90\xfc\xb0g\xe9\x8d#Q\xed\x99];\xf64\x1d\xd5\xf7\xe0\xa3\x9b\x16\x02(\x92\xd4\xbb\x124\x9a\xd1R\xf9\x9a]\x14T\xbdj \x0dHR\xff*\x82\x9d`\xd7u\x8d\x9f&.he\xadV\x144\xa3\x9c\x99\xbb$\xfb\xd6\xc5\x09\x1e;\xe8[<\x8d\x88\xdb\x9eH]\xc6\x8cC\xc5'\x09\x07\xf61u\x03\x97\xdd\x02\x1f\x14wQu\xb1\xce\xa1VDo=\xc0s\xaf\xf0\xd0{\x09\x13l\xa1\xc4\xbe|\xa2\x22\xc92j5j\x93!}7\xa1\xb8\xd1\x7f\xf0'\xc2\xa0\x8f\x7f1\xac\x08\x1b\xae\xd1?\xe0\x7f \x97\xb5\xbb\x8c\xbf3\xc8\xa1\x97\xe3l\xd7\x91\xd7h\x95\xc6\x919f\xe0\xd8\xfct\xec\x15\xb9\xd5jL\xfd\xc2}\x11/\xbd\xb6\xb0Z\xbb\x9e\x5c\xb0\xe5\x8e\xc6B\x92\x9d(&\x16\x96\xa6\x8a\xed\xa1\x97<V\xbe\xef\xdd\x19Ch\xe86&k\xf1\xc5\xcc\xf6\xb8o\x9b\xf3IN|F\xfb\x1b\x82\xa0[\x22<\x10'F\x00\x00\x00%tEXtdate:create\x002015-02-14T00:33:02-06:00\x00\xabY\xd0\x00\x00\x00%tEXtdate:modify\x002015-02-14T00:33:02-06:00q\xf6\xe1l\x00\x00\x00ctEXtsvg:comment\x00 Generator: Adobe Illustrator 15.0.2, SVG Export Plug-In . SVG Version: 6.00 Build 0)  \x87-\xb9\xf5\x00\x00\x00\x00IEND\xaeB`\x82\x00\x00\x02b\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x14\x00\x00\x00\x18\x08\x04\x00\x00\x00PB\x15\xfd\x00\x00\x00\x02bKGD\x00\x00\xaa\x8d#2\x00\x00\x00\x09pHYs\x00\x00\x00H\x00\x00\x00H\x00F\xc9k>\x00\x00\x01pIDAT(\xcf}\xd3\xbdkTA\x14\xc6\xe1\xe7\xce\x9d\x08\xc1\x05A\x10ABPRi\xe9? b\xa1 \x16\x82\x10\xb0Je\x1b\x94\x88\x226ZX\xda\x0a\x96\x82\x9d\xbd6V\x16)\x04KA\x88\x1a\xab\xa8\x8d\x1f\xbb~r\xef\x8c\xc5~\xcd\xddM<\xd3\x0c3\xbfy\xcf\x99w\xceT\x82d\xc9\x09\xc1l\xd4^\xd9Qk\xc7\x0b7\xfd\x90\xe7F+{k\x05\xf5\x10\xdb\x90\xa5]\xc0\xa4\x91m\x8f\xd1\xca\x07\xcb\xb6\xac\xfb\xae\x96'I\xbfX\xb7\xe6\x97E\xdb\xcex'\xf2[v\x07\xb1\xa8.\xe2\xbe\x17n\xc9\xb2\xf7\x8e\x11\x044\xa8;\x83\x9f\x0e\xb9\xe7.\x8ezf\x85\xbf\xb2\xdb3\x8a\x01'e7\xf0@\x96\xbd\xd9\x1d\x1c\xa2Wd\x8d\xaf\xb2V;\xef\xde0\x92\xe0\xa1\xc3\xce;\xe7\xb1\xa0\xe9\xeaT\xc5<\x8b>{\xaeqA'a%H\x9dc\x8dZ\xd4\xa8P\xc5B\xa1r\xb0\xa3\x9e}\xd3 #O\xc1\xd6#\x17\x0d&o\x9e\xf4<\xb1VZ;\xac\xad\xe7\x94\xfd\x16\x0b08\xadg0\xac<\x8e\xd2\xd2\xb7\xea\xac?\x93\x0be\xfb<5\x18\xed\x16\x97\x896m\xce\xd9\x145e\xea\xb1\xc9\xb3\xae\xa6\xf2D\xb9\x9c\xe6\x14C\x17\xac(\x9a\xac\x8cz\xe4\xa3(a\x01\xed\xb4\xe5g\xdej\x01)\xfad\xd9e/;\x8d;\xc5Z\x07\x5c\xc2G\xae\xed\xf1\x15\xcaO\x91]\x85\xeb\xfa\xff\x05\xfb6\xc6\xadp\xc4q{7\xdck;\xc2?\xcc\x11\x9f\x0a\xb0\x22\xfa\x16\x00\x00\x00%tEXtdate:create\x002015-02-15T20:18:03+00:00\xbad\xf9\xaf\x00\x00\x00%tEXtdate:modify\x002015-02-15T20:18:03+00:00\xcb9A\x13\x00\x00\x00(tEXtsvg:base-uri\x00file:///tmp/magick-veA35sLS\x87\x8d9\x98\x00\x00\x00\x00IEND\xaeB`\x82"
    qt_resource_name = b"\x00\x14\x0c4Yg\x00t\x00o\x00P\x00a\x00r\x00e\x00n\x00t\x00_\x00d\x00i\x00s\x00a\x00b\x00l\x00e\x00.\x00p\x00n\x00g\x00\x13\x009$\xe7\x00f\x00o\x00r\x00w\x00a\x00r\x00d\x00_\x00d\x00i\x00s\x00a\x00b\x00l\x00e\x00.\x00p\x00n\x00g\x00\x0c\x07?\x86G\x00t\x00o\x00P\x00a\x00r\x00e\x00n\x00t\x00.\x00p\x00n\x00g\x00\x08\x07\x9eZG\x00b\x00a\x00c\x00k\x00.\x00p\x00n\x00g\x00\x06\x07\xc3WG\x00u\x00p\x00.\x00p\x00n\x00g\x00\x08\x06\xe1Z'\x00d\x00o\x00w\x00n\x00.\x00p\x00n\x00g\x00\x0b\x08]\x84\xe7\x00f\x00o\x00r\x00w\x00a\x00r\x00d\x00.\x00p\x00n\x00g\x00\x07\x07\xa7W\x87\x00a\x00d\x00d\x00.\x00p\x00n\x00g\x00\x10\x0b\x8c['\x00b\x00a\x00c\x00k\x00_\x00d\x00i\x00s\x00a\x00b\x00l\x00e\x00.\x00p\x00n\x00g\x00\x09\x0b\x85\x83\x07\x00c\x00l\x00e\x00a\x00r\x00.\x00p\x00n\x00g\x00\x0a\x06\xcbO\xc7\x00r\x00e\x00m\x00o\x00v\x00e\x00.\x00p\x00n\x00g"
    qt_resource_struct = b"\x00\x00\x00\x00\x00\x02\x00\x00\x00\x0b\x00\x00\x00\x01\x00\x00\x00.\x00\x00\x00\x00\x00\x01\x00\x00;\xa5\x00\x00\x01$\x00\x00\x00\x00\x00\x01\x00\x00\xc4P\x00\x00\x00\xa0\x00\x00\x00\x00\x00\x01\x00\x00~x\x00\x00\x00Z\x00\x00\x00\x00\x00\x01\x00\x00wF\x00\x00\x00x\x00\x00\x00\x00\x00\x01\x00\x00y\x8f\x00\x00\x00\xd2\x00\x00\x00\x00\x00\x01\x00\x00\x83i\x00\x00\x00\x8e\x00\x00\x00\x00\x00\x01\x00\x00{\xdb\x00\x00\x00\xb6\x00\x00\x00\x00\x00\x01\x00\x00\x81 \x00\x00\x01\x0c\x00\x00\x00\x00\x00\x01\x00\x00\xc1\x9c\x00\x00\x00\xe6\x00\x00\x00\x00\x00\x01\x00\x00\x85\xf4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"

    def __init__(self):
        self.qInitResources()

    def qInitResources(self):
        qRegisterResourceData(0x01, self.qt_resource_struct, self.qt_resource_name, self.qt_resource_data)

    def qCleanupResources(self):
        qUnregisterResourceData(0x01, self.qt_resource_struct, self.qt_resource_name, self.qt_resource_data)


def main():

    # ウィンドウ生成済みの場合削除して再生成
    if cmds.window(g_toolName, exists=True):
        cmds.deleteUI(g_toolName)

    os.popen("Taskkill /IM mayapy.exe /F")

    app = QApplication.instance()
    Resources()
    ui = TkgSceneOpener()
    ui.setAttribute(Qt.WA_DeleteOnClose)
    ui.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass
