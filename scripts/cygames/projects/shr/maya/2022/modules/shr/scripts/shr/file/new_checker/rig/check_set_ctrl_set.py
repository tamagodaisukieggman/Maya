# -*- coding: utf-8 -*-

from maya import cmds

def get_set_members(_set):
    _sets = []
    if cmds.nodeType(_set) == "objectSet":
        _members = cmds.sets(_set, q=True)
        for _member in _members:
            res = get_set_members(_member)
            _sets.extend(res)
    else:
        _sets.append(_set)
    return _sets

def main(scene_path):
    
    types = []
    texts = []
    error_nodes = []

    set_name = "CtrlSet"

    """
    「_ctrl」のサフィックスがある、ナーブスカーブを持ったトランスフォームを抽出
    """
    _ctrl_nodes = [x for x in cmds.ls("*_ctrl",
            type="transform") if cmds.listRelatives(x, p=False, type="nurbsCurve")]
    
    if not _ctrl_nodes:
        types.append("{}".format(set_name))
        texts.append(u"[ _ctrl ] で終わるノードがない")
        error_nodes.append("")

    _set = cmds.ls(set_name, type="objectSet")
    
    if not _set:
        types.append("{}".format(set_name))
        texts.append(u"[ {} ] sets がない".format(set_name))
        error_nodes.append("")
    else:
        """
        「CtrlSet」内の全メンバーを抽出
        """
        _all_set_members_func = get_set_members(_set)
        
        for _node in _ctrl_nodes:
            """
            「_ctrl」のサフィックスと「CtrlSet」を比較し「CtrlSet」に入っていないものを抽出
            """
            if not _node in _all_set_members_func:
                types.append("{}".format(set_name))
                texts.append(u"[ {} ] にない".format(set_name))
                error_nodes.append(_node)
            else:
                """
                コントローラにコンストレイントがあればそれを抽出
                """
                _constraint = cmds.listRelatives(_node,
                                            type="constraint",
                                            fullPath=True)
                if _constraint:
                    types.append("{}".format("constraint"))
                    texts.append(u"constraint がある")
                    error_nodes.append(_node)

                """
                「_ctrl」のサフィックスではないものを抽出
                これはいらないかも
                """
                if not _node.endswith("_ctrl"):
                    types.append("{}".format("name"))
                    texts.append(u"[ _ctrl ] でない")
                    error_nodes.append(_node)
                    
                else:
                    """
                    各コントローラの移動値、回転値、スケール値を確認
                    リセットされている必要がある
                    """
                    if ([abs(round(x)) for x in cmds.getAttr("{}.t".format(_node))[0]]
                                                                    != [0.0, 0.0, 0.0]):
                        types.append("{}".format("transform"))
                        texts.append(u"[ 移動値 ]　あり")
                        error_nodes.append(_node)

                    if ([abs(round(x)) for x in cmds.getAttr("{}.r".format(_node))[0]]
                                                                    != [0.0, 0.0, 0.0]):
                        types.append("{}".format("transform"))
                        texts.append(u"[ 回転値 ]　あり")
                        error_nodes.append(_node)

                    if ([abs(round(x)) for x in cmds.getAttr("{}.s".format(_node))[0]]
                                                                    != [1.0, 1.0, 1.0]):
                        types.append("{}".format("transform"))
                        texts.append(u"[ スケール ]　あり")
                        error_nodes.append(_node)
    # print(" ----------------------check_set_ctrl_set")
    return zip(texts, types, error_nodes)