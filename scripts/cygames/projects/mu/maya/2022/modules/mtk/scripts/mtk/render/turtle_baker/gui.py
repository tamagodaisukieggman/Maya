# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from distutils.util import strtobool
import os
import sys
import importlib

import subprocess
from functools import partial
import json

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

import maya.api.OpenMaya as om2
import maya.cmds as cmds
import maya.mel


from . import command
from . import texture_changer
from mtk.utils import getCurrentSceneFilePath

from . import TITLE
from . import TOOL_NAME

# 開発中はTrue、リリース時にFalse
DEV_MODE = False

if DEV_MODE:
    importlib.reload(command)
    importlib.reload(texture_changer)
else:
    from . import logger


# from tatool.log import ToolLogging, Stage
# stage = Stage.dev
# ToolLogging = ToolLogging(projects=project, toolcategory=toolcategory, target_stage=stage, tool_version=version)
# logger = ToolLogging.getTemplateLogger(tool_title)

_file_path = os.path.dirname(__file__)
UI_FILE = os.path.join(os.path.dirname(__file__),
                       'turtle_baker_ui.ui').replace(os.sep, '/')


# クラス名同じ必要があるので変更する場合はクラス名も変更
# TOOL_NAME = "Mtk_MapBaker"

SUFFIX = "map_type"
TURTLE = "Turtle"

DEFAULT_FILE_NAME = "bake"

DEFAULT_UV_SET = 0
ANTI_ALIASING = 1
GI_FLAG = 0
SHADOW_FLAG = 0
EDGE_DILATION = 5
IMAGE_FORMAT = "tga"
IMAGE_SIZE = 1024
SAMPLE_RAYS = 64

COMBINE_MESH_NAME = "MapBakerCombineMesh"

# DEFAULT_EXPORT_DIRECTORY = "workbench/subdata/bakemaps"


def turtle_check():
    """Turtle 強制読み込み
    :rtype: bool
    """
    cmds.loadPlugin(TURTLE, quiet=True)
    if TURTLE not in cmds.pluginInfo(query=True, listPlugins=True):
        cmds.warning(u"{} プラグインが見つかりません".format(TURTLE))
        cmds.confirmDialog(message=u"{} プラグインが見つかりません".format(TURTLE),
                           title=u'プラグインの確認',
                           button=['OK'],
                           defaultButton='OK',
                           cancelButton="OK",
                           dismissString="OK")
        return False
    return True


class Mtk_MapBaker(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    script_job = None
    _tso_flag = False

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        if not os.path.exists(UI_FILE):
            return
        try:
            self.remove_job()
        except:
            pass

        self.clear_memory()

        # self.remove_job()

        loader = QUiLoader()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        uiFilePath = UI_FILE
        self.UI = loader.load(uiFilePath)

        menuBar = self.menuBar()
        menu = menuBar.addMenu('Help')
        openAct = QtWidgets.QAction('Help Site...', self)
        openAct.triggered.connect(self.openHelp)
        menu.addAction(openAct)

        self.resize(650, 490)
        self.setWindowTitle(TITLE)

        self.setCentralWidget(self.UI)

        # apply_scene_name　適用ボタン
        self.UI.apply_scene_name.clicked.connect(self.apply_scene_name)

        # open_folder ボタン
        image = QtGui.QIcon(':/folder-open.png')
        self.UI.open_folder.setIcon(image)
        self.UI.open_folder.clicked.connect(self.open_file_dialog)

        # opeh_with_explorer ボタン
        self.UI.opeh_with_explorer.clicked.connect(self.open_export_dirctory)

        # bake_maps ボタン
        self.UI.bake_maps.clicked.connect(self.bake_start)
        # self.UI.bake_maps.clicked.connect(self._print)

        # ターゲット、ソースのリスト
        self.UI.target_register.clicked.connect(self.target_list_regist)
        self.UI.target_clear.clicked.connect(self.target_list_clear)

        self.UI.source_register.clicked.connect(self.source_list_regist)
        self.UI.source_clear.clicked.connect(self.source_list_clear)

        # 設定保存　ボタン
        self.UI.save_settings.clicked.connect(self.save_settings)

        # リセット　ボタン
        self.UI.rest_settings.clicked.connect(self.set_default_values)

        # チェック全オフボタン
        self.UI.all_check_off_btn.clicked.connect(self.all_check_off)

        # ビルボード　ボタン
        self.UI.create_billboad.clicked.connect(self.create_billboad)

        # Occusion スイッチ
        # オン、オフで「スケール」アクティブ、ディアクティブ
        self.UI.occlusion_map.clicked.connect(self.occlusion_ck)

        # alpha スイッチ
        # オン、オフで「透過閾値」アクティブ、ディアクティブ
        # self.UI.alpha_map.clicked.connect(self.alpha_ck)

        self.UI.texture_changer_btn.clicked.connect(self.texture_changer_ui)

        self.UI.target_sel_btn.clicked.connect(self.target_select)
        self.UI.source_sel_btn.clicked.connect(self.source_select)

        self.UI.target_source_view_only_btn.clicked.connect(self.set_view)
        self.UI.view_return_btn.clicked.connect(self.view_return)
        self.UI.visible_all_mesh_btn.clicked.connect(self.visible_all_mesh)

        self.config_base_name = "{}".format(TOOL_NAME)

        self.UI.image_format.currentTextChanged.connect(
            self.change_export_file_name)
        self.UI.file_name_line.textChanged.connect(
            self.change_export_file_name)

        self._trackSelectionOrder_flag()
        self.create_job()
        self.read_prefs()
        self.change_export_file_name()

        # if DEV_MODE:
        #     self.all_check_off()
        #     self.UI.occlusion_map.setChecked(1)
        #     self.UI.occlusion_map.setChecked(1)
        #     self.occlusion_ck()
        #     self.UI.vtx_color_ck.setChecked(True)
        #     self.UI.enableGroundButton.setChecked(True)
        #     _test_item = '|mdl_vgt_tree301_002|model|st1|t|t_Shape'
        #     if cmds.objExists(_test_item):
        #         self.UI.target_list.addItem(_test_item)
        #         self.UI.source_list.addItem(_test_item)
        #         self.set_view()

    def openHelp(self, *args):
        """ヘルプサイト表示
        """
        command.open_help_site()

    def visible_all_mesh(self, *args):
        command.visible_all_mesh()

    def get_source_target(self):

        target_count = self.UI.target_list.count()
        source_cont = self.UI.source_list.count()

        targets = []
        sources = []

        hide_nodes = []

        if target_count:
            for i in range(target_count):
                target = self.UI.target_list.item(i).text()
                if cmds.objExists(target):
                    if len(cmds.ls(target)) != 1:
                        cmds.warning(u"同一名のターゲットが複数見つかりました　再度登録しなおしてください")
                        cmds.confirmDialog(message=u"同一名のターゲットが複数見つかりました　再度登録しなおしてください",
                                           title=u'同一名の確認',
                                           button=['OK'],
                                           defaultButton='OK',
                                           cancelButton="OK",
                                           dismissString="OK")
                        return
                    else:
                        hide_node = self.get_hide_node(target)
                        if hide_node:
                            hide_nodes.extend(hide_node)
                        targets.append(target)

        if source_cont:
            for i in range(source_cont):
                source = self.UI.source_list.item(i).text()
                if cmds.objExists(source):
                    if len(cmds.ls(source)) != 1:
                        cmds.warning(u"同一名のソースが複数見つかりました　再度登録しなおしてください")
                        cmds.confirmDialog(message=u"同一名のソースが複数見つかりました　再度登録しなおしてください",
                                           title=u'同一名の確認',
                                           button=['OK'],
                                           defaultButton='OK',
                                           cancelButton="OK",
                                           dismissString="OK")
                        return
                    else:
                        hide_node = self.get_hide_node(source)
                        if hide_node:
                            hide_nodes.extend(hide_node)
                        sources.append(source)

        if not sources and not targets:
            cmds.warning(u"ソース　と　ターゲット　となるメッシュがシーン上に確認できませんでした")
            cmds.confirmDialog(message=u"ソース　と　ターゲット　となるメッシュがシーン上に確認できませんでした",
                               title=u'登録の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        if not sources:
            cmds.warning(u"ソース　となるメッシュがシーン上に確認できませんでした")
            cmds.confirmDialog(message=u"ソース　となるメッシュがシーン上に確認できませんでした",
                               title=u'登録の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        if not targets:
            cmds.warning(u"ターゲット　となるメッシュがシーン上に確認できませんでした")
            cmds.confirmDialog(message=u"ターゲット　となるメッシュがシーン上に確認できませんでした",
                               title=u'登録の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return
        return targets, sources

    def view_return(self, *args):
        # print(self._show_hide_flags.items())
        if self._show_hide_flags:
            command.view_return(self._show_hide_flags)

    def set_view(self, *args):
        targets, sources = self.get_source_target()
        self._show_hide_flags = command.set_view(targets, sources)

    def texture_changer_ui(self, *args):
        self.tex_changer_ui = texture_changer.TextureChanger()
        self.tex_changer_ui.create()

    def _print(self, *args):
        _ui = self.tex_changer_ui
        if _ui:
            print(self.tex_changer_ui.rad_col)
            _sel = cmds.radioCollection(
                self.tex_changer_ui.rad_col, q=True, sl=True)
            if _sel:
                print(cmds.radioButton(_sel, q=True, label=True))

    def _bounding_box_center(self, bb_size):
        return [(bb_size[0][0] + bb_size[0][1]) / 2,
                (bb_size[1][0] + bb_size[1][1]) / 2,
                ((bb_size[2][0] + bb_size[2][1]) / 2)]

    def create_billboad(self):
        _1 = self.UI.create_1.isChecked()
        _2 = self.UI.create_2.isChecked()
        _4 = self.UI.create_4.isChecked()

        source_cont = self.UI.source_list.count()

        if not source_cont:
            cmds.warning(u"ハイモデル（ソース）を登録してから実行してください")
            cmds.confirmDialog(message=u"ハイモデル（ソース）を登録してから実行してください",
                               title=u'登録の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        # if source_cont != 1:
        #     cmds.warning(u"ビルボードを作成する場合は、ハイモデル（ソース）の登録は一つのみです")
        #     return

        sources = []

        if source_cont:
            for i in range(source_cont):
                source = self.UI.source_list.item(i).text()
                if cmds.objExists(source):
                    sources.append(source)

        if not sources:
            cmds.warning(u"ソース　となるメッシュがシーン上に確認できませんでした")
            cmds.confirmDialog(message=u"ソース　となるメッシュがシーン上に確認できませんでした",
                               title=u'登録の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        # source_name = sources[0].split("|")[-1].split("Shape")[0]
        source_name = ""

        _count = 1
        if _2:
            _count = 2
        elif _4:
            _count = 4

        # bb_size = cmds.exactWorldBoundingBox(sources, calculateExactly=True)
        # bb_size = [[bb_size[0],bb_size[3]],
        #             [bb_size[1],bb_size[4]],
        #             [bb_size[2],bb_size[5]]]

        bb_size = cmds.polyEvaluate(
            sources, boundingBox=True, accurateEvaluation=True)

        _planes = command.create_plane_meshes(source_name, bb_size, _count)

        if _planes:
            self.target_list_regist(_planes)

    def clear_memory(self):
        self.tex_changer_ui = ""
        self.export_path = ""
        self.file_name = ""
        self.settings = []
        self.bake_maps = []
        self.targets = []
        self.sources = []
        self._show_hide_flags = None

    def alpha_ck(self):
        _value = self.UI.alpha_map.isChecked()
        if _value:
            self.UI.op_threshold_label.setEnabled(True)
            self.UI.op_threshold_box.setEnabled(True)
        else:
            self.UI.op_threshold_label.setEnabled(False)
            self.UI.op_threshold_box.setEnabled(False)

    def occlusion_ck(self):
        _value = self.UI.occlusion_map.isChecked()
        if _value:
            self.UI.occ_scale_label.setEnabled(True)
            self.UI.occ_scale_box.setEnabled(True)
            self.UI.uv_set_id_ao_label.setEnabled(True)
            self.UI.uv_set_id_AO.setEnabled(True)
            self.UI.vtx_color_ck.setEnabled(True)
            self.UI.enableGroundButton.setEnabled(True)
            self.UI.filter_label.setEnabled(True)
            self.UI.filter_box.setEnabled(True)
        else:
            self.UI.occ_scale_label.setEnabled(False)
            self.UI.occ_scale_box.setEnabled(False)
            self.UI.uv_set_id_ao_label.setEnabled(False)
            self.UI.uv_set_id_AO.setEnabled(False)
            self.UI.vtx_color_ck.setEnabled(False)
            self.UI.enableGroundButton.setEnabled(False)
            self.UI.filter_label.setEnabled(False)
            self.UI.filter_box.setEnabled(False)

    def create_job(self):
        self.script_job = cmds.scriptJob(
            event=("SceneOpened", self.read_prefs))

    def remove_job(self):
        self.view_return()
        if self.script_job is not None:
            cmds.scriptJob(kill=self.script_job, force=True)
            self.script_job = None

    def _trackSelectionOrder_flag(self):
        _tso_flag = cmds.selectPref(q=True, tso=True)
        self._tso_flag = _tso_flag
        if not _tso_flag:
            cmds.selectPref(tso=True)
        return _tso_flag

    def closeEvent(self, event):
        cmds.selectPref(tso=self._tso_flag)
        # if not DEV_MODE:
        self.remove_job()
        try:
            cmds.deleteUI(texture_changer.NAME)
        except Exception as e:
            # print(e)
            pass

    def change_export_file_name(self, *args):

        export_path = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "exportPath"), q=True)

        file_name = self.UI.file_name_line.text()
        _error_flag = False

        for x in file_name:
            if x in u':;/\|,*?"<>':
                _error_flag = True

        if not file_name or _error_flag:

            cmds.warning(u"""「:;/\|,*?"<>」の文字は使用できません！""")
            cmds.confirmDialog(message=u"""「:;/\|,*?"<>」の文字は使用できません！""",
                               title=u'文字の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            file_name = DEFAULT_FILE_NAME
            self.UI.file_name_line.setText(DEFAULT_FILE_NAME)

        file_ext = self.UI.image_format.currentText()

        self.UI.export_path_label.setText(
            "{}_[ {} ].{}".format(file_name, SUFFIX, file_ext))
        # self.UI.file_name_line.setText(file_name)

        # self.UI.export_path_label.setText("{}.{}".format(_export_path,
        #                             self.UI.image_format.currentText()))
        # self.UI.file_name_line.setText(file_name)

    def read_prefs(self):
        self.UI.source_list.clear()
        self.UI.target_list.clear()
        # print("----------------------------------------------------------read_prefs---------------")
        _export_path = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "exportPath"), q=True)
        _file_name = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "fileName"), q=True)
        _settings = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "settings"), q=True)
        _maps = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "maps"), q=True)
        _targets = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "targets"), q=True)
        _sources = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "sources"), q=True)

        bake_vtx_color_flag = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "bake_vertex_color"), q=True)
        ao_bake_uv_set = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "ao_bake_uv_set"), q=True)
        scale_value = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "scale_value"), q=True)
        enable_ground_flag = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "enable_ground_flag"), q=True)
        filterNormalDev = cmds.fileInfo("{}_{}".format(
            self.config_base_name, "filterNormalDev"), q=True)

        # if bake_vtx_color_flag:
        #     self.UI.vtx_color_ck.setChecked(strtobool(bake_vtx_color_flag[0]))
        # if ao_bake_uv_set:
        #     self.UI.uv_set_id_AO.setValue(int(ao_bake_uv_set[0]))
        if bake_vtx_color_flag:
            self.UI.vtx_color_ck.setChecked(strtobool(bake_vtx_color_flag[0]))
        if ao_bake_uv_set:
            self.UI.uv_set_id_AO.setValue(int(ao_bake_uv_set[0]))
        if enable_ground_flag:
            self.UI.enableGroundButton.setChecked(
                strtobool(enable_ground_flag[0]))
        if scale_value:
            self.UI.occ_scale_box.setValue(float(scale_value[0]))
        if filterNormalDev:
            self.UI.filter_box.setValue(float(filterNormalDev[0]))
        if _export_path:
            _export_path = _export_path[0].replace(os.sep, '/')
            self.UI.export_path.setText(_export_path)
            self.UI.export_path_label.setText(_export_path)
        else:
            self.UI.export_path.setText("")
            self.UI.export_path_label.setText("")

        if _file_name:
            _file_name = _file_name[0]
            self.UI.file_name_line.setText(_file_name)
        else:
            self.UI.file_name_line.setText(DEFAULT_FILE_NAME)

        if _settings:
            _settings = _settings[0].split(",")
            self.UI.apply_gi.setChecked(strtobool(_settings[0]))
            self.UI.use_shadow.setChecked(strtobool(_settings[1]))
            self.UI.edge_dilation.setValue(int(_settings[2]))
            self.UI.image_format.setCurrentText(_settings[3])
            self.UI.resolusion.setCurrentText(_settings[4])
            self.UI.sample_rays.setValue(int(_settings[5]))
            self.UI.anti_aliasing.setValue(int(_settings[6]))
            self.UI.uv_set_id.setValue(int(_settings[7]))
            if _maps:
                _maps = _maps[0].split(",")
                self.UI.normal_map.setChecked(strtobool(_maps[0]))
                self.UI.occlusion_map.setChecked(strtobool(_maps[1]))
                self.UI.albedo_map.setChecked(strtobool(_maps[2]))
                self.UI.illumination_map.setChecked(strtobool(_maps[3]))
                self.UI.depth_map.setChecked(strtobool(_maps[4]))
                self.UI.thickness_map.setChecked(strtobool(_maps[5]))
                self.UI.root_map.setChecked(strtobool(_maps[6]))
                self.UI.ws_normal_map.setChecked(strtobool(_maps[7]))
                self.UI.full_shading_map.setChecked(strtobool(_maps[8]))
                self.UI.alpha_map.setChecked(strtobool(_maps[9]))
                self.UI.diffuse_map.setChecked(strtobool(_maps[-1]))
                # self.UI.position_map.setChecked(strtobool(_maps[-1]))
                self.occlusion_ck()
                # self.alpha_ck()

            if _targets:
                _targets = _targets[0].split(",")
                for _target in _targets:
                    if _target and not self.UI.target_list.findItems(_target,
                                                                     QtCore.Qt.MatchExactly):
                        self.UI.target_list.addItem(_target)

            if _sources:
                _sources = _sources[0].split(",")
                for _source in _sources:
                    if _source and not self.UI.source_list.findItems(_source,
                                                                     QtCore.Qt.MatchExactly):
                        self.UI.source_list.addItem(_source)
        else:
            self.set_default_values()

        self.change_export_file_name()

    def set_default_values(self, *args):
        self.UI.file_name_line.setText(DEFAULT_FILE_NAME)
        self.UI.export_path_label.setText("")

        self.UI.apply_gi.setChecked(GI_FLAG)
        self.UI.use_shadow.setChecked(SHADOW_FLAG)
        self.UI.edge_dilation.setValue(EDGE_DILATION)
        self.UI.image_format.setCurrentText("{}".format(IMAGE_FORMAT))
        self.UI.resolusion.setCurrentText("{}".format(IMAGE_SIZE))
        self.UI.sample_rays.setValue(SAMPLE_RAYS)
        self.UI.anti_aliasing.setValue(ANTI_ALIASING)
        self.UI.uv_set_id.setValue(DEFAULT_UV_SET)

        self.UI.normal_map.setChecked(1)
        self.UI.occlusion_map.setChecked(1)
        self.UI.albedo_map.setChecked(1)
        self.UI.diffuse_map.setChecked(1)
        self.UI.illumination_map.setChecked(1)
        self.UI.depth_map.setChecked(1)
        self.UI.thickness_map.setChecked(1)
        self.UI.root_map.setChecked(1)
        self.UI.ws_normal_map.setChecked(1)
        self.UI.full_shading_map.setChecked(1)
        self.UI.alpha_map.setChecked(1)
        # self.UI.position_map.setChecked(1)
        self.occlusion_ck()
        # self.alpha_ck()

        self.UI.target_list.clear()
        self.UI.source_list.clear()
        self.change_export_file_name()

        self.UI.create_1.setChecked(True)
        self.UI.create_2.setChecked(False)
        self.UI.create_4.setChecked(False)

    def all_check_off(self, *args):
        self.UI.normal_map.setChecked(0)
        self.UI.occlusion_map.setChecked(0)
        self.UI.albedo_map.setChecked(0)
        self.UI.diffuse_map.setChecked(0)
        self.UI.illumination_map.setChecked(0)
        self.UI.depth_map.setChecked(0)
        self.UI.thickness_map.setChecked(0)
        self.UI.root_map.setChecked(0)
        self.UI.ws_normal_map.setChecked(0)
        self.UI.full_shading_map.setChecked(0)
        self.UI.alpha_map.setChecked(0)
        # self.UI.position_map.setChecked(0)
        self.occlusion_ck()

    def get_settings(self):
        self.clear_memory()

        export_path = self.UI.export_path.text()
        if export_path:
            self.export_path = export_path

        file_name = self.UI.file_name_line.text()
        if file_name:
            self.file_name = file_name

        # self.UI.export_path_label.setText(self.export_path.replace(os.sep, '/'))

        self.settings.append(self.UI.apply_gi.isChecked())
        self.settings.append(self.UI.use_shadow.isChecked())
        self.settings.append(self.UI.edge_dilation.value())
        self.settings.append(self.UI.image_format.currentText())
        self.settings.append(self.UI.resolusion.currentText())
        self.settings.append(self.UI.sample_rays.value())
        self.settings.append(self.UI.anti_aliasing.value())
        self.settings.append(self.UI.uv_set_id.value())

        self.bake_maps.append(self.UI.normal_map.isChecked())
        self.bake_maps.append(self.UI.occlusion_map.isChecked())
        self.bake_maps.append(self.UI.albedo_map.isChecked())
        self.bake_maps.append(self.UI.illumination_map.isChecked())
        self.bake_maps.append(self.UI.depth_map.isChecked())
        self.bake_maps.append(self.UI.thickness_map.isChecked())
        self.bake_maps.append(self.UI.root_map.isChecked())
        self.bake_maps.append(self.UI.ws_normal_map.isChecked())
        self.bake_maps.append(self.UI.full_shading_map.isChecked())
        self.bake_maps.append(self.UI.alpha_map.isChecked())
        self.bake_maps.append(self.UI.diffuse_map.isChecked())
        # self.bake_maps.append(self.UI.position_map.isChecked())

        target_count = self.UI.target_list.count()
        source_cont = self.UI.source_list.count()

        if target_count:
            for i in range(target_count):
                target = self.UI.target_list.item(i).text()
                if cmds.objExists(target):
                    self.targets.append(target)

        if source_cont:
            for i in range(source_cont):
                source = self.UI.source_list.item(i).text()
                if cmds.objExists(source):
                    self.sources.append(source)

    def save_settings(self):
        self.get_settings()

        _export_path = "{}".format(self.export_path.replace(os.sep, "/"))
        _file_name = "{}".format(self.file_name)

        _settings = "{}".format(
            ",".join(["{}".format(x) for x in self.settings]))
        _maps = "{}".format(",".join(["{}".format(x) for x in self.bake_maps]))
        _targets = "{}".format(
            ",".join(["{}".format(x) for x in self.targets]))
        _sources = "{}".format(
            ",".join(["{}".format(x) for x in self.sources]))

        bake_vtx_color_flag = self.UI.vtx_color_ck.isChecked()
        ao_bake_uv_set = self.UI.uv_set_id_AO.value()
        scale_value = self.UI.occ_scale_box.value()
        enable_ground_flag = self.UI.enableGroundButton.isChecked()
        filterNormalDev = self.UI.filter_box.value()

        # print("**************************save setting")
        # print("_export_path-",_export_path)
        # print("_file_name---",_file_name)
        # print("_settings----",_settings)
        # print("_maps--------",_maps)
        # print("_targets-----",_targets)
        # print("_sources-----",_sources)

        cmds.fileInfo("{}_{}".format(
            self.config_base_name, "exportPath"), _export_path)
        cmds.fileInfo("{}_{}".format(
            self.config_base_name, "fileName"), _file_name)
        cmds.fileInfo("{}_{}".format(
            self.config_base_name, "settings"), _settings)
        cmds.fileInfo("{}_{}".format(self.config_base_name, "maps"), _maps)
        cmds.fileInfo("{}_{}".format(
            self.config_base_name, "targets"), _targets)
        cmds.fileInfo("{}_{}".format(
            self.config_base_name, "sources"), _sources)

        cmds.fileInfo("{}_{}".format(self.config_base_name,
                      "bake_vertex_color"), bake_vtx_color_flag)
        cmds.fileInfo("{}_{}".format(self.config_base_name,
                      "ao_bake_uv_set"), ao_bake_uv_set)
        cmds.fileInfo("{}_{}".format(
            self.config_base_name, "scale_value"), scale_value)
        cmds.fileInfo("{}_{}".format(self.config_base_name,
                      "enable_ground_flag"), enable_ground_flag)
        cmds.fileInfo("{}_{}".format(self.config_base_name,
                      "filterNormalDev"), filterNormalDev)

        # print("+++++++++++++++++++++++++++++++++fileInfo")
        # print("export_path------",cmds.fileInfo("{}_{}".format(self.config_base_name, "exportPath"), q=True))
        # print("_file_name-------",cmds.fileInfo("{}_{}".format(self.config_base_name, "fileName"), q=True))
        # print("_settings--------",cmds.fileInfo("{}_{}".format(self.config_base_name, "settings"), q=True))
        # print("_maps------------",cmds.fileInfo("{}_{}".format(self.config_base_name, "maps"), q=True))
        # print("_targets---------",cmds.fileInfo("{}_{}".format(self.config_base_name, "targets"), q=True))
        # print("_sources---------",cmds.fileInfo("{}_{}".format(self.config_base_name, "sources"), q=True))

        cmds.warning(u"設定を記憶しました　シーンを [　上書き　] 保存しないと　ファイルに書き込まれないのでご注意ください!!")

    def get_poly_meshes(self):
        """現在の選択からメッシュジオメトリのみを抽出
        :return: メッシュノードのリスト
        :rtype: list
        """
        _current_selections = cmds.ls(sl=True, long=True, type="transform")

        if not _current_selections:
            return []

        _target_meshes = []
        for _node in _current_selections:
            # _meshes = cmds.listRelatives(_node, allDescendents=True, fullPath=True, type="mesh")
            _meshes = [x for x in cmds.listRelatives(
                _node, allDescendents=True, fullPath=True, type="mesh")if not cmds.getAttr("{}.intermediateObject".format(x))]
            if _meshes:
                _target_meshes.extend(_meshes)

        if not _target_meshes:
            cmds.warning(u"選択されたノードにメッシュジオメトリがありませんでした")
            cmds.confirmDialog(message=u"選択されたノードにメッシュジオメトリがありませんでした",
                               title=u'選択の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return []

        return _target_meshes

    def source_list_regist(self, _source_meshes=[]):
        if not _source_meshes:
            _source_meshes = self.get_poly_meshes()
        if not _source_meshes:
            return
        for _source_mesh in _source_meshes:
            if not self.UI.source_list.findItems(_source_mesh, QtCore.Qt.MatchExactly):
                self.UI.source_list.addItem(_source_mesh)

        # for _source_mesh in _source_meshes:
        #     _source_mesh = cmds.ls(_source_mesh, shortNames=True)
        #     if _source_mesh:
        #         _source_mesh = _source_mesh[0]
        #         if not self.UI.source_list.findItems(_source_mesh, True):
        #             self.UI.source_list.addItem(_source_mesh)

    def source_list_clear(self):
        self.UI.source_list.clear()

    def target_list_regist(self, _target_meshes=[]):
        if not _target_meshes:
            _target_meshes = self.get_poly_meshes()
        if not _target_meshes:
            return

        for _target_mesh in _target_meshes:
            if not self.UI.target_list.findItems(_target_mesh, QtCore.Qt.MatchExactly):
                self.UI.target_list.addItem(_target_mesh)

        # for _target_mesh in _target_meshes:
        #     _target_mesh = cmds.ls(_target_mesh, shortNames=True)
        #     if _target_mesh:
        #         _target_mesh = _target_mesh[0]
        #         if not self.UI.target_list.findItems(_target_mesh, True):
        #             self.UI.target_list.addItem(_target_mesh)

        # self.UI.target_list.addItems(_target_meshes)

    def target_list_clear(self):
        # for i in range(self.UI.target_list.count()):
        #     print(self.UI.target_list.item(i).text())
        self.UI.target_list.clear()

    def open_export_dirctory(self):
        open_directory = self.UI.export_path.text()
        if not open_directory:
            cmds.warning(u"出力先が設定されてません")
            cmds.confirmDialog(message=u"出力先が設定されてません",
                               title=u'出力先の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return
        try:
            subprocess.Popen(['explorer', os.path.normpath(open_directory)])
        except:
            cmds.warning(open_directory.replace(os.sep, "/") + u" が開けませんでした")
            pass

    def apply_scene_name(self):
        scene_name = getCurrentSceneFilePath()

        if not scene_name:
            cmds.warning(u"シーン名がありません、シーンを保存するか、既存のシーンを開いてください")
            cmds.confirmDialog(message=u"シーン名がありません、シーンを保存するか、既存のシーンを開いてください",
                               title=u'保存の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        file_name = os.path.splitext(os.path.basename(scene_name))[0]
        self.UI.file_name_line.setText(file_name)

    def get_hide_node(self, node):
        _hide_data = []
        # print(node)
        # print(cmds.ls(node))
        _transform = cmds.listRelatives(node, parent=True, path=True)

        if _transform and not cmds.getAttr("{}.visibility".format(_transform[0])):
            _hide_data.append(_transform[0])
            cmds.setAttr("{}.visibility".format(_transform[0]), True)

        if not cmds.getAttr("{}.visibility".format(node)):
            _hide_data.append(node)
            cmds.setAttr("{}.visibility".format(node), True)

        return _hide_data

    def target_select(self):
        target_count = self.UI.target_list.count()

        targets = []

        if target_count:
            for i in range(target_count):
                target = self.UI.target_list.item(i).text()
                if cmds.objExists(target):
                    if len(cmds.ls(target)) != 1:
                        cmds.warning(u"同一名のターゲットが複数見つかりました　再度登録しなおしてください")
                        cmds.confirmDialog(message=u"同一名のターゲットが複数見つかりました　再度登録しなおしてください",
                                           title=u'同一名の確認',
                                           button=['OK'],
                                           defaultButton='OK',
                                           cancelButton="OK",
                                           dismissString="OK")
                        return
                    else:
                        targets.append(target)

        if targets:
            self.select_transform_nodes(targets)

    def select_transform_nodes(self, mesh_nodes):
        _mod = cmds.getModifiers()

        _select_nodes = []
        for mesh_node in mesh_nodes:
            _transform = cmds.listRelatives(mesh_node, parent=True, path=True)
            if _transform:
                _select_nodes.append(_transform[0])
        if _select_nodes:
            if _mod == 4:
                cmds.select(_select_nodes, add=True)
            else:
                cmds.select(_select_nodes, r=True)

    def source_select(self):
        source_cont = self.UI.source_list.count()

        sources = []

        if source_cont:
            for i in range(source_cont):
                source = self.UI.source_list.item(i).text()
                if cmds.objExists(source):
                    if len(cmds.ls(source)) != 1:
                        cmds.warning(u"同一名のソースが複数見つかりました　再度登録しなおしてください")
                        cmds.confirmDialog(message=u"同一名のソースが複数見つかりました　再度登録しなおしてください",
                                           title=u'同一名の確認',
                                           button=['OK'],
                                           defaultButton='OK',
                                           cancelButton="OK",
                                           dismissString="OK")
                        return
                    else:
                        sources.append(source)
        if sources:
            self.select_transform_nodes(sources)

    def bake_start(self):
        file_type_dict = {"tga": 0,
                          "tif": 3,
                          "png": 9}

        _plane = ""
        _plane_name = "map_baker_ground_plane"
        # scene_name = getCurrentSceneFilePath()

        # if not scene_name:
        #     cmds.warning(u"シーンを保存するか、既存のシーンを開いてから実行してください")
        #     return
        bake_vtx_color_flag = self.UI.vtx_color_ck.isChecked()
        enable_ground_flag = self.UI.enableGroundButton.isChecked()
        file_name = self.UI.file_name_line.text()
        export_path = self.UI.export_path.text()

        if not bake_vtx_color_flag:
            if not export_path:
                cmds.warning(u"出力先を設定してからベイクを開始してください")
                cmds.confirmDialog(message=u"出力先を設定してからベイクを開始してください",
                                   title=u'出力先の確認',
                                   button=['OK'],
                                   defaultButton='OK',
                                   cancelButton="OK",
                                   dismissString="OK")
                return

            if not os.path.exists(export_path):
                cmds.warning(u"出力先のフォルダが見つかりませんでした　処理を中止します")
                cmds.confirmDialog(message=u"出力先のフォルダが見つかりませんでした　処理を中止します",
                                   title=u'出力先の確認',
                                   button=['OK'],
                                   defaultButton='OK',
                                   cancelButton="OK",
                                   dismissString="OK")
                return

            # file_name = os.path.splitext(os.path.basename(scene_name))[0]

            _error_flag = False
            for x in file_name:
                if x in u':;/\|,*?"<>':
                    _error_flag = True

            if _error_flag:
                cmds.confirmDialog(message=u"""「:;/\|,*?"<>」の文字は使用できません！""",
                                   title=u'文字の確認',
                                   button=['OK'],
                                   defaultButton='OK',
                                   cancelButton="OK",
                                   dismissString="OK")
                return

        export_path = export_path.replace(os.sep, "/")
        apply_gi = int(self.UI.apply_gi.isChecked())
        use_shadow = int(self.UI.use_shadow.isChecked())
        edge_dilation = self.UI.edge_dilation.value()
        image_format = self.UI.image_format.currentText()
        resolusion = int(self.UI.resolusion.currentText())
        sample_rays = self.UI.sample_rays.value()
        anti_aliasing = self.UI.anti_aliasing.value()

        normal_map_flag = int(self.UI.normal_map.isChecked())
        occlusion_map_flag = int(self.UI.occlusion_map.isChecked())
        albedo_map_flag = int(self.UI.albedo_map.isChecked())
        diffuse_map_flag = int(self.UI.diffuse_map.isChecked())
        illumination_map_flag = int(self.UI.illumination_map.isChecked())
        depth_map_flag = int(self.UI.depth_map.isChecked())
        thickness_map = int(self.UI.thickness_map.isChecked())
        # position_map_flag = int(self.UI.position_map.isChecked())
        root_map_flag = int(self.UI.root_map.isChecked())
        ws_normal_map_flag = int(self.UI.ws_normal_map.isChecked())
        full_shading_map_flag = int(self.UI.full_shading_map.isChecked())
        alpha_map_flag = int(self.UI.alpha_map.isChecked())
        uv_set_id = self.UI.uv_set_id.value()
        ao_bake_uv_set = self.UI.uv_set_id_AO.value()

        opacity_threshold = self.UI.op_threshold_box.value()
        scale_value = self.UI.occ_scale_box.value()
        filterNormalDev = self.UI.filter_box.value()

        # ベイク前にコンバイン処理
        _combine_flag = self.UI.combine_meshes_ck.isChecked()
        _comb = None

        bilinear_filter = 1

        if (not normal_map_flag and
            not occlusion_map_flag and
            not illumination_map_flag and
            not albedo_map_flag and
            not diffuse_map_flag and
            not depth_map_flag and
            not thickness_map and
            # not position_map_flag and
            not root_map_flag and
            not ws_normal_map_flag and
            not full_shading_map_flag and
                not alpha_map_flag):
            cmds.warning(u"「ベイクするマップ」に最低一つのチェックを入れて実行してください")
            cmds.confirmDialog(message=u"「ベイクするマップ」に最低一つのチェックを入れて実行してください",
                               title=u'マップの確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        target_count = self.UI.target_list.count()
        source_cont = self.UI.source_list.count()

        targets = []
        sources = []

        uv_set = []
        ao_uv_set = []
        bake_maps = []
        hide_nodes = []

        if target_count:
            for i in range(target_count):
                target = self.UI.target_list.item(i).text()
                if cmds.objExists(target):
                    if len(cmds.ls(target)) != 1:
                        cmds.warning(u"同一名のターゲットが複数見つかりました　再度登録しなおしてください")
                        cmds.confirmDialog(message=u"同一名のターゲットが複数見つかりました　再度登録しなおしてください",
                                           title=u'同一名の確認',
                                           button=['OK'],
                                           defaultButton='OK',
                                           cancelButton="OK",
                                           dismissString="OK")
                        return
                    else:
                        hide_node = self.get_hide_node(target)
                        if hide_node:
                            hide_nodes.extend(hide_node)
                        targets.append(target)
                        if not uv_set:
                            uv_sets = cmds.polyUVSet(
                                target, allUVSets=True, q=True)
                            if len(uv_sets) > uv_set_id:
                                uv_set.append(uv_sets[uv_set_id])
                            if len(uv_sets) > ao_bake_uv_set:
                                ao_uv_set.append(uv_sets[ao_bake_uv_set])

        if source_cont:
            for i in range(source_cont):
                source = self.UI.source_list.item(i).text()
                if cmds.objExists(source):
                    if len(cmds.ls(source)) != 1:
                        cmds.warning(u"同一名のソースが複数見つかりました　再度登録しなおしてください")
                        cmds.confirmDialog(message=u"同一名のソースが複数見つかりました　再度登録しなおしてください",
                                           title=u'同一名の確認',
                                           button=['OK'],
                                           defaultButton='OK',
                                           cancelButton="OK",
                                           dismissString="OK")
                        return
                    else:
                        hide_node = self.get_hide_node(source)
                        if hide_node:
                            hide_nodes.extend(hide_node)
                        sources.append(source)

        if not sources and not targets:
            cmds.warning(u"ソース　と　ターゲット　となるメッシュがシーン上に確認できませんでした")
            cmds.confirmDialog(message=u"ソース　と　ターゲット　となるメッシュがシーン上に確認できませんでした",
                               title=u'登録の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        if not sources:
            cmds.warning(u"ソース　となるメッシュがシーン上に確認できませんでした")
            cmds.confirmDialog(message=u"ソース　となるメッシュがシーン上に確認できませんでした",
                               title=u'登録の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        if not targets:
            cmds.warning(u"ターゲット　となるメッシュがシーン上に確認できませんでした")
            cmds.confirmDialog(message=u"ターゲット　となるメッシュがシーン上に確認できませんでした",
                               title=u'登録の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        if not command.setting_turtle():
            return

        suffix = ""

        # print(targets," befor comb")
        if _combine_flag:
            _duplicate_nodes = []

            for mesh_node in targets:
                _transform = cmds.listRelatives(
                    mesh_node, parent=True, path=True)
                if _transform:
                    _duplicate_nodes.append(_transform[0])

            _duplicate_node = cmds.duplicate(_duplicate_nodes, rr=True)
            _duplicate_node = cmds.ls(_duplicate_node, l=True)
            _comb = cmds.polyUnite(_duplicate_node, muv=1, cp=True, ch=False)
            _comb = cmds.ls(_comb, l=True)
            targets = cmds.listRelatives(_comb, c=True)
            for _ in _duplicate_node:
                try:
                    cmds.delete(_)
                except:
                    pass

        # print(targets,"  comb")

        # ラジオボタンUIを探して選択されているボタンを元にサフィックスを入れる
        if cmds.radioCollection(texture_changer.RADIO_BTN_COLLECTION_NAME, ex=True):
            _sel = cmds.radioCollection(
                texture_changer.RADIO_BTN_COLLECTION_NAME, q=True, sl=True)
            if _sel != "NONE":
                suffix = cmds.radioButton(_sel, q=True, label=True).split()[0]

        if uv_set:
            uv_set = uv_set[0]
        else:
            uv_set = ""

        if normal_map_flag:
            map_type = "normal_map"

            command.turtle_bake_setup(exprot_path=export_path,
                                      file_name=file_name,
                                      map_type=map_type,
                                      targets=targets,
                                      sources=sources,
                                      resolusion=resolusion,
                                      image_format=image_format,
                                      edge_dilation=edge_dilation,
                                      anti_aliasing=anti_aliasing,
                                      normal_map_flag=1,
                                      bilinear_filter=bilinear_filter,
                                      uv_set=uv_set,
                                      alpha_map_flag=0,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            # logger.info("{}-baked".format(map_type))

        if ws_normal_map_flag:
            map_type = "ws_normal_map"
            command.turtle_bake_setup(exprot_path=export_path,
                                      file_name=file_name,
                                      map_type=map_type,
                                      targets=targets,
                                      sources=sources,
                                      resolusion=resolusion,
                                      image_format=image_format,
                                      edge_dilation=edge_dilation,
                                      anti_aliasing=anti_aliasing,
                                      normal_map_flag=1,
                                      bilinear_filter=bilinear_filter,
                                      uv_set=uv_set,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            # logger.info("{}-baked".format(map_type))

        if full_shading_map_flag:
            map_type = "full_shading_map"
            command.turtle_bake_setup(exprot_path=export_path,
                                      file_name=file_name,
                                      map_type=map_type,
                                      targets=targets,
                                      sources=sources,
                                      apply_gi=apply_gi,
                                      resolusion=resolusion,
                                      image_format=image_format,
                                      edge_dilation=edge_dilation,
                                      anti_aliasing=anti_aliasing,
                                      full_shading_flag=1,
                                      use_shadow=use_shadow,
                                      bilinear_filter=bilinear_filter,
                                      uv_set=uv_set,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            # logger.info("{}-baked".format(map_type))

        if albedo_map_flag:
            map_type = "albedo_map"
            command.turtle_bake_setup(exprot_path=export_path,
                                      file_name=file_name,
                                      map_type=map_type,
                                      targets=targets,
                                      sources=sources,
                                      resolusion=resolusion,
                                      image_format=image_format,
                                      edge_dilation=edge_dilation,
                                      anti_aliasing=anti_aliasing,
                                      albedo_map_flag=1,
                                      use_shadow=use_shadow,
                                      bilinear_filter=bilinear_filter,
                                      uv_set=uv_set,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            # logger.info("{}-baked".format(map_type))

        if diffuse_map_flag:
            map_type = "diffuse_map"
            command.turtle_bake_setup(exprot_path=export_path,
                                      file_name=file_name,
                                      map_type=map_type,
                                      targets=targets,
                                      sources=sources,
                                      resolusion=resolusion,
                                      image_format=image_format,
                                      edge_dilation=edge_dilation,
                                      anti_aliasing=anti_aliasing,
                                      diffuse_map_flag=1,
                                      use_shadow=use_shadow,
                                      bilinear_filter=bilinear_filter,
                                      uv_set=uv_set,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            # logger.info("{}-baked".format(map_type))

        if illumination_map_flag:
            map_type = "illumination_map"
            command.turtle_bake_setup(exprot_path=export_path,
                                      file_name=file_name,
                                      map_type=map_type,
                                      targets=targets,
                                      sources=sources,
                                      apply_gi=apply_gi,
                                      resolusion=resolusion,
                                      image_format=image_format,
                                      edge_dilation=edge_dilation,
                                      anti_aliasing=anti_aliasing,
                                      illumination_map_flag=1,
                                      use_shadow=use_shadow,
                                      bilinear_filter=bilinear_filter,
                                      uv_set=uv_set,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            # logger.info("{}-baked".format(map_type))

        if depth_map_flag:
            map_type = "depth_map"
            command.turtle_bake_setup(exprot_path=export_path,
                                      file_name=file_name,
                                      map_type=map_type,
                                      targets=targets,
                                      sources=sources,
                                      resolusion=resolusion,
                                      image_format=image_format,
                                      edge_dilation=edge_dilation,
                                      anti_aliasing=anti_aliasing,
                                      depth_map_flag=1,
                                      use_shadow=use_shadow,
                                      bilinear_filter=bilinear_filter,
                                      uv_set=uv_set,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            # logger.info("{}-baked".format(map_type))

        # ノーマルマップのアルファチャンネルにステンシルが格納されるため
        # それを使うときのため新たに用意
        if alpha_map_flag:
            map_type = "alpha_map"
            command.turtle_bake_setup(exprot_path=export_path,
                                      file_name=file_name,
                                      normal_map_flag=1,
                                      map_type=map_type,
                                      targets=targets,
                                      sources=sources,
                                      resolusion=resolusion,
                                      image_format=image_format,
                                      edge_dilation=0,
                                      anti_aliasing=anti_aliasing,
                                      use_shadow=0,
                                      bilinear_filter=bilinear_filter,
                                      alpha_map_flag=alpha_map_flag,
                                      uv_set=uv_set,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            # logger.info("{}-baked".format(map_type))

        if occlusion_map_flag:

            if enable_ground_flag:
                bb_size = cmds.polyEvaluate(
                    sources, boundingBox=True, accurateEvaluation=True)
                _plane = command.ground_plane(_plane_name, bb_size)

            if ao_uv_set:
                ao_uv_set = ao_uv_set[0]
            else:
                ao_uv_set = ""

            occ_shader, _sets = command.create_occ_sampler()

            # if not use_shadow:
            #     cmds.setAttr("{}.selfOcclusion".format(occ_shader), 0)
            # else:
            #     cmds.setAttr("{}.selfOcclusion".format(occ_shader), 1)

            cmds.setAttr("{}.selfOcclusion".format(occ_shader), 2)
            cmds.setAttr("{}.type".format(occ_shader), 0)

            cmds.setAttr("{}.uniformSampling".format(occ_shader), 0)
            # cmds.setAttr("{}.enableAdaptiveSampling".format(occ_shader), 1)
            cmds.setAttr("{}.scale".format(occ_shader), scale_value)
            cmds.setAttr("{}.coordSys".format(occ_shader), 2)
            cmds.setAttr("{}.enableAdaptiveSampling".format(occ_shader), 0)

            max_sample_rays = sample_rays * 2
            cmds.setAttr("{}.useTransparency".format(occ_shader, lock=False))
            cmds.setAttr("{}.minSamples".format(occ_shader), sample_rays)
            cmds.setAttr("{}.maxSamples".format(occ_shader), max_sample_rays)
            # cmds.setAttr("{}.useTransparency".format(occ_shader, 1))
            cmds.setAttr("{}.bendNormals".format(occ_shader, 0))

            maya.mel.eval('setAttr "{}.useTransparency" 1;'.format(occ_shader))
            map_type = "occlusion_map"

            if bake_vtx_color_flag:
                command.setting_turtle(False)
                command.turtle_vertex_bake_setup(
                    targets=targets,
                    sources=sources,
                    apply_gi=apply_gi,
                    custom_shader_use_flag=1,
                    custom_shader=occ_shader,
                    use_shadow=use_shadow,
                    scale_value=scale_value,
                    ground_plane=_plane,
                    filterNormalDev=filterNormalDev,
                )
            else:
                cmds.setAttr("{}.maxDistance".format(occ_shader), 1.0)
                if _plane:
                    sources.append(_plane)
                command.turtle_bake_setup(exprot_path=export_path,
                                          file_name=file_name,
                                          map_type=map_type,
                                          targets=targets,
                                          sources=sources,
                                          apply_gi=apply_gi,
                                          resolusion=resolusion,
                                          image_format=image_format,
                                          edge_dilation=edge_dilation,
                                          anti_aliasing=anti_aliasing,
                                          use_shadow=use_shadow,
                                          bilinear_filter=bilinear_filter,
                                          custom_shader_use_flag=1,
                                          custom_shader=occ_shader,
                                          uv_set=ao_uv_set,
                                          opacity_threshold=opacity_threshold,
                                          suffix=suffix,
                                          )
                if ao_uv_set:
                    for target in targets:
                        # command.change_uv_link(target)
                        command.vertex_color_off(target)
            if _plane:
                cmds.delete(occ_shader, _sets, _plane)
            else:
                cmds.delete(occ_shader, _sets)

            # logger.info("{}-baked".format(map_type))

        # if position_map_flag:
        #     _position_map_shader, _samlper_info = command.create_position_map_shader()
        #     map_type = "position_map"
        #     command.turtle_bake_setup(exprot_path = export_path,
        #                         file_name = file_name,
        #                         map_type = map_type,
        #                         targets = targets,
        #                         sources = sources,
        #                         resolusion = resolusion,
        #                         image_format = image_format,
        #                         edge_dilation = edge_dilation,
        #                         anti_aliasing = anti_aliasing,
        #                         bilinear_filter = bilinear_filter,
        #                         custom_shader_use_flag = 1,
        #                         custom_shader = _position_map_shader,
        #                         uv_set = uv_set)
        #     cmds.delete(_position_map_shader, _samlper_info)
        #     logger.info("{}-baked".format(map_type))

        if thickness_map:
            _thick_shader, _thick = command.create_thickness_shader()
            cmds.setAttr("{}.numberOfRays".format(_thick), sample_rays)
            cmds.setAttr("{}.coneAngle".format(_thick), 80)
            cmds.setAttr("{}.maxDistance".format(_thick), 0.5)
            map_type = "thickness_map"
            command.turtle_bake_setup(exprot_path=export_path,
                                      file_name=file_name,
                                      map_type=map_type,
                                      targets=targets,
                                      sources=sources,
                                      resolusion=resolusion,
                                      image_format=image_format,
                                      edge_dilation=edge_dilation,
                                      anti_aliasing=anti_aliasing,
                                      bilinear_filter=bilinear_filter,
                                      custom_shader_use_flag=1,
                                      custom_shader=_thick_shader,
                                      uv_set=uv_set,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            cmds.delete(_thick_shader, _thick)
            # logger.info("{}-baked".format(map_type))

        if root_map_flag:
            map_type = "root_map"
            _ramp, _place2d, _ramp_shader = command.create_ramp_shader()
            command.turtle_bake_setup(exprot_path=export_path,
                                      file_name=file_name,
                                      map_type=map_type,
                                      targets=targets,
                                      sources=sources,
                                      resolusion=resolusion,
                                      image_format=image_format,
                                      edge_dilation=edge_dilation,
                                      anti_aliasing=anti_aliasing,
                                      bilinear_filter=bilinear_filter,
                                      custom_shader_use_flag=1,
                                      custom_shader=_ramp_shader,
                                      uv_set=uv_set,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            cmds.delete(_ramp, _place2d, _ramp_shader)
            # logger.info("{}-baked".format(map_type))

        if hide_nodes:
            [cmds.setAttr("{}.visibility".format(x), False)
             for x in hide_nodes]

        if _comb:
            for _ in _comb:
                try:
                    cmds.delete(_)
                except:
                    pass

    def open_file_dialog(self):
        current_directory = getCurrentSceneFilePath()

        if not current_directory:
            current_directory = cmds.workspace(q=True, active=True)
        else:
            current_directory = os.path.split(current_directory)[0]

        if not current_directory:
            current_directory = os.getenv("HOME")

        result = cmds.fileDialog2(startingDirectory=current_directory,
                                  fileMode=3,
                                  dialogStyle=2,
                                  okCaption=u"ディレクトリ選択",
                                  caption=u"出力先ディレクトリを選択してください")
        if result:
            export_path = result[0]
            self.UI.export_path.setText(export_path.replace(os.sep, '/'))
        self.change_export_file_name()


def main():

    # app = QtWidgets.QApplication.instance()

    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == TOOL_NAME:
            _obj.close()
            del _obj

    ui = Mtk_MapBaker()

    if not os.path.exists(UI_FILE):
        cmds.warning(u"UI ファイルが見つかりません")
        return

    if turtle_check():
        ui.show()
        if not DEV_MODE:
            logger.send_launch(u'ツール起動')
