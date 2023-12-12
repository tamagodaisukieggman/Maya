# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CreateCameraOption.ui'
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
        MainWindow.resize(345, 260)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_2.addWidget(self.label)

        self.cameraGroup = QLineEdit(self.centralwidget)
        self.cameraGroup.setObjectName(u"cameraGroup")

        self.horizontalLayout_2.addWidget(self.cameraGroup)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_6.addWidget(self.label_3)

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


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(135, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.previewText = QLabel(self.centralwidget)
        self.previewText.setObjectName(u"previewText")
        self.previewText.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.previewText)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy3)

        self.horizontalLayout_4.addWidget(self.label_8)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_5.addWidget(self.label_5)

        self.shotPlacement = QComboBox(self.centralwidget)
        self.shotPlacement.addItem("")
        self.shotPlacement.addItem("")
        self.shotPlacement.addItem("")
        self.shotPlacement.setObjectName(u"shotPlacement")

        self.horizontalLayout_5.addWidget(self.shotPlacement)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_3.addWidget(self.label_4)

        self.cameraType = QComboBox(self.centralwidget)
        self.cameraType.addItem("")
        self.cameraType.addItem("")
        self.cameraType.addItem("")
        self.cameraType.setObjectName(u"cameraType")

        self.horizontalLayout_3.addWidget(self.cameraType)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_7.addWidget(self.label_6)

        self.startTime = QSpinBox(self.centralwidget)
        self.startTime.setObjectName(u"startTime")
        self.startTime.setMinimumSize(QSize(50, 0))
        self.startTime.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.horizontalLayout_7.addWidget(self.startTime)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_8.addWidget(self.label_7)

        self.endTime = QSpinBox(self.centralwidget)
        self.endTime.setObjectName(u"endTime")
        self.endTime.setMinimumSize(QSize(50, 0))
        self.endTime.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.endTime.setMaximum(9999)
        self.endTime.setValue(100)

        self.horizontalLayout_8.addWidget(self.endTime)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.createCameraButton = QPushButton(self.centralwidget)
        self.createCameraButton.setObjectName(u"createCameraButton")

        self.horizontalLayout.addWidget(self.createCameraButton)

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
        self.menubar.setGeometry(QRect(0, 0, 345, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Create Camera Options", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Camera GroupName", None))
        self.cameraGroup.setText(QCoreApplication.translate("MainWindow", u"CameraGroup", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Shot Name", None))
        self.shotName.setText(QCoreApplication.translate("MainWindow", u"Cut_", None))
        self.shotNumber.setText(QCoreApplication.translate("MainWindow", u"001", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"(\u30d7\u30ec\u30d3\u30e5\u30fc\uff1a", None))
        self.previewText.setText(QCoreApplication.translate("MainWindow", u"Cut_001", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u")", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"New Shot Placement", None))
        self.shotPlacement.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.shotPlacement.setItemText(1, QCoreApplication.translate("MainWindow", u"CurrentFrame", None))
        self.shotPlacement.setItemText(2, QCoreApplication.translate("MainWindow", u"EndFrame", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"CameraType", None))
        self.cameraType.setItemText(0, QCoreApplication.translate("MainWindow", u"Normal", None))
        self.cameraType.setItemText(1, QCoreApplication.translate("MainWindow", u"Aim", None))
        self.cameraType.setItemText(2, QCoreApplication.translate("MainWindow", u"AimAndUp", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Start time", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"End time", None))
        self.createCameraButton.setText(QCoreApplication.translate("MainWindow", u"Create Camera", None))
        self.applyButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

