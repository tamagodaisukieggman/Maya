# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playblastOption.ui'
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
        MainWindow.resize(430, 602)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 6, -1, -1)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(120, 0))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label)

        self.directory = QLineEdit(self.groupBox)
        self.directory.setObjectName(u"directory")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.directory.sizePolicy().hasHeightForWidth())
        self.directory.setSizePolicy(sizePolicy1)
        self.directory.setMinimumSize(QSize(0, 22))
        self.directory.setReadOnly(True)

        self.horizontalLayout_7.addWidget(self.directory)

        self.openFolderButton = QPushButton(self.groupBox)
        self.openFolderButton.setObjectName(u"openFolderButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.openFolderButton.sizePolicy().hasHeightForWidth())
        self.openFolderButton.setSizePolicy(sizePolicy2)
        self.openFolderButton.setMinimumSize(QSize(0, 0))
        self.openFolderButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_7.addWidget(self.openFolderButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 0))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_2)

        self.fileName = QLineEdit(self.groupBox)
        self.fileName.setObjectName(u"fileName")

        self.horizontalLayout_6.addWidget(self.fileName)

        self.fileNumber = QLineEdit(self.groupBox)
        self.fileNumber.setObjectName(u"fileNumber")
        sizePolicy2.setHeightForWidth(self.fileNumber.sizePolicy().hasHeightForWidth())
        self.fileNumber.setSizePolicy(sizePolicy2)
        self.fileNumber.setMinimumSize(QSize(0, 0))
        self.fileNumber.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_6.addWidget(self.fileNumber)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_8 = QSpacerItem(135, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_8)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_10.addWidget(self.label_9)

        self.previewText = QLabel(self.groupBox)
        self.previewText.setObjectName(u"previewText")
        self.previewText.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.previewText)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy3)

        self.horizontalLayout_10.addWidget(self.label_10)


        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.IsFileOverride = QCheckBox(self.groupBox)
        self.IsFileOverride.setObjectName(u"IsFileOverride")
        self.IsFileOverride.setMinimumSize(QSize(140, 0))
        self.IsFileOverride.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_14.addWidget(self.IsFileOverride)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_9)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 6, -1, -1)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.IsView = QCheckBox(self.groupBox_3)
        self.IsView.setObjectName(u"IsView")
        self.IsView.setMinimumSize(QSize(140, 0))
        self.IsView.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_8.addWidget(self.IsView)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.IsOffscreen = QCheckBox(self.groupBox_3)
        self.IsOffscreen.setObjectName(u"IsOffscreen")
        self.IsOffscreen.setMinimumSize(QSize(140, 0))
        self.IsOffscreen.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_9.addWidget(self.IsOffscreen)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.IsOrnaments = QCheckBox(self.groupBox_3)
        self.IsOrnaments.setObjectName(u"IsOrnaments")
        self.IsOrnaments.setMinimumSize(QSize(140, 0))
        self.IsOrnaments.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_13.addWidget(self.IsOrnaments)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_5)


        self.verticalLayout_4.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(120, 0))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.formatType = QComboBox(self.groupBox_3)
        self.formatType.setObjectName(u"formatType")

        self.horizontalLayout_5.addWidget(self.formatType)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(120, 0))
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.encodingType = QComboBox(self.groupBox_3)
        self.encodingType.setObjectName(u"encodingType")
        self.encodingType.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_4.addWidget(self.encodingType)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy4)
        self.label_8.setMinimumSize(QSize(120, 0))
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_8)

        self.modeType = QComboBox(self.groupBox_3)
        self.modeType.addItem("")
        self.modeType.addItem("")
        self.modeType.addItem("")
        self.modeType.setObjectName(u"modeType")

        self.horizontalLayout_11.addWidget(self.modeType)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.IsMP4 = QCheckBox(self.groupBox_3)
        self.IsMP4.setObjectName(u"IsMP4")
        self.IsMP4.setEnabled(False)
        self.IsMP4.setMinimumSize(QSize(140, 0))
        self.IsMP4.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_15.addWidget(self.IsMP4)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_10)


        self.verticalLayout_4.addLayout(self.horizontalLayout_15)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 6, -1, -1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(120, 0))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_5)

        self.quality = QSpinBox(self.groupBox_4)
        self.quality.setObjectName(u"quality")
        self.quality.setMinimumSize(QSize(0, 0))
        self.quality.setMaximumSize(QSize(40, 16777215))
        self.quality.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.quality.setMaximum(100)
        self.quality.setValue(70)

        self.horizontalLayout_3.addWidget(self.quality)

        self.qualitySlider = QSlider(self.groupBox_4)
        self.qualitySlider.setObjectName(u"qualitySlider")
        self.qualitySlider.setMaximum(100)
        self.qualitySlider.setValue(70)
        self.qualitySlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.qualitySlider)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(120, 0))
        self.label_6.setLayoutDirection(Qt.LeftToRight)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_6)

        self.resolutionWidth = QSpinBox(self.groupBox_4)
        self.resolutionWidth.setObjectName(u"resolutionWidth")
        self.resolutionWidth.setMaximumSize(QSize(40, 16777215))
        self.resolutionWidth.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.resolutionWidth.setMinimum(1)
        self.resolutionWidth.setMaximum(4048)
        self.resolutionWidth.setValue(1920)

        self.horizontalLayout_2.addWidget(self.resolutionWidth)

        self.resolutionWidthSlider = QSlider(self.groupBox_4)
        self.resolutionWidthSlider.setObjectName(u"resolutionWidthSlider")
        self.resolutionWidthSlider.setMinimum(1)
        self.resolutionWidthSlider.setMaximum(4048)
        self.resolutionWidthSlider.setValue(1920)
        self.resolutionWidthSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.resolutionWidthSlider)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(120, 0))
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_7)

        self.resolutionHeight = QSpinBox(self.groupBox_4)
        self.resolutionHeight.setObjectName(u"resolutionHeight")
        self.resolutionHeight.setMaximumSize(QSize(40, 16777215))
        self.resolutionHeight.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.resolutionHeight.setMinimum(1)
        self.resolutionHeight.setMaximum(4047)
        self.resolutionHeight.setValue(1080)

        self.horizontalLayout.addWidget(self.resolutionHeight)

        self.resolutionHeightSlider = QSlider(self.groupBox_4)
        self.resolutionHeightSlider.setObjectName(u"resolutionHeightSlider")
        self.resolutionHeightSlider.setMinimum(1)
        self.resolutionHeightSlider.setMaximum(4048)
        self.resolutionHeightSlider.setValue(1080)
        self.resolutionHeightSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.resolutionHeightSlider)


        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 6, -1, -1)
        self.StartFrameLayout = QHBoxLayout()
        self.StartFrameLayout.setObjectName(u"StartFrameLayout")
        self.startTimeLabel = QLabel(self.groupBox_2)
        self.startTimeLabel.setObjectName(u"startTimeLabel")
        self.startTimeLabel.setEnabled(True)
        self.startTimeLabel.setMinimumSize(QSize(120, 0))
        self.startTimeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.StartFrameLayout.addWidget(self.startTimeLabel)

        self.startTime = QSpinBox(self.groupBox_2)
        self.startTime.setObjectName(u"startTime")
        self.startTime.setEnabled(True)
        self.startTime.setMaximumSize(QSize(40, 16777215))
        self.startTime.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.startTime.setMinimum(0)
        self.startTime.setMaximum(99999)
        self.startTime.setValue(0)

        self.StartFrameLayout.addWidget(self.startTime)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.StartFrameLayout.addItem(self.horizontalSpacer_6)


        self.verticalLayout_3.addLayout(self.StartFrameLayout)

        self.EndFrameLayout = QHBoxLayout()
        self.EndFrameLayout.setObjectName(u"EndFrameLayout")
        self.endTimeLabel = QLabel(self.groupBox_2)
        self.endTimeLabel.setObjectName(u"endTimeLabel")
        self.endTimeLabel.setMinimumSize(QSize(120, 0))
        self.endTimeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.EndFrameLayout.addWidget(self.endTimeLabel)

        self.endTime = QSpinBox(self.groupBox_2)
        self.endTime.setObjectName(u"endTime")
        self.endTime.setMaximumSize(QSize(40, 16777215))
        self.endTime.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.endTime.setMinimum(0)
        self.endTime.setMaximum(99999)
        self.endTime.setValue(100)

        self.EndFrameLayout.addWidget(self.endTime)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.EndFrameLayout.addItem(self.horizontalSpacer_7)


        self.verticalLayout_3.addLayout(self.EndFrameLayout)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.startPlayblastButton = QPushButton(self.centralwidget)
        self.startPlayblastButton.setObjectName(u"startPlayblastButton")

        self.horizontalLayout_12.addWidget(self.startPlayblastButton)

        self.applyButton = QPushButton(self.centralwidget)
        self.applyButton.setObjectName(u"applyButton")

        self.horizontalLayout_12.addWidget(self.applyButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout_12.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 430, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PlayblastOption", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Directory:", None))
        self.openFolderButton.setText(QCoreApplication.translate("MainWindow", u"\ud83d\udcc1", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"File name:", None))
        self.fileName.setText(QCoreApplication.translate("MainWindow", u"Cut_", None))
        self.fileNumber.setText(QCoreApplication.translate("MainWindow", u"001", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"(\u30d7\u30ec\u30d3\u30e5\u30fc\uff1a", None))
        self.previewText.setText(QCoreApplication.translate("MainWindow", u"Cut_001", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u")", None))
        self.IsFileOverride.setText(QCoreApplication.translate("MainWindow", u"FileOverride", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.IsView.setText(QCoreApplication.translate("MainWindow", u"View:", None))
        self.IsOffscreen.setText(QCoreApplication.translate("MainWindow", u"Offscreen:", None))
        self.IsOrnaments.setText(QCoreApplication.translate("MainWindow", u"Ornaments:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Format:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Encoding:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Mode:", None))
        self.modeType.setItemText(0, QCoreApplication.translate("MainWindow", u"All Frame", None))
        self.modeType.setItemText(1, QCoreApplication.translate("MainWindow", u"Select Clip", None))
        self.modeType.setItemText(2, QCoreApplication.translate("MainWindow", u"Select Frame", None))

        self.IsMP4.setText(QCoreApplication.translate("MainWindow", u"Convert MP4", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Image", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Quality", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Resolution Width", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Resolution height", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Select Frame", None))
        self.startTimeLabel.setText(QCoreApplication.translate("MainWindow", u"Start Frame", None))
        self.endTimeLabel.setText(QCoreApplication.translate("MainWindow", u"End Frame", None))
        self.startPlayblastButton.setText(QCoreApplication.translate("MainWindow", u"Start Playblast", None))
        self.applyButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

