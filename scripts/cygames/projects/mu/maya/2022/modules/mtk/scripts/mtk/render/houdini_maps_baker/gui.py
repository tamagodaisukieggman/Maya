from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import importlib
import json

from functools import partial


from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

from mtk.utils.hda_loader import houdini_util

from . import command
from . import gui_util

from . import TITLE
from . import TOOL_NAME

# 開発中はTrue、リリース時にFalse
DEV_MODE = True

if DEV_MODE:
    importlib.reload(command)
else:
    from . import logger


UI_FILE = os.path.join(os.path.dirname(__file__),
                       'houdini_maps_baker_ui.ui').replace(os.sep, '/')

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


class MtkHoudiniMapsBaker(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    script_job = None
    _tso_flag = False

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        if not os.path.exists(UI_FILE):
            return

        loader = QUiLoader()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        uiFilePath = UI_FILE
        self.UI = loader.load(uiFilePath)

        menuBar = self.menuBar()
        menu = menuBar.addMenu('Help')
        openAct = QtWidgets.QAction('Help Site...', self)
        openAct.triggered.connect(self.openHelp)
        menu.addAction(openAct)

        self.UI.openExportFolderpushButton.clicked.connect(
            self.openExportDirectory)

        self.resize(650, 490)
        self.setWindowTitle(TITLE)

        self.setCentralWidget(self.UI)

        # setExportPathPushButton ボタン
        image = QtGui.QIcon(':/folder-open.png')
        self.UI.setExportPathPushButton.setIcon(image)
        self.UI.setExportPathPushButton.clicked.connect(
            self.openExportDirectoryDialog)

        # 解像度のコンボボックス作成
        self.setUpResolutionComboBox()

        self.UI.targetRegisterClearPushButton.clicked.connect(
            partial(self.registerListClear, "target"))
        self.UI.sourceRegisterClearPushButton.clicked.connect(
            partial(self.registerListClear, "source"))

        self.UI.targetRegisterAddPushButton.clicked.connect(
            partial(self.registerListAdd, "target"))
        self.UI.sourceRegisterAddPushButton.clicked.connect(
            partial(self.registerListAdd, "source"))

        self.UI.targetRegisterRemovePushButton.clicked.connect(
            partial(self.registerListRemove, "target"))
        self.UI.sourceRegisterRemovePushButton.clicked.connect(
            partial(self.registerListRemove, "source"))

        self.UI.targetRegisterListWidget.selectionModel().selectionChanged.connect(
            partial(self.registerListSelectChange, "target"))

        self.UI.sourceRegisterListWidget.selectionModel().selectionChanged.connect(
            partial(self.registerListSelectChange, "source"))

        self.UI.bakeStartPushButton.clicked.connect(self.bakeStart)

    def registerListSelectChange(self, widgetName="target", *args):
        """選択の切り替え

        Args:
            widgetName (str): ターゲットウェジット名
        """
        _selections = []
        _widget = self.getCurrentListWidget(widgetName)
        for i in range(_widget.count()):
            if _widget.isItemSelected(_widget.item(i)):
                _selections.append(_widget.item(i).text())
        if _selections:
            command.select_list(_selections)

    def getCurrentListWidget(self, widgetName="target"):
        """対象となるリストウェジットを返す

        Args:
            widgetName (str): ターゲットウェジット名

        Returns:
            [QlistWedgit]:
        """
        _widget = None
        if widgetName == "target":
            _widget = self.UI.targetRegisterListWidget
        else:
            _widget = self.UI.sourceRegisterListWidget
        return _widget

    def registerListRemove(self, widgetName="target"):
        """レジスタからアイテム削除
        takeItem でもできたが、リストの選択もいじる必要があるので
        選択していないものを再取得してリストウェジットを再構成

        Args:
            widgetName (str): ターゲットウェジット名
        """

        item_list = []
        _widget = self.getCurrentListWidget(widgetName)
        for i in range(_widget.count()):
            if _widget.isItemSelected(_widget.item(i)):
                continue
            item_list.append(_widget.item(i).text())

        if not item_list:
            _items = _widget.selectedItems()
            if _items:
                self.registerListClear(widgetName)
        else:
            self.registerListClear(widgetName)
            self.registerListAdd(widgetName, item_list)

    def registerListAdd(self, widgetName="target", mesh_nodes=[]):
        """レジスタに追加

        Args:
            widgetName (str): ターゲットウェジット名
            mesh_nodes (list): 追加するメッシュノードリスト
        """
        _widget = self.getCurrentListWidget(widgetName)
        if not mesh_nodes:
            mesh_nodes = command.get_current_selections()
            if not mesh_nodes:
                return

        for mesh_node in mesh_nodes:
            if not _widget.findItems(mesh_node, QtCore.Qt.MatchExactly):
                _widget.addItem(mesh_node)

    def registerListClear(self, widgetName="target"):
        """レジスタのクリア

        Args:
            widgetName (str): ターゲットウェジット名
        """
        _widget = self.getCurrentListWidget(widgetName)
        _widget.clear()

    def setUpResolutionComboBox(self):
        """解像度コンボボックスの値設定
        """
        for res in RESOLUTIONS:
            self.UI.exportResolutionComboBox.addItem("{}".format(res))
        self.UI.exportResolutionComboBox.setCurrentText("2048")

    def openExportDirectory(self):
        """ウィンドウズエクスプローラでディレクトリ表示
        """
        current_directory = self.UI.exportPathlineEdit.text()
        command.open_export_directory(current_directory)

    def openHelp(self, *args):
        """ヘルプサイト表示
        """
        command.open_help_site()

    def openExportDirectoryDialog(self):
        """ファイルの出力先設定
        """
        current_directory = self.UI.exportPathlineEdit.text()
        current_directory = command.get_current_directory(current_directory)

        dialog = QtWidgets.QFileDialog(directory=current_directory)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        if dialog.exec_():
            path = dialog.selectedFiles()[0].replace(os.sep, '/')
            self.UI.exportPathlineEdit.setText(path)

    def getListWidgetItems(self, widgetName="target"):
        """リストウィジェットに登録されているものを返す

        Args:
            widgetName (str): 対象とするウィジェット

        Returns:
            [list]: トランスフォームノード
        """
        _items = []
        _widget = self.getCurrentListWidget(widgetName)
        for i in range(_widget.count()):
            mesh_node = _widget.item(i).text()
            # transform_node = command.get_transform_node(mesh_node)
            # if transform_node:
            _items.append(mesh_node)
        return _items

    def bakeStart(self):
        no_color_texture_flag = False
        shading_group_textures = dict()

        current_directory = self.UI.exportPathlineEdit.text()
        resolution = int(self.UI.exportResolutionComboBox.currentText())
        max_trace_distance = self.UI.maxTraceDistanceDoubleSpinBox.value()
        target_items = self.getListWidgetItems("target")
        source_items = self.getListWidgetItems("source")

        # if not command.check_bake_items(current_directory, target_items, source_items):
        #     return

        mesh_shading_group = command.get_shading_group(source_items)

        for mesh, shading_group in mesh_shading_group.items():
            textures = command.get_textures(shading_group)
            _test_json = json.dumps(textures)
            print(_test_json)
            for sg, texture in textures.items():
                color_textrue = texture.get("color", None)
                alpha_texture = texture.get("alpha", None)
                if not color_textrue:
                    no_color_texture_flag = True
                    break
                shading_group_textures[sg] = color_textrue
                # print(sg, texture)


def main():
    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == TOOL_NAME:
            _obj.close()
            del _obj

    ui = MtkHoudiniMapsBaker()

    if not os.path.exists(UI_FILE):
        _d = gui_util.ConformDialog(title=TOOL_NAME,
                                    message="UI ファイルが見つかりません")
        _d.exec_()
        return

    if houdini_util.main():
        ui.show()
        if not DEV_MODE:
            logger.send_launch(u'ツール起動')
    else:
        _d = gui_util.ConformDialog(title=TOOL_NAME,
                                    message="Z ドライブの HoudiniEngine がアクティブにできませんでした")
        _d.exec_()
        return
