# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
import buildRig.node as brNode
import buildRig.transform as brTrs
import buildRig.grps as brGrp
reload(brCommon)
reload(brNode)
reload(brTrs)
reload(brGrp)

class Fk(brGrp.RigModule):
    def __init__(self,
                 module=None,
                 side=None):
        super(Fk, self).__init__(module=module,
                                 side=side)
