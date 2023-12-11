#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# PasteAtomFile.py
#

import os
import sys
import re

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from PySide.QtCore import QSettings

import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI

import Ui_PasteAtomFile
reload(Ui_PasteAtomFile)
from Ui_PasteAtomFile import Ui_Dialog

g_toolName = "CyAnimationCopy"
g_subToolName = "PasteAtomFile"
tool_dir = cmds.internalVar(userAppDir=True) + "Cygames/" + g_toolName + "/"

class PasteAtomFile(QtGui.QDialog):
    settingFilePath = tool_dir + g_toolName + '.ini'

    def __init__(self, parent=None, atomFile=None):
        super(PasteAtomFile, self).__init__(parent)

        self.parent = parent
        self.atomFile = atomFile;
        self.copyList = []

        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)

        self.setup()

        self.readWindowSettings()

    def closeEvent(self, event):
        del self.parent.pasteMenuDialog
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
        self.settings.beginGroup(g_subToolName)
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("maximized", self.isMaximized())
        if self.isMaximized() == True:
            self.settings.setValue("pos", self.wpos)
            self.settings.setValue("size", self.wsize)
        self.settings.setValue("splitterSizes", self.__ui.splitter.saveState())
        self.settings.setValue("atomFileViewHeaderSizes", self.__ui.treeWidget_atomFileView.header().saveState())
        if self.__ui.radioButton_fromCurrentTime.isChecked():
            self.settings.setValue("pasteTimeRange", 1)
        elif self.__ui.radioButton_timeSlider.isChecked():
            self.settings.setValue("pasteTimeRange", 2)
        else:
            self.settings.setValue("pasteTimeRange", 3)
        
        self.settings.endGroup()

    def readWindowSettings(self):
        self.settings = QSettings(self.settingFilePath, QSettings.IniFormat)
        self.settings.beginGroup(g_subToolName)
        geometry = self.settings.value('geometry')
        if geometry is not None:
            self.restoreGeometry(geometry)
        isMaximized = self.settings.value('maximized')
        if isMaximized == "true":
            self.move(self.settings.value("pos", self.pos()))
            self.resize(self.settings.value("size", self.size()))
            self.wpos = self.pos()
            self.wsize = self.size()
            self.showMaximized()
        splitterSizes = self.settings.value('splitterSizes')
        if splitterSizes is not None:
            self.__ui.splitter.restoreState(splitterSizes)
        atomFileViewSizes = self.settings.value('atomFileViewHeaderSizes')
        if atomFileViewSizes is not None:
            self.__ui.treeWidget_atomFileView.header().restoreState(atomFileViewSizes)

        pasteTimeRange = self.settings.value('pasteTimeRange')
        if pasteTimeRange is not None:
            if pasteTimeRange == '1':
                self.__ui.radioButton_fromCurrentTime.setChecked(True)
            elif pasteTimeRange == '2':
                self.__ui.radioButton_timeSlider.setChecked(True)
            else:
                self.__ui.radioButton_fromFile.setChecked(True)
        else:
            self.__ui.radioButton_fromFile.setChecked(True)
        self.settings.endGroup()

    def setup(self):
        #self.setModal(True)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setSignal()

    def setSignal(self):
        QtCore.QObject.connect(self.__ui.pushButton_clearCheckBox, QtCore.SIGNAL("clicked()"), self.clearCheckBox)
        QtCore.QObject.connect(self.__ui.pushButton_checkAllCheckBox, QtCore.SIGNAL("clicked()"), self.checkAllCheckBox)
        QtCore.QObject.connect(self.__ui.pushButton_pasteAnimation, QtCore.SIGNAL("clicked()"), self.copyAnimation)

    def changeCurrentItem(self, item):
        self.__ui.treeWidget_atomFileView._setCurrentItem(item)
        self.__ui.treeWidget_destinationView._setCurrentItem(item)

    def copyAnimation(self):
        if cmds.pluginInfo('atomImportExport', query=True, loaded=True) == False:
            cmds.loadPlugin('atomImportExport')
        cmds.select(self.__ui.treeWidget_destinationView.root)
        editedAtomFile = self.__ui.treeWidget_atomFileView.writeMapFile()
        cmds.file(editedAtomFile, i=True, type="atomImport", ra=True, namespace="atom", options=";;targetTime="+self.getTimeRangeOption()+";option=replace;match=string;;selected=childrenToo;search=;replace=;prefix=;suffix=;mapFile=;")

    def getTimeRangeOption(self):
        if self.__ui.radioButton_fromCurrentTime.isChecked():
            currentTime = cmds.currentTime(q=True);
            timeRangeOption = "2;time="+str(currentTime)+":"+str(currentTime+2)
            
        elif self.__ui.radioButton_timeSlider.isChecked():
            startTime = cmds.playbackOptions(q=True,min=True)
            endTime = cmds.playbackOptions(q=True,max=True)
            timeRangeOption = "2;time="+str(startTime)+":"+str(endTime)
        else:
            timeRangeOption = "3"
        return timeRangeOption

    def clearCheckBox(self):
        self.__ui.treeWidget_atomFileView.clearCheckBox()

    def checkAllCheckBox(self):
        self.__ui.treeWidget_atomFileView.checkAllCheckBox()
