# -*- coding: utf-8 -*-
"""ウェイトの一時モデル退避機能など"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya import cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma


class WeightCopyModel(object):
    """ウェイト複製用のモデル
    オブジェクトを生成しながら、対象にウェイトをコピーする

    copy_skin_weightで通常のウェイトコピーも対応

    """
    DUPLICATE_SUFFIX = "_duplicate"

    def __init__(self, target_model):
        self.dist_model = target_model
        self.dist_model_skin_cluster = None

        self.src_object = None
        self.src_object_skin_cluster = None

        self.is_duplicate = False

    def get_skin_cluster(self, target_model):
        """スキンクラスタ―を取得する

        Args:
            target_model (str): 対象のメッシュ名

        Returns:
            str: スキンクラスタ―名
        """
        history_list = cmds.listHistory(target_model)
        for history in history_list:
            if cmds.objectType(history, isType='skinCluster'):
                return history
        return None

    def get_all_bone_from_skin_cluster(self, target_skin_cluster):
        """スキンクラスタ―からボーンリストを取得する

        Args:
            target_skin_cluster (str): 対象のスキンクラスター名

        Returns:
            list: スキンクラスターに割り当てられているBoneリスト
        """
        result = cmds.skinCluster(target_skin_cluster, query=True, influence=True)
        return result

    def get_root_bone_from_skin_cluster(self, target_skin_cluster):
        """スキンクラスタ―からルートボーンを取得する

        Args:
            target_skin_cluster (str): 対象のスキンクラスタ―

        Returns:
            str: ルートボーン
        """
        target_bone_list = self.get_all_bone_from_skin_cluster(target_skin_cluster)
        target_bone_fullpath_list = cmds.ls(target_bone_list, long=True)

        result = target_bone_fullpath_list[0].count("|")
        root_bone = cmds.ls(target_bone_fullpath_list[0])

        for bone_full_path in target_bone_fullpath_list:
            count = bone_full_path.count("|")
            if count < result:
                result = count
                root_bone = cmds.ls(bone_full_path)
        return root_bone

    def duplicate_model(self, target_model=None):
        """モデルを複製する

        Args:
            target_model (str, optional): 複製したいモデル名

        Returns:
            str: 複製したオブジェクト名
        """
        if target_model:
            duplicate_model = cmds.duplicate(target_model, name=target_model + self.DUPLICATE_SUFFIX)
        else:
            duplicate_model = cmds.duplicate(self.dist_model, name=self.dist_model + self.DUPLICATE_SUFFIX)

        return duplicate_model[0]

    def copy_skin_weight(self, dist_model=None, src_model=None):
        """ウェイトをコピーする

        Args:
            dist_model (str, optional): 転送元モデル名
            src_model (str, optional): 転送先モデル名
        """
        self.is_duplicate = False

        if dist_model is None:
            dist_model = self.dist_model

        self.dist_model_skin_cluster = self.get_skin_cluster(dist_model)

        if src_model is None:
            self.src_object = self.duplicate_model()
            src_model = self.src_object
            self.is_duplicate = True

        # 選択状態を記憶
        before_selection = cmds.ls(selection=True)

        root_bone = self.get_root_bone_from_skin_cluster(self.dist_model_skin_cluster)

        self.src_object_skin_cluster = self.get_skin_cluster(src_model)
        if not (self.src_object_skin_cluster):

            cmds.skinCluster(src_model, root_bone, obeyMaxInfluences=False, bindMethod=1, maximumInfluences=2)

            self.src_object_skin_cluster = self.get_skin_cluster(src_model)

        # ウェイト転写
        self._transfer_weights(dist_model, src_model)

        # 選択を戻す
        cmds.select(before_selection)

    def _transfer_weights(self, src, dst):
        """SourceのウェイトをDestinationに転送

        転送はインデックス順

        :param src: Source (Transformノード)
        :param dst: Destination (Transformノード)
        """
        # src -> dstのindexOfInfluenceの変換表
        src_to_dst_map = {}
        # dstのindexOfInfluenceとインデックス (リストの並び順) の対応表
        dst_map_by_vertex = {}

        # ソース取得
        src_weights, src_influences, src_infl_num, vertex_num = [], [], 0, 0

        selection = om.MGlobal.getSelectionListByName(src)
        iter_ = om.MItSelectionList(selection, om.MFn.kMesh)
        src_dagpath, src_comps = iter_.getComponent()
        dg_iter = om.MItDependencyGraph(
            src_dagpath.node(),
            om.MFn.kSkinClusterFilter,
            om.MItDependencyGraph.kUpstream,
        )
        while not dg_iter.isDone():
            skin_cluster_filter = dg_iter.currentNode()
            skin_fn = oma.MFnSkinCluster(skin_cluster_filter)
            src_influences = skin_fn.influenceObjects()
            src_weights, src_infl_num = skin_fn.getWeights(src_dagpath, src_comps)
            vertex_num = len(src_weights) / src_infl_num
            # print([skin_fn.indexForInfluenceObject(influence) for influence in src_influences])

            # 構造的にSkinClusterがひとつのはずなので1度処理したらbreak
            break
            # dg_iter.next()

        # デスティネーション取得
        dst_weights, dst_influences = [], []
        dst_skin_fn = None
        dst_infl_indices = []

        selection = om.MGlobal.getSelectionListByName(dst)
        iter_ = om.MItSelectionList(selection, om.MFn.kMesh)
        dst_dagpath, dst_comps = iter_.getComponent()
        dg_iter = om.MItDependencyGraph(
            dst_dagpath.node(),
            om.MFn.kSkinClusterFilter,
            om.MItDependencyGraph.kUpstream,
        )
        while not dg_iter.isDone():
            skin_cluster_filter = dg_iter.currentNode()
            dst_skin_fn = oma.MFnSkinCluster(skin_cluster_filter)
            dst_influences = dst_skin_fn.influenceObjects()
            dst_infl_indices = [dst_skin_fn.indexForInfluenceObject(influence) for influence in dst_influences]
            # print(dst_infl_indices)

            # 構造的にSkinClusterがひとつのはずなので1度処理したらbreak
            break
            # dg_iter.next()

        # dstのindexOfInfluenceとインデックス (リストの並び順) の対応表を作る
        for i, influence in enumerate(dst_influences):
            index_of_influence = dst_skin_fn.indexForInfluenceObject(influence)
            dst_map_by_vertex[index_of_influence] = i

        # ソース → デスティネーション変換
        uncontains = []
        for i, influence in enumerate(src_influences):
            if influence in dst_influences:
                src_to_dst_map[i] = dst_skin_fn.indexForInfluenceObject(influence)
            else:
                uncontains.append(influence.partialPathName())

        # デスティネーションに見つからないインフルエンスがある場合はエラー
        if uncontains:
            om.MGlobal.displayError('Uncontain influences: {}'.format(uncontains))
            return

        # ウェイト整形
        # 事前に0で初期化しておく
        dst_weights = om.MDoubleArray(vertex_num * len(dst_influences), 0.0)
        # ウェイトの並び順は各頂点ごとにインフルエンスの値が順番に並ぶ
        # (v[0]のinfluence[0]の値, v[0]のinfluence[1]の値, ..., v[n]のinfluence[0]の値, v[n]のinfluence[1]の値, ...)
        for i in range(int(vertex_num)):
            for j, influence in enumerate(src_influences):
                src_index = i * len(src_influences) + j
                dst_index = i * len(dst_influences) + dst_map_by_vertex[src_to_dst_map[j]]
                dst_weights[dst_index] = src_weights[src_index]

        # ウェイトセット
        dst_skin_fn.setWeights(
            dst_dagpath,
            dst_comps,
            om.MIntArray(dst_infl_indices),
            dst_weights
        )
