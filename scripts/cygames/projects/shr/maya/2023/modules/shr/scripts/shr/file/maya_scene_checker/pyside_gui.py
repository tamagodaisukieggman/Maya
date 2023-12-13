from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial
import importlib

from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

from ...utils import gui_util

from . import scene_data
from . import checker
from . import maya_utils
from . import settings

from . import CHECKER_GUI_NAME
from . import CHECKER_RESULT_GUI_NAME

# 開発中はTrue、リリース時にFalse
DEV_MODE = settings.load_config(config_name='DEV_MODE')

if DEV_MODE:
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

        gui_util.close_pyside_windows([CHECKER_GUI_NAME,
                                       CHECKER_RESULT_GUI_NAME,
                                        ])

        self.memory_nodes = list()
        self.results = None

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

    def setTableData(self, results:scene_data.ResultDatas=None, scene_path:scene_data.SceneData=None):
        """エラー内容をテーブルに表示

        Args:
            results ([ResultDataObj]): [description]. Defaults to None.
            scene_path:scene_data.SceneData ([SceneDataObj]): [description]. Defaults to None.
        """
        if not results or not scene_path:
            return

        self.results = results
        _result_datas = results.get_sort_data()
        title = 'DataType: [ {} ]  '

        if not scene_path:
            _t = title.format("unknown")
        else:
            _t = title.format(scene_path.data_type_category)

        _t += f' |   Total [ {len(_result_datas)} ] error and warning'
        self.setWindowTitle(_t)

        self.tableWidget.setRowCount(len(_result_datas))

        self.memory_nodes = list()
        for row, result in enumerate(_result_datas):
            result:scene_data.ResultData = result
            ann = "None"
            button_name = ""

            text = str(result.error_text)
            error = str(result.error_type_message)
            node = result.error_nodes
            error_type_color = result.error_type_color
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

            item_b.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setColumnWidth(0, 350)
            item_b.setBackground(QtGui.QColor(error_type_color[0], error_type_color[1], error_type_color[2]))

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
        recheckButton = QtWidgets.QPushButton("Repair and reinspection")
        openExportWindowButton = QtWidgets.QPushButton("Open Export Window")

        # FIXME: エクスポータが決まったらボタンの有効化
        openExportWindowButton.setEnabled(False)

        buttonLayout.addWidget(recheckButton)
        buttonLayout.addWidget(openExportWindowButton)

        mainLayout.addLayout(checkBoxLayout)
        mainLayout.addWidget(tableWidget)
        mainLayout.addLayout(buttonLayout)

        recheckButton.clicked.connect(partial(self.modifyData))

        wrapper.setLayout(mainLayout)

        maya_utils.attach_job(self.objectName(),
                                partial(gui_util.close_pyside_windows,[CHECKER_GUI_NAME,
                                                                CHECKER_RESULT_GUI_NAME,
                                                                ]))


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

        _cheker = checker.Checker()
        modify_messages = _cheker.modify_data(result_all=self.results)

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
        else:
            main()

    def openHelp(self):
        """ヘルプサイト表示
        """
        maya_utils.open_help_site()

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

def main():
    scene_path_obj = scene_data.SceneData()
    if not scene_path_obj.scene_name:
        _d = gui_util.ConformDialog(title="Not Open Scene",
                                    message="Open Scene File")
        _d.exec_()
        return

    _cheker = checker.Checker()
    _cheker.do_check()
    if _cheker.result:
        _gui = CheckerGUI()
        _gui.setTableData(_cheker.result, _cheker.scene_path)
        _gui.show()
    else:
        _d = gui_util.ConformDialog(title="Not Fond Error",
                                    message="Not Found Error")
        _d.exec_()
        gui_util.close_pyside_windows([CHECKER_GUI_NAME])

