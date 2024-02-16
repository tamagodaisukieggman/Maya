# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\tech-designer\maya_legacy\scripts\Project_Gallop\glp_tp_simulator\ui\main_window.ui'
#
# Created: Thu Jan 11 10:22:04 2024
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(357, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_item_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_item_button.setObjectName("add_item_button")
        self.horizontalLayout.addWidget(self.add_item_button)
        self.update_item_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.update_item_button.sizePolicy().hasHeightForWidth())
        self.update_item_button.setSizePolicy(sizePolicy)
        self.update_item_button.setObjectName("update_item_button")
        self.horizontalLayout.addWidget(self.update_item_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.items_widget_area = QtWidgets.QScrollArea(self.centralwidget)
        self.items_widget_area.setWidgetResizable(True)
        self.items_widget_area.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.items_widget_area.setObjectName("items_widget_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 337, 518))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.items_widget_area.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.items_widget_area)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.all_enable_button = QtWidgets.QPushButton(self.centralwidget)
        self.all_enable_button.setObjectName("all_enable_button")
        self.horizontalLayout_2.addWidget(self.all_enable_button)
        self.all_disable_button = QtWidgets.QPushButton(self.centralwidget)
        self.all_disable_button.setObjectName("all_disable_button")
        self.horizontalLayout_2.addWidget(self.all_disable_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.add_item_button.setText(QtWidgets.QApplication.translate("MainWindow", "プロセスを追加", None, -1))
        self.update_item_button.setText(QtWidgets.QApplication.translate("MainWindow", "更新", None, -1))
        self.all_enable_button.setText(QtWidgets.QApplication.translate("MainWindow", "全て有効", None, -1))
        self.all_disable_button.setText(QtWidgets.QApplication.translate("MainWindow", "全て無効", None, -1))

