import re
import tempfile
import os

import maya.cmds as cmds
import pymel.core as pm

import apiutils
import rigtools.skin.weight_cmds as wc


tmpwfile = os.path.join(tempfile.gettempdir(), 'tmp.wdata')
print(tmpwfile)

def get_skinnodes(node):
    jnts = pm.ls(cmds.listHistory(node.name()), type='joint')
    roots = apiutils.get_typenode_roots(jnts, type='joint')
    alljnts = roots + pm.listRelatives(roots, ad=True, type='joint')
    meshes = pm.ls(pm.listHistory(alljnts, f=True), type='mesh')
    skinclusters = pm.ls(pm.listHistory(alljnts, f=True), type='skinCluster')
    return roots, meshes, skinclusters

def export_weight(node):
    roots, meshes, scs = get_skinnodes(node)
    pm.select(roots)
    wc.export_weight_cmd(tmpwfile, force=True)

    pm.delete(scs)

    return [x.name() for x in roots], [x.name() for x in meshes]

def exe():
    src = apiutils.get_typenodes(target=cmds.ls(sl=True)[0], types='mesh')[0]
    dst = apiutils.get_typenodes(target=cmds.ls(sl=True)[1], types='mesh')[0]

    roots, meshes = export_weight(dst)

    iclone_tgs = cmds.ls(cmds.listHistory(src.name()), type='mesh', ni=True)
    iclone_tgs.remove(src.name())


    buf = cmds.listRelatives(dst.firstParent().name(), type='mesh', ad=True, f=True)
    io = cmds.ls(buf, type='mesh', io=True)[0]
    
    #cmds.select(io)
    
    for n in iclone_tgs:
        p = cmds.listRelatives(n, p=True, f=True)[0]
        cmds.rotate(-90, 0, 0, p, r=True, p=(0, 0, 0))

    idx = 584
    pt = cmds.xform(io + '.vtx[%d]' % idx, q=True, ws=True, t=True)
    ps = cmds.xform(iclone_tgs[0] + '.vtx[%d]' % idx, q=True, ws=True, t=True)
    d = [x[1]-x[0] for x in zip(ps, pt)]

    for n in iclone_tgs:
        p = cmds.listRelatives(n, p=True, f=True)[0]
        cmds.move(d[0], d[1], d[2], p, r=True)
        cmds.makeIdentity(p, apply=True, t=True, r=True, s=True, n=False, pn=True)



    cmds.delete(cmds.ls(cmds.listHistory(dst.name()), type='blendShape')[0])
    cmds.delete(cmds.ls(cmds.listRelatives(dst.firstParent().name(), type='mesh', c=True, f=True), io=True))

    #cmds.setAttr(io+'.intermediateObject', False)
    cmds.select(iclone_tgs)
    #cmds.select(io, add=True)
    cmds.select(dst.name(), add=True)

    bstg = cmds.blendShape()[0]
    cmds.select(roots, meshes)
    cmds.SmoothBindSkin()
    cmds.select(meshes)
    wc.import_weight_cmd(tmpwfile, 'Closest Point', delete_history=False, force=True)

    cmds.setKeyframe(bstg)
    cmds.cutKey(bstg, cl=True, at='en')
    cmds.setAttr(bstg+'.en', 1)

    bsorg = cmds.ls(cmds.listHistory(src.name()), type='blendShape')[0]
    con = cmds.listConnections(bsorg, s=True, d=False, type='animCurve', c=True, p=True)
    done = []
    for i in range(len(con))[::2]:
        #print 'con0:', con[i]
        #print 'con1:', con[i+1]
        name = re.sub('.*[.]', '', con[i])
        anm = re.sub('[.].*$', '', con[i+1])
        #print name, anm
        cmds.selectKey(anm, k=True)
        cmds.copyKey()
        buf = cmds.listConnections(bstg, s=True, d=False, type='animCurve', c=True)
        for j in range(len(buf))[::2]:

            #print 'buf0:', buf[j]
            #print 'buf1:', buf[j+1]
            sh = re.sub('.*[.]', '', buf[j])
            if re.search(name, sh):
                tganm = buf[j+1]
                if tganm in done:
                    shapes = cmds.listConnections(bstg+'.inputTarget[0].inputTargetGroup', type='mesh', s=True, d=False)
                    cnt = len(shapes)
                    #print tganm, '-----' ,shapes[j/2]
                    buf = sh
                    if len(cmds.ls(buf))==0:
                        buf = '*:'+sh
                    tr = cmds.listRelatives(buf, f=True, p=True)[0]
                    trname = re.sub('.*[|:]', '', tr)

                    cmds.blendShape(bstg, e=True, t=[dst.name(), cnt , tr , 1.0])
                    cmds.setKeyframe(bstg+'.'+trname)
                    tganm = cmds.listConnections(bstg+'.'+trname, s=True, d=False, type='animCurve')[0]
                    
                #print 'Found: ', sh, tganm
                cmds.selectKey(tganm)
                cmds.pasteKey()
                done.append(tganm)
                break


    cmds.delete([cmds.listRelatives(x, f=True, p=True)[0] for x in iclone_tgs])
    roots, meshes, scs = get_skinnodes(src)
    pm.delete(roots)
    pm.delete([x.firstParent() for x in meshes])