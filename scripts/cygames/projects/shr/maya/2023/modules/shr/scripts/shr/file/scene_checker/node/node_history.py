from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))

def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    if maya_scene_data.current_category == 'ANIMATION':
        return

    DO_NOT_JUDGE_UNNECESSARY_HISTORY:dict = maya_scene_data.current_project_setting.get('DO_NOT_JUDGE_UNNECESSARY_HISTORY')

    checker.result.color = [77, 128, 77]
    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            node: data.CustomNodeData = node
            _bind_flag:bool = False
            _history_flag:bool = False
            # シェイプがないもの排除、ジョイントとか
            if not node.shapes:
                continue

            _historys = cmds.listHistory(node.full_path_name, pruneDagObjects=True, interestLevel=2)
            if not _historys:
                continue

            _dag_poses = cmds.listConnections(node.full_path_name, t='dagPose')

            for _history in _historys:

                if cmds.nodeType(_history) == 'skinCluster':
                    check_result.skining_geometory[node.full_path_name] = _history
                    _bind_flag = True

                if not cmds.nodeType(_history) in DO_NOT_JUDGE_UNNECESSARY_HISTORY:
                    _history_flag = True
                    break

            if _history_flag:
                checker.result.error_nodes.append(node.full_path_name)
                checker.result.error_message_list.append("Has History")

            if _dag_poses and not _bind_flag:
                checker.result.error_nodes.append(node.full_path_name)
                checker.result.error_message_list.append("Not Skinned")

            # skinCluster = [x for x in _historys if cmds.nodeType(x) == 'skinCluster']
            # if skinCluster and node.full_path_name not in check_result.skining_geometory:
            #     # スキンクラスタを覚えて置く
            #     check_result.skining_geometory[node.full_path_name] = skinCluster[0]
            # else:
            #     checker.result.error_nodes.append(node.full_path_name)
            #     checker.result.error_message_list.append("Has History")

            # for shape in node.shapes:


def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):

    if modify_data and modify_data.error_nodes:
        for node in modify_data.error_nodes:
            if not cmds.objExists(node):
                continue
            _bind_skin_flag = False
            _poly_bind_flag = False
            _historys = cmds.listHistory(node, pruneDagObjects=True, interestLevel=2)

            if _historys:
                if "skinCluster" in [cmds.nodeType(x) for x in _historys]:
                    _bind_skin_flag = True
                if not _bind_skin_flag:
                    for _history in _historys:
                        if cmds.nodeType(_history) in ["polyBlindData", "blindDataTemplate"]:
                            try:
                                cmds.delete(_history)
                                _poly_bind_flag = True
                            except BaseException:
                                pass
                    if _poly_bind_flag:
                        modify_result.modify_flag = True
                        modify_result.modify_messages.append(f'Delete [ PolyBlind ] {node}')
                        print("{:-<100}  {}".format(node, "Delete [ PolyBlind ]"))

                    if cmds.listHistory(node, pruneDagObjects=True, interestLevel=2):
                        try:
                            cmds.bakePartialHistory(node, pc=True)
                            modify_result.modify_flag = True
                            modify_result.modify_messages.append(f'Delete [ Non Deformer History ] {node}')
                            print("{:-<100}  {}".format(node, "Delete [ Non Deformer History ]"))
                        except Exception:
                            modify_result.error_flag = True
                            modify_result.error_messages.append(f'!! Could Not Delete [ Non Deformer History ] {node}')
                            print("{:+<100}  {}".format(node, "delete history error"))
                else:
                    try:
                        cmds.delete(node, channels=True)
                        # cmds.bakePartialHistory(node, ppt=True)
                        modify_result.modify_flag = True
                        modify_result.modify_messages.append(f'Delete [ History ] {node}')
                        print("{:-<100}  {}".format(node, "Delete [ History ]"))
                    except Exception:
                        modify_result.error_flag = True
                        modify_result.error_messages.append(f'!! Could Not Delete [ History ] {node}')
                        print("{:+<100}  {}".format(node, "delete history error"))

