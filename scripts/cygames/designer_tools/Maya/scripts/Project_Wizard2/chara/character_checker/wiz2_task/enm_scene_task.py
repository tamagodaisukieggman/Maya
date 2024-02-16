import typing as tp
import re
from collections import Counter


import maya.cmds as cmds

from .. import utils as chara_utils
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.data import ErrorType
from ....common.maya_checker.common_task import HasDuplicateNodeNames

class Wiz2EnmSceneLocation(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "シーンの場所"

    def exec_task_method(self):
        enm_type = chara_utils.parse_current_scene_name(self.maya_scene_data)[1]
        if "b" in enm_type:
            enm_type = "boss"

        elif "m" in enm_type:
            enm_type = "minion"
        
        else:
            raise ValueError("")
        
        boss_path = "C:/cygames/wiz2/team/3dcg/chr/enm/boss/"
        minion_path = "C:/cygames/wiz2/team/3dcg/chr/enm/minion/"
        is_valid_path = True
        if enm_type == "boss":
            if boss_path not in self.maya_scene_data.name:
                is_valid_path = False
        
        elif enm_type == "minion":
            if minion_path not in self.maya_scene_data.name:
                is_valid_path = False

        if is_valid_path:
            self.set_error_type(ErrorType.NOERROR)
        else:
            self.set_error_data("wiz2_enm_scene_location", None, "シーンの場所が規定と異なっています")


class Wiz2EnmFileName(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ファイル名"

    def exec_task_method(self):
        if self.check_string_format(self.maya_scene_data.basename):
            self.set_error_type(ErrorType.NOERROR)
        else:
            self.set_error_data("wiz2_enm_file_name", None, "ファイル名がプロジェクトの仕様と異なっています")

    @staticmethod
    def check_string_format(s: str) -> bool:
        """対象の文字列が以下の規則になっているかどうかを調べます。
        enm_"bかm"_"自由な文字列""数字2文字"
        Args:
            input_str (str): チェックする対象の文字列
        Returns:
            bool: 指定された規則に従っている場合はTrue、それ以外はFalse
        """
        pattern = r'^enm_[bm]_.*\d{2}$'
        return bool(re.match(pattern, s))

class Wiz2EnmMeshName(CheckTaskBase):
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
        enm_"bかm"_"自由な文字列""数字2文字"
        Args:
            input_str (str): チェックする対象の文字列
        Returns:
            bool: 指定された規則に従っている場合はTrue、それ以外はFalse
        """
        pattern = r'^enm_[bm]_.*\d{2}_\d{2}$'
        return bool(re.match(pattern, s))
    

class Wiz2EnmRootGroupName(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ルートのグループ名"
        self.error_type = ErrorType.WARNING

    def exec_task_method(self):
        """checkのテスト"""
        error_groups = []
        for root in self.maya_scene_data.root_nodes:
            if root.short_name == "enm":
                continue

            if root.short_name.startswith("enm"):
                pattern = r'^enm_\d{2}$'
                if False == bool(re.match(pattern, root.short_name)):
                    error_groups.append(root.short_name)
            else:
                error_groups.append(root.short_name)
            
        if error_groups:
            self.set_error_data(
                "enm_root_group",
                error_groups,
                "root_nodeの下のメッシュが規定の名前のメッシュ名になっていない",
                is_reset_debug_data=True,
            )

        # すべての条件が問題なければエラーなし
        if error_groups:
            self.set_error_type(ErrorType.WARNING)

        else:
            self.set_error_type(ErrorType.NOERROR)

# class Wiz2enmHasDuplicateNodeNames(HasDuplicateNodeNames):
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
