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
import re

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
            index = self.get_influence_index_by_name(inf.name)
            index_list.append(index)

        return index_list

    def create_mirror_influence_map(self, influences_data, mirror_setting):
        """ミラーリングを実施しながらinfluenceの名前のリストからindexのリストを作成する

        Args:
            influences_data (list(str)): indexを検索したいジョイントの名前のリスト
            mirror_setting (dict): ミラーリングの設定

        Returns:
            list(int): indexのリスト
        """
        index_list = []
        for inf_data in influences_data:
            is_match = False
            org_joint_name = inf_data.name

            # リネームをしてマッチするものがないか探す
            for match_setting in mirror_setting['mirror_pattern']:
                renamed_joint_name = re.sub(match_setting[0], match_setting[1], org_joint_name, 1)
                if org_joint_name == renamed_joint_name:
                    continue
                index = self.get_influence_index_by_name(renamed_joint_name)
                if index == -1:
                    continue
                fixed_vector = self.jointdatas[index].vector_from_root
                fixed_vector.x *= mirror_setting['coffient'][0]
                fixed_vector.y *= mirror_setting['coffient'][1]
                fixed_vector.z *= mirror_setting['coffient'][2]

                # positionが指定範囲内なら成立
                if (fixed_vector - inf_data.vector_from_root).length() <= mirror_setting['allow_distance']:
                    index_list.append(index)
                    is_match = True
                    break

            # Mirrorで条件マッチしない場合
            if not is_match:
                index_list.append(self.get_influence_index_by_name(org_joint_name))

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

    def get_influence_index_by_name(self, name):
        """influenceのindex番号をショートネームでマッチして取得する

        Args:
            name (str): 探したいinfluenceの名前

        Returns:
            int : index番号.該当するものが見つからなかった場合は-1.
        """
        result = -1
        for index, jnt in enumerate(self.jointdatas):
            if utility.get_namespace_removed_shortname(name) == utility.get_namespace_removed_shortname(jnt.name):
                result = index
                break
        return result


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
