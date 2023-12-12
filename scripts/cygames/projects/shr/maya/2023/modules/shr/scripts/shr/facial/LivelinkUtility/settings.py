# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import division as _division
from __future__ import print_function as _print_function
from __future__ import unicode_literals as _unicode_literals

from shr.cutscene import utility


class LivelinkUtilitySettings(utility.qt.QtSettings):
    def __init__(self):
        super(LivelinkUtilitySettings, self).__init__("LivelinkUtility")
