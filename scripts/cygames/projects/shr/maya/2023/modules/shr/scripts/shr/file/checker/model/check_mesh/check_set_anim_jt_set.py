# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds

def _check_set_anim_jt_set():
    errors = []

    set_name = "AnimJtSet"
    _set = cmds.ls(set_name, type="objectSet")
    _all_joint_nodes = cmds.ls(type="joint")

    if not _set:
        return errors
    
    if not _all_joint_nodes:
        return errors

    _set_menber = cmds.sets(_set, q=True)

    if not _set_menber:
        return _set
    
    _reference_nodes = [x for x in cmds.ls(type='reference',long=True)if "sharedReferenceNode"!=x]

    check_joints = list(set(_all_joint_nodes)&set(cmds.referenceQuery(_reference_nodes,nodes=True)))
    #for _reference_node in _reference_nodes:
    #    check_joints.extend([x for x in cmds.referenceQuery(_reference_node, nodes=True) if cmds.nodeType(cmds.ls(x)[0]) == "joint"])

    # print len(check_joints)
    # print check_joints

    for jnt in check_joints:
        if not jnt in cmds.sets(set_name, q=True, nodesOnly=True):
            errors.append(jnt)
        # jnt_short_name = jnt.split("|")[-1]
        # _current_set = cmds.listSets(object=jnt)
        # if _current_set and not _current_set[0] == set_name:
        #     errors.append(jnt)
    return errors


def __check_set_anim_jt_set():
    errors = []
    check_joints = []

    set_name = "AnimJtSet"
    _set = cmds.ls(set_name, type="objectSet")
    _all_joint_nodes = cmds.ls(type="joint", long=True)

    if not _set:
        return errors
    
    if not _all_joint_nodes:
        return errors
        
    _set_menber = cmds.sets(_set, q=True)

    _reference_joint_nodes = [x for x in _all_joint_nodes if cmds.referenceQuery(x, isNodeReferenced=True)]

    if not _reference_joint_nodes:
        return errors

    # _reference_nodes = [x for x in cmds.ls(type='reference',
    #                         long=True) if "sharedReferenceNode" != x]

    # if _reference_nodes:
    #     for _reference_node in _reference_nodes:
    #         check_joints.extend([x for x in cmds.referenceQuery(_reference_node,
    #                                     nodes=True) if cmds.nodeType(x) == "joint"])
    print(_set_menber)

    for jnt in _reference_joint_nodes:
        jnt_short_name = jnt.split("|")[-1]
        if not jnt_short_name in _set_menber:
            errors.append(jnt)
        print(jnt_short_name)
        _current_set = cmds.listSets(object=jnt)
        print(_current_set[0],"---")
        print(jnt in _set_menber)
        print("++++")
        # if _current_set and not _current_set[0] == set_name:
        #     errors.append(jnt)


    return errors