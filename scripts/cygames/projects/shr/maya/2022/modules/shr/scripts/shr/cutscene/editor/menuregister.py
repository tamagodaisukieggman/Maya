# -*- coding: utf-8 -*-
"""カットシーンエディター用のメニュー登録"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from functools import partial

from maya import cmds, mel

from . import menu
from . import viewport

from shr.cutscene import camerasequencer_camera_creator
from shr.cutscene import camerasequencer_playblast
from shr.cutscene import camerasequencer_shot_renamer
from shr.cutscene import camerasequencer_storyboard_render


MENU_NAME = "Mtk_CameraSequencer_Tools"
MENU_LABEL = "Mtk_Tools"


MENU_BASE = MENU_NAME + "_"


MENU_ARNOLD_MENU = "Mtk_CameraSequencer_Tools_arnold_menu"


MENU_ARNOLD_BASE = MENU_ARNOLD_MENU + "_"


class ToolsMenuRegster(object):
    """ツールメニュー登録
    """
    @classmethod
    def register(cls):
        menu.CameraSequencerMenuRegister.add_menu(MENU_NAME, MENU_LABEL)

        CreateCameraMenuRegister().register()
        StorybardBatchRendererMenuRegister().register()
        CameraSequencerPlayblastMenuRegister().register()
        ShotRenamerMenuRegister().register()

    @classmethod
    def unregister(cls):
        menu.CameraSequencerMenuRegister.delete_menu(MENU_NAME)


class CreateCameraMenuRegister(object):
    """カメラ作成ツールのメニュー登録機能
    """
    MENU_ITEMS_NAME = MENU_NAME + "_CreateCamera"
    MENU_ITEMS_LABEL_NAME = "Create Camera"

    def register(self):
        menu.CameraSequencerMenuRegister.add_menu_item(self.MENU_ITEMS_NAME, label=self.MENU_ITEMS_LABEL_NAME, parent=MENU_NAME, command=camerasequencer_camera_creator.create)
        menu.CameraSequencerMenuRegister.add_menu_item(self.MENU_ITEMS_NAME + "_option", parent=MENU_NAME, command=camerasequencer_camera_creator.show_option, optionBox=True)


class StorybardBatchRendererMenuRegister(object):
    """ストーリーボードバッチレンダラーツールのメニュー登録機能
    """
    MENU_ARNOLD_LABEL = "Start Storyboard Rendering"
    MENU_ARNOLD_START_RENDERING = "Mtk_CameraSequencer_Tools_arnold_menu_Start_Arnold_Rendering"

    def register(self):
        menu.CameraSequencerMenuRegister.add_menu_item(self.MENU_ARNOLD_START_RENDERING, parent=MENU_NAME, label=self.MENU_ARNOLD_LABEL, command=camerasequencer_storyboard_render.start_current_frame_render)
        menu.CameraSequencerMenuRegister.add_menu_item(self.MENU_ARNOLD_START_RENDERING + "_option", parent=MENU_NAME, command=camerasequencer_storyboard_render.show_option, optionBox=True)


class CameraSequencerPlayblastMenuRegister(object):
    """カメラシーケンサー用のプレイブラストツールのメニュー登録機能
    """
    MENU_PLAYBLAST_START_LABEL = "Start Playblast"

    MENU_PLAYBLAST_MENU = "Mtk_CameraSequencer_Tools_playblast_menu"
    MENU_PLAYBLAST_BASE = MENU_PLAYBLAST_MENU + "_"
    MENU_PLAYBLAST_START = MENU_PLAYBLAST_BASE + "Start_Playblast"

    def register(self):
        menu.CameraSequencerMenuRegister.add_menu_item(self.MENU_PLAYBLAST_START, parent=MENU_NAME, label=self.MENU_PLAYBLAST_START_LABEL, command=partial(camerasequencer_playblast.start_playblast, viewport.CinematicViewPortInfo().get_name()))
        menu.CameraSequencerMenuRegister.add_menu_item(self.MENU_PLAYBLAST_START + "_option", parent=MENU_NAME, command=partial(camerasequencer_playblast.show_playblast_option, viewport.CinematicViewPortInfo().get_name()), optionBox=True)


class ShotRenamerMenuRegister(object):
    """ショットのリネームツールのメニュー登録機能

    """
    MENU_SHOT_RENAMER_LABEL = "Shot Rename"
    MENU_SHOT_RENAMER_MENU = "Mtk_CameraSequencer_Tools_shot_rename_menu"

    MENU_SHOT_RENAMER = MENU_BASE + "_" + MENU_SHOT_RENAMER_LABEL

    def register(self):
        menu.CameraSequencerMenuRegister.add_menu_item(self.MENU_SHOT_RENAMER, parent=MENU_NAME, label=self.MENU_SHOT_RENAMER_LABEL, command=camerasequencer_shot_renamer.rename)
        menu.CameraSequencerMenuRegister.add_menu_item(self.MENU_SHOT_RENAMER + "_option", parent=MENU_NAME, command=camerasequencer_shot_renamer.show_option, optionBox=True)


class CameraMenuRegister(object):
    """カメラメニュー登録機能
    """
    TOOLBAR_NAME = "sequenceEditorMtkToolBarFormlayout"
    TOOLBAR_SELECT_CAMERA_BUTTON_NAME = "sequenceEditorSelectCamerabox"
    TOOLBAR_START_RENDER_BUTTON_NAME = "sequenceEditorStartRender"
    TOOLBAR_START_IPRENDER_BUTTON_NAME = "sequenceEditorStartIPRender"

    @classmethod
    def register(cls):
        cls.add_camera_menu()

    @classmethod
    def unregister(cls):
        cls.delete_camera_menu()

    @classmethod
    def add_camera_menu(cls):
        """カメラ回りの拡張機能を追加する
        """
        tool_bar = menu.CameraSequencerMenuRegister.add_tool_bar(cls.TOOLBAR_NAME, 3)
        menu.CameraSequencerMenuRegister.add_tool_bar_icon_text_button(tool_bar, cls.TOOLBAR_SELECT_CAMERA_BUTTON_NAME, command=cls.select_active_view_camera)
        menu.CameraSequencerMenuRegister.add_tool_bar_icon_text_button(tool_bar, cls.TOOLBAR_START_RENDER_BUTTON_NAME, command=cls.start_render_button, image="rvRender.png")
        menu.CameraSequencerMenuRegister.add_tool_bar_icon_text_button(tool_bar, cls.TOOLBAR_START_IPRENDER_BUTTON_NAME, command=cls.start_iprender_button, image="rvIprRender.png")

    @classmethod
    def delete_camera_menu(cls):
        """カメラ回りの拡張機能を削除する
        """
        menu.CameraSequencerMenuRegister.delete_tool_bar(cls.TOOLBAR_NAME)

    @classmethod
    def select_active_view_camera(cls, *args):
        current_shot = cmds.sequenceManager(query=True, currentShot=True)
        current_camera = cmds.shot(current_shot, query=True, currentCamera=True)

        cmds.select(current_camera)

        cmds.lookThru(current_camera, viewport.CAMERA_VIEWPORT_VIEW)

        viewport.camera_view_camera = current_camera

    @classmethod
    def start_render_button(cls, *args):
        """レンダリング開始ボタン
        """
        # TODO:CinematicViewPortで固定しておく
        target_camera = viewport.CinematicViewPortInfo().get_camera()

        mel.eval("RenderViewWindow;")
        mel.eval("renderWindowRenderCamera render renderView {};".format(target_camera))

    @classmethod
    def start_iprender_button(cls, *args):
        """IPRレンダリング開始ボタン
        """
        # TODO:CinematicViewPortで固定しておく
        target_camera = viewport.CinematicViewPortInfo().get_camera()

        mel.eval("RenderViewWindow;")
        mel.eval("renderWindowRenderCamera iprRender renderView {};".format(target_camera))
