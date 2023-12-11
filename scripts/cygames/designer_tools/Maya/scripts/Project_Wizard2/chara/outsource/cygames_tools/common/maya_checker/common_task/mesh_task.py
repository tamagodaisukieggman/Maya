# -*- coding: utf-8 -*-
import functools
import os
import typing as tp
from collections import Counter

from ..task import CheckTaskBase
from ..scene_data import MayaSceneDataBase
from ..data import ErrorType

import maya.cmds as cmds
import maya.mel as mel

from .. import utility as util

# メッシュ系


class AllTransformDefault(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "メッシュのトランスフォーム値"

    def exec_task_method(self):
        transforms = []
        error_transforms = []
        for root in self.maya_scene_data.root_nodes:
            transforms.extend(root.get_all_mesh_transform())

        # 問題のあるtransformをerror_transformに入れる
        for transform in transforms:
            if self.is_transform_default(transform) is False:
                error_transforms.append(transform)

        # error_transformが1以上ならエラー
        if len(error_transforms) > 0:
            self.set_error_data(
                "all_transform_default", error_transforms, "メッシュのトランスフォーム値がデフォルト値ではない"
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def is_transform_default(self, mesh_name):
        """指定されたメッシュのトランスフォーム属性がデフォルト値になっているかどうかをチェックする。
        Args:
            mesh_name (str): チェックするメッシュの名前。
        Returns:
            bool: トランスフォーム属性がデフォルト値の場合はTrue、それ以外の場合はFalse。
        """
        if not cmds.objExists(mesh_name):
            raise ValueError(f"Mesh '{mesh_name}' does not exist.")

        translate = cmds.getAttr(mesh_name + ".translate")[0]
        rotate = cmds.getAttr(mesh_name + ".rotate")[0]
        scale = cmds.getAttr(mesh_name + ".scale")[0]

        default_translate = (0, 0, 0)
        default_rotate = (0, 0, 0)
        default_scale = (1, 1, 1)

        return (
            translate == default_translate
            and rotate == default_rotate
            and scale == default_scale
        )


class PolygonCount(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "メッシュのトランスフォーム値"

    def exec_task_method(self):
        ...


class MeshPivotAtOrigin(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "メッシュのピボットが原点にあるか"

    def exec_task_method(self):
        self.register_error_info_to_mesh_descendants(
            self.find_meshes_with_non_origin_pivot,
            "mesh_pivot_at_origin",
            "メッシュのピボットが原点にあるかどうか",
        )

    def exec_fix_method(self):
        error_objects = self.get_debug_target_objects("mesh_pivot_at_origin")
        MeshPivotAtOrigin.move_pivot_to_origin(error_objects)

    @staticmethod
    def move_pivot_to_origin(obj_names: tp.List[str]) -> None:
        """
        対象のオブジェクトのpivotを原点に移動する関数。
        Args:
            obj_names (List[str]): 対象のオブジェクト名のリスト
        Returns: なし
        """
        for obj_name in obj_names:
            # Pivotを原点に移動
            cmds.xform(obj_name, pivots=[0, 0, 0], ws=True)
            print(f"Moved pivot of {obj_name} to origin")

    def is_pivot_at_origin(self, mesh_name: str) -> bool:
        """指定されたメッシュのピボットが原点にあるかどうかをチェックする。
        Args:
            mesh_name (str): チェックするメッシュの名前。
        Returns:
            bool: ピボットが原点の場合はTrue、それ以外の場合はFalse。
        """
        pivot = cmds.xform(mesh_name, query=True, rotatePivot=True, worldSpace=True)
        default_pivot = [0.0, 0.0, 0.0]
        return pivot == default_pivot

    def find_meshes_with_non_origin_pivot(
        self, mesh_list: tp.List[str]
    ) -> tp.List[str]:
        """対象のメッシュ達の中でピボットが原点にないメッシュを配列で返す。
        Args:
            mesh_list (tp.List[str]): チェックするメッシュのリスト。
        Returns:
            tp.List[str]: ピボットが原点にないメッシュの配列。
        """
        non_origin_pivot_meshes = [
            mesh for mesh in mesh_list if not self.is_pivot_at_origin(mesh)
        ]
        return non_origin_pivot_meshes


class LengthZeroEdge(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "長さが０のエッジ確認"

    def exec_task_method(self):
        self.register_error_info_to_mesh_descendants(
            self._check_zero_edge, "length_zero_edge", "エッジの距離が0"
        )

    @staticmethod
    def _check_zero_edge(target_transform_list, cleanup=False):
        """
        ゼロエッジをチェック

        :param target_transform_list: トランスフォームリスト
        :param cleanup: クリーンアップをかけるかどうか
        """

        if not target_transform_list:
            return

        cmds.select(target_transform_list, r=True)

        mel_script = 'polyCleanupArgList 3 { "0","replace","1","0","0","0","0","0","0","1e-005","1","1e-005","0","1e-005","0","-1","0" }'

        if cleanup:
            mel_script = mel_script.replace("replace", "1")
        else:
            mel_script = mel_script.replace("replace", "2")

        result = mel.eval(mel_script)

        if not result:
            return

        result = cmds.ls(result, fl=True, l=True)

        return result


class FiveOrMoreSidedFace(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "５辺以上のフェース確認	"

    def exec_task_method(self):
        self.register_error_info_to_mesh_descendants(
            self._find_ngons_multiple, "five_or_more_sided_face", "５辺以上のフェース"
        )

    @staticmethod
    def _find_ngons_multiple(mesh_names: tp.List[str]) -> dict:
        """対象オブジェクトに含まれるすべての5角形以上のポリゴンを返す。
        Args:
            mesh_names (List[str]): チェックするメッシュの名前のリスト。
        Returns:
            dict: キーがメッシュ名、値が5角形以上のポリゴンのリストの辞書。
        """
        ngons_dict = {}
        for mesh_name in mesh_names:
            if not cmds.objExists(mesh_name):
                raise ValueError(f"Mesh '{mesh_name}' does not exist.")

            ngons = []
            polygons = cmds.ls(f"{mesh_name}.f[*]", flatten=True)
            for polygon in polygons:
                vertices = cmds.ls(
                    cmds.polyListComponentConversion(polygon, toVertex=True),
                    flatten=True,
                )
                if len(vertices) >= 5:
                    ngons.append(polygon)
            ngons_dict[mesh_name] = ngons
        return ngons_dict


class ConcaveFace(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "凹型フェース確認"

    def exec_task_method(self):
        self.register_error_info_to_mesh_descendants(
            self.check_concave_face, "concave_face", "凹型フェース確認"
        )

    @staticmethod
    def check_concave_face(target_transform_list, cleanup=False):
        """
        凹面フェースをチェック

        :param target_transform_list: トランスフォームリスト
        :param cleanup: クリーンアップをかけるかどうか
        """

        if not target_transform_list:
            return

        cmds.select(target_transform_list, r=True)

        mel_script = 'polyCleanupArgList 3 { "0","replace","1","0","0","1","0","0","0","1e-005","0","1e-005","0","1e-005","0","-1","0" }'

        if cleanup:
            mel_script = mel_script.replace("replace", "1")
        else:
            mel_script = mel_script.replace("replace", "2")

        result = mel.eval(mel_script)

        if not result:
            return

        result = cmds.ls(result, fl=True, l=True)

        return result


class HoleFace(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "穴のあるフェース確認"

    def exec_task_method(self):
        self.register_error_info_to_mesh_descendants(
            self._check_face_with_hole, "hole_face", "穴のあるフェース確認"
        )

    @staticmethod
    def _check_face_with_hole(target_transform_list, cleanup=False):
        """
        穴の開いているフェースチェック

        :param target_transform_list: トランスフォームリスト
        :param cleanup: クリーンアップをかけるかどうか
        """

        if not target_transform_list:
            return

        cmds.select(target_transform_list, r=True)

        mel_script = 'polyCleanupArgList 3 { "0","replace","1","0","0","0","1","0","0","1e-005","0","1e-005","0","1e-005","0","-1","0" }'

        if cleanup:
            mel_script = mel_script.replace("replace", "1")
        else:
            mel_script = mel_script.replace("replace", "2")

        result = mel.eval(mel_script)

        if not result:
            return

        result = cmds.ls(result, fl=True, l=True)

        return result


class LaminaFace(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ラミナフェース確認"

    def exec_task_method(self):
        self.register_error_info_to_mesh_descendants(
            self._check_lamina_face, "lamina_face", "ラミナフェース"
        )

    @staticmethod
    def _check_lamina_face(target_transform_list, cleanup=False):
        """
        ラミナフェースチェック

        :param target_transform_list: トランスフォームリスト
        :param cleanup: クリーンアップをかけるかどうか
        """

        if not target_transform_list:
            return

        cmds.select(target_transform_list, r=True)

        mel_script = 'polyCleanupArgList 3 { "0","replace","1","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-1","1" }'

        if cleanup:
            mel_script = mel_script.replace("replace", "1")
        else:
            mel_script = mel_script.replace("replace", "2")

        result = mel.eval(mel_script)

        if not result:
            return

        result = cmds.ls(result, fl=True, l=True)

        return result


class NonManifoldFace(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "非多様体フェース確認"

    def exec_task_method(self):
        self.register_error_info_to_mesh_descendants(
            self._check_nonmanifold, "non_manifold_face", "非多様体フェースを所有する頂点"
        )

    @staticmethod
    def _check_nonmanifold(target_transform_list, cleanup=False):
        """
        非多様体チェック

        :param target_transform_list: トランスフォームリスト
        :param cleanup: クリーンアップをかけるかどうか
        """

        if not target_transform_list:
            return

        cmds.select(target_transform_list, r=True)

        mel_script = 'polyCleanupArgList 3 { "0","replace","1","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","1","0" }'

        if cleanup:
            mel_script = mel_script.replace("replace", "1")
        else:
            mel_script = mel_script.replace("replace", "2")

        result = mel.eval(mel_script)

        if not result:
            return

        result = cmds.ls(result, fl=True, l=True)

        return result


class UnnecessaryHistory(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "不要なヒストリ"

    def exec_task_method(self):
        self.register_error_info_to_mesh_descendants(
            self._find_objects_with_non_skin_history,
            "unnecessary_history",
            "不必要なヒストリを所有するオブジェクト",
        )

    @staticmethod
    def _find_objects_with_non_skin_history(mesh_names: tp.List[str]) -> tp.List[str]:
        """対象オブジェクトにskinCluster以外のヒストリーが入っていたらそのオブジェクトを返す。
        Args:
            mesh_names (List[str]): チェックするメッシュの名前のリスト。
        Returns:
            List[str]: skinCluster以外のヒストリーが入っているオブジェクトのリスト。
        """
        objects_with_non_skin_history = []
        mesh_names = util.get_shapes(mesh_names)

        for mesh_name in mesh_names:
            if not cmds.objExists(mesh_name):
                raise ValueError(f"Mesh '{mesh_name}' does not exist.")

            history_nodes = cmds.listHistory(mesh_name, il=2, pdo=True)
            if not history_nodes:
                continue

            has_non_skin_history = False
            for node in history_nodes:
                if cmds.nodeType(node) != "skinCluster":
                    has_non_skin_history = True
                    break

            if has_non_skin_history:
                objects_with_non_skin_history.append(mesh_name)

        return objects_with_non_skin_history


class ColorSetName(CheckTaskBase):
    """self.extra_dataが必要
    sample:
        "self.extra_data": {"colorset_names":["test"] }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "カラーセット名"

    def exec_task_method(self):
        colorset_names = self.extra_data["colorset_names"]
        current_func = functools.partial(
            self._find_objects_with_other_color_sets,
            color_set_names=colorset_names,
        )
        self.register_error_info_to_mesh_descendants(
            current_func,
            "color_set_name",
            f"指定以外のcolorsetが含まれている:{colorset_names}",
        )

    @staticmethod
    def _find_objects_with_other_color_sets(
        mesh_names: tp.List[str], color_set_names: tp.List[str]
    ) -> tp.List[str]:
        """対象オブジェクトがcolor_set_namesで指定したcolor set名以外のcolor setを持っている場合、そのオブジェクトを返す。
        Args:
            mesh_names (List[str]): チェックするメッシュの名前のリスト。
            color_set_names (List[str]): 調べるcolor setの名前のリスト。
        Returns:
            List[str]: color set名以外のcolor setを持っているオブジェクトのリスト。
        """
        objects_with_other_color_sets = []
        for mesh_name in mesh_names:
            if not cmds.objExists(mesh_name):
                raise ValueError(f"Mesh '{mesh_name}' does not exist.")

            existing_color_sets = cmds.polyColorSet(
                mesh_name, query=True, allColorSets=True
            )
            if not existing_color_sets:
                continue

            has_other_color_set = False
            for existing_color_set in existing_color_sets:
                if existing_color_set not in color_set_names:
                    has_other_color_set = True
                    break

            if has_other_color_set:
                objects_with_other_color_sets.append(mesh_name)

        return objects_with_other_color_sets


class ColorSetCount(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "カラーセット数"

        if self.extra_data == None:
            raise ValueError(f"{self.checker_info.label_name}:にはextradataが必要です")

        self.color_set_count = self.extra_data["color_set_count"]

    def exec_task_method(self):
        current_func = functools.partial(
            self._find_objects_with_more_color_sets, min_color_sets=self.color_set_count
        )
        self.register_error_info_to_mesh_descendants(
            current_func, "color_set_count", f"color_setの数が{self.color_set_count}より多い"
        )

    @staticmethod
    def _find_objects_with_more_color_sets(
        mesh_names: tp.List[str], min_color_sets: int
    ) -> tp.List[str]:
        """対象オブジェクトに与えた数以上の数のcolor setがあるかどうか調べる。
        Args:
            mesh_names (List[str]): チェックするメッシュの名前のリスト。
            min_color_sets (int): 調べるcolor setの最小数。
        Returns:
            List[str]: 与えた数以上の数のcolor setがあるオブジェクトのリスト。
        """
        objects_with_more_color_sets = []
        for mesh_name in mesh_names:
            if not cmds.objExists(mesh_name):
                raise ValueError(f"Mesh '{mesh_name}' does not exist.")

            existing_color_sets = cmds.polyColorSet(
                mesh_name, query=True, allColorSets=True
            )
            if existing_color_sets and len(existing_color_sets) >= min_color_sets:
                objects_with_more_color_sets.append(mesh_name)

        return objects_with_more_color_sets


@staticmethod
class NormalLock(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "法線ロック"

    def exec_task_method(self):
        current_func = self.get_wiz2_normal_locked_vertex
        self.register_error_info_to_mesh_descendants(
            current_func, "normal_lock", f"法線がロックされています"
        )

    def get_border_edges(self, mesh):
        # Get all edges
        edges = cmds.ls("%s.e[*]" % mesh, flatten=True)

        # Filter border edges
        border_edges = []
        for edge in edges:
            connected_faces = cmds.ls(
                cmds.polyListComponentConversion(edge, toFace=True), flatten=True
            )
            if len(connected_faces) == 1:
                border_edges.append(edge)

        return border_edges

    def are_vertices_not_in_edges(
        self, vertex_list: tp.List[str], edge_list: tp.List[str]
    ) -> dict:
        """対象の頂点が対象のエッジに含まれているかチェックする。
        Args:
            vertex_list (List[str]): チェックする頂点の名前のリスト。
            edge_list (List[str]): チェックするエッジの名前のリスト。
        Returns:

        """
        result = vertex_list.copy()
        connected_verteces = cmds.polyListComponentConversion(
            edge_list, toVertex=True, fromEdge=True
        )
        connected_verteces = cmds.ls(connected_verteces, flatten=True, l=True)
        for vertex in vertex_list:
            if vertex in connected_verteces:
                result.remove(vertex)
        return result

    def find_locked_normal_vertices_multiple(self, mesh_names: tp.List[str]) -> dict:
        """対象オブジェクトの法線がロックされている頂点を返す。
        Args:
            mesh_names (List[str]): チェックするメッシュの名前のリスト。
        Returns:
            dict: キーがオブジェクト名、値が法線がロックされている頂点のリスト。
        """
        locked_normal_vertices = {}
        for mesh_name in mesh_names:
            if not cmds.objExists(mesh_name):
                raise ValueError(f"Mesh '{mesh_name}' does not exist.")

            vertex_count = cmds.polyEvaluate(mesh_name, vertex=True)
            locked_vertices = []
            for i in range(vertex_count):
                vertex_name = f"{mesh_name}.vtx[{i}]"
                locked_normal = cmds.polyNormalPerVertex(
                    vertex_name, query=True, freezeNormal=True
                )
                if any(locked_normal):
                    locked_vertices.append(vertex_name)

            locked_normal_vertices[mesh_name] = locked_vertices
        return locked_normal_vertices

    def get_wiz2_normal_locked_vertex(self, mesh_names: tp.List[str]) -> dict:
        """wiz2で必要な法線ロックされている頂点取得
        境界エッジを除く頂点から取得

        Args:
            mesh_names (tp.List[str]): 対象のメッシュ名

        Returns:
            dict: 対象となる頂点
        """
        all_normal_locked_vertices = self.find_locked_normal_vertices_multiple(
            mesh_names
        )
        border_edges = []
        for mesh in mesh_names:
            border_edges.extend(self.get_border_edges(mesh))

        vertices = []
        for mesh_name in all_normal_locked_vertices:
            vertices.extend(all_normal_locked_vertices[mesh_name])

        vertices = self.are_vertices_not_in_edges(vertices, border_edges)

        return vertices


class UnusedNodes(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "未使用のノード"

        if self.extra_data == None:
            raise ValueError(f"{self.checker_info.label_name}:にはextradataが必要です")

        self.node_types = self.extra_data["node_types"]

    def exec_task_method(self):
        unused_nodes = self.get_unused_nodes(self.node_types)
        if len(self.get_unused_nodes(self.node_types)) > 0:
            self.set_error_data("unused_nodes", unused_nodes, "未使用のノード")
        else:
            self.set_error_type(ErrorType.NOERROR)

    @staticmethod
    def get_unused_nodes(node_types: tp.List[str]) -> tp.List[str]:
        """シーン内の未使用ノードを取得する関数

        Args:
            node_types (tp.List[str]): 未使用ノードを検索するノードタイプのリスト

        Returns:
            tp.List[str]: 未使用ノード名のリスト
        """
        unused_nodes = []
        for node_type in node_types:
            all_nodes = cmds.ls(type=node_type)
            for node in all_nodes:
                cmds.hyperShade(objects=node)
                connections = cmds.ls(sl=True)
                if not connections:
                    unused_nodes.append(node)
        return unused_nodes


class HasKeyframe(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "キーフレーム"

    def exec_task_method(self):
        roots = self.maya_scene_data.root_nodes
        target_nodes = []
        for root in roots:
            target_nodes.append(root.full_path_name)
            for descendent_node in root.all_descendents:
                target_nodes.append(descendent_node.full_path_name)

        error_objects = self.check_keyframe(target_nodes)
        self.set_error_data("has_key_frame", error_objects, "キーフレームが設定されているノード")

    def exec_fix_method(self):
        error_objects = self.get_debug_target_objects("has_key_frame")
        HasKeyframe.delete_all_keyframes(error_objects)

    @staticmethod
    def delete_all_keyframes(objects: tp.List[str]) -> None:
        """
        対象オブジェクトのキーフレームをすべて削除する関数。
        Args:
            objects (List[str]): 対象のオブジェクト名のリスト。
        Returns: なし
        """
        for obj in objects:
            cmds.cutKey(obj, clear=True)

    @staticmethod
    def get_objects_with_keyframes(obj_list: tp.List[str]) -> tp.List[str]:
        """対象のオブジェクトにキーフレームが存在しているかどうかを確認し、キーフレームが存在しているオブジェクトをすべて返す関数

        Args:
            obj_list (tp.List[str]): オブジェクト名のリスト

        Returns:
            tp.List[str]: キーフレームが存在しているオブジェクト名のリスト
        """
        objects_with_keyframes = []
        for obj in obj_list:
            keyframes = cmds.keyframe(obj, query=True, keyframeCount=True)
            if keyframes:
                objects_with_keyframes.append(obj)
        return objects_with_keyframes

    def check_keyframe(self, obejcts: tp.List[str]) -> tp.List[str]:
        """キーフレームを保有しているかどうか確認する

        Args:
            obejcts (tp.List[str]): 対象のオブジェクト

        Returns:
            tp.List[str]: キーフレームを保有しているジョイント
        """
        has_keyframe_joints = self.get_objects_with_keyframes(obejcts)
        return has_keyframe_joints
