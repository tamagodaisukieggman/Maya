# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'storyBoadrdRenderItems.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(508, 28)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(0, 28))
        Form.setMaximumSize(QSize(16777215, 28))
        Form.setAutoFillBackground(False)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(16, 0, 3, 0)
        self.isRender = QCheckBox(Form)
        self.isRender.setObjectName(u"isRender")
        self.isRender.setMaximumSize(QSize(18, 16777215))
        font = QFont()
        font.setPointSize(9)
        font.setStrikeOut(False)
        self.isRender.setFont(font)
        self.isRender.setLayoutDirection(Qt.LeftToRight)
        self.isRender.setAutoFillBackground(False)
        self.isRender.setChecked(True)
        self.isRender.setTristate(False)

        self.horizontalLayout.addWidget(self.isRender)

        self.frame = QSpinBox(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(60, 16777215))
        self.frame.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.frame.setMinimum(-99999)
        self.frame.setMaximum(99999)

        self.horizontalLayout.addWidget(self.frame)

        self.clipName = QLineEdit(Form)
        self.clipName.setObjectName(u"clipName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.clipName.sizePolicy().hasHeightForWidth())
        self.clipName.setSizePolicy(sizePolicy1)
        self.clipName.setReadOnly(False)
        self.clipName.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.clipName)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.isRender.setText("")
        self.clipName.setText(QCoreApplication.translate("Form", u"Clip Name", None))
    # retranslateUi

