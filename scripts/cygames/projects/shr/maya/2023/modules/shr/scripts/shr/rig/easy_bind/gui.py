from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial
import os
import importlib
import webbrowser
from pathlib import Path

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from ...utils import getCurrentSceneFilePath

import tool_log
from . import command
from . import TITLE
from . import NAME
from . import WEIGHT_FILE_FORMAT
from . import PROJECT_WEIGHT_FILE_FORMAT
from . import tool_version


CLASS_NAME = "".join(TITLE.split())

# 開発中はTrue、リリース時にFalse
DEV_MODE = command.load_config('DEV_MODE')

if DEV_MODE:
    importlib.reload(command)

file_directory = os.path.dirname(__file__)
UI_FILE = os.path.join(file_directory, f'{NAME}.ui').replace(os.sep, '/')

METHOD_OPTION_MENUS = [
        'index',
        'nearest',
        'barycentric',
        'bilinear',
        'over',
        ]
INFLUENCEASSOCIATION = [
    'closestJoint',
    'closestBone',
    'label',
    'name',
    'oneToOne',
    'None',
]


SAVE_DIRECTORY = NAME


class EasyBind(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    UI = None
    _tso_flag = False
    valueChanged = QtCore.Signal(float)
    _value = 0.0
    __boost = int('1'+('0'*2))

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self._settings = None
        loader = QUiLoader()
        self.UI = loader.load(UI_FILE)
        # self.weightData:dict = {}

        self._appendMenu()

        self.resize(300, 250)
        self.setWindowTitle(TITLE)
        self.setCentralWidget(self.UI)
        self.UI.tabWidget.setCurrentIndex(0)

        self._addComboBoxItems()
        # self._construction()
        self._setRadioButtonGroup()
        self._setUIConnections()
        self._setUIIcons()

        self._trackSelectionOrderFlag()
        self._setWindowSize()
        self._resetSettings()

        self.setRange(0.0, 1.0)
        self.setDecimals(2)

        self.UI.jointSizeDoubleSpinBox.valueChanged[float].connect(
            self.valueChangedCallback)
        self.UI.jointSizeHorizontalSlider.valueChanged[int].connect(self.valueChangedCallback)

        if not DEV_MODE:
            self._send_log()

        command.attach_job(self.objectName(), self._resetSettings)

    def valueChangedCallback(self, value):
        sender = self.sender()
        if sender == self.UI.jointSizeDoubleSpinBox:
            self.UI.jointSizeHorizontalSlider.blockSignals(True)
            self.UI.jointSizeHorizontalSlider.setValue(value*self.__boost)
            self.UI.jointSizeHorizontalSlider.blockSignals(False)

        elif sender == self.UI.jointSizeHorizontalSlider:
            value = float(value)/self.__boost
            self.UI.jointSizeDoubleSpinBox.blockSignals(True)
            self.UI.jointSizeDoubleSpinBox.setValue(value)
            self.UI.jointSizeDoubleSpinBox.blockSignals(False)
        self._value = value
        self.valueChanged.emit(value)
        self.attributeValueChange(value=value)

    def attributeValueChange(self, value:float=1.0):
        command.join_radius_edit(radius=value)

    def value(self):
        return self.UI.jointSizeDoubleSpinBox.value()

    def setValue(self, value):
        self.UI.jointSizeDoubleSpinBox.setValue(value)
        self.UI.jointSizeHorizontalSlider.setValue(value*self.__boost)

    def setRange(self, min, max):
        self.UI.jointSizeDoubleSpinBox.setRange(min, max)
        self.__updateSliderRange()

    def setDecimals(self, prec):
        self.UI.jointSizeDoubleSpinBox.setDecimals(prec)
        self.__updateSliderRange()

    def __updateSliderRange(self):
        decimals = self.UI.jointSizeDoubleSpinBox.decimals()
        minimum = round(self.UI.jointSizeDoubleSpinBox.minimum())
        maximum = round(self.UI.jointSizeDoubleSpinBox.maximum())
        self.__boost = int('1'+('0'*decimals))
        self.UI.jointSizeHorizontalSlider.setRange(minimum*self.__boost, maximum*self.__boost)

    def _send_log(self):
        logger = tool_log.get_logger(tool_title=TITLE, tool_version=tool_version)
        logger.send_launch("")

    def _setWindowSize(self):
        """ウィンドウサイズの設定保存
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
        fileInfo にデータ書き込み
        ファイルパスとスライダ情報
        """
        super(self.__class__, self).closeEvent(event)
        self._settings.setValue(f'{self.__class__.__name__}geometry', self.saveGeometry())
        command._reset_track_selection_order_flag(self._tso_flag)
        self._setFileInfoData()

    def _trackSelectionOrderFlag(self):
        """ウェイトコピーの際に選択順に適用するための関数
        元の設定をとっておきツール終了時に元に戻す
        Returns:
            [bool]: 元の設定のフラグ
        """
        self._tso_flag = command._trackSelectionOrder_Flag(self._tso_flag)

    def _setUIIcons(self):
        self.UI.selectMeshesPushButton.setIcon(QtGui.QIcon(':/cube.png'))
        self.UI.selectJointsPushButton.setIcon(QtGui.QIcon(':/kinJoint.png'))

        self.UI.selectMemoryMeshesPushButton.setIcon(QtGui.QIcon(':/cube.png'))
        self.UI.selectMemoryJointsPushButton.setIcon(QtGui.QIcon(':/kinJoint.png'))

        self.UI.viewJointCheckBox.setIcon(QtGui.QIcon(':/pickJointObjPartial.png'))
        self.UI.jointXrayCheckBox.setIcon(QtGui.QIcon(':/XRayJoints.png'))
        self.UI.jointAxisViewCheckBox.setIcon(QtGui.QIcon(':/menuIconModify.png'))

        self.UI.autoBindPushButton.setIcon(QtGui.QIcon(':/smoothSkin.png'))
        self.UI.addInfluencePushButton.setIcon(QtGui.QIcon(':/addSkinInfluence.png'))
        self.UI.unBindSelectionPushButton.setIcon(QtGui.QIcon(':/detachSkin.png'))

        self.UI.gotToBindPosePushButton.setIcon(QtGui.QIcon(':/goToBindPose.png'))
        self.UI.resetJointRotationPushButton.setIcon(QtGui.QIcon(':/kinSetPreferredAngle.png'))
        self.UI.restoreBindPosePushButton.setIcon(QtGui.QIcon(':/poseEditor.png'))

        self.UI.memoryWeightPushButton.setIcon(QtGui.QIcon(':/skinWeightCopy.png'))
        self.UI.pasteWeightPushButton.setIcon(QtGui.QIcon(':/skinWeightPaste.png'))

        self.UI.transferWeightsPushButton.setIcon(QtGui.QIcon(':/polyTransferAttributes.png'))

        self.UI.importWeightsPushButton.setIcon(QtGui.QIcon(':/loadPreset.png'))
        self.UI.exportWeightsPushButton.setIcon(QtGui.QIcon(':/save.png'))
        self.UI.selectListGeometriesPushButton.setIcon(QtGui.QIcon(':/selectModel.png'))

        self.UI.openTopologyCheckBox.setIcon(QtGui.QIcon(':/openCloseSurface.png'))
        self.UI.maxVValuePinCheckBox.setIcon(QtGui.QIcon(':/UVAlignTop.png'))

    def _setUIConnections(self):
        self.UI.jointAxisViewCheckBox.clicked.connect(partial(self.toggleJointAxisView))

        self.UI.selectMeshesPushButton.clicked.connect(partial(self._selectNodes, "transform"))
        self.UI.selectJointsPushButton.clicked.connect(partial(self._selectNodes, "all_joint"))
        self.UI.bindJointsSelectPushButton.clicked.connect(partial(self._selectNodes, "need_joint"))

        self.UI.resetJointRotationPushButton.clicked.connect(partial(self._resetJointRotation))
        self.UI.gotToBindPosePushButton.clicked.connect(partial(self._goToBind))
        self.UI.autoBindPushButton.clicked.connect(partial(self._bindSkin, "auto"))
        self.UI.bindToSelectPushButton.clicked.connect(partial(self._bindSkin, "selection"))
        self.UI.bindMetahumanPushButton.clicked.connect(partial(self._bindMetahuman))
        self.UI.unBindSelectionPushButton.clicked.connect(partial(self._unBindSkinSelections))
        self.UI.unBindSceneAllPushButton.clicked.connect(partial(self._unBindSkin))

        self.UI.transferWeightsPushButton.clicked.connect(partial(self._transferWeight))
        self.UI.transferLODWeightPushButton.clicked.connect(self._transferWeightLOD)
        self.UI.transferSelectChildrenPushButton.clicked.connect(self._transferWeightLOD)

        self.UI.exportWeightsPushButton.clicked.connect(partial(self._saveWeightData))
        self.UI.refreshListPushButton.clicked.connect(partial(self._resetListWidget))
        self.UI.selectListGeometriesPushButton.clicked.connect(partial(self._selectListWidgetGeometory))
        self.UI.importWeightsPushButton.clicked.connect(partial(self._loadWeightData))

        # self.UI.memoryBindNodesPushButton.clicked.connect(partial(self._memoryBindNodes))
        self.UI.selectMemoryMeshesPushButton.clicked.connect(self._selectMemoryNodes)
        self.UI.selectMemoryJointsPushButton.clicked.connect(self._selectMemoryNodes)
        self.UI.restoreBindPosePushButton.clicked.connect(partial(self._restoreBindPose))
        self.UI.addInfluencePushButton.clicked.connect(command.add_influence_selection)

        self.UI.memoryWeightPushButton.clicked.connect(partial(self.memoryWeights))
        self.UI.pasteWeightPushButton.clicked.connect(partial(self.pasteWeights))

        self.UI.viewJointCheckBox.stateChanged.connect(self._setJointView)
        self.UI.jointXrayCheckBox.stateChanged.connect(self._setJointXray)

        # self.UI.saveWeightPushButton.clicked.connect(partial(self.saveWeightJson))
        # self.UI.loadWeightPushButton.clicked.connect(partial(self.loadWeightJson))

    def toggleJointAxisView(self, *args):
        _checkState:bool = self.UI.jointAxisViewCheckBox.isChecked()
        command.toggle_joint_axis_view(view_state=_checkState)

    def saveWeightJson(self, clear:bool=False):
        command.save_weight_json(weight_data=self.weightData, save_directory=str(self.work_dir), clear=clear)

    def loadWeightJson(self):
        if not self.work_dir:
            return
        self.weightData:dict = command.load_weight_json(str(self.work_dir))

    def memoryWeights(self):
        clear:bool = False
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.ControlModifier:
            self.weightData:dict = dict()
            clear = True
        else:
            self.weightData:dict = command.memory_weights()

        self.saveWeightJson(clear=clear)
        # print(self.weightData)
        # self.weightData:dict = command.memory_weights_api2()

    def pasteWeights(self):
        command.paste_weights(weight_data=self.weightData)
        # command.paste_weights_api2(self.weightData)

    def _restoreBindPose(self):
        command.restore_bindpose()

    def _selectMemoryNodes(self):

        _ignore_lod_flag = self.UI.ignoreLODCheckBox.isChecked()
        _metahuman_flag = self.UI.metahumanCheckBox.isChecked()
        _shenron_flag = self.UI.shenronCheckBox.isChecked()
        _buttonName = self.sender().objectName()
        send_ndoes = []
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        _add_selection = False
        if modifiers == QtCore.Qt.ControlModifier:
            _add_selection = True

        if "Joint" in _buttonName:
            if self.memory_joints:
                send_ndoes.extend(self.memory_joints)
                # send_ndoes.extend(command.chose_node_selections(
                #                             nodes=self.memory_joints,
                #                             node_type='joint',
                #                             metahuman_name_flag=_metahuman_flag
                #                             ))
        else:
            if self.memory_bindskin_transform_mesh:
                send_ndoes.extend(self.memory_bindskin_transform_mesh)
                # send_ndoes.extend(command.chose_node_selections(
                #                             nodes=list(self.memory_bindskin_transform_mesh.keys()),
                #                             node_type='mesh',
                #                             metahuman_name_flag=_metahuman_flag
                #                             ))

        command.select_nodes(nodes=send_ndoes, add_select_flag=_add_selection, ignore_lod=_ignore_lod_flag)

    def _memoryBindNodes(self):
        """メッシュ：トランスフォームノードの辞書
        ジョイントのリストを取得
        """
        if self.memory_bindskin_transform_mesh and not command.overwrite_confirmation():
            return
        bindskin_transform_mesh, joints, mesh_influence = command.get_bind_nodes()

        if bindskin_transform_mesh:
            self.memory_bindskin_transform_mesh = bindskin_transform_mesh
        if joints:
            self.memory_joints = joints
        if mesh_influence:
            self.mesh_influence = mesh_influence

    def _setRadioButtonGroup(self):
        """ラジオボタングループ作成
        """
        self.influenceRadioButtonGroup = QtWidgets.QButtonGroup()
        self.influenceRadioButtonGroup.addButton(self.UI.inf4RadioButton, 1)
        self.influenceRadioButtonGroup.addButton(self.UI.inf6RadioButton, 2)
        self.influenceRadioButtonGroup.addButton(self.UI.inf8RadioButton, 3)
        self.influenceRadioButtonGroup.addButton(self.UI.inf12RadioButton, 4)
        self.influenceRadioButtonGroup.button(4).setChecked(True)

        self.surfaceAssociationRadioButtonGroup = QtWidgets.QButtonGroup()
        self.surfaceAssociationRadioButtonGroup.addButton(self.UI.closestPointRadioButton, 1)
        self.surfaceAssociationRadioButtonGroup.addButton(self.UI.uvSpaceRadioButton, 2)
        self.surfaceAssociationRadioButtonGroup.addButton(self.UI.rayCastRadioButton, 3)
        self.surfaceAssociationRadioButtonGroup.addButton(self.UI.closestCompornentRadioButton, 4)
        self.surfaceAssociationRadioButtonGroup.button(1).setChecked(True)

    def _resetTransfarSettings(self):
        self.UI.transferAssociationComboBox1.setCurrentText(INFLUENCEASSOCIATION[0])
        self.UI.transferAssociationComboBox2.setCurrentText(INFLUENCEASSOCIATION[-1])
        self.UI.transferAssociationComboBox3.setCurrentText(INFLUENCEASSOCIATION[-1])
        self.surfaceAssociationRadioButtonGroup.button(1).setChecked(True)

    def _addComboBoxItems(self):
        """ウェイトインポート時のメソッド選択オプション構築
        """
        for method in METHOD_OPTION_MENUS:
            self.UI.importMethodComboBox.addItem(method)

        for association in INFLUENCEASSOCIATION:
            self.UI.transferAssociationComboBox1.addItem(association)
            self.UI.transferAssociationComboBox2.addItem(association)
            self.UI.transferAssociationComboBox3.addItem(association)

    def _construction(self):
        """命名規則の仕様が決まれば機能を実装
        """
        self.UI.meshesAndJointsSelectPushButton.setEnabled(False)
        self.UI.autoBindPushButton.setEnabled(False)
        self.UI.transferLODWeightPushButton.setEnabled(False)

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
        """ディレクトリ選択ダイアログ表示
        """
        directory_path = self.work_dir
        dialog = QtWidgets.QFileDialog(directory=str(directory_path))
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        if dialog.exec_():
            path = dialog.selectedFiles()[0]
            self.work_dir = Path(path)
            self._resetListWidget()

    def _openHelp(self):
        """ヘルプサイト表示
        """
        command.open_web_site()

    def _resetListWidget(self):
        self._createListWidgetData()
        self._buildListWidgetItems()

    def _setJointView(self):
        self.joint_view = self.UI.viewJointCheckBox.isChecked()
        command.change_joint_view(joint_view=self.joint_view)

    def _setJointXray(self):
        self.joint_xray = self.UI.jointXrayCheckBox.isChecked()
        command.change_joint_xray(joint_xray=self.joint_xray)

    def _setJointViewState(self):
        if self.joint_view:
            self.UI.viewJointCheckBox.setChecked(True)
        else:
            self.UI.viewJointCheckBox.setChecked(False)
        if self.joint_xray:
            self.UI.jointXrayCheckBox.setChecked(True)
        else:
            self.UI.jointXrayCheckBox.setChecked(False)

    def _resetSettings(self):
        """設定のリセット
        新規シーン、シーンを開いた場合に発動
        """
        self.weight_data:dict = {}
        self.longname_shortname:dict = {}
        self.work_dir:str = ""
        self.scene_path:str = ""
        self.scene_basename:str = ""
        self.memory_bindskin_transform_mesh:dict = {}
        self.memory_joints:list = []
        self.mesh_influence:dict = {}
        self.weightData:dict = {}
        self.jointRadius = command.get_joint_radius()
        self.joint_view, self.joint_xray = command.query_joint_view()

        value = self.jointRadius
        self._value = value

        # self.setRange(0.0, 10.0)
        # self.setDecimals(2)
        self.setValue(value)

        self._getFileInfoData()
        self._getSceneName()

        self._resetListWidget()
        self._resetTransfarSettings()
        self._memoryBindNodes()
        self.loadWeightJson()
        self._setJointViewState()


    def _openExploer(self, *args):
        """Windows Exploer で表示させる
        """
        command.open_exploer(self.work_dir)

    def _setFileInfoData(self):
        """fileInfo にデータ格納
        """
        command.set_file_info_data("WINDOW_SETTINGS", self._settings)
        if self.work_dir:
            command.set_file_info_data("SAVE_DIRECTORY", str(self.work_dir).replace(os.sep, '/'))

    def _getFileInfoData(self):
        """fileInfo のデータ取得
        """
        _info_data = command.get_file_info_data("SAVE_DIRECTORY")
        if _info_data:
            self.work_dir = Path(_info_data[0])

    def _getProjectName(self)->str:
        """プロジェクト名をUIのチェックボックスから取得

        Returns:
            str: プロジェクト名
        """
        _project_name = ""
        _shrnron_rule_flag = self.UI.shenronRuleCheckBox.isChecked()
        if _shrnron_rule_flag:
            _project_name = "shenron"
        return _project_name

    def _selectNodes(self, select_node_type:str="need_joint"):
        """メッシュ、ジョイント選択ボタンの動作

        Args:
            select_node_type (str, optional): _description_. Defaults to "joint".
        """
        project_name = ""
        _ignore_lod_flag = self.UI.ignoreLODCheckBox.isChecked()
        project_name = self._getProjectName()
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        _add_selection = False
        if modifiers == QtCore.Qt.ControlModifier:
            _add_selection = True

        if select_node_type == "all_joint":
            command.select_all_joints(project=project_name, add_selection=_add_selection)
        elif select_node_type == "need_joint":
            command.select_need_joints(project=project_name, add_selection=_add_selection)
        elif select_node_type == "transform":
            command.select_need_transforms(project=project_name, ignore_lod_flag=_ignore_lod_flag, add_selection=_add_selection)
        elif select_node_type == "transform_joint":
            command.select_need_transform_and_joint(project=project_name, ignore_lod_flag=_ignore_lod_flag, add_selection=_add_selection)

    def _bindMetahuman(self):
        if not self.mesh_influence:
            return
        command.bind_metahuman(
                    mesh_influence=self.mesh_influence,
                    )

    def _bindSkin(self, bind_type:str="auto"):
        """バインド
        """
        _ignore_lod_flag = self.UI.ignoreLODCheckBox.isChecked()
        project_name = self._getProjectName()
        max_influences = int(self.influenceRadioButtonGroup.checkedButton().text())
        if bind_type=="auto":
            command.bind_skin(project=project_name, max_influences=max_influences, ignore_lod_flag=_ignore_lod_flag)
        elif bind_type=="selection":
            command.bind_skin(project=project_name, bind_type="selection", max_influences=max_influences, ignore_lod_flag=False)

    def _createListWidgetData(self):
        """ウェイト保存用ディレクトリの内容からjson のみを取り出しリスト化
        """
        self.longname_shortname = {}
        self.weight_data = {}
        if self.work_dir and self.work_dir.exists():
            _weight_files = list(self.work_dir.glob(f'*{WEIGHT_FILE_FORMAT[PROJECT_WEIGHT_FILE_FORMAT]}'))
            if _weight_files:
                for _weight_file in _weight_files:
                    ext = _weight_file.suffix[1:]
                    if ext not in list(WEIGHT_FILE_FORMAT.keys()):
                        continue
                    _basename = str(_weight_file.name).rsplit(".")[0]
                    _long_name = _basename.replace('__', '|')
                    _name = _basename.rsplit("__")[-1]
                    self.longname_shortname[_long_name] = _name
                    self.weight_data[_long_name] = _weight_file

    def _buildListWidgetItems(self):
        """ウェイトファイルをリストをUI に表示
        """
        self.UI.weightDataListWidget.clear()

        if not self.weight_data:
            return

        for _long_name in list(self.weight_data.keys()):
            _name = self.longname_shortname.get(_long_name)
            if _name:
                self.UI.weightDataListWidget.addItem(str(_name))

    def _selectListWidgetGeometory(self):
        """リストで詮索したジオメトリのノードを選択
        """
        meshes = [x.text() for x in self.UI.weightDataListWidget.selectedItems()]
        if not meshes:
            return
        mesh_longnames = [k for k,v in self.longname_shortname.items() if v in meshes]
        command.select_transformknodes(mesh_longnames)

    def _createDirectory(self, create:bool=True):
        """ディレクトリ作成

        Args:
            create (bool, optional): _description_. Defaults to True.
        """
        self.work_dir = command.create_work_directory(self.scene_path, create=create)

    def _getSceneName(self):
        """シーン名取得
        """
        scene_path = getCurrentSceneFilePath()
        if scene_path:
            scene_path = Path(scene_path)
            self.scene_basename = scene_path.name
            self.scene_path = scene_path.parent
            self._createDirectory(create=False)

    def _resetJointRotation(self):
        """Preferred Angle 適用
        """
        command.reset_joint_rotation()

    def _goToBind(self):
        """バインドポーズに戻す
        """
        command.go_to_bindpose()

    def _unBindSkinSelections(self):
        command.unbind_skin_selections()

    def _unBindSkin(self):
        """シーン内のバインドポーズ全解除
        """
        command.unbind_skin_preprocess()

    def _transferWeightLOD(self):
        sender = self.sender()
        project_name = self._getProjectName()
        self._getWeightTransferSettings()
        lodFlag = True
        if not 'LOD' in sender.objectName()[0]:
            lodFlag = False
            project_name = ''
        command.transfer_weight_lods(
                    lod_flag=lodFlag,
                    project=project_name,
                    surfaceAssociation=self._transWeightSurfaceAssociation,
                    influenceAssociation=self._transWeightInfluenceAssociation,
                    normalize=self._transWeightNormalize
                    )

    def _getWeightTransferSettings(self):
        _influenceAssociation = []
        _openTopology = self.UI.openTopologyCheckBox.isChecked()
        _normalize = self.UI.transferNormalizeCheckBox.isChecked()
        _uv_value_pin = self.UI.maxVValuePinCheckBox.isChecked()

        _surfaceAssociation = self.surfaceAssociationRadioButtonGroup.checkedButton().text()
        _influenceAssociation1 = self.UI.transferAssociationComboBox1.currentText()
        _influenceAssociation2 = self.UI.transferAssociationComboBox2.currentText()
        _influenceAssociation3 = self.UI.transferAssociationComboBox3.currentText()
        _influenceAssociation1 = INFLUENCEASSOCIATION[0] if _influenceAssociation1 == 'None' else _influenceAssociation1
        _influenceAssociation.append(_influenceAssociation1)

        if _influenceAssociation2 != 'None':
            _influenceAssociation.append(_influenceAssociation2)
        if _influenceAssociation3 != 'None':
            _influenceAssociation.append(_influenceAssociation3)

        self._transWeightOpenTopology = _openTopology
        self._transWeightNormalize = _normalize
        self._transWeightUVPin = _uv_value_pin
        self._transWeightSurfaceAssociation = _surfaceAssociation

        if len(_influenceAssociation) == 1:
            self._transWeightInfluenceAssociation = _influenceAssociation1
        else:
            self._transWeightInfluenceAssociation = _influenceAssociation

    def _transferWeight(self):
        """ウェイトの転送
        選択の一つ目のウェイトをそれ以降の選択全てに適用
        開いた形状の場合は一つの頂点のウェイトをトポロジ全体に適用
        """
        self._getWeightTransferSettings()
        command.transfer_weight(
                        openTopology=self._transWeightOpenTopology,
                        normalize=self._transWeightNormalize,
                        surfaceAssociation=self._transWeightSurfaceAssociation,
                        influenceAssociation=self._transWeightInfluenceAssociation,
                        uv_value_pin=self._transWeightUVPin,
            )

    def _saveWeightData(self):
        """ウェイトデータ保存
        """
        meshes = command.get_meshes()
        if not meshes:
            return

        _numberOfDigit = self.UI.numberOfDigitSpinBox.value()

        command.save_weight_data(directory=self.work_dir, meshes=meshes, number_of_digit=_numberOfDigit)
        self._resetListWidget()

    def _loadWeightData(self):
        """ウェイト読み込みボタンの動作
        Args:
            args (str): index, normalize
        index: デフォルト動作（読み込み前に0 書き込み）
        normalize: 読み込み時にノーマライズ
        """

        send_meshes = []
        errors = []
        meshes = command.get_meshes(long_name=False)

        _method = self.UI.importMethodComboBox.currentText()
        normalize = self.UI.weightNormalizeCheckBox.isChecked()

        if not meshes:
            meshes = [x.text() for x in self.UI.weightDataListWidget.selectedItems()]
            _mesh_longnames = [k for k,v in self.longname_shortname.items() if v in meshes]
        else:
            _mesh_longnames = command.get_full_path_mesh_node_names(meshes)
        _mesh_shortnames = [v for k,v in self.longname_shortname.items() if v in meshes]

        if not _mesh_longnames:
            return

        weightFilePaths = []
        for mesh_shape_long_name, weight_file_path in self.weight_data.items():
            short_name = mesh_shape_long_name.split('|')[-1]
            if command.obj_exists(short_name) and short_name in _mesh_shortnames:
                weightFilePaths.append(weight_file_path)
                send_meshes.append(short_name)
            # else:
            #     errors.append(short_name)

        command.load_weight_data(
                                meshes=send_meshes,
                                weightFilePaths=weightFilePaths,
                                method=_method,
                                error_nodes=errors,
                                normalize=normalize
                                )


def main():
    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == CLASS_NAME:
            _obj.close()
            del _obj

    if not command.check_path_exists(path=UI_FILE):
        return

    ui = EasyBind()
    ui.show()