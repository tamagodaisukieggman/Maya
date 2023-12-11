# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\tech-designer\Maya\scripts\Project_Gallop\glp_vaccine_delete\ui\vaccine_delete.ui'
#
# Created: Thu Aug 27 22:43:32 2020
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 78)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(65536, 78))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.targetPathLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.targetPathLabel.sizePolicy().hasHeightForWidth())
        self.targetPathLabel.setSizePolicy(sizePolicy)
        self.targetPathLabel.setObjectName("targetPathLabel")
        self.horizontalLayout.addWidget(self.targetPathLabel)
        self.filePathEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.filePathEdit.setObjectName("filePathEdit")
        self.horizontalLayout.addWidget(self.filePathEdit)
        self.pathSetButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pathSetButton.sizePolicy().hasHeightForWidth())
        self.pathSetButton.setSizePolicy(sizePolicy)
        self.pathSetButton.setObjectName("pathSetButton")
        self.horizontalLayout.addWidget(self.pathSetButton)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        self.horizontalLayout.setStretch(2, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.execButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.execButton.sizePolicy().hasHeightForWidth())
        self.execButton.setSizePolicy(sizePolicy)
        self.execButton.setObjectName("execButton")
        self.verticalLayout_2.addWidget(self.execButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Delete Vaccine", None, -1))
        self.targetPathLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Vaccineを削除する対象のパス", None, -1))
        self.pathSetButton.setText(QtWidgets.QApplication.translate("MainWindow", "パスをセットする", None, -1))
        self.execButton.setText(QtWidgets.QApplication.translate("MainWindow", "実行", None, -1))

