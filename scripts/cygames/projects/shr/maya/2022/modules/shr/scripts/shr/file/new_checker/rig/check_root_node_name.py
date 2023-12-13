# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from maya import cmds

ROOT_NODE_NAME = "root"
CAMERAS = ['persp', 'top', 'front', 'side']
RIG_NAME = "rig"
MODEL_NAME = "model"

def main(scene_path):
    
    types = []
    texts = []
    error_nodes = []

    # nodes = [x for x in cmds.ls(assemblies=True) if x not in CAMERAS]
    nodes = [x for x in cmds.ls(assemblies=True)
                if "camera" != cmds.nodeType(cmds.listRelatives(x, s=True))]
    root_node = None
    rig = None
    model = None

    if not nodes:
        types.append("root")
        texts.append(u"[ root ] がない")
        error_nodes.append("")
    else:
        u"""
        シーンルートのトランスフォーム全てを調査
        「root」以外のものは存在しないはず
        カメラは除く

        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ※今後無視するプレフィックスが追加される可能性あり
        """
        for node in nodes:
            if ROOT_NODE_NAME in node:
                root_node = node
                if ROOT_NODE_NAME != node:
                    types.append("group name")
                    texts.append(u"[ {} ] の名前".format(node))
                    error_nodes.append(node)
            else:
                types.append("unnecessary")
                texts.append(u"不要なノード")
                error_nodes.append(node)
    
    if not root_node:
        types.append("root")
        texts.append(u"[ root ] がない")
        error_nodes.append("")
    else:
        _clds = cmds.listRelatives(root_node,
                                    c=True,
                                    fullPath=True,
                                    type="transform")
        for _cld in _clds:
            _cld_short_name = _cld.split("|")[-1]

            _clds_second = cmds.listRelatives(_cld,
                                        c=True,
                                        fullPath=True,
                                        type="transform")

            
            if RIG_NAME in _cld_short_name:
                u"""
                rig グループ検索
                """
                rig = _cld
                if RIG_NAME != _cld_short_name:
                    types.append("group name")
                    texts.append(u"[ {} ] の名前".format(_cld_short_name))
                    error_nodes.append(_cld)

            for _c in _clds_second:
                _second_short_name = _c.split("|")[-1]
                print(_second_short_name, " --- _second_short_name")
                if MODEL_NAME in _second_short_name:
                    u"""
                    model グループ検索
                    """
                    model = _c
                    if MODEL_NAME != _second_short_name:
                        types.append("group name")
                        texts.append(u"[ {} ] の名前".format(_second_short_name))
                        error_nodes.append(_c)
            # else:
            #     u"""
            #     第一階層の「rig」「model」以外のノードがあれば
            #     それは不要なノード
            #     """
            #     types.append("unnecessary")
            #     texts.append(u"不要なノード")
            #     error_nodes.append(_cld)

        if not rig:
            types.append("group")
            texts.append(u"[ {} ] がない".format(RIG_NAME))
            error_nodes.append("")
        if not model:
            types.append("group")
            texts.append(u"[ {} ] がない".format(MODEL_NAME))
            error_nodes.append("")
    # print(" ----------------------check_root_node_name")
    return zip(texts, types, error_nodes)