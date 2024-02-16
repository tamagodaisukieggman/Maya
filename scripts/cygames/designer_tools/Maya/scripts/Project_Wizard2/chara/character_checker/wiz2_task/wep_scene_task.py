import typing as tp
import re
from collections import Counter


import maya.cmds as cmds

from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.data import ErrorType
from ....common.maya_checker.common_task import HasDuplicateNodeNames

class Wiz2WepSceneLocation(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "シーンの場所"

    def exec_task_method(self):
        weapon_path = "C:/cygames/wiz2/team/3dcg/chr/wep/general/"
        is_valid_path = True
        if weapon_path not in self.maya_scene_data.name:
            is_valid_path = False

        if is_valid_path:
            self.set_error_type(ErrorType.NOERROR)
        else:
            self.set_error_data("wiz2_prp_scene_location", None, "シーンの場所が規定と異なっています")


class Wiz2WepFileName(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ファイル名"

    def exec_task_method(self):
        if self.check_string_format(self.maya_scene_data.basename):
            self.set_error_type(ErrorType.NOERROR)
        else:
            self.set_error_data("wiz2_prp_file_name", None, "ファイル名がプロジェクトの仕様と異なっています")

    @staticmethod
    def check_string_format(s: str) -> bool:
        """対象の文字列が以下の規則になっているかどうかを調べます。
        pro_"gかc"_"自由な文字列""数字2文字"
        Args:
            input_str (str): チェックする対象の文字列
        Returns:
            bool: 指定された規則に従っている場合はTrue、それ以外はFalse
        """
        pattern = r'^wep_g_.*\d{3}$'
        return bool(re.match(pattern, s))

class Wiz2WepMeshName(CheckTaskBase):
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

        error_meshes = self._check_has_mesh(target_nodes)

        if error_meshes:
            self.set_error_data(
                "mesh_name",
                error_meshes,
                "root_nodeの下のメッシュが規定の名前のメッシュ名になっていない",
                is_reset_debug_data=True,
            )

        # すべての条件が問題なければエラーなし
        if error_meshes:
            self.set_error_type(ErrorType.WARNING)

        else:
            self.set_error_type(ErrorType.NOERROR)

    def _check_has_mesh(self, deep_1_nodes: tp.List[str]):
        error_meshes = []
        for target in deep_1_nodes:
            if "transform" == target.node_type:
                if target.extra_data["has_shape"]:          
                    short_name = target.short_name
                    if self.check_string_format(short_name):
                        continue
                    else:
                        if not short_name.endswith("_Outline"):
                            error_meshes.append(short_name)
        return error_meshes

                
    @staticmethod
    def check_string_format(s: str) -> bool:
        """対象の文字列が以下の規則になっているかどうかを調べます。
        pro_"gかc"_"自由な文字列""数字2文字"
        Args:
            input_str (str): チェックする対象の文字列
        Returns:
            bool: 指定された規則に従っている場合はTrue、それ以外はFalse
        """
        pattern = r'^wep_g_.*\d{3}_\d{2}$'
        return bool(re.match(pattern, s))
    

# class Wiz2WepJointName(CheckTaskBase):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.checker_info.label_name = "ルートジョイント名"
#         self.error_type = ErrorType.WARNING

#     def exec_task_method(self):
#         """checkのテスト"""
#         error_groups = []
#         for root in self.maya_scene_data.root_nodes:
#             target_nodes = []
#             for child_node in root.all_descendents:
#                 if child_node.deep == 1:
#                     target_nodes.append(child_node)

#             is_error_joint = self._check_joint_name(target_nodes)
#             if not is_error_joint:
#                 error_groups.append(root.full_path_name)

#         if error_groups:
#             self.set_error_data(
#                 "mesh_name",
#                 error_groups,
#                 "root_nodeの下のメッシュが規定の名前のメッシュ名になっていない",
#                 is_reset_debug_data=True,
#             )

#         # すべての条件が問題なければエラーなし
#         if error_groups:
#             self.set_error_type(ErrorType.WARNING)

#         else:
#             self.set_error_type(ErrorType.NOERROR)

#     def _check_joint_name(self,target_nodes):
#         for node in target_nodes:
#             if node.node_type == "joint":
#                 if node.short_name == "Root":
#                     return True
#         return False


class Wiz2WepMeshName(CheckTaskBase):
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

        error_meshes = self._check_has_mesh(target_nodes)

        if error_meshes:
            self.set_error_data(
                "mesh_name",
                error_meshes,
                "root_nodeの下のメッシュが規定の名前のメッシュ名になっていない",
                is_reset_debug_data=True,
            )

        # すべての条件が問題なければエラーなし
        if error_meshes:
            self.set_error_type(ErrorType.WARNING)

        else:
            self.set_error_type(ErrorType.NOERROR)

    def _check_has_mesh(self, deep_1_nodes: tp.List[str]):
        error_meshes = []
        for target in deep_1_nodes:
            if "transform" == target.node_type:
                if target.extra_data["has_shape"]:          
                    short_name = target.short_name
                    if self.check_string_format(short_name):
                        continue
                    else:
                        if not short_name.endswith("_Outline"):
                            error_meshes.append(short_name)
        return error_meshes

                
    @staticmethod
    def check_string_format(s: str) -> bool:
        """対象の文字列が以下の規則になっているかどうかを調べます。
        pro_"gかc"_"自由な文字列""数字2文字"
        Args:
            input_str (str): チェックする対象の文字列
        Returns:
            bool: 指定された規則に従っている場合はTrue、それ以外はFalse
        """
        pattern = r'^wep_g_.*\d{3}_\d{2}$'
        return bool(re.match(pattern, s))
    

class Wiz2WepRootGroupName(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ルートのグループ名"
        self.error_type = ErrorType.WARNING

    def exec_task_method(self):
        """checkのテスト"""
        error_groups = []
        for root in self.maya_scene_data.root_nodes:
            if root.short_name == "wep":
                continue

            if root.short_name.startswith("wep"):
                pattern = r'^wep_\d{2}$'
                if False == bool(re.match(pattern, root.short_name)):
                    error_groups.append(root.short_name)
            else:
                error_groups.append(root.short_name)
            
        if error_groups:
            self.set_error_data(
                "wep_root_group",
                error_groups,
                "root_nodeの下のメッシュが規定の名前のメッシュ名になっていない",
                is_reset_debug_data=True,
            )

        # すべての条件が問題なければエラーなし
        if error_groups:
            self.set_error_type(ErrorType.WARNING)

        else:
            self.set_error_type(ErrorType.NOERROR)

# class Wiz2WepHasDuplicateNodeNames(HasDuplicateNodeNames):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.checker_info.label_name = "ノード名の重複"

#     def _get_duplicate_node_names(self) -> tp.List[str]:
#         """シーン内の重複している全てのノード名を配列で返す。
#         Returns:
#             list: 重複しているノード名のリスト。
#         """
#         all_nodes = cmds.ls(long=True)
#         all_nodes = [node for node in all_nodes if cmds.objectType(node) != "joint" and "offSet_Root" not in node]

#         short_names = [node.rsplit("|")[-1] for node in all_nodes]

#         name_counts = Counter(short_names)
#         duplicate_names = [name for name, count in name_counts.items() if count > 1]

#         all_duplicate_names = []
#         for name in duplicate_names:
#             for lp in cmds.ls(f"*{name}"):
#                 all_duplicate_names.append(lp)
#         return all_duplicate_names
