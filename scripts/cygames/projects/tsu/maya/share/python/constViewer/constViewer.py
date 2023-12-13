# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : constViewer
# Author  : toi
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import maya.mel as mm
import os
import sys
import time
import json
import stat
from functools import partial
from collections import OrderedDict
from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import ui

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__

tree_view_name = 'constViewerTreeView'


class ExampleTreeView(QTreeView):
    def __init__(self, *args, **kwargs):
        #super(ExampleTreeView, self).__init__()
        super().__init__()
        self.headView = self.header()
        self.setObjectName(tree_view_name)
        self.headView.setObjectName(tree_view_name)

        self.tags = args[0]
        self.initUi()

    def initUi(self):
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setUniformRowHeights(True)
        # self.setHeaderHidden(True)
        # self.setSortingEnabled(False)

        self.stdItemModel = QStandardItemModel()
        self.stdItemModel.setColumnCount(1)
        self.stdItemModel.setHeaderData(0, Qt.Horizontal, "")

        self.setModel(self.stdItemModel)

        self.populateTree(self.tags)
        self.expandAll()

        self.pressed.connect(self._pressedItem)

    def _pressedItem(self, event):
        data_name = event.data()
        cmds.select(data_name)

    def populateTree(self, children, parent=None):
        if children is not None:
            for num, child in enumerate(sorted(children)):
                node = QStandardItem(child)
                if parent is None:
                    self.stdItemModel.appendRow(node)
                else:
                    parent.setChild(num, node)

                if isinstance(children, dict):
                    self.populateTree(children[child], node)


class ConstViewer(ui.QWindow):
    def __init__(self, *args, **kwargs):
        #super(ConstViewer, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

        const = cm.getConstraintTarget(cmds.ls(sl=True))
        self.example_tree_view = ExampleTreeView(const)

        self.setCentralWidget(self.example_tree_view)
        self.resize(350, 400)
        self.setStyleSheet("""
/* ----- QTreeView -----  */
QTreeView#{0} {{
    font-size: 18px;
}}

QTreeView::branch:selected#{0} {{
    background-color: #191970;
}}
QTreeView::item:hover#{0} {{
    background-color: #4169e1;
}}
QTreeView::item:selected#{0} {{
    color: #40c2fa;
    background-color: #191970;
}}
 
/* ----- QHeaderView ----- */
QHeaderView#{0} {{
    font-size: 10px;
    font-weight: 900;
    font-family: Yu Gothic;
    text-transform: uppercase;
    background-color: #4169e1;
}}
        """.format(tree_view_name))
        self.show()


def main():
    ConstViewer('Const Viewer')


