# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
import buildRig.node as brNode
import buildRig.transform as brTrs

class Joint:
    def __init__(self, node=None):
        self.node = node

    def create(self):
        if not cmds.objExists(self.node):
            cmds.createNode('joint', n=self.node, ss=True)
