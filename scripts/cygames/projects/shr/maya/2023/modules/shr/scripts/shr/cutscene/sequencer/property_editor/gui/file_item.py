# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'file_item.ui'
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
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.propertyLabel = QLabel(Item)
        self.propertyLabel.setObjectName(u"propertyLabel")

        self.horizontalLayout_2.addWidget(self.propertyLabel)

        self.label_2 = QLabel(Item)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.propertyValuePath = QLineEdit(Item)
        self.propertyValuePath.setObjectName(u"propertyValuePath")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.propertyValuePath.sizePolicy().hasHeightForWidth())
        self.propertyValuePath.setSizePolicy(sizePolicy)
        self.propertyValuePath.setReadOnly(True)

        self.horizontalLayout.addWidget(self.propertyValuePath)

        self.propertyFileOpen = QPushButton(Item)
        self.propertyFileOpen.setObjectName(u"propertyFileOpen")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.propertyFileOpen.sizePolicy().hasHeightForWidth())
        self.propertyFileOpen.setSizePolicy(sizePolicy1)
        self.propertyFileOpen.setMinimumSize(QSize(35, 35))
        self.propertyFileOpen.setMaximumSize(QSize(40, 16777215))
        self.propertyFileOpen.setIconSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.propertyFileOpen)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Item)

        QMetaObject.connectSlotsByName(Item)
    # setupUi

    def retranslateUi(self, Item):
        Item.setWindowTitle(QCoreApplication.translate("Item", u"Form", None))
        self.propertyLabel.setText(QCoreApplication.translate("Item", u"property_name", None))
        self.label_2.setText(QCoreApplication.translate("Item", u":", None))
        self.propertyValuePath.setText(QCoreApplication.translate("Item", u"Z:\\mtk\\tools\\maya\\2022\\modules\\mtk\\scripts\\mtk\\cutscene\\sequencer\\property_editor", None))
        self.propertyFileOpen.setText(QCoreApplication.translate("Item", u"Open", None))
    # retranslateUi

