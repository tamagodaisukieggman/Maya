# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

from __future__ import print_function
from __future__ import unicode_literals

try:
    # Maya 2022-
    from importlib import reload
    from builtins import zip
    from builtins import object
except Exception:
    pass

import os

import maya.cmds as cmds
from maya.api import OpenMaya as om2

from ..glp_common.classes import normal_info
from . import utility

reload(normal_info)

normal_plugin_name = 'normal_command.py'
normal_plugin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), normal_plugin_name)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CopyNormal(object):

    # ==================================================
    def __init__(self):

        self.src_normal_info = None

    # ==================================================
    def apply_normal(self, obj_info, keep_soft_edge):
        """
        法線情報をオブジェクトに適用
        """

        if not cmds.pluginInfo(normal_plugin_path, q=True, loaded=True):
            cmds.loadPlugin(normal_plugin_path)

        target, vertex_ids, face_ids, normals = obj_info.get_command_arguments()

        cmds.setNormal(target, vi=vertex_ids, fi=face_ids, n=normals, ks=keep_soft_edge)

    # ==================================================
    def copy_normal(self, src_target_list):
        """
        法線情報をコピー
        """

        if src_target_list.isEmpty():
            cmds.warning('頂点を選択してからコピーしてください')
            return

        self.src_normal_info = None
        self.src_normal_info = normal_info.NormalInfo()
        self.src_normal_info.create_info(src_target_list, False)

        om2.MGlobal.displayInfo('法線をコピーしました')

    # ==================================================
    def paste_normal_by_list_order(self, dst_target_list, is_locked_vtx_only, keep_soft_edge):
        """
        法線を「選択順でペースト」 (base_commonのnormal.pyから引っ越し)
        target_vertex_listの順番でペースト
        Args:
            dst_target_list (list<str>): ペースト先の頂点リスト
            is_locked_vtx_only (bool): ロック法線のみペースト対象
            keep_soft_edge (bool): ペースト先のエッジ状態を維持
        """

        if dst_target_list.isEmpty():
            cmds.warning('コピー先の頂点情報がありません')
            return

        if not self.src_normal_info:
            cmds.warning('コピー元の頂点情報がありません')
            return

        # ペースト先のinfoを作成
        dst_normal_info = normal_info.NormalInfo()
        dst_normal_info.create_info(dst_target_list, False)

        # コピー元とペースト先の選択頂点数が1個の時は選択順は関係ないのでTrack Selection Order設定は気にしない
        if len(self.src_normal_info.info_list[0].info_list) != 1 or len(dst_normal_info.info_list[0].info_list) != 1:
            if cmds.selectPref(q=True, trackSelectionOrder=True) is False:
                user_choice = cmds.confirmDialog(title='Confirm',
                                                 message='「選択順でペースト」を利用するにはPreferencesでSelect > ' +
                                                 'Track Selection Order（選択した順番を保持）をONにしておく必要があります。\n' +
                                                 'ONにしますか?',
                                                 button=['Yes', 'Cancel'], defaultButton='Cancel',
                                                 cancelButton='Cancel', dismissString='Cancel')
                if user_choice == 'Yes':
                    cmds.selectPref(trackSelectionOrder=True)
                    cmds.confirmDialog(title='Confirm',
                                       message='Mayaの「Track Selection Order」の設定をONにしました。\n' +
                                       'もう一度順番に選択してコピーをしてから実行してください。')
                    # 選択状態が残っているとユーザーがそのままコピー&ペーストするといけないので解除
                    cmds.select(self.src_normal_info.info_list[0].dag_path)
                    cmds.selectMode(component=True)
                    cmds.select(clear=True)
                    cmds.select(dst_normal_info.info_list[0].dag_path)
                    cmds.selectMode(component=True)
                    cmds.select(clear=True)
                    return
                else:
                    return

        info_item_pair_list = dst_normal_info.get_pair_list_by_name(self.src_normal_info)

        if not info_item_pair_list:
            cmds.warning('法線のペアリストの作成に失敗しました')
            return

        cmds.undoInfo(openChunk=True)

        for src_obj_info, dst_obj_info in info_item_pair_list:

            src_info_list = src_obj_info.info_list
            dst_info_list = dst_obj_info.info_list

            # 実際にコピーを行わないペアをコピー前にDROPする
            if is_locked_vtx_only:
                src_info_list, dst_info_list = self.drop_unlocked_pair(src_info_list, dst_info_list)

            obj_info = dst_obj_info.copy(dst_info_list)
            obj_info.update(src_info_list)

            self.apply_normal(obj_info, keep_soft_edge)

        cmds.undoInfo(closeChunk=True)

    # ==================================================
    def paste_normal_by_vertex_index(self, dst_target_list, is_locked_vtx_only, keep_soft_edge):
        """
        法線情報のペースト「頂点インデックスでペースト」 (base_commonのnormal.pyから引っ越し)
        Args:
            dst_target_list (list<str>): ペースト先の頂点リスト
            is_locked_vtx_only (bool): ロック法線のみペースト対象
            keep_soft_edge (bool): ペースト先のエッジ状態を維持
        """

        if dst_target_list.isEmpty():
            cmds.warning('コピー先の頂点情報がありません')
            return

        if not self.src_normal_info:
            cmds.warning('コピー元の頂点情報がありません')
            return

        # ペースト先のinfoを作成
        dst_normal_info = normal_info.NormalInfo()
        dst_normal_info.create_info(dst_target_list, False)

        info_item_pair_list = dst_normal_info.get_pair_list_by_name(self.src_normal_info)

        if not info_item_pair_list:
            cmds.warning('法線のペアリストの作成に失敗しました')
            return

        cmds.undoInfo(openChunk=True)

        for src_obj_info, dst_obj_info in info_item_pair_list:

            info_pair_list = utility.get_info_pair_list_by_index(
                src_obj_info.info_list, dst_obj_info.info_list)

            if not info_pair_list:
                cmds.warning('頂点番号が同じでないと動作しません')
                continue

            src_info_list, dst_info_list = info_pair_list

            # 実際にコピーを行わないペアをコピー前にDROPする
            if is_locked_vtx_only:
                src_info_list, dst_info_list = self.drop_unlocked_pair(src_info_list, dst_info_list)

            obj_info = dst_obj_info.copy(dst_info_list)
            obj_info.update(src_info_list)

            self.apply_normal(obj_info, keep_soft_edge)

        cmds.undoInfo(closeChunk=True)

    # ==================================================
    def paste_normal_by_vertex_position(self, dst_target_list, is_locked_vtx_only, keep_soft_edge, is_world_space, mirror_index, mirror_normal):
        """
        法線情報のペースト「頂点位置でペースト」 (base_commonのnormal.pyから引っ越し)
        Memo: MayaのMesh > Transfer Attributes のVertex Normalに挙動が似ているので、
        必要であればcmds.transferAttributesに置き換えることもできそう。
        Args:
            dst_target_list (list<str>): ペースト先の頂点リスト
            is_locked_vtx_only (bool): ロック法線のみペースト対象
            keep_soft_edge (bool): ペースト先のエッジ状態を維持
            is_world_space (bool): ペースト位置の座標空間 TrueならWorld Space、FalseならLocal Space
            mirror_option (None or int): ミラーした位置の頂点に対してペースト。 ミラーなし(None)、Xミラー(0)、Yミラー(1)、Zミラー(2)。
            mirror_normal (bool): ペースト時に法線を反転するか
        """

        if dst_target_list.isEmpty():
            cmds.warning('コピー先の頂点情報がありません')
            return

        if not self.src_normal_info:
            cmds.warning('コピー元の頂点情報がありません')
            return

        # ペースト先のinfoを作成
        dst_normal_info = normal_info.NormalInfo()
        dst_normal_info.create_info(dst_target_list, False)

        info_item_pair_list = dst_normal_info.get_pair_list_by_name(self.src_normal_info)

        if not info_item_pair_list:
            cmds.warning('法線のペアリストの作成に失敗しました')
            return

        cmds.undoInfo(openChunk=True)

        for src_obj_info, dst_obj_info in info_item_pair_list:

            info_pair_list = utility.get_info_pair_list_by_position(
                src_obj_info.info_list, dst_obj_info.info_list, is_world_space, mirror_index, mirror_normal)

            if not info_pair_list:
                continue

            src_info_list, dst_info_list = info_pair_list

            # 実際にコピーを行わないペアをコピー前にDROPする
            if is_locked_vtx_only:
                src_info_list, dst_info_list = self.drop_unlocked_pair(src_info_list, dst_info_list)

            obj_info = dst_obj_info.copy(dst_info_list)
            obj_info.update(src_info_list)

            self.apply_normal(obj_info, keep_soft_edge)

        cmds.undoInfo(closeChunk=True)

    # ==================================================
    def drop_unlocked_pair(self, src_info_list, dst_info_list):
        """src側がlockされていないペアをDROPする

        Args:
            src_info_list ([VertexNormalInfo]): コピー元のVertexNormalInfo
            dst_info_list ([VertexNormalInfo]): コピー先のVertexNormalInfo

        Return:
            (VertexNormalInfo, VertexNormalInfo): src側がlockされていないものをDROPしたリスト
        """
        filtered_src_info_list = []
        filtered_dst_info_list = []

        for i, src_info in enumerate(src_info_list):
            if src_info.is_locked:
                filtered_src_info_list.append(src_info)
                filtered_dst_info_list.append(dst_info_list[i])

        return filtered_src_info_list, filtered_dst_info_list
