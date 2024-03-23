# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds
import maya.mel as mel

import TKG.nodes as tkgNodes
import TKG.regulation as tkgRegulation
import TKG.library.rigJoints as tkgRigJoints
reload(tkgNodes)
reload(tkgRegulation)
reload(tkgRigJoints)

def ik_settings(solver=None):
    solvers = {
        0: 'ikSCsolver',
        1: 'ikRPsolver',
        2: 'ikSplineSolver',
        3: 'ikSpringSolver'
    }

    settings = {
        'name':None,
        'startJoint':None,
        'endEffector':None,
        'sticky':'sticky',
        'solver':solvers[solver]
    }

    return settings

def create_RP_ikHandle(start=None, end=None):
    settings = ik_settings(solver=1)
    settings['name'] = tkgRegulation.node_type_rename(end, 'ikHandle')
    settings['startJoint'] = start
    settings['endEffector'] = end
    return cmds.ikHandle(**settings)[0]

def create_spline_ikHandle(start=None, end=None):
    settings = ik_settings(solver=2)
    settings['name'] = tkgRegulation.node_type_rename(end, 'ikHandle')
    settings['startJoint'] = start
    ik_spline_end_jnt = tkgRigJoints.create_end_joint(end)
    settings['endEffector'] = ik_spline_end_jnt

    ik_spline_joints = tkgNodes.get_ancestors(start=start,
                                              end=ik_spline_end_jnt,
                                              parents=[])

    ik_spline_crv = tkgNodes.create_curve_on_nodes(nodes=ik_spline_joints,
                                   name=tkgRegulation.node_type_rename(end, 'ikSplineCrv'))

    settings['curve'] = ik_spline_crv
    settings['freezeJoints'] = True
    settings['createCurve'] = False
    # settings['snapHandleFlagToggle'] = True
    settings['scv'] = False
    settings['rtm'] = True

    return cmds.ikHandle(**settings)[0]