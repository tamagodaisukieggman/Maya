# !/usr/bin/env python2.7
# -*- coding: utf-8 -*-
u"""
    BEGIN__CYGAMES_MENU
    label=Cygames Maya Renamer
    command=main()
    order=2000
    author=Natsuko Kinoshita
    version=2021.11.16
    END__CYGAMES_MENU
"""
u"""
このツールはMayaのシーン内外のリネーマーです。
プロジェクトフォルダ内のファイルやテクスチャー、フォルダ、Mayaのシーン内のオブジェクトのリネームします。
Undoできませんので、元データはSVNなどでバージョン管理するか、複製を作ってから実行することを強くお勧めします。
Created: 2018/02/20
Last Modified: 2021/11/16
"""

try:
    # Maya2015-2016
    from PySide import QtGui, QtCore
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    # Maya2017-
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

import maya.cmds as cmds

import os
import functools
import tempfile
import sys
import time
import re
import CyMayaRenamerCore as renamer

g_tool_name = "CygamesMayaRenamer"
g_version = "2021.11.16"
g_curMayaVersion = 2019 # 一旦2019で初期化

def getMayaMainWindow():
    u"""
    Mayaのメインウィンドウオブジェクトを返します。　なければNoneを返します。
    :return　QtGui.QWidget: Mayaのメインウィンドウ、もしくはNone
    """
    try:
        import maya.OpenMayaUI as omui
        try:
            from shiboken import wrapInstance
        except:
            from shiboken2 import wrapInstance
        mainWindowPtr = omui.MQtUtil.mainWindow() # Mayaのメインウィンドウへのポインター
        try:
            winPointer = wrapInstance(long(mainWindowPtr), QWidget) # ポインターをPythonのQWidgetオブジェクトに変換
        except:
            # Maya 2022-
            winPointer = wrapInstance(int(mainWindowPtr), QWidget) # ポインターをPythonのQWidgetオブジェクトに変換
        return winPointer
    except:
        return None

class RenamerWindow(QMainWindow):
    u"""
    ツールのメインウィンドウ
    """
    def __init__(self, parent=None):
        super(RenamerWindow, self).__init__(parent)
        self.setWindowTitle(g_tool_name + " " + g_version)
        self.setObjectName(g_tool_name)
        self.uiSettingPath = os.path.expanduser("~\\Documents\\maya\\scripts\\cygamesMayaRenamerSetting.ini")
        self.createActions()
        self.createMenus()
        # self.resize(500, 285)
        self.renamerCentralWidget = CentralWidget()
        self.setCentralWidget(self.renamerCentralWidget)

        if parent:
            # Default Window location
            self.setGeometry(
                parent.x() + parent.width() / 2 - self.width() / 2,
                parent.y() + parent.height() / 2 - self.height() / 2,
                self.width(),
                self.height()
            )
        self.loadSetting() # Restore UI state

        try:
            import maya.cmds as cmds
        except:
            self.lblError.setVisible(True)
            self.lblError.setText(u"：Mayaのシーン内のリネームをする場合、このツールをMayaから実行してください。")
            return

    def createActions(self):
        self.showManualAct = QAction(u"マニュアル", self,
                statusTip=u"マニュアルページを開きます",
                triggered=self.showManual)

        self.showAboutAct = QAction("&About", self,
                statusTip=u"このツールについて",
                triggered=self.showAbout)

    def createMenus(self):
        self.helpMenu = self.menuBar().addMenu("Help")
        self.helpMenu.addAction(self.showAboutAct)
        self.helpMenu.addAction(self.showManualAct)

    def loadSetting(self):
        u"""
        前回のUIの状態を読み込みます。
        """
        setting = QSettings(self.uiSettingPath, QSettings.IniFormat)
        # print(setting.fileName())  # setting.ini file location
        if setting:
            restoreUiState(self, setting)
            self.restoreState(setting.value("windowState"))
            self.restoreGeometry(setting.value("geometry"))

    def closeEvent(self, event):
        u"""
        ウィンドウをクローズする時にUIの状態を保存します。
        :param event:
        """
        setting = QSettings(self.uiSettingPath, QSettings.IniFormat)
        print(setting.fileName())  # setting.ini file location
        if setting:
            saveUiState(self, setting)
            setting.setValue("windowState", self.saveState())
            setting.setValue("geometry", self.saveGeometry())

    def showAbout(self):
        QMessageBox.about(self, "About Cygames Maya Renamer",
                u"<b>Cygames Maya Renamer</b> はMayaのシーンやプロジェクト内のファイルをリネームするツールです。　"
                u"シーンを開かなくてもフォルダ一括モードを使えば、指定したフォルダ配下のMayaシーン内のリネームもできます。　"
                u"問題や要望、質問はテクニカルアーティストチームまでお願いいたします。　"
                u"Maya 2015, 2016, 2017, 2018で動作確認済みです。")

    def showManual(self):
        import webbrowser
        webbrowser.open(u"https://wisdom.cygames.jp/display/designersmanual/Maya%3A+General"
                        u"#Maya:General-CyMayaRenamer:一括リネーム")

class DirFileWidget(QWidget):
    def __init__(self, lblTxt="", btnTxt=u"選択", defaultPath="", type="dir", toolTip=""):
        u"""
        フォルダ選択ウィジェット
        :param lblTxt: string. パスのQLineEditの前のラベル
        :param btnTxt: string. フォルダ選択ボタンのラベル
        :param defaultPath: string. デフォルトでQLineEditに表示するパス
        :param type: string. file or dir expected
        :param toolTip: string. マウスホバーした時に表示したい説明文
        """
        super(DirFileWidget, self).__init__()
        if btnTxt is None:
            btnTxt = u"選択"
        self.rowDirPath = QHBoxLayout()
        lblFolder = QLabel(lblTxt)
        self.dirPath = QLineEdit()
        self.dirPath.setText(defaultPath)
        if toolTip:
            self.dirPath.setToolTip(toolTip)
        btnSelectDir = QPushButton(btnTxt)
        if type == "file":
            btnSelectDir.clicked.connect(self.btnSelectFileOnClick)
        else:
            btnSelectDir.clicked.connect(self.btnSelectDirOnClick)
        self.rowDirPath.addWidget(lblFolder)
        self.rowDirPath.addWidget(self.dirPath)
        self.rowDirPath.addWidget(btnSelectDir)
        self.setLayout(self.rowDirPath)

    def getPath(self):
        u"""
        このウィジェットで選択されたフォルダへのパスを返します。
        :return: string. The selected folder path.
        """
        if self.isVisible() and self.isEnabled():
            return self.dirPath.text()
        else:
            return ""

    def btnSelectDirOnClick(self):
        u"""
        このウィジェットのフォルダ「選択」ボタンが押された時のアクション。
        フォルダ選択ダイアログを表示し、フォルダが選ばれたらパスを表示します。
        """
        import os
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        if os.path.exists(self.dirPath.text()):
            d = QFileDialog.getExistingDirectory(self, "Open Directory", self.dirPath.text(), flags)
        else:
            d = QFileDialog.getExistingDirectory(self, "Open Directory", os.getcwd(), flags)
        if d:
            self.dirPath.setText(d)

    def btnSelectFileOnClick(self):
        u"""
        このウィジェットのフォルダ「選択」ボタンが押された時のアクション。
        ファイル選択ダイアログを表示し、ファイルが選ばれたらパスを表示します。
        """
        import os
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        d = QFileDialog.getOpenFileName(self, "Open CSV", os.getcwd(), u"ファイル(*.csv)")
        if d[0]:
            self.dirPath.setText(d[0])

class CentralWidget(QWidget):
    u"""
    RenamerWindowの中に入れるリネーマーのCentral(メイン)ウィジェット
    """
    beforeAfterDict = {} # key: 検索する文字列. value: リネーム後の文字列。　csvで複数指定する場合があるのでディクショナリ。
    isDryRun = False # Trueだとリネーム置換のテスト（リネームしない）

    def __init__(self):
        super(CentralWidget, self).__init__()

        # メインのレイアウト
        self.vLayout = QVBoxLayout()

        self.lblError = QLabel()
        self.lblError.setStyleSheet("color:red")
        self.lblError.setVisible(False)

        # メインのレイアウトに入れるUIパーツ作成
        self.InputMode = QGroupBox(u"入力モード")
        self.radioChangeInput = QRadioButton(u"記述指定")
        self.radioChangeInput.setToolTip(u"「検索する文字列」と「リネーム後の文字列」の入力でリネームします。"
                                         u"（csvで複数指定しない）")
        self.radioChangeInput.setChecked(True) # これをTrueにするなら読み込み時のフォームの状態チェックを要確認。
        self.radioChangeCSV = QRadioButton(u"csv指定")
        radioBoxInput = QHBoxLayout()
        radioBoxInput.addWidget(self.radioChangeCSV)
        radioBoxInput.addWidget(self.radioChangeInput)
        self.radioChangeCSV.toggled.connect(self.radioInputToggled)
        self.InputMode.setLayout(radioBoxInput)

        self.rowSearchTxt = QHBoxLayout()
        self.lblSearchTxt = QLabel(u"検索する文字列")
        self.fromText = QLineEdit()
        self.rowSearchTxt.addWidget(self.lblSearchTxt)
        self.rowSearchTxt.addWidget(self.fromText)

        self.rowReplaceTxt = QHBoxLayout()
        self.lblReplaceTxt = QLabel(u"リネーム後の文字列")
        self.toText = QLineEdit()
        self.rowReplaceTxt.addWidget(self.lblReplaceTxt)
        self.rowReplaceTxt.addWidget(self.toText)

        self.rowIgnoreText = QHBoxLayout()
        self.lblIgnoreText = QLabel(u"無視するフォルダ")
        self.ignoreText = QLineEdit()
        self.ignoreText.setToolTip(u"「old」フォルダなどリネームの対象外にしたいフォルダ名")
        self.rowIgnoreText.addWidget(self.lblIgnoreText)
        self.rowIgnoreText.addWidget(self.ignoreText)

        rowChkRegex = QHBoxLayout()
        self.chkRegex = QCheckBox(u"正規表現")
        self.chkRegex.setToolTip(u"「検索する文字列」を正規表現として扱い、リネームを行います。")
        rowChkRegex.addWidget(self.chkRegex)
        rowChkRegex.setAlignment(Qt.AlignRight)
        self.csvDirWidget = DirFileWidget(u"CSVパス", None, "", "file")
        lblCsv = QLabel(u"検索とリネームの一括設定")

        self.rowReplaceMode = QGroupBox(u"リネームモード")
        self.radioCurrentScene = QRadioButton(u"現在のScene")
        self.radioCurrentScene.setToolTip(u"現在Mayaで開いているシーン内のリネームをします。\n" + 
                    u"フォルダ名やシーン名など開いているとリネームできないものは多いので「フォルダ一括」の方がお勧めです。")
        self.radioBatchFolder = QRadioButton(u"フォルダ一括")
        self.radioBatchFolder.setToolTip(u"選択したルートフォルダ配下のMayaシーンをすべて開きリネームます。 "
                                         u"選択したルートフォルダ配下のファイルすべてが対象となります。")
        self.radioBatchFolder.setChecked(True)
        radioBox = QHBoxLayout()
        radioBox.addWidget(self.radioCurrentScene)
        radioBox.addWidget(self.radioBatchFolder)
        self.radioBatchFolder.toggled.connect(self.radioBatchFolderToggled)
        self.rowReplaceMode.setLayout(radioBox)

        self.rootDirWidget = DirFileWidget(u"一括するルートフォルダ", None, "", "dir")

        lblOptions = QLabel(u"リネームしたい項目")
        lblOptions.setMinimumHeight(30)

        self.optionGrid_Files = QGridLayout() # ファイル
        self.optionGrid_InScene = QGridLayout() # Mayaシーン内の項目
        # リネームしたい項目
        self.chkFolderName = QCheckBox(u"フォルダ")
        self.chkMayaFileName = QCheckBox(u"Mayaファイル")
        self.chkTextureName = QCheckBox(u"テクスチャーファイル名")
        self.chkMatFolderPath = QCheckBox(u"マテリアルのテクスチャーパスのフォルダ名")
        self.chkMatTextureName = QCheckBox(u"マテリアルのテクスチャーパスのテクスチャーファイル名")
        self.chkMaterialName = QCheckBox(u"マテリアル名")
        self.chkJointName = QCheckBox(u"ジョイント")
        self.chkLocatorName = QCheckBox(u"ロケーター")
        self.chkMeshName = QCheckBox(u"メッシュ")
        self.chkGroupName = QCheckBox(u"グループ") # shapeのないtransformでchildrenがあるものをグループとみなす
        self.chkRefPathFolderName = QCheckBox(u"リファレンスパスのフォルダ名")
        self.chkRefPathFileName = QCheckBox(u"リファレンスパスのファイル名")

        # Mayaファイルオプション
        self.boxChkMayaOption = QGroupBox("option")
        self.chkMayaFileName.toggled.connect(self.onToggleMayaFile)
        self.chkBatchMa = QCheckBox(".ma")
        self.chkBatchMb = QCheckBox(".mb")
        self.chkBatchMa.toggled.connect(functools.partial(self.onToggleMayaOption, self.chkBatchMa))
        self.chkBatchMb.toggled.connect(functools.partial(self.onToggleMayaOption, self.chkBatchMb))
        hlayoutChkMayaOption = QHBoxLayout()
        hlayoutChkMayaOption.addWidget(self.chkBatchMa)
        hlayoutChkMayaOption.addWidget(self.chkBatchMb)
        self.boxChkMayaOption.setLayout(hlayoutChkMayaOption)
        hrowChkMaya = QHBoxLayout()
        self.chkFolderName.setMinimumWidth(350)
        hrowChkMaya.addWidget(self.chkMayaFileName)
        hrowChkMaya.addWidget(self.boxChkMayaOption)

        # --------------------------------------------
        # シーン外
        self.boxFileOptions = QGroupBox(u"外ファイル")
        self.optionGrid_Files.addWidget(self.chkFolderName, 1, 1)  # widget, row, col
        self.optionGrid_Files.addLayout(hrowChkMaya, 2, 1)
        self.optionGrid_Files.addWidget(self.chkTextureName, 3, 1)
        self.boxFileOptions.setLayout(self.optionGrid_Files)
        # シーン内
        self.boxMayaSceneOptions = QGroupBox(u"Mayaシーン内")
        self.optionGrid_InScene.addWidget(self.chkMatFolderPath, 1, 1)
        self.optionGrid_InScene.addWidget(self.chkMatTextureName, 2, 1)
        self.optionGrid_InScene.addWidget(self.chkMaterialName, 3, 1)
        self.optionGrid_InScene.addWidget(self.chkJointName, 4, 1)
        self.optionGrid_InScene.addWidget(self.chkLocatorName, 5, 1)
        self.optionGrid_InScene.addWidget(self.chkMeshName, 6, 1)
        self.optionGrid_InScene.addWidget(self.chkGroupName, 7, 1)
        self.optionGrid_InScene.addWidget(self.chkRefPathFolderName, 8, 1)
        self.optionGrid_InScene.addWidget(self.chkRefPathFileName, 9, 1)
        self.boxMayaSceneOptions.setLayout(self.optionGrid_InScene)

        btnReplace = QPushButton(u"リネーム")
        btnReplace.clicked.connect(self.onBtnReplaceClick)

        btnTestReplace = QPushButton(u"リネームテスト（リネームしません）")
        btnTestReplace.clicked.connect(self.onBtnTestReplaceClick)

        lblNote01 = QLabel(u"* 対象テクスチャータイプ: " + str(renamer.g_supportedTextureTypes))

        # メインのレイアウトにUIパーツを配置
        self.vLayout.addWidget(self.lblError)
        self.vLayout.addWidget(self.InputMode)
        self.vLayout.addLayout(self.rowSearchTxt)
        self.vLayout.addLayout(self.rowReplaceTxt)
        self.vLayout.addLayout(self.rowIgnoreText)
        self.vLayout.addWidget(self.csvDirWidget)
        self.vLayout.addLayout(rowChkRegex)
        self.vLayout.addWidget(lblCsv)
        self.vLayout.addWidget(self.rowReplaceMode)
        self.vLayout.addWidget(self.rootDirWidget) # フォルダ一括ラジオボタンONで表示
        self.vLayout.addWidget(lblOptions)
        self.vLayout.addWidget(self.boxFileOptions)
        self.vLayout.addWidget(self.boxMayaSceneOptions)
        self.vLayout.addSpacing(10)
        self.vLayout.addWidget(btnReplace)
        self.vLayout.addSpacing(10)
        self.vLayout.addWidget(btnTestReplace)
        self.vLayout.addWidget(lblNote01)
        self.vLayout.setAlignment(Qt.AlignTop)
        self.setMinimumWidth(450)
        self.setLayout(self.vLayout)

        self.setupUi()


    ####### Begin UI 周り関数 #######
    def setupUi(self):
        u"""
        UI周り初期設定
        """
        self.radioBatchFolderToggled(self.radioBatchFolder.isChecked())  # フォルダ選択ウィジェットの表示
        self.radioInputToggled(self.radioChangeCSV.isChecked()) # フォルダ選択ウィジェットの表示
        self.onToggleMayaOption(self.chkBatchMa) # 少なくともどっちかチェック


    def radioBatchFolderToggled(self, state):
        u"""
        「フォルダ一括」モードのラジオボタンがチェックされた時のアクション。
        「フォルダ一括」モードの時のみ使えるUIを有効にしたり無効にしたりします。
        :param state: boolean.「フォルダ一括」モードがチェックされていたらTrue.
        """
        if state: # フォルダ一括
            self.chkFolderName.setDisabled(False)
            self.rootDirWidget.setVisible(True) # 「一括するルートフォルダ」UI表示
            self.chkMayaFileName.setChecked(True)
            self.chkMayaFileName.setDisabled(False)
            self.ignoreText.setDisabled(False)
            self.chkMatFolderPath.setDisabled(False)
        else: # 現在のScene
            self.chkFolderName.setDisabled(True)
            self.rootDirWidget.setVisible(False)
            self.chkMayaFileName.setChecked(False)
            self.chkMayaFileName.setDisabled(True)
            self.boxMayaSceneOptions.setDisabled(False)
            self.ignoreText.setDisabled(True)
            self.chkMatFolderPath.setDisabled(True)

    def radioInputToggled(self, state):
        u"""
        入力モードのラジオボタン
        :param state: boolean.「csv指定」モードがチェックされていたらTrue.
        :return:
        """
        if state: # csv指定
            self.csvDirWidget.setDisabled(False)
            self.lblSearchTxt.setDisabled(True) # 検索する文字列
            self.fromText.setDisabled(True) # 検索する文字列
            self.lblReplaceTxt.setDisabled(True) # リネーム後の文字列
            self.toText.setDisabled(True) # リネーム後の文字列
        else: # 記述指定
            self.csvDirWidget.setDisabled(True)
            self.lblSearchTxt.setDisabled(False) # 検索する文字列
            self.fromText.setDisabled(False)
            self.lblReplaceTxt.setDisabled(False) # リネーム後の文字列
            self.toText.setDisabled(False)

    def onToggleMayaOption(self, caller, *args):
        u"""
        「Mayaファイル」にチェックを入れている時、optionの「.ma」「.mb」どちらかはチェックが必ず入るようにする。
        :param args:
        :return:
        """
        if self.chkMayaFileName.isEnabled() and self.chkMayaFileName.isChecked():
            if self.chkBatchMa.isChecked() == False and self.chkBatchMb.isChecked() == False:
                caller.setChecked(True)
                print(u"「Mayaファイル」にチェックを入れている場合、「.ma」か「.mb」どちらかは必須です。")

    def onToggleMayaFile(self, *args):
        u"""
        「Mayaファイル」のチェックボックスのtoggleで呼ばれる。
        """
        isMafaFileChecked = args[0]
        if isMafaFileChecked:
            self.boxChkMayaOption.setDisabled(False)
            self.boxMayaSceneOptions.setDisabled(False)
            if (self.chkBatchMa.isEnabled() == True and self.chkBatchMa.isChecked() == False) and \
                    (self.chkBatchMb.isEnabled() == True and self.chkBatchMb.isChecked() == False):
                self.chkBatchMa.setChecked(True) # 少なくとも.maか.mbどちらかはチェックする
        else:
            self.boxChkMayaOption.setDisabled(True)
            self.boxMayaSceneOptions.setDisabled(True)

    def isSceneItemChecked(self):
        u"""
        リネームの対象のチェックボックスで、「シーン内」のアイテムが一つでも選択されているかどうか。
        :return: シーン内アイテムが一つでも選択されていたらTrue. そうでなければFalse.
        """
        for child in self.boxMayaSceneOptions.children():
            if isinstance(child, QCheckBox):
                if child.isEnabled() and child.isChecked():
                    return True
        return False

    def preValidation(self, isCurrentScene):
        """
        リネーム実行前のフォームチェック
        ここで「検索する文字列」「リネーム後の文字列」のディクショナリ「self.beforeAfterDict」も作っている。
        :param isCurrentScene:
        :return:
        """
        if isCurrentScene:
            if not cmds.file(q=True, sn=True):
                self.lblError.setVisible(True)
                self.lblError.setText(u"シーンを開いてから実効してください")
                return False
        if self.radioChangeCSV.isChecked():
            batchCsvPath = self.csvDirWidget.getPath().strip()
            if batchCsvPath:
                if os.path.exists(batchCsvPath) == False:
                    self.lblError.setVisible(True)
                    self.lblError.setText(u"CSVのパスが存在しません：" + batchCsvPath)
                    return False
                self.beforeAfterDict = renamer.readBeforeAfterCSV(batchCsvPath)
            else:
                self.lblError.setVisible(True)
                self.lblError.setText(u"CSVファイルを選択してください。")
                return False
        else:
            if len(self.fromText.text()) == 0:
                self.lblError.setVisible(True)
                self.lblError.setText(u"変更前の文字列の指定がありません。")
                return False
            self.beforeAfterDict = {self.fromText.text().strip(): self.toText.text().strip()}


        #####  現在のScene フォルダ一括 共通  #####
        if self.radioChangeInput.isChecked():
            if len(self.fromText.text().strip()) == 0:
                self.lblError.setVisible(True)
                self.lblError.setText(u"検索する文字列を指定してください")
                return False
            elif self.chkRegex.isEnabled() and not self.chkRegex.isChecked():
                chars = self.toText.text().strip()
                for char in chars:
                    if char in renamer.g_invalidChars:
                        renamer.writeLog(u"次の文字はリネームに使えません: " + char)
                        return False

        if len(next(iter(self.beforeAfterDict))) == 0:
            # リネーム後の文字列が空だったら再確認（文字列を取りたい時に対応）　csvで指定の時は全部まで面倒見ません。
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u"確認")
            msgBox.setText(u"リネーム後の文字列が指定されていません。　文字列削除になりますがよろしいですか？")
            msgBox.setInformativeText(u"削除後の名前が空になる時はリネームは行われません。")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            ret = msgBox.exec_()
            if ret == QMessageBox.Cancel:
                return False

        isSceneExists = cmds.file(q=True, exists=True, pmt=False)
        isSceneUnsaved = cmds.file(q=True, modified=True, pmt=False)
        if isSceneExists and isSceneUnsaved:
            # Need to save
            self.lblError.setVisible(True)
            self.lblError.setText(u"現在のシーンを保存するか空の新規シーンを開いてください")
            return False

        if not isCurrentScene:
            batchRootPath = self.rootDirWidget.getPath()
            if not batchRootPath:
                self.lblError.setVisible(True)
                self.lblError.setText(u"一括処理するフォルダを選択してください")
                return False
            else:
                if os.path.exists(batchRootPath) == False:
                    self.lblError.setVisible(True)
                    self.lblError.setText(u"一括フォルダのパスが存在しません：" + batchRootPath)
                    return False
        return True

    ####### End UI 周り関数 #######

    def onBtnTestReplaceClick(self):
        self.isDryRun = True
        self.onReplace()

    def onBtnReplaceClick(self):
        self.isDryRun = False
        self.onReplace()

    def onReplace(self):
        u"""
        リネーム開始。　「リネーム」ボタンを押した時のアクション。
        """
        # ログファイル書き出し準備
        if sys.version_info.major == 2:
            renamer.g_logFile = tempfile.NamedTemporaryFile(delete=False, mode="a")
        else:
            # Python3より上とみなす
            renamer.g_logFile = tempfile.NamedTemporaryFile(delete=False, encoding="utf-8_sig", mode="a")
        startTime = 0
        endTime = 0
        numProcessedScenes = 0
        numUnOpendScenes = 0

        # Reset Error messages
        self.lblError.setVisible(False)
        self.lblError.setText("")

        # Validation
        isCurrentScene = self.radioCurrentScene.isEnabled() and self.radioCurrentScene.isChecked()
        isFormOK = self.preValidation(isCurrentScene)
        if not isFormOK:
            print(u"処理を中断しました。 ツールウィンドウのエラーメッセージを見てください。")
            return

        if not renamer.didUserAcceptDisclaimer():
            return

        # Hypershadeウィンドウが開いているとシーンオープン時にMayaがクラッシュするバグがあるのでHypershadeを閉じる
        panels = cmds.lsUI(panels=True)
        for pnl in panels:
            if pnl.startswith("hyperShadePanel"):
                cmds.deleteUI(pnl, pnl=True)
                break

        ignoreFolderName = self.ignoreText.text().strip() # 無視するフォルダ
        curProjPath = renamer.getCurrentProjectDir() # 現在のシーン
        batchRootPath = self.rootDirWidget.getPath() # フォルダ一括
        doFolder = self.chkFolderName.isEnabled() and self.chkFolderName.isChecked() # フォルダをリネーム
        doTexture = self.chkTextureName.isEnabled() and self.chkTextureName.isChecked() # テクスチャーをリネーム
        doMaya = self.chkMayaFileName.isEnabled() and self.chkMayaFileName.isChecked() # Mayaファイルをリネーム
        doMayaAscii = doMaya and self.chkBatchMa.isEnabled() and self.chkBatchMa.isChecked()
        doMayaBinary = doMaya and self.chkBatchMb.isEnabled() and self.chkBatchMb.isChecked()
        bRegex = self.chkRegex.isEnabled() and self.chkRegex.isChecked()

        # 読み取り専用になっていないか確認
        if not self.isDryRun:
            if isCurrentScene:
                if renamer.checkFoldersAndFilesReadOnly(curProjPath) == False:
                    cmds.confirmDialog(title=u"Warning",
                                       message=u"「読み取り専用」です。変更を保存できないので中止します。" + curProjPath,
                                       button=["OK"])
                    return
            else:
                if renamer.checkFoldersAndFilesReadOnly(batchRootPath) == False:
                    cmds.confirmDialog(title=u"Warning",
                                       message=u"読み取り専用になっているので変更できません: " + batchRootPath,
                                       button=["OK"])
                    return

        if isCurrentScene:
            scenesToProcess = [cmds.file(query=True, sceneName=True)]
        else:
            scenesToProcess = renamer.getScenesToProcess(batchRootPath, False, True, True, ignoreFolderName)

        ##### リネーム(isDryRunならテスト)開始 #####
        startTime = time.time()

        # リネームの対象のチェックボックスで、「外ファイル」のアイテムが一つでも選択
        for fromText in self.beforeAfterDict:
            # ディクショナリを使っているのはリネームの記述がcsv指定で複数ある場合の為
            toText = self.beforeAfterDict[fromText]
            if isCurrentScene:
                curProjPath = renamer.renameFilesAndFolders(curProjPath, doFolder, doTexture, False, False,
                                         fromText, toText, bRegex, ignoreFolderName, self.isDryRun)
            else:
                batchRootPath = renamer.renameFilesAndFolders(batchRootPath, doFolder, doTexture, doMayaAscii,
                                        doMayaBinary, fromText, toText, bRegex, ignoreFolderName, self.isDryRun)

        # リネームの対象のチェックボックスで、「シーン内」のアイテムが一つでも選択
        if self.isSceneItemChecked():
            if not isCurrentScene:
                if not self.isDryRun:
                    # パスが上で変わっているかもしれないので、リスト作り直し
                    scenesToProcess = renamer.getScenesToProcess(batchRootPath, False, True, True, ignoreFolderName)
            numScenes = len(scenesToProcess)
            for fileFullPath in scenesToProcess:
                fileFullPath = re.sub(r'\\', '/', fileFullPath)
                print(u"処理中 " + str(numProcessedScenes + numUnOpendScenes + 1) + "/" + str(numScenes))
                try:
                    if fileFullPath:
                        # シーンパスがMayaのプロジェクトの構成だったらSet Project。(テクスチャーパス等の相対パス設定ができるようになるので)
                        if os.path.basename(os.path.dirname(fileFullPath)) == "scenes":
                            cmds.workspace(os.path.dirname(os.path.dirname(fileFullPath)), openWorkspace=True)
                        if not isCurrentScene:
                            cmds.file(fileFullPath, open=True, force=True, pmt=False)
                        numProcessedScenes += 1
                    else:
                        continue
                except RuntimeError as e:
                    print(str(e))
                    renamer.writeLog(u"シーンオープン中になにかエラーがありました," + fileFullPath)
                    numUnOpendScenes += 1
                    # continue
                # beforeAfterDictはリネーム前,リネーム後の組み合わせのディクショナリ。
                # csvで複数のリネームの組み合わせにも対応。
                for fromText in self.beforeAfterDict:
                    toText = self.beforeAfterDict[fromText]

                    # 現在のシーンのリネーム時はシーンファイル名はリネームしない・・・が関係ありそうなのでお知らせ
                    if isCurrentScene and not self.isDryRun:
                        if bRegex:
                            fullPathAfter = re.sub(fromText, toText, fileFullPath)
                        else:
                            fullPathAfter = fileFullPath.replace(fromText, toText)
                        if fileFullPath != fullPathAfter:
                            msgBox = QMessageBox()
                            msgBox.setWindowTitle(u"お知らせ")
                            msgBox.setInformativeText(u"シーンファイル名は変更されていません。　ご自分で直してください。")
                            msgBox.setDefaultButton(QMessageBox.Ok)
                            msgBox.exec_()

                    if fromText != toText:
                        renamer.renameCurrentScene(fromText,
                                                   toText,
                                                   bRegex,
                                                   self.chkMatFolderPath.isEnabled() and self.chkMatFolderPath.isChecked(),
                                                   self.chkMatTextureName.isEnabled() and self.chkMatTextureName.isChecked(),
                                                   self.chkMaterialName.isEnabled() and self.chkMaterialName.isChecked(),
                                                   self.chkLocatorName.isEnabled() and self.chkLocatorName.isChecked(),
                                                   self.chkMeshName.isEnabled() and self.chkMeshName.isChecked(),
                                                   self.chkJointName.isEnabled() and self.chkJointName.isChecked(),
                                                   self.chkGroupName.isEnabled() and self.chkGroupName.isChecked(),
                                                   self.chkRefPathFolderName.isEnabled() and self.chkRefPathFolderName.isChecked(),
                                                   self.chkRefPathFileName.isEnabled() and self.chkRefPathFileName.isChecked(),
                                                   self.isDryRun)
                try:
                    if cmds.file(q=True, modified=True):
                        # 一回リネームしないと上書き保存できない時があるのでリネームして元に戻す
                        tmpName = os.path.basename(fileFullPath)
                        tmpName = tmpName.replace(".ma", "_" + g_tool_name + ".ma")
                        cmds.file(rename=tmpName)
                        cmds.file(rename=os.path.basename(fileFullPath))
                        cmds.file(rn=fileFullPath)
                        if fileFullPath.endswith(".ma"):
                            try:
                                cmds.file(save=True, type='mayaAscii')
                            except RuntimeError as e:
                                renamer.writeLog(u"保存に失敗," + fileFullPath + "." + str(e))
                        elif fileFullPath.endswith(".mb"):
                            try:
                                cmds.file(save=True, type='mayaBinary')
                            except RuntimeError as e:
                                renamer.writeLog(u"保存に失敗," + fileFullPath + "." + str(e))
                    # 開いてしまったウィンドウ類を閉じる
                    windows = cmds.lsUI(type=['window'])
                    for window in windows:
                        if window != u'MayaWindow':
                            try:
                                cmds.deleteUI(window)
                            except:
                                pass
                except RuntimeError as e:
                    renamer.writeLog(u"シーンの保存に失敗しました," + fileFullPath)

        endTime = time.time()

        renamer.g_logFile.close()

        if os.stat(renamer.g_logFile.name).st_size > 0:
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u"完了")
            if self.isDryRun:
                msgBox.setText(u"リネームテストが終わりました。")
            else:
                msgBox.setText(u"リネームが終わりました。")
            msgBox.setInformativeText(u"かかった時間：" + str(int(endTime - startTime)) + u" 秒。\n" +
                                      u"チェックしたシーン数: " + str(numProcessedScenes) + "\n" +
                                      u"開けなかったシーン: " + str(numUnOpendScenes))
            msgBox.setDefaultButton(QMessageBox.Ok)
            msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u"変更なし")
            msgBox.setText(u"何も変更はありませんでした")
            print(u"何も変更はありませんでした")
            msgBox.setInformativeText(u"かかった時間：" + str(int(endTime - startTime)) + u" 秒。\n" +
                                      u"チェックしたシーン数: " + str(numProcessedScenes) + "\n" +
                                      u"開けなかったシーン: " + str(numUnOpendScenes))
            msgBox.setDefaultButton(QMessageBox.Ok)
            msgBox.exec_()

        if os.stat(renamer.g_logFile.name).st_size > 0:
            print(u"ログファイル: " + renamer.g_logFile.name)
            # ログに書き込まれていたら(size>0)タイトルをPrependして再保存
            if sys.version_info.major == 2:
                with open(renamer.g_logFile.name, "r") as original:
                    data = original.read().decode("utf-8_sig")
                os.unlink(renamer.g_logFile.name)
                with tempfile.NamedTemporaryFile(delete=False, mode="w") as renamer.g_logFile:
                    renamer.writeLog(u"変更項目,リネーム前,リネーム後,Mayaシーン\n" + data)
            else:
                # Python3より上とみなす
                with open(renamer.g_logFile.name, encoding="utf-8_sig", mode="r") as original:
                    data = original.read()
                os.unlink(renamer.g_logFile.name)
                with tempfile.NamedTemporaryFile(delete=False, encoding="utf-8_sig", mode="w") as renamer.g_logFile:
                    renamer.writeLog(u"変更項目,リネーム前,リネーム後,Mayaシーン\n" + data)
            renamer.g_logFile.close()
            osCommandString = "notepad.exe " + renamer.g_logFile.name
            import subprocess
            subprocess.Popen(osCommandString)
        else:
            print(u"ログファイル書き出しなし")
            os.unlink(renamer.g_logFile.name)


####### Begin Save UI #########
def saveUiState(ui, setting):
    u"""
    PySideのウィンドウのUIウィジェットの状態を保存します。
    現状 QLineEdit, QCheckBox, QRadioButton, QTabWidget, QComboBox に対応しています。
    他のUIパーツの状態を保存したい場合はタイプを追加してください。
    :param ui: QMainWindow.
    :param settings: QSettings.
    """
    # Window location
    setting.setValue("x", ui.x())
    setting.setValue("y", ui.y())

    index = 0 # For UI without objectName
    lineEdits = ui.findChildren(QLineEdit)
    for le in lineEdits:
        name = le.objectName()
        if not name:
            name = "QLineEdit_" + str(index)
            index += 1
        value = le.text()
        setting.setValue(name, value)

    checkBoxes = ui.findChildren(QCheckBox)
    for cb in checkBoxes:
        name = cb.objectName()
        if not name:
            name = "QCheckBox_" + str(index)
            index += 1
        value = cb.isChecked()
        setting.setValue(name, value)

    radioButtons = ui.findChildren(QRadioButton)
    for rb in radioButtons:
        name = rb.objectName()
        if not name:
            name = "QRadioButton_" + str(index)
            index += 1
        value = rb.isChecked()
        setting.setValue(name, value)

    tabs = ui.findChildren(QTabWidget)
    for tab in tabs:
        name = tab.objectName()
        if not name:
            name = "QTabWidget_" + str(index)
            index += 1
        value = tab.currentIndex()
        setting.setValue(name, value)

    combos = ui.findChildren(QComboBox)
    for combo in combos:
        name = combo.objectName()
        if not name:
            name = "QComboBox_" + str(index)
            index += 1
        value = combo.currentIndex()
        setting.setValue(name, value)


def deleteUISettings(uiSettingPath):
    u"""
    UIの状態を保存している.iniファイルを削除します。
    """
    try:
        os.remove(uiSettingPath)
        print(u"設定ファイルを削除しました: " + uiSettingPath)
    except:
        print(u"設定ファイルはありませんでした: " + uiSettingPath)

def restoreUiState(ui, setting):
    u"""
    保存したPySideのウィンドウのUIウィジェットの状態を読み込む。
    現状 QLineEdit, QCheckBox, QRadioButton, QTabWidget, QComboBox に対応しています。
    他のUIパーツの状態を保存したい場合はタイプを追加してください。
    :param ui: QMainWindow.
    :param settings: QSettings.
    """
    defaultKeys = ["x", "y", "windowState", "geometry"] # UIに何もなくてもこれらは保存される

    # UIなどに変更があり、UIの項目数と設定ファイルの項目数が合わなかったら設定ファイルを削除する
    uiParts = []
    uiParts += ui.findChildren(QLineEdit)
    uiParts += ui.findChildren(QCheckBox)
    uiParts += ui.findChildren(QRadioButton)
    uiParts += ui.findChildren(QTabWidget)
    uiParts += ui.findChildren(QComboBox)
    if len(setting.allKeys()) - len(defaultKeys) != len(uiParts):
        deleteUISettings(setting.fileName())

    x = setting.value("x")
    y = setting.value("y")
    if x and y:
        ui.setGeometry(int(x), int(y), ui.width(), ui.height())

    index = 0  # For UI without objectName
    lineEdits = ui.findChildren(QLineEdit)
    for le in lineEdits:
        name = le.objectName()
        if not name:
            name = "QLineEdit_" + str(index)
            index += 1
        value = setting.value(name)
        if not value:
            # テキストフィールドにはかならずしも文字がはいっているとは限らない
            value = ""
        else:
            le.setText(value)

    checkBoxes = ui.findChildren(QCheckBox)
    for cb in checkBoxes:
        isOff = False
        name = cb.objectName()
        if not name:
            name = "QCheckBox_" + str(index)
            index += 1
        state = setting.value(name)
        if g_curMayaVersion < 2017:
            if state == "false":
                state = False
            elif state == "true":
                state = True
        if state is None:
            state = True
            print("Error: Could not find check state for checkbox " + name + ", " + str(state))
        cb.setChecked(bool(state))

    radioButtons = ui.findChildren(QRadioButton)
    for rb in radioButtons:
        name = rb.objectName()
        if not name:
            name = "QRadioButton_" + str(index)
            index += 1
        state = setting.value(name)
        if g_curMayaVersion < 2017:
            if state == "false":
                state = False
            elif state == "true":
                state = True

            if state is None:
                state = True
                print("Error: Could not find check state for radio " + name)
        rb.setChecked(bool(state))

    tabs = ui.findChildren(QTabWidget)
    for tab in tabs:
        name = tab.objectName()
        if not name:
            name = "QTabWidget_" + str(index)
            index += 1
        state = setting.value(name)
        if state is None:
            state = 0
            print("Error: Could not find tab index for " + name)
        tab.setCurrentIndex(int(state))

    combos = ui.findChildren(QComboBox)
    for combo in combos:
        name = combo.objectName()
        if not name:
            name = "QComboBox_" + str(index)
            index += 1
        state = setting.value(name)
        if state is None:
            state = 0
            print("Error: Could not find combo index for " + name)
        combo.setCurrentIndex(int(state))


####### End Save UI ###########

####### メイン関数 ###########
def main():
    u"""
    メイン関数。　GUIモードでツールを起動
    """
    g_curMayaVersion = cmds.about(version=True)
    mayaWindow = getMayaMainWindow()
    if cmds.window(g_tool_name, exists=True):
        cmds.deleteUI(g_tool_name) # Delete existing window
    window = RenamerWindow(mayaWindow)
    window.show()
    window.activateWindow()
