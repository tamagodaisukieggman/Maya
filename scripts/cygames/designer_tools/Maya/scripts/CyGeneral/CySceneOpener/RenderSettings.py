#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# RenderSettings.py
#

from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
except Exception:
    pass

import os
import maya.cmds as cmds
import pymel.util.path as pmp


def init():
    cmds.loadPlugin('fbxmaya.mll')
    cmds.loadPlugin('Mayatomr')

def main(path):
    #if(os.path.splitext(path)[1] == '.fbx'):
    #    cmds.loadPlugin('fbxmaya.mll')

    cmds.file(path, o=True, f=True)
    cmds.viewSet('perspShape', p=True)
    cmds.viewFit('perspShape', all=True)
    cmds.viewSet('perspShape', p=True)
    meshes = cmds.ls(type='mesh')
    maxMeshes = 0
    for mesh in meshes:
        numTris = cmds.polyEvaluate(mesh, t=True)
        if maxMeshes < numTris:
            maxMeshes = numTris
            cmds.select(mesh)

    cmds.viewFit('perspShape', fitFactor=1.0)
    a = cmds.getAttr('persp.translate')
    aa = a[0]
    cmds.viewFit('perspShape', fitFactor=0.7)
    b = cmds.getAttr('persp.translate')
    bb = b[0]
    result = [x + x - y for (x, y) in zip(aa, bb)]
    print(result)

    cmds.setAttr('persp.translateX', result[0])
    cmds.setAttr('persp.translateY', result[1])
    cmds.setAttr('persp.translateZ', result[2])

    cmds.setAttr('perspShape.renderable', 1)
    cmds.setAttr('defaultRenderGlobals.enableDefaultLight', 1)
    cmds.setAttr('defaultResolution.width', 640)
    cmds.setAttr('defaultResolution.height', 480)
    cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
    cmds.setAttr('defaultRenderGlobals.animation', 0)
    cmds.setAttr('defaultRenderGlobals.outFormatControl', 0)
    cmds.setAttr('defaultRenderGlobals.periodInExt', 0)
    cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)

    #cmds.displayPref(wsa='none')
    #cmds.hide(cmds.ls(type='joint'))

    fixTexturePath(path)
    cmds.render(batch=True)
    #cmds.playblast(frame=[1], format='image', cf=u'C:/Users/tech_artist/Desktop/test.jpg', wh=[640*2,480*2],fo=True, fp=0, v=False)


def fixTexturePath(path):
    listedNodes = cmds.ls(type="file")

    if len(listedNodes) > 0:
        for currNode in listedNodes:
            if not pmp(cmds.getAttr(currNode + '.fileTextureName')).exists():

                if cmds.referenceQuery(currNode, isNodeReferenced=True) == 1:
                    dir_path = cmds.referenceQuery(currNode, filename=True).split("scenes")[0] + "sourceimages/"
                else:
                    dir_path = path.split("scenes")[0] + "sourceimages/"
                path_old = cmds.getAttr(
                    currNode + '.fileTextureName').split("/")
                tex_name = path_old[len(path_old) - 1]

                path_new = pmp(dir_path + tex_name)

                if path_new.exists():
                    cmds.setAttr(currNode + '.fileTextureName', path_new, type="string")
