from maya import cmds
from shr.cutscene.sequencer import const
from shr.cutscene.sequencer.api import *
from shr.cutscene.sequencer.config import ActorConfig
from shr.cutscene.sequencer.lib import reference
from shr.cutscene.sequencer.lib.event import is_sequencer_track


class ReferenceVisibleSelector(object):
    def __init__(self, sequencer: Sequencer):
        self._sequencer = sequencer

    def set_all_actor_visible(self, is_show):
        """全アクターの表示状態を更新する
        """
        groups = self._sequencer.get_all_groups()
        for group in groups:
            self.set_group_visible(group, is_show)

    def set_all_clip_visible(self, is_show):
        """全Clipの表示状態を更新する
        """
        clips = self._sequencer.get_all_clips()
        for clip in clips:
            self.set_clip_visible(clip, is_show)

    def set_group_visible(self, group: SequencerGroupTrackData, is_show):
        nodes = self._collect_actor_nodes(group)
        self._set_nodes_visible(nodes, is_show)

    def _collect_actor_nodes(self, group: SequencerGroupTrackData) -> tp.List[str]:
        event_type = group.get_event_type()

        if not is_sequencer_track(event_type):
            return []

        group_property = group.get_property()
        actor_config_path = group_property[const.Event.GROUP_ACTOR_CONFIG_PATH]
        reference_node = group_property[const.Event.GROUP_REFERENCE_PATH]
        config = ActorConfig(actor_config_path)
        ref_node = cmds.referenceQuery(reference_node, referenceNode=True)
        namespace = reference.get_namespace(ref_node)

        actor_nodes = config.get_actor_nodes(namespace)

        return actor_nodes

    def set_clip_visible(self, clip: SequencerClipData, is_show):
        # set_all_actor_visible(False)
        clip_nodes = self._collect_clip_nodes(clip)
        self._set_nodes_visible(clip_nodes, is_show)

    def _collect_clip_nodes(self, clip: SequencerClipData) -> tp.List[str]:
        """クリッのノードを収集する

        Args:
            clip (SequencerClipData): 対象のクリップ

        Returns:
            list[str]: ノードリスト
        """
        clip_nodes = []
        group = clip.get_parent_track()
        if not group:
            return

        event_type = group.get_event_type()
        if not is_sequencer_track(event_type):
            return []

        config = ActorConfig(group.get_property()[const.Event.GROUP_ACTOR_CONFIG_PATH])

        ref_node = cmds.referenceQuery(clip.get_clip_property()[const.Event.EVENT_REFERENCE_PATH], referenceNode=True)
        namespace = reference.get_namespace(ref_node)
        nodes = config.get_motion_nodes(namespace)

        return nodes

    def _set_nodes_visible(self, nodes, is_show):
        is_auto_key = cmds.autoKeyframe(query=True, state=True)

        cmds.autoKeyframe(edit=True, state=False)

        if is_show:
            cmds.showHidden(nodes)
        else:
            cmds.hide(nodes)

        cmds.autoKeyframe(edit=True, state=is_auto_key)
