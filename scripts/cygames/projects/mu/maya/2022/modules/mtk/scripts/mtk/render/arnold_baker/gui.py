# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from functools import partial
import os
import sys
import importlib

import subprocess

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

import maya.OpenMaya as om
import maya.cmds as cmds
from mtk.utils import getCurrentSceneFilePath

from . import command
from . import TITLE
from . import TOOL_NAME
from . import AUTOMATION_TOOL_KIT
from . import PYSBS


# 開発中はTrue、リリース時にFalse
DEV_MODE = True

if DEV_MODE:
    importlib.reload(command)
else:
    from . import logger

ARNOLD_PLUGIN_NAME = "mtoa"


UI_FILE = os.path.join(os.path.dirname(__file__), 'arnold_baker_ui.ui').replace(os.sep, '/')

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

FILE_TYPES = [
    "tga",
    "png",
    "tiff",
    "exr",
]

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


DIR_NAME = "MapBakerArnold"
FILE_NAME = "ar_bake"


def _confirm_dialog(message, title=""):
    if not title:
        title = TITLE
    rflag = False
    flag = True
    while flag:
        result = cmds.confirmDialog(title=title,
                                    messageAlign="center",
                                    message=message,
                                    button=["OK", "Cansel"],
                                    defaultButton="OK",
                                    cancelButton="Cansel",
                                    dismissString="Cansel")
        if result == "Cansel":
            rflag = False
            flag = False
        else:
            rflag = True
            flag = False
    return rflag


def _message_dialog(message, title=""):
    if not title:
        title = TITLE

    cmds.confirmDialog(
        message=message,
        title=title,
        button=['OK'],
        defaultButton='OK',
        cancelButton="OK",
        dismissString="OK")

    print(u"{}".format(message))


def check_plugin(plugin_name):
    cmds.loadPlugin(plugin_name, quiet=True)
    if plugin_name not in cmds.pluginInfo(query=True, listPlugins=True):
        cmds.warning(u"{} プラグインが見つかりません".format(plugin_name))
        _message_dialog(u"{} プラグインが見つかりません".format(plugin_name))
        return False
    return True


def get_scene_name():
    """シーン名を取得
    cmds で取得できないシーンがあったのでOpenMayaでも取得を試みる
    ただし、OpenMayaの場合は開いていなくても文字列は空にならないので
    そのための対処
    """
    scene_name = getCurrentSceneFilePath()
    if not scene_name:
        scene_name = om.MFileIO.currentFile()

    if len(scene_name.split(".")) < 2:
        scene_name = ""

    return scene_name


def get_selections():
    sel = cmds.ls(sl=True, l=True, type="transform")
    return sel


class MutsunokamiMapBakerArnold(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    scene_name = ""
    _show_hide_flags = dict()

    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)
        loader = QUiLoader()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.get_scene_name()
        uiFilePath = UI_FILE
        self.UI = loader.load(uiFilePath)

        self.resize(650, 480)
        self.setWindowTitle(TITLE)

        self.setCentralWidget(self.UI)

        # open_folder ボタン
        image = QtGui.QIcon(':/folder-open.png')
        self.UI.open_folder.setIcon(image)
        self.UI.open_folder.clicked.connect(self.open_file_dialog)

        self.UI.rest_settings.clicked.connect(self.reset_btn)

        self.UI.target_register.clicked.connect(partial(self.list_regist, "target"))
        self.UI.source_register.clicked.connect(partial(self.list_regist, "source"))

        self.UI.target_clear.clicked.connect(partial(self.list_clear, "target"))
        self.UI.source_clear.clicked.connect(partial(self.list_clear, "source"))

        self.UI.target_sel_btn.clicked.connect(partial(self.node_select, "target"))
        self.UI.source_sel_btn.clicked.connect(partial(self.node_select, "source"))

        self.UI.occlusion_map.clicked.connect(self.black_to_back_ground)

        # opeh_with_explorer ボタン
        self.UI.opeh_with_explorer.clicked.connect(self.open_export_dirctory)

        # self.UI.tga_convert.clicked.connect(self.debug_mode)
        self.UI.apply_scene_name.clicked.connect(self.apply_scene_name)
        # self.UI.file_name_line.textChanged.connect(self.change_export_file_name)
        self.UI.assign_shader.clicked.connect(self.assign_shader_ck)

        self.UI.bake_maps.clicked.connect(self.bake)

        self.UI.apply_random_vtx_color_btn.clicked.connect(self.apply_random_vertex_color_polygon_shell)

        self.build_resolution_cbox()
        # self.build_file_type_cbox()
        self.build_filter_type_cbox()

        self.set_default_setting()

    def black_to_back_ground(self):
        _value = self.UI.occlusion_map.isChecked()
        if _value:
            self.UI.black_to_back_ck.setEnabled(True)
        else:
            self.UI.black_to_back_ck.setEnabled(False)

    def apply_random_vertex_color_polygon_shell(self, *args):
        selection = cmds.ls(sl=True, type="transform")
        if not selection:
            return
        _m = u"現在選択されている [ {} ] 個のメッシュの\n".format(len(selection))
        _m += u"ポリゴンシェルに対して"
        _m += u"ランダムな頂点カラーを割り当てます\n\n"
        _m += u"よろしいですか？"
        if _confirm_dialog(_m):
            command.set_func()

    def apply_scene_name(self):
        scene_name = getCurrentSceneFilePath()

        if not self.scene_name:
            _message_dialog(u"シーンが開かれていないか、保存されてません")
            return

        file_name = os.path.splitext(os.path.basename(scene_name))[0]
        self.UI.file_name_line.setText(file_name)

    def open_file_dialog(self):
        current_directory = os.path.split(self.scene_name)[0]
        result = cmds.fileDialog2(startingDirectory=current_directory,
                                  fileMode=3,
                                  dialogStyle=2,
                                  okCaption=u"ディレクトリ選択",
                                  caption=u"出力先ディレクトリを選択してください")

        if result:
            export_path = result[0]
            self.UI.export_path.setText(export_path.replace(os.sep, '/'))

    def assign_shader_ck(self, *args):
        _flag = self.UI.assign_shader.isChecked()
        if not _flag:
            self.UI.delete_shader.setChecked(False)
            self.UI.delete_shader.setEnabled(False)
        else:
            self.UI.delete_shader.setEnabled(True)
            self.UI.delete_shader.setChecked(True)

    def get_scene_name(self):
        scene_name = get_scene_name()
        self.scene_name = scene_name.replace(os.sep, '/')

    def build_resolution_cbox(self):
        for res in RESOLUTIONS:
            self.UI.resolusion.addItem("{}".format(res))

    def build_file_type_cbox(self):
        for _type in FILE_TYPES:
            self.UI.image_format.addItem(_type)

    def build_filter_type_cbox(self):
        for _type in FILTER_TYPES:
            self.UI.filter_types.addItem(_type)

    def reset_btn(self, *args):
        self.UI.resolusion.setCurrentIndex(6)
        self.UI.filter_types.setCurrentIndex(5)
        # self.UI.image_format.setCurrentIndex(0)

        self.UI.sampling.setValue(3)
        self.UI.filter_width.setValue(2.0)
        self.UI.normal_offset.setValue(1000.0)
        self.UI.extend_edges.setChecked(True)
        # self.UI.aovs.setChecked(False)
        self.UI.uv_set_id.setValue(0)

    def set_default_setting(self, *args):
        self.reset_btn()
        # self.UI.export_path_label.setText("")
        self.UI.export_path.setText("")
        self.UI.file_name_line.setText(FILE_NAME)

    def list_regist(self, flag="target"):
        sel = cmds.ls(sl=True, l=True)

        transforms = []
        for s in sel:
            meshes = cmds.listRelatives(s, ad=True, f=True, type="mesh")
            parents = cmds.listRelatives(meshes, p=True, f=True, type="transform")
            for parent in parents:
                if parent not in transforms:
                    transforms.append(parent)

        if not transforms:
            _message_dialog(u"選択対象にメッシュがありません")
            return

        if flag == "target":
            current_list = self.UI.target_list
        else:
            current_list = self.UI.source_list

        for t in transforms:
            if not current_list.findItems(t, QtCore.Qt.MatchExactly):
                current_list.addItem(t)

    def target_list_regist(self):
        sel = cmds.ls(sl=True, l=True, type="transform")
        if not sel:
            return
        for s in sel:
            if not self.UI.target_list.findItems(s, QtCore.Qt.MatchExactly):
                self.UI.target_list.addItem(s)

    def source_list_regist(self):
        sel = cmds.ls(sl=True, l=True, type="transform")
        if not sel:
            return
        for s in sel:
            if not self.UI.source_list.findItems(s, QtCore.Qt.MatchExactly):
                self.UI.source_list.addItem(s)

    def list_clear(self, flag="target"):
        if flag == "target":
            current_list = self.UI.target_list
        else:
            current_list = self.UI.source_list
        current_list.clear()

    def target_list_clear(self):
        self.UI.target_list.clear()

    def source_list_clear(self):
        self.UI.source_list.clear()

    def get_list_node(self, flag="target"):
        result = []
        if flag == "target":
            current_list = self.UI.target_list
        else:
            current_list = self.UI.source_list

        count = current_list.count()
        if count:
            for i in range(count):
                target = current_list.item(i).text()
                if cmds.objExists(target):
                    result.append(target)
                else:
                    cmds.warning("[ {} ] Not Exists".format(target))
        return result

    def node_select(self, flag="target"):
        nodes = self.get_list_node(flag)

        if nodes:
            cmds.select(nodes, r=True)

    def set_up_bake(self, target_nodes):
        # _all_transform = cmds.ls(type="transform", long=True)
        _all_transform = cmds.ls(assemblies=True, l=True)
        self._show_hide_flags = {}
        for _transform in _all_transform:

            self._show_hide_flags[_transform] = cmds.getAttr("{}.v".format(_transform))
            cmds.setAttr("{}.v".format(_transform), 0)

        for node_longname in target_nodes:
            for name in node_longname.split("|"):
                if name:
                    cmds.setAttr("{}.v".format(name), 1)

    def debug_mode(self):
        self.UI.target_list.clear()
        self.UI.source_list.clear()
        # self.UI.export_path.setText("D:/ando/D_Drive/MapBaker_test_scene_from_Gohto/0727_Marmoset_Hair_AO/an_bake/test2")
        # self.UI.target_list.addItem(u'|aoBake_target_grp_main')
        # for i in [u'|aoBake_source_grp|jdWig_top', u'|aoBake_source_grp|wig_Bun']:
        #     self.UI.source_list.addItem(i)

        self.UI.export_path.setText("D:/ando/D_Drive/MapBaker_test_scene_from_Gohto/0727_Marmoset_Hair_AO/an_bake/test")
        self.UI.target_list.addItem(u'|group1|target10')
        self.UI.source_list.addItem(u'|group1|source10')

        # self.UI.export_path.setText("D:/ando/D_Drive/MapBaker_test_scene_from_Gohto/0727_Marmoset_Hair_AO/an_bake/test")
        # self.UI.target_list.addItem(u'|polySurface1303')
        # self.UI.source_list.addItem(u'|directionalLight2')

        self.UI.normal_map.setChecked(False)
        self.UI.flow_map.setChecked(False)
        self.UI.occlusion_map.setChecked(True)
        # self.UI.albedo_map.setChecked(False)
        self.UI.root_map.setChecked(False)
        self.UI.depth_map.setChecked(False)
        self.UI.alpha_map.setChecked(False)
        self.UI.id_map.setChecked(False)

        self.UI.assign_shader.setChecked(False)

        # self.UI.export_path.setText("D:/ando/D_Drive/MapBaker_test_scene_from_Gohto/0727_Marmoset_Hair_AO/an_bake/test")
        # self.UI.target_list.addItem(u'|pPlane1')
        # self.UI.source_list.addItem(u'|pSphere1')

        self.UI.resolusion.setCurrentIndex(4)

    def remove_exr(self, path, nodes):
        target_meshes = []
        for node in nodes:
            shape = cmds.listRelatives(node, s=True, path=True)
            if shape:
                target_meshes.append(shape[0])

        if target_meshes:
            for node in target_meshes:
                exr = os.path.join(path, "{}.exr".format(node))
                if os.path.exists(exr):
                    os.remove(exr)

    def open_export_dirctory(self):
        open_directory = self.UI.export_path.text()
        if not open_directory:
            _message_dialog(u"出力先が設定されてません")
            return
        try:
            subprocess.Popen(['explorer', os.path.normpath(open_directory)])
        except:
            cmds.warning(open_directory.replace(os.sep, "/") + u" が開けませんでした")
            pass

    def check_file_name(self):
        file_name = self.UI.file_name_line.text()

        _error_flag = False
        for x in file_name:
            if x in u':;/\|,*?"<>':
                _error_flag = True

        if _error_flag:
            _confirm_dialog(u"""「:;/\|,*?"<>」の文字は使用できません！""")
            return False
        return file_name

    def bake(self, *args):
        export_path = self.UI.export_path.text().replace(os.sep, '/')

        if not export_path:
            _message_dialog(u"出力パスが設定されていません")
            return

        if not os.path.exists(export_path):
            _message_dialog(u"出力パスが見つかりません")
            return

        target = self.get_list_node("target")

        if not target:
            _message_dialog(u"ターゲットがありません")
            return

        source = self.get_list_node("source")
        if not source:
            _message_dialog(u"ソースがありません")
            return

        file_name = self.check_file_name()
        if not file_name:
            return

        # image_format = self.UI.image_format.currentText()
        resolusion = int(self.UI.resolusion.currentText())
        filter = self.UI.filter_types.currentText()
        aa_samples = self.UI.sampling.value()
        filter_width = self.UI.filter_width.value()
        normal_offset = self.UI.normal_offset.value()
        uv_set_id = self.UI.uv_set_id.value()
        extend_edges = self.UI.extend_edges.isChecked()
        # enable_aovs = self.UI.aovs.isChecked()
        enable_aovs = False
        assign_shader = self.UI.assign_shader.isChecked()
        delete_shader = self.UI.delete_shader.isChecked()

        # シャドウマップベイク用
        # 背景が黒であってほしい場合にチェックが入っている
        # シャドウマップ以外では使わない
        black_bg_flag = self.UI.black_to_back_ck.isChecked()

        # UV 切り抜きフラグ
        _crop_uv_flag = self.UI.uv_crop_ck.isChecked()

        export_flags = [
            self.UI.normal_map.isChecked(),
            self.UI.flow_map.isChecked(),
            self.UI.occlusion_map.isChecked(),
            # self.UI.albedo_map.isChecked(),
            self.UI.root_map.isChecked(),
            self.UI.depth_map.isChecked(),
            self.UI.alpha_map.isChecked(),
            self.UI.id_map.isChecked(),
        ]

        export_map_types = [
            "Normal",
            "Flow",
            "AO",
            # "Albedo",
            "Root",
            "Depth",
            "Alpha",
            "Vcolor",
        ]

        if sum(export_flags) == 0 and assign_shader:
            _message_dialog(u"マップの出力チェックボックスが全てオフです")
            return

        export_maps = []
        for map_type, is_export in zip(export_map_types, export_flags):
            if is_export:
                export_maps.append(map_type)

        arn = command.ArnoldRenderTextureBake(
            export_path,
            target,
            source,
            uv_set_id,
            assign_shader
        )

        arn.arnold_render_textures(
            file_name,
            export_maps,
            resolusion,
            aa_samples,
            filter,
            filter_width,
            normal_offset,
            enable_aovs,
            extend_edges,
            delete_shader,
            black_bg_flag,
            _crop_uv_flag
        )
        if not DEV_MODE:
            logger.info(u'File Name : {}'.format(file_name))
            logger.info(u'Export Maps : {}'.format(",".join(export_maps)))
            logger.info(u'Resolusion : {}'.format(resolusion))
            logger.info(u'AA Samples : {}'.format(aa_samples))
            logger.info(u'Filter : {}'.format(filter))
            logger.info(u'Filter Width : {}'.format(filter_width))
            logger.info(u'Normal Offset : {}'.format(normal_offset))
            # logger.info(u'Enable AOVs : {}'.format(enable_aovs))
            logger.info(u'Extend Edges : {}'.format(extend_edges))
            logger.info(u'Delete Shader : {}'.format(delete_shader))

    def end_procces(self):
        if not self._show_hide_flags:
            return
        for name, value in self._show_hide_flags.items():
            cmds.setAttr("{}.v".format(name), value)


def main():

    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == TOOL_NAME:
            _obj.close()
            del _obj

    # scene_name = get_scene_name()
    # if not scene_name:
    #     _message_dialog(u"シーンを開くか、現在のシーンを保存してから実行してください")
    #     if not DEV_MODE:
    #         logger.warning(u'Not Open Scene File')
    #     return

    if not os.path.exists(UI_FILE):
        cmds.error(u"UI ファイルが見つかりません")
        if not DEV_MODE:
            logger.error(u'Not Found UI FIle')
        return

    if not os.path.exists(AUTOMATION_TOOL_KIT):
        _m = u"Substance Automation Toolkit が見つかりません"
        _m += u"\nEXR ファイルは TGA ファイルに変換されません"
        _message_dialog(_m)
        if not DEV_MODE:
            logger.warning(u'Not Found Substance Automation Toolkit')

    if not os.path.exists(PYSBS):
        _m = u"Pysbs が見つかりません"
        _m += u"\nEXR ファイルは TGA ファイルに変換されません"
        _message_dialog(_m)
        if not DEV_MODE:
            logger.warning(u'Not Found Pysbs Module')

    ui = MutsunokamiMapBakerArnold()
    if check_plugin(ARNOLD_PLUGIN_NAME):
        ui.show()
        if not DEV_MODE:
            logger.send_launch(u'ツール起動')
    else:
        if not DEV_MODE:
            logger.error(u'Not Found [ mtoa ] Plugin')
