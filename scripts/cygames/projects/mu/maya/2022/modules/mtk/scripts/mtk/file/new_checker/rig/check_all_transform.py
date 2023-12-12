# -*- coding: utf-8 -*-

from maya import cmds

def main(scene_path):
    
    types = []
    texts = []
    error_nodes = []
    
    root_node = [x for x in cmds.ls(assemblies=True)if "root" == x]
    if not root_node:
        return zip(texts, types, error_nodes)
    root_node = root_node[0]
    
    _type = "transform"
    text = u"キーフレームが存在"

    _all_transform = [x for x in cmds.listRelatives(root_node,
                                    allDescendents=True,
                                    fullPath=True)if cmds.nodeType(x)=="transform"]
                                            

    _all_transform.append(root_node)

    for _transform in _all_transform:

        if cmds.keyframe(_transform, q=True):
            texts.append(text)
            types.append("keyframe")
            error_nodes.append(_transform)
    # print(" ----------------------check_all_transform")
    return zip(texts, types, error_nodes)
