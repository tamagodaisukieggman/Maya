import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
ERROR_NO_UV_SET = f'{ERROR}:no uv set'
ERROR_MULTIPLE_UV_SET = f'{ERROR}:multiple uv set'
ERROR_NO_MAP1 = f'{ERROR}:no map1'
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds
import maya.api.OpenMaya as om2
from .. import scene_data


KEEP_UV_SET_NAME = "map1"


def check(data_type="env", scene_path="", nodes=None):
    _result_datas = scene_data.ResultDatas()

    if data_type != "env":
        return

    for node in nodes:
        bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)

        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            continue

        # _transform_node = cmds.listRelatives(node, parent=True, fullPath=True)[0]
        _result = scene_data.ResultData()
        _uv_sets = cmds.polyUVSet(node, q=True, allUVSets=True)
        if not _uv_sets:
            _result.error = ERROR_NO_UV_SET
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "Not Exists UV Set"
            _result.error_nodes = [node]
        elif len(_uv_sets) != 1 and data_type != "chara":
            _result.error = ERROR_MULTIPLE_UV_SET
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "Multiple UV Sets"
            _result.error_nodes = [node]
        elif KEEP_UV_SET_NAME not in _uv_sets:
            _result.error = ERROR_NO_MAP1
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = f"Not Found [ {KEEP_UV_SET_NAME} ] UV Set"
            _result.error_nodes = [node]

        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas

def delete_uv_set(mesh_fn=None, uv_set=None):
    _flag = 0
    if not mesh_fn:
        return _flag
    if not uv_set:
        return _flag
    if uv_set != "map1":
        _uv_sets = mesh_fn.getUVSetNames()
        if _uv_sets and uv_set in _uv_sets:
            mesh_fn.deleteUVSet(uv_set)
            _flag = 1
    return _flag

def rename_uv_set(mesh_fn=None, src_name=None, dst_name=None):
    _flag = 0
    _uv_sets = mesh_fn.getUVSetNames()
    if _uv_sets:
        if dst_name in _uv_sets:
            cmds.warning(u"[ {} ] はすでに存在します".format(dst_name))
        else:
            if src_name in _uv_sets:
                mesh_fn.renameUVSet(src_name, dst_name)
                _flag = 1
    return _flag

def modify(data_type="env", scene_path="", error_detail="", nodes=None):
    success = -1
    message = ""

    # 一応作ったがコメントアウト
    # if error_detail == ERROR_NO_UV_SET.split(":")[-1]:
    #     return success, message

    # selList = om2.MSelectionList()
    # for node in nodes:
    #     selList.add(node)
    #     dagPath = selList.getDagPath(0)
    #     mesh_fn = om2.MFnMesh(dagPath)

    # if not selList:
    #     return success, message

    # for x in range(selList.length()):
    #     dagPath = selList.getDagPath(x)
    #     mesh_fn = om2.MFnMesh(dagPath)
    #     node = dagPath.fullPathName()
    #     _uv_sets = cmds.polyUVSet(node, q=True, allUVSets=True)
    #     if error_detail == ERROR_NO_MAP1.split(":")[-1]:
    #         try:
    #             success = rename_uv_set(mesh_fn, _uv_sets[0], KEEP_UV_SET_NAME)
    #             # cmds.polyUVSet(rename=True, uvSet=_uv_sets[0], newUVSet=KEEP_UV_SET_NAME)
    #             message = f'[ {node} ] rename uvSet name [ {_uv_sets[0]} ] to [ {KEEP_UV_SET_NAME} ]'
    #             print(f'{node:-<100} rename uvSet name [ {_uv_sets[0]} ] to [ {KEEP_UV_SET_NAME} ]')
    #         except Exception as e:
    #             success = 0
    #             message = f'[ {node} ] could not rename uvSet name [ {_uv_sets[0]} ] to [ {KEEP_UV_SET_NAME} ]'
    #             print(f'{node:-<100}  could not rename uvSet name [ {_uv_sets[0]} ] to [ {KEEP_UV_SET_NAME} ]')
    #             print(e)

    #     if error_detail == ERROR_MULTIPLE_UV_SET.split(":")[-1]:
    #         _map1_flag = KEEP_UV_SET_NAME in _uv_sets
    #         if _map1_flag:
    #             for i, uv_set in enumerate(_uv_sets):
    #                 if uv_set != KEEP_UV_SET_NAME:
    #                     try:
    #                         success = delete_uv_set(mesh_fn, uv_set)
    #                         # cmds.polyUVSet(delete=True, uvSet=uv_set)
    #                         message = f'[ {node} ] delete uvSet [ {uv_set} ]'
    #                         print(f'{node:-<100}  delete uvSet [ {uv_set} ]')
    #                     except Exception as e:
    #                         success = 0
    #                         message = f'[ {node} ] could not delete uvSet [ {uv_set} ]'
    #                         print(f'{node:-<100}  could not delete uvSet [ {uv_set} ]')
    #                         print(e)
    #         else:
    #             for i, uv_set in enumerate(_uv_sets):
    #                 if i != 0:
    #                     try:
    #                         success = delete_uv_set(mesh_fn, uv_set)
    #                         # cmds.polyUVSet(delete=True, uvSet=uv_set)
    #                         message = f'[ {node} ] delete uvSet [ {uv_set} ]'
    #                         print(f'{node:-<100}  delete uvSet [ {uv_set} ]')
    #                     except Exception as e:
    #                         success = 0
    #                         message = f'[ {node} ] could not delete uvSet [ {uv_set} ]'
    #                         print(f'{node:-<100}  could not delete uvSet [ {uv_set} ]')
    #                         print(e)

    return success, message

def modify_cmds(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""

    if error_detail == ERROR_NO_UV_SET.split(":")[-1]:
        return success, message

    node = node[0]
    _uv_sets = cmds.polyUVSet(node, q=True, allUVSets=True)
    if error_detail == ERROR_NO_MAP1.split(":")[-1]:
        try:
            cmds.polyUVSet(rename=True, uvSet=_uv_sets[0], newUVSet=KEEP_UV_SET_NAME)
            message = f'[ {node} ] rename uvSet name [ {_uv_sets[0]} ] to [ {KEEP_UV_SET_NAME} ]'
            success = 1
            print(f'{node:-<100} rename uvSet name [ {_uv_sets[0]} ] to [ {KEEP_UV_SET_NAME} ]')
        except Exception as e:
            success = 0
            message = f'[ {node} ] could not rename uvSet name [ {_uv_sets[0]} ] to [ {KEEP_UV_SET_NAME} ]'
            print(f'{node:-<100}  could not rename uvSet name [ {_uv_sets[0]} ] to [ {KEEP_UV_SET_NAME} ]')
            print(e)

    if error_detail == ERROR_MULTIPLE_UV_SET.split(":")[-1]:
        _map1_flag = KEEP_UV_SET_NAME in _uv_sets
        if _map1_flag:
            for i, uv_set in enumerate(_uv_sets):
                if uv_set != KEEP_UV_SET_NAME:
                    try:
                        cmds.polyUVSet(delete=True, uvSet=uv_set)
                        message = f'[ {node} ] delete uvSet [ {uv_set} ]'
                        success = 1
                        print(f'{node:-<100}  delete uvSet [ {uv_set} ]')
                    except Exception as e:
                        success = 0
                        message = f'[ {node} ] could not delete uvSet [ {uv_set} ]'
                        print(f'{node:-<100}  could not delete uvSet [ {uv_set} ]')
                        print(e)
        else:
            for i, uv_set in enumerate(_uv_sets):
                if i != 0:
                    try:
                        cmds.polyUVSet(delete=True, uvSet=uv_set)
                        message = f'[ {node} ] delete uvSet [ {uv_set} ]'
                        success = 1
                        print(f'{node:-<100}  delete uvSet [ {uv_set} ]')
                    except Exception as e:
                        success = 0
                        message = f'[ {node} ] could not delete uvSet [ {uv_set} ]'
                        print(f'{node:-<100}  could not delete uvSet [ {uv_set} ]')
                        print(e)

    return success, message