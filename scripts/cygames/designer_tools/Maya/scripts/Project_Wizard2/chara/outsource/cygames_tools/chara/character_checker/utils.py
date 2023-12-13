import os
import yaml
import maya.cmds as cmds
from pathlib import Path
from ...common.maya_checker.scene_data import MayaSceneData


def get_scene_name_info():
    data = _get_chr_info_yaml_data()
    return data["scene_name_info"]


def get_character_info():
    data = _get_chr_info_yaml_data()
    return data["character_info"]


def _get_chr_info_yaml_data():
    yaml_path = get_chr_settings_directory() + "/chr_info.yaml"
    return _get_yaml_data(yaml_path)


def _get_yaml_data(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data


def _get_chr_checker_settings():
    yaml_path = get_chr_settings_directory() + "/character_checker.yaml"
    return _get_yaml_data(yaml_path)


def get_current_scene_info(maya_scene_data: MayaSceneData) -> dict:
    """シーン名からわかる情報をdictで返す

    Args:
        maya_scene_data (MayaSceneData): 情報もととなるscene_data

    Returns:
        dict: 現在開いているsceneの情報をdictで返す
    """
    scene_name_info = get_scene_name_info()

    scene_name = maya_scene_data.basename
    _player_type, _body_type, _parts_name = scene_name.split("_")

    result = {}

    result["player_type"] = scene_name_info["character_type"][_player_type[0]]

    result["gender_type"] = scene_name_info["gender_type"][int(_player_type[1])]

    result["body_type"] = scene_name_info["body_type"][_body_type]

    result["parts_name"] = _parts_name

    return result


def get_chr_settings_directory():
    """characterの設定階層を取得

    Returns:
        str: chr_settingsを取得
    """
    # 現在のスクリプトファイルのパスを取得
    current_file_path = Path(__file__).resolve(strict=True)

    # 一つ上の階層のパスを取得
    parent_directory = current_file_path.parent

    # 一つ上の階層にある "chr_settings" ディレクトリへのパスを取得
    chr_settings_directory = parent_directory / "wiz2_chr_settings"
    return str(chr_settings_directory)
