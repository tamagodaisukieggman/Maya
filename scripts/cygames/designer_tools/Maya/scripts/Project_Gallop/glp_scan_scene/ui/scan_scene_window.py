# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\tech-designer\Maya\scripts\Project_Gallop\glp_scan_scene\ui\scan_scene_window.ui'
#
# Created: Thu Jul 16 14:37:25 2020
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtWidgets

try:
    # Maya2022-
    from builtins import object
except Exception:
    pass


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 756)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.centralwidgetLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.centralwidgetLayout.setObjectName("centralwidgetLayout")
        self.fileScanGroupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.fileScanGroupBox.setObjectName("fileScanGroupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.fileScanGroupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.fileScanDescriptionGroupBox = QtWidgets.QGroupBox(self.fileScanGroupBox)
        self.fileScanDescriptionGroupBox.setObjectName("fileScanDescriptionGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.fileScanDescriptionGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.fileScanDescriptionLabel = QtWidgets.QLabel(self.fileScanDescriptionGroupBox)
        self.fileScanDescriptionLabel.setObjectName("fileScanDescriptionLabel")
        self.verticalLayout_2.addWidget(self.fileScanDescriptionLabel)
        self.verticalLayout_5.addWidget(self.fileScanDescriptionGroupBox)
        self.targetDirListGroupBox = QtWidgets.QGroupBox(self.fileScanGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.targetDirListGroupBox.sizePolicy().hasHeightForWidth())
        self.targetDirListGroupBox.setSizePolicy(sizePolicy)
        self.targetDirListGroupBox.setAutoFillBackground(False)
        self.targetDirListGroupBox.setFlat(False)
        self.targetDirListGroupBox.setCheckable(False)
        self.targetDirListGroupBox.setObjectName("targetDirListGroupBox")
        self.randObjPlacementLayout = QtWidgets.QVBoxLayout(self.targetDirListGroupBox)
        self.randObjPlacementLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.randObjPlacementLayout.setObjectName("randObjPlacementLayout")
        self.setTargetDirListButton = QtWidgets.QPushButton(self.targetDirListGroupBox)
        self.setTargetDirListButton.setObjectName("setTargetDirListButton")
        self.randObjPlacementLayout.addWidget(self.setTargetDirListButton)
        self.targetDirListScrollArea = QtWidgets.QScrollArea(self.targetDirListGroupBox)
        self.targetDirListScrollArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.targetDirListScrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.targetDirListScrollArea.setLineWidth(1)
        self.targetDirListScrollArea.setWidgetResizable(True)
        self.targetDirListScrollArea.setObjectName("targetDirListScrollArea")
        self.targetDirListWidget = QtWidgets.QWidget()
        self.targetDirListWidget.setGeometry(QtCore.QRect(0, 0, 540, 190))
        self.targetDirListWidget.setObjectName("targetDirListWidget")
        self.targetDirListLayout = QtWidgets.QVBoxLayout(self.targetDirListWidget)
        self.targetDirListLayout.setObjectName("targetDirListLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.targetDirListLayout.addItem(spacerItem)
        self.targetDirListScrollArea.setWidget(self.targetDirListWidget)
        self.randObjPlacementLayout.addWidget(self.targetDirListScrollArea)
        self.verticalLayout_5.addWidget(self.targetDirListGroupBox)
        self.optionGroupBox = QtWidgets.QGroupBox(self.fileScanGroupBox)
        self.optionGroupBox.setObjectName("optionGroupBox")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.optionGroupBox)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.logExportSettingGroupBox = QtWidgets.QGroupBox(self.optionGroupBox)
        self.logExportSettingGroupBox.setObjectName("logExportSettingGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.logExportSettingGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.isLogExportCheckBox = QtWidgets.QCheckBox(self.logExportSettingGroupBox)
        self.isLogExportCheckBox.setChecked(True)
        self.isLogExportCheckBox.setObjectName("isLogExportCheckBox")
        self.verticalLayout.addWidget(self.isLogExportCheckBox)
        self.logExportTargetDirLayout = QtWidgets.QHBoxLayout()
        self.logExportTargetDirLayout.setObjectName("logExportTargetDirLayout")
        self.logExportTargetDirLabel = QtWidgets.QLabel(self.logExportSettingGroupBox)
        self.logExportTargetDirLabel.setObjectName("logExportTargetDirLabel")
        self.logExportTargetDirLayout.addWidget(self.logExportTargetDirLabel)
        self.logExportTargetDirEdit = QtWidgets.QLineEdit(self.logExportSettingGroupBox)
        self.logExportTargetDirEdit.setEnabled(False)
        self.logExportTargetDirEdit.setInputMask("")
        self.logExportTargetDirEdit.setReadOnly(False)
        self.logExportTargetDirEdit.setObjectName("logExportTargetDirEdit")
        self.logExportTargetDirLayout.addWidget(self.logExportTargetDirEdit)
        self.setLogExportTargetDirButton = QtWidgets.QPushButton(self.logExportSettingGroupBox)
        self.setLogExportTargetDirButton.setObjectName("setLogExportTargetDirButton")
        self.logExportTargetDirLayout.addWidget(self.setLogExportTargetDirButton)
        self.logExportTargetDirLayout.setStretch(1, 5)
        self.verticalLayout.addLayout(self.logExportTargetDirLayout)
        self.verticalLayout_9.addWidget(self.logExportSettingGroupBox)
        self.verticalLayout_5.addWidget(self.optionGroupBox)
        self.execButtonBoxLayout = QtWidgets.QHBoxLayout()
        self.execButtonBoxLayout.setObjectName("execButtonBoxLayout")
        self.okButton = QtWidgets.QPushButton(self.fileScanGroupBox)
        self.okButton.setObjectName("okButton")
        self.execButtonBoxLayout.addWidget(self.okButton)
        self.verticalLayout_5.addLayout(self.execButtonBoxLayout)
        self.centralwidgetLayout.addWidget(self.fileScanGroupBox)
        self.referenceRepairGroupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.referenceRepairGroupBox.setEnabled(True)
        self.referenceRepairGroupBox.setObjectName("referenceRepairGroupBox")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.referenceRepairGroupBox)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.referenceRepairDescriptionGroupBox = QtWidgets.QGroupBox(self.referenceRepairGroupBox)
        self.referenceRepairDescriptionGroupBox.setObjectName("referenceRepairDescriptionGroupBox")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.referenceRepairDescriptionGroupBox)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.referenceRepairDescriptionLabel = QtWidgets.QLabel(self.referenceRepairDescriptionGroupBox)
        self.referenceRepairDescriptionLabel.setObjectName("referenceRepairDescriptionLabel")
        self.verticalLayout_8.addWidget(self.referenceRepairDescriptionLabel)
        self.verticalLayout_7.addWidget(self.referenceRepairDescriptionGroupBox)
        self.referenceRepairButton = QtWidgets.QPushButton(self.referenceRepairGroupBox)
        self.referenceRepairButton.setEnabled(False)
        self.referenceRepairButton.setObjectName("referenceRepairButton")
        self.verticalLayout_7.addWidget(self.referenceRepairButton)
        self.centralwidgetLayout.addWidget(self.referenceRepairGroupBox)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "ファイルスキャン一括実行ツール", None, -1))
        self.fileScanGroupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "ファイルスキャン一括実行", None, -1))
        self.fileScanDescriptionGroupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "使い方", None, -1))
        self.fileScanDescriptionLabel.setText(QtWidgets.QApplication.translate("MainWindow", "①ファイルスキャンを実行するフォルダのリスト内の\n"
"②ファイルスキャンするフォルダを選択して追加ボタンを押します。\n"
"ファイルダイアログが開くので、フォルダを選択して選択を押すとリストに追加されます。\n"
"③ログを出力するか選択し、出力する場合\n"
"④のログを出力する対象のフォルダを\n"
"⑤セットボタンから選択します。\n"
"準備が終わったら、\n"
"⑥実行ボタンを押してください。\n"
"\n"
"一度実行すると、コマンドプロンプトが何度も立ち上がるので、作業がしにくくなりますのでご注意ください。", None, -1))
        self.targetDirListGroupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "①ファイルスキャンを実行するフォルダのリスト", None, -1))
        self.setTargetDirListButton.setText(QtWidgets.QApplication.translate("MainWindow", "②ファイルスキャンするフォルダを選択して追加する", None, -1))
        self.optionGroupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "オプション", None, -1))
        self.logExportSettingGroupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "ログ出力設定", None, -1))
        self.isLogExportCheckBox.setText(QtWidgets.QApplication.translate("MainWindow", "④ログを出力する", None, -1))
        self.logExportTargetDirLabel.setText(QtWidgets.QApplication.translate("MainWindow", "⑤ログを出力する対象のフォルダ", None, -1))
        self.logExportTargetDirEdit.setText(QtWidgets.QApplication.translate("MainWindow", "D:\\", None, -1))
        self.setLogExportTargetDirButton.setText(QtWidgets.QApplication.translate("MainWindow", "セット", None, -1))
        self.okButton.setText(QtWidgets.QApplication.translate("MainWindow", "⑥ファイルスキャンを実行", None, -1))
        self.referenceRepairGroupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "リファレンス修復一括実行", None, -1))
        self.referenceRepairDescriptionGroupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "使い方", None, -1))
        self.referenceRepairDescriptionLabel.setText(QtWidgets.QApplication.translate("MainWindow", "⑥ファイルスキャンを実行後にスキャン対象がある場合に使えるようになります。\n"
"\n"
"⑦リファレンス修復を実行ボタンを押すと、\n"
"⑥ファイルスキャンを実行した結果スキャンが実行された対象に対してレファレンス修復を行います。", None, -1))
        self.referenceRepairButton.setText(QtWidgets.QApplication.translate("MainWindow", "⑦リファレンス修復を実行", None, -1))

