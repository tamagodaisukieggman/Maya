# -*- coding: utf-8 -*-
import functools
import typing as tp

from ..task import CheckTaskBase
from ..scene_data import MayaSceneDataBase
from ..data import ErrorType

import maya.cmds as cmds


class UVLayout(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "uvが0-1におさまっているか"

    def exec_task_method(self):
        current_func = self._get_vertices_outside_uv_bounds_multiple
        self.register_error_info_to_mesh_descendants(
            current_func, "", f"uvが0-1におさまっていない頂点"
        )

    @staticmethod
    def _get_vertices_outside_uv_bounds_multiple(
        mesh_names: tp.List[str],
    ) -> tp.Dict[str, tp.List[str]]:
        """対象オブジェクトの頂点のUVが(1.0, 1.0)内に収まっていないかを確認する。
        Args:
            mesh_names (List[str]): メッシュの名前のリスト。
        Returns:
            Dict[str, List[str]]: キーがオブジェクト名、値が(1.0, 1.0)内に収まっていない頂点のリスト。
        """
        result = {}

        for mesh_name in mesh_names:
            if not cmds.objExists(mesh_name):
                raise ValueError(f"Mesh '{mesh_name}' does not exist.")

            vertex_count = cmds.polyEvaluate(mesh_name, vertex=True)
            vertices_outside_bounds = []

            for i in range(vertex_count):
                vertex_name = f"{mesh_name}.vtx[{i}]"
                uv_list = cmds.polyListComponentConversion(
                    vertex_name, fromVertex=True, toUV=True
                )

                if uv_list:
                    uv_outside_bounds = False
                    for uv in uv_list:
                        uv_coords = cmds.polyEditUV(uv, query=True)
                        if (
                            uv_coords[0] < 0.0
                            or uv_coords[0] > 1.0
                            or uv_coords[1] < 0.0
                            or uv_coords[1] > 1.0
                        ):
                            uv_outside_bounds = True
                            break
                    if uv_outside_bounds:
                        vertices_outside_bounds.append(vertex_name)

            result[mesh_name] = vertices_outside_bounds

        return result


class UVSetName(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "UVセット名"

        if self.extra_data == None:
            raise ValueError(f"{self.checker_info.label_name}:にはextradataが必要です")

        self.uv_set_names = self.extra_data["uv_set_names"]

    def exec_task_method(self):
        current_func = functools.partial(
            self._check_uv_sets, allowed_uv_set_names=self.uv_set_names
        )
        self.register_error_info_to_mesh_descendants(
            current_func, "uv_set_name", f"不正なUVセットを保有するオブジェクト"
        )

    @staticmethod
    def _check_uv_sets(
        objects: tp.List[str], allowed_uv_set_names: tp.List[str]
    ) -> tp.List[str]:
        """指定された名前のUVセット以外が含まれているオブジェクトを確認する関数

        Args:
            objects (tp.List[str]): 対象オブジェクトのリスト
            allowed_uv_set_names (tp.List[str]): 許可されたUVセット名のリスト

        Returns:
            tp.List[str]: 指定された名前のUVセット以外が含まれているオブジェクトのリスト
        """
        invalid_uv_objects = []

        for obj in objects:
            uv_sets = cmds.polyUVSet(obj, query=True, allUVSets=True)
            for uv_set in uv_sets:
                if uv_set not in allowed_uv_set_names:
                    invalid_uv_objects.append(obj)
                    break

        return invalid_uv_objects
