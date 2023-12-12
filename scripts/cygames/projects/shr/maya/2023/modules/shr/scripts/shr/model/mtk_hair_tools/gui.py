# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import OrderedDict
from itertools import zip_longest
from distutils.util import strtobool
from functools import partial

import importlib

import os
import random


from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

import maya.cmds as cmds

from . import maya_util
from . import command
from . import gui_util
from . import util

from . import TEMP_PATH, TITLE
from . import ROOT_PATH
from . import MAP_SAMPLING_LIST
from . import PRESET_TEXTURE_PREFEX
from . import FILE_IMFO_DATA
from . import TOOL_NAME

from mtk.utils.hda_loader import houdini_util

CLASS_NAME = "".join(TITLE.split())

UI_FILE = r"Z:\mtk\tools\maya\2022\modules\mtk\scripts\mtk\model\mtk_hair_tools\hair_tool_set_ui.ui"


# 開発中はTrue、リリース時にFalse
DEV_MODE = True


if DEV_MODE:
    importlib.reload(command)
    importlib.reload(util)
    importlib.reload(gui_util)
    importlib.reload(maya_util)
else:
    from . import logger


RESOLUTIONS = [
    32,
    64,
    128,
    256,
    512,
    1024,
    2048,
    4096,
    8192,
]


FILE_TYPES = [
    "tga",
    "png",
    "tif",
]


FILTER_TYPES = [
    "blackman_harris",
    "box",
    "catrom",
    "closest",
    "farthest",
    "gaussian",
    "heatmap",
    "mitnet",
    "sinc",
    "triangle",
    "variance",
]

SURFACE_SAMPLER_FILTER_TYPES = {
    "Gaussian": 0,
    "Triangle": 1,
    "Box": 2,
}


def check_all():
    _flag = False
    check_plugins = util.check_plugin()
    if check_plugins:
        if not DEV_MODE:
            logger.error(check_plugins)
        _flag = True

    check_paths = util.path_check()
    if check_paths:
        if not DEV_MODE:
            logger.error(check_paths)
        _flag = True

    return _flag


class FileIconProvider(QtWidgets.QFileIconProvider):
    def icon(self, fileInfo):
        if isinstance(fileInfo, QtCore.QFileInfo):
            if fileInfo.suffix() and fileInfo.suffix() == "png":
                return QtGui.QIcon(fileInfo.filePath())
        # return super(FileIconProvider, self).icon(fileInfo)


class ColorButton(QtWidgets.QPushButton):
    colorChanged = QtCore.Signal(QtGui.QColor)

    def __init__(self, *args, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)
        self.material = None
        self.attr = None
        self.attr_color = None
        self.setFlat(True)
        self.clicked.connect(self.showDialog)

        self.__color = QtGui.QColor(255, 255, 255)
        self.__update()

    def value_chenge(self, r, g, b):
        if self.attr and cmds.objExists(self.material):
            _node = self.attr.split(".")[0]
            _attr = "color2"
            if cmds.attributeQuery(_attr, n=_node, ex=True):
                cmds.setAttr("{}.{}".format(_node, _attr),
                             r, g, b, type="double3")

    def setMaterial(self, material, attr, color_value):
        self.material = material
        self.attr = attr
        if not attr:
            self.setEnabled(False)

    def showDialog(self):
        color = QtWidgets.QColorDialog.getColor(self.__color)
        if not color.isValid():
            return

        self.__color = color
        self.__update()
        self.colorChanged.emit(self.__color)

    def __update(self):
        r, g, b, a = self.__color.getRgb()
        self.setStyleSheet(
            '*{border:none;background:rgb(%s, %s, %s);}' % (r, g, b)
        )
        r, g, b, a = self.__color.getRgbF()
        self.value_chenge(r, g, b)

    def color(self):
        return self.__color

    def setColor(self, color):
        self.__color = color
        self.__update()
        self.colorChanged.emit(self.__color)

    def rgba(self):
        return self.__color.getRgb()

    def setRgba(self, r, g, b, a=255):
        self.__color.setRgb(r, g, b, a)
        self.__update()
        self.colorChanged.emit(self.__color)

    def hsv(self):
        return self.__color.getHsv()

    def setHsv(self, h, s, v, a=255):
        self.__color.setHsv(h, s, v, a)
        self.__update()
        self.colorChanged.emit(self.__color)


class CheckBox(QtWidgets.QCheckBox):
    valueChanged = QtCore.Signal(bool)

    def __init__(self, *args, **kwargs):
        super(CheckBox, self).__init__(*args, **kwargs)
        self.hda = None
        self.attr = None

        self.clicked.connect(self._click)

    def setHDA(self, hda, attr):
        self.hda = hda
        self.attr = attr

    def setValue(self, value):
        if not self.hda or not self.attr:
            return

        if not cmds.objExists(self.hda):
            return

        if cmds.attributeQuery(self.attr, n=self.hda, ex=True):
            cmds.setAttr(self.hda + "." + self.attr, value)
            self.valueChanged.emit(value)
            self.setChecked(value)

    def _click(self):
        value = self.isChecked()
        self.setValue(value)


class DoubleSlider(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(float)

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

        self.__slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.__updateSliderRange()
        layout.addWidget(self.__slider)

        self.__doubleSpinBox.valueChanged[float].connect(
            self.valueChangedCallback)
        self.__slider.valueChanged[int].connect(self.valueChangedCallback)

    def setMaterial(self, material, attr):
        self.material = material
        self.attr = attr
        if not attr:
            self.__slider.setEnabled(False)
            self.__doubleSpinBox.setEnabled(False)

    def blend_value_chenge(self, value):
        if self.attr and cmds.objExists(self.material):
            _node, _attr = self.attr.split(".")
            if cmds.attributeQuery(_attr, n=_node, ex=True):
                cmds.setAttr(self.attr, value)

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

        self.blend_value_chenge(value)
        self.valueChanged.emit(value)

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


class HairToolSet(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    UI = None
    _colorList = QtGui.QColor.colorNames()
    _color = _colorList[random.randint(0, len(_colorList)-1)]

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.ar_obj = None
        self.mats = list()
        self.color_buttons = list()

        self.parameters_ui = OrderedDict()
        self.current_datas = OrderedDict()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        loader = QUiLoader()

        uiFilePath = UI_FILE.replace(os.sep, '/')
        self.UI = loader.load(uiFilePath)

        self.mapCheckBox = [
            self.UI.normal_map,
            self.UI.flow_map,
            self.UI.occlusion_map,
            self.UI.root_map,
            self.UI.depth_map,
            self.UI.alpha_map,
            self.UI.id_map,
        ]

        self.UI.openConfluButton.clicked.connect(self.goToWebSite)
        self.UI.createBillBordButton.clicked.connect(self.createBillBord)
        self.UI.randomColorVtColorButton.clicked.connect(
            self.applyRondomColorVtx)
        self.UI.applyHimeshNameCheckBox.clicked.connect(
            self.applyHimeshNameCheck)
        self.UI.createPresetHairTextureButton.clicked.connect(
            self.bakePresetTexture)

        self.UI.applyHimeshNameCheckBox.setChecked(True)
        self.UI.hairPresetNameLineEdit.setEnabled(False)

        self.UI.allCheckButton.clicked.connect(
            partial(self.allCheckMapTypes, True))
        self.UI.allUnCheckButton.clicked.connect(
            partial(self.allCheckMapTypes, False))
        # validator = SampleValidator(self.UI.hairPresetNameLineEdit)
        # self.UI.hairPresetNameLineEdit.setValidator(validator)

        self.buildDirectoryTree()

        self.setDirectoryLine(ROOT_PATH)
        self.UI.directoryPathLine.returnPressed.connect(
            self.setDirectoryLinePressReturn)

        self.UI.create_material_btn.clicked.connect(
            partial(self.create_material_from_texture))
        self.UI.blend_color_0_rbtn.clicked.connect(
            partial(self.chenge_zero_one_switch))
        self.UI.blend_color_1_rbtn.clicked.connect(
            partial(self.chenge_zero_one_switch))
        self.UI.get_materials_btn.clicked.connect(
            partial(self.get_scene_materials))
        self.UI.openFileDialogButton.clicked.connect(
            partial(self.openPresetPathEditDialog, True))

        self.UI.openAtlusTextureExportDialogButton.clicked.connect(
            partial(self.openPresetPathEditDialog, False))
        self.UI.exportAtlusTexturePathLineEdit.returnPressed.connect(
            self.setAtlusDirectoryLinePressReturn)
        self.UI.conbineOrnatrixButton.clicked.connect(
            partial(self.UniteGuideMeshes))
        self.UI.createAtlusUvButton.clicked.connect(partial(self.apply_hda))
        self.UI.createAtlusTextureButton.clicked.connect(
            partial(self.createAtlusTexture))

        self.UI.removeHairCardButton.clicked.connect(
            partial(self.apply_reduction_hda))
        self.UI.isolateToggleButton.clicked.connect(
            partial(self.isolate_select))
        self.UI.wireViewToggleButton.clicked.connect(
            partial(self.wire_display))
        self.UI.bakeAssetButton.clicked.connect(partial(self.bakeAssets))

        self.UI.returnToPreferenceButton.clicked.connect(
            partial(self.returnToPreference))

        # ヘアマテリアルのブレンドカラー一括変換
        self.changeAllColorPushButton = ColorButton()
        _color = QtGui.QColor()
        _color.setRgbF(1.0, 1.0, 1.0, 1.0)
        self.changeAllColorPushButton.setColor(_color)

        self.applyAllColorPushButton = QtWidgets.QPushButton()
        self.applyAllColorPushButton.setText("Apply Color All")
        self.applyAllColorPushButton.clicked.connect(
            partial(self.apply_all_color))

        self.UI.allColorChangeLayout.addWidget(self.changeAllColorPushButton)
        self.UI.allColorChangeLayout.addWidget(self.applyAllColorPushButton)

        self.UI.atlusAlphaExportCheckBox.clicked.connect(
            self.atlusCheckBoxCallBack)
        self.UI.atlusDepthExportCheckBox.clicked.connect(
            self.atlusCheckBoxCallBack)
        self.UI.atlusNormalExportCheckBox.clicked.connect(
            self.atlusCheckBoxCallBack)
        self.UI.atlusRootExportCheckBox.clicked.connect(
            self.atlusCheckBoxCallBack)
        self.UI.atlusVColorExportCheckBox.clicked.connect(
            self.atlusCheckBoxCallBack)

        self.UI.allOnOffTogglePushButton.clicked.connect(
            partial(self.atlusCheckBoxToggleCallBack))

        self.resize(840, 465)
        self.setWindowTitle(TITLE)
        self.setCentralWidget(self.UI)

        self.resetUIsettings()

        self._trackSelectionOrder_flag()
        self.reset_settings()
        # self.buildRightClickMenu()
        self.buildHoudiniParams()

        cmds.scriptJob(event=("SceneOpened", self.reset_settings),
                       parent=self.objectName())
        cmds.scriptJob(event=("SelectionChanged", partial(
            self.buildHoudiniParams)), parent=self.objectName())

    def goToWebSite(self, *args):
        """ヘルプサイト表示
        """
        command.jump_confluence()

    def reset_settings(self, *args):
        """設定のリセット
        """
        self.show_wire()
        self.show_all()
        self.load_ui_setting()
        self.get_scene_materials()

    def atlusCheckBoxToggleCallBack(self, *args):
        """アトラステクスチャ出力チェックボックスのトグル機能
        """
        _all_check_box = [
            self.UI.atlusVColorExportCheckBox,
            self.UI.atlusAOExportCheckBox,
            self.UI.atlusRootExportCheckBox,
            self.UI.atlusDepthExportCheckBox,
            self.UI.atlusAlphaExportCheckBox,
            self.UI.atlusNormalExportCheckBox,
            self.UI.atlusFlowExportCheckBox,
        ]
        _check_box_state = [x for x in _all_check_box if x.isChecked()]

        if len(_all_check_box)/2 > len(_check_box_state):
            [x.setChecked(True) for x in _all_check_box]
        else:
            [x.setChecked(False) for x in _all_check_box]

        self.atlusCheckBoxCallBack()

    def atlusCheckBoxCallBack(self):
        """アトラステクスチャエクスポートチェックボックス動作
        irda 全部がそろわないとチェックボックスが有効化しない
        """
        _i = self.UI.atlusVColorExportCheckBox.isChecked()
        _r = self.UI.atlusRootExportCheckBox.isChecked()
        _d = self.UI.atlusDepthExportCheckBox.isChecked()
        _a = self.UI.atlusAlphaExportCheckBox.isChecked()

        if (not _i or not _r or not _d or not _a):
            self.UI.atlusIRDAExportCheckBox.setEnabled(False)
        else:
            self.UI.atlusIRDAExportCheckBox.setEnabled(True)

    def load_ui_setting(self, *args):
        """fileInfo に入れた設定を参照
        """
        root_path = ""
        file_info_datas = maya_util.get_file_infos()

        if not file_info_datas:
            self.resetComboBox()
            return
        for info, _ui in self.parameters_ui.items():
            _data = file_info_datas.get(info, None)
            if not _data:
                continue
            _data_type = info.rsplit("_", 1)[-1]
            if _data_type == "text":
                self.current_datas[info] = _ui.setText(_data)
                if "preset_directory_text" == info:
                    root_path = _data
            elif _data_type == "value" or _data_type == "fvalue":
                self.current_datas[info] = _ui.setValue(_data)
            elif _data_type == "check":
                self.current_datas[info] = _ui.setChecked(strtobool(_data))
            elif _data_type == "txint":
                self.current_datas[info] = _ui.setCurrentText(_data)

        if not root_path:
            root_path = ROOT_PATH

        self.dirmodel.setRootPath(root_path)
        self.inner_dirmodel.setRootPath(root_path)
        self.UI.directory_tree.setRootIndex(self.dirmodel.index(root_path))
        self.UI.texture_file_table.setRootIndex(
            self.inner_dirmodel.index(root_path))

        self.applyHimeshNameCheck()

    def resetComboBox(self, *args):
        """コンボボックスの初期化
        """
        if not DEV_MODE:
            self.UI.bakeResolutionConboBox.setCurrentIndex(6)
            self.UI.atlusResolutionComboBox.setCurrentIndex(6)
            self.UI.atlusRenderQuarityComboBox.setCurrentIndex(0)
        # else:
        #     self.UI.bakeResolutionConboBox.setCurrentIndex(4)
        #     self.UI.exportAtlusTexturePathLineEdit.setText("D:/ando/mutsunokami/test_atlus")
        #     self.UI.atlusResolutionComboBox.setCurrentIndex(4)
        self.UI.atlusTextureFormatComboBox.setCurrentIndex(0)
        self.UI.bakeFillterTypeComboBox.setCurrentIndex(5)

        self.UI.bakeResolutionConboBox.setCurrentIndex(6)
        self.UI.atlusResolutionComboBox.setCurrentIndex(6)
        self.UI.atlusRenderQuarityComboBox.setCurrentIndex(0)

        self.UI.sampling.setValue(3)
        self.UI.filter_width.setValue(2.0)

    def returnToPreference(self, *args):
        """ツールの設定初期化
        """
        self.UI.polyScaleDoubleSpinBox.setValue(1.05)
        self.resetComboBox()
        self.applyHimeshNameCheck()

    def resetUIsettings(self):
        """UI のリセット
        """
        self.reestTextureFileName()
        self.bulidConboBoxs()
        self.set_ui()

    def reestTextureFileName(self):
        """アトラステクスチャの名前を初期値に変更
        """
        self.UI.textureFileNameLine.setText("")

    def bulidConboBoxs(self):
        """コンボボックスの初期設定
        """
        for res in RESOLUTIONS:
            self.UI.bakeResolutionConboBox.addItem("{}".format(res))
            self.UI.atlusResolutionComboBox.addItem("{}".format(res))

        for quality in MAP_SAMPLING_LIST:
            self.UI.atlusRenderQuarityComboBox.addItem("{}".format(quality))

        for _type in FILE_TYPES:
            self.UI.atlusTextureFormatComboBox.addItem("{}".format(_type))

        for _type in FILTER_TYPES:
            self.UI.bakeFillterTypeComboBox.addItem("{}".format(_type))

        for filter_type, type_int in SURFACE_SAMPLER_FILTER_TYPES.items():
            self.UI.atlusTextureFilterTypeComboBox.addItem(filter_type)

    def set_ui(self, *args):
        """ツールの設定をメモリに読み込み
        """
        self.parameters_ui = OrderedDict()
        _uis = [
            self.UI.directoryPathLine,
            self.UI.polyScaleDoubleSpinBox,
            self.UI.applyHimeshNameCheckBox,
            self.UI.hairPresetNameLineEdit,

            self.UI.bakeResolutionConboBox,
            self.UI.bakeFillterTypeComboBox,
            self.UI.sampling,
            self.UI.filter_width,

            self.UI.normal_map,
            self.UI.flow_map,
            self.UI.occlusion_map,
            self.UI.root_map,
            self.UI.depth_map,
            self.UI.alpha_map,
            self.UI.id_map,

            self.UI.delete_unused_ck,

            self.UI.atlusResolutionComboBox,
            self.UI.atlusRenderQuarityComboBox,
            self.UI.textureFileNameLine,
            self.UI.atlusTextureFormatComboBox,
            self.UI.atlusCreateMaterialCheckBox,
            self.UI.exportAtlusTexturePathLineEdit,

            self.UI.uv_crop_ck,

            self.UI.atlusTextureFilterTypeComboBox,
            self.UI.atlusTextureFilterDoubleSpinBox,
        ]
        for info, _ui in zip_longest(FILE_IMFO_DATA, _uis):
            self.parameters_ui[info] = _ui

    def get_ui_parameters(self, *args):
        """保存するため UI の情報を取得
        """
        self.current_datas = OrderedDict()

        for info, _ui in self.parameters_ui.items():
            _data_type = info.rsplit("_", 1)[-1]
            if _data_type == "text":
                self.current_datas[info] = _ui.text()
            elif _data_type == "value" or _data_type == "fvalue":
                self.current_datas[info] = _ui.value()
            elif _data_type == "check":
                self.current_datas[info] = _ui.isChecked()
            elif _data_type == "txint":
                self.current_datas[info] = _ui.currentText()

    def save_current_settings(self, *args):
        """設定をfileInfo に書き込み
        """
        self.get_ui_parameters()
        if not self.current_datas:
            return
        for info, value in self.current_datas.items():
            cmds.fileInfo("{}_{}".format(TOOL_NAME, info), value)

        cmds.warning(u"設定を記憶しました　シーンを [　上書き　] 保存しないと　ファイルに書き込まれないのでご注意ください!!")

    def bakeAssets(self, *args):
        command._bake_asset()

    def delete_combo_boxs(self):
        """コンボボックスの削除
        """
        _targets = [self.UI.hdaParameterLayout,
                    self.UI.reductionHdaParamLayout]
        for _target in _targets:
            for i in reversed(range(_target.count())):
                _widget = _target.itemAt(i)

                if isinstance(_widget, QtWidgets.QSpacerItem):
                    _target.removeItem(_widget)
                else:
                    _widget.widget().deleteLater()

    def buildHoudiniParams(self, *args):
        self.delete_combo_boxs()
        # self.buildHoudiniParametersReduction()
        self.buildHoudiniParametersEdgeReduction()
        self.bulidHoudiniParameters()

    def buildHoudiniParametersEdgeReduction(self, *args):
        hda = command.get_remove_hda_nodes()

        if not hda:
            return

        if (not cmds.attributeQuery("houdiniAssetParm_percentage", node=hda, ex=True) or
            not cmds.attributeQuery("houdiniAssetParm_reducepassedtarget", node=hda, ex=True) or
            not cmds.attributeQuery("houdiniAssetParm_originalpoints", node=hda, ex=True) or
                not cmds.attributeQuery("houdiniAssetParm_retainattribweight", node=hda, ex=True)):
            return

        _percentage = cmds.getAttr(hda + ".houdiniAssetParm_percentage")
        _reducepassedtarget = cmds.getAttr(
            hda + ".houdiniAssetParm_reducepassedtarget")
        _originalpoints = cmds.getAttr(
            hda + ".houdiniAssetParm_originalpoints")
        _retainattribweight = cmds.getAttr(
            hda + ".houdiniAssetParm_retainattribweight")

        _target = self.UI.reductionHdaParamLayout

        _box = QtWidgets.QGroupBox()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(3)

        _percentage_label = QtWidgets.QLabel(u"エッジ削減パーセント")
        _percentage_slider = DoubleSlider()

        _reducepassedtarget_ck = CheckBox(u"三角形の許容")
        _reducepassedtarget_ck.setHDA(
            hda, "houdiniAssetParm_reducepassedtarget")
        _reducepassedtarget_ck.setValue(_reducepassedtarget)

        _originalpoints_ck = CheckBox(u"オリジナルの頂点を使用")
        _originalpoints_ck.setHDA(hda, "houdiniAssetParm_originalpoints")
        _originalpoints_ck.setValue(_originalpoints)

        _retainattribweight_label = QtWidgets.QLabel(u"曲率の考慮")
        _retainattribweight_slider = DoubleSlider()

        _percentage_slider.setRange(0.0, 100.0)
        _percentage_slider.setDecimals(0)
        _percentage_slider.setMaterial(hda, hda+".houdiniAssetParm_percentage")
        _percentage_slider.setValue(_percentage)

        _retainattribweight_slider.setRange(0.0, 100.0)
        _retainattribweight_slider.setDecimals(0)
        _retainattribweight_slider.setMaterial(
            hda, hda+".houdiniAssetParm_retainattribweight")
        _retainattribweight_slider.setValue(_retainattribweight)

        layout.addWidget(_percentage_label)
        layout.addWidget(_percentage_slider)
        layout.addWidget(_reducepassedtarget_ck)
        layout.addWidget(_originalpoints_ck)
        layout.addWidget(_retainattribweight_label)
        layout.addWidget(_retainattribweight_slider)

        _box.setLayout(layout)
        _target.addWidget(_box)

        verticalSpacer = QtWidgets.QSpacerItem(20, 40,
                                               QtWidgets.QSizePolicy.Minimum,
                                               QtWidgets.QSizePolicy.Expanding)

        _target.addItem(verticalSpacer)

    def buildHoudiniParametersReduction(self, *args):
        hda = command.get_remove_hda_nodes()

        if not hda:
            return

        if (not cmds.attributeQuery("houdiniAssetParm_tol3d", node=hda, ex=True) or
                not cmds.attributeQuery("houdiniAssetParm_threshold", node=hda, ex=True)):
            return

        _density_value = cmds.getAttr(hda + ".houdiniAssetParm_tol3d")
        _threshold_value = cmds.getAttr(hda + ".houdiniAssetParm_threshold")
        _target = self.UI.reductionHdaParamLayout

        _box = QtWidgets.QGroupBox()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(3)

        _density_label = QtWidgets.QLabel(u"密度ベースの間引き")
        _density = DoubleSlider()
        _area_label = QtWidgets.QLabel(u"カードの面積ベースの間引き")
        _area = DoubleSlider()

        _density.setRange(0.0, 1.0)
        _density.setMaterial(hda, hda+".houdiniAssetParm_tol3d")
        _density.setValue(_density_value)

        _area.setRange(0.0, 100.0)
        _area.setMaterial(hda, hda+".houdiniAssetParm_threshold")
        _area.setValue(_threshold_value)

        layout.addWidget(_density_label)
        layout.addWidget(_density)
        layout.addWidget(_area_label)
        layout.addWidget(_area)

        _box.setLayout(layout)
        _target.addWidget(_box)

        verticalSpacer = QtWidgets.QSpacerItem(20, 40,
                                               QtWidgets.QSizePolicy.Minimum,
                                               QtWidgets.QSizePolicy.Expanding)

        _target.addItem(verticalSpacer)

    def bulidHoudiniParameters(self, *args):

        hda = command.get_hda_nodes()
        if not hda:
            return

        if (not cmds.attributeQuery("houdiniAssetParm_padding", node=hda, ex=True) or
            not cmds.attributeQuery("houdiniAssetParm_padding2", node=hda, ex=True) or
            not cmds.attributeQuery("houdiniAssetParm_correctareas", node=hda, ex=True) or
            not cmds.attributeQuery("houdiniAssetParm_edit_normal", node=hda, ex=True) or
            not cmds.attributeQuery("houdiniAssetParm_view_cage", node=hda, ex=True) or
            not cmds.attributeQuery("houdiniAssetParm_dilateerode", node=hda, ex=True) or
                not cmds.attributeQuery("houdiniAssetParm_smooth_iteration", node=hda, ex=True)):
            return

        # _scale_u_value = cmds.getAttr(hda + ".houdiniAssetParm_sx")
        _correctareas = cmds.getAttr(hda + ".houdiniAssetParm_correctareas")
        _padding1_value = cmds.getAttr(hda + ".houdiniAssetParm_padding")
        _padding2_value = cmds.getAttr(hda + ".houdiniAssetParm_padding2")
        _edit_nomal_value = cmds.getAttr(hda + ".houdiniAssetParm_edit_normal")
        _view_cage_value = cmds.getAttr(hda + ".houdiniAssetParm_view_cage")
        _dilate_erode_value = cmds.getAttr(
            hda + ".houdiniAssetParm_dilateerode")
        _smooth_iteration_value = cmds.getAttr(
            hda + ".houdiniAssetParm_smooth_iteration")

        _target = self.UI.hdaParameterLayout

        _box = QtWidgets.QGroupBox()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(3)

        # _scale_U_label = QtWidgets.QLabel("Scale U")
        # _scale_U = DoubleSlider()

        _enable_correctareas = CheckBox(u"大きさの比率を拡大")
        _enable_correctareas.setHDA(hda, "houdiniAssetParm_correctareas")
        _enable_correctareas.setValue(_correctareas)

        _padding_uv1_label = QtWidgets.QLabel(u"UV Set 1 のパディング")
        _padding_uv1 = DoubleSlider()
        _padding_uv2_label = QtWidgets.QLabel(u"UV Set 2 のパディング")
        _padding_uv2 = DoubleSlider()

        _dilate_erode_label = QtWidgets.QLabel(u"ケージモデルの縮小 / 拡張")
        _dilate_erode = DoubleSlider()
        _smooth_iteration_label = QtWidgets.QLabel(u"ケージモデルのスムース")
        _smooth_iteration = DoubleSlider()

        # _scale_U.setRange(0.0, 10.0)
        # _scale_U.setMaterial(hda, hda+".houdiniAssetParm_sx")
        # _scale_U.setValue(_scale_u_value)

        _padding_uv1.setRange(0.0, 20.0)
        _padding_uv1.setMaterial(hda, hda+".houdiniAssetParm_padding")
        _padding_uv1.setValue(_padding1_value)

        _padding_uv2.setRange(0.0, 20.0)
        _padding_uv2.setMaterial(hda, hda+".houdiniAssetParm_padding2")
        _padding_uv2.setValue(_padding2_value)

        _dilate_erode.setRange(-10.0, 10.0)
        _dilate_erode.setMaterial(hda, hda+".houdiniAssetParm_dilateerode")
        _dilate_erode.setValue(_dilate_erode_value)

        _smooth_iteration.setDecimals(0)
        _smooth_iteration.setRange(0.0, 10.0)
        _smooth_iteration.setMaterial(
            hda, hda+".houdiniAssetParm_smooth_iteration")
        _smooth_iteration.setValue(_smooth_iteration_value)

        _enable_edit_normal = CheckBox(u"ノーマルの編集")
        _enable_edit_normal.setHDA(hda, "houdiniAssetParm_edit_normal")
        _enable_edit_normal.setValue(_edit_nomal_value)

        _view_cage = CheckBox(u"ノーマル編集用のケージ表示")
        _view_cage.setHDA(hda, "houdiniAssetParm_view_cage")
        _view_cage.setValue(_view_cage_value)

        # layout.addWidget(_scale_U_label)
        # layout.addWidget(_scale_U)

        layout.addWidget(_enable_correctareas)
        layout.addWidget(_padding_uv1_label)
        layout.addWidget(_padding_uv1)
        layout.addWidget(_padding_uv2_label)
        layout.addWidget(_padding_uv2)
        layout.addWidget(_enable_edit_normal)
        layout.addWidget(_view_cage)
        layout.addWidget(_dilate_erode_label)
        layout.addWidget(_dilate_erode)
        layout.addWidget(_smooth_iteration_label)
        layout.addWidget(_smooth_iteration)

        _box.setLayout(layout)
        _target.addWidget(_box)

        verticalSpacer = QtWidgets.QSpacerItem(20, 40,
                                               QtWidgets.QSizePolicy.Minimum,
                                               QtWidgets.QSizePolicy.Expanding)

        _target.addItem(verticalSpacer)

    def buildDirectoryTree(self, path=ROOT_PATH):
        self.dirmodel = QtWidgets.QFileSystemModel()
        self.dirmodel.setRootPath(path)
        self.dirmodel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Dirs)
        self.UI.directory_tree.setModel(self.dirmodel)
        self.UI.directory_tree.setRootIndex(self.dirmodel.index(path))
        self.UI.directory_tree.header().setSectionHidden(1, True)
        self.UI.directory_tree.header().setSectionHidden(2, True)
        self.UI.directory_tree.header().setSectionHidden(3, True)
        self.UI.directory_tree.setHeaderHidden(True)
        self.UI.directory_tree.clicked[QtCore.QModelIndex].connect(
            self.clicked_tree)

        # TreeView を展開させない
        # self.UI.directory_tree.setItemsExpandable(False)

        # 矢印自体を表示させない
        # self.UI.directory_tree.setRootIsDecorated(False)

        self.inner_dirmodel = QtWidgets.QFileSystemModel()
        # self.inner_dirmodel.setRootPath(path)
        self.inner_dirmodel.setIconProvider(FileIconProvider())
        self.UI.texture_file_table.setModel(self.inner_dirmodel)
        self.UI.texture_file_table.setRootIndex(
            self.inner_dirmodel.index(path))
        self.UI.texture_file_table.verticalHeader().hide()
        self.UI.texture_file_table.setSortingEnabled(True)
        self.inner_dirmodel.setFilter(QtCore.QDir.Files)
        # self.inner_dirmodel.setNameFilters(['*_depth.png'])
        self.inner_dirmodel.setNameFilters(['*.png'])
        self.inner_dirmodel.setNameFilterDisables(False)

        header = self.UI.texture_file_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.UI.texture_file_table.verticalHeader().setDefaultSectionSize(128)
        self.UI.texture_file_table.clicked[QtCore.QModelIndex].connect(
            self.clicked_table)
        self.UI.texture_file_table.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.UI.texture_file_table.setSelectionBehavior(
            self.UI.texture_file_table.SelectRows)
        self.UI.texture_file_table.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        # self.UI.texture_file_table.customContextMenuRequested.connect(self.contextMenu)

        self.UI.texture_file_table.setMouseTracking(True)
        self.UI.texture_file_table.viewport().installEventFilter(self)

    def buildRightClickMenu(self):
        """左のテーブルを右クリックしたときに表示させるメニュー
        """
        self.replace_menu = QtWidgets.QMenu(self)
        _text = self.UI.create_material_btn.text()
        action = QtWidgets.QAction(u"{}".format(_text), self)
        action.triggered.connect(self.getTexturePath)
        self.replace_menu.addAction(action)

    def contextMenu(self, point):
        select_table = self.UI.texture_file_table.selectedIndexes()
        if not select_table:
            return

        _add = QtCore.QPoint(self.UI.directory_tree.width(), 120)
        self.replace_menu.exec_(_add + self.mapToGlobal(point))

    def getTexturePath(self):
        _index = self.UI.texture_file_table.currentIndex()
        if not _index:
            return
        dir_path = self.inner_dirmodel.filePath(_index)

    def _trackSelectionOrder_flag(self):
        """選択順番の初期フラグ取得
        選択順番適用

        Returns:
            [bool]: 選択順番フラグ
        """
        _tso_flag = cmds.selectPref(q=True, tso=True)

        self._tso_flag = _tso_flag
        if not _tso_flag:
            cmds.selectPref(tso=True)
        return _tso_flag

    def change_tso(self, *args):
        """選択順番を初期値に戻す
        """
        cmds.selectPref(tso=self._tso_flag)

    def closeEvent(self, event):
        """ツール終了時の動作
        選択順番を初期値に戻すメソッド実行
        """
        self.change_tso()
        self.show_wire()
        self.show_all()
        # if self.current_datas:
        self.save_current_settings()

        if self.ar_obj:
            self.ar_obj.end_bake_process()
        if self.mats:
            self.blend_switch(True)
        event.accept()

    # プリセットの保存場所
    def openPresetPathEditDialog(self, preset_line=True):
        u"""Button Command"""
        if preset_line:
            path = self.UI.directoryPathLine.text().replace(os.sep, '/')
        else:
            path = self.UI.exportAtlusTexturePathLineEdit.text().replace(os.sep, '/')
        if not os.path.exists(path):
            path = ROOT_PATH

        dialog = QtWidgets.QFileDialog(directory=path)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        if dialog.exec_():
            path = dialog.selectedFiles()[0]
            if preset_line:
                self.UI.directoryPathLine.setText(path)
                self.setDirectoryLinePressReturn()
            else:
                self.UI.exportAtlusTexturePathLineEdit.setText(path)

    def setDirectoryLinePressReturn(self):
        path = self.UI.directoryPathLine.text().replace(os.sep, '/')

        # self.buildDirectoryTree(path)

        self.dirmodel.setRootPath(path)
        self.inner_dirmodel.setRootPath(path)
        self.UI.directory_tree.setRootIndex(self.dirmodel.index(path))
        self.UI.texture_file_table.setRootIndex(
            self.inner_dirmodel.index(path))
        self.UI.directoryPathLine.setText(path)

    def setDirectoryLine(self, path):
        path = path.replace(os.sep, '/')
        self.UI.directoryPathLine.setText(path)
        # self.buildDirectoryTree(path)

        self.dirmodel.setRootPath(path)
        self.inner_dirmodel.setRootPath(path)

    def setAtlusDirectoryLinePressReturn(self):
        path = self.UI.exportAtlusTexturePathLineEdit.text().replace(os.sep, '/')
        self.UI.exportAtlusTexturePathLineEdit.setText(path)

    # プリセット作成ツール群

    def createBillBord(self, *args):
        _scale_value = self.UI.polyScaleDoubleSpinBox.value()
        command.create_billbord(_scale_value)

    def allCheckMapTypes(self, flag=True):
        for ck in self.mapCheckBox:
            ck.setChecked(flag)

    def applyHimeshNameCheck(self):
        """ハイメッシュのジオメトリから作成
        チェックボックスの動作
        """
        _value = self.UI.applyHimeshNameCheckBox.isChecked()
        if _value:
            self.UI.hairPresetNameLineEdit.setEnabled(False)

        else:
            # self.UI.hairPresetNameLineEdit.setText("")
            self.UI.hairPresetNameLineEdit.setEnabled(True)
            # self.UI.hairPresetNameLineEdit.setReadOnly(True)

    def applyRondomColorVtx(self):
        """ランダム頂点カラー適用
        """
        command.apply_random_vertex_color_polygon_shell()

    def getMapTypeCheckBox(self):
        """ヘアカードベイク時の出力マップ

        Returns:
            [list]: export map type: ex. "normal"
        """
        export_flags = [
            self.UI.normal_map.isChecked(),
            self.UI.flow_map.isChecked(),
            self.UI.occlusion_map.isChecked(),
            self.UI.root_map.isChecked(),
            self.UI.depth_map.isChecked(),
            self.UI.alpha_map.isChecked(),
            self.UI.id_map.isChecked(),
        ]

        export_map_types = [
            "normal",
            "flow",
            "ao",
            "root",
            "depth",
            "alpha",
            "vcolor",
        ]

        export_maps = []
        for _map, flag in zip(export_map_types, export_flags):
            if flag:
                export_maps.append(_map)

        if not export_maps:
            _m = u"マップの出力チェックボックスが全てオフです"
            _d = gui_util.ConformDialog(title=u"出力マップの確認", message=_m)
            _d.exec_()
            return False

        return export_maps

    def bakePresetTexture(self):
        """ヘアカードベイク
        """
        check_box = self.UI.applyHimeshNameCheckBox.isChecked()
        resolusion = int(self.UI.bakeResolutionConboBox.currentText())
        sample_filter = self.UI.bakeFillterTypeComboBox.currentText()
        file_name = self.UI.hairPresetNameLineEdit.text()
        _crop_uv_flag = self.UI.uv_crop_ck.isChecked()

        aa_samples = self.UI.sampling.value()
        filter_width = self.UI.filter_width.value()
        normal_offset = 1000.0
        enable_aovs = False
        extend_edges = False
        black_bg_flag = False

        selections = command.check_transform_selection()

        if not selections:
            return

        _flag = check_all()
        if _flag:
            return

        export_path = TEMP_PATH

        source_node = selections[0]
        target_node = selections[1]

        if check_box:
            preset_name = source_node.split("|")[-1]
        else:
            preset_name = file_name

        if not command.check_preset_name(preset_name):
            return

        path = self.UI.directoryPathLine.text()
        hair_preset_path = os.path.join(path, preset_name).replace(os.sep, '/')
        _path_check = command.check_preset_path(hair_preset_path)
        if not _path_check:
            return

        export_maps = self.getMapTypeCheckBox()
        if not export_maps:
            return

        preset_name = "{}_{}".format(PRESET_TEXTURE_PREFEX, preset_name)

        ar_obj = command.ArnoldRenderTextureBake(
            hair_preset_path,
            export_path,
            source_node,
            target_node,
            export_maps,
            preset_name,
            resolusion,
            aa_samples,
            sample_filter,
            filter_width,
            normal_offset,
            enable_aovs,
            extend_edges,
            _crop_uv_flag,
            black_bg_flag,
        )

        _m = ""
        if not ar_obj.target_nodes:
            _m = u"ターゲットにメッシュがありません"
        if not ar_obj.source_nodes:
            _m = u"ソースにメッシュがありません"
        if _m:
            _d = gui_util.ConformDialog(title=TITLE, message=_m)
            _d.exec_()
            return

        cmds.select(target_node, r=True)

        self.ar_obj = ar_obj
        error_message = ar_obj.set_up_bake_process()

        if error_message:
            print(error_message)
            if not DEV_MODE:
                logger.error(error_message)

        if not error_message:
            error_message = ar_obj.arnold_render_textures()
            if error_message:
                error_message = "\n".join(error_message)
                print(error_message)
                if not DEV_MODE:
                    logger.error(error_message)

        ar_obj.end_bake_process()
        # self.buildDirectoryTree(path)

        cmds.select(source_node, r=True)
        cmds.select(target_node, add=True)

    def get_scene_materials(self, *args):
        """シーンマテリアル取得
        ヘアマテリアルがあれば UI に埋め込む
        """
        self.delete_all_group_sets()
        self.mats = command.get_scene_materials()

        if self.mats:
            self.create_material_group_set()

    def chenge_zero_one_switch(self, *args):
        """ヘアマテリアルのブレンドノードを
        ゼロか一に一括変換
        """
        if self.mats:
            flag = self.UI.blend_color_0_rbtn.isChecked()
            self.blend_switch(flag)

    def blend_switch(self, flag=True):
        """ヘアマテリアルのブレンドノードの一括変換

        Args:
            flag (bool):
                0 にする場合は True
                1 にする場合は False
        """
        for mat in self.mats:
            if not cmds.objExists(mat):
                continue
            if mat.blend_attribute:
                # _blend_attr = mat.blend_attribute
                _node, _attr = mat.blend_attribute.split(".")
                if not cmds.attributeQuery(_attr, n=_node, ex=True):
                    continue
                if flag:
                    mat.slider.setValue(0.0)
                    cmds.setAttr(mat.blend_attribute, 0)
                else:
                    mat.slider.setValue(1.0)
                    cmds.setAttr(mat.blend_attribute, 1)

    def create_material_from_texture(self, *args):
        """ヘアカードテクスチャからマテリアルを生成、適用
        """
        blend_switch_flag = self.UI.blend_color_1_rbtn.isChecked()
        select_tree = self.UI.directory_tree.selectedIndexes()
        select_tree = command.get_texture_from_tree(self.UI.directory_tree)
        if not select_tree:
            return

        file_path = self.dirmodel.filePath(select_tree[0])

        png_files = command.get_file_path_from_tree_selection(file_path)

        if not png_files:
            return

        _shapes = command.get_shapes()
        if not _shapes:
            _shapes = command.get_current_face_selections()

        _color = self.getNextColor()
        _color = QtGui.QColor(_color)
        _color_rgb = _color.getRgbF()

        command.create_new_material(
            png_files["depth"], png_files["alpha"], _shapes, _color_rgb)
        if self.UI.delete_unused_ck.isChecked():
            command.delete_unused_materials()
        self.get_scene_materials()

    def getNextColor(self):
        """カラー設定をある程度のランダムにしている
        次のカラーをピックアップして適用

        Returns:
            [QtGui.QColor]:
        """
        index = self._colorList.index(self._color)
        index += 1
        if index > len(self._colorList)-1:
            index = 0
        self._color = self._colorList[index]

        return self._color

    def delete_all_group_sets(self, *args):
        """ヘアマテリアル編集機能の全削除
        """
        for i in reversed(range(self.UI.material_group_set_area.count())):
            _widget = self.UI.material_group_set_area.itemAt(i)
            if isinstance(_widget, QtWidgets.QSpacerItem):
                self.UI.material_group_set_area.removeItem(_widget)
            else:
                _widget.widget().deleteLater()

        # カラーボタンのリストも初期化
        self.color_buttons = list()

    def apply_all_color(self, *args):
        """Apply Color All ボタンで全部の色を変える動作
        """
        if not self.color_buttons:
            return
        _color = self.changeAllColorPushButton.color()
        for _color_btn in self.color_buttons:
            _color_btn.setColor(_color)

    def create_material_group_set(self, *args):
        """ヘアマテリアルの色設定、ブレンド設定
        マテリアル選択、フェース選択機能
        self.mat にマテリアル自体を入れて管理
        """
        self.color_buttons = []
        for mat in self.mats:
            if not mat.blend_attribute:
                continue
            _box = QtWidgets.QGroupBox('{}'.format(mat))
            layout = QtWidgets.QVBoxLayout()
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setSpacing(10)

            _slider = DoubleSlider()
            _color_btn = ColorButton()
            _slider.setRange(0.0, 1.0)
            _slider.setMaterial(mat, mat.blend_attribute)
            _color_btn.setMaterial(mat, mat.blend_attribute, mat.blend_value)

            _r, _g, _b = mat.blend_color[0]
            _color = QtGui.QColor()
            _color.setRgbF(_r, _g, _b, 1.0)
            _color_btn.setColor(_color)

            self.color_buttons.append(_color_btn)
            _slider.setValue(mat.blend_value)

            btn_layout = QtWidgets.QHBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(10)

            _btn_mat_select = QtWidgets.QPushButton(u"ﾏﾃﾘｱﾙ選択")
            _btn_face_select = QtWidgets.QPushButton(u"ﾌｪｰｽ選択")
            _btn_mat_select.clicked.connect(partial(self.select_material, mat))
            _btn_face_select.clicked.connect(
                partial(self.select_material_face, mat))

            btn_layout.addWidget(_btn_mat_select)
            btn_layout.addWidget(_btn_face_select)

            layout.addWidget(_slider)
            layout.addWidget(_color_btn)
            layout.addLayout(btn_layout)
            _box.setLayout(layout)
            self.UI.material_group_set_area.addWidget(_box)

            mat.slider = _slider
            mat.button = _btn_face_select

        self.verticalSpacer = QtWidgets.QSpacerItem(20, 40,
                                                    QtWidgets.QSizePolicy.Minimum,
                                                    QtWidgets.QSizePolicy.Expanding)

        self.UI.material_group_set_area.addItem(self.verticalSpacer)

    def delete_unused_materials(self, *args):
        """使用していないマテリアルを削除
        mel を呼び出している
        """
        command.delete_unused_materials()

    def select_material(self, material):
        """マテリアルの選択

        Args:
            material ([str]]): maya material node
        """
        command.select_material(material)

    def select_material_face(self, material):
        """マテリアルが適用されているフェースを選択

        Args:
            material ([str]): maya material node
        """
        command.select_material_face(material)

    def clicked_table(self, *args):
        _index = self.UI.texture_file_table.currentIndex()
        dir_path = self.inner_dirmodel.filePath(_index)

    def clicked_tree(self, *args):
        _index = self.UI.directory_tree.currentIndex()
        dir_path = self.dirmodel.filePath(_index)
        self.inner_dirmodel.setRootPath(dir_path)
        self.UI.texture_file_table.setRootIndex(
            self.inner_dirmodel.index(dir_path))
        self.UI.texture_file_table.clearSelection()

    def UniteGuideMeshes(self, *args):
        guides = command.get_hair_gides()

    def apply_reduction_hda(self, *args):
        _flag = check_all()
        if _flag:
            return

        _m = command.apply_redction_hda()
        if _m:
            _d = gui_util.ConformDialog(title=TITLE, message=_m)
            _d.exec_()

    def apply_hda(self, *args):
        _flag = check_all()
        if _flag:
            return

        _m = command.apply_hda()
        if _m:
            _d = gui_util.ConformDialog(title=TITLE, message=_m)
            _d.exec_()

    def createAtlusTexture(self, *args):
        resolution = self.UI.atlusResolutionComboBox.currentText()
        quality = self.UI.atlusRenderQuarityComboBox.currentText()
        file_format = self.UI.atlusTextureFormatComboBox.currentText()
        file_name = self.UI.textureFileNameLine.text()
        path = self.UI.exportAtlusTexturePathLineEdit.text()
        create_material = self.UI.atlusCreateMaterialCheckBox.isChecked()
        filter_type = self.UI.atlusTextureFilterTypeComboBox.currentText()
        filter_type_int = SURFACE_SAMPLER_FILTER_TYPES.get(filter_type)
        filter_size = self.UI.atlusTextureFilterDoubleSpinBox.value()

        # 書き出すマップを確認
        export_maps = []
        _i = self.UI.atlusVColorExportCheckBox.isChecked()
        _r = self.UI.atlusRootExportCheckBox.isChecked()
        _d = self.UI.atlusDepthExportCheckBox.isChecked()
        _a = self.UI.atlusAlphaExportCheckBox.isChecked()
        _normal = self.UI.atlusNormalExportCheckBox.isChecked()
        _flow = self.UI.atlusFlowExportCheckBox.isChecked()
        _irda = self.UI.atlusIRDAExportCheckBox.isChecked()

        # irda はチェックボックスが無効の場合は出力しない
        if not self.UI.atlusIRDAExportCheckBox.isEnabled():
            _irda = False

        if _i:
            export_maps.append("vcolor")
        if _r:
            export_maps.append("root")
        if _d:
            export_maps.append("depth")
        if _a:
            export_maps.append("alpha")
        if _normal:
            export_maps.append("normal")
        if _flow:
            export_maps.append("flow")

        _m = command.create_atlus_texture(
            path=path,
            file_name=file_name,
            resolution=resolution,
            quality=quality,
            file_format=file_format,
            filter_type=filter_type_int,
            filter_size=filter_size,
            export_maps=export_maps,
            irda_map_flag=_irda,
            create_material=create_material)

    def show_wire(self, *args):
        cmds.displayPref(wireframeOnShadedActive='full')

    def show_all(self, *args):
        _Panels = cmds.getPanel(type="modelPanel")
        for _Panel in _Panels:
            cmds.isolateSelect(_Panel, state=False)
            cmds.isolateSelect(_Panel, removeSelected=True)

    def getTransformSelections(self):
        selections = cmds.ls(sl=True, type="transform")
        if not selections:
            return
        return selections

    def wire_display(self, *args):
        sel = self.getTransformSelections()
        if not sel:
            return
        if cmds.displayPref(q=True, wireframeOnShadedActive=True) == 'full':
            cmds.displayPref(wireframeOnShadedActive='none')
        else:
            cmds.displayPref(wireframeOnShadedActive='full')

    def isolate_select(self, *args):
        _Panels = cmds.getPanel(type="modelPanel")
        _state = cmds.isolateSelect(_Panels[-1], q=True, state=True)
        for _Panel in _Panels:
            if _state:
                cmds.isolateSelect(_Panel, state=False)
                cmds.isolateSelect(_Panel, removeSelected=True)
            else:
                cmds.isolateSelect(_Panel, state=True)
                cmds.isolateSelect(_Panel, addSelected=True)


def main():
    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == CLASS_NAME:
            _obj.close()
            del _obj

    if not houdini_util.main():
        return

    # _flag = check_all()
    # if _flag:
    #     return

    if not os.path.exists(UI_FILE):
        cmds.warning(u"UI ファイルが見つかりません")
        if not DEV_MODE:
            _m = "not found UI file [ {} ]".format(
                UI_FILE.replace(os.sep, '/'))
            logger.error(_m)
        return

    ui = HairToolSet()
    ui.show()
    if not DEV_MODE:
        logger.send_launch(u'ツール起動')
