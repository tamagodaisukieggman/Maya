# -*- coding: utf-8 -*-
"""ホットキー回りの機能"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya import cmds
from PySide2 import QtWidgets

import functools
import numpy as np

from shr.cutscene import utility


class CameraSequencerHotkeyRegister(object):
    """カメラシーケンサー用のホットキー登録
    """
    CUTSCENE_SHOTCUT_NAME = "CameraSequencerShortcut"

    @classmethod
    def register(cls):
        cls.create_cutscene_shotcut()
        ViewToggleToolContext.register()
        CameraSequencerShotCursorMoverShotcutRegister.register()
        YawPitchToolShotcutRegister.register()

    @classmethod
    def unregister(cls):
        ViewToggleToolContext.unregister()

        cls.delete_cutscene_shotcut()

    @classmethod
    def create_cutscene_shotcut(cls):
        if cmds.hotkeySet(cls.CUTSCENE_SHOTCUT_NAME, exists=True):
            cmds.hotkeySet(cls.CUTSCENE_SHOTCUT_NAME, edit=True, delete=True)

        cmds.hotkeySet(cls.CUTSCENE_SHOTCUT_NAME, current=True)

    @classmethod
    def delete_cutscene_shotcut(cls):
        if cmds.hotkeySet(cls.CUTSCENE_SHOTCUT_NAME, exists=True):
            cmds.hotkeySet(cls.CUTSCENE_SHOTCUT_NAME, edit=True, delete=True)


class CameraSequencerShotCursorMoverShotcutRegister(object):
    """カメラシーケンサーのショットカーソル移動ツールのショートカット登録
    """
    PREVIOUS_CLIP_COMMAND_NAME = "CameraSequencerPreviousClip"
    NEXT_CLIP_COMMAND_NAME = "CameraSequencerNextClip"

    @classmethod
    def register(cls):
        """キーフレーム移動イベントを登録する
        """
        # なぜかsourceTypeをPythonにしてもmelになるので、melコマンドで渡す
        cmds.nameCommand(cls.PREVIOUS_CLIP_COMMAND_NAME,
                         annotation=cls.PREVIOUS_CLIP_COMMAND_NAME,
                         command='python("import shr.cutscene.camerasequencer_shot_cursor_mover as mover;mover.CameraSequencerShotCursorMover.previous_key_event()")',
                         default=True)
        cmds.nameCommand(cls.NEXT_CLIP_COMMAND_NAME,
                         annotation=cls.NEXT_CLIP_COMMAND_NAME,
                         command='python("import shr.cutscene.camerasequencer_shot_cursor_mover as mover;mover.CameraSequencerShotCursorMover.next_key_event()")',
                         default=True)

        cmds.hotkey(keyShortcut=',', name=cls.PREVIOUS_CLIP_COMMAND_NAME, altModifier=True)
        cmds.hotkey(keyShortcut='.', name=cls.NEXT_CLIP_COMMAND_NAME, altModifier=True)


class ViewToggleToolContext(object):
    """View用のトグルツール

    ContextはMaya固有の呼び名でツールを示す
    """
    target_camera_focallength = ""
    context_name = "ViewToggleToolContext"
    call_back = "ToggleCameraFocalLengthDragged"

    press_event_name = "ViewToggleToolPress"
    release_event_name = "ViewToggleToolRelease"

    current_focal_length = 0
    before_value = 0
    current_context = None

    hud_creator = None
    grid_creator = None
    custom_hud_creator = None

    @classmethod
    def press_event(cls):
        target_camera = utility.panel.get_camera_from_focus_model_panel()
        cls.target_camera_focallength = "{}.focalLength".format(target_camera)
        cls.current_focal_length = cmds.getAttr(cls.target_camera_focallength)

    @classmethod
    def drag_event(cls):
        global before_value

        anchor = cmds.draggerContext(cls.context_name, query=True, anchorPoint=True)
        dragPosition = cmds.draggerContext(cls.context_name, query=True, dragPoint=True)
        # button = cmds.draggerContext(cls.context_name, query=True, button=True)
        # modifier = cmds.draggerContext(cls.context_name, query=True, modifier=True)

        # アンカーのY座標から
        result = (anchor[1] - dragPosition[1]) / 100

        camera_focal_length = cmds.getAttr(cls.target_camera_focallength)

        target_focal_length = camera_focal_length + result

        if target_focal_length < 3:
            return

        cmds.setAttr(cls.target_camera_focallength, round(target_focal_length, 1))

        cmds.refresh(currentView=True)

        cls.before_value = result

        utility.mevent.MEventManager.post_user_event(cls.call_back)

    @classmethod
    def release_event(cls):
        cls.current_focal_length = cmds.getAttr(cls.target_camera_focallength)

    @classmethod
    def register(cls):
        utility.mevent.MEventManager.register_user_event(cls.call_back)

        if cmds.draggerContext(cls.context_name, exists=True):
            cmds.draggerContext(cls.context_name,
                                edit=True,
                                pressCommand="import shr.cutscene.editor.hotkey as hotkey;hotkey.ViewToggleToolContext.press_event()",
                                dragCommand="import shr.cutscene.editor.hotkey as hotkey;hotkey.ViewToggleToolContext.drag_event()",
                                releaseCommand="import shr.cutscene.editor.hotkey as hotkey;hotkey.ViewToggleToolContext.release_event()",
                                cursor="dolly",
                                space="screen")
        else:
            cmds.draggerContext(cls.context_name,
                                pressCommand="import shr.cutscene.editor.hotkey as hotkey;hotkey.ViewToggleToolContext.press_event()",
                                dragCommand="import shr.cutscene.editor.hotkey as hotkey;hotkey.ViewToggleToolContext.drag_event()",
                                releaseCommand="import shr.cutscene.editor.hotkey as hotkey;hotkey.ViewToggleToolContext.release_event()",
                                cursor="dolly",
                                space="screen")

        cmds.nameCommand(cls.press_event_name,
                         annotation=cls.press_event_name,
                         command='python("import shr.cutscene.editor.hotkey as hotkey;hotkey.ViewToggleToolContext.press()")',
                         default=True)
        cmds.nameCommand(cls.release_event_name,
                         annotation=cls.release_event_name,
                         command='python("import shr.cutscene.editor.hotkey as hotkey;hotkey.ViewToggleToolContext.release()")',
                         default=True)

        cmds.hotkey(keyShortcut='z', name=cls.press_event_name, shiftModifier=True, ctrlModifier=True, releaseName=cls.release_event_name)

    @classmethod
    def unregister(cls):
        utility.mevent.MEventManager.deregister_user_event(cls.call_back)

    @classmethod
    def press(cls):
        cls.current_context = cmds.currentCtx()

        cmds.setToolTo(cls.context_name)

        if cls.hud_creator is None:
            cls.hud_creator = MayaForcalLengthHUDCreator()

        if cls.grid_creator is None:
            cls.grid_creator = MayaGridHUDCreator()

        if cls.custom_hud_creator is None:
            cls.custom_hud_creator = CustomHUDCreator()

        focus_model_panel = utility.panel.get_focus_model_panel()
        focus_model_panel_qobject = utility.qt.convert_qwidget_from_modeleditor(focus_model_panel)

        cls.hud_creator.create_all_hud_button(focus_model_panel_qobject)
        cls.grid_creator.create_button(focus_model_panel_qobject)
        cls.custom_hud_creator.create_button(focus_model_panel_qobject)

    @classmethod
    def release(cls):
        cmds.setToolTo(cls.current_context)

        cls.hud_creator.delete_all_button()
        cls.grid_creator.delete_button()
        cls.custom_hud_creator.delete_button()


class ButtonForMayaModelEditorHUD(object):
    """MayaHUD用のButton
    """
    @classmethod
    def create_hudbutton(cls, parent_widget, text, position, function):
        """HUD用のボタンを追加する
        """
        my_button = QtWidgets.QPushButton(parent_widget)
        my_button.setText(text)

        # 透明にしたいが、MayaUI以下だと背景色がとれないのか、黒になる。
        # MayaのWidgetsは透明化に対応していない
        # my_button.setStyleSheet("QPushButton{background: transparent;}")
        # my_button.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        my_button.clicked.connect(function)
        my_button.move(position[0], position[1])  # Relative to top-left corner of viewport

        my_button.show()

        return my_button

    @classmethod
    def delete_qobject(cls, qobject):
        """QObjectを削除する

        :param qobject: 削除したいQObject
        :type qobject: QtWidgets.QObject
        """
        qobject.setParent(None)
        qobject.deleteLater()
        del qobject


class MayaForcalLengthHUDCreator(object):
    """MayaのフォーカルレングスHUD生成機
    """
    CREATE_BUTTON_NAME_LIST = [
        "12",
        "16",
        "25",
        "35",
        "40",
        "50",
        "65",
        "135"
    ]
    WIDTH_MARGIN = 100
    HEIGHT_BASE_MARGIN = 20

    UNIT_NOTATION = "mm"

    def __init__(self):
        self.create_button_list = []

    def change_focal_length_event(self, focal_length, *args):
        """FocalLengthの変更イベント
        ホットキーイベントとして利用

        :param focal_length: 焦点距離
        :type focal_length: int
        """
        target_camera = utility.panel.get_camera_from_focus_model_panel()
        cmds.setAttr("{}.focalLength".format(target_camera), focal_length)
        utility.mevent.MEventManager.post_user_event(ViewToggleToolContext.call_back)

    def create_all_hud_button(self, modelpanel_qojbect):
        """ボタンを作成する
        カット班から頂いたmm単位と個数で生成する

        :param modelpanel_qojbect: ボタンを追加するModelEditorのQObject
        :type modelpanel_qojbect: qobject
        """
        qsize = modelpanel_qojbect.size()

        target_width = qsize.width() - self.WIDTH_MARGIN
        target_height = self.HEIGHT_BASE_MARGIN

        self.create_button_list = []
        for i, name in enumerate(self.CREATE_BUTTON_NAME_LIST):
            create_point = (target_width, target_height * (i + 1))

            button_event = functools.partial(self.change_focal_length_event, int(name))

            name = name + self.UNIT_NOTATION

            create_button = ButtonForMayaModelEditorHUD.create_hudbutton(modelpanel_qojbect, name, create_point, button_event)
            self.create_button_list.append(create_button)

    def delete_all_button(self):
        for create_button_qobject in self.create_button_list:
            ButtonForMayaModelEditorHUD.delete_qobject(create_button_qobject)


class MayaGridHUDCreator(object):
    """MayaのグリッドHUDの生成機
    """
    CREATE_BUTTON_TEXT = "Grid On/Off"

    WIDTH_MARGIN = 100
    HEIGHT_BASE_MARGIN = 200

    def __init__(self):
        self.button = None

    def toggle_grid_event(self, *args):
        """グリッド表示切り替えイベント
        """
        from . import CutsceneEditorRegister

        target_view = utility.panel.get_focus_panel()
        drawer = CutsceneEditorRegister.viewport_controller.view_grid_drawermanager.get_drawer_from_view_name(target_view)

        drawer.toggle()

    def create_button(self, modelpanel_qojbect):
        qsize = modelpanel_qojbect.size()
        target_width = qsize.width() - self.WIDTH_MARGIN
        target_height = self.HEIGHT_BASE_MARGIN

        create_point = (target_width, target_height)

        create_button = ButtonForMayaModelEditorHUD.create_hudbutton(modelpanel_qojbect, self.CREATE_BUTTON_TEXT, create_point, self.toggle_grid_event)
        self.button = create_button

    def delete_button(self):
        ButtonForMayaModelEditorHUD.delete_qobject(self.button)

        self.button = None


class CustomHUDCreator(object):
    """カスタムHUD作成機
    """
    CREATE_BUTTON_TEXT = "HUD On/Off"
    WIDTH_MARGIN = 100
    HEIGHT_BASE_MARGIN = 250

    def __init__(self):
        self.button = None

    def toggle_hud_event(self):
        from . import CutsceneEditorRegister
        target_view = utility.panel.get_focus_panel()
        CutsceneEditorRegister.viewport_controller.view_hud_drawermanager.toggle(target_view)

    def create_button(self, modelpanel_qojbect):
        qsize = modelpanel_qojbect.size()
        target_width = qsize.width() - self.WIDTH_MARGIN
        target_height = self.HEIGHT_BASE_MARGIN

        create_point = (target_width, target_height)

        create_button = ButtonForMayaModelEditorHUD.create_hudbutton(modelpanel_qojbect, self.CREATE_BUTTON_TEXT, create_point, self.toggle_hud_event)
        self.button = create_button

    def delete_button(self):
        ButtonForMayaModelEditorHUD.delete_qobject(self.button)
        self.button = None


class YawPitchToolShotcutRegister(object):
    """ヨーピッチツールのショットカット登録機能
    """
    RUNTIME_COMMAND_NAME = "YawPitchTool"
    NAMED_COMMAND_NAME = RUNTIME_COMMAND_NAME + "Command"
    TOOL_ANNOTATION = "YawpitchTool"

    @classmethod
    def register(cls):
        if not cmds.runTimeCommand(cls.RUNTIME_COMMAND_NAME, exists=True):
            cmds.runTimeCommand(cls.RUNTIME_COMMAND_NAME,
                                category="User",
                                commandLanguage="python",
                                command='cmds.setToolTo("yawPitchContext")',
                                default=True,
                                )

            cmds.nameCommand(cls.NAMED_COMMAND_NAME,
                             annotation=cls.TOOL_ANNOTATION,
                             command=cls.RUNTIME_COMMAND_NAME,
                             sourceType="python",
                             default=True)

        cmds.hotkey(keyShortcut="y", name=cls.NAMED_COMMAND_NAME, releaseName="")
