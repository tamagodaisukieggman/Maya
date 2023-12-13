# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random
import re

import maya.cmds as cmds
import pymel.core as pm

from ...glp_random_obj_placement import placement_objs


class PlacementMobAudienceObjs(object):

    def __init__(self):

        self.placement_objs = placement_objs.PlacementObjs()

    def placement_mob_audience_objs(self, max_count, shade_flag, weather_flag, surface_area_ratio, placement_info_list):
        """インポスター観客(モブ観客)用のオブジェクトをメッシュ面積に応じて配置する

        Args:
            max_count (int): 最大配置数
            placement_info_list ([type]): [description]
        """

        placement_count_sum_value = 0

        for placement_info in placement_info_list:

            target_mesh = None

            if len(placement_info.mesh_list) == 0:
                continue
            elif len(placement_info.mesh_list) == 1:
                target_mesh = placement_info.mesh_list[0]
            else:
                # ランダムの偏りを減らすためメッシュを結合する
                dup_mesh_list = cmds.duplicate(placement_info.mesh_list)
                target_mesh = cmds.polyUnite(dup_mesh_list)[0]
                placement_info.is_mesh_unite = True
                # 結合したら複製した結合前メッシュは削除(Material剥がれるが関係ない)
                cmds.delete(dup_mesh_list)

            placement_info.placement_value_info.base_mesh_list = [target_mesh]

            placement_info.placement_count = self.calculate_objs_count_from_mesh_area(
                target_mesh,
                placement_info.ratio,
                surface_area_ratio)
            placement_count_sum_value += placement_info.placement_count

        placement_ratio = float(max_count) / float(placement_count_sum_value)

        # 配置数オーバーしている時は個数の再分配が必要
        flag_count = 0
        while placement_ratio < 1.0:

            flag_count += 1
            if flag_count == 5:
                break

            for placement_info in placement_info_list:
                placement_info.placement_count = int(round(placement_info.placement_count * placement_ratio))

            placement_count_sum_value = sum([pi.placement_count for pi in placement_info_list])
            placement_ratio = float(placement_count_sum_value) / float(max_count)

        orig_locator = cmds.spaceLocator(n='pos00000')
        orig_locator_name = orig_locator[0]

        # 日向/日陰の状態と天候の状態を複製するロケーターのScaleX/Yにセット
        cmds.setAttr('{}.scaleX'.format(orig_locator_name), shade_flag)
        cmds.setAttr('{}.scaleY'.format(orig_locator_name), weather_flag)

        print('=' * 20)

        for placement_info in placement_info_list:

            target_obj_info_list = [
                TargetObjInfo(orig_locator_name, placement_info.placement_count)
            ]

            placement_objs.PlacementObjs().placement_objs_at_random_based_on_mesh(
                placement_info.placement_value_info,
                target_obj_info_list
            )

            if placement_info.is_mesh_unite:
                cmds.delete(placement_info.placement_value_info.base_mesh_list)

            print(u'配置メッシュ: {} 配置個数: {}'.format(','.join(placement_info.mesh_list), placement_info.placement_count))

        print('=' * 20)

        if cmds.objExists(orig_locator_name):
            cmds.delete(orig_locator_name)

    def calculate_objs_count_from_mesh_area(self, mesh, ratio, surface_area_ratio):
        """メッシュ面積と掛け率から、配置個数を算出する

        Args:
            mesh (string): 対象のmeshオブジェクト名
            ratio (int): 面積に対する配置個数の掛け率
            surface_area_ratio (int): 面積の割率 数値が小さければ小さいほど少ない面積に多くのオブジェクトを置く

        Returns:
            int: 算出した配置個数
        """

        mesh_node = pm.PyNode(mesh)
        mesh_area_sum_value = mesh_node.getShape().area()

        return int(round(mesh_area_sum_value * ratio / surface_area_ratio))

    def shave_mob_audience_objs_from_selected(self, ratio=0, count=0):
        """選択したモブ観客ロケーター(pos[0-9]{5}$)からratio(割合)またはcount(実数)に応じて間引く
        ratioとcount両方とも入力されている場合は、ratioを優先する

        Args:
            ratio (int): 削減割合(0~10)
            count (int): 削減数の実数
        """

        target_mob_audience_obj_list = [
            loc for loc in cmds.ls(sl=True, type='transform') if cmds.listRelatives(loc, type='locator') is not None and re.search(r'pos[0-9]{5}$', loc)]
        if not target_mob_audience_obj_list:
            return []

        target_mob_audience_obj_count = len(target_mob_audience_obj_list)
        shave_mob_audience_obj_count = 0
        # 間引く数の計算はratio(割合)が入力されていたら優先する
        if ratio > 0:
            shave_mob_audience_obj_count = int(target_mob_audience_obj_count / 10 * ratio)
        elif count > 0:
            shave_mob_audience_obj_count = count
            if shave_mob_audience_obj_count > target_mob_audience_obj_count:
                shave_mob_audience_obj_count = target_mob_audience_obj_count

        shave_mob_audience_obj_list = []
        # python2だとchoicesが存在しないのでchoiceでランダム抽出
        for _ in range(shave_mob_audience_obj_count):
            target = random.choice(target_mob_audience_obj_list)
            target_mob_audience_obj_list.remove(target)
            shave_mob_audience_obj_list.append(target)

        cmds.delete(shave_mob_audience_obj_list)

        return [target_mob_audience_obj_count, shave_mob_audience_obj_count]


class TargetObjInfo(object):

    def __init__(self, target_obj, count):

        self.target_obj = target_obj
        self.count = count

    def get_value(self):

        return self.count
