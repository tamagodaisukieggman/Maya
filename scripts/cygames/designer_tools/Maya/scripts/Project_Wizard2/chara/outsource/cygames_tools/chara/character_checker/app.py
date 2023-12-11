from . import wiz2_task  # taskのmodule読み込み(タスクを使用できるようにするため必須)
from ...common.maya_checker_gui import controller as checker_gui
from ...common.maya_checker import checker 
from . import utils as character_utils
from importlib import reload


def show_checker_gui():
    reload(checker_gui)
    checker_settings_data = character_utils._get_chr_checker_settings()
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

def get_character_checker():
    from ...common.maya_checker_gui.controller import CheckerMainWindow
    checker_settings_data = character_utils._get_chr_checker_settings()
    name = checker_settings_data["checker_name"]
    version = checker_settings_data["checker_ui_version"]
    helps = checker_settings_data["helps"]
    tools = checker_settings_data["tools"]
    tasks = checker_settings_data["tasks"]
    checker_settings = checker_settings_data["checker_settings"]
    post_process_settings = checker_settings_data["post_process_settings"]
    
    main_window = CheckerMainWindow(checker_name=name,
        checker_ui_version=version,
        helps=helps,
        tools=tools,
        tasks=tasks,
        checker_settings=checker_settings,
        post_process_settings=post_process_settings,)
    
    chceker = main_window.checker
    return chceker