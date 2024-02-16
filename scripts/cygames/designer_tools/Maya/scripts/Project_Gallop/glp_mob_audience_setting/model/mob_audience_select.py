# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re

import maya.cmds as cmds
import maya.api.OpenMaya as om


class MobAudienceSelect(object):

    def select_mob_audience_locator(self, select_type):
        """雨具無し・雨具あり・雨合羽のみそれぞれのモブ観客用ロケーターを選択する

        Args:
            type (string): 選択するモブ観客用ロケーターのタイプ
            normal=雨具無し(ScaleY=1)、rain_gear=雨具あり(ScaleY=2)、raincort=雨合羽のみ(ScaleY=3)
        """

        locator_list = self.__get_mob_audience_locator_list()

        target_scale = None
        if select_type == 'normal':
            target_scale = 1
        elif select_type == 'rain_gear':
            target_scale = 2
        elif select_type == 'raincort':
            target_scale = 3
        else:
            return

        locator_list = [loc for loc in locator_list if cmds.getAttr('{}.scaleY'.format(loc)) == target_scale]

        cmds.select(cl=True)
        cmds.select(locator_list)

    def select_mob_audience_locator_on_mesh(self):
        """選択されているメッシュ上にいるモブ観客用ロケーターを選択する

        各メッシュに対してシーン上に存在するモブ観客用ロケーター(pos[0-9]{5})から
        Y軸でRayを飛ばし交差判定を行いHit=メッシュ上に乗っているロケーターとして選択対象に加える
        """

        selected = [sel for sel in cmds.ls(sl=True, type='transform') if cmds.listRelatives(sel, type='mesh') is not None]
        if not selected:
            cmds.warning(u'メッシュが何も選択されていません')
            return

        # 子ノードのtypeが「locator」並びに名前が「pos[0-9]{5}$」のノードを取得する
        mob_audience_locator_list = self.__get_mob_audience_locator_list()
        if not mob_audience_locator_list:
            cmds.warning(u'インポスター観客(モブ観客)用配置ロケーター(pos*****)が存在しませんでした')
            return

        hit_mob_audience_locator_list = []

        for sel in selected:

            mesh_fn = self.__get_fn_mesh(sel)

            for mob_audience_locator in mob_audience_locator_list:

                # 既にhitしていたら処理しない
                if mob_audience_locator in hit_mob_audience_locator_list:
                    continue

                locator_translate_point = self.__get_obj_float_point_translate(mob_audience_locator)

                # 交差判定
                ret = mesh_fn.allIntersections(
                    locator_translate_point,   # raySource ---------- レイスタートポイント
                    om.MFloatVector(0, 1, 0),  # rayDirection ------- レイの方向
                    om.MSpace.kWorld,          # coordinate space --- ヒットポイントが指定されている座標空間
                    99999.0,                   # maxParam ----------- ヒットを考慮する最大半径
                    True,                      # testBothDirections - 負のrayDirectionのヒットも考慮する必要があるかどうか
                    tolerance=0.001,           # tolerance ---------- 交差操作の数値許容差
                )

                # retの引数0はhitpoint(交錯した点)のリストなので、1つでもあれば交錯した判定
                if ret and len(ret[0]):
                    hit_mob_audience_locator_list.append(mob_audience_locator)

        # 最後にまとめて選択
        cmds.select(hit_mob_audience_locator_list)

    def __get_mob_audience_locator_list(self):
        """モブ観客用ロケーターのリストを取得する

        子ノードのtypeが「locator」尚且つpos[0-9]{5}$に当てはまる
        モブ観客用ロケーターのリストを取得する

        Returns:
            list: モブ観客用ロケーターのリスト
        """

        return [loc for loc in cmds.ls('pos*', type='transform') if cmds.listRelatives(loc, type='locator') is not None and re.search(r'pos[0-9]{5}$', loc)]

    def __get_obj_float_point_translate(self, target):
        """対象のオブジェクトのMFloatPoint型のtranslate値を取得する

        Args:
            target (string): translate値を取得したいオブジェクト

        Returns:
            targetのtranslate値が入ったMFloatPoint
        """

        selection = om.MSelectionList()
        selection.add(target)
        dag_path = selection.getDagPath(0)
        transform = om.MFnTransform(dag_path)
        translation = transform.translation(om.MSpace.kWorld)

        return om.MFloatPoint(translation)

    def __get_fn_mesh(self, target):
        """targer名からopenMayaのMFnMeshノードを取得する

        Args:
            target: 取得するオブジェクトの名前

        Returns:
            MFnMesh
        """

        selection = om.MSelectionList()
        selection.add(target)
        dag_path = selection.getDagPath(0)

        return om.MFnMesh(dag_path)
