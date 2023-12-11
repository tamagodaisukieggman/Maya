import os
import typing as tp
from dataclasses import dataclass, field

import maya.cmds as cmds

from .node_data_factory import RootNodeDataFactory

@dataclass
class MayaSceneDataBase:
    """
    name: シーン名
    basename: 拡張子を抜かしたファイル名
    root_nodes: ルートノード
    ext: 拡張子
    """
    name: str = field(default_factory=str)
    basename: str = field(default_factory=str)
    root_nodes: list = field(default_factory=list)
    ext: str = field(default_factory=str)


class MayaSceneData(MayaSceneDataBase):
    """Maya シーン情報
    """
    def __init__(self,root_objects:tp.List[str] = []) -> None:
        super().__init__()
        self.root_objects = root_objects
        self.set_scene_name()
        self.set_root_node_datas()
        

    def set_scene_name(self) -> None:
        _name = cmds.file(q=True,sn=True)
        if _name:
            basename = os.path.basename(_name)
            _base_name, _ext = os.path.splitext(basename)
            self.basename = _base_name
            self.name = _name
            self.ext = _ext
    
    def set_root_node_datas(self) -> list:
        root_nodes:list = self._get_current_root_node_datas()
        if not root_nodes:
            return
        self.root_nodes = root_nodes

    # TODO: anyを作成したクラスに編集
    def _get_current_root_node_datas(self) -> tp.List[any]:
        """ルートノード群の情報を取得して返す"""
        # TODO: 選択をベースにするか、シーン内すべてのルートをとるか選択できるようにする
        selected = []
        if len(self.root_objects) > 0:
            selected = self.root_objects
        # else:
        #     selected = cmds.ls(sl=True)
        root_node_datas = []
        for select_node in selected:

            root_node_data = RootNodeDataFactory.create(select_node)
            root_node_datas.append(root_node_data)

        return root_node_datas
        

    def get_check_target(self) -> list:
        """チェックの対象となるルートノード取得

        Returns:
            list: _description_
        """
        return self.nodes
