from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial
import importlib


from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin


from mtk.file.new_checker import gui_util
from mtk.file.new_checker import scene_data
from mtk.file.new_checker import checker
from mtk.file.new_checker import maya_utils

from mtk.file.new_checker import CHECKER_GUI_NAME
from mtk.file.new_checker import CHECKER_RESULT_GUI_NAME


# 開発中はTrue、リリース時にFalse
DEV_MODE = True

if not DEV_MODE:
    from mtk.file.new_checker import logger
else:
    importlib.reload(gui_util)
    importlib.reload(checker)
    importlib.reload(scene_data)
    importlib.reload(maya_utils)


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
        gui_util.close_pyside_windows(
            [CHECKER_RESULT_GUI_NAME])

    def setTableData(self, modify_flag=True, datas=None):
        """エラー内容をテーブルに表示

        Args:
            results ([ResultDataObj]): [description]. Defaults to None.
        """
        if not datas:
            return

        title = f'[ {len(datas)} ] modify error'
        headerLabel = 'Modify Error'

        if not modify_flag:
            title = f'[ {len(datas)} ] can not modify error'
            headerLabel = 'Can not Modify Error'

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
            select_nodes.append(target.split()[1])

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
    def __init__(self, *args, **kwargs):
        super(CheckerGUI, self).__init__(*args, **kwargs)

        self.memory_nodes = list()
        self.scene_path_obj = None
        self.results = None

        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.resize(640, 455)
        self.initUI()

    def createTableWidget(self):
        """テーブルウィジェットの作成

        Returns:
            [QTableWidget]:
        """
        tableWidget = QtWidgets.QTableWidget()
        headerLabels = ["内容", "種類", "該当ノード"]

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

    def setTableData(self, results=None, scene_path_obj=None):
        """エラー内容をテーブルに表示

        Args:
            results ([ResultDataObj]): [description]. Defaults to None.
            scene_path_obj ([SceneDataObj]): [description]. Defaults to None.
        """
        if not results or not scene_path_obj:
            return

        self.scene_path_obj = scene_path_obj
        self.results = results

        _result_datas = results.get_sort_data()
        title = '[ {} ]  DataType  '

        if not scene_path_obj.data_type:
            _t = title.format("unknown")
        else:
            _t = title.format(scene_path_obj.data_type)

        _t += f' : Total [ {len(_result_datas)} ] error and warning'
        self.setWindowTitle(_t)

        self.tableWidget.setRowCount(len(_result_datas))

        self.memory_nodes = list()
        for row, result in enumerate(_result_datas):

            ann = "None"
            button_name = ""

            text = str(result.error_text)
            error = str(result.error)
            node = result.error_nodes
            self.memory_nodes.append(node)

            if ":" in error:
                _split = error.split(":")
                error = _split[0]
                error_detail = _split[-1]

            # logger.info(u"text [ {} ],type [ {}] ,node [ {} ]".format(text, _type, node))

            if node:
                if isinstance(node, list):
                    ann = "{}...".format(node[0])
                    button_name = f'{node[0].split("|")[-1]}, ...'
                else:
                    ann = " > ".join(node.split("|"))
                    button_name = node.split("|")[-1]

            item_a = QtWidgets.QTableWidgetItem(text)
            item_b = QtWidgets.QTableWidgetItem(error)
            item_c = QtWidgets.QTableWidgetItem(button_name)
            self.tableWidget.setItem(row, 0, item_a)
            self.tableWidget.setItem(row, 1, item_b)
            self.tableWidget.setItem(row, 2, item_c)
            item_b.setBackground(QtGui.QColor(100, 100, 150))

    def initUI(self):
        """UI 初期化
        """

        wrapper = QtWidgets.QWidget()
        self.setCentralWidget(wrapper)

        mainLayout = QtWidgets.QVBoxLayout()

        helpAct = QtWidgets.QAction('Go to Website', self)
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
        recheckButton = QtWidgets.QPushButton("解決できるエラーを修正し　再検査")
        openExportWindowButton = QtWidgets.QPushButton("エラーを無視して出力ウィンドウを開く")
        buttonLayout.addWidget(recheckButton)
        buttonLayout.addWidget(openExportWindowButton)

        mainLayout.addLayout(checkBoxLayout)
        mainLayout.addWidget(tableWidget)
        mainLayout.addLayout(buttonLayout)

        recheckButton.clicked.connect(partial(self.modifyData))

        wrapper.setLayout(mainLayout)

        cmds.scriptJob(parent=self.objectName(), event=(
            "SceneOpened", partial(gui_util.close_pyside_windows, [
                CHECKER_GUI_NAME,
                CHECKER_RESULT_GUI_NAME,
            ])))
        cmds.scriptJob(parent=self.objectName(), event=(
            "NewSceneOpened", partial(gui_util.close_pyside_windows, [
                CHECKER_GUI_NAME,
                CHECKER_RESULT_GUI_NAME,
            ])))

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

    def modifyData(self, *args):
        """データの修正
        """
        gui_util.close_pyside_windows(
            [CHECKER_GUI_NAME, CHECKER_RESULT_GUI_NAME])

        _cheker = checker.Check()
        modify_messages = _cheker.modify_data(result=self.results)
        # _modifys 修正に成功した結果のリスト
        # _errors 修正に失敗した理由のリスト
        _modifys, _errors = modify_messages
        if _modifys:
            _mod_window = CheckerResultGUI()
            _mod_window.setTableData(True, _modifys)
            _mod_window.show()
        if _errors:
            _error_window = CheckerResultGUI()
            _error_window.setTableData(False, _errors)
            _error_window.show()
        do_check()

    def openHelp(self):
        """ヘルプサイト表示
        """
        gui_util.open_help_site()

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
                select_nodes.extend(x)

        if select_nodes:
            maya_utils.select_target(
                select_nodes, _select_flag, _focus_flag, _focus_outliner_flag)


def do_check():
    scene_path_obj = scene_data.SceneData()

    if not scene_path_obj.scene_name:
        _d = gui_util.ConformDialog(title="Not Open Scene",
                                    message="Open Scene File")
        _d.exec_()
        return

    if scene_path_obj.error:
        _d = gui_util.ConformDialog(title=scene_path_obj.error,
                                    message=scene_path_obj.error)
        _d.exec_()
        return

    _cheker = checker.Check()
    _cheker.check_start()
    result = _cheker.result_obj

    if result:
        _ck = CheckerGUI()
        _ck.setTableData(result, scene_path_obj)
        _ck.show()
    else:
        gui_util.close_pyside_windows([CHECKER_GUI_NAME,
                                       CHECKER_RESULT_GUI_NAME, ])
        _d = gui_util.ConformDialog(title="Not Fond Error",
                                    message="Not Found Error")
        _d.exec_()
        gui_util.open_export_window()


def main():
    gui_util.close_pyside_windows([CHECKER_GUI_NAME,
                                   CHECKER_RESULT_GUI_NAME, ])
    do_check()
