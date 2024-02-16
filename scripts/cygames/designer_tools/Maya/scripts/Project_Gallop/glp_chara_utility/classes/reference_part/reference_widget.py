# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\tech-designer\maya_legacy\scripts\Project_Gallop\glp_chara_utility\classes\reference_part\reference_widget.ui'
#
# Created: Wed Jan 17 10:29:41 2024
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 30)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.typeLabel = QtWidgets.QLabel(self.widget)
        self.typeLabel.setMinimumSize(QtCore.QSize(30, 0))
        self.typeLabel.setMaximumSize(QtCore.QSize(30, 16777215))
        self.typeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.typeLabel.setObjectName("typeLabel")
        self.horizontalLayout_2.addWidget(self.typeLabel)
        self.idLabel = QtWidgets.QLabel(self.widget)
        self.idLabel.setMinimumSize(QtCore.QSize(50, 0))
        self.idLabel.setMaximumSize(QtCore.QSize(50, 16777215))
        self.idLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.idLabel.setObjectName("idLabel")
        self.horizontalLayout_2.addWidget(self.idLabel)
        spacerItem = QtWidgets.QSpacerItem(261, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.selectJointButton = QtWidgets.QPushButton(self.widget)
        self.selectJointButton.setMinimumSize(QtCore.QSize(80, 20))
        self.selectJointButton.setMaximumSize(QtCore.QSize(80, 20))
        self.selectJointButton.setObjectName("selectJointButton")
        self.horizontalLayout_2.addWidget(self.selectJointButton)
        self.resetYButton = QtWidgets.QPushButton(self.widget)
        self.resetYButton.setMinimumSize(QtCore.QSize(70, 20))
        self.resetYButton.setMaximumSize(QtCore.QSize(70, 20))
        self.resetYButton.setObjectName("resetYButton")
        self.horizontalLayout_2.addWidget(self.resetYButton)
        self.removeReferenceButton = QtWidgets.QPushButton(self.widget)
        self.removeReferenceButton.setMinimumSize(QtCore.QSize(50, 20))
        self.removeReferenceButton.setMaximumSize(QtCore.QSize(50, 20))
        self.removeReferenceButton.setObjectName("removeReferenceButton")
        self.horizontalLayout_2.addWidget(self.removeReferenceButton)
        self.verticalLayout.addWidget(self.widget)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.typeLabel.setText(QtWidgets.QApplication.translate("Form", "デカ", None, -1))
        self.idLabel.setText(QtWidgets.QApplication.translate("Form", "1001_00", None, -1))
        self.selectJointButton.setText(QtWidgets.QApplication.translate("Form", "ジョイント選択", None, -1))
        self.resetYButton.setText(QtWidgets.QApplication.translate("Form", "Y位置リセット", None, -1))
        self.removeReferenceButton.setText(QtWidgets.QApplication.translate("Form", "非表示", None, -1))

