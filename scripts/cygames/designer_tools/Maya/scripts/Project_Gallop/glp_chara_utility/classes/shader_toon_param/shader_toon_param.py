# -*- coding: utf-8 -*-
"""
Unityプレビューシェーダー Toon系のパラメーターを取得、設定用のmethod群
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds

from ....glp_common.classes.info import chara_info


class ShaderToonParam(object):

    def __init__(self):

        self.toon_shader_suffix = '____dx11'
        self.shader_node_type = 'dx11Shader'

    def get_shader_toon_param(self, target_attr, target_part, default_value, target_data_type):
        """対象のアトリビュートが存在するShaderの一覧とその値を取得する

        Args:
            target_attr (str): 対象のアトリビュート名
            target_part (str): 対象のメッシュパーツ名
            default_value (list or float): アトリビュートの初期値
            target_data_type (str): 対象のデータタイプ

        Returns:
            dict: 対象のアトリビュートの値と値を設定するToonマテリアルのリスト
        """

        shader_toon_param = {'value': default_value, 'toon_material_list': []}

        # chara_infoのデフォルトmaterial読み込みを行う
        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if _chara_info.exists:

            toon_material_list = []
            for material in _chara_info.part_info.material_list:

                toon_material = '{}{}'.format(material, self.toon_shader_suffix)
                if not cmds.objExists(toon_material) or cmds.objectType(toon_material) != self.shader_node_type:
                    continue

                if target_data_type and not _chara_info.data_type.endswith(target_data_type):
                    continue

                if _chara_info.data_type.endswith('head'):
                    if toon_material.find(target_part) == -1:
                        continue

                # 体操服は一旦今の所だけで対応
                if _chara_info.data_type.endswith('bdy0001_body'):
                    if not material.endswith('_1'):
                        continue

                toon_material_list.append(toon_material)

            if toon_material_list:

                if cmds.attributeQuery(target_attr, n=toon_material_list[0], exists=True):

                    attr_value = cmds.getAttr('{0}.{1}'.format(toon_material_list[0], target_attr))
                    # double3を取得するとlistにtapleが内包されているため、list[0]から値を取得する
                    if type(attr_value) == list:
                        attr_value = attr_value[0]
                    shader_toon_param['value'] = attr_value
                    shader_toon_param['toon_material_list'] = toon_material_list

        return shader_toon_param

    def set_shader_toon_param(self, target_attr, target_toon_material_list, value_type, target_value):
        """Toonマテリアルの対象のアトリビュートに値をセット

        Args:
            target_attr (str): 対象のアトリビュート名
            target_toon_material_list (list): 対象のToonマテリアルの一覧
            value_type (str): 対象のアトリビュートのtype
            target_value (list or float): 設定する値
        """

        for target_toon_material in target_toon_material_list:

            if not cmds.attributeQuery(target_attr, n=target_toon_material, exists=True):
                return

            if value_type == 'double3':
                cmds.setAttr(
                    '{0}.{1}'.format(target_toon_material, target_attr),
                    target_value[0], target_value[1], target_value[2],
                    type='double3')
            elif value_type == 'float':
                cmds.setAttr(
                    '{0}.{1}'.format(target_toon_material, target_attr),
                    target_value)
