from . import wiz2_task  # taskのmodule読み込み(タスクを使用できるようにするため必須)
from ...common.maya_checker_gui import controller as checker_gui
from ...common.maya_checker.checker_factory import CheckerFactory 
from . import utils as character_utils
from importlib import reload


def _get_checker_settings(yaml_name:str):
    yaml_path = character_utils.get_chr_settings_directory() + "/" + yaml_name
    return character_utils._get_yaml_data(yaml_path)

def show_checker_gui(checker_type:str):
    reload(checker_gui)
    
    if checker_type == "chr":
        checker_settings_data = _get_checker_settings("character_checker.yaml")
    elif checker_type == "prp":
        checker_settings_data = _get_checker_settings("prop_checker.yaml")
    elif checker_type == "wep":
        checker_settings_data = _get_checker_settings("weapon_checker.yaml")
    elif checker_type == "enm":
        checker_settings_data = _get_checker_settings("enemy_checker.yaml")

    name = checker_settings_data["checker_name"]
    version = checker_settings_data["checker_ui_version"]
    helps = checker_settings_data["helps"]
    tools = checker_settings_data["tools"]
    tasks = checker_settings_data["tasks"]
    checker_settings = checker_settings_data["checker_settings"]
    post_process_settings = checker_settings_data["post_process_settings"]
    checker_gui.show(
        checker_name=name,
        checker_ui_version=version,
        helps=helps,
        tools=tools,
        tasks=tasks,
        checker_settings=checker_settings,
        post_process_settings=post_process_settings,
    )



def get_character_checker(roots):
    checker_settings_data = _get_chr_checker_settings()
    chceker = CheckerFactory.create(roots,checker_settings_data)
    return chceker