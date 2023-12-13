# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\work\maya_legacy\scripts\Project_Farm\env\exporter\utility\main_window.ui'
#
# Created: Wed Jan 19 10:43:34 2022
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

try:
    # Maya 2022-
    from builtins import object
except:
    pass

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 458)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.MainLayout.setSpacing(0)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.setObjectName("MainLayout")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(8, 0, 8, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget_3)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.widget_3)
        self.CameraList = QtWidgets.QListWidget(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CameraList.sizePolicy().hasHeightForWidth())
        self.CameraList.setSizePolicy(sizePolicy)
        self.CameraList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.CameraList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.CameraList.setObjectName("CameraList")
        self.verticalLayout.addWidget(self.CameraList)
        self.MainLayout.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(378, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.ExecuteButton = QtWidgets.QPushButton(self.widget)
        self.ExecuteButton.setMinimumSize(QtCore.QSize(80, 0))
        self.ExecuteButton.setObjectName("ExecuteButton")
        self.horizontalLayout.addWidget(self.ExecuteButton)
        self.MainLayout.addWidget(self.widget)
        self.widget_4 = QtWidgets.QWidget(self.centralwidget)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setSpacing(8)
        self.horizontalLayout_2.setContentsMargins(16, 8, 8, 8)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget_4)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.DefaultViewportButton = QtWidgets.QPushButton(self.widget_4)
        self.DefaultViewportButton.setObjectName("DefaultViewportButton")
        self.horizontalLayout_2.addWidget(self.DefaultViewportButton)
        self.HideViewportButton = QtWidgets.QPushButton(self.widget_4)
        self.HideViewportButton.setObjectName("HideViewportButton")
        self.horizontalLayout_2.addWidget(self.HideViewportButton)
        self.MainLayout.addWidget(self.widget_4)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "FarmEnvExporterUtility", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "背面削除設定", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "選択したカメラから見てすべてのフレームで背面になっているフェースを出力時の削除対象として設定します", None, -1))
        self.ExecuteButton.setText(QtWidgets.QApplication.translate("MainWindow", "実行", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "ビューポート設定", None, -1))
        self.DefaultViewportButton.setText(QtWidgets.QApplication.translate("MainWindow", "通常", None, -1))
        self.HideViewportButton.setText(QtWidgets.QApplication.translate("MainWindow", "背面削除", None, -1))

