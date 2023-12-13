import typing as tp
from dataclasses import dataclass, field


@dataclass
class NodeData:
    """nodeDataの基底クラス"""
    root_node_name: str = field(default_factory=str)
    full_path_name: str = field(default_factory=str)
    short_name: str = field(default_factory=str)
    node_type: str = field(default_factory=str)
    extra_data: dict = field(default_factory=dict)

@dataclass
class RootNodeData(NodeData):
    """rootNode用のデータクラス"""
    all_descendents: list = field(default_factory=list)
    
    def get_all_mesh_transform(self) -> tp.List[str]:
        """meshを所有しているtransformを全て取得
        mayaでそのまま使えるように、nodeのlong名を配列で返す

        Returns:
            tp.List[str]: 全てのメッシュ名（long）
        """
        all_mesh = []
        for node in self.all_descendents:
            if node.node_type == "transform":
                if node.extra_data["has_shape"] == True:
                    all_mesh.append(node.full_path_name)
        return all_mesh

@dataclass
class DescendentsNodeData(NodeData):
    """rootNodeの子孫保持用のデータクラス"""
    deep: int = field(default_factory=int)
    
    

