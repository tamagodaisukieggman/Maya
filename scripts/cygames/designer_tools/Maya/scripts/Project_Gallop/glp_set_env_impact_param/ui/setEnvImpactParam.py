# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\tech-designer\Maya\scripts\Project_Gallop\glp_set_env_impact_param\ui\setEnvImpactParam.ui'
#
# Created: Thu Jan 14 17:40:55 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

from PySide2 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.targetObjectListView = QtWidgets.QListView(self.groupBox_2)
        self.targetObjectListView.setObjectName("targetObjectListView")
        self.verticalLayout_3.addWidget(self.targetObjectListView)
        self.addTargetButton = QtWidgets.QPushButton(self.groupBox_2)
        self.addTargetButton.setObjectName("addTargetButton")
        self.verticalLayout_3.addWidget(self.addTargetButton)
        self.deleteTargetButton = QtWidgets.QPushButton(self.groupBox_2)
        self.deleteTargetButton.setObjectName("deleteTargetButton")
        self.verticalLayout_3.addWidget(self.deleteTargetButton)
        self.allDeleteTargetButton = QtWidgets.QPushButton(self.groupBox_2)
        self.allDeleteTargetButton.setObjectName("allDeleteTargetButton")
        self.verticalLayout_3.addWidget(self.allDeleteTargetButton)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.impactParamSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.impactParamSpinBox.setMaximum(1.0)
        self.impactParamSpinBox.setSingleStep(0.01)
        self.impactParamSpinBox.setProperty("value", 1.0)
        self.impactParamSpinBox.setObjectName("impactParamSpinBox")
        self.horizontalLayout.addWidget(self.impactParamSpinBox)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.execButton = QtWidgets.QPushButton(self.centralwidget)
        self.execButton.setObjectName("execButton")
        self.verticalLayout.addWidget(self.execButton)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "草揺れ影響度一括設定ツール", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "草揺れの影響度をUV3のUに一括で入れるためのツールです。\n"
"UV3のVには一律で「0」が入ります。\n"
"詳細に設定したい場合はこのツールで一括で設定後にUVを編集してください。\n"
"なお、元々UV2(Lightmapで利用されていることが多い)がある場合は編集せずに利用されます。", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MainWindow", "対象オブジェクト一覧", None, -1))
        self.addTargetButton.setText(QtWidgets.QApplication.translate("MainWindow", "選択したオブジェクトを一覧に追加", None, -1))
        self.deleteTargetButton.setText(QtWidgets.QApplication.translate("MainWindow", "選択したオブジェクトを一覧から削除", None, -1))
        self.allDeleteTargetButton.setText(QtWidgets.QApplication.translate("MainWindow", "全てのオブジェクトを一覧から削除", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "パラメーター", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "影響度(uv3.u)", None, -1))
        self.execButton.setText(QtWidgets.QApplication.translate("MainWindow", "実行", None, -1))

