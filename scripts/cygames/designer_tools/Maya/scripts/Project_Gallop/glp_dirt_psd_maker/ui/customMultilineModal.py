# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TkgDesignerTools_Legacy\Maya\scripts\Project_Gallop\glp_dirt_psd_maker\ui\customMultilineModal.ui'
#
# Created: Tue Jun  8 11:38:11 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLbl = QtWidgets.QLabel(Form)
        self.titleLbl.setObjectName("titleLbl")
        self.verticalLayout.addWidget(self.titleLbl)
        self.dataOutputArea = QtWidgets.QPlainTextEdit(Form)
        self.dataOutputArea.setProperty("cursor", QtCore.Qt.IBeamCursor)
        self.dataOutputArea.setAcceptDrops(False)
        self.dataOutputArea.setUndoRedoEnabled(False)
        self.dataOutputArea.setOverwriteMode(False)
        self.dataOutputArea.setTabStopWidth(84)
        self.dataOutputArea.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.dataOutputArea.setObjectName("dataOutputArea")
        self.verticalLayout.addWidget(self.dataOutputArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.countLbl = QtWidgets.QLabel(Form)
        self.countLbl.setObjectName("countLbl")
        self.horizontalLayout.addWidget(self.countLbl)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.okBtn = QtWidgets.QPushButton(Form)
        self.okBtn.setObjectName("okBtn")
        self.verticalLayout.addWidget(self.okBtn)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "対象データリスト", None, -1))
        self.titleLbl.setText(QtWidgets.QApplication.translate("Form", "以下が対象データになります", None, -1))
        self.dataOutputArea.setPlainText(QtWidgets.QApplication.translate("Form", "test message", None, -1))
        self.countLbl.setText(QtWidgets.QApplication.translate("Form", "TextLabel", None, -1))
        self.okBtn.setText(QtWidgets.QApplication.translate("Form", "OK", None, -1))

