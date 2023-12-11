# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/CF0438/Desktop/Ui_CyAnimationCopy.ui'
#
# Created: Tue Mar 01 17:07:12 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

import TreeView_AtomFileView
reload(TreeView_AtomFileView)
from TreeView_AtomFileView import TreeView_AtomFileView

import TextEdit_AtomFileInfo
reload(TextEdit_AtomFileInfo)
from TextEdit_AtomFileInfo import TextEdit_AtomFileInfo

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(524, 626)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_atomFilePath = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_atomFilePath.setObjectName("lineEdit_atomFilePath")
        self.verticalLayout.addWidget(self.lineEdit_atomFilePath)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        #self.treeView_atomFile = QtGui.QTreeView(self.splitter)
        self.treeView_atomFile = TreeView_AtomFileView(self.splitter)
        self.treeView_atomFile.setObjectName("treeView_atomFile")
        self.treeView_atomFile.header().setVisible(True)
        self.treeView_atomFile.header().setHighlightSections(False)
        #self.textEdit_atomFileInfo = QtGui.QTextEdit(self.splitter)
        self.textEdit_atomFileInfo = TextEdit_AtomFileInfo(self.splitter)
        self.textEdit_atomFileInfo.setObjectName("textEdit_atomFileInfo")
        self.verticalLayout.addWidget(self.splitter)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolButton_copy = QtGui.QToolButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_copy.sizePolicy().hasHeightForWidth())
        self.toolButton_copy.setSizePolicy(sizePolicy)
        self.toolButton_copy.setMinimumSize(QtCore.QSize(120, 60))
        self.toolButton_copy.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_copy.setAutoRaise(False)
        self.toolButton_copy.setArrowType(QtCore.Qt.NoArrow)
        self.toolButton_copy.setObjectName("toolButton_copy")
        self.horizontalLayout.addWidget(self.toolButton_copy)
        self.toolButton_paste = QtGui.QToolButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_paste.sizePolicy().hasHeightForWidth())
        self.toolButton_paste.setSizePolicy(sizePolicy)
        self.toolButton_paste.setMinimumSize(QtCore.QSize(120, 60))
        self.toolButton_paste.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolButton_paste.setPopupMode(QtGui.QToolButton.DelayedPopup)
        self.toolButton_paste.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_paste.setObjectName("toolButton_paste")
        self.horizontalLayout.addWidget(self.toolButton_paste)
        self.toolButton_rename = QtGui.QToolButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_rename.sizePolicy().hasHeightForWidth())
        self.toolButton_rename.setSizePolicy(sizePolicy)
        self.toolButton_rename.setMinimumSize(QtCore.QSize(120, 60))
        self.toolButton_rename.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_rename.setAutoRaise(False)
        self.toolButton_rename.setArrowType(QtCore.Qt.NoArrow)
        self.toolButton_rename.setObjectName("toolButton_rename")
        self.horizontalLayout.addWidget(self.toolButton_rename)
        self.toolButton_remove = QtGui.QToolButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_remove.sizePolicy().hasHeightForWidth())
        self.toolButton_remove.setSizePolicy(sizePolicy)
        self.toolButton_remove.setMinimumSize(QtCore.QSize(120, 60))
        self.toolButton_remove.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_remove.setAutoRaise(False)
        self.toolButton_remove.setArrowType(QtCore.Qt.NoArrow)
        self.toolButton_remove.setObjectName("toolButton_remove")
        self.horizontalLayout.addWidget(self.toolButton_remove)
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "CyAnimationCopy", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_copy.setText(QtGui.QApplication.translate("MainWindow", "コピー", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_paste.setText(QtGui.QApplication.translate("MainWindow", "ペースト", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_rename.setText(QtGui.QApplication.translate("MainWindow", "名前変更", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_remove.setText(QtGui.QApplication.translate("MainWindow", "削除", None, QtGui.QApplication.UnicodeUTF8))

