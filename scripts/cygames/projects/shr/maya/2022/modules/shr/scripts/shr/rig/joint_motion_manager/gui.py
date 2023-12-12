from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial

import json
import os
import importlib
from pathlib import Path

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import QBrush, QColor, QIcon, QPainter, QPixmap
from PySide2.QtUiTools import QUiLoader

from ...utils import getCurrentSceneFilePath
from . import command
from . import TITLE
from . import NAME

CLASS_NAME = "".join(TITLE.split())


# 開発中はTrue、リリース時にFalse
DEV_MODE = True

if DEV_MODE:
    importlib.reload(command)
else:
    from . import logger

file_directory = os.path.dirname(__file__)
UI_FILE = os.path.join(file_directory, f'{NAME}.ui').replace(os.sep, '/')

ICON_DIRECTORY = Path(r'C:\cygames\shrdev\shr\tools\in\ext\maya\2022\modules\shr\scripts\shr\rig\joint_motion_manager\imgaes')
P4_ICON_DIRECTORY = Path(r'C:\cygames\shrdev\shr\tools\in\ext\maya\2022\modules\shr\scripts\shr\rig\joint_motion_manager\icons')
SAVE_DIRECTORY = NAME


class FileIconProvider(QtWidgets.QFileIconProvider):
    def icon(self, fileInfo):
        pixmap = QtGui.QPixmap(str(P4_ICON_DIRECTORY / 'add.png'))
        _icon = QtCore.QFileInfo(str(P4_ICON_DIRECTORY / 'add.png'))
        if isinstance(fileInfo, QtCore.QFileInfo):
            # if fileInfo.suffix() and fileInfo.suffix() == "json":
            print(_icon.filePath())
            return QtGui.QIcon(_icon.filePath())
            # return super(FileIconProvider, self).icon(_icon)


class ConformDialogResult(QtWidgets.QDialog):
    """[summary]

    Args:
        QtWidgets ([type]): [description]

    使い方例
    _m = u"マテリアルをアサインする対象が選ばれておりません\n"
    _m += u"マテリアルアサインをせずにマテリアルを生成しますか？"
    _d = ConformDialogResult(title=u"マテリアル生成",
                    message=_m)
    result = _d.exec_()
    if not result:
        return

    """

    def __init__(self, *args, **kwargs):
        super(ConformDialogResult, self).__init__(
            parent=kwargs.setdefault('parent', None),
            f=QtCore.Qt.WindowFlags())

        self.setWindowTitle(kwargs.setdefault('title', ''))

        main_layout = QtWidgets.QVBoxLayout()
        btn_layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(kwargs.setdefault('message', ''))
        self._ok_btn = QtWidgets.QPushButton('OK')
        self._cancel_btn = QtWidgets.QPushButton('Cancel')

        main_layout.addWidget(label)
        main_layout.addLayout(btn_layout)
        btn_layout.addWidget(self._ok_btn)
        btn_layout.addWidget(self._cancel_btn)
        self.setLayout(main_layout)

        self._ok_btn.clicked.connect(self._ok_btn_clicked)
        self._cancel_btn.clicked.connect(self._cancel_btn_clicked)

    def _ok_btn_clicked(self, *args):
        self.close()
        self.setResult(True)

    def _cancel_btn_clicked(self, *args):
        self.close()
        self.setResult(False)


class ConformDialog(QtWidgets.QDialog):
    """[summary]

    Args:
        QtWidgets ([type]): [description]

    使い方例
    _d = ConformDialog(title=u"一覧から選択してください",
                    message=u"マテリアルに適用するテクスチャを選択してから実行してください")
    _d.exec_()
    return
    """

    def __init__(self, *args, **kwargs):
        super(ConformDialog, self).__init__(
            parent=kwargs.setdefault('parent', None),
            f=QtCore.Qt.WindowFlags())

        self.setWindowTitle(kwargs.setdefault('title', ''))

        _label = QtWidgets.QLabel(kwargs.setdefault('message', ''))

        _btn = QtWidgets.QPushButton("OK")
        _btn.clicked.connect(self._btn_clicked)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(_label)
        layout.addWidget(_btn)
        self.setLayout(layout)

    def _btn_clicked(self, *args):
        self.close()
        self.setResult(False)


class DoubleSlider(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(float)

    def __init__(self, *args, **kwargs):
        super(DoubleSlider, self).__init__(*args, **kwargs)
        self.material = None
        self.attr = None

        self.attribute = None
        self.attributes = None
        self.nodes = None
        self._default_value = 0.0

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.__doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.__doubleSpinBox.setMinimumWidth(50)

        self.__doubleSpinBox.setSingleStep(0.01)
        self.__doubleSpinBox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons)
        layout.addWidget(self.__doubleSpinBox)

        self.__slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.__updateSliderRange()

        self.__to_default_button = QtWidgets.QPushButton(self)
        self.__to_default_button.setText("to Defult")

        layout.addWidget(self.__slider)
        layout.addWidget(self.__to_default_button)

        self.__to_default_button.clicked.connect(self.setToDefaultValue)
        self.__doubleSpinBox.valueChanged[float].connect(
            self.valueChangedCallback)
        self.__slider.valueChanged[int].connect(self.valueChangedCallback)

        # スライダーの変更をUndo で一気に戻すための機構
        self.__slider.sliderPressed.connect(self.dragStart)
        self.__slider.sliderReleased.connect(self.dragStop)

    def setAttributeValue(self, nodes=[], attribute="", default_value=0.0):
        """アトリビュートの設定
        移動値の範囲: -20 20
        回転値の範囲: -90 90
        スケール値の範囲: 0 2
        Args:
            nodes (list): maya transform nodes
            attribute (str): transform attribute(t, r, s)
            default_value (float): attribute value
        """
        self.nodes = nodes
        self.attribute = attribute
        self._default_value = default_value
        if attribute[0] == "t":
            self.setRange(self._default_value-20, self._default_value+20)
        elif attribute[0] == "r":
            self.setRange(self._default_value-180, self._default_value+180)
        elif attribute[0] == "s":
            self.setRange(0, 2)

    def setToDefaultValue(self):
        """デフォルト値に戻す
        """
        self.setValue(self._default_value)

    def slider_value_change(self, value):
        """スライダの値変更

        Args:
            value (float):
        """
        command.attribute_value_chane(self.nodes, self.attribute, value)

    def valueChangedCallback(self, value):
        sender = self.sender()
        if sender == self.__doubleSpinBox:
            self.__slider.blockSignals(True)
            self.__slider.setValue(value*self.__boost)
            self.__slider.blockSignals(False)

        elif sender == self.__slider:
            value = float(value)/self.__boost
            self.__doubleSpinBox.blockSignals(True)
            self.__doubleSpinBox.setValue(value)
            self.__doubleSpinBox.blockSignals(False)

        self.slider_value_change(value)
        self.valueChanged.emit(value)

    def value(self):
        return self.__doubleSpinBox.value()

    def setValue(self, value):
        self.__doubleSpinBox.setValue(value)

    def setRange(self, min, max):
        self.__doubleSpinBox.setRange(min, max)
        self.__updateSliderRange()

    def setDecimals(self, prec):
        self.__doubleSpinBox.setDecimals(prec)
        self.__updateSliderRange()

    def __updateSliderRange(self):
        decimals = self.__doubleSpinBox.decimals()
        minimum = round(self.__doubleSpinBox.minimum())
        maximum = round(self.__doubleSpinBox.maximum())
        self.__boost = int('1'+('0'*decimals))
        self.__slider.setRange(minimum*self.__boost, maximum*self.__boost)

    def dragStart(self):
        command.undo_info_open_chunk()

    def dragStop(self):
        command.undo_info_close_chunk()


class JointMotionManager(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    cbox_default = " --- "

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self._clearMemory()
        self._setWindowSize()

        self.r_to_l_flag = True
        self.thumbnail_paths = ''
        self.scene_path = ''
        self.work_dir = ''
        self.json_files = list()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        loader = QUiLoader()
        self.UI = loader.load(UI_FILE)
        self.resize(400, 500)
        self.setWindowTitle(TITLE)
        self.setCentralWidget(self.UI)

        self._appendMenu()
        self._setIcons()
        self._setConnections()

        self._construction()

        self._setWindowSize()
        self._resetSettings()

        command.attach_job(self.objectName(), self._resetSettings)

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
        fileInfo にデータ書き込み
        ファイルパスとスライダ情報
        """
        super(self.__class__, self).closeEvent(event)
        self._settings.setValue(f'{self.__class__.__name__}geometry', self.saveGeometry())
        self._setFileInfoData()

    def _setFileInfoData(self):
        """fileInfo にデータ格納
        """
        if self.work_dir:
            command.set_file_info_data("SAVE_DIRECTORY", str(self.work_dir).replace(os.sep, '/'))
        if self.node_attribute_default_values:
            command.set_file_info_data("NODE_ATTRIBUTE_VALUES", json.dumps(self.node_attribute_default_values))
        else:
            command.set_file_info_data("NODE_ATTRIBUTE_VALUES", "")

    def _setFileListTableView(self):
        """リストテーブル作成
        """
        self.fileSystemModel = QtWidgets.QFileSystemModel()
        self.fileSystemModel.setRootPath(str(self.work_dir).replace(os.sep, '/'))
        self.fileSystemModel.setFilter(QtCore.QDir.Files)

        self.fileSystemModel.setNameFilters(['*.json'])
        self.fileSystemModel.setNameFilterDisables(False)
        self.UI.fileListTableView.setModel(self.fileSystemModel)
        self.UI.fileListTableView.setRootIndex(
            self.fileSystemModel.index(str(self.work_dir).replace(os.sep, '/')))
        self.UI.fileListTableView.verticalHeader().hide()
        self.UI.fileListTableView.horizontalHeader().hide()
        self.UI.fileListTableView.setSortingEnabled(False)
        self.UI.fileListTableView.setColumnHidden(1, True)
        self.UI.fileListTableView.setColumnHidden(2, True)
        self.UI.fileListTableView.setColumnHidden(3, True)
        self.UI.fileListTableView.setColumnWidth(0, 200)
        self.UI.fileListTableView.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.UI.fileListTableView.setFixedWidth(200)

        self.UI.fileListTableView.setSelectionBehavior(
                                        self.UI.fileListTableView.SelectRows)
        self.UI.fileListTableView.setContextMenuPolicy(
                                        QtCore.Qt.CustomContextMenu)

        # ダブルクリックを使うと二度実行されるのでオミットしている
        # self.UI.fileListTableView.doubleClicked.connect(partial(self.importJointAnimation))

    def _clickTest(self):
        selectTableIndexes = self.UI.fileListTableView.selectedIndexes()
        if not selectTableIndexes:
            return
        selectTableIndex = selectTableIndexes[0]
        fileIcon = self.fileSystemModel.data(selectTableIndex, 1)
        filePath = self.fileSystemModel.filePath(selectTableIndex)
        print(filePath)

    def buildRightClickMenu(self):
        """右クリックしたときに表示させるメニュー
        """
        self.replace_menu = QtWidgets.QMenu(self)

        action1 = QtWidgets.QAction(u"{}".format("test1"), self)
        action2 = QtWidgets.QAction(u"{}".format("test2"), self)
        action3 = QtWidgets.QAction(u"{}".format("test3"), self)

        self.replace_menu.addAction(action1)
        self.replace_menu.addAction(action2)
        self.replace_menu.addAction(action3)

    def contextMenu(self, point):
        """右クリック用の仕込み（使っていない）

        Args:
            point (_type_): _description_
        """
        _add = QtCore.QPoint(40, 40)
        self.replace_menu.exec_(_add+self.mapToGlobal(point))

    def _setConnections(self, *args):
        """UI のコネクション接続
        """
        self.UI.getNewestPushButton.clicked.connect(partial(self.getNewstFiles))
        self.UI.submitPushButton.clicked.connect(partial(self.submitFiles))

        self.UI.saveButton.clicked.connect(partial(self.saveJointAnimation))
        self.UI.importButton.clicked.connect(partial(self.importJointAnimation))

        self.UI.mirrorKeyframeButton.clicked.connect(partial(self.mirrorKeyframe))

        self.UI.gotoZeroframeButton.clicked.connect(partial(self.gotoZeroframe))
        self.UI.timePrevPushButton.clicked.connect(partial(command.goto_previous_keyframe))
        self.UI.timeNextPushButton.clicked.connect(partial(command.goto_next_keyframe))

        self.UI.removeKeyframeButton.clicked.connect(partial(self.removeKeyframe))
        self.UI.setKeyframeAllButton.clicked.connect(partial(self.setKeyframeAll))
        self.UI.addAllKeyframeToStartTimePushButton.clicked.connect(partial(self.allKeyframeToStartTime))
        self.UI.deleteKeyButton.clicked.connect(partial(self.deleteKeyframe))

        self.UI.createDragSliderPushButton.clicked.connect(
            partial(self._createDragSlider))
        self.UI.clearAllDragSliderPudhButton.clicked.connect(
            partial(self._clearAllDragSlider))

    def _setIcons(self):
        """UI のアイコンを設定
        """
        submit_icon = QtGui.QIcon(str(P4_ICON_DIRECTORY / 'p4_submit.png').replace(os.sep, '/'))
        getnewest_icon = QtGui.QIcon(str(P4_ICON_DIRECTORY / 'p4_getnewest.png').replace(os.sep, '/'))
        save_icon = QtGui.QIcon(str(ICON_DIRECTORY / 'save.png').replace(os.sep, '/'))
        self.r_to_l_icon = QtGui.QIcon(str(ICON_DIRECTORY / 'RtoL.png').replace(os.sep, '/'))
        self.l_to_r_icon = QtGui.QIcon(str(ICON_DIRECTORY / 'LtoR.png').replace(os.sep, '/'))

        setKeyframe_icon = QtGui.QIcon(':/setKeyframe.png')

        timerew_icon = QtGui.QIcon(':/timerew.png')
        timeprev_icon = QtGui.QIcon(':/timeprev.png')
        timenext_icon = QtGui.QIcon(':/timenext.png')
        removeKeyframe_icon = QtGui.QIcon(str(ICON_DIRECTORY / 'removeKeyframe.png').replace(os.sep, '/'))

        self.UI.submitPushButton.setIcon(submit_icon)
        self.UI.getNewestPushButton.setIcon(getnewest_icon)
        self.UI.saveButton.setIcon(save_icon)
        self.UI.mirrorKeyframeButton.setIcon(self.r_to_l_icon)
        self.UI.gotoZeroframeButton.setIcon(timerew_icon)
        self.UI.timePrevPushButton.setIcon(timeprev_icon)
        self.UI.timeNextPushButton.setIcon(timenext_icon)
        self.UI.setKeyframeAllButton.setIcon(setKeyframe_icon)
        self.UI.deleteKeyButton.setIcon(removeKeyframe_icon)

    def _clearMemory(self):
        """メモリクリア
        """
        self.node_attribute_default_values = {}
        self.slider_remove_button = {}
        self.sliders = {}
        self.boxs = {}

    def _openExploer(self, *args):
        """Windows Exploer で表示させる
        """
        command.open_exploer(self.work_dir)

    def _openHelp(self, *args):
        """ヘルプサイト表示
        """
        command.open_help_site()

    def _construction(self):
        """命名規則の仕様が決まれば機能を実装
        """
        self.UI.getNewestPushButton.setEnabled(False)
        self.UI.submitPushButton.setEnabled(False)

    def _appendMenu(self):
        """ファイルメニュー、ヘルプメニューを作成
        """
        menuBar = self.menuBar()

        openDirectory = QtWidgets.QAction('Open Save Directory ...', self)
        openDirectory.triggered.connect(self._openExploer)

        setDirectory = QtWidgets.QAction('Set Save Directory ...', self)
        setDirectory.triggered.connect(self._openFileBrowser)

        openAct = QtWidgets.QAction('Open Help Site ...', self)
        openAct.triggered.connect(self._openHelp)

        fileMenu = menuBar.addMenu('File')
        helpMenu = menuBar.addMenu('Help')

        fileMenu.addAction(openDirectory)
        fileMenu.addAction(setDirectory)
        helpMenu.addAction(openAct)

    def _openFileBrowser(self):
        """フォルダ選択ダイアログ表示
        """
        directory_path = self.work_dir
        dialog = QtWidgets.QFileDialog(directory=str(directory_path))
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        if dialog.exec_():
            path = dialog.selectedFiles()[0]
            self.work_dir = Path(path)
            self._setFileListTableView()

    def _resetSettings(self):
        """設定のリセット
        新規シーン、シーンを開いた場合に発動
        """
        self.work_dir = ""
        self.scene_path = ""
        self.scene_basename = ""

        self._getFileInfoData()
        self._getSceneName()

        self._setFileListTableView()

    def _createDirectory(self, create=True):
        self.work_dir = command.create_work_directory(self.scene_path, create=create)
        self._setFileListTableView()

    def _getSceneName(self):
        """シーン名取得
        """
        scene_path = getCurrentSceneFilePath()
        if scene_path:
            scene_path = Path(scene_path)
            self.scene_basename = scene_path.name
            self.scene_path = scene_path.parent
            self._createDirectory(create=True)

    def _getFileInfoData(self):
        """fileInfo のデータ取得
        """
        _info_data = command.get_file_info_data("SAVE_DIRECTORY")

        if _info_data:
            self.work_dir = Path(_info_data[0])

        _info_data = command.get_file_info_data("NODE_ATTRIBUTE_VALUES")

        if _info_data and _info_data[0]:
            _info_data = _info_data[0].replace("\\", "")
            if _info_data:
                self.node_attribute_default_values = json.loads(_info_data)
                self._createDragSlider(fromSelection=False)
        else:
            self._clearAllDragSlider(True)

    def submitFiles(self, *args):
        """json ファイルのサブミット
        """
        other_user_check_out_files = {}
        edit_files = []
        add_files = []
        command.get_newest_file(self.work_dir)
        file_states = command.check_p4_file_statuses(self.work_dir)

        for _file, (status, current_users) in file_states.items():
            if not status:
                add_files.append(_file)
            elif status == 'other':
                _users = u", ".join(current_users)
                other_user_check_out_files[_file] = _users
            elif status != "checkout":
                edit_files.append(_file)

        if other_user_check_out_files:
            _m = '以下のファイルがチェックアウトされていました\n\n'
            for _file_path, users in other_user_check_out_files.items():
                _m += f'ユーザー：[ {users} ] :[ {_file_path} ]'

            _d = ConformDialog(title=TITLE, message='チェックアウトされているファイルがあります')
            _d.exec_()
            return

        if add_files and command.add_p4_files(add_files):
            edit_files.extend(add_files)

        if edit_files:
            if command.check_out_p4_files(edit_files):
                _m = '{}'.format("\n".join(edit_files))
                _m += '\n\nのファイルをサブミットします、よろしいですか？'

                _d = ConformDialogResult(title=TITLE, message=_m)
                result = _d.exec_()
                if not result:
                    return

                if not command.submit_p4_files(edit_files):
                    _d = ConformDialog(
                        title=TITLE,
                        message='サブミットに失敗しました'
                    )
                    _d.exec_()
            else:
                _d = ConformDialog(
                    title=TITLE,
                    message='チェックアウトに失敗しました'
                )
                _d.exec_()

    def getNewstFiles(self, *args):
        """保存ディレクトリのP4 の最新取得
        """
        _m = f'[ {self.work_dir} ]\n\n'
        _m += '以下の最新を取得します　よろしいですか？'
        _d = ConformDialogResult(title='最新データ取得',
                                 message=_m)
        result = _d.exec_()
        if not result:
            return

        json_file_exists_flag = command.get_newest_file(self.work_dir)

        self.readMotionFiles()

    def readMotionFiles(self):
        """json ファイルを読み込み
        サムネイル取得
        コンボボックスに追加
        """
        self.json_files = command.get_json_files(self.work_dir)
        if self.json_files:
            self.buildFileListTableView()

    def getSelectNodeAttribute(self, *args):
        """現在選択されているジョイントと
        アクティブな軸の取得
        """

        attributes = None
        nodes = command.get_selection_nodes()
        if not nodes:
            return

        _type, axis = command.get_active_handle()

        if not _type or not axis:
            return

        attributes = f'{_type}{axis}'

        node = nodes.split(",")[0]
        _exists_name = f'{nodes};{attributes}'
        _exists = self.node_attribute_default_values.get(_exists_name)
        if not _exists:
            _default_value = command.get_default_value(node, attributes)
            self.node_attribute_default_values[_exists_name] = _default_value

    def _createDragSlider(self, fromSelection=True):
        """ドラッグスライダー作成
        """
        if fromSelection:
            self.getSelectNodeAttribute()

        if not self.node_attribute_default_values:
            return
        self._clearAllDragSlider(False)

        for nodes_str_attr, value in self.node_attribute_default_values.items():
            nodes_str, attribute = nodes_str_attr.split(";")
            nodes = command.str_to_list(nodes_str)

            _exist_flag = True

            short_names = []
            for node in nodes:
                if not node:
                    continue
                short_name = node.split("|")[-1]
                short_names.append(short_name)
                if not command.check_node_exists(node):
                    _exist_flag = False

            if not _exist_flag:
                continue

            _box = QtWidgets.QGroupBox(f'{short_names[0]}')
            layout = QtWidgets.QHBoxLayout()
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setSpacing(10)

            _slider = DoubleSlider()
            _slider.setAttributeValue(nodes, attribute, value)
            _value = command.get_default_value(node, attribute)
            _slider.setValue(_value)

            _remove_button = QtWidgets.QPushButton()
            _remove_button.setMaximumSize(22, 22)
            _remove_button.clicked.connect(
                partial(self._removeSlider, nodes_str_attr))
            image = QtGui.QIcon(':/nodeGrapherClose.png')
            _remove_button.setIcon(image)

            layout.addWidget(_remove_button)
            layout.addWidget(_slider)

            _box.setLayout(layout)
            self.UI.sliderVerticalLayout.addWidget(_box)
            self.slider_remove_button[_box] = nodes_str_attr
            self.sliders[nodes_str_attr] = _slider
            self.boxs[nodes_str_attr] = _box

        verticalSpacer = QtWidgets.QSpacerItem(20, 40,
                                               QtWidgets.QSizePolicy.Minimum,
                                               QtWidgets.QSizePolicy.Expanding)

        self.UI.sliderVerticalLayout.addItem(verticalSpacer)

    def _removeSlider(self, *args):
        """スライダー削除
        """
        nodes_str_attr = args[0]
        _slider = self.sliders.get(nodes_str_attr)
        _value = self.node_attribute_default_values.get(nodes_str_attr)

        if not _slider and _value:
            return

        _slider.setValue(_value)
        _box = self.boxs.get(nodes_str_attr)
        if not _box:
            return

        del self.boxs[nodes_str_attr]
        del self.sliders[nodes_str_attr]
        del self.slider_remove_button[_box]
        del self.node_attribute_default_values[nodes_str_attr]

        self._setFileInfoData()
        _box.deleteLater()

    def _clearAllDragSlider(self, clear_flag=True):
        """ドラッグスライダー全クリア

        Args:
            clear_flag (bool): メモリクリアフラグ
        """
        for i in reversed(range(self.UI.sliderVerticalLayout.count())):
            _widget = self.UI.sliderVerticalLayout.itemAt(i)
            if isinstance(_widget, QtWidgets.QSpacerItem):
                self.UI.sliderVerticalLayout.removeItem(_widget)
            else:
                if clear_flag:
                    nodes_str_attr = self.slider_remove_button.get(
                        _widget.widget())
                    _slider = self.sliders.get(nodes_str_attr)

                    if _slider and nodes_str_attr:
                        _value = self.node_attribute_default_values.get(
                            nodes_str_attr)
                        _slider.setValue(_value)
                _widget.widget().deleteLater()

        if clear_flag:
            self._clearMemory()
        self._setFileInfoData()

    def deleteKeyframe(self, *args):
        """カレントのキーフレーム削除
        """
        joint_anim_dict = command.get_joints_animation()
        if not joint_anim_dict:
            return
        command.delete_keyframe(joint_anim_dict)
        if not DEV_MODE:
            logger.info("delete keyframe")

    def allKeyframeToStartTime(self, *args):
        command.all_keyframe_alljoints()

    def setKeyframeAll(self, *args):
        """カレントにキーフレーム設定
        """
        command.set_keyframe_alljoints()
        if not DEV_MODE:
            logger.info("set keyframe")

    def gotoZeroframe(self, *args):
        """カレントをゼロフレームに
        """
        command.goto_zero_frame()

    def mirrorKeyframe(self, *args):
        """ミラーコピー実行
        """
        command.mirror_keyframe()
        if not DEV_MODE:
            logger.info("mirror keyframe")

    def removeKeyframe(self, *args):
        """ジョイントのキーフレーム全削除
        """
        command.remove_joint_keyframe()

    def importJointAnimation(self, *args):
        """ジョイントアニメーションの読み込み
        """

        selectedListTableIndexes = self.UI.fileListTableView.selectedIndexes()
        if not selectedListTableIndexes:
            return
        currentAnimationFile = self.fileSystemModel.filePath(selectedListTableIndexes[0])

        onlyRotateFlag = self.UI.onlyRotateCheckBox.isChecked()

        command.read_json_file(currentAnimationFile, onlyRotateFlag)

    def saveJointAnimation(self, *args):
        """ジョイントに設定されているアニメーション情報の保存
        """
        joint_anim_dict = command.get_joints_animation()

        if not joint_anim_dict:
            return

        current_file_name = command.save_json_file(
            self.work_dir,
            self.scene_path,
            joint_anim_dict
        )

        if not DEV_MODE:
            logger.info("save joint motion")




def main():
    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == CLASS_NAME:
            _obj.close()
            del _obj

    if not command.check_path_exists(path=UI_FILE):
        return

    if not DEV_MODE:
        logger.send_launch(u'ツール起動')

    ui = JointMotionManager()
    ui.show()
