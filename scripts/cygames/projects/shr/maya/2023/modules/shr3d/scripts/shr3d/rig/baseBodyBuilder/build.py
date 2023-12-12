# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pymel.core as pm
import maya.cmds as mc

from . import command
from . import setup


import importlib
importlib.reload(setup)
importlib.reload(command)


# ------------------------------------------------------------------------------
# build: generate joint
# ------------------------------------------------------------------------------
def generateJoint(info={}):
    log = ''
    hList = mc.ls('_guideHidden_GP', dag=True, typ='hikEffector')
    for k, v in info.items():
        #-- main
        if not 'e' in k:
            if v[0]:
                if not v[0] in hList:
                    #-- create joint
                    g = pm.PyNode('_{0}_guide'.format(v[1][0]))
                    p = pm.xform(g, ws=True, t=True, q=True)
                    j = command.addNode('joint', n=v[0])  
                    #-- set joint attributes
                    j.segmentScaleCompensate.set(0)
                    j.side.set(v[2][0])
                    j.typ.set(v[2][1])
                    j.otherType.set(v[2][2])
                    j.radius.set(v[2][3])
                    #-- move
                    pm.move(p[0], p[1], p[2], j, a=True)
                    #-- log
                    log += '{0:30}: {1}\n'.format(g.name(), j.name())

        #-- extra
        elif 'e' in k:
            if v[0]:
                if not v[0] in hList:
                    # -- create joint
                    g = pm.PyNode('_{0}_guide'.format(v[1][0]))
                    p = pm.xform(g, ws=True, t=True, q=True)
                    j = command.addNode('joint', n=v[0])  
                    # -- set joint attributes
                    j.segmentScaleCompensate.set(0)
                    j.side.set(v[2][0])
                    j.typ.set(v[2][1])
                    j.otherType.set(v[2][2])
                    j.radius.set(v[2][3])
                    #-- move
                    pm.move(p[0], p[1], p[2], j, a=True)
                    #-- parent
                    
                    #-- log
                    log += '{0:30}: {1}\n'.format(g.name(), j.name())
                    
    print ('---- base body builder : generate joints ----')
    print (log)


# ------------------------------------------------------------------------------
# build: spine
# ------------------------------------------------------------------------------
def buildSpine(info={}):
    plv    = pm.PyNode(info['001'][0])
    sp0    = pm.PyNode(info['008'][0])
    spList = []
    log    = ''

    plv.tx.set(0)
    sp0.tx.set(0)
    
    # -- spine1 - spine9
    for i in range(23, 32):
        j = info['{0:03d}'.format(i)][0]
        if j:
            j = pm.PyNode(j)
            j.tx.set(0)
            spList.append(j)
    if spList:
        pm.parent(spList[0], sp0)
        command.chainParent(spList[::-1])
        spEnd = spList[-1]
    else:
        spEnd = sp0
    log  += 'build: {0:>10} successfully. End: {1:>8}'.format('spine', spEnd)

    # -- parent spine -> plvis
    sp0.setParent(plv)
    pm.select(d=True)
    print (log)
    return spEnd


# ------------------------------------------------------------------------------
# build: neck
# ------------------------------------------------------------------------------
def buildNeck(info={}, spEnd=''):
    spEnd  = pm.PyNode(spEnd)
    nk0    = pm.PyNode(info['020'][0])
    hed    = pm.PyNode(info['015'][0])
    nkList = []
    log    = ''

    nk0.tx.set(0)
    hed.tx.set(0)

    # -- neck1 - neck9
    for i in range(32, 41):
        j = info['{0:03d}'.format(i)][0]
        if j:
            j = pm.PyNode(j)
            j.tx.set(0)
            nkList.append(j)
    if nkList:
        pm.parent(nkList[0], nk0)
        command.chainParent(nkList[::-1])
        nkEnd = nkList[-1]
    else:
        nkEnd = nk0

    # -- parent: head -> neck -> spine
    hed.setParent(nkEnd)
    nk0.setParent(spEnd)
    pm.select(d=True)
    log  += 'build: {0:>10} successfully. End: {1:>8}'.format('neck', nkEnd)
    print (log)
    return nkEnd


def buildHeadDirection(info={}):
    #-- hand plane
    hed   = pm.PyNode(info['015'][0])
    plane = pm.PyNode('_head_facePlane')
    pm.delete(pm.orientConstraint(plane, hed, mo=False, w=1))


def buildHeadEnd(info={}):
    hed   = pm.PyNode(info['015'][0])
    hdEnd = pm.PyNode(info['e01'][0])
    hdEnd.setParent(hed)
    #setup.composeRotate([hdEnd])


# ------------------------------------------------------------------------------
# build: clavicle
# ------------------------------------------------------------------------------
def buildLeftClavicle(info={}, spEnd=''):
    spEnd  = pm.PyNode(spEnd)
    shd    = pm.PyNode(info['009'][0])
    clList = []
    log    = ''

    for i in ['018', '170']:
        j = info[i][0]
        if j:
            j = pm.PyNode(j)
            clList.append(j)
    if clList:
        v = [(0,0,0), (1,0,0), (0,0,1), 'vector', (0,0,1)]
        clList.append(shd)
        # -- clList: [clavicle0, clavicle1, shoulder]
        for k in range(0, len(clList)-1):
            t, s = clList[k], clList[k+1]
            pm.delete(pm.aimConstraint(s, t,
                                       w = 1.0,
                                       o = v[0],
                                     aim = v[1],
                                       u = v[2],
                                     wut = v[3], 
                                      wu = v[4]))
        command.chainParent(clList[:-1][::-1])
        # -- parent: clavicle0 -> spine
        clList[0].setParent(spEnd)
        pm.select(d=True)
        setup.composeRotate(clList[:-1])
        clEnd = clList[-2]
        log  += 'build: {0:>10} successfully. End: {1:>8}'.format('L_clavicle', clEnd)
    else:
        clEnd = sp0
        log  += 'build: {0:>10} doesn\'t exists. End: {1:>8}'.format('L_clavicle', clEnd)
    print (log)
    return clEnd


def buildLeftClavicle_quad(info={}, spEnd=''):
    spEnd  = pm.PyNode(spEnd)
    shd    = pm.PyNode(info['009'][0])
    clList = []
    log    = ''

    for i in ['018', '170']:
        j = info[i][0]
        if j:
            j = pm.PyNode(j)
            clList.append(j)
    if clList:
        v = [(0,0,0), (1,0,0), (0,0,1), 'vector', (0,0,1)]
        clList.append(shd)
        # -- clList: [clavicle0, clavicle1, shoulder]
        for k in range(0, len(clList)-1):
            t, s = clList[k], clList[k+1]
            pm.delete(pm.aimConstraint(s, t,
                                       w = 1.0,
                                       o = v[0],
                                     aim = v[1],
                                       u = v[2],
                                     wut = v[3], 
                                      wu = v[4]))
        command.chainParent(clList[:-1][::-1])
        # -- parent: clavicle0 -> spine
        clList[0].setParent(spEnd)
        pm.select(d=True)
        setup.composeRotate(clList[:-1])
        clEnd = clList[-2]
        log  += 'build: {0:>10} successfully. End: {1:>8}'.format('L_clavicle', clEnd)
    else:
        clEnd = sp0
        log  += 'build: {0:>10} doesn\'t exists. End: {1:>8}'.format('L_clavicle', clEnd)
    print (log)
    return clEnd


def buildRightClavicle(info={}, spEnd=''):
    spEnd  = pm.PyNode(spEnd)
    shd    = pm.PyNode(info['012'][0])
    clList = []
    log    = ''

    for i in ['019', '171']:
        j = info[i][0]
        if j:
            j = pm.PyNode(j)
            clList.append(j)
    if clList:
        v = [(0,0,0), (-1,0,0), (0,0,1), 'vector', (0,0,1)]
        clList.append(shd)
        # -- clList: [clavicle0, clavicle1, shoulder]
        for k in range(0, len(clList)-1):
            t, s = clList[k], clList[k+1]
            pm.delete(pm.aimConstraint(s, t,
                                       w = 1.0,
                                       o = v[0],
                                     aim = v[1],
                                       u = v[2],
                                     wut = v[3], 
                                      wu = v[4]))
        command.chainParent(clList[:-1][::-1])
        # -- parent: clavicle0 -> spine
        clList[0].setParent(spEnd)
        pm.select(d=True)
        setup.composeRotate(clList[:-1])
        clEnd = clList[-2]
        log  += 'build: {0:>10} successfully. End: {1:>8}'.format('R_clavicle', clEnd)
    else:
        clEnd = sp0
        log  += 'build: {0:>10} doesn\'t exists. End: {1:>8}'.format('R_clavicle', clEnd)
    print (log)
    return clEnd


def buildRightClavicle_quad(info={}, spEnd=''):
    spEnd  = pm.PyNode(spEnd)
    shd    = pm.PyNode(info['012'][0])
    clList = []
    log    = ''

    for i in ['019', '171']:
        j = info[i][0]
        if j:
            j = pm.PyNode(j)
            clList.append(j)
    if clList:
        v = [(0,0,0), (-1,0,0), (0,0,1), 'vector', (0,0,1)]
        clList.append(shd)
        # -- clList: [clavicle0, clavicle1, shoulder]
        for k in range(0, len(clList)-1):
            t, s = clList[k], clList[k+1]
            pm.delete(pm.aimConstraint(s, t,
                                       w = 1.0,
                                       o = v[0],
                                     aim = v[1],
                                       u = v[2],
                                     wut = v[3], 
                                      wu = v[4]))
        command.chainParent(clList[:-1][::-1])
        # -- parent: clavicle0 -> spine
        clList[0].setParent(spEnd)
        pm.select(d=True)
        setup.composeRotate(clList[:-1])
        clEnd = clList[-2]
        log  += 'build: {0:>10} successfully. End: {1:>8}'.format('R_clavicle', clEnd)
    else:
        clEnd = sp0
        log  += 'build: {0:>10} doesn\'t exists. End: {1:>8}'.format('R_clavicle', clEnd)
    print (log)
    return clEnd



# ------------------------------------------------------------------------------
# build: arm
# ------------------------------------------------------------------------------
def buildLeftArm(info, clEnd=''):
    clEnd  = pm.PyNode(clEnd)
    shd    = pm.PyNode(info['009'][0])
    elb    = pm.PyNode(info['010'][0])
    wrt    = pm.PyNode(info['011'][0])
    log    = ''

    shd.setParent(clEnd)
    # -- elbow -> shoulder
    v = [(0,0,0),(1,0,0),(0,0,1),'object',wrt]
    pm.delete(pm.aimConstraint(elb, shd,
                               w = 1.0,
                               o = v[0],
                             aim = v[1],
                               u = v[2],
                             wut = v[3], 
                             wuo = v[4]))
    elb.setParent(shd)
    # -- L elbow
    v = [(0,0,0),(1,0,0),(0,0,1),'object',shd]
    pm.delete(pm.aimConstraint(wrt, elb,
                               w = 1.0,
                               o = v[0],
                             aim = v[1],
                               u = v[2],
                             wut = v[3], 
                             wuo = v[4]))
    
    # -- parent
    wrt.setParent(elb)
    setup.composeRotate([shd, elb, wrt])
    
    # -- L wrist
    wrt.r.set(0,0,0)
    wrt.jo.set(0,0,0)

    log  += 'build: {0:>10} successfully. End: {1:>8}'.format('L_arm', wrt)
    print (log)
    return wrt


def buildLeftArm_quad(info, clEnd=''):
    clEnd  = pm.PyNode(clEnd)
    shd    = pm.PyNode(info['009'][0])
    elb    = pm.PyNode(info['010'][0])
    wrt    = pm.PyNode(info['011'][0])
    log    = ''

    shd.setParent(clEnd)
    # -- elbow -> shoulder
    v = [(0,0,0), (0,-1,0), (0,0,1), 'object', wrt]
    pm.delete(pm.aimConstraint(elb, shd,
                               w = 1.0,
                               o = v[0],
                             aim = v[1],
                               u = v[2],
                             wut = v[3], 
                             wuo = v[4]))
    elb.setParent(shd)
    # -- L elbow
    v = [(0,0,0), (0,-1,0), (0,0,1), 'object', shd]
    pm.delete(pm.aimConstraint(wrt, elb,
                               w = 1.0,
                               o = v[0],
                             aim = v[1],
                               u = v[2],
                             wut = v[3], 
                             wuo = v[4]))
    
    # -- parent
    wrt.setParent(elb)
    setup.composeRotate([shd, elb, wrt])
    
    # -- L wrist
    wrt.r.set(0,0,0)
    wrt.jo.set(0,0,0)

    log  += 'build: {0:>10} successfully. End: {1:>8}'.format('L_arm', wrt)
    print (log)
    return wrt


def buildRightArm(info, clEnd=''):
    clEnd  = pm.PyNode(clEnd)
    shd    = pm.PyNode(info['012'][0])
    elb    = pm.PyNode(info['013'][0])
    wrt    = pm.PyNode(info['014'][0])
    log    = ''

    shd.setParent(clEnd)
    # -- elbow -> shoulder
    v = [(0,0,0), (-1,0,0), (0,0,1), 'object', wrt]
    pm.delete(pm.aimConstraint(elb, shd,
                               w = 1.0,
                               o = v[0],
                             aim = v[1],
                               u = v[2],
                             wut = v[3], 
                             wuo = v[4]))
    elb.setParent(shd)
    # -- L elbow
    v = [(0,0,0), (-1,0,0), (0,0,1), 'object', shd]
    pm.delete(pm.aimConstraint(wrt, elb,
                               w = 1.0,
                               o = v[0],
                             aim = v[1],
                               u = v[2],
                             wut = v[3], 
                             wuo = v[4]))
    # -- parent
    wrt.setParent(elb)
    setup.composeRotate([shd, elb, wrt])
    # -- L wrist
    wrt.r.set(0,0,0)
    wrt.jo.set(0,0,0)
    log  += 'build: {0:>10} successfully. End: {1:>8}'.format('R_arm', wrt)
    print (log)
    return wrt


def buildRightArm_quad(info, clEnd=''):
    clEnd  = pm.PyNode(clEnd)
    shd    = pm.PyNode(info['012'][0])
    elb    = pm.PyNode(info['013'][0])
    wrt    = pm.PyNode(info['014'][0])
    log    = ''

    shd.setParent(clEnd)
    # -- elbow -> shoulder
    v = [(0,0,0), (0,-1,0), (0,0,1), 'object', wrt]
    pm.delete(pm.aimConstraint(elb, shd,
                               w = 1.0,
                               o = v[0],
                             aim = v[1],
                               u = v[2],
                             wut = v[3], 
                             wuo = v[4]))
    elb.setParent(shd)
    # -- L elbow
    v = [(0,0,0), (0,-1,0), (0,0,1), 'object', shd]
    pm.delete(pm.aimConstraint(wrt, elb,
                               w = 1.0,
                               o = v[0],
                             aim = v[1],
                               u = v[2],
                             wut = v[3], 
                             wuo = v[4]))
    # -- parent
    wrt.setParent(elb)
    setup.composeRotate([shd, elb, wrt])
    # -- L wrist
    wrt.r.set(0,0,0)
    wrt.jo.set(0,0,0)
    log  += 'build: {0:>10} successfully. End: {1:>8}'.format('R_arm', wrt)
    print (log)
    return wrt


# ------------------------------------------------------------------------------
# build: arm twist
# ------------------------------------------------------------------------------
def buildWristDirection(wtEnd='', side='L'):
    #-- hand plane
    wtEnd = pm.PyNode(wtEnd)
    plane = pm.PyNode('_{0}_hand_floorPlane'.format(side))
    pm.delete(pm.orientConstraint(plane, wtEnd, mo=False, w=1))


# ------------------------------------------------------------------------------
# build finger base
# ------------------------------------------------------------------------------
def buildLeftFingerBase_quad(info, wtEnd=''):
    wtEnd = pm.PyNode(wtEnd)
    tob   = pm.PyNode(info['021'][0])
    toe   = pm.PyNode(info['147'][0])
    log   = ''
    # -- L ball
    tob.setParent(wtEnd)
    tob.r.set(0,0,0)
    tob.jo.set(0,0,0)
    # -- L toe
    toe.setParent(tob)
    toe.r.set(0,0,0)
    toe.jo.set(0,0,0)
    log += 'build: {0:>10} successfully. End: {1:>8}'.format('L_foot', '')
    print (log)


def buildRightFingerBase_quad(info, wtEnd=''):
    wtEnd = pm.PyNode(wtEnd)
    tob   = pm.PyNode(info['022'][0])
    toe   = pm.PyNode(info['153'][0])
    log   = ''
    # -- L ball
    tob.setParent(wtEnd)
    tob.r.set(0,0,0)
    tob.jo.set(0,0,0)
    # -- L toe
    toe.setParent(tob)
    toe.r.set(0,0,0)
    toe.jo.set(0,0,0)
    log += 'build: {0:>10} successfully. End: {1:>8}'.format('R_foot', '')
    print (log)




# ------------------------------------------------------------------------------
# build finger
# ------------------------------------------------------------------------------
def buildLeftInHand(info={}, wtEnd=''):
    wtEnd  = pm.PyNode(wtEnd)
    avList = [[(0,0,0), (1,0,0), (0,0,1), 'object', '_L_thumb_upGuide'],
              [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_index_upGuide'],
              [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_middle_upGuide'],
              [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_ring_upGuide'],
              [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_pinky_upGuide'],
              [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_extra_upGuide'],
             ]
    ihList  = ['146','147','148','149','150','151']
    frList  = ['050','054','058','062','066','070']
    endList = []
    log     = ''

    #-- inhand
    for i in range(6):
        j = info[ihList[i]][0]
        v = avList[i]
        f = info[frList[i]][0]
        if j:
            j = pm.PyNode(j)
            endList.append(j)
            if f:
                pm.delete(pm.aimConstraint(f, j, 
                                           w = 1.0,
                                           o = v[0],
                                         aim = v[1],
                                           u = v[2],
                                         wut = v[3], 
                                         wuo = v[4]))
            else:
                j.r.set(0,0,0)
                j.jo.set(0,0,0)
            j.setParent(wtEnd)
            log  += 'build: {0:>10} successfully. End: {1:>8}\n'.format(j.name(), j.name())
        else:
            endList.append(wtEnd)
    setup.composeRotate(endList)
    print (log)
    return endList


def buildLeftInHand_quad(info={}, wtEnd=''):
    wtEnd  = pm.PyNode(wtEnd)
    avList = [[(0,0,0), (1,0,0), (0,0,1), 'object', '_L_thumb_upGuide'],
              [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_index_upGuide'],
              [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_middle_upGuide'],
              [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_ring_upGuide'],
              [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_pinky_upGuide'],
              [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_extra_upGuide'],
             ]
    ihList  = ['146','147','148','149','150','151']
    frList  = ['050','054','058','062','066','070']
    endList = []
    log     = ''

    #-- inhand
    for i in range(6):
        j = info[ihList[i]][0]
        v = avList[i]
        f = info[frList[i]][0]
        if j:
            j = pm.PyNode(j)
            endList.append(j)
            if f:
                pm.delete(pm.aimConstraint(f, j, 
                                           w = 1.0,
                                           o = v[0],
                                         aim = v[1],
                                           u = v[2],
                                         wut = v[3], 
                                         wuo = v[4]))
            else:
                j.r.set(0,0,0)
                j.jo.set(0,0,0)
            j.setParent(wtEnd)
            log  += 'build: {0:>10} successfully. End: {1:>8}\n'.format(j.name(), j.name())
        else:
            endList.append(wtEnd)
    setup.composeRotate(endList)
    print (log)
    return endList


def buildRightInHand(info={}, wtEnd=''):
    wtEnd  = pm.PyNode(wtEnd)
    avList = [[(0,0,0), (-1,0,0), (0,0,1), 'object', '_R_thumb_upGuide'],
              [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_index_upGuide'],
              [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_middle_upGuide'],
              [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_ring_upGuide'],
              [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_pinky_upGuide'],
              [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_extra_upGuide'],         
             ]
    ihList  = ['152','153','154','155','156','157']
    frList  = ['074','078','082','086','090','094']
    endList = []
    log     = ''
    # -- inhand
    for i in range(6):
        j = info[ihList[i]][0]
        v = avList[i]
        f = info[frList[i]][0]
        if j:
            j = pm.PyNode(j)
            endList.append(j)
            if f:
                pm.delete(pm.aimConstraint(f, j, 
                                           w = 1.0,
                                           o = v[0],
                                         aim = v[1],
                                           u = v[2],
                                         wut = v[3], 
                                         wuo = v[4]))
            else:
                j.r.set(0,0,0)
                j.jo.set(0,0,0)
            j.setParent(wtEnd)
            log  += 'build: {0:>10} successfully. End: {1:>8}\n'.format(j.name(), j.name())
        else:
            endList.append(wtEnd)
    setup.composeRotate(endList)
    print (log)
    return endList    


def buildRightInHand_quad(info={}, wtEnd=''):
    wtEnd  = pm.PyNode(wtEnd)
    avList = [[(0,0,0), (-1,0,0), (0,0,1), 'object', '_R_thumb_upGuide'],
              [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_index_upGuide'],
              [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_middle_upGuide'],
              [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_ring_upGuide'],
              [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_pinky_upGuide'],
              [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_extra_upGuide'],         
             ]
    ihList  = ['022']
    frList  = ['153']
    endList = []
    log     = ''
    # -- inhand
    for i in range(6):
        j = info[ihList[i]][0]
        v = avList[i]
        f = info[frList[i]][0]
        if j:
            j = pm.PyNode(j)
            endList.append(j)
            if f:
                pm.delete(pm.aimConstraint(f, j, 
                                           w = 1.0,
                                           o = v[0],
                                         aim = v[1],
                                           u = v[2],
                                         wut = v[3], 
                                         wuo = v[4]))
            else:
                j.r.set(0,0,0)
                j.jo.set(0,0,0)
            j.setParent(wtEnd)
            log  += 'build: {0:>10} successfully. End: {1:>8}\n'.format(j.name(), j.name())
        else:
            endList.append(wtEnd)
    setup.composeRotate(endList)
    print (log)
    return endList    


lhfi = [[['050', '051', '052', '053'], [(0,0,0), (1,0,0), (0,0,1), 'object', '_L_thumb_upGuide']],
        [['054', '055', '056', '057'], [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_index_upGuide']],
        [['058', '059', '060', '061'], [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_middle_upGuide']],
        [['062', '063', '064', '065'], [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_ring_upGuide']],
        [['066', '067', '068', '069'], [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_pinky_upGuide']],
        [['070', '071', '072', '073'], [(0,0,0), (1,0,0), (0,1,0), 'object', '_L_extra_upGuide']],
       ]

rhfi = [[['074', '075', '076', '077'], [(0,0,0), (-1,0,0), (0,0,1), 'object', '_R_thumb_upGuide']],
        [['078', '079', '080', '081'], [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_index_upGuide']],
        [['082', '083', '084', '085'], [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_middle_upGuide']],
        [['086', '087', '088', '089'], [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_ring_upGuide']],
        [['090', '091', '092', '093'], [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_pinky_upGuide']],
        [['094', '095', '096', '097'], [(0,0,0), (-1,0,0), (0,1,0), 'object', '_R_extra_upGuide']],
       ]


#-- build Left Fingers ---------------------------------------------------------
def buildLeftFinger(info={}, fid=0, ihEnd=''):
    fName = ['thumb', 'index', 'middle', 'ring', 'pinky', 'extra']
    fList = [info[i][0] for i in lhfi[fid][0] if info[i][0]]
    v     = lhfi[fid][1]
    jList = [] 
    log   = ''
    if fList: 
        for t, s in zip(fList[:-1], fList[1:]):
            if t:
                t = pm.PyNode(t)
                if s:
                    s = pm.PyNode(s)
                    pm.delete(pm.aimConstraint(s, t,
                                               w = 1.0,
                                               o = v[0],
                                             aim = v[1],
                                               u = v[2],
                                             wut = v[3], 
                                             wuo = v[4]))
                    log += 'build: {0:>10} successfully.\n'.format(t.name())
                else:
                    log += 'build: {0:>10} successfully. End: {0:>8}\n'.format(t.name())
            else:
                break
        command.chainParent(fList[::-1])
        pm.parent(fList[0], ihEnd)
        fEnd = pm.PyNode(fList[-1])
        fEnd.r.set(0,0,0)
        fEnd.jo.set(0,0,0)
        setup.composeRotate(fList)
    else:
        log  += 'build: Left {0:>10} doesn\'t exists.\n'.format(fName[fid])
    print (log)


#-- build Left Fingers ---------------------------------------------------------
def buildRightFinger(info={}, fid=0, ihEnd=''):
    fName = ['thumb', 'index', 'middle', 'ring', 'pinky', 'extra']
    fList = [info[i][0] for i in rhfi[fid][0] if info[i][0]]
    v     = rhfi[fid][1]
    jList = [] 
    log   = ''
    if fList: 
        for t, s in zip(fList[:-1], fList[1:]):
            if t:
                t = pm.PyNode(t)
                if s:
                    s = pm.PyNode(s)
                    pm.delete(pm.aimConstraint(s, t,
                                               w = 1.0,
                                               o = v[0],
                                             aim = v[1],
                                               u = v[2],
                                             wut = v[3], 
                                             wuo = v[4]))
                    log += 'build: {0:>10} successfully.\n'.format(t.name())
                else:
                    log += 'build: {0:>10} successfully. End: {0:>8}\n'.format(t.name())
            else:
                break
        command.chainParent(fList[::-1])
        pm.parent(fList[0], ihEnd)
        fEnd = pm.PyNode(fList[-1])
        fEnd.r.set(0,0,0)
        fEnd.jo.set(0,0,0)
        setup.composeRotate(fList)
    else:
        log  += 'build: Right {0:>10} doesn\'t exists.\n'.format(fName[fid])
    print (log)


#-- fix thumb rotation ---------------------------------------------------------
def fixInhandRotation(info={}):
    #-- left inHand
    lwt = pm.PyNode(info['011'][0])
    fid = [['050', '051'], ['147', '054'], ['148', '058'], 
           ['149', '062'], ['150', '066'], ['151', '070']]

    for id0, id1 in fid:
        if command.allOjbExists([info[id0][0], info[id1][0]]):
            lt0 = pm.PyNode(info[id0][0])
            lt1 = pm.PyNode(info[id1][0])
            lt1.setParent(w=True)
            lt0.r.set(0,0,0)
            #-- align thumb0 rotation to wrist
            pm.delete(pm.aimConstraint(lt1, lt0, o=(0,0,0), w=1, aim=(1,0,0), u=(0,1,0),
                                       wut='object', wuo=lwt, sk=('x', 'y')))
            lt1.setParent(lt0)   
            setup.composeRotate([lt1])

    #-- right inHand
    rwt = pm.PyNode(info['014'][0])
    fid = [['050', '051'], ['153', '078'], ['154', '082'], 
           ['155', '086'], ['156', '090'], ['157', '094']]

    for id0, id1 in fid:
        if command.allOjbExists([info[id0][0], info[id1][0]]):
            rt0 = pm.PyNode(info[id0][0])
            rt1 = pm.PyNode(info[id1][0])
            rt1.setParent(w=True)
            rt0.r.set(0,0,0)
            #-- align thumb0 rotation to wrist
            pm.delete(pm.aimConstraint(rt1, rt0, o=(0,0,0), w=1, aim=(1,0,0), u=(0,1,0),
                                       wut='object', wuo=rwt, sk=('x', 'y')))
            rt1.setParent(rt0)   
            setup.composeRotate([rt1])

    #-- set preferred angle
    pvj = pm.PyNode(info['001'][0])
    pm.joint(pvj, spa=True, ch=True, e=True)




# ------------------------------------------------------------------------------
# parent: leg
# ------------------------------------------------------------------------------
def buildLeftLeg(info={}):
    plv = pm.PyNode(info['001'][0])
    hip = pm.PyNode(info['002'][0])
    kne = pm.PyNode(info['003'][0])
    akl = pm.PyNode(info['004'][0])
    log = ''
    v   = [(0,0,0), (0,-1,0), (0,0,-1), 'object', akl]
    pm.delete(pm.aimConstraint(kne, hip, w = 1.0,
                                         o = v[0],
                                       aim = v[1],
                                         u = v[2],
                                       wut = v[3], 
                                       wuo = v[4]))
    # -- parent hip -> hip
    hip.setParent(plv)
    setup.composeRotate([hip])

    # -- L knee
    v   = [(0,0,0), (0,-1,0), (0,0,-1), 'object', hip]
    pm.delete(pm.aimConstraint(akl, kne, w = 1.0,
                                         o = v[0],
                                       aim = v[1],
                                         u = v[2],
                                       wut = v[3], 
                                       wuo = v[4]))
    kne.setParent(hip)
    setup.composeRotate([kne])

    # -- L ankle
    akl.setParent(kne)
    akl.r.set(0,0,0)
    akl.jo.set(0,0,0)
    log += 'build: {0:>10} successfully. End: {1:>8}'.format('L_leg', akl)
    print (log)
    return akl


def buildRightLeg(info={}):
    plv = pm.PyNode(info['001'][0])
    hip = pm.PyNode(info['005'][0])
    kne = pm.PyNode(info['006'][0])
    akl = pm.PyNode(info['007'][0])
    log = ''
    v   = [(0,0,0), (0,-1,0), (0,0,-1), 'object', akl]
    pm.delete(pm.aimConstraint(kne, hip, w = 1.0,
                                         o = v[0],
                                       aim = v[1],
                                         u = v[2],
                                       wut = v[3], 
                                       wuo = v[4]))
    # -- parent
    hip.setParent(plv)
    setup.composeRotate([hip])

    # -- R knee
    v   = [(0,0,0), (0,-1,0), (0,0,-1), 'object', hip]
    pm.delete(pm.aimConstraint(akl, kne, w = 1.0,
                                         o = v[0],
                                       aim = v[1],
                                         u = v[2],
                                       wut = v[3], 
                                       wuo = v[4]))
    kne.setParent(hip)
    setup.composeRotate([kne])
    
    # -- R ankle
    akl.setParent(kne)
    akl.r.set(0,0,0)
    akl.jo.set(0,0,0)
    log += 'build: {0:>10} successfully. End: {1:>8}'.format('R_leg', akl)
    print (log)
    return akl


# ------------------------------------------------------------------------------
# build: leg twist
# ------------------------------------------------------------------------------
def buildAnkleDirection(akEnd='', side='L'):
    #-- hand plane
    akEnd = pm.PyNode(akEnd)
    plane = pm.PyNode('_{0}_foot_floorPlane'.format(side))
    pm.delete(pm.orientConstraint(plane, akEnd, mo=False, w=1))


# -----------------------------------------------------------------------------
# parent: Foot
# -----------------------------------------------------------------------------
def buildLeftFoot(info, akEnd=''):
    akEnd = pm.PyNode(akEnd)
    tob   = pm.PyNode(info['016'][0])
    toe   = pm.PyNode(info['118'][0])
    log   = ''
    # -- L ball
    tob.setParent(akEnd)
    tob.r.set(0,0,0)
    tob.jo.set(0,0,0)
    # -- L toe
    toe.setParent(tob)
    toe.r.set(0,0,0)
    toe.jo.set(0,0,0)
    log += 'build: {0:>10} successfully. End: {1:>8}'.format('L_foot', '')
    print (log)


def buildRightFoot(info, akEnd=''):
    akEnd = pm.PyNode(akEnd)
    tob   = pm.PyNode(info['017'][0])
    toe   = pm.PyNode(info['142'][0])
    log   = ''
    # -- L ball
    tob.setParent(akEnd)
    tob.r.set(0,0,0)
    tob.jo.set(0,0,0)
    # -- L toe
    toe.setParent(tob)
    toe.r.set(0,0,0)
    toe.jo.set(0,0,0)
    log += 'build: {0:>10} successfully. End: {1:>8}'.format('R_foot', '')
    print (log)


# -----------------------------------------------------------------------------
# system joint generate
# -----------------------------------------------------------------------------
def generateSysJoint(info={}):
    log = ''
    for k, v in info.items():
        if v[0]:
            # -- create joint
            j = addNode('joint', n=v[0]) 
            p = v[3]
            # -- set joint attributes
            j.segmentScaleCompensate.set(0)
            j.side.set(v[2][0])
            j.typ.set(v[2][1])
            j.otherType.set(v[2][2])
            j.radius.set(v[2][3])
            # -- move
            pm.move(p[0], p[1], p[2], j, a=True)
            # -- log
            log += '{0:30}: {1}\n'.format(k, j.name())
    print ('---- base body builder : generate system joints ----')
    print (log)


def parentSysJoint(info={}):
    for k, v in info.items():
        if v[1][1]:
            j = pm.PyNode(v[0])
            j.setParent(v[1][1])


def buildParentRootJoint(info={}):
    plv    = pm.PyNode(info['001'][0])
    rtjt   = pm.PyNode(info['e00'][0])
    plv.setParent(rtjt)


#-------------------------------------------------------------------------------
#-- aim angle
#-------------------------------------------------------------------------------
def setHandFloorAngle(ax='XZ'):
    loc   = pm.spaceLocator(n='_L_hand_worldDirection')
    #guide = pm.PyNode('_L_wrist_guide')
    guide = pm.PyNode('_L_hand_floorPlane')    
    
    if ax == 'XZ':
        pm.matchTransform(loc, guide, pos=True, scl=True, sp=True, ry=True)
        pm.matchTransform(guide, loc, pos=True, scl=True, sp=True, rot=True)
        
    elif ax == 'XY':
        loc.rx.set(90)
        pm.matchTransform(loc, guide, pos=True, scl=True, sp=True)
        pm.matchTransform(guide, loc, pos=True, scl=True, sp=True, rot=True)

    #-- delete locator
    pm.delete(loc)


def setFootFloorAngle(ax='XZ'):
    loc   = pm.spaceLocator(n='_L_foot_worldDirection')
    #guide = pm.PyNode('_L_ankle_guide')
    guide = pm.PyNode('_L_foot_floorPlane')    
    
    if ax == 'XZ':
        pm.matchTransform(loc, guide, pos=True, scl=True, sp=True, ry=True)
        pm.matchTransform(guide, loc, pos=True, scl=True, sp=True, rot=True)
        
    elif ax == 'XY':
        loc.rx.set(90)
        pm.matchTransform(loc, guide, pos=True, scl=True, sp=True)
        pm.matchTransform(guide, loc, pos=True, scl=True, sp=True, rot=True)

    #-- delete locator
    pm.delete(loc)


#-------------------------------------------------------------------------------
#-- set preffered angle
#-------------------------------------------------------------------------------
def setPrefferedAngle():
    pm.joint('null', spa=True, ch=True, e=True)
    for j in pm.ls('null', dag=True):
        j.pa.set(l=True)
        j.jo.set(l=True)


def setJointDrawStyle():
    pm.setAttr('null.drawStyle', 2)
    pm.setAttr('_900.drawStyle', 2)


def sortHierarchy(rt=''):
    for i in sorted(mc.listRelatives(rt, c=True), reverse=True):
        pm.reorder(i, f=True)


#-------------------------------------------------------------------------------
#-- fix thumb rotation
#-------------------------------------------------------------------------------
'''
def fixThumbRotation():
    # --- left thumb
    lt0 = pm.PyNode('_200')
    lt1 = pm.PyNode('_201')
    lt1.setParent(w=True)
    lt0.r.set(0,0,0)
    pm.delete(pm.aimConstraint(lt1, lt0, o=(0,0,0),
                                         w=1.0,
                                       aim=(1,0,0),
                                         u=(0,1,0),
                                       wut='object',
                                       wuo='_00d',
                                        sk=('x', 'y')))
    lt1.setParent(lt0)   
    setup.composeRotate(['_201'])
    
    # --- right thumb
    rt0 = pm.PyNode('_100')
    rt1 = pm.PyNode('_101')
    rt1.setParent(w=True)
    rt0.r.set(0,0,0)
    pm.delete(pm.aimConstraint(rt1, rt0, o=(0,0,0),
                                         w=1.0,
                                       aim=(-1,0,0),
                                         u=(0,1,0),
                                       wut='object',
                                       wuo='_009',
                                        sk=('x', 'y')))
    rt1.setParent(rt0)   
    setup.composeRotate(['_101'])
    
    pm.joint('_000', spa=True, ch=True, e=True)
'''

# -----------------------------------------------------------------------------
# build skeleton : 
# -----------------------------------------------------------------------------
def testBuild(info={}):
    #-- build
    generateJoint(info)
    #-- Spine - Neck
    spEnd  = buildSpine(info)
    nkEnd  = buildNeck(info, spEnd)
    buildHeadDirection(info)
    buildHeadEnd(info)
    #-- Arm
    lClEnd = buildLeftClavicle(info, spEnd)
    rClEnd = buildRightClavicle(info, spEnd)
    lWtEnd = buildLeftArm(info, lClEnd)
    rWtEnd = buildRightArm(info, rClEnd)
    buildWristDirection(lWtEnd, 'L')
    buildWristDirection(rWtEnd, 'R')
    #-- Hand
    lIHEnd = buildLeftInHand(info, lWtEnd)
    rIHEnd = buildRightInHand(info, rWtEnd)
    for i in range(6):  
        buildLeftFinger(info, i, lIHEnd[i])
        buildRightFinger(info, i, rIHEnd[i])
    #-- Leg
    lAkEnd = buildLeftLeg(info)
    rAkEnd = buildRightLeg(info)
    buildAnkleDirection(lAkEnd, 'L')
    buildAnkleDirection(rAkEnd, 'R')
    buildLeftFoot(info, lAkEnd)
    buildRightFoot(info, rAkEnd)

    #-- thumb rotation
    fixInhandRotation(info)

    #-- root joint
    buildParentRootJoint(info)

    '''
    #-- create null 
    n = pm.createNode('joint', n='null')
    o = pm.createNode('joint', n='_900', p=n)
    #-- set prefered angle
    pm.joint('_000', spa=True, ch=True, e=True)
    #-- parent
    pm.parent('_000', '_900')
    #-- fix thumb rotation
    fixThumbRotation()
    '''


def quadBuild(info={}):
    #-- build
    generateJoint(info)
    #-- Spine - Neck
    spEnd  = buildSpine(info)
    nkEnd  = buildNeck(info, spEnd)
    buildHeadDirection(info)
    buildHeadEnd(info)
    #-- Arm
    lClEnd = buildLeftClavicle_quad(info, spEnd)
    rClEnd = buildRightClavicle_quad(info, spEnd)
    lWtEnd = buildLeftArm_quad(info, lClEnd)
    rWtEnd = buildRightArm_quad(info, rClEnd)
    buildWristDirection(lWtEnd, 'L')
    buildWristDirection(rWtEnd, 'R')
    #-- Hand
    lIHEnd = buildLeftFingerBase_quad(info, lWtEnd)
    rIHEnd = buildRightFingerBase_quad(info, rWtEnd)
    #for i in range(6):  
    #    buildLeftFinger(info, i, lIHEnd[i])
    #    buildRightFinger(info, i, rIHEnd[i])
    #-- Leg
    lAkEnd = buildLeftLeg(info)
    rAkEnd = buildRightLeg(info)
    buildAnkleDirection(lAkEnd, 'L')
    buildAnkleDirection(rAkEnd, 'R')
    buildLeftFoot(info, lAkEnd)
    buildRightFoot(info, rAkEnd)

    #-- thumb rotation
    fixInhandRotation(info)

    #-- root joint
    buildParentRootJoint(info)

    '''
    #-- create null 
    n = pm.createNode('joint', n='null')
    o = pm.createNode('joint', n='_900', p=n)
    #-- set prefered angle
    pm.joint('_000', spa=True, ch=True, e=True)
    #-- parent
    pm.parent('_000', '_900')
    #-- fix thumb rotation
    fixThumbRotation()
    '''



def rebuild(info={}):
    # -- unparent
    if pm.objExists('_000'):
        for i in pm.ls('_000', dag=True):
            i.setParent(w=True)
    # -- fit 
    for k, i in info.items():
        if i[0]:
            g = pm.PyNode('_{0}_guide'.format(i[1][0]))
            p = pm.xform(g, ws=True, t=True, q=True)
            pm.move(p[0], p[1], p[2], i[0], a=True)
    # -- rebuild
    spEnd  = buildSpine(info)
    nkEnd  = buildNeck(info, spEnd)
    lClEnd = buildLeftClavicle(info, spEnd)
    rClEnd = buildRightClavicle(info, spEnd)
    lWtEnd = buildLeftArm(info, lClEnd)
    rWtEnd = buildRightArm(info, rClEnd)
    lIHEnd = buildLeftInHand(info, lWtEnd)
    rIHEnd = buildRightInHand(info, rWtEnd)
    for i in range(6):  
        buildLeftFinger(info, i, lIHEnd[i])
        buildRightFinger(info, i, rIHEnd[i])
    lAkEnd = buildLeftLeg(info)
    rAkEnd = buildRightLeg(info)
    buildLeftFoot(info, lAkEnd)
    buildRightFoot(info, rAkEnd)

    '''
    # -- set prefered angle
    pm.joint('_000', spa=True, ch=True, e=True)
    # -- parent
    pm.parent('_000', '_900')
    # -- fix thumb rotation
    fixThumbRotation()
    '''


def runBuildBaseBody():
    generateJoint(dfDict)
    generateSysJoint(sysDict)
    parentSpine(dfDict, bDict['body'])
    buildCravicle()
    buildLeftArm()
    buildRightArm()
    buildLeftLeg()
    buildRightLeg()
    # -- finger
    for side in ['L_', 'R_']:
        for part in ['thumb', 'index', 'middle', 'ring', 'pinky']:
            f   = '{0}{1}'.format(side, part)
            buildFinger(dfDict, fDict[f][0], fDict[f][1], fDict[f][2])
    # -- parent system joints
    parentSysJoint(sysDict)
    # -- preffered angle
    setPrefferedAngle()
    # -- joint draw style
    setJointDrawStyle()
    # -- reorder
    sortHierarchy(rt='null')




# ------------------------------------------------------------------------------
# guide: scale
# ------------------------------------------------------------------------------
def scaleGuide(v=1.0):
    if pm.objExists('_guidePosition_GP'):
        gGrp = pm.PyNode('_guidePosition_GP')
        gGrp.s.set(v, v, v)


# edit height



