#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# AtomFileView.py
#

import os
import sys
import re

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI

class AtomFileView(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        super(AtomFileView, self).__init__(parent)
        self.parent = parent
        self.setup()

    def setup(self):
        self.clicked[QtCore.QModelIndex].connect(self.clickEvent)
        root = cmds.ls(sl=True)
        self.des_list = cmds.listRelatives(root, allDescendents=True, type='transform', path=True)
        self.des_list.append(root[0])

        self.setExpandsOnDoubleClick(False)
        self.setAlternatingRowColors(True)
        self.setStyle(QtGui.QStyleFactory.create("CDE"))

        self.atom_file_path = ""

        self.headerItem().setText(0, u'コピー元(Atom ファイル)')
        self.headerItem().setText(1, u'出力アニメーション ⇒')

        self.setSelectedAtomFile()

        self.parent.copyList = self.copy_items


    def clickEvent(self):
        if self.currentItem():
            item = self.currentItem().text(0)
            self.parent.changeCurrentItem(item)


    def setSelectedAtomFile(self):
        f = open(self.parent.atomFile)
        lines = f.readlines()
        f.close()

        self.nodes, self.nodeFlags = self.extractNodesNameFromAtom(lines)
        self.buildNodeTreeView(self.nodes, self.nodeFlags)


    def readAtomFile(self):
        self.atom_file_path = cmds.fileDialog2(fm=4, dir= ".", ff=u"Atom ファイル (*.atom)")
        if self.atom_file_path:
            f = open(self.atom_file_path[0])
            lines = f.readlines()
            f.close()

            self.nodes, self.nodeFlags = self.extractNodesNameFromAtom(lines)
            self.buildNodeTreeView(self.nodes, nodeFlags)

    def extractNodesNameFromAtom(self, lines):
        nodes = []
        nodeFlags = []

        for i, line in enumerate(lines):
            if line.find('dagNode {') >= 0:
                nodes.append(lines[i+1].replace(";","").split())
                if lines[i+2].find('anim ') < 0:
                    nodeFlags.append(1)
                else:
                    nodeFlags.append(2)
        
            if line.find('shape {') >= 0:
                nodes.append(lines[i+1].replace(";","").split())
                nodeFlags.append(0)

        return [nodes, nodeFlags]

    def buildNodeTreeView(self, nodes, nodeFlags):
        self.copy_items = []
        self.index = 0
        self.clear()
        self.createNodeTreeView(nodes, nodeFlags, True)
        self.expandAll()

    def createNodeTreeView(self, nodes, nodeFlags, check, parent=None):
        if self.index < len(nodes):
            if parent:
                parent = self.addItem(nodes[self.index], nodeFlags[self.index], check, parent)
            else:
                parent = self.addItem(nodes[self.index], nodeFlags[self.index], check)

            num_child = int(nodes[self.index][2])
            for i in range(num_child):
                self.index += 1
                if(num_child>0):
                    self.createNodeTreeView(nodes, nodeFlags, check, parent)

    def addItem(self, node, nodeFlag, check, parent = None):
        if parent:
            if nodeFlag == 1:
                item = QtGui.QTreeWidgetItem(parent)
                item.setText(0, node[0])
                parent.addChild(item)
                return item

            if nodeFlag == 2: # anim
                item = QtGui.QTreeWidgetItem(parent)
                item.setText(0, node[0])
                self.copy_items.append(item.text(0))

                if node[0] in self.des_list:
                    if check:
                        item.setData(1, QtCore.Qt.CheckStateRole, QtCore.Qt.Checked)
                    else:
                        item.setData(1, QtCore.Qt.CheckStateRole, QtCore.Qt.Unchecked)
                    item.setText(1, node[0])
                    item.setBackground(0 , QtGui.QBrush(QtGui.QColor(51,153,204,70)))
                    item.setBackground(1 , QtGui.QBrush(QtGui.QColor(51,153,204,70)))
                    self.copy_items.append(item.text(0))
                else:
                    item.setData(1, QtCore.Qt.CheckStateRole, QtCore.Qt.Unchecked)
                    item.setBackground(0 , QtGui.QBrush(QtGui.QColor(204,0,51,70)))

                parent.addChild(item)
                return item
        else:
            if nodeFlag == 1:
                item = QtGui.QTreeWidgetItem(self)
                item.setText(0, node[0])
                self.addTopLevelItem(item)
                return item

            if nodeFlag == 2: # anim
                item = QtGui.QTreeWidgetItem(self)
                item.setText(0, node[0])

                if node[0] in self.des_list:
                    if check:
                        item.setData(1, QtCore.Qt.CheckStateRole, QtCore.Qt.Checked)
                    else:
                        item.setData(1, QtCore.Qt.CheckStateRole, QtCore.Qt.Unchecked)
                    item.setText(1, node[0])
                    item.setBackground(0 , QtGui.QBrush(QtGui.QColor(51,153,204,70)))
                    item.setBackground(1 , QtGui.QBrush(QtGui.QColor(51,153,204,70)))
                    self.copy_items.append(item.text(0))
                else:
                    item.setData(1, QtCore.Qt.CheckStateRole, QtCore.Qt.Unchecked)
                    item.setBackground(0 , QtGui.QBrush(QtGui.QColor(204,0,51,70)))
                self.addTopLevelItem(item)
                return item

    def getCopyList(self):
        self.getCopyListToplevelItem()

    def getCopyListToplevelItem(self):
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if item.data(1, QtCore.Qt.CheckStateRole) == QtCore.Qt.Unchecked:
                self.not_copy_list.append(item.text(0))
            self.getCopyListChildItem(item)

    def getCopyListChildItem(self, parent):
        for i in range(parent.childCount()):
            item = parent.child(i)
            if item.data(1, QtCore.Qt.CheckStateRole) == QtCore.Qt.Unchecked:
                self.not_copy_list.append(item.text(0))
            self.getCopyListChildItem(item)

    def writeMapFile(self):
        self.not_copy_list = []
        self.getCopyList()

        return self.prefixFileText(self.parent.atomFile, self.not_copy_list, "__", " ", False)

    def _setCurrentItem(self, item):
        match_list = self.findItems(item, QtCore.Qt.MatchRecursive, 0)
        if match_list:
            self.setCurrentItem(match_list[0])
        else:
            self.setCurrentItem(None)

    def prefixFileText(self, file_path, search_list, prefix, delimiter="", replace_flag=True):
        temp_file_path = os.path.dirname(file_path) + "/temp"
    
        try:
            file = open(file_path, "r")
            temp_file = open(temp_file_path, "w")
            for line in file:
                for search in search_list:
                    if line.find(search + delimiter) != -1:
                        line = re.sub(search, prefix + search, line)
                temp_file.write(line)
        finally:
            file.close()
            temp_file.close()

        if replace_flag:
            if os.path.exists(file_path) and os.path.exists(temp_file_path):
                os.remove(file_path)
                os.rename(temp_file_path, file_path)
        else:
            return temp_file_path

    def clearCheckBox(self):
        self.copy_items = []
        self.index = 0
        self.clear()
        self.createNodeTreeView(self.nodes, self.nodeFlags, False)
        self.expandAll()


    def checkAllCheckBox(self):
        self.copy_items = []
        self.index = 0
        self.clear()
        self.createNodeTreeView(self.nodes, self.nodeFlags, True)
        self.expandAll()