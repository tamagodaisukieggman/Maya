# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from pathlib import Path
import time
import importlib

from PySide2 import QtCore

from maya import cmds

from ...utils import gui_util
from . import data
from . import utils
from . import scene_data
from . import pyside_gui
from . import setting
from . import logger

HERE = Path(os.path.dirname(os.path.abspath(__file__)))

DEV_MODE = setting.load_config(config_name='DEV_MODE')
if DEV_MODE:
    importlib.reload(data)
    importlib.reload(utils)
    importlib.reload(scene_data)
    importlib.reload(pyside_gui)
    importlib.reload(setting)


def maya_scene_check(lower_drive_letter:bool, _execute_check_modules:list, set_category:str):
    check_start_str = 'Check Start'

    _start_time = time.time()

    maya_scene_data:scene_data.MayaSceneData = scene_data.MayaSceneData()
    check_result:data.CheckResultData = data.CheckResultData()

    check_target_str = 'Check Target Root Nodes'
    # チェッカーモジュール取得
    checker_modules:list = utils.get_chckermodules()
    if not checker_modules:
        if not DEV_MODE:
            logger.warning('Not Found Checker Modules')
        cmds.warning('Not Found Checker Modules')
        return check_result, maya_scene_data
    # Maya データ取得

    if not maya_scene_data.scene_name:
        if not DEV_MODE:
            logger.warning('Not Open Maya Scene')
        cmds.warning('Not Open Maya Scene')
        return check_result, maya_scene_data

    # プロジェクトデータ設定
    project_settings:data.ProjectSettings = utils.get_project_settings(
                                                                scene_path=maya_scene_data.scene_name,
                                                                lower_drive_letter=lower_drive_letter
                                                                )


    # シーンデータにプロジェクト設定を反映させる
    maya_scene_data.project_setting = project_settings

    if set_category:
        maya_scene_data.current_category = set_category

    check_result:data.CheckResultData = data.CheckResultData()

    current_scene_path = maya_scene_data.name

    current_projyect = maya_scene_data.project
    current_category = maya_scene_data.current_category

    if not DEV_MODE:
        logger.info(f'Project: {current_projyect} {current_scene_path}')
        logger.info(f'Data Category: {current_category}')

    log_message = f'{current_projyect}\n'
    log_message += f'{current_scene_path}\n'
    log_message += f'{current_category}\n'

    # シーンデータにプロジェクト設定を反映させる
    maya_scene_data.project_setting = project_settings

    # senjin 仕様、mdl_ で始まるルートノードを対象とする
    if lower_drive_letter:
        maya_scene_data.extract_check_root_node_start_names_mdl()

    # チェック開始
    print('\n\n')

    _message:str = utils.check_data(
                    execute_check_module = _execute_check_modules,
                    check_modules = checker_modules,
                    maya_scene_data = maya_scene_data,
                    check_result = check_result,
                    project_settings = project_settings,
                    )

    print(f'{check_start_str:-^100}')

    if not maya_scene_data.nodes:
        print(f'{check_target_str}: No Target Nodes ... ')
    else:
        print(f'{check_target_str}: {len(maya_scene_data.nodes): ^4} {[x.node_name for x in maya_scene_data.nodes]}')

    # チェッカーに不備があればエラーの文字列が返ってくる
    if _message and not DEV_MODE:
        logger.error(_message)
        return check_result, maya_scene_data
    else:
        if check_result:
            if check_result.result_datas:
                for check, result in check_result.result_datas.items():
                    result:data.ResultData = result
                    if not DEV_MODE and result.error_nodes:
                        logger.info(f'{check} error: {len(result.error_nodes)}')
                    log_message += f'{check} error: {len(result.error_nodes)}\n'
            if check_result.all_result_count:
                log_message += f'total error: [{check_result.all_result_count}]'

    if DEV_MODE:
        print(log_message)

    calc_time = time.time() - _start_time
    print(f'{calc_time:->100} sec.')
    print('\n\n')

    return check_result, maya_scene_data

def main(is_cyllista: bool = False, set_category : str = ''):
    open_cyllista_exporter_window:bool = False
    lower_drive_letter:bool = False

    if is_cyllista:
        open_cyllista_exporter_window:bool = True
        lower_drive_letter:bool = True

    if not DEV_MODE:
        logger.send_launch(f'Launch')
    # チェッカーモジュール取得
    CHECKER_GUI_NAME = setting.load_config('CHECKER_GUI_NAME')
    CHECKER_RESULT_GUI_NAME = setting.load_config('CHECKER_RESULT_GUI_NAME')
    gui_util.close_pyside_windows([CHECKER_GUI_NAME,
                                   CHECKER_RESULT_GUI_NAME,
                                   ])

    # テストでモジュールを限定したい時はここに書く
    _execute_check_modules:list = ['texture', 'material']
    _execute_check_modules:list = ['transform']
    _execute_check_modules:list = []

    # チェック実行
    _return_data = maya_scene_check(lower_drive_letter=lower_drive_letter, _execute_check_modules=_execute_check_modules, set_category=set_category)
    check_result:data.CheckResultData = _return_data[0]
    maya_scene_data:scene_data.MayaSceneData = _return_data[1]

    if check_result.result_datas:
        if check_result.all_result_count:
            _gui = pyside_gui.CheckerGUI(name = set_category)
            _gui.setTableData(check_result=check_result,
                            maya_scene_data=maya_scene_data,
                            )
            _gui.show()
        else:
            _d = gui_util.ConformDialog(title="Not Fond Error",
                                        message="Not Found Error")
            _d.exec_()
            if open_cyllista_exporter_window:
                utils.open_cyllista_export_window()
