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

import os

from ..base_common import utility as base_utility
from ..glp_common.classes.info import chara_info


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EyeControllerCreator(object):

    # ===============================================
    def __init__(self):

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.chara_info = None

        self.controller_file_path = None

    # ===============================================
    def create(self):

        # ファイルチェック
        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info()

        if not self.chara_info.exists:
            return

        if self.chara_info.part_info.data_id is None:
            return

        # 各名前の確定
        target_namespace = \
            base_utility.namespace.search('chr\d{4}_\d{2}($|_face\d{3}$)')

        if target_namespace != '':
            target_namespace += ':'

        # chara_infoからマテリアル名取得
        material_prefix = ''
        all_material_list = self.chara_info.part_info.material_list

        for material in all_material_list:
            if material.endswith('_eye'):
                material_prefix = material
                break

        eye_material = '{0}{1}'.format(
            target_namespace,
            material_prefix
        )

        eye_big_info_l = '{0}Eye_big_info_L'.format(target_namespace)
        eye_big_info_r = '{0}Eye_big_info_R'.format(target_namespace)

        eye_small_info_l = '{0}Eye_small_info_L'.format(target_namespace)
        eye_small_info_r = '{0}Eye_small_info_R'.format(target_namespace)

        eye_base_info_l = '{0}Eye_base_info_L'.format(target_namespace)
        eye_base_info_r = '{0}Eye_base_info_R'.format(target_namespace)

        eye_kira_info = '{0}Eye_kira_info'.format(target_namespace)

        eye_ctrl_root = 'Rig_eye_high'

        eye_big_ctrl_l = 'Eye_big_info_L_Ctrl'
        eye_big_ctrl_r = 'Eye_big_info_R_Ctrl'

        eye_small_ctrl_l = 'Eye_small_info_L_Ctrl'
        eye_small_ctrl_r = 'Eye_small_info_R_Ctrl'

        eye_base_ctrl_l = 'Eye_base_info_L_Ctrl'
        eye_base_ctrl_r = 'Eye_base_info_R_Ctrl'

        eye_kira_ctrl = 'Eye_kira_info_Ctrl'

        # マテリアル確認
        if not base_utility.node.exists(eye_material):
            return


        # 情報ノード確認
        if not base_utility.node.exists(eye_big_info_l):
            return

        if not base_utility.node.exists(eye_big_info_r):
            return

        if not base_utility.node.exists(eye_small_info_l):
            return

        if not base_utility.node.exists(eye_small_info_r):
            return

        if not base_utility.node.exists(eye_base_info_l):
            return

        if not base_utility.node.exists(eye_base_info_r):
            return

        if not base_utility.node.exists(eye_kira_info):
            return

        # コントローラーファイルの読み込み

        if not base_utility.node.exists(eye_ctrl_root):

            self.controller_file_path = self.script_dir_path + \
                '/resource/rig_eye_high.ma'

            if not os.path.isfile(self.controller_file_path):
                return

            cmds.file(
                self.controller_file_path,
                i=True,
                ignoreVersion=True,
                rpr='_',
                mergeNamespacesOnClash=False,
                f=True
            )

        # コントローラー確認
        if not base_utility.node.exists(eye_ctrl_root):
            return

        if not base_utility.node.exists(eye_big_ctrl_l):
            return

        if not base_utility.node.exists(eye_big_ctrl_r):
            return

        if not base_utility.node.exists(eye_small_ctrl_l):
            return

        if not base_utility.node.exists(eye_small_ctrl_r):
            return

        if not base_utility.node.exists(eye_base_ctrl_l):
            return

        if not base_utility.node.exists(eye_base_ctrl_r):
            return

        if not base_utility.node.exists(eye_kira_ctrl):
            return

        # コントローラとノードの紐づけ
        self.create_eye_controller(
            "big",
            False,
            False,
            eye_big_ctrl_l,
            eye_material,
            eye_big_info_l,
            True
        )

        self.create_eye_controller(
            "big",
            True,
            False,
            eye_big_ctrl_r,
            eye_material,
            eye_big_info_r,
            True
        )

        self.create_eye_controller(
            "small",
            False,
            False,
            eye_small_ctrl_l,
            eye_material,
            eye_small_info_l,
            True
        )

        self.create_eye_controller(
            "small",
            True,
            False,
            eye_small_ctrl_r,
            eye_material,
            eye_small_info_r,
            True
        )

        self.create_eye_controller(
            "base",
            False,
            False,
            eye_base_ctrl_l,
            eye_material,
            eye_base_info_l,
            True
        )

        self.create_eye_controller(
            "base",
            True,
            False,
            eye_base_ctrl_r,
            eye_material,
            eye_base_info_r,
            True
        )

        self.create_eye_controller(
            "kira",
            False,
            True,
            eye_kira_ctrl,
            eye_material,
            eye_kira_info,
            True
        )

        self.create_eye_controller(
            "kira",
            True,
            True,
            eye_kira_ctrl,
            eye_material,
            eye_kira_info,
            False
        )

    # ==================================================
    def create_eye_controller(
        self,
        link_type,
        is_right,
        is_share,
        controller_obj,
        material,
        result_obj,
        delete_node,
    ):
        layered_node = None
        file_node = None
        texture_path = None
        p2d_node = None

        first_multiply_node = None
        second_multiply_node = None
        third_multiply_node = None

        texture_find_name = ''
        first_multiply_node_x_value = -0.1
        third_multiply_node_x_value = -1

        if not base_utility.node.exists(controller_obj):
            return

        if not base_utility.node.exists(result_obj):
            return

        if not base_utility.node.exists(material):
            return

        if link_type == 'big':

            texture_find_name = '_eyehi00'

        if link_type == 'small':

            texture_find_name = '_eyehi01'

        if link_type == 'kira':

            texture_find_name = '_eyehi02'

        if link_type == 'base':

            texture_find_name = '_eye0'
            first_multiply_node_x_value = 0.25
            third_multiply_node_x_value = -4

        layered_node = None

        blendcolor_node = \
            cmds.listConnections('{0}.color'.format(material))

        if not blendcolor_node:
            return

        blendcolor_node = blendcolor_node[0]

        if is_right:

            layered_node = \
                cmds.listConnections('{0}.color1'.format(blendcolor_node))

        else:

            layered_node = \
                cmds.listConnections('{0}.color2'.format(blendcolor_node))

        if not layered_node:
            return

        layered_node = layered_node[0]

        node_list = cmds.listConnections(layered_node, d=True)

        if not node_list:
            return

        file_node_list = []

        for node in node_list:

            this_type = cmds.objectType(node)

            if this_type == 'file':

                file_node_list.append(node)

            elif this_type == 'remapHsv':

                child_node_list = cmds.listConnections(node, d=True)

                if not node_list:
                    continue

                for child_node in child_node_list:

                    if cmds.objectType(child_node) == 'file':

                        file_node_list.append(child_node)

        if not file_node_list:
            return

        for file_node in file_node_list:

            this_texture_path = \
                cmds.getAttr('{0}.fileTextureName'.format(file_node))

            this_texture_name = os.path.basename(this_texture_path)

            find_type = False

            if this_texture_name.find(texture_find_name) >= 0:
                find_type = True

            if not find_type:
                continue

            texture_path = this_texture_path

            break

        if texture_path is None:
            return

        p2d_node = \
            cmds.listConnections('{0}.uvCoord'.format(file_node))

        if not p2d_node:
            return

        p2d_node = p2d_node[0]

        node_suffix = None

        if is_share:
            node_suffix = 'center'
        else:
            if is_right:
                node_suffix = 'right'
            else:
                node_suffix = 'left'

        first_multiply_node = 'multi_01_{0}_{1}_{2}'.format(
            self.chara_info.part_info.data_id, link_type, node_suffix)

        second_multiply_node = 'multi_02_{0}_{1}_{2}'.format(
            self.chara_info.part_info.data_id, link_type, node_suffix)

        third_multiply_node = 'multi_03_{0}_{1}_{2}'.format(
            self.chara_info.part_info.data_id, link_type, node_suffix)

        # 追加されるノードを削除
        if delete_node:

            if base_utility.node.exists(first_multiply_node):
                cmds.delete(first_multiply_node)

            if base_utility.node.exists(second_multiply_node):
                cmds.delete(second_multiply_node)

            if base_utility.node.exists(third_multiply_node):
                cmds.delete(third_multiply_node)

        # ノード作成
        if not base_utility.node.exists(first_multiply_node):
            cmds.shadingNode(
                'multiplyDivide', asUtility=True, name=first_multiply_node)

        if not base_utility.node.exists(second_multiply_node):
            cmds.shadingNode(
                'multiplyDivide', asUtility=True, name=second_multiply_node)

        if not base_utility.node.exists(third_multiply_node):
            cmds.shadingNode(
                'multiplyDivide', asUtility=True, name=third_multiply_node)

        base_utility.attribute.set_value(
            first_multiply_node, 'input2X', first_multiply_node_x_value)
        base_utility.attribute.set_value(
            first_multiply_node, 'input2Y', -0.1)
        base_utility.attribute.set_value(
            first_multiply_node, 'input2Z', -1)

        base_utility.attribute.set_value(
            third_multiply_node, 'input2X', third_multiply_node_x_value)
        base_utility.attribute.set_value(
            third_multiply_node, 'input2Y', -1)
        base_utility.attribute.set_value(
            third_multiply_node, 'input2Z', 1)

        # コントローラと第一乗算ノードのコネクト
        base_utility.attribute.connect(
            controller_obj,
            'translateX',
            first_multiply_node,
            'input1X'
        )

        base_utility.attribute.connect(
            controller_obj,
            'translateY',
            first_multiply_node,
            'input1Y'
        )

        base_utility.attribute.connect(
            controller_obj,
            'rotateZ',
            first_multiply_node,
            'input1Z'
        )

        # 第一乗算ノードとplaced2dTextureのコネクト
        base_utility.attribute.connect(
            first_multiply_node,
            'outputX',
            p2d_node,
            'offsetU'
        )

        base_utility.attribute.connect(
            first_multiply_node,
            'outputY',
            p2d_node,
            'offsetV'
        )

        base_utility.attribute.connect(
            first_multiply_node,
            'outputZ',
            p2d_node,
            'rotateUV'
        )

        # コントローラのScaleXと第二乗算ノードのコネクト
        base_utility.attribute.connect(
            controller_obj,
            'scaleX',
            second_multiply_node,
            'input1X'
        )

        base_utility.attribute.connect(
            controller_obj,
            'scaleX',
            second_multiply_node,
            'input2X'
        )

        # 第二乗算ノードとカラーゲインのコネクト
        base_utility.attribute.connect(
            second_multiply_node,
            'outputX',
            file_node,
            'colorGainR'
        )

        base_utility.attribute.connect(
            second_multiply_node,
            'outputX',
            file_node,
            'colorGainG'
        )

        base_utility.attribute.connect(
            second_multiply_node,
            'outputX',
            file_node,
            'colorGainB'
        )

        # placed2dTextureのUVとUV回転を第三乗算ノードへコネクト
        base_utility.attribute.connect(
            p2d_node,
            'offsetU',
            third_multiply_node,
            'input1X'
        )

        base_utility.attribute.connect(
            p2d_node,
            'offsetV',
            third_multiply_node,
            'input1Y'
        )

        base_utility.attribute.connect(
            p2d_node,
            'rotateUV',
            third_multiply_node,
            'input1Z'
        )

        # 第三乗算ノードを結果オブジェクトへコネクト
        base_utility.attribute.connect(
            third_multiply_node,
            'outputX',
            result_obj,
            'translateX'
        )

        base_utility.attribute.connect(
            third_multiply_node,
            'outputY',
            result_obj,
            'translateY'
        )

        base_utility.attribute.connect(
            third_multiply_node,
            'outputZ',
            result_obj,
            'translateZ'
        )

        # カラーゲインを結果ノードへコネクト
        base_utility.attribute.connect(
            file_node,
            'colorGainR',
            result_obj,
            'scaleX'
        )
