#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# TreeView_AtomFileView.py
#

import sys
import os
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

class TreeView_AtomFileView(QtGui.QTreeView):
    def __init__(self, parent=None):
        super(TreeView_AtomFileView, self).__init__(parent)
        self.parent = parent
        self.setup()

    def setup(self):
        self.model = QtGui.QFileSystemModel()
        self.model.setFilter(QtCore.QDir.Files);
        self.model.setNameFilters(["*.atom",])
        self.model.setNameFilterDisables(False);
        self.setModel(self.model)

        self.defaultPath = ""
        self.model.setRootPath(self.defaultPath)
        self.setRootIndex(self.model.index(self.defaultPath))
        self.setItemsExpandable(False)
        self.setRootIsDecorated(False)

        self.hideColumn(1)
        self.hideColumn(2)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.setContextMenu)

        
    def doubleClickEvent(self):
        self.showPasteMenu()


    def getCurrentPath(self):
        index = self.currentIndex()
        path = self.model.filePath(index)
        return path


    def setCurrentPath(self, path):
        index = self.model.index(path)
        if os.path.isdir(path):
            self.setRootIndex(index)
        else:
            self.setRootIndex(self.model.index(os.path.dirname(path)))
        self.setCurrentIndex(index)


    def setRootPath(self, path):
        self.setRootIndex(self.model.index(path))


    def setContextMenu(self, pos):
        contextMenu = QtGui.QMenu(self)
        contextMenuLabels = [u"エクスプローラで開く"]
        actionList = []
        for label in contextMenuLabels:
             actionList.append(contextMenu.addAction(label))
        action = contextMenu.exec_(self.mapToGlobal(pos))
        for act in actionList:
            if act == action:
                if(act.text() == u"エクスプローラで開く"):
                    pass

