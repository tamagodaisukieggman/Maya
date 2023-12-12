# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pymel.core as pm
import maya.cmds as mc

from . import command
from . import setup


import importlib
importlib.reload(setup)
importlib.reload(command)