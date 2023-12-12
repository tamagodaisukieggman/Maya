# -*- coding: utf-8 -*-
import sys
# import logging
# from tatool.log import ToolLogging, Stage

import maya.OpenMayaUI as omui

from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

TITLE = "Maya Scene Checker"
NAME = "{}".format("_".join(TITLE.lower().split()))

project = "shenron"
TOOL_NAME = "{}".format("".join(TITLE.split()))

tool_category = "Maya"

tool_version = 'v2022.11.25'

CHECKER_GUI_NAME = "CheckerGUI"
CHECKER_RESULT_GUI_NAME = "CheckerResultGUI"
CHECKER_ERROR_GUI_NAME = "ChekerErrorGUI"