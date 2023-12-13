# -*- coding: utf-8 -*-
try:
    # Maya 2022-
    from builtins import range
except:
    pass

import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.OpenMaya as om_old
import maya.OpenMayaAnim as oma_old


BAKE = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]


def delete_attrs(node):
    u"""不要な接続を削除

    :param node: ノード
    :type node:str
    """
    for attr in BAKE:
        connections = cmds.listConnections(
                '{}.{}'.format(node, attr), s=True, d=False, p=True,
            )
        if not connections:
            continue

        for connection in connections:
            cmds.disconnectAttr(connection, '{}.{}'.format(node, attr))


def delete_anim_curves(nodes):
    u"""アニメーションカーブを削除

    :param nodes: ノードリスト
    :type nodes: list
    """
    connections = cmds.listConnections(nodes, s=True, d=True)
    if not connections:
        return

    connection_lists = om.MSelectionList()
    [connection_lists.add(connection) for connection in connections]
    listIter = om.MItSelectionList(connection_lists, om.MFn.kAnimCurve)
    while not listIter.isDone():
        cmds.delete(listIter.getStrings())
        next(listIter)


def rotate_filter(rotate, order):
    u"""rotateの値を変換

    :param rotate: (x, y, z) radians
    :type rotate: tuple

    :return: (x, y, z) radians
    :rtype: tuple
    """
    euler = om.MEulerRotation(*rotate, order=order)
    quat = euler.asQuaternion()
    euler_order = quat.asEulerRotation().reorder(order)

    return euler_order[0], euler_order[1], euler_order[2]


def get_values(nodes, start, end):
    u"""ノードの値を取得

    :param nodes: ノードリスト
    :param start: 開始フレーム
    :param int end: 終了フレーム
    :type nodes: list
    :type start: int
    :type end: int

    :return: data_dict {node: ({attr: type}, dataFrame), ...}
    :rtype: dict
    """
    time_array = om_old.MTimeArray()
    for i in range(start, end + 1):
        time_array.append(om_old.MTime(i, om_old.MTime.uiUnit()))

    data_dict = {
        'node': {node: {} for node in nodes},
        'times': time_array
    }

    selection_list = om.MSelectionList()
    [selection_list.add(node) for node in nodes]
    listIter = om.MItSelectionList(selection_list)

    while not listIter.isDone():
        dagpath = listIter.getDagPath()
        name = dagpath.partialPathName()
        mobject = dagpath.node()
        dependency_node = om.MFnDependencyNode(mobject)

        attrs = data_dict['node'][name]
        for attr in BAKE:
            attrs[attr] = {
                'plug': dependency_node.findPlug(attr, False),
                'type': cmds.getAttr('{}.{}'.format(name, attr), typ=True),
                'values': om_old.MDoubleArray()
            }

        next(listIter)
    listIter.reset()

    for i in range(start, end + 1, 1):
        oma.MAnimControl.setCurrentTime(om.MTime(i, om.MTime.uiUnit()))
        while not listIter.isDone():
            dagpath = listIter.getDagPath()
            name = listIter.getStrings()[0]
            attr_items = data_dict['node'][name]

            for attr, items in list(attr_items.items()):
                values = items['values']

                if attr in BAKE[3:6]:
                    mfn_transform = om.MFnTransform(dagpath)
                    rot = mfn_transform.rotation(om.MSpace.kTransform, False)
                    order = mfn_transform.rotationOrder() - 1
                    rot = rotate_filter((rot.x, rot.y, rot.z), order)

                    rotate = {
                            'rx': round(rot[0], 5),
                            'ry': round(rot[1], 5),
                            'rz': round(rot[2], 5)
                            }
                    values.append(rotate[attr])
                else:
                    values.append(round(items['plug'].asDouble(), 5))

            next(listIter)
        listIter.reset()

    return data_dict


def set_values(data_dict):
    u"""ノードにアニメーションカーブを作成して値を設定

    :param data_dict: {node: ({attr: type}, dataFrame), ...}
    :type data_dict: dict
    """
    node_items = data_dict['node']
    times = data_dict['times']

    for node, node_items in list(node_items.items()):
        for attr, attr_items in list(node_items.items()):
            sel = om_old.MSelectionList()
            sel.add('{}.{}'.format(node, attr))
            plug = om_old.MPlug()
            sel.getPlug(0, plug)

            if attr_items['type'] == 'doubleLinear':
                curve_type = oma.MFnAnimCurve.kAnimCurveTL
            elif attr_items['type'] == 'doubleAngle':
                curve_type = oma.MFnAnimCurve.kAnimCurveTA
            else:
                curve_type = oma.MFnAnimCurve.kAnimCurveTU

            anim_curve_mobj = oma_old.MFnAnimCurve().create(plug, curve_type)
            anim_curve_fn = oma_old.MFnAnimCurve(anim_curve_mobj)
            anim_curve_fn.addKeys(times, attr_items['values'])


def bake_node(nodes, start, end):
    u"""アニメーションカーブを削除

    :param list nodes: ノードリスト
    :param start: 開始フレーム
    :param int end: 終了フレーム
    :type nodes: list
    :type start: int
    :type end: int
    """
    autokey_stat = cmds.autoKeyframe(q=True, st=True)
    cmds.autoKeyframe(st=False)
    current_time = cmds.currentTime(q=True)
    cmds.currentTime(current_time)

    evaluation = cmds.evaluationManager(q=True, m=True)[0]
    cmds.evaluationManager(m='off')

    nodes = cmds.ls(nodes, dag=True, type=["joint", "transform"])
    data_dict = get_values(nodes, start, end)

    delete_anim_curves(nodes)
    for node in nodes:
        delete_attrs(node)

    set_values(data_dict)

    cmds.evaluationManager(m=evaluation)
    cmds.currentTime(current_time)
    cmds.autoKeyframe(st=autokey_stat)
