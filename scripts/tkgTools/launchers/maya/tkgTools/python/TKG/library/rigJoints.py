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

def create_bendy_joints(nodes=None, bendy_num=8):
    if not nodes:
        nodes = cmds.ls(os=True, fl=True) or []

    # bendy joints
    dup = tkgNodes.Duplicate(nodes, *tkgRegulation.node_type_rename(node=None, type='bendy'))
    bendy_joints = dup.duplicate()

    bendy_segments = tkgNodes.segment_duplicates(base=bendy_joints[0],
                                tip=bendy_joints[1],
                                i=bendy_num,
                                base_include=True,
                                tip_include=True,
                                children=True)

    return [bendy_joints, bendy_segments]

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