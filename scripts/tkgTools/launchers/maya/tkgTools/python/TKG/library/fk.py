# -*- coding: utf-8 -*-
from imp import reload
import math

import maya.cmds as cmds
import maya.mel as mel

import TKG.nodes as tkgNodes
import TKG.common as tkgCommon
import TKG.regulation as tkgRegulation
import TKG.library.rigJoints as tkgRigJoints
reload(tkgNodes)
reload(tkgRegulation)
reload(tkgRigJoints)

