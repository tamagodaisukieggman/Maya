import pathlib


_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
ERROR_EXISTS_COLOR_SET = f'{ERROR}:exists color set'
ERROR_MULTIPLE_COLOR_SET = f'{ERROR}:multiple color set'
ERROR_NOT_KEEP_NAME = f'{ERROR}:no mtk vcolor'
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds

from .. import scene_data


COLOR_SET_NAME = "mtk_vcolor"


def check(data_type="env", scene_path="", nodes=None):
    _result_datas = scene_data.ResultDatas()

    if data_type != "env":
        return

    for node in nodes:
        _result = scene_data.ResultData()
        bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)

        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            continue

        color_sets = cmds.polyColorSet(node, q=True, allColorSets=True)

        if not color_sets:
            continue

        if len(color_sets) != 1:
            _result.error = ERROR_MULTIPLE_COLOR_SET
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "Multiple Color Sets"
            _result.error_nodes = [node]
        elif COLOR_SET_NAME not in color_sets:
            _result.error = ERROR_NOT_KEEP_NAME
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = f"Not Found [ {COLOR_SET_NAME} ] Color Set"
            _result.error_nodes = [node]

        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas



def modify(data_type="env", scene_path="", error_detail="", nodes=None):
    success = -1
    message = ""

    for node in nodes:
        color_sets = cmds.polyColorSet(node, q=True, allColorSets=True)

        if not color_sets:
            continue

        keep_color_set_index = 0
        color_set_exists = COLOR_SET_NAME in color_sets

        if color_set_exists:
            keep_color_set_index = color_sets.index(COLOR_SET_NAME)

        for i, color_set in enumerate(color_sets):
            if color_set_exists and color_set != COLOR_SET_NAME:
                try:
                    cmds.polyColorSet(node, delete=True, colorSet=color_set)
                    message = f'[ {node} ] delete ColorSet [ {color_set} ]'
                    success = 1
                    print(f'{node:-<100}  delete ColorSet [ {color_set} ]')
                except Exception as e:
                    success = 0
                    message = f'[ {node} ] could not delete ColorSet [ {color_set} ]'
                    print(f'{node:-<100}  could not delete ColorSet [ {color_set} ]')
                    print(e)
            elif i == keep_color_set_index:
                try:
                    cmds.polyColorSet(node, rename=True, colorSet=color_set, newColorSet=COLOR_SET_NAME)
                    message = f'[ {node} ] rename ColorSet name [ {color_set} ] to [ {COLOR_SET_NAME} ]'
                    success = 1
                    print(f'{node:-<100} rename ColorSet name [ {color_set} ] to [ {COLOR_SET_NAME} ]')
                except Exception as e:
                    success = 0
                    message = f'[ {node} ] could not rename ColorSet name [ {color_set} ] to [ {COLOR_SET_NAME} ]'
                    print(f'{node:-<100}  could not rename ColorSet name [ {color_set} ] to [ {COLOR_SET_NAME} ]')
                    print(e)


    return success, message