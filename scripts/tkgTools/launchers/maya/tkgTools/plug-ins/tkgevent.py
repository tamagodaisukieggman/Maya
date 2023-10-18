# -*- coding: utf-8 -*-
from logging import getLogger
import maya.api.OpenMaya as om
import maya.cmds as cmds

import sys
import traceback

logger = getLogger(__name__)


class TkgEvent(object):

    plugin_name = 'tkgevent'

    after_file_read_id = None
    after_open_id = None
    before_file_read_id = None
    before_save_id = None

    @classmethod
    def after_file_read(cls, client_data=None):
        # logger.info('start: after_file_read')
        cls._delete_ui_configuration()
        cls._delete_mentalray_items()
        cls._delete_turtle_nodes()
        # cls._detect_unknowns()
        # logger.info('end: after_file_read')

    @classmethod
    def after_open(cls, client_data=None):
        # cls._change_current_unit_force()
        try:
            scene_name = cmds.file(q=1, sn=1)
            sys.__stdout__.write('FILE READ: {}\n'.format(scene_name))
            print('FILE READ: {}\n'.format(scene_name))
            cls._delete_ui_configuration()
            cls._delete_panel_configuration()
        except:
            print(traceback.format_exc())
        # cls._reload_reference_node()
        # logger.info('after_open')

    @classmethod
    def before_save(cls, client_data=None):
        # cls._change_current_unit()
        cls._delete_turtle_nodes()
        cls._delete_nodeGraphEditorInfo_nodes()
        # logger.info('before_save')

    @classmethod
    def before_file_read(cls, client_data=None):
        cls._delete_hypershade_window()
        # logger.info('before_file_read')

    @classmethod
    def _reset_modeleditor(cls):
        u"""modelEditorの情報をリセット"""
        editors = cmds.lsUI(editors=True)
        if not editors:
            return

        for editor in editors:
            if cmds.modelEditor(editor, ex=True) and cmds.optionVar(ex=editor):
                cmds.optionVar(rm=editor)
        cmds.panelConfiguration(rap=True)

        sys.__stdout__.write('RESET: modelEditor\n')
        print('RESET: modelEditor\n')


    @classmethod
    def _delete_ui_configuration(cls):
        ui_configuration = 'uiConfigurationScriptNode'
        if cmds.ls(ui_configuration):
            cmds.delete(ui_configuration)
            sys.__stdout__.write('DELETE: uiConfigurationScriptNode\n')
            print('DELETE: uiConfigurationScriptNode\n')

        cls._reset_modeleditor()

    @classmethod
    def _delete_mentalray_items(cls):
        u"""mentalray情報を除去"""
        plugin_name = 'Mayatomr'
        unnecessary_nodes = ('mentalrayGlobals', 'mentalrayItemsList', 'miDefaultFramebuffer', 'miDefaultOptions')

        unknown_plugins = cmds.unknownPlugin(q=True, l=True) or []
        unknown_nodes = cmds.ls(typ='unknown')

        # mentalray関連のノードの削除
        for node in unknown_nodes:
            for unknown in unnecessary_nodes:
                if unknown in node and cmds.ls(node):
                    logger.info('Delete: {}'.format(node))
                    cmds.delete(node)
                    sys.__stdout__.write('DELETE: mentalray :{}\n'.format(node))
                    print(('DELETE: mentalray :{}\n'.format(node)))

        # mentalray関連のプラグインの削除
        if plugin_name in unknown_plugins:
            logger.info('Remove: {}'.format(plugin_name))
            cmds.unknownPlugin(plugin_name, r=True)
            sys.__stdout__.write('REMOVE PLUGIN: mentalray :{}\n'.format(plugin_name))
            print('REMOVE PLUGIN: mentalray :{}\n'.format(plugin_name))

    @classmethod
    def _detect_unknowns(cls):
        u"""不明なデータを検出する"""
        message = u'不明なデータが検出されました。\nこのファイルを制作管理に渡して不正データのチェックを依頼してください。'

        known_plugins = ['stereoCamera', 'mtoa']
        known_nodes = ['vectorRenderGlobals']

        unknown_plugins = cmds.unknownPlugin(q=True, l=True) or []
        unknown_plugins = list(set(unknown_plugins) - set(known_plugins))

        unknown_nodes = list(set(cmds.ls(typ='unknown')) - set(known_nodes))
        unknown_dags = cmds.ls(typ='unknownDag')
        unknown_transforms = cmds.ls(typ='unknownTransform')

        if unknown_plugins or unknown_nodes or unknown_dags or unknown_transforms:
            logger.error('Detected unknowns')
            # cmds.confirmDialog(m=message, b='OK')

            if unknown_plugins:
                logger.error('[unknown plugins]')
                for unknown in unknown_plugins:
                    logger.error(unknown)
            if unknown_nodes:
                logger.error('[unknown nodes]')
                for unknown in unknown_nodes:
                    logger.error(unknown)
            if unknown_dags:
                logger.error('[unknown dags]')
                for unknown in unknown_dags:
                    logger.error(unknown)

    @classmethod
    def _delete_turtle_nodes(cls):
        turtle_nodes = [u'TurtleBakeLayerManager',
         u'TurtleDefaultBakeLayer',
         u'TurtleRenderOptions',
         u'TurtleUIOptions']

        for tn in turtle_nodes:
            try:
                if cmds.objExists(tn):
                    cmds.lockNode(tn, l=0)
                    cmds.delete(tn)
                    sys.__stdout__.write('DELETE: TurtleDefaultBake :{}\n'.format(tn))
                    print('DELETE: TurtleDefaultBake :{}\n'.format(tn))
            except Exception as e:
                print(traceback.format_exc())

    @classmethod
    def _delete_nodeGraphEditorInfo_nodes(cls):
        u"""MayaNodeEditorSavedTabsInfoを削除する"""
        ngei_nodes = cmds.ls(type='nodeGraphEditorInfo')
        for ni in ngei_nodes:
            cmds.lockNode(ni, l=0)
            cmds.delete(ni)
            sys.__stdout__.write('DELETE: MayaNodeEditorSavedTabsInfo :{}\n'.format(ni))
            print('DELETE: MayaNodeEditorSavedTabsInfo :{}\n'.format(ni))

    @classmethod
    def _change_current_unit_force(cls):
        u"""フレームレートを30 に変更

        :return:
        """
        current_unit = cmds.currentUnit(q=True, t=True)
        if current_unit != 'ntsc':
            cmds.currentUnit(t='ntsc')
            cmds.warning(u'フレームレートを変更: {} > ntsc'.format(current_unit))

    @classmethod
    def _change_current_unit(cls, client_data=None):
        u"""モーション用データのみ保存時にダイアログ表示

        :param client_data:
        :return:
        """

        motion_directory = 'C:/perforce/tkg/data/3d/03_motion'
        scene_path = cmds.file(sn=True, q=True)

        if scene_path.startswith(motion_directory):
            current_unit = cmds.currentUnit(q=True, t=True)
            if current_unit != 'ntsc':
                cls._change_current_unit_force()
                cmds.confirmDialog(
                    t='Change Working Unit Time',
                    b=['OK'],
                    m=u'フレームレートを変更: {} > ntsc'.format(current_unit)
                )
        else:
            cls._change_current_unit_force()

    @classmethod
    def _delete_panel_configuration(cls):
        u"""パネルコンフィグを初期値以外削除

        :return:
        """

        panel_configs = cmds.getPanel(ac=True)

        if panel_configs:
            if len(panel_configs) > 18:
                custom_panels = panel_configs[18:]
                cmds.deleteUI(custom_panels, pc=True)
                sys.__stdout__.write('DELETE: PanelConfigs :{}\n'.format(custom_panels))
                print('DELETE: PanelConfigs :{}\n'.format(custom_panels))
                # logger.info(u'初期値以外のパネルコンフィグを削除しました\n{}'.format(custom_panels))

    @classmethod
    def _delete_hypershade_window(cls):
        windows = cmds.lsUI(type='window')
        if windows:
            if 'hyperShadePanel1Window' in windows:
                cmds.deleteUI('hyperShadePanel1Window')
                sys.__stdout__.write('DELETE: hyperShadePanel1Window\n')
                print('DELETE: hyperShadePanel1Window\n')
                # logger.info(u'ハイパーシェードウィンドウを閉じます')

    @classmethod
    def _reload_reference_node(cls):
        u"""リファレンス再読み込み"""
        reference_nodes = cmds.ls(rf=True)

        if reference_nodes:
            for node in reference_nodes:
                try:
                    is_loaded = cmds.referenceQuery(node, il=True)
                    if not is_loaded:
                        cmds.file(lrd='asPrefs', lr=node)
                        sys.__stdout__.write('RELOAD REFERENCE :{}\n'.format(node))
                        print('RELOAD REFERENCE :{}\n'.format(node))
                        # logger.info('{}: {}'.format(u'リファレンス再読み込み'.encode('cp932'), node))
                except Exception as e:
                    print(traceback.format_exc())


def initializePlugin(obj):
    u"""initializePlugin"""
    # kAfterFileRead
    try:
        TkgEvent.after_file_read_id = om.MSceneMessage.addCallback(
            om.MSceneMessage.kAfterFileRead,
            TkgEvent.after_file_read,
            None,
        )
    except Exception as e:
        print(traceback.format_exc())

    # kAfterOpen
    try:
        TkgEvent.after_open_id = om.MSceneMessage.addCallback(
            om.MSceneMessage.kAfterOpen,
            TkgEvent.after_open,
            None,
        )
    except Exception as e:
        print(traceback.format_exc())

    # kBeforeFileRead
    try:
        TkgEvent.before_file_read_id = om.MSceneMessage.addCallback(
            om.MSceneMessage.kBeforeFileRead,
            TkgEvent.before_file_read,
            None,
        )
    except Exception as e:
        print(traceback.format_exc())

    # kBeforeSave
    try:
        TkgEvent.before_save_id = om.MSceneMessage.addCallback(
            om.MSceneMessage.kBeforeSave,
            TkgEvent.before_save,
            None,
        )
    except Exception as e:
        print(traceback.format_exc())

    # # kBeforeCreateReference
    # try:
    #     TkgEvent.before_create_reference_id = om.MSceneMessage.addCallback(
    #         om.MSceneMessage.kBeforeCreateReference,
    #         TkgEvent.before_create_reference,
    #         None,
    #     )
    # except Exception as e:
    #     logger.error(e)


def uninitializePlugin(obj):
    u"""uninitializePlugin"""
    # kAfterFileRead
    try:
        om.MSceneMessage.removeCallback(TkgEvent.after_file_read_id)
    except Exception as e:
        print(traceback.format_exc())

    # kAfterOpen
    try:
        om.MSceneMessage.removeCallback(TkgEvent.after_open_id)
    except Exception as e:
        print(traceback.format_exc())

    # kBeforeFileRead
    try:
        om.MSceneMessage.removeCallback(TkgEvent.before_file_read_id)
    except Exception as e:
        print(traceback.format_exc())

    # kBeforeSave
    try:
        om.MSceneMessage.removeCallback(TkgEvent.before_save_id)
    except Exception as e:
        print(traceback.format_exc())

    # # kBeforeCreateReference
    # try:
    #     om.MSceneMessage.removeCallback(TkgEvent.before_create_reference_id)
    # except Exception as e:
    #     logger.error(e)
