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

from ....glp_common.classes.info import chara_info
from ....glp_common.classes import body_shape as body_shape_classes


NAMESPACE_PREFIX = '__refpart__'


def equals_abs_path(path_a, path_b):
    """絶対パスが一致するかを返す

    Args:
        path_a (str): 比較する最初のパス
        path_b (str): 比較する2番目のパス

    Returns:
        bool: 絶対パスが一致するか
    """

    return os.path.abspath(path_a) == os.path.abspath(path_b)


def equals_to_current_path(path):
    """現在のシーンと絶対パスが一致するかを返す

    Args:
        path (str): 現在のシーンと比較するパス

    Returns:
        bool: 現在のシーンと絶対パスが一致するか
    """

    return equals_abs_path(path, cmds.file(q=True, sn=True))


def get_node_target_word(top_node, target_word):
    """トップノード以下の指定文字列を含むノードを返す

    Args:
        top_node (str): 基準のトップノード名
        target_word (str): ノード名に含む文字列

    Returns:
        str: 指定文字列を含むノード
    """

    child_nodes = cmds.listRelatives(top_node, ad=True, pa=True)
    target_node = ''
    if child_nodes:
        for node in child_nodes:
            if node.endswith(target_word):
                target_node = node
                break

    return target_node


def get_loaded_ref_path_with_namespace(namespace):
    """ネームスペースが一致するリファレンスを返す

    Args:
        namespace (str): ネームスペース

    Returns:
        str: ネームスペースが一致するリファレンス
    """

    ref_files = cmds.file(q=True, r=True)

    for ref_file in ref_files:
        if not cmds.referenceQuery(ref_file, il=True):
            continue

        if namespace is not None and cmds.referenceQuery(ref_file, ns=True, shn=True) != namespace:
            continue

        return ref_file

    return None


def load_ref_path(ref_path, namespace):
    """リファレンスファイルを読み込む

    Args:
        ref_path (str): ファイルパス
        namespace (str): ネームスペース

    Returns:
        bool: ファイルが読み込めたか
    """

    exists = get_loaded_ref_path_with_namespace(namespace) is not None

    if exists:
        return False

    cmds.file(ref_path, r=True, ns=namespace)

    return True


def unload_ref_path(namespace):
    """リファレンスファイルを削除する

    Args:
        namespace (str): ネームスペース
    """

    ref_file = get_loaded_ref_path_with_namespace(namespace)

    if ref_file is None:
        return

    cmds.file(ref_file, rr=True)

    # リファレンス解除しても残ってしまうcgfxのゴミ等を削除し、namespaceを削除する
    ref_items = cmds.ls(namespace + ':*')

    if ref_items:
        cmds.delete(ref_items)

    if cmds.namespace(ex=namespace):
        cmds.namespace(rm=namespace)


def get_ref_nodes_with_namespace(namespace, node_type=None):
    """ネームスペースからリファレンスノードを取得する

    Args:
        namespace (str): ネームスペース
        node_type (str): ノードタイプ

    Returns:
        list[str]: リファレンスノードのリスト
    """

    ref_nodes = cmds.ls(rn=True, l=True, typ=node_type) if node_type is not None else cmds.ls(rn=True, l=True)
    return [ref_node for ref_node in ref_nodes if cmds.referenceQuery(ref_node, ns=True, shn=True) == namespace]


def get_loaded_ref_nodes():
    """読み込まれているリファレンスノードリストを返す

    Returns:
        list[str]: リファレンスノードのリスト
    """

    loaded_ref_files = (ref_file for ref_file in cmds.file(q=True, r=True) if cmds.referenceQuery(ref_file, il=True))
    ref_files = (ref_file for ref_file in loaded_ref_files if cmds.referenceQuery(ref_file, ns=True, shn=True).startswith(NAMESPACE_PREFIX))

    return [cmds.referenceQuery(ref_file, rfn=True, tr=True) for ref_file in ref_files]


def get_mdl_data_ids(string):
    """パターンに一致するモデルIDを取得する

    Args:
        string (str): ID取得元となる文字列

    Returns:
        tuple[str, str, str, str] or None: データタイプ、データID、サブID、サフィックスのタプル
    """

    match_obj = re.search(r'mdl_(mbdy|bdy|mchr|chr|mtail|tail)([0-9]{4}_[0-9]{2})(_[0-9]{2}|)(_face|_hair|_tail|)', string)

    if not match_obj:
        return None

    data_type = match_obj.group(1)
    data_id = match_obj.group(2)
    data_sub_id = match_obj.group(3)
    data_suffix = match_obj.group(4)

    return data_type, data_id, data_sub_id, data_suffix


def get_mdl_name(string, override_id=None):
    """パターンに一致するモデル名を取得する

    Args:
        string (str): ID取得元となる文字列
        override_id (str): 上書きするID

    Returns:
        str: モデル名
    """

    data_ids = get_mdl_data_ids(string)

    if not data_ids:
        return None

    data_type, data_id, data_sub_id, data_suffix = data_ids

    # ミニ頭部か尻尾なら指定されたIDに変更する
    if override_id:
        if data_type == 'mchr':
            data_id = override_id

        if data_type.endswith('tail'):
            data_type = data_type.replace('tail', 'bdy')
            data_id = override_id
            data_suffix = '_tail'

    return 'mdl_{0}{1}{2}{3}'.format(data_type, data_id, data_sub_id, data_suffix)


def is_ref_data_type(ref_node, data_type):
    """リファレンスノードが指定のデータタイプかを返す

    Args:
        ref_node (str): リファレンスノード
        data_type (str): データタイプ

    Returns:
        bool: リファレンスノードが指定のデータタイプか
    """

    namespace = cmds.referenceQuery(ref_node, ns=True, shn=True)

    data_ids = get_mdl_data_ids(namespace)

    if not data_ids:
        return False

    ref_data_type, _, _, data_suffix = data_ids

    # データタイプで一致した場合は、サフィックスに何もなければ指定されたデータタイプとする
    if ref_data_type.endswith(data_type):
        return data_suffix == ''

    return data_suffix.endswith(data_type)


def get_ref_data_id(ref_node):
    """リファレンスノードのデータIDを返す

    Args:
        ref_node (str): リファレンスノード

    Returns:
        bool: リファレンスノードのデータID
    """

    namespace = cmds.referenceQuery(ref_node, ns=True, shn=True)

    data_ids = get_mdl_data_ids(namespace)

    if not data_ids:
        return ''

    return data_ids[1]


def is_ref_mini(ref_node):
    """リファレンスノードがミニかを返す

    Args:
        ref_node (str): リファレンスノード

    Returns:
        bool: リファレンスノードがミニか
    """

    namespace = cmds.referenceQuery(ref_node, ns=True, shn=True)

    data_ids = get_mdl_data_ids(namespace)

    if not data_ids:
        return False

    return data_ids[0].startswith('m')


def get_root_joint_node(top_node_name):
    """ルートジョイントを取得する

    Args:
        top_node_name (str): トップノード名

    Returns:
        str: ルートジョイント
    """

    short_name = top_node_name.split(':')[-1]

    data_ids = get_mdl_data_ids(short_name)

    if not data_ids:
        return ''

    data_type = data_ids[0]

    if data_type.endswith('bdy'):
        root_joint_name = 'Position'

    elif data_type.endswith('chr'):
        root_joint_name = 'Neck'

    elif data_type.endswith('tail'):
        root_joint_name = 'Hip'

    else:
        return ''

    root_joint_node = get_node_target_word(top_node_name, root_joint_name)

    if not root_joint_node:
        return ''

    return cmds.ls(root_joint_node, l=True)[0]


def get_scene_dress_id():
    """現在のシーンの衣装IDを返す

    Returns:
        tuple[bool, str or None, bool]: デカモデルか否か、現在のシーンの衣装ID、汎用シーンかのタプル
    """

    current_chara_info = chara_info.CharaInfo()
    current_chara_info.create_info()

    if not current_chara_info.exists:
        return True, None, False

    is_normal = not current_chara_info.is_mini
    data_id = '{}_{}'.format(current_chara_info.data_main_id, current_chara_info.data_sub_id)
    is_general = current_chara_info.part_info.data_type == 'mini_face_head' or current_chara_info.part_info.data_type.endswith('general_tail')

    return is_normal, data_id, is_general


class ReferencePart(object):

    def __init__(self):
        """
        """

        self.mdl_path = 'W:\\gallop\\svn\\svn_gallop\\80_3D\\01_character\\01_model'
        self.mdl_body_path = '{}\\body'.format(self.mdl_path)
        self.mdl_head_path = '{}\\head'.format(self.mdl_path)
        self.mdl_tail_path = '{}\\tail'.format(self.mdl_path)
        self.mdl_mini_path = '{}\\mini'.format(self.mdl_path)
        self.mdl_mini_body_path = '{}\\body'.format(self.mdl_mini_path)
        self.mdl_mini_head_path = '{}\\head'.format(self.mdl_mini_path)
        self.mdl_child_dir_path_list = [self.mdl_body_path, self.mdl_head_path, self.mdl_tail_path, self.mdl_mini_path]

        self.mini_mdl_default_face_path = '\\mini\\head\\mchr0001_00\\scenes\\mdl_mchr0001_00_face0.ma'
        self.mini_mdl_default_audience_face_path = '\\mini\\head\\mchr0900_00\\scenes\\mdl_mchr0900_00_face0.ma'

        self.mdl_general_tail_path = self.mdl_tail_path + '\\tail{0:0>4}_00\\scenes\\mdl_tail{0:0>4}_00.ma'
        self.mini_mdl_general_tail_path = self.mdl_mini_path + '\\tail\\mtail{0:0>4}_00\\scenes\\mdl_mtail{0:0>4}_00.ma'

        self.mdl_general_tail_texture_path = self.mdl_tail_path + '\\tail{0:0>4}_00\\sourceimages\\tex_tail{0:0>4}_00_{1:0>4}_diff.tga'
        self.mini_mdl_general_tail_texture_path = self.mdl_mini_path + '\\tail\\mtail{0:0>4}_00\\sourceimages\\tex_mtail{0:0>4}_00_{1:0>4}_diff.tga'

        self.path_regex = r'\\(body|head|tail)\\(bdy|chr|tail)([0-9])([0-9]{3}_[0-9]{2})\\scenes\\mdl_(bdy|chr|tail)([0-1])([0-9]{3}_[0-9]{2})(_[0-9]{2}|)(_Bust[LM]|).ma'
        self.mini_path_regex = r'\\(mini\\body|mini\\head|mini\\tail)\\(mbdy|mchr|mtail)([0-9])([0-9]{3}_[0-9]{2})\\scenes\\mdl_(mbdy|mchr|mtail)([0-1])([0-9]{3}_[0-9]{2})(_[0-9]{2}|)(_Bust[LM]|_hair|).ma'

        self.full_path_regex = re.compile(re.escape(self.mdl_path) + self.path_regex)
        self.mini_full_path_regex = re.compile(re.escape(self.mdl_path) + self.mini_path_regex)
        self.chara_info = chara_info.CharaInfo()

        self.general_dress_path_list = []
        self.special_dress_path_list = []
        self.head_path_list = []
        self.tail_path_list = []

    def __get_ref_path(self, is_general, head_short_name, body_short_name):
        """リファレンスパスを取得する

        Args:
            is_general (bool): 汎用衣装か
            head_short_name (str): 頭部ID
            body_short_name (str): 衣装ID

        Returns:
            str: リファレンスパス
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

    def __get_tail_ref_path(self, is_general, ref_file_path):
        """尻尾のリファレンスパスを取得する

        Args:
            is_general (bool): 汎用衣装か
            ref_file_path (str): リファレンスパス

        Returns:
            str: 尻尾のリファレンスパス
        """

        tail_chara_info = chara_info.CharaInfo()

        if self.chara_info.part_info.is_unique_chara:
            if is_general:
                # 通常頭部から汎用衣装を読み込んだ場合、シーンのCharaInfoを反映した汎用尻尾にする
                if self.chara_info.part_info.data_type.endswith('head') and self.chara_info.data_info.chara_tail_model_id is not None:
                    tail_id = str(self.chara_info.data_info.chara_tail_model_id)
                    tail_path = self.mini_mdl_general_tail_path if self.chara_info.is_mini else self.mdl_general_tail_path
                    tail_chara_info.tail_char_id = self.chara_info.part_info.main_id
                    tail_chara_info.create_info(tail_path.format(tail_id), is_create_all_info=True)

            else:
                # 特別衣装を読み込んだ場合、シーンのCharaInfoから取得した尻尾にする
                tail_chara_info.tail_char_id = self.chara_info.part_info.main_id
                tail_chara_info.create_info(self.chara_info.file_path, is_create_all_info=True)

        else:
            if is_general:
                # 汎用衣装から頭部を読み込んだ場合、頭部のCharaInfoを反映した汎用尻尾にする
                if self.chara_info.part_info.data_type.endswith('body') and ref_file_path:
                    temp_chara_info = chara_info.CharaInfo()
                    temp_chara_info.create_info(ref_file_path)
                    if temp_chara_info.exists and temp_chara_info.data_info.chara_tail_model_id is not None:
                        tail_id = str(temp_chara_info.data_info.chara_tail_model_id)
                        tail_path = self.mini_mdl_general_tail_path if self.chara_info.is_mini else self.mdl_general_tail_path
                        tail_chara_info.tail_char_id = temp_chara_info.part_info.main_id
                        tail_chara_info.create_info(tail_path.format(tail_id), is_create_all_info=True)

                # モブ頭部/ミニ頭部から汎用衣装を読み込んだ場合、汎用尻尾0001にする
                elif self.chara_info.part_info.data_type.endswith('head'):
                    tail_id = '0001'
                    char_id = '1001' if self.chara_info.is_mini else '0001'

                    tail_path = self.mini_mdl_general_tail_path if self.chara_info.is_mini else self.mdl_general_tail_path
                    tail_texture_path = self.mini_mdl_general_tail_texture_path if self.chara_info.is_mini else self.mdl_general_tail_texture_path

                    return tail_path.format(tail_id), tail_texture_path.format(tail_id, char_id)

        if not tail_chara_info or not tail_chara_info.exists:
            return None, None

        tail_part_info = tail_chara_info.tail_part_info

        if not tail_part_info or not tail_part_info.exists:
            return None, None

        tmp_tail_ref_file_path = ''
        tmp_tail_ref_texture_path = ''

        for file in tail_part_info.maya_file_list:

            if 'tail' not in file:
                continue

            tmp_path = '{0}\\{1}'.format(tail_part_info.maya_scenes_dir_path, file)

            if not os.path.exists(tmp_path):
                continue

            tmp_tail_ref_file_path = tmp_path
            break

        for texture in tail_part_info.texture_list:

            if '_diff' not in texture:
                continue

            tmp_path = '{0}\\{1}'.format(tail_part_info.maya_sourceimages_dir_path, texture)

            if not os.path.exists(tmp_path):
                continue

            tmp_tail_ref_texture_path = tmp_path
            break

        return tmp_tail_ref_file_path, tmp_tail_ref_texture_path

    def __adjust_tail_ref_pos(self, body_top_node, tail_top_node):
        """尻尾リファレンスの位置を調整する

        Args:
            body_top_node (str): 身体のトップノード名
            tail_top_node (str): 尻尾のトップノード名
        """

        tail_root_joint_node = get_root_joint_node(tail_top_node)

        if not tail_root_joint_node:
            return

        pos = self.__get_node_pos_diff(body_top_node, tail_top_node, 'Hip')

        cmds.xform(tail_root_joint_node, ws=True, t=pos)

    def __load_tail_ref_texture(self, tail_ref_texture_path, tail_ref_file_path, current_chara_info):
        """尻尾リファレンスにテクスチャを読み込み適用する

        Args:
            tail_ref_texture_path (str): 尻尾のテクスチャパス
            tail_ref_file_path (str): 尻尾のリファレンスパス
            current_chara_info (chara_info.CharaInfo): 現在のシーンのCharaInfo
        """

        if not tail_ref_texture_path or not os.path.exists(tail_ref_texture_path):
            return

        mesh_nodes = self.__get_ref_or_current_nodes(tail_ref_file_path, current_chara_info)

        if not mesh_nodes:
            return

        m_tail_node = next((node for node in mesh_nodes if node.split('|')[-1].split(':')[-1] == 'M_Tail'), '')

        if not cmds.objExists(m_tail_node):
            return

        self.__set_texture(m_tail_node, tail_ref_texture_path)

    def __get_mini_head_chara_info(self, is_general, head_short_name):
        """ミニ頭部のCharaInfoを取得する

        髪または顔のCharaInfo

        Args:
            is_general (bool): 汎用衣装か
            head_short_name (str): 頭部ID

        Returns:
            chara_info.CharaInfo: ミニ頭部のCharaInfo
        """

        face_ref_path = self.mdl_path + self.mini_mdl_default_face_path

        if (is_general and 'mchr09' in head_short_name) or self.chara_info.data_main_id.startswith('09'):
            face_ref_path = self.mdl_path + self.mini_mdl_default_audience_face_path

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

        # 肌色を取得するためにidから一時的なinfoを作成
        tmp_info = chara_info.CharaInfo()
        tmp_id = 'mdl_chr{}_{}'.format(chara_id, chara_sub_id)
        tmp_info.create_info(tmp_id)

        # 髪や肌色のテクスチャを参照するために顔のキャラインフォを作成
        option = {}
        option.update({'hair_id': chara_id, 'hair_sub_id': chara_sub_id})

        if tmp_info.data_info:
            option.update({
                'extra_value_dict_list': [
                    {'name': 'SKINCOLOR', 'value': tmp_info.data_info.skin_id}
                ]
            })

        mini_head_chara_info = chara_info.CharaInfo()
        mini_head_chara_info.create_info(face_ref_path, option=option)

        return mini_head_chara_info

    def __get_mini_head_ref_path(self, mini_head_chara_info):
        """ミニ頭部のリファレンスパスを取得する

        Args:
            mini_head_chara_info (chara_info.CharaInfo): ミニ頭部のCharaInfo

        Returns:
            str: ミニ頭部のリファレンスパス
        """

        if self.chara_info.part_info.data_type.endswith('_face_head'):

            scene_path = mini_head_chara_info.alternative_info.maya_scenes_dir_path
            file_name = 'mdl_mchr{}_{}_hair.ma'.format(mini_head_chara_info.alternative_hair_id, mini_head_chara_info.alternative_hair_sub_id)
            hair_ref_path = '{}/{}'.format(scene_path, file_name)

            return hair_ref_path

        else:
            return mini_head_chara_info.file_path

    def __adjust_mini_head_ref_pos(self, body_top_node, head_top_node):
        """ミニ頭部リファレンスの位置を調整する

        Args:
            body_top_node (str): 身体のトップノード名
            head_top_node (str): ミニ頭部のトップノード名
        """

        neck_root_joint_node = get_root_joint_node(head_top_node)

        if not neck_root_joint_node:
            return

        pos = self.__get_node_pos_diff(body_top_node, head_top_node, 'Neck')

        cmds.xform(neck_root_joint_node, ws=True, t=pos)

    def __load_mini_head_ref_texture(self, ref_chara_info, mini_head_ref_file_path, current_chara_info):
        """ミニ頭部リファレンスにテクスチャを読み込み適用する

        Args:
            ref_chara_info (chara_info.CharaInfo): リファレンスのCharaInfo
            mini_head_ref_file_path (str): ミニ頭部のリファレンスパス
            current_chara_info (chara_info.CharaInfo): 現在のシーンのCharaInfo
        """

        if not ref_chara_info.alternative_info or not ref_chara_info.alternative_info.exists:
            return

        mesh_nodes = self.__get_ref_or_current_nodes(mini_head_ref_file_path, current_chara_info)

        if not mesh_nodes:
            return

        for mesh in mesh_nodes:

            no_ns_name = mesh.split('|')[-1].split(':')[-1]

            # matrialリストのindexを検索
            this_material_index = None
            for mesh_param in ref_chara_info.part_info.mesh_param_list:
                if mesh_param['name'].endswith(no_ns_name):
                    this_material_index = int(mesh_param['material_list'][0])
                    break

            if this_material_index is None:
                continue

            # hair側のtextureリストのindexを検索
            if not ref_chara_info.part_info.material_param_list:
                continue

            material_param = ref_chara_info.part_info.material_param_list[this_material_index]
            alternate_id = material_param['diff']

            # テクスチャ名を検索
            this_texture = ''
            souce_image_dir = ''

            # 髪側のテクスチャを髪のinfoから検索
            for tex_param in ref_chara_info.alternative_info.texture_param_list:
                if tex_param['alternate_id'] == alternate_id:
                    this_texture = tex_param['name']
                    souce_image_dir = ref_chara_info.alternative_info.maya_sourceimages_dir_path
                    break

            # 肌色を修正するために顔のinfoから検索
            for tex_param in ref_chara_info.part_info.texture_param_list:
                if tex_param['id'] == alternate_id:
                    this_texture = tex_param['name']
                    souce_image_dir = ref_chara_info.part_info.maya_sourceimages_dir_path
                    break

            if not this_texture:
                continue

            texture_path = '{}/{}'.format(souce_image_dir, this_texture)

            self.__set_texture(mesh, texture_path)

    def __get_base_file_path(self, is_normal_dress_type, special_dress_id):
        """衣装IDからファイルパスを取得する

        Args:
            is_normal_dress_type (bool): デカ衣装か
            special_dress_id (str): 衣装ID

        Returns:
            str: ファイルパス
        """

        base_dress_file_path = ''

        if is_normal_dress_type:
            base_dress_file_path = os.path.join(self.mdl_body_path, r'bdy{0}\scenes\mdl_bdy{0}.ma'.format(special_dress_id))
        else:
            base_dress_file_path = os.path.join(self.mdl_mini_body_path, r'mbdy{0}\scenes\mdl_mbdy{0}.ma'.format(special_dress_id))

        return base_dress_file_path

    def __get_ref_namespace(self, ref_file_path):
        """リファレンス用のネームスペースを取得する

        Args:
            ref_file_path (str): リファレンスパス

        Returns:
            str: ネームスペース
        """

        data_id = '{}_{}'.format(self.chara_info.data_main_id, self.chara_info.data_sub_id)

        mdl_name = get_mdl_name(ref_file_path, data_id)

        if not mdl_name:
            return ''

        return NAMESPACE_PREFIX + mdl_name

    def __get_ref_top_node_name(self, ref_file_path):
        """リファレンス対象のトップノード名を取得する

        Args:
            ref_file_path (str): リファレンスパス

        Returns:
            str: トップノード名
        """

        namespace = self.__get_ref_namespace(ref_file_path)

        if not namespace:
            return ''

        mdl_name = get_mdl_name(ref_file_path)

        if not mdl_name:
            return ''

        top_node_name = os.path.splitext(os.path.basename(ref_file_path))[0] if self.chara_info.is_mini else mdl_name

        return '{0}:{1}'.format(namespace, top_node_name)

    def __get_ref_top_nodes(self):
        """リファレンスのトップノード名のリストを取得する

        Returns:
            list[str]: トップノード名のリスト
        """

        ref_top_nodes = []

        ref_nodes = get_loaded_ref_nodes()

        for ref_node in ref_nodes:
            file_name = cmds.referenceQuery(ref_node, f=True, wcn=True)
            top_node_name = self.__get_ref_top_node_name(file_name)

            if not top_node_name:
                continue

            if not cmds.objExists(top_node_name):
                continue

            ref_top_nodes.append(top_node_name)

        return ref_top_nodes

    def __get_should_load_base(self, is_general, is_normal_dress_type, special_dress_id, current_chara_info):
        """ベースシーンをロードする必要があるかを返す

        Args:
            is_general (bool): 汎用衣装か
            is_normal_dress_type (bool): デカ衣装か
            special_dress_id (str): 特別衣装ID
            current_chara_info (chara_info.CharaInfo): 現在のシーンのCharaInfo

        Returns:
            bool: ベースシーンをロードする必要があるか
        """

        if is_general:
            return False

        if not current_chara_info.exists:
            return True

        data_type = current_chara_info.part_info.data_type

        if not data_type.endswith('head') and not data_type.endswith('body'):
            return True

        is_normal = not current_chara_info.is_mini
        data_id = '{}_{}'.format(current_chara_info.data_main_id, current_chara_info.data_sub_id)

        return is_normal != is_normal_dress_type or data_id != special_dress_id

    def __get_ref_or_current_nodes(self, ref_file_path, current_chara_info):
        """リファレンスファイルが現在のシーンと同一かによってリファレンスノードか現在のシーンのノードを取得する

        Args:
            ref_file_path (str): リファレンスファイル
            current_chara_info (chara_info.CharaInfo): 現在のシーンのCharaInfo

        Returns:
            list[str]: ノードリスト
        """

        if current_chara_info and current_chara_info.exists and equals_abs_path(current_chara_info.file_path, ref_file_path):
            return cmds.ls(current_chara_info.part_info.mesh_list, typ='transform', l=True)

        else:
            namespace = self.__get_ref_namespace(ref_file_path)
            return get_ref_nodes_with_namespace(namespace, 'transform')

    def __get_base_pos_x(self, current_chara_info):
        """リファレンスのX座標を取得する

        Args:
            current_chara_info (chara_info.CharaInfo): 現在のシーンのCharaInfo

        Returns:
            float: リファレンスのX座標
        """

        distance = 80

        ref_top_nodes = self.__get_ref_top_nodes()
        ref_root_joints = [get_root_joint_node(ref_top_node) for ref_top_node in ref_top_nodes]

        if not ref_root_joints:
            if not current_chara_info.exists:
                distance = 0

            return distance

        max_joint = max((joint for joint in ref_root_joints if joint), key=lambda x: cmds.xform(x, q=True, ws=True, t=True)[0])

        if not is_ref_mini(max_joint):
            if self.chara_info.exists and not self.chara_info.is_mini:
                distance = 130

        return cmds.xform(max_joint, q=True, ws=True, t=True)[0] + distance

    def __get_base_pos_y(self, current_chara_info):
        """リファレンスのY座標を取得する

        Args:
            current_chara_info (chara_info.CharaInfo): 現在のシーンのCharaInfo

        Returns:
            float: リファレンスのY座標
        """

        if not current_chara_info.exists:
            return 0

        is_mini = current_chara_info.is_mini
        data_type = current_chara_info.part_info.data_type

        if not data_type.endswith('head') and not data_type.endswith('tail'):
            return 0

        data_id = '{}_{}'.format(current_chara_info.data_main_id, current_chara_info.data_sub_id)

        ref_top_nodes = self.__get_ref_top_nodes()
        bdy_ref_top_nodes = (node for node in ref_top_nodes if is_ref_data_type(node, 'bdy') and is_ref_mini(node) == is_mini)

        if data_type == 'mini_face_head' or data_type.endswith('general_tail'):
            bdy_ref_top_node = next(bdy_ref_top_nodes, None)
        else:
            bdy_ref_top_node = next((node for node in bdy_ref_top_nodes if get_ref_data_id(node) == data_id), None)

        if not bdy_ref_top_node or not cmds.objExists(bdy_ref_top_node):
            return 0

        bdy_mesh_node = get_node_target_word(bdy_ref_top_node, 'M_Body')

        if not bdy_mesh_node or not cmds.objExists(bdy_mesh_node):
            return 0

        return cmds.xform(cmds.ls(bdy_mesh_node, l=True)[0], q=True, ws=True, bb=True)[1]

    def __get_mini_base_pos(self, src_top_node, base_top_node):
        """現在のシーンがミニ頭部の場合のリファレンスの位置を取得する

        Args:
            src_top_node (str): 現在のシーンのトップノード名
            base_top_node (str): ベースシーンのトップノード名

        Returns:
            list[float, float, float]: ミニ頭部のリファレンスの位置
        """

        return self.__get_node_pos_diff(src_top_node, base_top_node, 'Neck')

    def __get_tail_base_pos(self, src_top_node, base_top_node):
        """現在のシーンが尻尾の場合のリファレンスの位置を取得する

        Args:
            src_top_node (str): 現在のシーンのトップノード名
            base_top_node (str): ベースシーンのトップノード名

        Returns:
            list[float, float, float]: 尻尾のリファレンスの位置
        """

        return self.__get_node_pos_diff(src_top_node, base_top_node, 'Hip')

    def __adjust_base_pos(self, base_top_node, pos):
        """ベース用リファレンスの位置を調整する

        Args:
            base_top_node (str): ベースシーンのトップノード名
            pos (list[float, float, float]): リファレンスの位置
        """

        root_joint_node = get_root_joint_node(base_top_node)
        cmds.xform(root_joint_node, ws=True, t=pos)

    def __get_node_pos_diff(self, src_top_node, dst_top_node, node_name):
        """同名ノード間の差を取得する

        Args:
            src_top_node (str): 基準のトップノード名
            dst_top_node (str): 差をとるトップノード名
            node_name (str): ノード名

        Returns:
            list[float, float, float]: 同名ノード間の差
        """

        diff = [0, 0, 0]

        src_node = get_node_target_word(src_top_node, node_name)

        if not src_node or not cmds.objExists(src_node):
            return diff

        dst_node = get_node_target_word(dst_top_node, node_name)

        if not dst_node or not cmds.objExists(dst_node):
            return diff

        src_node_pos = cmds.xform(src_node, q=True, ws=True, t=True)
        dst_node_pos = cmds.xform(dst_node, q=True, ws=True, t=True)

        diff = [
            (src_node_pos[0] - dst_node_pos[0]),
            (src_node_pos[1] - dst_node_pos[1]),
            (src_node_pos[2] - dst_node_pos[2])
        ]

        return diff

    def __adjust_ref_pos(self, src_top_node, dst_top_node):
        """リファレンスの位置を調整する

        Args:
            src_top_node (str): 元のシーンのトップノード名
            dst_top_node (str): リファレンスのトップノード名
        """

        dst_root_joint_node = get_root_joint_node(dst_top_node)

        if not dst_root_joint_node:
            return

        trans_value = self.__get_node_pos_diff(src_top_node, dst_top_node, 'Neck')

        cmds.xform(dst_root_joint_node, ws=True, t=trans_value)

    def view_parts_ref(self, is_visible, is_general, head_short_name, body_short_name, body_shape_id, is_normal_dress_type, special_dress_id):
        """リファレンスの表示/非表示

        Args:
            is_visible (bool): 表示/非表示
            is_general (bool): 汎用衣装か
            head_short_name (str): 頭部ID
            body_short_name (str): 衣装ID
            body_shape_id (str): 体型差分ID
            is_normal_dress_type (bool): デカ衣装か
            special_dress_id (str): 特別衣装ID
        """

        current_chara_info = chara_info.CharaInfo()
        current_chara_info.create_info()

        if is_general and not current_chara_info.exists:
            return

        should_load_base = self.__get_should_load_base(is_general, is_normal_dress_type, special_dress_id, current_chara_info)

        if should_load_base:
            base_file_path = self.__get_base_file_path(is_normal_dress_type, special_dress_id)

            if not os.path.exists(base_file_path):
                return

            self.chara_info.create_info(base_file_path)

            if not self.chara_info.exists:
                return
        else:
            self.chara_info = current_chara_info

        is_mini = self.chara_info.is_mini
        is_head = self.chara_info.part_info.data_type.endswith('head')
        is_body = self.chara_info.part_info.data_type.endswith('body')

        ref_file_path = self.__get_ref_path(is_general, head_short_name, body_short_name)

        if not ref_file_path or not os.path.exists(ref_file_path):
            return

        if is_mini:
            mini_head_chara_info = self.__get_mini_head_chara_info(is_general, head_short_name)
            mini_head_ref_file_path = self.__get_mini_head_ref_path(mini_head_chara_info)

        tail_ref_file_path, tail_ref_texture_path = self.__get_tail_ref_path(is_general, ref_file_path)

        # 尻尾を持つキャラクターで尻尾が取得できない場合のみ処理を中断
        has_tail = tail_ref_file_path is not None or tail_ref_texture_path is not None

        if has_tail:
            if not tail_ref_file_path or not os.path.exists(tail_ref_file_path):
                return
            if not tail_ref_texture_path or not os.path.exists(tail_ref_texture_path):
                return

        # ネームスペースの取得
        namespace = self.__get_ref_namespace(ref_file_path)

        if not namespace:
            return

        if should_load_base:
            base_namespace = self.__get_ref_namespace(base_file_path)

            if not base_namespace:
                return

        if is_mini:
            mini_namespace = self.__get_ref_namespace(mini_head_ref_file_path)

            if not mini_namespace:
                return

        if has_tail:
            tail_namespace = self.__get_ref_namespace(tail_ref_file_path)

            if not tail_namespace:
                return

        if is_visible:

            # トップノード名の取得
            ref_top_node_name = self.__get_ref_top_node_name(ref_file_path)

            if should_load_base:
                base_top_node_name = self.__get_ref_top_node_name(base_file_path)

            if self.chara_info.is_mini:
                mini_top_node_name = self.__get_ref_top_node_name(mini_head_ref_file_path)
                mini_equals_to_current_path = equals_to_current_path(mini_head_ref_file_path)

            if has_tail:
                tail_top_node_name = self.__get_ref_top_node_name(tail_ref_file_path)
                tail_equals_to_current_path = equals_to_current_path(tail_ref_file_path)

            if should_load_base:
                base_pos_x = self.__get_base_pos_x(current_chara_info)

            ref_loaded = load_ref_path(ref_file_path, namespace)

            if should_load_base:
                load_ref_path(base_file_path, base_namespace)

            if not ref_loaded:
                return

            src_top_nodes = []

            if should_load_base:
                src_top_nodes = cmds.ls(base_top_node_name)
            else:
                src_top_nodes = cmds.ls(self.chara_info.part_info.root_node)

            if not src_top_nodes:
                return

            src_top_node = src_top_nodes[0]

            dst_top_nodes = cmds.ls(ref_top_node_name)
            if not dst_top_nodes:
                return

            dst_top_node = dst_top_nodes[0]

            if should_load_base:
                base_pos = [base_pos_x, self.__get_base_pos_y(current_chara_info), 0]

                if self.chara_info.is_mini and mini_equals_to_current_path:
                    base_pos = self.__get_mini_base_pos(current_chara_info.part_info.root_node, src_top_node)

                if has_tail and tail_equals_to_current_path:
                    base_pos = self.__get_tail_base_pos(current_chara_info.part_info.root_node, src_top_node)

                self.__adjust_base_pos(src_top_node, base_pos)

            self.__adjust_ref_pos(src_top_node, dst_top_node)

            # 汎用衣装の体型差分の適用
            if is_head:
                self.__apply_body_shape(ref_file_path, dst_top_node, body_shape_id)

            # ミニ頭部
            if self.chara_info.is_mini:
                if not mini_equals_to_current_path:
                    load_ref_path(mini_head_ref_file_path, mini_namespace)
                    self.__adjust_mini_head_ref_pos(src_top_node, mini_top_node_name)

                self.__load_mini_head_ref_texture(mini_head_chara_info, mini_head_ref_file_path, current_chara_info)

            # 尻尾
            if has_tail:
                if not tail_equals_to_current_path:
                    load_ref_path(tail_ref_file_path, tail_namespace)

                    if is_head:
                        self.__adjust_tail_ref_pos(dst_top_node, tail_top_node_name)
                    elif is_body:
                        self.__adjust_tail_ref_pos(src_top_node, tail_top_node_name)

                self.__load_tail_ref_texture(tail_ref_texture_path, tail_ref_file_path, current_chara_info)

        else:
            unload_ref_path(namespace)

            if should_load_base:
                unload_ref_path(base_namespace)

            if is_mini:
                unload_ref_path(mini_namespace)

            if has_tail:
                unload_ref_path(tail_namespace)

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

        body_node = get_node_target_word(top_node, 'M_Body')
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
        """すべてのリファレンスを削除する
        """

        ref_nodes = get_loaded_ref_nodes()

        if not ref_nodes:
            return

        for ref_node in ref_nodes:
            namespace = cmds.referenceQuery(ref_node, ns=True, shn=True)
            unload_ref_path(namespace)

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

    def get_special_dress_ids_list(self):
        """特別衣装IDリストを取得する

        Returns:
            tuple[list[str], list[str]]: 衣装IDリストのデカ、ミニのタプル
        """

        normal_body_regex = re.compile(r'bdy([1-9][0-9]{3}_[0-9]{2})')
        normal_head_regex = re.compile(r'chr([1-9][0-9]{3}_[0-9]{2})')
        mini_body_regex = re.compile(r'mbdy([1-9][0-9]{3}_[0-9]{2})')
        mini_head_regex = re.compile(r'mchr([1-9][0-9]{3}_[0-9]{2})')

        normal_body_ids = {match.group(1) for match in (normal_body_regex.search(path) for path in os.listdir(self.mdl_body_path)) if match}
        normal_head_ids = {match.group(1) for match in (normal_head_regex.search(path) for path in os.listdir(self.mdl_head_path)) if match}
        mini_body_ids = {match.group(1) for match in (mini_body_regex.search(path) for path in os.listdir(self.mdl_mini_body_path)) if match}
        mini_head_ids = {match.group(1) for match in (mini_head_regex.search(path) for path in os.listdir(self.mdl_mini_head_path)) if match}

        normal_ids = sorted(normal_body_ids | normal_head_ids)
        mini_ids = sorted(mini_body_ids | mini_head_ids)

        return normal_ids, mini_ids
