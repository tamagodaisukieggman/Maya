from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):

    checker.result.color = [77, 154, 51]

    _reference_nodes = [x for x in cmds.ls(type='reference',
                                           long=True) if not "sharedReferenceNode" in x]
    if _reference_nodes:
        for _reference_node in _reference_nodes:
            if not cmds.referenceQuery(_reference_node, isNodeReferenced=True):
                continue
            reference_file_path = Path(cmds.referenceQuery(_reference_node, filename=True))

            if not reference_file_path.exists():
                checker.result.error_nodes.append(_reference_node)
                checker.result.error_message_list.append('Not Exists Reference')



def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    return