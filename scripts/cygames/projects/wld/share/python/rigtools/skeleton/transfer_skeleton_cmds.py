import sys
import re

import pymel.core as pm
import apiutils


import maya.api.OpenMaya as om
import maya.cmds as cmds

def exe():
    toolopt = apiutils.ToolOpt('Retarget_Skeleton')
    mm = toolopt.getvalue('matchMode', 'UV')
    objmm = toolopt.getvalue('objMatchMode', 'Object Name')
    ch = False and toolopt.getvalue('history', False)

    meshes = apiutils.get_typenodes('mesh')
    if len(meshes) < 1:
        raise Exception('Specify target mesh(es).')
    jnts = apiutils.get_typenodes('joint')
    pm.select(jnts)
    sk = pm.listConnections('.worldMatrix', s=False, d=True, type='skinCluster')
    if len(sk) == 0:
        pm.error('Cannot find any skinCluster.')
        return
    pm.select(sk)
    sets = pm.listConnections('.message', s=False, d=True, type='objectSet')
    if len(sets) == 0:
        pm.error('Cannot find any skinClusterSet.')
        return
    pm.select(sets)
    src = pm.listConnections('.memberWireframeColor', sh=True, s=False, d=True, type='mesh')
    if len(src) == 0:
        pm.error('Cannot find source meshes.')
        return

    if not pm.pluginInfo('cyWldSkeletonTransferNode', q=True, l=True):
        pm.loadPlugin('cyWldSkeletonTransferNode')
    stnode = pm.createNode('cyWldSkeletonTransferNode')
    pm.setAttr(stnode+'.iteration', 1)

    modes = pm.attributeQuery('matchMode', n=stnode, listEnum=True)[0].split(':')
    try:
        mmindex = modes.index(mm.lower())
        stnode.setAttr('matchMode', mmindex)

    except:
        pass

    stnode.setAttr('enable', False)
    for i, m in enumerate(src):
        pm.connectAttr(m + '.worldMesh', stnode + '.srcMesh[%d]' % i, f=True)
    buf = list()
    used = list()
    for i, m in enumerate(meshes):
        _src = [re.sub('.*:', '', x.nodeName()) for x in src]
        index = None
        nodename = re.sub('.*:', '', m.nodeName())
        if nodename in _src:
            index = _src.index(nodename)
        if index != None:
            #print 'connectAttr ', m + '.worldMesh', stnode + '.dstMesh[%d]' % index
            pm.connectAttr(m + '.worldMesh', stnode + '.dstMesh[%d]' % index, f=True)
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
        print('connectAttr ', m + '.worldMesh', stnode + '.dstMesh[%d]' % index)
        pm.connectAttr(m + '.worldMesh', stnode + '.dstMesh[%d]' % index, f=True)

    newjnts = apiutils.copy_hierarchy(types='joint', target=jnts[0])
    #print newjnts
    

    lcts = []
    for i, jnt in enumerate(newjnts):
        pm.connectAttr(jnt[0] + '.worldMatrix', stnode + '.inJointsPos[%d]' % i)
        lct = pm.spaceLocator()
        #lct.setAttr('v', False)
        lcts.append(lct)
        pm.connectAttr(stnode + '.outJointsPos[%d]' % i, lct + '.t')
        #pm.pointConstraint(lct, jnt[1], weight=1)
    #print lcts


    stnode.setAttr('enable', True)
    jnts = [x[1] for x in newjnts]

    set_jointorient(newjnts, lcts)

    if ch == 'True':
        pm.group(lcts, name='lctGroup')
        #for i, jnt in enumerate(jnts):
        #    pm.pointConstraint(lcts[i], jnt, weight=1)

    else:
        pm.select([x[1] for x in newjnts])        
        pm.delete(apiutils.get_typenodes(types='pointConstraint'))
        pm.delete(lcts)

    pm.select(jnts)
    
def get_worldpos(tr):
    sl = om.MGlobal.getSelectionListByName(tr.name())
    tr = om.MFnTransform(sl.getDagPath(0))
    v0 = tr.translation(om.MSpace.kWorld)
    return v0

def get_pairindex(newjnt, newjnts):
    buf = [x for x in newjnts if x[1]==newjnt]
    if len(buf)==0:
        return None
    index = newjnts.index(buf[0])
    return index, buf[0][0], buf[0][1]


def __set_jointorient(jnt, newjnts, lcts):
    index, orgjnt, _ = get_pairindex(jnt, newjnts)

    lct = lcts[index]

    v = pm.xform(lct, q=True, ws=True, t=True)
    pm.xform(jnt, ws=True, t=v)
    


    njnts = pm.listRelatives(jnt, c=True, type='joint')

    rot = None
    #print 'jnt:', jnt
    for njnt in njnts:
        index, cjnt, _ = get_pairindex(njnt, newjnts)

        v = pm.getAttr(cjnt+'.t')
        #print '\tcjnt:', cjnt, '  v:', v,  '    len(njnts):', len(njnts)
        sg = 0.0001
        if len(njnts)>1 and (abs(v[1])>sg or abs(v[2])>sg):
            continue

        lct = lcts[index]
        #if len(njnts)>1:
        #    print '\t[orgjnt]%s  [cjnt]%s  [jnt]%s  [lct]%s' % (orgjnt, cjnt, jnt, lct)
        p0 = get_worldpos(jnt)
        c0 = get_worldpos(njnt)
        p1 = get_worldpos(jnt)
        c1 = get_worldpos(lct)
        axis = (c0-p0) ^ (c1-p1)
        axis.normalize()
        angle = (c0-p0).angle(c1-p1)
        rot = om.MQuaternion(angle, axis)
        break

    if rot:
        slist = om.MGlobal.getSelectionListByName(jnt.name())
        tr = slist.getDagPath(0)
        fntr = om.MFnTransform(tr)
        _jo = pm.getAttr(jnt+'.jointOrient')
        k = 180.0/3.141592
        _jo = [x /k for x in _jo]
        
        orot = fntr.rotation()
        jo = om.MEulerRotation(_jo)
        
        pm.setAttr(jnt+'.r', 0, 0, 0)
        
        fntr.rotateBy(orot, om.MSpace.kWorld)
        fntr.rotateBy(rot, om.MSpace.kWorld)
        fntr.rotateBy(jo, om.MSpace.kWorld)

        x, y, z, _ = fntr.rotationComponents()
        pm.setAttr(jnt+'.r', 0, 0, 0)
        pm.setAttr(jnt+'.jointOrient', x * k, y * k, z * k)
        

    for i, njnt in enumerate(njnts):
        __set_jointorient(njnt, newjnts, lcts)

def set_jointorient(newjnts, lcts):
    roots = apiutils.get_typenode_roots([x[1] for x in newjnts], type='joint')
    for root in roots:
        __set_jointorient(root, newjnts, lcts)

        





