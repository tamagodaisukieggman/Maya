from __future__ import annotations

import typing as tp

# from cy.datatype import typedef
from maya import cmds
from mtk.cutscene.sequencer import const
from mtk.cutscene.sequencer.api import *
from mtk.cutscene.sequencer.config.collector import ActorConfig
from mtk.cutscene.sequencer.lib import reference
from mtk.cutscene.sequencer.lib.event import is_sequencer_track
from PySide2 import QtGui


class OutlinerActorData:
    def __init__(self, group: SequencerGroupTrackData) -> None:
        self._group = group

        self.name = group.display_name()
        self._property = self._group.get_property()
        self._event_type = self._group.get_event_type()

        self._config_path = self._property[const.Event.GROUP_ACTOR_CONFIG_PATH]
        self._reference_path = self._property[const.Event.GROUP_REFERENCE_PATH]
        self.config = ActorConfig(self._config_path)
        self.actor_node = self._collect_actor_node()

        self.motion_data: tp.List[OutlinerMotionData] = []

    def _collect_actor_node(self):
        namespace = reference.get_namespace(self._reference_path)
        return self.config.get_actor_nodes(namespace)

    def append_motion(self, clip: SequencerClipData):
        color_code = clip.track_data().get_element_color()

        self.motion_data.append(OutlinerMotionData(clip, self.config))


class OutlinerMotionData:
    def __init__(self, clip: SequencerClipData, config: ActorConfig) -> None:
        self._clip = clip
        self._property = self._clip.get_clip_property()
        self._reference_path = self._property[const.Event.EVENT_REFERENCE_PATH]
        self._config = config
        self.name = clip.get_label()
        self.background_color = QtGui.QColor(clip.track_data().get_element_color())
        self.background_color.setAlphaF(0.5)

        self.motion_nodes = self._collect_clip_node(self._reference_path)

    def _collect_clip_node(self, reference_path_path: str):
        namespace = reference.get_namespace(reference_path_path)
        return self._config.get_motion_nodes(namespace)


def collect_actor_data() -> tp.List[OutlinerActorData]:
    from mtk.cutscene.sequencer.controller import SequencerController
    seq = SequencerController.get_instance()
    clips = seq.get_all_clips()

    group_list: tp.List[OutlinerActorData] = []
    exists_groups: tp.Dict[str, OutlinerActorData] = {}
    for clip in clips:
        group = clip.get_parent_track()
        event_type = group.get_event_type()
        if not is_sequencer_track(event_type):
            continue

        group = clip.get_parent_track()
        group_name = group.display_name()
        if group_name in exists_groups:
            exists_groups[group_name].append_motion(clip)
        else:
            data = OutlinerActorData(group)
            group_list.append(data)
            exists_groups[group_name] = data
            data.append_motion(clip)

    return group_list
