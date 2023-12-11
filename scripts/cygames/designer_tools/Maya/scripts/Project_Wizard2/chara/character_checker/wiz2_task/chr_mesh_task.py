import typing as tp
import functools
import maya.cmds as cmds

from .. import utils
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.scene_data import MayaSceneDataBase
from ....common.maya_checker.data import ErrorType
from ....common.maya_checker.common_task.weight_task import BoundJoint


class Wiz2SceneNameObjectExists(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "メッシュ名"

    def exec_task_method(self):
        is_scene_name_object_exists = self.check_scene_name_object_exists()
        if is_scene_name_object_exists == False:
            self.set_error_data(
                "wiz2_scene_name_object_exists",
                None,
                "シーン名と同じ名前のオブジェクトはルートの下に存在しません",
            )

        else:
            self.set_error_type(ErrorType.NOERROR)

    def check_scene_name_object_exists(self) -> bool:
        """シーン名と同名のオブジェクトが存在するかのチェック

        Returns:
            _type_: _description_
        """
        for root_node in self.maya_scene_data.root_nodes:
            for node in root_node.all_descendents:
                if node.deep == 1:
                    if self.maya_scene_data.basename == node.short_name:
                        return True

        return False


class Wiz2BoundJoint(BoundJoint):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "バインド確認"

    def exec_task_method(self):
        self.extra_data["exclude_objects"] = cmds.ls(
            "*_Outline", type="transform", l=True
        )
        current_func = functools.partial(self.check_not_bound_object)

        self.register_error_info_to_mesh_descendants(
            current_func, "not_bound_object", "バインドされていないオブジェクト"
        )


class Wiz2PolyCount(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ポリゴン数"

    def exec_task_method(self):
        scene_file_info = utils.get_current_scene_info(self.maya_scene_data)
        body_type = scene_file_info["body_type"]
        character_info = utils.get_character_info()
        current_max_count = character_info["polygon_count_max"][body_type]

        if body_type == "shoes":
            self.set_error_data(
                f"wiz2_poly_count",
                None,
                f"{body_type} には現在このチェックは対応しておりません。{body_type} のポリゴン最大数は{current_max_count}です。手動で確認をお願いいたします。",
            )
            return

        has_error, has_error_targets, reset_message = self.get_check_poly_count_results(current_max_count)

        if has_error == True:
            self.set_error_data(
                f"wiz2_poly_count",
                has_error_targets,
                f"{body_type} の規定ポリゴン数({current_max_count})を超えています",
                is_reset_debug_data=reset_message,
            )

        elif has_error == False:
            self.set_error_type(ErrorType.NOERROR)

    def get_check_poly_count_results(self, current_max_count):
        meshes = self.get_meshes()
        has_error = False
        has_error_targets = []
        for i, base_mesh in enumerate(meshes):
            reset_message = False
            if i == 0:
                reset_message = True
            mesh = meshes[base_mesh]
            if len(mesh) == 1:
                if base_mesh == mesh[0]:
                    check_meshes = [base_mesh]
                else:
                    check_meshes = [base_mesh, *mesh]
                
            else:
                check_meshes = [base_mesh, *mesh]

            is_valid_polycount = Wiz2PolyCount.check_poly_count(
                check_meshes, current_max_count
            )

            if not is_valid_polycount:
                has_error_targets.append(str(check_meshes))
                has_error = True
        return has_error,has_error_targets,reset_message

    @staticmethod
    def check_poly_count(meshes: tp.List[str], max_poly_count: int) -> bool:
        """メッシュのポリゴン数の合計がmax_poly_count以下であるかどうかを判定します。
        Args:
            meshes (List[str]): 対象のメッシュリスト
            max_poly_count (int): 許容する最大ポリゴン数
        Returns:
            bool: ポリゴン数の合計がmax_poly_count以下ならTrue、それ以外はFalse
        """
        total_poly_count = 0
        for mesh in meshes:
            try:
                poly_count = cmds.polyEvaluate(mesh, triangle=True)
                total_poly_count += poly_count
            except Exception as e:
                print(f"Error: {e}")
                return False

        if total_poly_count > max_poly_count:
            return False

        return True

    def get_scenename_meshes(self) -> dict:
        """シーンネームと同名のメッシュを返す

        Returns:
            str: シーンネームと同名のメッシュのlong
        """
        rtn = {}
        for root_node in self.maya_scene_data.root_nodes:
            rtn[root_node.full_path_name] = []
            for node in root_node.all_descendents:
                if node.deep == 1:
                    if self.maya_scene_data.basename == node.short_name:
                        rtn[root_node.full_path_name].append(node.full_path_name)
        return rtn

    def get_meshes(self) -> dict:
        """シーンネームと同名のメッシュを返す

        Returns:
            str: シーンネームと同名のメッシュのlong
        """

        rtn = {}

        for root_node in self.maya_scene_data.root_nodes:
            # rtn[root_node.full_path_name] = []
            deep_1_list = [node for node in root_node.all_descendents if node.deep == 1 and node.node_type == "transform"]
            # has shapeのトランスフォームのみ対象とする
            deep_1_list = [node for node in deep_1_list if node.extra_data["has_shape"]]
            base_mesh_list = []

            # _base用の処理
            # _baseがsuffixになっているメッシュを取得
            for node in deep_1_list:
                if node.short_name.endswith("_base"):
                    base_mesh_list.append(node)

            # 差分メッシュの取得
            for base_mesh in base_mesh_list:
                rtn = {base_mesh.full_path_name: []}
                character_id = base_mesh.short_name.replace("_base", "")
                for node in deep_1_list:
                    if character_id in node.short_name:
                        for suffix in ["_base","_Outline","a1","a2"]:
                            if node.short_name.endswith(suffix):
                                break
                        else:
                            append_list = [node.full_path_name]
                            for alpha_node in deep_1_list:
                                #baseか差分のalphaを判定
                                if alpha_node.short_name.startswith(node.short_name) or alpha_node.short_name.startswith(base_mesh.short_name):
                                    for lp in ["a1","a2"]:
                                        if alpha_node.short_name.endswith(lp):
                                            append_list.append(alpha_node.full_path_name)
                            rtn[base_mesh.full_path_name] = append_list

            
            # どちらにも含まれないメッシュは単一でエクスポートされるメッシュ
            single_mesh_list = deep_1_list.copy()
            for base_mesh in base_mesh_list:
                character_id = base_mesh.short_name.replace("_base", "")
                for node in single_mesh_list:
                    if character_id in node.short_name:
                        single_mesh_list.remove(node)
            
            
            for single_mesh_node in single_mesh_list:
                is_alpha = False
                for lp in ["a1","a2"]:
                    if single_mesh_node.short_name.endswith(lp):
                        is_alpha = True
                
                if is_alpha:
                    continue

                append_list = []
                for alpha_node in single_mesh_list:
                    #baseか差分のalphaを判定
                    if alpha_node.short_name.startswith(single_mesh_node.short_name):
                        for lp in ["a1","a2"]:
                            if alpha_node.short_name.endswith(lp):
                                append_list.append(alpha_node.full_path_name)
                rtn[single_mesh_node.full_path_name] = [*append_list]
        return rtn

class Wiz2OutlineDif(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "アウトラインメッシュ"

    def exec_task_method(self):
        invalid_outlines = self.get_invalid_outlines()
        self.set_error_type(ErrorType.NOERROR)
        if invalid_outlines:
            self.set_error_data(
                "wiz2_outline_dif",
                invalid_outlines,
                "_Outlineのメッシュと本体のメッシュの頂点数or頂点位置が異なる",
            )

    def get_invalid_outlines(self):
        """有効ではないoutlineメッシュの取得"""
        not_valid_outlines = []
        for root in self.maya_scene_data.root_nodes:
            for mesh_transform in root.get_all_mesh_transform():
                if "_Outline" in mesh_transform:
                    outline_mesh = mesh_transform
                    origine_mesh = outline_mesh.replace("_Outline", "")
                    is_invalid_outline = self.check_vertex_position_difference(
                        origine_mesh, outline_mesh
                    )
                    if is_invalid_outline:
                        not_valid_outlines.append(outline_mesh)
        return not_valid_outlines

    @staticmethod
    def check_vertex_position_difference(
        obj1: str, obj2: str, tolerance: float = 0.0001
    ) -> bool:
        """対象のオブジェクトがターゲットのオブジェクトと各頂点の位置にずれがあるかどうかを調べます。
        Args:
            obj1 (str): 調べる対象のオブジェクト1
            obj2 (str): 調べる対象のオブジェクト2
            tolerance (float): 位置の違いを許容する閾値（デフォルトは0.0001）
        Returns:
            bool: ずれがある場合はTrue、ない場合はFalse
        """
        should_compare, vertex_count = Wiz2OutlineDif.compare_objects_vertex_count(
            obj1, obj2
        )

        if not should_compare:
            return True

        # 頂点位置の違いを調べる
        for i in range(vertex_count):
            point1 = cmds.xform(
                f"{obj1}.vtx[{i}]", query=True, worldSpace=True, translation=True
            )
            point2 = cmds.xform(
                f"{obj2}.vtx[{i}]", query=True, worldSpace=True, translation=True
            )

            diff = [abs(p1 - p2) for p1, p2 in zip(point1, point2)]

            if any(d > tolerance for d in diff):
                return True

        return False

    @staticmethod
    def compare_objects_vertex_count(obj1: str, obj2: str) -> tuple:
        """対象のオブジェクトがターゲットのオブジェクトと頂点数が同じかどうかを調べます。

        Args:
            obj1 (str): 調べる対象のオブジェクト1
            obj2 (str): 調べる対象のオブジェクト2

        Returns:
            tuple of bool and int:
                - 頂点数が同じ場合はTrue、違う場合はFalse
                - 頂点数が同じ場合は頂点数、違う場合は0
        """
        vertex_count_obj1 = cmds.polyEvaluate(obj1, vertex=True)
        vertex_count_obj2 = cmds.polyEvaluate(obj2, vertex=True)

        return vertex_count_obj1 == vertex_count_obj2, vertex_count_obj1


class Wiz2ColorSetExists(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "カラーセットの有無"

        if self.extra_data == None:
            raise ValueError(f"{self.checker_info.label_name}:にはextradataが必要です")

    def exec_task_method(self):
        check_datas = {}
        for root in self.maya_scene_data.root_nodes:
            mesh_transforms = root.get_all_mesh_transform()
            
            check_datas.update(self.check_color_sets(mesh_transforms))
        
        error_nodes = []
        for node_name in check_datas:
            if check_datas[node_name] == False:
                error_nodes.append(node_name)
        
        if error_nodes:
            self.set_error_data(
                "wiz2_colorset_exists",
                error_nodes,
                error_message="カラーセットが存在しないノード"
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def count_color_sets(self,mesh: str) -> int:
        """
        指定したメッシュのカラーセットの数を返します。
        Args:
            mesh (str): カラーセットを調べたいメッシュの名前
        Returns:
            int: カラーセットの数
        """
        color_sets = cmds.polyColorSet(mesh, query=True, allColorSets=True)
        if color_sets:
            return len(color_sets)
        else:
            return 0
        
    def check_color_sets(self,meshes: list) -> dict:
        """
        各メッシュのカラーセット存在の有無を調べ、その結果を返します。
        Args:
            meshes (list): カラーセットを調べたいメッシュのリスト
        Returns:
            dict: キーがメッシュの名前、値がカラーセット存在の有無(bool)の辞書
        """
        result = {}
        for mesh in meshes:
            color_sets = cmds.polyColorSet(mesh, query=True, allColorSets=True)
            result[mesh] = bool(color_sets)
        return result