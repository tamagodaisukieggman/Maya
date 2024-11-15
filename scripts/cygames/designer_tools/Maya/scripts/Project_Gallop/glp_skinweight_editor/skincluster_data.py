# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import maya.api.OpenMaya as om

from . import joint, utility
reload(joint)
reload(utility)


class SkinClusterData(object):
    def __init__(self):
        self.jointdatas = []
        self.weights = []

    def create_influence_map(self, influences):
        """influenceの名前のリストからindexのリストを作成する

        Args:
            influences (list(str)): indexを検索したいジョイントの名前のリスト

        Returns:
            list(int): indexのリスト
        """
        index_list = []
        for inf in influences:
            index = self.get_influence_index(inf.full_path)
            index_list.append(index)

        return index_list

    def create_mirror_influence_map(self, influences_data, mirror_setting):
        """ミラーリングを実施しながらinfluenceの名前のリストからindexのリストを作成する
        ミラーしたインフルエンスが見つからなかったらスキップしたいので-1(無効なインデックス)を返す

        Args:
            influences_data (list(str)): indexを検索したいジョイントの名前のリスト
            mirror_setting (dict): ミラーリングの設定

        Returns:
            list(int): indexのリスト
        """
        index_list = []
        for inf_data in influences_data:

            # リネームをしてマッチするものがないか探す
            org_joint_full_path = inf_data.full_path
            mirror_joint_full_path = utility.get_mirror_name(org_joint_full_path, mirror_setting['mirror_pattern'])

            # 名前がミラーマッチのパターンを含んでいない
            if org_joint_full_path == mirror_joint_full_path:
                index_list.append(-1)
                continue

            # ミラーした名前のインフルエンスが見つからない
            index = self.get_influence_index(mirror_joint_full_path)
            if index == -1:
                index_list.append(-1)
                continue

            # positionが指定範囲内なら成立
            fixed_vector = self.jointdatas[index].vector_from_root
            fixed_vector.x *= mirror_setting['coffient'][0]
            fixed_vector.y *= mirror_setting['coffient'][1]
            fixed_vector.z *= mirror_setting['coffient'][2]

            if (fixed_vector - inf_data.vector_from_root).length() <= mirror_setting['allow_distance']:
                index_list.append(index)
            else:
                index_list.append(-1)

        return index_list

    def get_weights(self, index):
        """指定したIndexのweight情報を取得します

        Args:
            index (int): 取得したい頂点のweight情報

        Returns:
            list(float): 当該頂点のウェイトのリスト
        """
        inf_count = len(self.jointdatas)

        this_index_weights = []
        for inf_index in range(inf_count):
            current_val = self.weights[inf_count * index + inf_index]
            this_index_weights.append(current_val)

        return this_index_weights

    def set_weights(self, index, indexed_weights):
        """weightを指定の値で更新する

        Args:
            index (int): vtxのindex
            indexed_weights (list(list(int), list(float))): infのindexとfloatが格納されたlist
        """
        inf_count = len(self.jointdatas)

        for inf_index, weight in indexed_weights:
            self.weights[inf_count * index + inf_index] = weight

    def get_influence_index(self, src_inf_full_path):
        """ソースのinfluenceに対応する自身のinfluenceのindex番号を取得

        Args:
            src_inf_full_path (str): ソースのinfluenceのフルパス

        Returns:
            int : index番号.該当するものが見つからなかった場合は-1.
        """

        # まずショートネームで検索
        result_idxs = []
        for idx, jnt in enumerate(self.jointdatas):
            if utility.get_namespace_removed_shortname(src_inf_full_path) == utility.get_namespace_removed_shortname(jnt.name):
                result_idxs.append(idx)

        # 該当のショートネームなし
        if len(result_idxs) < 1:
            return -1

        # 検索結果が１件なら確定
        if len(result_idxs) == 1:
            return result_idxs[0]

        # 複数件ヒットした場合は最も類似性の高いジョイントを選ぶ
        best_match_idx = -1
        best_match_length = 0
        ctrl_joint_name = utility.get_namespace_removed_name(src_inf_full_path)

        for idx in result_idxs:
            joint_name = utility.get_namespace_removed_name(self.jointdatas[idx].full_path)

            rev_ctrl_names = reversed(ctrl_joint_name.split('|'))
            rev_names = reversed(joint_name.split('|'))

            match_length = 0
            for rev_ctrl_name, rev_name in zip(rev_ctrl_names, rev_names):
                if rev_ctrl_name == rev_name:
                    match_length += 1
                else:
                    break

            if match_length > best_match_length:
                best_match_length = match_length
                best_match_idx = idx

        return best_match_idx


def get_skinweight_data(mfn_skincluster, transform, om_pos_mode):
    """SkinClusterDataを与えられたパラメータをもとに作成する

    Args:
        mfn_skincluster (om.MFnSKinCluster): 対象のスキンクラスター
        transform (str): 対象とするトランスフォームの名前
        om_pos_mode (om.MSpace): どこを基準にJointの位置情報を設定するか
    """
    current_skinclusterdata = SkinClusterData()

    pos_mode = 'root'
    if om_pos_mode == om.MSpace.kWorld:
        pos_mode = 'world'
    current_skinclusterdata.jointdatas = joint.get_jointdatas(mfn_skincluster, pos_mode)

    sel = om.MSelectionList()
    sel.add(transform)
    geo_dag_path = sel.getDagPath(0)
    current_skinclusterdata.weights, _ = mfn_skincluster.getWeights(geo_dag_path, om.MObject())

    return current_skinclusterdata
