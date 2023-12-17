# -*- coding: utf-8 -*-
import codecs
from collections import OrderedDict
from imp import reload
import json
import os
import re

import maya.cmds as cmds
import maya.mel as mel

def set_environment(set_fps=30, set_focalLength=100):
    # fps
    cmds.currentUnit(time = '{0}fps'.format(set_fps))
    cmds.playbackOptions(min=0, max=1, ast=0, aet=1)
    cmds.currentTime(0)

    # camera
    # cmds.viewSet(home=True)
    persp_cam_shape = cmds.ls('*persp*', type='camera')[0]
    cmds.setAttr('{0}.focalLength'.format(persp_cam_shape), set_focalLength)
    cmds.viewFit(persp_cam_shape, fitFactor=1, all=True)

    # turtle
    def turtleKiller():
        if cmds.pluginInfo('Turtle', loaded=True, q=True):
            cmds.unloadPlugin('Turtle', f=True)
        for unk in cmds.ls('Turtle*'):
            cmds.lockNode(unk, l=False)
            cmds.delete(unk)
        print('unloaded turtle plugin and deleted related nodes successfully.')

    turtleKiller()

    # MayaNodeEditorSavedTabsInfo
    mnesti = cmds.ls('MayaNodeEditorSavedTabsInfo*')
    [cmds.delete(mo) for mo in mnesti]

    # hardwareRenderingGlobals
    cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
    cmds.setAttr('hardwareRenderingGlobals.multiSampleCount', 8)


def ihi_hides(set_ihi_nodes=None):
    if not set_ihi_nodes:
        set_ihi_nodes = [
            'constraint',
            'reverse',
            'shape',
            'decomposeMatrix',
            'multiplyDivide',
            'condition',
            'multDoubleLinear',
            'plusMinusAverage',
            'pairBlend',
            'clamp',
            'distanceBetween'
        ]

    def ihi_hide(node_type=None):
        nodes = cmds.ls(type=node_type)
        if nodes:
            [cmds.setAttr('{}.ihi'.format(node), 0) for node in nodes]

    [ihi_hide(ihi_n) for ihi_n in set_ihi_nodes]


def finalize_rig():
    ihi_hides()
    set_environment()
