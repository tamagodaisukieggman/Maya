# -*- coding: utf-8 -*-
from imp import reload
import math
import re

import maya.cmds as cmds
import maya.api.OpenMaya as om2

import TKG.common as tkgCommon
import TKG.regulation as tkgRegulation
reload(tkgCommon)
reload(tkgRegulation)

# rename
def rename(obj=None, prefix=None, suffix=None, replace=None):
    """
    obj=None, prefix=None, suffix=None, replace=None
    """
    # replace
    replace_name = obj
    if replace:
        replace_name = obj.replace(*replace)

    # prefix
    if not prefix:
        prefix = ''
    prefix_name = re.sub('^', prefix, replace_name)

    # suffix
    if not suffix:
        suffix = ''
    renamed = re.sub('$', suffix, prefix_name)

    return renamed

# virtual rename
def virtual_reames(names=None, p='', s='', r=['', '']):
    """
    仮想のリネームを取得
    """
    return [rename(n, p, s, r) for n in names]

# duplicate
class Duplicate:
    """
    dup = Duplicate(nodes, '', '', ['BIND_', 'IK_'])
    dups = dup.duplicate()
    """
    def __init__(self, nodes=None, prefix=None, suffix=None, replace=None, hierarchy=None):
        if nodes:
            self.nodes = nodes
        else:
            self.nodes = cmds.ls(os=True, fl=True) or []
        self.prefix = prefix
        self.suffix = suffix
        self.replace = replace
        self.hierarchy = hierarchy
        self.virtuals = None

        self.virtual_reames()

    def virtual_reames(self):
        if self.hierarchy:
            self.nodes = cmds.ls(self.nodes, dag=True)

        self.virtuals = virtual_reames(self.nodes,
                              self.prefix,
                              self.suffix,
                              self.replace)

    def duplicate(self):
        if self.hierarchy:
            dups = cmds.duplicate(self.nodes, rc=True)
        else:
            dups = cmds.duplicate(self.nodes, rc=True, po=True)

        return [cmds.rename(d, rslt) for d, rslt in zip(dups, self.virtuals)]


def segment_duplicates(base=None, tip=None, i=2, base_include=None, tip_include=None, children=None):
    """
    baseとtipの間にジョイントを作成する
    例：BIND_ForeArm_L > BIND_ForeArm_00_L
    """
    segments = []
    mps = tkgCommon.step_positions(nodes=[base, tip],
                                   i=i,
                                   base_include=base_include,
                                   tip_include=tip_include)
    for j in range(i):
        renamed, bkwd_under = tkgRegulation.segment_padding_rename(base, j, 2, 0)

        dup = Duplicate([base], '', '', [bkwd_under, renamed], False)
        dups = dup.duplicate()
        cmds.xform(dups[0], t=mps[j], ws=True, a=True)
        if children:
            cmds.parent(dups[0], base)
        segments.append(dups[0])

    return segments

def get_shapes(node):
    shape_list = cmds.listRelatives(node, s=True, ni=True)

    if not shape_list:
        shape_list = cmds.ls(node, s=True)

    if shape_list:
        return shape_list
    else:
        return None

def fix_shapes(node):
    curve_shapes = get_shapes(node)
    for i, shp in enumerate(curve_shapes):
        cmds.setAttr('{}.lineWidth'.format(shp), 2)

        if i == 0:
            cmds.rename(shp, node + "Shape")
        else:
            cmds.rename(shp, "{}Shape_{}".format(node, i))

def create_curve_on_nodes(nodes=None, name=None, d=3):
    pts = [cmds.xform(j,q=True,ws=True,t=True) for j in nodes]
    crv = cmds.curve(ep=pts, d=d, n=name)
    fix_shapes(crv)
    return crv

def get_ancestors(start=None, end=None, parents=[]):
    start_pa = cmds.listRelatives(start, p=True) or None
    end_pa = cmds.listRelatives(end, p=True) or None
    if not end in parents:
        parents.append(end)
    if end_pa:
        if start_pa[0] != end_pa[0]:
            parents.append(end_pa[0])
            parents = get_ancestors(start=start, end=end_pa[0], parents=parents)

    return parents

def get_transform(node):
    if node:
        if cmds.nodeType(node) == 'transform':
            transform = node
        else:
            transform = cmds.listRelatives(node, type='transform', parent=True)[0]

        return transform

    else:
        return None

def set_rgb(node, color):
    rgb = ("R","G","B")
    for channel, color in zip(rgb, color):
        cmds.setAttr(node + ".overrideColor{}".format(channel), color)

def set_rgb_color(ctrl=None, color=[1,1,1]):
    # shape = cmds.listRelatives(ctrl, s=True, f=True)[0]
    shapes = cmds.listRelatives(ctrl, s=True, f=True)
    for shape in shapes:
        cmds.setAttr(shape + ".overrideEnabled",1)
        cmds.setAttr(shape + ".overrideRGBColors",1)
        set_rgb(shape, color)

def set_obj_color(obj=None, color=[0.5, 0.5, 0.5], outliner=None):
    cmds.setAttr(obj+'.useObjectColor', 2)
    cmds.setAttr(obj+'.wireColorRGB', *color)

    if outliner:
        cmds.setAttr(obj+'.useOutlinerColor', 1)
        cmds.setAttr(obj+'.outlinerColor', *color)

def merge_curves(sel=None):
    if not sel:
        sel = cmds.ls(os=True)
    # cmds.select(sel[0], r=True)
    # cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
    if not sel:
        return
    shape = cmds.listRelatives(sel[0], s=True, f=True) or list()
    # cmds.select(sel[0], r=True)
    # mel.eval('channelBoxCommand -freezeAll;')
    if shape:
        for sh in shape:
            cmds.parent(sh, sel[1], s=True, r=True)

    cmds.delete(sel[0])

    cmds.select(sel[1], r=True)

def offset(node=None, type=None):
    if not node:
        node = cmds.ls(os=True, fl=True)[0] or []
    name = tkgRegulation.offset_type_rename(node, type)
    off = cmds.createNode('transform', n=name, ss=True)
    cmds.matchTransform(off, node)

    parent = cmds.listRelatives(node, p=True, f=True) or None
    if parent:
        cmds.parent(off, parent[0])

    cmds.parent(node, off)

    return off

def offsets(node=None, types=None):
    root_off = None
    for i, ty in enumerate(types):
        off = offset(node, ty)
        if i == 0:
            root_off = off
    return root_off

def pole_vec(start=None, mid=None, end=None, move=None, obj=None):
    start = cmds.xform(start, q=True, t=True, ws=True)
    mid = cmds.xform(mid, q=True, t=True, ws=True)
    end = cmds.xform(end, q=True, t=True, ws=True)

    startV = om2.MVector(start[0], start[1], start[2])
    midV = om2.MVector(mid[0], mid[1], mid[2])
    endV = om2.MVector(end[0], end[1], end[2])
    startEnd = endV - startV
    startMid = midV - startV
    dotP = startMid * startEnd
    proj = float(dotP) / float(startEnd.length())
    startEndN = startEnd.normal()
    projV = startEndN * proj
    arrowV = startMid - projV
    arrowV *= 0.5
    finalV = arrowV + midV
    cross1 = startEnd ^ startMid
    cross1.normalize()
    cross2 = cross1 ^ arrowV
    cross2.normalize()
    arrowV.normalize()
    matrixV = [arrowV.x, arrowV.y, arrowV.z, 0,
               cross1.x, cross1.y, cross1.z, 0,
               cross2.x, cross2.y, cross2.z, 0,
               0, 0, 0, 1]
    matrixM = om2.MMatrix(matrixV)
    matrixFn = om2.MTransformationMatrix(matrixM)
    # rot = matrixFn.rotation().asEulerRotation()
    rot = matrixFn.rotation()

    pvLoc = cmds.spaceLocator(n='poleVecPosLoc')
    cmds.xform(pvLoc[0], ws=1, t=(finalV.x, finalV.y, finalV.z))
    # cmds.xform(pvLoc[0], ws=1, rotation=(rot.x / om2.MMath.kRadiansToDegrees,
    #                                       rot.y / om2.MMath.kRadiansToDegrees,
    #                                       rot.z / om2.MMath.kRadiansToDegrees))

    cmds.xform(pvLoc[0], ws=1, rotation=(rot.x * 180.0 / math.pi,
                                        rot.y * 180.0 / math.pi,
                                        rot.z * 180.0 / math.pi))

    cmds.select(pvLoc[0])
    if move is not None:
        cmds.move(move, 0, 0, r=1, os=1, wd=1)

    pvwt = None
    if obj:
        cmds.matchTransform(obj, pvLoc[0])
    else:
        pvwt = cmds.xform(pvLoc[0], q=True, t=True, ws=True)

    cmds.delete(pvLoc[0])
    return pvwt

def m_obj(obj):
    selection_list = om2.MSelectionList()
    selection_list.add(obj)
    return selection_list.getDependNode(0)

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

def get_up_stream(node=None):
    pa = cmds.listRelatives(node, p=True, f=True) or []
    parents = None
    if pa:
        parents = pa[0].split('|')[::-1]
        parents.remove('')
    else:
        parents = []
    return parents

def get_world_rot(node=None):
    return cmds.xform(node, q=True, ro=True, ws=True)

def get_world_pos(node=None):
    return cmds.xform(node, q=True, t=True, ws=True)

def get_world_pos_rot(node=None):
    node_tr = []
    for t in get_world_pos(node):
        node_tr.append(t)
    for ro in get_world_rot(node):
        node_tr.append(ro)
    return node_tr

def matrix_constraint(src=None, dst=None):
    if not src or not dst:
        sel = cmds.ls(os=True)
        src = sel[0]
        dst = sel[1]

    src_tr = get_world_pos_rot(src)
    dst_tr = get_world_pos_rot(dst)

    round_src_tr = [tkgCommon.round_value(v, 3) for v in src_tr]
    round_dst_tr = [tkgCommon.round_value(v, 3) for v in dst_tr]

    not_same = None
    for s, d in zip(round_src_tr, round_dst_tr):
        if s != d:
            not_same = True
            break

    src_stream = get_up_stream(node=src)

    if not_same:
        dst_dup = cmds.duplicate(dst, n=dst+'_MAT_DUP', po=True)[0]
        cmds.parent(dst_dup, src)

        src_stream = get_up_stream(node=dst_dup)
        src = dst_dup

    dst_stream = get_up_stream(node=dst)[::-1]

    if len(src_stream) <= len(dst_stream):
        same_nodes = [n for n in dst_stream if n in src_stream]
    elif len(src_stream) >= len(dst_stream):
        same_nodes = [n for n in src_stream if n in dst_stream]
    [src_stream.remove(n) for n in same_nodes]
    [dst_stream.remove(n) for n in same_nodes]

    pos_mmx = cmds.createNode('multMatrix', ss=True)
    rot_mmx = cmds.createNode('multMatrix', ss=True)
    scl_mmx = cmds.createNode('multMatrix', ss=True)

    pos_dcmx = cmds.createNode('decomposeMatrix', ss=True)
    rot_dcmx = cmds.createNode('decomposeMatrix', ss=True)
    scl_dcmx = cmds.createNode('decomposeMatrix', ss=True)

    cmds.connectAttr(src+'.matrix', pos_mmx+'.matrixIn[0]', f=True)
    cmds.connectAttr(src+'.matrix', rot_mmx+'.matrixIn[0]', f=True)
    cmds.connectAttr(src+'.matrix', scl_mmx+'.matrixIn[0]', f=True)

    src_end_idx = 0
    for i, n in enumerate(src_stream):
        cmds.connectAttr(n+'.matrix', pos_mmx+'.matrixIn[{}]'.format(i+1), f=True)
        cmds.connectAttr(n+'.matrix', rot_mmx+'.matrixIn[{}]'.format(i+1), f=True)
        cmds.connectAttr(n+'.matrix', scl_mmx+'.matrixIn[{}]'.format(i+1), f=True)
        src_end_idx = i+1

    dst_end_idx = 0
    if not dst_stream:
        dst_end_idx = src_end_idx+1

    for j, n in enumerate(dst_stream):
        cmds.connectAttr(n+'.inverseMatrix', pos_mmx+'.matrixIn[{}]'.format(src_end_idx+j+1), f=True)
        cmds.connectAttr(n+'.inverseMatrix', rot_mmx+'.matrixIn[{}]'.format(src_end_idx+j+1), f=True)
        cmds.connectAttr(n+'.inverseMatrix', scl_mmx+'.matrixIn[{}]'.format(src_end_idx+j+1), f=True)
        dst_end_idx = src_end_idx+j+1

    cmds.connectAttr(pos_mmx+'.matrixSum', pos_dcmx+'.inputMatrix', f=True)
    cmds.connectAttr(rot_mmx+'.matrixSum', rot_dcmx+'.inputMatrix', f=True)
    cmds.connectAttr(scl_mmx+'.matrixSum', scl_dcmx+'.inputMatrix', f=True)

    # translate connection
    cmds.connectAttr(pos_dcmx+'.outputTranslate', dst+'.t', f=True)
    cmds.connectAttr(pos_dcmx+'.outputShear', dst+'.shear', f=True)

    # rotate connection
    if cmds.objectType(dst) == 'joint':
        cmp_mat = cmds.createNode('composeMatrix', ss=True)
        inv_mat = cmds.createNode('inverseMatrix', ss=True)

        cmds.connectAttr(dst+'.jo', cmp_mat+'.inputRotate', f=True)
        cmds.connectAttr(dst+'.rotateOrder', cmp_mat+'.inputRotateOrder', f=True)
        cmds.connectAttr(cmp_mat+'.outputMatrix', inv_mat+'.inputMatrix', f=True)

        if not cmds.objExists(dst+'.ijom'):
            cmds.addAttr(dst, ln='inverseJointOrientMatrix', sn='ijom', at='matrix', k=True)

        cmds.setAttr(
            dst+'.inverseJointOrientMatrix',
            cmds.getAttr(inv_mat+'.outputMatrix'),
            type='matrix'
        )

        cmds.setAttr(
            rot_mmx+'.matrixIn[{}]'.format(dst_end_idx+1),
            cmds.getAttr(dst+'.inverseJointOrientMatrix'),
            type='matrix'
        )

    cmds.connectAttr(rot_dcmx+'.outputRotate', dst+'.r', f=True)

    # scale connection
    cmds.connectAttr(scl_dcmx+'.outputScale', dst+'.s', f=True)
    # cmds.connectAttr(src+'.s', dst+'.s', f=True)
