# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'actor_animation.ui'
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
        MainWindow.resize(728, 272)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.import_file_widget = QWidget(self.centralwidget)
        self.import_file_widget.setObjectName(u"import_file_widget")
        self.horizontalLayout_6 = QHBoxLayout(self.import_file_widget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.import_file_layout = QHBoxLayout()
        self.import_file_layout.setObjectName(u"import_file_layout")
        self.label_3 = QLabel(self.import_file_widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 0))
        self.label_3.setMaximumSize(QSize(100, 16777215))

        self.import_file_layout.addWidget(self.label_3)

        self.file_path = QLineEdit(self.import_file_widget)
        self.file_path.setObjectName(u"file_path")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_path.sizePolicy().hasHeightForWidth())
        self.file_path.setSizePolicy(sizePolicy)
        self.file_path.setMinimumSize(QSize(540, 0))

        self.import_file_layout.addWidget(self.file_path)

        self.dialog_button = QPushButton(self.import_file_widget)
        self.dialog_button.setObjectName(u"dialog_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dialog_button.sizePolicy().hasHeightForWidth())
        self.dialog_button.setSizePolicy(sizePolicy1)
        self.dialog_button.setMinimumSize(QSize(50, 0))
        self.dialog_button.setMaximumSize(QSize(40, 16777215))

        self.import_file_layout.addWidget(self.dialog_button)


        self.horizontalLayout_6.addLayout(self.import_file_layout)


        self.verticalLayout.addWidget(self.import_file_widget)

        self.camera_type_widget = QWidget(self.centralwidget)
        self.camera_type_widget.setObjectName(u"camera_type_widget")
        self.horizontalLayout_3 = QHBoxLayout(self.camera_type_widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.camera_type_layout = QHBoxLayout()
        self.camera_type_layout.setObjectName(u"camera_type_layout")
        self.label_5 = QLabel(self.camera_type_widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(100, 0))
        self.label_5.setMaximumSize(QSize(100, 16777215))

        self.camera_type_layout.addWidget(self.label_5)

        self.horizontalSpacer_5 = QSpacerItem(500, 21, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.camera_type_layout.addItem(self.horizontalSpacer_5)

        self.camera_type_combo_box = QComboBox(self.camera_type_widget)
        self.camera_type_combo_box.setObjectName(u"camera_type_combo_box")
        sizePolicy1.setHeightForWidth(self.camera_type_combo_box.sizePolicy().hasHeightForWidth())
        self.camera_type_combo_box.setSizePolicy(sizePolicy1)
        self.camera_type_combo_box.setMinimumSize(QSize(60, 0))

        self.camera_type_layout.addWidget(self.camera_type_combo_box)


        self.horizontalLayout_3.addLayout(self.camera_type_layout)


        self.verticalLayout.addWidget(self.camera_type_widget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 0))
        self.label_2.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.clip_name = QLineEdit(self.centralwidget)
        self.clip_name.setObjectName(u"clip_name")
        sizePolicy.setHeightForWidth(self.clip_name.sizePolicy().hasHeightForWidth())
        self.clip_name.setSizePolicy(sizePolicy)
        self.clip_name.setMinimumSize(QSize(540, 0))

        self.horizontalLayout_2.addWidget(self.clip_name)

        self.clip_mumber = QLineEdit(self.centralwidget)
        self.clip_mumber.setObjectName(u"clip_mumber")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.clip_mumber.sizePolicy().hasHeightForWidth())
        self.clip_mumber.setSizePolicy(sizePolicy2)
        self.clip_mumber.setMinimumSize(QSize(0, 0))
        self.clip_mumber.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.clip_mumber)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(110, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

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


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.time_widget = QWidget(self.centralwidget)
        self.time_widget.setObjectName(u"time_widget")
        self.horizontalLayout_7 = QHBoxLayout(self.time_widget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_6 = QLabel(self.time_widget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy4)
        self.label_6.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_4.addWidget(self.label_6)

        self.horizontalSpacer_4 = QSpacerItem(300, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.startTime = QSpinBox(self.time_widget)
        self.startTime.setObjectName(u"startTime")
        self.startTime.setMinimumSize(QSize(50, 0))
        self.startTime.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.startTime.setMaximum(999999)

        self.horizontalLayout_4.addWidget(self.startTime)

        self.endTime = QSpinBox(self.time_widget)
        self.endTime.setObjectName(u"endTime")
        self.endTime.setMinimumSize(QSize(50, 0))
        self.endTime.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.endTime.setMaximum(999999)
        self.endTime.setValue(100)

        self.horizontalLayout_4.addWidget(self.endTime)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.time_widget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ok_button = QPushButton(self.centralwidget)
        self.ok_button.setObjectName(u"ok_button")

        self.horizontalLayout.addWidget(self.ok_button)

        self.apply_button = QPushButton(self.centralwidget)
        self.apply_button.setObjectName(u"apply_button")

        self.horizontalLayout.addWidget(self.apply_button)

        self.close_button = QPushButton(self.centralwidget)
        self.close_button.setObjectName(u"close_button")

        self.horizontalLayout.addWidget(self.close_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 728, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u30af\u30ea\u30c3\u30d7\u3092\u8ffd\u52a0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Import File: ", None))
        self.file_path.setText(QCoreApplication.translate("MainWindow", u"Z:/mtk/work/resources/animations/clips/player/ply00_nrm/ply00_nrm_wlk_flt.ma", None))
        self.dialog_button.setText(QCoreApplication.translate("MainWindow", u"\u958b\u304f", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Camera Type: ", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Clip Name: ", None))
        self.clip_name.setText(QCoreApplication.translate("MainWindow", u"sample", None))
        self.clip_mumber.setText(QCoreApplication.translate("MainWindow", u"001", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"(\u30d7\u30ec\u30d3\u30e5\u30fc\uff1a", None))
        self.previewText.setText(QCoreApplication.translate("MainWindow", u"Cut_001", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u")", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Time Range", None))
        self.ok_button.setText(QCoreApplication.translate("MainWindow", u"Insert", None))
        self.apply_button.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.close_button.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

