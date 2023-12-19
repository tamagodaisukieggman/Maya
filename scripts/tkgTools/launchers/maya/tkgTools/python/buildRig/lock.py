# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
reload(brCommon)

class LockTransform:
    def __init__(self, node=None, lock=True, keyable=False, channelBox=False, skip=None):
        self.node = node
        self.lock = lock
        self.keyable = keyable
        self.channelBox = channelBox

        self.options = {
            'lock':self.lock,
            'keyable':self.keyable,
            'channelBox':self.channelBox
        }

        self.skip = skip
        self.axis = ['x', 'y', 'z']

        self.skip_axis()

    def skip_axis(self):
        if self.skip: [self.axis.remove(s) for s in self.skip]

    def lock_and_hide(self, trs_at=['t', 'r', 's', 'v']):
        for tat in trs_at:
            if tat == 'v' or tat == 'visibility':
                cmds.setAttr(self.node+'.{}'.format(tat), **self.options)
            else:
                [cmds.setAttr(self.node+'.{}{}'.format(tat, at), **self.options) for at in self.axis]

class LockTransforms:
    def __init__(self, nodes=None, lock=True, keyable=False, channelBox=False, skip=None):
        self.nodes = nodes
        self.lock = lock
        self.keyable = keyable
        self.channelBox = channelBox
        self.skip = skip

        self.ltrs_options = {
            'lock':self.lock,
            'keyable':self.keyable,
            'channelBox':self.channelBox,
            'skip':self.skip
        }

    def lock_and_hide(self, trs_at=['t', 'r', 's', 'v']):
        for node in self.nodes:
            ltrs = LockTransform(node, **self.ltrs_options)
            ltrs.lock_and_hide(trs_at)
