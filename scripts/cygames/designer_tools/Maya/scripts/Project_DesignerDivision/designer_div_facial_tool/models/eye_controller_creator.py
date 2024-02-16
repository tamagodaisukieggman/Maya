# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from . import util

try:
    from builtins import object
except Exception:
    pass


class EyeControllerCreator(object):

    def __init__(self):

        script_file_path = os.path.abspath(__file__)
        script_dir_path = os.path.dirname(script_file_path)
        script_root_dir_path = os.path.dirname(script_dir_path)
        self.controller_file_path = script_root_dir_path + '/resource/rig_eye_high.ma'

        self.data_id = None

        self.controller_file_path = None

    def create(self):

        scene_path = cmds.file(q=True, sn=True)
        if not scene_path:
            return

        self.data_id, _ = os.path.splitext(os.path.basename(scene_path))
        # facial_target名は除く
        self.data_id = self.data_id.replace('_facial_target', '')

        # 各名前の確定
        namespace_list = cmds.namespaceInfo(lon=True)
        target_namespace = ''
        for namespace in namespace_list:
            if self.data_id.find(namespace) >= 0:
                target_namespace = namespace
                break

        if target_namespace != '':
            target_namespace += ':'

        eye_material = ''
        for material in cmds.ls(type='lambert'):
            if material.endswith('_eye'):
                eye_material = material
                break

        # マテリアル確認
        if not cmds.objExists(eye_material):
            util.debug_print('目のマテリアルが見つかりませんでした {}'.format(eye_material), 'WARNING')
            return

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

        # 情報ノード確認
        for info_node in [eye_big_info_l, eye_big_info_r, eye_small_info_l, eye_small_info_r, eye_base_info_l, eye_base_info_r, eye_kira_info]:
            if not cmds.objExists(info_node):
                util.debug_print('情報ノードが存在しません {}'.format(info_node), 'WARNING')
                return

        # コントローラーファイルの読み込み
        if not cmds.objExists(eye_ctrl_root):
            cmds.file(self.controller_file_path, i=True, ignoreVersion=True, rpr='_', mergeNamespacesOnClash=False, f=True)

        # コントローラー確認
        for ctrl_node in [eye_ctrl_root, eye_big_ctrl_l, eye_big_ctrl_r, eye_small_ctrl_l, eye_small_ctrl_r, eye_base_ctrl_l, eye_base_ctrl_r, eye_kira_ctrl]:
            if not cmds.objExists(ctrl_node):
                util.debug_print('コントローラーが存在しません {}'.format(ctrl_node), 'WARNING')
                return

        # コントローラとノードの紐づけ
        self.create_eye_controller('big', False, False, eye_big_ctrl_l, eye_material, eye_big_info_l, True)
        self.create_eye_controller('big', True, False, eye_big_ctrl_r, eye_material, eye_big_info_r, True)

        self.create_eye_controller('small', False, False, eye_small_ctrl_l, eye_material, eye_small_info_l, True)
        self.create_eye_controller('small', True, False, eye_small_ctrl_r, eye_material, eye_small_info_r, True)

        self.create_eye_controller('base', False, False, eye_base_ctrl_l, eye_material, eye_base_info_l, True)
        self.create_eye_controller('base', True, False, eye_base_ctrl_r, eye_material, eye_base_info_r, True)

        self.create_eye_controller('kira', False, True, eye_kira_ctrl, eye_material, eye_kira_info, True)
        self.create_eye_controller('kira', True, True, eye_kira_ctrl, eye_material, eye_kira_info, False)

    # ==================================================
    def create_eye_controller(self, link_type, is_right, is_share, controller_obj, material, result_obj, delete_node):

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

        if not cmds.objExists(controller_obj) or not cmds.objExists(result_obj) or not cmds.objExists(material):
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

        blendcolor_node = cmds.listConnections('{0}.color'.format(material))
        if not blendcolor_node:
            return

        blendcolor_node = blendcolor_node[0]

        if is_right:
            layered_node = cmds.listConnections('{0}.color1'.format(blendcolor_node))
        else:
            layered_node = cmds.listConnections('{0}.color2'.format(blendcolor_node))

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

            this_texture_path = cmds.getAttr('{0}.fileTextureName'.format(file_node))
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

        p2d_node = cmds.listConnections('{0}.uvCoord'.format(file_node))
        if not p2d_node:
            return

        p2d_node = p2d_node[0]

        node_suffix = 'center'

        if not is_share:
            if is_right:
                node_suffix = 'right'
            else:
                node_suffix = 'left'

        first_multiply_node = 'multi_01_{0}_{1}_{2}'.format(self.data_id, link_type, node_suffix)
        second_multiply_node = 'multi_02_{0}_{1}_{2}'.format(self.data_id, link_type, node_suffix)
        third_multiply_node = 'multi_03_{0}_{1}_{2}'.format(self.data_id, link_type, node_suffix)

        # 追加されるノードを削除
        if delete_node:
            if cmds.objExists(first_multiply_node):
                cmds.delete(first_multiply_node)

            if cmds.objExists(second_multiply_node):
                cmds.delete(second_multiply_node)

            if cmds.objExists(third_multiply_node):
                cmds.delete(third_multiply_node)

        # ノード作成
        if not cmds.objExists(first_multiply_node):
            cmds.shadingNode('multiplyDivide', asUtility=True, name=first_multiply_node)

        if not cmds.objExists(second_multiply_node):
            cmds.shadingNode('multiplyDivide', asUtility=True, name=second_multiply_node)

        if not cmds.objExists(third_multiply_node):
            cmds.shadingNode('multiplyDivide', asUtility=True, name=third_multiply_node)

        cmds.setAttr(first_multiply_node + '.input2X'.format(first_multiply_node), first_multiply_node_x_value)
        cmds.setAttr(first_multiply_node + 'input2Y', -0.1)
        cmds.setAttr(first_multiply_node + 'input2Z', -1)

        cmds.setAttr(third_multiply_node + 'input2X', third_multiply_node_x_value)
        cmds.setAttr(third_multiply_node + 'input2Y', -1)
        cmds.setAttr(third_multiply_node + 'input2Z', 1)

        # コントローラと第一乗算ノードのコネクト
        self.__connect_attribute(controller_obj, 'translateX', first_multiply_node, 'input1X')
        self.__connect_attribute(controller_obj, 'translateY', first_multiply_node, 'input1Y')
        self.__connect_attribute(controller_obj, 'rotateZ', first_multiply_node, 'input1Z')

        # 第一乗算ノードとplaced2dTextureのコネクト
        self.__connect_attribute(first_multiply_node, 'outputX', p2d_node, 'offsetU')
        self.__connect_attribute(first_multiply_node, 'outputY', p2d_node, 'offsetV')
        self.__connect_attribute(first_multiply_node, 'outputZ', p2d_node, 'rotateUV')

        # コントローラのScaleXと第二乗算ノードのコネクト
        self.__connect_attribute(controller_obj, 'scaleX', second_multiply_node, 'input1X')
        self.__connect_attribute(controller_obj, 'scaleX', second_multiply_node, 'input2X')

        # 第二乗算ノードとカラーゲインのコネクト
        self.__connect_attribute(second_multiply_node, 'outputX', file_node, 'colorGainR')
        self.__connect_attribute(second_multiply_node, 'outputX', file_node, 'colorGainG')

        self.__connect_attribute(second_multiply_node, 'outputX', file_node, 'colorGainB')

        # placed2dTextureのUVとUV回転を第三乗算ノードへコネクト
        self.__connect_attribute(p2d_node, 'offsetU', third_multiply_node, 'input1X')
        self.__connect_attribute(p2d_node, 'offsetV', third_multiply_node, 'input1Y')
        self.__connect_attribute(p2d_node, 'rotateUV', third_multiply_node, 'input1Z')

        # 第三乗算ノードを結果オブジェクトへコネクト
        self.__connect_attribute(third_multiply_node, 'outputX', result_obj, 'translateX')
        self.__connect_attribute(third_multiply_node, 'outputY', result_obj, 'translateY')
        self.__connect_attribute(third_multiply_node, 'outputZ', result_obj, 'translateZ')

        # カラーゲインを結果ノードへコネクト
        self.__connect_attribute(file_node, 'colorGainR', result_obj, 'scaleX')

    def __connect_attribute(self, org_node, org_attr, dst_node, dst_attr):

        org_set_attr = '{}.{}'.format(org_node, org_attr)
        dst_set_attr = '{}.{}'.format(dst_node, dst_attr)

        if cmds.isConnected(org_set_attr, dst_set_attr):
            return

        cmds.connectAttr(org_set_attr, dst_set_attr)
