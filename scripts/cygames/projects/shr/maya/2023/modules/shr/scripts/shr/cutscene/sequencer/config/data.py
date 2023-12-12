from __future__ import annotations

import pathlib
import typing as tp
from dataclasses import dataclass
from enum import Enum, auto

import yaml


class ObjectType(Enum):
    motion = "motion"
    camera = "camera"


@dataclass
class BindingData:
    binding_condition: str
    is_binding_solo: bool
    node_type: str
    extra_attrs: tp.List[str]


@dataclass
class ActorConfigData:
    object_type: ObjectType
    version: str
    actor_nodes: tp.List[str]
    motion_nodes: tp.List[str]
    actor_import_path: str
    recommended_name: str
    recommended_animation_path: str
    binding_data: BindingData


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        data: ActorConfigData = yaml.load(f, Loader=yaml.Loader)
    return data
