# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from shr.cutscene import utility


class ShotRenamerToolSettings(utility.qt.QtSettings):
    def __init__(self):
        super(ShotRenamerToolSettings, self).__init__("CutsceneEditor_ShotRenamer")
