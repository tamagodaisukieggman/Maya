# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
        MainWindow.resize(409, 200)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_8.addWidget(self.label_7)

        self.offsetFrame = QSpinBox(self.centralwidget)
        self.offsetFrame.setObjectName(u"offsetFrame")
        self.offsetFrame.setMinimumSize(QSize(50, 0))
        self.offsetFrame.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.offsetFrame.setMaximum(9999)
        self.offsetFrame.setValue(60)

        self.horizontalLayout_8.addWidget(self.offsetFrame)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.isWavFileCheckBox = QCheckBox(self.centralwidget)
        self.isWavFileCheckBox.setObjectName(u"isWavFileCheckBox")
        self.isWavFileCheckBox.setChecked(True)
        self.isWavFileCheckBox.setTristate(False)

        self.gridLayout.addWidget(self.isWavFileCheckBox, 0, 1, 1, 1)

        self.isRigAnimationCheckBox = QCheckBox(self.centralwidget)
        self.isRigAnimationCheckBox.setObjectName(u"isRigAnimationCheckBox")
        self.isRigAnimationCheckBox.setChecked(True)

        self.gridLayout.addWidget(self.isRigAnimationCheckBox, 0, 0, 1, 1)

        self.isMovieFIleCheckBox = QCheckBox(self.centralwidget)
        self.isMovieFIleCheckBox.setObjectName(u"isMovieFIleCheckBox")
        self.isMovieFIleCheckBox.setChecked(True)

        self.gridLayout.addWidget(self.isMovieFIleCheckBox, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.syncTimeSliderButton = QPushButton(self.centralwidget)
        self.syncTimeSliderButton.setObjectName(u"syncTimeSliderButton")

        self.verticalLayout.addWidget(self.syncTimeSliderButton)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.syncButton = QPushButton(self.centralwidget)
        self.syncButton.setObjectName(u"syncButton")

        self.horizontalLayout.addWidget(self.syncButton)

        self.applyButton = QPushButton(self.centralwidget)
        self.applyButton.setObjectName(u"applyButton")

        self.horizontalLayout.addWidget(self.applyButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 409, 26))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Live link Utility", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Offset Frame", None))
        self.isWavFileCheckBox.setText(QCoreApplication.translate("MainWindow", u"wav", None))
        self.isRigAnimationCheckBox.setText(QCoreApplication.translate("MainWindow", u"rig Animation", None))
        self.isMovieFIleCheckBox.setText(QCoreApplication.translate("MainWindow", u"movie(image plane)", None))
        self.syncTimeSliderButton.setText(QCoreApplication.translate("MainWindow", u"Sync Time slider only", None))
        self.syncButton.setText(QCoreApplication.translate("MainWindow", u"Sync", None))
        self.applyButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

