# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import re
import shutil
import glob
import itertools

import maya.cmds as cmds
import maya.mel as mel


# ==================================================
def set_texture(material_name, attr, texture_path):

    if not cmds.objExists(material_name):
        return False

    attr_list = cmds.listAttr(material_name)
    if attr not in attr_list:
        return False

    files = cmds.listConnections('{0}.{1}'.format(material_name, attr), type='file')
    if not files:
        return False

    cmds.setAttr('{}.{}'.format(files[0], 'fileTextureName'), texture_path, typ='string')
    return True


# ==================================================
def set_attr_value(material_name, attr, value):

    if not cmds.objExists(material_name):
        return False

    attr_list = cmds.listAttr(material_name)
    if attr not in attr_list:
        return False

    try:
        cmds.setAttr('{}.{}'.format(material_name, attr), lock=False)
        if type(value) == list:
            cmds.setAttr('{}.{}'.format(material_name, attr), *value)
        else:
            cmds.setAttr('{}.{}'.format(material_name, attr), value)
        return True
    except Exception as e:
        print(e)
        return False


# ==================================================
def replace_material(src_material, dst_material, target_mesh=''):

    if not cmds.objExists(src_material) or not cmds.objExists(dst_material):
        return

    cmds.hyperShade(objects=src_material)

    # targetはmeshタイプで返ってくるはず
    target_list = cmds.ls(sl=True, fl=True, l=True)

    if not target_list:
        return

    fix_target_list = []

    if not target_mesh:
        fix_target_list = target_list
    else:
        for target in target_list:
            if target.find('.f') >= 0:
                # target は |mdl_chr1001_00|M_Face_Outline.f[525] のような形式
                target_short_name = target.split('|')[-1]
                target_short_name = target_short_name.split('.')[0]
                if target_short_name == target_mesh.split('|')[-1]:
                    fix_target_list.append(target)
            else:
                # target は |mdl_chr1001_00|M_Face_OutlineShape のような形式
                target_shape = cmds.listRelatives(target_mesh, s=True, ni=True, f=True)[0]
                if target.split('|')[-1] == target_shape.split('|')[-1]:
                    fix_target_list.append(target)

    if not fix_target_list:
        return

    cmds.select(fix_target_list, r=True)
    cmds.hyperShade(assign=dst_material)

    cmds.select(cl=True)


# ==================================================
def get_all_file_node_list(material_name):

    if not cmds.objExists(material_name):
        return []

    all_attrs = cmds.listAttr(material_name)

    all_file_nodes = []
    for attr in all_attrs:
        file_nodes = cmds.listConnections('{0}.{1}'.format(material_name, attr), type='file')
        if file_nodes:
            all_file_nodes.extend(file_nodes)

    return list(set(all_file_nodes))


# ==================================================
def get_shading_engine(material_name):

    if not cmds.objExists(material_name):
        return ''

    shading_engines = cmds.listConnections('{0}.{1}'.format(material_name, "outColor"), type="shadingEngine")

    if not shading_engines:
        return ''

    return shading_engines[0]


# ==================================================
def delete_file_and_2d_nodes(file_nodes, is_force=False):

    target_file_nodes = []
    for file_node in file_nodes:

        # 強制じゃない場合は接続がないことを確認する
        if is_force:
            target_file_nodes.append(file_node)
        else:
            material_connection_list = cmds.listConnections('{}.outColor'.format(file_node), s=False)
            if not material_connection_list:
                target_file_nodes.append(file_node)

    target_place_2d_nodes = []
    for file_node in target_file_nodes:
        place_2ds = cmds.listConnections(file_node, type='place2dTexture')
        if place_2ds:
            target_place_2d_nodes.extend(list(set(place_2ds)))

    cmds.delete(target_file_nodes + target_place_2d_nodes)

