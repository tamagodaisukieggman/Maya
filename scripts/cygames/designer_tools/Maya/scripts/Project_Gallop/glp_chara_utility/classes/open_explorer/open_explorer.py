# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import os

from ....base_common import utility as base_utility

from ....glp_common.classes.info import chara_info


class OpenExplorer(object):

    def open_explorer(self, type):
        """
        """

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            return

        target_dir_path = None

        if type == "scenes":
            target_dir_path = _chara_info.part_info.maya_scenes_dir_path

        elif type == "sourceimages":
            target_dir_path = _chara_info.part_info.maya_sourceimages_dir_path

        elif type == "mayaRoot":
            target_dir_path = _chara_info.part_info.maya_root_dir_path

        if target_dir_path is None:
            return

        if not os.path.isdir(target_dir_path):
            return

        base_utility.io.open_directory(target_dir_path)
