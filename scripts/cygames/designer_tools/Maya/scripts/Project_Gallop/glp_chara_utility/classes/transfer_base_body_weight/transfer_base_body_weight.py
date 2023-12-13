# -*- coding: utf-8 -*-
"""
"""

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import os

import maya.cmds as cmds

from ....base_common import classes as base_class
from ....base_common import utility as base_utility

from ....glp_common.classes.info import chara_info


class TransferBaseBodyWeight(object):
    """
    """

    def __init__(self):
        """
        """

        self.bdy0000_mdl_svn_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/body/bdy0000_00/scenes/mdl_bdy0000_00.ma'
        self.bdy0000_namespace = 'refbdy0001'
        self.bdy0000_mdl_top_node = '{0}:mdl_bdy0000_00'.format(self.bdy0000_namespace)
        self.bdy0000_mdl_mbody_node = '{0}|{1}:M_Body'.format(self.bdy0000_mdl_top_node, self.bdy0000_namespace)

        self.size_list = [
            'SS', 'S', 'M', 'L', 'LL'
        ]

    def set_base_body_weight_data(self):
        """
        選択した頂点に素体のweightをPositionコピー
        """

        selected = cmds.ls(sl=True)
        if not selected:
            cmds.warning('何も選択されていません')
            return

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists or not _chara_info.data_info.exists:
            cmds.warning('キャラクターの情報が取得できませんでした')
            return

        height_num = _chara_info.data_info.height_id
        shape_num = _chara_info.data_info.shape_id
        bust_num = _chara_info.data_info.bust_id

        height_type = self.size_list[height_num]
        bust_type = self.size_list[bust_num]

        # 素体リファレンスをロード
        if not os.path.exists(self.bdy0000_mdl_svn_path):
            cmds.warning('SVNの素体が見つかりません : {0}'.format(self.bdy0000_mdl_svn_path))
            return

        base_utility.reference.load(self.bdy0000_mdl_svn_path, self.bdy0000_namespace)

        if not cmds.objExists(self.bdy0000_mdl_top_node):
            cmds.warning('素体のトップノードが見つかりません : {0}'.format(self.bdy0000_mdl_top_node))
            return

        if cmds.objExists(self.bdy0000_mdl_mbody_node):

            # 素体のblendShapeノードを検索
            blend_shape_nodes = cmds.ls(cmds.listHistory(self.bdy0000_mdl_mbody_node), type='blendShape')

            if blend_shape_nodes:

                # blendShapeノードが複数ついている場合は対象不明なので1番目を対象とする
                blend_shape_node = blend_shape_nodes[0]

                blend_shape_height_attr = 'M_Body_Height_{}'.format(height_type)
                if cmds.attributeQuery(blend_shape_height_attr, node=blend_shape_node, exists=True):
                    cmds.setAttr('{0}.{1}'.format(blend_shape_node, blend_shape_height_attr), 1)

                blend_shape_shape_attr = 'M_Body_Shape_{}'.format(str(shape_num))
                if cmds.attributeQuery(blend_shape_shape_attr, node=blend_shape_node, exists=True):
                    cmds.setAttr('{0}.{1}'.format(blend_shape_node, blend_shape_shape_attr), 1)

                blend_shape_bust_attr = 'M_Body_Bust_{}'.format(bust_type)
                if cmds.attributeQuery(blend_shape_bust_attr, node=blend_shape_node, exists=True):
                    cmds.setAttr('{0}.{1}'.format(blend_shape_node, blend_shape_bust_attr), 1)

        src_skin_info = base_class.mesh.skin_info.SkinInfo()
        src_skin_info.create_info([self.bdy0000_mdl_top_node])

        # 素体リファレンスをアンロード
        base_utility.reference.unload(self.bdy0000_mdl_svn_path, self.bdy0000_namespace)

        dst_skin_info = base_class.mesh.skin_info.SkinInfo()
        dst_skin_info.create_info(selected)

        base_utility.mesh.skin.paste_weight_by_vertex_position(src_skin_info, dst_skin_info)
