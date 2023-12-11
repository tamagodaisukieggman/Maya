#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# CyAnimationCopy.py
#

import os
import sys
import re

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from PySide.QtCore import QSettings

import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI

import Ui_CyAnimationCopy
reload(Ui_CyAnimationCopy)
from Ui_CyAnimationCopy import Ui_MainWindow

import WriteAtomFile
reload(WriteAtomFile)
from WriteAtomFile import WriteAtomFileWindow

import PasteAtomFile
reload(PasteAtomFile)
from PasteAtomFile import PasteAtomFile

g_version = "0.1.0"
g_toolName = "CyAnimationCopy"
tool_dir = cmds.internalVar(userAppDir=True) + "Cygames/" + g_toolName + "/"

isMayaWindow = False

def get_maya_window():
    from shiboken import wrapInstance
    return wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtGui.QMainWindow)

class MainWindow(QtGui.QMainWindow):

    settingFilePath =  tool_dir = cmds.internalVar(userAppDir=True) + "Cygames/" + g_toolName + "/" + g_toolName + '.ini'

    def __init__(self, parent=None):
        if isMayaWindow:
            super(MainWindow, self).__init__(get_maya_window())
        else:
            super(MainWindow, self).__init__(parent)
        self.parent = parent
        self.setup()

    def setup(self):
        self.defaultPath = cmds.internalVar(userAppDir=True) + "Cygames/CyAnimationCopy/Atom/"
        if not os.path.exists(self.defaultPath):
            os.makedirs(self.defaultPath)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__ui.lineEdit_atomFilePath.setText(self.defaultPath)
        self.__ui.lineEdit_atomFilePath.setReadOnly(True)
        self.__ui.treeView_atomFile.setRootPath(self.defaultPath)
        self.readWindowSettings()
        self.setEvent()

    def setEvent(self):  
        QtCore.QObject.connect(self.__ui.toolButton_copy, QtCore.SIGNAL("clicked()"), self.openWriteDialog)
        QtCore.QObject.connect(self.__ui.toolButton_paste, QtCore.SIGNAL("clicked()"), self.openPasteDialog)
        QtCore.QObject.connect(self.__ui.toolButton_rename, QtCore.SIGNAL("clicked()"), self.renameFile)
        QtCore.QObject.connect(self.__ui.toolButton_remove, QtCore.SIGNAL("clicked()"), self.removeFile)
        self.__ui.treeView_atomFile.clicked[QtCore.QModelIndex].connect(self.setAtomFileInfo)
        self.__ui.treeView_atomFile.doubleClicked[QtCore.QModelIndex].connect(self.openPasteDialog)

    def openWriteDialog(self):
        root = cmds.ls(sl=True)
        if root:
            try:
                self.copyMenuDialog
            except:
                self.copyMenuDialog = WriteAtomFileWindow(self)
                self.copyMenuDialog.show()
        else:
            QtGui.QMessageBox.warning(self, u"警告", u"コピー元のルートノードを選択してください。")


    def openPasteDialog(self):
        selectedAtomFilePath = self.__ui.treeView_atomFile.getCurrentPath()
        if selectedAtomFilePath:
            root = cmds.ls(sl=True)
            if root:
                try:
                    self.pasteMenuDialog
                except:
                    self.pasteMenuDialog = PasteAtomFile(self, selectedAtomFilePath)
                    self.pasteMenuDialog.show()
            else:
                QtGui.QMessageBox.warning(self, u"警告", u"ペースト先のルートノードを選択してください。")
        else:
            QtGui.QMessageBox.warning(self, u"警告", u"コピーするアニメーションをリストから選択してください。")

    def renameFile(self):
        filePath = self.__ui.treeView_atomFile.getCurrentPath()
        if os.path.exists(filePath):
            dirPath = os.path.dirname(filePath)
            fileName, fileExt = os.path.splitext(os.path.basename(filePath))
            newFileName = QtGui.QInputDialog.getText(self, u"名前の変更", u"新しいファイル名を入力してください。                  ", 
                                                        QtGui.QLineEdit.Normal, fileName)
            if newFileName[0]:
                if not re.match(r"^.*[\\\/\:\,\;\*\?\"\<\>\|].*", newFileName[0]):
                    newFilePath = dirPath + "/" + newFileName[0] + fileExt
                    if filePath != newFilePath:
                        if not os.path.exists(newFilePath):
                            os.rename(filePath, newFilePath)
                            self.__ui.treeView_atomFile.setCurrentPath(newFilePath)
                        else:
                            QtGui.QMessageBox.critical(self, u"名前の変更", u"この場所には同じ名前のファイルがすでにあります。")
                else:
                    QtGui.QMessageBox.critical(self, u"名前の変更", u"ファイル名には次の文字は使えません。\n \ / : , ; * ? \" < > |")


    def removeFile(self):
        filePath = self.__ui.treeView_atomFile.getCurrentPath()
        fileName, fileExt = os.path.splitext(os.path.basename(filePath))
        reply = QtGui.QMessageBox.question(self, u"ファイルの削除", fileName + u" を削除してよろしいですか？",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            if os.path.exists(filePath):
                os.remove(filePath)
                self.__ui.textEdit_atomFileInfo.clear()
            else:
                QtGui.QMessageBox.critical(self, u"ファイルの削除", fileName + u" が見つかりません。")

    def setAtomFileInfo(self):
        filePath = self.__ui.treeView_atomFile.getCurrentPath()
        self.__ui.textEdit_atomFileInfo.setAtomFileInfo(filePath)

    def closeEvent(self, event):
        self.writeWindowSettings()

    def resizeEvent(self, event):
        self.storeWindowGeomery()

    def moveEvent(self, event):
        self.storeWindowGeomery()

    def storeWindowGeomery(self):
        if self.isMaximized() == False:
            self.wpos = self.pos()
            self.wsize = self.size()

    def writeWindowSettings(self):
        self.settings = QSettings(self.settingFilePath, QSettings.IniFormat)
        self.settings.beginGroup(g_toolName)
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("state", self.saveState())
        self.settings.setValue( "maximized", self.isMaximized())
        if self.isMaximized() == True:
            self.settings.setValue("pos", self.wpos)
            self.settings.setValue("size", self.wsize)
        self.settings.setValue("treeView_atomFileHeaderState", self.__ui.treeView_atomFile.header().saveState())
        self.settings.endGroup()

    def readWindowSettings(self):
        self.settings = QSettings(self.settingFilePath, QSettings.IniFormat)
        self.settings.beginGroup(g_toolName)
        state = self.settings.value('state')
        if state is not None:
            self.restoreState(state)
        geometry = self.settings.value('geometry')
        if geometry is not None:
            self.restoreGeometry(geometry)
        isMaximized = self.settings.value('maximized')
        if isMaximized == "true":
            self.move(self.settings.value( "pos", self.pos()))
            self.resize(self.settings.value( "size", self.size()))
            self.wpos = self.pos()
            self.wsize = self.size()
            self.showMaximized()
        treeView_atomFileHeaderState = self.settings.value('treeView_atomFileHeaderState')
        if treeView_atomFileHeaderState is not None:
            self.__ui.treeView_atomFile.header().restoreState(treeView_atomFileHeaderState)
        self.settings.endGroup()

def main():
    global isMayaWindow
    isMayaWindow = True
    app = QtGui.QApplication.instance()
    if cmds.window(g_toolName, exists=True):
       cmds.setFocus(g_toolName)
       return

    ui = MainWindow();
    ui.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    ui.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    ui.show()

    sys.exit(app.exec_())
