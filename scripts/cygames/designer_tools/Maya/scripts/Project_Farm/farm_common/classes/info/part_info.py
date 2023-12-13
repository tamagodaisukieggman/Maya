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
except:
    pass

import os

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

        self.is_unique_chara = False

        self.__is_create_texture_variation = False
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
        self.mesh_naming_rule_list = []
        self.mesh_naming_rule_param_list = []
        self.outline_mesh_list = []
        self.outline_mesh_param_list = []
        self.joint_list = []
        self.joint_param_list = []
        self.joint_naming_rule_list = []
        self.joint_naming_rule_param_list = []
        self.material_list = []
        self.material_param_list = []
        self.material_naming_rule_list = []
        self.material_naming_rule_param_list = []
        self.material_link_rule_list = []
        self.material_link_rule_param_list = []
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

        self.maya_dir_list = []
        self.maya_dir_param_list = []
        self.maya_file_list = []
        self.maya_file_param_list = []

        self.model_list = []
        self.model_param_list = []

        self.material_link_list = []

        self.root_node = ''
        self.grp_joint_pattern = ''
        self.grp_mesh_pattern = ''

        self.maya_root_dir_path = ''
        self.maya_scenes_dir_path = ''
        self.maya_sourceimages_dir_path = ''
        self.maya_clothes_dir_path = ''
        self.maya_flares_dir_path = ''

        # 部位毎の共通設定
        self.sp_bone_limit = 0

    # ===============================================
    def create_info(self,
                    data_type, head_type,
                    data_id, main_id, sub_id, file_id,
                    is_unique_chara,
                    is_create_texture_variation, is_create_model_list, is_use_extra_texture,
                    unity_asset_dir_path, maya_root_dir_path, csv_path, common_setting_csv_path,
                    **kwargs):
        """
        """

        if not data_type or not main_id or not sub_id:
            return

        self.data_type = data_type
        self.head_type = head_type
        self.data_id = data_id
        self.main_id = main_id
        self.sub_id = sub_id
        self.file_id = file_id
        self.is_unique_chara = is_unique_chara
        self.__is_create_texture_variation = is_create_texture_variation
        self.__is_create_model_list = is_create_model_list
        self.__is_use_extra_texture = is_use_extra_texture
        self.__unity_asset_dir_path = unity_asset_dir_path
        self.__csv_path = csv_path
        self.__common_setting_csv_path = common_setting_csv_path

        self.maya_root_dir_path = maya_root_dir_path

        if 'extra_value_dict_list' in kwargs:
            self.__extra_value_dict_list = kwargs['extra_value_dict_list']

        if 'variable_value_dict_list' in kwargs:
            self.__variable_value_dict_list = kwargs['variable_value_dict_list']

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
        self.maya_file_param_list = self.__create_replaced_dict_list()
        self.maya_file_list = self.__create_replaced_list('name', self.maya_file_param_list)

        # ROOT node
        self.csv_reader.update('RootList', 'RootListEnd', 1)
        root_node_list = self.csv_reader.get_value_list('name')
        if len(root_node_list) == 1:
            self.root_node = self.__replace_item(root_node_list[0])

        # Group node
        self.csv_reader.update('GroupList', 'GroupListEnd', 1)
        group_param_list = self.__create_replaced_dict_list()
        for group_param in group_param_list:
            if group_param.get('type', '') == 'joint':
                self.grp_joint_pattern = group_param.get('name', '')
            if group_param.get('type', '') == 'mesh':
                self.grp_mesh_pattern = group_param.get('name', '')

        # Mesh
        self.csv_reader.update('MeshList', 'MeshListEnd', 1)
        self.mesh_param_list = self.__create_replaced_dict_list()
        self.mesh_list = self.__create_replaced_list('name', self.mesh_param_list)

        # Mesh Naming Rule
        self.csv_reader.update('MeshNamingRuleList', 'MeshNamingRuleListEnd', 1)
        self.mesh_naming_rule_param_list = self.__create_replaced_dict_list()
        self.mesh_naming_rule_list = self.__create_replaced_list('name', self.mesh_naming_rule_param_list)

        # Outline Mesh
        self.csv_reader.update('OutlineMeshList', 'OutlineMeshListEnd', 1)
        self.outline_mesh_param_list = self.__create_replaced_dict_list()
        self.outline_mesh_list = self.__create_replaced_list('name', self.outline_mesh_param_list)

        # Joint
        self.csv_reader.update('JointList', 'JointListEnd', 1)
        self.joint_param_list = self.__create_replaced_dict_list()
        self.joint_list = self.__create_replaced_list('name', self.joint_param_list)

        # Joint Naming Rule
        self.csv_reader.update('JointNamingRuleList', 'JointNamingRuleListEnd', 1)
        self.joint_naming_rule_param_list = self.__create_replaced_dict_list()
        self.joint_naming_rule_list = self.__create_replaced_list('name', self.joint_naming_rule_param_list)

        # Material
        self.csv_reader.update('MaterialList', 'MaterialListEnd', 1)
        self.material_param_list = self.__create_replaced_dict_list()
        self.material_list = self.__create_replaced_list('name', self.material_param_list)

        # material_link_list
        self.__create_material_link_list()

        # Material Naming Rule
        self.csv_reader.update('MaterialNamingRuleList', 'MaterialNamingRuleListEnd', 1)
        self.material_naming_rule_param_list = self.__create_replaced_dict_list()
        self.material_naming_rule_list = self.__create_replaced_list('name', self.material_naming_rule_param_list)

        # Material Link Rule
        self.csv_reader.update('MaterialLinkRuleList', 'MaterialLinkRuleListEnd', 1)
        self.material_link_rule_param_list = self.__create_replaced_dict_list()
        self.material_link_rule_list = self.__create_replaced_list('name', self.material_link_rule_param_list)

        # Texture
        self.csv_reader.update('TextureList', 'TextureListEnd', 1)
        self.texture_param_list = self.__create_replaced_dict_list()
        self.texture_list = self.__create_replaced_list('name', self.texture_param_list)
        self.__set_unity_dir_full_path(self.texture_param_list)

        # AllTextureList(Mob/汎用衣装用)
        # 全てのパターンのテクスチャ名リスト
        if self.__is_create_texture_variation:
            self.__create_texture_variation_list()
            self.__set_unity_dir_full_path(self.all_texture_param_list)
        else:
            self.all_texture_param_list = self.texture_param_list
            self.all_texture_list = self.texture_list

        self.__apply_extra_texture_setting()

        # Psd
        self.csv_reader.update('TexturePsdList', 'TexturePsdListEnd', 1)
        self.psd_param_list = self.__create_replaced_dict_list()
        self.psd_list = self.__create_replaced_list('name', self.psd_param_list)

        # Locator
        self.csv_reader.update('LocatorList', 'LocatorListEnd', 1)
        self.locator_param_list = self.__create_replaced_dict_list()
        self.locator_list = self.__create_replaced_list('name', self.locator_param_list)

        # Locator Pattern
        self.csv_reader.update('LocatorPatternList', 'LocatorPatternListEnd', 1)
        self.locator_pattern_param_list = self.__create_replaced_dict_list()
        self.locator_pattern_list = self.__create_replaced_list('name', self.locator_pattern_param_list)

        # clothes
        self.csv_reader.update('ClothesList', 'ClothesListEnd', 1)
        self.cloth_param_list = self.__create_replaced_dict_list()
        self.cloth_list = self.__create_replaced_list('name', self.cloth_param_list)
        self.__set_unity_dir_full_path(self.cloth_param_list)

        # flares
        self.__create_flare_list()
        self.__set_unity_dir_full_path(self.flare_param_list)

        # Model List
        self.__create_model_list()
        self.__set_unity_dir_full_path(self.model_param_list)

        # commonSettingの取得
        if os.path.exists(self.__common_setting_csv_path):
            self.csv_reader = base_class.csv_reader.CsvReader()
            self.csv_reader.read(self.__common_setting_csv_path, 'utf-8')
            self.csv_reader.update('SpBoneLimitList', 'SpBoneLimitListEnd', 1)
            sp_bone_limit_param_list = self.__create_replaced_dict_list()
            if len(sp_bone_limit_param_list) == 1:
                self.sp_bone_limit = sp_bone_limit_param_list[0]['value']

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
    def __create_replaced_dict_list(self, is_use_extra=True):
        """
        現在のcsv_readerで参照している箇所から取得する
        """

        dict_list = self.csv_reader.get_value_dict_list()
        dict_list = self.__trim_dict_item('used_id_list', dict_list, False)
        dict_list = self.__trim_dict_item('unused_id_list', dict_list, True)
        dict_list = self.__replace_dict_item(dict_list, is_use_extra)

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
        ]
        self.__extra_replace_item_dict_list = []

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
    def __replace_dict_item(self, target_dict_list, is_use_extra=True):
        """
        """

        if target_dict_list is None:
            return []

        for i in range(len(target_dict_list)):

            for key in target_dict_list[i]:

                temp_target = self.__replace_item(target_dict_list[i][key], is_use_extra)
                target_dict_list[i][key] = temp_target

        result = []

        for target_dict in target_dict_list:
            temp_result_list = [target_dict]

            for variable_value_dict in self.__variable_value_dict_list:
                replaced_dict_list = []

                for temp_target_dict in temp_result_list:
                    temp_dict_list = self.__replace_variable_dict_list(
                        temp_target_dict,
                        variable_value_dict)
                    replaced_dict_list += temp_dict_list

                temp_result_list = replaced_dict_list

            result += temp_result_list

        return result

    # ===============================================
    def __replace_variable_dict_list(self, target, replace_value):
        """
        可変要素を置換したdictのlistを返す

        :returns: 置換されたdictのlist
        :rtype: list
        """

        name = replace_value['name']
        replace_str_list = replace_value['replace_str_list']

        # replace_valueのキーが含まれているかを先に取得
        match = False
        for value in list(target.values()):
            if name in str(value):
                match = True
                break

        if not match:
            return [target]

        result = []

        for replace_str in replace_str_list:
            temp_target = target.copy()
            for key, value in list(temp_target.items()):
                if name in str(value):
                    temp_target[key] = str(value).replace(name, replace_str)
            result.append(temp_target)

        return result

    # ===============================================
    def __replace_list_item(self, target_list, is_use_extra=True):
        """
        """

        if target_list is None:
            return None

        for i in range(len(target_list)):
            target_list[i] = self.__replace_item(target_list[i], is_use_extra)

        result = []

        for target in target_list:
            temp_result_list = [target]

            for variable_value_dict in self.__variable_value_dict_list:
                replaced_list = []

                for temp_target in temp_result_list:
                    temp_list = self.__replace_variable_list(
                        temp_target,
                        variable_value_dict)
                    replaced_list += temp_list

                temp_result_list = replaced_list

            result += temp_result_list

        return result

    # ===============================================
    def __replace_variable_list(self, target, replace_value):
        """
        可変要素を置換したlistを返す

        :returns: 置換されたlist
        :rtype: list
        """

        name = replace_value['name']
        replace_str_list = replace_value['replace_str_list']

        # replace_valueのキーがあったなら置換
        match = name in str(target)

        if not match:
            return [target]

        result = []

        for replace_str in replace_str_list:
            result.append(str(target).replace(name, replace_str))

        return result

    # ===============================================
    def __replace_item(self, target, is_use_extra=True):
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

        return target

    # ===============================================
    def __create_texture_variation_list(self):
        """
        """

        self.all_texture_list = []
        self.all_texture_param_list = []

        self.csv_reader.update('TextureReplaceList', 'TextureReplaceListEnd', 1)
        texture_replace_dict_list = self.csv_reader.get_value_dict_list()

        self.csv_reader.update('TextureList', 'TextureListEnd', 1)
        texture_dict_list = self.__create_replaced_dict_list(False)

        if not texture_replace_dict_list:
            return

        for texture_dict in texture_dict_list:

            texture = texture_dict['name']

            replace_texture_list = []

            for texture_replace_dict in texture_replace_dict_list:

                replace_name = texture_replace_dict['name']
                item_range = texture_replace_dict['value']
                digit = 1
                if 'digit' in texture_replace_dict:
                    digit = texture_replace_dict['digit']

                if replace_texture_list:

                    temp_replace_texture_list = []

                    for replace_texture in replace_texture_list:

                        if replace_texture.find(replace_name) < 0:
                            continue

                        for i in range(item_range):

                            value = self.__get_padding_value(digit, str(i))

                            temp_replace_texture = replace_texture.replace(replace_name, value)

                            if temp_replace_texture in temp_replace_texture_list:
                                continue

                            temp_replace_texture_list.append(temp_replace_texture)

                    if temp_replace_texture_list:
                        replace_texture_list = temp_replace_texture_list

                else:

                    if texture.find(replace_name) < 0:
                        continue

                    for i in range(item_range):

                        value = self.__get_padding_value(digit, str(i))

                        temp_replace_texture = texture.replace(replace_name, value)
                        replace_texture_list.append(temp_replace_texture)

            if not replace_texture_list:
                self.all_texture_param_list.append(texture_dict)
                self.all_texture_list.append(texture_dict['name'])

            for replace_texture in replace_texture_list:

                if replace_texture in self.all_texture_list:
                    continue

                replace_texture_dict = texture_dict.copy()
                replace_texture_dict['name'] = replace_texture

                self.all_texture_list.append(replace_texture)
                self.all_texture_param_list.append(replace_texture_dict)

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

        self.model_list = []
        self.model_param_list = []

        self.model_list, self.model_param_list = self.__apply_model_num_list('ModelList', False)

    # ===============================================
    def __create_flare_list(self):
        """
        """

        self.flare_list = []
        self.flare_param_list = []

        self.flare_list, self.flare_param_list = self.__apply_model_num_list('FlaresList', True)

    # ===============================================
    def __apply_model_num_list(self, target_list_label, is_use_extra):

        self.csv_reader.update('ModelNumList', 'ModelNumListEnd', 1)
        model_num_dict_list = self.__get_dict_list_with_padding_value(self.__create_replaced_dict_list())

        self.csv_reader.update(target_list_label, target_list_label + 'End', 1)
        temp_target_param_list = self.__create_replaced_dict_list()
        temp_target_list = self.csv_reader.get_value_list('name')
        temp_target_list = self.__replace_list_item(temp_target_list, is_use_extra)

        result_list = []
        result_param_list = []

        if not model_num_dict_list:
            result_list = temp_target_list
            result_param_list = temp_target_param_list
            return result_list, result_param_list

        model_num_data_dict_list = []

        for model_num_dict in model_num_dict_list:

            name = model_num_dict['name']
            value = model_num_dict['value']

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

        include_label_list = [
            'diff', 'base', 'ctrl', 'shad_c',
            'dirt', 'diff_wet', 'base_wet', 'ctrl_wet', 'shad_c_wet',
            'emissive', 'emissive_wet', 'area', 'area_wet'
        ]

        self.material_link_list = []

        for material_param in self.material_param_list:

            material_dict = {}

            for k, i in list(material_param.items()):

                if k not in include_label_list:
                    continue

                if i == '' or i == -1:
                    continue

                material_dict[k] = i

            self.material_link_list.append(material_dict)
