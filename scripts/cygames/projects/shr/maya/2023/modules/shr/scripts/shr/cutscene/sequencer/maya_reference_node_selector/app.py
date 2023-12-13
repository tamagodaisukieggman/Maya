from maya import cmds
from shr.cutscene.sequencer.api import *
from shr.cutscene.sequencer.config import ActorConfig


class ReferenceNodeSelector(object):
    def __init__(self, sequencer: Sequencer):
        self._sequencer = sequencer

    def select(self, clip: SequencerClipData):
        group = clip.get_parent_track()
        config_path = group.actor_config_path

        ref_path = clip.reference_node()
        namespace = cmds.referenceQuery(ref_path, namespace=True)

        config = ActorConfig(config_path)

        nodes = config.get_motion_nodes(namespace)

        cmds.select(nodes)
