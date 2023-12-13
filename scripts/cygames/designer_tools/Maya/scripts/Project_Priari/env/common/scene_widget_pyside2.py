# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\work\maya_legacy\scripts\Project_Priari\env\common\scene_widget.ui'
#
# Created: Wed Jan 19 10:35:08 2022
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.vboxlayout = QtWidgets.QVBoxLayout(Form)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setContentsMargins(8, 0, 8, 0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.MainLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.MainLayout_2.setSpacing(4)
        self.MainLayout_2.setContentsMargins(8, 8, 8, 8)
        self.MainLayout_2.setObjectName("MainLayout_2")
        self.NameLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.NameLabel.setFont(font)
        self.NameLabel.setText("")
        self.NameLabel.setObjectName("NameLabel")
        self.MainLayout_2.addWidget(self.NameLabel)
        self.PathWidget = QtWidgets.QWidget(self.widget)
        self.PathWidget.setObjectName("PathWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.PathWidget)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.PathLabel = QtWidgets.QLabel(self.PathWidget)
        self.PathLabel.setText("")
        self.PathLabel.setObjectName("PathLabel")
        self.horizontalLayout.addWidget(self.PathLabel)
        self.MainLayout_2.addWidget(self.PathWidget)
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 368, 252))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.MainLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.MainLayout.setSpacing(8)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.setObjectName("MainLayout")
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.MainLayout.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.MainLayout_2.addWidget(self.scrollArea)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))

