# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\tech-designer\maya_legacy\scripts\Project_Gallop\glp_chara_utility\classes\reference_part\manager_window.ui'
#
# Created: Wed Jan 17 10:29:44 2024
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_GallopCharaUtilityReferenceManagerWindow(object):
    def setupUi(self, GallopCharaUtilityReferenceManagerWindow):
        GallopCharaUtilityReferenceManagerWindow.setObjectName("GallopCharaUtilityReferenceManagerWindow")
        GallopCharaUtilityReferenceManagerWindow.resize(400, 100)
        self.centralwidget = QtWidgets.QWidget(GallopCharaUtilityReferenceManagerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(80, 0))
        self.label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.resetYButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetYButton.setMinimumSize(QtCore.QSize(70, 20))
        self.resetYButton.setMaximumSize(QtCore.QSize(70, 20))
        self.resetYButton.setObjectName("resetYButton")
        self.horizontalLayout.addWidget(self.resetYButton)
        self.refreshReferenceListButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshReferenceListButton.setMinimumSize(QtCore.QSize(50, 20))
        self.refreshReferenceListButton.setMaximumSize(QtCore.QSize(50, 20))
        self.refreshReferenceListButton.setObjectName("refreshReferenceListButton")
        self.horizontalLayout.addWidget(self.refreshReferenceListButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.referenceListWidget = QtWidgets.QWidget(self.centralwidget)
        self.referenceListWidget.setObjectName("referenceListWidget")
        self.referenceListLayout = QtWidgets.QVBoxLayout(self.referenceListWidget)
        self.referenceListLayout.setSpacing(4)
        self.referenceListLayout.setContentsMargins(0, 0, 0, 0)
        self.referenceListLayout.setObjectName("referenceListLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.referenceListLayout.addItem(spacerItem1)
        self.verticalLayout_2.addWidget(self.referenceListWidget)
        GallopCharaUtilityReferenceManagerWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(GallopCharaUtilityReferenceManagerWindow)
        QtCore.QMetaObject.connectSlotsByName(GallopCharaUtilityReferenceManagerWindow)

    def retranslateUi(self, GallopCharaUtilityReferenceManagerWindow):
        GallopCharaUtilityReferenceManagerWindow.setWindowTitle(QtWidgets.QApplication.translate("GallopCharaUtilityReferenceManagerWindow", "Gallop Chara Utility Reference Manager", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("GallopCharaUtilityReferenceManagerWindow", "リファレンスリスト", None, -1))
        self.resetYButton.setText(QtWidgets.QApplication.translate("GallopCharaUtilityReferenceManagerWindow", "Y位置リセット", None, -1))
        self.refreshReferenceListButton.setText(QtWidgets.QApplication.translate("GallopCharaUtilityReferenceManagerWindow", "更新", None, -1))

