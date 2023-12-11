# -*- coding: utf-8 -*-
import typing as tp
import json

from . import utility
from .task import CheckTaskBase
from .data import DebugData
from .scene_data import MayaSceneData
from .common_task import *


class Checker:
    def __init__(
        self,
        checker_title: str,
        task_names: tp.List[str],
        extra_datas: dict,
        root_objects: tp.List[str] = [],
        post_process_settings: tp.List[any] = [],
    ):
        self.checker_title = checker_title
        self.extra_datas = extra_datas
        self.root_objects = root_objects
        self.post_process_settings = post_process_settings

        self.current_tasks = {}
        self.debug_datas = {}

        self.maya_scene_data: MayaSceneData = None
        self.initialize(task_names)

    def initialize(self, task_names: tp.List[str]):
        self.initialize_postprocess_settings()

        self._reset_maya_scene_data()
        self._initialize_tasks(task_names)  # task情報の初期化
        self._initialize_debug_data()

    def initialize_postprocess_settings(self):
        """postprocess設定の初期化
        デフォルト設定にoverride設定を反映
        """

        if self.post_process_settings != []:
            checker_settings = utility._get_checker_settings()
            for pp_setting in checker_settings["post_process_settings"]:
                for override_pp_settings in self.post_process_settings:
                    if pp_setting["name"] == override_pp_settings["name"]:
                        pp_setting["value"] = override_pp_settings["value"]
                        break
                else:
                    pp_setting = override_pp_settings
            self.post_process_settings = checker_settings["post_process_settings"]

    def _initialize_tasks(self, task_datas: tp.List[str]):
        """taskの初期化 インスタンスを保持

        Args:
            task_names (tp.List[str]): _description_
        """
        for task_name in task_datas:
            self.current_tasks[task_name] = self._get_new_task_by_taskname(task_name)
            extra_data = None
            if task_name in self.extra_datas:
                extra_data = self.extra_datas[task_name]
                self.current_tasks[task_name].extra_data.update(extra_data)

    def _initialize_debug_data(self):
        """self.debug_datas(debug用のデータ)を初期化"""
        for task_name in self.current_tasks:
            # 初期のデバッグデータを作成
            debug_data = DebugData()
            self.set_debug_data(task_name, debug_data)

    def _reset_maya_scene_data(self):
        """MayaSceneDataの再取得"""
        self.maya_scene_data = MayaSceneData(self.root_objects)

    def _get_new_task_by_taskname(self, task_name: str) -> CheckTaskBase:
        """名前からタスクのインスタンスを取得

        Args:
            task_name (str): タスク名

        Returns:
            CheckTaskBase: 取得した
        """
        task_class = self._find_checker_task(task_name)
        extra_data = {}
        if task_name in self.extra_datas:
            extra_data = self.extra_datas[task_name]

        task = task_class(
            maya_scene_data=self.maya_scene_data,
            extra_data=extra_data,
            post_process_settings=self.post_process_settings,
        )

        return task

    def _get_task_by_taskname(self, task_name: str) -> CheckTaskBase:
        """名前からタスクのインスタンスを取得

        Args:
            task_name (str): タスク名

        Returns:
            CheckTaskBase: 取得した
        """
        task = self.current_tasks[task_name]

        return task

    def exec_task_by_taskname(self, task_name: str) -> CheckTaskBase:
        """名前からタスクを実行

        Args:
            task_name (str): タスク名

        Returns:
            CheckTaskBase: 実行したタスク
        """
        task = self.current_tasks[task_name]
        task.maya_scene_data = self.maya_scene_data
        self.exec_task(task)

        return task

    def exec_task(self, task):
        """タスクの実行、事前処理で依存関係のあるタスクのエラーステータスの確認を行う"""

        # 依存しているタスクにエラーがなければtaskの実行
        if self.check_dependent_task_error_state(task) == True:
            task.exec_task()

        current_debug_data = task.debug_data
        self.set_debug_data(task.__class__.__name__, current_debug_data)

    def exec_fix_by_taskname(self, task_name: str) -> CheckTaskBase:
        """名前からタスクを実行

        Args:
            task_name (str): タスク名

        Returns:
            CheckTaskBase: 実行したタスク
        """
        task = self.current_tasks[task_name]
        task.maya_scene_data = self.maya_scene_data
        self.exec_fix(task)

        return task

    def exec_fix(self, task):
        """タスクの実行、事前処理で依存関係のあるタスクのエラーステータスの確認を行う"""

        # 依存しているタスクにエラーがなければtaskの実行
        if self.check_dependent_task_error_state(task) == True:
            task.exec_task()

        task.exec_fix()

        current_debug_data = task.debug_data
        self.set_debug_data(task.__class__.__name__, current_debug_data)

    def check_dependent_task_error_state(self, task: CheckTaskBase) -> bool:
        """依存関係のあるタスクがエラーかどうかのチェック

        Args:
            task (CheckTaskBase): 対象のタスク

        Returns:
            bool: エラーを持っているかどうか
        """
        if "dependent_task_names" not in task.extra_data:
            return True
        for task_name in task.extra_data["dependent_task_names"]:
            dependent_task = self._get_task_by_taskname(task_name)
            if ErrorType.NOERROR != dependent_task.debug_data.error_type:
                task.set_error_data(
                    "dependent_task",
                    None,
                    f'依存しているタスク 【 {dependent_task.checker_info.label_name} 】がエラーステータス、"OK"ではありません',
                )
                task.set_error_type(ErrorType.ERROR)
                return False
        task.set_error_type(ErrorType.NOERROR)
        return True

    def exec_all_check(self):
        """チェックの実行"""
        for task_name in self.current_tasks:
            task = self.exec_task_by_taskname(task_name)
            current_debug_data = task.debug_data
            self.debug_datas[task_name] = current_debug_data

    def _all_subclasses(self, cls: any) -> tp.List[any]:
        """サブクラスを再帰的に取得

        Returns:
            tp.List[any]: タスクのサブクラス
        """
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in self._all_subclasses(c)]
        )

    def _find_checker_task(self, task_name: str) -> CheckTaskBase:
        """checkerのtaskを検索
        CheckTaskBaseのサブクラスでクラス名と一致しているものを返す

        Args:
            task_name (str): CheckTaskBaseのサブクラス名と同一のタスク名

        Raises:
            ValueError: checker taskが見つからなかった場合エラー

        Returns:
            CheckTaskBase: CheckTaskBaseのサブクラスを返す
        """
        for checker_task in self._all_subclasses(CheckTaskBase):
            if checker_task.__name__ == task_name:
                return checker_task

        raise ValueError(f"Not found checker task [{task_name}]")

    def get_debug_data(self, task_name: str) -> DebugData:
        """ためていたデバッグデータからタスク名と一致する物を返す

        Args:
            task_name (str): タスク名

        Returns:
            DebugData: タスク名の対象のDebugData
        """
        return self.debug_datas[task_name]

    def set_debug_data(self, task_name: str, value: DebugData):
        """デバッグデータのセット

        Args:
            task_name (str): セットするでバックデータを保持するタスク名
            value (DebugData): セットするデバッグデータ

        """
        self.debug_datas[task_name] = value
