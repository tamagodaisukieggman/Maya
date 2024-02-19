﻿# -*- coding: utf-8 -*-
from maya import cmds, mel
import maya.api.OpenMaya as OpenMaya

import math

TWIST_WEIGHT = "twist"
SWING_WEIGHT = "swing"
TWIST_OUTPUT = "twistOutput"
INV_TWIST_OUTPUT = "invertedTwistOutput"
SWING_OUTPUT = "swingOutput"
INV_SWING_OUTPUT = "invertedSwingOutput"

def _twist_network_exists(driver):
    """Test whether the twist decomposition network already exists on driver.

    :param driver: Driver transform
    :return: True or False
    """
    has_twist_attribute = cmds.objExists("{}.{}".format(driver, TWIST_OUTPUT))
    if not has_twist_attribute: return False
    twist_node = cmds.listConnections("{}.{}".format(driver, TWIST_OUTPUT), d=False)
    return True if twist_node else False


def _create_twist_decomposition_network(driver, twist_axis):
    """Create the twist decomposition network for driver.

    :param driver: Driver transform
    :param twist_axis: Local twist axis on driver
    """
    # Connect message attributes to the decomposed twist nodes so we can reuse them
    # if the network is driving multiple nodes

    mult = cmds.createNode("multMatrix", name="{}_local_multMatrix".format(driver))
    parent_inverse = "{}.parentInverseMatrix[0]".format(driver)
    world_matrix = "{}.worldMatrix[0]".format(driver)
    cmds.connectAttr(world_matrix, "{}.matrixIn[0]".format(mult))
    cmds.connectAttr(parent_inverse, "{}.matrixIn[1]".format(mult))
    pinv = OpenMaya.MMatrix(cmds.getAttr(parent_inverse))
    m = OpenMaya.MMatrix(cmds.getAttr(world_matrix))
    inv_local_rest_matrix = (m * pinv).inverse()
    cmds.setAttr(
        "{}.matrixIn[2]".format(mult), list(inv_local_rest_matrix), type="matrix"
    )

    rotation = cmds.createNode("decomposeMatrix", name="{}_rotation_decomposeMatrix".format(driver))
    cmds.connectAttr("{}.matrixSum".format(mult), "{}.inputMatrix".format(rotation))

    twist = cmds.createNode("quatNormalize", name="{}_twist_quatNormalize".format(driver))
    cmds.connectAttr(
        "{}.outputQuat.outputQuatW".format(rotation),
        "{}.inputQuat.inputQuatW".format(twist),
    )
    axis = "XYZ"[twist_axis]
    cmds.connectAttr(
        "{}.outputQuat.outputQuat{}".format(rotation, axis),
        "{}.inputQuat.inputQuat{}".format(twist, axis),
    )

    # swing = twist.inverse() * rotation
    inv_twist = cmds.createNode("quatInvert", name="{}_twist_quatInvert".format(driver))
    cmds.connectAttr("{}.outputQuat".format(twist), "{}.inputQuat".format(inv_twist))
    swing = cmds.createNode("quatProd", name="{}_swing_quatProd".format(driver))
    cmds.connectAttr("{}.outputQuat".format(inv_twist), "{}.input1Quat".format(swing))
    cmds.connectAttr("{}.outputQuat".format(rotation), "{}.input2Quat".format(swing))

    inv_swing = cmds.createNode("quatInvert", name="{}_swing_quatInvert".format(driver))
    cmds.connectAttr("{}.outputQuat".format(swing), "{}.inputQuat".format(inv_swing))

    # Connect the nodes to the driver so we can find and reuse them for multiple setups
    for node, attr in [
        (twist, TWIST_OUTPUT),
        (inv_twist, INV_TWIST_OUTPUT),
        (swing, SWING_OUTPUT),
        (inv_swing, INV_SWING_OUTPUT),
    ]:
        cmds.connectAttr("{}.message".format(node), "{}.{}".format(driver, attr))


def _get_swing_twist_attributes(driver):
    """Get the quaternion output attribute of the twist decomposition network.

    :param driver: Driver transform
    :param invert: True to get the inverted twist attribute
    :param twist_axis: Local twist axis of driver
    :return: The quaternion output attribute
    """
    nodes = []
    for attr in [TWIST_OUTPUT, INV_TWIST_OUTPUT, SWING_OUTPUT, INV_SWING_OUTPUT]:
        node = cmds.listConnections("{}.{}".format(driver, attr), d=False)
        if not node:
            # The network isn't connected so create it
            _create_twist_decomposition_network(driver, twist_axis)
            return _get_swing_twist_attributes(driver)
        nodes.append(node[0])

    return ["{}.outputQuat".format(node) for node in nodes]


def _create_slerp(driven, weight, rotation, inv_rotation, attribute):
    slerp = cmds.createNode("quatSlerp", name="{}_{}_quatSlerp".format(driven, attribute))
    cmds.setAttr("{}.{}".format(driven, attribute), math.fabs(weight))
    cmds.connectAttr("{}.{}".format(driven, attribute), "{}.inputT".format(slerp))
    cmds.setAttr("{}.input1QuatW".format(slerp), 1)
    if weight >= 0.0:
        cmds.connectAttr(rotation, "{}.input2Quat".format(slerp))
    else:
        cmds.connectAttr(inv_rotation, "{}.input2Quat".format(slerp))
    return slerp


def create_swing_twist(
    driver, driven, twist_weight=1.0, swing_weight=1.0, twist_axis=0, connect_rotate=None
):
    """Create a node network to drive a transforms offsetParentMatrix from the
    decomposed swing/twist of another transform.

    Setting cmt.settings.ENABLE_PLUGINS to False will use vanilla Maya nodes. Otherwise,
    the compiled plug-in will be used.

    :param driver: Driver transform
    :param driven: Driven transform
    :param twist_weight: -1 to 1 twist scalar
    :param swing_weight: -1 to 1 swing scalar
    :param twist_axis: Local twist axis on driver (0: X, 1: Y, 2: Z)
    """
    for attr in [TWIST_OUTPUT, INV_TWIST_OUTPUT, SWING_OUTPUT, INV_SWING_OUTPUT]:
        if not cmds.objExists("{}.{}".format(driver, attr)):
            cmds.addAttr(driver, ln=attr, at="message")

    if not _twist_network_exists(driver):
        _create_twist_decomposition_network(driver, twist_axis)
    for attr in [TWIST_WEIGHT, SWING_WEIGHT]:
        if not cmds.objExists("{}.{}".format(driven, attr)):
            cmds.addAttr(
                driven,
                ln=attr,
                keyable=True,
                minValue=-1,
                maxValue=1,
                defaultValue=math.fabs(twist_weight),
            )

    twist, inv_twist, swing, inv_swing = _get_swing_twist_attributes(driver)

    twist_slerp = _create_slerp(driven, twist_weight, twist, inv_twist, TWIST_WEIGHT)
    swing_slerp = _create_slerp(driven, swing_weight, swing, inv_swing, SWING_WEIGHT)

    rotation = cmds.createNode("quatProd", name="{}_rotation_quatProd".format(driver))
    cmds.connectAttr(
        "{}.outputQuat".format(twist_slerp), "{}.input1Quat".format(rotation)
    )
    cmds.connectAttr(
        "{}.outputQuat".format(swing_slerp), "{}.input2Quat".format(rotation)
    )

    rotation_matrix = cmds.createNode(
        "composeMatrix", name="{}_rotation_composeMatrix".format(driver)
    )
    cmds.setAttr("{}.useEulerRotation".format(rotation_matrix), 0)
    cmds.connectAttr(
        "{}.outputQuat".format(rotation), "{}.inputQuat".format(rotation_matrix)
    )

    mult = cmds.createNode("multMatrix", name="{}_offset_parent_multMatrix".format(driven))
    cmds.connectAttr(
        "{}.outputMatrix".format(rotation_matrix), "{}.matrixIn[0]".format(mult)
    )

    pinv = OpenMaya.MMatrix(cmds.getAttr("{}.parentInverseMatrix[0]".format(driven)))
    m = OpenMaya.MMatrix(cmds.getAttr("{}.worldMatrix[0]".format(driven)))
    local_rest_matrix = m * pinv
    cmds.setAttr("{}.matrixIn[1]".format(mult), list(local_rest_matrix), type="matrix")

    # # Zero out local xforms to prevent double xform
    # for attr in ["{}{}".format(x, y) for x in ["t", "r", "jo"] for y in "xyz"]:
    #     is_locked = cmds.getAttr("{}.{}".format(driven, attr), lock=True)
    #     if is_locked:
    #         cmds.setAttr("{}.{}".format(driven, attr), lock=False)
    #     cmds.setAttr("{}.{}".format(driven, attr), 0.0)
    #     if is_locked:
    #         cmds.setAttr("{}.{}".format(driven, attr), lock=True)

    if connect_rotate:
        # cmds.disconnectAttr("{}.matrixSum".format(mult), "{}.offsetParentMatrix".format(driven))
        matrix = cmds.getAttr("{}.matrixSum".format(mult))
        cmds.setAttr(driven + '.opm', matrix, type='matrix')

        pos_matrix = cmds.getAttr(driven + '.opm')

        rot_dcmx = cmds.createNode("decomposeMatrix", name="{}_offset_rotate_decomposeMatrix".format(driven))
        rot_pma = cmds.createNode("plusMinusAverage", name="{}_offset_rotate_plusMinusAverage".format(driven))

        cmds.connectAttr("{}.matrixSum".format(mult), "{}.inputMatrix".format(rot_dcmx))

        mat_rot = cmds.getAttr("{}.outputRotate".format(rot_dcmx))
        negative_rot = [val * -1 for val in mat_rot[0]]
        cmds.setAttr("{}.input3D[0]".format(rot_pma), *negative_rot)
        cmds.setAttr("{}.input3D[1]".format(rot_pma), *cmds.getAttr("{}.r".format(driven))[0])
        cmds.connectAttr("{}.outputRotate".format(rot_dcmx), "{}.input3D[2]".format(rot_pma))
        cmds.connectAttr("{}.output3D".format(rot_pma), "{}.r".format(driven))

        matrix = 16*[0]
        matrix[0], matrix[5], matrix[10], matrix[15] = 1,1,1,1
        tx, ty, tz = pos_matrix[12], pos_matrix[13], pos_matrix[14]
        cmds.setAttr(driven + '.opm', matrix, type='matrix') # Zero out opm
        cmds.setAttr(driven + '.t', *[tx, ty, tz]) # set pos

    else:
        cmds.connectAttr(
            "{}.matrixSum".format(mult), "{}.offsetParentMatrix".format(driven)
        )


# create_swing_twist('Thigh_L', 'joint2', twist_weight=0.5, swing_weight=0.0, twist_axis=1, connect_rotate=True)
