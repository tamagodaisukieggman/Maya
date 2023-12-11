# -*- coding: utf-8 -*-
import typing as tp
import yaml
from pathlib import Path
import maya.cmds as cmds


def get_shapes(transforms: tp.List[str]) -> tp.List[str]:
    """トランスフォームの配列から各トランスフォームが所有するshapeを取得する関数

    Args:
        transforms (tp.List[str]): トランスフォーム名のリスト

    Returns:
        tp.List[str]: shape名の配列
    """
    shape_list = []
    for transform in transforms:
        shapes = cmds.listRelatives(transform, shapes=True, path=True)
        if shapes:
            shape_list.extend(shapes)
    return shape_list


def get_assigned_material(objects: tp.List[str]) -> tp.List[str]:
    """オブジェクトにアサインされているマテリアルを取得する関数

    Args:
        obj (str): オブジェクト名(shape)

    Returns:
        tp.Optional[str]: マテリアル名 (マテリアルが見つからない場合はNone)
    """

    materials = set()

    for obj in objects:
        shading_groups = cmds.listConnections(obj, type="shadingEngine")
        if not shading_groups:
            continue

        for sg in shading_groups:
            connected_materials = cmds.ls(cmds.listConnections(sg), materials=True)
            if connected_materials:
                materials.update(connected_materials)

        # フェースにアサインされているマテリアルを取得
        num_faces = cmds.polyEvaluate(obj, face=True)
        for i in range(num_faces):
            face = "{}.f[{}]".format(obj, i)
            shading_group = cmds.listConnections(face, type="shadingEngine")
            if shading_group:
                connected_material = cmds.ls(
                    cmds.listConnections(shading_group), materials=True
                )
                if connected_material:
                    materials.update(connected_material)

    return list(materials)


def get_file_nodes(material: str) -> tp.List[str]:
    """マテリアルにアサインされているすべてのfileノードを取得する関数

    Args:
        material (str): マテリアル名

    Returns:
        tp.List[str]: fileノード名のリスト
    """
    file_nodes = cmds.listConnections(material, type="file")
    return file_nodes if file_nodes else []


def get_bound_joints(obj: str) -> tp.List[str]:
    """対象のオブジェクトにバインドされているジョイントを配列で返す関数

    Args:
        obj (str): オブジェクト名

    Returns:
        tp.List[str]: バインドされているジョイント名のリスト
    """
    skin_clusters = cmds.ls(cmds.listHistory(obj), type="skinCluster")
    bound_joints = []
    if skin_clusters:
        for skin_cluster in skin_clusters:
            joints = cmds.skinCluster(skin_cluster, query=True, inf=True)
            bound_joints.extend(joints)
    return bound_joints


def get_default_settings_directory():
    """characterの設定階層を取得

    Returns:
        str: chr_settingsを取得
    """
    # 現在のスクリプトファイルのパスを取得
    current_file_path = Path(__file__).resolve(strict=True)

    # 一つ上の階層のパスを取得
    parent_directory = current_file_path.parent

    # 一つ上の階層にある "chr_settings" ディレクトリへのパスを取得
    chr_settings_directory = parent_directory / "default_settings"
    return str(chr_settings_directory)


def _get_yaml_data(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data


def _get_checker_settings():
    yaml_path = get_default_settings_directory() + "/checker_default_settings.yaml"
    return _get_yaml_data(yaml_path)
