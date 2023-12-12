from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
import importlib

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

# import logging

from . import command
from . import TITLE
from . import NAME
from . import project

# logger = logging.getLogger(f'Maya{"".join(TITLE.split())}')
# logger.setLevel(logging.DEBUG)

CLASS_NAME = "".join(TITLE.split())

file_directory = os.path.dirname(__file__)
UI_FILE = os.path.join(file_directory, f'{NAME}.ui').replace(os.sep, '/')
TOOL_SETTING_DIRECTORY = os.path.join(os.getenv('MAYA_APP_DIR'),
                                f'{project}_settings', CLASS_NAME)

DEV_MODE = True

if DEV_MODE:
    importlib.reload(command)


class HDALoader(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    UI = None
    _tso_flag = False
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        loader = QUiLoader()
        self.UI = loader.load(UI_FILE)

        self._clearMemory()
        self._appendMenu()

        self.resize(300, 150)
        self.setWindowTitle(TITLE)
        self.setCentralWidget(self.UI)

        self._buildRightClickMenu()
        self._setUIConnections()

        self._trackSelectionOrderFlag()
        self._getHDA()
        self._listHDA()

        self._setWindowSize()

    def _buildRightClickMenu(self):
        """右クリックしたときに表示させるメニュー
        """
        self.replace_menu = QtWidgets.QMenu(self)
        action1 = QtWidgets.QAction(u"{}".format("Apply HDA ..."), self)
        action1.triggered.connect(lambda: self._applyHDA())
        self.replace_menu.addAction(action1)

    def _trackSelectionOrderFlag(self):
        """選択順を考慮
        元の設定をとっておきツール終了時に元に戻す
        Returns:
            [bool]: 元の設定のフラグ
        """
        self._tso_flag = command._trackSelectionOrder_Flag(self._tso_flag)

    def _clearMemory(self):
        """各種変数リセット
        """
        self._hdas = {}

    def _setWindowSize(self):
        """ウィンドウサイズの設定保存
        fileInfo に書き込む
        """
        self.settingFileName = f'{self.__class__.__name__}.ini'
        filename = os.path.join(os.getenv('MAYA_APP_DIR'),
                                'shenron_tool_settings',
                                self.settingFileName)
        self._settings = QtCore.QSettings(filename, QtCore.QSettings.IniFormat)

    def restore(self):
        """ウィンドウサイズのリストア
        """
        self.restoreGeometry(self._settings.value(f'{self.__class__.__name__}geometry'))

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
        super(self.__class__, self).closeEvent(event)
        self._settings.setValue(f'{self.__class__.__name__}geometry', self.saveGeometry())
        command._reset_track_selection_order_flag(self._tso_flag)
        command.wire_display_full()

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
        command.open_help_site()

    def contextMenu(self, point: QtCore.QPoint):
        """コンテクストメニューの表示位置調整

        Args:
            point (QtCore.QPoint): _description_
        """
        _add = QtCore.QPoint(20, 100)
        self.replace_menu.exec_(_add+self.mapToGlobal(point))

    def _setUIConnections(self):
        """コネクションの設定
        """
        self.UI.developModeCheckBox.clicked.connect(lambda: self._listHDA())
        self.UI.reloadAllHDAPushButton.clicked.connect(lambda: self._reloadHDA())
        self.UI.viewWireTogglePushButton.clicked.connect(lambda: self._viewWireToggle())
        self.UI.bakeAssetPushButton.clicked.connect(lambda: self._bakeAsset())
        self.UI.listHDAListWidget.itemDoubleClicked.connect(lambda: self._applyHDA())
        self.UI.listHDAListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.UI.listHDAListWidget.customContextMenuRequested.connect(self.contextMenu)

    def _bakeAsset(self):
        command.bake_asset()

    def _reloadHDA(self):
        """HDA をリロードし、特定のパスから再度取得する
        """
        command.reload_hda()
        self._getHDA()

    def _getHDA(self):
        """特定のパスにあるHDA を取ってくる
        """
        self._clearMemory()
        self._hdas = command.get_hdas(hda_path="")
        self._listHDA()

    def _listHDA(self):
        """listWidget にリスト作成
        """
        _flag = self.UI.developModeCheckBox.isChecked()
        self.UI.listHDAListWidget.clear()
        if not self._hdas:
            return
        for _hda_short_name, _hda in self._hdas.items():
            if _flag:
                self.UI.listHDAListWidget.addItem(_hda_short_name)
            elif not _hda.develop:
                self.UI.listHDAListWidget.addItem(_hda_short_name)

    def _applyHDA(self):
        """HDA の適用
        """
        if not self._hdas:
            return

        _hdas = self.UI.listHDAListWidget.selectedItems()
        if not _hdas:
            return

        _hda = _hdas[0]
        _current_hda = self._hdas[_hda.text()]

        command.load_hda(_current_hda)
        command.sync_asset(_current_hda, sync_output=True)

    def _viewWireToggle(self):
        command.wire_display_toggle()


def main():
    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == CLASS_NAME:
            _obj.close()
            del _obj

    if not command.check_path_exists(path=UI_FILE):
        return

    if not command.check_houdini_engine():
        return

    ui = HDALoader()
    ui.show()
