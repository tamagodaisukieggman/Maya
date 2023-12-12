# -*- coding: utf-8 -*-
u"""Bake Simulation"""
import re

import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.OpenMaya as om_old
import maya.OpenMayaAnim as oma_old

import logging
# from mtku.maya.mtklog import MtkLog
from mtk.utils.decoration import suspend
from mtk.utils.decoration import keep_selections
from mtk.utils.decoration import timer


# logger = MtkLog(__name__)
logger = logging.getLogger(__name__)


class BakeSimulation(object):

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
            om.MFn.kAimConstraint,
            om.MFn.kConstraint,
            om.MFn.kDynamicConstraint,
            om.MFn.kGeometryConstraint,
            om.MFn.kHairConstraint,
            om.MFn.kNormalConstraint,
            om.MFn.kOldGeometryConstraint,
            om.MFn.kOrientConstraint,
            om.MFn.kParentConstraint,
            om.MFn.kPluginConstraintNode,
            om.MFn.kPointConstraint,
            om.MFn.kPointOnPolyConstraint,
            om.MFn.kPoleVectorConstraint,
            om.MFn.kRigidConstraint,
            om.MFn.kScaleConstraint,
            om.MFn.kSymmetryConstraint,
            om.MFn.kTangentConstraint,
        )

        sel = om.MGlobal.getSelectionListByName(node)
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
            connections = cmds.listConnections(
                '{}.{}'.format(node, attr), s=True, d=False, p=True,
            )
            if not connections:
                continue

            for connection in connections:
                connect_node = connection.split('.')[0]
                if cls._is_constraint(connect_node):
                    cmds.disconnectAttr(connection, '{}.{}'.format(node, attr))

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
        e = om.MEulerRotation(*rotate, order=order)
        q = e.asQuaternion()
        qua = om.MQuaternion(q)
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
        time_array = om_old.MTimeArray()
        [time_array.append(om_old.MTime(i, om_old.MTime.uiUnit())) for i in range(start, end + 1)]

        results = {
            'node': {node: {} for node in nodes},
            'time': time_array,
        }
        node_transform = {}

        selection_list = om.MSelectionList()
        [selection_list.add(node) for node in nodes]
        iter_ = om.MItSelectionList(selection_list)

        # attributeと型の取得
        while not iter_.isDone():
            dagpath = iter_.getDagPath()
            mobject = dagpath.node()
            dependency_node = om.MFnDependencyNode(mobject)
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
                plug = om.MPlug(mobject, dependency_node.attribute(i))
                attr = plug.info.split('.')[-1]

                if attr in keyable_attrs:
                    attrs[attr] = {
                        'plug': plug,
                        'type': cmds.getAttr('{}.{}'.format(name, attr), typ=True),
                        'values': om_old.MDoubleArray(),
                    }

            iter_.next()
        iter_.reset()

        # フレームごとの値をdataFrameに格納
        for i in range(start, end + 1, 1):
            oma.MAnimControl.setCurrentTime(om.MTime(i, om.MTime.uiUnit()))
            while not iter_.isDone():
                dagpath = iter_.getDagPath()
                name = dagpath.partialPathName()
                attr_items = results['node'][name]

                if node_transform[name]:
                    mfn_transform = om.MFnTransform(dagpath)
                    r = mfn_transform.rotation(om.MSpace.kTransform, False)
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

        connection_lists = om.MSelectionList()
        [connection_lists.add(connection) for connection in connections]
        iter_ = om.MItSelectionList(connection_lists, om.MFn.kAnimCurve)
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

                curve_selection = om_old.MSelectionList()
                om_old.MGlobal.getSelectionListByName(anim_curve, curve_selection)
                mobj = om_old.MObject()
                curve_selection.getDependNode(0, mobj)
                anim_curve_fn = oma_old.MFnAnimCurve(mobj)
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

        logger.debug('Bake Option\nstart: {s} end:{e}\nhierarcy: {h}\nattrs: {a}'.format(
            s=start, e=end, h=hierarchy, a=attrs,
        ))

        nodes = cmds.ls(root_nodes, dag=True) if hierarchy == 'below' else cmds.ls(root_nodes)
        nodes = [node for node in nodes if not cls._is_constraint(node) and cmds.listAnimatable(node)]

        current = cmds.currentTime(q=True)
        cls._set_keys(nodes, start, end, attrs=attrs, euler_filter=euler_filter)
        # 最初のフレームにリセット
        oma.MAnimControl.setCurrentTime(om.MTime(current, om.MTime.uiUnit()))

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

        # evaluation = cmds.evaluationManager(q=True, m=True)[0]
        # cmds.evaluationManager(m='parallel')
        #
        # start = int(kwargs.setdefault('start', cmds.playbackOptions(q=True, min=True)))
        # end = int(kwargs.setdefault('end', cmds.playbackOptions(q=True, max=True)))
        # hierarchy = kwargs.setdefault('hierarchy', 'below')
        # attrs = kwargs.setdefault('attrs', None)
        #
        # nodes = cmds.ls(root_nodes, dag=True) if hierarchy == 'below' else cmds.ls(root_nodes)
        # nodes = [node for node in nodes if not cls._is_constraint(node) and cmds.listAnimatable(node)]
        #
        # if attrs:
        #     cmds.bakeResults(nodes, t=(start, end), sm=True, hierarchy='none', at=attrs)
        # else:
        #     cmds.bakeResults(nodes,  t=(start, end), sm=True, hierarchy='none')
        #
        # for node in nodes:
        #     # コンストレインの削除
        #     cls._disconnect_constraint(node)
        #     cls._delete_attrs(node)
        #
        # cmds.delete(nodes, sc=True, tac=True)
        #
        # if attrs:
        #     cmds.setKeyframe(nodes, t=(start,), attribute=attrs)
        # else:
        #     cmds.setKeyframe(nodes, t=(start, ))
        #
        # curves = cls._get_double_angle_curves(nodes)
        # if curves:
        #     cmds.filterCurve(curves)
        #
        # cmds.evaluationManager(m=evaluation)

    @classmethod
    @timer
    def main(cls, root_nodes, **kwargs):
        autokey_stat = cmds.autoKeyframe(q=True, st=True)
        cmds.autoKeyframe(st=False)

        current_time = cmds.currentTime(q=True)
        cmds.currentTime(current_time)

        if int(cmds.about(v=True)) < 2018:
            logger.debug('Bake Mode: Maya2015')
            cls.main2015(root_nodes, **kwargs)
        else:
            logger.debug('Bake Mode: Maya2018')
            cls.main2018(root_nodes, **kwargs)

        cmds.currentTime(current_time)
        cmds.autoKeyframe(st=autokey_stat)

    @classmethod
    @suspend
    def bake(cls, root_nodes, **kwargs):
        u"""廃止"""
        logger.debug(u'BakeSimulation.bake: この関数は廃止となりました。次の関数を使用してください: BakeSimulation.main')
        cls.main(root_nodes, **kwargs)

    @classmethod
    @suspend
    def filter(cls, root_nodes, **kwargs):
        u"""廃止"""
        logger.debug(u'BakeSimulation.filter: この関数は廃止となりました。次の関数を使用してください: BakeSimulation.main')
        cls.main(root_nodes, **kwargs)


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


# def _is_ntsc():
#     u"""作業中のシーンのTime設定が30fpsがどうか
#
#     :return: bool
#     """
#     current_unit = cmds.currentUnit(q=True, time=True)
#     if not current_unit == 'ntsc':
#         return False
#
#     return True


@keep_selections
def main():
    u"""Animation > ベイクアニメーション"""

    # # Time設定のチェック (30fpsでなかったら警告ダイアログを出して終了)
    # if not _is_ntsc():
    #     cmds.confirmDialog(
    #         title=u'Time設定の警告',
    #         message=u'Working UnitsのTime設定を NTSC (30fps) に変更してください',
    #         button=['OK'],
    #         defaultButton='OK'
    #     )
    #     return

    nodes = _get_selections()
    if not nodes:
        logger.warning(u'ノードを選択してください')
        return

    BakeSimulation.main(nodes, hierarchy='none', euler_filter=True)
