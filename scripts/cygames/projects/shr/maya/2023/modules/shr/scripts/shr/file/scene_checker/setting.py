# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
from pathlib import Path
import yaml

config_node = None
CYLISTA_SCRIPT_PATH = "Z:/cyllista/tools_ext/maya/modules/cyllista/scripts/"


if os.path.exists(CYLISTA_SCRIPT_PATH) and CYLISTA_SCRIPT_PATH not in sys.path:
    sys.path.append(CYLISTA_SCRIPT_PATH)

HERE = Path(os.path.dirname(os.path.abspath(__file__)))
YAML_FILE_NAME = "settings.yaml"

try:
    import cyllista.config_node as config_node
except Exception:
    print('can\'t import "config_node"')


def load_config(config_name: str = '')->dict:
    _yaml_data = HERE / YAML_FILE_NAME
    if not _yaml_data.exists():
        return

    with open(HERE / YAML_FILE_NAME, encoding='utf-8') as f:
        config = yaml.safe_load(f)
    _confing_data = config.get(config_name, None)
    return _confing_data


def get_influence_length_from_cyllista_config() -> int:
    inf_num: int = 4
    if config_node:
        config = config_node.get_config()
        inf_num = config.get("cySkinInfluenceCountMax", inf_num)
    return inf_num