import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds
from .. import scene_data


def check(data_type="env", scene_path="", nodes=None):
    """チェックする内容

    Args:
        data_type (str): env, chara, prop
        scene_path (str): scene name
        nodes (list): nodes

    Returns:
        [scene_data.ResultDatas]
    """

    # 複数のエラー情報を入れるもの
    _result_datas = scene_data.ResultDatas()

    for node in nodes:
        # 個々のエラーを入れるもの
        _result = scene_data.ResultData()

        # 大きさのないメッシュに対して調べるとエラーが出るものを省くため大きさ取得
        bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)

        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            continue

        # メッシュの場合トランスフォームノードが必要な場合に
        _transform_node = cmds.listRelatives(node, parent=True, type="transform", fullPath=True)[0]

        # ここでエラーを検出する
        if _transform_node.rsplit("|")[-1] == "pCylinder26":
            # チェッカーのファイル名から取得
            _result.error = ERROR
            # チェッカーの親のディレクトリ名から取得
            _result.category = CATEGORY
            # 引数で取得 env, chara, prop
            _result.data_type = data_type
            # エラーの内容メッセージ
            _result.error_text = "多角形"
            # ノードはリストで入れる
            _result.error_nodes = [_transform_node]

        # エラーを検出した場合追加
        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas


def modify(data_type="env", scene_path="", error_detail="", nodes=None):
    """修正する内容

    Args:
        data_type (str): env, chara, prop
        scene_path (str): scene name
        error_detail (str): 必要があれば詳細内容
        nodes (list): nodes

    Returns:
        success [int]: 修正がなければ-1, 修正成功したら1, 修正失敗したら0
        message [str]: 修正内容
    """
    success = -1
    message = ""

    return success, message