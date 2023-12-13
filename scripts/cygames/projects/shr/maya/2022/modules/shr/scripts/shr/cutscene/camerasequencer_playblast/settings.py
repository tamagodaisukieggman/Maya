# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function
import os

from PySide2.QtCore import QSettings
from PySide2.QtWidgets import QLineEdit, QCheckBox, QComboBox, QSpinBox

from shr.cutscene import utility
from maya import cmds, mel


class ToolSettings(utility.qt.QtSettings):
    """ツールセッティング
    """

    def __init__(self):
        super(ToolSettings, self).__init__("CutsceneEditor_StartPlayblast")
