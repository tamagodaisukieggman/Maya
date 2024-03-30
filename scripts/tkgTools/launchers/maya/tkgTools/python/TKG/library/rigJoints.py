# -*- coding: utf-8 -*-
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

def create_limb_joints(nodes=None,
                       blend_prefix=None,
                       blend_suffix=None,
                       blend_replace=None,
                       first_segments_num=8,
                       second_segments_num=8,
                       fk_prefix=None,
                       fk_suffix=None,
                       fk_replace=None,
                       ik_prefix=None,
                       ik_suffix=None,
                       ik_replace=None):
    if not nodes:
        nodes = cmds.ls(os=True, fl=True) or []

    # blend joints
    dup = tkgNodes.Duplicate(nodes, blend_prefix, blend_suffix, blend_replace)
    blend_joints = dup.duplicate()

    blend_first_segments = tkgNodes.segment_duplicates(base=blend_joints[0],
                                tip=blend_joints[1],
                                i=first_segments_num,
                                base_include=True,
                                tip_include=True,
                                children=True)

    blend_second_segments = tkgNodes.segment_duplicates(base=blend_joints[1],
                                tip=blend_joints[2],
                                i=second_segments_num,
                                base_include=True,
                                tip_include=True,
                                children=True)

    # fk joints
    fk_joints = create_fk_joints(nodes, fk_prefix, fk_suffix, fk_replace)

    # ik joints
    ik_joints = create_ik_joints(nodes, ik_prefix, ik_suffix, ik_replace)

    return [blend_joints, blend_first_segments, blend_second_segments], fk_joints, ik_joints

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