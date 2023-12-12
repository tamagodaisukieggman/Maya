# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import yaml
from functools import partial
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# shibokenの読み込み
try:
    import shiboken2 as shiboken
except:
    import shiboken

import pymel.core as pm
import maya.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
import shr.file.character_exporter.command as command
from shr.file.character_exporter.ue import ue_gui_utils, ue_importer

# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")
UIFILEPATH = filePath + "/ui/anim_gui.ui"


class AnimToolMainTool(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    _instance = None

    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return "{}.{}".format(self.__module__, self.__class__.__name__)

    def __init__(self, parent=None):
        super(AnimToolMainTool, self).__init__(parent)
        self.setObjectName("AnimationExporter")

        self.delete_instances()
        self.exporter = command.Exporter("animation")
        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)

        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # infoがないと配列の中に空の文字列が入っている
        if cmds.fileInfo("animation_export_path", q=True) == []:
            # UIの情報が無かったらCurrentPathで初期化
            self.exporter.initialize_ui_info()
        self.load_ui_info()

        # UIの初期化
        ue_gui_utils.initialize_ue_import_settings(self.UI)

        # ue用uiのinitialize
        initialize_ue = partial(ue_gui_utils.initialize_ue_import_settings, self.UI)
        self.UI.check_connection_btn.clicked.connect(initialize_ue)

        # connect
        self.UI.get_directory_btn.clicked.connect(self.exec_get_directory)
        self.UI.export_btn.clicked.connect(self.exec_export)
        self.UI.export_current_directory_btn.clicked.connect(
            self.export_current_directory
        )
        self.UI.directory_txt.textChanged.connect(self.save_ui_info)
        self.UI.filename_txt.textChanged.connect(self.save_ui_info)

        # importer connected
        self.UI.Import_current_data_btn.clicked.connect(self.exec_import_current_dir)
        self.UI.Import_directory_btn.clicked.connect(self.exec_import_dir)
        self.UI.import_selected_files_btn.clicked.connect(
            self.exec_import_selected_files
        )

    def delete_instances(self):
        workspace_control_name = self.objectName() + "WorkspaceControl"
        if cmds.workspaceControl(workspace_control_name, exists=True):
            pm.deleteUI(workspace_control_name)

    def dockCloseEventTriggered(self):
        self.delete_instances()

    # -------------------------------
    # UIの情報保存/読み込み
    # -------------------------------

    def save_ui_info(self):
        cmds.fileInfo("animation_export_path", self.UI.directory_txt.text())
        cmds.fileInfo("animation_export_name", self.UI.filename_txt.text())

    def load_ui_info(self):
        self.UI.directory_txt.setText(
            cmds.fileInfo("animation_export_path", query=True)[0]
        )
        self.UI.filename_txt.setText(
            cmds.fileInfo("animation_export_name", query=True)[0]
        )

    # -------------------------------
    # ボタン押したときの処理
    # -------------------------------
    def exec_get_directory(self):
        # 階層を取得してdirectory_txtへ入れる
        folder_directory = cmds.fileDialog2(fm=2, dir=self.UI.directory_txt.text())[0]
        self.UI.directory_txt.setText(folder_directory)
        self.save_ui_info()

    def exec_export(self):
        export_directory = self.UI.directory_txt.text()
        export_name = self.UI.filename_txt.text()
        self.exporter.export(export_directory, export_name)

    def export_current_directory(self):
        self.exporter.export_by_currently_scene_path(self.UI.filename_txt.text())

    def exec_import_dir(self):
        basicFilter = "*.fbx"
        skel_name = ue_gui_utils.get_skeleton_name(self.UI)
        dir_path = cmds.fileDialog2(fileFilter=basicFilter, fm=3)[0]

        for current_dir, sub_dirs, files_list in os.walk(dir_path):
            for file_name in files_list:
                fbx_path = os.path.join(current_dir, file_name)

                # fbx出なければ除外
                if file_name.endswith(".fbx") is False:
                    continue

                if self.UI.update_only_cbox.isChecked():

                    # パス解決
                    uasset_path = os.path.join(
                        ue_gui_utils.get_anim_uasset_path(fbx_path),
                        file_name.replace(".fbx", ".uasset"),
                    )
                    uasset_path = ue_gui_utils.get_absolute_path(uasset_path)

                    if os.path.exists(uasset_path):
                        # 対象のuasetが最新の場合はスキップ
                        if self._check_update_data(fbx_path, uasset_path) is False:
                            continue

                ue_importer.anim_uasset_import(skel_name, fbx_path)

    def exec_import_selected_files(self):
        basicFilter = "*.fbx"
        skel_name = ue_gui_utils.get_skeleton_name(self.UI)
        file_paths = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=1, fm=4)
        for fbx_path in file_paths:
            file_name = os.path.basename(fbx_path)

            if self.UI.update_only_cbox.isChecked():

                # パス解決
                uasset_path = os.path.join(
                    ue_gui_utils.get_anim_uasset_path(fbx_path),
                    file_name.replace(".fbx", ".uasset"),
                )
                uasset_path = ue_gui_utils.get_absolute_path(uasset_path)

                if os.path.exists(uasset_path):
                    # 対象のuasetが最新の場合はスキップ
                    if self._check_update_data(fbx_path, uasset_path) is False:
                        continue

            ue_importer.anim_uasset_import(skel_name, fbx_path)

    @staticmethod
    def _check_update_data(fbx_path, uasset_path):
        # uassetよりfbxの方が新しければ
        if os.path.getmtime(fbx_path) > os.path.getmtime(uasset_path):
            return True
        return False

    def exec_import_current_dir(self):
        file_name = os.path.basename(cmds.file(sn=True, q=True))
        fbx_path = ue_gui_utils.get_anim_fbx_path(file_name) + "\\a_" + file_name
        fbx_path = fbx_path.replace(".mb", ".fbx")

        # TODO: 今は_defaultになっているので　治ったらこの部分は消す
        if "ply0000_basemodel" in fbx_path:
            fbx_path = fbx_path.replace("ply0000_basemodel", "ply0000_default")

        skel_name = ue_gui_utils.get_skeleton_name(self.UI)
        ue_importer.anim_uasset_import(skel_name, fbx_path)


def show(**kwargs):
    if AnimToolMainTool._instance is None:
        AnimToolMainTool._instance = AnimToolMainTool()

    AnimToolMainTool._instance.show(
        dockable=True,
    )

    AnimToolMainTool._instance.setWindowTitle("AnimationExporter")
