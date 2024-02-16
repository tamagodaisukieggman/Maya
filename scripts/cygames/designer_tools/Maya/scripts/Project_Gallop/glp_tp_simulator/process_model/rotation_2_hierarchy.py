# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

from . import base_model

reload(base_model)


class Rotation2HierarchyModel(base_model.BaseModel):

    def __init__(self, *args, **kwargs):
        super(Rotation2HierarchyModel, self).__init__(*args, **kwargs)

        # 姿勢の復元のためのdagPose
        # 初期姿勢取得のために、bindPose→実行→姿勢を復元という挙動になる
        self.__tmp_pose = None

    def create_process(self):
        """プロセスを実行するノードを作成

        Returns:
            bool: 実行結果
            list: 作成されたノードリスト
        """

        target = self.target()
        if not target:
            return False, []

        parent = None
        grand_parent = None

        if cmds.objExists(target):
            parents = cmds.listRelatives(target, p=True)
            if parents:
                parent = parents[0]
                grand_parents = cmds.listRelatives(parents, p=True)
                if grand_parents:
                    grand_parent = grand_parents[0]

        if parent and grand_parent:
            result, created_nodes = self.__create_process_nodes(target, parent, grand_parent)
            return result, created_nodes

    def __create_process_nodes(self, target, parent, grand_parent):
        """処理本体となるノード構成の作成

        Args:
            target (str): プロセスの対象トランスフォーム（Tp骨）
            parent (str): targetの親トランスフォーム
            grand_parent (str): targetの親の親トランスフォーム

        Returns:
            bool, list[node]: ノード構成に成功したか、作成したノードリスト
        """

        process_nodes = []
        grand_parent_anti_roll, created_nodes1 = self.__create_anti_roll_nodes(grand_parent)
        parent_anti_roll, created_nodes2 = self.__create_anti_roll_nodes(parent)

        process_nodes.extend(created_nodes1 + created_nodes2)
        if not grand_parent_anti_roll or not parent_anti_roll:
            return False, process_nodes

        anti_roll_sum = cmds.shadingNode('quatProd', au=True)
        process_nodes.append(anti_roll_sum)
        cmds.connectAttr(grand_parent_anti_roll + '.outputQuat', anti_roll_sum + '.input1Quat', f=True)
        cmds.connectAttr(parent_anti_roll + '.outputQuat', anti_roll_sum + '.input2Quat', f=True)

        to_euler = cmds.shadingNode('quatToEuler', au=True)
        process_nodes.append(to_euler)
        cmds.connectAttr(anti_roll_sum + '.outputQuat', to_euler + '.inputQuat', f=True)

        cmds.connectAttr(to_euler + '.outputRotate.outputRotateY', target + '.rotate.rotateY', f=True)

        return True, process_nodes

    def __create_anti_roll_nodes(self, transform):
        """捻り成分を打ち消すノード群を作成

        Args:
            transform (str): 対象トランスフォーム

        Returns:
            node, list[node]: 捻り成分を打ち消すquatInvertノード、作成したノードリスト
        """

        anti_roll_node = None
        created_nodes = []
        target = transform

        if not cmds.objExists(target):
            return anti_roll_node, created_nodes

        # 曲げ(bent)と捩じり(roll)にターゲットのrotateを分離する
        # 曲げ成分をとるため、軸方向のyへの単位ベクトルのマトリクスを作成
        fwd_mtx = cmds.shadingNode('composeMatrix', au=True)
        created_nodes.append(fwd_mtx)
        cmds.setAttr(fwd_mtx + '.inputTranslateY', 1)

        # ターゲットのrotateマトリクスを作成
        rot_mtx = cmds.shadingNode('composeMatrix', au=True)
        created_nodes.append(rot_mtx)
        cmds.connectAttr(target + '.rotate', rot_mtx + '.inputRotate', f=True)

        # ターゲットのマトリクスと軸方向単位ベクトルを掛け合わせたマトリクスを生成
        fwd_mul_mtx = cmds.shadingNode('multMatrix', au=True)
        created_nodes.append(fwd_mul_mtx)
        cmds.connectAttr(fwd_mtx + '.outputMatrix', fwd_mul_mtx + '.matrixIn[0]', f=True)
        cmds.connectAttr(rot_mtx + '.outputMatrix', fwd_mul_mtx + '.matrixIn[1]', f=True)

        # 単位ベクトルの移動量が曲げ(bent)成分になるので分離
        fwd_dcmp_mtx = cmds.shadingNode('decomposeMatrix', au=True)
        created_nodes.append(fwd_dcmp_mtx)
        cmds.connectAttr(fwd_mul_mtx + '.matrixSum', fwd_dcmp_mtx + '.inputMatrix', f=True)

        # 初期位置をvector1に記録し、そこからどれだけ移動したかを角度に変換（=曲げ角）
        fwd_angle_between = cmds.shadingNode('angleBetween', au=True)
        created_nodes.append(fwd_angle_between)
        org_fwd = cmds.getAttr(fwd_dcmp_mtx + '.outputTranslate')[0]
        cmds.setAttr(fwd_angle_between + '.vector1', org_fwd[0], org_fwd[1], org_fwd[2], type='double3')
        cmds.connectAttr(fwd_dcmp_mtx + '.outputTranslate', fwd_angle_between + '.vector2', f=True)

        # 曲げ成分をクオータニオン変換
        bent_angle_to_quat = cmds.shadingNode('axisAngleToQuat', au=True)
        created_nodes.append(bent_angle_to_quat)
        cmds.connectAttr(fwd_angle_between + '.axisAngle.axis', bent_angle_to_quat + '.inputAxis', f=True)
        cmds.connectAttr(fwd_angle_between + '.axisAngle.angle', bent_angle_to_quat + '.inputAngle', f=True)

        # 曲げ成分を打ち消すクオータニオンを作成
        anti_bent_quat = cmds.shadingNode('quatInvert', au=True)
        created_nodes.append(anti_bent_quat)
        cmds.connectAttr(bent_angle_to_quat + '.outputQuat', anti_bent_quat + '.inputQuat', f=True)

        # ターゲットのrotateクオータニオンを作成
        target_quat = cmds.shadingNode('eulerToQuat', au=True)
        created_nodes.append(target_quat)
        cmds.connectAttr(target + '.rotate', target_quat + '.inputRotate', f=True)

        # ターゲットのrotateから曲げ成分を打ち消した（＝捩じり成分）クオータニオンを作成
        roll_quat = cmds.shadingNode('quatProd', au=True)
        created_nodes.append(roll_quat)
        cmds.connectAttr(target_quat + '.outputQuat', roll_quat + '.input1Quat', f=True)
        cmds.connectAttr(anti_bent_quat + '.outputQuat', roll_quat + '.input2Quat', f=True)

        # 捩じり成分を打ち消すクオータニオンを作成
        anti_roll_quat = cmds.shadingNode('quatInvert', au=True)
        created_nodes.append(anti_roll_quat)
        cmds.connectAttr(roll_quat + '.outputQuat', anti_roll_quat + '.inputQuat', f=True)

        anti_roll_node = anti_roll_quat
        return anti_roll_quat, created_nodes

    def pre_start_process(self):
        """プロセスの前処理
        """

        # 実行時のポーズをself.__tmp_poseに記録して、初期姿勢記録のためバインドポーズに戻す
        target = self.target()
        if not cmds.attributeQuery('bindPose', n=target, ex=True):
            return

        bind_poses = cmds.listConnections(target + '.bindPose', d=True, s=False, type='dagPose')
        if not bind_poses:
            return

        if not cmds.dagPose(bind_poses[0], q=True, ap=True):  # バインドポーズから動いていない
            return

        # targetには計算結果が反映されるのでtarget以外のポーズを保存
        members = cmds.ls(cmds.dagPose(bind_poses[0], q=True, m=True), l=True)
        members.remove(cmds.ls(target, l=True)[0])
        self.__tmp_pose = cmds.dagPose(members, save=True, sl=True)

        mel.eval('doEnableNodeItems false all;')
        cmds.dagPose(n=bind_poses[0], r=True)  # goToBindPose
        mel.eval('doEnableNodeItems true all;')

        # バインドポーズに戻した場合は初期値を再セット
        target_attrs = self.target_attrs()
        if target_attrs:
            self.set_init_vals([cmds.getAttr('{}.{}'.format(target, x)) for x in target_attrs])

    def post_start_process(self):
        """プロセス実行直後処理
        """

        # 実行時のポーズを復元する
        if self.__tmp_pose and cmds.objExists(self.__tmp_pose):
            mel.eval('doEnableNodeItems false all;')
            cmds.dagPose(n=self.__tmp_pose, restore=True)
            mel.eval('doEnableNodeItems true all;')
            cmds.delete(self.__tmp_pose)
            self.__tmp_pose = None
