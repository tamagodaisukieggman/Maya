# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\work\maya_legacy\scripts\Project_Farm\env\common\model_widget.ui'
#
# Created: Mon Nov  8 19:26:08 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

try:
    # Maya 2022-
    from builtins import object
except:
    pass

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        Form.setStyleSheet("background-color: rgb(55, 55, 55);")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(8, 4, 8, 4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Enabled = QtWidgets.QCheckBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Enabled.sizePolicy().hasHeightForWidth())
        self.Enabled.setSizePolicy(sizePolicy)
        self.Enabled.setStyleSheet("background-color: rgb(41, 41, 41);")
        self.Enabled.setText("")
        self.Enabled.setChecked(True)
        self.Enabled.setObjectName("Enabled")
        self.verticalLayout_2.addWidget(self.Enabled)
        self.horizontalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(Form)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setContentsMargins(8, 0, 8, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.NameLabel = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.NameLabel.setFont(font)
        self.NameLabel.setText("")
        self.NameLabel.setObjectName("NameLabel")
        self.verticalLayout.addWidget(self.NameLabel)
        self.InfoLabel = QtWidgets.QLabel(self.widget_2)
        self.InfoLabel.setText("")
        self.InfoLabel.setObjectName("InfoLabel")
        self.verticalLayout.addWidget(self.InfoLabel)
        self.PathLabel = QtWidgets.QLabel(self.widget_2)
        self.PathLabel.setText("")
        self.PathLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.PathLabel.setObjectName("PathLabel")
        self.verticalLayout.addWidget(self.PathLabel)
        self.horizontalLayout.addWidget(self.widget_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))

