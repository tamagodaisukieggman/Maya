# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\tech-designer\maya_legacy\scripts\Project_Gallop\glp_icon_model_maker\ui\main_window.ui'
#
# Created: Wed Oct  5 15:44:44 2022
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(264, 247)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.add_face_button = QtWidgets.QPushButton(self.groupBox)
        self.add_face_button.setObjectName("add_face_button")
        self.verticalLayout_2.addWidget(self.add_face_button)
        self.rem_face_button = QtWidgets.QPushButton(self.groupBox)
        self.rem_face_button.setObjectName("rem_face_button")
        self.verticalLayout_2.addWidget(self.rem_face_button)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.view_body_button = QtWidgets.QPushButton(self.groupBox_2)
        self.view_body_button.setObjectName("view_body_button")
        self.verticalLayout_3.addWidget(self.view_body_button)
        self.view_mask_button = QtWidgets.QPushButton(self.groupBox_2)
        self.view_mask_button.setObjectName("view_mask_button")
        self.verticalLayout_3.addWidget(self.view_mask_button)
        self.isolate_off_button = QtWidgets.QPushButton(self.groupBox_2)
        self.isolate_off_button.setObjectName("isolate_off_button")
        self.verticalLayout_3.addWidget(self.isolate_off_button)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "アイコン用マスクの指定", None, -1))
        self.add_face_button.setText(QtWidgets.QApplication.translate("MainWindow", "選択面を指定", None, -1))
        self.rem_face_button.setText(QtWidgets.QApplication.translate("MainWindow", "選択面を除外", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MainWindow", "アイコン用マスクの確認", None, -1))
        self.view_body_button.setText(QtWidgets.QApplication.translate("MainWindow", "衣装部分を分離表示", None, -1))
        self.view_mask_button.setText(QtWidgets.QApplication.translate("MainWindow", "マスク部分を分離表示", None, -1))
        self.isolate_off_button.setText(QtWidgets.QApplication.translate("MainWindow", "分離表示OFF", None, -1))

