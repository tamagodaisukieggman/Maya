# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\work\maya_legacy\scripts\Project_Farm\env\exporter\main_window.ui'
#
# Created: Wed Jan 19 10:44:30 2022
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
        MainWindow.resize(480, 320)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.MainLayout.setSpacing(0)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.setObjectName("MainLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(378, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.ShouldTrim = QtWidgets.QCheckBox(self.widget)
        self.ShouldTrim.setChecked(True)
        self.ShouldTrim.setObjectName("ShouldTrim")
        self.horizontalLayout.addWidget(self.ShouldTrim)
        self.ExecuteButton = QtWidgets.QPushButton(self.widget)
        self.ExecuteButton.setObjectName("ExecuteButton")
        self.horizontalLayout.addWidget(self.ExecuteButton)
        self.MainLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "FarmEnvExporter", None, -1))
        self.ShouldTrim.setText(QtWidgets.QApplication.translate("MainWindow", "不要フェースを削除", None, -1))
        self.ExecuteButton.setText(QtWidgets.QApplication.translate("MainWindow", "Export", None, -1))

