from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from functools import partial
import importlib
import webbrowser

from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

from ...utils import gui_util

from . import data
from . import scene_data
from . import maya_utils
from . import utils
from . import setting

# 開発中はTrue、リリース時にFalse
DEV_MODE = setting.load_config(config_name='DEV_MODE')

if DEV_MODE:
    importlib.reload(gui_util)
    importlib.reload(data)
    importlib.reload(scene_data)
    importlib.reload(maya_utils)
    importlib.reload(utils)

CHECKER_GUI_NAME = setting.load_config(config_name='CHECKER_GUI_NAME')
CHECKER_RESULT_GUI_NAME = setting.load_config(config_name='CHECKER_RESULT_GUI_NAME')
CHECKER_ERROR_GUI_NAME = setting.load_config(config_name='CHECKER_ERROR_GUI_NAME')
CURRENT_PROJECT = setting.load_config(config_name='CURRENT_PROJECT')
if not CURRENT_PROJECT:
    CURRENT_PROJECT = 'cygames'

def open_help_site():
    _web_site = setting.load_config('WEB_SITE')
    webbrowser.open(_web_site)


class CheckerResultGUI(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(CheckerResultGUI, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.resize(640, 455)
        self.initUI()

    def initUI(self):
        """UI 初期化
        """
        wrapper = QtWidgets.QWidget()
        self.setCentralWidget(wrapper)

        mainLayout = QtWidgets.QVBoxLayout()

        checkBoxLayout = QtWidgets.QHBoxLayout()
        self.selectionCheckBox = QtWidgets.QCheckBox('Select Target')
        self.focusCheckBox = QtWidgets.QCheckBox('Focus View')
        self.focusOutlinerCheckBox = QtWidgets.QCheckBox('Focus Outliner')

        self.selectionCheckBox.clicked.connect(
            partial(self.selectionCheckBoxCallBack))
        self.selectionCheckBox.setChecked(1)
        self.focusCheckBox.setChecked(1)
        self.focusOutlinerCheckBox.setChecked(1)

        checkBoxLayout.addWidget(self.selectionCheckBox)
        checkBoxLayout.addWidget(self.focusCheckBox)
        checkBoxLayout.addWidget(self.focusOutlinerCheckBox)

        tableWidget = self.createTableWidget()
        self.tableWidget = tableWidget

        buttonLayout = QtWidgets.QHBoxLayout()
        closeButton = QtWidgets.QPushButton("CLOSE")
        buttonLayout.addWidget(closeButton)

        mainLayout.addLayout(checkBoxLayout)
        mainLayout.addWidget(tableWidget)
        mainLayout.addLayout(buttonLayout)

        wrapper.setLayout(mainLayout)

        closeButton.clicked.connect(partial(self.closeWindow))

    def createTableWidget(self):
        """テーブルウィジェットの作成

        Returns:
            [QTableWidget]:
        """
        tableWidget = QtWidgets.QTableWidget()
        headerLabels = ["Modify Error"]

        tableWidget.setColumnCount(len(headerLabels))
        tableWidget.setHorizontalHeaderLabels(headerLabels)

        header = tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

        tableWidget.setAlternatingRowColors(True)
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tableWidget.setSelectionBehavior(tableWidget.SelectRows)
        tableWidget.selectionModel().selectionChanged.connect(self.selectTableItems)
        return tableWidget

    def closeWindow(self, *args):
        gui_util.close_pyside_windows([CHECKER_RESULT_GUI_NAME])

    def setTableData(self, modify_flag=True, datas=None):
        """エラー内容をテーブルに表示

        Args:
            results ([ResultDataObj]): [description]. Defaults to None.
        """
        if not datas:
            return

        title = f'[ {len(datas)} ] modify error'
        headerLabel = ['Modify Error']

        if not modify_flag:
            title = f'[ {len(datas)} ] can not modify error'
            headerLabel = ['Could not Modify Error']

        self.setWindowTitle(title)
        self.tableWidget.setHorizontalHeaderLabels(headerLabel)
        self.tableWidget.setRowCount(len(datas))

        for row, result in enumerate(datas):
            item_a = QtWidgets.QTableWidgetItem(result)
            self.tableWidget.setItem(row, 0, item_a)

    def selectTableItems(self):
        """テーブル選択の動作
        """
        _select_flag = self.selectionCheckBox.isChecked()
        _focus_flag = self.focusCheckBox.isChecked()
        _focus_outliner_flag = self.focusOutlinerCheckBox.isChecked()
        select_nodes = []

        for QModelIndex in self.tableWidget.selectedItems():
            target = QModelIndex.text()
            select_nodes.append(target.split()[-1])

        if select_nodes:
            maya_utils.select_target(
                select_nodes, _select_flag, _focus_flag, _focus_outliner_flag)

    def selectionCheckBoxCallBack(self, *args):
        """SelectTarget のチェックが入っていない時はフォーカスと
        アウトライナフォーカスのチェックボックスを無効化する
        """
        _flag = self.selectionCheckBox.isChecked()
        if _flag:
            self.focusCheckBox.setEnabled(1)
            self.focusOutlinerCheckBox.setEnabled(1)
        else:
            self.focusCheckBox.setEnabled(0)
            self.focusOutlinerCheckBox.setEnabled(0)


class CheckerGUI(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, name: str = ''):
        super(CheckerGUI, self).__init__()
        self.check_button_name:str = name

        self.unknown_category_type = setting.load_config(config_name='UNKNOWN_SCENE_CATEGORY_NAME')
        self.memory_nodes:list = []
        self.results:data.ResultData = None
        self.checker_modules:list = []

        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.resize(800, 455)
        self.initUI()

    def createTableWidget(self):
        """テーブルウィジェットの作成

        Returns:
            [QTableWidget]:
        """
        tableWidget = QtWidgets.QTableWidget()
        headerLabels = ["Error / Warning", "Type", "Node / Compornent"]

        tableWidget.setColumnCount(len(headerLabels))
        tableWidget.setHorizontalHeaderLabels(headerLabels)

        header = tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

        tableWidget.setAlternatingRowColors(True)
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tableWidget.setSelectionBehavior(tableWidget.SelectRows)
        tableWidget.selectionModel().selectionChanged.connect(self.selectTableItems)

        return tableWidget



    def setTableData(self,
                     check_result: data.CheckResultData = None,
                     maya_scene_data: scene_data.MayaSceneData = None,
                     ):
        """エラー内容をテーブルに表示

        Args:
            results ([ResultDataObj]): [description]. Defaults to None.
            scene_path:scene_data.SceneData ([SceneDataObj]): [description]. Defaults to None.
        """
        if not check_result or not maya_scene_data:
            return

        # 選択用のリスト
        self.memory_nodes:list = []

        self.results = check_result.result_datas.values()
        self.setWindowTitleText(maya_scene_data = maya_scene_data, check_result= check_result)

        # テーブルの数を設定
        all_item_count = 0
        for result in check_result.result_datas.values():
            all_item_count += result.all_item_count
        self.tableWidget.setRowCount(all_item_count)

        count = 0
        for result in check_result.result_datas.values():
            result: data.ResultData = result
            if result.error_nodes:
                _text_background_color = setting.load_config('ERROR_BG_COLOR')
                count += self.setTableCompornent(error_flag=True, count=count, messages=result.error_message_list, nodes=result.error_nodes, result=result, text_bg_color=_text_background_color)

            if result.warning_nodes:
                _text_background_color = setting.load_config('WARNING_BG_COLOR')
                _text_background_color = []
                count += self.setTableCompornent(error_flag=False, count=count, messages=result.warning_message_list, nodes=result.warning_nodes, result=result, text_bg_color=_text_background_color)


    def setTableCompornent(self, error_flag:bool, count: int, messages:list, nodes: list, result: data.ResultData, text_bg_color: list)->int:
        for i, (message, node) in enumerate(zip(messages, nodes), 1):
            compornent:list = []

            self.setTable(row=count, text=message, type_text=result.checker, node_text=node, type_color=result.color, text_bg_color=text_bg_color)

            _key_strings:str = f'{message}.{node}'

            if error_flag:
                compornent = result.error_compornent.get(_key_strings)
            else:
                compornent = result.warning_compornent.get(_key_strings)

            if compornent:
                self.memory_nodes.append(compornent)
            else:
                self.memory_nodes.append([node])
            count += 1
        return i


    def setTable(self, row:int, text:str, type_text:str, node_text:str, type_color:list, text_bg_color:list):
        item_a = QtWidgets.QTableWidgetItem(text)
        item_b = QtWidgets.QTableWidgetItem(type_text)
        item_c = QtWidgets.QTableWidgetItem(str(node_text))

        self.tableWidget.setItem(row, 0, item_a)
        self.tableWidget.setItem(row, 1, item_b)
        self.tableWidget.setItem(row, 2, item_c)

        item_b.setTextAlignment(QtCore.Qt.AlignCenter)
        item_b.setBackground(QtGui.QColor(type_color[0], type_color[1], type_color[2]))
        if text_bg_color:
            item_a.setBackground(QtGui.QColor(text_bg_color[0], text_bg_color[1], text_bg_color[2]))


    def initUI(self):
        """UI 初期化
        """

        wrapper = QtWidgets.QWidget()
        self.setCentralWidget(wrapper)

        mainLayout = QtWidgets.QVBoxLayout()

        helpAct = QtWidgets.QAction('Open Help Site ...', self)
        helpAct.triggered.connect(self.openHelp)

        menuBar = self.menuBar()
        menu = menuBar.addMenu('Help')
        menu.addAction(helpAct)

        checkBoxLayout = QtWidgets.QHBoxLayout()
        self.selectionCheckBox = QtWidgets.QCheckBox('Select Target')
        self.focusCheckBox = QtWidgets.QCheckBox('Focus View')
        self.focusOutlinerCheckBox = QtWidgets.QCheckBox('Focus Outliner')

        self.selectionCheckBox.clicked.connect(
            partial(self.selectionCheckBoxCallBack))
        self.selectionCheckBox.setChecked(1)
        self.focusCheckBox.setChecked(1)
        self.focusOutlinerCheckBox.setChecked(1)

        checkBoxLayout.addWidget(self.selectionCheckBox)
        checkBoxLayout.addWidget(self.focusCheckBox)
        checkBoxLayout.addWidget(self.focusOutlinerCheckBox)

        tableWidget = self.createTableWidget()
        self.tableWidget = tableWidget

        buttonLayout = QtWidgets.QHBoxLayout()
        recheckButton = QtWidgets.QPushButton(f"Check")

        pepairButton = QtWidgets.QPushButton("Repair and reinspection")
        openExportWindowButton = QtWidgets.QPushButton("Open Export Window")

        # FIXME: エクスポータが決まったらボタンの有効化
        # openExportWindowButton.setEnabled(False)

        buttonLayout.addWidget(recheckButton)
        buttonLayout.addWidget(pepairButton)
        buttonLayout.addWidget(openExportWindowButton)

        mainLayout.addLayout(checkBoxLayout)
        mainLayout.addWidget(tableWidget)
        mainLayout.addLayout(buttonLayout)

        recheckButton.clicked.connect(partial(self.reCheck))
        pepairButton.clicked.connect(partial(self.modifyData))
        openExportWindowButton.clicked.connect(partial(self._open_export_window))

        wrapper.setLayout(mainLayout)

        # 自動修理ボタンの無効化
        pepairButton.setEnabled(False)

        self._setWindowSize()
        maya_utils.attach_job(self.objectName(), partial(self.clearTableItems))


    def clearTableItems(self, *args):
        if not self.tableWidget:
            return
        self.tableWidget.setRowCount(0)
        self.setWindowTitleText()

    def selectionCheckBoxCallBack(self, *args):
        """SelectTarget のチェックが入っていない時はフォーカスと
        アウトライナフォーカスのチェックボックスを無効化する
        """
        _flag = self.selectionCheckBox.isChecked()
        if _flag:
            self.focusCheckBox.setEnabled(1)
            self.focusOutlinerCheckBox.setEnabled(1)
        else:
            self.focusCheckBox.setEnabled(0)
            self.focusOutlinerCheckBox.setEnabled(0)

    def setWindowTitleText(self, maya_scene_data: scene_data.MayaSceneData = None, check_result: data.CheckResultData = None):
        error_count:int = 0
        if check_result:
            error_count = check_result.all_result_count
        title = 'DataType: [ {} ]  '

        if not maya_scene_data:
            _t = title.format(self.unknown_category_type)
        else:
            _t = title.format(maya_scene_data.current_category)

        _t += f' |   Total [ {error_count} ] error and warning'
        self.setWindowTitle(_t)

    def reCheck(self, *args):
        if self.tableWidget:
            from . import main

            _return_data = main.maya_scene_check(lower_drive_letter=False, _execute_check_modules=[], set_category=self.check_button_name)
            check_result:data.CheckResultData = _return_data[0]
            maya_scene_data:scene_data.MayaSceneData = _return_data[1]

            if check_result.all_result_count:
                self.setWindowTitleText(maya_scene_data = maya_scene_data, check_result = check_result)
                self.setTableData(check_result=check_result,
                                maya_scene_data=maya_scene_data,
                                )
            else:
                _d = gui_util.ConformDialog(title="Not Fond Error",
                                            message="Not Found Error")
                _d.exec_()
                utils.open_cyllista_export_window()
        else:
            from . import main
            main.main()

    def modifyData(self, *args):
        """データの修正
        """
        modify_results:data.ModifyResult  = utils.modify_data(results=self.results)

        if modify_results.modify_flag:
            _mod_window = CheckerResultGUI()
            _mod_window.setTableData(True, modify_results.modify_messages)
            _mod_window.show()
        if modify_results.error_flag:
            _error_window = CheckerResultGUI()
            _error_window.setTableData(False, modify_results.error_messages)
            _error_window.show()

        self.reCheck()


    def openHelp(self):
        """ヘルプサイト表示
        """
        open_help_site()

    def _open_export_window(self, *args):
        utils.open_cyllista_export_window()

    def selectTableItems(self):
        """テーブル選択の動作
        """
        _ids = []
        select_nodes = []
        _select_flag = self.selectionCheckBox.isChecked()
        _focus_flag = self.focusCheckBox.isChecked()
        _focus_outliner_flag = self.focusOutlinerCheckBox.isChecked()

        for QModelIndex in self.tableWidget.selectedIndexes():
            _id = QModelIndex.row()
            if _id not in _ids:
                _ids.append(_id)

        for i, x in enumerate(self.memory_nodes):
            if i in _ids:
                select_nodes.append(x)

        if select_nodes:
            maya_utils.select_target(
                select_nodes[0], _select_flag, _focus_flag, _focus_outliner_flag)

    def _setWindowSize(self):
        """ウィンドウサイズの設定保存
        """
        self.settingFileName = f'{self.__class__.__name__}.ini'
        project_name = CURRENT_PROJECT.lower()
        filename = os.path.join(os.getenv('MAYA_APP_DIR'), f'{project_name}_tool_settings', self.settingFileName)
        self._settings = QtCore.QSettings(filename, QtCore.QSettings.IniFormat)

    def closeEvent(self, event):
        super(self.__class__, self).closeEvent(event)
        self._settings.setValue(f'{self.__class__.__name__}geometry', self.saveGeometry())
        for col in range(self.tableWidget.columnCount()):
            width = self.tableWidget.columnWidth(col)
            self._settings.setValue(f'column_widths/{col}', width)

    def restore(self):
        """ウィンドウサイズのリストア
        """
        self.restoreGeometry(self._settings.value(f'{self.__class__.__name__}geometry'))
        for col in range(self.tableWidget.columnCount()):
            width = self._settings.value(f'column_widths/{col}', type=int)
            if width:
                self.tableWidget.setColumnWidth(col, width)

    def show(self):
        """ウィンドウサイズを戻すためにオーバーライド
        """
        self.restore()
        super(self.__class__, self).show()

