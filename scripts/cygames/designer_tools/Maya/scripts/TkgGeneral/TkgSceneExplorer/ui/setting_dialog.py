# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\tech-designer\maya_legacy\scripts\TkgGeneral\TkgSceneExplorer\ui\setting_dialog.ui'
#
# Created: Tue Nov 21 18:17:02 2023
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(415, 576)
        Dialog.setModal(True)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_9.setObjectName("groupBox_9")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_9)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_9)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.walk_file_limit_spin = QtWidgets.QSpinBox(self.groupBox_9)
        self.walk_file_limit_spin.setMinimum(0)
        self.walk_file_limit_spin.setMaximum(10000000)
        self.walk_file_limit_spin.setProperty("value", 100000)
        self.walk_file_limit_spin.setObjectName("walk_file_limit_spin")
        self.horizontalLayout.addWidget(self.walk_file_limit_spin)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_9)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox_5)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.tree_double_click_expand_radio = QtWidgets.QRadioButton(self.groupBox_5)
        self.tree_double_click_expand_radio.setChecked(True)
        self.tree_double_click_expand_radio.setObjectName("tree_double_click_expand_radio")
        self.horizontalLayout_3.addWidget(self.tree_double_click_expand_radio)
        self.tree_double_click_set_root_radio = QtWidgets.QRadioButton(self.groupBox_5)
        self.tree_double_click_set_root_radio.setObjectName("tree_double_click_set_root_radio")
        self.horizontalLayout_3.addWidget(self.tree_double_click_set_root_radio)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.verticalLayout_10.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_9)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox_6)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.sep_slash_radio = QtWidgets.QRadioButton(self.groupBox_6)
        self.sep_slash_radio.setChecked(True)
        self.sep_slash_radio.setObjectName("sep_slash_radio")
        self.horizontalLayout_4.addWidget(self.sep_slash_radio)
        self.sep_back_slash_radio = QtWidgets.QRadioButton(self.groupBox_6)
        self.sep_back_slash_radio.setObjectName("sep_back_slash_radio")
        self.horizontalLayout_4.addWidget(self.sep_back_slash_radio)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        self.verticalLayout_10.addWidget(self.groupBox_6)
        self.groupBox_10 = QtWidgets.QGroupBox(self.groupBox_9)
        self.groupBox_10.setObjectName("groupBox_10")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox_10)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.col_obj_del_confirm_check = QtWidgets.QCheckBox(self.groupBox_10)
        self.col_obj_del_confirm_check.setChecked(True)
        self.col_obj_del_confirm_check.setObjectName("col_obj_del_confirm_check")
        self.verticalLayout_11.addWidget(self.col_obj_del_confirm_check)
        self.verticalLayout_10.addWidget(self.groupBox_10)
        self.verticalLayout.addWidget(self.groupBox_9)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_8 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_8)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.exec_set_project_check = QtWidgets.QCheckBox(self.groupBox_2)
        self.exec_set_project_check.setChecked(True)
        self.exec_set_project_check.setObjectName("exec_set_project_check")
        self.verticalLayout_2.addWidget(self.exec_set_project_check)
        self.verticalLayout_9.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_8)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.no_use_namespace_radio = QtWidgets.QRadioButton(self.groupBox_3)
        self.no_use_namespace_radio.setObjectName("no_use_namespace_radio")
        self.verticalLayout_3.addWidget(self.no_use_namespace_radio)
        self.use_file_namespace_radio = QtWidgets.QRadioButton(self.groupBox_3)
        self.use_file_namespace_radio.setChecked(True)
        self.use_file_namespace_radio.setObjectName("use_file_namespace_radio")
        self.verticalLayout_3.addWidget(self.use_file_namespace_radio)
        self.verticalLayout_9.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_8)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.exec_fix_texture_path_check = QtWidgets.QCheckBox(self.groupBox_4)
        self.exec_fix_texture_path_check.setChecked(True)
        self.exec_fix_texture_path_check.setObjectName("exec_fix_texture_path_check")
        self.verticalLayout_5.addWidget(self.exec_fix_texture_path_check)
        self.exec_script_node_on_open_check = QtWidgets.QCheckBox(self.groupBox_4)
        self.exec_script_node_on_open_check.setObjectName("exec_script_node_on_open_check")
        self.verticalLayout_5.addWidget(self.exec_script_node_on_open_check)
        self.verticalLayout_9.addWidget(self.groupBox_4)
        self.verticalLayout_4.addWidget(self.groupBox_8)
        self.groupBox_7 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_4 = QtWidgets.QLabel(self.groupBox_7)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_8.addWidget(self.label_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.project_setting_file_path_edit = QtWidgets.QLineEdit(self.groupBox_7)
        self.project_setting_file_path_edit.setEnabled(False)
        self.project_setting_file_path_edit.setObjectName("project_setting_file_path_edit")
        self.horizontalLayout_6.addWidget(self.project_setting_file_path_edit)
        self.set_project_setting_file_path_button = QtWidgets.QPushButton(self.groupBox_7)
        self.set_project_setting_file_path_button.setObjectName("set_project_setting_file_path_button")
        self.horizontalLayout_6.addWidget(self.set_project_setting_file_path_button)
        self.open_project_setting_file_dir_button = QtWidgets.QPushButton(self.groupBox_7)
        self.open_project_setting_file_dir_button.setObjectName("open_project_setting_file_dir_button")
        self.horizontalLayout_6.addWidget(self.open_project_setting_file_dir_button)
        self.verticalLayout_8.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5.addLayout(self.verticalLayout_8)
        self.verticalLayout_4.addWidget(self.groupBox_7)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.reset_setting_button = QtWidgets.QPushButton(Dialog)
        self.reset_setting_button.setObjectName("reset_setting_button")
        self.horizontalLayout_2.addWidget(self.reset_setting_button)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Dialog", "ツール", None, -1))
        self.groupBox_9.setTitle(QtWidgets.QApplication.translate("Dialog", "エクスプローラー", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "ルートフォルダ以下のファイル数の上限を指定", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "ツリーダブルクリック時の挙動：", None, -1))
        self.tree_double_click_expand_radio.setText(QtWidgets.QApplication.translate("Dialog", "何もしない", None, -1))
        self.tree_double_click_set_root_radio.setText(QtWidgets.QApplication.translate("Dialog", "ルートに指定", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "ファイルパスコピー時の区切り：", None, -1))
        self.sep_slash_radio.setText(QtWidgets.QApplication.translate("Dialog", "「/」", None, -1))
        self.sep_back_slash_radio.setText(QtWidgets.QApplication.translate("Dialog", "「\\」", None, -1))
        self.groupBox_10.setTitle(QtWidgets.QApplication.translate("Dialog", "コレクション", None, -1))
        self.col_obj_del_confirm_check.setText(QtWidgets.QApplication.translate("Dialog", "コレクションやシーンをリストから削除する際に確認する", None, -1))
        self.groupBox_8.setTitle(QtWidgets.QApplication.translate("Dialog", "実行時オプション", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("Dialog", "ファイルオープン", None, -1))
        self.exec_set_project_check.setText(QtWidgets.QApplication.translate("Dialog", "プロジェクトのセットを行う", None, -1))
        self.groupBox_3.setTitle(QtWidgets.QApplication.translate("Dialog", "リファレンス/インポート", None, -1))
        self.no_use_namespace_radio.setText(QtWidgets.QApplication.translate("Dialog", "ネームスペースを使用しない", None, -1))
        self.use_file_namespace_radio.setText(QtWidgets.QApplication.translate("Dialog", "ファイル名をネームスペースに使用する", None, -1))
        self.groupBox_4.setTitle(QtWidgets.QApplication.translate("Dialog", "その他", None, -1))
        self.exec_fix_texture_path_check.setText(QtWidgets.QApplication.translate("Dialog", "テクスチャパスの修正を行う", None, -1))
        self.exec_script_node_on_open_check.setText(QtWidgets.QApplication.translate("Dialog", "スクリプトノードを実行する", None, -1))
        self.groupBox_7.setTitle(QtWidgets.QApplication.translate("Dialog", "プロジェクト専用セッティング", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "プロジェクト専用セッティングのパス", None, -1))
        self.set_project_setting_file_path_button.setText(QtWidgets.QApplication.translate("Dialog", "設定", None, -1))
        self.open_project_setting_file_dir_button.setText(QtWidgets.QApplication.translate("Dialog", "開く", None, -1))
        self.reset_setting_button.setText(QtWidgets.QApplication.translate("Dialog", "設定を初期値に戻す", None, -1))

