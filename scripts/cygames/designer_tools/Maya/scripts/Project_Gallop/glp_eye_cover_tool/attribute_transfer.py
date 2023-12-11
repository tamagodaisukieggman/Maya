# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds

from .. import base_common
from ..base_common import utility as base_utility
from ..base_common import classes as base_class

reload(base_common)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class AttributeTransfer(object):
    """法線やカラーアトリビュートをM_Faceから目隠しメッシュに転送するためのクラス
    """

    # ===============================================
    def __init__(self):
        """コンストラクタ
        """

        self.target_transform = None

        self.chara_info = None
        self.m_face = None

        self.is_ready = False

    # ===============================================
    def initialize(self, target_transform, chara_info):
        """初期化

        Args:
            target_transform(str): 目隠しメッシュ
            chara_info(chara_info.CharaInfo): 現在のシーンのCharaInfoインスタンス
        """

        if not cmds.objExists(target_transform):
            return

        self.target_transform = target_transform

        for mesh in chara_info.part_info.mesh_list:
            if mesh.endswith('|M_Face'):
                self.m_face = mesh

        if not self.m_face or not cmds.objExists(self.m_face):
            return

        self.is_ready = True

    # ===============================================
    def transfer(self):
        """法線とカラーの転送の実行
        """

        if not self.is_ready:
            return

        self._transferVtxColor(self.m_face, self.target_transform)

        self._transferVtxNormal(self.m_face, self.target_transform)

    # ===============================================
    def _transferVtxColor(self, src, dst):
        """頂点カラーの転送

        Args:
            src: 転送元オブジェクト
            dst: 転送先オブジェクト
        """

        cmds.transferAttributes(src, dst, pos=0, nml=0, uvs=0, col=1, spa=0, sm=3, fuv=0, clb=0)

        cmds.delete(ch=True)

        # 頂点カラーのb以外は0にする
        vtx_list = cmds.ls(dst + '.vtx[*]', l=True, fl=True)
        cmds.polyColorPerVertex(vtx_list, r=0, g=0)

        cmds.delete(ch=True)

    # ===============================================
    def _transferVtxNormal(self, src, dst):
        """法線の転送

        Args:
            src: 転送元オブジェクト
            dst: 転送先オブジェクト
        """

        src_info = base_class.mesh.normal_info.NormalInfo()
        src_info.create_info([src])

        dst_info = base_class.mesh.normal_info.NormalInfo()
        dst_info.create_info([dst])

        base_utility.mesh.normal.paste_normal_by_vertex_position(src_info, dst_info)

        cmds.polySoftEdge(dst)

        cmds.delete(ch=True)
