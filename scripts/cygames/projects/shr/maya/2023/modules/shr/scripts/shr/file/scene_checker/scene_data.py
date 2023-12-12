# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from dataclasses import dataclass, field
import importlib
import os

from maya import cmds
from ...utils import getCurrentSceneFilePath
from . import utils
from . import setting
from . import data

DEV_MODE = setting.load_config(config_name='DEV_MODE')
if DEV_MODE:
    importlib.reload(utils)
    importlib.reload(setting)
    importlib.reload(data)


@dataclass
class MayaSceneDataBase:
    """
    name: シーン名
    basename: 拡張子を抜かしたファイル名
    nodes: ルートノード
    ext: 拡張子
    _project_setting: プロジェクト設定
    _project: プロジェクト名
    batch_mode: バッチモード
    """
    name: str = field(default_factory=str)
    basename: str = field(default_factory=str)
    nodes: list = field(default_factory=list)
    ext: str = field(default_factory=str)
    _project_setting: data.ProjectSettings = field(default_factory=data.ProjectSettings)
    _project: str = field(default_factory=str)
    batch_mode: bool = field(default_factory=bool)
    _special_conditions_group: dict = field(default_factory=dict)
    _special_conditions_group_checker: dict = field(default_factory=dict)
    _current_category:str = field(default_factory=str)

class MayaSceneData(MayaSceneDataBase):
    """Maya シーン情報

    Args:
        MayaSceneDataBase (_type_): _description_
        scene_name:
    """
    def __init__(self) -> None:
        super().__init__()
        self.set_scene_name()
        # self.get_all_scene_data()

    @property
    def name_split_all(self) -> str:
        return self.name.replace('/', os.sep).split(os.sep)

    @property
    def is_batch(self) -> bool:
        return cmds.about(batch=True)

    @property
    def scene_name(self) -> str:
        return self.name

    @property
    def scene_ext(self) -> str:
        return self.ext

    @property
    def all_node_type(self) -> list:
        return cmds.allNodeTypes()

    @property
    def all_nodes(self) -> list:
        return cmds.ls()

    @property
    def root_nodes(self) -> list:
        return self.nodes

    def set_scene_name(self) -> None:
        _name = getCurrentSceneFilePath()
        if _name:
            basename = os.path.basename(_name)
            _base_name, _ext = os.path.splitext(basename)
            self.basename = _base_name
            self.name = _name
            self.ext = _ext

    def get_all_scene_data(self, ignore_check_group_name:list) -> list:
        check_nodes:list = utils.get_check_root_nodes(
                                                ignore_check_group_name = ignore_check_group_name,
                                                project_setting = self._project_setting
                                                )
        if not check_nodes:
            return
        self.nodes = check_nodes

    @property
    def special_conditions_group(self):
        return self._special_conditions_group

    @special_conditions_group.setter
    def special_conditions_group(self, group_name:str, nodes:list):
        self._special_conditions_group[group_name] = nodes
        self._special_conditions_group_checker[group_name] = self._project_setting.current_settings.get('SPECIAL_CONDITIONS_GROUP_CHECKER')

    @property
    def project_setting(self) -> data.ProjectSettings:
        return self._project_setting

    @project_setting.setter
    def project_setting(self, project_setting:data.ProjectSettings) -> None:
        self._project_setting = project_setting
        self._project = project_setting.name
        if self._project_setting.current_settings:
            IGNORE_CHECK_GROUP_NAME:list = self._project_setting.current_settings.get('IGNORE_CHECK_GROUP_NAME')
            self.get_all_scene_data(ignore_check_group_name=IGNORE_CHECK_GROUP_NAME)

    @property
    def special_conditions_group_checker(self):
        return self._special_conditions_group_checker

    @property
    def project(self) -> str:
        """現在のプロジェクト名

        Returns:
            str: _description_
        """
        return self._project

    # @project.setter
    # def project(self, project_name:str) -> None:
    #     """プロジェクトのセット

    #     Args:
    #         project_name (str): _description_
    #     """
    #     self._project = project_name

    @property
    def current_project_setting(self) -> dict:
        """現在のプロジェクト設定を返す

        Returns:
            dict: _description_
        """
        return self._project_setting.settings.get(self._project)

    @property
    def current_category(self) -> str:
        """現在のカテゴリを返す

        Returns:
            str: _description_
        """

        return self._current_category if self._current_category else self._project_setting.category


    @current_category.setter
    def current_category(self, category:str):
        _categories:dict = self._project_setting.current_settings.get('DATA_TYPE_CATEGORY')
        if _categories and category in _categories:
            self._current_category = category
        else:
            self._current_category = self._project_setting.category



    # @property
    # def current_checker(self):
    #     return self._current_checker

    # @current_checker.setter
    # def current_checker(self, current_checker:str):
    #     self._current_checker = current_checker

    def get_check_target(self) -> list:
        """チェックの対象となるルートノード取得

        Returns:
            list: _description_
        """
        return self.nodes

    def extract_check_root_node_start_names_mdl(self) -> None:
        """「mdl_」などの特定の命名が付くものをピックアップ
        """
        current_setting = self.current_project_setting

        if not current_setting:
            return

        start_name_rule:dict = current_setting.get('ROOT_NODE_START_NAMES')

        if not start_name_rule:
            return

        start_names:list = start_name_rule.get(self.current_category)

        if not start_names:
            return

        _keep_nodes:list = []
        for node in self.nodes:
            node: data.RootNodeData
            for name_start in start_names:
                # print(name_start)
                if name_start == 'basename' and node.node_name.startswith(self.basename):
                    _keep_nodes.append(node)
                elif node.full_path_name.startswith(name_start) and node not in _keep_nodes:
                    _keep_nodes.append(node)

        self.nodes = _keep_nodes


