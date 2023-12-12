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
UIFILEPATH = filePath + "/ui/face_anim_gui.ui"
TITLE = "MH_Animation_Exporter"


class FaceAnimToolMainTool(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    _instance = None

    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return "{}.{}".format(self.__module__, self.__class__.__name__)

    def __init__(self, parent=None):
        super(FaceAnimToolMainTool, self).__init__(parent)
        self.setObjectName(TITLE)

        self.delete_instances()
        self.exporter = command.Exporter("mh_animation")
        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)

        get_dir_icon = QtGui.QIcon(":/fileOpen.png")
        self.UI.get_directory_btn.setIcon(get_dir_icon)

        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # infoがないと配列の中に空の文字列が入っている
        if cmds.fileInfo("mh_animation_export_path", q=True) == []:
            # UIの情報が無かったらCurrentPathで初期化
            self.exporter.initialize_ui_info()
        self.load_ui_info()

        # connect
        self.UI.get_directory_btn.clicked.connect(self.exec_get_directory)
        self.UI.export_btn.clicked.connect(self.exec_export)

        self.UI.directory_txt.textChanged.connect(self.save_ui_info)
        self.UI.filename_txt.textChanged.connect(self.save_ui_info)

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
        cmds.fileInfo("mh_animation_export_path", self.UI.directory_txt.text())
        cmds.fileInfo("mh_animation_export_name", self.UI.filename_txt.text())

    def load_ui_info(self):
        self.UI.directory_txt.setText(
            cmds.fileInfo("mh_animation_export_path", query=True)[0]
        )
        self.UI.filename_txt.setText(
            cmds.fileInfo("mh_animation_export_name", query=True)[0]
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


def show(**kwargs):
    if FaceAnimToolMainTool._instance is None:
        FaceAnimToolMainTool._instance = FaceAnimToolMainTool()

    FaceAnimToolMainTool._instance.show(
        dockable=True,
    )

    FaceAnimToolMainTool._instance.setWindowTitle(TITLE)
