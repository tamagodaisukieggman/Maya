import os
import yaml
import typing as tp

from .data import EdgeSetType


import maya.cmds as cmds
import maya.mel as mel

from ..chara_rebinder.bind_rebind import BindSkinCmd


class EdgeSetTools:
    def __init__(self, edge_set_type: EdgeSetType):
        self.edge_set_type = self._get_edge_set_type_str(edge_set_type)
        if not edge_set_type:
            raise ("有効なEdgeSetTypeが与えられていません")

        self.set_name = f"{edge_set_type.name.lower()}_edge_sets"

    def create_edge_set(self):
        """edge setの作成,追加の場合もこの関数を使用"""
        selected_edges = self._get_selected_edge()

        if not cmds.objExists(self.set_name):
            cmds.sets(name=self.set_name)

        # エッジをセットに追加します
        cmds.sets(selected_edges, add=self.set_name)

    def remove_edge_set(self):
        """選択したエッジをセットから除去"""
        selected_edges = self._get_selected_edge()
        if not cmds.objExists(self.set_name):
            raise ValueError(f"'{self.set_name}' は存在しません")

        # エッジをセットから除去します
        cmds.sets(selected_edges, remove=self.set_name)

    def delete_edge_set(self):
        cmds.delete(self.set_name)

    def select_sets_member(self):
        members = cmds.sets(self.set_name, query=True)
        cmds.select(members, r=True)

    def get_current_yaml_path(self):
        player_type = get_player_type()
        yaml_name = f"{player_type}_{self.edge_set_type}.yaml"
        file_path = __file__.rsplit("\\", 1)[0]
        file_path = f"{file_path}\\settings\\"
        yaml_path = file_path + yaml_name
        return yaml_path

    def _get_edge_set_type_str(self, edge_set_type):
        """現在のedgeセット名を返す

        Returns:
            str: edgeセット名
        """
        prefix = None
        prefix = edge_set_type.name.lower()
        return prefix

    def _get_selected_edge(self) -> tp.List[str]:
        """選択edgeを返す

        Returns:
            _type_: _description_
        """
        selection = cmds.ls(selection=True)
        selected_edges = cmds.filterExpand(selection, expand=True, selectionMask=32)
        return selected_edges

    def _remove_selected_edges_from_set(self, set_name):
        """
        選択したエッジを指定したセットから除去します。
        Args:
            set_name (str): セットの名前
        Raises:
            ValueError: セットが存在しないまたは選択しているオブジェクトがエッジでない場合
        """
        # セットが存在しない場合はエラーを発生させます
        if not cmds.objExists(set_name):
            raise ValueError(f"Set '{set_name}' does not exist")

        # 選択しているエッジを取得します
        selection = cmds.ls(selection=True)
        selected_edges = cmds.filterExpand(selection, expand=True, selectionMask=32)

        # 選択がエッジでなければエラーを発生させます
        if not selected_edges:
            raise ValueError("Selected objects are not edges")

        # エッジをセットから除去します
        cmds.sets(selected_edges, remove=set_name)

    def _get_set_members(self):
        """
        指定したセットに含まれるオブジェクトを取得

        Args:
            set_name (str): 対象のセット名

        Returns:
            list: セットに含まれるメンバーオブジェクトのリスト
        """
        return cmds.sets(self.set_name, query=True)

    def get_vertices_from_edges(self, edges):
        """
        指定したエッジが含む頂点を取得
        Args:
            edges (list): 対象のエッジ名のリスト
        Returns:
            dict: 各エッジに含まれる頂点のリストを値とした辞書
        """
        edge_to_vertices = []
        for edge in edges:
            vertex_info = cmds.polyInfo(edge, edgeToVertex=True)
            if vertex_info is not None:
                for lp in vertex_info:
                    # "EDGE 0: 33 34\n" のような形式の文字列を整形
                    if "Hard" in lp:
                        lp = lp.replace("Hard", "")

                    vertices = lp.split(":")[1].split()
                    # フルパスの頂点名に変換
                    vertices = [
                        edge.rsplit(".", 1)[0] + ".vtx[" + v + "]" for v in vertices
                    ]
                    edge_to_vertices.extend(vertices)
        return list(set(edge_to_vertices))

    def get_current_and_close_vertex_info(self, vertices):
        yaml_path = self.get_current_yaml_path()
        saved_vertex_info = load_vertex_info(yaml_path)
        skin_clusters = self.get_current_skin_clusters(vertices)

        current_vertex_info = {}
        closest_vertex_info = {}

        for vertex in vertices:
            current_vertex_info.update(get_vertex_info(skin_clusters, vertex))
            current_closest_vertex_info = self.find_closest_vertex_info(
                vertex, saved_vertex_info
            )
            closest_vertex_info[vertex] = current_closest_vertex_info
        return current_vertex_info, closest_vertex_info

    def get_current_skin_clusters(self, vertices):
        skin_clusters = set(
            cmds.listHistory(vertices, future=False, pruneDagObjects=True)
        )
        skin_clusters = [
            node for node in skin_clusters if cmds.nodeType(node) == "skinCluster"
        ]

        return skin_clusters

    def find_closest_vertex_info(self, vertex, vertex_info):
        """指定した頂点に最も近い頂点とその情報を探す
        Args:
            vertex (str):対象の頂点名
            vertex_info (dict):頂点情報の辞書
        Returns:
            dict: 対象頂点に最も近い頂点の情報
        """
        target_position = cmds.pointPosition(vertex)
        closest_vertex = min(
            vertex_info,
            key=lambda v: sum(
                (p1 - p2) ** 2
                for p1, p2 in zip(target_position, vertex_info[v]["position"])
            ),
        )
        return vertex_info[closest_vertex]


class EdgeSetModifier:
    def __init__(self, edge_set_type: EdgeSetType):
        if not edge_set_type:
            raise ("有効なEdgeSetTypeが与えられていません")
        self.edge_set_tools = EdgeSetTools(edge_set_type)
        self.edge_set_checker = EdgeSetChecker(edge_set_type)

    def set_default_value_to_edge(self):
        if not cmds.objExists(self.edge_set_tools.set_name):
            raise ValueError(f"'{self.edge_set_tools.set_name}' は存在しません")

        vertices = self.edge_set_checker.get_no_match_vertices()

        yaml_path = self.edge_set_tools.get_current_yaml_path()

        target_objects = []

        print("weightの処理")
        if vertices["weight"]:
            for vertex in vertices["weight"]:
                self.apply_vertex_weights(vertex, yaml_path.replace("\\", "/"))
            target_objects.extend(get_object_names_from_vertices(vertices["weight"]))

        print("normalの処理")
        if vertices["normal"]:
            for vertex in vertices["normal"]:
                self.apply_vertex_normal(vertex, yaml_path.replace("\\", "/"))
            target_objects.extend(get_object_names_from_vertices(vertices["normal"]))

        print("positionの処理")
        if vertices["position"]:
            for vertex in vertices["position"]:
                self.apply_vertex_position(vertex, yaml_path.replace("\\", "/"))
            target_objects.extend(get_object_names_from_vertices(vertices["position"]))

        target_objects = list(set(target_objects))
        BindSkinCmd.rebind_targets(target_objects, is_result=False)
        if target_objects:
            cmds.select(target_objects, r=True)
            mel.eval('doBakeNonDefHistory( 1, {"prePost"});')

    def apply_vertex_position(self, vertex: str, vertex_info_file: str):
        """頂点を指定した位置に移動し、法線を適用する
        Args:
            vertex (str): 対象の頂点名
            vertex_info_file (str):頂点情報を含むyamlファイルのパス
        """
        # yamlファイルから頂点情報をロードします
        vertex_info = load_vertex_info(vertex_info_file)

        # 最も近い頂点の情報を取得します
        closest_info = self.edge_set_tools.find_closest_vertex_info(vertex, vertex_info)

        current_position = get_vertex_position_and_normal(vertex)[vertex]["position"]

        if not compare_xyz(closest_info["position"], current_position):
            # 対象頂点を最も近い頂点の位置に移動します
            cmds.xform(vertex, translation=closest_info["position"], worldSpace=True)

    def apply_vertex_normal(self, vertex: str, vertex_info_file: str):
        # yamlファイルから頂点情報をロードします
        vertex_info = load_vertex_info(vertex_info_file)

        # 最も近い頂点の情報を取得します
        closest_info = self.edge_set_tools.find_closest_vertex_info(vertex, vertex_info)

        current_normal = get_vertex_position_and_normal(vertex)[vertex]["normal"]

        if not compare_xyz(closest_info["normal"][0], current_normal[0]):
            # 対象頂点に最も近い頂点の法線を適用します
            cmds.polyNormalPerVertex(vertex, normalXYZ=closest_info["normal"][0])

    def apply_vertex_weights(self, vertex, vertex_info_file):
        if "p1_f_sotai01.vtx[252]" in vertex:
            print("test")

        # yamlファイルから頂点情報をロード
        vertex_info = load_vertex_info(vertex_info_file)

        # 最も近い頂点の情報を取得
        closest_info = self.edge_set_tools.find_closest_vertex_info(vertex, vertex_info)

        skin_clusters = cmds.ls(cmds.listHistory(vertex), type="skinCluster")
        values = []

        for skin_cluster in skin_clusters:
            for influence in closest_info["weight"]:
                current_vertex_info = get_vertex_info(skin_clusters, vertex)

                current_weight = current_vertex_info[vertex]["weight"][influence]
                if compare_float(current_weight, closest_info["weight"][influence]):
                    values.append((influence, 0.0))
                    continue

                values.append((influence, closest_info["weight"][influence]))

            print(f"{vertex}の{influence}の処理を開始")
            print(values)
            cmds.skinPercent(
                skin_cluster,
                vertex,
                normalize=False,
                zeroRemainingInfluences=True,
                transformValue=values,
            )


class EdgeSetChecker:
    def __init__(self, edge_set_type: EdgeSetType):
        if not edge_set_type:
            raise ("有効なEdgeSetTypeが与えられていません")
        self.edge_set_tools = EdgeSetTools(edge_set_type)

    def get_no_match_vertices(self):
        """一致しない頂点を取得

        Returns:
            dict: 一致しない頂点を返す
        """
        edges = self.edge_set_tools._get_set_members()
        vertices = self.edge_set_tools.get_vertices_from_edges(edges)

        (
            current_vertex_info,
            closest_vertex_info,
        ) = self.edge_set_tools.get_current_and_close_vertex_info(vertices)

        position_result = self.check_position(current_vertex_info, closest_vertex_info)
        normal_result = self.check_normal(current_vertex_info, closest_vertex_info)
        weight_result = self.check_weight(current_vertex_info, closest_vertex_info)

        no_match_position_vertices = self.get_no_match_vertex(position_result)
        no_match_normal_vertices = self.get_no_match_vertex(normal_result)
        no_match_weight_vertices = self.get_no_match_vertex(weight_result)

        no_match_vertices = {
            "position": no_match_position_vertices,
            "normal": no_match_normal_vertices,
            "weight": no_match_weight_vertices,
        }

        return no_match_vertices

    def get_no_match_vertex(self, result):
        no_match_vertices = []
        for vertex_name in result:
            if not result[vertex_name]:
                no_match_vertices.append(vertex_name)
        return no_match_vertices

    def check_position(self, current_vertex_info: dict, closest_vertex_info: dict):
        """頂点のポジションを比較し、頂点の情報が正しいかどうか確認

        Args:
            current_vertex_info (dict): 現在の対象の頂点の情報
            closest_vertex_info (dict): 頂点に一番近い頂点の情報

        Returns:
            dict: 一致しているかどうかのフラグ
        """
        vertex_info = {}
        for vertex in current_vertex_info:
            current_info = current_vertex_info[vertex]
            closest_info = closest_vertex_info[vertex]

            are_positions_equal = compare_xyz(
                current_info["position"], closest_info["position"]
            )
            vertex_info.update({vertex: are_positions_equal})
        return vertex_info

    def check_normal(self, current_vertex_info: dict, closest_vertex_info: dict):
        """頂点の法線を比較し、頂点の情報が正しいかどうか確認

        Args:
            current_vertex_info (dict): 現在の対象の頂点の情報
            closest_vertex_info (dict): 頂点に一番近い頂点の情報

        Returns:
            dict: 各頂点が一致しているかどうかのフラグ
        """
        vertex_info = {}
        for vertex in current_vertex_info:
            current_info = current_vertex_info[vertex]
            closest_info = closest_vertex_info[vertex]

            are_normals_equal = True
            for current_normal, closest_normal in zip(
                current_info["normal"], closest_info["normal"]
            ):
                are_normals_equal = True
                if not compare_xyz(current_normal, closest_normal):
                    are_normals_equal = False
                    break
            vertex_info.update({vertex: are_normals_equal})
        return vertex_info

    def check_weight(self, current_vertex_info: dict, closest_vertex_info: dict):
        """頂点のウエイトを比較し、頂点の情報が正しいかどうか確認

        Args:
            current_vertex_info (dict): 現在の対象の頂点の情報
            closest_vertex_info (dict): 頂点に一番近い頂点の情報

        Returns:
            dict: 各頂点が一致しているかどうかのフラグ
        """
        vertex_info = {}
        for vertex in current_vertex_info:
            is_weight_equal = True
            current_info = current_vertex_info[vertex]
            closest_info = closest_vertex_info[vertex]
            if vertex == "p1_f_sotai01.vtx[256]":
                print(vertex)
            for joint_name in current_info["weight"]:
                if joint_name in closest_info["weight"]:
                    is_valid_weight = compare_float(
                        current_info["weight"][joint_name],
                        closest_info["weight"][joint_name],
                    )

                    if not is_valid_weight:
                        is_weight_equal = False
                        break
                else:
                    is_weight_equal = False

            vertex_info.update({vertex: is_weight_equal})
        return vertex_info


class EdgeSetDataExporter:
    @staticmethod
    def extract_vertex_info():
        """選択した頂点から位置情報と法線情報を抽出する
        Returns:
            dict: 頂点名をキー、位置情報と法線情報を値とした辞書
        """
        vertices = cmds.filterExpand(sm=31)
        if not vertices:
            raise ValueError("No vertices selected")

        info = {}

        skin_clusters = set(
            cmds.listHistory(vertices, future=False, pruneDagObjects=True)
        )
        skin_clusters = [
            node for node in skin_clusters if cmds.nodeType(node) == "skinCluster"
        ]

        # 頂点位置と法線の書き出し
        for vertex in vertices:
            info.update(get_vertex_info(skin_clusters, vertex))
        return info

    @classmethod
    def export_vertex_info_to_yaml(cls, yaml_file):
        """選択した頂点の情報をyamlファイルに出力する
        Args:
            yaml_file (str):出力ファイルのパス
        """
        info = cls.extract_vertex_info()
        with open(yaml_file, "w") as f:
            yaml.dump(info, f)
            print(f"complete >> {yaml_file}")

    @classmethod
    def export_edge_set_data(cls, edge_set_type: EdgeSetTools):
        edge_set_tools = EdgeSetTools(edge_set_type)
        yaml_path = edge_set_tools.get_current_yaml_path()
        cls.export_vertex_info_to_yaml(yaml_path)


def load_vertex_info(yaml_file):
    """yamlファイルから頂点情報をロードする
    Args:
        yaml_file (str): 入力ファイルのパス
    Returns:
        dict: yamlファイルからロードした頂点情報
    """
    with open(yaml_file, "r") as f:
        info = yaml.safe_load(f)
    return info


def get_vertex_info(skin_clusters: tp.List[str], vertex: str):
    """頂点とスキンクラスターから頂点の各情報を取得

    Args:
        skin_clusters (tp.List[str]): スキンクラスタ
        vertex (str): 頂点名

    Returns:
        info: 頂点の持つ位置情報、法線情報　ウエイト情報を返す
    """

    weights = {}
    info = {vertex: {"position": {}, "normal": {}, "weight": {}}}
    position_and_normal_info = get_vertex_position_and_normal(vertex)

    if position_and_normal_info:
        info.update(position_and_normal_info)

    for skin in skin_clusters:
        influence_list = cmds.skinCluster(skin, query=True, inf=True)
        weights_per_vertex_per_skin = cmds.skinPercent(
            skin, vertex, query=True, value=True
        )
        try:
            skin_weights = {
                inf: wgt
                for inf, wgt in zip(influence_list, weights_per_vertex_per_skin)
            }
            weights.update(skin_weights)

        except TypeError:
            continue
    info[vertex].update({"weight": weights})
    return info


def get_vertex_position_and_normal(vertex: str):
    info = {}
    position = cmds.pointPosition(vertex)
    normal = cmds.polyNormalPerVertex(vertex, query=True, xyz=True)
    normal = [normal[i : i + 3] for i in range(0, len(normal), 3)]

    info = {vertex: {"position": position, "normal": normal}}
    return info


def get_current_scene_name():
    """
    現在開いているシーンの名前を取得
    Returns:
        str: 開いているシーンの名前（フルパスでなく、拡張子なし）
    """
    # 現在のシーンのフルパスを取得
    full_path = cmds.file(query=True, sceneName=True)
    # ディレクトリパスを削除してファイル名だけにし（os.path.basename）、
    # その後、拡張子を削除（os.path.splitext）
    scene_name = os.path.splitext(os.path.basename(full_path))[0]
    return scene_name


def get_player_type():
    """シーン名からプレイヤーの種別を取得

    Returns:
        str: "p1" or "p2"
    """
    scene_name = get_current_scene_name()
    player_type = None

    if scene_name.startswith("p1") or scene_name.startswith("p0"):
        player_type = "p1"
    elif scene_name.startswith("p2"):
        player_type = "p2"
    return player_type


def get_object_names_from_vertices(vertices):
    """
    対象の頂点が属するオブジェクト名をリストで返す
    Args:
        vertices (list): 頂点名のリスト
    Returns:
        list: 頂点が属するオブジェクト名のリスト
    """
    return list(set([vertex.rsplit(".", 1)[0] for vertex in vertices]))


def compare_xyz(xyz1, xyz2, tolerance=0.0001):
    """
    指定された2つの頂点位置が一致しているかをcheckする
    Args:
        xyz1 (list): 頂点位置1 [x, y, z]
        xyz2 (list): 頂点位置2 [x, y, z]
        tolerance (float): 誤差範囲
    Returns:
        bool: 位置が一致していればTrue、そうでなければFalse
    """
    for coord1, coord2 in zip(xyz1, xyz2):
        if abs(coord1 - coord2) > tolerance:
            return False
    return True


def compare_float(value1, value2, tolerance=0.001):
    """
    指定された2つのfloatが一致しているかをcheckする
    Args:
        value1 (float):
        value2 (float):
        tolerance (float): 誤差範囲
    Returns:
        bool: floatが一致していればTrue、そうでなければFalse
    """
    if abs(value1 - value2) > tolerance:
        return False
    else:
        return True
