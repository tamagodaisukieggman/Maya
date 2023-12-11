# -*- coding: utf-8 -*-

import os
try:
    import yaml
except Exception:
    pass

from PySide2 import QtWidgets

from . import wiz2_env_task  # taskのmodule読み込み(タスクを使用できるようにするため必須)
from ...common.maya_checker_gui import controller as checker_gui
from ...common.maya_checker_gui.controller import CheckerMainWindow
from . import env_export


def show_checker_gui():
    yaml_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'wiz2_env_settings',
                                             'env_checker.yaml'))
    with open(yaml_path, 'r', encoding='utf-8') as yaml_file:
        checker_settings_data = yaml.safe_load(yaml_file)
        name = checker_settings_data['checker_name']
        version = checker_settings_data['checker_ui_version']
        helps = checker_settings_data['helps']
        tools = checker_settings_data['tools']
        tasks = checker_settings_data['tasks']
        checker_settings = checker_settings_data['checker_settings']
        window = checker_gui.show(
            checker_name=name,
            checker_ui_version=version,
            helps=helps,
            tools=tools,
            tasks=tasks,
            checker_settings=checker_settings
        )
        try:
            # checker commonのcontroller変更対応
            if CheckerMainWindow._instance:
                try:
                    CheckerMainWindow._instance.UI.btn_fbx_export
                except Exception:
                    CheckerMainWindow._instance.UI.btn_fbx_export = QtWidgets.QPushButton('FBXエクスポート')
                    CheckerMainWindow._instance.UI.vertical_custom_tool_layout.addWidget(CheckerMainWindow._instance.UI.btn_fbx_export)
                    CheckerMainWindow._instance.UI.btn_fbx_export.clicked.connect(lambda: env_export.export_fbx(CheckerMainWindow._instance.checker.root_objects))
        except Exception:
            if window:
                try:
                    window.UI.btn_fbx_export
                except Exception:
                    window.UI.btn_fbx_export = QtWidgets.QPushButton('FBXエクスポート')
                    window.UI.vertical_custom_tool_layout.addWidget(window.UI.btn_fbx_export)
                    window.UI.btn_fbx_export.clicked.connect(lambda: env_export.export_fbx(window.checker.root_objects))
