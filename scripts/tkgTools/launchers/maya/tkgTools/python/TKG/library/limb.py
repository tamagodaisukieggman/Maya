# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import traceback

import maya.cmds as cmds

from .. import nodes as tkgNodes
reload(tkgNodes)

def create_limb_joints(nodes=None):
    if not nodes:
        nodes = cmds.ls(os=True, fl=True) or []

    # BLEND joints
    dup = tkgNodes.Duplicate(nodes, '', '', ['BIND_', 'BLEND_'])
    dups = dup.duplicate()

    segments = tkgNodes.segment_duplicates(base=dups[0],
                                tip=dups[1],
                                i=8,
                                base_include=True,
                                tip_include=True,
                                children=True)