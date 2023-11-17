# -*- coding: utf-8 -*-
from maya import cmds, mel
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import maya.OpenMayaUI as omui

import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma2

import codecs
from collections import OrderedDict
from datetime import datetime
from distutils.util import strtobool
from functools import partial, wraps
import fnmatch
import functools
import getpass
import json
from logging import getLogger
import math
import os
import re
import subprocess
import traceback
import pdb

u"""モーション反転ツール(GUI)"""

# from .command import ReverseMotionCmd
# from wzdx.maya.anim.bake import Bake

WORLD_OFFSET = 'main_ctrl'

logger = getLogger(__name__)

# ---------------------------------------------------
# decorator
def suspend(func):
    u"""リフレッシュ イベントをsuspend"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        cmds.refresh(su=True)
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.error('{}'.format(e))
            logger.error(traceback.format_exc())
        finally:
            cmds.refresh(su=False)
            return result
    return wrapper


def keep_selections(func):
    u"""選択を保持するdecorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return _keep_selections_wrapper(func, *args, **kwargs)
    return wrapper


def _keep_selections_wrapper(func, *args, **kwargs):
    u"""選択を保持"""
    selection = cmds.ls(sl=True)
    result = func(*args, **kwargs)
    if selection:
        cmds.select(selection, ne=True)
    return result

# ---------------------------------------------------


class Bake(object):

    @classmethod
    def _get_keyable_attrs(cls, node, attrs=None):
        u"""キー設定が可能なアトリビュートの取得

        :param node: ノード
        :return: キー設定
        """
        if attrs:
            key_attrs = cmds.listAnimatable(['{}.{}'.format(node, attr) for attr in attrs])
        else:
            key_attrs = cmds.listAnimatable(node)
        if key_attrs:
            key_attrs = [key_attr.split('.')[-1] for key_attr in key_attrs]
            return key_attrs
        else:
            return []

    @classmethod
    def _is_constraint(cls, node):
        u"""コンストレインかどうか

        :param node:
        :return: bool
        """
        constraint_type = (
            om2.MFn.kAimConstraint,
            om2.MFn.kConstraint,
            om2.MFn.kDynamicConstraint,
            om2.MFn.kGeometryConstraint,
            om2.MFn.kHairConstraint,
            om2.MFn.kNormalConstraint,
            om2.MFn.kOldGeometryConstraint,
            om2.MFn.kOrientConstraint,
            om2.MFn.kParentConstraint,
            om2.MFn.kPluginConstraintNode,
            om2.MFn.kPointConstraint,
            om2.MFn.kPointOnPolyConstraint,
            om2.MFn.kPoleVectorConstraint,
            om2.MFn.kRigidConstraint,
            om2.MFn.kScaleConstraint,
            om2.MFn.kSymmetryConstraint,
            om2.MFn.kTangentConstraint,
        )

        sel = om2.MGlobal.getSelectionListByName(node)
        depend_node = sel.getDependNode(0)
        # logger.debug('{} {}'.format(node, depend_node.apiTypeStr))
        if depend_node.apiType() in constraint_type:
            return True
        else:
            return False

    @classmethod
    def _disconnect_constraint(cls, node):
        u"""コンストレインを切断

        :param node: ノード
        """
        # キー設定前にコンストレインなどの接続があれば切断
        attrs = cls._get_keyable_attrs(node)

        for attr in attrs:
            # Transform => Shape の場合アトリビュートが違う場合
            try:
                connections = cmds.listConnections(
                    '{}.{}'.format(node, attr), s=True, d=False, p=True,
                )
                if not connections:
                    continue

                for connection in connections:
                    connect_node = connection.split('.')[0]
                    if cls._is_constraint(connect_node):
                        cmds.disconnectAttr(connection, '{}.{}'.format(node, attr))
            except Exception as e:
                logger.error('{}'.format(e))

    @classmethod
    def _is_delete_attrs(cls, attr):
        u"""削除して良いアトリビュートか"""
        delete_words = ('blendPoint', 'blendOrient', 'blendParent')
        for word in delete_words:
            if re.search(word, attr):
                return True
        return False

    @classmethod
    def _delete_attrs(cls, node):
        u"""不要なアトリビュートを削除"""
        attrs = cls._get_keyable_attrs(node)
        for attr in attrs:
            if cls._is_delete_attrs(attr):
                cmds.deleteAttr('{}.{}'.format(node, attr))

    @classmethod
    def _rotate_filter(cls, rotate, order):
        u"""rotateの値を変換

        :param rotate: (x, y, z) radians
        :return: (x, y, z) radians
        """
        e = om2.MEulerRotation(*rotate, order=order)
        q = e.asQuaternion()
        qua = om2.MQuaternion(q)
        rad_order = qua.asEulerRotation().reorder(order)

        return rad_order[0], rad_order[1], rad_order[2]

    @classmethod
    def get_values(cls, nodes, start, end, **kwargs):
        u"""値の取得

        :param nodes: ノードのリスト
        :param start: start
        :param end: end
        :return: {node: ({attr: type}, dataFrame), ...}
        """
        time_array = om.MTimeArray()
        [time_array.append(om.MTime(i, om.MTime.uiUnit())) for i in range(start, end + 1)]

        results = {
            'node': {node: {} for node in nodes},
            'time': time_array,
        }
        node_transform = {}

        selection_list = om2.MSelectionList()
        [selection_list.add(node) for node in nodes]
        iter_ = om2.MItSelectionList(selection_list)

        # attributeと型の取得
        while not iter_.isDone():
            dagpath = iter_.getDagPath()
            mobject = dagpath.node()
            dependency_node = om2.MFnDependencyNode(mobject)
            name = dagpath.partialPathName()

            attrs = results['node'][name]
            keyable_attrs = cls._get_keyable_attrs(name, kwargs.setdefault('attrs', None))
            if (
                'rotateX' in keyable_attrs and
                'rotateY' in keyable_attrs and
                'rotateZ' in keyable_attrs
            ):
                node_transform[name] = True
            else:
                node_transform[name] = False

            for i in range(dependency_node.attributeCount()):
                plug = om2.MPlug(mobject, dependency_node.attribute(i))
                attr = plug.info.split('.')[-1]

                if attr in keyable_attrs:
                    attrs[attr] = {
                        'plug': plug,
                        'type': cmds.getAttr('{}.{}'.format(name, attr), typ=True),
                        'values': om.MDoubleArray(),
                    }

            iter_.next()
        iter_.reset()

        # フレームごとの値をdataFrameに格納
        for i in range(start, end + 1, 1):
            oma2.MAnimControl.setCurrentTime(om2.MTime(i, om2.MTime.uiUnit()))
            while not iter_.isDone():
                dagpath = iter_.getDagPath()
                name = dagpath.partialPathName()
                attr_items = results['node'][name]

                if node_transform[name]:
                    mfn_transform = om2.MFnTransform(dagpath)
                    r = mfn_transform.rotation(om2.MSpace.kTransform, False)
                    # MEluerRotationのorderはMTransformationMatrixのorderと値が1違うので引く
                    order = mfn_transform.rotationOrder() - 1
                    r = cls._rotate_filter((r.x, r.y, r.z), order)
                    rotate = {'rotateX': round(r[0], 5), 'rotateY': round(r[1], 5), 'rotateZ': round(r[2], 5)}

                    for attr, items in attr_items.items():
                        values = items['values']
                        if attr in ('rotateX', 'rotateY', 'rotateZ'):
                            values.append(rotate[attr])
                        else:
                            values.append(round(items['plug'].asDouble(), 5))
                else:
                    for attr, items in attr_items.items():
                        values = items['values']
                        values.append(round(items['plug'].asDouble(), 5))

                iter_.next()
            iter_.reset()

        return results

    @classmethod
    def _delete_anim_curves(cls, nodes):
        # アニメーションカーブの削除
        connections = cmds.listConnections(nodes, s=True, d=True)
        if not connections:
            return

        connection_lists = om2.MSelectionList()
        [connection_lists.add(connection) for connection in connections]
        iter_ = om2.MItSelectionList(connection_lists, om2.MFn.kAnimCurve)
        while not iter_.isDone():
            cmds.delete(iter_.getStrings())
            iter_.next()

    @classmethod
    def _get_double_angle_curves(cls, nodes):
        connections = cmds.listConnections(nodes, s=True, d=False)
        if not connections:
            return []
        curves = cmds.ls(connections, typ='animCurveTA')

        return curves

    @classmethod
    def _cleanup_nodes(cls, nodes):
        u"""不要な接続などを除去"""
        for node in nodes:
            # コンストレインの削除
            cls._disconnect_constraint(node)
            cls._delete_attrs(node)

        # 古いアニメーションカーブを削除
        cls._delete_anim_curves(nodes)

    @classmethod
    def _set_keys(cls, nodes, start, end, **kwargs):
        u"""キーフレームの作成

        :param nodes: ノードのリスト
        :param start: start
        :param end: end
        :return: {node: ({attr: type}, dataFrame), ...}
        """
        filter_curves = []
        euler_filter = kwargs.setdefault('euler_filter', False)
        remove_static_channels = kwargs.setdefault('remove_static_channels', False)

        results = cls.get_values(nodes, start, end, attrs=kwargs.setdefault('attrs', None))
        node_items = results['node']
        times = results['time']

        # ベイク前に不要な接続などを除去
        cls._cleanup_nodes(nodes)

        for node, node_items in node_items.items():
            for attr, attr_items in node_items.items():
                # コンストレイン削除時にblend関連のアトリビュートが消えるので事前にチェック
                if not cmds.attributeQuery(attr, node=node, ex=True):
                    continue

                if attr_items['type'] == 'doubleLinear':
                    anim_curve = cmds.createNode('animCurveTL', n='{}_{}'.format(node, attr))
                elif attr_items['type'] == 'doubleAngle':
                    anim_curve = cmds.createNode('animCurveTA', n='{}_{}'.format(node, attr))
                    filter_curves.append(anim_curve)
                else:
                    anim_curve = cmds.createNode('animCurveTU', n='{}_{}'.format(node, attr))

                curve_selection = om.MSelectionList()
                om.MGlobal.getSelectionListByName(anim_curve, curve_selection)
                mobj = om.MObject()
                curve_selection.getDependNode(0, mobj)
                anim_curve_fn = oma.MFnAnimCurve(mobj)
                anim_curve_fn.addKeys(times, attr_items['values'])

                # スタティックチャンネルの除去(先頭１フレームのキーは残す)
                if remove_static_channels:
                    if anim_curve_fn.isStatic():
                        for i in range(anim_curve_fn.numKeys() - 1, 0, -1):
                            anim_curve_fn.remove(i)

                cmds.connectAttr('{}.output'.format(anim_curve), '{}.{}'.format(node, attr), f=True)

        # Euler Filter
        if euler_filter:
            cmds.filterCurve(filter_curves)

    @classmethod
    @suspend
    def main2015(cls, root_nodes, **kwargs):
        u"""BakeしてEuler Filterをかける

        :param root_nodes: ノードのリスト
        :param start: 開始フレーム
        :param end: 終了フレーム
        :param hierarchy: 階層展開オプション ('below' or 'none')
        :param attrs: ベイクするアトリビュート
        """
        start = int(kwargs.setdefault('start', cmds.playbackOptions(q=True, min=True)))
        end = int(kwargs.setdefault('end', cmds.playbackOptions(q=True, max=True)))
        hierarchy = kwargs.setdefault('hierarchy', 'below')
        attrs = kwargs.setdefault('attrs', None)
        euler_filter = kwargs.setdefault('euler_filter', False)

        # logger.debug('Bake Option\nstart: {s} end:{e}\nhierarcy: {h}\nattrs: {a}'.format(
        #     s=start, e=end, h=hierarchy, a=attrs,
        # ))
        nodes = cmds.ls(root_nodes, dag=True) if hierarchy == 'below' else cmds.ls(root_nodes)
        nodes = [node for node in nodes if not cls._is_constraint(node) and cmds.listAnimatable(node)]

        current = cmds.currentTime(q=True)
        cls._set_keys(nodes, start, end, attrs=attrs, euler_filter=euler_filter)
        # 最初のフレームにリセット
        oma2.MAnimControl.setCurrentTime(om2.MTime(current, om2.MTime.uiUnit()))

    @classmethod
    def main2018(cls, root_nodes, **kwargs):
        u"""BakeしてEuler Filterをかける

        :param root_nodes: ノードのリスト
        :param start: 開始フレーム
        :param end: 終了フレーム
        :param hierarchy: 階層展開オプション ('below' or 'none')
        :param attrs: ベイクするアトリビュート
        """
        evaluation = cmds.evaluationManager(q=True, m=True)[0]
        cmds.evaluationManager(m='off')

        cls.main2015(root_nodes, **kwargs)
        cmds.evaluationManager(m=evaluation)

    @classmethod
    def main(cls, root_nodes, **kwargs):

        autokey_stat = cmds.autoKeyframe(q=True, st=True)

        cmds.autoKeyframe(st=False)

        current_time = cmds.currentTime(q=True)
        # cycleCheck Off
        cycle_check = cmds.cycleCheck(q=True, e=True)
        cmds.cycleCheck(e=False)
        cmds.currentTime(current_time, e=True)
        cmds.cycleCheck(e=cycle_check)

        if int(cmds.about(v=True)) < 2018:
            # logger.debug('Bake Mode: Maya2015')
            cls.main2015(root_nodes, **kwargs)
        else:
            # logger.debug('Bake Mode: Maya2018')
            cls.main2018(root_nodes, **kwargs)

        cmds.currentTime(current_time)
        cmds.autoKeyframe(st=autokey_stat)


def _get_selections():
    u"""選択情報を取得する

    リグのセットを選んでいるときはリグのノードに展開する

    :return: 選択ノード
    """
    selections = []
    nodes = cmds.ls(sl=True)
    for node in nodes:
        if cmds.objectType(node) == 'objectSet':
            temp_nodes = cmds.sets(node, q=True)
            if temp_nodes:
                selections.extend(temp_nodes)
        else:
            selections.append(node)

    return selections


@keep_selections
def main():
    u"""Animation > ベイクアニメーション"""

    nodes = _get_selections()
    if not nodes:
        logger.warning('Please Select Node')
        return

    Bake.main(nodes, hierarchy='none', euler_filter=True)


class ReverseMotionCmd(object):

    type_at = (
        'bool',
        'long', 'long2', 'long3',
        'short', 'short2', 'short3',
        'byte', 'char', 'enum',
        'float', 'float2', 'float3',
        'double', 'double2', 'doubleAngle', 'doubleLinear',
        'compound', 'message', 'time',
    )
    type_dt = (
        'string', 'stringArray', 'matrix', 'ftMatrix',
        'doubleArray', 'floatArray', 'Int32Array', 'vectorArray',
    )

    # 一時凌ぎの処理の判定に使うノード
    temp_check_words = (
        'shoulder',
        'hand',
        'thumb',
        'index',
        'middle',
        'ring',
        'pinky',
    )

    temp_check_words = (
        'Shoulder',
        'Wrist',
        'Thumb',
        'Index',
        'Middle',
        'Ring',
        'Pinky',
    )

    # ########################################
    #  Math
    # ########################################
    @staticmethod
    def _conv_degrees(degrees):
        u"""角度を-180度～180度の範囲に変換し直す

        :param degrees: degrees
        :return: degrees
        """
        degrees_ = degrees % 360
        degrees_ = degrees_ - 360 if degrees_ > 180 else degrees_
        return round(degrees_, 1)

    @classmethod
    def _get_rotate_matrix(cls, node):
        u"""回転行列の取得

        :param node: ノード
        :return: 回転行列
        """
        cos = lambda degrees: round(math.cos(math.radians(degrees)), 3)
        sin = lambda degrees: round(math.sin(math.radians(degrees)), 3)

        order = cmds.getAttr('{}.rotateOrder'.format(node))
        x, y, z = cmds.xform(node, q=True, ws=True, ro=True)
        x = cls._conv_degrees(x)
        y = cls._conv_degrees(y)
        z = cls._conv_degrees(z)
        rx = [
            [1, 0, 0],
            [0, cos(x), sin(x)],
            [0, -1 * sin(x), cos(x)],
        ]
        ry = [
            [cos(y), 0, -1 * sin(y)],
            [0, 1, 0],
            [sin(y), 0, cos(y)],
        ]
        rz = [
            [cos(z), sin(z), 0],
            [-1 * sin(z), cos(z), 0],
            [0, 0, 1],
        ]
        if order == 0:
            rmatrix = (rx, ry, rz)
        elif order == 1:
            rmatrix = (ry, rz, rx)
        elif order == 2:
            rmatrix = (rz, rx, ry)
        elif order == 3:
            rmatrix = (rx, rz, ry)
        elif order == 4:
            rmatrix = (ry, rx, rz)
        else:
            rmatrix = (rz, ry, rx)

        return rmatrix

    @staticmethod
    def _vec3_x_matrix3x3(vec3, mat3x3):
        u"""vector3 × matrix3x3 の計算

        :param vec3: vector3
        :param mat3x3: matrix3x3
        :return: vector3
        """
        return (
            vec3[0] * mat3x3[0][0] + vec3[1] * mat3x3[1][0] + vec3[2] * mat3x3[2][0],
            vec3[0] * mat3x3[0][1] + vec3[1] * mat3x3[1][1] + vec3[2] * mat3x3[2][1],
            vec3[0] * mat3x3[0][2] + vec3[1] * mat3x3[1][2] + vec3[2] * mat3x3[2][2],
        )

    # ########################################
    #  Rig
    # ########################################
    @classmethod
    def _is_behavior(cls, node, right_id, left_id, primary_axis='x', secondary_axis='y'):
        u"""behaivorか

        :param node: ノード
        :param right_id: 右の識別子
        :param left_id: 左の識別子
        :param primary_axis: primary axis
        :param secondary_axis: secondary axis
        :return: bool
        """
        mirror_node = cls._get_mirror_node(node, right_id, left_id)
        if not mirror_node or cmds.ls(mirror_node, tr=True):
            return False

        primary_index = cls._get_index_from_axis(primary_axis)
        secondary_index = cls._get_index_from_axis(secondary_axis)

        local_axis = cls._get_local_axis(node, primary_axis, secondary_axis)
        mirror_local_axis = cls._get_local_axis(mirror_node, primary_axis, secondary_axis)

        primary_v = local_axis['primary_vector']
        secondary_v = local_axis['secondary_vector']
        mirror_main_v = mirror_local_axis['primary_vector']
        mirror_secondary_v = mirror_local_axis['secondary_vector']

        if (
            round(primary_v[primary_index], 2) == round(mirror_main_v[primary_index], 2) and
            round(secondary_v[secondary_index], 2) == round(mirror_secondary_v[secondary_index], 2)
        ):
            return False
        else:
            return True

    @staticmethod
    def _get_index_from_axis(axis):
        u"""軸に対応するindexを返す

        :param axis: 'x', 'y', 'z'
        :return: x 0, y 1, z 2 (それ以外の入力亜はx軸をデフォルトして「0」を返す)
        """
        axis_index = {'x': 0, 'y': 1, 'z': 2}
        if axis in axis_index:
            return axis_index[axis]
        else:
            return 0

    @classmethod
    def _get_local_axis(cls, node, primary_axis='x', secondary_axis='y'):
        u"""ローカル軸の取得

        :param node: ノード
        :param primary_axis: primary axis
        :param secondary_axis: secondary axis
        :return:{'primary_axis': axis, 'secondary_axis': axis, 'primary_vector': vector, 'secondary_vector': vector}
        """
        round_vec = lambda vec3, n: (round(vec3[0], n), round(vec3[1], n), round(vec3[2], n))

        vector_x = (1, 0, 0)
        vector_y = (0, 1, 0)
        vector_z = (0, 0, 1)

        primary_index = cls._get_index_from_axis(primary_axis)
        secondary_index = cls._get_index_from_axis(secondary_axis)

        rmatrix = cls._get_rotate_matrix(node)
        for r in rmatrix:
            vector_x = cls._vec3_x_matrix3x3(vector_x, r)
            vector_y = cls._vec3_x_matrix3x3(vector_y, r)
            vector_z = cls._vec3_x_matrix3x3(vector_z, r)

        vector_x = round_vec(vector_x, 3)
        vector_y = round_vec(vector_y, 3)
        vector_z = round_vec(vector_z, 3)

        max_ = max((abs(vector_x[primary_index]), abs(vector_y[primary_index]), abs(vector_z[primary_index])))
        if round(max_, 3) == round(abs(vector_x[primary_index]), 3):
            primary_a = 'x'
            primary_v = vector_x
        elif round(max_, 3) == round(abs(vector_y[primary_index]), 3):
            primary_a = 'y'
            primary_v = vector_y
        else:
            primary_a = 'z'
            primary_v = vector_z

        max_ = max((abs(vector_x[secondary_index]), abs(vector_y[secondary_index]), abs(vector_z[secondary_index])))
        if round(max_, 3) == round(abs(vector_x[secondary_index]), 3):
            secondary_a = 'x'
            secondary_v = vector_x
        elif round(max_, 3) == round(abs(vector_y[secondary_index]), 3):
            secondary_a = 'y'
            secondary_v = vector_y
        else:
            secondary_a = 'z'
            secondary_v = vector_z

        return {
            'primary_axis': primary_a, 'secondary_axis': secondary_a,
            'primary_vector': primary_v, 'secondary_vector': secondary_v,
        }

    @staticmethod
    def _get_world_offset(nodes):
        u"""ノードのリストからworldOffsetを取得

        :param nodes: ノードのリスト
        :return: worldOffset
        """
        for node in nodes:
            if node.find(WORLD_OFFSET) != -1:
                return node

    @staticmethod
    def _has_keyframe(node):
        u"""キーフレームを持っているか

        :param node: ノード名
        :return: bool
        """
        key_index = cmds.keyframe(node, q=True, iv=True)
        return True if key_index else False

    @staticmethod
    def _get_anim_curve(node):
        u"""animCurveの取得

        :param node: ノード名
        :return: {アトリビュート名: カーブ名}
        """
        attr_curve = {}  # アトリビュート名: カーブ名
        attrs = ('tx', 'ty', 'tz', 'rx', 'ry', 'rz')
        # 初期化
        for attr in attrs:
            attr_curve[attr] = None

        for attr in attrs:
            curves = cmds.listConnections('{node}.{attr}'.format(node=node, attr=attr))
            if curves:
                for curve in curves:
                    if cmds.objectType(curve).find('animCurve') != -1:
                        attr_curve[attr] = curve
                        break
            else:
                attr_curve[attr] = None

        return attr_curve

    @staticmethod
    def _is_id_node(node, id_):
        u"""識別子を持つノードかどうか

        :param node: ノード名
        :param id_: 識別子
        :return: bool
        """
        return True if re.search(id_, node) else False

    @staticmethod
    def _get_mirror_node(node, right_id, left_id):
        u"""対称のノードの取得

        :param node: ノード名
        :param right_id: 右側の識別子
        :param left_id: 左側の識別子
        :return:
        """
        left_node = re.sub(right_id, left_id, node)
        right_node = re.sub(left_id, right_id, node)
        if left_node == right_node:
            return None
        elif left_node != node:
            return left_node
        else:
            return right_node

    # ########################################
    #  Reverse
    # ########################################
    @staticmethod
    def _get_reverse_attrs(axis, copytype, is_behavior):
        u"""指定した軸に対して反転するアトリビュートを取得

        :param axis: 軸
        :param copytype: 1: ミラーコピー, 2 ミラー反転
        :param is_behavior: behaviorか
        :return: 反転するアトリビュート
        """
        if copytype == 1:
            if is_behavior:
                axis_attrs = {
                    'x': ('tx', ),
                    'y': ('ty', ),
                    'z': ('tz', ),
                }
            else:
                axis_attrs = {
                    'x': ('tx', 'ry', 'rz'),
                    'y': ('ty', 'rx', 'rz'),
                    'z': ('tz', 'rx', 'ry'),
                }
            if axis in axis_attrs:
                return axis_attrs[axis]
            else:
                return None

        elif copytype == 2:
            axis_attrs = {
                'x': ('tx', 'ry', 'rz'),
                'y': ('ty', 'rx', 'rz'),
                'z': ('tz', 'rx', 'ry'),
            }
            if axis in axis_attrs:
                return axis_attrs[axis]
            else:
                return None
        else:
            return None

    @staticmethod
    def _reverse_pose(node, reverse_attrs, time):
        u"""ポーズを反転

        :param node: ノード名
        :param reverse_attrs: 反転するアトリビュート
        :param time: time
        """
        for attr in reverse_attrs:
            if not cmds.getAttr('{}.{}'.format(node, attr), l=True):
                value = cmds.getAttr('{}.{}'.format(node, attr), t=time)
                cmds.setAttr('{}.{}'.format(node, attr), -1 * value)
                cmds.setKeyframe('{}.{}'.format(node, attr))

    @classmethod
    def _reverse_motion(cls, node, reverse_attrs):
        u"""モーションを反転

        :param node: ノード名
        :param reverse_attrs: 反転するアトリビュート
        """
        attr_curve = cls._get_anim_curve(node)
        for attr in reverse_attrs:
            if attr_curve[attr]:
                cmds.scaleKey(attr_curve[attr], time=(':',), float=(':',), valueScale=-1, valuePivot=0)

    @classmethod
    def _reverse(cls, node, axis, animtype, **kwargs):
        u"""ポーズまたはモーションの反転

        :param node: ノード名
        :param axis: 軸
        :param animtype: 1 pose, 2 motion
        :param copytype: 1: ミラーコピー, 2 ミラー反転
        :param time: 反転時のtime
        """
        logger.debug('Reverse: {} {} {}'.format(node, axis, animtype))

        copytype = kwargs.setdefault('copytype', 2)
        time = kwargs.setdefault('time', 0)
        is_behavior = kwargs.setdefault('is_behavior', True)

        negative_objects = kwargs.setdefault('negative_objects', list())
        negative_attrs = kwargs.setdefault('negative_attrs', list())

        neg_attr_dict = {
            0: 'tx',
            1: 'ty',
            2: 'tz',
            3: 'rx',
            4: 'ry',
            5: 'rz',
        }

        negative_attrs_stock = []
        for i, neg_sts in enumerate(negative_attrs):
            if neg_sts:
                negative_attrs_stock.append(neg_attr_dict[i])

        # ノードの存在判定
        if not cmds.ls(node):
            logger.warning(u'ノードが存在しないため反転をスキップしました: {}'.format(node))
            return
        # 反転するアトリビュートの取得
        reverse_attrs = cls._get_reverse_attrs(axis, copytype, is_behavior)

        # ここから下に一時対処の処理を差し込む
        # ------------------------------------------------------
        for word in cls.temp_check_words:
            if word in node:
                reverse_attrs = ('tx', 'ry', 'rz')  # mirrorもreverseも同じ
                break

        ############# world extend start
        # world用に追加したダミー処理
        world_extend_words = ['hand', 'shoulder']
        for word in world_extend_words:
            if word in node:
                reverse_attrs = ('tx', 'tx', 'tx') # ダミーの値
                break
        ############# end

        ############# wizard2 extend start
        if negative_attrs_stock:
            for word in negative_objects:
                if word in node:
                    reverse_attrs = negative_attrs_stock # ダミーの値
                    break
        else:
            wizard2_extend_words = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
            for word in wizard2_extend_words:
                if word in node:
                    reverse_attrs = ('tx', 'ry', 'rz') # ダミーの値
                    break

        ############# end

        # ------------------------------------------------------
        # ここまで

        if not reverse_attrs:
            logger.warning(u'{}: 軸の指定が不正なので終了します'.format(node))
            return

        if animtype == 1:
            cls._reverse_pose(node, reverse_attrs, time)
        else:
            cls._reverse_motion(node, reverse_attrs)

    @classmethod
    def _reverse_world_offset(cls, world_offset, axis, mode, **kwargs):
        u"""WorldOffsetの反転

        :param world_offset: worldOffsetノード
        :param axis: 反転の軸
        :param mode: 1 Pose, 2 Motion
        :param kwargs: 'time' 反転時のtime
        """
        time = kwargs.setdefault('time', 0)
        # Pose
        if mode == 1:
            if axis == 'x':
                tx = cmds.getAttr('{}.tx'.format(world_offset), t=time)
                cmds.setAttr('{}.tx'.format(world_offset), -1 * tx)
                cmds.setKeyframe('{}.tx'.format(world_offset))
                ry = cmds.getAttr('{}.ry'.format(world_offset), t=time)
                cmds.setAttr('{}.ry'.format(world_offset), -1 * ry)
                cmds.setKeyframe('{}.ry'.format(world_offset))
            elif axis == 'z':
                tz = cmds.getAttr('{}.tz'.format(world_offset), t=time)
                cmds.setAttr('{}.tz'.format(world_offset), -1 * tz)
                cmds.setKeyframe('{}.tz'.format(world_offset))
                ry = cmds.getAttr('{}.ry'.format(world_offset), t=time)
                cmds.setAttr('{}.ry'.format(world_offset), cls._conv_degrees(ry + 180))
                cmds.setKeyframe('{}.ry'.format(world_offset))
        # Motion
        else:
            if axis == 'x':
                cls._reverse_motion(world_offset, ('tx', 'ry'))
            elif axis == 'z':
                cls._reverse_motion(world_offset, ('tz',))
                cmds.keyframe(world_offset, time=(':',), float=(':',), at='ry', vc=180, r=True)

    # ########################################
    #  Mirror
    # ########################################
    @classmethod
    def _copy_animation(cls, node1, node2, **kwargs):
        u"""アニメーションキーをコピー、交換

        :param node1: ノード名1
        :param node2: ノード名2
        :param animtype: 1: ポーズ, 2: モーション
        :param copytype: 1: ミラーコピー, 2 ミラー反転
        :param time: time
        """
        animtype = kwargs.setdefault('animtype', 1)
        copytype = kwargs.setdefault('copytype', 2)
        time = kwargs.setdefault('time', 0)
        times = (time, time)

        # ノードの存在判定
        for node in (node1, node2):
            if not cmds.ls(node):
                logger.debug(u'ノードが存在しないため反転をスキップしました: {}'.format(node))
                return
        # キーフレームの存在判定
        for node in (node1, node2):
            if not cls._has_keyframe(node):
                logger.debug(u'キーが存在しないため反転をスキップしました: {}'.format(node))
                return

        logger.debug(u'アニメーション入れ替え: {}, {}, frame: {}'.format(node1, node2, time))

        # キーの保存用の一時ノードの作成
        temp_node = cmds.spaceLocator()[0]
        try:
            # 一時ノードにキーの保存に必要なカスタムアトリビュートをnode1から取得して追加
            custom_attrs = cmds.listAttr(node1, ud=True, k=True) or []
            for attr in custom_attrs:
                attr_type = cmds.getAttr('{}.{}'.format(node1, attr), typ=True)
                logger.debug(u'カスタムアトリビュート: {}, {}'.format(attr, attr_type))
                if attr_type in cls.type_at:
                    cmds.addAttr(temp_node, ln=attr, k=True, at=attr_type)
                elif attr_type in cls.type_dt:
                    cmds.addAttr(temp_node, ln=attr, k=True, dt=attr_type)
                else:
                    logger.warning(u'カスタムアトリビュートのタイプが判別できませんでした: {}'.format(attr_type))
            # node1のキーを保存
            cmds.copyKey(node1, time=(':',), float=(':',))
            cmds.pasteKey(temp_node, option='replace')

            if animtype == 1:  # pose
                if copytype == 1:
                    # node1のキーをnode2へコピー
                    cmds.copyKey(node1, time=times)
                    cmds.pasteKey(node2, option='replace')

                else:
                    # node1のキーをnode2へコピー
                    cmds.copyKey(node2, time=times)
                    cmds.pasteKey(node1, option='replace')
                    # node2のキーをnode1へコピー
                    cmds.copyKey(temp_node, time=times)
                    cmds.pasteKey(node2, option='replace')

            else:  # motion
                if copytype == 1:
                    # node1のキーをnode2へコピー
                    cmds.cutKey(node2, clear=True)
                    cmds.copyKey(node1, time=(':',), float=(':',))
                    cmds.pasteKey(node2, option='replace')

                else:
                    # node1のキーをnode2へコピー
                    cmds.cutKey(node1, clear=True)
                    cmds.copyKey(node2, time=(':',), float=(':',))
                    cmds.pasteKey(node1, option='replace')
                    # node2のキーをnode1へコピー
                    cmds.cutKey(node2, clear=True)
                    cmds.copyKey(temp_node, time=(':',), float=(':',))
                    cmds.pasteKey(node2, option='replace')

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error(u'キーの入れ替え失敗: {}, {}'.format(node1, node2))
        finally:
            cmds.delete(temp_node)

    @staticmethod
    def _reset_controller(nodes):
        for node in nodes:
            for attr in ('tx', 'ty', 'tz', 'rx', 'ry', 'rz'):
                if not cmds.attributeQuery(attr, node=node, ex=True):
                    continue
                if cmds.getAttr('{}.{}'.format(node, attr), l=True):
                    continue
                cmds.setAttr('{}.{}'.format(node, attr), 0)

    @staticmethod
    def _get_time_range():
        u"""Time Rangeの取得

        :return: start, end
        """
        range_set = cmds.ls('rangeSet', typ='objectSet')
        if range_set:
            start = cmds.getAttr('rangeSet.startFrame')
            end = cmds.getAttr('rangeSet.endFrame')
        else:
            start = cmds.playbackOptions(q=True, min=True)
            end = cmds.playbackOptions(q=True, max=True)

        return start, end

    # ########################################
    #  Set
    # ########################################
    @classmethod
    def _is_set(cls, node):
        u"""セットか

        :param node: ノード
        :return: bool
        """
        if cmds.ls(node, typ='objectSet'):
            return True
        else:
            return False

    @classmethod
    def _get_nodes_from_selections(cls, selections):
        u"""指定したセット名からノードを取得

        :param set_: セット名
        :return: ノードのリスト
        """
        nodes = []
        for selection in selections:
            if cls._is_set(selection):
                temp_nodes = cmds.sets(selection, q=True)
                temp_nodes = cls._get_nodes_from_selections(temp_nodes)
                if temp_nodes:
                    nodes.extend(temp_nodes)
            else:
                nodes.append(selection)
        return nodes

    @classmethod
    def _classify_nodes(cls, nodes, right_id, left_id):
        u"""指定したノードからセンター、右、左のノードに分類する

        :param nodes: ノードのリスト
        :param right_id: 右側のノードの識別子
        :param left_id: 左側のノードの識別子
        :return: {'center': center_nodes, 'right': right_nodes, 'left': left_nodes}
        """
        center_nodes = []
        right_nodes = []
        left_nodes = []

        for node in nodes:
            if cls._is_id_node(node, right_id):
                if node not in right_nodes:
                    right_nodes.append(node)
                left_node = cls._get_mirror_node(node, right_id, left_id)
                if left_node not in left_nodes:
                    left_nodes.append(left_node)
            elif cls._is_id_node(node, left_id):
                if node not in left_nodes:
                    left_nodes.append(node)
                right_node = cls._get_mirror_node(node, right_id, left_id)
                if right_node not in right_nodes:
                    right_nodes.append(right_node)
            else:
                if node.find(WORLD_OFFSET) == -1:
                    center_nodes.append(node)

        return {'center': center_nodes, 'right': right_nodes, 'left': left_nodes}

    # ########################################
    #  Exec
    # ########################################
    @classmethod
    def main(cls, nodes_or_sets, **kwargs):
        u"""反転実行用関数

        :param nodes_or_sets: ノードまたはセット (文字列、リストどちらでも可)

        :param right_id: 右側のノードの識別子
        :param left_id: 左側のノードの識別子
        :param animtype: 1: ポーズ, 2: モーション
        :param copytype: 1: ミラーコピー, 2 ミラー反転
        :param function: 1 local, 2 worldOffsetのみ, 3, local反転後、worldoffset反転
        :param axis: 反転の基準軸 'x', 'y', 'z'
        :param l_to_r: LeftノードがソースでRightノードがターゲットか (boolでFalseの場合は逆の処理)
        :param bakes: bakeするか
        """
        right_id = kwargs.setdefault('right_id', 'R_')
        left_id = kwargs.setdefault('left_id', 'L_')
        animtype = kwargs.setdefault('animtype', 1)
        copytype = kwargs.setdefault('copytype', 2)
        function = kwargs.setdefault('function', 1)
        axis = kwargs.setdefault('axis', 'x')
        l_to_r = kwargs.setdefault('l_to_r', True)
        bakes = kwargs.setdefault('bake', False)

        negative_objects = kwargs.setdefault('negative_objects', list())
        negative_attrs = kwargs.setdefault('negative_attrs', list())

        # auto keyかどうかチェック
        state = cmds.autoKeyframe(q=True, st=True)
        cmds.autoKeyframe(st=False)
        # 現在のtimeの記憶
        current = cmds.currentTime(q=True)

        nodes = cls._get_nodes_from_selections(nodes_or_sets)
        world_offset = cls._get_world_offset(nodes)

        # アニメーションのBake
        # poseの場合はbakeのフラグに関わらず必ずベイク
        if animtype == 1 or bakes:
            Bake.main(nodes, hierarchy='none')

        # local
        # if typ == 'local' or typ == 'both':
        if function == 1 or function == 3:
            logger.debug('reverse: local')

            # worldOffsetのリセット
            if world_offset:
                pos = cmds.getAttr('{}.t'.format(world_offset))[0]
                rot = cmds.getAttr('{}.r'.format(world_offset))[0]

                cmds.mute('{}.t'.format(world_offset))
                cmds.mute('{}.r'.format(world_offset))

                cmds.setAttr('{}.t'.format(world_offset), 0, 0, 0)
                cmds.setAttr('{}.r'.format(world_offset), 0, 0, 0)

            classified_nodes = cls._classify_nodes(nodes, right_id, left_id)
            center_nodes = classified_nodes['center']
            right_nodes = classified_nodes['right']
            left_nodes = classified_nodes['left']
            nodes = center_nodes + right_nodes + left_nodes

            node_axis = {}
            node_behavior = {}
            cls._reset_controller(nodes)

            for node in nodes:
                local_axis = cls._get_local_axis(node)
                node_axis[node] = local_axis['primary_axis']
                node_behavior[node] = cls._is_behavior(node, right_id, left_id)

            # mirror
            if copytype == 1:
                # 右、左のノードのミラー
                for right, left in zip(right_nodes, left_nodes):
                    if l_to_r:
                        cls._copy_animation(left, right, animtype=animtype, copytype=copytype, time=current)
                        cls._reverse(right,
                                     node_axis[right],
                                     animtype,
                                     copytype=copytype,
                                     time=current,
                                     is_behavior=node_behavior[right],
                                     negative_objects=negative_objects,
                                     negative_attrs=negative_attrs)
                    else:
                        cls._copy_animation(right, left, animtype=animtype, copytype=copytype, time=current)
                        cls._reverse(left,
                                     node_axis[left],
                                     animtype,
                                     copytype=copytype,
                                     time=current,
                                     is_behavior=node_behavior[left],
                                     negative_objects=negative_objects,
                                     negative_attrs=negative_attrs)

            # reverse
            else:
                # センターノードの反転
                for node in center_nodes:
                    cls._reverse(node,
                                 node_axis[node],
                                 animtype,
                                 time=current,
                                 negative_objects=negative_objects,
                                 negative_attrs=negative_attrs)

                # 右、左のノードの反転
                for right, left in zip(right_nodes, left_nodes):
                    cls._copy_animation(right, left, animtype=animtype, copytype=copytype, time=current)
                    if not node_behavior[right]:
                        cls._reverse(right, node_axis[right], animtype, copytype=copytype, time=current, negative_objects=negative_objects, negative_attrs=negative_attrs)
                        cls._reverse(left, node_axis[left], animtype, copytype=copytype, time=current, negative_objects=negative_objects, negative_attrs=negative_attrs)
                    else:
                        logger.info('skipped reverse: {}, {}'.format(right, left))

            if world_offset:
                cmds.mute('{}.t'.format(world_offset), d=True, f=True)
                cmds.mute('{}.r'.format(world_offset), d=True, f=True)

                cmds.setAttr('{}.t'.format(world_offset), *pos)
                cmds.setAttr('{}.r'.format(world_offset), *rot)

            # if typ == 'both':
            if function == 3:
                logger.debug('reverse: world')
                if world_offset:
                    cls._reverse_world_offset(world_offset, axis, animtype, time=current)

        # worldOffset
        else:
            logger.debug('reverse: world')
            if world_offset:
                cls._reverse_world_offset(world_offset, axis, animtype, time=current)

        cmds.currentTime(current)
        cmds.autoKeyframe(st=state)
    # ########################################
    #  Debug
    # ########################################
    @classmethod
    def debug_reset_controller(cls, *args, **kwargs):
        u"""コントローラーのリセット"""
        selections = cmds.ls(sl=True, typ='objectSet')
        if not selections:
            return

        # ctrl_set = selections[0]
        # nodes = cls._get_nodes_from_selections(ctrl_set)
        nodes = cls._get_nodes_from_selections(selections)

        # auto keyかどうかチェック
        state = cmds.autoKeyframe(q=True, st=True)
        cmds.autoKeyframe(st=False)
        cls._reset_controller(nodes)
        cmds.autoKeyframe(st=state)

    @classmethod
    def debug_show_info(cls, *args, **kwargs):
        u"""ScriptEditorにコントローラーの情報を表示

        :param kwargs: 'mode' 0: Both, 1: behavior, 2: orientation
        """
        # コントローラーの取得

        # 0: Both, 1: behavior, 2: orientation
        mode = kwargs.setdefault('mode', 0)
        displays_left_only = kwargs.setdefault('displays_left_only', False)

        selections = cmds.ls(sl=True, typ='objectSet')
        if not selections:
            return

        ctrl_set = selections[0]
        right_id = 'L_'
        left_id = 'R_'

        # nodes = cls._get_nodes_from_selections(ctrl_set)
        nodes = cls._get_nodes_from_selections([ctrl_set])
        nodes.sort()
        info = u'\n{:^35s} {:^6s} {:^6s} {:^7s} {:^30s} {:^30s}\n'.format(
            'node', 'p_axis', 's_axis', 'behavior', 'p_v', 's_v',
        )
        info += u'{:-<35s} {:-<6s} {:-<6s} {:-<7s} {:-<30s} {:-<30s}\n'.format('', '', '', '', '', '')

        cls.debug_reset_controller()
        for node in nodes:
            if displays_left_only and (not cls._is_id_node(node, right_id) or cls._is_id_node(node, left_id)):
                continue

            is_behavior = cls._is_behavior(node, right_id, left_id)
            if (mode == 1 and not is_behavior) or (mode == 2 and is_behavior):
                continue

            local_axis = cls._get_local_axis(node)
            primary_axis = local_axis['primary_axis']
            secondary_axis = local_axis['secondary_axis']

            primary_vector = local_axis['primary_vector']
            secondary_vector = local_axis['secondary_vector']

            info += u'{:35s} {:6s} {:6s} {:7} {:30s} {:30s}\n'.format(
                node, primary_axis, secondary_axis, is_behavior, primary_vector, secondary_vector,
            )

        logger.info(info)


class ReverseMotion(object):

    def __init__(self, *args, **kwargs):
        u"""初期化"""
        self.window = self.__class__.__name__
        self.close()

        self.main_layout = None

        self.ui = None
        self.url = 'https://wisdom2.cygames.jp/pages/viewpage.action?pageId=30421204'

        self._tool_name = 'mirrormotion'
        self.title = 'MirrorMotion'

        self._animtype_key = '{}.animtype'.format(__package__)
        self._animtype_control = None

        self._copytype_key = '{}.copytype'.format(__package__)
        self._copytype_control = None

        self._l_to_r_key = '{}.l_to_r'.format(__package__)
        self._l_to_r_control = None
        self._num_l_to_r = {1: True, 2: False}

        self._left_id_key = '{}.left_id'.format(__package__)
        self._left_id_control = None

        self._right_id_key = '{}.right_id'.format(__package__)
        self._right_id_control = None

        self._bakes_key = '{}.bakes'.format(__package__)
        self._bakes_control = None

        self._function_key = '{}.function'.format(__package__)
        self._function_control = None

        self._axis_key = '{}.axis'.format(__package__)
        self._axis_control = None
        self._num_axis = {1: 'x', 2: 'y', 3: 'z'}

        self._negative_objects_key = '{}.negative_objects'.format(__package__)
        self._negative_attrs_key = '{}.negative_attrs'.format(__package__)

        self.width = 540
        self.height = 360

    def _initialize_window(self):
        u"""Windowの初期化"""
        if not cmds.window(self.window, ex=True):
            self.window = cmds.window(self.window, mb=True)

    def _add_baselayout(self):
        u"""基本レイアウトの追加"""
        # メニューバー
        self._add_editmenu()
        self._add_helpmenu()
        self._add_debugmenu()

        mainform = cmds.formLayout(nd=100)
        maintab = cmds.tabLayout(tv=False, scr=True, cr=True, h=1)
        self.main_layout = cmds.columnLayout(adj=1)
        # レイアウト作成 ====
        self._create()
        # ====
        cmds.setParent(mainform)

        execform = self._add_execform()
        cmds.formLayout(
            mainform, e=True,
            af=(
                [maintab, 'top', 0],
                [maintab, 'left', 2],
                [maintab, 'right', 2],
                [execform, 'left', 2],
                [execform, 'right', 2],
                [execform, 'bottom', 0],
            ),
            ac=(
                [maintab, 'bottom', 5, execform],
            ),
        )
        cmds.setParent(self.main_layout)

    def _create(self):
        u"""Windowのレイアウト作成"""
        form = cmds.formLayout()
        column = cmds.columnLayout(adj=1)
        cmds.frameLayout(l='Basic Options', mh=5)
        # animtype
        self._animtype_control = cmds.radioButtonGrp(
            l='Anim Type:', la2=('Pose', 'Motion'),
            cw3=(80, 150, 150), nrb=2, sl=1,
            cc=self._animtype_control_command,
        )
        # copytype
        self._copytype_control = cmds.radioButtonGrp(
            # la2=('Mirror', 'Reverse'), ラベル名をアニメーター要望に合わせて変更
            # コマンド側の名称は時間の都合で昔のまま
            l='Copy Type:', la2=('Copy', 'Mirror'),
            cw3=(80, 150, 150), nrb=2, sl=1,
            cc=self._copytype_control_command,
        )
        # l_tor_r
        self._l_to_r_control = cmds.radioButtonGrp(
            l='', la2=('L -> R', 'R -> L'),
            cw3=(80, 150, 150), nrb=2, sl=1,
            cc=self._save_settings,
        )

        # ID
        cmds.rowLayout(
            adj=5, nc=5,
            cat=[(1, 'right', 0), (2, 'left', 0), (3, 'right', 0), (4, 'left', 0)],
            cw=((1, 80), (2, 70), (3, 80), (4, 70)),
        )
        # left_id
        cmds.text(l='Left ID:')
        self._left_id_control = cmds.textField(tx='L_', cc=self._save_settings)
        cmds.text(l='Right ID:')
        self._right_id_control = cmds.textField(tx='R_', cc=self._save_settings)
        cmds.text(l='')  # スペーサー
        cmds.setParent('..')  # rowLayout

        # Negative Objects
        cmds.rowLayout(
            adj=5, nc=5,
            cat=[(1, 'right', 0), (2, 'left', 0), (3, 'right', 0), (4, 'left', 0)],
            cw=((1, 80), (2, 70), (3, 80), (4, 70)),
        )
        cmds.text(l='Neg Objects:')
        self._negative_objects = cmds.textField(tx='Thumb, Index, Middle, Ring, Pinky', cc=self._save_settings, w=400)
        cmds.text(l='')  # スペーサー
        cmds.setParent('..')  # rowLayout

        # Negative Objects
        cmds.rowLayout(
            adj=8, nc=8,
            cat=[(1, 'right', 0)],
            cw=((1, 80)),
        )
        cmds.text(l='Neg Attrs:')
        self._negative_attrs_tx = cmds.checkBox(l='tx', cc=self._save_settings)
        self._negative_attrs_ty = cmds.checkBox(l='ty', cc=self._save_settings)
        self._negative_attrs_tz = cmds.checkBox(l='tz', cc=self._save_settings)
        self._negative_attrs_rx = cmds.checkBox(l='rx', cc=self._save_settings)
        self._negative_attrs_ry = cmds.checkBox(l='ry', cc=self._save_settings)
        self._negative_attrs_rz = cmds.checkBox(l='rz', cc=self._save_settings)
        cmds.text(l='')  # スペーサー
        cmds.setParent('..')  # rowLayout

        cmds.setParent('..')  # frame

        cmds.frameLayout(l='Extra Options', mh=5)
        # function
        self._function_control = cmds.radioButtonGrp(
            l='Function:', la3=('Local', 'WorldOffset Only', 'Local && WorldOffset'),
            cw4=(80, 150, 150, 150), nrb=3, sl=1,
            cc=self._function_control_command,
        )
        # axis
        self._axis_control = cmds.radioButtonGrp(
            l='Axis:', la3=('X (YZ)', 'Y (XZ)', 'Z (XY)'),
            cw4=(80, 150, 150, 150), nrb=3, sl=1,
            cc=self._save_settings,
        )
        self._bakes_control = cmds.checkBoxGrp(l='Bakes:', v1=False, cw2=(80, 150), cc=self._save_settings)
        cmds.setParent('..')

        cmds.setParent('..')  # column
        cmds.formLayout(
            form, e=True,
            af=(
                [column, 'top', 10],
                [column, 'left', 0],
                [column, 'bottom', 50],
            ),
        )
        cmds.setParent('..')  # form

    def _boot_event(self):
        self._animtype_control_command()
        self._copytype_control_command()
        self._function_control_command()

    def _animtype_control_command(self, *args):
        if cmds.radioButtonGrp(self._animtype_control, q=True, sl=True) == 2:
            cmds.checkBoxGrp(self._bakes_control, e=True, en=True)
        else:
            cmds.checkBoxGrp(self._bakes_control, e=True, en=False)
        self._save_settings()

    def _copytype_control_command(self, *args):
        if cmds.radioButtonGrp(self._copytype_control, q=True, sl=True) == 1:
            cmds.radioButtonGrp(self._l_to_r_control, e=True, en=True)
        else:
            cmds.radioButtonGrp(self._l_to_r_control, e=True, en=False)
        self._save_settings()

    def _function_control_command(self, *args):
        if cmds.radioButtonGrp(self._function_control, q=True, sl=True) == 1:
            cmds.radioButtonGrp(self._axis_control, e=True, en=False)
        else:
            cmds.radioButtonGrp(self._axis_control, e=True, en=True)
        self._save_settings()

    def _add_execform(self):
        u"""Apply Closeボタンの追加

        :return: フォーム名
        """
        execform = cmds.formLayout(nd=100)
        # ボタン
        apply_close_btn = cmds.button(l='Apply and Close', h=26, c=self._apply_close)
        apply_btn = cmds.button(l='Apply', h=26, c=self._apply)
        close_btn = cmds.button(l='Close', h=26, c=self.close)
        # レイアウト
        cmds.formLayout(
            execform, e=True,
            af=(
                [apply_close_btn, 'left', 0],
                [apply_close_btn, 'bottom', 5],
                [apply_btn, 'bottom', 5],
                [close_btn, 'bottom', 5],
                [close_btn, 'right', 0],
            ),
            ap=(
                [apply_close_btn, 'right', 1, 33],
                [close_btn, 'left', 0, 67],
            ),
            ac=(
                [apply_btn, 'left', 4, apply_close_btn],
                [apply_btn, 'right', 4, close_btn],
            ),
        )
        cmds.setParent('..')
        return execform

    def _help(self, *args):
        u"""help表示"""
        cmds.showHelp(self.url, a=True)

    def _add_editmenu(self):
        u"""menu「Edit」を追加"""
        cmds.menu(l='Edit')
        cmds.menuItem(l='Save Settings', c=self._save_settings)
        cmds.menuItem(l='Reset Settings', c=self._reset_settings)

    def _add_helpmenu(self):
        u"""menu「Help」を追加"""
        cmds.menu(l='Help')
        cmds.menuItem(l='Help on {0}'.format(self.title), c=self._help)

    def _add_debugmenu(self):
        u"""メニューアイテムを追加"""
        cmds.menu(l='Debug', to=True)
        cmds.menuItem(l=u'コントローラーのリセット', c=ReverseMotionCmd.debug_reset_controller)
        cmds.menuItem(l=u'コントローラーの情報を表示', c=ReverseMotionCmd.debug_show_info)
        cmds.menuItem(l=u'コントローラーの情報を表示(behaviorのみ)', c=partial(ReverseMotionCmd.debug_show_info, mode=1))
        cmds.menuItem(
            l=u'コントローラーの情報を表示(leftノードのみ)',
            c=partial(ReverseMotionCmd.debug_show_info, displays_left_only=True),
        )
        cmds.menuItem(
            l=u'コントローラーの情報を表示(behavior, leftノードのみ)',
            c=partial(ReverseMotionCmd.debug_show_info, mode=1, displays_left_only=True),
        )

    def _read_settings(self, *args):
        u"""設定の読み込み"""
        animtype = int(cmds.optionVar(q=self._animtype_key))
        if animtype:
            cmds.radioButtonGrp(self._animtype_control, e=True, sl=animtype)
        l_to_r = int(cmds.optionVar(q=self._copytype_key))
        if l_to_r:
            cmds.radioButtonGrp(self._copytype_control, e=True, sl=l_to_r)
        copytype = int(cmds.optionVar(q=self._copytype_key))
        if copytype:
            cmds.radioButtonGrp(self._copytype_control, e=True, sl=copytype)
        function = int(cmds.optionVar(q=self._function_key))
        if function:
            cmds.radioButtonGrp(self._function_control, e=True, sl=function)
        axis = int(cmds.optionVar(q=self._axis_key))
        if axis:
            cmds.radioButtonGrp(self._axis_control, e=True, sl=axis)
        left_id = cmds.optionVar(q=self._left_id_key)
        if left_id:
            cmds.textField(self._left_id_control, e=True, tx=left_id)
        right_id = cmds.optionVar(q=self._right_id_key)
        if right_id:
            cmds.textField(self._right_id_control, e=True, tx=right_id)
        bakes = strtobool(str(cmds.optionVar(q=self._bakes_key)))
        if bakes:
            cmds.checkBoxGrp(self._bakes_control, e=True, v1=True)
        else:
            cmds.checkBoxGrp(self._bakes_control, e=True, v1=False)

        try:
            negative_objects = eval(cmds.optionVar(q=self._negative_objects_key))
            if negative_objects:
                text_negative_objects = ','.join(negative_objects)
                cmds.textField(self._negative_objects, e=True, tx=text_negative_objects)

            negative_attrs = eval(cmds.optionVar(q=self._negative_attrs_key))
            if negative_attrs:
                if negative_attrs[0]:
                    cmds.checkBox(self._negative_attrs_tx, e=True, v=True)
                if negative_attrs[1]:
                    cmds.checkBox(self._negative_attrs_ty, e=True, v=True)
                if negative_attrs[2]:
                    cmds.checkBox(self._negative_attrs_tz, e=True, v=True)
                if negative_attrs[3]:
                    cmds.checkBox(self._negative_attrs_rx, e=True, v=True)
                if negative_attrs[4]:
                    cmds.checkBox(self._negative_attrs_ry, e=True, v=True)
                if negative_attrs[5]:
                    cmds.checkBox(self._negative_attrs_rz, e=True, v=True)

        except:
            print(traceback.format_exc())

    def get_negative_object_values(self):
        _negative_objects = cmds.textField(self._negative_objects, q=True, tx=True)
        _neg_tx = cmds.checkBox(self._negative_attrs_tx, q=True, v=True)
        _neg_ty = cmds.checkBox(self._negative_attrs_ty, q=True, v=True)
        _neg_tz = cmds.checkBox(self._negative_attrs_tz, q=True, v=True)
        _neg_rx = cmds.checkBox(self._negative_attrs_rx, q=True, v=True)
        _neg_ry = cmds.checkBox(self._negative_attrs_ry, q=True, v=True)
        _neg_rz = cmds.checkBox(self._negative_attrs_rz, q=True, v=True)

        _negative_objects = [ng_ob.replace(' ', '') for ng_ob in _negative_objects.split(',')]

        return _negative_objects, [_neg_tx, _neg_ty, _neg_tz, _neg_rx, _neg_ry, _neg_rz]

    def _save_settings(self, *args):
        u"""設定の保存

        :return: 設定 (dict)
        """

        neg_objects, neg_attrs = self.get_negative_object_values()

        settings = {
            self._animtype_key: cmds.radioButtonGrp(self._animtype_control, q=True, sl=True),
            self._copytype_key: cmds.radioButtonGrp(self._copytype_control, q=True, sl=True),
            self._l_to_r_key: cmds.radioButtonGrp(self._l_to_r_control, q=True, sl=True),
            self._function_key: cmds.radioButtonGrp(self._function_control, q=True, sl=True),
            self._axis_key: cmds.radioButtonGrp(self._axis_control, q=True, sl=True),
            self._left_id_key: cmds.textField(self._left_id_control, q=True, tx=True),
            self._right_id_key: cmds.textField(self._right_id_control, q=True, tx=True),
            self._bakes_key: cmds.checkBoxGrp(self._bakes_control, q=True, v1=True),

            self._negative_objects_key: neg_objects,
            self._negative_attrs_key: neg_attrs,
        }

        # print('Save Settings: ', settings)

        # mayaPrefs.melに保存
        [cmds.optionVar(sv=(k, str(v))) for k, v in settings.items()]
        logger.debug(settings)
        return settings

    def _reset_settings(self, *args):
        u"""設定のリセット"""
        cmds.radioButtonGrp(self._animtype_control, e=True, sl=1)
        cmds.radioButtonGrp(self._copytype_control, e=True, sl=1)
        cmds.radioButtonGrp(self._l_to_r_control, e=True, sl=1)
        cmds.radioButtonGrp(self._function_control, e=True, sl=1)
        cmds.radioButtonGrp(self._axis_control, e=True, sl=1)
        cmds.textField(self._left_id_control, e=True, tx='_L_')
        cmds.textField(self._right_id_control, e=True, tx='_R_')

        cmds.textField(self._negative_objects, e=True, tx='Thumb, Index, Middle, Ring, Pinky')

        cmds.checkBox(self._negative_attrs_tx, e=True, v=True)
        cmds.checkBox(self._negative_attrs_ty, e=True, v=False)
        cmds.checkBox(self._negative_attrs_tz, e=True, v=False)
        cmds.checkBox(self._negative_attrs_rx, e=True, v=False)
        cmds.checkBox(self._negative_attrs_ry, e=True, v=True)
        cmds.checkBox(self._negative_attrs_rz, e=True, v=True)

        # リセット後に設定を保存
        self._save_settings()
        self._boot_event()

    def _apply(self, *args):
        u"""「現在のシーンを反転」ボタンのコマンド"""
        settings = self._save_settings()
        settings[self._l_to_r_key] = self._num_l_to_r[settings[self._l_to_r_key]]
        settings[self._axis_key] = self._num_axis[settings[self._axis_key]]
        settings = {re.sub('{}.'.format(__package__), '', k): v for k, v in settings.items()}

        logger.debug('Option')
        for k, v in settings.items():
            logger.debug('{}: {}'.format(k, v))

        selections = cmds.ls(sl=True)
        ReverseMotionCmd.main(selections, **settings)
        cmds.select(selections, ne=True)

    def _apply_close(self, *args):
        u"""ApplyCloseボタンの実行コマンド"""
        self._apply()
        self.close()

    def show(self, *args):
        u"""Windowの表示"""
        self._initialize_window()
        self._add_baselayout()

        self._read_settings()
        self._boot_event()

        cmds.showWindow(self.window)
        cmds.window(self.window, e=True, t=self.title, wh=(self.width, self.height))

    def close(self, *args):
        u"""Windowのclose"""
        if cmds.window(self.window, ex=True):
            cmds.deleteUI(self.window)

if __name__ == '__main__':
    mirror_tool = ReverseMotion()
    mirror_tool.show()
