# -*- coding: utf-8 -*-
import math
import functools
import typing as tp

from decimal import Decimal, ROUND_DOWN

from ..task import CheckTaskBase
from ..scene_data import MayaSceneDataBase
from ..data import ErrorType

import maya.cmds as cmds
from .. import utility as util


class BoundJoint(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "バインド確認"

    def exec_task_method(self):
        current_func = functools.partial(self.check_not_bound_object)
        self.register_error_info_to_mesh_descendants(
            current_func, "not_bound_object", "バインドされていないオブジェクト"
        )

    def check_not_bound_object(self, obejcts: tp.List[str]) -> tp.List[str]:
        """バインドされていないオブジェクトを返す

        Args:
            obejcts (tp.List[str]): 対象のオブジェクト

        Returns:
            tp.List[str]: バインドされていないオブジェクト
        """
        not_bound_objects = []
        for object in obejcts:
            joints = util.get_bound_joints(object)
            if len(joints) == 0:
                not_bound_objects.append(object)

        return not_bound_objects


# TODO:Extradataで指定可能にする 決め打ち、第2位
class WeightValue(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ウェイト値"

    def exec_task_method(self):
        current_func = functools.partial(self.check_weight_value)
        self.register_error_info_to_mesh_descendants(
            current_func, "weight_value", "不正なウエイト値の頂点"
        )

    def check_weight_value(self, obejcts: tp.List[str]) -> tp.List[str]:
        """バインドされていないオブジェクトを返す

        Args:
            obejcts (tp.List[str]): 対象のオブジェクト

        Returns:
            tp.List[str]: バインドされていないオブジェクト
        """
        invalid_value_object = []
        for object in obejcts:
            weights = self.get_vertex_skin_weights(object)
            for vertex_name in weights:
                for value in weights[vertex_name]:
                    if self.exist_round_weight(value, 2):
                        invalid_value_object.append(vertex_name)
        return list(set(invalid_value_object))

    @staticmethod
    def exist_round_weight(value: float, n: int):
        """cy weight wditorに合わせたウエイトの桁数チェック

        Args:
            value (float): チェック対象の値
            n (int): 桁数

        Returns:
            bool: 対象の値が任意の範囲に入っているかどうか
        """
        temp_full_value = value * pow(10, n)
        temp_value = math.modf(temp_full_value)
        if temp_value[0] < 0.01 or temp_value[0] > 0.99:
            return False
        return True

    @staticmethod
    def get_vertex_skin_weights(obj: str) -> tp.Dict[str, tp.List[float]]:
        """対象のオブジェクトの全ての頂点のスキンウエイト値を取得する関数

        Args:
            obj (str): オブジェクト名

        Returns:
            tp.Dict[str, tp.List[float]]: 頂点インデックスをキーとし、ウェイト値のリストを値とする辞書
        """
        skin_clusters = cmds.ls(cmds.listHistory(obj), type="skinCluster")
        vertex_weights = {}
        if skin_clusters:
            skin_cluster = skin_clusters[0]  # 最初のスキンクラスタを取得
            num_vertices = cmds.polyEvaluate(obj, vertex=True)

            for i in range(num_vertices):
                vertex_name = f"{obj}.vtx[{i}]"
                weights = cmds.skinPercent(
                    skin_cluster, vertex_name, query=True, value=True
                )
                vertex_weights[vertex_name] = weights
        return vertex_weights

    class MinInfluence(CheckTaskBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.checker_info.label_name = "インフルエンス数"
            if self.extra_data == None:
                raise ValueError(f"{self.checker_info.label_name}:にはextradataが必要です")

            self.min_influence = self.extra_data["min_influence"]

        def exec_task_method(self):
            current_func = functools.partial(
                self.get_influenced_objects, min_influence=self.min_influence
            )
            self.register_error_info_to_mesh_descendants(
                current_func, "min_influence", f"インフルエンス数が{self.min_influence-1}以上"
            )

        def get_influenced_objects(
            self, obj_list: tp.List[str], min_influence: int = 5
        ) -> tp.List[str]:
            """対象のオブジェクトの頂点で、インフルエンスが指定された数以上の頂点を持つオブジェクトをすべて返す関数

            Args:
                obj_list (tp.List[str]): オブジェクト名のリスト
                min_influence (int): 最小インフルエンス数

            Returns:
                tp.List[str]: インフルエンスが指定された数以上の頂点を持つオブジェクト名のリスト
            """
            objects_with_high_influence = []
            for obj in obj_list:
                num_vertices = cmds.polyEvaluate(obj, vertex=True)
                for i in range(num_vertices):
                    vertex_name = f"{obj}.vtx[{i}]"
                    if self.get_vertex_with_influence_greater_than(
                        vertex_name, min_influence
                    ):
                        objects_with_high_influence.append(vertex_name)
            return objects_with_high_influence

        @staticmethod
        def get_vertex_with_influence_greater_than(
            vertex: str, min_influence: int = 5
        ) -> tp.Optional[str]:
            """与えた頂点のインフルエンス数が指定された数以上だった場合その頂点を返す関数

            Args:
                vertex (str): 頂点名
                min_influence (int): 最小インフルエンス数

            Returns:
                tp.Optional[str]: インフルエンス数が指定された数以上の頂点名 (該当しない場合はNone)
            """
            obj = vertex.split(".")[0]
            skin_clusters = cmds.ls(cmds.listHistory(obj), type="skinCluster")
            if skin_clusters:
                skin_cluster = skin_clusters[0]
                weights = cmds.skinPercent(skin_cluster, vertex, query=True, value=True)
                non_zero_weights = [w for w in weights if w > 0]
                if len(non_zero_weights) >= min_influence:
                    return vertex
            return None

    class NoWeightJoint(CheckTaskBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.checker_info.label_name = "不要なウェイト"

            if self.extra_data == None:
                raise ValueError(f"{self.checker_info.label_name}:にはextradataが必要です")

            self.joint_names = self.extra_data["joint_names"]

        def exec_task_method(self):
            joint_info = self._are_weights_assigned_to_joints(self.joint_names)

            # ウエイトが振られている骨を配列に入れる
            error_joints = []
            for joint_name in joint_info:
                is_weighed = joint_info[joint_name]
                if is_weighed:
                    error_joints.append(joint_name)

            if len(error_joints) > 0:
                self.set_error_data(
                    "no_weight_joint",
                    error_joints,
                    "ウエイトが存在してしまっているjoint",
                )
            else:
                self.set_error_type(ErrorType.NOERROR)

        def exec_fix_method(self):
            self.remove_joint_from_influenced_meshes(self.joint_names)

        @staticmethod
        def remove_joint_from_influenced_meshes(joint_names):
            """
            Removes the specified joints from the influences of all the meshes it affects.
            Args:
                joint_names: list of joint names to be removed
            Returns:
                None
            """
            for joint_name in joint_names:
                # Retrieve skinClusters influenced by the joint
                skin_clusters = cmds.skinCluster(joint_name, query=True, influence=True)
                # For each skinCluster, retrieve the geometry name and remove joint influence
                for skin_cluster in skin_clusters:
                    # Retrieve the name of the geometry the skinCluster affects
                    geometry_name = cmds.skinCluster(
                        skin_cluster, query=True, geometry=True
                    )[0]
                    if joint_name in cmds.skinCluster(
                        skin_cluster, query=True, influence=True
                    ):
                        cmds.skinCluster(
                            geometry_name, edit=True, removeInfluence=joint_name
                        )
                        print(f"Removed {joint_name} from {geometry_name}")

        @staticmethod
        def _are_weights_assigned_to_joints(
            joint_list: tp.List[str],
        ) -> tp.Dict[str, bool]:
            """対象のジョイントにウェイトが振られているかどうかを確認する関数

            Args:
                joint_list (tp.List[str]): ウェイト確認対象のジョイント名のリスト

            Returns:
                tp.Dict[str, bool]: ジョイント名とウェイトが振られているかどうかの辞書
            """
            weight_info = {}
            for joint in joint_list:
                if not cmds.objExists(joint):
                    cmds.warning(f"{joint} is not exists.")
                    continue

                skin_cluster_list = cmds.listConnections(joint, type="skinCluster")
                if not skin_cluster_list:
                    weight_info[joint] = False
                    continue
                skin_cluster = skin_cluster_list[0]
                geometry = cmds.skinCluster(skin_cluster, query=True, geometry=True)[0]
                vtx_count = cmds.polyEvaluate(geometry, vertex=True)
                has_weight = False
                for vtx_index in range(vtx_count):
                    vtx_weight = cmds.skinPercent(
                        skin_cluster,
                        f"{geometry}.vtx[{vtx_index}]",
                        query=True,
                        transform=joint,
                        value=True,
                    )
                    if vtx_weight > 0:
                        has_weight = True
                        break
                weight_info[joint] = has_weight
            return weight_info
