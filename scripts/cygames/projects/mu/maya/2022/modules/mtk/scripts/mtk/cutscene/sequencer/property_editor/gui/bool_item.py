# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bool_item.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Item(object):
    def setupUi(self, Item):
        if not Item.objectName():
            Item.setObjectName(u"Item")
        Item.resize(400, 45)
        Item.setMinimumSize(QSize(400, 45))
        Item.setMaximumSize(QSize(16777215, 45))
        self.horizontalLayout_2 = QHBoxLayout(Item)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.propertyLabel = QLabel(Item)
        self.propertyLabel.setObjectName(u"propertyLabel")

        self.horizontalLayout.addWidget(self.propertyLabel)

        self.label_2 = QLabel(Item)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.propertyValueBool = QCheckBox(Item)
        self.propertyValueBool.setObjectName(u"propertyValueBool")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.propertyValueBool.sizePolicy().hasHeightForWidth())
        self.propertyValueBool.setSizePolicy(sizePolicy)
        self.propertyValueBool.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QCheckBox {\n"
"	border-color: white;\n"
"}")
        self.propertyValueBool.setIconSize(QSize(20, 20))
        self.propertyValueBool.setAutoRepeat(False)
        self.propertyValueBool.setTristate(False)

        self.horizontalLayout.addWidget(self.propertyValueBool)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Item)

        QMetaObject.connectSlotsByName(Item)
    # setupUi

    def retranslateUi(self, Item):
        Item.setWindowTitle(QCoreApplication.translate("Item", u"Form", None))
        self.propertyLabel.setText(QCoreApplication.translate("Item", u"property_name", None))
        self.label_2.setText(QCoreApplication.translate("Item", u":", None))
        self.propertyValueBool.setText("")
    # retranslateUi

