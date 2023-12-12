# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import OrderedDict
import os
from functools import partial

import importlib
import webbrowser

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

import maya.cmds as cmds

import tool_log

from . import command
from . import TITLE
from . import tool_version


# from ...utils.hda_loader import houdini_util
import shr.utils.hda_loader.houdini_util as houdini_util
importlib.reload(houdini_util)

CLASS_NAME = "".join(TITLE.split())


# 開発中はTrue、リリース時にFalse
DEV_MODE = False

if DEV_MODE:
    importlib.reload(command)

UI_FILE = r"C:\cygames\shrdev\shr\tools\in\ext\maya\2022\modules\shr\scripts\shr\model\lod_create\lod_create.ui"

_suffix = "_lod_create"


class Slider(QtWidgets.QSlider):
    def __init__(self, *args, **kwargs):
        super(Slider, self).__init__(*args, **kwargs)

        self.sliderPressed.connect(self.dragStart)
        self.sliderReleased.connect(self.dragEnd)

    def dragStart(self):
        cmds.undoInfo(openChunk=True)

    def dragEnd(self):
        cmds.undoInfo(closeChunk=True)


class DoubleSlider(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(float)
    _value = 0.0

    def __init__(self, *args, **kwargs):
        super(DoubleSlider, self).__init__(*args, **kwargs)
        self.material = None
        self.attr = None

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.__doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.__doubleSpinBox.setMinimumWidth(50)

        self.__doubleSpinBox.setSingleStep(0.01)
        self.__doubleSpinBox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons)
        layout.addWidget(self.__doubleSpinBox)

        self.__percent_label = QtWidgets.QLabel("%")
        self.__percent_label.setMinimumWidth(20)
        layout.addWidget(self.__percent_label)

        self.__slider = Slider(QtCore.Qt.Horizontal, self)
        self.__updateSliderRange()
        layout.addWidget(self.__slider)

        self.__label = QtWidgets.QLabel("")
        self.__label.setMinimumWidth(60)
        self.__label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.__label)

        self.__label_ply = QtWidgets.QLabel("poly")
        self.__label_ply.setMinimumWidth(30)
        layout.addWidget(self.__label_ply)

        self.__doubleSpinBox.valueChanged[float].connect(
            self.valueChangedCallback)
        self.__slider.valueChanged[int].connect(self.valueChangedCallback)

        self.hda = None
        self.attr = None

    def setPolyCount(self, num):
        self.__label.setText("{}".format(num))

    def setEnable(self, flag):
        self.__doubleSpinBox.setEnabled(flag)
        self.__slider.setEnabled(flag)

    def setHDA(self, hda, attr):
        self.hda = hda
        self.attr = attr

    def attributeValueChange(self, value):
        if not self.hda:
            return
        if not cmds.objExists(self.hda):
            return
        if not cmds.attributeQuery(self.attr, n=self.hda, ex=True):
            return
        cmds.setAttr(self.hda + "." + self.attr, value)

    def valueChangedCallback(self, value):
        sender = self.sender()
        if sender == self.__doubleSpinBox:
            self.__slider.blockSignals(True)
            self.__slider.setValue(value*self.__boost)
            self.__slider.blockSignals(False)

        elif sender == self.__slider:
            value = float(value)/self.__boost
            self.__doubleSpinBox.blockSignals(True)
            self.__doubleSpinBox.setValue(value)
            self.__doubleSpinBox.blockSignals(False)
        self._value = value
        self.valueChanged.emit(value)
        self.attributeValueChange(value)
        # command.sync_asset(self.hda, sync_output=True)

    def value(self):
        return self.__doubleSpinBox.value()

    def setValue(self, value):
        self.__doubleSpinBox.setValue(value)

    def setRange(self, min, max):
        self.__doubleSpinBox.setRange(min, max)
        self.__updateSliderRange()

    def setDecimals(self, prec):
        self.__doubleSpinBox.setDecimals(prec)
        self.__updateSliderRange()

    def __updateSliderRange(self):
        decimals = self.__doubleSpinBox.decimals()
        minimum = round(self.__doubleSpinBox.minimum())
        maximum = round(self.__doubleSpinBox.maximum())
        self.__boost = int('1'+('0'*decimals))
        self.__slider.setRange(minimum*self.__boost, maximum*self.__boost)


class LODCreateTool(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    UI = None
    valueChanged = QtCore.Signal(float)
    project_lod_max = 7
    _rebuild_flag = True

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.current_hda = None
        self.current_hdas = None

        self.threshold = None
        self.add = None
        self.lod_num = None
        self.view_align = None
        self.preservequads = None
        self.equalize_lengths = None
        self.lods_percent = OrderedDict()

        self._lodBox = OrderedDict()
        self._lodSlider = OrderedDict()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        loader = QUiLoader()

        uiFilePath = UI_FILE.replace(os.sep, '/')
        self.UI = loader.load(uiFilePath)

        _icon = self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton)
        openAct = QtWidgets.QAction('Open Help Site ...', self)
        openAct.triggered.connect(self.openHelp)

        menuBar = self.menuBar()
        menu = menuBar.addMenu('Help')
        menu.addAction(openAct)

        self.UI.viewAlignCheckBox.stateChanged.connect(self.alignLods)
        self.UI.QuadCheckBox.stateChanged.connect(self.quadPolygon)
        self.UI.equalizeLengthCheckBox.stateChanged.connect(
            self.equalizeLength)

        self.UI.lodNumSpinBox.valueChanged[int].connect(self.numLodValueChange)
        self.UI.thresholdSpinBox.valueChanged[float].connect(
            self.thresholdValueChange)
        self.UI.thresholdAddSpinBox.valueChanged[float].connect(
            self.thresholdAddValueChange)

        self.UI.createLodFromSelectionButton.clicked.connect(
            partial(self.createLod))
        self.UI.checkPolyCountButton.clicked.connect(
            partial(self.checkPolygonCount))
        self.UI.createLodButton.clicked.connect(partial(self.bakeAsset))

        self.UI.selectHDAConboBox.currentIndexChanged.connect(
            partial(self.chengeHDAConboBox))

        self.buildLodBoxLayout()
        self.resize(430, 500)
        self.setWindowTitle(TITLE)
        self.setCentralWidget(self.UI)

        self._setWindowSize()
        self.getSceneHdas()

        if not DEV_MODE:
            self._send_log()

        cmds.scriptJob(event=("deleteAll", self.getSceneHdas),
                       parent=self.objectName())
        cmds.scriptJob(event=("SceneOpened", self.getSceneHdas),
                       parent=self.objectName())
        cmds.scriptJob(event=("SelectionChanged", self.buildHdaConboBox),
                       parent=self.objectName())

    def _send_log(self):
        logger = tool_log.get_logger(tool_title=TITLE, tool_version=tool_version)
        logger.send_launch("")


    def _setWindowSize(self):
        """ウィンドウサイズの設定保存
        """
        self.settingFileName = f'{self.__class__.__name__}.ini'
        filename = os.path.join(os.getenv('MAYA_APP_DIR'),
                                'shenron_tool_settings',
                                self.settingFileName)
        self._settings = QtCore.QSettings(filename, QtCore.QSettings.IniFormat)

    def restore(self):
        """ウィンドウサイズのリストア
        """
        self.restoreGeometry(self._settings.value(f'{self.__class__.__name__}geometry'))

    def show(self):
        """ウィンドウサイズを戻すためにオーバーライド
        """
        self.restore()
        super(self.__class__, self).show()

    def closeEvent(self, event):
        """ツールウィンドウを閉じたときの動作
        ウィンドウサイズ保存
        fileInfo にデータ書き込み
        ファイルパスとスライダ情報
        """
        super(self.__class__, self).closeEvent(event)
        self._settings.setValue(f'{self.__class__.__name__}geometry', self.saveGeometry())

    def openHelp(self):
        _web_site = "https://wisdom.cygames.jp/pages/viewpage.action?pageId=284836889"
        webbrowser.open(_web_site)

    def getCurrentHDA(self, hda_name=None):
        _current_hda = None
        if not hda_name:
            _current_hda = self.UI.selectHDAConboBox.currentText()
            if cmds.objExists(_current_hda):
                _current_hda = _current_hda
            else:
                _current_hda = None
        else:
            _current_hda = cmds.ls(hda_name, long=True)
            if _current_hda:
                _current_hda = _current_hda[0]
            else:
                _current_hda = None
        self.current_hda = _current_hda

    def checkPolygonCount(self, *args):
        self.getCurrentHDA()

        if not self.current_hda:
            return

        command.delete_sets()
        command.sync_asset(self.current_hda, sync_output=True)
        _sets = command.get_lod_sets()

        if not _sets:
            return

        for lod_num in range(1, self.project_lod_max + 1):
            self.polyCount(lod_num)

    def polyCount(self, lod_num):
        current_set = command.get_lod_set(lod_num)
        _slider = self._lodSlider.get(int(lod_num))
        if current_set:
            _count = current_set[0].split("_", 1)[-1]
        else:
            _count = 0
        _slider.setPolyCount(_count)

    def chengeHDAConboBox(self, *args):
        self.getCurrentHDA()
        if not self.current_hda:
            return

        if self.getHoudiniParameters():
            self.setHoudiniParameters()

            command.delete_sets()
            command.sync_asset(self.current_hda, sync_output=True)
            self.setLodBox()

    def bakeAsset(self, *args):
        self.getCurrentHDA()
        if not self.current_hda:
            return
        lod_num = self.UI.lodNumSpinBox.value()
        remove_lod = self.UI.removeLODcheckBox.isChecked()

        command.delete_sets()
        _attr = self.current_hda + ".houdiniAssetParm_view_align"
        _value = cmds.getAttr(_attr)
        cmds.setAttr(_attr, False)
        command.bake_asset(hda_name=self.current_hda, lod_num=lod_num, remove_lod=remove_lod)
        cmds.setAttr(_attr, _value)
        cmds.setAttr(f'{self.current_hda}.visibility', 0)

    def equalizeLength(self, *args):
        if not self.current_hda:
            return
        value = self.UI.equalizeLengthCheckBox.isChecked()
        attr = "houdiniAssetParm_equalize_lengths"
        if not cmds.attributeQuery(attr, n=self.current_hda, ex=True):
            return
        cmds.setAttr(f'{self.current_hda}.visibility', 1)
        cmds.setAttr(self.current_hda + ".{}".format(attr), value)
        command.sync_asset(self.current_hda, sync_output=True)

    def quadPolygon(self, *args):
        if not self.current_hda:
            return
        value = self.UI.QuadCheckBox.isChecked()
        attr = "houdiniAssetParm_preservequads"
        if not cmds.attributeQuery(attr, n=self.current_hda, ex=True):
            return
        cmds.setAttr(f'{self.current_hda}.visibility', 1)
        cmds.setAttr(self.current_hda + ".{}".format(attr), value)
        command.sync_asset(self.current_hda, sync_output=True)

    def alignLods(self, state):
        if not self.current_hda:
            return
        value = self.UI.viewAlignCheckBox.isChecked()
        attr = "houdiniAssetParm_view_align"
        if not cmds.attributeQuery(attr, n=self.current_hda, ex=True):
            return
        cmds.setAttr(f'{self.current_hda}.visibility', 1)
        cmds.setAttr(self.current_hda + ".{}".format(attr), value)
        command.sync_asset(self.current_hda, sync_output=True)

    def numLodValueChange(self, value):
        if not self.current_hda:
            return
        attr = "houdiniAssetParm_lod_num"
        if not cmds.attributeQuery(attr, n=self.current_hda, ex=True):
            return
        cmds.setAttr(f'{self.current_hda}.visibility', 1)
        cmds.setAttr(self.current_hda + ".{}".format(attr), value)
        command.sync_asset(self.current_hda, sync_output=True)
        self.setLodBox()

    def thresholdAddValueChange(self, value):
        if not self.current_hda:
            return
        attr = "houdiniAssetParm_add"
        if not cmds.attributeQuery(attr, n=self.current_hda, ex=True):
            return
        cmds.setAttr(self.current_hda + ".{}".format(attr), value)
        # command.sync_asset(self.current_hda, sync_output=True)

    def thresholdValueChange(self, value):
        if not self.current_hda:
            return
        attr = "houdiniAssetParm_threshold"
        if not cmds.attributeQuery(attr, n=self.current_hda, ex=True):
            return
        cmds.setAttr(self.current_hda + ".{}".format(attr), value)
        # command.sync_asset(self.current_hda, sync_output=True)

    def getSceneHdas(self, *args):
        self.current_hdas = command.get_scene_lod_create_hdas(_suffix)
        if self.current_hdas:
            self.getCurrentHDA()
            self.buildHdaConboBox()
            if self.getHoudiniParameters():
                self.setHoudiniParameters()
        else:
            self.resetSettings()
        self.setLodBox()

    def buildHdaConboBox(self, current_selection=None):

        if not current_selection:
            current_selection = self.UI.selectHDAConboBox.currentText()
        self.UI.selectHDAConboBox.clear()

        if self.current_hdas:
            for _hda in self.current_hdas:
                if cmds.objExists(_hda):
                    self.UI.selectHDAConboBox.addItem(_hda)

            if current_selection in self.current_hdas:
                self.UI.selectHDAConboBox.setCurrentText(current_selection)

    def resetSettings(self):
        self.buildHdaConboBox()

        self.UI.viewAlignCheckBox.setChecked(False)
        self.UI.QuadCheckBox.setChecked(False)
        self.UI.equalizeLengthCheckBox.setChecked(False)

        self.UI.thresholdAddSpinBox.setValue(0)
        self.UI.thresholdAddSpinBox.setValue(0)
        self.UI.lodNumSpinBox.setValue(4)

        command.delete_sets()

        for i in range(1, self.project_lod_max + 1):
            _slider = self._lodSlider.get(i)
            if _slider:
                _slider.setPolyCount(0)

    def getHoudiniParameters(self):
        if not self.current_hda:
            return

        _attr = self.current_hda + ".houdiniAssetParm_threshold"
        self.threshold = cmds.getAttr(_attr)

        _attr = self.current_hda + ".houdiniAssetParm_add"
        self.add = cmds.getAttr(_attr)

        _attr = self.current_hda + ".houdiniAssetParm_lod_num"
        self.lod_num = cmds.getAttr(_attr)

        _attr = self.current_hda + ".houdiniAssetParm_view_align"
        self.view_align = cmds.getAttr(_attr)
        self.UI.viewAlignCheckBox.setChecked(self.view_align)

        _attr = self.current_hda + ".houdiniAssetParm_preservequads"
        self.preservequads = cmds.getAttr(_attr)
        self.UI.QuadCheckBox.setChecked(self.preservequads)

        _attr = self.current_hda + ".houdiniAssetParm_equalize_lengths"
        self.equalize_lengths = cmds.getAttr(_attr)
        self.UI.equalizeLengthCheckBox.setChecked(self.equalize_lengths)
        return True

    def setHoudiniParameters(self):
        self.UI.lodNumSpinBox.setValue(self.lod_num)
        self.UI.QuadCheckBox.setChecked(self.preservequads)
        self.UI.equalizeLengthCheckBox.setChecked(self.equalize_lengths)
        self.UI.thresholdSpinBox.setValue(self.threshold)
        self.UI.thresholdAddSpinBox.setValue(self.add)

    def buildLodBoxLayout(self):
        value = self.UI.lodNumSpinBox.value()
        self._rebuild_flag = False
        self._lodBox = OrderedDict()
        self._lodSlider = OrderedDict()
        _target = self.UI.lodBoxLayouts

        for lod_num in range(1, self.project_lod_max + 1):
            _box = QtWidgets.QGroupBox()
            _box.setTitle("LOD{}".format(lod_num))
            layout = QtWidgets.QVBoxLayout()
            layout.setContentsMargins(1, 1, 1, 1)
            layout.setSpacing(3)

            _percentage_slider = DoubleSlider()
            _percentage_slider.setRange(0.0, 100.0)
            _percentage_slider.setDecimals(2)

            self._lodBox[lod_num] = _box
            self._lodSlider[lod_num] = _percentage_slider

            if lod_num < value:
                _percentage_slider.setEnable(True)

                _box.setEnabled(True)
            else:
                _percentage_slider.setEnable(False)
                _box.setEnabled(False)

            layout.addWidget(_percentage_slider)

            _box.setLayout(layout)
            _target.addWidget(_box)

        verticalSpacer = QtWidgets.QSpacerItem(20, 40,
                                               QtWidgets.QSizePolicy.Minimum,
                                               QtWidgets.QSizePolicy.Expanding)

        _target.addItem(verticalSpacer)

    def setLodBox(self):
        if not self.current_hda:
            return
        value = self.UI.lodNumSpinBox.value()
        for lod_num in range(1, self.project_lod_max + 1):
            _attr = ""
            lod_parcent = 0
            if self.current_hda and cmds.objExists(self.current_hda):
                _attr = self.current_hda + \
                    ".houdiniAssetParm_percent{}".format(lod_num)
                lod_parcent = cmds.getAttr(_attr)
                # self.lods_percent[lod_num] = cmds.getAttr(_attr)
            _box = self._lodBox.get(lod_num)
            _slider = self._lodSlider.get(lod_num)
            _slider.setHDA(self.current_hda,
                           "houdiniAssetParm_percent{}".format(lod_num))
            if lod_num <= value:
                _slider.setEnable(True)
                _box.setEnabled(True)
            else:
                _slider.setEnable(False)
                _box.setEnabled(False)
            _slider.setValue(lod_parcent)
            self.polyCount(lod_num)

    def createLod(self, *args):
        _hda, root_node = command.apply_lod_create_hda(_suffix)
        if not _hda:
            return
        value = self.UI.lodNumSpinBox.value()
        self.lod_num = value

        if root_node[0] == "|":
            root_node = root_node[1:]

        _current_hda = cmds.rename(_hda, "{}{}".format(root_node, _suffix))

        self.getCurrentHDA(_current_hda)

        cmds.setAttr(self.current_hda + ".houdiniAssetParm_lod_num", value)
        self.current_hdas = command.get_scene_lod_create_hdas(_suffix)
        self.buildHdaConboBox(self.current_hda)


def main():

    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == CLASS_NAME:
            _obj.close()
            del _obj
    if not houdini_util.main():
        return

    if not os.path.exists(UI_FILE):
        # cmds.warning(u"UI ファイルが見つかりません")
        if not DEV_MODE:
            _m = "not found UI file [ {} ]".format(
                UI_FILE.replace(os.sep, '/'))
            logger.error(_m)
        return

    ui = LODCreateTool()
    ui.show()
    if not DEV_MODE:
        logger.send_launch(u'ツール起動')
