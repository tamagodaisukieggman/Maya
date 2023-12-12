# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import re

import maya.cmds as cmds

from mtk.animation.animstore import lib_maya
from ..bakesimulation import BakeSimulation


class CharaAsset(object):
    """
    """

    def __init__(self, namespace=':'):
        self._namespace = namespace or ':'
        self._root_jt = ''
        self._hip_jt = ''
        self._move_ctrl = ''
        self._hip_ctrl = ''
        self._aim_target = ''
        self._model = ''

    # model
    def get_model(self, **kwargs):
        namespace = kwargs.get('namespace', self._namespace) or ':'
        return re.sub(':+', ':', '{}:{}'.format(
            self.get_chara_namespace(namespace=namespace), self._model))

    model = property(get_model)

    # bindJt
    def get_root_jt(self, **kwargs):
        namespace = kwargs.get('namespace', self._namespace) or ':'
        return re.sub(':+', ':', '{}:{}'.format(
            self.get_chara_namespace(namespace=namespace), self._root_jt))

    root_jt = property(get_root_jt)

    def get_hip_jt(self, **kwargs):
        namespace = kwargs.get('namespace', self._namespace) or ':'
        return re.sub(':+', ':', '{}:{}'.format(
            self.get_chara_namespace(namespace=namespace), self._hip_jt))

    hip_jt = property(get_hip_jt)

    # ctrl
    def get_move_ctrl(self, **kwargs):
        namespace = kwargs.get('namespace', self._namespace) or ':'
        return re.sub(':+', ':', '{}:{}'.format(namespace, self._move_ctrl))

    move_ctrl = property(get_move_ctrl)

    def get_hip_ctrl(self, **kwargs):
        namespace = kwargs.get('namespace', self._namespace) or ':'
        return re.sub(':+', ':', '{}:{}'.format(namespace, self._hip_ctrl))

    hip_ctrl = property(get_hip_ctrl)

    def get_aim_target(self, **kwargs):
        namespace = kwargs.get('namespace', self._namespace) or ':'
        return re.sub(':+', ':', '{}:{}'.format(namespace, self._aim_target))

    aim_target = property(get_aim_target)

    def get_chara_namespace(self, **kwargs):
        namespace = kwargs.get('namespace', self._namespace) or ':'
        namespaces = lib_maya.list_namespaces(namespace)
        return namespaces[0] if namespaces else ':'


class PLYAsset(CharaAsset):
    """plyアセット ノード名定義
    """

    def __init__(self, namespace=':'):
        self._namespace = namespace or ':'
        self._root_jt = 'rootBindJt'
        self._hip_jt = 'hipBindJt'
        self._move_ctrl = 'moveCtrl'
        self._hip_ctrl = 'hip_Ctrl'
        self._aim_target = 'headAimerXYPosLoc'
        self._model = 'model'


class MSTAsset(CharaAsset):
    """mstアセット ノード名定義
    """

    def __init__(self, namespace=':'):
        self._namespace = namespace or ':'
        self._root_jt = 'j00_root_bindJt'
        self._hip_jt = 'j01_hip_bindJt'
        self._move_ctrl = 'moveCtrl'
        self._hip_ctrl = 'hip_Ctrl'
        self._aim_target = 'headAimerXYPosLoc'
        self._model = 'model'


class DRGAsset(CharaAsset):
    """drgアセット ノード名定義
    """

    def __init__(self, namespace=':'):
        self._namespace = namespace or ':'
        self._root_jt = 'root'
        self._hip_jt = 'hip'
        self._move_ctrl = 'moveCtrl'
        self._hip_ctrl = 'hipCtrl'
        self._aim_target = 'headAimerXYPosLoc'
        self._model = 'model'


def get_asset_definition(namespace):
    """ノード名の定義帯を取得

    :param str namespace: アセットネームスペース
    :return: ノード名定義オブジェクト
    :rtype: CharaAsset
    """

    namespace = namespace or ':'

    if namespace == ':':
        return PLYAsset(namespace)

    elif 'ply' in namespace:
        return PLYAsset(namespace)

    elif 'mst' in namespace:
        return MSTAsset(namespace)

    elif 'drg' in namespace:
        return DRGAsset(namespace)

    else:
        return CharaAsset(namespace)


def get_move_ctrl_constraint(namespace=':'):
    """moveCtrlのコンストレインノードを取得
    :param str namespace: rigアセットのネームスペース
    :return: コンストレインノードを辞書で取得
    :rtype: dict
    """

    ret = {
        'aim': None,
        'point': None,
    }

    chara_def = get_asset_definition(namespace)

    move_ctrl = chara_def.move_ctrl
    if not cmds.objExists(move_ctrl):
        return ret

    # aim
    aim_constraint = cmds.listRelatives(move_ctrl, c=True, type='aimConstraint', pa=True)
    if aim_constraint:
        ret['aim'] = aim_constraint[0]

    # point
    point_constraint = cmds.listRelatives(move_ctrl, c=True, type='pointConstraint', pa=True)
    if point_constraint:
        ret['point'] = point_constraint[0]

    return ret


def restore_move_ctrl_constraint(namespace=':', **kwargs):
    """moveCtrlのコンストレインを復元する
    |rigデータ(リファレンス)にコンストレインノードは残っているはずだが、
    |ノードが消えている場合は新規でコンストレインを設定する。

    :param str namespace: rigアセットのネームスペース
    :keyword bool restoreTranslateX: txのコネクションを復元
    :keyword bool restoreTranslateZ: tzのコネクションを復元
    :keyword bool restoreRotateY: ryのコネクションを復元
    """

    restore_tx = kwargs.get('restoreTranslateX', kwargs.get('rtx', True))
    restore_tz = kwargs.get('restoreTranslateZ', kwargs.get('rtz', True))
    restore_ry = kwargs.get('restoreRotateY', kwargs.get('rry', True))

    if not (restore_tx or restore_tz or restore_ry):
        cmds.warning('Invalid restore constraint options.')
        return

    chara_def = get_asset_definition(namespace)

    if not cmds.objExists(chara_def.move_ctrl):
        cmds.warning('{} is not found.'.format(chara_def.move_ctrl))
        return

    constraints = get_move_ctrl_constraint(namespace=namespace)

    if restore_ry:
        # aim
        aim_const = constraints.get('aim', None)
        if aim_const:
            # ry
            s_plug = '{}.constraintRotateY'.format(aim_const)
            d_plug = '{}.rotateY'.format(chara_def.move_ctrl)
            if not cmds.isConnected(s_plug, d_plug):
                cmds.connectAttr(s_plug, d_plug, f=True)
        else:
            # aim_constraintが見つからない場合は新しく作成
            if cmds.objExists(chara_def.aim_target):
                d_plug = '{}.rotateY'.format(chara_def.move_ctrl)
                connects = cmds.listConnections(d_plug, s=True, d=False, c=True, p=True)
                if connects:
                    cmds.disconnectAttr(*connects[::-1])

                cmds.aimConstraint(
                    chara_def.aim_target, chara_def.move_ctrl,
                    offset=[0.0, 0.0, 0.0], weight=1, aimVector=[0.0, 0.0, 1.0],
                    upVector=[0.0, 1.0, 0.0], worldUpType='scene', skip=['x', 'z'])

    if restore_tx or restore_tz:
        # point
        point_const = constraints.get('point', None)
        if point_const:
            if restore_tx:
                # tx
                s_plug = '{}.constraintTranslateX'.format(point_const)
                d_plug = '{}.translateX'.format(chara_def.move_ctrl)
                if not cmds.isConnected(s_plug, d_plug):
                    cmds.connectAttr(s_plug, d_plug, f=True)

            if restore_tz:
                # tz
                s_plug = '{}.constraintTranslateZ'.format(point_const)
                d_plug = '{}.translateZ'.format(chara_def.move_ctrl)
                if not cmds.isConnected(s_plug, d_plug):
                    cmds.connectAttr(s_plug, d_plug, f=True)

        else:
            skip = ['y']
            if restore_tx:
                d_plug = '{}.translateX'.format(chara_def.move_ctrl)
                connects = cmds.listConnections(d_plug, s=True, d=False, c=True, p=True)
                if connects:
                    cmds.disconnectAttr(*connects[::-1])
            else:
                skip.append('x')

            if restore_tz:
                d_plug = '{}.translateZ'.format(chara_def.move_ctrl)
                connects = cmds.listConnections(d_plug, s=True, d=False, c=True, p=True)
                if connects:
                    cmds.disconnectAttr(*connects[::-1])
            else:
                skip.append('z')

            # point_constraintが見つからない場合は新しく作成
            if cmds.objExists(chara_def.hip_ctrl):
                cmds.pointConstraint(
                    chara_def.hip_ctrl, chara_def.move_ctrl, offset=[0.0, 0.0, 0.0], weight=1, skip=skip)


def bake_move_ctrl(namespace=':', **kwargs):
    """moveCtrlをベイク
    :param str namespace: rigアセットのネームスペース
    :keyword bool bakeTranslateX: txをベイク
    :keyword bool bakeTranslateZ: tzをベイク
    :keyword bool bakeRotateY: ryをベイク
    """

    chara_def = get_asset_definition(namespace)

    bake_tx = kwargs.get('bakeTranslateX', kwargs.get('btx', True))
    bake_ty = kwargs.get('bakeTranslateY', kwargs.get('bty', False))
    bake_tz = kwargs.get('bakeTranslateZ', kwargs.get('btz', True))
    bake_ry = kwargs.get('bakeRotateY', kwargs.get('bry', True))

    use_bbox = kwargs.get('useBBox', True)

    if not (bake_tx or bake_tz or bake_ry):
        cmds.warning('Invalid bake options.')
        return

    if not cmds.objExists(chara_def.hip_jt):
        cmds.warning('{} is not found.'.format(chara_def.hip_jt))
        return

    dmy_obj = cmds.createNode('transform', n='move_ctrl', ss=True)

    # translate
    cmds.pointConstraint(chara_def.hip_jt, dmy_obj, offset=[0.0, 0.0, 0.0], weight=1)

    # rotate
    constraints = get_move_ctrl_constraint(namespace=namespace)
    if bake_ry:
        aim_const = constraints.get('aim', None)
        if aim_const:
            s_plug = '{}.constraintRotateY'.format(aim_const)
            d_plug = '{}.rotateY'.format(dmy_obj)
            if not cmds.isConnected(s_plug, d_plug):
                cmds.connectAttr(s_plug, d_plug, f=True)

        else:
            cmds.aimConstraint(
                chara_def.aim_target, dmy_obj,
                offset=[0.0, 0.0, 0.0], weight=1, aimVector=[0.0, 0.0, 1.0],
                upVector=[0.0, 1.0, 0.0], worldUpType='scene', skip=['x', 'z'])

    copy_attrs = []
    if bake_tx:
        copy_attrs.append('tx')

    if bake_ty:
        copy_attrs.append('ty')
        if use_bbox and cmds.objExists(chara_def.model):
            cmds.connectAttr('{}.boundingBoxMinY'.format(chara_def.model), '{}.ty'.format(dmy_obj), f=True)

    if bake_tz:
        copy_attrs.append('tz')

    if bake_ry:
        copy_attrs.append('ry')

    if copy_attrs:
        BakeSimulation.filter([dmy_obj], hierarchy='none')

        for attr in copy_attrs:
            d_plug = '{}.{}'.format(chara_def.move_ctrl, attr)
            connects = cmds.listConnections(d_plug, s=True, d=False, c=True, p=True)
            if connects:
                cmds.disconnectAttr(*connects[::-1])

        cmds.copyKey(dmy_obj, at=copy_attrs, option='curve')
        cmds.pasteKey(chara_def.move_ctrl, option='replaceCompletely', at=copy_attrs)
        cmds.delete(dmy_obj)
