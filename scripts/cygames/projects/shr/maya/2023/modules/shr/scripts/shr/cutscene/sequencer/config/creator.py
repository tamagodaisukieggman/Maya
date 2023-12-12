"""Configの生成機能。未来的に要望あればGUI付けて表示できる様にする

"""
from __future__ import annotations

import pathlib
import typing as tp

import yaml

from .data import ActorConfig, BindingData, ObjectType

SCRIPT_PATH = pathlib.Path(__file__).parent


def main(file_name):
    binding_data = BindingData(binding_condition="{namespace}::rig",
                               is_binding_solo=False,
                               node_type="nurbsCurve")

    data = ActorConfig(version="1.0.0",
                       object_type=ObjectType.motion,
                       actor_import_path="z:/mtk/work/resources/animations/clips/player/workscenes/anm_ply00_m_000_rig.ma",
                       binding_data=binding_data,
                       recommended_name="Player_001",
                       necessary_nodes=["{namespace}::rig", "{namespace}::root"],
                       unnecessary_nodes=["{namespace}::rig", "{namespace}::root"],
                       recommended_animation_path="Z:/mtk/work/resources/animations/clips/player")

    with open(SCRIPT_PATH / f"{file_name}.yaml", "w", encoding="utf-8") as wf:
        yaml.dump(data, wf)
