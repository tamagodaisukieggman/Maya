import os
import maya.cmds as cmds
import pymel.core as pm

import apiutils
import cypyapiutils
import rigtools.skin

def exe():
    toolopt = apiutils.ToolOpt('Lod_Builder')
    delorg = toolopt.getvalue('deleteOriginal', False)

    varfile = os.path.join(os.path.dirname(__file__), 'variables.yaml')
    var = cypyapiutils.Variable('Lod_Builder', toolgroup='Maya', defaultfile=varfile)
    sel = cmds.ls(sl=True, l=True)
    for root in sel:
        for lod in var.get('LODs'):
            cmds.select(d=True)
            procroot(root, lod['name'], lod['percent'])
        if delorg:
            cmds.delete(root)


def procroot(root, name, percent):
    meshes = cmds.listRelatives(root, f=True, ad=True, type='mesh', ni=True) + cmds.ls(root, type='mesh')
    if len(meshes) == 0:
        return
    

    cp = cmds.duplicate(root, n=name)[0]

    io = cmds.ls(cmds.listRelatives(cp, f=True, ad=True, type='mesh'), io=True)
    if len(io)>0:
        cmds.delete(io)
    if percent < 1:
        pct = (1.0-percent) * 100.0
        reducecmd(cp, pct)

    scs = cmds.ls(cmds.listHistory(meshes), type='skinCluster')
    if not scs or len(scs)==0:
        return
    jnts = [pm.PyNode(x) for x in cmds.ls(cmds.listHistory(scs), type='joint')]
    if not jnts or len(jnts) ==0:
        return
    jointroots = apiutils.get_typenode_roots(jnts, type='joint')
    if len(jointroots) == 0:
        return

    cmds.select(cp, jointroots[0].name())
    cmds.SmoothBindSkin()

    cmds.select(root, cp)
    rigtools.skin.weight_cmds.copy_weight()


def reducecmd(cp, percent):
    meshes = cmds.listRelatives(cp, f=True, ad=True, type='mesh', ni=True)
    for m in meshes:
        cmds.polyReduce(m, ver=1, trm=0, shp=0, keepBorder=1, keepMapBorder=1, keepColorBorder=1, 
                keepFaceGroupBorder=1, keepHardEdge=1, keepCreaseEdge=1,
                keepBorderWeight=0.5, keepMapBorderWeight=0.5, keepColorBorderWeight=0.5, 
                keepFaceGroupBorderWeight=0.5, keepHardEdgeWeight=0.5, keepCreaseEdgeWeight=0.5, 
                useVirtualSymmetry=0, preserveTopology=1, keepQuadsWeight=1, cachingReduce=1, 
                ch=0,  p=percent, vct=0, tct=0, replaceOriginal=1)





