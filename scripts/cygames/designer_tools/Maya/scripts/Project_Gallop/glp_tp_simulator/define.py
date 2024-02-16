# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os


TOOL_NAME = 'GlpTpSimulator'
TOOL_VERSION = '24011101'

ITEM_NODE_BASE_NAME = 'GLP_SCRIPT_TP_SIMULATE_ITEM'

ICON_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui', 'icon')
FRAME_OPEN_ICON_PATH = os.path.join(ICON_FOLDER, 'opening_frame.png')
FRAME_CLOSE_ICON_PATH = os.path.join(ICON_FOLDER, 'closing_frame.png')
DELETE_ICON_PATH = os.path.join(ICON_FOLDER, 'delete.png')
ADD_ICON_PATH = os.path.join(ICON_FOLDER, 'plus.png')
RELOAD_ICON_PATH = os.path.join(ICON_FOLDER, 'reload.png')
