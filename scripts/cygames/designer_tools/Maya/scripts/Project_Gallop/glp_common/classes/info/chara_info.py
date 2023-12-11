# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import os
import re

from . import part_info
from . import data_info
from ....base_common import utility as base_utility

import maya.cmds as cmds


class CharaInfo(object):

    # ===============================================
    def __init__(self):
        """
        """

        self.__svn_model_root_dir_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model'

        # __initializeで無効化されてほしくないパラメータ
        self.skin_color = None
        self.hair_color = None
        self.bust_size = None
        self.tail_char_id = None
        self.sexdiff = None

        # 命名規則_Body
        self.body_type_lbls = ['普通', '細い', '太い']
        self.height_lbls = ['SS', 'M(S)', 'L', 'LL']
        self.bust_lbls = ['SS', 'S', 'M', 'L', 'LL']  # 通常キャラのバストサイズ
        self.mini_bust_lbls = ['SS, S', 'M', 'L, LL']  # ミニキャラのバストサイズ

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
        self.data_sex_id = None
        self.texture_sex_id = None
        self.file_id = None

        self.is_unique_chara = False
        self.is_mini = False
        self.is_create_asset_list = False
        self.is_use_extra_texture = True
        self.is_facial_target = False
        # Textureのバリエーションが存在するか
        self.is_create_variation = False
        # 汎用衣装か
        self.is_common_body = False

        # headを対象としている時のtype(hair/face)
        self.head_type = None

        # キャラクター名やdescription等を格納するinfoクラス
        self.data_info = None

        # mini alternative_info用パラメータ
        # 何も設定しない限りはこれが初期値になる
        self.is_use_alternative_info = False
        self.alternative_hair_id = '1001'
        self.alternative_hair_sub_id = '00'
        self.alternative_face_id = '0001'
        self.alternative_face_sub_id = '00'
        self.alternative_face_num = '0'

        self.__extra_option = {}
        self.__extra_value_dict_list = []

        self.file_dir = ''
        self.file_root_dir = ''
        self.type_dir = ''
        self.root_dir = ''

        self.facial_target_path = ''

        self.__reference_name = ''

        self.middle_data_type = ''
        self.short_data_type = ''

    # ===============================================
    def create_info(self, file_path='', unity_asset_path='', is_create_all_info=False, option={}, reference_namespace=''):
        """
        """

        self.__initialize()
        self.__part_info_initialize()

        # dress_dataの為に仮のdata_infoを作成
        # data_idとdata_sub_idはこの時点ではNoneが渡される
        self.__create_data_info()

        self.__extra_option = option
        self.__reference_name = reference_namespace

        # filePathが未入力の場合、自動的にファイルパスを開いているシーンから取得する
        if not file_path:
            file_path = cmds.file(q=True, sn=True, exn=True)
            if not file_path:
                return

        self.file_path = file_path
        self.file_exists = os.path.exists(file_path)

        self.unity_asset_dir_path = unity_asset_path

        self.__create_path()

        is_done_create_settings = self.__create_param_settings()
        # パラメータが全て作成できていない場合は処理を中断する
        if not is_done_create_settings:
            return

        self.__create_dir_path()

        if self.is_unique_chara:
            self.__create_data_info()

        self.create_part_info(self.__extra_option)

        # part_infoがexistsにならない場合は処理を中断する
        if not self.part_info.exists:
            return

        if is_create_all_info:
            self.create_all_info()

        # mini頭 特殊対応
        self.create_mini_alternative_head_info(**self.__extra_option)

        self.exists = True

    # ===============================================
    def create_mini_alternative_head_info(self, **keywords):
        """
        mini頭 特殊対応
        主にmaterial_link_listを作成するためのinfo取得
        """

        self.__set_mini_alternative_param(**keywords)

        # part_infoが出来ていない状態では作れない
        if not self.part_info or not self.part_info.exists:
            return

        if not self.is_mini:
            return

        if not self.data_type.endswith('_hair_head') and not self.data_type.endswith('_face_head'):
            return

        if self.is_use_alternative_info:

            if self.data_type == 'mini_hair_head':

                settings = {
                    'data_type': 'mini_face_head',
                    'data_id': 'mchr{0}_{1}_face{2}'.format(
                        self.alternative_face_id,
                        self.alternative_face_sub_id,
                        self.alternative_face_num
                    ),
                    'main_id': self.alternative_face_id,
                    'sub_id': self.alternative_face_sub_id
                }

            elif self.data_type == 'mini_audience_hair_head':

                self.alternative_face_id = '0900'
                self.alternative_face_sub_id = '00'
                self.alternative_face_num = '0'

                settings = {
                    'data_type': 'mini_face_head',
                    'data_id': 'mchr{0}_{1}_face{2}'.format(
                        self.alternative_face_id,
                        self.alternative_face_sub_id,
                        self.alternative_face_num
                    ),
                    'main_id': self.alternative_face_id,
                    'sub_id': self.alternative_face_sub_id
                }

            elif self.data_type == 'mini_face_head':

                settings = {
                    'data_type': 'mini_hair_head',
                    'data_id': 'mchr{0}_{1}_hair'.format(
                        self.alternative_hair_id,
                        self.alternative_hair_sub_id
                    ),
                    'main_id': self.alternative_hair_id,
                    'sub_id': self.alternative_hair_sub_id
                }

            elif self.data_type == 'mini_audience_face_head':

                self.alternative_hair_id = '0901'
                self.alternative_hair_sub_id = '00'

                settings = {
                    'data_type': 'mini_hair_head',
                    'data_id': 'mchr{0}_{1}_hair'.format(
                        self.alternative_hair_id,
                        self.alternative_hair_sub_id
                    ),
                    'main_id': self.alternative_hair_id,
                    'sub_id': self.alternative_hair_sub_id
                }

            _option = self.__extra_option
            if 'option' in keywords:
                _option = keywords['option']

            settings.update(_option)

            self.create_part_info(settings)

    # ===============================================
    def __set_mini_alternative_param(self, **keywords):
        """
        """

        if 'hair_id' in keywords:
            self.alternative_hair_id = keywords['hair_id']
        if 'hair_sub_id' in keywords:
            self.alternative_hair_sub_id = keywords['hair_sub_id']
        if 'face_id' in keywords:
            self.alternative_face_id = keywords['face_id']
        if 'face_sub_id' in keywords:
            self.alternative_hair_sub_id = keywords['face_sub_id']
        if 'face_num' in keywords:
            self.alternative_face_num = keywords['face_num']

    # ===============================================
    def __create_data_info(self):
        """
        """
        temp_data_info = data_info.DataInfo()
        temp_data_info.create_info(self.data_main_id, self.data_sub_id)

        self.data_info = temp_data_info

    # ===============================================
    def __create_path(self):
        """
        """

        script_file_path = os.path.abspath(__file__)
        script_chara_info_path = os.path.dirname(script_file_path)
        script_classeas_path = os.path.dirname(script_chara_info_path)
        self.script_root_path = os.path.dirname(script_classeas_path)

        self.file_name = os.path.basename(self.file_path)
        self.file_name_without_ext, self.file_ext = os.path.splitext(self.file_name)

    # ===============================================
    def __create_dir_path(self):
        """
        """

        # ファイル自体のdir
        # face/hair階層を挟む場合があるので、その場合はもう一つ下を見る
        # 通常モデル -> 01_model/body/bdy1001_00/scenes
        # Mini      -> 01_model/mini/body/mbdy1001_00/scenes
        self.file_dir = os.path.dirname(self.file_path)
        # モデルIDのdir
        # 通常モデル -> 01_model/body/bdy1001_00
        # Mini      -> 01_model/mini/body/mbdy1001_00
        self.file_root_dir = os.path.dirname(self.file_dir)

        # envの場合はスキップ
        if self.data_type.startswith('bg_'):
            return

        if not self.file_root_dir.endswith('{0}_{1}'.format(self.data_main_id, self.data_sub_id)):
            self.file_root_dir = os.path.dirname(self.file_root_dir)

    # ===============================================
    def __create_replace_str_dict(self, settings):
        """
        """

        replace_str_dict = {
            'head': {'middle': 'head', 'short': 'chr', 'main_id': settings['main_id'], 'sub_id': settings['sub_id']},
            'body': {'middle': 'body', 'short': 'bdy', 'main_id': settings['main_id'], 'sub_id': settings['sub_id']},
            'tail': {'middle': 'tail', 'short': 'tail', 'main_id': settings['main_id'], 'sub_id': settings['sub_id']}
        }

        return replace_str_dict

    # ===============================================
    def __create_file_and_data_id(self, settings):
        """
        特別衣装、顔、特別尻尾、汎用尻尾のfile_idとdata_idを作成する
        """

        file_id = self.file_id
        data_id = self.data_id

        if self.data_type != settings['data_type']:

            replace_str_dict = self.__create_replace_str_dict(settings)

            short_data_type = settings['data_type'].split('_')[-1]

            id_prefix = ''
            if 'is_mini' in settings and settings['is_mini']:
                id_prefix = 'm'

            if short_data_type in replace_str_dict:

                temp_id = '{0}{1}{2}_{3}'.format(
                    id_prefix,
                    replace_str_dict[short_data_type]['short'],
                    replace_str_dict[short_data_type]['main_id'],
                    replace_str_dict[short_data_type]['sub_id']
                )

                file_id = temp_id
                data_id = temp_id

        return file_id, data_id

    # ===============================================
    def __validate_path(self, settings):
        """
        """

        maya_root_dir_path = self.file_root_dir

        if self.data_type == settings['data_type']:

            return maya_root_dir_path

        replace_str_dict = self.__create_replace_str_dict(settings)

        short_data_type = settings['data_type'].split('_')[-1]

        if short_data_type not in replace_str_dict:
            return ''

        middle_replace_str = replace_str_dict[short_data_type]['middle']
        short_replace_str = replace_str_dict[short_data_type]['short']

        maya_root_dir_path = re.sub(self.middle_data_type, middle_replace_str, maya_root_dir_path)
        maya_root_dir_path = re.sub(self.short_data_type, short_replace_str, maya_root_dir_path)

        if os.path.exists(maya_root_dir_path) and \
            self.data_main_id == replace_str_dict[short_data_type]['main_id'] and \
                self.data_sub_id == replace_str_dict[short_data_type]['sub_id']:
            return maya_root_dir_path

        data_main_id = replace_str_dict[short_data_type]['main_id']
        data_sub_id = replace_str_dict[short_data_type]['sub_id']

        mini_path = ''
        mini_prefix = ''
        if self.is_mini:
            mini_path = 'mini/'
            mini_prefix = 'm'

        maya_root_dir_path = '{0}/{1}{2}/{3}{4}{5}_{6}'.format(
            self.__svn_model_root_dir_path,
            mini_path,
            middle_replace_str,
            mini_prefix,
            short_replace_str,
            data_main_id,
            data_sub_id
        )

        if os.path.exists(maya_root_dir_path):
            return maya_root_dir_path

        return ''

    # ===============================================
    def create_part_info(self, option={}):
        """
        """

        temp_part_info = part_info.PartInfo()
        # part_infoがまだ無かったらpart_info=現在のinfoとする
        if self.part_info is None:
            self.part_info = temp_part_info

        settings = {
            'data_type': self.data_type,
            'head_type': self.head_type,
            'main_id': self.data_main_id,
            'sub_id': self.data_sub_id,
            'is_create_variation': self.is_create_variation,
            'is_create_model_list': self.is_create_asset_list,
            'is_use_extra_texture': self.is_use_extra_texture,
            'is_unique_chara': self.is_unique_chara,
            'is_mini': self.is_mini,
            'unity_asset_dir_path': self.unity_asset_dir_path,
            'texture_sex_id': self.texture_sex_id,
            'reference_name': self.__reference_name
        }
        settings.update(option)

        csv_path, common_setting_csv_path = self.__create_csv_path(settings['data_type'])
        if not os.path.exists(csv_path):
            return
        settings.update({'csv_path': csv_path, 'common_setting_csv_path': common_setting_csv_path})

        maya_root_dir_path = self.file_root_dir
        file_id = self.file_id
        data_id = self.data_id
        if self.is_unique_chara or self.is_use_alternative_info:
            maya_root_dir_path = self.__validate_path(settings)
        if self.is_unique_chara:
            file_id, data_id = self.__create_file_and_data_id(settings)
        settings.update({
            'maya_root_dir_path': maya_root_dir_path,
            'file_id': file_id,
            'data_id': data_id
        })

        self.__create_extra_value_dict_list()
        if self.__extra_value_dict_list:
            settings.update({'extra_value_dict_list': self.__extra_value_dict_list})

        temp_part_info = part_info.PartInfo()
        temp_part_info.create_info(**settings)

        self.__allocation_parts_info_by_data_type(settings['data_type'], temp_part_info)

    # ===============================================
    def __create_csv_path(self, data_type):
        """
        """

        csv_dir_path = self.script_root_path + '/_resource/chara_info'
        csv_file_name = '{0}_info.csv'.format(data_type)
        csv_path = '{0}/{1}'.format(csv_dir_path, csv_file_name)

        # 共通設定のcsvパス
        common_setting_csv_file_name = ''
        if self.is_mini:
            if data_type == 'mini_face_head':
                common_setting_csv_file_name = 'common_setting_mini_face_head_info.csv'
            elif data_type == 'mini_hair_head':
                common_setting_csv_file_name = 'common_setting_mini_hair_head_info.csv'
            else:
                common_setting_csv_file_name = 'common_setting_mini_{0}_info.csv'.format(data_type.split('_')[-1])
        else:
            common_setting_csv_file_name = 'common_setting_{0}_info.csv'.format(data_type.split('_')[-1])

        common_setting_csv_path = '{0}/{1}'.format(csv_dir_path, common_setting_csv_file_name)

        return csv_path, common_setting_csv_path

    # ==============================================================================================
    # data_typeが増えたら追加する必要のある項目
    # ==============================================================================================
    def __part_info_initialize(self):
        """
        info用変数の初期化
        head、body、tailのそれぞれのInfoはMiniも共通で利用する
        """

        # 現在の部位用
        self.part_info = None
        # Head用
        self.head_part_info = None
        # body用
        self.body_part_info = None
        # tail用
        self.tail_part_info = None
        # prop用
        self.prop_part_info = None
        # toon_prop用
        self.toon_prop_part_info = None
        # attach用
        self.attach_part_info = None

        # mini用
        self.alternative_info = None

        self.skin_color = None
        self.hair_color = None
        self.bust_size = None
        self.sexdiff = None

    # ===============================================
    def __create_extra_value_dict_list(self):
        """
        """

        extra_target_set = {
            'SKINCOLOR': self.skin_color,
            'HAIRCOLOR': self.hair_color,
            'BUSTSIZE': self.bust_size,
            'CHAR_ID': self.tail_char_id,
            'SEXDIFF': self.data_sex_id
        }

        self.__extra_value_dict_list = []

        for k, v in list(extra_target_set.items()):

            if v is None:
                continue

            self.__extra_value_dict_list.append({'name': k, 'value': v})

    # ===============================================
    def create_all_info(self, option={}):
        """
        全てのdata_typeのpart_infoを取得する
        但しpropはpropの時のみ必要なので取得しない
        """

        # モブ顔は対応する体が、汎用衣装は対応する顔が存在しないため、infoを作成しない
        if not self.is_unique_chara:
            return

        if not option:
            option = self.__extra_option

        self.head_part_info = None
        self.body_part_info = None
        self.tail_part_info = None
        self.attach_part_info = None

        body_type_prefix = ''
        head_type_prefix = ''
        if self.is_mini:
            body_type_prefix = 'mini_'
            head_type_prefix = 'mini_hair_'

        # head
        settings = {'data_type': '{0}head'.format(head_type_prefix)}
        # 元の呼び出しがbodyタイプな場合でdress_head_sub_idがNoneではない場合
        # headの特定が出来るのでdress_head_sub_idをsub_idとして登録
        if self.part_info.data_type.endswith('body') and self.data_info.dress_head_sub_id is not None:
            settings['sub_id'] = self.data_info.dress_head_sub_id
        # 元の呼び出しがattachの場合、sub_idはアタッチ固有なので00で呼び出す
        elif self.part_info.data_type.endswith('attach'):
            settings['sub_id'] = '00'
        _option = option.copy()
        _option.update(settings)
        self.create_part_info(_option)

        # body
        settings = {'data_type': '{0}body'.format(body_type_prefix)}
        # 元の呼び出しがattachの場合、sub_idはアタッチ固有なので00で呼び出す
        if self.part_info.data_type.endswith('attach'):
            settings['sub_id'] = '00'
        _option = option.copy()
        _option.update(settings)
        self.create_part_info(_option)

        # attach
        if not str(self.data_info.attachment_model_id) == '-1':
            settings = {'data_type': '{0}general_body_attach'.format(body_type_prefix)}
            settings['sub_id'] = str(self.data_info.attachment_model_id).zfill(2)
            _option = option.copy()
            _option.update(settings)
            self.create_part_info(_option)

        # tail
        settings = {}

        if self.data_info.dress_tail_model_id is not None and self.data_info.dress_tail_model_sub_id is not None:

            if str(self.data_info.dress_tail_model_id) == '-1':

                # general_tailを取得する
                settings = {
                    'data_type': '{0}general_tail'.format(body_type_prefix),
                    'main_id': '0001',
                    'sub_id': '00',
                    'is_unique_chara': False
                }

            elif str(self.data_info.dress_tail_model_id) == str(self.data_main_id) and \
                    str(self.data_info.dress_tail_model_sub_id) == str(self.data_sub_id):

                # 特殊尻尾を取得する
                settings = {
                    'data_type': '{0}tail'.format(body_type_prefix),
                    'main_id': self.data_info.dress_tail_model_id,
                    'sub_id': self.data_info.dress_tail_model_sub_id
                }

            else:

                # 特殊尻尾(tail_model_id_00)を取得する
                settings = {
                    'data_type': '{0}tail'.format(body_type_prefix),
                    'main_id': self.data_info.dress_tail_model_id,
                    'sub_id': '00'
                }

        elif str(self.data_info.chara_tail_model_id) == '1':

            # general_tailを取得する
            settings = {
                'data_type': '{0}general_tail'.format(body_type_prefix),
                'main_id': '0001',
                'sub_id': '00',
                'is_unique_chara': False
            }

        if not settings:
            return

        _option = option.copy()
        _option.update(settings)
        self.create_part_info(_option)

    # ===============================================
    def __allocation_parts_info_by_data_type(self, data_type, temp_parts_info):
        """
        """

        allocate_data_type = ''

        if data_type.endswith('head'):
            allocate_data_type = 'head'
            self.head_part_info = temp_parts_info

        elif data_type.endswith('body'):
            allocate_data_type = 'body'
            self.body_part_info = temp_parts_info

        elif data_type.endswith('tail'):
            allocate_data_type = 'tail'
            self.tail_part_info = temp_parts_info

        elif data_type.endswith('toon_prop'):
            allocate_data_type = 'toon_prop'
            self.toon_prop_part_info = temp_parts_info

        elif data_type.endswith('prop'):
            allocate_data_type = 'prop'
            self.prop_part_info = temp_parts_info

        elif data_type.endswith('attach'):
            allocate_data_type = 'attach'
            self.attach_part_info = temp_parts_info

        # mini特殊対応
        if self.is_use_alternative_info and self.data_type != data_type:
            self.alternative_info = temp_parts_info
            return

        if self.data_type.endswith(allocate_data_type):
            self.part_info = temp_parts_info

    # ===============================================
    def __create_param_settings(self):
        """
        """

        if not self.file_name:
            return False

        # Env系のファイルの場合別箇所で分類
        if self.file_name.startswith('mdl_env'):
            return self.__create_env_param_settings()

        self.data_id = ''

        # 性別差分対応
        # 0=通常、1=牡馬牝馬差分あり、2=牡馬牝馬差分あり特殊仕様
        use_gender = 0

        if self.file_name.find('_toon_prop') >= 0:

            self.middle_data_type = 'toon_prop'
            self.short_data_type = 'toon_prop'

            self.data_type = 'toon_prop'
            self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'toon_prop\d{4}_\d{2}')
            self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'toon_prop[^.]*')

        elif self.file_name.find('_chr_prop') >= 0:

            self.middle_data_type = 'prop'
            self.short_data_type = 'prop'

            # キャラ小物
            self.data_type = 'prop'
            self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'chr_prop\d{4}_\d{2}')
            self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'chr_prop[^.]*')

        elif self.file_name.find('attach') >= 0:

            self.middle_data_type = 'attach'
            self.short_data_type = 'attach'

            # miniアタッチ
            if self.file_name.find('_mattach') >= 0:
                self.data_type = 'mini_general_body_attach'
                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'mattach\d{4}_\d{2}')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'mattach[^.]*')
                self.is_mini = True
                self.is_unique_chara = True

            # 通常キャラアタッチ
            elif self.file_name.find('_attach') >= 0:
                self.data_type = 'general_body_attach'
                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'attach\d{4}_\d{2}')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'attach[^.]*')
                self.is_unique_chara = True

        elif self.file_name.find('chr') >= 0:

            self.middle_data_type = 'head'
            self.short_data_type = 'chr'

            # 観客頭部 ※暫定対応
            if self.file_name.find('_mchr09') >= 0:

                if self.file_name.find('_face') >= 0:
                    self.data_type = 'mini_audience_face_head'
                elif self.file_name.find('_hair') >= 0:
                    self.data_type = 'mini_audience_hair_head'
                    self.is_unique_chara = True

                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'mchr\d{4}_\d{2}_[A-Za-z]*(\d|)')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'mchr[^.]*')
                self.is_mini = True
                self.is_use_alternative_info = True

            # Mini頭部
            elif self.file_name.find('_mchr') >= 0:

                if self.file_name.find('_face') >= 0:
                    self.data_type = 'mini_face_head'
                elif self.file_name.find('_hair') >= 0:
                    self.data_type = 'mini_hair_head'
                    self.is_unique_chara = True

                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'mchr\d{4}_\d{2}_[A-Za-z]*(\d|)')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'mchr[^.]*')
                self.is_mini = True
                self.is_use_alternative_info = True

            # Mob頭部
            elif self.file_name.find('_chr0001') >= 0 or self.file_name.find('_chr0900') >= 0:

                if self.file_name.find('_face') >= 0:
                    self.data_type = 'mob_face_head'
                elif self.file_name.find('_hair') >= 0:
                    self.data_type = 'mob_hair_head'

                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'chr\d{4}_\d{2}_\D*\d{3}')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'chr[^.]*')
                self.is_create_variation = True

            # 通常頭部
            elif self.file_name.find('_chr') >= 0:
                self.data_type = 'head'
                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'chr\d{4}_\d{2}')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'chr[^.]*')
                self.is_unique_chara = True

                if self.file_name_without_ext.endswith('_facial_target'):
                    self.is_facial_target = True
                    self.facial_target_path = self.file_path
                else:
                    self.facial_target_path = os.path.dirname(self.file_path) + '/mdl_' + self.data_id + '_facial_target.ma'

            if self.file_name.find('_face') >= 0:
                self.head_type = 'face'
            elif self.file_name.find('_hair') >= 0:
                self.head_type = 'hair'

        elif self.file_name.find('bdy') >= 0:

            self.middle_data_type = 'body'
            self.short_data_type = 'bdy'

            # 汎用衣装対応 data_infoからdress_param_listを読み込み、gender_typeを使うかどうかを判断
            is_wet = True
            if self.file_name.find('bdy00') >= 0:

                tmp_main_id = None
                tmp_sub_id = None
                tmp_sex_id = None
                tmp_data_id_match_obj = re.search(r'bdy(\d{4})_(\d{2})', self.file_name)

                if tmp_data_id_match_obj:
                    tmp_main_id = int(tmp_data_id_match_obj.group(1))
                    tmp_sub_id = int(tmp_data_id_match_obj.group(2))

                for dress_param in self.data_info.dress_param_list:
                    if dress_param['body_type'] != tmp_main_id or dress_param['body_type_sub'] != tmp_sub_id:
                        continue

                    use_gender = dress_param['use_gender']
                    if dress_param['is_wet'] == 0:
                        is_wet = False

                    break

            # Mini衣装
            if self.file_name.find('_mbdy') >= 0:

                # 観客衣装
                if self.file_name.find('_mbdy09') >= 0:

                    self.data_type = 'mini_body'
                    self.is_unique_chara = True

                # 性別差分付き汎用衣装
                elif use_gender == 2:

                    self.data_type = 'mini_general_sexdiff_body'
                    self.is_create_variation = True
                    self.is_common_body = True

                # 汎用衣装
                elif self.file_name.find('_mbdy0') >= 0:

                    self.data_type = 'mini_general_body'
                    self.is_create_variation = True
                    self.is_common_body = True

                # 特別衣装
                else:

                    self.data_type = 'mini_body'
                    self.is_unique_chara = True

                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'mbdy\d{4}_\d{2}(_\d{2}|)')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'mbdy[^.]*')
                self.is_mini = True

            # 素体 ※SSR扱い
            elif self.file_name.find('_bdy0000') >= 0:

                self.data_type = 'body'
                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'bdy\d{4}_\d{2}')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'bdy[^.]*')

            # 汎用衣装
            elif self.file_name.find('_bdy0') >= 0:

                # 体操服
                if self.file_name.find('_bdy0001') >= 0:
                    self.data_type = 'bdy0001_body'
                # バックダンサー衣装
                elif self.file_name.find('_bdy0006') >= 0:
                    self.data_type = 'bdy0006_body'
                # 水着バックダンサー衣装
                # バックダンサー衣装と微妙に仕様が異なるため、別ファイルに
                elif self.file_name.find('_bdy0009') >= 0:
                    self.data_type = 'bdy0009_body'
                # パジャマ・正装
                # テクスチャサイズが違ったり複数のエリアが刺さるようになったりしているため、別ファイルに
                elif self.file_name.find('_bdy0013') >= 0 or self.file_name.find('_bdy0014') >= 0:
                    self.data_type = 'general_multi_area_body'
                # 性別差分つき汎用衣装
                elif use_gender == 2:
                    self.data_type = 'general_sexdiff_body'
                # 上記以外の衣装
                else:
                    self.data_type = 'general_body'

                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'bdy\d{4}_\d{2}_\d{2}')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'bdy[^.]*')
                self.is_create_variation = True
                self.is_create_asset_list = True
                self.is_common_body = True

            # 特別衣装
            elif self.file_name.find('_bdy') >= 0:

                self.data_type = 'body'
                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'bdy\d{4}_\d{2}')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'bdy[^.]*')
                self.is_unique_chara = True

        elif self.file_name.find('tail') >= 0:

            self.middle_data_type = 'tail'
            self.short_data_type = 'tail'

            # Mini尻尾
            if self.file_name.find('_mtail0') >= 0:
                self.data_type = 'mini_general_tail'
                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'mtail\d{4}_\d{2}')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'mtail[^.]*')
                self.is_mini = True

            # 汎用尻尾
            elif self.file_name.find('_tail0') >= 0:
                self.data_type = 'general_tail'
                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'tail\d{4}_\d{2}')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'tail[^.]*')

            # 特別尻尾
            elif self.file_name.find('_tail') >= 0:
                self.data_type = 'tail'
                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'tail\d{4}_\d{2}')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'tail[^.]*')

            # Mini特別尻尾
            elif self.file_name.find('_mtail1') >= 0:
                self.data_type = 'mini_tail'
                self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'mtail\d{4}_\d{2}')
                self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'mtail[^.]*')
                self.is_mini = True

        else:
            return False

        match_obj = re.search(r'([0-9]{4})_([0-9]{2})(_[0-9]{2}|)', self.data_id)
        if match_obj:
            self.data_main_id = match_obj.group(1)
            self.data_sub_id = match_obj.group(2)
            data_sex_id = match_obj.group(3).replace('_', '')
            self.data_sex_id = data_sex_id if data_sex_id != '' else None

            # 性別差分対応
            self.texture_sex_id = self.__get_texture_sex_id(use_gender)
        else:
            return False

        return True

    # ===============================================
    def __create_env_param_settings(self):

        self.data_id = ''

        # live(common)
        if re.match(r'mdl_env_cutin\d{4}_\d{2}_\d{2}.*_toon', self.file_name):

            self.middle_data_type = 'bg_toon'
            self.short_data_type = 'toon_prop'

            self.data_type = 'bg_toon_prop'
            self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'cutin\d{4}_\d{2}_\d{2}')
            self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'cutin[^.]*')

            match_obj = re.search(r'([0-9]{4})_([0-9]{2}_[0-9]{2})', self.data_id)
            if match_obj:
                self.data_main_id = match_obj.group(1)
                self.data_sub_id = match_obj.group(2)

        # cutin
        elif re.match(r'mdl_env_live_cmn_prop\d{3}_toon', self.file_name):
            self.middle_data_type = 'bg_toon'
            self.short_data_type = 'toon_prop'

            self.data_type = 'bg_toon_prop'
            self.data_id = base_utility.string.get_string_by_regex(self.file_name, r'prop\d{3}')
            self.file_id = base_utility.string.get_string_by_regex(self.file_name, r'prop[^.]*')

            match_obj = re.search(r'[0-9]{3}', self.data_id)
            if match_obj:
                self.data_main_id = match_obj.group()
                self.data_sub_id = ''

        else:
            return False

        return True

    def __get_texture_sex_id(self, use_gender):
        """テクスチャの性別差分変換用idを取得する

        args:
            use_gender: dress_data.csvのuse_genderの項目
                        0=性別差分なし(特殊性別差分除く、例えば太り気味体系とか)
                        1=性別差分あり(ジャージ等の牝牡差がある汎用衣装)
                        2=特殊性別差分(現在未使用)
        """

        texture_sex_id = None

        if use_gender == 0:
            texture_sex_id = self.data_sex_id
        elif use_gender == 1:
            # テクスチャは今の所牝馬牡馬共通する仕様の為、
            if self.data_sex_id == '01' or self.data_sex_id == '02':
                texture_sex_id = '00'
            elif self.data_sex_id == '04' or self.data_sex_id == '05':
                texture_sex_id = '03'
            else:
                texture_sex_id = self.data_sex_id

        return texture_sex_id

    def debug_all(self):
        for attr in dir(self):
            if attr.startswith('__') or callable(getattr(self, attr)):
                continue
            print('#' * 20)
            print(attr)
            print(getattr(self, attr))
