# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
"""
CGFX Toon系のパラメーターを取得、設定用のmethod群
"""

try:
    # Maya 2022-
    from builtins import object
except:
    pass

import maya.cmds as cmds


class CgfxToonParam(object):

    def __init__(self):
        """
        """

        self.cgfx_suffix = '____cgfx'
        self.cgfx_mtl = None

    def pre_process(self, target_part, data_id):
        """
        """

        self.cgfx_mtl = None

        id_suffix = ''
        # 体操服特殊対応 cgfxシェーダーの値は「mtl_bdy0001_00_1___cgfx」のみ取得/設定する
        if data_id is not None and data_id.find('bdy0001') >= 0:
            id_suffix = '1'

        # cgfxシェーダーが読み込まれてないときにtype=cgfxshaderを行うと
        # cgfx unknownのエラーが出るため、ワンクッション挟む
        tmp_this_cgfx_mtl_list = cmds.ls('*{0}{1}'.format(id_suffix, self.cgfx_suffix))
        if not tmp_this_cgfx_mtl_list:
            return False

        this_cgfx_mtl_list = []
        for tmp_this_cgfx_mtl in tmp_this_cgfx_mtl_list:
            if cmds.objectType(tmp_this_cgfx_mtl) == 'cgfxShader':
                this_cgfx_mtl_list.append(tmp_this_cgfx_mtl)

        if not this_cgfx_mtl_list:
            return False

        for this_cgfx_mtl in this_cgfx_mtl_list:
            if this_cgfx_mtl.find(target_part) >= 0:
                self.cgfx_mtl = this_cgfx_mtl
                break
        else:
            return False

        return True

    def set_cgfx_toon_param(self, target_part, target_attr, value_type, target_value, data_id=None):
        """
        """

        if not self.pre_process(target_part, data_id):
            return

        if not cmds.attributeQuery(target_attr, n=self.cgfx_mtl, exists=True):
            return

        if value_type == 'double3':
            cmds.setAttr('{0}.{1}'.format(self.cgfx_mtl, target_attr), target_value[0], target_value[1], target_value[2], type='double3')
        else:
            cmds.setAttr('{0}.{1}'.format(self.cgfx_mtl, target_attr), target_value)

    def get_cgfx_toon_param(self, target_part, target_attr, default_value=0, data_id=None):
        """
        """

        if not self.pre_process(target_part, data_id):
            return default_value

        if not cmds.attributeQuery(target_attr, n=self.cgfx_mtl, exists=True):
            return default_value

        value = cmds.getAttr('{0}.{1}'.format(self.cgfx_mtl, target_attr))

        return value
