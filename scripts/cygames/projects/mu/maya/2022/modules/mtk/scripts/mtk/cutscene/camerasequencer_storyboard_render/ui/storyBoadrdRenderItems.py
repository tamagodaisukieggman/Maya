# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'z:\mtk\tools\maya\modules\mtku\scripts\mtku\maya\menus\cutscene\camerasequencer_storyboard_render\ui\storyBoadrdRenderItems.ui'
#
# Created: Wed Jul 21 20:30:07 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(508, 28)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 28))
        Form.setMaximumSize(QtCore.QSize(16777215, 28))
        Form.setAutoFillBackground(False)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(16, 0, 3, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.isRender = QtWidgets.QCheckBox(Form)
        self.isRender.setMaximumSize(QtCore.QSize(18, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setStrikeOut(False)
        self.isRender.setFont(font)
        self.isRender.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.isRender.setAutoFillBackground(False)
        self.isRender.setText("")
        self.isRender.setChecked(True)
        self.isRender.setTristate(False)
        self.isRender.setObjectName("isRender")
        self.horizontalLayout.addWidget(self.isRender)
        self.frame = QtWidgets.QSpinBox(Form)
        self.frame.setMaximumSize(QtCore.QSize(60, 16777215))
        self.frame.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.frame.setMinimum(-99999)
        self.frame.setMaximum(99999)
        self.frame.setObjectName("frame")
        self.horizontalLayout.addWidget(self.frame)
        self.clipName = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clipName.sizePolicy().hasHeightForWidth())
        self.clipName.setSizePolicy(sizePolicy)
        self.clipName.setReadOnly(False)
        self.clipName.setClearButtonEnabled(True)
        self.clipName.setObjectName("clipName")
        self.horizontalLayout.addWidget(self.clipName)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.clipName.setText(QtWidgets.QApplication.translate("Form", "Clip Name", None, -1))

