# -*- coding: utf-8 -*-
"""
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import re
import os

import maya.cmds as cmds

from ....base_common import utility as base_utility

from ....glp_common.classes.info import chara_info

from ....glp_common.classes import body_shape as body_shape_classes


class ReferencePart(object):

    def __init__(self):
        """
        """

        self.name_space_prefix = '__refpart__'
        self.mdl_path = 'W:\\gallop\\svn\\svn_gallop\\80_3D\\01_character\\01_model'
        self.mdl_body_path = '{}\\body'.format(self.mdl_path)
        self.mdl_head_path = '{}\\head'.format(self.mdl_path)
        self.mdl_tail_path = '{}\\tail'.format(self.mdl_path)
        self.mdl_mini_path = '{}\\mini'.format(self.mdl_path)
        self.mdl_child_dir_path_list = [self.mdl_body_path, self.mdl_head_path, self.mdl_tail_path, self.mdl_mini_path]

        self.mini_mdl_default_face_path = '\\mini\\head\\mchr0001_00\\scenes\\mdl_mchr0001_00_face0.ma'
        self.mini_mdl_default_audience_face_path = '\\mini\\head\\mchr0900_00\\scenes\\mdl_mchr0900_00_face0.ma'

        self.mdl_default_tail_path = self.mdl_path + '\\tail\\tail0001_00\\scenes\\mdl_tail0001_00.ma'
        self.mini_mdl_default_tail_path = self.mdl_path + '\\mini\\tail\\mtail0001_00\\scenes\\mdl_mtail0001_00.ma'

        self.path_regex = r'\\(body|head|tail)\\(bdy|chr|tail)([0-9])([0-9]{3}_[0-9]{2})\\scenes\\mdl_(bdy|chr|tail)([0-1])([0-9]{3}_[0-9]{2})(_[0-9]{2}|)(_Bust[LM]|).ma'
        self.mini_path_regex = r'\\(mini\\body|mini\\head|mini\\tail)\\(mbdy|mchr|mtail)([0-9])([0-9]{3}_[0-9]{2})\\scenes\\mdl_(mbdy|mchr|mtail)([0-1])([0-9]{3}_[0-9]{2})(_[0-9]{2}|)(_Bust[LM]|_hair|).ma'

        self.full_path_regex = re.compile(re.escape(self.mdl_path) + self.path_regex)
        self.mini_full_path_regex = re.compile(re.escape(self.mdl_path) + self.mini_path_regex)
        self.chara_info = chara_info.CharaInfo()

        self.general_dress_path_list = []
        self.special_dress_path_list = []
        self.head_path_list = []
        self.tail_path_list = []

    def _get_ref_path(self, is_general, head_short_name, body_short_name):
        """
        """

        ref_file_path = ''

        if self.chara_info.part_info.data_type.endswith('body'):

            # 特別衣装に汎用はつかない
            if self.chara_info.part_info.is_unique_chara and is_general:
                return ref_file_path

            if is_general:
                for head_path in self.head_path_list:
                    if head_path.find(head_short_name) > -1:
                        ref_file_path = head_path
            else:
                ref_file_path = re.sub(r'body', 'head', self.chara_info.file_path)
                ref_file_path = re.sub(r'bdy', 'chr', ref_file_path)

                if self.chara_info.is_mini:
                    if not ref_file_path.endswith('_hair.ma'):
                        ref_file_path = ref_file_path.replace('.ma', '_hair.ma')

                # 対応する頭のパスが存在しないときは、sub_idが00の頭を読み込む
                if not os.path.exists(ref_file_path):
                    is_match = re.search(r'chr([0-9]{4})_[0-9]{2}', ref_file_path)
                    if is_match:
                        main_id = is_match.group(1)
                        ref_file_path = re.sub(
                            r'chr[0-9]{4}_[0-9]{2}',
                            'chr{0}_00'.format(main_id),
                            ref_file_path
                        )

        elif self.chara_info.part_info.data_type.endswith('head'):

            if is_general:
                for dress_path in self.general_dress_path_list:
                    if dress_path.find(body_short_name) > -1:
                        ref_file_path = dress_path
            else:
                ref_file_path = re.sub(r'head', 'body', self.chara_info.file_path)
                ref_file_path = re.sub(r'chr', 'bdy', ref_file_path)

                # 身体は必ず対応するパスがあるので頭で行っている特殊処理を行わない
            if self.chara_info.is_mini:
                ref_file_path = ref_file_path.replace('_hair.ma', '.ma')
                ref_file_path = ref_file_path.replace('_face0.ma', '.ma')

        return ref_file_path

    def _get_tail_ref_path(self, is_general, head_short_name):
        """
        """

        tmp_tail_ref_file_path = ''
        tmp_tail_ref_texture_path = ''

        if not is_general and self.chara_info.tail_part_info and self.chara_info.tail_part_info.exists:

            file_list = self.chara_info.tail_part_info.maya_file_list
            taxture_list = self.chara_info.tail_part_info.texture_list

            for _file in file_list:
                if _file.find('tail') < 0:
                    continue

                tmp_path = '{0}\\{1}'.format(
                    self.chara_info.tail_part_info.maya_scenes_dir_path,
                    _file
                )

                if not os.path.exists(tmp_path):
                    continue

                tmp_tail_ref_file_path = tmp_path
                break

            for _texture in taxture_list:

                if _texture.find('_diff') < 0:
                    continue

                tmp_path = '{0}\\{1}'.format(
                    self.chara_info.tail_part_info.maya_sourceimages_dir_path,
                    _texture
                )

                if not os.path.exists(tmp_path):
                    continue

                tmp_tail_ref_texture_path = tmp_path
                break

        if not tmp_tail_ref_file_path or not tmp_tail_ref_texture_path:

            tmp_tail_ref_file_path = self.mdl_default_tail_path
            if self.chara_info.is_mini:
                tmp_tail_ref_file_path = self.mini_mdl_default_tail_path

            tmp_head_short_name = head_short_name
            head_id = '1001'

            if self.chara_info.part_info.data_type.endswith('head'):
                tmp_head_short_name = self.chara_info.part_info.data_id

            is_match = re.search(r'chr([0-9]{4})_00', tmp_head_short_name)
            if is_match:
                head_id = is_match.group(1)

            tail_ref_scene_dir = os.path.dirname(tmp_tail_ref_file_path)
            tail_ref_root_dir = os.path.dirname(tail_ref_scene_dir)
            tail_ref_sourceresouces_dir = '{0}\\sourceimages'.format(tail_ref_root_dir)
            tail_general_texture_path = '{0}\\tex_tail0001_00_{1}_diff.tga'.format(tail_ref_sourceresouces_dir, head_id)
            if self.chara_info.is_mini:
                tail_general_texture_path = '{0}\\tex_mtail0001_00_{1}_diff.tga'.format(tail_ref_sourceresouces_dir, head_id)
            if os.path.exists(tail_general_texture_path):
                tmp_tail_ref_texture_path = tail_general_texture_path

        return tmp_tail_ref_file_path, tmp_tail_ref_texture_path

    def __load_tail_ref(self, target_tail_ref_path, name_space):

        if base_utility.reference.exists(target_tail_ref_path, name_space):
            return

        base_utility.reference.load(target_tail_ref_path, name_space)

    def __adjust_tail_ref_pos(self, body_top_node, name_space):

        hip_node = self.__get_node_target_word(body_top_node, 'Hip')

        if not hip_node:
            return

        tail_hip_node_name = '{0}:{1}'.format(name_space, 'Hip')
        if not cmds.objExists(tail_hip_node_name):
            return

        tail_constraint = cmds.parentConstraint(hip_node, tail_hip_node_name)
        cmds.delete(tail_constraint)

    def __load_tail_ref_texture(self, tail_ref_texture_path, name_space):

        if tail_ref_texture_path and os.path.exists(tail_ref_texture_path):
            m_tail_node = name_space + ':M_Tail'

            if not cmds.objExists(m_tail_node):
                return

            self.__set_texture(m_tail_node, tail_ref_texture_path)

    def __load_mini_head_ref_base(self, face_ref_path, name_space, chara_id='1001', chara_sub_id='00', is_face_load=True):

        # 肌色を取得するためにidから一時的なinfoを作成
        tmp_info = chara_info.CharaInfo()
        tmp_id = 'mdl_chr{}_{}'.format(chara_id, chara_sub_id)
        tmp_info.create_info(tmp_id)

        # 髪や肌色のテクスチャを参照するために顔のキャラインフォを作成
        _option = {}
        _option.update({'hair_id': chara_id, 'hair_sub_id': chara_sub_id})

        if tmp_info.data_info:
            _option.update({
                'extra_value_dict_list': [
                    {'name': 'SKINCOLOR', 'value': tmp_info.data_info.skin_id}
                ]
            })

        ref_face_chara_info = chara_info.CharaInfo()
        ref_face_chara_info.create_info(face_ref_path, option=_option)

        scene_path = ref_face_chara_info.alternative_info.maya_scenes_dir_path
        file_name = 'mdl_mchr{}_{}_hair.ma'.format(chara_id, chara_sub_id)
        hair_ref_path = '{}/{}'.format(scene_path, file_name)

        load_ref_path = ''

        if is_face_load:
            load_ref_path = face_ref_path
        else:
            load_ref_path = hair_ref_path

        self.__load_mini_alter_ref(load_ref_path, name_space)
        self.__load_mini_head_ref_texture(ref_face_chara_info, face_ref_path, hair_ref_path)

        return load_ref_path

    def __load_mini_alter_ref(self, mini_alter_ref_path, name_space):

        if base_utility.reference.exists(mini_alter_ref_path, name_space):
            return
        elif base_utility.reference.exist_reference_file_path(mini_alter_ref_path):
            # 顔ファイルを二重でロードしないようにする
            return
        else:
            base_utility.reference.load(mini_alter_ref_path, name_space)

    def __load_mini_head_ref_texture(self, ref_face_chara_info, face_ref_path, hair_ref_path):

        if not ref_face_chara_info.alternative_info or not ref_face_chara_info.alternative_info.exists:
            return

        face_mesh_list = []

        if self.chara_info.part_info.data_type.endswith('face_head'):
            face_mesh_list = cmds.ls(self.chara_info.part_info.mesh_list, typ='transform', l=True)
        elif base_utility.reference.exist_reference_file_path(face_ref_path):
            face_ref_list = cmds.referenceQuery(face_ref_path, n=True, dp=True)
            face_mesh_list = cmds.ls(face_ref_list, typ='transform', l=True)

        hair_mesh_list = []

        if self.chara_info.part_info.data_type.endswith('hair_head'):
            hair_mesh_list = cmds.ls(self.chara_info.part_info.mesh_list, typ='transform', l=True)
        elif base_utility.reference.exist_reference_file_path(hair_ref_path):
            hair_ref_list = cmds.referenceQuery(hair_ref_path, n=True, dp=True)
            hair_ref_mesh_list = cmds.ls(hair_ref_list, typ='transform', l=True)

        ref_mesh_list = face_mesh_list + hair_mesh_list

        for mesh in ref_mesh_list:

            no_ns_name = mesh.split(':')[-1]

            # matrialリストのindexを検索
            this_material_index = None
            for mesh_param in ref_face_chara_info.part_info.mesh_param_list:
                if mesh_param['name'].endswith(no_ns_name):
                    this_material_index = int(mesh_param['material_list'][0])
                    break

            if this_material_index is None:
                continue

            # hair側のtextureリストのindexを検索
            if not ref_face_chara_info.part_info.material_param_list:
                continue

            material_param = ref_face_chara_info.part_info.material_param_list[this_material_index]
            alternate_id = material_param['diff']

            # テクスチャ名を検索
            this_texture = ''
            souce_image_dir = ''

            # 髪側のテクスチャを髪のinfoから検索
            for tex_param in ref_face_chara_info.alternative_info.texture_param_list:
                if tex_param['alternate_id'] == alternate_id:
                    this_texture = tex_param['name']
                    souce_image_dir = ref_face_chara_info.alternative_info.maya_sourceimages_dir_path
                    break

            # 肌色を修正するために顔のinfoから検索
            for tex_param in ref_face_chara_info.part_info.texture_param_list:
                if tex_param['id'] == alternate_id:
                    this_texture = tex_param['name']
                    souce_image_dir = ref_face_chara_info.part_info.maya_sourceimages_dir_path
                    break

            if not this_texture:
                continue

            texture_path = '{}/{}'.format(souce_image_dir, this_texture)

            self.__set_texture(mesh, texture_path)

    def __adjust_mini_head_ref_pos(self, target_neck_node, ref_path):

        ref_list = cmds.referenceQuery(ref_path, n=True, dp=True)
        ref_joint_list = cmds.ls(ref_list, typ='joint', l=True)

        if not ref_joint_list:
            return

        neck_joint = None
        for joint in ref_joint_list:
            if joint.endswith('Neck'):
                neck_joint = joint
                break

        if not neck_joint:
            return

        dst_neck_node_pos = cmds.xform(target_neck_node, q=True, ws=True, t=True)
        ref_neck_node_pos = cmds.xform(neck_joint, q=True, ws=True, t=True)

        trans_value = [
            (dst_neck_node_pos[0] - ref_neck_node_pos[0]),
            (dst_neck_node_pos[1] - ref_neck_node_pos[1]),
            (dst_neck_node_pos[2] - ref_neck_node_pos[2])
        ]

        cmds.xform(neck_joint, ws=True, t=trans_value)

    def __get_normal_file_path(self):
        """デカ体型のファイルパスを取得する

        Returns:
            str: デカ体型のファイルパス
        """

        normal_file_path = ''

        data_id = '{}_{}'.format(self.chara_info.data_main_id, self.chara_info.data_sub_id)

        if self.chara_info.data_type.endswith('body'):
            normal_file_path = os.path.join(self.mdl_path, r'body\bdy{0}\scenes\mdl_bdy{0}.ma'.format(data_id))
        elif self.chara_info.data_type.endswith('head'):
            normal_file_path = os.path.join(self.mdl_path, r'head\chr{0}\scenes\mdl_chr{0}.ma'.format(data_id))

        return normal_file_path

    def __get_ref_namespace_and_node_name(self, ref_file_path):
        """リファレンス対象のネームスペースとトップノード名を取得する

        Returns:
            str, str: ネームスペース、トップノード名
        """

        match_obj = re.search(r'mdl_(mbdy|bdy|mchr|chr)([0-9]{4}_[0-9]{2})(_[0-9]{2}|)(_Bust[LM]|)', ref_file_path)
        if not match_obj:
            return None, None

        name_space = self.name_space_prefix + 'mdl_{0}{1}{2}'.format(match_obj.group(1), match_obj.group(2), match_obj.group(3))

        ref_file_name_without_ext = ''

        if self.chara_info.is_mini:
            ref_file_name_without_ext = os.path.splitext(os.path.basename(ref_file_path))[0]
        else:
            # BustLMは含まない
            ref_file_name_without_ext = 'mdl_{0}{1}{2}'.format(match_obj.group(1), match_obj.group(2), match_obj.group(3))

        top_node_name = '{0}:{1}'.format(name_space, ref_file_name_without_ext)

        return name_space, top_node_name

    def view_parts_ref(self, is_visible, is_general, is_mini_to_normal, head_short_name, body_short_name, body_shape_id):
        """
        """

        ref_file_path = ''

        self.chara_info.create_info()
        if not self.chara_info.exists:
            return

        if is_mini_to_normal:
            if not self.chara_info.is_mini:
                return
            
            normal_file_path = self.__get_normal_file_path()

            if not os.path.exists(normal_file_path):
                return

            self.chara_info.create_info(normal_file_path)
            if not self.chara_info.exists:
                return

        # tailのために作り直し
        self.chara_info.tail_char_id = self.chara_info.part_info.main_id

        if is_mini_to_normal:
            self.chara_info.create_info(normal_file_path, is_create_all_info=True)
        else:
            self.chara_info.create_info(is_create_all_info=True)

        ref_file_path = self._get_ref_path(is_general, head_short_name, body_short_name)
        tail_ref_file_path, tail_ref_texture_path = self._get_tail_ref_path(is_general, head_short_name)

        if not ref_file_path or not os.path.exists(ref_file_path):
            return

        if not tail_ref_file_path or not os.path.exists(tail_ref_file_path):
            return

        mini_face_ref_path = self.mdl_path + self.mini_mdl_default_face_path

        # ミニの09始まりはモブ観客
        if self.chara_info.is_mini:
            if is_general and head_short_name.find('mchr09') >= 0:
                mini_face_ref_path = self.mdl_path + self.mini_mdl_default_audience_face_path
            elif str(self.chara_info.data_main_id).startswith('09'):
                mini_face_ref_path = self.mdl_path + self.mini_mdl_default_audience_face_path

        name_space, ref_top_node_name = self.__get_ref_namespace_and_node_name(ref_file_path)

        if name_space is None or ref_top_node_name is None:
            return

        if is_mini_to_normal:
            normal_name_space, normal_top_node_name = self.__get_ref_namespace_and_node_name(normal_file_path)

            if normal_name_space is None or normal_top_node_name is None:
                return

        if is_visible:

            ref_exists = base_utility.reference.exists(ref_file_path, name_space)

            if not ref_exists:
                base_utility.reference.load(ref_file_path, name_space)

            if is_mini_to_normal:
                if base_utility.reference.exists(normal_file_path, normal_name_space) and ref_exists:
                    return

                base_utility.reference.load(normal_file_path, normal_name_space)

            else:
                if ref_exists:
                    return

            src_top_node = []

            if is_mini_to_normal:
                src_top_node = cmds.ls(normal_top_node_name)
            else:
                src_top_node = cmds.ls(self.chara_info.part_info.root_node)

            if not src_top_node:
                return

            src_neck_node = self.__get_node_target_word(src_top_node, 'Neck')
            if not src_neck_node:
                return

            dst_top_nodes = cmds.ls(ref_top_node_name)
            if not dst_top_nodes:
                return

            dst_top_node = dst_top_nodes[0]
            dst_neck_node = self.__get_node_target_word(dst_top_node, 'Neck')
            if not dst_neck_node:
                return

            if self.chara_info.part_info.data_type.endswith('head'):
                dst_position_node = self.__get_node_target_word(dst_top_node, 'Position')
                if not dst_position_node:
                    return

            if is_mini_to_normal:

                if self.chara_info.part_info.data_type.endswith('head'):
                    cmds.xform(src_neck_node, ws=True, r=True, t=[80, 80, 0])
                elif self.chara_info.part_info.data_type.endswith('body'):
                    src_position_node = self.__get_node_target_word(src_top_node, 'Position')
                    if not src_position_node:
                        return

                    cmds.xform(src_position_node, ws=True, r=True, t=[80, 0, 0])

            dst_neck_node_pos = cmds.xform(src_neck_node, q=True, ws=True, t=True)
            ref_neck_node_pos = cmds.xform(dst_neck_node, q=True, ws=True, t=True)

            trans_value = [
                (dst_neck_node_pos[0] - ref_neck_node_pos[0]),
                (dst_neck_node_pos[1] - ref_neck_node_pos[1]),
                (dst_neck_node_pos[2] - ref_neck_node_pos[2])
            ]

            if self.chara_info.part_info.data_type.endswith('head'):
                cmds.xform(dst_position_node, ws=True, t=trans_value)
            elif self.chara_info.part_info.data_type.endswith('body'):
                cmds.xform(dst_neck_node, ws=True, t=trans_value)

            # 汎用衣装の体型差分の適用
            if self.chara_info.part_info.data_type.endswith('head'):
                self.__apply_body_shape(ref_file_path, dst_top_node, body_shape_id)

            # 尻尾
            self.__load_tail_ref(tail_ref_file_path, name_space + '_tail')
            self.__load_tail_ref_texture(tail_ref_texture_path, name_space + '_tail')

            if self.chara_info.part_info.data_type.endswith('head'):
                self.__adjust_tail_ref_pos(dst_top_node, name_space + '_tail')
            elif self.chara_info.part_info.data_type.endswith('body'):
                self.__adjust_tail_ref_pos(src_top_node, name_space + '_tail')

            # mini_face
            if self.chara_info.is_mini:

                ref_path = ''

                chara_id = '1001'
                chara_sub_id = '00'

                if is_general:
                    is_match = re.search(r'mchr([0-9]{4})_([0-9]{2})', head_short_name)
                    if is_match:
                        chara_id = is_match.group(1)
                        chara_sub_id = is_match.group(2)
                else:
                    chara_id = self.chara_info.data_main_id
                    chara_sub_id = self.chara_info.data_sub_id

                if self.chara_info.part_info.data_type.endswith('_face_head'):

                    ref_path = self.__load_mini_head_ref_base(
                        mini_face_ref_path,
                        name_space + '_face',
                        chara_id,
                        chara_sub_id,
                        False
                    )

                elif self.chara_info.part_info.data_type.endswith('_hair_head'):

                    ref_path = self.__load_mini_head_ref_base(
                        mini_face_ref_path,
                        name_space + '_face',
                        chara_id,
                        chara_sub_id,
                        True
                    )

                else:

                    ref_path = self.__load_mini_head_ref_base(
                        mini_face_ref_path,
                        name_space + '_face',
                        chara_id,
                        chara_sub_id,
                        True
                    )

                self.__adjust_mini_head_ref_pos(src_neck_node, ref_path)

        else:
            if base_utility.reference.exists(ref_file_path, name_space):
                base_utility.reference.unload(ref_file_path, name_space)

            if is_mini_to_normal:
                if base_utility.reference.exists(normal_file_path, normal_name_space):
                    base_utility.reference.unload(normal_file_path, normal_name_space)

            tail_ref_namespace = name_space + '_tail'
            if base_utility.reference.exists(tail_ref_file_path, tail_ref_namespace):
                base_utility.reference.unload(tail_ref_file_path, tail_ref_namespace)

            mini_head_ref_namespace = name_space + '_face'
            mini_head_ref = base_utility.reference.get_reference_file_path_by_namespace(mini_head_ref_namespace)
            if mini_head_ref:
                base_utility.reference.unload(mini_head_ref, mini_head_ref_namespace)

            # リファレンス解除しても残ってしまうcgfxのゴミ等を削除し、namespaceを削除する
            ref_item = cmds.ls(name_space + ':*')
            normal_item = cmds.ls(normal_name_space + ':*') if is_mini_to_normal else []
            tail_ref_item = cmds.ls(tail_ref_namespace + ':*')
            mini_head_ref_item = cmds.ls(mini_head_ref_namespace + ':*')

            delete_target_item = ref_item + normal_item + tail_ref_item + mini_head_ref_item
            if delete_target_item:
                cmds.delete(delete_target_item)

            if cmds.namespace(ex=name_space):
                cmds.namespace(rm=name_space)

            if is_mini_to_normal:
                if cmds.namespace(ex=normal_name_space):
                    cmds.namespace(rm=normal_name_space)

            if cmds.namespace(ex=tail_ref_namespace):
                cmds.namespace(rm=tail_ref_namespace)

            if cmds.namespace(ex=mini_head_ref_namespace):
                cmds.namespace(rm=mini_head_ref_namespace)

    def __get_node_target_word(self, top_node, target_word):
        child_nodes = cmds.listRelatives(top_node, ad=True, pa=True)
        neck_node = ''
        if child_nodes:
            for node in child_nodes:
                if node.endswith(target_word):
                    neck_node = node
                    break

        return neck_node

    def __set_texture(self, target_transform, texture_path):

        if not cmds.objExists(target_transform):
            return
        if not os.path.exists(texture_path):
            return

        shapes = cmds.listRelatives(target_transform, type='shape')
        if not shapes:
            return

        for shape in shapes:
            sgs = cmds.listConnections(shape, t='shadingEngine')
            if not sgs:
                continue

            for sg in sgs:
                mats = cmds.ls(cmds.listConnections(sg), mat=True)
                if not mats:
                    continue

                for mat in mats:
                    files = cmds.ls(cmds.listHistory(mat), type='file')
                    if not files:
                        continue

                    for _file in files:

                        if not _file:
                            continue

                        cmds.setAttr(_file + '.fileTextureName', texture_path, type='string')
                        break

    def __apply_body_shape(self, ref_file_path, top_node, body_shape_id):
        """汎用衣装の体型差分を適用する

        Args:
            ref_file_path (str): 汎用衣装パス
            top_node (str): トップノード名
            body_shape_id (str): 体型差分ID
        """

        dress_chara_info = chara_info.CharaInfo()
        dress_chara_info.create_info(ref_file_path)
        if not dress_chara_info.exists:
            return

        body_shape_info = body_shape_classes.BodyShapeInfoParser.create_from_chara_info(dress_chara_info, False)
        if not body_shape_info:
            return

        body_shape = next((shape for shape in body_shape_info.shapes if shape.suffix[1:] == body_shape_id), None)
        if body_shape is None:
            return

        body_node = self.__get_node_target_word(top_node, 'M_Body')
        if not body_node:
            return

        blend_shapes = cmds.ls(cmds.listHistory(body_node), type='blendShape')
        if not blend_shapes:
            return

        blend_shape = blend_shapes[0]

        shape_targets = {'M_Body' + target: weight for target, weight in body_shape.targets.items()}
        targets = cmds.listAttr(blend_shape + '.weight', multi=True)
        weights = [[i, shape_targets.get(target, 0)] for i, target in enumerate(targets)]

        cmds.blendShape(blend_shape, e=True, w=weights)

    def unload_all_ref(self):

        name_space_list = base_utility.reference.get_reference_namespace_list()

        if not name_space_list:
            return

        for name_space in name_space_list:

            if not name_space.startswith(self.name_space_prefix):
                continue

            ref_file_path = base_utility.reference.get_reference_file_path_by_namespace(name_space)
            cmds.file(ref_file_path, rr=True)

            # リファレンス解除しても残ってしまうcgfxのゴミ等を削除し、namespaceを削除する
            delete_target_item = cmds.ls(name_space + ':*')
            if delete_target_item:
                cmds.delete(delete_target_item)

            if cmds.namespace(ex=name_space):
                cmds.namespace(rm=name_space)

    def set_chara_path_list(self):
        """
        """

        self.general_dress_path_list = []
        self.special_dress_path_list = []
        self.head_path_list = []

        if not os.path.exists(self.mdl_path):
            return {}

        self.chara_info.create_info()

        file_path_list = self._get_file_path_list(self.mdl_path)

        for file_path in file_path_list:

            path_reg = ''
            if self.chara_info.is_mini:
                path_reg = self.mini_full_path_regex
            else:
                path_reg = self.full_path_regex

            search_obj = path_reg.search(file_path)

            if search_obj:

                first_type = search_obj.group(1)
                second_type = search_obj.group(2)
                first_division_id = search_obj.group(3)
                first_body_id = search_obj.group(4)
                third_type = search_obj.group(5)
                second_division_id = search_obj.group(6)
                second_body_id = search_obj.group(7)

                if first_division_id == second_division_id and first_body_id == second_body_id and second_type == third_type:
                    if first_type == 'head' or first_type == 'mini\\head':
                        self.head_path_list.append(file_path)
                    elif first_type == 'tail' or first_type == 'mini\\tail':
                        self.tail_path_list.append(file_path)
                    elif first_division_id == '0':
                        self.general_dress_path_list.append(file_path)
                    elif first_division_id == '1':
                        self.special_dress_path_list.append(file_path)

    def _get_file_path_list(self, dir_path):
        """
        """

        found = []
        for mdl_child_dir_path in self.mdl_child_dir_path_list:

            if not os.path.exists(mdl_child_dir_path):
                continue

            for root, _, files in os.walk(mdl_child_dir_path):

                if not root.endswith('scenes'):
                    continue
                if not files:
                    continue

                found.extend([os.path.join(root, filename) for filename in files])

        return found

    def get_file_name_list_without_ext(self, target_path_list):
        """
        """

        file_name_list = []

        for target_path in target_path_list:
            target_short_path = os.path.split(target_path)
            target_short_path_without_ext = os.path.splitext(target_short_path[1])
            file_name_list.append(target_short_path_without_ext[0])

        return file_name_list

    def get_body_shape_list(self, body_short_name):
        """指定した汎用衣装の体型差分リストを取得する

        Args:
            body_short_name (str): 汎用衣装ID

        Returns:
            list[str] or None: 体型差分リスト
        """

        dress_path = next((path for path in self.general_dress_path_list if body_short_name in path), None)

        if dress_path is None:
            return None

        dress_chara_info = chara_info.CharaInfo()
        dress_chara_info.create_info(dress_path)

        if not dress_chara_info.exists:
            return None

        body_shape_info = body_shape_classes.BodyShapeInfoParser.create_from_chara_info(dress_chara_info, False)

        # 1文字目にアンダースコアが入っているため削除
        return [shape.suffix[1:] for shape in body_shape_info.shapes]

    def get_default_body_shape(self):
        """デフォルト体型差分IDを返す

        Returns:
            str or None: デフォルト体型差分ID（デカ: 1_0_2, ミニ: 1）
        """

        self.chara_info.create_info()

        if not self.chara_info.exists:
            return None

        return '1' if self.chara_info.is_mini else '1_0_2'

    def get_scene_body_shape(self):
        """現在のシーンの体型差分IDを返す

        Returns:
            str or None: 現在のシーンの体型差分ID
        """

        self.chara_info.create_info()

        if not self.chara_info.exists:
            return None

        if self.chara_info.is_mini:
            if self.chara_info.data_info.mini_bust_id is None:
                return None
            return str(self.chara_info.data_info.mini_bust_id)
        else:
            data_info = self.chara_info.data_info
            if data_info.height_id is None or data_info.shape_id is None or data_info.bust_id is None:
                return None
            return '{}_{}_{}'.format(data_info.height_id, data_info.shape_id, data_info.bust_id)
