import sys
import re

import pymel.core as pm
import apiutils


import maya.api.OpenMaya as om
import maya.cmds as cmds

def connectmesh(src, stnode, attr, extras):
    tmpsrc = cmds.duplicate(src, rc=True)[0]
    enternode = None
    exitnode = src + '.worldMesh'
    if extras['en_average']:
        av = cmds.polyAverageVertex(tmpsrc, i=extras['average_value'], ch=True)[0]
        enternode = av + '.inputPolymesh'
        exitnode = av + '.output'
    if extras['en_smooth']:
        sm = cmds.polySmooth(tmpsrc, mth=0, sdt=2, ovb=1, ofb=3, ofc=0, 
                ost=0, ocr=0, dv=extras['smooth_value'], bnr=1, c=1, kb=1, ksb=1, khe=0, 
                kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)[0]
        if not enternode:
            enternode = sm + '.inputPolymesh'
        exitnode = sm + '.output'
    
    stnode_attr = stnode + '.' + attr

    if enternode:
        cmds.connectAttr(src + '.worldMesh', enternode, f=True)
        cmds.connectAttr(exitnode, stnode_attr, f=True)
    else:
        cmds.connectAttr(src + '.worldMesh', stnode_attr, f=True)
        
    cmds.delete(tmpsrc)


def exe():
    toolopt = apiutils.ToolOpt('Retarget_Attached_Meshes')
    mm = toolopt.getvalue('matchMode', 'UV')
    objmm = toolopt.getvalue('objMatchMode', 'Object Name')
    ch = False and toolopt.getvalue('history', False)
    en_smooth = toolopt.getvalue('preSmoothEnabled', True)
    smooth_value = toolopt.getvalue('preSmoothValue', 1)
    en_average = toolopt.getvalue('preAverageEnabled', False)
    average_value = toolopt.getvalue('preAverageValue', 10)
    niters = toolopt.getvalue('numIterations', 1)
    

    sel = cmds.ls(sl=True)
    atgp = sel[0]
    srcgp = sel[1]
    dstgp = sel[2]


    if not cmds.pluginInfo('cyWldSkeletonTransferNode', q=True, l=True):
        cmds.loadPlugin('cyWldSkeletonTransferNode')
    stnode = cmds.createNode('cyWldSkeletonTransferNode')
    cmds.setAttr(stnode+'.iteration', niters)

    modes = cmds.attributeQuery('matchMode', n=stnode, listEnum=True)[0].split(':')
    mmindex = modes.index(mm.lower())
    cmds.setAttr(stnode+'.matchMode', mmindex)

    cmds.setAttr(stnode+'.enable', False)

    atmeshes = apiutils.get_typenodes(types='mesh', target=atgp)
    for i, n in enumerate(atmeshes):
        cmds.connectAttr(n+'.worldMesh', stnode + '.atchIn[%d]' % i)
        #dst = cmds.duplicate(n.name())[0]
        #cmds.setAttr(dst+'.t', 0, 0, 0)
        #cmds.setAttr(dst+'.r', 0, 0, 0)
        #cmds.setAttr(dst+'.s', 1, 1, 1)
        dst = cmds.createNode('mesh', n=n.nodeName())
        cmds.sets(dst, e=True, forceElement='initialShadingGroup')

        cmds.connectAttr(stnode+'.atchOut[%d]' % i, dst+'.inMesh')
    srcmeshes = apiutils.get_typenodes(types='mesh', target=srcgp)
    dstmeshes = apiutils.get_typenodes(types='mesh', target=dstgp)

    
    extras = {'en_smooth':en_smooth, 'smooth_value':smooth_value, 'en_average':en_average, 'average_value':average_value}
    for i, m in enumerate(srcmeshes):
        connectmesh(m.name(), stnode, 'srcMesh[%d]' % i, extras)
    
    buf = list()
    used = list()
    for i, m in enumerate(dstmeshes):
        _src = [re.sub('.*:', '', x.nodeName()) for x in srcmeshes]
        index = None
        nodename = re.sub('.*:', '', m.nodeName())
        if nodename in _src:
            index = _src.index(nodename)
        if index != None:
            print('connectAttr ', m + '.worldMesh', stnode + '.dstMesh[%d]' % index)
            connectmesh(m.name(), stnode, 'dstMesh[%d]' % index, extras)    
            if index >= len(used):
                for j in range(index-len(used)+1):
                    used.append(False)
            used[index] = True
        else:
            buf.append(m)
    for m in buf:
        index = len(used)
        for i, v in enumerate(used):   
            if v != True:
                index = i
                break
        connectmesh(m.name(), stnode, 'dstMesh[%d]' % i, extras)
    cmds.setAttr(stnode+'.enable', True)




