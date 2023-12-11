# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/CF0438/Desktop/Ui_PasteAtomFile.ui'
#
# Created: Thu Mar 03 15:49:14 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

import AtomFileView
reload(AtomFileView)
from AtomFileView import AtomFileView

import DestinationView
reload(DestinationView)
from DestinationView import DestinationView

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1196, 709)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_clearCheckBox = QtGui.QPushButton(Dialog)
        self.pushButton_clearCheckBox.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_clearCheckBox.setObjectName("pushButton_clearCheckBox")
        self.horizontalLayout_2.addWidget(self.pushButton_clearCheckBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_pasteAnimation = QtGui.QPushButton(Dialog)
        self.pushButton_pasteAnimation.setObjectName("pushButton_pasteAnimation")
        self.horizontalLayout_2.addWidget(self.pushButton_pasteAnimation)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.splitter = QtGui.QSplitter(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        #self.treeWidget_atomFileView = QtGui.QTreeWidget(self.splitter)
        self.treeWidget_atomFileView = AtomFileView(Dialog)
        self.splitter.addWidget(self.treeWidget_atomFileView)
        self.treeWidget_atomFileView.setObjectName("treeWidget_atomFileView")
        #self.treeWidget_destinationView = QtGui.QTreeWidget(self.splitter)
        self.treeWidget_destinationView = DestinationView(Dialog)
        self.splitter.addWidget(self.treeWidget_destinationView)
        self.treeWidget_destinationView.setObjectName("treeWidget_destinationView")
        
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_checkAllCheckBox = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_checkAllCheckBox.sizePolicy().hasHeightForWidth())
        self.pushButton_checkAllCheckBox.setSizePolicy(sizePolicy)
        self.pushButton_checkAllCheckBox.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_checkAllCheckBox.setObjectName("pushButton_checkAllCheckBox")
        self.horizontalLayout.addWidget(self.pushButton_checkAllCheckBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_timeRange = QtGui.QLabel(Dialog)
        self.label_timeRange.setObjectName("label_timeRange")
        self.horizontalLayout.addWidget(self.label_timeRange)
        self.radioButton_fromCurrentTime = QtGui.QRadioButton(Dialog)
        self.radioButton_fromCurrentTime.setObjectName("radioButton_fromCurrentTime")
        self.horizontalLayout.addWidget(self.radioButton_fromCurrentTime)
        self.radioButton_timeSlider = QtGui.QRadioButton(Dialog)
        self.radioButton_timeSlider.setObjectName("radioButton_timeSlider")
        self.horizontalLayout.addWidget(self.radioButton_timeSlider)
        self.radioButton_fromFile = QtGui.QRadioButton(Dialog)
        self.radioButton_fromFile.setObjectName("radioButton_fromFile")
        self.horizontalLayout.addWidget(self.radioButton_fromFile)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "アニメーションのペースト", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_clearCheckBox.setText(QtGui.QApplication.translate("Dialog", "すべてのチェックをOFF", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_pasteAnimation.setText(QtGui.QApplication.translate("Dialog", "アニメーション ペースト", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_atomFileView.headerItem().setText(0, QtGui.QApplication.translate("Dialog", "コピー元(Atomファイル)", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_atomFileView.headerItem().setText(1, QtGui.QApplication.translate("Dialog", "出力アニメーション ⇒", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_destinationView.headerItem().setText(0, QtGui.QApplication.translate("Dialog", "コピー先", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_checkAllCheckBox.setText(QtGui.QApplication.translate("Dialog", "すべてのチェックをON", None, QtGui.QApplication.UnicodeUTF8))
        self.label_timeRange.setText(QtGui.QApplication.translate("Dialog", "タイム レンジ：", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_fromCurrentTime.setText(QtGui.QApplication.translate("Dialog", "カレントタイムから", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_timeSlider.setText(QtGui.QApplication.translate("Dialog", "タイム スライダ", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_fromFile.setText(QtGui.QApplication.translate("Dialog", "ファイルから", None, QtGui.QApplication.UnicodeUTF8))

