# -*- coding: utf-8 -*-
"""アニメーション追加機能
"""
from __future__ import annotations

import glob
import os
import typing as tp
from pathlib import Path

import yaml
from maya import cmds
from mtk.cutscene.sequencer.config.data import ActorConfigData


class ActorConfig(object):
    def __init__(self, config_path):
        self.config_path = str(Path(config_path))
        self.config_name = None
        self.data = None
        self._collect_config_name()
        self._load_data()

    def _collect_config_name(self):
        self.config_name = os.path.splitext(os.path.basename(self.config_path))[0]

    def _load_data(self):
        with open(self.config_path, encoding='utf-8') as f:
            self.data: tp.Optional[ActorConfigData] = yaml.load(f, yaml.Loader)

    def get_actor_nodes(self, namespace) -> tp.List[str]:
        nodes = []
        for node_str in self.data.actor_nodes:
            formated_node_name = node_str.format(namespace=namespace)
            if cmds.objExists(formated_node_name):
                nodes.append(formated_node_name)
        return nodes

    def get_motion_nodes(self, namespace) -> tp.List[str]:
        nodes = []
        for node_str in self.data.motion_nodes:
            formated_node_name = node_str.format(namespace=namespace)
            if cmds.objExists(formated_node_name):
                nodes.append(formated_node_name)
        return nodes


class BaseConfingCollector(object):
    def __init__(self, search_path) -> None:
        self.search_path = search_path
        self.actor_config_list: tp.List[ActorConfig] = []

        self._collect_config()

    def collect_actor_name_list(self) -> tp.Optional[tp.List[str]]:
        return [_.config_name for _ in self.actor_config_list]

    def get_actor_config_by_actor_name(self, actor_name):
        for actor_config in self.actor_config_list:
            if actor_config.config_name == actor_name:
                return actor_config

        raise ValueError("Not found actor_config")

    def _collect_config(self):
        config_list = self._collect_config_path()
        self.actor_config_list = [ActorConfig(_) for _ in config_list]

    def _collect_config_path(self) -> tp.List[str]:
        config_list = glob.glob("{}/*.yaml".format(self.search_path))
        return config_list


class CameraConfigCollector(BaseConfingCollector):
    def __init__(self) -> None:
        super().__init__("Z:/mtk/tools/maya/share/presets/Sequencer/camera/cofig/")


class ActorConfigCollector(BaseConfingCollector):
    """configにあるyaml取集すクラス
    - yamlの名前のリストを返す
    - 名前にヒットしたyamlの中身を返す

    """

    def __init__(self) -> None:
        super().__init__("z:/mtk/tools/maya/share/presets/Sequencer/actor/config/")
