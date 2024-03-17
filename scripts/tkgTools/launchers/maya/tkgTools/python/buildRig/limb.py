# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
import buildRig.connecter as brConnecter
import buildRig.node as brNode
import buildRig.grps as brGrp
import buildRig.joint as brJnt
import buildRig.libs.control.draw as brDraw
import buildRig.transform as brTrs
import buildRig.aim as brAim
import buildRig.fk as brFk
import buildRig.ik as brIk
import buildRig.switch as brSwitch
reload(brCommon)
reload(brConnecter)
reload(brNode)
reload(brGrp)
reload(brJnt)
reload(brDraw)
reload(brTrs)
reload(brAim)
reload(brFk)
reload(brIk)
reload(brSwitch)

class Limb(brGrp.RigModule):
    def __init__(self):
        pass