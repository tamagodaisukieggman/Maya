# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
import time
import importlib

from PySide2.QtCore import Qt
from PySide2 import QtCore, QtGui, QtWidgets

import tool_log
from ...utils import gui_util

from . import scene_data
from . import settings
from . import pyside_gui
from . import tool_version
from . import TITLE

# 開発中はTrue、リリース時にFalse
DEV_MODE = settings.load_config(config_name='DEV_MODE')
if DEV_MODE:
    importlib.reload(gui_util)
    importlib.reload(settings)
    importlib.reload(scene_data)
    importlib.reload(pyside_gui)


class Checker:
    def __init__(self)->None:
        self.memory_clear()
        self.load_checker()

    def memory_clear(self)->None:
        self.scene_path = scene_data.SceneData()
        self.node_datas = scene_data.NodeDatas()
        self.result = scene_data.ResultDatas()
        self._cheker_files = {}

    def _send_log(self):
        logger = tool_log.get_logger(tool_title=TITLE, tool_version=tool_version)
        logger.send_launch("")

    def do_check(self)->None:
        project_name = settings.load_config('PROJRCT_NAME')

        # シーンが開かれていない場合エラー
        if not self.scene_path:
            _d = gui_util.ConformDialog(title="No Maya Scene",
                                        message="Open Scene File")
            _d.exec_()
            return

        # 開いているシーンが想定されていない場合のエラー
        # if not self.scene_path.data_type_category:
        #     _d = gui_util.ConformDialog(title="Not Shenron Path",
        #                                 message="This scene is not a project scene.")
        #     _d.exec_()
        #     return

        _start_time = time.time()

        checker_count = 0
        for k,v in self._cheker_files.items():
            checker_count += len(v)
        _length = checker_count
        progress = None

        self._send_log()

        if not self.scene_path.is_batch:
            progress = gui_util.ProgressDialog()
            progress.setUp(maxValue=_length, title=f"check :")
            progress.show()
        count = 0

        for checker_category, checkers in self._cheker_files.items():
            if checker_category == "component":
                check_targets = [self.node_datas.all_meshes]
            else:
                check_targets = [self.node_datas.root_nodes]

            for checker in checkers:
                for check_target in check_targets:
                    command = str(self.create_check_python_command(
                                                    data_type_category=self.scene_path.data_type_category,
                                                    checker_category=checker_category,
                                                    _python=checker,
                                                    check_target=check_target))
                    _return = eval(command)
                    if _return:
                        if isinstance(_return, scene_data.ResultDatas):
                            for _ in _return.datas:
                                self.result.set_data_obj(_)
                        else:
                            self.result.set_data_obj(_return)

                if progress:
                    progress.setValue(count)
                    progress.setLabelText(f'{count} / {_length}')
                    QtCore.QCoreApplication.processEvents()
                    if progress.wasCanceled():
                        break
                count += 1

        calc_time = time.time() - _start_time
        print(f'End : Calculation time : {calc_time}')

    def load_checker(self) -> None:
        """["node", "mesh", "scene"]各ディレクトリのPyhon ファイル読み込み
        """
        for checker_category in settings.load_config(config_name='CHECKER_CATEGORY'):
            _module_directory = Path(settings.load_config(config_name='CHECKER_CATEGORY')[checker_category])
            if not _module_directory.exists():
                continue

            # フォルダ排除、__で始まるファイル排除
            _module_files = [p for p in _module_directory.iterdir()
                                            if p.is_file() and not p.stem.startswith('__')]

            if _module_files:
                self._cheker_files[checker_category] = _module_files

    def create_check_python_command(self,
                              data_type_category:str="ENVIRONMENT",
                              checker_category:str="node",
                              _python:str='',
                              check_target:list=[]
                              )->str:
        """チェッカーとして実行するコマンドを作成

        Args:
            category (str, [node, scene, mesh]):      チェック対象のタイプ
            _python (pathLib.Path)):                チェッカー本体
            node (list):                            チェック対象

        Returns:
            [str]: チェックコマンド
        """

        command = ''

        if not isinstance(_python, Path):
            module_name = _python
        else:
            module_name = _python.stem.lower()

        _root_dir = settings.load_config(config_name='MODULE_ROOT')
        modulename = f'{_root_dir}.{checker_category}.{module_name}'

        exec(f'import {modulename}', globals())

        if DEV_MODE:
            exec(f'importlib.reload({modulename})', globals())

        funcname = f'{modulename}.{"check"}'
        command = f'{funcname}("{data_type_category}", "{self.scene_path}", "{check_target}")'
        # print(command)

        return command

    def create_modify_python_command(self,
                                    data_type_category:str="ENVIRONMENT",
                                    checker_category:str="node",
                                    checker_module:str="",
                                    error_type_message:str="",
                                    modify_targets:list=[]
                                     )->str:
        """python ファイルを読み込み修正コマンドを返す

        Args:
            data_type (str): env, chara, prop
            category (str): scene, node, mesh
            _python (pathlib): python file path
            modify_target (str): [description]. Defaults to "".
            node (list): node list

        Returns:
            [str]: function
        """
        command = ''

        _root_dir = settings.load_config(config_name='MODULE_ROOT')
        modulename = f'{_root_dir}.{checker_category}.{checker_module}'

        exec(f'import {modulename}', globals())

        if DEV_MODE:
            exec(f'importlib.reload({modulename})', globals())

        funcname = f'{modulename}.{"modify"}'
        command = f'{funcname}("{data_type_category}", "{self.scene_path}", "{error_type_message}", "{modify_targets}")'

        return command

    def modify_data(self, result_all:scene_data.ResultDatas=None):
        """エラーを修正

        Args:
            result_all ([scene_data.ResultDatas]):

        Returns:
            [list, list]: _modifys, _errors
        """
        _modifys = []
        _errors = []
        _length = len(result_all.datas)

        # print(f'\n\nModify Scene  {"":-<10} [ {self.scene_path} ]')

        progress = None
        if not self.scene_path.is_batch:
            progress = gui_util.ProgressDialog()
            progress.setUp(_length, "modify ... ")
            progress.show()

        _start_time = time.time()

        count = 0
        for i, result in enumerate(result_all.datas):
            result:scene_data.ResultData = result
            modify_targets = result.error_nodes

            if not modify_targets:
                continue
            _command = self.create_modify_python_command(
                                data_type_category=result.data_type_category,
                                checker_category=result.checker_category,
                                checker_module=result.checker_module,
                                error_type_message=result.error_type_message,
                                modify_targets=modify_targets)

            success, message = eval(_command)

            if success == 1:
                _modifys.append(message)
            elif success == 0:
                _errors.append(message)

            count += 1
            if progress:
                progress.setValue(count)
                progress.setLabelText(f'{count} / {_length}')
                QtCore.QCoreApplication.processEvents()
                if progress.wasCanceled():
                    break

        calc_time = time.time() - _start_time
        print(f'End : Calculation time : {calc_time}')

        return _modifys, _errors


