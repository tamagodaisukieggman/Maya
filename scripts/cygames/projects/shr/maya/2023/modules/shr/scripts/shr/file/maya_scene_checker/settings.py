
import os
from pathlib import Path
import yaml

HERE = Path(os.path.dirname(os.path.abspath(__file__)))
YAML_FILE_NAME = "cheker_settings.yaml"


def load_config(config_name:str = ''):
    with open(HERE / YAML_FILE_NAME, encoding='utf-8') as f:
        config = yaml.safe_load(f)
    _confing_data = config.get(config_name, None)
    return _confing_data

