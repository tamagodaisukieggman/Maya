# -*- coding: utf-8 -*-

from maya import cmds

def main(scene_path):
    
    types = []
    texts = []
    error_nodes = []
    
    set_name = "AnimJtSet"

    _set = cmds.ls(set_name, type="objectSet")
    _all_joint_nodes = cmds.ls(type="joint")

    if not _set:
        types.append(set_name)
        texts.append(u"[ {} ] sets がない".format(set_name))
        error_nodes.append("")

    else:
        _set_member = cmds.sets(_set, q=True)
        if not _set_member:
            types.append(set_name)
            texts.append(u"[ {} ] が空".format(set_name))
            error_nodes.append("")
    
        else:
            if not _all_joint_nodes:
                types.append("joint")
                texts.append(u"[ {} ] がない".format("joint"))
                error_nodes.append("")

            else:
                _reference_nodes = [x for x in cmds.ls(type='reference',
                                            long=True) if "sharedReferenceNode" != x]

                if _reference_nodes:
                    
                    check_joints = list(set(_all_joint_nodes) & 
                                set(cmds.referenceQuery(_reference_nodes, nodes=True)))
                    for jnt in check_joints:
                        if not jnt in cmds.sets(set_name, q=True, nodesOnly=True):
                            types.append(set_name)
                            texts.append(u"[ {} ] にない".format(set_name))
                            error_nodes.append(jnt)
                else:
                    types.append("reference")
                    texts.append(u"[ reference ] がない")
                    error_nodes.append("")
    # print(" ----------------------check_anim_jt_set")
    return zip(texts, types, error_nodes)