# -*- coding: utf-8 -*-
from __future__ import absolute_import

# ----------------------------------
# Project : Common
# Name    : Maya Bootstrap GUI (mbg)
# Author  : ryo kanda
# Version : 0.0.1
# Updata  : 2022/09/18 19:14:41
# ----------------------------------

import json
import os
import sys
import shutil

import pymel.core as pm
import maya.cmds as mc

from . import core as mbc
import importlib
importlib.reload(mbc)



uiList = ['skinCluster', 'Bend', 'Cluster', 'BlendShape']





