# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\tech-designer\maya_legacy\scripts\Project_Temp\material_chenger\material_changer_gui.ui'
#
# Created: Wed Mar 30 11:36:59 2022
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
try:
    from builtins import object
except Exception:
    pass


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(401, 444)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.grp_root_setting = QtWidgets.QGroupBox(self.centralwidget)
        self.grp_root_setting.setObjectName("grp_root_setting")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.grp_root_setting)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_update_root = QtWidgets.QPushButton(self.grp_root_setting)
        self.btn_update_root.setObjectName("btn_update_root")
        self.horizontalLayout_2.addWidget(self.btn_update_root)
        self.txt_root = QtWidgets.QLineEdit(self.grp_root_setting)
        self.txt_root.setObjectName("txt_root")
        self.horizontalLayout_2.addWidget(self.txt_root)
        self.verticalLayout.addWidget(self.grp_root_setting)
        self.grp_change_material = QtWidgets.QGroupBox(self.centralwidget)
        self.grp_change_material.setObjectName("grp_change_material")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.grp_change_material)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_material_default = QtWidgets.QPushButton(self.grp_change_material)
        self.btn_material_default.setObjectName("btn_material_default")
        self.horizontalLayout.addWidget(self.btn_material_default)
        self.btn_material_work = QtWidgets.QPushButton(self.grp_change_material)
        self.btn_material_work.setObjectName("btn_material_work")
        self.horizontalLayout.addWidget(self.btn_material_work)
        self.btn_material_unity = QtWidgets.QPushButton(self.grp_change_material)
        self.btn_material_unity.setObjectName("btn_material_unity")
        self.horizontalLayout.addWidget(self.btn_material_unity)
        self.verticalLayout.addWidget(self.grp_change_material)
        self.grp_change_outline = QtWidgets.QGroupBox(self.centralwidget)
        self.grp_change_outline.setObjectName("grp_change_outline")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.grp_change_outline)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_outline_default = QtWidgets.QPushButton(self.grp_change_outline)
        self.btn_outline_default.setObjectName("btn_outline_default")
        self.horizontalLayout_3.addWidget(self.btn_outline_default)
        self.btn_outline_unity = QtWidgets.QPushButton(self.grp_change_outline)
        self.btn_outline_unity.setObjectName("btn_outline_unity")
        self.horizontalLayout_3.addWidget(self.btn_outline_unity)
        self.verticalLayout.addWidget(self.grp_change_outline)
        self.txt_info = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_info.setObjectName("txt_info")
        self.verticalLayout.addWidget(self.txt_info)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.grp_root_setting.setTitle(QtWidgets.QApplication.translate("MainWindow", "オブジェクトルート", None, -1))
        self.btn_update_root.setText(QtWidgets.QApplication.translate("MainWindow", "更新", None, -1))
        self.grp_change_material.setTitle(QtWidgets.QApplication.translate("MainWindow", "メッシュのマテリアル変更", None, -1))
        self.btn_material_default.setText(QtWidgets.QApplication.translate("MainWindow", "TGA（デフォルト）", None, -1))
        self.btn_material_work.setText(QtWidgets.QApplication.translate("MainWindow", "PSD", None, -1))
        self.btn_material_unity.setText(QtWidgets.QApplication.translate("MainWindow", "Unityシェーダー", None, -1))
        self.grp_change_outline.setTitle(QtWidgets.QApplication.translate("MainWindow", "アウトラインのマテリアル変更", None, -1))
        self.btn_outline_default.setText(QtWidgets.QApplication.translate("MainWindow", "OFF（デフォルト）", None, -1))
        self.btn_outline_unity.setText(QtWidgets.QApplication.translate("MainWindow", "ON（Unityシェーダー）", None, -1))

