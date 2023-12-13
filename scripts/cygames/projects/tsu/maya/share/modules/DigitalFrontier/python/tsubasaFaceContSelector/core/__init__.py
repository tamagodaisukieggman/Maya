# -*- coding: utf-8 -*-
"""
Copyright (C) 2021 Digital Frontier Inc.
"""
from .logger import get_logger
from .main import get_button_settings_info
try:
    from . import maya_cmds
    from .maya_cmds import *
except:
    from .standalone_cmds import *
