#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# DestinationView.py
#

import os
import sys
import re

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI

class DestinationView(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        super(DestinationView, self).__init__(parent)
        self.parent = parent
        self.setup()

    def setup(self):
        self.copy_items = self.parent.copyList
        
        self.clicked[QtCore.QModelIndex].connect(self.clickEvent)
        self.headerItem().setText(0, u'コピー先')
        self.setExpandsOnDoubleClick(False)
        self.setAlternatingRowColors(True)
        self.setStyle(QtGui.QStyleFactory.create("CDE"))

        self.setRootNode()

    def clickEvent(self):
        item = self.currentItem().text(0)
        self.parent.changeCurrentItem(item)

    def setRootNode(self):
        self.clear()
        self.root = cmds.ls(sl=True)

        root_item = QtGui.QTreeWidgetItem(self)
        root_item.setText(0, self.root[0])
        self.addTopLevelItem(root_item)

        if root_item.text(0) in self.copy_items:
            root_item.setBackground(0 , QtGui.QBrush(QtGui.QColor(51,153,204,70)))

        self.buildDestionationTree(root_item)
        self.expandAll()


    def buildDestionationTree(self, parent_item):
        children = cmds.listRelatives(parent_item.text(0), path=True)
        shapes = cmds.listRelatives(parent_item.text(0), shapes=True, path=True)

        if children:
            for child in children:  
                if shapes:
                    if child not in shapes:
                        child_item = self.addItem(child, parent_item)
                        self.buildDestionationTree(child_item)
                else:
                    child_item = self.addItem(child, parent_item)
                    self.buildDestionationTree(child_item)

    def addItem(self, node, parent=None):
        item = QtGui.QTreeWidgetItem(parent)
        parent.addChild(item)
        item.setText(0, node)

        if item.text(0) in self.copy_items:
            item.setBackground(0 , QtGui.QBrush(QtGui.QColor(51,153,204,70)))
        return item

    def _setCurrentItem(self, item):
        match_list = self.findItems(item, QtCore.Qt.MatchRecursive, 0)
        if match_list:
            self.setCurrentItem(match_list[0])
        else:
            self.setCurrentItem(None)