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

import re

import maya.cmds as cmds

from .. import base_common
from ..base_common import utility as base_utility
from ..base_common import classes as base_class

reload(base_common)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EyeCoverSetup(object):
    """目隠しメッシュをM_Faceに仕込む処理を行うクラス
    """

    # ===============================================
    def __init__(self):
        """コンストラクタ
        """

        self.l_rotate = [0, 180, 0]
        self.r_rotate = [0, 180, 0]
        self.l_translate = [1.5, 0, -2.5]
        self.r_translate = [-1.5, 0, -2.5]

        self.target_transform = None
        self.target_joint = None

        self.mirror_transform = None
        self.mirror_joint = None

        self.l_transform = None
        self.r_transform = None

        self.l_joint = None
        self.r_joint = None

        self.is_l = False

        self.chara_info = None
        self.m_face = None
        self.root_node = None

        self.is_ready = False

    # ===============================================
    def initialize(self, target_obj, target_joint, chara_info):
        """初期化

        Args:
            target_obj(str): 目隠しメッシュ
            target_joint(str): 目隠しメッシュをバインドするジョイント
            chara_info(chara_info.CharaInfo): 現在のシーンのCharaInfoインスタンス
        """

        if not cmds.objExists(target_obj) or not cmds.objExists(target_joint):
            return

        self.target_transform = target_obj
        self.target_joint = target_joint
        self.l_joint, self.r_joint = self.__get_both_side_joint(self.target_joint)

        if not cmds.objExists(self.l_joint) or not cmds.objExists(self.r_joint):
            return

        for mesh in chara_info.part_info.mesh_list:
            if mesh.endswith('|M_Face'):
                self.m_face = mesh

        if not self.m_face or not cmds.objExists(self.m_face):
            return

        if not chara_info.part_info.root_node:
            return

        self.root_node = chara_info.part_info.root_node

        self.is_ready = True

    # ===============================================
    def setup(self):
        """目隠しメッシュを規定位置に配置しM_Faceに統合

        Returns:
            float: 左目の配置時に使用したX座標の移動値
            str: 左目の目隠しをバインドしたジョイント
        """

        # フェイシャルセットアップ用に返す値
        result_left_x_offset = None

        if not self.is_ready:
            return result_left_x_offset, self.target_joint

        self.__unlock_transform(self.target_transform)

        # 左右のセットアップ用メッシュを作成
        self.l_transform, self.r_transform = self.__create_both_side_eye_coverself(self.target_transform)

        # ジョイントをピボットにして回転
        self.__translate_around_node(self.l_transform, self.l_joint, self.l_translate, self.l_rotate)
        self.__translate_around_node(self.r_transform, self.r_joint, self.r_translate, self.r_rotate)

        # 左右メッシュが重ならないようにworldのx=0から左右に0.3間隔をあける
        l_bounds = cmds.polyEvaluate(self.l_transform, b=True, ae=True)
        l_most_inner_x = l_bounds[0][0]
        l_target_inner_x = 0.3
        l_translate_x = round(l_target_inner_x - l_most_inner_x, 1)  # キャラ班要望で作業しやすいように移動値は小数1桁に丸める
        r_translate_x = l_translate_x * -1
        cmds.xform(self.l_transform, r=True, t=[l_translate_x, 0, 0])
        cmds.xform(self.r_transform, r=True, t=[r_translate_x, 0, 0])

        # 結果出力用に左側の移動値を保持しておく
        result_l_translate = cmds.xform(self.l_transform, q=True, t=True, ws=False)
        result_left_x_offset = result_l_translate[0]

        # 対応ジョイントのみにスキニング
        cmds.skinCluster(self.l_transform, self.l_joint, tsb=True)
        cmds.skinCluster(self.r_transform, self.r_joint, tsb=True)

        # ヒストリーが残っているとコンバイン時にメッシュが崩れることがあるので一度リバインド
        self._rebind_skin(self.m_face)
        self._rebind_skin(self.l_transform)
        self._rebind_skin(self.r_transform)

        # スキンドコンバインを実行
        cmds.polyUniteSkinned(self.l_transform, self.r_transform, self.m_face, op=True, ch=False)

        # 新しくコンバインされたメッシュのuuidを取得
        new_m_face_uuid = cmds.ls(sl=True, uuid=True)[0]

        # M_Faceの階層構造を再生
        new_m_face = cmds.ls(new_m_face_uuid)[0]
        cmds.parent(new_m_face, self.root_node)

        # 不要ノードが残っていれば削除
        del_transform_list = []

        if cmds.objExists(self.l_transform):
            del_transform_list.append(self.l_transform)
        if cmds.objExists(self.r_transform):
            del_transform_list.append(self.r_transform)
        if cmds.objExists(self.m_face):
            del_transform_list.append(self.m_face)
        if cmds.objExists(self.target_transform):
            del_transform_list.append(self.target_transform)

        if del_transform_list:
            cmds.delete(del_transform_list)

        # 新規コンバインされたメッシュの名前をM_Faceに戻す
        new_m_face = cmds.ls(new_m_face_uuid)[0]
        cmds.rename(new_m_face, 'M_Face')

        # リバインド
        new_m_face = cmds.ls(new_m_face_uuid)[0]
        self._rebind_skin(new_m_face)

        # フェイシャルセットアップ時に必要になるので左目の移動値とバインド先を返す
        return result_left_x_offset, self.l_joint

    # ===============================================
    def __get_both_side_joint(self, target_joint):
        """セットアップ用の左右のジョイントを取得

        Args:
            target_joint(str): 作業者が指定したジョイント(左右は不明)
        Returns:
            左目用のジョイント
            右目用のジョイント
        """

        pattern = r'_[LR]$'
        match_obj = re.search(pattern, target_joint)

        if not match_obj:
            return None, None

        suffix = match_obj.group()
        mirror_joint = None

        if suffix == '_L':
            mirror_joint = target_joint.replace(suffix, '_R')
            return target_joint, mirror_joint
        elif suffix == '_R':
            mirror_joint = target_joint.replace(suffix, '_L')
            return mirror_joint, target_joint

    # ===============================================
    def __create_both_side_eye_coverself(self, input_eye_cover_mesh):
        """セットアップ用の左右の目隠しメッシュを生成する

        input_eye_cover_meshが両側ある場合は左右に分離。片側の場合は反対側を複製して両方用意する

        Args:
            input_eye_cover_mesh: 作業者が用意した目隠しメッシュ

        Returns:
            左目のセットアップ用メッシュ
            右目のセットアップ用メッシュ
        """

        dup_eye_cover_mesh = cmds.duplicate(input_eye_cover_mesh)[0]
        self.__unlock_transform(dup_eye_cover_mesh)
        parent = cmds.listRelatives(dup_eye_cover_mesh, p=True)

        cover_obj_list = []
        # 目隠しメッシュは両側の場合ポリシェルが2つ、片側の場合1つのはずなのでpolySeparate出来るかで判別
        try:
            parent = cmds.listRelatives(dup_eye_cover_mesh, p=True)

            # 両側あれば左右のシェルが分割されて、2オブジェクトとノードになるはず
            objs_and_node = cmds.polySeparate(dup_eye_cover_mesh)
            cover_obj_list = objs_and_node[:-1]
            cmds.delete(cover_obj_list, ch=True)

            # dup_eye_cover_mesh下に階層が掘られるので、外に出して不要なトランスフォームを削除
            if parent is not None:
                cover_obj_list = cmds.parent(cover_obj_list, parent)
            else:
                cover_obj_list = cmds.parent(cover_obj_list, w=True)
            cmds.delete(dup_eye_cover_mesh)

        except Exception:
            # 片側の場合polySeparateでエラーになるので、反対側をコピーで作成する
            mirror_obj = cmds.duplicate(dup_eye_cover_mesh)[0]
            cmds.scale(-1, 1, 1, mirror_obj, p=[0, 0, 0], r=True)
            cmds.delete([dup_eye_cover_mesh, mirror_obj], ch=True)
            cover_obj_list = [dup_eye_cover_mesh, mirror_obj]

        # バウンディングボックスのX座標最低値を比較して左、右の順でフルパスを返す
        if cmds.xform(cover_obj_list[0], q=True, bb=True, ws=True)[0] > cmds.xform(cover_obj_list[1], q=True, bb=True, ws=True)[0]:
            return cmds.ls(cover_obj_list[0], l=True)[0], cmds.ls(cover_obj_list[1], l=True)[0]
        else:
            return cmds.ls(cover_obj_list[1], l=True)[0], cmds.ls(cover_obj_list[0], l=True)[0]

    # ===============================================
    def __translate_around_node(self, target, pivot_node, translate, rotate):
        """別オブジェクトをピボットとして移動させる

        Args:
            target: 対象のオブジェクト
            pivot_node: ピボットとするオブジェクト
            translate ([float, float, float]): 移動
            rotate([float, float, float]): 回転
        """

        if not cmds.objExists(target) or not cmds.objExists(pivot_node):
            return

        pivot_pos = cmds.xform(pivot_node, q=True, t=True, ws=True)

        cmds.rotate(rotate[0], rotate[1], rotate[2], target, p=pivot_pos, ws=True, r=True)

        cmds.delete(target, ch=True)

        cmds.xform(target, r=True, t=translate)

        cmds.delete(target, ch=True)

    # ===============================================
    def _rebind_skin(self, target_transform):
        """メッシュのリバインド

        Args:
            target_transform: 対象のオブジェクト
        """

        skin_root_joint = \
            base_utility.mesh.skin.get_skin_root_joint(target_transform)

        if skin_root_joint is None:
            return

        skin_joint_list = [skin_root_joint]

        child_joint_list = cmds.listRelatives(skin_root_joint, ad=True, fullPath=True, type='joint')

        if child_joint_list:
            skin_joint_list.extend(child_joint_list)

        skin_info = base_class.mesh.skin_info.SkinInfo()
        skin_info.create_info([target_transform])

        cmds.delete(target_transform, ch=True)

        cmds.skinCluster(target_transform,
                         skin_joint_list,
                         obeyMaxInfluences=False,
                         bindMethod=0,
                         maximumInfluences=2,
                         removeUnusedInfluence=False,
                         skinMethod=0)

        target_skin_info = base_class.mesh.skin_info.SkinInfo()
        target_skin_info.create_info([target_transform])

        base_utility.mesh.skin.paste_weight_by_vertex_index(skin_info, target_skin_info)

        # 複数バインドポーズがある場合は削除して初期化
        bind_pose_list = cmds.dagPose(skin_root_joint, q=True, bp=True)

        if len(bind_pose_list) > 1:

            cmds.delete(bind_pose_list)
            cmds.dagPose(skin_root_joint, bp=True, save=True)

    # ===============================================
    def __unlock_transform(self, target_transform):
        """必要なアトリビュートのロックを解除する

        Args:
            target_transform: 対象のオブジェクト
        """

        attr_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']

        for attr in attr_list:
            cmds.setAttr('{}.{}'.format(target_transform, attr), lock=False)
