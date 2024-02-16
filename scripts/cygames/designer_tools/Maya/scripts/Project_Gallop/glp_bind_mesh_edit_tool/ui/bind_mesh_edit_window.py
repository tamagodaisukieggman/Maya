# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\tech-designer\maya_legacy\scripts\Project_Gallop\glp_bind_mesh_edit_tool\ui\bind_mesh_edit_window.ui'
#
# Created: Fri Oct 28 12:45:01 2022
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 108)
        MainWindow.setMaximumSize(QtCore.QSize(400, 110))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.exec_devide_skinned_mesh_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.exec_devide_skinned_mesh_btn.setObjectName("exec_devide_skinned_mesh_btn")
        self.verticalLayout_4.addWidget(self.exec_devide_skinned_mesh_btn)
        self.exec_merge_skinned_meshes_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.exec_merge_skinned_meshes_btn.setObjectName("exec_merge_skinned_meshes_btn")
        self.verticalLayout_4.addWidget(self.exec_merge_skinned_meshes_btn)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.verticalLayout.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.register_exec_clean_mesh_deformer_cmd = QtWidgets.QAction(MainWindow)
        self.register_exec_clean_mesh_deformer_cmd.setObjectName("register_exec_clean_mesh_deformer_cmd")
        self.register_exec_devide_skinned_mesh_cmd = QtWidgets.QAction(MainWindow)
        self.register_exec_devide_skinned_mesh_cmd.setObjectName("register_exec_devide_skinned_mesh_cmd")
        self.register_exec_merge_skinned_meshes_cmd = QtWidgets.QAction(MainWindow)
        self.register_exec_merge_skinned_meshes_cmd.setObjectName("register_exec_merge_skinned_meshes_cmd")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "バインドメッシュ編集ツール", None, -1))
        self.groupBox_3.setTitle(QtWidgets.QApplication.translate("MainWindow", "バインドメッシュ分割・結合", None, -1))
        self.exec_devide_skinned_mesh_btn.setText(QtWidgets.QApplication.translate("MainWindow", "選択したメッシュのフェースをスキニングを維持したまま分割する", None, -1))
        self.exec_merge_skinned_meshes_btn.setText(QtWidgets.QApplication.translate("MainWindow", "選択したメッシュ同士をスキニング及びウェイトを維持したまま結合する", None, -1))
        self.register_exec_clean_mesh_deformer_cmd.setText(QtWidgets.QApplication.translate("MainWindow", "編集したバインドメッシュを複製してウェイトコピー", None, -1))
        self.register_exec_devide_skinned_mesh_cmd.setText(QtWidgets.QApplication.translate("MainWindow", "選択したフェースのバインドを保持したままメッシュ分割", None, -1))
        self.register_exec_merge_skinned_meshes_cmd.setText(QtWidgets.QApplication.translate("MainWindow", "選択した複数のオブジェクトのバインドを保持したまま結合", None, -1))

