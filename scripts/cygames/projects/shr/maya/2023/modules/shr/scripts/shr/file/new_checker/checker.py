# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pathlib
import time

from PySide2.QtCore import Qt
from PySide2 import QtCore, QtGui, QtWidgets

from ...utils import gui_util

import importlib
import shr.utils.gui_util as gui_util
importlib.reload(gui_util)

from . import PATH
from . import PACKAGE
from . import scene_data
from . import maya_utils


CHECK_TYPE = ["node", "mesh", "scene"]

# 開発中はTrue、リリース時にFalse
DEV_MODE = True


class Check:
    results = []
    _cheker_files = {}

    def __init__(self):

        # 種類別にチェックファイルを読み込んでおくためのもの
        # scene, node, mesh

        self.result_obj = None
        self.node_datas_obj = None
        self.scene_path_obj = None
        self.memory_clear()

        self.get_datas()
        self.load_checker()

    def memory_clear(self):
        self.result_obj = scene_data.ResultDatas()
        self._cheker_files = {}

    def get_datas(self):
        """シーンパスの情報取得
        """
        # シーンパスの情報を取得し対象を選別[env, chara, prop]
        self.scene_path_obj = scene_data.SceneData()

        # 「mdl_」グループ以下のノード情報を取得
        # 各ルートノード（背景では複数のmdl を許容しているため
        # 各ルートノードの全メッシュ
        self.node_datas_obj = scene_data.NodeDatas()

    def load_checker(self):
        """["node", "mesh", "scene"]各ディレクトリのPyhon ファイル読み込み
        """
        for category in CHECK_TYPE:
            self.load_python_modules(category)

    def load_python_modules(self, category="node"):
        """Python ファイル読み込み時に各要素に振り分け

        Args:
            category (str, [node, scene, mesh]):
        """
        _python_files = list(self.load_python_module_file(category))

        if not _python_files:
            return

        _cheker_files = []

        for _file in _python_files:
            if not _file.stem.startswith("__"):
                _cheker_files.append(_file)

        self._cheker_files[category] = _cheker_files

    def load_python_module_file(self, category="node"):
        """PATH 以下のサブフォルダに入れたスクリプトをチェッカーとして読み込む

        Args:
            category (str, [node, scene, mesh]): チェックする対象、ディレクトリ名でもある

        Returns:
            [PathObject]: category で指定されて以下のPython ファイル
        """
        _python_path = pathlib.Path(PATH)
        _module_directory = _python_path / category

        _module_files = [p for p in _module_directory.iterdir()
                         if p.is_file() and not p.stem.startswith('__')]

        return _module_files

    def create_modify_python_command(self,
                                     data_type="env",
                                     category="node",
                                     _python=None,
                                     error_detail="",
                                     node=[]
                                     ):
        """python ファイルを読み込み修正コマンドを返す

        Args:
            data_type (str): env, chara, prop
            category (str): scene, node, mesh
            _python (pathlib): python file path
            error_detail (str): [description]. Defaults to "".
            node (list): node list

        Returns:
            [str]: function
        """
        command = ''
        if not isinstance(_python, pathlib.Path):
            module_name = _python
        else:
            module_name = _python.stem

        modulename = f'{PACKAGE}.{category}.{module_name}'

        exec(f'import {modulename}', globals())

        if DEV_MODE:
            exec(f'importlib.reload({modulename})', globals())

        funcname = f'{modulename}.{"modify"}'

        if category == "mesh":
            command = f'{funcname}("{data_type}", "{self.scene_path_obj.get_scene_name()}", "{error_detail}", {node})'
        else:
            command = f'{funcname}("{data_type}", "{self.scene_path_obj.get_scene_name()}", "{error_detail}", "{node[0]}")'

        return command

    def create_python_command(self,
                              data_type="env",
                              category="node",
                              _python=None,
                              node=[]
                              ):
        """チェッカーとして実行するコマンドを作成

        Args:
            category (str, [node, scene, mesh]):      チェック対象のタイプ
            _python (pathLib.Path)):                チェッカー本体
            node (list):                            チェック対象

        Returns:
            [str]: チェックコマンド
        """

        command = ''

        if not isinstance(_python, pathlib.Path):
            module_name = _python
        else:
            module_name = _python.stem

        modulename = f'{PACKAGE}.{category}.{module_name}'

        exec(f'import {modulename}', globals())

        if DEV_MODE:
            exec(f'importlib.reload({modulename})', globals())

        funcname = f'{modulename}.{"check"}'

        if category == "mesh":
            command = f'{funcname}("{data_type}", "{self.scene_path_obj.get_scene_name()}", {node})'
        else:
            command = f'{funcname}("{data_type}", "{self.scene_path_obj.get_scene_name()}", "{node}")'

        return command

    def do_check(self, category="node", data_type="", progress=None):
        """チェック実行

        Args:
            category (str, [node, scene, mesh]): チェック対象タイプ
            data_type (str, [env, chara, prop]): モデルタイプ

        チェックで引っ掛かったものはself.result_obj に格納される
        """

        self.get_datas()

        if not data_type:
            data_type = self.scene_path_obj.data_type

        _modules = self._cheker_files.get(category, None)

        if not _modules:
            return

        command = ""
        _check_targets = [0]

        if category == "node":
            _check_targets = self.node_datas_obj.root_nodes
        elif category == "mesh":
            _check_targets = [self.node_datas_obj.all_meshes]

        if not _check_targets:
            return

        for i, _target in enumerate(_check_targets):
            if progress:
                progress.setValue(i+1)
                QtCore.QCoreApplication.processEvents()
                if progress.wasCanceled():
                    break
            # print("_target -- ", _target)
            for _python in self._cheker_files[category]:
                # print("_python -- ", _python)
                command = str(self.create_python_command(
                                                data_type=data_type,
                                                category=category,
                                                _python=_python,
                                                node=_target))
                _return = eval(command)

                if _return:
                    if isinstance(_return, scene_data.ResultDatas):
                        for _ in _return.datas:
                            self.result_obj.set_data_obj(_)
                    else:
                        self.result_obj.set_data_obj(_return)

    def modify_data(self, *args, result=None):
        """エラーを修正

        Args:
            result ([scene_data.ResultDatas]):

        Returns:
            [list, list]: _modifys, _errors
        """
        _modifys = []
        _errors = []
        _length = len(result.datas)

        if self.scene_path_obj.is_batch:
            _show_prg = False
        else:
            _show_prg = True

        print(f'\n\nModify Scene  {"":-<10} [ {self.scene_path_obj.get_scene_name()} ]')

        progress = None
        if _show_prg:
            progress = gui_util.ProgressDialog()
            progress.setUp(_length, "modify ... ")
            progress.show()

        _start_time = time.time()

        for i, _result in enumerate(result.datas):

            error = "_".join(str(_result.error).split())
            error_detail = ""

            if progress:
                progress.setValue(i+1)
                progress.setLabelText(f'{i} / {_length}')
                QtCore.QCoreApplication.processEvents()
                if progress.wasCanceled():
                    break

            if ":" in error:
                _split = error.split(":")
                error = _split[0]
                error_detail = " ".join(_split[-1].split("_"))

            category = str(_result.category)
            data_type = str(_result.data_type)

            nodes = _result.error_nodes

            _command = self.create_modify_python_command(
                data_type=data_type,
                category=category,
                _python=error,
                error_detail=error_detail,
                node=nodes)

            _return = eval(_command)

            if _return[0] == 1:
                _modifys.append(_return[1])
            elif _return[0] == 0:
                _errors.append(_return[1])

        calc_time = time.time() - _start_time
        print(f'End : Calculation time : {calc_time}')

        # polyBind というヒストリは強制的に消す
        maya_utils.delete_poly_bind_data()
        return _modifys, _errors

    def check_start(self, *args):
        """チェック実行
        """
        self.memory_clear()
        self.load_checker()
        _targets = [
            "scene",
            "node",
            "mesh",
        ]

        if self.scene_path_obj.is_batch:
            _show_prg = False
        else:
            _show_prg = True

        _length = 0
        _files = []

        if "node" in _targets:
            _files = self._cheker_files.get("node", None)
        if "mesh" in _targets:
            _files = self._cheker_files.get("mesh", None)
        if "scene" in _targets:
            _files = self._cheker_files.get("scene", None)
        if _files:
            _length += len(_files)

        progress = None
        if _show_prg:
            progress = gui_util.ProgressDialog()
            progress.setUp(maxValue=_length, title="check ... ")
            progress.show()

        _start_time = time.time()

        for i, _target in enumerate(_targets):
            if progress:
                progress.setValue(i+1)
                progress.setLabelText(f'{i} / {_length}')
                QtCore.QCoreApplication.processEvents()
                if progress.wasCanceled():
                    break
            self.do_check(category=_target,
                          data_type=self.scene_path_obj.data_type, progress=progress)

        calc_time = time.time() - _start_time
        print(f'End : Calculation time : {calc_time}')
