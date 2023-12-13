from __future__ import annotations

from typing import Union
from pathlib import Path

import maya.cmds as cmds


def get_current_scene_info():
    "開いているシーンの各情報を取り出す"
    path = Path(cmds.file(q=True, sn=True))

    texture_dir = Path(str(path.parent.parent) + "/sourceimages")
    return {"file_path": path.parent, "file_name": path.stem, "tex_dir": texture_dir}


def get_texture_path_from_material(material: str) -> Union[str, None]:
    """
    対象のマテリアルからテクスチャのパスを取得します。

    Args:
        material (str): マテリアル名

    Returns:
        str, None: テクスチャのパスが存在する場合はそのパスを文字列で返し、存在しない場合はNoneを返します。
    """

    file_nodes = cmds.listConnections(material, type="file")
    if file_nodes is None:
        return None

    # ファイルノードからテクスチャのパスを取得
    for file_node in file_nodes:
        texture_path = cmds.getAttr(file_node + ".fileTextureName")
        if texture_path:
            return texture_path

    return None


def get_current_sourceimages_dir(material: str) -> any:
    texture_path = get_texture_path_from_material(material)
    if texture_path:
        sourceimages = find_sourceimages(texture_path)
        return sourceimages
    return None


def find_sourceimages(directory):
    path = Path(directory)
    for parent in path.parents:
        potential_sourceimages = parent / "sourceimages"
        if potential_sourceimages.exists() and potential_sourceimages.is_dir():
            return potential_sourceimages
    return None
