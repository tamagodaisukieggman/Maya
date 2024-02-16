import typing as tp
import functools
import maya.cmds as cmds

from .. import utils
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.data import ErrorType
from ....common.maya_checker.common_task.weight_task import BoundJoint
from ....common.maya_checker.node_data import RootNodeData , NodeData


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
                "wiz2_poly_count",
                None,
                f"{body_type} には現在このチェックは対応しておりません。{body_type} のポリゴン最大数は{current_max_count}です。手動で確認をお願いいたします。",
            )
            return

        self.reset_debug_data()
        self.set_error_type(ErrorType.NOERROR)

        print("poly_count_debug_data:")
        for i,root_node in enumerate(self.maya_scene_data.root_nodes):
            has_error, debug_datas = self.get_check_poly_count_results(current_max_count,root_node)
            
            for ii,debug_data in enumerate(debug_datas):
                total_polygon = debug_data["total_poly_count"]

                print(debug_data)

                if has_error == True:
                    self.error_type = ErrorType.WARNING
                    self.set_error_data(
                        f"wiz2_poly_count_{str(i)+'-'+str(ii)}",
                        str(debug_data["check_targets"]),
                        f"{body_type} の規定ポリゴン数({current_max_count}tris)を超えています\n現在の合計ポリゴン数は{total_polygon}tris です。",
                        is_reset_debug_data=False,
                    )
                else :
                    self.error_type = ErrorType.NOERROR
                    self.set_error_data(
                        error_name=f"wiz2_poly_count_{str(i)+'-'+str(ii)}",
                        target_objects=[""],
                        error_message=f"{body_type} の規定ポリゴン数({current_max_count}tris)内です\n詳細はスクリプトエディタを参照ください",
                        is_reset_debug_data=False,
                    )

    def get_check_poly_count_results(self, current_max_count,root):
        target_node_datas = self.get_dif_node_datas(root)

        target_node_datas.extend(self.get_not_dif_node_datas(root))

        has_error = False

        debug_datas = []
        for target_node_data in target_node_datas:
            check_targets = target_node_data["target_nodes"]
            check_targets.extend(target_node_data["alpha_nodes"])
            is_valid_polycount,total_poly_count = Wiz2PolyCount.check_poly_count(
                check_targets, current_max_count
            )

            debug_data = {"has_error":not is_valid_polycount,"check_targets":check_targets,"total_poly_count":total_poly_count}

            if not is_valid_polycount:
                has_error = True
            debug_datas.append(debug_data)

        return has_error,debug_datas

    def get_check_poly_count_results_for_multroot(self, current_max_count,roots):
        target_node_datas = []
        for root in roots:
            target_node_datas.extend(self.get_dif_node_datas(root))
            target_node_datas.extend(self.get_not_dif_node_datas(root))

        has_error = False
        debug_datas = []
        check_targets = []
        for target_node_data in target_node_datas:
            check_targets.extend(target_node_data["target_nodes"])
            check_targets.extend(target_node_data["alpha_nodes"])
        is_valid_polycount,total_poly_count = Wiz2PolyCount.check_poly_count(
            check_targets, current_max_count
        )

        debug_data = {"has_error":not is_valid_polycount,"check_targets":check_targets,"total_poly_count":total_poly_count}

        if not is_valid_polycount:
            has_error = True
        debug_datas.append(debug_data)

        return has_error,debug_datas
    

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
                return False,total_poly_count

        if total_poly_count > max_poly_count:
            return False,total_poly_count

        return True,total_poly_count

    def get_deep_1_mesh_node_list(self,root_node:RootNodeData) -> tp.List[NodeData]:
        deep_1_list = [node for node in root_node.all_descendents if node.deep == 1 and node.node_type == "transform"]
        # has shapeのトランスフォームのみ対象とする
        deep_1_list = [node for node in deep_1_list if node.extra_data["has_shape"]]
        return deep_1_list

    def get_base_node_list(self,root_node:RootNodeData) -> tp.List[NodeData]:
        """指定のroot以下の_baseのNodeDataを返す

        Args:
            root_node (RootNodeData): 対象のRoot

        Returns:
            tp.List[NodeData]: ノードのリスト
        """
        deep_1_list = self.get_deep_1_mesh_node_list(root_node)
        base_node_list = []

        # _baseがsuffixになっているメッシュを取得
        for node in deep_1_list:
            if node.short_name.endswith("_base"):
                base_node_list.append(node)
        return base_node_list
    
    def get_not_dif_node_datas(self,root_node:RootNodeData) -> tp.List[list]:
        """指定のroot以下の差分以外の調査対象のデータを返す

        Args:
            root_node (RootNodeData): 対象のRoot

        Returns:
            tp.List[dict]: チェック対象の情報を収めたdictを配列で返す
        """
        deep_1_list = self.get_deep_1_mesh_node_list(root_node)
        base_name_list = []

        # _baseがsuffixになっているメッシュを取得
        for node in deep_1_list:
            if node.short_name.endswith("_base"):
                base_name_list.append(node.short_name)

        target_node_list = deep_1_list.copy()
        # 対象外のノードを除外
        for suffix in ["_base","_Outline"]:
            target_node_list = [node for node in target_node_list if not node.short_name.endswith(suffix)]

        has_alpha_node_list = [node for node in target_node_list if utils.check_alpha(node.short_name)]
        target_node_list = [node for node in target_node_list if not utils.check_alpha(node.short_name)]
        
        exclution_name_list = [] 

        # baseのchara_idを含むオブジェクトをすべて除外
        for base_name in base_name_list:
            character_id =base_name.split("_base")[0]
            for node in target_node_list:
                if node.short_name.startswith(character_id):
                    exclution_name_list.append(node.full_path_name)
        
        not_dif_node_list = []
        for node in target_node_list:
            if node.full_path_name not in exclution_name_list:
                alpha_nodes = [alpha_node.full_path_name for alpha_node in has_alpha_node_list if alpha_node.short_name.startswith(node.short_name)]
                not_dif_data = {"chr_id":node.short_name,"target_nodes":[node.full_path_name],"alpha_nodes":alpha_nodes}
                not_dif_node_list.append(not_dif_data)
        return not_dif_node_list

    def get_dif_node_datas(self,root_node:RootNodeData) -> tp.List[dict]:
        """差分のノードの情報を配列で返す

        Args:
            root_node (RootNodeData): 親階層の指定

        Returns:
            tp.List[dict]: チェック対象の情報を収めたdictを配列で返す
        """
        base_node_list = self.get_base_node_list(root_node)
        temp_dif_data_list = []

        # 差分メッシュの取得
        for base_node in base_node_list: 
            character_id = base_node.short_name.replace("_base", "")
            dif_data = {"chr_id":character_id,"base_node":base_node.full_path_name,"dif_nodes":[],"alpha_nodes":[]}

            deep_1_list = self.get_deep_1_mesh_node_list(root_node)
            target_node_list = deep_1_list.copy()
            
            # 対象外のノードを除外
            for suffix in ["_base","_Outline"]:
                target_node_list = [node for node in target_node_list if not node.short_name.endswith(suffix)]
            
            for node in target_node_list:
                # alphaメッシュの登録
                if character_id in node.short_name:
                    if utils.check_alpha(node.short_name):
                        dif_data["alpha_nodes"].append(node.full_path_name)
                    
                    # alpha以外は差分ノードの想定
                    else:
                        dif_data["dif_nodes"].append(node.full_path_name)
            temp_dif_data_list.append(dif_data)

        dif_data_list = []
        for dif_data in temp_dif_data_list:
            for dif_node_name in dif_data["dif_nodes"]:
                alpha_nodes = [node for node in dif_data["alpha_nodes"] if dif_node_name in node ]
                alpha_nodes_base = [node for node in dif_data["alpha_nodes"] if dif_data["base_node"] in node]
                alpha_nodes.extend(alpha_nodes_base)
                fixed_dif_data = {"chr_id":dif_data["chr_id"],"target_nodes":[dif_data["base_node"],dif_node_name],"alpha_nodes":alpha_nodes}
                dif_data_list.append(fixed_dif_data)
        
        return dif_data_list

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