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

import re

import maya.cmds as cmds

from ....glp_common.classes.info import chara_info


class EyeUvChanger(object):

    def __init__(self):
        """
        """

        self.mdl_node = ""
        self.mtl_node = ""
        self.lt_node = ""

    def main(self, flag):
        """
        実行関数
        :param flag: "oldUV": 旧仕様UVに変更 "newUV": 新仕様UVに変更
        :return:
        """

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            return

        mesh_nodes = _chara_info.part_info.mesh_list
        for node in mesh_nodes:
            if not node.endswith("M_Face"):
                continue
            cmds.polyUVSet(node, currentUVSet=True, uvSet="map1")

        # rootノードを取得する
        mdl_node = _chara_info.part_info.root_node
        if not mdl_node:
            return
        self.mdl_node = mdl_node
        if not cmds.objExists(self.mdl_node):
            return

        self.mtl_node = self.mdl_node.replace("mdl", "mtl").replace("|", "") + "_eye"
        if not cmds.objExists(self.mtl_node):
            return

        self.lt_node = self.mdl_node.replace("mdl", "lt")

        # UVを等倍にひろげる
        if flag == "oldUV":
            self.change_old_uv_view()
        # UVを新仕様に合わせる
        elif flag == "newUV":
            self.change_new_uv_view()

    def change_new_uv_view(self):
        """
        UVを新仕様に戻す
        """

        for suffix in ["r", "l"]:
            dummy_shader = "dummy_eye_shader_" + suffix
            if not cmds.objExists(dummy_shader):
                return

            # アサインされているフェース取得
            selected = cmds.ls(sl=True)
            cmds.hyperShade(objects=dummy_shader)
            eye_faces = cmds.ls(sl=True, l=True, fl=True)
            cmds.select(selected)

            layered_texture_nodes = cmds.listConnections(dummy_shader + ".color")
            if not layered_texture_nodes:
                return
            layered_texture_node = layered_texture_nodes[0]
            cmds.disconnectAttr(layered_texture_node + ".outColor", dummy_shader + ".color")

            blendColor_eye_nodes = cmds.ls("blendColor_eye")
            if not blendColor_eye_nodes:
                return
            blendColor_eye_node = blendColor_eye_nodes[0]

            place2d_node = self.search_place2dtexture_node(layered_texture_node)
            if not place2d_node:
                return

            mtl_sg_nodes = cmds.listConnections(self.mtl_node + ".outColor")
            if not mtl_sg_nodes:
                return
            mtl_sg_node = mtl_sg_nodes[0]

            cmds.sets(eye_faces, e=True, forceElement=mtl_sg_node)

            if suffix == "r":
                cmds.connectAttr(layered_texture_node + '.outColor', blendColor_eye_node + '.color1', f=True)
                cmds.polyEditUV(eye_faces, su=1, sv=0.5)
                cmds.setAttr(place2d_node + ".repeatV", 1)

            elif suffix == "l":
                cmds.connectAttr(layered_texture_node + '.outColor', blendColor_eye_node + '.color2', f=True)
                cmds.polyEditUV(eye_faces, pu=-0.25, pv=1, su=1, sv=0.5)
                cmds.setAttr(place2d_node + ".repeatV", 1)
                cmds.setAttr(place2d_node + ".offsetV", 0)

            cmds.delete(dummy_shader)

    def change_old_uv_view(self):
        """
        UVを旧仕様に変更する
        """

        # 目のface取得
        eye_face_r_list, eye_face_l_list = self.set_eye_face_list()

        blendColor_eye_nodes = cmds.ls("blendColor_eye")
        if not blendColor_eye_nodes:
            return
        blendColor_eye_node = blendColor_eye_nodes[0]

        layered_texture_node_r = ""
        layered_texture_node_l = ""
        for attr in ["color1", "color2"]:
            blendColor_eye_color_attr = blendColor_eye_node + "." + attr
            layered_texture_nodes = cmds.listConnections(blendColor_eye_color_attr, d=True)
            if not layered_texture_nodes:
                return
            layered_texture_node = layered_texture_nodes[0]

            if (self.lt_node + "_eye_r").endswith(layered_texture_node):
                layered_texture_node_r = layered_texture_node
            elif (self.lt_node + "_eye_l").endswith(layered_texture_node):
                layered_texture_node_l = layered_texture_node
            else:
                return

            cmds.disconnectAttr(layered_texture_node + ".outColor", blendColor_eye_color_attr)

        for suffix in ["r", "l"]:
            dummy_shader_node, dummy_sg_node = self.create_shader("dummy_eye_shader_" + suffix)

            if suffix == "r":
                # Rの処理
                cmds.connectAttr(layered_texture_node_r + ".outColor", dummy_shader_node + ".color")
                cmds.sets(eye_face_r_list, e=True, forceElement=dummy_sg_node)
                cmds.polyEditUV(eye_face_r_list, su=1, sv=2)

                place2d_node = self.search_place2dtexture_node(layered_texture_node_r)
                if not place2d_node:
                    return

                cmds.setAttr(place2d_node + ".repeatV", 0.5)

            elif suffix == "l":
                # Lの処理
                cmds.connectAttr(layered_texture_node_l + ".outColor", dummy_shader_node + ".color")
                cmds.sets(eye_face_l_list, e=True, forceElement=dummy_sg_node)
                cmds.polyEditUV(eye_face_l_list, pu=0.25, pv=1, su=1, sv=2)

                place2d_node = self.search_place2dtexture_node(layered_texture_node_l)
                if not place2d_node:
                    return

                cmds.setAttr(place2d_node + ".repeatV", 0.5)
                cmds.setAttr(place2d_node + ".offsetV", 0.5)

    def set_eye_face_list(self):
        """
        左右の目のアサイン対象フェースをそれぞれ取得
        :return: 左右の目のアサイン対象フェース
        """
        selected = cmds.ls(sl=True)

        eye_face_r_list = []
        eye_face_l_list = []

        # 左右の目の対象ポリゴンを取得する
        cmds.hyperShade(objects=self.mtl_node)
        eye_faces = cmds.ls(sl=True, l=True, fl=True)

        for eye_face in eye_faces:
            # フェースのバウンディングボックス取得
            face_bb_pos = cmds.xform(eye_face, q=True, bb=True)
            face_bb_x_min = face_bb_pos[0]
            face_bb_x_max = face_bb_pos[3]

            if face_bb_x_min < 0 and face_bb_x_max < 0:
                eye_face_r_list.append(eye_face)
            elif face_bb_x_min > 0 and face_bb_x_max > 0:
                eye_face_l_list.append(eye_face)

        cmds.select(selected)

        return eye_face_r_list, eye_face_l_list

    def search_place2dtexture_node(self, node):
        """
        place2dTextureノードをノードを辿って検索、取得する
        :param node: 検索するノード
        :return: place2dTextureの名前
        """
        file_nodes = cmds.listConnections(node, d=False, s=True, type="file", exactType=True)
        file_node = ""
        for node in file_nodes:
            search_node = re.search(self.lt_node.replace("lt", "Tex"), node)
            if search_node:
                file_node = node
                break

        if not file_node:
            return

        place2d_nodes = cmds.listConnections(
            file_node + ".uvCoord", d=False, s=True, type="place2dTexture", exactType=True
        )
        if not place2d_nodes:
            return

        return place2d_nodes[0]

    def create_shader(self, shader_name):
        """
        lambertシェーダーを作成する
        :param shader_name: 作成するシェーダー名
        :return: 作成したシェーダーの名前, SGの名前
        """

        shader = cmds.shadingNode("lambert", asShader=True, name=shader_name)
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shader_name + "SG")
        cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", f=True)

        return shader, sg
