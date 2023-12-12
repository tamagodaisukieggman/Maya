from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import OrderedDict
from functools import partial

import os
import json
import webbrowser

import importlib

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

import maya.OpenMaya as om
import maya.cmds as cmds
from shr.utils import getCurrentSceneFilePath


from . import TITLE
from . import TOOL_NAME

from . import command
from . import DEFAULT_REFERENCE_NAME
from . import THUMBNAIL_ROOT_PATH
from . import CHARACTER_DIR_NAME
from . import CHARACTER_MODEL_ROOT_PATH
from . import CY_THUMBNAIL_EXT



# 開発中はTrue、リリース時にFalse
DEV_MODE = True

if DEV_MODE:
    importlib.reload(command)
else:
    from . import logger


UI_FILE_NAME = "variation_canger.ui"
UI_FILE = os.path.join(os.path.dirname(__file__), UI_FILE_NAME).replace(os.sep, '/')


class FileIconProvider(QtWidgets.QFileIconProvider):
    def _get_thumbnail(self, fileInfo):
        split_path = fileInfo.path().split(CHARACTER_DIR_NAME)
        if len(split_path) != 2:
            return
        thumbnail_path = os.path.join(
            THUMBNAIL_ROOT_PATH,
            CHARACTER_DIR_NAME,
            split_path[-1][1:],
            fileInfo.baseName() + CY_THUMBNAIL_EXT)
        if not os.path.exists(thumbnail_path):
            return
        return QtCore.QFileInfo(thumbnail_path)

    def icon(self, fileInfo):
        _file = None
        if isinstance(fileInfo, QtCore.QFileInfo):
            if fileInfo.suffix() and fileInfo.suffix() == "ma":
                _file = self._get_thumbnail(fileInfo)
            if _file:
                return QtGui.QIcon(_file.filePath())
            else:
                return super(FileIconProvider, self).icon(fileInfo)

        else:
            return super(FileIconProvider, self).icon(fileInfo)


class VariationModelChanger(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    cbox_default = " --- "

    def __init__(self, parent=None):
        self.current_scene_reference = OrderedDict()

        self.submeshdata = OrderedDict()
        self.scene_group_data = OrderedDict()

        self.json_path = ""

        self.replace_reference_path = ""

        super(self.__class__, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        loader = QUiLoader()

        uiFilePath = UI_FILE
        self.UI = loader.load(uiFilePath)

        helpAct = QtWidgets.QAction('Open Document Site ...', self)
        helpAct.triggered.connect(self.openHelp)

        menuBar = self.menuBar()
        menu = menuBar.addMenu('Help')
        menu.addAction(helpAct)

        self.dirmodel = QtWidgets.QFileSystemModel()
        self.dirmodel.setRootPath(CHARACTER_MODEL_ROOT_PATH)
        self.dirmodel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Dirs)

        self.UI.directory_tree.setModel(self.dirmodel)
        self.UI.directory_tree.setRootIndex(self.dirmodel.index(CHARACTER_MODEL_ROOT_PATH))
        self.UI.directory_tree.header().setSectionHidden(1, True)
        self.UI.directory_tree.header().setSectionHidden(2, True)
        self.UI.directory_tree.header().setSectionHidden(3, True)
        self.UI.directory_tree.setHeaderHidden(True)
        self.UI.directory_tree.clicked[QtCore.QModelIndex].connect(self.clicked_tree)

        self.inner_dirmodel = QtWidgets.QFileSystemModel()
        self.inner_dirmodel.setFilter(QtCore.QDir.Files)
        self.inner_dirmodel.setNameFilters(['*.ma', '*.mb'])
        self.inner_dirmodel.setNameFilterDisables(False)
        self.inner_dirmodel.setRootPath(CHARACTER_MODEL_ROOT_PATH)
        self.inner_dirmodel.setIconProvider(FileIconProvider())

        self.UI.fileTable.setModel(self.inner_dirmodel)
        self.UI.fileTable.setRootIndex(self.inner_dirmodel.index(CHARACTER_MODEL_ROOT_PATH))
        self.UI.fileTable.verticalHeader().hide()
        self.UI.fileTable.setSortingEnabled(True)

        header = self.UI.fileTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.UI.fileTable.verticalHeader().setDefaultSectionSize(128)
        self.UI.fileTable.doubleClicked[QtCore.QModelIndex].connect(self.getReferencePath)
        self.UI.fileTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.UI.fileTable.setSelectionBehavior(self.UI.fileTable.SelectRows)
        self.UI.fileTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.UI.fileTable.customContextMenuRequested.connect(self.contextMenu)

        self.UI.fileTable.setMouseTracking(True)
        self.UI.fileTable.viewport().installEventFilter(self)

        self.UI.referenceComboBox.currentIndexChanged.connect(partial(self.changeReferenceComboBox))

        self.UI.return_default_btn.clicked.connect(partial(self.returnToDefaultModel))
        self.UI.return_default_btn.clicked.connect(partial(self.returnToDefaultModel))
        self.UI.changeVariationPushButton.clicked.connect(partial(self.changePresetComboBox))
        self.UI.selectNodeCheckBox.clicked.connect(partial(self.selectReferenceNodes))

        self.resize(780, 360)
        self.setWindowTitle(TITLE)
        self.setCentralWidget(self.UI)

        self.buildRightClickMenu()

        self.getSceneName()
        cmds.scriptJob(event=("SceneOpened", self.getSceneName), parent=self.objectName())
        cmds.scriptJob(event=("NewSceneOpened", self.getSceneName), parent=self.objectName())

    def openHelp(self):
        """ヘルプサイトにジャンプ
        """
        _web_site = "https://wisdom.cygames.jp/pages/viewpage.action?pageId=257494721"
        webbrowser.open(_web_site)

    def getCurrentReferenceByConboBox(self):
        """現在選択されているコンボボックスのアイテムを返す

        Returns:
            [list]: [maya reference nodes]
        """
        _ref_node = []
        _text = self.UI.referenceComboBox.currentText()
        if _text and _text != self.cbox_default:
            _ref_node = cmds.ls(_text, type='reference')
        return _ref_node

    def getAllReferenceByComboBox(self):
        """リファレンスコンボボックス全てのアイテムをリストで返す

        Returns:
            [list]: クラスインスタンス
        """
        _ref_nodes = []
        for _i in range(self.UI.referenceComboBox.count()):
            _text = self.UI.referenceComboBox.itemText(_i)
            _ref = self.current_scene_reference.get(_text, None)
            if _ref and cmds.objExists(_text):
                _ref_nodes.append(_ref)
        return _ref_nodes

    def selectReferenceNodes(self, *args):
        """コンボボックスで選ばれているリファレンスノードを選択
        """

        _flag = self.UI.selectNodeCheckBox.isChecked()
        if not _flag:
            return

        _ref_node = self.getCurrentReferenceByConboBox()
        if _ref_node:
            nodes = cmds.referenceQuery(_ref_node[0], nodes=True)
            if nodes:
                for node in nodes:
                    # print(node)
                    if node.endswith(":model"):
                        # print(node,"---")
                        cmds.select(node, r=True)
                        break
        # self.fitOutliner()

    def fitOutliner(self):
        """Maya Outliner 全てのアウトライナを取得し、showSelected をオンにする
        """
        _outliners = [x for x in cmds.getPanel(type="outlinerPanel")
                      if x in cmds.getPanel(vis=True)]
        if _outliners:
            [cmds.outlinerEditor(x, e=True, showSelected=True) for x in _outliners]

    def getSceneName(self, *args):
        """シーン名を取得
        cmds で取得できないシーンがあったのでOpenMayaでも取得を試みる
        ただし、OpenMayaの場合は開いていなくても文字列は空にならないので
        そのための対処
        """
        self.current_scene_reference = OrderedDict()
        self.scene_group_data = OrderedDict()
        scene_name = getCurrentSceneFilePath()
        if not scene_name:
            scene_name = om.MFileIO.currentFile()

        if len(scene_name.split(".")) < 2:
            scene_name = ""

        if scene_name:
            self.scene_name = scene_name
            self.get_character_reference_nodes()
        if not DEV_MODE:
            logger.info("Get Variation Data Scene Name : [{}]".format(self.scene_name))
        else:
            self.scene_name = ""

        self.setUpReferenceComboBox()
        self.setUpPresetComboBox()

    def returnToDefaultModel(self, *args):
        """デフォルトのリファレンスモデルに戻す
        """
        _ref_nodes = self.getAllReferenceByComboBox()
        if not _ref_nodes:
            return

        _not_same_path_nodes = []
        for _ref in _ref_nodes:
            if _ref.get_current_path() != _ref.get_default_path():
                _not_same_path_nodes.append(_ref)

        if not _not_same_path_nodes:
            return

        _m = u"[ {} ]個 のリファレンスを元に戻します\n".format(len(_not_same_path_nodes))
        _m += u"\nよろしいですか？"
        _d = command.ConformDialogResult(title=u"リファレンスの置き換え",
                                         message=_m)
        result = _d.exec_()
        if not result:
            return

        for _ref in _not_same_path_nodes:
            _ref.set_default_referance_path()
        self.changeReferenceComboBox()

    def resetReferenceComboBox(self, allClear=False):
        """referenceComboBox のクリア

        Args:
            allClear (bool, optional): 全削除でない場合は「---」を追加
        """
        self.UI.referenceComboBox.clear()
        if not allClear:
            self.UI.referenceComboBox.addItem(self.cbox_default)

    def resetComboBox(self, allClear=False):
        """variationComboBox のクリア

        Args:
            allClear (bool, optional): 全削除でない場合は「---」を追加
        """
        self.UI.variationComboBox.clear()
        if not allClear:
            self.UI.variationComboBox.addItem(self.cbox_default)

    def readJsonData(self, node_name="", json_path=""):
        """json の読み込み

        self.submeshdata
        self.scene_group_data
        を作成

        Args:
            node_name (str): reference node name
            json_path (str): json file path
        """
        with open(json_path, "r") as json_data:
            preset_data = json.load(json_data)

        if not preset_data:
            return

        if not preset_data["row"]:
            return

        self.submeshdata = OrderedDict()
        _variation_group_data = command.get_groups(node_name)
        self.scene_group_data[node_name] = _variation_group_data

        for _rows in preset_data["row"]:
            if not _rows:
                continue
            for k, v in _rows.items():
                if k == "id":
                    # self.variations.append(v)
                    continue
                elif k.startswith("sub_meshes"):
                    self.submeshdata[_rows["id"]] = v

    def setUpReferenceComboBox(self):
        """referenceComboBox のセットアップ
        """
        if self.current_scene_reference:
            self.resetReferenceComboBox(True)
            for _ref_node, ref_node_data in self.current_scene_reference.items():
                self.UI.referenceComboBox.addItem(_ref_node)
        else:
            self.resetReferenceComboBox()

    def setUpPresetComboBox(self):
        """バリエーションデータが存在すればコンボボックスに
        メニューを追加する
        """
        _flag = True
        _current_node = self.getCurrentReferenceByConboBox()
        if _current_node:
            _current_node = _current_node[0]
            _group_data = self.scene_group_data.get(_current_node, None)
            if self.submeshdata and _group_data:
                self.resetComboBox(True)
                for var, sbm in self.submeshdata.items():
                    # print(var, sbm, " --- var, sbm")
                    self.UI.variationComboBox.addItem(var)
            else:
                _flag = False
        else:
            _flag = False

        if not _flag:
            self.resetComboBox()

    def changeReferenceComboBox(self, *args):
        """コンボボックスでリファレンスノードを選んだ時
        """

        json_path = ""
        _current_node = self.getCurrentReferenceByConboBox()
        if _current_node:
            # print(_current_node, " -- _current_node")
            _current_node = _current_node[0]
            _ref = self.current_scene_reference.get(_current_node, None)
            # print(_ref," -- _ref")
            if _ref:
                json_path = _ref.get_json_path()
                # print(json_path," -- json_path")

        if json_path:
            self.readJsonData(_current_node, json_path)

        self.setUpPresetComboBox()
        self.selectReferenceNodes()

    def changePresetComboBox(self, *args):
        """combo box で選択したプリセットに合わせて
        サブメッシュグループの表示を切り替える
        プリセットが存在しない場合は[ default ]が表示される
        その場合は001のノードが表示
        表示に合わせてチェックボックスがあればチェックボックスの値も変化
        """
        _current_reference = self.UI.referenceComboBox.currentText()
        _current_preset = self.UI.variationComboBox.currentText()
        _current_submesh_setting = self.submeshdata.get(_current_preset, None)

        if not _current_submesh_setting or not self.scene_group_data:
            return
        _group_data = self.scene_group_data.get(_current_reference, None)
        if not _group_data:
            return
        for short_name, real_node in _group_data.items():

            if not cmds.objExists(real_node):
                continue
            _vis_flag = False
            if short_name in _current_submesh_setting:
                _vis_flag = True

            cmds.setAttr("{}.v".format(real_node), _vis_flag)

    def buildRightClickMenu(self):
        """左のテーブルを右クリックしたときに表示させるメニュー
        """
        self.replace_menu = QtWidgets.QMenu(self)

        action = QtWidgets.QAction("Replace Reference ...", self)
        action.triggered.connect(self.getReferencePath)
        self.replace_menu.addAction(action)

    def getReferencePath(self):
        """リファレンスの置き換え
        バリエーションデータが存在すればそれも適用
        """
        _index = self.UI.fileTable.currentIndex()
        if not _index:
            return

        _ref_node = self.getCurrentReferenceByConboBox()
        if not _ref_node:
            return
        _ref_node = _ref_node[0]

        if not self.current_scene_reference:
            return

        dir_path = self.inner_dirmodel.filePath(_index)
        if not os.path.exists(dir_path):
            return

        _current_reference = self.current_scene_reference.get(_ref_node, None)
        if not _current_reference:
            return
        _current_reference.replace_referance_model(dir_path)
        self.changeReferenceComboBox()

    def get_character_reference_nodes(self):
        """シーン内のリファレンスノード取得
        キャラモデルのリファレンスを取りたいので
        rigs, prop animations の文字列がパスに含まれる場合は排除している
        ノード名: クラスインスタンス
        の辞書を作成
        """
        for ref_node in cmds.ls(type='reference', long=True):
            if "sharedReferenceNode" in ref_node:
                continue
            _path = cmds.referenceQuery(ref_node, filename=True)
            if "rigs" not in _path and "prop" not in _path and "animations" not in _path:
                _path = command.clean_reference_path(_path)
            else:
                continue
            _ref = command.ReferenceNodeFilePath(ref_node, _path)
            self.current_scene_reference[ref_node] = _ref

    def contextMenu(self, point):
        """左のテーブルを右クリックでメニューを出す
        mapTpGlobal だけだとポインタが左に寄るので
        self.UI.directory_tree の幅と
        メニューをクリックしやすいように少し下げたのが「_add」

        Args:
            point ([type]): [description]
        """
        _add = QtCore.QPoint(self.UI.directory_tree.width(), 40)
        self.replace_menu.exec_(_add + self.mapToGlobal(point))

    def clicked_tree(self, *args):
        """左のディレクトリツリーのクリック処理
        """
        _index = self.UI.directory_tree.currentIndex()
        dir_path = self.dirmodel.filePath(_index)
        self.inner_dirmodel.setRootPath(dir_path)
        self.UI.fileTable.setRootIndex(self.inner_dirmodel.index(dir_path))
        self.UI.fileTable.clearSelection()


def main():

    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == TOOL_NAME:
            _obj.close()
            del _obj

    if not os.path.exists(UI_FILE):
        cmds.warning(u"UI ファイルが見つかりません")
        return

    if not DEV_MODE:
        logger.send_launch(u'ツール起動')

    ui = VariationModelChanger()
    ui.show()
