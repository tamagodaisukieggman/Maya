# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om2

def create_swing_twist(src=None, dst=None, twist_axis='x'):
    twist_dict = {
        'x':[1,0,0],
        'y':[0,1,0],
        'z':[0,0,1],
        '-x':[-1,0,0],
        '-y':[0,-1,0],
        '-z':[0,0,-1]
    }

    # Twist Add Axis
    if not cmds.objExists(dst+'.twistAxis'):
        children_attributes = ['twistAxisX', 'twistAxisY', 'twistAxisZ']
        cmds.addAttr(dst, ln='twistAxis', at='compound', nc=len(children_attributes), k=True)
        for at in children_attributes:
            cmds.addAttr(dst, ln=at, at='float', dv=0, max=1, min=-1, k=True, parent='twistAxis')

    cmds.setAttr(dst+'.twistAxis', *twist_dict[twist_axis])

    # Initial Calc
    mult = cmds.createNode('multMatrix', ss=True)
    parent_inverse = '{}.parentInverseMatrix[0]'.format(src)
    world_matrix = '{}.worldMatrix[0]'.format(src)
    cmds.connectAttr(world_matrix, '{}.matrixIn[0]'.format(mult))
    cmds.connectAttr(parent_inverse, '{}.matrixIn[1]'.format(mult))
    pinv = om2.MMatrix(cmds.getAttr(parent_inverse))
    m = om2.MMatrix(cmds.getAttr(world_matrix))
    inv_local_rest_matrix = (m * pinv).inverse()
    cmds.setAttr(
        '{}.matrixIn[2]'.format(mult), list(inv_local_rest_matrix), type='matrix'
    )

    # Twist Calc
    dcmx = cmds.createNode('decomposeMatrix', ss=True)
    md = cmds.createNode('multiplyDivide', ss=True)
    quatnm = cmds.createNode('quatNormalize', ss=True)
    quattwistslerp = cmds.createNode('quatSlerp', ss=True)

    cmds.connectAttr(mult+'.matrixSum', dcmx+'.inputMatrix', f=True)

    cmds.connectAttr(dst+'.twistAxis', md+'.input2', f=True)

    cmds.connectAttr(dcmx+'.outputQuatX', md+'.input1X', f=True)
    cmds.connectAttr(dcmx+'.outputQuatY', md+'.input1Y', f=True)
    cmds.connectAttr(dcmx+'.outputQuatZ', md+'.input1Z', f=True)

    cmds.connectAttr(md+'.outputX', quatnm+'.inputQuatX', f=True)
    cmds.connectAttr(md+'.outputY', quatnm+'.inputQuatY', f=True)
    cmds.connectAttr(md+'.outputZ', quatnm+'.inputQuatZ', f=True)
    cmds.connectAttr(dcmx+'.outputQuatW', quatnm+'.inputQuatW', f=True)

    cmds.setAttr(quattwistslerp+'.input1Quat', *[0,0,0,1])
    cmds.connectAttr(quatnm+'.outputQuat', quattwistslerp+'.input2Quat', f=True)

    # Swing Calc
    quatinv = cmds.createNode('quatInvert', ss=True)
    quatprod = cmds.createNode('quatProd', ss=True)
    quatswingslerp = cmds.createNode('quatSlerp', ss=True)

    cmds.connectAttr(quatnm+'.outputQuat', quatinv+'.inputQuat', f=True)
    cmds.connectAttr(quatinv+'.outputQuat', quatprod+'.input1Quat', f=True)
    cmds.connectAttr(dcmx+'.outputQuat', quatprod+'.input2Quat', f=True)

    cmds.setAttr(quatswingslerp+'.input1Quat', *[0,0,0,1])
    cmds.connectAttr(quatprod+'.outputQuat', quatswingslerp+'.input2Quat', f=True)

    # Combine Twist Swing
    quatcombineprod = cmds.createNode('quatProd', ss=True)
    cmds.connectAttr(quattwistslerp+'.outputQuat', quatcombineprod+'.input1Quat', f=True)
    cmds.connectAttr(quatswingslerp+'.outputQuat', quatcombineprod+'.input2Quat', f=True)


    # QuatToEuler
    qte = cmds.createNode('quatToEuler', ss=True)
    parentcmpmat = cmds.createNode('composeMatrix', ss=True)
    parentmultmat = cmds.createNode('multMatrix', ss=True)
    parentdcmx = cmds.createNode('decomposeMatrix', ss=True)

    cmds.setAttr(parentcmpmat+'.useEulerRotation', 0)

    cmds.connectAttr(quatcombineprod+'.outputQuat', parentcmpmat+'.inputQuat', f=True)
    cmds.connectAttr(parentcmpmat+'.outputMatrix', parentmultmat+'.matrixIn[0]', f=True)
    cmds.connectAttr(parentmultmat+'.matrixSum', parentdcmx+'.inputMatrix', f=True)
    cmds.connectAttr(parentdcmx+'.outputQuat', qte+'.inputQuat', f=True)

    pinv = om2.MMatrix(cmds.getAttr("{}.parentInverseMatrix[0]".format(dst)))
    m = om2.MMatrix(cmds.getAttr("{}.worldMatrix[0]".format(dst)))
    local_rest_matrix = m * pinv
    cmds.setAttr("{}.matrixIn[1]".format(parentmultmat), list(local_rest_matrix), type="matrix")

    # Twist Add Weight
    if not cmds.objExists(dst+'.twistWeight'):
        cmds.addAttr(dst, ln='twistWeight', at='float', dv=0, k=True)

    # Swing Add Weight
    if not cmds.objExists(dst+'.swingWeight'):
        cmds.addAttr(dst, ln='swingWeight', at='float', dv=0, k=True)

    pb = cmds.createNode('pairBlend', ss=True)
    pma = cmds.createNode('plusMinusAverage', ss=True)

    cmds.setAttr(pb+'.rotInterpolation', 1)
    cmds.setAttr(pb+'.inRotate1', *cmds.getAttr(dst+'.r')[0])

    dst_rot = cmds.getAttr(dst+'.r')[0]
    qte_rot = cmds.getAttr(qte+'.outputRotate')[0]
    offset_rot = [i-j for i, j in zip(dst_rot, qte_rot)]

    cmds.setAttr(pma+'.input3D[0]', *offset_rot)

    cmds.connectAttr(dst+'.twistWeight', quattwistslerp+'.inputT', f=True)
    cmds.connectAttr(dst+'.swingWeight', quatswingslerp+'.inputT', f=True)

    cmds.connectAttr(dst+'.rotateOrder', qte+'.inputRotateOrder', f=True)
    cmds.connectAttr(qte+'.inputRotateOrder', pb+'.rotateOrder', f=True)

    # cmds.connectAttr(qte+'.outputRotate', dst+'.r', f=True)

    cmds.connectAttr(qte+'.outputRotate', pma+'.input3D[1]', f=True)

    cmds.connectAttr(pma+'.output3D', pb+'.inRotate2', f=True)

    cmds.connectAttr(pb+'.outRotate', dst+'.r', f=True)

def add_swing_twist_from_selection():
    sel = cmds.ls(os=True)
    if sel:
        if len(sel) == 2:
            create_swing_twist(src=sel[0], dst=sel[1])
