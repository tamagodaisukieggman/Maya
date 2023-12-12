# -*- coding: utf-8 -*-
u"""モーション反転ツール

.. END__CYGAMES_DESCRIPTION
"""

import re
import os
import math
import traceback

import maya.cmds as cmds

import logging
# from mtku.maya.mtklog import MtkLog
from mtk.animation.bakesimulation import BakeSimulation
from mtk.utils import getCurrentSceneFilePath


CTRL_SET = 'ctrlSet'
WORLD_OFFSET = 'worldOffset'


# logger = MtkLog(__name__)
logger = logging.getLogger(__name__)


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

    # ########################################
    #  Math
    # ########################################
    @staticmethod
    def _cos(degrees):
        u"""cos

        :param degrees: degrees
        :return: cos
        """
        return round(math.cos(math.radians(degrees)), 3)

    @staticmethod
    def _sin(degrees):
        u"""sin

        :param degrees: degrees
        :return: sin
        """
        return round(math.sin(math.radians(degrees)), 3)

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
        order = cmds.getAttr('{}.rotateOrder'.format(node))
        x, y, z = cmds.xform(node, q=True, ws=True, ro=True)
        x = cls._conv_degrees(x)
        y = cls._conv_degrees(y)
        z = cls._conv_degrees(z)
        rx = [
            [1, 0, 0],
            [0, cls._cos(x), cls._sin(x)],
            [0, -1 * cls._sin(x), cls._cos(x)],
        ]
        ry = [
            [cls._cos(y), 0, -1 * cls._sin(y)],
            [0, 1, 0],
            [cls._sin(y), 0, cls._cos(y)],
        ]
        rz = [
            [cls._cos(z), cls._sin(z), 0],
            [-1 * cls._sin(z), cls._cos(z), 0],
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

    @staticmethod
    def _round_vector3(vec3, ndigits):
        u"""vector3の桁数を丸め込む

        :param vec3: vector3
        :param ndigits: 丸め込む桁
        :return: vector3
        """
        return round(vec3[0], ndigits), round(vec3[1], ndigits), round(vec3[2], ndigits)

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
        if not mirror_node:
            return False
        elif not cmds.ls(mirror_node, tr=True):
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

        vector_x = cls._round_vector3(vector_x, 3)
        vector_y = cls._round_vector3(vector_y, 3)
        vector_z = cls._round_vector3(vector_z, 3)

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
    def is_ignore_file(maya_scene_path):
        u"""保存をスキップするファイルかどうかを判定

        :param maya_scene_path: Mayaシーンパス
        :return: bool
        """
        txt_path = '{}/ignore.txt'.format(os.path.dirname(maya_scene_path))
        if not os.path.exists(txt_path):
            return False

        with open(txt_path) as f:
            for l in f:
                ignore = l.rstrip('\r\n')
                if maya_scene_path.find(ignore) != -1:
                    return True

        return False

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
    def _get_reverse_attrs(mirror_axis):
        u"""指定した軸に対して反転するアトリビュートを取得

        :param mirror_axis: 軸
        :return: 反転するアトリビュート
        """
        axis_attrs = {
            'x': ('tx', 'ry', 'rz'),
            'y': ('ty', 'rx', 'rz'),
            'z': ('tz', 'rx', 'ry'),
        }
        if mirror_axis in axis_attrs:
            return axis_attrs[mirror_axis]
        else:
            return None

    @staticmethod
    def _get_reverse_custom_attrs(node):
        u"""反転するカスタムアトリビュートの取得

        :param node: ノード名
        :return: 反転するアトリビュート
        """
        attrs = cmds.listAttr(node, ud=True, k=True)
        return attrs if attrs else []

    @staticmethod
    def _reverse_curve(anim_curve):
        u"""アニメーションカーブの値を反転

        :param anim_curve: アニメーションカーブ名
        """
        return cmds.scaleKey(anim_curve, time=(':',), float=(':',), valueScale=-1, valuePivot=0)

    @staticmethod
    def _reverse_pose(node, reverse_attrs, time_):
        u"""ポーズを反転

        :param node: ノード名
        :param reverse_attrs: 反転するアトリビュート
        :param time_: time
        """
        for attr in reverse_attrs:
            if not cmds.getAttr('{}.{}'.format(node, attr), l=True):
                value = cmds.getAttr('{}.{}'.format(node, attr), t=time_)
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
                cls._reverse_curve(attr_curve[attr])

    @classmethod
    def _reverse(cls, node, mirror_axis, mode, **kwargs):
        u"""ポーズまたはモーションの反転

        :param node: ノード名
        :param mirror_axis: 軸
        :param mode: 0 Pose, 1 Motion
        :param kwargs: 'time' 反転時のtime
        """
        logger.debug('Reverse: {} {} {}'.format(node, mirror_axis, mode))

        # ノードの存在判定
        if not cmds.ls(node):
            logger.warning(u'ノードが存在しないため反転をスキップしました: {}'.format(node))
            return
        # 反転するアトリビュートの取得
        reverse_attrs = cls._get_reverse_attrs(mirror_axis)
        if not reverse_attrs:
            logger.warning(u'{}: 軸の指定が不正なので終了します'.format(node))
            return

        time_ = kwargs.setdefault('time', 0)
        if mode == 0:
            cls._reverse_pose(node, reverse_attrs, time_)
        else:
            cls._reverse_motion(node, reverse_attrs)

    @classmethod
    def _reverse_world_offset(cls, world_offset, mirror_axis, mode, **kwargs):
        u"""WorldOffsetの反転

        :param world_offset: worldOffsetノード
        :param mirror_axis: 反転の軸
        :param mode: 0 Pose, 1 Motion
        :param kwargs: 'time' 反転時のtime
        """
        time_ = kwargs.setdefault('time', 0)
        # Pose
        if mode == 0:
            if mirror_axis == 'x':
                tx = cmds.getAttr('{}.tx'.format(world_offset), t=time_)
                cmds.setAttr('{}.tx'.format(world_offset), -1 * tx)
                cmds.setKeyframe('{}.tx'.format(world_offset))
                ry = cmds.getAttr('{}.ry'.format(world_offset), t=time_)
                cmds.setAttr('{}.ry'.format(world_offset), -1 * ry)
                cmds.setKeyframe('{}.ry'.format(world_offset))
            elif mirror_axis == 'z':
                tz = cmds.getAttr('{}.tz'.format(world_offset), t=time_)
                cmds.setAttr('{}.tz'.format(world_offset), -1 * tz)
                cmds.setKeyframe('{}.tz'.format(world_offset))
                ry = cmds.getAttr('{}.ry'.format(world_offset), t=time_)
                cmds.setAttr('{}.ry'.format(world_offset), cls._conv_degrees(ry + 180))
                cmds.setKeyframe('{}.ry'.format(world_offset))
        # Motion
        else:
            if mirror_axis == 'x':
                cls._reverse_motion(world_offset, ('tx', 'ry'))
            elif mirror_axis == 'z':
                cls._reverse_motion(world_offset, ('tz',))
                cmds.keyframe(world_offset, time=(':',), float=(':',), at='ry', vc=180, r=True)

    # ########################################
    #  Swap
    # ########################################
    @classmethod
    def _swap_animation_values(cls, node1, node2, time_):
        u"""アニメーションキーを交換

        :param node1: ノード名1
        :param node2: ノード名2
        :param time_: time
        """
        # ノードの存在判定
        for node in (node1, node2):
            if not cmds.ls(node):
                logger.warning(u'ノードが存在しないため反転をスキップしました: {}'.format(node))
                return
        # キーフレームの存在判定
        for node in (node1, node2):
            if not cls._has_keyframe(node):
                logger.warning(u'キーが存在しないため反転をスキップしました: {}'.format(node))
                return

        logger.debug(u'アニメーション入れ替え: {}, {}, frame: {}'.format(node1, node2, time_))

        # キーの保存用の一時ノードの作成
        temp_node = cmds.spaceLocator()[0]
        # 一時ノードにキーの保存に必要なカスタムアトリビュートを追加
        custom_attrs = cls._get_reverse_custom_attrs(node1)

        for attr in custom_attrs:
            attr_type = cmds.getAttr('{}.{}'.format(node1, attr), typ=True)
            logger.debug(u'カスタムアトリビュート: {}, {}'.format(attr, attr_type))
            if attr_type in cls.type_at:
                cmds.addAttr(temp_node, ln=attr, k=True, at=attr_type)
            elif attr_type in cls.type_dt:
                cmds.addAttr(temp_node, ln=attr, k=True, dt=attr_type)
            else:
                logger.warning(u'カスタムアトリビュートのタイプが判別できませんでした: {}'.format(attr_type))
        try:
            # node1のキーを保存
            cmds.copyKey(node1, time=(':',), float=(':',))
            cmds.pasteKey(temp_node, option='replace')

            times = (time_, time_)

            # node1のキーをnode2へコピー
            cmds.copyKey(node2, time=times)
            cmds.pasteKey(node1, option='replace')

            # node2のキーをnode1へコピー
            cmds.copyKey(temp_node, time=times)
            cmds.pasteKey(node2, option='replace')
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error(u'キーの入れ替え失敗: {}, {}'.format(node1, node2))
        finally:
            cmds.delete(temp_node)

    @classmethod
    def _swap_animation_curve(cls, node1, node2):
        u"""接続されているアニメーションカーブを交換

        :param node1: ノード名1
        :param node2: ノード名2
        """
        # ノードの存在判定
        for node in (node1, node2):
            if not cmds.ls(node):
                logger.warning(u'ノードが存在しないため反転をスキップしました: {}'.format(node))
                return
        # キーフレームの存在判定
        for node in (node1, node2):
            if not cls._has_keyframe(node):
                logger.warning(u'キーが存在しないため反転をスキップしました: {}'.format(node))
                return

        # キーの保存用の一時ノードの作成
        temp_node = cmds.spaceLocator()[0]
        # 一時ノードにキーの保存に必要なカスタムアトリビュートを追加
        custom_attrs = cls._get_reverse_custom_attrs(node1)
        for attr in custom_attrs:
            attr_type = cmds.getAttr('{}.{}'.format(node1, attr), typ=True)
            # cmds.addAttr(temp_node, ln=attr, k=True, at=attr_type)
            logger.debug(u'カスタムアトリビュート: {}, {}'.format(attr, attr_type))
            if attr_type in cls.type_at:
                cmds.addAttr(temp_node, ln=attr, k=True, at=attr_type)
            elif attr_type in cls.type_dt:
                cmds.addAttr(temp_node, ln=attr, k=True, dt=attr_type)
            else:
                logger.warning(u'カスタムアトリビュートのタイプが判別できませんでした: {}'.format(attr_type))

        # node1のキーを保存
        cmds.copyKey(node1, time=(':', ), float=(':', ))
        cmds.pasteKey(temp_node, option='replace')

        # node1のキーをnode2へコピー
        cmds.cutKey(node1, clear=True)
        cmds.copyKey(node2, time=(':',), float=(':',))
        cmds.pasteKey(node1, option='replace')

        # node2のキーをnode1へコピー
        cmds.cutKey(node2, clear=True)
        cmds.copyKey(temp_node, time=(':',), float=(':',))
        cmds.pasteKey(node2, option='replace')

        cmds.delete(temp_node)

    @classmethod
    def _swap_animation(cls, node1, node2, mode, **kwargs):
        u"""ポーズまたはモーションの反転

        :param node1: ノード名1
        :param node2: ノード名2
        :param mode: 0: ポーズ, 1: モーション
        :param kwargs: 'time' 反転時のフレーム
        """
        time_ = kwargs.setdefault('time', 0)
        if mode == 0:
            cls._swap_animation_values(node1, node2, time_)
        else:
            cls._swap_animation_curve(node1, node2)

    @classmethod
    def _get_reloacated_path(cls, path_, dirname_=None):
        u"""Mayaシーンパスを指定したディレクトリ名に変換して返す

        :param path_: Mayaシーンパス
        :param dirname_: ディレクトリ名(絶対パス名 or 相対パス名)
        :return: Mayaシーンパス
        """
        if not dirname_:
            return path_

        # バックスラッシュにパスを統一
        dirpath = re.sub(r'\\', '/', os.path.dirname(path_))
        _dirname = re.sub(r'\\', '/', dirname_)
        filename = os.path.basename(path_)

        if cls._is_relative_path(dirname_):
            dirpath = '{0}/{1}'.format(dirpath, _dirname)
        else:
            dirpath = _dirname

        maya_scene_path = '{0}/{1}'.format(dirpath, filename)
        return maya_scene_path

    @staticmethod
    def _is_relative_path(path_):
        u"""相対パスか確認

        :param path_: パス
        :return: bool
        """
        if path_.find(':') == -1:
            return True
        else:
            return False

    @classmethod
    def save_scene(cls, maya_scene, dirpath):
        u"""mayaシーンファイルの保存

        :param maya_scene: mayaシーンのパス
        :param dirpath: ディレクトリ名(絶対パス名 or 相対パス名)
        :return: 保存したmayaシーンのパス
        """
        if dirpath:
            newname = cls._get_reloacated_path(maya_scene, dirpath)
        else:
            newname = maya_scene

        dirpath = os.path.dirname(newname)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        cmds.file(rename=newname)
        file_path = cmds.file(s=True, f=True)
        return file_path

    @staticmethod
    def get_reverse_file_path(file_path):
        u"""反転モーションのファイル名を取得

        :param file_path:
        :return: ファイルパス
        """
        dirpath = os.path.dirname(file_path)
        filename, ext = os.path.splitext(os.path.basename(file_path))

        if filename[-2:] == '_r':
            return False

        l_id = re.compile('_l[0-9]')
        r_id = re.compile('_r[0-9]')
        l_search = l_id.search(filename)
        r_search = r_id.search(filename)
        if l_search:
            index = l_search.start()
            reverse_name = filename[:index + 1] + 'r' + filename[index + 2:] + '_r'
        elif r_search:
            index = r_search.start()
            reverse_name = filename[:index + 1] + 'l' + filename[index + 2:] + '_r'
        else:
            reverse_name = filename + '_r'

        reverse_file_path = '{}/{}{}'.format(dirpath, reverse_name, ext)
        return re.sub(r'\\', '/', reverse_file_path)

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
    @staticmethod
    def _get_ctrl_set():
        u"""コントローラーのセットを取得"""

        ctrl_sets = cmds.ls(CTRL_SET) + cmds.ls('*:{}'.format(CTRL_SET))
        logger.debug(u'ctrlSets: {}'.format(ctrl_sets))

        if len(ctrl_sets) == 1:
            return ctrl_sets[0]
        # 2つ以上、該当するセットがある場合はシーンと同名のnamespaceがついているものを取得
        namespace = getCurrentSceneFilePath().split('/')[-4]
        logger.debug('namespace: {}'.format(namespace))
        for ctrl_set in ctrl_sets:
            if ctrl_set.find(namespace) != -1:
                return ctrl_set
        # 見つからない場合
        return

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
        # if not cmds.ls(set_):
        #     return []

        nodes = []
        if isinstance(selections, list):
            for selection in selections:
                if not cls._is_set(selection):
                    nodes.append(selection)
                else:
                    temp_nodes = cmds.sets(selection, q=True)
                    if temp_nodes:
                        nodes.extend(temp_nodes)
        else:
            if not cls._is_set(selections):
                nodes.append(selections)
            else:
                temp_nodes = cmds.sets(selections, q=True)
                if temp_nodes:
                    nodes.extend(temp_nodes)

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
    def main(cls, nodes_or_sets, typ, mirror_axis, right_id, left_id, can_bake, mode):
        u"""反転実行用関数

        :param nodes_or_sets: ノードまたはセット (文字列、リストどちらでも可)
        :param typ: 'local' リグの軸基準, 'world' worldOffsetのみ反転, 'both' リグ基準反転後、worldoffset反転
        :param mirror_axis: 軸
        :param right_id: 右側のノードの識別子
        :param left_id: 左側のノードの識別子
        :param can_bake: bakeするか
        :param mode: 0: ポーズ, 1: モーション
        """
        # auto keyかどうかチェック
        state = cmds.autoKeyframe(q=True, st=True)
        cmds.autoKeyframe(st=False)
        # 現在のtimeの記憶
        current = cmds.currentTime(q=True)

        nodes = cls._get_nodes_from_selections(nodes_or_sets)
        world_offset = cls._get_world_offset(nodes)

        # アニメーションのBake
        if mode == 1 and can_bake:
            BakeSimulation.bake(nodes, hierarchy='none')

        # local
        if typ == 'local' or typ == 'both':
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

            # センターノードの反転
            for node in center_nodes:
                cls._reverse(node, node_axis[node], mode, time=current)

            # 右、左のノードの反転
            for right, left in zip(right_nodes, left_nodes):
                cls._swap_animation(right, left, mode, time=current)
                if not node_behavior[right]:
                    cls._reverse(right, node_axis[right], mode, time=current)
                    cls._reverse(left, node_axis[left], mode, time=current)
                else:
                    logger.info('skipped reverse: {}, {}'.format(right, left))

            if world_offset:
                cmds.mute('{}.t'.format(world_offset), d=True, f=True)
                cmds.mute('{}.r'.format(world_offset), d=True, f=True)

                cmds.setAttr('{}.t'.format(world_offset), *pos)
                cmds.setAttr('{}.r'.format(world_offset), *rot)

            if typ == 'both':
                logger.debug('reverse: world')
                if world_offset:
                    cls._reverse_world_offset(world_offset, mirror_axis, mode, time=current)

        # worldOffset
        else:
            logger.debug('reverse: world')
            if world_offset:
                cls._reverse_world_offset(world_offset, mirror_axis, mode, time=current)

        cmds.currentTime(current)
        cmds.autoKeyframe(st=state)

    # ########################################
    #  Batch Mode
    # ########################################
    @classmethod
    def exec_standalone(cls, maya_scene, typ, mirror_axis, right_id, left_id, can_bake, can_save, dirpath):
        u"""バッチモード実行用の関数

        :param maya_scene: mayaシーンのパス
        :param typ: 'local' リグの軸基準, 'world' worldOffsetのみ反転, 'both' リグ基準反転後、worldoffset反転
        :param mirror_axis: 軸
        :param right_id: 右側のノードの識別子
        :param left_id: 左側のノードの識別子
        :param can_bake: bakeするか
        :param can_save: 保存するか
        :param dirpath: 出力先のディレクトリ
        :return: 保存後のmayaシーンのパス
        """
        if cls.is_ignore_file(maya_scene):
            logger.warning(u'除外対象のファイルだったため処理をスキップしました')
            return

        # ファイルを開く
        file_path = cmds.file(maya_scene, o=True, f=True)
        # コントローラーの取得
        ctrl_set = cls._get_ctrl_set()
        if not ctrl_set:
            logger.warning(u'コントローラーを取得できなかったためスキップしました')
            return

        # スクリプトの実行
        cls.main(ctrl_set, typ, mirror_axis, right_id, left_id, can_bake, 1)
        if can_save:
            save_scene_path = cls.get_reverse_file_path(maya_scene)
            if save_scene_path:
                file_path = cls.save_scene(save_scene_path, dirpath)
            else:
                logger.warning(u'右側モーションだったため保存をスキップしました')

        return file_path

    # ########################################
    #  Debug
    # ########################################
    @classmethod
    def debug_reset_controller(cls, *args, **kwargs):
        u"""コントローラーのリセット"""
        selections = cmds.ls(sl=True, typ='objectSet')
        if not selections:
            return

        ctrl_set = selections[0]
        nodes = cls._get_nodes_from_selections(ctrl_set)

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
        right_id = '_L_'
        left_id = '_R_'

        nodes = cls._get_nodes_from_selections(ctrl_set)
        nodes.sort()
        info = u'\n{:^35s} {:^6s} {:^6s} {:^7s} {:^30s} {:^30s}\n'.format(
            'node', 'p_axis', 's_axis', 'behavior', 'p_v', 's_v',
        )
        info += u'{:-<35s} {:-<6s} {:-<6s} {:-<7s} {:-<30s} {:-<30s}\n'.format('', '', '', '', '', '')

        cls.debug_reset_controller()
        for node in nodes:
            if displays_left_only:
                if not cls._is_id_node(node, right_id) or cls._is_id_node(node, left_id):
                    continue
            is_behavior = cls._is_behavior(node, right_id, left_id)
            if mode == 1 and not is_behavior:
                continue
            elif mode == 2 and is_behavior:
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
