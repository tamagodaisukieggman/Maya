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
import maya.mel

from . import command
from . import TITLE
from . import NAME
from . import NODE_CHILDREN
from . import GROUP_ROOTNODES

from . import gui_util

CLASS_NAME = "".join(TITLE.split())
TEMP_NODE = "{}_temp_group".format(NAME)

# 開発中はTrue、リリース時にFalse
DEV_MODE = True

if DEV_MODE:
    importlib.reload(command)
    importlib.reload(gui_util)
else:
    from . import logger

UI_FILE = r"Z:\mtk\tools\maya\2022\modules\mtk\scripts\mtk\file\partssplitexporter\parts_split_exporter.ui"


def get_children(node):
    """再帰的にMayaのノードの親をたどりルートを返す

    Args:
        node (str): maya dag node

    Yields:
        [str]: dag_root_node
    """
    children = cmds.listRelatives(node, c=True, pa=True)

    if children:
        for c in children:
            _c = cmds.listRelatives(c, c=True, pa=True)
            if _c:
                for _ in _c:
                    yield _
            else:
                yield c


class XRayJointCheckBox(QtWidgets.QCheckBox):
    def __init__(self, *args, **kwargs):
        super(XRayJointCheckBox, self).__init__(*args, **kwargs)
        image = QtGui.QIcon(':/XRayJoints.png')
        self.setIcon(image)
        # self.setStyleSheet('QGroupBox::indicator:checked {image: url(XRayJoints.png);}')


class OrignalTreeWedget(QtWidgets.QTreeWidget):
    def __init__(self, *args, **kwargs):
        super(OrignalTreeWedget, self).__init__(*args, **kwargs)
    # ---------------------------------------------------------------------------

    def keyPressEvent(self, event):

        shift = event.modifiers() & QtCore.Qt.ShiftModifier
        print(shift, "# --- shift")
        if shift:
            self.expand_all(self.currentIndex())
        else:
            expand = not(self.isExpanded(self.currentIndex()))

            self.setExpanded(self.currentIndex(), expand)
        # if (event.key() == QtCore.Qt.Key_Space and self.currentIndex().column() == 0):
        #     shift = event.modifiers() & QtCore.Qt.ShiftModifier
        #     if shift:
        #         self.expand_all(self.currentIndex())
        #     else:
        #         expand = not(self.isExpanded(self.currentIndex()))
        #         self.setExpanded(self.currentIndex(), expand)

    # ---------------------------------------------------------------------------

    def expand_all(self, index):
        """
        Expands/collapses all the children and grandchildren etc. of index.
        """
        expand = not(self.isExpanded(index))
        # if collapsing, do that first (wonky animation otherwise)
        if not expand:
            self.setExpanded(index, expand)
        childCount = index.internalPointer().get_child_count()
        self.recursive_expand(index, childCount, expand)
        if expand:  # if expanding, do that last (wonky animation otherwise)
            self.setExpanded(index, expand)

    # ---------------------------------------------------------------------------

    def recursive_expand(self, index, childCount, expand):
        """
        Recursively expands/collpases all the children of index.
        """
        for childNo in range(0, childCount):
            childIndex = index.child(childNo, 0)
            # if expanding, do that first (wonky animation otherwise)
            if expand:
                self.setExpanded(childIndex, expand)
            subChildCount = childIndex.internalPointer().get_child_count()
            if subChildCount > 0:
                self.recursive_expand(childIndex, subChildCount, expand)
            # if collapsing, do it last (wonky animation otherwise)
            if not expand:
                self.setExpanded(childIndex, expand)


class PartsSplitExporter(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    UI = None
    defaultConboBoxText = "---"

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.selectionChildHighlightMode = 0

        self.short_name_long_name = dict()
        self.fullpath_shortname = dict()

        self.short_name_parent = dict()
        self.short_name_children = dict()

        self.parts_preset = dict()
        self.visible_states = dict()
        self.current_group_nodes = dict()
        self.root_nodes = dict()

        self.root_joint = None
        self.model_group = None

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        loader = QUiLoader()

        uiFilePath = UI_FILE.replace(os.sep, '/')
        self.UI = loader.load(uiFilePath)

        openAct = QtWidgets.QAction('Import Group Data ...', self)
        saveAct = QtWidgets.QAction('Export Group Data ...', self)
        helpAct = QtWidgets.QAction('Help ...', self)
        openAct.triggered.connect(self.importFileDialog)
        saveAct.triggered.connect(self.exportFileDirectoryDialog)
        helpAct.triggered.connect(self.openHelp)

        menuBar = self.menuBar()
        menu = menuBar.addMenu('File')
        menu.addAction(openAct)
        menu.addAction(saveAct)
        menu.addAction(helpAct)

        # self.UI.XRayJointsCheckBox = XRayJointCheckBox("Xra")
        # self.XRayJointsImage = QtGui.QIcon(':/XRayJoints.png')
        # self.UI.XRayJointsCheckBox.setIcon(self.XRayJointsImage)
        # self.UI.XRayJointsCheckBox.setIcon(self.XRayJointsImage)
        self.UI.XRayJointsCheckBox.clicked.connect(self.xrayJoint)

        self.UI.presetComboBox.addItem(self.defaultConboBoxText)
        self.UI.registPushButton.clicked.connect(partial(self.registNodes))
        self.UI.unRegistPushButton.clicked.connect(partial(self.unRegistNodes))
        self.UI.selectRegistedNodes.clicked.connect(
            partial(self.selectAllGroup))
        self.UI.hiliteSelectionOnlyCheckBox.clicked.connect(
            partial(self.changeHiliteSelectionType))

        self.UI.addPresetPushButton.clicked.connect(partial(self.addPreset))
        self.UI.editPresetPushButton.clicked.connect(partial(self.editPreset))
        self.UI.deletePresetPushButton.clicked.connect(
            partial(self.deletePreset))

        self.UI.saveSceneConvertPushButton.clicked.connect(
            partial(self.saveAndConvertButton))

        self.UI.presetComboBox.currentIndexChanged.connect(
            partial(self.changePreset))

        self.UI.treeWidgetSelectRadioButton.clicked.connect(
            partial(self.radioButtonCallBack))
        self.UI.groupTreeWidgetSelectRadioButton.clicked.connect(
            partial(self.radioButtonCallBack))

        self.UI.regstInfluenceJointsPushButton.clicked.connect(
            partial(self.registMeshInfluenceJoints))

        # _icon = self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton)
        # openAct = QtWidgets.QAction('Help', self)
        # openAct.triggered.connect(self.openHelp)

        self.resize(500, 700)
        self.setWindowTitle(TITLE)
        self.setCentralWidget(self.UI)

        self.UI.treeWidget.selectionModel().selectionChanged.connect(
            self.treeWidgetSelectChanged)
        self.UI.groupTreeWidget.selectionModel().selectionChanged.connect(
            self.groupTreeWidgetSelectChanged)

        # self.UI.treeWidget.itemDoubleClicked.connect(self.doubleClickTree)
        # self.UI.treeWidget.installEventFilter(self)
        # self.UI.treeWidget.itemClicked.connect(self.onItemClicked)

        self.getSelectionMode()
        self.getSceneObjects()
        self.changeHiliteSelectionType()

        cmds.scriptJob(event=("SceneOpened", self.getSceneObjects),
                       parent=self.objectName())
        # cmds.scriptJob(event=("SelectionChanged", self.selectionChange),
        #                parent=self.objectName())

    def doubleClickTree(self, item):
        # _li = []
        # items = self.getItemsToSelection(item, _li)
        # if items:
        #     [x.setSelected(True) for x in items]
        # return
        _selections = []
        item_list = []
        self.UI.treeWidget.setCurrentItem(item)
        count = item.childCount()
        if count:
            for i in range(count):

                child = item.child(i)
                # _selections.append(child.text(0))
                item_list.append(child)
                # self.selectTreeItems(self.UI.treeWidget, _selections)
                # self.getItemsToSelection(child, item_list)
        if item_list:
            [x.setSelected(True) for x in item_list]
        # if _selections:
        #     self.selectTreeItems(self.UI.treeWidget, _selections)

    # def setDefalutParents(self):
    #     """記憶した階層順を再現する
    #     再現方法は、フルパスを元に行う
    #     """
    #     if not self.short_name_long_name:
    #         return
    #     command.set_default_hierarchy(self.short_name_long_name.keys(),
    #                                   self.short_name_parent)

    def saveAndConvertButton(self, *args):
        """登録されたグループの保存とコンバートを行う

        set_up_scene_path
        シーンのチェック、保存されているか、「all」がシーン名に入っているか

        check_parts_scene
        グループの内容チェック

        writeFileInfo
        グループ情報をシーンに書き込み

        setDefaultSelectPref
        選択時のヒエラルキー表示を元に戻す

        save_base_scene
        元のシーン開いている「all」が含まれたシーンを保存

        all_save_parts_scene
        各グループのシーン保存、コンバート
        """
        scene_name, root_path, basename, ext = command.set_up_scene_path()
        if not ext:
            return
        _error = command.check_parts_scene(self.parts_preset)
        if _error:
            return
        _m = u"現在のシーンを保存した後\n"
        _m += u"パーツ分割シーンの生成、コンバートを行います\n"
        _m += u"よろしいですか？"
        _d = gui_util.ConformDialogResult(message=_m)
        result = _d.exec_()
        if not result:
            return
        self.writeFileInfo()
        self.setDefaultSelectPref()
        command.save_base_scene()
        # self.readFileInfo()
        # print(scene_name, root_path, basename, ext, self.parts_preset)
        command.all_save_parts_scene(
            self.parts_preset, scene_name, root_path, basename, ext)

    def getSelectionMode(self):
        """選択時のヒエラルキー表示の状態を取得
        """
        self.selectionChildHighlightMode = cmds.selectPref(
            q=True, selectionChildHighlightMode=True)

    def setDefaultSelectPref(self):
        """選択時のヒエラルキー表示を元に戻す
        記憶した状態を戻すようにしていたが、強制的にMaya デフォルトの状態、
        ヒエラルキー全て選択にした
        """
        # cmds.selectPref(sch=self.selectionChildHighlightMode)
        cmds.selectPref(selectionChildHighlightMode=0)

    def changeHiliteSelectionType(self):
        """チェックボックスでの
        選択時のヒエラルキー表示の
        表示切替
        """
        value = self.UI.hiliteSelectionOnlyCheckBox.isChecked()
        if value:
            cmds.selectPref(selectionChildHighlightMode=1)
        else:
            cmds.selectPref(selectionChildHighlightMode=0)
            # cmds.selectPref(selectionChildHighlightMode=self.selectionChildHighlightMode)

    def closeEvent(self, event):
        """ツール終了時の実行コマンド

        グループ設定の保存
        選択時のヒエラルキー表示を元に戻す
        """
        self.writeFileInfo()
        self.setDefaultSelectPref()

    def select_item(self, item):
        """item を再帰的に取得し選択する
        都度都度選択なので重いかもしれない
        最終的には使っていない

        Args:
            item ([type]): [description]
        """
        item.setSelected(True)
        _range = item.childCount()
        for i in range(item.childCount()):
            child = item.child(i)
            self.select_item(child)

    def model_iter(self, model, parent_index=QtCore.QModelIndex(), col_iter=True):
        """

        Args:
            model ([type]): [description]
            parent_index ([type], optional): [description]. Defaults to QtCore.QModelIndex().
            col_iter (bool, optional): [description]. Defaults to True.

        Yields:
            [type]: [description]
        """
        index = model.index(0, 0, parent_index)

        while True:
            if col_iter:
                for col in range(0, model.columnCount(parent_index)):
                    yield index.sibling(index.row(), col)
            else:
                yield index

            if model.rowCount(index) > 0:
                for _ in self.model_iter(model, index, col_iter):
                    yield _

            index = index.sibling(index.row() + 1, index.column())
            if not index.isValid():
                break

    def selectAllGroup(self, *args):
        """グループ登録したノードを選択
        """

        # 選択を反映のチェックボックスを強制的に変更
        self.UI.groupTreeWidgetSelectRadioButton.setChecked(True)

        item = self.UI.groupTreeWidget.invisibleRootItem()

        # 空のリストにアイテムを追加、最後に選択
        _li = []
        items = self.getItemsToSelection(item, _li)

        if items:
            [x.setSelected(True) for x in items]

    def getItemsToSelection(self, item, item_list):
        """ツリーウィジェットのアイテムを親から再帰的に全ての子を取得

        Args:
            item (QtreeWidgetItem):
            item_list ([list]): アイテムをまとめるリスト

        Returns:
            [list]: 引数としてもらったリストを返す
        """
        count = item.childCount()
        if count:
            for i in range(count):
                child = item.child(i)
                item_list.append(child)
                self.getItemsToSelection(child, item_list)
        return item_list

    def checkParent(self, current):
        """親のノードをチェック

        Args:
            current ([type]): [description]

        Returns:
            [type]: [description]
        """
        _checkParentItem = None
        for p in command.get_parents(current):
            parent_short = cmds.ls(p, sn=True)[0]
            _checkParentItem = self.UI.groupTreeWidget.findItems(parent_short,
                                                                 QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive)
            if _checkParentItem:
                _checkParentItem = _checkParentItem[0]
                break
        return _checkParentItem

    def getChildNodeGroupTreeItems(self,
                                   current_node,
                                   parentItem=None,
                                   node_type="transform"):
        """再帰的に繰り返すことで選択以下の階層を登録している

        Args:
            current_node ([type]): [description]
            parentItem ([type], optional): [description]. Defaults to None.
            node_type (str, optional): [description]. Defaults to "transform".
        """
        current_short_name = cmds.ls(current_node, sn=True)[0]
        current_full_path = cmds.ls(current_node, l=True)[0]
        _flag = self.UI.registryHierarchycheckBox.isChecked()
        if not parentItem:
            parentItem = self.checkParent(current_node)
            if parentItem:
                # self.joint_dict[current_full_path] = current_short_name
                _c_item = QtWidgets.QTreeWidgetItem([current_short_name])
                parentItem.addChild(_c_item)
                parentItem = _c_item
            else:
                parentItem = QtWidgets.QTreeWidgetItem([current_short_name])
                self.UI.groupTreeWidget.addTopLevelItem(parentItem)

        children = cmds.listRelatives(
            current_node, children=True, type=node_type, path=True)

        if not children:
            return
        else:
            for child in children:
                if "_mtp_" in child:
                    continue
                _currentItem = self.UI.groupTreeWidget.findItems(child,
                                                                 QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive)
                child_full_path = cmds.ls(child, l=True)[0]
                if _currentItem:
                    _currentItem = _currentItem[0]
                    root = self.UI.groupTreeWidget.invisibleRootItem()
                    (_currentItem.parent() or root).removeChild(_currentItem)
                    parentItem.addChild(_currentItem)
                else:
                    if not _flag:
                        continue
                    _c_item = QtWidgets.QTreeWidgetItem([child])
                    parentItem.addChild(_c_item)
                    self.getChildNodeGroupTreeItems(child, _c_item, node_type)
                # self.joint_dict[child_full_path] = child

    def regitrRootJoint(self):
        _root_joint = command.get_root_joint()
        if not _root_joint:
            return

        _root_joint_short_name = cmds.ls(_root_joint, shortNames=True)[0]
        parentItem = QtWidgets.QTreeWidgetItem([_root_joint_short_name])
        self.UI.groupTreeWidget.addTopLevelItem(parentItem)

    def registMeshInfluenceJoints(self, *args):
        """登録されたメッシュからインフルエンスをたどって追加
        """
        root = self.UI.groupTreeWidget.invisibleRootItem()
        joint_items = []
        mesh_items = []
        for i in range(root.childCount()):
            child = root.child(i)
            short_name = child.text(0)
            # if not cmds.objExists(short_name):
            #     continue
            if cmds.nodeType(short_name) == "joint":
                joint_items.append(short_name)
            else:
                mesh_items.append(short_name)

        if mesh_items:
            joints = command.get_influence_joints_api2(mesh_items, joint_items)
            if not joints:
                return

            _check = self.UI.registryHierarchycheckBox.isChecked()
            self.UI.registryHierarchycheckBox.setChecked(False)
            self.registNodes(text_edit=False, preset_edit=True,
                             _selections=joints)
            self.UI.registryHierarchycheckBox.setChecked(_check)

    def registNodes(self, text_edit=False, preset_edit=True, _selections=[], *args):
        """ノードをツリーに登録

        Args:
            text_edit (bool): グループ名を変更
            preset_edit (bool): グループの内容を変更
            _selections (list): 初期選択状態
        """
        if not _selections:
            _selections = cmds.ls(sl=True, type="transform", long=True)

        if not _selections:
            return
        self.UI.groupTreeWidgetSelectRadioButton.setChecked(True)

        with gui_util.ProgressWindowBlock(title='Registration', maxValue=len(_selections)) as prg:
            prg.step(1)
            for _selection in _selections:
                prg.status = '[ {} ]'.format(_selection)
                prg.step(1)
                if "_mtp_" in _selection:
                    continue
                _short_name = cmds.ls(_selection, shortNames=True)[0]
                _currentItem = self.UI.groupTreeWidget.findItems(_short_name,
                                                                 QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive)
                if _currentItem:
                    continue
                self.getChildNodeGroupTreeItems(_selection)

        self.sortGroupTree()

        _short_names = cmds.ls(_selections, shortNames=True)
        self.selectTreeItems(self.UI.groupTreeWidget, _short_names)
        # self.selectNodeFromTree(self.UI.groupTreeWidget)
        self.UI.groupTreeWidget.expandAll()
        self.editPreset(text_edit=text_edit, preset_edit=preset_edit)

    def sortGroupTree(self):
        """グループツリーのソート
        ジョイント、メッシュの順番になるようにしている
        """
        root = self.UI.groupTreeWidget.invisibleRootItem()
        joint_items = []
        mesh_items = []
        for i in range(root.childCount()):
            child = root.child(i)
            short_name = child.text(0)
            # if not cmds.objExists(short_name):
            #     continue
            if cmds.nodeType(short_name) == "joint":
                joint_items.append(child)
            else:
                mesh_items.append(child)
        all_items = joint_items + mesh_items
        [(item.parent() or root).removeChild(item) for item in all_items]
        [self.UI.groupTreeWidget.addTopLevelItem(item) for item in all_items]

    def unRegistNodes(self, *args):
        """登録解除機能
        """
        root = self.UI.groupTreeWidget.invisibleRootItem()
        for item in self.UI.groupTreeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

        self.editPreset(text_edit=False, preset_edit=True)

    def selectTreeItems(self, treeWidget=QtWidgets.QTreeWidget, selections=[]):
        """ツリーウィジェットの選択動作

        Args:
            treeWidget ([QtWidgets.QTreeWidget]):ツリーウィジェット
            selections (list): Maya の選択ノード
        """

        if not selections:
            treeWidget.clearSelection()
            return

        current_selection = selections.pop(-1)
        currentGroupItem = treeWidget.findItems(current_selection,
                                                QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive)
        if not currentGroupItem:
            return
        currentGroupItem = currentGroupItem[0]
        treeWidget.setCurrentItem(currentGroupItem)

        for short_name in selections:
            if not cmds.objExists(short_name):
                continue
            _currentItem = treeWidget.findItems(short_name,
                                                QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive)
            if _currentItem:
                _currentItem = _currentItem[0]
                treeWidget.setItemSelected(_currentItem, True)

    # def selectionChange(self, *args):
    #     """scriptJob での選択切り替え時の動作
    #     ツリーウィジェットの選択を行う
    #     """
    #     _tree_flag = self.UI.treeWidgetSelectRadioButton.isChecked()
    #     _tree_group_flag = self.UI.groupTreeWidgetSelectRadioButton.isChecked()

    #     # _selections = cmds.ls(sl=True, type="transform", long=True)
    #     # _short_names = cmds.ls(_selections, shortNames=True)
    #     _selections = cmds.ls(sl=True, type="transform", shortNames=True)

    #     if _tree_flag:
    #         self.UI.groupTreeWidget.clearSelection()
    #         self.selectTreeItems(self.UI.treeWidget, _selections)

    #     else:
    #         self.UI.treeWidget.clearSelection()
    #         self.selectTreeItems(self.UI.groupTreeWidget, _selections)

    def checkStrings(self, _text=""):
        """グループ作成時に文字列をチェック
        ディレクトリ名に使えない文字列を弾く

        Args:
            _text ([str]): 検査する文字列

        Returns:
            [bool]: 検査結果
            問題なければ True
        """
        _m = u""
        for _t in _text:
            if _t in u':;/\|,*?"<>':
                _m = u']:;/\|,*?"<> \n\nの含まれる文字は使用できません'
                break

        if _m:
            _d = gui_util.ConformDialog(message=_m)
            _d.exec_()
            return
        return True

    def checkExists(self, _text=""):
        """グループ名が既に存在するかを確認する

        Args:
            _text (str): 確認するグループ名

        Returns:
            [bool]: 検査結果
            問題なければ Ture
        """
        _m = u""
        print(self.parts_preset, " --- self.parts_preset")
        if self.parts_preset:
            if _text in self.parts_preset:
                _m = u"[ {} ] は既に存在します".format(_text)

        if _m:
            _d = gui_util.ConformDialog(message=_m)
            _d.exec_()
            return
        return True

    # def getShortNameLongName(self):
    #     """アウトライナの順番を元に戻すための機能
    #     結局使わなくなった
    #     """
    #     self.short_name_long_name = dict()
    #     self.short_name_parent = dict()
    #     self.short_name_children = dict()

    #     _nodes = [self.root_joint, self.model_group]
    #     _nodes = []
    #     for node in [self.root_joint, self.model_group]:
    #         temp_list = []
    #         l = command.get_children(node, temp_list)
    #         _nodes.extend(l)
    #     for node in _nodes:
    #         _short_name = cmds.ls(node, shortNames=True)[0]
    #         _parent = cmds.listRelatives(node, parent=True, path=True)
    #         _children = cmds.listRelatives(node, children=True, path=True)
    #         self.short_name_long_name[_short_name] = node
    #         self.short_name_parent[_short_name] = _parent
    #         self.short_name_children[_short_name] = _children

    def getDefaultVisibleState(self):
        self.visible_states = dict()
        _nodes = [self.root_joint, self.model_group]
        _nodes.extend(cmds.listRelatives(self.root_joint,
                      ad=True, type="transform", f=True))
        _nodes.extend(cmds.listRelatives(self.model_group,
                      ad=True, type="transform", f=True))
        for node in _nodes:
            self.visible_states[node] = True

    def _getCurrentGroupTreeItems(self):
        """もっと簡単な方法がないかと探ったもの
        階層を深く取れなかった

        Returns:
            [type]: [description]
        """
        self.node_childern = dict()
        # self.root_nodes = dict()
        root_nodes = []

        item = self.UI.groupTreeWidget.invisibleRootItem()
        _li = []
        items = self.getItemsToSelection(item, _li)

        for i in range(root.childCount()):
            _children = []
            child = root.child(i)
            short_name = child.text(0)

            if not child.parent():
                root_nodes.append(short_name)
            for _i in range(child.childCount()):
                _children.append(child.child(_i).text(0))

            if _children:
                self.node_childern[short_name] = _children
            else:
                self.node_childern[short_name] = [None]

        self.UI.groupTreeWidget.expandAll()
        return root_nodes

    def getCurrentGroupTreeItems(self):
        """グループを記憶するのに使用
        この方法でないと階層を全部掘り下げられなかった
        self.node_childern にノードのショートパスと子供を入れている

        Returns:
            [list]: ルートジョイント直下になるべきジョイント
        """
        self.node_childern = dict()
        # self.root_nodes = dict()
        root_nodes = []

        for _index in self.model_iter(self.UI.groupTreeWidget.model()):
            _children = []
            _short_name = _index.data(QtCore.Qt.DisplayRole)

            _currentItem = self.UI.groupTreeWidget.findItems(_short_name,
                                                             QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive)
            if not _currentItem:
                continue
            _currentItem = _currentItem[0]
            if not _currentItem.parent():
                root_nodes.append(_short_name)
            for _i in range(_currentItem.childCount()):
                _children.append(_currentItem.child(_i).text(0))

            if _children:
                self.node_childern[_short_name] = _children
            else:
                self.node_childern[_short_name] = [None]

        self.UI.groupTreeWidget.expandAll()
        return root_nodes

    def getTextDialog(self, message=None, default=None):
        """グループ追加、名前編集時に出すダイアログ
        テキストの内容チェック、既存グループとの確認をしている

        Args:
            message ([str]): ウィンドウ内に表示するメッセージ
            default ([str]): デフォルト値、グループ名編集時元の名前を表示させる

        Returns:
            [str]: 問題なければ文字列を返す
        """
        _d = gui_util.PromptDialog(message=message, default=default)
        result = _d.exec_()
        if not result:
            return
        _text = _d.textValue()

        if not _text:
            return
        if not self.checkStrings(_text):
            return
        if not self.checkExists(_text):
            return
        return _text

    def addPreset(self):
        """グループ追加処理
        """
        root_nodes = []
        _current_preset = self.UI.presetComboBox.currentText()

        _m = u"グループを作成します"
        _m += u"\nグループ名を入力してください"

        _text = self.getTextDialog(_m)
        if not _text:
            return

        self.UI.presetComboBox.addItem(_text)
        _selections = cmds.ls(sl=True, type="transform", long=True)
        if _current_preset == self.defaultConboBoxText:
            if _selections:
                self.registNodes(text_edit=False,
                                 preset_edit=False,
                                 _selections=_selections)
        else:
            self.UI.groupTreeWidget.clear()
            if _selections:
                self.registNodes(text_edit=False,
                                 preset_edit=False,
                                 _selections=_selections)

        root_nodes = self.getCurrentGroupTreeItems()
        self.parts_preset[_text] = self.node_childern
        self.root_nodes[_text] = root_nodes

        self.UI.presetComboBox.setCurrentIndex(
            self.UI.presetComboBox.count()-1)
        self.UI.groupTreeWidget.expandAll()
        self.writeFileInfo()

    def editPreset(self, text_edit=True, preset_edit=True):
        """グループ名編集処理

        Args:
            text_edit (bool): グループ名を変更するフラグ
            preset_edit (bool): グループ内容を変更するフラグ
        """
        # root_nodes = []

        _current_preset = self.UI.presetComboBox.currentText()
        _current_preset_index = self.UI.presetComboBox.currentIndex()
        if _current_preset == self.defaultConboBoxText:
            return

        _m = u"現在のグループを変更します"
        _m += u"\nグループ名を入力してください"

        if text_edit:
            _text = self.getTextDialog(_m, _current_preset)
            if not _text:
                return
        else:
            _text = _current_preset

        if _current_preset != self.defaultConboBoxText and preset_edit:
            if _current_preset in self.parts_preset:
                del self.parts_preset[_current_preset]
            if _current_preset in self.root_nodes:
                del self.root_nodes[_current_preset]

            root_nodes = self.getCurrentGroupTreeItems()
            self.parts_preset[_text] = self.node_childern
            self.root_nodes[_text] = root_nodes

        self.UI.presetComboBox.setItemText(_current_preset_index, _text)
        self.UI.groupTreeWidget.expandAll()
        self.writeFileInfo()

    def deletePreset(self):
        """グループ削除処理
        """
        _current_preset = self.UI.presetComboBox.currentText()
        _current_preset_index = self.UI.presetComboBox.currentIndex()

        if _current_preset == self.defaultConboBoxText:
            self.UI.groupTreeWidget.clear()
            return

        self.UI.presetComboBox.removeItem(_current_preset_index)
        self.UI.presetComboBox.setCurrentIndex(_current_preset_index-1)

        if _current_preset in self.parts_preset:
            del self.parts_preset[_current_preset]
        if _current_preset in self.root_nodes:
            del self.root_nodes[_current_preset]
        self.writeFileInfo()

    def buildTree(self, current_node=None, child=None):
        """comboBox でグループが切り替わった時のツリーの表示切り替え処理

        Args:
            current_node ([str]): Maya トランスフォームノードのショートパス
            child ([list], None): current_node の子のノード、無ければ None
        """
        _current_preset = self.UI.presetComboBox.currentText()
        _current_root_nodes = self.root_nodes.get(_current_preset, None)

        _currentItem = self.UI.groupTreeWidget.findItems(current_node,
                                                         QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive)
        if _currentItem:
            _currentItem = _currentItem[0]
        else:
            _currentItem = QtWidgets.QTreeWidgetItem(
                [current_node.split("|")[-1]])

        if current_node in _current_root_nodes:
            self.UI.groupTreeWidget.addTopLevelItem(_currentItem)

        if child and cmds.objExists(child):
            _c_item = QtWidgets.QTreeWidgetItem([child])
            _currentItem.addChild(_c_item)

    def changePreset(self, *args):
        """comboBox を変更してグループ切り替え処理
        """
        _current_preset = self.UI.presetComboBox.currentText()
        _nodes_children = self.parts_preset.get(_current_preset, None)
        _current_root_nodes = self.root_nodes.get(_current_preset, None)
        self.UI.groupTreeWidget.clear()

        if not _nodes_children or not _current_root_nodes:
            return

        if _current_preset == self.defaultConboBoxText:
            return

        for _short_name, children in _nodes_children.items():
            if not cmds.objExists(_short_name):
                continue
            for child in children:
                self.buildTree(_short_name, child)

        self.UI.groupTreeWidget.expandAll()

    def eventFilter(self, obj, event):
        """expand 時にshift キーなどを押して全展開したかった
        """
        # print(obj, event.type(), " -----")#Timer, MouseButtonPress
        if (obj == self.UI.treeWidget and
                event.type() == QtCore.QEvent.Timer):
            print(event, " ---- event")
            print(event.type())
            index = self.UI.treeWidget.currentIndex()
            print(index.data(QtCore.Qt.DisplayRole))

    def _eventFilter(self, obj, event):
        """expand 時にshift キーなどを押して全展開したかった
        """
        # for _index in self.model_iter(self.UI.treeWidget.model()):
        #     _short_name = _index.data(QtCore.Qt.DisplayRole)
        #     print(_short_name)
        getSelected = self.UI.treeWidget.selectedItems()
        getChildNode = None
        # print(self.UI.treeWidget.currentIndex(), " ====")
        if getSelected:
            baseNode = getSelected[0]
            getChildNode = baseNode.text(0)
            # print(getChildNode)
        if obj == self.UI.treeWidget:
            if event.type() == QtCore.QEvent.KeyPress:
                key = event.key()
                mod = event.modifiers()
                pressed = QtGui.QKeySequence(key).toString()
                index = self.UI.treeWidget.currentIndex()
                print(self.UI.treeWidget.selectedIndexes())
                print(index.data(QtCore.Qt.DisplayRole))
                # childCount = index.internalPointer().get_child_count()
                # print(index, "! ---- index")
                if mod == QtCore.Qt.ShiftModifier:
                    # self.UI.treeWidget.expandAll()

                    # for _index in self.model_iter(self.UI.treeWidget.model()):
                    #     _short_name = _index.data(QtCore.Qt.DisplayRole)
                    #     print(_short_name)
                    # print(childCount, " ---- ")
                    print(pressed)
                    print(mod == QtCore.Qt.ShiftModifier)
                    print(mod == QtCore.Qt.ControlModifier)
                    print(getChildNode)
                # if mod == QtCore.Qt.ShiftModifier and pressed == "H":
                #     # print(pressed)
                #     # print("------")
                #     self.unHideSelections()
                elif pressed == "F":
                    self.fitView()
                elif pressed == "H":
                    _value = cmds.optionVar(
                        q="toggleVisibilityAndKeepSelectionBehaviour")
                    maya.mel.eval(
                        'toggleVisibilityAndKeepSelection {};'.format(_value))

                # if event.key() == QtCore.Qt.Key_Return:
                #     print("enter pressed")
        return super(QtWidgets.QMainWindow, self).eventFilter(obj, event)

    # def unHideSelections(self, *args):
    #     _select = []
    #     for QModelIndex in self.UI.treeWidget.selectedIndexes():
    #         text = QModelIndex.data(QtCore.Qt.DisplayRole)
    #         # if cmds.objExists(text):
    #         full_path_name = [long_name for long_name,short_name in self.joint_dict.items()
    #                         if short_name==text]
    #         if full_path_name:
    #             _select.extend(full_path_name)

    #     if _select:
    #         _flag = cmds.getAttr("{}.v".format(self.joint_dict.keys()[0]))
    #         parent_nodes = set()
    #         for long_name in self.joint_dict.keys():
    #             if cmds.objExists(long_name):
    #                 if long_name in _select:
    #                     cmds.setAttr("{}.v".format(long_name), _flag)
    #                 else:
    #                     cmds.setAttr("{}.v".format(long_name), not _flag)
    #                     for parent in command.get_parents(long_name):
    #                         parent_nodes.add(parent)
    #         if parent_nodes:
    #             for parent in list(parent_nodes):
    #                 cmds.setAttr("{}.v".format(parent), 1)

    def getChildNodeTreeItems(self, current_node, parentItem=None, node_type="transform"):
        """treeWidget の全アイテムを取得し
        self.joint_dict にフルパス、ショートパスを入れている

        Args:
            current_node ([str]): Maya ノードのフルパス
            parentItem ([QTreeWidgetItem]): ツリーの親となるアイテム
            node_type (str, [joint or transform]): 取得するべきノードのタイプ
        """
        # 親がない場合は自身が親
        # print(current_node)
        # print(parentItem)
        # print(node_type)
        if not parentItem:
            parentItem = QtWidgets.QTreeWidgetItem(
                [current_node.split("|")[-1]])
            self.UI.treeWidget.addTopLevelItem(parentItem)

        # 子のノードを取得

        # children = cmds.listRelatives(current_node, c=True, type=node_type)
        children = command.get_children_fullpath_dict(
            current_node=current_node, node_type=node_type)

        if not children:
            return

        # 取得した子のノードのフルパス、ショートパスを辞書に格納
        # 子供のノードを QTreeWidgetItem にし、
        # parentItem の子供にして再帰を繰り返す
        for fullpath, shortname in children.items():
            if "lod" in fullpath:
                continue
            self.fullpath_shortname[fullpath] = shortname
            _c_item = QtWidgets.QTreeWidgetItem([shortname])
            parentItem.addChild(_c_item)
            self.getChildNodeTreeItems(shortname, _c_item, node_type)

    def clearItem(self):
        """各ウィジェットの内容をクリア
        """
        # 初期化時に treeWidget をクリア
        self.UI.treeWidget.clear()

        # presetComboBox がデフォルト値であれば、groupTreeWidget もクリア
        _current_preset = self.UI.presetComboBox.currentText()
        if _current_preset == self.defaultConboBoxText:
            self.UI.groupTreeWidget.clear()

        # presetComboBox　をクリア後デフォルト値追加
        self.UI.presetComboBox.clear()
        self.UI.presetComboBox.addItem(self.defaultConboBoxText)

    def readFileInfo(self):
        """fileInfo に書かれた情報を読み込み変数に代入
        """
        _node_childern = "{}_{}".format(NAME, NODE_CHILDREN)
        _group_root_name = "{}_{}".format(NAME, GROUP_ROOTNODES)
        parts_preset = command.file_info_load(_node_childern)
        group_root_node = command.file_info_load(_group_root_name)
        if parts_preset:
            self.parts_preset = parts_preset
            self.root_nodes = group_root_node

    def checkPreset(self):
        """記憶しているグループの確認
        シーンに該当ノードがない場合は辞書から削除している
        """
        _parts_preset = dict()
        _root_nodes = dict()
        for group_name, child in self.parts_preset.items():
            for node, children in child.items():
                if not cmds.objExists(node):
                    del child[node]
            root_nodes = self.root_nodes.get(group_name, None)
            if not root_nodes:
                continue
            for root_node in root_nodes:
                if not cmds.objExists(root_node):
                    del root_nodes[root_node]
            _parts_preset[group_name] = child
            _root_nodes[group_name] = root_nodes
        self.parts_preset = _parts_preset
        self.root_nodes = _root_nodes

    def writeFileInfo(self):
        """
        _node_childern は
        PartsSplitExporter_NodeChildren
        という名前でfileInfo に記憶
        self.parts_preset
        ノードとそのノードの子供

        _group_root_node は
        PartsSplitExporter_GroupRootNodes
        という名前でfileInfo に記憶
        self.root_nodes
        ツリーでルートになるべきノード
        """
        _node_childern = "{}_{}".format(NAME, NODE_CHILDREN)
        _group_root_node = "{}_{}".format(NAME, GROUP_ROOTNODES)
        # command.file_info_save(_node_childern, "")
        # command.file_info_save(_group_root_node, "")
        if self.parts_preset:
            command.file_info_save(_node_childern, self.parts_preset)
        else:
            command.file_info_save(_node_childern, "")
        if self.root_nodes:
            command.file_info_save(_group_root_node, self.root_nodes)
        else:
            command.file_info_save(_group_root_node, "")

    def getSceneObjects(self):
        """シーンの各情報を取得
        ツール起動時とscriptJob でシーンが開かれた時に実行される
        """
        # self.joint_dict = dict()
        self.clearItem()
        self.readFileInfo()
        self.root_joint = None
        self.model_group = None

        _model_group = None
        root_node = None

        # jnt_0000_skl_root の名前のジョイントを取ってくる
        _root_joint = command.get_root_joint()
        if not _root_joint:
            return

        # ルートジョイントから再帰的に親を取って最後のノードを取ってくる
        root_node = command.get_root_node(_root_joint)

        # ルートノード以下のノードで「model」という名前のノードを取ってくる
        _model_group = command.get_model_node(root_node)

        if not _model_group:
            return

        self.root_joint = _root_joint
        self.model_group = _model_group

        # ルートジョイント、モデルグループの子供のノードをたどってツリーに登録
        self.getChildNodeTreeItems(_root_joint)
        self.getChildNodeTreeItems(_model_group, node_type="transform")

        # 読み込んだ初期設定に self.parts_preset があれば、comboBox を作る
        # groupTreeWidget は常に展開された状態にしたい
        if isinstance(self.parts_preset, dict):
            self.buildConboBox()
            self.UI.groupTreeWidget.expandAll()

        # ショートパス、ロングパス
        # ショートパス、親
        # ショートパス、子供
        # の辞書作成
        # self.getShortNameLongName()

    def buildConboBox(self):
        """グループを取得したらグループ名でcomboBox にテキスト追加
        """
        for k, v in self.parts_preset.items():
            self.UI.presetComboBox.addItem(k)
        self.UI.presetComboBox.setCurrentIndex(
            self.UI.presetComboBox.count()-1)

    def rebuildConboBox(self):
        """グループのcomboBox を一旦クリアする処理
        """
        self.UI.presetComboBox.clear()
        self.UI.presetComboBox.addItem(self.defaultConboBoxText)
        self.buildConboBox()

    def fitOutliner(self):
        """Maya Outliner 全てのアウトライナを取得し、showSelected をオンにする
        """
        _outliners = [x for x in cmds.getPanel(type="outlinerPanel")
                      if x in cmds.getPanel(vis=True)]
        if _outliners:
            [cmds.outlinerEditor(x, e=True, showSelected=True)
             for x in _outliners]

    def xrayJoint(self):
        """XRayJointsCheckBox チェックボックスの動作
        ジョイントのxray をチェックボックスと同じにする
        """
        value = self.UI.XRayJointsCheckBox.isChecked()
        _modelpanels = cmds.getPanel(type="modelPanel")
        if _modelpanels:
            for _modelpanes in _modelpanels:
                cmds.modelEditor(_modelpanes, e=True, jx=value)

    def radioButtonCallBack(self, *args):
        """選択を同期、ラジオボタンの動作
        treeWidget, groupTreeWidget どちらのリストを選択で使用するか
        """
        # _selections = cmds.ls(sl=True, type="transform", long=True)
        # _short_names = cmds.ls(_selections, shortNames=True)
        _tree_flag = self.UI.treeWidgetSelectRadioButton.isChecked()
        _tree_group_flag = self.UI.groupTreeWidgetSelectRadioButton.isChecked()
        _short_names = cmds.ls(sl=True, type="transform", shortNames=True)
        return
        print("0------")
        print(_tree_group_flag)
        print(_tree_flag)
        if _tree_flag:
            self.selectTreeItems(self.UI.treeWidget, _short_names)
            # self.selectNodeFromTree(self.UI.treeWidget)
            self.UI.groupTreeWidgetSelectRadioButton.setChecked(False)
        else:
            self.selectTreeItems(self.UI.groupTreeWidget, _short_names)
            # self.selectNodeFromTree(self.UI.groupTreeWidget)
            self.UI.treeWidgetSelectRadioButton.setChecked(False)

    def groupTreeWidgetSelectChanged(self, selected, deselected):
        """groupTreeWidget の選択動作

        Args:
            selected ([type]): [description]
            deselected ([type]): [description]
        """

        # 「選択の同期」ラジオボタンの状態
        _flag = self.UI.groupTreeWidgetSelectRadioButton.isChecked()

        if not _flag:
            # self.UI.treeWidget.clearSelection()
            return
        # selections = cmds.ls(sl=True, type="transform", shortNames=True)

        # 選択されたアイテムのテキストを取得、ノードが存在していればリストに入れる
        _select = []
        for QModelIndex in self.UI.groupTreeWidget.selectedIndexes():
            text = QModelIndex.data(QtCore.Qt.DisplayRole)
            if cmds.objExists(text):
                _select.append(text)

        # リストが空でない場合は選択しなおし
        # 空の時は選択をクリア
        if _select:
            cmds.select(_select, r=True)
        else:
            cmds.select(cl=True)

        # アウトライナフィット
        self.fitOutliner()

    def treeWidgetSelectChanged(self, selected, deselected):
        """treeWidget の選択動作

        Args:
            selected ([type]): [description]
            deselected ([type]): [description]
        """

        # 「選択の同期」ラジオボタンの状態
        _flag = self.UI.treeWidgetSelectRadioButton.isChecked()

        if not _flag:
            # self.UI.groupTreeWidget.clearSelection()
            return

        # 選択されたアイテムのテキストを取得、ノードが存在していればリストに入れる
        _select = []
        for QModelIndex in self.UI.treeWidget.selectedIndexes():
            text = QModelIndex.data(QtCore.Qt.DisplayRole)
            _select.append(text)

        # リストが空でない場合は選択しなおし
        # 空の時は選択をクリア
        if _select:
            cmds.select(_select, r=True)
        else:
            cmds.select(cl=True)

        # アウトライナフィット
        self.fitOutliner()

    def importFileDialog(self):
        """書き出したyaml ファイルの読み込み
        """
        scene_name, root_path, basename, ext = command.set_up_scene_path()
        if not ext:
            return

        filters = "Yaml files (*.yaml)"
        title = u"yaml ファイルを選択してください"
        dialog = QtWidgets.QFileDialog(directory=root_path)

        (file_paths, selectedFilter) = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                                              title,
                                                                              "",
                                                                              filters)

        # 読み込んだyaml から辞書を復元
        _parts_preset, _root_nodes = command.yaml_load_files(file_paths)
        if _parts_preset:
            for group_name, node_childern in _parts_preset.items():
                self.parts_preset[group_name] = node_childern
                _roots = _root_nodes.get(group_name, None)
                if _roots:
                    self.root_nodes[group_name] = _roots
            self.checkPreset()
            self.writeFileInfo()
            self.rebuildConboBox()

    def exportFileDirectoryDialog(self):
        """yaml ファイルの書き出し
        """

        scene_name, root_path, basename, ext = command.set_up_scene_path()
        if not ext:
            return
        if not self.parts_preset:
            return

        dialog = QtWidgets.QFileDialog(directory=root_path)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)

        path = ""
        if dialog.exec_():
            path = dialog.selectedFiles()[0]

        # yaml_file_path: stat の辞書を貰う
        _yml_path_stat = command.check_p4state_yaml_files(
            path, self.parts_preset.keys())
        self.checkPreset()

        command.yaml_save_files_p4(
            _yml_path_stat, self.parts_preset, self.root_nodes)

    def openHelp(self):
        _web_site = "https://wisdom.cygames.jp/display/mutsunokami/Maya:+Parts+Split+Exporter"
        webbrowser.open(_web_site)


def main():
    print("launch ----")

    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == CLASS_NAME:
            _obj.close()
            del _obj

    if not os.path.exists(UI_FILE):
        # cmds.warning(u"UI ファイルが見つかりません")
        if not DEV_MODE:
            _m = "not found UI file [ {} ]".format(
                UI_FILE.replace(os.sep, '/'))
            logger.error(_m)
        return

    ui = PartsSplitExporter()
    ui.show()
    if not DEV_MODE:
        logger.send_launch(u'ツール起動')
