# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om2

from collections import OrderedDict
from imp import reload

def match_pose(node, position=None, rotation=None, scale=None):
    if isinstance(position, list) or isinstance(position, tuple):
        if len(position) == 3:
            cmds.setAttr(node + ".t", *position)
        else:
            cmds.error("Please provide X, Y, and Z translate coordinates.")
    elif not position:
        pass
    else:
        if cmds.objExists(position):
            src = cmds.xform(position, q=True, ws=True, t=True)
            cmds.xform(node, ws=True, t=src)
        else:
            cmds.error("Input for position not valid. Please give " +
                       "coordinates or an existing object.")

    if isinstance(rotation, list) or isinstance(rotation, tuple):
        if len(rotation) == 3:
            cmds.setAttr(node + ".r", *rotation)
        else:
            cmds.error("")
    elif not rotation:
        pass
    else:
        if cmds.objExists(rotation):
            src = cmds.xform(rotation, q=True, ws=True, ro=True)
            cmds.xform(node, ws=True, ro=src)
        else:
            cmds.error("")

    if isinstance(scale, list) or isinstance(scale, tuple):
        if len(scale) == 3:
            cmds.setAttr(node + ".scale", *scale)
        else:
            cmds.error("")
    elif not scale:
        pass
    else:
        if cmds.objExists(scale):
            src = cmds.xform(scale, q=True, ws=True, s=True)
            cmds.xform(node, ws=True, s=src)
        else:
            cmds.error("")

def read_pose(nodes):
    if not isinstance(nodes, list):
        nodes = [nodes]
    pose_dict = OrderedDict()

    for node in nodes:
        pose_dict[node] = cmds.xform(node,
                                     q=True,
                                     ws=True,
                                     m=True)

    return pose_dict

def set_pose(node, matrix):
    cmds.xform(node, ws=True, m=matrix)

def find_position_on_curve(curve, u_value):
    pci = cmds.createNode('pointOnCurveInfo', name='tmp_pci')
    cmds.connectAttr(curve + 'Shape.worldSpace[0]', pci + '.inputCurve')
    cmds.setAttr(pci + '.turnOnPercentage', 1)
    cmds.setAttr(pci + '.parameter', u_value)
    pos = cmds.getAttr(pci + '.position')[0]
    cmds.delete(pci)
    return pos

def move_pivot(ctrl=None, edge_axis='-x'):
    if edge_axis:
        bbx = cmds.xform(ctrl, q=True, bb=True)

        pivot_axis = {
            'x':bbx[3],
            'y':bbx[4],
            'z':bbx[5],
            '-x':bbx[0],
            '-y':bbx[1],
            '-z':bbx[2],
        }

        pivot_value = {
            'x':[pivot_axis[edge_axis], 0, 0],
            'y':[0, pivot_axis[edge_axis], 0],
            'z':[0, 0, pivot_axis[edge_axis]],
            '-x':[pivot_axis[edge_axis], 0, 0],
            '-y':[0, pivot_axis[edge_axis], 0],
            '-z':[0, 0, pivot_axis[edge_axis]],
        }

        cmds.move(*pivot_value[edge_axis], ctrl+'.scalePivot', ctrl+'.rotatePivot', r=True)
        rev_xform = [v*-1 for v in pivot_value[edge_axis]]
        cmds.xform(ctrl, t=rev_xform, ws=True, a=True)
        cmds.makeIdentity(ctrl, n=False, s=True, r=True, t=True, apply=True, pn=True)

def m_obj(obj):
    selection_list = om2.MSelectionList()
    selection_list.add(obj)
    return selection_list.getDependNode(0)

def m_dag(obj):
    selection_list = om2.MSelectionList()
    selection_list.add(obj)
    return selection_list.getDagPath(0)

def m_dependency(obj):
    m_dependency_node = om2.MFnDependencyNode(m_obj(obj))
    return m_dependency_node

def fn_transform(obj):
    dag = m_dag(obj)
    fn_trans = om2.MFnTransform(dag)
    return fn_trans

def fn_transform_pos(obj):
    fn_trans = fn_transform(obj)
    return fn_trans.translation(om2.MSpace.kWorld)

def get_distance(objA, objB):
    posA = fn_transform_pos(objA)
    posB = fn_transform_pos(objB)
    return om2.MPoint(posA).distanceTo(om2.MPoint(posB))

def fn_addNumAttr(obj=None, longName=None, shortName=None, minValue=None, maxValue=None, defaultValue=None, numericData=om2.MFnNumericData.kFloat):
    m_object = m_obj(obj)
    m_dependency_node = om2.MFnDependencyNode(m_object)

    num_att_fn = om2.MFnNumericAttribute(m_object)
    attr = num_att_fn.create(longName, shortName, numericData, defaultValue) # float
    num_att_fn.keyable=True

    if maxValue != None:
        num_att_fn.setMax(maxValue)
    if minValue != None:
        num_att_fn.setMin(minValue)

    m_dependency_node.addAttribute(attr)
