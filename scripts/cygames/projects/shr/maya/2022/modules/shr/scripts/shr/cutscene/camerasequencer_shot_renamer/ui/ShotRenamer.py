# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ShotRenamer.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(387, 204)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_6.addWidget(self.label_7)

        self.shotName = QLineEdit(self.centralwidget)
        self.shotName.setObjectName(u"shotName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.shotName.sizePolicy().hasHeightForWidth())
        self.shotName.setSizePolicy(sizePolicy1)

        self.horizontalLayout_6.addWidget(self.shotName)

        self.shotNumber = QLineEdit(self.centralwidget)
        self.shotNumber.setObjectName(u"shotNumber")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.shotNumber.sizePolicy().hasHeightForWidth())
        self.shotNumber.setSizePolicy(sizePolicy2)
        self.shotNumber.setMinimumSize(QSize(0, 0))
        self.shotNumber.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_6.addWidget(self.shotNumber)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(135, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.previewText = QLabel(self.centralwidget)
        self.previewText.setObjectName(u"previewText")
        self.previewText.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.previewText)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy3)

        self.horizontalLayout_5.addWidget(self.label_8)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_3.addWidget(self.label_6)

        self.sortType = QComboBox(self.centralwidget)
        self.sortType.addItem("")
        self.sortType.setObjectName(u"sortType")
        self.sortType.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_3.addWidget(self.sortType)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_2.addWidget(self.label_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.is_rename_camera = QCheckBox(self.centralwidget)
        self.is_rename_camera.setObjectName(u"is_rename_camera")

        self.verticalLayout.addWidget(self.is_rename_camera)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setMinimumSize(QSize(0, 0))

        self.verticalLayout.addWidget(self.label_5)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.startRenameButton = QPushButton(self.centralwidget)
        self.startRenameButton.setObjectName(u"startRenameButton")

        self.horizontalLayout.addWidget(self.startRenameButton)

        self.applyButton = QPushButton(self.centralwidget)
        self.applyButton.setObjectName(u"applyButton")

        self.horizontalLayout.addWidget(self.applyButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 387, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ShotRenamer", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Shot Name", None))
        self.shotName.setText(QCoreApplication.translate("MainWindow", u"Cut_", None))
        self.shotNumber.setText(QCoreApplication.translate("MainWindow", u"001", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"(\u30d7\u30ec\u30d3\u30e5\u30fc\uff1a", None))
        self.previewText.setText(QCoreApplication.translate("MainWindow", u"Cut_001", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u")", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"SortType", None))
        self.sortType.setItemText(0, QCoreApplication.translate("MainWindow", u"\u6607\u9806", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"SortTarget", None))
        self.is_rename_camera.setText(QCoreApplication.translate("MainWindow", u"Camera\u3082\u30ea\u30cd\u30fc\u30e0\u306b\u542b\u3081\u308b", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>(\u8907\u6570\u306e\u306eShot\u3067\u4e00\u3064\u306e\u30ab\u30e1\u30e9\u3092\u53c2\u7167\u3057\u3066\u3044\u308b\u6642\u306f<br/>\u30ea\u30cd\u30fc\u30e0\u306b\u5931\u6557\u3059\u308b\u306e\u3067\u3001\u30c1\u30a7\u30c3\u30af\u3092\u5916\u3057\u3066\u304f\u3060\u3055\u3044\u3002</p></body></html>", None))
        self.startRenameButton.setText(QCoreApplication.translate("MainWindow", u"Rename Shot", None))
        self.applyButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

