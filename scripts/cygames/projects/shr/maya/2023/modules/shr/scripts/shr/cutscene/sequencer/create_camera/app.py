from __future__ import annotations

from typing import TYPE_CHECKING

from shr.cutscene.sequencer import const

from ..config.collector import CameraConfigCollector
from ..create_actor import ActorCreator
from ..screen_writer import ScreenWriterManager

if TYPE_CHECKING:
    from ..controller import SequencerController


class CameraCreator(object):
    def __init__(self, sequencer: SequencerController):
        self._sequencer = sequencer

    def create_camera(self):
        actor_config = CameraConfigCollector().get_actor_config_by_actor_name("camera")
        screen_writer_manager = ScreenWriterManager.get_instance()
        screen_writer_path = screen_writer_manager.create_node()

        actor_creator = ActorCreator(actor_config.data, screen_writer_path)
        actor_path = actor_creator.create_actor("MainCamera")
        self._sequencer._maya_signals.created_group_actor.emit("main",
                                                               const.EVENT_TYPE_CAMERA,
                                                               screen_writer_path,
                                                               actor_config.config_path,
                                                               actor_path)
