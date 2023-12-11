# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds
import maya.mel as mel

from ..base_common.utility.mesh import skin
from ..base_common.classes.mesh import skin_info
from ..glp_chara_utility.classes.bind_rebind_skin import bind_rebind_skin

# Maya 2022-
try:
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(skin)
reload(skin_info)
reload(bind_rebind_skin)


class BindMeshEdit(object):

    def devide_skinned_mesh(self):
        """選択したメッシュのフェースをスキニングを維持したまま分割する
        """

        sels = cmds.ls(sl=True, fl=True)
        objs = list(set([sel.split('.')[0] for sel in sels]))

        is_devided = False
        for obj in objs:

            target_face_list = [sel for sel in sels if sel.startswith(obj) and sel.find('.f[') >= 0]
            if not target_face_list:
                continue

            cmds.select(obj)
            mel.eval('gotoBindPose;')
            cmds.select(cl=True)

            obj_face_list = cmds.ls(cmds.polyListComponentConversion(obj, tf=True), fl=True)

            # 選択したフェース以外のオブジェクト全体のフェースリスト（反転選択フェース）
            removed_selected_face_list = [face for face in obj_face_list if face not in target_face_list]

            self.__create_divide_skinned_mesh(obj, removed_selected_face_list)
            self.__create_divide_skinned_mesh(obj, target_face_list)

            is_devided = True

        return is_devided

    def merge_skinned_meshes(self):
        """選択したメッシュ同士をスキニング及びウェイトを維持したまま結合する
        同座標頂点はマージ等は行われない
        """

        sels = cmds.ls(sl=True)
        if not sels:
            return False

        for sel in sels:
            # skinClusterがないメッシュが含まれているとエラーになる
            if not skin.get_skin_cluster(sel):
                return False

        dup_target_mesh_list = []
        for sel in sels:

            cmds.select(sel)
            mel.eval('gotoBindPose;')
            cmds.select(cl=True)

            duplicate_mesh = cmds.duplicate(sel)[0]
            dup_target_mesh_list.append(duplicate_mesh)

        # オブジェクトを結合
        unite_obj = cmds.polyUnite(dup_target_mesh_list)[0]
        # オブジェクトを複製してヒストリ削除
        duplicate_obj = cmds.duplicate(unite_obj)[0]
        # 結合した最初のオブジェクト削除
        cmds.delete(unite_obj)
        # 複製したオブジェクトも削除
        cmds.delete(dup_target_mesh_list)
        # 名前を「元メッシュ名 + _mergedMesh」に変更
        duplicate_obj = cmds.rename(duplicate_obj, '{}_MargedMesh'.format(sels[0].split('|')[-1]))
        # 階層も元の物と同じ所に
        tmp_parent = cmds.listRelatives(sel, parent=True, f=True)
        if tmp_parent is not None:
            cmds.parent(duplicate_obj, tmp_parent[0])

        # メッシュをバインド
        self.__bind_skin_from_base_mesh_joint(sels, duplicate_obj)
        # 選択した元オブジェクトのweightをそれぞれ位置でペースト
        for sel in sels:
            self.__paste_weight_by_vertex_position(sel, duplicate_obj)

        return True

    def __create_divide_skinned_mesh(self, base_skinned_mesh, remove_face_list):
        """スキニング済みのメッシュから指定されたフェースを取り除いたスキニングメッシュを作成する

        Args:
            base_skinned_mesh (str): ベースとなるスキニングメッシュ
            remove_face_list (list): ベーススキニングメッシュから取り除くフェースの一覧
        """

        duplicate_mesh = cmds.duplicate(base_skinned_mesh)[0]
        dup_delete_face_list = [f.replace(base_skinned_mesh, duplicate_mesh) for f in remove_face_list]
        cmds.delete(dup_delete_face_list)

        # オブジェクトにスキンクラスターが無ければ以下の対応はしない
        if not skin.get_skin_cluster(base_skinned_mesh):
            return

        self.__bind_skin_from_base_mesh_joint([base_skinned_mesh], duplicate_mesh)
        self.__paste_weight_by_vertex_position(base_skinned_mesh, duplicate_mesh)

    def __bind_skin_from_base_mesh_joint(self, base_mesh_list, target_mesh):
        """対象のメッシュを元となるメッシュのスキニング対象ジョイントを利用してバインド

        Args:
            base_mesh_list (list): スキニング対象ジョイントを取得する元のメッシュ
            target_mesh (str): バインドする対象のメッシュ
        """

        skin_joint_list = []
        for base_mesh in base_mesh_list:
            skin_joint_list.extend(skin.get_skin_joint_list(base_mesh))

        skin_joint_list = list(set(skin_joint_list))

        bind_skin = bind_rebind_skin.BindSkin()
        bind_skin.set_transform_list([target_mesh])
        bind_skin.set_joint_list(skin_joint_list, False)
        bind_skin.exec_bind()

    def __paste_weight_by_vertex_position(self, base_mesh, target_mesh):
        """対象のメッシュに元メッシュのウェイト情報を頂点位置で設定

        Args:
            base_mesh (str): ウェイト情報を取得する元メッシュ
            target_mesh (str): ウェイト情報を設定する対象メッシュ
        """

        # weight情報を取得
        org_skin_info = skin_info.SkinInfo()
        org_skin_info.create_info([base_mesh])
        tgt_skin_info = skin_info.SkinInfo()
        tgt_skin_info.create_info([target_mesh])

        # 頂点位置でウェイトをペースト
        skin.paste_weight_by_vertex_position(org_skin_info, tgt_skin_info)
