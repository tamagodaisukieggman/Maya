from __future__ import absolute_import
from __future__ import print_function
from __future__ import division


from pathlib import Path
import os
import importlib

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from ...utils import gui_util
import tool_log

from . import NAME
from . import TITLE
from . import command
from . import tool_version

CLASS_NAME = "".join(TITLE.split())

# 開発中は1、リリース時に0
DEV_MODE = command.load_config('DEV_MODE')

if DEV_MODE:
    importlib.reload(command)

HERE = Path(os.path.dirname(os.path.abspath(__file__)))
UI_FILE = HERE / f'{NAME}_ui.ui'

HOME_PATH = Path(os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH"))
MY_DOCUMENT_PATH = HOME_PATH / 'Documents'
MEGASCAN_DEFAULT_PATH = MY_DOCUMENT_PATH / 'Megascans Library' / 'Downloaded' / 'DHI'
SHENRON_CHARACTOR_PATH = r'C:\cygames\shrdev\shr_art\resources\characters'


class FlowGridLayout(QtWidgets.QLayout):
    def __init__(self, margin: int, horizontalSpacing: int, verticalSpacing: int, parent=None):
        super().__init__(parent=parent)
        self.setContentsMargins(margin, margin, margin, margin)

        self.item_list = []
        self.horizontalSpacing = horizontalSpacing
        self.verticalSpacing = verticalSpacing

    def addItem(self, item: QtWidgets.QLayoutItem):
        self.item_list.append(item)

    def count(self):
        return len(self.item_list)

    def itemAt(self, index: int):
        if self.count() > 0 and index < self.count():
            return self.item_list[index - 1]
        return None

    def takeAt(self, index):
        if index >= 0 and index < self.count():
            return self.item_list.pop(index - 1)
        return None

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width: int):
        height = self.doLayout(QtCore.QRect(0, 0, width, 0))
        return height

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self.item_list:
            size = size.expandedTo(item.minimumSize())

        margins = self.contentsMargins()
        size += QtCore.QSize(margins.left() + margins.right(), margins.top() + margins.bottom())

    def setGeomertry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect)

    def doLayout(self, rect):
        x = rect.x()
        y = rect.y()
        _lineHeight = 0
        for item in self.item_list:
            # wid = item.widget()
            nextH = x + item.sizeHint().width() + self.horizontalSpacing
            if nextH - self.horizontalSpacing > rect.right() and _lineHeight > 0:
                x = rect.x()
                y = y + _lineHeight + self.verticalSpacing
                nextH = x + item.sizeHint().width() + self.horizontalSpacing
                _lineHeight = 0
            item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
            x = nextH
            _lineHeight = max(_lineHeight, item.sizeHint().height())
        return y + _lineHeight - rect.y()


class MetahumanSupport(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    UI = None
    def __init__(self, parent=None):
        self.clearMemory()
        super(self.__class__, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        loader = QUiLoader()
        self.UI = loader.load(str(UI_FILE))

        self.UI.layout = FlowGridLayout(5, 5, 5)
        self.UI.insideWidget.setLayout(self.UI.layout)

        self.appendMenu()
        self.setButtonIcon()

        self.resize(300, 150)
        self.setWindowTitle(TITLE)
        self.setCentralWidget(self.UI)

        self.setWindowState()
        self.setUIConnections()
        self._setUIIcons()

        if not DEV_MODE:
            self._send_log()

    def _send_log(self):
        logger = tool_log.get_logger(tool_title=TITLE, tool_version=tool_version)
        logger.send_launch("")

    def clearMemory(self):
        self.character_id = ''
        self.metahuman_path = Path()
        self.character_path = Path()
        self.metahuman_button_path = dict()
        self.dna_file_path = Path()
        self.body_model_path = Path()
        self.body_name_space = ''
        self._currentAxis = 'y'

    def _setUIIcons(self):
        self.UI.createMetahumanPushButton.setIcon(QtGui.QIcon(':/BasicHead.png'))

        self.UI.importBodyModelPushButton.setIcon(QtGui.QIcon(':/loadPreset.png'))
        # self.UI.reParentPushButton.setIcon(QtGui.QIcon(':/kinDisconnect.png'))
        # self.UI.importWeightsPushButton.setIcon(QtGui.QIcon(':/traxOpenLibrary.png'))

        # self.UI.visibleNodesParentChangePushButton.setIcon(QtGui.QIcon(':/deleteRenderPass.png'))
        # self.UI.axisChangePushButton.setIcon(QtGui.QIcon(':/rotate_M.png'))
        # self.UI.removeNameSpacePushButton.setIcon(QtGui.QIcon(':/publishNamedAttribute.png'))
        # self.UI.unBindPushButton.setIcon(QtGui.QIcon(':/unbind.png'))
        self.UI.shenronCharacterPartSetUpPushButton.setIcon(QtGui.QIcon(':/CharacterGenerator.png'))
        self.UI.deleteHistoryReconnectionPushButton.setIcon(QtGui.QIcon(':/DeleteHistory.png'))
        self.UI.importMetahumanWeightsPushButton.setIcon(QtGui.QIcon(':/RS_import_layer.png'))

        self.UI.removeLayersPushButton.setIcon(QtGui.QIcon(':/deleteRenderPass.png'))
        self.UI.applyOutlinerColorPushButton.setIcon(QtGui.QIcon(':/paintCan.png'))

        self.UI.rotatePushButton.setIcon(QtGui.QIcon(':/rotate_M.png'))
        self.UI.rotateResetPushButton.setIcon(QtGui.QIcon(':/hyperShadeResetCameraView.png'))

        self.UI.useAllLightsPushButton.setIcon(QtGui.QIcon(':/render_phong.png'))
        self.UI.useDefaultLightingPushButton.setIcon(QtGui.QIcon(':/render_surfaceShader.png'))

        self.UI.zUpAxisPushButton.setIcon(QtGui.QIcon(':/polyRotateUVCCW.png'))
        self.UI.yUpAxisPushButton.setIcon(QtGui.QIcon(':/polyRotateUVCW.png'))

        self.UI.setCurrentCharacterPushButton.setIcon(QtGui.QIcon(':/defaultTextureList.png'))
        self.UI.LODNodeRenameSelectionPushButton.setIcon(QtGui.QIcon(':/polyColorSetRename.png'))


        # self.UI.unBindFacialPushButton.setIcon(QtGui.QIcon(':/unbind.png'))
        # self.UI.preProcessPushButton.setIcon(QtGui.QIcon(':/greasePencilPostGhostOff.png'))
        # self.UI.createSecondUVPushButton.setIcon(QtGui.QIcon(':/polySetCurrentUVSet.png'))
        # self.UI.postProcessPushButton.setIcon(QtGui.QIcon(':/greasePencilPreGhostOff.png'))

        # self.UI.reBindPushButton.setIcon(QtGui.QIcon(':/bind.png'))
        # self.UI.createLODGroupPushButton.setIcon(QtGui.QIcon(':/out_default.png'))
        # self.UI.createCharacterIDGroupPushButton.setIcon(QtGui.QIcon(':/out_transform.png'))
        # self.UI.showDisplayLayerPushButton.setIcon(QtGui.QIcon(':/LightDown.png'))

        # self.UI.removeNameSpaceFacialPushButton.setIcon(QtGui.QIcon(':/publishNamedAttribute.png'))
        # self.UI.deleteNodesFacialPushButton.setIcon(QtGui.QIcon(':/delete.png'))

        self.UI.facialSceneSetUpPushButton.setIcon(QtGui.QIcon(':/BasicHead.png'))

        self.UI.deleteHistoryReconnectionFacialPushButton.setIcon(QtGui.QIcon(':/DeleteHistory.png'))
        self.UI.importShenronWeightsPushButton.setIcon(QtGui.QIcon(':/RS_import_layer.png'))

        # self.UI.createSecondUVPushButton.setEnabled(False)

    def setUIConnections(self):
        """シグナル設定
        """
        self.UI.libraryPathPushButton.clicked.connect(self.openPathSetDialog)
        self.UI.characterPathPushButton.clicked.connect(self.openPathSetDialog)
        # self.UI.dnaFilePathPushButton.clicked.connect(self.openDNAFilePathSetDialog)
        self.UI.characterPathLineEdit.returnPressed.connect(self.libraryPathLineEditPressReturn)
        self.UI.megascanLibraryPathLineEdit.returnPressed.connect(self.megascanLibraryPathLineEditPressReturn)
        self.UI.createMetahumanPushButton.clicked.connect(self.createMetahuman)
        self.UI.setCurrentCharacterPushButton.clicked.connect(command.set_current_character_path)
        # self.UI.removeNameSpacePushButton.clicked.connect(command.remove_name_space)

        # self.UI.applyShenronInfluencePushButton.clicked.connect(command.apply_shenron_influence)

        self.UI.zUpAxisPushButton.clicked.connect(self.setViewAxis)
        self.UI.yUpAxisPushButton.clicked.connect(self.setViewAxis)
        self.UI.useAllLightsPushButton.clicked.connect(self.setLighting)
        self.UI.useDefaultLightingPushButton.clicked.connect(self.setLighting)
        # self.UI.setupFacialScenePushButton.clicked.connect(self.setupFacialScene)
        # self.UI.selectExportNodesPushButton.clicked.connect(command.SetupFacialScene.select_export_nodes)
        # self.UI.createLODFromSelectNodePushButton.clicked.connect(self.createLODFromSelectNode)
        # self.UI.characterIDPushButton.clicked.connect(self.characterID)
        self.UI.LODNodeRenameSelectionPushButton.clicked.connect(command.lod_group_rename_selection)
        self.UI.removeLayersPushButton.clicked.connect(command.show_head_display_layers)
        self.UI.applyOutlinerColorPushButton.clicked.connect(command.chenge_outliner_color_scene_all)


        # self.UI.shenronLODCreatePushButton.clicked.connect(self.createShenronLOD)
        self.UI.rotatePushButton.clicked.connect(command.set_up_rotation)
        self.UI.rotateResetPushButton.clicked.connect(command.rotation_reset)

        self.UI.bodyModelPathPushButton.clicked.connect(self.openBodyModelFilePathSetDialog)
        self.UI.importBodyModelPushButton.clicked.connect(self.importBodyModel)

        # self.UI.importWeightsPushButton.clicked.connect(command.import_metahuman_weight)
        # self.UI.importWeightsPushButton.clicked.connect(command.import_weight_test)
        # self.UI.importWeightsPushButton.clicked.connect(command.import_other_weight)
        # self.UI.deleteNodesFacialPushButton.clicked.connect(self.deleteNodesFacial)

        # self.UI.reParentPushButton.clicked.connect(command.re_parent_ndoes)

        # self.UI.preProcessPushButton.clicked.connect(self.preProcess)
        # self.UI.postProcessPushButton.clicked.connect(self.postProcess)

        self.UI.shenronCharacterPartSetUpPushButton.clicked.connect(self.shenronCaracterPartSetUp)
        # self.UI.axisChangePushButton.clicked.connect(self.axisChangeNodeRotate)
        # self.UI.removeNameSpacePushButton.clicked.connect(self.removeNameSpace)
        # self.UI.unBindPushButton.clicked.connect(self.unbind)
        self.UI.deleteHistoryReconnectionPushButton.clicked.connect(self.deleteHistoryReconnection)
        self.UI.importMetahumanWeightsPushButton.clicked.connect(self.import_weight_to_selections)

        self.UI.deleteHistoryReconnectionFacialPushButton.clicked.connect(self.deleteHistoryReconnection)
        self.UI.importShenronWeightsPushButton.clicked.connect(self.import_weight_to_selections)

        # self.UI.createLODGroupPushButton.clicked.connect(self.createLODGroupNode)
        # self.UI.createCharacterIDGroupPushButton.clicked.connect(self.createCharacterIDGroup)
        # self.UI.showDisplayLayerPushButton.clicked.connect(self.showDisplayLayerChangeLighting)

        # self.UI.removeNameSpaceFacialPushButton.clicked.connect(command.remove_name_space)

        # self.UI.unBindFacialPushButton.clicked.connect(self.unbindFacial)

        self.UI.facialSceneSetUpPushButton.clicked.connect(self.facialSceneSetUp)

    def import_weight_to_selections(self):
        weight_type:str = 'Metahuman'
        sender = self.sender()
        _sender_string:str = sender.objectName()
        if 'Shenron' in _sender_string:
            weight_type = 'Shenron'

        command.import_metahuman_weight_to_selections(weight_type=weight_type)

    def shenronCaracterPartSetUp(self):
        self.preProcess()
        self.postProcess()

    def preProcess(self):
        self.nodeVisibleDeleteReparetnt()
        self.axisChangeNodeRotate()
        self.removeNameSpace()
        # if self._currentAxis == 'z':
        self.unbind()
        self.showDisplayLayerChangeLighting()

    def postProcess(self):
        self.rebind()
        self.createLODGroupNode()
        self.createCharacterIDGroup()
        self.showDisplayLayerChangeLighting()

    def facialSceneSetUp(self):
        body_model_path:str = self.UI.importBodyModelLineEdit.text().replace(os.sep, '/')
        if not body_model_path:
            _d = gui_util.ConformDialog(title="Not Found Body Model",
                                        message="Not Found Body Model")
            _d.exec_()
            return
        command.remove_name_space()

        self.jointConnections = command.MetahumanJointReConnections()
        self.jointConnections.un_bind(body_model_path=body_model_path)
        self.jointConnections.disconnect_attribute()
        self.jointConnections.freeze_transform_joint()
        self.jointConnections.connect_attribute()

        self.jointConnections.reparent_nodes()
        self.jointConnections.delete_node_facial()
        self.jointConnections.import_metahuman_weight()

    def unbindFacial(self):
        body_model_path:str = self.UI.importBodyModelLineEdit.text().replace(os.sep, '/')
        if not body_model_path:
            _d = gui_util.ConformDialog(title="Not Found Body Model",
                                        message="Not Found Body Model")
            _d.exec_()
            return

        body_model_path:Path = Path(body_model_path)
        file_name:str = body_model_path.stem
        model_id:str = file_name.split("_", 1)[-1]

        self.jointConnections = command.MetahumanJointReConnections()
        self.jointConnections.un_bind(body_root_node=model_id)
        self.jointConnections.disconnect_attribute()
        self.jointConnections.freeze_transform_joint()

        self.jointConnections.connect_attribute()
        command.re_parent_ndoes()

    def nodeVisibleDeleteReparetnt(self):
        _flag = command.visible_nodes()
        if _flag:
            _flag = command.delete_nodes()
        if _flag:
            command.spine04_parent()

    def axisChangeNodeRotate(self):
        self._currentAxis:str = command.get_current_axis()
        command.set_up_displlay(change_to_axis='y', current_axis=self._currentAxis)
        command.set_up_rotation()


    def removeNameSpace(self):
        command.remove_name_space()

    def unbind(self):
        command.un_bind_character_part()

    def deleteHistoryReconnection(self):
        is_reset_transform:bool = False
        sender = self.sender()
        _sender_string:str = sender.objectName()
        # command._delete_history_reconnection()
        if 'Facial' in _sender_string:
            is_reset_transform = True
        command.delete_history_reconneciotns_from_selection(is_reset_transform=is_reset_transform)

    def rebind(self):
        command.re_bind()
        # self.jointConnections = command.MetahumanJointReConnections()
        # self.jointConnections.un_bind()
        # self.jointConnections.disconnect_attribute()
        # self.jointConnections.freeze_transform_joint()
        # self.jointConnections.connect_attribute()

    def createLODGroupNode(self):
        command.create_lodgroup()

    def createCharacterIDGroup(self):
        command.create_character_id_group()

    def showDisplayLayerChangeLighting(self):
        command.show_head_display_layers()
        command.chenge_light_modelPanel4(display_light='all')


    def characterID(self):
        _fs = command.SetupFacialScene()
        _fs.create_character_id_group()

    def createShenronLOD(self):
        _fs = command.SetupFacialScene()
        _fs.create_lodgroup_select_mode()

    def createLODFromSelectNode(self):
        _fs = command.SetupFacialScene()
        _fs.create_lodgroup_from_selection()


    def setUpCurrentCharacterPath(self):
        character_path = self.getCharacterPath()
        if not character_path:
            _d = gui_util.ConformDialog(title="Not Found Character Path",
                                        message="Not Found Character Path")
            _d.exec_()
            return
        command.file_replace(local_path=character_path)

    def setLighting(self):
        sender = self.sender()
        if 'All' in sender.objectName():
            command.chenge_light_modelPanel4(display_light='all')
        else:
            command.chenge_light_modelPanel4(display_light='default')

    def setViewAxis(self):
        self._currentAxis:str = command.get_current_axis()
        sender = self.sender()
        change_to_axis = sender.objectName()[0]
        command.set_up_displlay(change_to_axis=change_to_axis, current_axis=self._currentAxis)


    def getCharacterPath(self):
        _character_path_exists = True
        character_path = self.UI.characterPathLineEdit.text()
        if not character_path:
            _character_path_exists = False
        character_path = Path(character_path)
        if not character_path.exists():
            _character_path_exists = False
        if _character_path_exists:
            return character_path
        else:
            return

    def getMegascanPath(self):
        _megascan_path_exists = True
        megascan_path = self.UI.megascanLibraryPathLineEdit.text()
        if not megascan_path:
            _megascan_path_exists = False
        megascan_path = Path(megascan_path)
        if not megascan_path.exists():
            _megascan_path_exists = False
        if _megascan_path_exists:
            return megascan_path
        else:
            return

    def getCurrentMetahumanRadioButton(self):
        _source_data_path = None
        for _radio_button, _asset_path in self.metahuman_button_path.items():
            _radio_button:QtWidgets.QRadioButton = _radio_button
            _asset_path:Path = _asset_path
            if _radio_button.isChecked():
                _source_data_path = _asset_path
                _name = _radio_button.toolTip()
                break
        return _source_data_path

    def getCharacterID(self)->str:
        """キャラクターID取得

        Returns:
            str: キャラクターID [mfc1010_citizen] など
        """
        _result:str = ''
        _id_name = self.UI.charactreIDLineEdit.text()

        if not _id_name:
            _d = gui_util.ConformDialog(title="No Character ID name",
                                        message="Input Character ID name")
            _d.exec_()
            return _result

        _id_split_name = _id_name.split("_")
        if len(_id_split_name) == 1:
            _d = gui_util.ConformDialog(title="There is no [ _ ]",
                                        message="Underbar is required")
            _d.exec_()
            return _result
        _result = _id_name

        return _result

    def createMetahuman(self):
        _source_data_path = None
        _target_directory_path = Path()
        _id_name = self.getCharacterID()

        if not _id_name:
            return

        _name = ''

        megascan_path = self.getMegascanPath()
        if not megascan_path:
            _d = gui_util.ConformDialog(title="Not Found DHI Library Path",
                                        message="Not Found DHI Library Path")
            _d.exec_()
            return

        character_path = self.getCharacterPath()
        if not character_path:
            _d = gui_util.ConformDialog(title="Not Found Character Path",
                                        message="Not Found Character Path")
            _d.exec_()
            return

        # if not _id_name:
        #     _d = gui_util.ConformDialog(title="No Character ID name",
        #                                 message="Input Character ID name")
        #     _d.exec_()
        #     return

        # _dna_file_path = self.getDNAFilePath()
        # if not _dna_file_path:
        #     _d = gui_util.ConformDialog(title="Not Found DNA file Path",
        #                                 message="Not Found DNA file Path")
        #     _d.exec_()
        #     return


        _id_split_name = _id_name.split("_")
        # if len(_id_split_name) == 1:
        #     _d = gui_util.ConformDialog(title="There is no [ _ ]",
        #                                 message="Underbar is required")
        #     _d.exec_()
        #     return

        model_name_prefix = _id_split_name[0]
        _source_data_path = self.getCurrentMetahumanRadioButton()

        if not _source_data_path:
            _d = gui_util.ConformDialog(title="Select Metahuman",
                                        message="Select Metahuman")
            _d.exec_()
            return

        _target_directory_path = character_path / _id_name
        _scene_path = command.copy_scene_file(
                                    src_path=_source_data_path,
                                    dst_path=_target_directory_path,
                                    new_scene_name=model_name_prefix
                                    )
        if not _scene_path:
            return
        if _scene_path.exists():
            command.set_up_maya_scene(scene_path=_scene_path, dst_path=_target_directory_path, character_id=model_name_prefix)
            dst_path = command.texture_file_replace(dst_path=_target_directory_path, character_id=model_name_prefix)
            command.save_maya_scene(scene_path=_scene_path)


    def setCharacterID(self, id:str=''):
        self.character_id = id
        self.UI.charactreIDLineEdit.setText(id)

    def setCharacterPath(self, path:str=''):
        path = Path(path)
        self.character_path = path
        self.UI.characterPathLineEdit.setText(str(path).replace(os.sep, '/'))

    def setLibralyPath(self, path:str=''):
        path = Path(path)
        self.metahuman_path = path
        self.UI.megascanLibraryPathLineEdit.setText(str(path).replace(os.sep, '/'))
        self.createIconRadioButton()

    def setImportBodyModelFilePath(self, path:str=''):
        path:Path = Path(path)
        self.body_model_path = path
        self.UI.importBodyModelLineEdit.setText(str(path).replace(os.sep, '/'))
        self.body_name_space = path.stem

    def megascanLibraryPathLineEditPressReturn(self):
        path = self.UI.megascanLibraryPathLineEdit.text()
        self.setLibralyPath(path)

    def libraryPathLineEditPressReturn(self):
        path = self.UI.characterPathLineEdit.text()
        self.setCharacterPath(path)

    def openDNAFilePathSetDialog(self):
        path = self.getCurrentMetahumanRadioButton()

        if not path:
            _d = gui_util.ConformDialog(title="Select Metahuman",
                                        message="Select Metahuman")
            _d.exec_()
            return

        dialog = QtWidgets.QFileDialog(directory=str(path))
        file_path = dialog.getOpenFileName(self, "Select DNA File", filter="dna files (*.dna)")
        if file_path[0]:
            file_path = file_path[0]
            self.dna_file_path = Path(file_path)

    def openBodyModelFilePathSetDialog(self):
        path = Path(self.body_model_path)
        if str(path) != ".":
            path = path.parent
        else:
            path = Path(command.load_config('SHENRON_RIG_PATH'))

        dialog = QtWidgets.QFileDialog(directory=str(path))
        project_file_types = command.load_config('Import_File_Type').keys()
        _file_type = ' *'.join([x for x in project_file_types])
        _filtter_str = f'Scene file (*.fbx)'
        file_path = dialog.getOpenFileName(self, "Select File", filter=_filtter_str)

        if file_path[0]:
            file_path = file_path[0]
            self.body_model_path = Path(file_path)
            self.UI.importBodyModelLineEdit.setText(file_path.replace(os.sep, '/'))

    def _openBodyModelFilePathSetDialog(self):
        path = Path(self.body_model_path)
        if str(path) != ".":
            path = path.parent
        else:
            path = Path(command.load_config('SHENRON_RIG_PATH'))

        dialog = QtWidgets.QFileDialog(directory=str(path))
        project_file_types = command.load_config('Import_File_Type').keys()
        _file_type = ' *'.join([x for x in project_file_types])
        _filtter_str = f'Scene file (*{_file_type})'
        file_path = dialog.getOpenFileName(self, "Select File", filter=_filtter_str)

        if file_path[0]:
            file_path = file_path[0]
            self.body_model_path = Path(file_path)
            self.UI.importBodyModelLineEdit.setText(file_path.replace(os.sep, '/'))

    def deleteNodesFacial(self):
        path = self.body_model_path
        command.delete_nodes_facial(body_model_path=path)


    def importBodyModel(self):
        _nameSpaceChecked = self.UI.nameSpaceApplyCheckBox.isChecked()
        path = Path(self.body_model_path)
        if not path or not path.exists():
            return
        nameSpace = self.body_name_space if _nameSpaceChecked else ''
        command.import_body_model(file_path=path, name_space=nameSpace)

    def importNeckWeights(self):
        command.import_neck_weights(self.body_name_space)

    def openPathSetDialog(self):
        sender = self.sender()
        path = Path()
        if sender.objectName() == 'libraryPathPushButton':
            path = self.UI.megascanLibraryPathLineEdit.text()
            if not path:
                path = Path(MEGASCAN_DEFAULT_PATH)
            else:
                path = Path(path)
        elif sender.objectName() == 'characterPathPushButton':
            path = self.UI.characterPathLineEdit.text()
            if not path:
                path = Path(command.load_config('SHENRON_CHARACTOR_PATH'))
            else:
                path = Path(path)

        if not path.exists():
            path = ''
        else:
            path = str(path)

        dialog = QtWidgets.QFileDialog(directory=path)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        if dialog.exec_():
            path = dialog.selectedFiles()[0]
            if sender.objectName() == 'libraryPathPushButton':
                self.setLibralyPath(path)
            elif sender.objectName() == 'characterPathPushButton':
                self.export_path = Path(path)
                self.UI.characterPathLineEdit.setText(path.replace(os.sep, '/'))


    def createIconRadioButton(self):
        self.deleteRadioButtons()

        icon_path = list(self.metahuman_path.glob('**/*_preview.png'))
        icon_path.sort(key=os.path.getmtime, reverse=True)
        with gui_util.ProgressDialog(
                            title='Loading Metahumans',
                            message='Now Loading ...',
                            maxValue=len(icon_path)) as prg:
            QtCore.QCoreApplication.processEvents()
            for i, icon_path in enumerate(icon_path):
                _asset_path = icon_path
                _parent = icon_path.parent
                _maya_file = list(_parent.glob('**/*_full_rig.mb'))

                if not _maya_file:
                    continue

                basename = icon_path.stem.split("_", 1)[0]
                json_path = _parent / f'{basename}.json'
                name = command.get_name_from_json(json_path)

                if not name:
                    name = basename

                icon = QtGui.QIcon(str(icon_path))
                _radioButton = QtWidgets.QRadioButton()
                _radioButton.setIcon(icon)
                _radioButton.setIconSize(QtCore.QSize(200, 200))
                _radioButton.setToolTip(name)

                self.metahuman_button_path[_radioButton] = _asset_path.parent

                self.UI.layout.addWidget(_radioButton)
                if prg.wasCanceled():
                    break
                prg.step(i)


    def appendMenu(self):
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

    def setButtonIcon(self):
        """ボタンアイコン適用
        """
        image = QtGui.QIcon(':/folder-open.png')
        self.UI.libraryPathPushButton.setIcon(image)
        self.UI.characterPathPushButton.setIcon(image)
        # self.UI.dnaFilePathPushButton.setIcon(image)
        self.UI.bodyModelPathPushButton.setIcon(image)

    def setWindowState(self):
        """ウィンドウサイズの設定保存
        fileInfo に書き込む
        """
        self.UI.tabWidget.setCurrentIndex(0)
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
        library_path = self._settings.value(f'{self.UI.megascanLibraryPathLineEdit.objectName()}.text')
        character_path = self._settings.value(f'{self.UI.characterPathLineEdit.objectName()}.text')
        # dna_file_Path = self._settings.value(f'{self.UI.dnaFilePathLineEdit.objectName()}.text')
        character_id = self._settings.value(f'{self.UI.charactreIDLineEdit.objectName()}.text')
        body_model_path = self._settings.value(f'{self.UI.importBodyModelLineEdit.objectName()}.text')
        print("restore -- ")
        print('library_path --', library_path)
        print('character_path -- ', character_path)
        print('character_id -- ', character_id)
        # print('dna_file_Path -- ', dna_file_Path)
        print('body_model_path -- ', body_model_path)
        if library_path:
            self.setLibralyPath(library_path)
        if character_path:
            self.setCharacterPath(character_path)
        if character_id:
            self.setCharacterID(character_id)
        # if dna_file_Path:
        #     self.setDnaFilePath(dna_file_Path)
        if body_model_path:
            self.setImportBodyModelFilePath(body_model_path)
            self.body_name_space = body_model_path.rsplit('/')[-1].rsplit('.')[0]

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
        library_path = self.UI.megascanLibraryPathLineEdit.text().replace(os.sep, '/')
        character_path = self.UI.characterPathLineEdit.text().replace(os.sep, '/')
        # dna_file_path = self.UI.dnaFilePathLineEdit.text().replace(os.sep, '/')
        character_id = self.UI.charactreIDLineEdit.text()
        body_model_path = self.UI.importBodyModelLineEdit.text().replace(os.sep, '/')

        print("close -- ")
        print('library_path --', library_path)
        print('character_path -- ', character_path)
        print('character_id -- ', character_id)
        print('body_model_path -- ', body_model_path)

        self._settings.setValue(f'{self.UI.megascanLibraryPathLineEdit.objectName()}.text', library_path)
        self._settings.setValue(f'{self.UI.characterPathLineEdit.objectName()}.text', character_path)
        # self._settings.setValue(f'{self.UI.dnaFilePathLineEdit.objectName()}.text', dna_file_path)
        self._settings.setValue(f'{self.UI.charactreIDLineEdit.objectName()}.text', character_id)
        self._settings.setValue(f'{self.UI.importBodyModelLineEdit.objectName()}.text', body_model_path)
        self._settings.setValue(f'{self.__class__.__name__}geometry', self.saveGeometry())
        self._settings.setValue(f'{self.__class__.__name__}state', self.saveState())

        super(self.__class__, self).closeEvent(event)

    def deleteRadioButtons(self):
        for i in reversed(range(self.UI.layout.count())):
            _w = self.UI.layout.itemAt(i)
            _w.widget().deleteLater()


def main():
    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == CLASS_NAME:
            _obj.close()
            del _obj

    ui = MetahumanSupport()
    ui.show()


