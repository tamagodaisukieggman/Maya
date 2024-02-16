# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import re
import maya.cmds as cmds

from . import const

reload(const)


class ObjMappingData(object):

    def __init__(self, grp_info_dicts, axis_obj=None):
        """初期化

        Args:
            grp_info_dicts (dict): UnitySnapData.get_grp_info_dicts()で取得できるグループ情報
            axis_obj (str): 基準オブジェ
        """

        # {GrpId: {'Type': str, 'Root': str, 'Objs': {obj_name: {'Path': xxx, 'Parent': xxx, 'Opts': [,,,]},,,}}}
        self.obj_mapping_dict = {}
        self.axis_obj = axis_obj

        for grp_info_dict in grp_info_dicts:
            self.obj_mapping_dict[grp_info_dict['GrpId']] = {
                'Type': grp_info_dict['Type'],
                'Root': grp_info_dict['RootName'],
                'Objs': {}
            }

    def init_obj_mapping_for_each_root(self, grp_id, maya_root, mapping_opts):
        """指定したルート以下のマッピングを初期化

        Args:
            obj_type (str): オブジェクトタイプ
            unity_root (str): unityのルート名
            maya_root (str): mayaのルートパス
            mapping_opts (list): マッピングオプションリスト
        """

        if grp_id not in self.obj_mapping_dict:
            return

        if not maya_root:
            self.obj_mapping_dict[grp_id]['Objs'] = {}
            return

        grp_type = self.obj_mapping_dict[grp_id]['Type']
        grp_root = self.obj_mapping_dict[grp_id]['Root']
        obj_dict = self.obj_mapping_dict[grp_id]['Objs']

        roots = cmds.ls(maya_root, l=True)
        if not roots:
            return

        if grp_type == const.TYPE_CHARA_MATERIAL:

            all_objs = [roots[0]]
            all_children = cmds.listRelatives(roots[0], ad=True, f=True)
            if all_children:
                all_objs.extend(all_children)

            all_materials = self.__get_material_list(all_objs)

            for mat in all_materials:
                if mat.endswith(const.DX11_MAT_SUFFIX):
                    mat_base_name = mat.replace(const.DX11_MAT_SUFFIX, '').split(':')[-1]
                    obj_dict[re.sub('[0-9]+', '', mat_base_name)] = {'Path': mat, 'Parent': None, 'Opts': mapping_opts}

        else:
            # root名は入力からマッピング
            root_data_dict = {'Path': None, 'Parent': None, 'Opts': mapping_opts}
            root_data_dict['Path'] = roots[0]
            root_data_dict['Parent'] = self.__get_parent(roots[0])
            obj_dict[grp_root] = root_data_dict

            # 子階層はunityとmayaでショートネームが一致しているものとしてマッピング
            all_children = cmds.listRelatives(roots[0], ad=True, f=True)
            if all_children:
                for child in all_children:
                    this_dict = {'Path': child, 'Parent': None, 'Opts': mapping_opts}
                    this_dict['Parent'] = self.__get_parent(child)
                    obj_dict[child.split('|')[-1].split(':')[-1]] = this_dict

    def init_axis_obj_mapping(self, maya_obj):
        """基準オブジェクトのマッピングを初期化

        Args:
            maya_obj (str): mayaの基準オブジェクトのパス
        """

        self.axis_obj = maya_obj

    def get_mapping_info(self, grp_id, obj_name):
        """Mayaのobjパスを取得
        """

        if grp_id not in self.obj_mapping_dict:
            return None, None, []

        grp_type = self.obj_mapping_dict[grp_id]['Type']
        obj_dict = self.obj_mapping_dict[grp_id]['Objs']

        if grp_type == const.TYPE_CHARA_MATERIAL:

            # マテリアルの場合はidの数字を無視して判定
            non_id_name = re.sub('[0-9]+', '', obj_name)

            for obj_key in obj_dict:

                non_id_key = re.sub('[0-9]+', '', obj_key)

                if non_id_name == non_id_key:
                    obj_data = obj_dict[obj_key]

                    return obj_data['Path'], obj_data['Parent'], obj_data['Opts']

        else:

            obj_data = obj_dict.get(obj_name)
            if obj_data:
                return obj_data['Path'], obj_data['Parent'], obj_data['Opts']

        return None, None, []

    def get_axis_obj_path(self):
        """基準オブジェクトのパスを取得
        """

        return self.axis_obj

    def __get_parent(self, maya_path):
        """親を取得
        """

        if not maya_path:
            return
        parents = cmds.listRelatives(maya_path, p=True, f=True)
        if parents:
            return parents[0]

    def __get_material_list(self, obj_list):
        """マテリアルを取得
        """

        shapes = []

        for obj in obj_list:

            this_shapes = cmds.listRelatives(obj, s=True, ni=True, f=True)
            if this_shapes:
                shapes.extend(this_shapes)

        shading_engines = []

        for shape in shapes:

            sgs = cmds.listConnections(shape, type='shadingEngine')

            if not sgs:
                continue

            for sg in sgs:
                if sg not in shading_engines:
                    shading_engines.append(sg)

        materials = []

        for shading_engine in shading_engines:

            mtls = cmds.listConnections(shading_engine + '.surfaceShader')

            if not mtls:
                continue

            for mtl in mtls:
                if mtl not in materials:
                    materials.append(mtl)

        return materials
