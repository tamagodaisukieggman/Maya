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
    dup = tkgNodes.Duplicate(nodes, fk_prefix, fk_suffix, fk_replace)
    fk_joints = dup.duplicate()

    # ik joints
    dup = tkgNodes.Duplicate(nodes, ik_prefix, ik_suffix, ik_replace)
    ik_joints = dup.duplicate()

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