# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib
from dataclasses import dataclass, field

from . import setting

DEV_MODE = setting.load_config(config_name='DEV_MODE')
if DEV_MODE:
    importlib.reload(setting)


@dataclass
class ResultDataBase:
    data_category: str = field(default_factory=str)
    checker: str = field(default_factory=str)

    error_message_list: list = field(default_factory=list)
    warning_message_list: list = field(default_factory=list)
    color: list = field(default_factory=list)

    warning_nodes: list = field(default_factory=list)
    error_nodes: list = field(default_factory=list)
    error_compornent: dict = field(default_factory=dict)
    warning_compornent: dict = field(default_factory=dict)

    delete_target_nodes: list = field(default_factory=list)
    remove_target_uv_sets: dict = field(default_factory=dict)
    remove_target_color_sets: dict  = field(default_factory=dict)


class ResultData(ResultDataBase):
    def __init__(self):
        super().__init__()
        self.color = setting.load_config('TYPE_BG_COLOR')

    @property
    def all_item_count(self)->int:
        return int(len(self.error_nodes) + len(self.warning_nodes))


@dataclass
class ResultDataMultiBase:
    data_category: str = field(default_factory=str)
    result_datas: dict = field(default_factory=dict)
    skining_geometory: dict = field(default_factory=dict)
    no_polygon_mesh:list = field(default_factory=list)
    intermediate_objects:list = field(default_factory=list)
    mesh_shape_materials:dict = field(default_factory=dict)
    should_not_exists_nodes:list = field(default_factory=list)
    no_confirmation_required_nodes:list = field(default_factory=list)
    # checker_module:

class CheckResultData(ResultDataMultiBase):
    def __init__(self):
        super().__init__()

    @property
    def all_result_count(self):
        count = 0
        if not self.result_datas:
            return count
        for result_data in self.result_datas.values():
            count += result_data.all_item_count
        return count


@dataclass
class ModifyResult:
    modify_flag:bool = field(default_factory=bool)
    error_flag:bool = field(default_factory=bool)

    modify_nodes:list = field(default_factory=list)
    error_nodes:list = field(default_factory=list)

    modify_messages:list = field(default_factory=list)
    error_messages:list = field(default_factory=list)


@dataclass
class ProjectSettingsBase:
    name:str = field(default_factory=str)
    settings:dict = field(default_factory=dict)
    current_settings:dict = field(default_factory=dict)
    _category:str = field(default_factory=dict)
    unknown_category_type:str = field(default_factory=dict)
    _current_checker: str = field(default_factory=dict)


class ProjectSettings(ProjectSettingsBase):
    def __init__(self, scene_path:str='', lower_drive_letter:bool=False) -> None:
        """プロジェクト独自の設定

        Args:
            scene_path (str, optional): Maya シーンファイルパス
            lower_drive_letter (bool, optional): ドライブレターの小文字化
        """
        super().__init__()
        self.scene_path:str = scene_path
        if lower_drive_letter:
            self.convert_lowercase()

        # シーンのファイルパスでは分類できなかったものをどのような表示にするか
        # デフォルトは「UNKNOWN」
        self.unknown_category_type = setting.load_config(config_name='UNKNOWN_SCENE_CATEGORY_NAME')
        self.set_project()

    def set_project(self) -> None:
        """
        現在のプロジェクト名、プロジェクトの設定を yaml から読み込み
        """
        # self.name = ''
        # self.settings = dict()
        self.name = setting.load_config(config_name='CURRENT_PROJECT')
        self.settings = setting.load_config(config_name='PROJECT_SETTINGS')
        self.current_settings = self.settings.get(self.name)

    def convert_lowercase(self) -> None:
        """ドライブレターを小文字に変換
        """
        _:str = self.scene_path[0].lower()
        other:str = self.scene_path[1:]
        self.scene_path = f'{_}{other}'

    @property
    def project_name(self) -> str:
        """プロジェクト名

        Returns:
            str: _description_
        """
        return self.name

    @property
    def project_settings(self) -> dict:
        """プロジェクト設定

        Returns:
            dict: _description_
        """
        return self.settings

    @property
    def category(self) -> str:
        """カテゴリ名
        分類不可であれば「UNKNOWN」

        Returns:
            str: _description_
        """
        _result:str = self.unknown_category_type
        current_setting = self.settings.get(self.name)
        if not current_setting:
            return self._category

        category_paths = current_setting.get('PATH')
        if not category_paths:
            return self._category

        for category, paths in category_paths.items():
            for path in paths:
                if self.scene_path.startswith(path):
                    _result = category
                    break

        self._category = _result
        return self._category

    @property
    def current_checker(self):
        return self._current_checker

    @current_checker.setter
    def current_checker(self, current_checker:str):
        self._current_checker = current_checker


@dataclass
class RootNodeDataBase:
    full_path_name: str = field(default_factory=str)
    # ルートノード名（ショートネーム）
    node_name: str = field(default_factory=str)
    node_type: str = field(default_factory=str)
    # ルートノード以下の全階層
    _all_descendents: list = field(default_factory=list)

    _all_nodes: list = field(default_factory=list)


class RootNodeData(RootNodeDataBase):
    def __init__(self, node_name:str, full_path_name:str, node_type:str, project_setting:ProjectSettings) -> None:
        super().__init__()
        self.node_name = node_name
        self.full_path_name = full_path_name
        self.node_type = node_type
        self._project_setting = project_setting

    @property
    def project_setting(self):
        return self._project_setting

    @property
    def all_descendents(self) -> list:
        """
        SPECIAL_CONDITIONS_GROUP はルート以下の第二階層にある特定のグループ名
        SPECIAL_CONDITIONS_GROUP_CHECKER は特定のグループで実行させたい項目

        Returns:
            list: _description_
        """
        _keep_nodes:list = []
        if self._project_setting:
            SPECIAL_CONDITIONS_GROUP:str = self._project_setting.current_settings.get('SPECIAL_CONDITIONS_GROUP')
            SPECIAL_CONDITIONS_GROUP_CHECKER:str = self._project_setting.current_settings.get('SPECIAL_CONDITIONS_GROUP_CHECKER')
            if SPECIAL_CONDITIONS_GROUP_CHECKER and self._project_setting.current_checker not in SPECIAL_CONDITIONS_GROUP_CHECKER:
                for node in self._all_nodes:
                    node: CustomNodeData = node
                    if  node.category_group != SPECIAL_CONDITIONS_GROUP:
                        _keep_nodes.append(node)

        return _keep_nodes if _keep_nodes else self._all_nodes

    @property
    def all_nodes(self) -> list:
        return self._all_descendents

    @all_nodes.setter
    def all_node(self, all_nodes:list):
        self._all_descendents = all_nodes

    def __repr__(self) -> str:
        return super().__repr__()


@dataclass
class CustomNodeData:
    # ルートノード名
    root_node: str = field(default_factory=str)
    number: int = field(default_factory=int)
    full_path_name: str = field(default_factory=str)
    node_type: str = field(default_factory=str)
    short_name: str = field(default_factory=str)
    deep: int = field(default_factory=int)
    shapes: list = field(default_factory=list)
    category_group: str = field(default_factory=str)
    has_mesh: bool  = field(default_factory=bool)
    is_locator: bool = field(default_factory=bool)

    def __repr__(self) -> str:
        return self.full_path_name

    @property
    def split_full_path_name(self):
        return self.full_path_name.split('|')[1:]

@dataclass
class CheckerBase:
    error_nodes:list = field(default_factory=list)
    warning_nodes:list = field(default_factory=list)
    error_message_list:list = field(default_factory=list)
    warning_message_list:list = field(default_factory=list)
    result:ResultData = field(default_factory=ResultData)
    # _special_conditions_group: dict = field(default_factory=dict)


class Checker(CheckerBase):
    """チェッカーで検出したものを引き継がせるためのもの
    スキニングとか、面積を持たないメッシュとか判定して処理を変える

    Args:
        CheckerBase (_type_): _description_
    """
    def __init__(self) -> None:
        super().__init__()

    def set_result_data(self, category:str, checker:str, checker_path:str) -> None:
        self.result.data_category = category
        self.result.checker = checker


    def check_end(self) -> None:
        """チェック終了時の動作
        """
        _error = 'Error'
        _warning = 'Warning'
        _no_error = 'No Error'
        _ = ''
        return
