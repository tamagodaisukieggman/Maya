# -*- coding: utf-8 -*-
from maya import cmds

NEED_LAYERS = [
    "model_objLay",
    "bind_joints_objLay",
    "rig_objLay"
]

def main(scene_path):
    types = []
    texts = []
    error_nodes = []

    layers = [x for x in cmds.ls(type="displayLayer") if not x.startswith("defaultLayer")]
    if layers:
        for layer in layers:
            if layer not in NEED_LAYERS:
                types.append("{}".format("Display Layer"))
                texts.append(u"[ {} ] がある".format(layer))
                error_nodes.append(layer)

    default_layer = cmds.ls("defaultLayer*", type="displayLayer")
    
    if not default_layer:
        types.append("{}".format("No Default"))
        texts.append(u"[ {} ] がない".format("defaultLayer"))
        error_nodes.append("")
    return zip(texts, types, error_nodes)