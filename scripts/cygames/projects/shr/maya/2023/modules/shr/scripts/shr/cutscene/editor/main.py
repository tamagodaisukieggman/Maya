# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os
import re

from . import viewport
from . import hotkey
from . import callback
from . import menuregister
from .. import camerasequencer_range_slider_syncer
from .. import range_slider_panel_width_syncer

from maya import cmds, mel
from shr.utils import getCurrentSceneFilePath


class CutsceneEditorRegister(object):

    viewport_controller = None

    @classmethod
    def register(cls):
        """エディターへの拡張機能を追加する
        # TODO: 現状Camera Sequencerになってるが、未来的には内製Sequencerに変更する
        """
        if CutsceneExtensionSwitcher.instance:
            if not CutsceneExtensionSwitcher.instance.is_work_scene:

                mel.eval("GraphEditor")
                mel.eval("DopeSheetEditor")

                cls.viewport_controller = viewport.ViewPortController()
                cls.viewport_controller.show_view_port()

                menuregister.CameraMenuRegister.register()
                menuregister.ToolsMenuRegster.register()

                hotkey.CameraSequencerHotkeyRegister.register()
                callback.ViewPortCallBackRegister.register()

                camerasequencer_range_slider_syncer.start_sync()
                range_slider_panel_width_syncer.start_sync()

                # TODO: 増えてくる様であればcut班用の設定クラスを作る
                # 非表示ノードを評価しない様にする。こうする事で高速化できるが、リグなどで問題になる可能性がある。
                # その為、問題が起きたらOffにする。
                cmds.evaluator(name="invisibility", en=True)

                CutsceneExtensionSwitcher.instance.is_work_scene = True
        else:
            # Reloadなどでstartup.cutscene_extension_switcher_instanceが消滅する
            CutsceneExtensionSwitcher.instance = CutsceneExtensionSwitcher()

    @classmethod
    def unregister(cls):
        """エディターへの拡張機能を削除する
        # TODO: 現状Camera Sequencerになってるが、未来的には内製Sequencerに変更する
        """

        if (cls.viewport_controller):
            cls.viewport_controller.close_view_port()
            cls.viewport_controller = None

        menuregister.CameraMenuRegister.unregister()
        menuregister.ToolsMenuRegster.unregister()

        hotkey.CameraSequencerHotkeyRegister.unregister()
        callback.ViewPortCallBackRegister.unregister()

        camerasequencer_range_slider_syncer.end_sync()
        range_slider_panel_width_syncer.end_sync()

        CutsceneExtensionSwitcher.instance.is_work_scene = False


class CutsceneExtensionSwitcher(object):
    WORKSCENE_NAME = "cut_sq"
    WORKSCENE_NAME_REGEX = re.compile(r"^{}.*".format(WORKSCENE_NAME))

    instance = None

    def __init__(self):
        self.is_work_scene = False

    def switch(self):
        scene_path = getCurrentSceneFilePath()
        if not scene_path:
            # 空 = 新規シーンなので、拡張機能をOffにする
            self.off()
            return

        scene_name = os.path.basename(scene_path)
        now_work_scene = self.WORKSCENE_NAME_REGEX.search(scene_name)

        # 該当するシーン名
        if now_work_scene:
            self.on()

        # 該当しないシーン名
        else:
            self.off()

    def on(self):
        from shr.cutscene.editor.main import CutsceneEditorRegister
        if self.is_work_scene:
            CutsceneEditorRegister.viewport_controller.change_cutscene_layout()
        else:
            CutsceneEditorRegister.register()
            self.is_work_scene = True

    def off(self):
        if self.is_work_scene:
            CutsceneEditorRegister.unregister()
            self.is_work_scene = False

        # ワークシーンじゃない and 直前もワークシーンではない。
        else:
            # 何もしない
            pass


def create_cutscene_extension_switcher_job():
    """カットシーンの拡張機能切り替え機能ジョブを作成する

    MayaのSceneOpenedのscriptJobでファイル名を監視、該当するシーンであれば拡張機能機能をOnにする処理を追加
    """
    CutsceneExtensionSwitcher.instance = CutsceneExtensionSwitcher()

    cmds.scriptJob(event=["SceneOpened", CutsceneExtensionSwitcher.instance.switch])
