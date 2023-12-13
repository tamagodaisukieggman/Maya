import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds
from .. import scene_data

# 丸めの桁数
_round_value = 4


def check(data_type="env", scene_path="", node=None):

    # 背景データの場合は除外
    if data_type == "env":
        return

    error_nodes = []
    _result_datas = scene_data.ResultDatas()

    _all_transform = [x for x in cmds.listRelatives(node,
                                            allDescendents=True,
                                            fullPath=True)if cmds.nodeType(x)=="transform"]

    """
    子にシェイプを持たないノードを
    つまりグループノードのみを抽出
    """
    _all_group_nodes = [x for x in _all_transform if not cmds.listRelatives(x, s=True)]

    """
    ルートノードがないのでルートノードを追加
    """
    _all_transform.append(node)
    _all_group_nodes.append(node)


    """
    キーフレームの存在チェック
    全トランスフォームノードに対して行う
    """

    for _transform_node in _all_transform:
        _result = scene_data.ResultData()

        _transform_value = cmds.xform(_transform_node, q=True, t=True, os=True)
        _rotate_value = cmds.xform(_transform_node, q=True, ro=True, os=True)

        _scale_value = cmds.getAttr("{}.s".format(_transform_node))[0]

        # 必要に応じてピボットの値も検査できるように
        # _os_scale_pivot = cmds.xform(_transform_node, q=True, sp=True, os=True)
        # _os_rotate_pivot = cmds.xform(_transform_node, q=True, rp=True, os=True)
        # _ws_scale_pivot = cmds.xform(_transform_node, q=True, sp=True, ws=True)
        # _ws_rotate_pivot = cmds.xform(_transform_node, q=True, rp=True, ws=True)
        # _os_scale_pivot = [round(x, _round_value) for x in _os_scale_pivot]
        # _os_rotate_pivot = [round(x, _round_value) for x in _os_rotate_pivot]
        # _ws_scale_pivot = [round(x, _round_value) for x in _ws_scale_pivot]
        # _ws_rotate_pivot = [round(x, _round_value) for x in _ws_rotate_pivot]

        _transform_value = [round(x, _round_value) for x in _transform_value]
        _rotate_value = [round(x, _round_value) for x in _rotate_value]
        _scale_value = [round(x, _round_value) for x in _scale_value]

        if _transform_value != [0.0, 0.0, 0.0] or _rotate_value != [0.0, 0.0, 0.0]:
            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "Not Freeze Transformatins"
            _result.error_nodes = [_transform_node]
            _result.error_type_color = [90, 90, 175]
            error_nodes.append(_transform_node)

        if _scale_value != [1.0, 1.0, 1.0] and _transform_node not in error_nodes:
            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "Not Scale [ 1, 1, 1 ]"
            _result.error_nodes = [_transform_node]
            _result.error_type_color = [90, 90, 175]

        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas


def unlock_attribute(node, attr):
    """
    connectionInfo を使わないとロックを解除できないケースがある
    ただ、その場合はconnectionInfoで取得する前に一度setAttrでロックを解除しておく必要があるようだ
    """
    for _axis in ["x", "y", "z"]:
        cmds.setAttr("{}.{}{}".format(node, attr, _axis), l=False)
        plug_name = cmds.connectionInfo("{}.{}{}".format(node, attr, _axis), gla=True)
        # print(plug_name, "-----plug_name")
        if plug_name:
            cmds.setAttr(plug_name, l=False)


def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    _cld = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="transform")

    if _cld:
        for _c in sorted(_cld, key=lambda x: len(x.split("|")), reverse=True):
            cmds.lockNode(_c, lock=False)
            for attr in ["t", "r", "s"]:
                unlock_attribute(_c, attr)

    try:
        cmds.makeIdentity(node, apply=True, t=True, r=True, s=True, n=False, pn=True)
        message = f"Freeze Transformatins [ {node} ]"
        print("{:-<100}  {}".format(node, "freeze transformatins"))
        success = 1
    except Exception as e:
        message = f"!! Could not Freeze Transformatins [ {node} ]"
        success = 0
        print(e, " ++ freeze transformatins error")
        print("{:+<100}  {}".format(node, "freeze transformatins error"))
    return success, message