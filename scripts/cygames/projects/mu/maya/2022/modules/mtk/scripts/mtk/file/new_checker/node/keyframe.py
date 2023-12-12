import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds
from .. import scene_data

def check(data_type="env", scene_path="", node=None):

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

    for _transform in _all_transform:
        _result = scene_data.ResultData()
        if cmds.keyframe(_transform, q=True):
            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "キーフレームが存在"
            _result.error_nodes = [_transform]
        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas


def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    try:
        cmds.cutKey(node, cl=True)
        # self.modifies.append(u"[ {} ] の [ キーフレーム ] を削除".format(node))
        print("{:-<100}  {}".format(node, "delete key frame"))
        success = 1
        message = f'[ {node} ] の [ キーフレーム ] を削除'
        # print(node, " -- delete key frame")
    except Exception as e:
        success = 0
        message = f'[ {node} ] の [ キーフレーム ] を削除できない'
        # self.modify_errors.append(u"!! [ {} ] の [ キーフレーム ] を削除できない".format(node))
        print(e, " ++ delete key frame error")
        print("{:+<100}  {}".format(node, "delete key frame error"))
    return success, message