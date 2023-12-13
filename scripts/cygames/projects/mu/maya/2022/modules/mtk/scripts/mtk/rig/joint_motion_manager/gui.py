from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial

import os
import importlib

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin


from . import command
from . import TITLE
from . import NAME

CLASS_NAME = "".join(TITLE.split())


# 検証データ
# z:\mtk\work\resources\characters\player\00\000\model\mdl_ply00_m_000.ma


# 開発中はTrue、リリース時にFalse
DEV_MODE = False

if DEV_MODE:
    importlib.reload(command)
else:
    from . import logger

UI_FILE_NAME = "{}.ui".format(NAME)
UI_FILE = os.path.join(os.path.dirname(__file__),
                       UI_FILE_NAME).replace(os.sep, '/')

# SAVE_DIRECTORY = r"Z:\mtk\tools\maya\modules\mtku\scripts\mtku\maya\menus\animation\joint_motion_manager\test"
# SAVE_DIRECTORY = r"\\CGS-STR-PRI01-M\mutsunokami_storage\30_design\chara\00_user\22_TA\00_backup"
SAVE_DIRECTORY = os.path.join(os.environ["HOME"], NAME)


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

    def setAttributeValue(self, nodes=[], attribute="", default_value=0.0):
        """アトリビュートの設定
        移動値の範囲：-20 20
        回転値の範囲：-90 90
        スケール値の範囲：0 2
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
            self.setRange(self._default_value-90, self._default_value+90)
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


class JointMotionManager(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    cbox_default = " --- "

    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.clearMemory()

        self.r_to_l_flag = True
        self.thumbnail_paths = None
        self.root_path = None
        self.save_path = None
        self.json_files = list()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        loader = QUiLoader()

        self.UI = loader.load(UI_FILE)

        menuBar = self.menuBar()
        menu = menuBar.addMenu('Help')
        openAct = QtWidgets.QAction('Help Site...', self)
        openAct.triggered.connect(self.openHelp)
        menu.addAction(openAct)

        folder_open = QtGui.QIcon(':/folder-open.png')
        set_directory_icon = QtGui.QIcon(
            r"Z:\mtk\tools\maya\2022\modules\mtk\scripts\mtk\rig\joint_motion_manager\imgaes\set_directory.png")
        submit_icon = QtGui.QIcon(
            r"Z:\mtk\tools\maya\2022\modules\mtk\scripts\mtk\rig\joint_motion_manager\imgaes\p4_submit.png")
        getnewest_icon = QtGui.QIcon(
            r"Z:\mtk\tools\maya\2022\modules\mtk\scripts\mtk\rig\joint_motion_manager\imgaes\p4_getnewest.png")
        save_icon = QtGui.QIcon(
            r"Z:\mtk\tools\maya\2022\modules\mtk\scripts\mtk\rig\joint_motion_manager\imgaes\save.png")
        self.r_to_l_icon = QtGui.QIcon(
            r"Z:\mtk\tools\maya\2022\modules\mtk\scripts\mtk\rig\joint_motion_manager\imgaes\RtoL.png")
        self.l_to_r_icon = QtGui.QIcon(
            r"Z:\mtk\tools\maya\2022\modules\mtk\scripts\mtk\rig\joint_motion_manager\imgaes\LtoR.png")

        self.UI.openExplorerPushButton.setIcon(folder_open)
        self.UI.setDirectoryPushButton.setIcon(set_directory_icon)
        self.UI.submitPushButton.setIcon(submit_icon)
        self.UI.getNewestPushButton.setIcon(getnewest_icon)
        self.UI.saveButton.setIcon(save_icon)
        self.UI.mirrorKeyframeButton.setIcon(self.r_to_l_icon)

        self.UI.openExplorerPushButton.clicked.connect(
            partial(self.openExploer))
        self.UI.motionListComboBox.currentIndexChanged.connect(
            partial(self.changeComboBox))
        self.UI.setDirectoryPushButton.clicked.connect(
            partial(self.setRootDirectory))
        self.UI.getNewestPushButton.clicked.connect(
            partial(self.getNewstFiles))
        self.UI.saveButton.clicked.connect(partial(self.saveJointAnimation))
        self.UI.importButton.clicked.connect(
            partial(self.importJointAnimation))
        self.UI.removeKeyframeButton.clicked.connect(
            partial(self.removeKeyframe))
        # self.UI.removeSelectButton.clicked.connect(partial(self.removeComboBoxMenu))
        self.UI.mirrorKeyframeButton.clicked.connect(
            partial(self.mirrorKeyframe))
        self.UI.gotoZeroframeButton.clicked.connect(
            partial(self.gotoZeroframe))
        self.UI.setKeyframeAllButton.clicked.connect(
            partial(self.setKeyframeAll))
        self.UI.deleteKeyButton.clicked.connect(partial(self.deleteKeyframe))
        self.UI.submitPushButton.clicked.connect(partial(self.submitFiles))
        self.UI.l_r_changeCheckBox.clicked.connect(
            partial(self.changeLRswitchCheckBox))

        self.UI.createDragSliderPushButton.clicked.connect(
            partial(self.createDragSlider))
        self.UI.clearAllDragSliderPudhButton.clicked.connect(
            partial(self.clearAllDragSlider))

        self.resize(700, 450)
        self.setWindowTitle(TITLE)
        self.setCentralWidget(self.UI)

        self.initUI()

        command.attach_job(self.objectName(), self.initUI)

    def initUI(self):
        self.clearAllDragSlider
        self.getRootPath()
        self.readMotionFiles()

    def submitFiles(self, *args):
        """json ファイルのサブミット
        """
        other_user_check_out_files = {}
        edit_files = []
        add_files = []
        command.get_newest_file(self.save_path)
        file_states = command.check_p4_file_statuses(self.save_path)

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

    def openHelp(self, *args):
        """ヘルプサイト表示
        """
        command.open_help_site()

    def getRootPath(self, *args):
        """保存するディレクトリ取得
        """
        self.get_scene_name()
        self.root_path = command.get_root_directory()
        self.save_path = command.get_save_directory(self.root_path)

    def setRootDirectory(self, *args):
        """ファイルダイアログを開いてディレクトリ指定
        """
        # self.getRootPath()

        dialog = QtWidgets.QFileDialog(directory=self.root_path)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        if dialog.exec_():
            _path = dialog.selectedFiles()[0]
            if not command.check_model_directory(_path):
                _m = f'{_path}\n以下に [ model ] フォルダがありません'
                _m += '\nルートディレクトリには設定できません'
                _d = ConformDialog(
                    title=TITLE,
                    message=_m
                )
                _d.exec_()
                return

            _m = f'{_path}\nをルートディレクトリと設定します\nよろしいですか？'
            _d = ConformDialogResult(title=TITLE, message=_m)
            result = _d.exec_()

            if not result:
                return

            self.root_path = _path
            self.save_path = command.get_save_directory(self.root_path)
            self.readMotionFiles()

    def getNewstFiles(self, *args):
        """保存ディレクトリのP4 の最新取得
        """
        _m = f'[ {self.save_path} ]\n\n'
        _m += '以下の最新を取得します　よろしいですか？'
        _d = ConformDialogResult(title='最新データ取得',
                                 message=_m)
        result = _d.exec_()
        if not result:
            return

        json_file_exists_flag = command.get_newest_file(self.save_path)

        self.readMotionFiles()

    def readMotionFiles(self):
        """json ファイルを読み込み
        サムネイル取得
        コンボボックスに追加
        """
        self.json_files = command.get_json_files(self.save_path)
        self.resetComboBox(False)
        if self.json_files:
            self.thumbnail_paths = command.get_thumbnail_paths(self.json_files)
            if self.thumbnail_paths:
                self.buildConboBox()

    def getSelectNodeAttribute(self, *args):
        """現在選択されているジョイントと
        アクティブな軸の取得
        """
        axis_dict = {
            0: "x",
            1: "y",
            2: "z",
        }
        attributes = None
        nodes = command.get_selection_nodes()
        if not nodes:
            _d = ConformDialog(title=u"選択ノードを確認してください",
                               message=u"ジョイントを選択してください")
            _d.exec_()
            return

        _type, axis = command.get_active_handle()

        axis = axis_dict.get(axis, None)
        if not _type:
            _d = ConformDialog(title=u"選択しているツールを確認してください",
                               message=u"[ 移動、回転、スケール ] ツールで実行してください")
            _d.exec_()
            return
        if not axis:
            _d = ConformDialog(title=u"選択の軸を確認してください",
                               message=u"ハンドルの軸を選択してください")
            _d.exec_()
            return

        attributes = f'{_type}{axis}'

        node = nodes.split(",")[0]
        _exists_name = f'{nodes};{attributes}'
        _exists = self.node_attribute_default_values.get(_exists_name)
        if not _exists:
            _default_value = command.get_default_value(node, attributes)
            self.node_attribute_default_values[_exists_name] = _default_value

    def createDragSlider(self, *args):
        """ドラッグスライダー作成
        """
        self.getSelectNodeAttribute()

        if not self.node_attribute_default_values:
            return
        self.clearAllDragSlider(False)

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
                partial(self.removeSlider, nodes_str_attr))
            image = QtGui.QIcon(':/nodeGrapherClose.png')
            _remove_button.setIcon(image)

            layout.addWidget(_slider)
            layout.addWidget(_remove_button)

            _box.setLayout(layout)
            self.UI.sliderVerticalLayout.addWidget(_box)
            self.slider_remove_button[_box] = nodes_str_attr
            self.sliders[nodes_str_attr] = _slider
            self.boxs[nodes_str_attr] = _box

        verticalSpacer = QtWidgets.QSpacerItem(20, 40,
                                               QtWidgets.QSizePolicy.Minimum,
                                               QtWidgets.QSizePolicy.Expanding)

        self.UI.sliderVerticalLayout.addItem(verticalSpacer)

    def clearMemory(self):
        """メモリクリア
        """
        self.node_attribute_default_values = {}
        self.slider_remove_button = {}
        self.sliders = {}
        self.boxs = {}

    def removeSlider(self, *args):
        """スライダー削除
        """
        # _slider = args[0]
        nodes_str_attr = args[0]
        _slider = self.sliders.get(nodes_str_attr)
        _value = self.node_attribute_default_values.get(nodes_str_attr)

        if not _slider and _value:
            return

        _slider.setValue(_value)
        _box = self.boxs.get(nodes_str_attr)
        if not _box:
            return
        _box.deleteLater()

        del self.boxs[nodes_str_attr]
        del self.sliders[nodes_str_attr]
        del self.slider_remove_button[_box]
        del self.node_attribute_default_values[nodes_str_attr]

    def clearAllDragSlider(self, clear_flag=True):
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
                # _widget.widget().setParent(None)

        if clear_flag:
            self.clearMemory()

    def changeLRswitchCheckBox(self, *args):
        """キーのミラーコピー時のLR反転
        デフォルト:R>L
        """
        l = 'L'
        r = 'R'
        _buttonMessage = f'[ {r} ] から [ {l} ] にキーフレームをコピー'

        _value = self.UI.l_r_changeCheckBox.isChecked()
        if _value:
            self.r_to_l_flag = False
            _buttonMessage = f'[ {l} ] から [ {r} ] にキーフレームをコピー'
            self.UI.mirrorKeyframeButton.setIcon(self.l_to_r_icon)
        else:
            self.UI.mirrorKeyframeButton.setIcon(self.r_to_l_icon)

        self.UI.mirrorKeyframeButton.setText(_buttonMessage)

    def deleteKeyframe(self, *args):
        """カレントのキーフレーム削除
        """
        joint_anim_dict = command.get_joints_animation()
        if not joint_anim_dict:
            return
        command.delete_keyframe(joint_anim_dict)
        if not DEV_MODE:
            logger.info("delete keyframe")

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
        joint_anim_dict = command.get_joints_animation()
        if not joint_anim_dict:
            return
        command.mirror_keyframe(joint_anim_dict, self.r_to_l_flag)
        if not DEV_MODE:
            logger.info("mirror keyframe")

    def removeComboBoxMenu(self, *args):
        """現在選ばれているコンボボックス削除
        """
        current_json_file_name = self.UI.motionListComboBox.currentText()
        if not current_json_file_name:
            return

        current_index = self.UI.motionListComboBox.currentIndex()

        if current_json_file_name == self.cbox_default:
            _m = u"[ {} ] は削除できません".format(self.cbox_default)
            _d = ConformDialog(title=TITLE,
                               message=_m)
            _d.exec_()
            return
        current_json_file_path = os.path.join(
            SAVE_DIRECTORY, current_json_file_name+".json")
        current_json_file_path = current_json_file_path.replace(os.sep, "/")

        if not command.check_path_exists(current_json_file_path):
            _d = ConformDialog(title=TITLE,
                               message=u"ファイル\n{}\nが見つかりません".format(current_json_file_path))
            _d.exec_()
            return

        _m = u"ジョイントアニメーション\n\n"
        _m += u"[ {} ]\n\n".format(current_json_file_name)
        _m += u"を削除します、よろしいですか？"
        _d = ConformDialogResult(title=TITLE,
                                 message=_m)
        result = _d.exec_()

        if result:
            if not command.remove_json_file(current_json_file_path):
                self.UI.motionListComboBox.removeItem(current_index)
                if current_index:
                    self.UI.motionListComboBox.setCurrentIndex(current_index-1)

    def removeKeyframe(self, *args):
        """ジョイントのキーフレーム全削除
        """
        _m = u"現在のシーンのジョイントに設定されているキーを全て削除します\n"
        _m += u"よろしいですか？"
        _d = ConformDialogResult(title=TITLE,
                                 message=_m)
        result = _d.exec_()

        if not result:
            return

        command.remove_joint_keyframe()

    def importJointAnimation(self, *args):
        """コンボボックスで選択されているファイルの読み込み
        """
        self.get_scene_name()

        if not command.check_path_exists(self.save_path):
            _d = ConformDialog(title=TITLE,
                               message=u"ディレクトリ\n{}\nが見つかりません".format(self.save_path))
            _d.exec_()
            return

        onlyRotateFlag = self.UI.onlyRotateCheckBox.isChecked()
        current_json_file_name = self.UI.motionListComboBox.currentText()
        if not current_json_file_name:
            return
        current_json_file_path = os.path.join(
            self.save_path, current_json_file_name+".json")
        current_json_file_path = current_json_file_path.replace(os.sep, "/")

        if not current_json_file_path and not os.path.exists(current_json_file_path):
            _m = u"モーションファイル\n[ {} ]\nが見つかりません".format(current_json_file_path)
            _d = ConformDialog(title=TITLE,
                               message=_m)
            _d.exec_()
            return

        _m = u"ジョイントアニメーション\n\n"
        _m += u"[ {} ]\n\n".format(current_json_file_name)
        _m += u"を読み込みます、よろしいですか？"
        _d = ConformDialogResult(title=TITLE,
                                 message=_m)
        result = _d.exec_()

        if not result:
            return

        apply_joints = command.read_json_file(
            current_json_file_path, onlyRotateFlag)
        if apply_joints:
            _m = u"[ {} ] 個のジョイントモーションを適用しました".format(len(apply_joints))
            if not DEV_MODE:
                logger.info("read joint motion")
        else:
            _m = u"ジョイントモーションを適用できる骨が見つかりませんでした"
        _d = ConformDialog(title=TITLE,
                           message=_m)
        _d.exec_()

    def saveJointAnimation(self, *args):
        """ジョイントに設定されているアニメーション情報の保存
        """
        self.get_scene_name()

        current_index = self.UI.motionListComboBox.currentIndex()
        current_text = self.UI.motionListComboBox.currentText()

        joint_anim_dict = command.get_joints_animation()

        if not joint_anim_dict:
            _m = u"シーンにあるジョイントにキーフレームアニメーションがありませんでした"
            _d = ConformDialog(title=TITLE,
                               message=_m)
            _d.exec_()
            return

        _m = u"ジョイントアニメーション"
        _m += u"を保存します、よろしいですか？"
        _d = ConformDialogResult(title=TITLE,
                                 message=_m)
        result = _d.exec_()

        if not result:
            return

        command.get_newest_file(self.save_path)
        current_file_name = command.save_json_file(
            self.save_path,
            self.scene_name,
            joint_anim_dict
        )

        if not DEV_MODE:
            logger.info("save joint motion")

        self.readMotionFiles()
        self.UI.motionListComboBox.setCurrentText(current_file_name)

    def resetComboBox(self, allClear=False):
        """コンボボックスクリア

        Args:
            allClear (bool): [description]. Defaults to False.
        """
        self.UI.motionListComboBox.clear()
        if not allClear:
            self.UI.motionListComboBox.addItem(self.cbox_default)

    def buildConboBox(self):
        """コンボボックス組み立て
        """
        self.resetComboBox(True)
        for basename, thumbnail_path in self.thumbnail_paths.items():
            self.UI.motionListComboBox.addItem(basename)

    def changeComboBox(self, *args):
        """コンボボックスを変更したときにサムネイルが
        存在すればそれを表示する
        """
        self.UI.imageLabel.setPixmap(None)

        if not self.thumbnail_paths:
            return

        _current_preset = self.UI.motionListComboBox.currentText()
        if not _current_preset:
            return

        _current_thumbnail_path = self.thumbnail_paths.get(
            _current_preset, None)

        if _current_thumbnail_path and os.path.exists(_current_thumbnail_path):
            pixMap = QtGui.QPixmap(_current_thumbnail_path)
            self.UI.imageLabel.setPixmap(pixMap)

    def get_scene_name(self, *args):
        """シーン名を取得
        """
        self.scene_name, self.scene_path, self.scene_basename = command.get_scene_name()

    def openExploer(self, *args):
        """Windows Exploer で表示させる
        """
        if not command.check_path_exists(self.save_path):
            _d = ConformDialog(title=TITLE,
                               message=u"ディレクトリ\n{}\nが見つかりません".format(self.save_path))
            _d.exec_()
            return
        command.open_exploer(self.save_path)

        if not DEV_MODE:
            logger.info("open exploer")


def main():
    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == CLASS_NAME:
            _obj.close()
            del _obj

    if not command.check_path_exists(UI_FILE):
        return

    if not DEV_MODE:
        logger.send_launch(u'ツール起動')

    ui = JointMotionManager()
    ui.show()
