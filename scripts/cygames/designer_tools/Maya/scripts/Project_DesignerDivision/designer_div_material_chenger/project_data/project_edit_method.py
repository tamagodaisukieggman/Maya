# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from . import project_define as pj_define
from .. import tool_define as tool_define


# ==================================================
def create_project_material(material_name, shader_file, target_mesh):

    result_material = None

    # 今のところdx11シェーダーしかない
    if shader_file:
        result_material = __create_dx11_material(material_name, shader_file, target_mesh)
    else:
        result_material = __create_lambert_material(material_name)

    return result_material


# ==================================================
def __create_lambert_material(material_name):

    result_material = None

    try:
        result_material = cmds.shadingNode('lambert', name=material_name, asShader=True)
    except Exception:
        result_material = None

    return result_material


# ==================================================
def __create_dx11_material(material_name, shader_file, mesh):

    if not cmds.pluginInfo("dx11Shader", query=True, loaded=True):
        cmds.loadPlugin("dx11Shader.mll")

    if not cmds.pluginInfo("matrixNodes", query=True, loaded=True):
        cmds.loadPlugin("matrixNodes.mll")

    result_material = None
    shader_file_path = '{}/{}'.format(pj_define.shader_dir_path, shader_file).replace('\\', '/')

    result_material = cmds.shadingNode('dx11Shader', name=material_name, asShader=True)
    cmds.setAttr(result_material + '.shader', shader_file_path, typ='string')
    __apply_vertex_color_attr_to_dx11(result_material, mesh)

    return result_material


# ==================================================
def __apply_vertex_color_attr_to_dx11(target_dx11_material, mesh):

    mesh_str = ''

    if target_dx11_material.find(pj_define.MTL_SFX_FACE) >= 0:
        mesh_str = pj_define.MSH_FACE_STR
    elif target_dx11_material.find(pj_define.MTL_SFX_HAIR) >= 0:
        mesh_str = pj_define.MSH_HAIR_STR
    elif target_dx11_material.find(pj_define.MTL_PFX_BODY) >= 0:
        mesh_str = pj_define.MSH_BODY_STR
    elif target_dx11_material.find(pj_define.MTL_SFX_MAYU) >= 0:
        mesh_str = pj_define.MSH_MAYU_STR

    if mesh.find(mesh_str) < 0:
        return

    target_color_set_list = cmds.polyColorSet(mesh, q=True, acs=True)

    if not target_color_set_list:
        return

    target_color_set = target_color_set_list[0]

    shader_attr_list = cmds.listAttr(target_dx11_material)
    if 'Position_Source' in shader_attr_list:
        cmds.setAttr('{}.{}'.format(target_dx11_material, 'Position_Source'), 'position', type='string')
    if 'TexCoord0_Source' in shader_attr_list:
        cmds.setAttr('{}.{}'.format(target_dx11_material, 'TexCoord0_Source'), 'uv:map1', type='string')
    if 'Normal_Source' in shader_attr_list:
        cmds.setAttr('{}.{}'.format(target_dx11_material, 'Normal_Source'), 'normal', type='string')
    if 'Color0_Source' in shader_attr_list:
        cmds.setAttr('{}.{}'.format(target_dx11_material, 'Color0_Source'), '{}{}'.format('color:', target_color_set), type='string')


# ==================================================
def execute_project_command_settingup(command_key, material_data):

    if command_key == pj_define.CMD_CHARA_LIGHT_CONNECTION:
        __setup_chara_light()
        __connect_chara_light(material_data.name)

    if command_key == pj_define.CMD_SPEC_LOC_CONNECTION:
        __connect_spec_locator(material_data.name)

    if command_key == pj_define.CMD_HEAD_LOCATOR_CONNECTION:
        __connect_head_center_locator(material_data.name)

    if command_key == pj_define.CMD_OUTLINE_MESH_VISIBLE:
        __set_mesh_visible(material_data.mesh, True)


# ==================================================
def execute_project_command_removing(command_key, material_data):

    if command_key == pj_define.CMD_CHARA_LIGHT_CONNECTION:
        __remove_chara_light()

    if command_key == pj_define.CMD_HEAD_LOCATOR_CONNECTION:
        __remove_matrix_decomposer(material_data.name)

    if command_key == pj_define.CMD_OUTLINE_MESH_VISIBLE:
        __set_mesh_visible(material_data.mesh, False)


# ==================================================
def __setup_chara_light():

    if not cmds.objExists(pj_define.CHARA_LIGHT_NAME):
        cmds.pointLight(name=pj_define.CHARA_LIGHT_NAME)

    cmds.setAttr('{}.{}'.format(pj_define.CHARA_LIGHT_NAME, 'translate'), 30, 30, 30)


# ==================================================
def __connect_chara_light(material_name):

    scr_attr = '{}.{}'.format(pj_define.CHARA_LIGHT_NAME, 'translate')
    dst_attr = '{}.{}'.format(material_name, 'xWorldSpaceLightPos0')
    cmds.connectAttr(scr_attr, dst_attr, f=True)


# ==================================================
def __remove_chara_light():

    if not cmds.objExists(pj_define.CHARA_LIGHT_NAME):
        return

    if not cmds.listConnections('{}.{}'.format(pj_define.CHARA_LIGHT_NAME, 'translate'), s=False):
        cmds.delete(pj_define.CHARA_LIGHT_NAME)


# ==================================================
def __connect_head_center_locator(material_name):

    target_locator_name = pj_define.LOC_HAIR_CENTER
    if material_name.find(pj_define.MTL_SFX_FACE) >= 0:
        target_locator_name = pj_define.LOC_FACE_CENTER

    target_locators = cmds.ls(target_locator_name, type='transform')
    if not target_locators:
        return

    matrix_decomposer = material_name + '_world_matrix_decomposer'
    if not cmds.objExists(matrix_decomposer):
        cmds.shadingNode('decomposeMatrix', au=True, n=matrix_decomposer)

    cmds.connectAttr(target_locators[0] + '.worldMatrix[0]', matrix_decomposer + '.inputMatrix', f=True)
    cmds.connectAttr(matrix_decomposer + '.outputTranslate', material_name + '.xFaceCenterPos', f=True)


# ==================================================
def __remove_matrix_decomposer(material_name):

    target_node_name = material_name + '_world_matrix_decomposer'
    target_nodes = cmds.ls(target_node_name)

    if target_nodes:
        cmds.delete(target_nodes)


# ==================================================
def __connect_spec_locator(material_name):

    spec_locator = __get_spec_color_locator(material_name)

    if spec_locator:
        # 初期値を取得
        spec_color_dict = __get_current_spec_color_dict(spec_locator)
        for attr, val in list(spec_color_dict.items()):
            cmds.setAttr('{}.{}'.format(material_name, attr), *val)

        # コネクト
        spec_connect_dict = __get_spec_color_connect_dict(material_name, spec_locator)
        for attr, val in list(spec_connect_dict.items()):
            if not cmds.isConnected(attr, val):
                cmds.connectAttr(attr, val, f=True)


# ==================================================
def __get_spec_color_locator(material_name):

    target_locater_name = ''

    if material_name.find(pj_define.MTL_SFX_FACE) >= 0:
        target_locater_name = pj_define.LOC_FACE_SPEC
    elif material_name.find(pj_define.MTL_SFX_HAIR) >= 0:
        target_locater_name = pj_define.LOC_HAIR_SPEC
    elif material_name.find(pj_define.MTL_PFX_BODY) >= 0:
        target_locater_name = pj_define.LOC_BODY_SPEC

    target_locator = cmds.ls(target_locater_name, type='transform', l=True)

    if not target_locator:
        return ''
    else:
        return target_locator[0]


# ==================================================
def __get_current_spec_color_dict(spec_locator):

    specular_color = [1.0, 1.0, 1.0]
    if cmds.objExists(spec_locator):
        specular_color = cmds.getAttr(spec_locator + '.scale')[0]

    return {
        'xSpecularColorRGB': specular_color
    }


# ==================================================
def __get_spec_color_connect_dict(material_name, spec_locator):

    return {
        material_name + '.xSpecularColorR': spec_locator + '.scale.scaleX',
        material_name + '.xSpecularColorG': spec_locator + '.scale.scaleY',
        material_name + '.xSpecularColorB': spec_locator + '.scale.scaleZ',
    }


# ==================================================
def __set_mesh_visible(mesh, is_visible):

    if not cmds.objExists(mesh):
        return
    cmds.setAttr(mesh + '.visibility', is_visible)