# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import os
import re
import shutil
import glob

import maya.cmds as cmds
import maya.mel as mel
from ..add_chara_info_obj import add_chara_info_obj
from . import cgfx_param_setting

from ....base_common import utility as base_utility

from ....farm_common.classes.info import chara_info
from ....farm_common.utility import model_define
from ....farm_common.utility import model_mesh_finder
from ....farm_common.utility import model_texture_finder

reload(add_chara_info_obj)
reload(cgfx_param_setting)
reload(model_define)
reload(model_mesh_finder)
reload(model_texture_finder)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TextureChanger(object):

    # ==================================================
    def __init__(self, root):

        self.root = root

        self.divide_flag = '____'

        self.chara_light0 = 'charaLight0'

        self.chara_light0_cgfx_vector = 'charaLight0_cgfxVector'

        self.cgfx_file_path_list = []

        self.dirt_toggle_list = []

        self.chara_info = None

        script_dir_path = os.path.dirname(__file__)
        classes_dir_path = os.path.dirname(script_dir_path)
        root_dir_path = os.path.dirname(classes_dir_path)
        self.resource_dir_path = '{0}/_resource'.format(root_dir_path)

        self.cgfx_dir_path = '{}/{}'.format(self.resource_dir_path, 'Cgfx')
        self.cgfx_tmp_path = '{}/{}'.format(self.cgfx_dir_path, '_tmp')
        self.cgfx_outline_tmp_path = '{}/{}'.format(self.cgfx_dir_path, '_outline_tmp')
        self.texture_dir_path = '{}/{}'.format(self.resource_dir_path, 'Textures')

    # ==================================================
    def __create_spec_info(self):

        add_obj = add_chara_info_obj.AddCharaInfoObj()
        if self.chara_info.part_info.data_type.endswith('head'):

            add_obj.add_obj('locator', 'Face_spec_info')
            add_obj.add_obj('locator', 'Hair_spec_info')

        elif self.chara_info.part_info.data_type.endswith('body'):

            match_obj = re.match('bdy0001_[0-9]{2}', self.chara_info.data_id)

            if match_obj:

                add_obj.add_obj('locator', 'Body_spec_info_0')
                add_obj.add_obj('locator', 'Body_spec_info_1')
                add_obj.add_obj('locator', 'Body_spec_info_2')

            else:

                add_obj.add_obj('locator', 'Body_spec_info')

    # ==================================================
    def change_texture(self, change_type):

        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info()

        if not self.chara_info.exists:
            return

        self.__create_spec_info()

        if change_type == 'cgfx':

            if self.chara_info is None:
                self.chara_info = chara_info.CharaInfo()
                self.chara_info.create_info()

            if self.chara_info.exists:
                self.apply_cgfx()

        elif change_type == 'cgfx_outline':

            self.__change_outline_visible_state(True)
            self.apply_outline_cgfx()

        elif change_type == 'psd':

            self.change_default_material()
            self.change_texture_path('psd')

        elif change_type == 'default':

            self.change_default_material()
            self.change_texture_path('default')

        elif change_type == 'cgfx_outline_default':
            # アウトラインのマテリアルをベースに合わせる
            self.__change_outline_visible_state(False)
            self.adjust_outline_material_to_base_material()
            self.remove_cgfx_material(is_outline=True)

        if change_type.find('cgfx') < 0:
            self.remove_cgfx_material()

    # ==================================================
    def change_texture_path(self, texture_type):

        naming_rule = self.chara_info.part_info.material_naming_rule_list[0]
        pattern = re.compile(naming_rule)

        tmp_material_list = cmds.ls(mat=True)
        target_material_list = []

        for material in tmp_material_list:
            if pattern.match(material):
                target_material_list.append(material)

        for material in target_material_list:
            texture_name = ''

            texture_list = model_texture_finder.get_texture_list_from_material(
                material, texture_type == 'psd')

            if texture_type == 'psd':
                texture_name = texture_list[0]

            elif texture_type == 'default':
                for texture in texture_list:
                    if 'diff' in texture:
                        texture_name = texture
                        break

            if not texture_name:
                continue

            texture_path = '{}/{}'.format(
                self.chara_info.part_info.maya_sourceimages_dir_path,
                texture_name)

            if not texture_path:
                print('テクスチャのパスが取得できませんでした')
                continue

            if not os.path.exists(texture_path):
                print('テクスチャのパスが存在しませんでした : {0}'.format(texture_path))
                continue

            self.apply_file_to_material_attr(material, "color", texture_path)

    # ==================================================
    def apply_cgfx(self):

        self.__remove_tmp_cgfx_dir()
        self.load_plugins()
        self.create_chara_light()

        # grp_mesh直下のアウトラインでないメッシュリスト
        main_base_mesh_list = model_mesh_finder.get_all_base_mesh_list(
            self.chara_info.part_info.root_node)

        # mtl_から始まるcgfxでないマテリアルをリスト
        target_material_list = []
        for mesh in main_base_mesh_list:
            this_material_list = self.__get_fix_no_cgfx_material_list(mesh)

            if this_material_list:
                target_material_list.extend(this_material_list)

        # cgfxの適用
        for default_mat in target_material_list:

            cgfx_mat = default_mat + model_define.CGFX_SUFFIX
            setup = self.__setup_cgfx_material(cgfx_mat)

            if not setup:
                continue

            # デフォルトテクスチャの適用
            self.__set_default_texture_to_cgfx(cgfx_mat)

            # デフォルトパラメータの適用
            self.__set_default_param_val_to_cgfx(cgfx_mat)

            # ノードコネクトするパラメータの適用
            self.__set_connect_param_to_cgfx(cgfx_mat)

            # マテリアルからテクスチャの検索
            self.__set_texture_to_cgfx(cgfx_mat, default_mat, self.chara_info.part_info.maya_sourceimages_dir_path)

            # 適用
            self.link_chara_light(cgfx_mat)
            self.replace_material(default_mat, cgfx_mat)

    # ==================================================
    def apply_outline_cgfx(self):

        self.__remove_tmp_outline_cgfx_dir()
        self.load_plugins()

        # grp_mesh直下のアウトラインメッシュリスト
        main_outline_mesh_list = model_mesh_finder.get_all_outline_mesh_list(
            self.chara_info.part_info.root_node)

        for mesh in main_outline_mesh_list:

            # mtl_から始まるoutlineCgfxでないマテリアルをリスト
            this_material_list = self.__get_fix_no_cgfx_material_list(mesh, is_outline=True)

            if not this_material_list:
                continue

            # cgfxの適用
            for material in this_material_list:

                if material.find('_eye') >= 0:
                    continue

                # cgfxの可能性があるのでセパレーターでスプリット
                material_root = material.split(self.divide_flag)[0]
                cgfx_mat = material_root + model_define.CGFX_OUTLINE_SUFFIX
                setup = self.__setup_cgfx_material(cgfx_mat)

                if not setup:
                    continue

                # デフォルトテクスチャの適用
                self.__set_default_texture_to_cgfx(cgfx_mat)

                # デフォルトパラメータの適用
                self.__set_default_param_val_to_cgfx(cgfx_mat, is_outline=True)

                # マテリアルからテクスチャの検索
                self.__set_texture_to_outline_cgfx(cgfx_mat, mesh)

                # 適用
                self.replace_material(material, cgfx_mat, mesh)

    # ==================================================
    def remove_cgfx_material(self, is_outline=False):

        target_suffix = model_define.CGFX_SUFFIX

        if is_outline:
            target_suffix = model_define.CGFX_OUTLINE_SUFFIX

        if not is_outline:
            self.delete_chara_light()

        cgfx_list = cmds.ls('*{}'.format(target_suffix), type='cgfxShader')

        if not cgfx_list:
            self.__remove_tmp_cgfx_dir()

        for cgfx in cgfx_list:

            # ファイルノードの削除
            self.delete_file_node(cgfx)

            # マトリックスノードの削除
            self.delete_decompose_matrix_node(cgfx, '_FaceCenterPos')

            # シェーディングエンジンの削除
            self.delete_shading_engine(cgfx)

            cmds.delete(cgfx)

        if is_outline:
            self.__remove_tmp_outline_cgfx_dir()
        else:
            self.__remove_tmp_cgfx_dir()

    # ==================================================
    def change_default_material(self):
        """CGFXマテリアルを元のマテリアルに戻す
        """

        all_mesh_list = model_mesh_finder.get_all_base_mesh_list(
            self.chara_info.part_info.root_node)

        if not all_mesh_list:
            return

        for mesh in all_mesh_list:

            this_material_list = base_utility.material.get_material_list(mesh)

            if not this_material_list:
                continue

            for material in this_material_list:

                if material.find(model_define.CGFX_SUFFIX) < 0:
                    continue

                original_material = material.replace(model_define.CGFX_SUFFIX, '')

                if not cmds.objExists(original_material):
                    continue

                self.replace_material(material, original_material)

    # ==================================================
    def adjust_outline_material_to_base_material(self):
        """アウトラインのマテリアルをベースメッシュに合わせる
        """

        outline_list = model_mesh_finder.get_all_outline_mesh_list(
            self.chara_info.part_info.root_node)

        for this_outline in outline_list:

            this_material_list = base_utility.material.get_material_list(this_outline)

            if not this_material_list:
                continue

            base_mesh = this_outline.replace(model_define.OUTLINE_SUFFIX, '')

            base_material_list = base_utility.material.get_material_list(base_mesh)

            if not base_material_list:
                continue

            for this_material in this_material_list:

                this_material_base = this_material.replace(model_define.CGFX_OUTLINE_SUFFIX, '')

                target_material = None

                for base_material in base_material_list:
                    if base_material.find(this_material_base) >= 0:
                        target_material = base_material
                        break

                if not target_material:
                    continue

                if this_material == target_material:
                    continue

                self.replace_material(this_material, target_material)

    # ==================================================
    def __change_outline_visible_state(self, is_visible):
        """全アウトラインメッシュの表示を切り替え
        """

        outline_list = model_mesh_finder.get_all_outline_mesh_list(
            self.chara_info.part_info.root_node)

        for outline in outline_list:

            if not cmds.objExists(outline):
                continue

            cmds.setAttr(outline + '.visibility', is_visible)

    # ==================================================
    def __get_fix_no_cgfx_material_list(self, mesh, is_outline=False):

        all_material_list = base_utility.material.get_material_list(mesh)
        fix_material_list = []

        cgfx_suffix = model_define.CGFX_SUFFIX

        if is_outline:
            cgfx_suffix = model_define.CGFX_OUTLINE_SUFFIX

        if not all_material_list:
            return fix_material_list

        for material in all_material_list:
            if not material.startswith(model_define.MATERIAL_PREFIX):
                continue
            if material.endswith(cgfx_suffix):
                continue
            fix_material_list.append(material)

        return fix_material_list

    # ==================================================
    def __create_cgfx_file(self, cgfx_material):
        """複数マテリアルで共通のcgfxファイルを使おうとするとエラーになるため都度作成する
        """

        copy_target_dir_path = self.cgfx_tmp_path

        if cgfx_material.find(model_define.CGFX_OUTLINE_SUFFIX) >= 0:
            copy_target_dir_path = self.cgfx_outline_tmp_path

        if not os.path.exists(copy_target_dir_path):
            os.makedirs(copy_target_dir_path)

        # cgincもコピー
        for cginc in glob.glob(self.cgfx_dir_path + '/*.cginc'):
            shutil.copy(cginc, cginc.replace(self.cgfx_dir_path, copy_target_dir_path))

        org_cgfx_file_name = cgfx_param_setting.get_original_cgfx_file_name(cgfx_material)
        org_cgfx_file = os.path.join(self.cgfx_dir_path, org_cgfx_file_name)

        if not os.path.exists(org_cgfx_file):
            return ''
        if not org_cgfx_file:
            return ''

        org_cgfx_file_name = os.path.basename(org_cgfx_file)
        tmp_cgfx_file_name = '{}{}'.format(cgfx_material.replace('_', ''), org_cgfx_file_name)

        copy_target_path = os.path.join(copy_target_dir_path, tmp_cgfx_file_name)

        if os.path.exists(copy_target_path):
            return copy_target_path
        else:
            try:
                shutil.copy(org_cgfx_file, copy_target_path)
                return copy_target_path
            except Exception:
                print('cgfx file copy failed')
                return ''

    # ==================================================
    def __setup_cgfx_material(self, cgfx_material_name):
        """CGFXノードを作成し、cgfxファイルをセット
        """

        print('=' * 20)
        print('START: CGFXマテリアルのセットアップ：{}'.format(cgfx_material_name))

        if not cmds.objExists(cgfx_material_name):
            cmds.shadingNode("cgfxShader", name=cgfx_material_name, asShader=True)

        this_cgfx_file = self.__create_cgfx_file(cgfx_material_name)

        if this_cgfx_file:
            this_cgfx_file = this_cgfx_file.replace('\\', '/')
            mel_script = u"cgfxShader -e -fx \"{0}\" {1};".format(this_cgfx_file, cgfx_material_name)
            mel.eval(mel_script)

            # cgfxで頂点カラーが自動で刺さらないので、setAttrする
            self.apply_vertex_color_attr_to_cgfx(cgfx_material_name)
            return True
        else:
            return False

    # ==================================================
    def __set_default_texture_to_cgfx(self, cgfx_material):

        print('=' * 20)
        print('START: 規定テクスチャの設定：{}'.format(cgfx_material))

        default_attr_tex_dict = cgfx_param_setting.get_default_texture_dict(self.texture_dir_path)

        for attr, tex_path in list(default_attr_tex_dict.items()):
            self.apply_file_to_material_attr(cgfx_material, attr, tex_path)

    # ==================================================
    def __set_default_param_val_to_cgfx(self, cgfx_material, is_outline=False):

        print('=' * 20)
        print('START: 静的パラメーターの設定：{}'.format(cgfx_material))

        default_attr_val_dict = {}

        if is_outline:
            default_attr_val_dict = cgfx_param_setting.get_outline_default_value_dict()
        else:
            default_attr_val_dict = cgfx_param_setting.get_default_value_dict(cgfx_material)

        for attr, val in list(default_attr_val_dict.items()):

            if not cgfx_material or not cmds.objExists(cgfx_material):
                continue

            if not attr:
                continue

            try:
                cmds.getAttr(cgfx_material + '.' + attr, type=True)
            except:
                continue

            attr_type = cmds.getAttr(cgfx_material + '.' + attr, typ=True)

            if attr_type == 'string':

                is_settable = \
                    cmds.getAttr(cgfx_material + '.' + attr, settable=True)

                if not is_settable:
                    continue

                cmds.setAttr(cgfx_material + '.' + attr,
                            val,
                            type='string')

            elif re.search('.*\d$', attr_type):

                is_settable = \
                    cmds.getAttr(cgfx_material + '.' + attr, settable=True)

                if is_settable:

                    if attr_type.find('2') > 0:
                        cmds.setAttr(cgfx_material + '.' +
                                    attr, val[0], val[1])
                        continue

                    if attr_type.find('3') > 0:
                        cmds.setAttr(cgfx_material + '.' + attr,
                                    val[0], val[1], val[2])
                        continue

                attr_list = search_list(
                    cgfx_material, attr + '.{1}$')

                if not attr_list:
                    continue

                value_list = None
                if type(val) == list:
                    value_list = val
                else:
                    value_list = [val]

                count = -1
                for attr in attr_list:
                    count += 1

                    this_value = value_list[-1]

                    if count < len(value_list):
                        this_value = value_list[count]

                    is_settable = \
                        cmds.getAttr(cgfx_material + '.' + attr, settable=True)

                    if not is_settable:
                        continue

                    cmds.setAttr(cgfx_material + '.' + attr, this_value)

            else:

                is_settable = \
                    cmds.getAttr(cgfx_material + '.' + attr, settable=True)

                if not is_settable:
                    continue

                cmds.setAttr(cgfx_material + '.' + attr, val)

    # ==================================================
    def __set_connect_param_to_cgfx(self, cgfx_material):

        print('=' * 20)
        print('START: 接続系パラメーターの設定：{}'.format(cgfx_material))

        # spec系
        spec_locator = cgfx_param_setting.get_spec_color_locator(cgfx_material)

        if spec_locator:

            # 初期値を取得
            spec_color_dict = cgfx_param_setting.get_current_spec_color_dict(spec_locator)
            for attr, val in list(spec_color_dict.items()):

                if not cgfx_material or not cmds.objExists(cgfx_material):
                    continue

                if not attr:
                    continue

                try:
                    cmds.getAttr(cgfx_material + '.' + attr, type=True)
                except:
                    continue

                attr_type = cmds.getAttr(cgfx_material + '.' + attr, typ=True)

                if attr_type == 'string':

                    is_settable = \
                        cmds.getAttr(cgfx_material + '.' + attr, settable=True)

                    if not is_settable:
                        continue

                    cmds.setAttr(cgfx_material + '.' + attr,
                                val,
                                type='string')

                elif re.search('.*\d$', attr_type):

                    is_settable = \
                        cmds.getAttr(cgfx_material + '.' + attr, settable=True)

                    if is_settable:

                        if attr_type.find('2') > 0:
                            cmds.setAttr(cgfx_material + '.' +
                                        attr, val[0], val[1])
                            continue

                        if attr_type.find('3') > 0:
                            cmds.setAttr(cgfx_material + '.' + attr,
                                        val[0], val[1], val[2])
                            continue

                    attr_list = search_list(
                        cgfx_material, attr + '.{1}$')

                    if not attr_list:
                        continue

                    value_list = None
                    if type(val) == list:
                        value_list = val
                    else:
                        value_list = [val]

                    count = -1
                    for attr in attr_list:
                        count += 1

                        this_value = value_list[-1]

                        if count < len(value_list):
                            this_value = value_list[count]

                        is_settable = \
                            cmds.getAttr(cgfx_material + '.' + attr, settable=True)

                        if not is_settable:
                            continue

                        cmds.setAttr(cgfx_material + '.' + attr, this_value)

                else:

                    is_settable = \
                        cmds.getAttr(cgfx_material + '.' + attr, settable=True)

                    if not is_settable:
                        continue

                    cmds.setAttr(cgfx_material + '.' + attr, val)

            # コネクト
            spec_connect_dict = cgfx_param_setting.get_spec_color_connect_dict(cgfx_material, spec_locator)
            for attr, val in list(spec_connect_dict.items()):
                if not cmds.isConnected(attr, val):
                    cmds.connectAttr(attr, val, f=True)

        # head_center系
        head_center_locator = cgfx_param_setting.get_head_center_locator(cgfx_material)

        if head_center_locator:
            matrix_decomposer = head_center_locator.split('|')[-1] + '_world_matrix_decomposer'

            if not cmds.objExists(matrix_decomposer):
                cmds.shadingNode('decomposeMatrix', au=True, n=matrix_decomposer)

            cmds.connectAttr(head_center_locator + '.worldMatrix[0]', matrix_decomposer + '.inputMatrix', f=True)
            cmds.connectAttr(matrix_decomposer + '.outputTranslate', cgfx_material + '._FaceCenterPos', f=True)

    # ==================================================
    def __set_texture_to_cgfx(self, cgfx_material, default_material, texture_root_path):

        print('=' * 20)
        print('START: テクスチャの割り当て：{}'.format(cgfx_material))

        attr_tex_dict = cgfx_param_setting.get_texture_dict(default_material, texture_root_path)

        for attr, tex_path in list(attr_tex_dict.items()):
            self.apply_file_to_material_attr(cgfx_material, attr, tex_path)
            print('APPLY_TEX tex:{} ===> {}: {}'.format(tex_path, cgfx_material, attr))

    # ==================================================
    def __set_texture_to_outline_cgfx(self, outline_cgfx_material, outline_mesh):

        print('=' * 20)
        print('START: テクスチャの割り当て：{}'.format(outline_cgfx_material))

        # アウトラインのメッシュとマテリアル名から元メッシュのマテリアルを特定
        true_base_material = ''
        expected_base_mesh = outline_mesh.replace(model_define.OUTLINE_SUFFIX, '')
        expected_base_material = outline_cgfx_material.replace(model_define.CGFX_OUTLINE_SUFFIX, '')

        base_material_list = base_utility.material.get_material_list(expected_base_mesh)

        if not base_material_list:
            return

        for base_material in base_material_list:
            if base_material.find(expected_base_material) >= 0:
                true_base_material = base_material
                break

        if not true_base_material:
            return

        # アトリビュートと、ターゲットパスのdict
        attr_path_list_dict = {
            '_MainTex': '',
        }

        if true_base_material.find(model_define.CGFX_SUFFIX) >= 0:
            attr_path_list_dict['_MainTex'] = self.get_file_from_material_attr(true_base_material, '_MainTex')
        else:
            attr_path_list_dict['_MainTex'] = self.get_file_from_material_attr(true_base_material, 'color')

        for attr, tex_path in list(attr_path_list_dict.items()):
            self.apply_file_to_material_attr(outline_cgfx_material, attr, tex_path)
            print('APPLY_TEX tex:{} ===> {}: {}'.format(tex_path, outline_cgfx_material, attr))

    # ==================================================
    def __remove_tmp_cgfx_dir(self):

        if os.path.exists(self.cgfx_tmp_path):
            shutil.rmtree(self.cgfx_tmp_path)

    # ==================================================
    def __remove_tmp_outline_cgfx_dir(self):

        if os.path.exists(self.cgfx_outline_tmp_path):
            shutil.rmtree(self.cgfx_outline_tmp_path)

    # ==================================================
    def get_texture_info_from_material_link(self, material_link, key):

        texture_index = material_link.get(key)

        if texture_index is None:

            return None

        texture_name = ''
        texture_path = ''

        for texture_param in self.chara_info.part_info.texture_param_list:

            if texture_param['id'] == texture_index:

                texture_name = texture_param['name']
                texture_path = '{0}/{1}'.format(
                    self.chara_info.part_info.maya_sourceimages_dir_path,
                    texture_name
                )
                break

        if texture_name and texture_path:
            return texture_index, texture_name, texture_path

        else:

            return None

        return texture_index, texture_name, texture_path

    # ==================================================
    def load_plugins(self):

        if not cmds.pluginInfo("cgfxShader", query=True, loaded=True):
            cmds.loadPlugin("cgfxShader.mll")

        if not cmds.pluginInfo("matrixNodes", query=True, loaded=True):
            cmds.loadPlugin("matrixNodes.mll")

    # ==================================================
    def create_chara_light(self):

        if not self.chara_light0 or not cmds.objExists(self.chara_light0):

            cmds.pointLight(name=self.chara_light0)

        light0_translate = cmds.getAttr(self.chara_light0 + '.' + 'translate')

        if type(light0_translate) == list:
            light0_translate = list(light0_translate[0])

        if light0_translate == [0, 0, 0]:

            if not self.chara_light0 or not cmds.objExists(self.chara_light0):
                return

            try:
                cmds.getAttr(self.chara_light0 + '.' + 'translate', type=True)
            except:
                return

            attr_type = cmds.getAttr(self.chara_light0 + '.' + 'translate', typ=True)

            if attr_type == 'string':

                is_settable = \
                    cmds.getAttr(self.chara_light0 + '.' + 'translate', settable=True)

                if not is_settable:
                    return

                cmds.setAttr(self.chara_light0 + '.' + 'translate',
                            [30, 30, 30],
                            type='string')

            elif re.search('.*\d$', attr_type):

                is_settable = \
                    cmds.getAttr(self.chara_light0 + '.' + 'translate', settable=True)

                if is_settable:

                    if attr_type.find('2') > 0:
                        cmds.setAttr(self.chara_light0 + '.' +
                                    'translate', [30, 30, 30][0], [30, 30, 30][1])
                        return

                    if attr_type.find('3') > 0:
                        cmds.setAttr(self.chara_light0 + '.' + 'translate',
                                    [30, 30, 30][0], [30, 30, 30][1], [30, 30, 30][2])
                        return

                attr_list = search_list(
                    self.chara_light0, 'translate' + '.{1}$')

                if not attr_list:
                    return

                value_list = None
                if type([30, 30, 30]) == list:
                    value_list = [30, 30, 30]
                else:
                    value_list = [[30, 30, 30]]

                count = -1
                for attr in attr_list:
                    count += 1

                    this_value = value_list[-1]

                    if count < len(value_list):
                        this_value = value_list[count]

                    is_settable = \
                        cmds.getAttr(self.chara_light0 + '.' + attr, settable=True)

                    if not is_settable:
                        continue

                    cmds.setAttr(self.chara_light0 + '.' + attr, this_value)

            else:

                is_settable = \
                    cmds.getAttr(self.chara_light0 + '.' + 'translate', settable=True)

                if not is_settable:
                    return

                cmds.setAttr(self.chara_light0 + '.' + 'translate', [30, 30, 30])

            if not self.chara_light0_cgfx_vector or not cmds.objExists(self.chara_light0_cgfx_vector):
                cmds.shadingNode(
                    'cgfxVector',
                    name=self.chara_light0_cgfx_vector, asShader=True)

    # ==================================================
    def delete_chara_light(self):

        if self.chara_light0 and cmds.objExists(self.chara_light0):

            cmds.delete(self.chara_light0)

        if self.chara_light0_cgfx_vector and cmds.objExists(self.chara_light0_cgfx_vector):

            cmds.delete(self.chara_light0_cgfx_vector)

    # ==================================================
    def link_chara_light(self, target_cgfx_material):

        if not self.chara_light0_cgfx_vector or not cmds.objExists(self.chara_light0_cgfx_vector):
            return

        this_exists = True
        try:
            cmds.getAttr(self.chara_light0_cgfx_vector + '.' + 'worldVector', type=True)
        except:
            this_exists = False

        if not this_exists:
            return

        if not target_cgfx_material or not cmds.objExists(target_cgfx_material):
            return

        this_exists = True
        try:
            cmds.getAttr(target_cgfx_material + '.' + 'surfaceShader', type=True)
        except:
            this_exists = False

        if not this_exists:
            return

        if cmds.isConnected(self.chara_light0_cgfx_vector + '.' + 'worldVector',
                            target_cgfx_material + '.' + 'surfaceShader'):
            return

        try:
            cmds.connectAttr(material_name + '.' + 'worldVector',
                            target_cgfx_material + '.' + 'surfaceShader',
                            force=True)
        except Exception as e:
            print('{0}'.format(e))
        

        if not self.chara_light0_cgfx_vector or not cmds.objExists(self.chara_light0_cgfx_vector):
            return

        this_exists = True
        try:
            cmds.getAttr(self.chara_light0_cgfx_vector + '.' + 'worldVectorW', type=True)
        except:
            this_exists = False

        if not this_exists:
            return

        if not target_cgfx_material or not cmds.objExists(target_cgfx_material):
            return

        this_exists = True
        try:
            cmds.getAttr(target_cgfx_material + '.' + 'surfaceShader', type=True)
        except:
            this_exists = False

        if not this_exists:
            return

        if cmds.isConnected(self.chara_light0_cgfx_vector + '.' + 'worldVectorW',
                            target_cgfx_material + '.' + 'surfaceShader'):
            return

        try:
            cmds.connectAttr(material_name + '.' + 'worldVectorW',
                            target_cgfx_material + '.' + 'surfaceShader',
                            force=True)
        except Exception as e:
            print('{0}'.format(e))
        

        if not self.chara_light0 or not cmds.objExists(self.chara_light0):
            return

        this_exists = True
        try:
            cmds.getAttr(self.chara_light0 + '.' + 'worldMatrix[0]', type=True)
        except:
            this_exists = False

        if not this_exists:
            return

        if not chara_light0_cgfx_vector or not cmds.objExists(chara_light0_cgfx_vector):
            return

        this_exists = True
        try:
            cmds.getAttr(chara_light0_cgfx_vector + '.' + 'surfaceShader', type=True)
        except:
            this_exists = False

        if not this_exists:
            return

        if cmds.isConnected(self.chara_light0 + '.' + 'worldMatrix[0]',
                            chara_light0_cgfx_vector + '.' + 'surfaceShader'):
            return

        try:
            cmds.connectAttr(material_name + '.' + 'worldMatrix[0]',
                            chara_light0_cgfx_vector + '.' + 'surfaceShader',
                            force=True)
        except Exception as e:
            print('{0}'.format(e))
        

    # ==================================================
    def apply_vertex_color_attr_to_cgfx(self, target_cgfx_material):

        mesh_type = None

        if target_cgfx_material.find('face') > -1:
            mesh_type = model_define.MESH_PREFIX + 'face'

        elif target_cgfx_material.find('hair') > -1:
            mesh_type = model_define.MESH_PREFIX + 'hair'

        elif target_cgfx_material.find('body') > -1:
            mesh_type = model_define.MESH_PREFIX + 'body'

        if not mesh_type:
            return

        if not self.chara_info.part_info.mesh_list:
            return

        # 対象メッシュのカラーセット0があれば、それを適用する
        target_mesh = None

        target_mesh_list = self.chara_info.part_info.mesh_list

        if target_cgfx_material.find(model_define.CGFX_OUTLINE_SUFFIX) > -1:
            target_mesh_list = model_mesh_finder.get_all_outline_mesh_list(
                self.chara_info.part_info.root_node)

        for mesh in target_mesh_list:

            if mesh.find(mesh_type) > -1:
                target_mesh = mesh
                break

        if not target_mesh:
            return

        target_color_set_list = base_utility.mesh.colorset.get_colorset_list(target_mesh)

        if not target_color_set_list:
            return

        target_color_set = target_color_set_list[0]

        cmds.setAttr(
            target_cgfx_material + '.vertexAttributeSource',
            4,
            "position",
            "uv:map1",
            "normal",
            "color:" + target_color_set,
            type='stringArray')

    # ==================================================
    def get_file_from_material_attr(self, target_material, attr_name):

        if not cmds.objExists(target_material):
            return

        if not target_material or not cmds.objExists(target_material):
            return

        if not attr_name:
            return

        try:
            cmds.getAttr(target_material + '.' + attr_name, type=True)
        except:
            return

        this_file_node_list = cmds.listConnections(
            "{0}.{1}".format(target_material, attr_name), type="file")

        if not this_file_node_list:
            return

        this_file_node = this_file_node_list[0]

        result_value = None

        if not this_file_node or not cmds.objExists(this_file_node):
            return result_value

        try:
            cmds.getAttr(this_file_node + '.' + 'fileTextureName', type=True)
        except:
            return result_value

        result_value = cmds.getAttr(this_file_node + '.' + 'fileTextureName')

        if type(result_value) == list:
            result_value = list(result_value[0])

        return result_value



    # ==================================================
    def apply_file_to_material_attr(
            self,
            target_material,
            attr_name,
            texture_file_path,
            default_texture_file_path=None):

        if not cmds.objExists(target_material):
            return

        if not attr_name:
            return

        try:
            cmds.getAttr(target_material + '.' + attr_name, type=True)
        except:
            return

        target_texture_file_path = default_texture_file_path

        if os.path.isfile(texture_file_path):
            target_texture_file_path = texture_file_path

        if target_texture_file_path is None:
            return

        if not os.path.isfile(target_texture_file_path):
            return

        this_file_node_list = cmds.listConnections(
            "{0}.{1}".format(target_material, attr_name), type="file")

        if not this_file_node_list:
            return

        this_file_node = this_file_node_list[0]

        if not this_file_node or not cmds.objExists(this_file_node):
            return

        try:
            cmds.getAttr(this_file_node + '.' + "fileTextureName", type=True)
        except:
            return

        attr_type = cmds.getAttr(this_file_node + '.' + "fileTextureName", typ=True)

        if attr_type == 'string':

            is_settable = \
                cmds.getAttr(this_file_node + '.' + "fileTextureName", settable=True)

            if not is_settable:
                return

            cmds.setAttr(this_file_node + '.' + "fileTextureName",
                        target_texture_file_path,
                        type='string')

        elif re.search('.*\d$', attr_type):

            is_settable = \
                cmds.getAttr(this_file_node + '.' + "fileTextureName", settable=True)

            if is_settable:

                if attr_type.find('2') > 0:
                    cmds.setAttr(this_file_node + '.' +
                                "fileTextureName", target_texture_file_path[0], target_texture_file_path[1])
                    return

                if attr_type.find('3') > 0:
                    cmds.setAttr(this_file_node + '.' + "fileTextureName",
                                target_texture_file_path[0], target_texture_file_path[1], target_texture_file_path[2])
                    return

            attr_list = search_list(
                this_file_node, "fileTextureName" + '.{1}$')

            if not attr_list:
                return

            value_list = None
            if type(target_texture_file_path) == list:
                value_list = target_texture_file_path
            else:
                value_list = [target_texture_file_path]

            count = -1
            for attr in attr_list:
                count += 1

                this_value = value_list[-1]

                if count < len(value_list):
                    this_value = value_list[count]

                is_settable = \
                    cmds.getAttr(this_file_node + '.' + attr, settable=True)

                if not is_settable:
                    continue

                cmds.setAttr(this_file_node + '.' + attr, this_value)

        else:

            is_settable = \
                cmds.getAttr(this_file_node + '.' + "fileTextureName", settable=True)

            if not is_settable:
                return

            cmds.setAttr(this_file_node + '.' + "fileTextureName", target_texture_file_path)


    # ==================================================
    def replace_material(self, src_material, dst_material, target_filter=''):

        if not cmds.objExists(src_material):
            return

        if not cmds.objExists(dst_material):
            return

        print('=' * 20)
        print('START: マテリアルの入れ替え：{} => {}'.format(src_material, dst_material))

        cmds.hyperShade(objects=src_material)

        target_list = cmds.ls(sl=True, fl=True, l=True)

        if not target_list:
            return

        fix_target_list = []

        if not target_filter:
            fix_target_list = target_list
        else:
            for target in target_list:
                if target.find(target_filter) >= 0:
                    fix_target_list.append(target)

        if not fix_target_list:
            return

        cmds.select(fix_target_list, r=True)
        cmds.hyperShade(assign=dst_material)

        cmds.select(cl=True)

        print('FINISH')
        print('=' * 20)

    # ==================================================
    def delete_file_node(self, target_material):

        if not cmds.objExists(target_material):
            return

        delete_node_list = []
        this_file_node_list = cmds.listConnections(target_material, type="file")

        if not this_file_node_list:
            return

        delete_node_list.extend(this_file_node_list)

        for file_node in this_file_node_list:

            this_p2d_node_list = cmds.listConnections("{0}.{1}".format(file_node, "uvCoord"), type="place2dTexture")

            if this_p2d_node_list:
                delete_node_list.extend(this_p2d_node_list)

        if delete_node_list:
            cmds.delete(delete_node_list)

    # ==================================================
    def delete_decompose_matrix_node(self, target_material, attr_name):

        if not cmds.objExists(target_material):
            return

        if not cmds.objExists(target_material):
            return

        if not target_material or not cmds.objExists(target_material):
            return

        if not attr_name:
            return

        try:
            cmds.getAttr(target_material + '.' + attr_name, type=True)
        except:
            return

        this_decompose_matrix_node_list = cmds.listConnections(
            "{0}.{1}".format(target_material, attr_name), type="decomposeMatrix")

        if not this_decompose_matrix_node_list:
            return

        this_decompose_matrix_node = this_decompose_matrix_node_list[0]

        cmds.delete(this_decompose_matrix_node)

    # ==================================================
    def delete_shading_engine(self, target_material):

        if not cmds.objExists(target_material):
            return

        this_shading_engine_list = cmds.listConnections(
            "{0}.{1}".format(target_material, "outColor"),
            type="shadingEngine"
        )

        if not this_shading_engine_list:
            return

        this_shading_engine = this_shading_engine_list[0]

        cmds.delete(this_shading_engine)
