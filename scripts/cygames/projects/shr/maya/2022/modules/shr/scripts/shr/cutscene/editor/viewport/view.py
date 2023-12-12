# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya import cmds
from maya import mel

from . import const


class View(object):
    @classmethod
    def show(cls):
        # cls.settings.load()
        cls.delete_overlap_view()
        cls.create_model_view_ui(const.CINEMATIC_VIEWPORT_VIEW, const.CINEMATIC_VIEWPORT_CONTROL, const.CINEMATIC_VIEWPORT_NAME)
        cls.create_model_panel(const.EDIT_VIEWPORT_VIEW, const.EDIT_VIEWPORT_CONTROL, const.EDIT_VIEWPORT_NAME)
        cls.create_model_panel(const.CAMERA_VIEWPORT_VIEW, const.CAMERA_VIEWPORT_CONTROL, const.CAMERA_VIEWPORT_NAME)

        cls.create_panel_configuration()
        # TODO: 生成後defaultのカメラの更新が必要か？

        cls.set_cutscene_layout()

    @classmethod
    def set_cutscene_layout(cls):
        mel.eval('setNamedPanelLayout( "{}" )'.format(const.PANEL_LAYOUT_NAME))

    @classmethod
    def close(cls):
        cls.delete_all_modelview_workspace()
        cls.delete_layout()

        mel.eval('setNamedPanelLayout "Single Perspective View"')

    @classmethod
    def create_model_view_ui(cls, view_name, control_name, control_label):
        main_window = mel.eval('$temp=$gMainWindow')
        cmds.modelPanel(view_name, label=view_name, parent=main_window, isUnique=True)

        # なぜかlabelが一度で適用されないので、別途適用。
        cmds.panel(view_name, edit=True, label=view_name)

        model_editor = cmds.modelPanel(view_name, query=True, modelEditor=True)

        cmds.modelEditor(model_editor, edit=True,
                         displayAppearance="smoothShaded",
                         polymeshes=True, displayTextures=True,
                         headsUpDisplay=True, selectionHiliteDisplay=False,
                         nurbsCurves=False, planes=False, lights=True, cameras=False, grid=False,
                         locators=False, joints=False, manipulators=False,
                         camera="persp")

        cmds.modelPanel(view_name, edit=True, unParent=True)

    @classmethod
    def create_model_panel(cls, view_name, control_name, control_label):
        main_window = mel.eval('$temp=$gMainWindow')
        cmds.modelPanel(view_name, label=view_name, camera="persp", parent=main_window)

        # なぜかlabelが一度で適用されないので、別途適用。
        cmds.panel(view_name, edit=True, label=view_name)

        cmds.modelPanel(view_name, edit=True, unParent=True)

        # TODO: カット班にデフォルトのModelView状態を固定する可能性あり。

    @classmethod
    def delete_overlap_view(cls):
        """重複しているViewを削除する
        """
        cls.delete_all_modelview_workspace()

    @classmethod
    def delete_all_modelview_workspace(cls):
        """モデルビューのワークスペースを全削除する
        """
        cls.__delete_modelview_workspace(const.CINEMATIC_VIEWPORT_CONTROL, const.CINEMATIC_VIEWPORT_VIEW)
        cls.__delete_modelview_workspace(const.CAMERA_VIEWPORT_CONTROL, const.CAMERA_VIEWPORT_VIEW)
        cls.__delete_modelview_workspace(const.EDIT_VIEWPORT_CONTROL, const.EDIT_VIEWPORT_VIEW)

    @classmethod
    def __delete_modelview_workspace(cls, control_name, view_name):
        """モデルビューのワークスペースを削除する

        :param control_name: コントロール名
        :type control_name: str
        :param view_name: View名
        :type view_name: str
        """
        if cmds.modelPanel(view_name, query=True, exists=True):
            cmds.deleteUI(view_name, panel=True)

    @classmethod
    def create_panel_configuration(cls):

        cls.delete_layout()

        cmds.panelConfiguration(const.PANEL_LAYOUT_NAME,
                                label=const.PANEL_LAYOUT_NAME,
                                sceneConfig=False,
                                configString="paneLayout -e -configuration \"top4\" -ps 1 33 60 -ps 2 33 60 -ps 3 33 60 -ps 4 90 20 $gMainPane;",
                                addPanel=[
                                    (True,
                                        "CinematicViewPortView",
                                        "modelPanel",
                                        ("{global int $gUseMenusInPanels;\
                    modelPanel -mbv $gUseMenusInPanels\
                    -unParent -l \"CinematicViewPortView\" -cam persp;}"),
                                        "modelPanel -edit -l \"CinematicViewPortView\"  -cam \"persp\" $panelName"),

                                    (True,
                                        "CameraViewPortView",
                                        "modelPanel",
                                        ("{global int $gUseMenusInPanels;\
                    modelPanel -mbv $gUseMenusInPanels\
                    -unParent -l \"CameraViewPortView\" -cam persp;}"),
                                        "modelPanel -edit -l \"CameraViewPortView\"  -cam \"persp\" $panelName"),

                                    (True,
                                        "EditViewPortPortView",
                                        "modelPanel",
                                        ("{global int $gUseMenusInPanels;\
                    modelPanel -mbv $gUseMenusInPanels\
                    -unParent -l \"EditViewPortPortView\" -cam persp;}"),
                                        "modelPanel -edit -l \"EditViewPortPortView\"  -cam \"persp\" $panelName"),

                                    (False,
                                        'Camera Sequencer',
                                        'sequenceEditorPanel1',
                                        ("{global int $gUseMenusInPanels;\
                    $panelName = `outlinerPanel -mbv $gUseMenusInPanels -unParent -l \"Camera Sequencer\"`;\
                    outlinerEditor -e -highlightActive true $panelName;}"),
                                        "outlinerPanel -edit -l \"Camera Sequencer\"  $panelName"),
                                ]
                                )

    @classmethod
    def delete_layout(cls):
        panel_conf = cmds.getPanel(allConfigs=True)
        for i, conf in enumerate(panel_conf):
            if conf == const.PANEL_LAYOUT_NAME:
                cmds.deleteUI(const.PANEL_LAYOUT_NAME)
                return

            conf_label = cmds.panelConfiguration(conf, query=True, label=True)
            if conf_label == const.PANEL_LAYOUT_NAME:
                cmds.deleteUI(conf)
                return
