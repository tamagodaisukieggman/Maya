# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
    from builtins import str
    from builtins import range
    from builtins import object
except Exception:
    pass

import os
import re

import maya.cmds as cmds

from ....base_common import classes as base_class


class PartInfo(object):

    # ===============================================
    def __init__(self):
        """
        """

        self.exists = False

        self.data_type = None
        self.head_type = None
        self.file_type = None
        self.data_id = None
        self.main_id = None
        self.sub_id = None
        self.file_id = None
        self.top_node = None

        self.is_mini = False
        self.is_unique_chara = False

        self.__is_create_variation = False
        self.__is_create_model_list = False
        self.__is_use_extra_texture = True

        self.__unity_asset_dir_path = None
        self.__script_file_path = None
        self.__script_dir_path = None
        self.__script_root_path = None

        self.__csv_dir_path = None
        self.__csv_file_name = None
        self.__csv_path = None

        self.__extra_value_dict_list = []

        self.csv_reader = None

        # データ一覧
        # param_list = 全要素
        # list = Nameのみ
        self.mesh_list = []
        self.mesh_param_list = []
        self.outline_mesh_list = []
        self.outline_mesh_param_list = []
        self.joint_list = []
        self.joint_param_list = []
        self.material_list = []
        self.material_param_list = []
        self.texture_list = []
        self.texture_param_list = []
        self.all_texture_list = []
        self.all_texture_param_list = []
        self.psd_param_list = []
        self.psd_list = []
        self.locator_list = []
        self.locator_param_list = []
        self.cloth_list = []
        self.cloth_param_list = []
        self.flare_list = []
        self.flare_param_list = []
        self.all_flare_list = []
        self.all_flare_param_list = []
        self.extensions_list = []
        self.extensions_param_list = []

        self.maya_dir_list = []
        self.maya_dir_param_list = []
        self.maya_file_list = []
        self.maya_file_param_list = []

        self.model_list = []
        self.model_param_list = []
        self.all_model_list = []
        self.all_model_param_list = []

        self.material_link_list = []

        self.root_node = ''

        self.maya_root_dir_path = ''
        self.maya_scenes_dir_path = ''
        self.maya_sourceimages_dir_path = ''
        self.maya_clothes_dir_path = ''
        self.maya_flares_dir_path = ''
        self.maya_extensions_dir_path = ''

        # 部位毎の共通設定
        self.normal_bone_limit = 10000
        self.sp_bone_limit = 10000
        self.polygon_limit = 10000
        self.hip_original_translate = None
        self.model_num_list = []
        self.model_num_param_list = []

        self.__replace_item_dict_list = []
        self.__extra_replace_item_dict_list = []

        self.TEX_TYPE_LIST = [
            'diff', 'base', 'ctrl', 'shad_c',
            'dirt', 'diff_wet', 'base_wet', 'ctrl_wet', 'shad_c_wet',
            'emissive', 'emissive_wet', 'area', 'area_wet', 'reflection',
        ]

    # ===============================================
    def create_info(self,
                    data_type, head_type,
                    data_id, main_id, sub_id, file_id,
                    is_unique_chara, is_mini,
                    is_create_variation, is_create_model_list, is_use_extra_texture,
                    unity_asset_dir_path, maya_root_dir_path, csv_path, common_setting_csv_path,
                    texture_sex_id, reference_name, **kwargs):
        """
        """

        if not data_type or not main_id or not sub_id:
            # bg_系の場合は、sub_idが空の場合もあるためその場合は通す
            if not (data_type and data_type.startswith('bg_') and not sub_id):
                return

        self.data_type = data_type
        self.head_type = head_type
        self.data_id = data_id
        self.main_id = main_id
        self.sub_id = sub_id
        self.file_id = file_id
        self.is_unique_chara = is_unique_chara
        self.is_mini = is_mini
        self.texture_sex_id = texture_sex_id
        self.__is_create_variation = is_create_variation
        self.__is_create_model_list = is_create_model_list
        self.__is_use_extra_texture = is_use_extra_texture
        self.__unity_asset_dir_path = unity_asset_dir_path
        self.__csv_path = csv_path
        self.__common_setting_csv_path = common_setting_csv_path
        self.__reference_name = reference_name

        self.maya_root_dir_path = maya_root_dir_path

        if 'extra_value_dict_list' in kwargs:
            self.__extra_value_dict_list = kwargs['extra_value_dict_list']

        # commonSettingの取得
        # 2021/7/6 体型差分リストを先行取得する為、通常CSVより先に取得
        self.__create_common_setting()

        self.csv_reader = base_class.csv_reader.CsvReader()
        self.csv_reader.read(self.__csv_path, 'utf-8')

        self.__create_replace_item_dict_list()

        # Maya Directory List
        self.csv_reader.update('MayaDirectoryList', 'MayaDirectoryListEnd', 1)
        self.maya_dir_param_list = self.__create_replaced_dict_list()
        self.maya_dir_list = self.__create_replaced_list('name', self.maya_dir_param_list)

        tmp_maya_dir_list = []
        for item, path in zip(self.maya_dir_param_list, self.maya_dir_list):

            item['name'] = '{0}/{1}'.format(self.maya_root_dir_path, item['name'])

            this_maya_dir_path = '{0}/{1}'.format(self.maya_root_dir_path, path)

            tmp_maya_dir_list.append(this_maya_dir_path)
            if path.startswith('scenes'):
                self.maya_scenes_dir_path = this_maya_dir_path
            elif path.startswith('sourceimages'):
                self.maya_sourceimages_dir_path = this_maya_dir_path
            elif path.startswith('Clothes'):
                self.maya_clothes_dir_path = this_maya_dir_path
            elif path.startswith('Flares'):
                self.maya_flares_dir_path = this_maya_dir_path
            elif path.startswith('Extensions'):
                self.maya_extensions_dir_path = this_maya_dir_path

        self.maya_dir_list = tmp_maya_dir_list

        # maya_dir_param_listとmaya_dir_listをフルパスに
        # シーンとソースイメージを足すメソッドを
        for maya_dir_param in self.maya_dir_param_list:

            maya_dir_path = maya_dir_param['name']

            if maya_dir_path.endswith('scenes'):
                self.maya_scenes_dir_path = maya_dir_path
            elif maya_dir_path.endswith('sourceimages'):
                self.maya_sourceimages_dir_path = maya_dir_path

        # Maya File List
        self.csv_reader.update('MayaFileList', 'MayaFileListEnd', 1)
        self.maya_file_param_list = self.__create_replaced_dict_list(True, False)
        self.maya_file_list = self.__create_replaced_list('name', self.maya_file_param_list)

        # ROOT node
        self.csv_reader.update('RootList', 'RootListEnd', 1)
        root_node_list = self.csv_reader.get_value_list('name')
        if root_node_list and len(root_node_list) == 1:
            self.root_node = self.__replace_item(root_node_list[0], True, True)

        # Mesh
        self.csv_reader.update('MeshList', 'MeshListEnd', 1)
        self.mesh_param_list = self.__create_replaced_dict_list(True, True)
        self.mesh_list = self.__create_replaced_list('name', self.mesh_param_list)

        # Outline Mesh
        self.csv_reader.update('OutlineMeshList', 'OutlineMeshListEnd', 1)
        self.outline_mesh_param_list = self.__create_replaced_dict_list(True, True)
        self.outline_mesh_list = self.__create_replaced_list('name', self.outline_mesh_param_list)

        # Joint
        self.csv_reader.update('JointList', 'JointListEnd', 1)
        self.joint_param_list = self.__create_replaced_dict_list(True, True)
        self.joint_list = self.__create_replaced_list('name', self.joint_param_list)

        # Material
        self.csv_reader.update('MaterialList', 'MaterialListEnd', 1)
        self.material_param_list = self.__create_replaced_dict_list(True, True)
        self.material_list = self.__create_replaced_list('name', self.material_param_list)

        # material_link_list
        self.__create_material_link_list()

        # Texture
        self.csv_reader.update('TextureList', 'TextureListEnd', 1)
        self.texture_param_list = self.__create_replaced_dict_list(True, False)
        if self.texture_param_list and 'dynamic' in self.texture_param_list[0].keys():
            self.texture_param_list = self.__dynamic_area_texture_param_creation(self.texture_param_list)
        self.texture_list = self.__create_replaced_list('name', self.texture_param_list)
        self.__set_unity_dir_full_path(self.texture_param_list)

        # AllTextureList(Mob/汎用衣装用)
        # 全てのパターンのテクスチャ名リスト
        if self.__is_create_variation:
            self.all_texture_list, self.all_texture_param_list = self.__create_variation_list('TextureList')
            self.__set_unity_dir_full_path(self.all_texture_param_list)
        else:
            self.all_texture_param_list = self.texture_param_list
            self.all_texture_list = self.texture_list

        self.__apply_extra_texture_setting()

        # Psd
        self.csv_reader.update('TexturePsdList', 'TexturePsdListEnd', 1)
        self.psd_param_list = self.__create_replaced_dict_list(True, False)
        self.psd_list = self.__create_replaced_list('name', self.psd_param_list)

        # Locator
        self.csv_reader.update('LocatorList', 'LocatorListEnd', 1)
        self.locator_param_list = self.__create_replaced_dict_list(True, True)
        self.locator_list = self.__create_replaced_list('name', self.locator_param_list)

        # clothes
        self.csv_reader.update('ClothesList', 'ClothesListEnd', 1)
        self.cloth_param_list = self.__create_replaced_dict_list(True, False)
        self.cloth_list = self.__create_replaced_list('name', self.cloth_param_list)
        self.__set_unity_dir_full_path(self.cloth_param_list)
        if self.__is_create_variation:
            self.all_cloth_list, self.all_cloth_param_list = self.__create_variation_list('ClothesList')
            self.__set_unity_dir_full_path(self.all_cloth_param_list)
        else:
            self.all_cloth_list = self.cloth_list
            self.all_cloth_param_list = self.cloth_param_list

        # flares
        self.__create_flare_list()
        self.__set_unity_dir_full_path(self.flare_param_list)

        # Model List
        self.__create_model_list()
        self.__set_unity_dir_full_path(self.model_param_list)

        # extensions
        self.csv_reader.update('ExtensionsList', 'ExtensionsListEnd', 1)
        self.extensions_param_list = self.__create_replaced_dict_list(True, False)
        self.extensions_list = self.__create_replaced_list('name', self.extensions_param_list)
        self.__set_unity_dir_full_path(self.extensions_param_list)
        if self.__is_create_variation:
            self.all_extensions_list, self.all_extensions_param_list = self.__create_variation_list('ExtensionsList', False)
            self.__set_unity_dir_full_path(self.all_extensions_param_list)
        else:
            self.all_extensions_list = self.extensions_list
            self.all_extensions_param_list = self.extensions_param_list

        if self.data_type.startswith('bg_'):
            self.__dynamic_update()

        self.exists = True

    # ===============================================
    def __apply_extra_texture_setting(self):
        """
        """

        if self.__is_use_extra_texture:
            return

        if self.texture_param_list and self.texture_list:
            self.texture_param_list, self.texture_list = \
                self.exclude_extra(self.texture_param_list, self.texture_list)

        if self.all_texture_param_list and self.all_texture_list:
            self.all_texture_param_list, self.all_texture_list = \
                self.exclude_extra(self.all_texture_param_list, self.all_texture_list)

    # ===============================================
    def exclude_extra(self, param_list, _list):
        """
        """

        result_param_list = []
        result_list = []

        for param, texture in zip(param_list, _list):

            if 'extra' in param and param['extra']:
                continue

            result_param_list.append(param)
            result_list.append(texture)

        return result_param_list, result_list

    # ===============================================
    def __set_unity_dir_full_path(self, param_list):
        """
        """

        if not param_list:
            return

        for param in param_list:

            if 'unity_dir_path' not in param:
                return

            param['unity_dir_path'] = '{0}/{1}'.format(
                self.__unity_asset_dir_path,
                param['unity_dir_path']
            )

    # ===============================================
    def __create_replaced_dict_list(self, is_use_extra=True, reference_replace=False):
        """
        現在のcsv_readerで参照している箇所から取得する
        """

        dict_list = self.csv_reader.get_value_dict_list()
        dict_list = self.__trim_dict_item('used_id_list', dict_list, False)
        dict_list = self.__trim_dict_item('unused_id_list', dict_list, True)
        dict_list = self.__replace_dict_item(dict_list, is_use_extra, reference_replace)

        return dict_list

    # ===============================================
    def __trim_dict_item(self, target_label, target_dict_list, should_trim_target_item=True):
        """
        対象のdictの要素をトリミングする
        """

        result_dict_list = []

        if not target_dict_list:
            return result_dict_list

        for target_dict in target_dict_list:

            if target_label not in list(target_dict.keys()):
                result_dict_list.append(target_dict)
                continue

            exclude_id_list = target_dict[target_label]

            if should_trim_target_item:

                is_exclude_item = False

                for exclude_id in exclude_id_list:
                    if exclude_id == '':
                        continue

                    if self.data_id.find(exclude_id) >= 0:
                        is_exclude_item = True
                        break

            else:

                is_exclude_item = True

                for exclude_id in exclude_id_list:
                    if exclude_id == '':
                        is_exclude_item = False
                        continue

                    if self.data_id.find(exclude_id) >= 0:
                        is_exclude_item = False
                        break

            if not is_exclude_item:
                result_dict_list.append(target_dict)

        return result_dict_list

    # ===============================================
    def __create_replaced_list(self, label, param_list, is_use_extra=True):
        """
        """

        if not param_list:
            return []

        _list = []

        for param in param_list:

            if not param:
                continue

            _list.append(param[label])

        _list = self.__replace_list_item(_list, is_use_extra)

        return _list

    # ===============================================
    def __create_replace_item_dict_list(self):
        """
        """

        self.__replace_item_dict_list = [
            {'name': 'CHAR_ID', 'replace_str': self.main_id},
            {'name': 'CHAR_SUB_ID', 'replace_str': self.sub_id},
            {'name': 'DATAID', 'replace_str': self.data_id},
            {'name': 'TEX_SEX_ID', 'replace_str': self.texture_sex_id},
        ]
        self.__extra_replace_item_dict_list = []

        # 性別差分特別対応 太り気味のような特殊な体型の場合、ClothesやIkcolsは専用の物を使わなければならない事が多いため
        # 性別差分番号を追加する必要があるため、それ用の判定を行う
        # self.texture_sex_idが1以上(00ではない)状態であれば特殊な状態なので、_ADD_SEX_ID_のreplace_str書き換えを行う
        # self.texture_sex_idの大元の設定関数はchara_info.pyの「__get_texture_sex_id」
        add_sex_id_dict = {'name': '_ADD_SEX_ID_', 'replace_str': '_'}
        if self.texture_sex_id is not None and int(self.texture_sex_id) >= 1:
            add_sex_id_dict['replace_str'] = '_{}_'.format(self.texture_sex_id)
        self.__replace_item_dict_list.append(add_sex_id_dict)

        self.csv_reader.update('DefaultValueList', 'DefaultValueListEnd', 1)
        default_value_dict_list = self.csv_reader.get_value_dict_list()

        if not default_value_dict_list:

            return

        for default_value_dict in default_value_dict_list:

            name = default_value_dict['name']
            value = str(default_value_dict['value'])
            digit = default_value_dict['digit']

            if self.__extra_value_dict_list is not None:

                for extra_value_dict in self.__extra_value_dict_list:

                    extra_name = extra_value_dict['name']
                    extra_value = str(extra_value_dict['value'])

                    if name == extra_name:
                        value = extra_value
                        break

            value = self.__get_padding_value(digit, value)

            self.__extra_replace_item_dict_list.append(
                {'name': name, 'replace_str': value}
            )

    # ===============================================
    def __replace_dict_item(self, target_dict_list, is_use_extra=True, reference_replace=False):
        """
        """

        if target_dict_list is None:
            return []

        for i in range(len(target_dict_list)):

            for key in target_dict_list[i]:

                tmp_referance_replace = reference_replace
                if key != 'name':
                    tmp_referance_replace = False

                temp_target = self.__replace_item(target_dict_list[i][key], is_use_extra, tmp_referance_replace)
                target_dict_list[i][key] = temp_target

        return target_dict_list

    # ===============================================
    def __replace_list_item(self, target_list, is_use_extra=True, reference_replace=False):
        """
        """

        if target_list is None:
            return None

        for i in range(len(target_list)):
            target_list[i] = self.__replace_item(target_list[i], is_use_extra, reference_replace)

        return target_list

    # ===============================================
    def __replace_item(self, target, is_use_extra=True, reference_replace=False):
        """
        """

        replace_item_dict_list = self.__replace_item_dict_list[:]

        if is_use_extra:

            extra_replace_item_dict_list = self.__extra_replace_item_dict_list[:]
            replace_item_dict_list = extra_replace_item_dict_list + replace_item_dict_list

        for replace_item_dict in replace_item_dict_list:

            if str(target).find(replace_item_dict['name']) < 0:
                continue

            target = target.replace(replace_item_dict['name'], str(replace_item_dict['replace_str']))

        # reference名が渡されている時、リファレンス名が先頭に付与されていなければリファレンス名をセット
        if reference_replace and self.__reference_name:
            if type(target) == list:
                for i in range(len(target)):
                    if not target[i].startswith(self.__reference_name):
                        target[i] = self.__add_reference_name(target[i])
            else:
                target = self.__add_reference_name(target)

        return target

    # ===============================================
    def __create_variation_list(self, csv_start_str, reference_replace=False):
        """
        """

        all_target_list = []
        all_target_param_list = []

        self.csv_reader.update('TargetReplaceList', 'TargetReplaceListEnd', 1)
        target_replace_dict_list = self.csv_reader.get_value_dict_list()

        self.csv_reader.update(csv_start_str, '{}End'.format(csv_start_str), 1)
        target_dict_list = self.__create_replaced_dict_list(False, reference_replace)

        if target_replace_dict_list:

            for target_dict in target_dict_list:

                target_dict_name = target_dict['name']

                replace_target_list = []

                for target_replace_dict in target_replace_dict_list:

                    replace_name = target_replace_dict['name']
                    item_range = target_replace_dict['value']

                    start_value = 0
                    if 'start_value' in target_replace_dict:
                        if target_replace_dict['start_value'] != '':
                            start_value = target_replace_dict['start_value']

                    digit = 1
                    if 'digit' in target_replace_dict:
                        digit = target_replace_dict['digit']

                    if replace_target_list:

                        temp_replace_target_list = []

                        for replace_target in replace_target_list:

                            if replace_target.find(replace_name) < 0:
                                continue

                            for i in range(item_range):

                                num = i + start_value
                                value = self.__get_padding_value(digit, str(num))

                                temp_replace_target = replace_target.replace(replace_name, value)

                                if temp_replace_target in temp_replace_target_list:
                                    continue

                                temp_replace_target_list.append(temp_replace_target)

                        if temp_replace_target_list:
                            replace_target_list = temp_replace_target_list

                    else:

                        if target_dict_name.find(replace_name) < 0:
                            continue

                        for i in range(item_range):

                            num = i + start_value
                            value = self.__get_padding_value(digit, str(num))

                            temp_replace_target = target_dict_name.replace(replace_name, value)
                            replace_target_list.append(temp_replace_target)

                if not replace_target_list:
                    # 特殊対応: dynamicモードが入っている場合には動的生成を試みる
                    if 'dynamic' in target_dict.keys() and target_dict['dynamic']:
                        generated_param_list = self.__dynamic_area_texture_param_creation([target_dict])
                        for param_dict in generated_param_list:
                            all_target_param_list.append(param_dict)
                            all_target_list.append(param_dict['name'])

                    else:
                        all_target_param_list.append(target_dict)
                        all_target_list.append(target_dict['name'])

                for replace_target in replace_target_list:

                    if replace_target in all_target_list:
                        continue

                    replace_target_dict = target_dict.copy()
                    replace_target_dict['name'] = replace_target

                    all_target_list.append(replace_target)
                    all_target_param_list.append(replace_target_dict)

        return all_target_list, all_target_param_list

    # ===============================================
    def __get_padding_value(self, digit, org_value):

        return_value = str(org_value)

        if len(return_value) < digit:
            return_value = '0' * (digit - len(return_value)) + str(org_value)

        return return_value

    # ===============================================
    def __get_dict_list_with_padding_value(self, org_dict_list):

        if not org_dict_list:
            return org_dict_list

        result_dict_list = []

        for _dict in org_dict_list:

            digit = None
            org_value = None

            for key in _dict:
                if key == 'digit':
                    digit = _dict[key]
                elif key == 'value':
                    org_value = _dict[key]

            if not digit or not org_value:
                result_dict_list.append(_dict)

            else:
                _dict['value'] = self.__get_padding_value(digit, org_value)
                result_dict_list.append(_dict)

        return result_dict_list

    # ===============================================
    def __create_model_list(self):
        """
        """
        self.csv_reader.update('ModelList', 'ModelListEnd', 1)
        temp_target_param_list = self.__create_replaced_dict_list()
        temp_target_list = self.csv_reader.get_value_list('name')
        temp_target_list = self.__replace_list_item(temp_target_list, True)

        self.model_list, self.model_param_list = self.__apply_model_num_list(temp_target_list, temp_target_param_list)
        if self.__is_create_variation:
            temp_all_model_list, temp_all_model_param_list = self.__create_variation_list('ModelList', True)
            self.all_model_list, self.all_model_param_list = self.__apply_model_num_list(temp_all_model_list, temp_all_model_param_list)
            self.__set_unity_dir_full_path(self.all_model_param_list)
        else:
            self.all_model_list = self.model_list
            self.all_model_param_list = self.model_param_list

    # ===============================================
    def __create_flare_list(self):
        """
        """

        self.csv_reader.update('FlaresList', 'FlaresListEnd', 1)
        temp_target_param_list = self.__create_replaced_dict_list()
        temp_target_list = self.csv_reader.get_value_list('name')
        temp_target_list = self.__replace_list_item(temp_target_list, True)

        self.flare_list, self.flare_param_list = self.__apply_model_num_list(temp_target_list, temp_target_param_list)
        if self.__is_create_variation:
            temp_all_flare_list, temp_all_flare_param_list = self.__create_variation_list('FlaresList')
            self.all_flare_list, self.all_flare_param_list = self.__apply_model_num_list(temp_all_flare_list, temp_all_flare_param_list)
            self.__set_unity_dir_full_path(self.all_flare_param_list)
        else:
            self.all_flare_list = self.flare_list
            self.all_flare_param_list = self.flare_param_list

    # ===============================================
    def __apply_model_num_list(self, temp_target_list, temp_target_param_list):

        if not self.model_num_param_list:
            self.csv_reader.update('ModelNumList', 'ModelNumListEnd', 1)
            self.model_num_param_list = self.__get_dict_list_with_padding_value(self.__create_replaced_dict_list())

        if not self.model_num_param_list:
            return temp_target_list, temp_target_param_list

        result_list = []
        result_param_list = []
        model_num_data_dict_list = []

        for model_num_param in self.model_num_param_list:

            name = model_num_param['name']
            value = model_num_param['value']

            for i in range(len(model_num_data_dict_list)):
                if model_num_data_dict_list[i]['name'] == name:
                    model_num_data_dict = model_num_data_dict_list[i]['values'].append(value)
                    break
            else:
                model_num_data_dict_list.append({'name': name, 'values': [value]})

        for temp_model_param in temp_target_param_list:

            temp_model = temp_model_param['name']
            model_type = ''
            if 'type' in temp_model_param:
                model_type = temp_model_param['type']

            replace_model_list = []

            for model_num_data_dict in model_num_data_dict_list:

                replace_target = model_num_data_dict['name']
                values = model_num_data_dict['values']

                if replace_model_list:

                    temp_replace_model_list = []

                    for replace_model in replace_model_list:

                        if replace_model.find(replace_target) < 0:
                            continue

                        for value in values:

                            temp_replace_model = replace_model.replace(replace_target, value)

                            if temp_replace_model not in temp_replace_model_list:
                                temp_replace_model_list.append(temp_replace_model)

                    if temp_replace_model_list:
                        replace_model_list = temp_replace_model_list

                else:

                    if temp_model.find(replace_target) < 0:
                        continue

                    for value in values:

                        temp_replace_model = temp_model.replace(replace_target, value)
                        replace_model_list.append(temp_replace_model)

            for replace_model in replace_model_list:

                param_model_copy = temp_model_param.copy()
                param_model_copy['name'] = replace_model

                result_param_list.append(param_model_copy)

                if model_type != '' and model_type != self.head_type:
                    continue

                result_list.append(replace_model)

        return result_list, result_param_list

    # ===============================================
    def __create_material_link_list(self):
        """
        """

        self.material_link_list = []

        for material_param in self.material_param_list:

            material_dict = {}

            for k, i in list(material_param.items()):

                if k not in self.TEX_TYPE_LIST:
                    continue

                if i == '' or i == -1:
                    continue

                material_dict[k] = i

            self.material_link_list.append(material_dict)

    def __create_common_setting(self):
        """モデルで共通する基本設定をCSVから作成
        """

        if os.path.exists(self.__common_setting_csv_path):
            self.csv_reader = base_class.csv_reader.CsvReader()
            self.csv_reader.read(self.__common_setting_csv_path, 'utf-8')

            # 上限値
            self.csv_reader.update('LimitList', 'LimitListEnd', 1)
            limit_param_list = self.__create_replaced_dict_list()
            for limit_param in limit_param_list:
                # 通常骨
                if limit_param['name'] == 'NormalBoneLimit':
                    self.normal_bone_limit = limit_param['value']
                # クロス骨
                elif limit_param['name'] == 'SpBoneLimit':
                    self.sp_bone_limit = limit_param['value']
                # ポリゴン数
                elif limit_param['name'] == 'PolygonLimit':
                    self.polygon_limit = limit_param['value']

            # Hipの位置
            self.csv_reader.update('HipTranslateList', 'HipTranslateListEnd', 1)
            hip_translate_param_list = self.__create_replaced_dict_list()
            if len(hip_translate_param_list) == 3:
                self.hip_original_translate = [
                    hip_translate_param_list[0]['value'],
                    hip_translate_param_list[1]['value'],
                    hip_translate_param_list[2]['value']
                ]

            # 体型差分IDの一覧
            if self.__is_create_variation:
                suffix = ''
                if self.data_type.startswith('mini_'):
                    suffix = 'Mini'

                self.csv_reader.update('{}ModelNumList'.format(suffix), '{}ModelNumListEnd'.format(suffix), 1)
                model_num_param_list = self.__create_replaced_dict_list()
                if len(model_num_param_list):
                    self.model_num_param_list = model_num_param_list
                    self.model_num_list = self.__create_replaced_list('value', self.model_num_param_list)

    # ===============================================
    def __add_reference_name(self, target):
        """対象の文字列にリファレンス名を追加する
        Node名(先頭が|(パイプ))で始まるものに関しては|でリプレイス
        それ以外に関しては先頭にリファレンス名を追加する

        Args:
            target ([type]): 書き換えた文字列
        """

        # Node名の場合は|(パイプ)を全てreplace
        if target.startswith('|'):
            target = target.replace('|', '|{}:'.format(self.__reference_name))
        # それ以外(Material名とか)の場合は単純に先頭にリファレンス名を付与
        else:
            target = '{}:{}'.format(self.__reference_name, target)

        return target

    # ===============================================
    def __dynamic_area_texture_param_creation(self, _list):
        """動的にエリアテクスチャのparamリストを生成する

        存在するファイルベースで検証を行っているため、存在確認には用いないこと
        Args:
            _list (list): paramのlist

        Returns:
            list: paramのlist
        """
        if not os.path.exists(self.maya_sourceimages_dir_path):
            return _list

        result = []
        for param_dict in _list:
            if 'dynamic' in param_dict.keys() and param_dict['dynamic']:
                for file in os.listdir(self.maya_sourceimages_dir_path):
                    if re.search(param_dict['name'], file):
                        temp_dict = param_dict.copy()
                        temp_dict['name'] = file
                        result.append(temp_dict)
            else:
                result.append(param_dict)

        return result

    # ===============================================
    def __dynamic_update(self):
        """一意にデータが定まらないケースにおいて動的にデータを更新します
        とりあえずDX11表示に必要そうな箇所を優先して実装
        このDynamicデータはデータが存在していることが前提です。存在しないデータを検出したりする用途には利用できません
        """
        # 大元となるtop_nodeの検索を試みる
        self.top_node = ''
        for maya_dir in self.maya_dir_list:
            if maya_dir.endswith('scenes'):

                # フォルダが存在しない場合には処理を打ち切る
                if not os.path.exists(maya_dir):
                    return

                scene_file_list = os.listdir(maya_dir)
                for scene_file in scene_file_list:
                    if self.file_id in scene_file:
                        self.top_node = scene_file.rsplit('.', 1)[0]
                        break

        # 見つからない場合は何もしない
        if not cmds.objExists(self.top_node):
            return

        self.__dynamic_material_update()
        self.__dynamic_mesh_update()
        self.__dynamic_texture_update()
        self.__create_material_link_list()

    # ===============================================
    def __dynamic_material_update(self):
        """マテリアル周辺の情報を動的にアップデート
        """
        material_param_template = {
            'psd_id': -1,
            'unused_id_list': [],
            'diff_wet': -1,
            'name': -1,
            'ctrl': -1,
            'emissive_wet': -1,
            'dirt': -1,
            'emissive': -1,
            'check': False,
            'ctrl_wet': -1,
            'base': -1,
            'shad_c_wet': -1,
            'base_wet': -1,
            'diff': -1,
            'id': -1,
            'shad_c': -1,
        }
        self.material_list = []
        self.material_param_list = []

        current_id = 0
        for material in cmds.ls(materials=True):
            if material.startswith('mtl_'):
                current_param = material_param_template.copy()
                current_param.update({'name': material, 'id': current_id})
                self.material_list.append(material)
                self.material_param_list.append(current_param)
                current_id += 1

    # ===============================================
    def __dynamic_mesh_update(self):
        """メッシュに関する情報を動的に生成する
        """

        mesh_param_template = {
            'unused_id_list': [],
            'name': '',
            'extra': 0,
            'check': 1,
            'material_list': [],
            'id': 0,
        }

        self.mesh_list = []
        self.mesh_param_list = []

        self.outline_mesh_param_list = []
        self.outline_mesh_list = []

        outline_id = 0
        mesh_id = 0
        for mesh in cmds.ls(self.top_node, dag=True, type='mesh', long=True):
            transform = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
            shading_eng = cmds.listConnections(mesh, type='shadingEngine')
            material_list = cmds.ls(cmds.listConnections(shading_eng), materials=True)
            material_id_list = self.__material_name_id_conversion(material_list)

            if not transform.endswith('_Outline') and transform not in self.mesh_list:
                current_mesh_param = mesh_param_template.copy()
                current_mesh_param.update({'name': transform, 'material_list': material_id_list, 'id': mesh_id, 'extra': 0})
                self.mesh_list.append(transform)
                self.mesh_param_list.append(current_mesh_param)
                mesh_id += 1

            elif transform.endswith('_Outline') and transform not in self.outline_mesh_list:
                current_outline_param = mesh_param_template.copy()
                current_outline_param.update({'name': transform, 'material_list': material_id_list, 'id': outline_id, 'extra': 1})
                self.outline_mesh_list.append(transform)
                self.outline_mesh_param_list.append(current_outline_param)
                outline_id += 1

    # ===============================================
    def __material_name_id_conversion(self, material_name_list):
        """マテリアル名のリストをマテリアルIDのリストに変換

        Args:
            material_name_list (list[str]): 変換対象のマテリアルのリスト

        Returns:
            list[int]: マテリアルIDのリスト
        """
        material_id_list = []
        for material_name in material_name_list:
            try:
                current_id = self.material_list.index(material_name)
            except ValueError:
                current_id = -1
            material_id_list.append(current_id)

        return material_id_list

    # ===============================================
    def __dynamic_texture_update(self):
        """テクスチャ情報をアップデート
        """
        texture_param_template = {
            'unused_id_list': [],
            'name': '',
            'extra': -1,
            'check': False,
            'unity_dir_path': '',
            'height': ['512'],
            'width': ['512'],
            'id': -1
        }
        psd_param_template = {
            'unused_id_list': [],
            'name': '',
            'extra': -1,
            'check': False,
            'height': ['512'],
            'width': ['512'],
            'id': -1
        }
        self.texture_list = []
        self.all_texture_list = []
        self.texture_param_list = []
        self.all_texture_param_list = []
        self.psd_list = []
        self.psd_param_list = []

        texture_path = ''
        for item in self.maya_dir_list:
            if item.endswith('sourceimages'):
                texture_path = item
                break

        if not texture_path:
            return

        estimated_file_list = []
        for material_param in self.material_param_list:
            estimated_file_list.append(material_param['name'].replace('mtl_', 'tex_') + '.tga')
            for tex_type in self.TEX_TYPE_LIST:
                estimated_file_list.append(material_param['name'].replace('mtl_', 'tex_') + '_' + tex_type + '.tga')

        psd_id = 0
        tex_id = 0
        for file_name in os.listdir(texture_path):

            # psdの場合
            if file_name.endswith('.psd'):
                current_psd_param = psd_param_template.copy()
                current_psd_param.update({'name': file_name, 'id': psd_id})
                self.psd_param_list.append(current_psd_param)
                self.psd_list.append(file_name)
                psd_id += 1
                continue

            # tex系ファイルではない
            if not file_name.startswith('tex_'):
                continue

            # 複数シーンファイル向けのテクスチャデータが入っているかもしれないので可能性のある名前でフィルタリングする
            if file_name not in estimated_file_list:
                continue

            # texファイル
            current_tex_param = texture_param_template.copy()
            current_tex_param.update({'name': file_name, 'id': tex_id})

            self.all_texture_list.append(file_name)
            self.all_texture_param_list.append(current_tex_param)
            self.texture_list.append(file_name)
            self.texture_param_list.append(current_tex_param)
            tex_id += 1

        # 名前でマッチしてtex, psdとmaterialを紐づける
        for material_param in self.material_param_list:

            material_base_name = material_param['name'].replace('mtl_', 'tex_')

            psd_match_pattern = material_base_name + '(_all|).psd'
            index = 0
            for psd in self.psd_list:
                match_item = re.match(psd_match_pattern, psd)
                if match_item:
                    material_param['psd_id'] = index
                    break
                index += 1

            for tex_type in self.TEX_TYPE_LIST:
                estimated_tex_name = material_base_name + '_' + tex_type + '.tga'

                # とりあえずIndexとってみてなければ-1を入れておく
                try:
                    material_param[tex_type] = self.texture_list.index(estimated_tex_name)
                except ValueError:
                    material_param[tex_type] = -1

    def test_print(self):
        """デバッグ用の一括パラメータプリント
        """

        print('mesh -------------------')
        print(self.mesh_list)
        print(self.mesh_param_list)
        print('outline mesh -------------------')
        print(self.outline_mesh_list)
        print(self.outline_mesh_param_list)
        print('joint -------------------')
        print(self.joint_list)
        print(self.joint_param_list)
        print('material -------------------')
        print(self.material_list)
        print(self.material_param_list)
        print('texture -------------------')
        print(self.texture_list)
        print(self.texture_param_list)
        print('all texture -------------------')
        print(self.all_texture_list)
        print(self.all_texture_param_list)
        print('psd texture -------------------')
        print(self.psd_param_list)
        print(self.psd_list)
        print('locator -------------------')
        print(self.locator_list)
        print(self.locator_param_list)
        print('cloth -------------------')
        print(self.cloth_list)
        print(self.cloth_param_list)
        print('flare -------------------')
        print(self.flare_list)
        print(self.flare_param_list)
        print('all flare -------------------')
        print(self.all_flare_list)
        print(self.all_flare_param_list)
        print('extensions -------------------')
        print(self.extensions_list)
        print(self.extensions_param_list)

        print('maya dir file -------------------')
        print(self.maya_dir_list)
        print(self.maya_dir_param_list)
        print(self.maya_file_list)
        print(self.maya_file_param_list)

        print('model -------------------')
        print(self.model_list)
        print(self.model_param_list)
        print(self.all_model_list)
        print(self.all_model_param_list)

        print('material link -------------------')
        print(self.material_link_list)
