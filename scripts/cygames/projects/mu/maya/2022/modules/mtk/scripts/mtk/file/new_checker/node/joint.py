import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds
import maya.api.OpenMaya as om2
from .. import scene_data

ROUND_VALUE = 3


WITH_INDEX_JOINT_NAMES = ["skl", "face", "helper"]
WITH_INDEX_JOINT_INDEX = [3000, 4000, 5000]
_with_index_joint_dict = dict([x, y] for x, y in zip(WITH_INDEX_JOINT_NAMES, WITH_INDEX_JOINT_INDEX))
NO_INDEX_JOINT_NAMES = ["mtp", "cnp", "move"]

JOINT_PREFIX = "jnt"

ROOT_JOINT_NAME = "jnt_0000_skl_root"



def check_joint_type_index(data_type="env", jnt="", _result=None):
    jnt_short_name = jnt.split("|")[-1]
    name_split = jnt_short_name.split("_")
    current_index = name_split[1]
    current_index_int = int(current_index)

    if name_split[2] in WITH_INDEX_JOINT_NAMES:
        """
        jnt_0000_[ skl ]_something が"skl", "face", "helper"であるか
        """
        if name_split[2] == WITH_INDEX_JOINT_NAMES[0]:
            """
            jnt_0000_[ skl ]_somethingが[ skl ]の場合indexは3000未満
            """
            if not 0 < current_index_int < 3000:
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = f"[ {name_split[1]} ]のindexは[ {3000} ]未満の整数です"
                _result.error_nodes = [jnt]

        elif name_split[2] == WITH_INDEX_JOINT_NAMES[1]:
            """
            jnt_0000_[ face ]_somethingが[ face ]の場合indexは4000未満
            """
            if not 3000 <= current_index_int < 4000:
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = f"[ {name_split[1]} ]のindexは[ {3000} ]以上[ {4000} ]未満の整数です"
                _result.error_nodes = [jnt]

        elif name_split[2] == WITH_INDEX_JOINT_NAMES[2]:
            """
            jnt_0000_[ helper ]_somethingが[ helper ]の場合indexは5000未満
            """
            if not 4000 <= current_index_int < 5000:
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = f"[ {name_split[1]} ]のindexは[ {4000} ]以上[ {5000} ]未満の整数です"
                _result.error_nodes = [jnt]

    return _result

def check_joint_brother(data_type="env", jnt="", _result=None):
    jnt_short_name = jnt.split("|")[-1]
    name_split = jnt_short_name.split("_")
    parent_jnt = cmds.listRelatives(jnt, parent=True, fullPath=True, type="joint")[0]
    current_index = name_split[1]
    current_index_int = int(current_index)

    brother_joints = cmds.listRelatives(parent_jnt, children=True, fullPath=True, type="joint")
    if jnt[-1] == "L":
        _current_type = jnt_short_name.split("_")[3]
        same_type_joints = [x for x in brother_joints if (x.split("|")[-1].split("_")[2] == name_split[2]
                                            and x.split("|")[-1].split("_")[3] == _current_type
                                            and x != jnt)]
        r_joints = [x for x in same_type_joints if x.split("|")[-1].split("_")[-1] == "R"]
        if r_joints:
            # if len(r_joints) > 1:
            #     texts.append(u"[ {} ] indexの値が不正".format(name_split[1]))
            #     types.append("Joint name")
            #     error_nodes.append(jnt)
            #     print("index value error {:-^20} {}".format("", jnt))
            r_joints = r_joints[0]
            if not brother_joints.index(jnt) < brother_joints.index(r_joints):
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = f"[ R ] Jointは [ L ] よりも下"
                _result.error_nodes = [r_joints]

            # _l_joint_position = [round(x, ROUND_VALUE) for x in cmds.joint(jnt, q=True, position=True)]
            # _r_joint_position = [round(x, ROUND_VALUE) for x in cmds.joint(r_joints, q=True, position=True)]
            _l_joint_position = om2.MVector([round(x, ROUND_VALUE) for x in cmds.getAttr("{}.t".format(jnt))[0]])
            _r_joint_position = om2.MVector([round(x, ROUND_VALUE) for x in cmds.getAttr("{}.t".format(r_joints))[0]])
            _l_joint_orientation = om2.MVector([round(x, ROUND_VALUE) for x in cmds.getAttr("{}.r".format(jnt))[0]])
            _r_joint_orientation = om2.MVector([round(x, ROUND_VALUE) for x in cmds.getAttr("{}.r".format(r_joints))[0]])

            _rer_pos = om2.MVector([_l_joint_position[0]*-1,_l_joint_position[1],_l_joint_position[2]])

            if _rer_pos != _r_joint_position:
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = "[ R ] [ L ] で位置が違う"
                _result.error_nodes = [r_joints, jnt]

            # ちょっと強引だが左右の骨の回転は絶対値で見ている
            if _l_joint_orientation != -_r_joint_orientation or not _l_joint_orientation == _r_joint_orientation:
                if not [abs(x) for x in _l_joint_orientation] == [abs(x) for x in _r_joint_orientation]:
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = "[ R ] [ L ] で回転が違う"
                    _result.error_nodes = [r_joints, jnt]

        elif same_type_joints:
            same_type_joint = same_type_joints[0]
            if same_type_joint.split("|")[-1].split("_")[4] != "R":
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = "[ R ] 以外のジョイント"
                _result.error_nodes = [same_type_joint]

    for i,brother_joint in enumerate(brother_joints):

        brother_joint_short_name = brother_joint.split("|")[-1]
        brother_name_split = brother_joint_short_name.split("_")
        brother_index = brother_name_split[1]

        """
        "mtp", "cnp", "move"でなければindexの値を見る
        """
        if brother_index not in NO_INDEX_JOINT_NAMES:
            if brother_index.isdecimal():
                brother_index_int = int(brother_index)

                """
                indexの最初の桁が同じ数のものを確認
                """
                if current_index[0] == brother_index[0]:
                    # print(brother_joints.index(jnt),brother_joints.index(brother_joint))
                    # print(brother_index_int,current_index_int)
                    # print(brother_joint_short_name)

                    """
                    現在のジョイントindexが兄弟のジョイントindexより小さく
                    """
                    if (brother_index_int > current_index_int
                        and not brother_joints.index(jnt) < brother_joints.index(brother_joint)
                        and jnt not in _result.error_nodes):

                        _result.error = ERROR
                        _result.category = CATEGORY
                        _result.data_type = data_type
                        _result.error_text = f"[ {name_split[1]} ] indexの値が不正"
                        _result.error_nodes = [jnt]

    return _result

def check_index_value(data_type="env", jnt="", _result=None):
    jnt_short_name = jnt.split("|")[-1]
    name_split = jnt_short_name.split("_")
    parent_jnt = cmds.listRelatives(jnt, parent=True, fullPath=True, type="joint")[0]
    parent_jnt_short_name = parent_jnt.split("|")[-1]
    current_index = name_split[1]
    current_index_int = int(current_index)

    parent_index_int = parent_jnt_short_name.split("_")[1]

    inverseScale = cmds.listConnections(parent_jnt, plugs=True, source=True, type="joint")
    if not inverseScale:
        _result.error = ERROR
        _result.category = CATEGORY
        _result.data_type = data_type
        _result.error_text = "インバーススケールがない"
        _result.error_nodes = [jnt]

    else:
        inverseScale = [x for x in inverseScale
                        if x.endswith("inverseScale") and x.startswith(jnt_short_name)]
        if not inverseScale:
            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "インバーススケールがない"
            _result.error_nodes = [jnt]

    if parent_index_int.isdecimal():
        parent_index_int = int(parent_index_int)
        if not parent_index_int < current_index_int:
            child_jnt = cmds.listRelatives(jnt, children=True, fullPath=True, type="joint")
            if child_jnt:
                child_short_name = child_jnt[0].split("|")[-1]
                child_index_int = child_short_name.split("_")[1]
                if child_index_int.isdecimal():
                    child_index_int = int(child_index_int)
                    if not child_index_int > current_index_int:
                        _result.error = ERROR
                        _result.category = CATEGORY
                        _result.data_type = data_type
                        _result.error_text = "indexの値が親のジョイントよりもより小さい"
                        _result.error_nodes = child_jnt

                    elif not parent_index_int < child_index_int:
                        _result.error = ERROR
                        _result.category = CATEGORY
                        _result.data_type = data_type
                        _result.error_text = "indexの値が子のジョイントよりも大きい"
                        _result.error_nodes = [parent_jnt]

                    else:
                        _result.error = ERROR
                        _result.category = CATEGORY
                        _result.data_type = data_type
                        _result.error_text = "indexの値が親のジョイントよりもより小さい"
                        _result.error_nodes = [jnt]

            else:
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = "indexの値が子のジョイントよりもより大きい"
                _result.error_nodes = [parent_jnt]

    return _result


def joint_check(data_type="env", joints=None):

    _result_datas = scene_data.ResultDatas()
    index_dict = {}


    # ジョイントを階層順に並べ替える
    # 先頭がルートのジョイントとなるので、それを抜き出す
    # ルートは「jnt_0000_skl_root」
    joints = sorted(joints, key=lambda x:len(x.split("|")))

    memory_joints = []
    _root_jnt = []
    for jnt in joints:
        _result = scene_data.ResultData()
        jnt_hierarche_names = jnt.split("|")
        jnt_short_name = jnt_hierarche_names[-1]
        parent_jnt = cmds.listRelatives(jnt, parent=True, fullPath=True, type="joint")

        if jnt_short_name not in memory_joints:
            memory_joints.append(jnt_short_name)
        else:
            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "同名のジョイントがある"
            _result.error_nodes = [jnt]

        name_split = jnt_short_name.split("_")

        """
        アンダーバーは必ず2つは必要 :　jnt_move_root
        """
        if len(name_split) < 3:
            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "アンダーバーが必要"
            _result.error_nodes = [jnt]

        if not parent_jnt:
            # child_jnt = cmds.listRelatives(jnt, children=True, fullPath=True, type="joint")
            if not _root_jnt:
                _root_jnt.append(jnt)
                if ROOT_JOINT_NAME in jnt_short_name:
                    if ROOT_JOINT_NAME == jnt_short_name:
                        continue
                    else:
                        _result.error = ERROR
                        _result.category = CATEGORY
                        _result.data_type = data_type
                        _result.error_text = "root joint の名前が違う"
                        _result.error_nodes = [jnt]

                else:
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = "root joint の名前が違う"
                    _result.error_nodes = [jnt]

            else:
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = "root joint が複数ある"
                _result.error_nodes = [jnt]

        else:
            parent_jnt = parent_jnt[0]
            """
            jnt で始まっている必要がある
            """
            if name_split[0] != JOINT_PREFIX:
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = f"[ {JOINT_PREFIX} ]で始まっていない"
                _result.error_nodes = [jnt]
                continue
            else:

                """
                "mtp", "cnp", "move"は特殊なのでindexは見ない
                """
                if name_split[1] in NO_INDEX_JOINT_NAMES:
                    continue

                # parent_jnt_short_name = parent_jnt.split("|")[-1]
                current_index = name_split[1]

                """
                jnt_[ 0000 ]_skl_root indexが整数かを確認
                """
                if current_index.isdecimal():
                    current_index_int = int(current_index)
                    if current_index_int not in list(index_dict.keys()):
                        index_dict[current_index_int] = jnt
                    else:
                        same_id_joint = index_dict.get(current_index_int, None)
                        _result.error = ERROR
                        _result.category = CATEGORY
                        _result.data_type = data_type
                        _result.error_text = f"[ {current_index} ] 同じindexが既にあり"
                        _result.error_nodes = [jnt, same_id_joint]

                    """
                    texts.append(u"{}_[ {} ]_{} indexが整数ではない".format(name_split[0], name_split[1], "_".join(name_split[2:])))
                    indexが4桁の整数であるかの確認
                    """
                    if len(current_index) != 4:
                        _m = f'{name_split[0]}_[ {name_split[1]} ] '
                        _m += f'_{"_".join(name_split[2:])} indexが4桁の整数ではない'
                        _result.error = ERROR
                        _result.category = CATEGORY
                        _result.data_type = data_type
                        _result.error_text = _m
                        _result.error_nodes = [jnt]

                    else:
                        check_joint_type_index(data_type, jnt, _result)
                        # print(jnt, " ----")
                        # print(name_split[2])
                        # if not _result.error:
                        #     _m = f'{"_".join(name_split[:2])}_ [ {name_split[2]} ] '
                        #     _m += f'_{"_".join(name_split[3:])} 仕様にない命名'
                        #     _result.error = ERROR
                        #     _result.category = CATEGORY
                        #     _result.data_type = data_type
                        #     _result.error_text = _m
                        #     _result.error_nodes = [jnt]

                        """
                        同一階層のindexの大きさを確認
                        アウトライナの並びが上のものがindexの値が小さい
                        """
                        check_joint_brother(data_type, jnt, _result)
                        check_index_value(data_type, jnt, _result)

                else:
                    _m = f'{name_split[0]}_[ {name_split[1]} ]_'
                    _m += f'{"_".join(name_split[2:])} index部分が整数ではない'
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = _m
                    _result.error_nodes = [jnt]

        if _result.error_nodes:
            _result_datas.set_data_obj(_result)

    return _result_datas

def check(data_type="env", scene_path="", nodes=None):
    _result_datas = None

    _all_joint = sorted([x for x in cmds.listRelatives(nodes,
                                        allDescendents=True,
                                        fullPath=True)if cmds.nodeType(x)=="joint"])
    if not _all_joint:
        return

    _result_datas = joint_check(data_type="env", joints=_all_joint)

    return _result_datas

def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    return success, message