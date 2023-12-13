# -*- coding: utf-8 -*-
from __future__ import print_function

import os
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
import shr.file.create_anim_defaultscene.command as sfc
import tool_log


UIFILEPATH = (
    os.path.dirname(__file__).replace("\\", "/") + "/ui/create_anim_defaultscene_gui.ui"
)
TITLE = "create_anim_defaultscene"
BODY_PARTS = ["body", "face", "hair"]
DEV = False


class CreateAnimDefaultScene(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    _instance = None

    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return "{}.{}".format(self.__module__, self.__class__.__name__)

    def __init__(self, parent=None):
        if DEV == False:
            self.send_logger()

        super(CreateAnimDefaultScene, self).__init__(parent)
        self.setObjectName(TITLE)

        self.delete_instances()
        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)
        self.parts_cmbboxes = [
            self.UI.body_cmbbox,
            self.UI.face_cmbbox,
            self.UI.hair_cmbbox,
        ]
        self.parts_version_cmbbox = [
            self.UI.body_version_cmbbox,
            self.UI.face_version_cmbbox,
            self.UI.hair_version_cmbbox,
        ]

        self.parts_cboxes = [self.UI.body_cbox, self.UI.face_cbox, self.UI.hair_cbox]

        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.character_datas = sfc.get_yaml_data()["character_info"]
        self.weapon_datas = sfc.get_yaml_data()["weapons"]
        self.init_chr_type_cmbbox()
        self.init_weapon_item()

        # # Connected
        self.UI.chr_type_cmbbox.currentIndexChanged.connect(self.change_chr_type_cmbbox)

        self.UI.body_cmbbox.currentIndexChanged.connect(self.change_body_parts_cmbbox)
        self.UI.face_cmbbox.currentIndexChanged.connect(self.change_body_parts_cmbbox)
        self.UI.hair_cmbbox.currentIndexChanged.connect(self.change_body_parts_cmbbox)
        self.UI.used_weapon_cbox.stateChanged.connect(self.change_state)

        self.UI.create_button.clicked.connect(self.exec_create_button)
        self.UI.select_folder_export_btn.clicked.connect(
            self.exec_select_folder_export_btn
        )
        self.UI.override_name_cbox.stateChanged.connect(
            self.state_change_override_name_cbox
        )

    def send_logger(self) -> None:
        """ログ送信用"""
        logger_type = "create_anim_defaultscene"
        version = "v2022.11.30"
        logger = tool_log.get_logger(logger_type, version)
        logger.send_launch("")

    def delete_instances(self):
        workspace_control_name = self.objectName() + "WorkspaceControl"
        if cmds.workspaceControl(workspace_control_name, exists=True):
            pm.deleteUI(workspace_control_name)

    def dockCloseEventTriggered(self):
        self.delete_instances()

    def change_state(self):
        self.UI.weapon_lwidget.setEnabled(self.UI.used_weapon_cbox.isChecked())

    def exec_create_button(self):
        """create_default_buttonを押したときの処理"""

        body_namespace_name = ""
        other_namespace_names = []
        used_namespaces = []
        # 既に存在しているnamespaceと比較する処理を追加
        current_chr_type = self.UI.chr_type_cmbbox.currentText()

        # 体のパーツ読み込み
        for i, lp in enumerate(self.parts_cmbboxes):
            current_name = lp.currentText()
            version = self.parts_version_cmbbox[i].currentText()
            if not self.parts_cboxes[i].isChecked() or current_name == "":
                continue
            path = sfc.get_mb_path(current_chr_type, current_name, version)
            ns = lp.currentText()
            current_ns = sfc.set_reference([path], namespace=ns)
            used_namespaces.append(current_ns)
            # ディスプレイレイヤーの作成
            sfc.set_display_layer_by_namespace(current_ns)
            # 体の処理の時のみ
            if i == 0:
                body_namespace_name = current_ns
                self.UI.override_name_txt.setText(
                    current_name.split("_")[0] + "_default"
                )

            else:
                other_namespace_names.append(current_ns)

        for lp in other_namespace_names:
            sfc.constraint_by_namespace(lp, body_namespace_name)

        # 武器の読み込み
        if self.UI.used_weapon_cbox.isChecked():
            lw = self.UI.weapon_lwidget
            items = [lw.item(x) for x in range(lw.count())]
            for item in items:
                for weapon_data in self.weapon_datas:
                    layer_widget = lw.itemWidget(item)
                    layer = layer_widget.layer
                    if weapon_data["file_name"] == layer.file_name:
                        current_ns = sfc.set_reference(
                            [layer.path], namespace=weapon_data["label"]
                        )
                        sfc.set_display_layer_by_namespace(current_ns)
                        if layer.enabled != True:
                            cmds.file(layer.path, unloadReference=current_ns)
                        used_namespaces.append(current_ns)

        # setの作成 namespace
        roots = []
        for ns in used_namespaces:
            nodes = sfc.get_nodes_by_namespace(ns, type="transform")
            roots.append(sfc.get_root_node(nodes[0]))
        cmds.sets(roots, n=self.UI.set_name_txt.text() + "_dl_sets")

    def state_change_override_name_cbox(self):
        self.UI.override_name_txt.setEnabled(self.UI.override_name_cbox.isChecked())

    def change_body_parts_cmbbox(self):
        for lp in BODY_PARTS:
            self.update_parts_version(lp)

    def exec_select_folder_export_btn(self):
        current_name = self.UI.override_name_txt.text()
        chr_type = self.UI.chr_type_cmbbox.currentText()
        body_name = self.UI.body_cmbbox.currentText()
        sfc.save_file_dialog(current_name, chr_type, body_name)

    def init_weapon_item(self):
        for lp in self.weapon_datas:
            curret_path = sfc.get_share_path(lp["path"])
            files = sfc.get_directories(curret_path, file_suffix="mb")["files"]
            versions = sfc.get_versions(files)
            latest_version = sfc.get_latest_version(versions)

            fullpath = "{0}/{1}_{2}.mb".format(
                curret_path, lp["file_name"], latest_version
            )

            layer_object = LayerObject(
                name=lp["label"],
                file_name=lp["file_name"],
                enabled=True,
                items=versions,
                version=latest_version,
                path=fullpath,
            )
            layer = LayerWidget(layer_object, versions)
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(layer.sizeHint())
            self.UI.weapon_lwidget.insertItem(self.UI.weapon_lwidget.count(), item)
            self.UI.weapon_lwidget.setItemWidget(item, layer)

    def init_chr_type_cmbbox(self):
        for lp in self.character_datas:
            # chr_typeのcommboboxの設定
            self.UI.chr_type_cmbbox.addItem(lp["label"])

        self.change_chr_type_cmbbox()

    def clear_parts_cmbbox(self):
        self.parts_cmbboxes
        for lp in self.parts_cmbboxes:
            lp.clear()

        for lp in self.parts_version_cmbbox:
            lp.clear()

    def get_curretn_data(self):
        current_data = dict
        chr_type = self.UI.chr_type_cmbbox.currentText()
        for lp in self.character_datas:
            if chr_type == lp["label"]:
                current_data = lp
                return current_data

    def get_parts_path(self, parts_type):
        current_data = self.get_curretn_data()
        body_path = sfc.get_share_path(current_data["path"]) + "/" + current_data["id"]
        if parts_type == "face":
            return body_path[:-2] + "fc"
        elif parts_type == "hair":
            return body_path[:-2] + "hr"
        else:
            return body_path

    def change_chr_type_cmbbox(self):
        # commboboxを一旦クリアにする
        self.clear_parts_cmbbox()

        # partsへの設定
        current_data = self.get_curretn_data()

        body_path = self.get_parts_path("body")
        face_path = self.get_parts_path("face")
        hair_path = self.get_parts_path("hair")
        keys = list(current_data.keys())

        if "active_parts" not in keys:
            self.UI.body_cmbbox.addItems(sfc.get_directories(body_path)["folder"])
            self.UI.face_cmbbox.addItems(sfc.get_directories(face_path)["folder"])
            self.UI.hair_cmbbox.addItems(sfc.get_directories(hair_path)["folder"])

            for lp in BODY_PARTS:
                self.update_parts_version(lp)

            self.set_enable_parts_ui("face", True)
            self.set_enable_parts_ui("hair", True)

        else:
            # アクティブかどうか
            if "face" in current_data["active_parts"]:
                self.UI.face_cmbbox.addItems(sfc.get_directories(face_path)["folder"])
                self.set_enable_parts_ui("face", True)
            else:
                self.set_enable_parts_ui("face", False)

            if "hair" in current_data["active_parts"]:
                self.UI.hair_cmbbox.addItems(sfc.get_directories(hair_path)["folder"])
                self.set_enable_parts_ui("hair", True)
            else:
                self.set_enable_parts_ui("hair", False)

            # bodyは必ず追加
            self.UI.body_cmbbox.addItems(sfc.get_directories(body_path)["folder"])

    def set_enable_parts_ui(self, parts_name, enable):
        eval("self.UI.{}_cmbbox".format(parts_name)).setEnabled(enable)
        eval("self.UI.{}_cbox".format(parts_name)).setEnabled(enable)
        eval("self.UI.{}_cbox".format(parts_name)).setChecked(enable)

    def get_version_cmbbox(self, parts_type):
        version_cmbbox = eval("self.UI.{}_version_cmbbox".format(parts_type))

    def set_latest_version(self, parts_type):
        "self.UI.{}_version_cmbbox"

    def update_parts_version(self, parts_type):
        version_cmbbox = eval("self.UI.{}_version_cmbbox".format(parts_type))
        version_cmbbox.clear()
        cmbbox = eval("self.UI.{}_cmbbox".format(parts_type))

        path = "{0}/{1}/maya/".format(
            self.get_parts_path(parts_type), cmbbox.currentText()
        )
        versions = sfc.get_versions(
            sfc.get_directories(path, file_suffix="mb")["files"]
        )
        version_cmbbox.addItems(versions)
        latest_version = sfc.get_latest_version(versions)
        index = self.find_current_version_Index(version_cmbbox, latest_version)
        if index != None:
            version_cmbbox.setCurrentIndex(index)

    @staticmethod
    def find_current_version_Index(cmbbox: QtWidgets.QComboBox, version: str) -> int:
        all_items = [cmbbox.itemText(i) for i in range(cmbbox.count())]
        if version != "v000":
            return all_items.index(version)


class LayerObject(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.file_name = kwargs.get("file_name", "")
        self.enabled = kwargs.get("enabled", False)
        self.items = kwargs.get("items")
        self.path = kwargs.get("path", "")
        self.version = kwargs.get("version")


class LayerWidget(QtWidgets.QWidget):
    def __init__(self, layer: LayerObject, versions: list):
        super(LayerWidget, self).__init__()

        # controls
        self.ui_enabled = QtWidgets.QCheckBox()
        self.ui_layername = QtWidgets.QLabel()
        self.ui_items = QtWidgets.QComboBox()
        spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.ui_enabled)
        main_layout.addWidget(self.ui_layername)
        main_layout.addSpacerItem(spacer)
        main_layout.addWidget(self.ui_items)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)
        main_layout.setStretch(2, 0)
        self.setLayout(main_layout)

        for version in versions:
            self.ui_items.addItem(version)

        # construct
        self._layer = None
        self.layer = layer

        self.ui_items.currentIndexChanged.connect(self.update_layer)
        self.ui_enabled.stateChanged.connect(self.update_layer)

    def get_layer_path(self):
        fullpath = "{0}/{1}_{2}.mb".format(
            self.layer.path.rsplit("/", 1)[0],
            self.layer.file_name,
            self.layer.version,
        )
        return fullpath

    def update_layer(self):
        current_layer = self._layer
        current_layer.version = self.ui_items.currentText()
        current_layer.path = self.get_layer_path()
        current_layer.enabled = self.ui_enabled.isChecked()
        self.layer = current_layer

    # properties
    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value
        self.ui_layername.setText(value.name)
        self.ui_enabled.setChecked(value.enabled)
        if value.version != "v000":
            self.ui_items.setCurrentIndex(self.find_current_Index(value.version))

    def find_current_Index(self, version):
        all_items = [self.ui_items.itemText(i) for i in range(self.ui_items.count())]
        return all_items.index(version)


def show(**kwargs):
    if CreateAnimDefaultScene._instance is None:
        CreateAnimDefaultScene._instance = CreateAnimDefaultScene()

    CreateAnimDefaultScene._instance.show(
        dockable=True,
    )

    CreateAnimDefaultScene._instance.setWindowTitle(TITLE)
