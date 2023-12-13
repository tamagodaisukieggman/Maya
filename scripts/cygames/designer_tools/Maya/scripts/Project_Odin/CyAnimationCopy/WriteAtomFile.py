# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------
# WriteAtomFile
#-------------------------------------------------------------------------------------------

import os
import sys
import re

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from PySide.QtCore import QSettings

import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI
import maya.mel as mel

import Ui_WriteAtomFile
reload(Ui_WriteAtomFile)
from Ui_WriteAtomFile import Ui_Dialog

g_version = "0.1.0"
g_toolName = "CyAnimationCopy"
g_subToolName = "WriteAtomFile"
tool_dir = cmds.internalVar(userAppDir=True) + "Cygames/" + g_toolName + "/"

isMayaWindow = False

def get_maya_window():
    from shiboken import wrapInstance
    return wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtGui.QMainWindow)


class WriteAtomFileWindow(QtGui.QDialog):

    settingFilePath = tool_dir + g_toolName + '.ini'

    def __init__(self, parent=None):
        if isMayaWindow:
            super(WriteAtomFileWindow, self).__init__(get_maya_window())
        else:
            super(WriteAtomFileWindow, self).__init__(parent)

        self.parent = parent
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        self.setup()
        self.loadCopyOptions()
        self.readWindowSettings()
        self.setEvent()


    def closeEvent(self, event):
        del self.parent.copyMenuDialog
        self.saveCopyOptions()
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
        self.settings.endGroup()


    def saveCopyOptions(self):
        self.getGuiValue()
        self.settings = QSettings(self.settingFilePath, QSettings.IniFormat)
        self.settings.beginGroup(g_subToolName)
        self.settings.setValue("fileName", self.fileName)
        self.settings.setValue("sdk", self.sdk)
        self.settings.setValue("constraint", self.constraint)
        self.settings.setValue("animLayers", self.animLayers)
        self.settings.setValue("statics", self.statics)
        self.settings.setValue("baked", self.baked)
        self.settings.setValue("selected", self.selected)
        self.settings.setValue("channel", self.channel)
        self.settings.setValue("range", self.selectedRange)
        self.settings.setValue("startTime", self.startTime)
        self.settings.setValue("endTime", self.endTime)
        self.settings.endGroup()


    def getGuiValue(self):
        self.fileName = self.__ui.lineEdit_fileName.text()
        self.sdk=1 if self.__ui.checkBox_sdk.checkState()==QtCore.Qt.CheckState.Checked else 0
        self.constraint=1 if self.__ui.checkBox_constraint.checkState()==QtCore.Qt.CheckState.Checked else 0
        self.animLayers=1 if self.__ui.checkBox_animLayers.checkState()==QtCore.Qt.CheckState.Checked else 0
        self.statics=1 if self.__ui.checkBox_statics.checkState()==QtCore.Qt.CheckState.Checked else 0
        self.baked=1 if self.__ui.checkBox_baked.checkState()==QtCore.Qt.CheckState.Checked else 0
        self.selected = self.__ui.buttonGroup_selected.checkedId()
        self.channel = self.__ui.buttonGroup_channel.checkedId()
        self.selectedRange = self.__ui.buttonGroup_range.checkedId()

        if self.__ui.lineEdit_startTime.text():
            self.startTime = int(self.__ui.lineEdit_startTime.text())

        if self.__ui.lineEdit_endTime.text():
            self.endTime = int(self.__ui.lineEdit_endTime.text())


    def loadCopyOptions(self):
        self.settings = QSettings(self.settingFilePath, QSettings.IniFormat)
        self.settings.beginGroup(g_subToolName)

        scenePath = cmds.file(q=True, sn=True)
        sceneName = os.path.basename(scenePath)
        sceneBaseName, ext = os.path.splitext(sceneName)
        self.fileName = sceneBaseName
        self.__ui.lineEdit_fileName.setText(self.fileName)

        sdk = self.settings.value('sdk')
        if sdk:
            if int(sdk) == 0:
                self.__ui.checkBox_sdk.setCheckState(QtCore.Qt.CheckState.Unchecked)
            else:
                self.__ui.checkBox_sdk.setCheckState(QtCore.Qt.CheckState.Checked)
        
        constraint = self.settings.value('constraint')
        if constraint:
            if int(constraint) == 0:
                self.__ui.checkBox_constraint.setCheckState(QtCore.Qt.CheckState.Unchecked)
            else:
                self.__ui.checkBox_constraint.setCheckState(QtCore.Qt.CheckState.Checked)

        animLayers = self.settings.value('animLayers')
        if animLayers:
            if int(animLayers) == 0:
                self.__ui.checkBox_animLayers.setCheckState(QtCore.Qt.CheckState.Unchecked)
            else:
                self.__ui.checkBox_animLayers.setCheckState(QtCore.Qt.CheckState.Checked)

        statics = self.settings.value('statics')
        if statics:
            if int(statics) == 0:
                self.__ui.checkBox_statics.setCheckState(QtCore.Qt.CheckState.Unchecked)
            else:
                self.__ui.checkBox_statics.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.__ui.checkBox_statics.setCheckState(QtCore.Qt.CheckState.Checked)

        baked = self.settings.value('baked')
        if baked:
            if int(baked) == 0:
                self.__ui.checkBox_baked.setCheckState(QtCore.Qt.CheckState.Unchecked)
            else:
                self.__ui.checkBox_baked.setCheckState(QtCore.Qt.CheckState.Checked)
     
        selected = self.settings.value('selected')
        if selected:
            if int(selected) == -1:
                self.__ui.buttonGroup_selected.button(1).setChecked(True)
            else:
                self.__ui.buttonGroup_selected.button(int(selected)).setChecked(True)
        else:
            self.__ui.buttonGroup_selected.button(1).setChecked(True)

        channel = self.settings.value('channel')
        if channel:
            if int(channel) == -1:
                self.__ui.buttonGroup_channel.button(1).setChecked(True)
            else:
                self.__ui.buttonGroup_channel.button(int(channel)).setChecked(True)
        else:
            self.__ui.buttonGroup_channel.button(1).setChecked(True)

        range = self.settings.value('range')
        if range:
            if int(range) == -1:
                self.__ui.buttonGroup_range.button(1).setChecked(True)
            else:
                self.__ui.buttonGroup_range.button(int(range)).setChecked(True)
        else:
            self.__ui.buttonGroup_range.button(1).setChecked(True)

        self.changeTimeRangeState()

        # startTimeは現在のフレームを設定
        self.startTime = str(int((cmds.currentTime(q=True))))
        self.__ui.lineEdit_startTime.setText(self.startTime);

        # startTimeはタイムスライダのmaxを設定
        self.endTime = str(int((cmds.playbackOptions(q=True,max=True))))
        self.__ui.lineEdit_endTime.setText(self.endTime);
        
        self.settings.endGroup()


    def setup(self):
        self.setWindowTitle(u"アニメーションのコピー")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.__ui.lineEdit_startTime.setValidator(QtGui.QIntValidator(0, 99999, self));
        self.__ui.lineEdit_endTime.setValidator(QtGui.QIntValidator(0, 99999, self));
        self.__ui.buttonGroup_selected.setId(self.__ui.radioButton_selectedOnly,0)
        self.__ui.buttonGroup_selected.setId(self.__ui.radioButton_childrenToo,1)
        self.__ui.buttonGroup_channel.setId(self.__ui.radioButton_allKey,1)
        self.__ui.buttonGroup_channel.setId(self.__ui.radioButton_fromChannelBox,2)
        self.__ui.buttonGroup_range.setId(self.__ui.radioButton_range_timeSlider,0)
        self.__ui.buttonGroup_range.setId(self.__ui.radioButton_range_all,1)
        self.__ui.buttonGroup_range.setId(self.__ui.radioButton_range_oneFrame,2)
        self.__ui.buttonGroup_range.setId(self.__ui.radioButton_range_startEnd,3)

    def setEvent(self):
        QtCore.QObject.connect(self.__ui.pushButton_currentTime, QtCore.SIGNAL("clicked()"), self.setCurrentFrame)
        QtCore.QObject.connect(self.__ui.pushButton_applyAndClose, QtCore.SIGNAL("clicked()"), self.pushButton_applyAndClose_clicked)
        QtCore.QObject.connect(self.__ui.pushButton_apply, QtCore.SIGNAL("clicked()"), self.pushButton_apply_clicked)
        QtCore.QObject.connect(self.__ui.pushButton_close, QtCore.SIGNAL("clicked()"), self.pushButton_close_clicked)
        QtCore.QObject.connect(self.__ui.radioButton_range_timeSlider, QtCore.SIGNAL("clicked()"), self.changeTimeRangeState)
        QtCore.QObject.connect(self.__ui.radioButton_range_all, QtCore.SIGNAL("clicked()"), self.changeTimeRangeState)
        QtCore.QObject.connect(self.__ui.radioButton_range_oneFrame, QtCore.SIGNAL("clicked()"), self.changeTimeRangeState)
        QtCore.QObject.connect(self.__ui.radioButton_range_startEnd, QtCore.SIGNAL("clicked()"), self.changeTimeRangeState)

    def setCurrentFrame(self):
        currentTime = int(cmds.currentTime(q=True))
        self.__ui.lineEdit_startTime.setText(str(currentTime))

    def pushButton_applyAndClose_clicked(self):
        self.writeAtomFile()
        self.saveCopyOptions()
        self.writeWindowSettings()
        self.done(0)


    def pushButton_apply_clicked(self):
        self.writeAtomFile()


    def pushButton_close_clicked(self):
        self.saveCopyOptions()
        self.writeWindowSettings()
        self.done(0)


    def changeTimeRangeState(self):
        if self.__ui.radioButton_range_startEnd.isChecked():
            self.__ui.label_startTime.setEnabled(True)
            self.__ui.lineEdit_startTime.setEnabled(True)
            self.__ui.label_endTime.setEnabled(True)
            self.__ui.lineEdit_endTime.setEnabled(True)
        elif self.__ui.radioButton_range_oneFrame.isChecked():
            self.__ui.label_startTime.setEnabled(True)
            self.__ui.lineEdit_startTime.setEnabled(True)
            self.__ui.label_endTime.setEnabled(False)
            self.__ui.lineEdit_endTime.setEnabled(False)
        else:
            self.__ui.label_startTime.setEnabled(False)
            self.__ui.lineEdit_startTime.setEnabled(False)
            self.__ui.label_endTime.setEnabled(False)
            self.__ui.lineEdit_endTime.setEnabled(False)


    def writeAtomFile(self):
        if cmds.pluginInfo('atomImportExport', query=True, loaded=True) == False:
            cmds.loadPlugin('atomImportExport')
        self.getGuiValue()
        self.filePath = cmds.internalVar(userAppDir=True) + "Cygames/CyAnimationCopy/Atom/" + self.fileName +".atom"

        selected = "childrenToo" if int(self.selected) == 1 else "selectedOnly"

        range_min, range_max, whitchRange, addtionalOptions = self.generateRangeOptions(self.selectedRange, self.startTime, self.endTime)

        self.options = "precision=8;statics=" + str(self.statics) + ";baked="+ str(self.baked) +";sdk="+str(self.sdk)+";constraint="+str(self.constraint)+";animLayers="+str(self.animLayers)+";selected="+str(selected)+";whichRange="+str(whitchRange)+";range="+str(range_min)+":"+str(range_max)+";hierarchy=none;controlPoints=0;useChannelBox="+str(self.channel)+";options=keys;" + addtionalOptions
        
        tempNamespace = "CyAnimanitonCopy"
        if not cmds.namespace(exists=tempNamespace):
           cmds.namespace(add=tempNamespace)
        cmds.namespace(set=tempNamespace)

        userSelected = cmds.ls(sl=True, l=True)
        cmds.duplicate(rr=True, un=True)
        cmds.namespace(set=':')
        
        userTime = cmds.currentTime(q=True)
        cmds.select(hierarchy=True)
        cmds.currentTime(range_min)
        mel.eval('HoldCurrentKeys')
        cmds.currentTime(range_max)
        mel.eval('HoldCurrentKeys')

        try:
            cmds.file(self.filePath, es=True, force=True, options=self.options, type="atomExport");
        except:
            pass

        print self.options

        cmds.delete()
        cmds.select(userSelected)
        cmds.currentTime(userTime)

        self.replaceFileText(self.filePath, tempNamespace + ":", "")


    def generateRangeOptions(self, selectedRange, startTime, endTime):
        slider_min = cmds.playbackOptions(q=True,min=True)
        slider_max = cmds.playbackOptions(q=True,max=True)
        if startTime < slider_min: startTime = slider_min
        if endTime > slider_max: endTime = slider_max
        if selectedRange == 0:
            range_min = slider_min
            range_max = slider_max
            whitchRange = 2
        elif selectedRange == 1:
            range_min = slider_min
            range_max = slider_max
            whitchRange = 1
        elif selectedRange == 2:
            range_min = startTime
            range_max = startTime
            whitchRange = 2
        else:
            range_min = startTime
            range_max = endTime
            whitchRange = 2
        
        if whitchRange == 2:
            addtionalOptions = "copyKeyCmd=-animation objects -time >"+str(range_min)+":"+str(range_max)+"> -float >"+str(range_min)+":"+str(range_max)+"> -option keys -hierarchy none -controlPoints 0 "
        else:
            addtionalOptions = ""
        
        return [range_min, range_max, whitchRange, addtionalOptions]

    def replaceFileText(self, file_path, search, replace):
        temp_path = os.path.dirname(file_path) + "/temp"
    
        try:
            f = open(file_path, "r")
            temp = open(temp_path, "w")
            for line in f:
                if line.find(search) != -1:
                    line = re.sub(search, replace, line)
                temp.write(line)
        finally:
            f.close()
            temp.close()
        
        if os.path.exists(file_path) and os.path.exists(temp_path):
            os.remove(file_path)
            os.rename(temp_path, file_path)


def main():
    global isMayaWindow
    isMayaWindow = True
    app = QtGui.QApplication.instance()
    if cmds.window(g_toolName, exists=True):
       cmds.setFocus(g_toolName)
       return

    ui = WriteAtomFileWindow();
    ui.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    ui.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = WriteAtomFileWindow()
    ui.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    ui.show()
    sys.exit(app.exec_())
