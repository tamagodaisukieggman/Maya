# -*- coding: utf-8 -*-
u"""Shotgridのアセットの特定やデフォルト設定の取得を行う
ShotgunDataLinkのsettingデータを取得しており独自形式の為、
将来的には全てのShotgrid系のモジュールから引用しやすくするためにフォーマットの簡素化・共通化を行う
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import re
import csv
import json

from .util import Util

try:
    from builtins import next
    from builtins import str
    from builtins import object
except Exception:
    pass

SDL_SETTING_JSON_DIR_PATH = '\\\\cgs-str-fas05\\100_projects\\049_gallop\\30_design\\08_ta\\tools\\shotgun_data_link\\setting'
TARGET_SDL_SETTING_TERGET_KEY_PARAM_LIST = [
    {'field_key': 'searchSgField', 'value_key': 'searchSgFieldValue', 'is_search_target': True},
    {'field_key': 'subSearchSgField0', 'value_key': 'subSearchSgField0Value', 'is_search_target': True},
    {'field_key': 'subSearchSgField1', 'value_key': 'subSearchSgField1Value', 'is_search_target': True},
    {'field_key': 'optionSgField0', 'value_key': 'optionSgFieldValue0', 'is_search_target': False},
    {'field_key': 'optionSgField1', 'value_key': 'optionSgFieldValue1', 'is_search_target': False},
    {'field_key': 'optionSgField2', 'value_key': 'optionSgFieldValue2', 'is_search_target': False},
    {'field_key': 'optionSgField3', 'value_key': 'optionSgFieldValue3', 'is_search_target': False},
    {'field_key': 'optionSgField4', 'value_key': 'optionSgFieldValue4', 'is_search_target': False},
    {'field_key': 'optionSgField5', 'value_key': 'optionSgFieldValue5', 'is_search_target': False},
    {'field_key': 'taskTemplateSgField', 'value_key': 'taskTemplateSgFieldValue', 'is_search_target': False}
]
ASSET_NAME_REGEX = r'(m|)(chr|bdy|toon_prop|prop|tail|attach)(\d{4}_\d{2})(_\d{2}|_face\d|_face\d{3}|_hair\d{3}|)'


class SgAssetDefaultSetting(object):

    def __init__(self):

        self.sg_asset_default_setting = []

        self.__set_sg_asset_default_setting()

    def __set_sg_asset_default_setting(self):
        u"""ShotgunDataLinkのsettingファイルを全て読み込み優先度順で並べてリスト化する
        """

        if not os.path.exists(SDL_SETTING_JSON_DIR_PATH):
            return

        file_dir_list = os.listdir(SDL_SETTING_JSON_DIR_PATH)
        file_name_list = [f for f in file_dir_list if os.path.isfile(os.path.join(SDL_SETTING_JSON_DIR_PATH, f))]

        tmp_asset_setting_list = []

        for file_name in file_name_list:

            basename_without_ext = os.path.splitext(os.path.basename(file_name))[0]

            with open(os.path.join(SDL_SETTING_JSON_DIR_PATH, file_name), 'r') as f:

                f_settings = json.load(f)

                f_settings['setting_type'] = basename_without_ext

                # json内のtargetDataPathに\n(改行)が含まれているので、リストにsplitして渡す
                if 'targetDataPath' in f_settings:
                    f_settings['targetDataPath'] = f_settings['targetDataPath'].split('\n')

                if 'priority' in f_settings:
                    priority = f_settings.get('priority')
                    if priority == "":
                        priority = "0"

                tmp_asset_setting_list.append({'priority': priority, 'settings': f_settings})

        sorted_asset_setting_list = sorted(tmp_asset_setting_list, key=lambda x: x["priority"], reverse=True)
        self.sg_asset_default_setting = [
            sorted_asset_setting.get('settings') for sorted_asset_setting in sorted_asset_setting_list]

    def get_scene_sg_asset_default_setting(self):
        u"""
        シーンのShotgridアセット情報取得用の設定を取得する
        将来的には共通フォーマットに置き換えたい

        Returns:
            [type]: {
                'code': シーンのshotgridアセット名,
                'target_list: shotgridAsset新規作成時のデフォルト設定リスト [
                    {
                        'field': shotgridのフィールド名,
                        'field_item': fieldに入る値
                    },
                    {
                        ...
                    }
                ],
                'specific_target_list': shotgridAsset検索時の対象リスト [
                    {
                        'field': shotgridのフィールド名,
                        'field_item': fieldに入る値
                    },
                    {
                        ...
                    }
                ]
            }

            ex) {
                'code': bdy1001_00,
                'target_list': [
                    {
                        'field': u'sg_glp_section',
                        'field_item': u'3DCGキャラ班'
                    },
                    {
                        'field': u'sg_glp_division',
                        'field_item': u'Body'
                    },
                    ...
                    {
                        'field': u'task_template',
                        'field_item': u'glp_3d_chara_body_unique'
                    }
                ],
                'specific_target_list': [
                    {
                        'field': u'sg_glp_section',
                        'field_item': u'3DCGキャラ班'
                    },
                    {
                        'field': u'sg_glp_division',
                        'field_item': u'Body'
                    }
                    ...
                ]
            }
        """

        target_setting = None

        if not self.sg_asset_default_setting:
            return None

        asset_path = Util.get_scene_name()
        if not asset_path:
            return None

        asset_path = asset_path.replace('\\', '/')
        asset_name = os.path.splitext(os.path.basename(asset_path))[0]
        # mdl_から始まるファイルのみ正規表現でファイル抽出
        if asset_name.find('mdl_') >= 0:
            match_obj = re.search(ASSET_NAME_REGEX, os.path.splitext(os.path.basename(asset_path))[0])
            if match_obj:
                asset_name = match_obj.group(0)

        # assetパスから該当する設定を取得
        for sorting_setting in self.sg_asset_default_setting:

            if 'targetDataPath' not in sorting_setting:
                continue

            setting_type = sorting_setting.get('setting_type')

            for target_data_path in sorting_setting['targetDataPath']:

                target_data_path = target_data_path.replace('\\', '/')
                if target_data_path not in asset_path:
                    continue

                target_setting = {
                    'code': asset_name,
                    'target_list': [],
                    'specific_target_list': []
                }

                for field_name_param in TARGET_SDL_SETTING_TERGET_KEY_PARAM_LIST:

                    field_name = sorting_setting.get(field_name_param.get('field_key'))
                    field_value_name = sorting_setting.get(field_name_param.get('value_key'))
                    is_search_target = field_name_param.get('is_search_target')

                    if not field_name or not field_value_name:
                        continue

                    if field_name == 'task_template':

                        if field_value_name.find('<SCRIPT>') >= 0:
                            field_value_name = self.__get_task_template(asset_name, setting_type)

                    elif field_value_name.find('<TEXT>') > -1:

                        if field_value_name.find('3d_motion_part_from_path') > -1:
                            part = self.__get_motion_part_from_path(asset_name)
                            if not part:
                                continue
                            field_value_name = part

                        elif field_value_name.find('3d_motion_division') > -1:

                            field_value_name = self.__get_motion_division(asset_name)

                        elif field_value_name.find('3d_motion_type') > -1:

                            match = re.search(r'_(type\d{2}|(chr|bdy|crd)\d{4})', asset_name)
                            if match:

                                this_value = match.group(1)
                                fix_value = this_value[0].upper() + this_value[1:]

                                if fix_value.find('Type') < 0:
                                    fix_value = 'Chara'

                                field_value_name = fix_value

                            else:

                                field_value_name = ''

                        elif field_value_name.find('<TEXT>chara_name</TEXT>') > -1:

                            field_value_name = self.__get_chara_name(asset_name)

                        elif field_value_name.find('3d_chara_name') > -1:

                            field_value_name = self.__get_chara_name(asset_name)

                        elif field_value_name.find('3d_chara_body_kind') > -1:

                            if asset_name.find('bdy0000') >= 0:
                                field_value_name = u'素体'

                            elif asset_name.find('bdy0') >= 0:
                                field_value_name = u'汎用衣装'

                            elif asset_name.find('_9') >= 0:
                                field_value_name = u'私服'

                            else:
                                field_value_name = u'勝負服'

                        elif field_value_name.find('3d_chara_head_kind') > -1:

                            if asset_name.find('chr0') >= 0:
                                field_value_name = u'モブ'

                            elif asset_name.find('mchr09') >= 0:
                                field_value_name = u'モブ'

                            elif asset_name.find('_00') >= 0:
                                field_value_name = u'通常'

                            elif asset_name.find('_99') >= 0:
                                field_value_name = u'すっぴん'

                            elif asset_name.find('_9') >= 0:
                                field_value_name = u'私服'

                            else:
                                field_value_name = u'勝負服'

                        elif field_value_name.find('3d_chara_attach_kind') > -1:
                            field_value_name = ''

                        elif field_value_name.find('3d_chara_tail_kind') > -1:

                            if asset_name.find('tail0') > -1:
                                field_value_name = u'汎用尻尾'
                            else:
                                field_value_name = u'固有尻尾'

                        elif field_value_name.find('3d_chara_id_kind') > -1:

                            match = re.search(r'(mchr|chr|bdy|crd|tail|attach)(\d{4}_\d{2})', asset_name)
                            if match:
                                field_value_name = match.group(2)
                            else:
                                field_value_name = ''

                        elif field_value_name.find('3d_chara_sub_kind') > -1:

                            field_value_name = self.__get_chara_sub(asset_name)

                        elif field_value_name.find('training_category') > -1:
                            pass

                        elif field_value_name.find('training_sub_category') > -1:
                            pass

                    target_data_dict = {
                        'field': field_name,
                        'field_item': field_value_name
                    }

                    target_setting['target_list'].append(target_data_dict)

                    if is_search_target:
                        target_setting['specific_target_list'].append(target_data_dict)

                break

            else:
                continue

            break

        if not target_setting:
            return None

        return target_setting

    def __get_chara_name(self, asset_name):
        u"""アセット名からキャラ名を取得する
        アセット名がcsv上に存在すればそれを取得して返す

        Args:
            asset_name ([type]): shotgrid用のアセット名(ex: bdy1001_00)

        Returns:
            [type]: キャラ名
        """

        csv_path = '{}\\csv\\chara_name.csv'.format(SDL_SETTING_JSON_DIR_PATH)
        if not os.path.exists(csv_path):
            return ''

        chara_name = u'該当なし'
        with open(csv_path, 'r') as csv_file:
            f = csv.reader(csv_file, delimiter=str(","), doublequote=True, lineterminator=str("\r\n"), quotechar=str('"'), skipinitialspace=True)
            next(f)  # header飛ばす
            for row in f:
                if asset_name.find(row[0]) == -1:
                    continue

                if sys.version_info.major == 2:
                    chara_name = row[1].decode('cp932')
                else:
                    chara_name = row[1]

        return chara_name

    def __get_chara_sub(self, asset_name):
        u"""アセット名からキャラの区分を取得する

        Args:
            asset_name ([type]): shotgrid用のアセット名(ex: bdy1001_00)

        Returns:
            [type]: キャラクターの区分(ex: Body, Head...等)
        """

        csv_path = '{}\\csv\\chara_sub_kind.csv'.format(SDL_SETTING_JSON_DIR_PATH)
        if not os.path.exists(csv_path):
            return ''

        match = re.search(r'(mchr|chr|bdy|crd|tail|attach)(\d{4})_(\d{2})', asset_name)
        if not match:
            return ''

        sub_id = str(int(match.group(3)))

        chara_sub = ''
        with open(csv_path, 'r') as csv_file:
            f = csv.reader(csv_file, delimiter=str(","), doublequote=True, lineterminator=str("\r\n"), quotechar=str('"'), skipinitialspace=True)
            next(f)  # header飛ばす

            for row in f:
                if sub_id != row[0]:
                    continue

                if sys.version_info.major == 2:
                    chara_sub = row[1].decode('cp932')
                else:
                    chara_sub = row[1]

        return chara_sub

    def __get_motion_division(self, asset_name):
        u"""アセット名からモーションのtypeを取得する

        Args:
            asset_name ([type]): shotgrid用のアセット名(ex: anm_eve_chr1001_00_act01)

        Returns:
            [type]: モーションのtype(ex: Camera, Body...等)
        """

        csv_path = '{}\\csv\\motion.csv'.format(SDL_SETTING_JSON_DIR_PATH)
        if not os.path.exists(csv_path):
            return None

        match = re.search(r'_(tail|ear|cam|add|plus)\D*?$', asset_name)
        if not match:
            return 'Body'

        tag = str(match.group(1))

        division = None
        with open(csv_path, 'r') as csv_file:
            f = csv.reader(csv_file, delimiter=str(","), doublequote=True, lineterminator=str("\r\n"), quotechar=str('"'), skipinitialspace=True)
            next(f)  # header飛ばす
            for row in f:
                if tag != row[0]:
                    continue

                if sys.version_info.major == 2:
                    division = row[1].decode('cp932')
                else:
                    division = row[1]

        return division

    def __get_motion_part_from_path(self, asset_name):
        u"""アセット名からモーションのパート分けを取得する

        Args:
            asset_name ([type]): shotgrid用のアセット名(ex: anm_eve_chr1001_00_act01)

        Returns:
            [type]: モーションのpart(ex: Event, Live...等)
        """

        csv_path = '{}\\csv\\motion.csv'.format(SDL_SETTING_JSON_DIR_PATH)
        if not os.path.exists(csv_path):
            return None

        part = None
        with open(csv_path, 'r') as csv_file:
            f = csv.reader(csv_file, delimiter=str(","), doublequote=True, lineterminator=str("\r\n"), quotechar=str('"'), skipinitialspace=True)
            next(f)  # header飛ばす
            for row in f:
                if '_{}_'.format(row[0]) not in asset_name:
                    continue

                if sys.version_info.major == 2:
                    part = row[1].decode('cp932')
                else:
                    part = row[1]

        return part

    def __get_task_template(self, asset_name, setting_type):
        u"""タスクテンプレート「名」を取得する
        利用する場合は別途タスクテンプレートエンティティから同名エンティティを取ってくる必要がある

        Args:
            asset_name ([type]): shotgrid用のアセット名(ex: anm_eve_chr1001_00_act01)
            setting_type ([type]): setting.jsonのファイル名

        Returns:
            [type]: タスクテンプレート名
        """

        if re.search(r'^chr', asset_name):

            if asset_name.find('chr0') >= 0 and asset_name.find('face') >= 0:
                return 'glp_3d_chara_mob_face'
            if asset_name.find('chr0') >= 0 and asset_name.find('hair') >= 0:
                return 'glp_3d_chara_mob_hair'
            if asset_name.find('_00') >= 0:
                return 'glp_3d_chara_head_default'

            return 'glp_3d_chara_head_unique'

        elif re.search(r'^bdy', asset_name):

            if asset_name.find('bdy0') >= 0:
                return 'glp_3d_chara_body_multi'

            return 'glp_3d_chara_body_unique'

        elif setting_type == '3d_motion_common':

            if asset_name.find('_liv_') >= 0:
                return 'glp_3d_motion_live'
            elif asset_name.find('cti_crd') >= 0:
                return 'glp_3d_motion_skillcutin'

            return 'glp_3d_motion_default'

        return None
