# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import re
import shutil
import glob

import maya.cmds as cmds
import maya.mel as mel


# ------------------------------------------------------------
# 
# ------------------------------------------------------------

SEPARATE_STR = '____'