﻿# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import traceback

import maya.cmds as cmds

import TKG.common as tkgCommon
import TKG.nodes as tkgNodes
import TKG.regulation as tkgRegulation
reload(tkgCommon)
reload(tkgNodes)
reload(tkgRegulation)

def create_fk_joints(nodes=None):
    dup = tkgNodes.Duplicate(nodes, *tkgRegulation.node_type_rename(node=None, type='fk'))
    return dup.duplicate()

def create_ik_joints(nodes=None):
    dup = tkgNodes.Duplicate(nodes, *tkgRegulation.node_type_rename(node=None, type='ik'))
    return dup.duplicate()

def create_blend_joints(nodes=None):
    dup = tkgNodes.Duplicate(nodes, *tkgRegulation.node_type_rename(node=None, type='blend'))
    return dup.duplicate()

def create_start_end_joints(nodes=None):
    start_name = tkgRegulation.node_type_rename(node=nodes[0], type='start')
    end_name = tkgRegulation.node_type_rename(node=nodes[-1], type='end')
    start_dup = cmds.duplicate(nodes[0], n=start_name, po=True)[0]
    end_dup = cmds.duplicate(nodes[-1], n=end_name, po=True)[0]
    start_dup_pa = cmds.listRelatives(start_dup, p=True) or None
    if start_dup_pa:
        cmds.parent(start_dup, w=True)
    end_dup_pa = cmds.listRelatives(end_dup, p=True) or None
    if end_dup_pa:
        cmds.parent(end_dup, w=True)

    return start_dup, end_dup

def create_sc_ik_joints(nodes=None, aim_axis='x', up_axis='y', freeze=None):
    start = nodes[0]
    middle = nodes[1]
    end = nodes[2]

    pv_start = cmds.duplicate(start, n=tkgRegulation.node_type_rename(node=start, type='sc_ik_dummy'), po=True)[0]
    pv_end = cmds.duplicate(end, n=tkgRegulation.node_type_rename(node=end, type='sc_ik_dummy'), po=True)[0]

    aim_axis_vector = tkgRegulation.axis_vector(aim_axis)
    up_axis_vector = tkgRegulation.axis_vector(up_axis)

    cmds.delete(cmds.aimConstraint(end,
                    pv_start,
                    aimVector=aim_axis_vector,
                    upVector=up_axis_vector,
                    worldUpType='object',
                    worldUpObject=middle,
                    offset=[0,0,0],
                    w=True))

    if freeze:
        cmds.makeIdentity(pv_start,
                        apply=True,
                        t=False,
                        r=True,
                        s=False,
                        n=False,
                        pn=True)

    cmds.parent(pv_end, pv_start)

    return [pv_start, pv_end]

def create_bendy_limb_joints(nodes=None, bendy_num=8):
    if not nodes:
        nodes = cmds.ls(os=True, fl=True) or []

    # bendy joints
    bendy_limb_joints = []
    bendy_segments_list = []
    for i, node in enumerate(nodes):
        bendy = tkgRegulation.node_type_rename(node, 'bendy_limb')
        if not cmds.objExists(bendy):
            cmds.duplicate(node, n=bendy, po=True)

        if i != 0:
            bendy_segments = tkgNodes.segment_duplicates(base=bendy_limb_joints[i-1],
                                        tip=bendy,
                                        i=bendy_num,
                                        base_include=True,
                                        tip_include=True,
                                        children=True)

            cmds.parent(bendy, bendy_limb_joints[i-1])

            bendy_segments_list.append(bendy_segments)

        bendy_limb_joints.append(bendy)

    return bendy_limb_joints, bendy_segments_list

def create_ribbon_joints(nodes=None, ribbon_num=8, base_include=True, tip_include=True):
    if not nodes:
        nodes = cmds.ls(os=True, fl=True) or []

    # ribbon joints
    ribbon_joints = []
    ribbon_segments_list = []
    for i, node in enumerate(nodes):
        ribbon = tkgRegulation.node_type_rename(node, 'ribbon')
        if not cmds.objExists(ribbon):
            cmds.duplicate(node, n=ribbon, po=True)

        if i != 0:
            ribbon_segments = tkgNodes.segment_duplicates(base=ribbon_joints[i-1],
                                        tip=ribbon,
                                        i=ribbon_num,
                                        base_include=base_include,
                                        tip_include=tip_include,
                                        children=True)

            cmds.parent(ribbon, ribbon_joints[i-1])

            ribbon_segments_list.append(ribbon_segments)

        ribbon_joints.append(ribbon)

    return ribbon_joints, ribbon_segments_list

def create_end_joint(node=None):
    parent = cmds.listRelatives(node, p=True) or None
    if not parent:
        return
    else:
        end_parent = parent[0]
    mid_point = tkgCommon.mid_point(node, end_parent, percentage=-0.1)
    end_jnt = tkgRegulation.node_type_rename(node, 'end')
    cmds.createNode('joint', n=end_jnt, ss=True)
    cmds.xform(end_jnt, t=mid_point, ws=True, a=True)
    cmds.parent(end_jnt, node)
    return end_jnt