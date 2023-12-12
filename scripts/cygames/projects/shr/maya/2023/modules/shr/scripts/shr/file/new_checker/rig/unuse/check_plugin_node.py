# -*- coding: utf-8 -*-

from maya import cmds

PLUGIN_NODES = ["ngSkinTools*"]
NODE_TYPES = [
        "ngst2SkinLayerData",
        "ngst2MeshDisplay",
        ]

def main(scene_path):
    types = []
    texts = []
    error_nodes = []

    # plugin_nodes = cmds.ls(PLUGIN_NODES)
    plugin_nodes = cmds.ls(type=NODE_TYPES)
    if plugin_nodes:
        for node in plugin_nodes:
            types.append("{}".format("plugin"))
            texts.append(u"[ {} ] がある".format(node))
            error_nodes.append(node)

    return zip(texts, types, error_nodes)