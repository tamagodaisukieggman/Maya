# -*- coding: utf-8 -*-
"""SettingsViewのControllerモジュール"""
from __future__ import annotations

import typing as tp
from typing import TYPE_CHECKING

from shr.cutscene.sequencer import const
from shr.cutscene.utility.dialog import show_error_dialog

from ..config import ActorConfigCollector
from ..screen_writer import ScreenWriterManager
from . import app, view

if TYPE_CHECKING:
    from ..controller import SequencerController


class CreateActorController(object):
    def __init__(self, sequencer: SequencerController):
        print("call CreateActorController __init__")
        self.ui = view.View()
        self.actor_config_collector = ActorConfigCollector()

        self._sequencer = sequencer

        self.setup_event()

    def setup_event(self):
        self.ui.gui.close_button.clicked.connect(self.close_option)
        self.ui.gui.ok_button.clicked.connect(self.clicked_ok_button)
        self.ui.gui.apply_button.clicked.connect(self.clicked_apply_button)
        self.ui.gui.character_box.currentIndexChanged.connect(self.changed_character_box)

    def show_option(self):
        self.ui.gui.character_box.addItems(self.actor_config_collector.collect_actor_name_list())
        self.ui.show()

    def close_option(self):
        self.ui.close()

    def clicked_ok_button(self):
        self.clicked_apply_button()
        self.close_option()

    def clicked_apply_button(self):
        target_group_name = self.ui.gui.actor_name_edit.text()
        target_actor_config_name = self.ui.gui.character_box.currentText()

        group = self._sequencer.find_group(target_group_name)
        if group:
            show_error_dialog("読み込み失敗", "同名のアクターが存在します。")
            return

        actor_config = self.actor_config_collector.get_actor_config_by_actor_name(target_actor_config_name)
        screen_writer_manager = ScreenWriterManager.get_instance()
        screen_writer = screen_writer_manager.create_node()

        actor_creator = app.ActorCreator(actor_config.data, screen_writer)
        actor_path = actor_creator.create_actor(target_group_name)

        self._sequencer._maya_signals.created_group_actor.emit(target_group_name,
                                                               const.EVENT_TYPE_MOTION,
                                                               screen_writer,
                                                               actor_config.config_path,
                                                               actor_path)

    def changed_character_box(self, index):
        name = self.ui.gui.character_box.currentText()
        actor_config = self.actor_config_collector.get_actor_config_by_actor_name(name)

        self.ui.gui.actor_name_edit.setText(actor_config.data.recommended_name)
