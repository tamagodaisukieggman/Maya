# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import shutil
import os
import ast

import sys

import subprocess

import maya.cmds as cmds
import maya.mel as mel

from .. import base_common
from ..base_common import utility as base_utility
from ..base_common import classes as base_class

from .. import farm_common
from ..farm_common import utility as farm_utility
from ..farm_common import classes as farm_class

from . import checker_param_root
from . import checker_param_item
from . import checker_param_list
from . import checker_method
from . import checker_info
from . import checker_info_window

reload(base_common)
reload(farm_common)

reload(checker_param_root)
reload(checker_param_item)
reload(checker_method)
reload(checker_info_window)
reload(checker_param_list)
reload(checker_info)


# ==================================================
def main():

    this_main = Main()
    this_main.create_ui()


# ==================================================
def export_csv():

    this_main = Main()
    this_main.export_csv()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ==================================================
    def __init__(self):

        self.tool_version = '20121701'
        self.tool_name = 'FarmCharaChecker'

        self.window_name = self.tool_name + 'Win'

        self.setting = \
            base_class.setting.Setting(self.tool_name)

        self.chara_info = None
        self.checker_param_root = None

        # UI関連
        self.ui_updating = False

        self.ui_update_count = 0

        self.logger = base_class.logger.Logger()

        self.each_info_logger = base_class.logger.Logger()

        # 初期化フラグ
        self.is_init = False

    # ==================================================
    def initialize(self):

        self.is_init = False

        self.chara_info = farm_class.info.chara_info.CharaInfo()

        self.checker_param_root = checker_param_root.CheckerParamRoot(self)
        self.checker_param_root.initialize()

        self.is_init = True

    # ==================================================
    def create_ui(self):

        self.initialize()

        if not self.is_init:
            return

        self.checker_param_root.create_ui()

    # ==================================================
    def update_chara_info(self):

        current_path = cmds.file(q=True, sn=True)

        if not current_path:
            self.chara_info.create_info('temp')
            return

        self.chara_info.create_info(current_path, is_create_all_info=True)

    # ==================================================
    def export_csv(self):

        self.initialize()

        if not self.is_init:
            return

        self.checker_param_root.export_csv()
