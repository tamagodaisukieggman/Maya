# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.api.OpenMaya as om


class JointData(object):
    """ジョイント情報を保持するクラス
    """

    def __init__(self):

        # 基礎情報
        self.name = ''
        self.full_path = ''
        self.vector_from_root = None


def get_jointdatas(mfn_skincluster, pos_mode):
    """当該スキンクラスターのインフルエンスのJointDataのListを作成

    Args:
        mfn_skincluster (om.MFnSkinCluster): 対象となるスキンクラスター
        pos_mode (str): どの座標系でデータを取得するか

    Returns:
        list(JointData): インフルエンスのJointDataのList
    """

    influence_objects_dag = [om.MFnDagNode(joint) for joint in mfn_skincluster.influenceObjects()]

    root_joint_dag = None
    min_count = 999999
    for inf_dag in influence_objects_dag:
        current_depth = inf_dag.fullPathName().count('|')
        if min_count > current_depth:
            min_count = current_depth
            root_joint_dag = inf_dag

            if current_depth == 1:
                break

    root_mpoint = om.MPoint(om.MFnTransform(root_joint_dag.getPath()).translation(om.MSpace.kWorld))
    basis_matrix = calc_basis_matrix(root_joint_dag.getPath())

    result_joints = []
    for joint in mfn_skincluster.influenceObjects():
        joint_mfn_dag = om.MFnDagNode(joint)

        this_joint_data = JointData()
        this_joint_data.name = joint_mfn_dag.name()
        this_joint_data.full_path = joint_mfn_dag.fullPathName()
        jnt_mpoint = om.MPoint(om.MFnTransform(joint_mfn_dag.getPath()).translation(om.MSpace.kWorld))

        # vectorのroot
        this_joint_data.vector_from_root = om.MVector(jnt_mpoint - root_mpoint)
        if pos_mode == 'root':
            this_joint_data.vector_from_root = convert_vector_base_from_matrix(this_joint_data.vector_from_root, basis_matrix)

        result_joints.append(this_joint_data)

    return result_joints


def convert_vector_base_from_matrix(target_vector, base_matrix):
    """マトリックスの座標系にvectorを変換する

    Args:
        target_vector (om.MVector): 変換対象のvector
        base_matrix (om.MMatrix): 基底となるマトリックス(要正規化)

    Returns:
        om.MVector: Matrixの座標系に変換されたvector
    """
    transformed_vector = target_vector * base_matrix
    return transformed_vector


def calc_basis_matrix(dag_path):
    """dagPathのオブジェクト空間の基底となるマトリクスを計算

    Args:
        dag_path (om.MDagPath): オブジェクト空間をとりたいオブジェクト

    Returns:
        om.MMatrix: オブジェクト空間の基底となるmatrixを返す
    """
    transformation_matrix = dag_path.inclusiveMatrix()
    x_vector = om.MVector(transformation_matrix[0], transformation_matrix[1], transformation_matrix[2]).normalize()
    y_vector = om.MVector(transformation_matrix[4], transformation_matrix[5], transformation_matrix[6]).normalize()
    z_vector = om.MVector(transformation_matrix[8], transformation_matrix[9], transformation_matrix[10]).normalize()

    basis_matrix = om.MMatrix([x_vector[0], x_vector[1], x_vector[2], 0.0, y_vector[0], y_vector[1], y_vector[2], 0.0, z_vector[0], z_vector[1], z_vector[2], 0.0, 0.0, 0.0, 0.0, 1.0])

    return basis_matrix
