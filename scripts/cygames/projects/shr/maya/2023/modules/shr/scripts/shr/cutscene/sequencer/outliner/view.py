from __future__ import annotations

import typing as tp
from pprint import pprint

from maya import cmds
from shr.cutscene.sequencer.lib.qt import MayaMainWindowBase
from shr.cutscene.sequencer.outliner.model import (OutlinerActorData,
                                                   OutlinerMotionData,
                                                   collect_actor_data)
from PySide2 import QtCore, QtGui, QtWidgets


class OutlineWindow(MayaMainWindowBase):
    """アウトライナーウィンドウ
    """

    def __init__(self):
        super().__init__()

    def setup(self, central_widget) -> None:
        self.setObjectName(self.abolute_name)
        self.setWindowTitle("Seq Outliner")
        self.resize(500, 500)

        self.layout = QtWidgets.QVBoxLayout(central_widget)
        self.layout.setContentsMargins(2, 2, 2, 2)

        self.model = QtGui.QStandardItemModel()
        self.model.setItemPrototype(OutlinerBaseItem())

        self.view = OutlinerTreeView()
        self.view.setModel(self.model)

        self.layout.addWidget(self.view)

        self.init()

        self.view.expanded.connect(self.expanded)
        self.view.selectionModel().selectionChanged.connect(self.selection_changed)

    def expanded(self, idx):
        item = self.model.itemFromIndex(idx)

        if item.hasChildren():
            for row in range(item.rowCount()):
                child = item.child(row)
                child.removeRows(0, child.rowCount())

                if hasattr(child, "child_node"):
                    children_nodes = child.child_node
                    child.appendRows(children_nodes)

    def selection_changed(self, selected, deselected):
        indexes = self.view.selectedIndexes()
        nodes = []
        for index in indexes:
            item = self.model.itemFromIndex(index)
            if isinstance(item, NodeTreeItem):
                nodes.append(item.fullname)

            if isinstance(item, ClipItem):
                nodes.extend(item.motion_data.motion_nodes)

            if isinstance(item, ActorTitleItem):
                nodes.extend(item.actor_data.actor_node)

            if isinstance(item, MotionsTitleItem):
                clip_items = item.child_node
                for clip in clip_items:
                    nodes.extend(clip.motion_data.motion_nodes)

            if isinstance(item, ActorGroupItem):
                actor_title_item, motion_title_item = item.child_node
                actor_node_items = actor_title_item.child_node
                for actor_node_item in actor_node_items:
                    nodes.append(actor_node_item.fullname)

                clip_items = motion_title_item.child_node
                for clip_item in clip_items:
                    for node_item in clip_item.child_node:
                        nodes.append(node_item.fullname)

        if nodes:
            cmds.select(nodes, replace=True)
        else:
            cmds.select(clear=True)

    def init(self):
        self.model.clear()

        roots = self.root_scan()
        if roots:
            self.model.appendColumn(roots)

    def root_scan(self):
        actor_data_list = collect_actor_data()
        if actor_data_list == []:
            return None

        actor_group_item_list = []
        for actor_data in actor_data_list:
            actor_item = ActorGroupItem(actor_data.name, actor_data)
            actor_title_item, motion_title_item = actor_item.child_node
            actor_item.appendRows([actor_title_item, motion_title_item])

            actor_group_item_list.append(actor_item)

        return actor_group_item_list


class OutlinerTreeView(QtWidgets.QTreeView):
    """アウトライナー用のツリービュー
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.header().setVisible(False)
        self.setEditTriggers(self.NoEditTriggers)
        self.setSelectionMode(self.ExtendedSelection)
        self.setContentsMargins(100, 100, 5, 5)
        self.setIndentation(15)


class OutlinerBaseItem(QtGui.QStandardItem):
    def __init__(self, name=""):
        super().__init__()
        self.setText(name)
        self.setSizeHint(QtCore.QSize(100, 25))


class ActorGroupItem(OutlinerBaseItem):
    def __init__(self, name, actor_data: OutlinerActorData):
        self.actor_data = actor_data
        super().__init__(name)

    @property
    def child_node(self) -> tp.Tuple[ActorTitleItem, MotionsTitleItem]:
        actor_title_item = ActorTitleItem(self.actor_data)
        motion_title_item = MotionsTitleItem(self.actor_data)

        return (actor_title_item, motion_title_item)


class ActorTitleItem(OutlinerBaseItem):
    def __init__(self, actor_data: OutlinerActorData):
        super().__init__("Actor")
        self.actor_data = actor_data

    @property
    def child_node(self):
        item_list: tp.List[NodeTreeItem] = []
        for node in self.actor_data.actor_node:
            node_item = NodeTreeItem(cmds.ls(node, long=True)[0])
            item_list.append(node_item)

        return item_list


class ClipItem(OutlinerBaseItem):
    def __init__(self, motion_data: OutlinerMotionData):
        self.motion_data = motion_data
        super().__init__(motion_data.name)
        self.setBackground(motion_data.background_color)

    @property
    def child_node(self):
        item_list: tp.List[NodeTreeItem] = []
        for node in self.motion_data.motion_nodes:
            node_item = NodeTreeItem(cmds.ls(node, long=True)[0])
            item_list.append(node_item)

        return item_list


class MotionsTitleItem(OutlinerBaseItem):
    def __init__(self, actor_data: OutlinerActorData):
        self.actor_data = actor_data
        super().__init__("Motions")
        self.setBackground(self.actor_data.motion_data[0].background_color)

    @property
    def child_node(self):
        item_list: tp.List[ClipItem] = []
        for motion in self.actor_data.motion_data:
            clip_item = ClipItem(motion)
            item_list.append(clip_item)

        return item_list


class NodeTreeItem(OutlinerBaseItem):
    """
    """

    DEFAULT_ICON = ":default.svg"

    def __init__(self, full_path=None):
        self.node = full_path
        super().__init__(self.name)

        self.icon_name = self.DEFAULT_ICON
        self.update_icon()

        self.setSizeHint(QtCore.QSize(100, 30))

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.name)

    @property
    def fullname(self):
        if self.node:
            return self.node

    @property
    def name(self):
        if self.node:
            nodes = cmds.ls(self.node)
            return nodes[0]

    @property
    def parentname(self):
        if self.node:
            return self.fullname.rsplit('|', 1)[0]

    @property
    def is_child(self):
        if cmds.listRelatives(self.fullname, children=True, type="transform"):
            return True
        else:
            return False

    @property
    def child_node(self):
        nodes = cmds.listRelatives(self.fullname, children=True, type="transform")
        if nodes:
            return [NodeTreeItem(_) for _ in nodes]
        else:
            return []

    def update_icon(self):
        icon_path = self.fetch_icon(self.name)
        self.setIcon(QtGui.QIcon(icon_path))

    def fetch_icon(self, node_obj) -> str:
        if not node_obj:
            return None
        icon_name = None
        if cmds.objExists(node_obj):
            node_type = cmds.nodeType(node_obj)
            shapes = cmds.listRelatives(node_obj, s=True, pa=True)
            icon_name = ':%s.svg' % node_type
            if node_type == 'transform' and shapes:
                node_type = cmds.nodeType(shapes[0])
                icon_name = ':%s.svg' % node_type

                if node_type == 'spotLight':
                    icon_name = ':%s.svg' % node_type.lower()

                if node_type == 'volumeLight':
                    icon_name = ':%s.png' % node_type.lower()

            if not QtCore.QResource(icon_name).isValid():
                icon_name = self.DEFAULT_ICON

        return icon_name
