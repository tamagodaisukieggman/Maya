# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\work\maya_legacy\scripts\Project_Gallop\glp_bg_exporter\node_widget.ui'
#
# Created: Tue Jul 18 10:40:25 2023
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(6, 8, 6, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.removeItemButton = QtWidgets.QPushButton(self.widget)
        self.removeItemButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeItemButton.sizePolicy().hasHeightForWidth())
        self.removeItemButton.setSizePolicy(sizePolicy)
        self.removeItemButton.setMinimumSize(QtCore.QSize(12, 12))
        self.removeItemButton.setMaximumSize(QtCore.QSize(12, 12))
        self.removeItemButton.setStyleSheet("padding-left: 1px;\n"
"padding-top: -2px;\n"
"background-color: rgb(64, 64, 64);")
        self.removeItemButton.setObjectName("removeItemButton")
        self.horizontalLayout.addWidget(self.removeItemButton)
        self.nodeNameLabel = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nodeNameLabel.sizePolicy().hasHeightForWidth())
        self.nodeNameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.nodeNameLabel.setFont(font)
        self.nodeNameLabel.setStyleSheet("margin-left: 2px;\n"
"margin-top: -1px;\n"
"color: rgb(255, 255, 255);")
        self.nodeNameLabel.setText("")
        self.nodeNameLabel.setObjectName("nodeNameLabel")
        self.horizontalLayout.addWidget(self.nodeNameLabel)
        self.fileNameLabel = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileNameLabel.sizePolicy().hasHeightForWidth())
        self.fileNameLabel.setSizePolicy(sizePolicy)
        self.fileNameLabel.setStyleSheet("margin-left: 4px;\n"
"margin-top: -1px;\n"
"color: rgb(255, 255, 255);")
        self.fileNameLabel.setText("")
        self.fileNameLabel.setObjectName("fileNameLabel")
        self.horizontalLayout.addWidget(self.fileNameLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.nodeErrorLabel = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nodeErrorLabel.sizePolicy().hasHeightForWidth())
        self.nodeErrorLabel.setSizePolicy(sizePolicy)
        self.nodeErrorLabel.setMinimumSize(QtCore.QSize(42, 0))
        self.nodeErrorLabel.setMaximumSize(QtCore.QSize(42, 16777215))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.nodeErrorLabel.setFont(font)
        self.nodeErrorLabel.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(204, 77, 77);")
        self.nodeErrorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nodeErrorLabel.setObjectName("nodeErrorLabel")
        self.horizontalLayout.addWidget(self.nodeErrorLabel)
        self.selectNodeButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectNodeButton.sizePolicy().hasHeightForWidth())
        self.selectNodeButton.setSizePolicy(sizePolicy)
        self.selectNodeButton.setMinimumSize(QtCore.QSize(60, 20))
        self.selectNodeButton.setMaximumSize(QtCore.QSize(60, 20))
        self.selectNodeButton.setObjectName("selectNodeButton")
        self.horizontalLayout.addWidget(self.selectNodeButton)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.folderButton = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.folderButton.sizePolicy().hasHeightForWidth())
        self.folderButton.setSizePolicy(sizePolicy)
        self.folderButton.setMinimumSize(QtCore.QSize(16, 16))
        self.folderButton.setMaximumSize(QtCore.QSize(16, 16))
        self.folderButton.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-color: rgb(179, 179, 179);\n"
"    padding-top: -1px;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QPushButton:checked\n"
"{\n"
"    background-color: rgb(255, 179, 77);\n"
"    border-color: rgb(179, 141, 90);\n"
"}\n"
"")
        self.folderButton.setText("")
        self.folderButton.setCheckable(True)
        self.folderButton.setChecked(True)
        self.folderButton.setObjectName("folderButton")
        self.horizontalLayout_2.addWidget(self.folderButton)
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.folderPathLineEdit = QtWidgets.QLineEdit(self.widget_3)
        self.folderPathLineEdit.setStyleSheet("QLineEdit {\n"
"    margin-left: 4px;\n"
"    margin-right: 4px;\n"
"    padding-left: 2px;\n"
"}\n"
"QLineEdit[dirExists=\"true\"] {\n"
"    background-color: rgb(42, 42, 42);\n"
"}\n"
"QLineEdit[dirExists=\"false\"] {\n"
"    background-color: rgb(51, 31, 31);\n"
"}\n"
"QLineEdit[dirExists=\"false\"][canMakeDir=\"true\"] {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(153, 153, 0);\n"
"}\n"
"")
        self.folderPathLineEdit.setProperty("dirExists", False)
        self.folderPathLineEdit.setProperty("canMakeDir", False)
        self.folderPathLineEdit.setObjectName("folderPathLineEdit")
        self.horizontalLayout_3.addWidget(self.folderPathLineEdit)
        self.selectFolderButton = QtWidgets.QPushButton(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectFolderButton.sizePolicy().hasHeightForWidth())
        self.selectFolderButton.setSizePolicy(sizePolicy)
        self.selectFolderButton.setMinimumSize(QtCore.QSize(40, 20))
        self.selectFolderButton.setMaximumSize(QtCore.QSize(40, 20))
        self.selectFolderButton.setObjectName("selectFolderButton")
        self.horizontalLayout_3.addWidget(self.selectFolderButton)
        self.openExplorerButton = QtWidgets.QPushButton(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openExplorerButton.sizePolicy().hasHeightForWidth())
        self.openExplorerButton.setSizePolicy(sizePolicy)
        self.openExplorerButton.setMinimumSize(QtCore.QSize(60, 20))
        self.openExplorerButton.setMaximumSize(QtCore.QSize(60, 20))
        self.openExplorerButton.setObjectName("openExplorerButton")
        self.horizontalLayout_3.addWidget(self.openExplorerButton)
        self.horizontalLayout_2.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.horizontalLayout_2.addWidget(self.widget_4)
        self.verticalLayout.addWidget(self.widget_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 4, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.line = QtWidgets.QFrame(Form)
        self.line.setStyleSheet("border: none;\n"
"max-height: 1px;\n"
"background-color: rgb(153, 153, 153)")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.folderButton, QtCore.SIGNAL("toggled(bool)"), self.widget_3.setVisible)
        QtCore.QObject.connect(self.folderButton, QtCore.SIGNAL("toggled(bool)"), self.widget_4.setHidden)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.removeItemButton.setText(QtWidgets.QApplication.translate("Form", "×", None, -1))
        self.nodeErrorLabel.setText(QtWidgets.QApplication.translate("Form", "error !", None, -1))
        self.selectNodeButton.setText(QtWidgets.QApplication.translate("Form", "ノード選択", None, -1))
        self.folderPathLineEdit.setPlaceholderText(QtWidgets.QApplication.translate("Form", "保存先フォルダパス", None, -1))
        self.selectFolderButton.setText(QtWidgets.QApplication.translate("Form", "参照", None, -1))
        self.openExplorerButton.setText(QtWidgets.QApplication.translate("Form", "Explorer", None, -1))

