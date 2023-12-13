# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'float3_item.ui'
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
        self.horizontalLayout = QHBoxLayout(Item)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.propertyLabel = QLabel(Item)
        self.propertyLabel.setObjectName(u"propertyLabel")

        self.horizontalLayout.addWidget(self.propertyLabel)

        self.label_2 = QLabel(Item)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.propertyValueFloatX = QDoubleSpinBox(Item)
        self.propertyValueFloatX.setObjectName(u"propertyValueFloatX")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.propertyValueFloatX.sizePolicy().hasHeightForWidth())
        self.propertyValueFloatX.setSizePolicy(sizePolicy)
        self.propertyValueFloatX.setMinimumSize(QSize(0, 0))
        self.propertyValueFloatX.setDecimals(5)
        self.propertyValueFloatX.setMaximum(1000000.000000000000000)

        self.horizontalLayout.addWidget(self.propertyValueFloatX)

        self.propertyValueFloatY = QDoubleSpinBox(Item)
        self.propertyValueFloatY.setObjectName(u"propertyValueFloatY")
        sizePolicy.setHeightForWidth(self.propertyValueFloatY.sizePolicy().hasHeightForWidth())
        self.propertyValueFloatY.setSizePolicy(sizePolicy)
        self.propertyValueFloatY.setMinimumSize(QSize(0, 0))
        self.propertyValueFloatY.setDecimals(5)
        self.propertyValueFloatY.setMaximum(1000000.000000000000000)

        self.horizontalLayout.addWidget(self.propertyValueFloatY)

        self.propertyValueFloatZ = QDoubleSpinBox(Item)
        self.propertyValueFloatZ.setObjectName(u"propertyValueFloatZ")
        sizePolicy.setHeightForWidth(self.propertyValueFloatZ.sizePolicy().hasHeightForWidth())
        self.propertyValueFloatZ.setSizePolicy(sizePolicy)
        self.propertyValueFloatZ.setMinimumSize(QSize(0, 0))
        self.propertyValueFloatZ.setDecimals(5)
        self.propertyValueFloatZ.setMaximum(1000000.000000000000000)

        self.horizontalLayout.addWidget(self.propertyValueFloatZ)


        self.retranslateUi(Item)

        QMetaObject.connectSlotsByName(Item)
    # setupUi

    def retranslateUi(self, Item):
        Item.setWindowTitle(QCoreApplication.translate("Item", u"Form", None))
        self.propertyLabel.setText(QCoreApplication.translate("Item", u"property_name", None))
        self.label_2.setText(QCoreApplication.translate("Item", u":", None))
    # retranslateUi

