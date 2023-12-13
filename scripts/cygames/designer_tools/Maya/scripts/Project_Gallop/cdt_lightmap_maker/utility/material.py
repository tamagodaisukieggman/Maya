# -*- coding: utf-8 -*-

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
import maya.mel as mel

from . import node as utility_node
from . import attribute as utility_attribute


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Method(object):

    # ===========================================
    @staticmethod
    def create_new_material(material_new_name):
        """マテリアル作成
        """

        if utility_node.Method.exist_node(material_new_name):
            return

        shading_engine_name = material_new_name + 'SG'

        cmds.shadingNode('lambert', asShader=True,
                         name=material_new_name)

        cmds.sets(
            renderable=True, noSurfaceShader=True, empty=True,
            name=shading_engine_name
        )

        utility_attribute.Method.connect_attr(
            material_new_name, 'outColor',
            shading_engine_name, 'surfaceShader'
        )

    # ===========================================
    @staticmethod
    def get_material_list(target_transform):
        """マテリアルリスト取得

        :param target_material:対象トランスフォーム
        """

        shape = utility_node.Method.get_mesh_shape(target_transform)

        if shape is None:
            return

        shading_engine_list = cmds.listConnections(shape, type="shadingEngine")

        if shading_engine_list is None:
            return

        if len(shading_engine_list) == 0:
            return

        fix_shading_engine_list = []

        for shading_engine in shading_engine_list:

            exist = False
            for fix_shading_engine in fix_shading_engine_list:

                if shading_engine == fix_shading_engine:
                    exist = True

            if exist:
                continue

            fix_shading_engine_list.append(shading_engine)

        material_list = []

        for shading_engine in fix_shading_engine_list:

            this_material_list =\
                cmds.listConnections(shading_engine + ".surfaceShader")

            if this_material_list is None:
                continue

            if len(this_material_list) == 0:
                continue

            material_list.extend(this_material_list)

        return material_list

    # ==================================================
    @staticmethod
    def get_shading_group(target_material):
        """マテリアルからシェーディンググループを取得

        :param target_material:対象マテリアル
        """

        if target_material is None:
            return

        if not cmds.objExists(target_material):
            return

        shading_group_list = \
            cmds.listConnections(target_material, t='shadingEngine')

        if shading_group_list is None:
            return

        if len(shading_group_list) == 0:
            return

        return shading_group_list[0]

    # ==================================================
    @staticmethod
    def assign_material(target_material, target_list):
        """マテリアルを割り当て

        :param target_material:対象マテリアル
        :param target_list:対象リスト
        """

        material_sg = Method.get_shading_group(target_material)

        if material_sg is None:
            return

        if target_list is None:
            return

        if len(target_list) == 0:
            return

        cmds.select(target_list, r=True)

        cmds.sets(e=True, forceElement=material_sg)

    # ==================================================
    @staticmethod
    def get_node_list_with_material(target_material, target_list=None):
        """マテリアルを使用しているノードリストを取得

        :param target_material:対象マテリアル
        :param target_list:対象リスト Noneのときはすべて対象
        """

        cmds.select(cl=True)

        material_sg = Method.get_shading_group(target_material)

        if material_sg is None:
            return

        if target_list is None:
            cmds.select(material_sg, r=True, ne=False)
            return cmds.ls(sl=True, l=True, fl=True)

        if len(target_list) == 0:
            cmds.select(material_sg, r=True, ne=False)
            return cmds.ls(sl=True, l=True, fl=True)

        cmds.select(target_list, r=True)
        cmds.select(target_material, add=True)

        mel.eval("HideUnselectedObjects")

        cmds.select(material_sg, r=True, ne=False)
        cmds.select(vis=True)

        mel.eval("ShowLastHidden")

        return cmds.ls(sl=True, l=True, fl=True)
