# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\tech-designer\TkgDesignerTools_Legacy\Maya\scripts\Project_Gallop\glp_facial_recorder_importer\glp_facial_recorder_importer_ui.ui'
#
# Created: Fri Jan 22 17:39:58 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(439, 708)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.import_data_group = QtWidgets.QGroupBox(self.centralwidget)
        self.import_data_group.setObjectName("import_data_group")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.import_data_group)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.import_dir_label = QtWidgets.QLabel(self.import_data_group)
        self.import_dir_label.setObjectName("import_dir_label")
        self.horizontalLayout.addWidget(self.import_dir_label)
        self.import_dir_edit_text = QtWidgets.QLineEdit(self.import_data_group)
        self.import_dir_edit_text.setObjectName("import_dir_edit_text")
        self.horizontalLayout.addWidget(self.import_dir_edit_text)
        self.select_dir_button = QtWidgets.QPushButton(self.import_data_group)
        self.select_dir_button.setObjectName("select_dir_button")
        self.horizontalLayout.addWidget(self.select_dir_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.show_info_button = QtWidgets.QPushButton(self.import_data_group)
        self.show_info_button.setObjectName("show_info_button")
        self.verticalLayout.addWidget(self.show_info_button)
        self.verticalLayout_3.addWidget(self.import_data_group)
        self.option_setting_group = QtWidgets.QGroupBox(self.centralwidget)
        self.option_setting_group.setObjectName("option_setting_group")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.option_setting_group)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.start_option_label = QtWidgets.QLabel(self.option_setting_group)
        self.start_option_label.setObjectName("start_option_label")
        self.horizontalLayout_2.addWidget(self.start_option_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.start_option_edit = QtWidgets.QLineEdit(self.option_setting_group)
        self.start_option_edit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.start_option_edit.setObjectName("start_option_edit")
        self.horizontalLayout_2.addWidget(self.start_option_edit)
        self.get_crrent_frame_button = QtWidgets.QPushButton(self.option_setting_group)
        self.get_crrent_frame_button.setMinimumSize(QtCore.QSize(90, 0))
        self.get_crrent_frame_button.setBaseSize(QtCore.QSize(0, 0))
        self.get_crrent_frame_button.setObjectName("get_crrent_frame_button")
        self.horizontalLayout_2.addWidget(self.get_crrent_frame_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.target_option_label = QtWidgets.QLabel(self.option_setting_group)
        self.target_option_label.setObjectName("target_option_label")
        self.horizontalLayout_3.addWidget(self.target_option_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.target_option_edit = QtWidgets.QLineEdit(self.option_setting_group)
        self.target_option_edit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.target_option_edit.setObjectName("target_option_edit")
        self.horizontalLayout_3.addWidget(self.target_option_edit)
        self.get_current_target_button = QtWidgets.QPushButton(self.option_setting_group)
        self.get_current_target_button.setMinimumSize(QtCore.QSize(90, 0))
        self.get_current_target_button.setObjectName("get_current_target_button")
        self.horizontalLayout_3.addWidget(self.get_current_target_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addWidget(self.option_setting_group)
        self.bake_start_button = QtWidgets.QPushButton(self.centralwidget)
        self.bake_start_button.setMinimumSize(QtCore.QSize(0, 50))
        self.bake_start_button.setObjectName("bake_start_button")
        self.verticalLayout_3.addWidget(self.bake_start_button)
        self.log_edit = QtWidgets.QTextEdit(self.centralwidget)
        self.log_edit.setReadOnly(True)
        self.log_edit.setObjectName("log_edit")
        self.verticalLayout_3.addWidget(self.log_edit)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.import_data_group.setTitle(QtWidgets.QApplication.translate("MainWindow", "Unityで記録したデータ情報", None, -1))
        self.import_dir_label.setText(QtWidgets.QApplication.translate("MainWindow", "記録フォルダパス", None, -1))
        self.select_dir_button.setText(QtWidgets.QApplication.translate("MainWindow", "選択", None, -1))
        self.show_info_button.setText(QtWidgets.QApplication.translate("MainWindow", "記録情報の表示", None, -1))
        self.option_setting_group.setTitle(QtWidgets.QApplication.translate("MainWindow", "ベイクオプション", None, -1))
        self.start_option_label.setText(QtWidgets.QApplication.translate("MainWindow", "開始フレーム", None, -1))
        self.get_crrent_frame_button.setText(QtWidgets.QApplication.translate("MainWindow", "現在のフレーム", None, -1))
        self.target_option_label.setText(QtWidgets.QApplication.translate("MainWindow", "Ctrlルートノード", None, -1))
        self.get_current_target_button.setText(QtWidgets.QApplication.translate("MainWindow", "現在の選択", None, -1))
        self.bake_start_button.setText(QtWidgets.QApplication.translate("MainWindow", "ベイク開始", None, -1))

