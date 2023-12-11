# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


try:
    # Maya 2022-
    from builtins import range
    from builtins import object
    from importlib import reload
except:
    pass

import os
import re

from . import part_info
from . import data_info
from ....base_common import utility as base_utility
from ...utility import model_id_finder as model_id_finder
from ...utility import model_define as model_define

import maya.cmds as cmds

reload(model_id_finder)
reload(model_define)


class CharaInfo(object):

    # ===============================================
    def __init__(self):
        """
        """

        self.__svn_model_root_dir_path = model_define.SVN_PATH

        # __initializeで無効化されてほしくないパラメータ
        self.bust_size = None

        self.__initialize()
        self.__part_info_initialize()

    # ===============================================
    def __initialize(self):
        """
        """

        self.exists = False

        self.file_path = None
        self.file_name = None
        self.file_name_without_ext = None
        self.file_ext = None
        self.file_exists = False

        self.unity_asset_dir_path = None

        self.data_type = None
        self.data_id = None
        self.data_main_id = None
        self.data_sub_id = None
        self.file_id = None

        self.is_unique_chara = False
        self.is_mini = False
        self.is_create_texture_variation = False
        self.is_create_asset_list = False
        self.is_use_extra_texture = True

        # headを対象としている時のtype(hair/face)
        self.head_type = None

        # キャラクター名やdescription等を格納するinfoクラス
        self.data_info = None

        self.__extra_option = {}
        self.__extra_value_dict_list = []

        self.file_dir = ''
        self.file_root_dir = ''
        self.type_dir = ''
        self.root_dir = ''

    # ===============================================
    def create_info(self, file_path='', unity_asset_path='',
                    is_create_all_info=False,
                    option={}, data_option={}):
        """
        キャラインフォを作成する
        file_path引数が未入力なら現在のシーンから、ファイル名だけならデフォルトパスからパスを作成

        :param file_path: ファイルパスかファイル名 unity_asset_path: Unityのアセットパス is_create_all_info: 関連infoも作成するか option: 特殊設定用dict
        """

        self.__initialize()
        self.__part_info_initialize()
        self.__extra_option = option

        # path関連の初期化
        self.__create_path(file_path, unity_asset_path)

        # 各種data_typeやidの取得
        is_done_create_settings = self.__create_param_settings()
        # パラメータが全て作成できていない場合は処理を中断する
        if not is_done_create_settings:
            return

        # 付加情報を作成。
        if self.is_unique_chara:
            self.__create_data_info(is_create_all_info, data_option)

        # 現在シーンのinfoを作成
        self.create_part_info(self.__extra_option)

        if not self.part_info.exists:
            return

        # 関連シーンのinfoを作成
        if is_create_all_info:
            self.create_all_info()

        self.exists = True

    # ===============================================
    def __create_data_info(self, is_create_all_info, data_option):
        """
        """

        temp_data_info = data_info.DataInfo()
        temp_data_info.create_info(
            self.data_main_id,
            self.data_sub_id,
            self.data_type,
            self.data_id,
            is_create_all_info)
        temp_data_info.update_info(data_option)

        self.data_info = temp_data_info

    # ===============================================
    def __create_path(self, file_path, unity_asset_path):
        """
        """

        # スクリプト関連
        script_file_path = os.path.abspath(__file__)
        script_chara_info_path = os.path.dirname(script_file_path)
        script_classeas_path = os.path.dirname(script_chara_info_path)
        self.script_root_path = os.path.dirname(script_classeas_path)

        # ファイル関連
        self.file_path = self.__optimize_file_path(file_path)
        if os.path.exists(self.file_path):
            self.file_exists = True
        self.file_name = os.path.basename(self.file_path)
        self.file_name_without_ext, self.file_ext = os.path.splitext(self.file_name)
        # ファイル自体のdir
        self.file_dir = os.path.dirname(self.file_path)
        # モデルIDのdir
        self.file_root_dir = os.path.dirname(self.file_dir)

        # Unity関連
        self.unity_asset_dir_path = unity_asset_path

    # ===============================================
    def __optimize_file_path(self, file_path):
        """
        ユーザーの入力に応じて、使用するファイルパスを変更する
        未入力=>現在シーン, ファイル名のみ=>デフォルトSVNパス, パス=>そのまま
        """

        fix_file_path = file_path

        # filePathが未入力の場合、自動的にファイルパスを開いているシーンから取得する
        if not fix_file_path:
            fix_file_path = cmds.file(q=True, sn=True)

        else:
            tmp_file_name = os.path.basename(fix_file_path)

            # ファイルパスがファイル名ならデフォルトのパスを採用
            if tmp_file_name == fix_file_path:

                if tmp_file_name.endswith(model_define.MAYA_EXT):
                    tmp_file_name = tmp_file_name + model_define.MAYA_EXT

                fix_file_path = model_id_finder.get_maya_file_path(tmp_file_name)

        return fix_file_path

    # ===============================================
    def create_part_info(self, option={}):
        """
        """

        temp_part_info = part_info.PartInfo()
        # part_infoがまだ無かったらpart_info=現在のinfoとする
        if self.part_info is None:
            self.part_info = temp_part_info

        # part_info作成時の引数dictの作成
        settings = self.__create_part_info_arg_dict(option)

        if not settings:
            return

        temp_part_info = part_info.PartInfo()
        temp_part_info.create_info(**settings)

        # このinfoの格納先を指定
        self.__allocation_parts_info_by_data_type(settings['data_type'], temp_part_info)

    # ===============================================
    def __create_part_info_arg_dict(self, override_setting_dict):
        """
        part_infoの引数になるdictを返す

        param: override_setting_dict: 初期値を上書きたい項目を記載したdict
        return: part_infoの引数になる設定dict
        """

        # dictの初期化
        settings = {
            'data_type': self.data_type,
            'head_type': self.head_type,
            'main_id': self.data_main_id,
            'sub_id': self.data_sub_id,
            'is_create_texture_variation': self.is_create_texture_variation,
            'is_create_model_list': self.is_create_asset_list,
            'is_use_extra_texture': self.is_use_extra_texture,
            'is_unique_chara': self.is_unique_chara,
            'unity_asset_dir_path': self.unity_asset_dir_path,
            'maya_root_dir_path': self.file_root_dir,
            'file_id': self.file_id,
            'data_id': self.data_id,
            'csv_path': None,
            'common_setting_csv_path': None,
        }

        # ユーザー定義の項目を上書き
        settings.update(override_setting_dict)

        # data_typeからcsvパスを更新
        csv_path, common_setting_csv_path = self.__create_csv_path(settings['data_type'])
        if not os.path.exists(csv_path):
            return
        settings.update({'csv_path': csv_path, 'common_setting_csv_path': common_setting_csv_path})

        # 特殊設定を受け渡す用のdictを作成
        self.__create_extra_value_dict_list()
        if self.__extra_value_dict_list:
            settings.update({'extra_value_dict_list': self.__extra_value_dict_list})

        # 可変要素置換用のdictを作成
        self.__create_variable_value_dict_list()
        if self.__variable_value_dict_list:
            settings.update({'variable_value_dict_list': self.__variable_value_dict_list})

        # maya_root_dir_path、data_id、file_idの更新
        file_name = model_id_finder.create_scene_name(
            settings['data_type'], settings['main_id'], settings['sub_id'])

        data_id = model_id_finder.get_data_id(file_name, settings['data_type'])
        file_id = model_id_finder.get_file_id(file_name, settings['data_type'])

        settings.update({
            'maya_root_dir_path': self.file_root_dir,
            'data_id': data_id,
            'file_id': file_id
        })

        return settings

    # ===============================================
    def __create_csv_path(self, data_type):
        """
        """

        csv_dir_path = self.script_root_path + '/_resource/chara_info'
        csv_file_name = '{0}_info.csv'.format(data_type)
        csv_path = '{0}/{1}'.format(csv_dir_path, csv_file_name)

        # 共通設定のcsvパス
        common_setting_csv_file_name = 'common_setting_{0}_info.csv'.format(data_type.split('_')[-1])
        common_setting_csv_path = '{0}/{1}'.format(csv_dir_path, common_setting_csv_file_name)

        return csv_path, common_setting_csv_path

    # ==============================================================================================
    # data_typeが増えたら追加する必要のある項目
    # ==============================================================================================
    def __part_info_initialize(self):
        """
        info用変数の初期化
        """

        # 現在の部位用
        self.part_info = None
        # アバター用
        self.avatar_part_info = None
        # ユニット用
        self.unit_part_info = None
        # 武器用
        self.weapon_part_info = None
        # 小物用
        self.prop_part_info = None
        # 召喚物用
        self.summon_part_info = None
        # 敵用
        self.enemy_part_info = None

        self.bust_size = None

    # ===============================================
    def __create_extra_value_dict_list(self):
        """
        バストサイズなどのidをキャラインフォ作成時に指定したい場合に使う
        現状farmで使用なし
        """

        extra_target_set = {
            'BUSTSIZE': self.bust_size,
        }

        self.__extra_value_dict_list = []

        for k, v in list(extra_target_set.items()):

            if v is None:
                continue

            self.__extra_value_dict_list.append({'name': k, 'value': v})

    # ===============================================
    def __create_variable_value_dict_list(self):
        """
        可変要素置換用のdictを作成
        """

        variable_dict_list = [
            {
                'name': 'WEAPON_PARTS_ID',
                'replace_str': '{}',
                'count': self.data_info.weapon_parts_count
            },
        ]

        self.__variable_value_dict_list = []

        for variable_dict in variable_dict_list:
            name = variable_dict['name']
            replace_str = variable_dict['replace_str']
            count = variable_dict['count']

            variable_value = {
                'name': name,
                'replace_str_list': [],
            }

            if count:
                replace_str_list = []

                for i in range(count):
                    replace_str_list.append(replace_str.format(i))

                variable_value.update({'replace_str_list': replace_str_list})

            self.__variable_value_dict_list.append(variable_value)

    # ===============================================
    def create_all_info(self, option={}):
        """
        関連モデルのinfoも作る
        一旦avatar, unit, weaponをセットで作る
        """

        if not self.is_unique_chara:
            return

        if not option:
            option = self.__extra_option

        self.avatar_part_info = None
        self.unit_part_info = None
        self.weapon_part_info = None

        # avatar
        settings = {'data_type': model_define.AVATAR_DATA_TYPE}
        _option = option.copy()
        _option.update(settings)
        self.create_part_info(_option)

        # unit
        settings = {'data_type': model_define.UNIT_DATA_TYPE}
        _option = option.copy()
        _option.update(settings)
        self.create_part_info(_option)

        # weapon
        # data_infoからweaponを持っているかを参照する
        # TODO: propにも応用
        if self.data_info.has_weapon:
            settings = {'data_type': model_define.WEAPON_DATA_TYPE}
            _option = option.copy()
            _option.update(settings)
            self.create_part_info(_option)

    # ===============================================
    def __allocation_parts_info_by_data_type(self, data_type, temp_parts_info):
        """
        """

        allocate_data_type = ''

        if data_type.endswith(model_define.AVATAR_DATA_TYPE):
            allocate_data_type = model_define.AVATAR_DATA_TYPE
            self.avatar_part_info = temp_parts_info

        elif data_type.endswith(model_define.UNIT_DATA_TYPE):
            allocate_data_type = model_define.UNIT_DATA_TYPE
            self.unit_part_info = temp_parts_info

        elif data_type.endswith(model_define.WEAPON_DATA_TYPE):
            allocate_data_type = model_define.WEAPON_DATA_TYPE
            self.weapon_part_info = temp_parts_info

        elif data_type.endswith(model_define.PROP_DATA_TYPE):
            allocate_data_type = model_define.PROP_DATA_TYPE
            self.prop_part_info = temp_parts_info

        elif data_type.endswith(model_define.SUMMON_DATA_TYPE):
            allocate_data_type = model_define.SUMMON_DATA_TYPE
            self.summon_part_info = temp_parts_info

        elif data_type.endswith(model_define.ENEMY_DATA_TYPE):
            allocate_data_type = model_define.ENEMY_DATA_TYPE
            self.enemy_part_info = temp_parts_info

        if self.data_type.endswith(allocate_data_type):
            self.part_info = temp_parts_info

    # ===============================================
    def __create_param_settings(self):
        """
        """

        if not self.file_name:
            return False

        data_types = model_id_finder.get_data_types(self.file_name)
        self.data_type = data_types[0]
        self.middle_data_type = data_types[1]
        self.short_data_type = data_types[2]

        if self.data_type == '':
            return False

        self.data_id = model_id_finder.get_data_id(self.file_name, self.data_type)
        self.file_id = model_id_finder.get_file_id(self.file_name, self.data_type)

        main_sub_ids = model_id_finder.get_main_sub_ids(self.data_id, self.data_type)
        self.data_main_id = main_sub_ids[0]
        self.data_sub_id = main_sub_ids[1]

        if self.data_main_id == '':
            return False

        # farmはいまのところ全部ユニーク
        self.is_unique_chara = True

        return True
