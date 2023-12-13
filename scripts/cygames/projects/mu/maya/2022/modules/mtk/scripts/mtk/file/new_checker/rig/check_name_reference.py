# -*- coding: utf-8 -*-

from maya import cmds

def main(scene_path):
    
    types = []
    texts = []
    error_nodes = []

    _type = "reference"

    _reference_nodes = [x for x in cmds.ls(type='reference',
                                    long=True) if "sharedReferenceNode" != x]
    if not _reference_nodes:
        texts.append(u"リファレンスがない")
        types.append(_type)
        error_nodes.append("")
    else:
        for _reference_node in _reference_nodes:
            _name_split = cmds.referenceQuery(_reference_node, namespace=True).split(":")
            if [x for x in _name_split if x]:
                texts.append(u"namespance が正しくない")
                types.append(_type)
                error_nodes.append(_reference_node)
    # print(" ----------------------check_name_reference")
    return zip(texts, types, error_nodes)