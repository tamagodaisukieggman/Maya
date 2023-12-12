from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import importlib
from functools import partial

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

from . import command
from . import TITLE
from . import NAME
from . import CLASS_NAME

from . import BUTTONS
from . import FILE_NODE_NAME
from . import FILE_PATH_NAME
from . import IMAGE_FILE_TYPES


# 開発中はTrue、リリース時にFalse
DEV_MODE = True

if DEV_MODE:
    importlib.reload(command)


file_directory = os.path.dirname(__file__)
UI_FILE = os.path.join(file_directory, f'{NAME}.ui').replace(os.sep, '/')


class HairToolSupporter(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    UI = None
    _tso_flag = False
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self._settings = None
        loader = QUiLoader()
        self.UI = loader.load(UI_FILE)
        self._setRadioButtonGroup()

        self._appendMenu()

        self.resize(200, 250)
        self.setWindowTitle(TITLE)
        self.setCentralWidget(self.UI)

        self._setButtonIcon()
        self._setUIConnections()

        # self._setWindowSize()
        self._resetSettings()

        self.setWindowState()

        command.attach_job(self.objectName(), self._resetSettings)

    def setWindowState(self):
        """ウィンドウサイズの設定保存
        fileInfo に書き込む
        """
        # self.UI.tabWidget.setCurrentIndex(0)
        self.settingFileName = f'{self.__class__.__name__}.ini'
        filename = os.path.join(os.getenv('MAYA_APP_DIR'), 'shenron_tool_settings', self.settingFileName).replace(os.sep, '/')
        print('ini file ---- ')
        print(filename)
        self._settings = QtCore.QSettings(filename, QtCore.QSettings.IniFormat)
        self._settings.setIniCodec('utf-8')


    def restore(self):
        """ウィンドウサイズのリストア
        """
        self.restoreGeometry(self._settings.value(f'{self.__class__.__name__}geometry'))
        self.restoreState(self._settings.value(f'{self.__class__.__name__}state'))
        # library_path = self._settings.value(f'{self.UI.megascanLibraryPathLineEdit.objectName()}.text')
        # character_path = self._settings.value(f'{self.UI.characterPathLineEdit.objectName()}.text')
        # # dna_file_Path = self._settings.value(f'{self.UI.dnaFilePathLineEdit.objectName()}.text')
        # character_id = self._settings.value(f'{self.UI.charactreIDLineEdit.objectName()}.text')
        # body_model_path = self._settings.value(f'{self.UI.importBodyModelLineEdit.objectName()}.text')
        # print("restore -- ")
        # print('library_path --', library_path)
        # print('character_path -- ', character_path)
        # print('character_id -- ', character_id)
        # # print('dna_file_Path -- ', dna_file_Path)
        # print('body_model_path -- ', body_model_path)
        # if library_path:
        #     self.setLibralyPath(library_path)
        # if character_path:
        #     self.setCharacterPath(character_path)
        # if character_id:
        #     self.setCharacterID(character_id)
        # # if dna_file_Path:
        # #     self.setDnaFilePath(dna_file_Path)
        # if body_model_path:
        #     self.setImportBodyModelFilePath(body_model_path)
        #     self.body_name_space = body_model_path.rsplit('/')[-1].rsplit('.')[0]

    def show(self):
        """ウィンドウサイズを戻すためにオーバーライド
        """
        self.restore()
        super(self.__class__, self).show()

    def closeEvent(self, event):
        """ツールウィンドウを閉じたときの動作
        ウィンドウサイズ保存
        選択順を元に戻す
        ワイヤー表示をオン
        """
        # library_path = self.UI.megascanLibraryPathLineEdit.text().replace(os.sep, '/')
        # character_path = self.UI.characterPathLineEdit.text().replace(os.sep, '/')
        # # dna_file_path = self.UI.dnaFilePathLineEdit.text().replace(os.sep, '/')
        # character_id = self.UI.charactreIDLineEdit.text()
        # body_model_path = self.UI.importBodyModelLineEdit.text().replace(os.sep, '/')

        # print("close -- ")
        # print('library_path --', library_path)
        # print('character_path -- ', character_path)
        # print('character_id -- ', character_id)
        # print('body_model_path -- ', body_model_path)

        # self._settings.setValue(f'{self.UI.megascanLibraryPathLineEdit.objectName()}.text', library_path)
        # self._settings.setValue(f'{self.UI.characterPathLineEdit.objectName()}.text', character_path)
        # # self._settings.setValue(f'{self.UI.dnaFilePathLineEdit.objectName()}.text', dna_file_path)
        # self._settings.setValue(f'{self.UI.charactreIDLineEdit.objectName()}.text', character_id)
        # self._settings.setValue(f'{self.UI.importBodyModelLineEdit.objectName()}.text', body_model_path)
        self._settings.setValue(f'{self.__class__.__name__}geometry', self.saveGeometry())
        self._settings.setValue(f'{self.__class__.__name__}state', self.saveState())
        self._setFileInfoData()

        super(self.__class__, self).closeEvent(event)

    def _setRadioButtonGroup(self):
        """ラジオボタングループ作成
        """
        self.actionRadioButtonGroup = QtWidgets.QButtonGroup()
        self.actionRadioButtonGroup.addButton(self.UI.assignMaterialRadioButton, 1)
        self.actionRadioButtonGroup.addButton(self.UI.selectGeometoryRadioButton, 2)
        self.actionRadioButtonGroup.button(1).setChecked(True)

        self.selectRadioButtonGroup = QtWidgets.QButtonGroup()
        self.selectRadioButtonGroup.addButton(self.UI.curveRadioButton, 1)
        self.selectRadioButtonGroup.addButton(self.UI.meshRadioButton, 2)
        self.selectRadioButtonGroup.button(1).setChecked(True)

    def _setButtonIcon(self):
        """ボタンアイコン適用
        """
        image = QtGui.QIcon(':/folder-open.png')
        self.UI.irdaMapDialogPushButton.setIcon(image)

    def _setWindowSize(self):
        """ウィンドウサイズの設定保存
        """
        self.settingFileName = f'{self.__class__.__name__}.ini'
        filename = os.path.join(os.getenv('MAYA_APP_DIR'),
                                'shenron_tool_settings',
                                self.settingFileName)
        self._settings = QtCore.QSettings(filename, QtCore.QSettings.IniFormat)

    def _getSceneName(self):
        """シーン名取得
        """
        self.scenePath = command.get_scene_name()

    def _resetSettings(self):
        """設定初期化
        """
        self._clearMemory()
        self._getFileInfoData()
        self._getSceneName()

    def _clearMemory(self):
        """メモリクリア
        """
        self.scenePath = ""
        self.irdaTexture = dict()

    # def restore(self):
    #     """ウィンドウサイズのリストア
    #     """
    #     self.restoreGeometry(self._settings.value(f'{self.__class__.__name__}geometry'))

    # def show(self):
    #     """ウィンドウサイズを戻すためにオーバーライド
    #     """
    #     self.restore()
    #     super(self.__class__, self).show()

    # def closeEvent(self, event):
    #     """ツールウィンドウを閉じたときの動作
    #     ウィンドウサイズ保存
    #     fileInfo にデータ書き込み
    #     ファイルパスとスライダ情報
    #     """
    #     super(self.__class__, self).closeEvent(event)
    #     self._settings.setValue(f'{self.__class__.__name__}geometry', self.saveGeometry())
    #     self._setFileInfoData()

    def _setTextureNodeData(self, mapType: str="irda", file_node: str="", file_path: str=""):
        """画像ファイルデータ記憶

        Args:
            mapType (str, optional): アルファかデプスか. Defaults to "irda".
            file_node (str, optional): ファイルノード名. Defaults to "".
            file_path (str, optional): ファイルパス. Defaults to "".
        """
        if mapType=="irda":
            self.irdaTexture[FILE_NODE_NAME] = file_node
            self.irdaTexture[FILE_PATH_NAME] = file_path

    def _getFileInfoData(self):
        """fileInfo のデータ取得
        """
        file_node = command.get_file_info_data(f"irdaTexture_{FILE_NODE_NAME}")
        file_path = command.get_file_info_data(f"irdaTexture_{FILE_PATH_NAME}")
        if file_node and file_path:
            if file_node:
                active_file_node = command.file_node_exists(file_path[0])
                self._setTextureNodeData(mapType="irda", file_node=active_file_node, file_path=file_path[0])
        self._textureLineEdit('irda')

    def _setTexturePath(self):
        """テクスチャパスの記憶
        """
        if self.irdaTexture:
            file_node = self.irdaTexture[FILE_NODE_NAME]
            file_path = str(self.irdaTexture[FILE_PATH_NAME]).replace(os.sep, '/')
            command.set_file_info_data(f"irdaTexture_{FILE_NODE_NAME}", file_node)
            command.set_file_info_data(f"irdaTexture_{FILE_PATH_NAME}", file_path)

    def _setFileInfoData(self):
        """fileInfo にデータ格納
        """
        command.set_file_info_data("WINDOW_SETTINGS", self._settings)
        self._setTexturePath()


    def _appendMenu(self):
        """ファイルメニュー、ヘルプメニューを作成
        """
        menuBar = self.menuBar()

        openAct = QtWidgets.QAction('Open Help Site ...', self)
        openAct.triggered.connect(self._openHelp)

        helpMenu = menuBar.addMenu('Help')
        helpMenu.addAction(openAct)

    def _openHelp(self):
        """ヘルプサイト表示
        """
        command.open_web_site()

    def _textureLineEdit(self, mapType: str = "irda"):
        """lineEdit にパスを記述

        Args:
            mapType (str, optional): アルファかデプスか. Defaults to "irda".
        """
        if mapType == "irda":
            self.UI.irdaTextureLineEdit.setText("")
            if self.irdaTexture:
                self.UI.irdaTextureLineEdit.setText(self.irdaTexture[FILE_PATH_NAME])
        self._setTexturePath()

    def _openFIleDialog(self, mapType: str = "irda"):
        """画像ファイル選択ダイアログ表示

        Args:
            mapType (str, optional): アルファかデプスか. Defaults to "irda".
        """
        _filter = f'Images (*.{" *.".join([x for x in IMAGE_FILE_TYPES])})'
        if self.scenePath:
            directory = self.scenePath.replace(os.sep, '/')
            directory = directory.rsplit("/", 1)[0]
        else:
            directory = ""

        dialog = QtWidgets.QFileDialog(directory=directory)
        dialog.setNameFilters([_filter])
        dialog.selectNameFilter(_filter)

        if dialog.exec_():
            path = dialog.selectedFiles()[0].replace(os.sep, '/')
        else:
            return

        if not command.texture_file_name_check(path):
            return

        file_node = command.file_node_exists(path)
        if not file_node:
            file_node = command.create_file_node(texture_file_path=path)

        self._setTextureNodeData(mapType=mapType, file_node=file_node, file_path=path)

        self._textureLineEdit(mapType=mapType)

    def chengeColorSwitch(self):
        _buttonName = self.sender().objectName()
        command.color_change_switch(_buttonName)


    def buttonClicked(self):
        """カラーボタンのクリック動作
        """
        _actionButtonState = self.actionRadioButtonGroup.checkedButton().text()
        _radioButtonState = self.selectRadioButtonGroup.checkedButton().text()

        _button_name = self.sender().objectName()
        _color = BUTTONS[_button_name]
        command.button_clicked(
                            action_type=_actionButtonState,
                            button_name=_button_name,
                            button_color=_color,
                            irda=self.irdaTexture,
                            selection_type=_radioButtonState
                            )

    def _setUIConnections(self):
        """シグナル設定
        """
        self.UI.colorButtonA.clicked.connect(self.buttonClicked)
        self.UI.colorButtonB.clicked.connect(self.buttonClicked)
        self.UI.colorButtonC.clicked.connect(self.buttonClicked)
        self.UI.colorButtonD.clicked.connect(self.buttonClicked)
        self.UI.colorButtonE.clicked.connect(self.buttonClicked)
        self.UI.colorButtonF.clicked.connect(self.buttonClicked)
        self.UI.colorButtonG.clicked.connect(self.buttonClicked)
        self.UI.colorButtonH.clicked.connect(self.buttonClicked)
        self.UI.colorButtonI.clicked.connect(self.buttonClicked)
        self.UI.colorButtonJ.clicked.connect(self.buttonClicked)

        self.UI.irdaMapDialogPushButton.clicked.connect(partial(self._openFIleDialog, 'irda'))

        self.UI.colorChangePushButton.clicked.connect(self.chengeColorSwitch)
        self.UI.grayScalePushButton.clicked.connect(self.chengeColorSwitch)




def main():
    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == CLASS_NAME:
            _obj.close()
            del _obj

    if not command.check_path_exists(path=UI_FILE):
        return

    command.set_environ()
    command.set_plugin_path()
    command.load_plugins()
    ui = HairToolSupporter()
    ui.show()
