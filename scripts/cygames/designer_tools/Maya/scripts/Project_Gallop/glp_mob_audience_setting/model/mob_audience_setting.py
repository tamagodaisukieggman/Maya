# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import random
from PySide2 import QtWidgets

import maya.cmds as cmds

USE_RAIN_GEAR_SCALEY_VALUE = 2  # 雨合羽/傘 両方とも設定できる
USE_ONLY_OILCOAT_SCALEY_VALUE = 3  # 雨合羽のみ設定できる


class MobAudienceSetting(object):

    def exec_mob_audience_setting(self, limit_tgt_to_loc, settings):
        """背景に配置する3Dモブ観客用のオブジェクトに対して設定を行う

        Args:
            limit_tgt_to_loc (bool): ロケーターのみ実行対象にするかどうか
            settings (list): 実行する対象関数の情報
        """

        target_obj_list = self.__get_selected_obj_list(limit_tgt_to_loc)
        if not target_obj_list:
            message = u'選択オブジェクトが取得できませんでした。'
            if limit_tgt_to_loc:
                message += u'\nロケーターを選択しているか確認してください。'

            QtWidgets.QMessageBox.warning(None, 'warning', message)
            return

        for setting in settings:

            setting_type = setting.get('type')
            setting_option = setting.get('option')

            # モブ観客の雨具設定
            if setting_type == 'set_rein_gear_setting':
                do_umbrella_distance_setting = setting_option.get('do_umbrella_distance_setting')
                umbrella_distance = setting_option.get('umbrella_distance')
                direction = setting_option.get('direction')
                self.__set_mob_audience_rein_gear_setting(target_obj_list, do_umbrella_distance_setting, umbrella_distance, direction)

            # モブ観客の雨具無し/雨具ありのランダム振り分け設定
            if setting_type == 'set_random_rein_gear_setting':
                rein_gear_ratio = setting_option.get('rain_gear_ratio')
                normal_gear_ratio = setting_option.get('normal_gear_ratio')
                self.__set_rain_gear_setting_to_mob_audience_at_random(target_obj_list, rein_gear_ratio, normal_gear_ratio)

        QtWidgets.QMessageBox.information(None, 'information', u'処理が完了しました')

    def __set_rain_gear_setting_to_mob_audience_at_random(self, target_obj_list, rein_gear_ratio, normal_gear_ratio):
        """モブ観客に雨具設定をランダムに設定する

        選択しているモブ観客ロケーターに対して、雨具なし(ScaleY=1)、雨具あり(ScaleY=2)を引数で指定した割合に従って設定する

        Args:
            target_obj_list (list): 対象ロケーターのリスト
            rein_gear_ratio (int): 雨具有り側の比率
            normal_gear_ratio ([type]): 雨具無し側の比率
        """

        if rein_gear_ratio <= 0 or normal_gear_ratio <= 0:
            QtWidgets.QMessageBox.warning(None, 'warning', u'数値が0の欄が存在します')
            return

        ratio_sum = rein_gear_ratio + normal_gear_ratio

        # 雨具ありのオブジェクト数を算出
        rain_gear_count = int(len(target_obj_list) / ratio_sum * rein_gear_ratio)
        rain_gear_target_obj_list = []

        choice_target_obj_list = target_obj_list[:]
        # python2だとchoicesが存在しないのでchoiceでランダム抽出
        for i in range(rain_gear_count):
            target = random.choice(choice_target_obj_list)
            choice_target_obj_list.remove(target)
            rain_gear_target_obj_list.append(target)

        for target_obj in target_obj_list:
            target_scale = 1
            if target_obj in rain_gear_target_obj_list:
                target_scale = 2
            cmds.setAttr('{}.scaleY'.format(target_obj), target_scale)

    def __set_mob_audience_rein_gear_setting(self, target_obj_list, do_umbrella_distance_setting, umbrella_distance, direction):
        """モブ観客の雨具設定を行う

        モブ観客の雨具設定はScaleYの値で行っており、それぞれ
        1=通常(雨具無し)
        2=傘/雨合羽ランダム
        3=雨合羽のみ
        という設定に分かれる
        変数に応じて、対象のオブジェクトのScaleYの値を設定する

        do_umbrella_distance_settingをTrueにすると、傘の距離制限処理が実行され
        雨具設定が傘/雨合羽ランダム(2)であるオブジェクトの隣のオブジェクトとの距離が
        umbrella_distance以下のオブジェクトは必ず雨合羽(3)となる設定になる

        Falseの場合は一律で全て傘/雨合羽ランダム(2)となる

        Args:
            target_obj_list (list)): 実行対象のオブジェクト
            do_umbrella_distance_setting (bool): 傘の距離制限処理を実行するか
            umbrella_distance (float): 傘同士の距離
            direction (string): 傘の距離制限処理をX、-Xどちらの方向から実行するか
        """

        # 距離設定あり
        if do_umbrella_distance_setting:

            # オブジェクトの情報クラスを個数分作成
            audience_obj_info_list = [MobAudienceObjInfo(target_obj) for target_obj in target_obj_list]

            # translateX順にソート
            if direction == '-X':
                audience_obj_info_list = sorted(audience_obj_info_list, key=lambda x: (-x.translate[0], -x.translate[2]))
            elif direction == 'X':
                audience_obj_info_list = sorted(audience_obj_info_list, key=lambda x: (x.translate[0], -x.translate[2]))

            self.__divide_mob_audience_rein_gear_type(audience_obj_info_list, umbrella_distance)

        # 距離設定なし
        else:
            for target_obj in target_obj_list:
                cmds.setAttr('{}.scaleY'.format(target_obj), USE_RAIN_GEAR_SCALEY_VALUE)

    def __divide_mob_audience_rein_gear_type(self, audience_obj_info_list, umbrella_distance):
        """モブ観客の雨具タイプの振り分けを行う

        オブジェクトをソート順に傘/雨合羽ランダムか雨合羽のみかに振り分ける

        Args:
            audience_obj_info_list (list): オブジェクトの設定情報クラスのリスト
            umbrella_distance (float): 傘同士の制限距離
        """

        for i in range(len(audience_obj_info_list)):

            audience_obj_info = audience_obj_info_list[i]

            # 既に雨具設定が決まっている(=audience_rein_gear_type)ものは対応に入れない
            if audience_obj_info.audience_rein_gear_type is None:

                audience_obj_info.audience_rein_gear_type = USE_RAIN_GEAR_SCALEY_VALUE

                # 距離を測定して特定距離以内にあるオブジェクトのaudience_rein_gear_typeを雨合羽限定に
                for j in range(i, len(audience_obj_info_list)):

                    comparison_audience_obj_info = audience_obj_info_list[j]
                    if comparison_audience_obj_info.audience_rein_gear_type is not None:
                        continue

                    org_translate = audience_obj_info.translate
                    comp_translate = comparison_audience_obj_info.translate

                    # XまたはZがそもそもumbrella_distance以上距離が空いていたら
                    if comp_translate[0] - org_translate[0] > umbrella_distance:
                        continue
                    if comp_translate[2] - org_translate[2] > umbrella_distance:
                        continue
                    if self.__get_distance(org_translate, comp_translate) > umbrella_distance:
                        continue

                    comparison_audience_obj_info.audience_rein_gear_type = USE_ONLY_OILCOAT_SCALEY_VALUE

            audience_obj_info.set_audience_rein_gear_type_to_scale_attr()

    def __get_selected_obj_list(self, limit_tgt_to_loc):
        """選択しているオブジェクトを取得する

        Args:
            limit_tgt_to_loc (bool): ロケーターのみ実行対象にするかどうか

        Returns:
            [list]: 選択しているオブジェクト一覧 limit_tgt_to_locがTrueの場合は選択しているロケーター一覧
        """

        selected = []

        if limit_tgt_to_loc:
            selected = [sel for sel in cmds.ls(sl=True) if cmds.listRelatives(sel, type='locator') is not None]
        else:
            selected = cmds.ls(sl=True)

        return selected

    def __get_distance(self, translate_1, translate_2):
        """2点間の距離を取得する

        平面処理の為Yは考慮に入れない

        Args:
            translate_1 (list): object1のtranslate情報 [X, Y, Z]
            translate_2 (list): object2のtranslate情報 [X, Y, Z]

        Returns:
            float: object1と2との距離
        """

        return math.sqrt((translate_2[0] - translate_1[0]) ** 2 + (translate_2[2] - translate_1[2]) ** 2)


class MobAudienceObjInfo(object):
    """モブ観客オブジェクトの情報セット用クラス
    """

    def __init__(self, obj):

        self.obj = obj  # 対象オブジェクト自身
        self.translate = None  # オブジェクトのtranslate値(ws)
        self.audience_rein_gear_type = None  # 雨具の設定タイプ

        self.__initialize()  # 現状未使用

    def __initialize(self):
        """初期設定

        Returns:
            bool: 初期設定が完了しているか
        """

        self.translate = cmds.xform(self.obj, q=True, t=True, ws=True)

    def set_audience_rein_gear_type_to_scale_attr(self):
        """オブジェクトのScaleYに雨具設定タイプをセットする
        """

        if self.audience_rein_gear_type is None:
            return

        cmds.setAttr('{}.scaleY'.format(self.obj), self.audience_rein_gear_type)
