import typing as tp
import re

import maya.cmds as cmds

from .. import utils

from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.scene_data import MayaSceneDataBase
from ....common.maya_checker.data import ErrorType


class Wiz2HasJoint(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "骨の存在確認"

    def exec_task_method(self):
        """checkのテスト"""
        
        no_joint_groups = []
        has_joint = True
        for root in self.maya_scene_data.root_nodes:
            target_nodes = []
            for child_node in root.all_descendents:
                if child_node.deep == 1:
                    target_nodes.append(child_node)

            has_joint = self._check_has_joint(target_nodes)

            if not has_joint:
                no_joint_groups.append(root.full_path_name)
        
        if no_joint_groups:
            self.set_error_data(
                "has_joint", no_joint_groups, "root_nodeの下にジョイントが存在しない", is_reset_debug_data=True
            )

        # すべての条件が問題なければエラーなし
        if no_joint_groups:
            self.set_error_type(ErrorType.ERROR)

        else:
            self.set_error_type(ErrorType.NOERROR)

    def _check_has_joint(self, deep_1_nodes: tp.List[str]):
        for target in deep_1_nodes:
            if "joint" == target.node_type:
                return True
        return False


class Wiz2HasOutline(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "Outlineの存在確認"

    def exec_task_method(self):
        """checkのテスト"""
        has_outline = True
        
        no_outline_groups = []
        for root in self.maya_scene_data.root_nodes:
            target_nodes = []
            for child_node in root.all_descendents:
                if child_node.deep == 1:
                    target_nodes.append(child_node)

            has_outline = self._check_has_outline(target_nodes)

            if not has_outline:
                no_outline_groups.append(root.full_path_name)

        if has_outline == False:
            self.set_error_data(
                "has_outline",
                no_outline_groups,
                'root_nodeの下に"シーン名"+_Outlineが存在しない',
                is_reset_debug_data=True,
            )

        # すべての条件が問題なければエラーなし
        if True == has_outline:
            self.set_error_type(ErrorType.NOERROR)

    def _check_has_outline(self, deep_1_nodes: tp.List[str]):
        for target in deep_1_nodes:
            if "transform" == target.node_type:
                short_name = target.short_name
                if short_name.endswith("_a1") or short_name.endswith("_a2"):
                    continue 
                if target.extra_data["has_shape"] and "_Outline" not in short_name:
                    if not cmds.objExists(target.full_path_name + "_Outline"):
                        return False
        return True


class Wiz2MeshName(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "メッシュ名"
        self.error_type = ErrorType.WARNING

    def exec_task_method(self):
        """checkのテスト"""
        target_nodes = []
        for root in self.maya_scene_data.root_nodes:
            for child_node in root.all_descendents:
                if child_node.deep == 1:
                    target_nodes.append(child_node)

        has_mesh = self._check_has_mesh(target_nodes)

        if has_mesh == False:
            self.set_error_data(
                "mesh_name",
                None,
                "root_nodeの下のメッシュが規定の名前のメッシュ名になっていない",
                is_reset_debug_data=True,
            )

        # すべての条件が問題なければエラーなし
        if False == has_mesh:
            self.set_error_type(ErrorType.WARNING)

        else:
            self.set_error_type(ErrorType.NOERROR)

    def _check_has_mesh(self, deep_1_nodes: tp.List[str]):
        scene_name = self.maya_scene_data.basename

        body_type = utils.get_current_scene_info(self.maya_scene_data)["body_type"]

        for target in deep_1_nodes:
            if "transform" == target.node_type:
                if target.extra_data["has_shape"]:
                    short_name = target.short_name
                    if short_name.startswith(scene_name):
                        suffix = short_name.replace(scene_name, "")
                        if suffix in ["", "_base"] or Wiz2MeshName.is_format_valid(
                            suffix
                        ):
                            return True

                        elif body_type == "shoes" and suffix in [
                            "_s",
                            "_p",
                            "_b",
                            "_l",
                        ]:
                            return True

                        else:
                            return False
        return False

    @staticmethod
    def is_format_valid(s):
        if len(s) != 3:
            return False
        if s[0] != "_":
            return False
        if not s[1:].isdigit():
            return False
        return True


class Wiz2DisplayLayerSettings(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ディスプレイレイヤーの設定"

    def exec_task_method(self):
        has_joint_display_layer = self._does_display_layer_exist("joint")
        has_mesh_display_layer = self._does_display_layer_exist("mesh")
        is_error = False

        # mesh display layer settings check
        if has_mesh_display_layer:
            layer_name = "mesh"
            types = self._get_object_types_in_display_layer(layer_name)

            # transformのノードが含まれていない場合の処理
            if "transform" not in types:
                self.set_error_data(
                    "transform_in_mesh_display_layer",
                    None,
                    "meshにtransformタイプのノードが含まれていません",
                )
                is_error = True
        else:
            # mesh display layerが存在しない
            self.set_error_data(
                "has_mesh_display_layer",
                None,
                "meshのディスプレイレイヤーが存在しない",
            )
            is_error = True

        # joint display layer settings check
        if has_joint_display_layer:
            layer_name = "joint"
            types = self._get_object_types_in_display_layer(layer_name)

            # transformのノードが含まれていない場合の処理
            if "joint" not in types:
                self.set_error_data(
                    "joint_in_joint_display_layer",
                    None,
                    "jointにjointタイプのノードが含まれていません",
                )
                is_error = True
        else:
            # mesh display layerが存在しない
            self.set_error_data(
                "has_joint_display_layer",
                None,
                "jointのディスプレイレイヤーが存在しない",
            )
            is_error = True
        if is_error == False:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        ...

    def _get_object_types_in_display_layer(self, layer_name):
        """ディスプレイレイヤーに含まれるオブジェクトのタイプを返す。
        Args:
            layer_name (str): チェックするディスプレイレイヤーの名前。
        Returns:
            list: ディスプレイレイヤーに含まれるオブジェクトのタイプのリスト。
        """
        if not cmds.objExists(layer_name):
            raise ValueError(f"Display layer '{layer_name}' does not exist.")

        members = cmds.editDisplayLayerMembers(layer_name, query=True, fullNames=True)
        if not members:
            return []

        object_types = set()
        for member in members:
            object_type = cmds.objectType(member)
            object_types.add(object_type)

        return list(object_types)

    def _does_display_layer_exist(self, layer_name):
        """特定の名前のDisplayLayerが存在しているかどうかをboolで返す。
        Args:
            layer_name (str): チェックするDisplayLayerの名前。
        Returns:
            bool: DisplayLayerが存在する場合はTrue、存在しない場合はFalse。
        """
        display_layers = cmds.ls(type="displayLayer")
        return layer_name in display_layers


class Wiz2FileName(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ファイル名"

    def exec_task_method(self):
        if self.check_string_format(self.maya_scene_data.basename):
            self.set_error_type(ErrorType.NOERROR)
        else:
            self.set_error_data("wiz2_file_name", None, "ファイル名がプロジェクトの仕様と異なっています")

    @staticmethod
    def check_string_format(input_str: str) -> bool:
        """対象の文字列が以下の規則になっているかどうかを調べます。
        "英字1文字""数字1文字"_"英字1文字_"英字文字列""数字2文字"
        Args:
            input_str (str): チェックする対象の文字列
        Returns:
            bool: 指定された規則に従っている場合はTrue、それ以外はFalse
        """
        pattern = r"^[a-zA-Z]\d_[a-zA-Z]_[a-zA-Z]+\d{2}$"
        return bool(re.match(pattern, input_str))


class Wiz2UnusedMaterial(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "未使用マテリアル"
        self.fix_detail = "未使用マテリアルの削除"

    def exec_task_method(self):
        unused_materials = self.get_unused_materials()
        defalt_material = ["lambert1", "standardSurface1", "particleCloud1"]
        for material in defalt_material:
            unused_materials.remove(material)

        if unused_materials:
            self.set_error_data(
                "wiz2_unused_material", unused_materials, "使用されていないマテリアル"
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        error_targets = self.debug_data.error_target_info["wiz2_unused_material"][
            "target_objects"
        ]
        cmds.delete(error_targets)
        for error_target in error_targets:
            print(f"{error_target} >> 削除しました")

    @staticmethod
    def get_unused_materials() -> tp.List[str]:
        """
        シーン内でアサインされていない（使用されていない）マテリアルをすべて取得する関数

        Returns:
            List[str]: 使用されていないマテリアルのリスト
        """
        all_materials = cmds.ls(materials=True)
        all_meshes = cmds.ls(type="mesh")
        assigned_materials = []

        for mesh in all_meshes:
            shading_groups = cmds.listConnections(mesh, type="shadingEngine")
            if shading_groups is None:
                continue
            for shading_group in shading_groups:
                materials = cmds.ls(cmds.listConnections(shading_group), materials=True)
                if materials is None:
                    continue
                assigned_materials.extend(materials)

        assigned_materials = list(set(assigned_materials))
        unused_materials = [
            material for material in all_materials if material not in assigned_materials
        ]
        return unused_materials
