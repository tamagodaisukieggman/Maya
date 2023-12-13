# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds
import math


class AimMobAudienceDirection(object):

    def aim_mob_audience_direction(self, target_list, limit_tgt_to_loc=False):
        """選択したオブジェクトを一番近いtarget方向にAimさせる

        Args:
            target_list ([type]): [description]
            limit_tgt_to_loc (bool, optional): [description]. Defaults to False.
        """

        selected = [sel for sel in self.__get_selected_obj_list(limit_tgt_to_loc) if sel not in target_list]
        if not selected:
            return

        # エイムコンストレインで、エイム先よりY値が低いオブジェクトのRotateYが期待通りの挙動をしてくれない
        # 現状では解決方法が思いつかないためAim先と同じオブジェクトを複製しtranslateYを-10000に設定し
        # 選択したオブジェクトよりY値を低くする事によって疑似的に回避する
        # モブ観客が-100mより低い位置にいることはない筈
        # バッファを取りすぎると遠すぎてAimしてくれなくなるため、数値注意
        tmp_target_list = []
        for target in target_list:
            if not cmds.objExists(target):
                return

            tmp_target = cmds.duplicate(target)[0]
            cmds.setAttr('{}.translateY'.format(tmp_target), -10000)
            tmp_target_list.append(tmp_target)

        constraint_node_list = []
        for sel in selected:
            direction_locator = None
            near_distance = None
            for i in range(len(target_list)):
                target = target_list[i]
                tmp_target = tmp_target_list[i]
                distance = self.calculate_distance(target, sel)
                if near_distance is None or near_distance > distance:
                    direction_locator = tmp_target
                    near_distance = distance

            # 距離計算
            constrain_node = cmds.aimConstraint(
                direction_locator,
                sel,
                aimVector=[0.0, 0.0, 1.0],
                upVector=[0.0, 1.0, 0.0],
                worldUpVector=[0.0, 1.0, 0.0],
                skip=['x', 'z'])

            # エイムしたロケーターのrotateX,Zに微値が入ることがあるので、これを必ず0にする
            cmds.setAttr('{}.rotateX'.format(sel), 0.0)
            cmds.setAttr('{}.rotateZ'.format(sel), 0.0)
            constraint_node_list.extend(constrain_node)

        if constraint_node_list:
            cmds.delete(constraint_node_list)

        if tmp_target_list:
            cmds.delete(tmp_target_list)

    def __get_selected_obj_list(self, limit_tgt_to_loc):
        """選択しているオブジェクトを取得する

        Args:
            limit_tgt_to_loc (bool): ロケーターのみ実行対象にするかどうか

        Returns:
            [list]: 選択しているオブジェクト一覧 limit_tgt_to_locがTrueの場合は選択しているロケーター一覧
        """

        selected = []

        if limit_tgt_to_loc:
            selected = [sel for sel in cmds.ls(sl=True, l=True) if cmds.listRelatives(sel, type='locator') is not None]
        else:
            selected = cmds.ls(sl=True, l=True)

        return selected

    def calculate_distance(self, obj1, obj2):
        """三点間の距離計算

        Args:
            obj1 ([type]): [description]
            obj2 ([type]): [description]

        Returns:
            [type]: [description]
        """

        obj1_translate = cmds.xform(obj1, q=True, t=True, ws=True)
        obj2_translate = cmds.xform(obj2, q=True, t=True, ws=True)

        return math.sqrt((obj1_translate[0] - obj2_translate[0]) ** 2 + (obj1_translate[1] - obj2_translate[1]) ** 2 + (obj1_translate[2] - obj2_translate[2]) ** 2)
