# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'storyBoadrdRenderOption.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_StoryboardPatchRenderWindow(object):
    def setupUi(self, StoryboardPatchRenderWindow):
        if not StoryboardPatchRenderWindow.objectName():
            StoryboardPatchRenderWindow.setObjectName(u"StoryboardPatchRenderWindow")
        StoryboardPatchRenderWindow.resize(690, 753)
        StoryboardPatchRenderWindow.setStyleSheet(u"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    padding: 0 10px;\n"
"}\n"
"\n"
"QGroupBox{\n"
"	border: 1px solid #1d1d1d;\n"
"	padding: 2px;\n"
"	margin-top: 2ex;\n"
"}\n"
"QListWidget{\n"
"	background-color:#383838;\n"
"\n"
"}\n"
"")
        self.centralwidget = QWidget(StoryboardPatchRenderWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.firstClipList = QListWidget(self.groupBox)
        self.firstClipList.setObjectName(u"firstClipList")
        self.firstClipList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_3.addWidget(self.firstClipList)

        self.updateButton = QPushButton(self.groupBox)
        self.updateButton.setObjectName(u"updateButton")

        self.verticalLayout_3.addWidget(self.updateButton)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.customClipList = QListWidget(self.groupBox_2)
        self.customClipList.setObjectName(u"customClipList")
        self.customClipList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_4.addWidget(self.customClipList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.AddcustomClipListButton = QPushButton(self.groupBox_2)
        self.AddcustomClipListButton.setObjectName(u"AddcustomClipListButton")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddcustomClipListButton.sizePolicy().hasHeightForWidth())
        self.AddcustomClipListButton.setSizePolicy(sizePolicy)
        self.AddcustomClipListButton.setMinimumSize(QSize(50, 0))
        self.AddcustomClipListButton.setMaximumSize(QSize(0, 16777215))
        self.AddcustomClipListButton.setBaseSize(QSize(50, 0))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.AddcustomClipListButton.setFont(font)

        self.horizontalLayout.addWidget(self.AddcustomClipListButton)

        self.removeCustomClipListButton = QPushButton(self.groupBox_2)
        self.removeCustomClipListButton.setObjectName(u"removeCustomClipListButton")
        sizePolicy.setHeightForWidth(self.removeCustomClipListButton.sizePolicy().hasHeightForWidth())
        self.removeCustomClipListButton.setSizePolicy(sizePolicy)
        self.removeCustomClipListButton.setMinimumSize(QSize(50, 0))
        self.removeCustomClipListButton.setMaximumSize(QSize(0, 16777215))
        self.removeCustomClipListButton.setBaseSize(QSize(50, 0))
        self.removeCustomClipListButton.setFont(font)

        self.horizontalLayout.addWidget(self.removeCustomClipListButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout = QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(120, 0))
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_4)

        self.directory = QLineEdit(self.groupBox_3)
        self.directory.setObjectName(u"directory")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.directory.sizePolicy().hasHeightForWidth())
        self.directory.setSizePolicy(sizePolicy2)
        self.directory.setMinimumSize(QSize(0, 22))
        self.directory.setReadOnly(True)

        self.horizontalLayout_7.addWidget(self.directory)

        self.openFolderButton = QPushButton(self.groupBox_3)
        self.openFolderButton.setObjectName(u"openFolderButton")
        sizePolicy.setHeightForWidth(self.openFolderButton.sizePolicy().hasHeightForWidth())
        self.openFolderButton.setSizePolicy(sizePolicy)
        self.openFolderButton.setMinimumSize(QSize(0, 0))
        self.openFolderButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_7.addWidget(self.openFolderButton)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)
        self.label.setMinimumSize(QSize(120, 0))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.comboBox = QComboBox(self.groupBox_3)
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_2.addWidget(self.comboBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)
        self.label_2.setMinimumSize(QSize(120, 0))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.width = QSpinBox(self.groupBox_3)
        self.width.setObjectName(u"width")
        self.width.setMinimumSize(QSize(70, 0))
        self.width.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.width.setMinimum(1)
        self.width.setMaximum(4096)
        self.width.setValue(1920)

        self.horizontalLayout_3.addWidget(self.width)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)
        self.label_3.setMinimumSize(QSize(120, 0))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.height = QSpinBox(self.groupBox_3)
        self.height.setObjectName(u"height")
        self.height.setMinimumSize(QSize(70, 0))
        self.height.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.height.setMinimum(1)
        self.height.setMaximum(4096)
        self.height.setValue(1080)

        self.horizontalLayout_4.addWidget(self.height)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.isOutline = QCheckBox(self.groupBox_3)
        self.isOutline.setObjectName(u"isOutline")
        self.isOutline.setMinimumSize(QSize(125, 0))
        self.isOutline.setChecked(True)

        self.horizontalLayout_5.addWidget(self.isOutline)

        self.isOpenExplorer = QCheckBox(self.groupBox_3)
        self.isOpenExplorer.setObjectName(u"isOpenExplorer")
        self.isOpenExplorer.setChecked(True)

        self.horizontalLayout_5.addWidget(self.isOpenExplorer)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.groupBox_4 = QGroupBox(self.groupBox_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setFlat(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(6)
        self.isCutName = QCheckBox(self.groupBox_4)
        self.isCutName.setObjectName(u"isCutName")
        self.isCutName.setMinimumSize(QSize(96, 0))
        self.isCutName.setChecked(True)

        self.gridLayout_2.addWidget(self.isCutName, 1, 0, 1, 1)

        self.isFocalLength = QCheckBox(self.groupBox_4)
        self.isFocalLength.setObjectName(u"isFocalLength")
        self.isFocalLength.setChecked(True)

        self.gridLayout_2.addWidget(self.isFocalLength, 0, 1, 1, 1)

        self.isSceneName = QCheckBox(self.groupBox_4)
        self.isSceneName.setObjectName(u"isSceneName")
        self.isSceneName.setMinimumSize(QSize(96, 0))
        self.isSceneName.setChecked(True)

        self.gridLayout_2.addWidget(self.isSceneName, 0, 0, 1, 1)

        self.isFrame = QCheckBox(self.groupBox_4)
        self.isFrame.setObjectName(u"isFrame")
        self.isFrame.setChecked(True)

        self.gridLayout_2.addWidget(self.isFrame, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.startCurrentFrameRendering = QPushButton(self.groupBox_3)
        self.startCurrentFrameRendering.setObjectName(u"startCurrentFrameRendering")

        self.verticalLayout.addWidget(self.startCurrentFrameRendering)


        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.startRenderButton = QPushButton(self.centralwidget)
        self.startRenderButton.setObjectName(u"startRenderButton")

        self.horizontalLayout_12.addWidget(self.startRenderButton)

        self.applyButton = QPushButton(self.centralwidget)
        self.applyButton.setObjectName(u"applyButton")

        self.horizontalLayout_12.addWidget(self.applyButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout_12.addWidget(self.closeButton)


        self.gridLayout.addLayout(self.horizontalLayout_12, 3, 0, 1, 1)

        StoryboardPatchRenderWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(StoryboardPatchRenderWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 690, 21))
        StoryboardPatchRenderWindow.setMenuBar(self.menubar)

        self.retranslateUi(StoryboardPatchRenderWindow)

        QMetaObject.connectSlotsByName(StoryboardPatchRenderWindow)
    # setupUi

    def retranslateUi(self, StoryboardPatchRenderWindow):
        StoryboardPatchRenderWindow.setWindowTitle(QCoreApplication.translate("StoryboardPatchRenderWindow", u"StoryboardPatchRender", None))
        self.groupBox.setTitle(QCoreApplication.translate("StoryboardPatchRenderWindow", u"FirstClipList", None))
        self.updateButton.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Update Clip", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("StoryboardPatchRenderWindow", u"CustomClipList", None))
        self.AddcustomClipListButton.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"+", None))
        self.removeCustomClipListButton.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"-", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("StoryboardPatchRenderWindow", u"RenderSettings", None))
        self.label_4.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Directory:", None))
        self.openFolderButton.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"\ud83d\udcc1", None))
        self.label.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Image format:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("StoryboardPatchRenderWindow", u"png", None))

        self.label_2.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Width:", None))
        self.label_3.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Height:", None))
        self.isOutline.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Draw Outline", None))
        self.isOpenExplorer.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Open explorer later", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("StoryboardPatchRenderWindow", u"DrawOption", None))
        self.isCutName.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"CutName", None))
        self.isFocalLength.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"FocalLength", None))
        self.isSceneName.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"SceneName", None))
        self.isFrame.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Frame", None))
        self.startCurrentFrameRendering.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Current Frame Rendering", None))
        self.startRenderButton.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Start Render", None))
        self.applyButton.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Apply", None))
        self.closeButton.setText(QCoreApplication.translate("StoryboardPatchRenderWindow", u"Close", None))
    # retranslateUi

