# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pymel.core as pm
import maya.cmds as mc

from . import command


# -----------------------------------------------------------------------------
# Guide Functions
# -----------------------------------------------------------------------------
def createGuide(i=''):
    g = pm.createNode('hikEffector', n='_{0}_guide'.format(i))
    # -- shape
    if i == 'root':
        g.markerLook.set(2)
    else:
        g.markerLook.set(3)
    # -- side
    if 'L_' in i:
        g.overrideEnabled.set(1)
        g.overrideColor.set(13)
    elif 'R_' in i:
        g.overrideEnabled.set(1)
        g.overrideColor.set(6)
    elif i in ['root', 'pelvis', 'crown']:
        g.overrideEnabled.set(1)
        g.overrideColor.set(17)
    else:
        g.overrideEnabled.set(1)
        g.overrideColor.set(9)
    # -- non-keyable
    g.pin.set(k=False, cb=False)
    g.px.set(k=False, cb=False)
    g.py.set(k=False, cb=False)
    g.pz.set(k=False, cb=False)
    g.rt.set(k=False, cb=False)
    g.rr.set(k=False, cb=False)
    g.radi.set(k=False, cb=False)
    g.mkl.set(k=False, cb=False)
    # -- add guide attr
    addGuideAttr(g)
    # -- return
    return g


def addGuideAttr(g=''):
    g    = pm.PyNode(g)
    tStr = '\
None:Root:Hip:Knee:Foot:Toe:Spine:Neck:Head:Collar:\
Shoulder:Elbow:Hand:Finger:Thumb:PropA:PropB:PropC:\
Other:IndexFinger:MiddleFinger:RingFinger:PinkyFinger:\
ExtraFinger:BigToe:IndexToe:MiddleToe:RingToe:PinkyToe:FootThumb'
    # -- add attr
    pm.addAttr(g, ln='_jointName', sn='_jn', dt='string')
    g._jn.set(k=False, cb=False)
    pm.addAttr(g, ln='_guideName', sn='_gn', dt='string')
    g._gn.set(k=False, cb=False)
    pm.addAttr(g, ln='_parentName', sn='_pn', dt='string')
    g._pn.set(k=False, cb=False)
    pm.addAttr(g, ln='_side', sn='_sd', at='enum', en='center:left:right:none:')
    g._sd.set(k=False, cb=False)
    pm.addAttr(g, ln='_type', sn='_typ', at='enum', en=tStr)
    g._typ.set(k=False, cb=False)
    pm.addAttr(g, ln='_jointLable', sn='_jl', dt='string')
    g._jl.set(k=False, cb=False)
    pm.addAttr(g, ln='_jointRadius', sn='_rad', at='double', min=0.01, dv=0.5)
    g._rad.set(k=False, cb=False)
    pm.addAttr(g, ln='_absolutePosition', sn='_ap', at='double3')
    pm.addAttr(g, ln='_absolutePositionX', sn='_apx', at='double', p='_absolutePosition')
    pm.addAttr(g, ln='_absolutePositionY', sn='_apy', at='double', p='_absolutePosition')
    pm.addAttr(g, ln='_absolutePositionZ', sn='_apz', at='double', p='_absolutePosition')
    g._ap.set(0,0,0)
    g._ap.set(k=False, cb=False)
    g._apx.set(k=False, cb=False)
    g._apy.set(k=False, cb=False)
    g._apz.set(k=False, cb=False)
    pm.addAttr(g, ln='_relativePosition', sn='_rp', at='double3')
    pm.addAttr(g, ln='_relativePositionX', sn='_rpx', at='double', p='_relativePosition')
    pm.addAttr(g, ln='_relativePositionY', sn='_rpy', at='double', p='_relativePosition')
    pm.addAttr(g, ln='_relativePositionZ', sn='_rpz', at='double', p='_relativePosition')
    g._rp.set(0,0,0)
    g._rp.set(k=False, cb=False)
    g._rpx.set(k=False, cb=False)
    g._rpy.set(k=False, cb=False)
    g._rpz.set(k=False, cb=False)
    pm.addAttr(g, ln='_sourceCompornents', sn='_sc', dt='string')
    g._sc.set(k=False, cb=False)


# ---- link curve
def createLinkCurve(src='', tgt=''):
    srcN = pm.PyNode(src) 
    tgtN = pm.PyNode(tgt)
    sDmx = command.getDecomposeMatrix(srcN)
    if not sDmx:
        sDmx = command.createDecomposeMatrix(srcN)
    tDmx = command.getDecomposeMatrix(tgtN)
    if not tDmx:
        tDmx = command.createDecomposeMatrix(tgtN)
    # -- curve
    crv = pm.curve(d=1,
                   p=[(0,0,0),(1,0,0)],
                   k=(0,1),
                   n='{0}_link'.format(tgt))
    cSh = crv.getShape()
    # -- connection
    pm.connectAttr('{0}.outputTranslate'.format(sDmx.name()),
                   '{0}.controlPoints[0]'.format(cSh.name()), f=True)
    pm.connectAttr('{0}.outputTranslate'.format(tDmx.name()),
                   '{0}.controlPoints[1]'.format(cSh.name()), f=True)
    return crv


# ---- distance 
def createDistance(src='', tgt=''):
    srcN = pm.PyNode(src) 
    tgtN = pm.PyNode(tgt)
    sDmx = command.getDecomposeMatrix(srcN)
    tDmx = command.getDecomposeMatrix(tgtN)
    pDst = pm.createNode('transform', n='{0}_distance'.format(tgt))
    dst  = pm.createNode('distanceDimShape', 
                         n='{0}_distanceShape'.format(tgt), 
                         p=pDst)
    dst.precision.set(2)
    # -- connection
    sDmx.outputTranslate >> dst.startPoint
    tDmx.outputTranslate >> dst.endPoint
    return [pDst, dst]


# ---- reverse connect between two object
def reverseConnection(src='', tgt=''):
    md = pm.createNode('multiplyDivide', n='_{0}_md'.format(src))
    s  = pm.PyNode(src)
    t  = pm.PyNode(tgt)
    s.t  >> md.i1
    md.o >> t.t
    md.op.set(1)
    md.i2.set(-1,1,1)


# ---- create ik plane polygon
def createGuidePlane(side='L_', guide=[], pv=[], n=''):
    posList = []
    cDict   = {'L_':[1,0,0],
               'R_':[0,0,1],
               'C_':[1,0,1]}
    for i in guide:
        posList.append((0,0,0))
    p = pm.polyCreateFacet(ch=False, tx=1, s=1, p=posList, n='{0}_guidePlane'.format(n))[0]
    # -- connect
    for i, g in enumerate(guide):
        # -- decompose matrix
        dmx = command.getDecomposeMatrix(g)
        if not dmx:
            dmx = command.createDecomposeMatrix(g)
        pm.connectAttr('{0}.ot'.format(dmx), 
                       '{0}.vtx[{1}]'.format(p, i), f=True)
        # -- vertex color
        a = 0.01
        if g in pv:
            a = 0.5
        pm.polyColorPerVertex('{0}.vtx[{1}]'.format(p, i),
                              r = cDict[side][0],
                              g = cDict[side][1],
                              b = cDict[side][2],
                              a = a,
                            cdo = True)
    # -- display orverride
    ps = pm.PyNode(p).getShape()
    ps.overrideEnabled.set(1)
    ps.overrideDisplayType.set(2)
    return p


# ---- up vector
def createUpGuide(side='L_', i=''):
    # -- create up vector guide
    ug = pm.createNode('hikEffector', n='_{0}{1}_upGuide'.format(side, i))
    ug.markerLook.set(2)
    g2 = pm.xform('_{0}{1}2_guide'.format(side, i), ws=True, t=True, q=True)
    if side == 'L_':
        if i == 'thumb':
            pm.move(g2[0]-5, g2[1]+5, g2[2]+5, ug, a=True)
        else:
            pm.move(g2[0]+5, g2[1]+5, g2[2], ug, a=True)

    elif side == 'R_':
        if i == 'thumb':
            pm.move(g2[0]+5, g2[1]+5, g2[2]+5, ug, a=True)
        else:
            pm.move(g2[0]-5, g2[1]+5, g2[2], ug, a=True)
    # -- create plane
    ugList = mc.ls('_{0}{1}*_guide'.format(side, i))[1:]
    ugList.append(ug.name())
    up = pm.PyNode(createGuidePlane(side, ugList, [ug.name()], n='_{0}{1}'.format(side, i)))
    # -- parent
    ug.setParent(ugGp)
    up.setParent(gpGp)
    return ug


# ------------------------------------------------------------------------------
# Setup Functions
# ------------------------------------------------------------------------------
def createGuideHierarchy():
    gdGp = pm.createNode('transform', n='_guide_GP')

    psGp = pm.createNode('transform', n='_guidePosition_GP', p=gdGp)
    psGp.overrideEnabled.set(1)
    psGp.overrideDisplayType.set(0)

    ghGP = pm.createNode('transform', n='_guideHidden_GP', p=psGp)
    ghGP.v.set(0, l=True)

    ugGp = pm.createNode('transform', n='_guideUpVector_GP', p=gdGp)
    ugGp.overrideEnabled.set(1)
    ugGp.overrideDisplayType.set(0)

    lkGp = pm.createNode('transform', n='_guideLink_GP', p=gdGp)
    lkGp.overrideEnabled.set(1)
    lkGp.overrideDisplayType.set(1)

    dsGp = pm.createNode('transform', n='_guideDistance_GP', p=gdGp)
    dsGp.overrideEnabled.set(1)
    dsGp.overrideDisplayType.set(1)

    ldGp = pm.createNode('transform', n='_L_guideDistance_GP', p=dsGp)
    ldGp.overrideEnabled.set(1)
    ldGp.overrideDisplayType.set(1)

    rdGp = pm.createNode('transform', n='_R_guideDistance_GP', p=dsGp)
    rdGp.overrideEnabled.set(1)
    rdGp.overrideDisplayType.set(1)

    cdGp = pm.createNode('transform', n='_C_guideDistance_GP', p=dsGp)
    cdGp.overrideEnabled.set(1)
    cdGp.overrideDisplayType.set(1)

    lhGp = pm.createNode('transform', n='_L_hand_guideDistance_GP', p=dsGp)
    lhGp.overrideEnabled.set(1)
    lhGp.overrideDisplayType.set(1)

    rhGp = pm.createNode('transform', n='_R_hand_guideDistance_GP', p=dsGp)
    rhGp.overrideEnabled.set(1)
    rhGp.overrideDisplayType.set(1)

    lhGp = pm.createNode('transform', n='_L_foot_guideDistance_GP', p=dsGp)
    lhGp.overrideEnabled.set(1)
    lhGp.overrideDisplayType.set(1)

    rhGp = pm.createNode('transform', n='_R_foot_guideDistance_GP', p=dsGp)
    rhGp.overrideEnabled.set(1)
    rhGp.overrideDisplayType.set(1)

    gpGp = pm.createNode('transform', n='_guidePlane_GP', p=ugGp)
    gpGp.overrideEnabled.set(1)
    gpGp.overrideDisplayType.set(1)

    return [gdGp, psGp, ghGP, ugGp, lkGp, dsGp, ldGp, 
            rdGp, cdGp, lhGp, rhGp, lhGp, rhGp, gpGp]


# ------------------------------------------------------------------------------
# ---- create part guide
# ------------------------------------------------------------------------------
def createBaseGuide(info={}):
    log = ''
    val = info['000']
    g = createGuide(val[1][0])
    g.radius.set(val[2][3]*2)
    g.t.set(val[3][0], val[3][1], val[3][2])
    command.createDecomposeMatrix(g)
    # ---- log
    log += 'Create Guide : {0: >24} : < Valid >'.format(g.name())
    print (log)
    return g


def createHipTransGuide(info={},  p='', htv=False):
    log = ''
    val = info['049']
    g = createGuide(val[1][0])
    g.radius.set(val[2][3]*2)
    g.t.set(val[3][0], val[3][1], val[3][2])
    g.setParent(p)
    # ---- log   
    if htv == True:
        log += 'Create Guide : {0: >24} : < Valid >'.format(g.name()) 
        print (log)
        return g
    else:
        g.setParent('_guideHidden_GP')
        log += 'Create Guide : {0: >24} : < Hidden >'.format(g.name())
        pag = '_{0}_guide'.format(info['001'][1][1])
        command.worldConnection(pag, g)
        print (log)
        return p


def createPelvisGuide(info={},  p=''):
    log = '' 
    val = info['001']
    g = createGuide(val[1][0])
    g.radius.set(val[2][3]*2)
    g.t.set(val[3][0], val[3][1], val[3][2])
    g.setParent(p)
    # ---- log
    log += 'Create Guide : {0: >24} : < Valid >'.format(g.name())
    print (log)
    return g


def createSpineGuide(info={}, uiv=3, p=''):
    idList = ['008','023','024','025','026','027','028','029','030','031']
    pList  = []
    log    = ''
    gList  = [createGuide(info[i][1][0]) for i in idList]
    vList  = [info[i] for i in idList] 
    for i, g, v in zip(range(10), gList, vList): 
        g.radius.set(v[2][3]*2)
        if i < uiv:
            pList.append(g)
            g.t.set(v[3][0], v[3][1], v[3][2])
            log += 'Create Guide : {0: >24} : < Valid >\n'.format(g.name()) 
        else:
            g.setParent('_guideHidden_GP')
            command.worldConnection(gList[uiv-1], g)
            log += 'Create Guide : {0: >24} : < Hidden >\n'.format(g.name()) 
    command.chainParent(pList[::-1])
    pList[0].setParent(p)
    # ---- log
    print (log)
    return pList[-1]


def createNeckGuide(info={}, nkv=1, p=''):
    iList = ['020','032','033','034','035','036','037','038','039','040']
    pList = []
    log   = '' 
    for i, num in enumerate(iList):
        val = info[num]
        g = createGuide(val[1][0])
        g.radius.set(val[2][3]*2)
        if i < nkv:
            pList.append(g)
            g.t.set(val[3][0], val[3][1], val[3][2])
            log += 'Create Guide : {0: >24} : < Valid >\n'.format(g.name()) 
        else:
            g.setParent('_guideHidden_GP')
            log += 'Create Guide : {0: >24} : < Hidden >\n'.format(g.name()) 
    command.chainParent(pList[::-1])
    pList[0].setParent(p)
    # ---- log
    print (log)
    return pList[-1]


def createHeadGuide(info={}, p=''):
    log = '' 
    val = info['015']
    g = createGuide(val[1][0])
    g.radius.set(val[2][3]*2)
    g.t.set(val[3][0], val[3][1], val[3][2])
    g.setParent(p)
    # ---- log
    log += 'Create Guide : {0: >24} : < Valid >'.format(g.name())
    print (log)
    return g


def createCrownGuide(info={}, p='', h=170.0):
    log = '' 
    g = createGuide('crown')
    g.radius.set(1.0)
    g.t.set(0.0, h, 0.0)
    g.setParent(p)
    # ---- log
    log += 'Create Guide : {0: >24} : < Valid >'.format(g.name())
    print (log)
    return g


def createClavicleGuide(info={}, clv=1, p='', side='L'):
    if side == 'L':
        iList = ['018','170']
    else:
        iList = ['019','171']
    pList = []
    log   = '' 
    for i, num in enumerate(iList):
        val = info[num]
        g = createGuide(val[1][0])
        g.radius.set(val[2][3]*2)
        if i < clv:
            pList.append(g)
            g.t.set(val[3][0], val[3][1], val[3][2])
            log += 'Create Guide : {0: >24} : < Valid >\n'.format(g.name())
        else:
            g.setParent('_guideHidden_GP')
            log += 'Create Guide : {0: >24} : < Hidden >\n'.format(g.name()) 
    if pList:
        command.chainParent(pList[::-1])
        pList[0].setParent(p)
    # ---- log
    print (log)
    return pList[-1]


def createArmGuide(info={}, p='', side='L'):
    if side == 'L':
        iList = ['009','010','011']
    else:
        iList = ['012','013','014']
    pList = []
    log   = '' 
    for i, num in enumerate(iList):
        val = info[num]
        g = createGuide(val[1][0])
        g.radius.set(val[2][3]*2)
        g.t.set(val[3][0], val[3][1], val[3][2])
        pList.append(g)
        log += 'Create Guide : {0: >24} : < Valid >\n'.format(g.name())
    command.chainParent(pList[::-1])
    pList[0].setParent(p)
    # ---- log
    print (log)
    return pList[-1]


def createFingerBase(info={}, fbv=1, p='', side='L'):
    if side == 'L':
        num = '021'
    else:
        num = '022'
    pList = []
    log   = ''
    val   = info[num]
    g = createGuide(val[1][0])
    g.radius.set(val[2][3]*2)
    g.t.set(val[3][0], val[3][1], val[3][2])
    if fbv:
        g.setParent(p)
        log += 'Create Guide : {0: >24} : < Valid >'.format(g.name())
        # ---- log
        print (log)
        return g
    else:
        g.setParent('_guideHidden_GP')
        log += 'Create Guide : {0: >24} : < Hidden >'.format(g.name())
        # ---- log
        print (log)
        return p


def createInhandGuide(info={}, p='', side='L', ihv=[0,0,0,0,0,0]):
    if side == 'L':
        iList = ['146','147','148','149','150','151']
    else:
        iList = ['152','153','154','155','156','157']
    eList = []
    log   = ''
    for i, num in zip(ihv, iList):
        val = info[num]
        g = createGuide(val[1][0])
        g.radius.set(val[2][3]*2)
        g.t.set(val[3][0], val[3][1], val[3][2])
        if i == True:
            eList.append(g)
            g.setParent(p)
            log += 'Create Guide : {0: >24} : < Valid >\n'.format(g.name())
        else:
            eList.append(p)
            g.setParent('_guideHidden_GP')
            log += 'Create Guide : {0: >24} : < Hidden >\n'.format(g.name()) 
    # ---- log
    print (log)
    return eList



def createFingerGuide(info={}, size=4, p='', side='L', part='thumb'):
    lfDict = {'thumb' :['050','051','052','053'],
              'index' :['054','055','056','057'],
              'middle':['058','059','060','061'],
              'ring'  :['062','063','064','065'],
              'pinky' :['066','067','068','069'],
              'extra' :['070','071','072','073']}
    rfDict = {'thumb' :['074','075','076','077'],
              'index' :['078','079','080','081'],
              'middle':['082','083','084','085'],
              'ring'  :['086','087','088','089'],
              'pinky' :['090','091','092','093'],
              'extra' :['094','095','096','097']}
    if side == 'L':
        iList = lfDict[part]
    else:
        iList = rfDict[part]
    pList = []
    log   = ''
    for i, num in enumerate(iList):
        val = info[num]
        g = createGuide(val[1][0])

        g.radius.set(val[2][3]*2)
        g.t.set(val[3][0], val[3][1], val[3][2])
        if i < size:
            pList.append(g)
            log += 'Create Guide : {0: >24} : < Valid >\n'.format(g.name())
        else:
            g.setParent('_guideHidden_GP')
            log += 'Create Guide : {0: >24} : < Hidden >\n'.format(g.name()) 
    command.chainParent(pList[::-1])
    if pList: 
        pList[0].setParent(p)
    # ---- log
    print (log)
    return pList


def createlegGuide(info={}, p='', side='L'):
    if side == 'L':
        iList = ['002','003','004']
    else:
        iList = ['005','006','007']
    pList = []
    log   = '' 
    for i, num in enumerate(iList):
        val = info[num]
        g = createGuide(val[1][0])
        g.radius.set(val[2][3]*2)
        g.t.set(val[3][0], val[3][1], val[3][2])
        pList.append(g)
        log += 'Create Guide : {0: >24} : < Valid >\n'.format(g.name())
    command.chainParent(pList[::-1])
    pList[0].setParent(p)
    # ---- log
    print (log)
    return pList[-1]


def createToeBase(info={}, tbv=1, p='', side='L'):
    if side == 'L':
        num = '016'
    else:
        num = '017'
    pList = []
    log   = ''
    val   = info[num]
    g = createGuide(val[1][0])
    g.radius.set(val[2][3]*2)
    g.t.set(val[3][0], val[3][1], val[3][2])
    if tbv:
        g.setParent(p)
        log += 'Create Guide : {0: >24} : < Valid >'.format(g.name())
        # ---- log
        print (log)
        return g
    else:
        g.setParent('_guideHidden_GP')
        log += 'Create Guide : {0: >24} : < Hidden >'.format(g.name())
        # ---- log
        print (log)
        return p


def createInfootGuide(info={}, p='', side='L', ifv=[0,0,0,0,0,0]):
    if side == 'L':
        iList = ['158','159','160','161','162','163']
    else:
        iList = ['164','165','166','167','168','169']
    eList = []
    log   = ''
    for i, num in zip(ifv, iList):
        val = info[num]
        g = createGuide(val[1][0])
        g.radius.set(val[2][3]*2)
        g.t.set(val[3][0], val[3][1], val[3][2])
        if i == True:
            g.setParent(p)
            eList.append(g)
            log += 'Create Guide : {0: >24} : < Valid >\n'.format(g.name())
        else:
            g.setParent('_guideHidden_GP')
            eList.append(p)
            log += 'Create Guide : {0: >24} : < Hidden >\n'.format(g.name())
    # ---- log
    print (log)
    return eList


def createFootFingerGuide(info={}, size=4, p='', side='L', part='thumb'):
    lfDict = {'thumb' :['098','099','100','101'],
              'index' :['102','103','104','105'],
              'middle':['106','107','108','109'],
              'ring'  :['110','111','112','113'],
              'pinky' :['114','115','116','117'],
              'extra' :['118','119','120','121']}
    rfDict = {'thumb' :['122','123','124','125'],
              'index' :['126','127','128','129'],
              'middle':['130','131','132','133'],
              'ring'  :['134','135','136','137'],
              'pinky' :['138','139','140','141'],
              'extra' :['142','143','144','145']}
    if side == 'L':
        iList = lfDict[part]
    else:
        iList = rfDict[part]
    pList = []
    log   = ''
    for i, num in enumerate(iList):
        val = info[num]
        g = createGuide(val[1][0])
        g.radius.set(val[2][3]*2)
        g.t.set(val[3][0], val[3][1], val[3][2])
        if i < size:
            pList.append(g)
            log += 'Create Guide : {0: >24} : < Valid >\n'.format(g.name())
        else:
            g.setParent('_guideHidden_GP')
            log += 'Create Guide : {0: >24} : < Hidden >\n'.format(g.name())
    command.chainParent(pList[::-1])
    if pList: 
        pList[0].setParent(p)
    # ---- log
    print (log)
    return pList


# ------------------------------------------------------------------------------
# Create Guide from UI
# ------------------------------------------------------------------------------
def createGuideFromUI(info={}, uiVal=[]):
    scv, hiv, spv, nkv, clv, uar, lar, ulr, llr, \
    iht, ihi, ihm, ihr, ihp, ihe, fbv, tfv, ifv, \
    mfv, rfv, pfv, efv, ift, ifi, ifm, ifr, ifp, \
    ife, tbv, ftv, fiv, fmv, frv, fpv, fev, htv = uiVal
    # ---- create guide hierarchy
    gList = createGuideHierarchy()
    # ---- body guide
    bsEnd = createBaseGuide(info)
    htEnd = createHipTransGuide(info, bsEnd, htv)
    plEnd = createPelvisGuide(info, htEnd)
    spEnd = createSpineGuide(info, spv, plEnd)
    nkEnd = createNeckGuide(info, nkv, spEnd)
    hdEnd = createHeadGuide(info, nkEnd)
    crown = createCrownGuide(info, hdEnd, hiv)
    # ---- arm guide
    lcEnd = createClavicleGuide(info, clv, spEnd, 'L')
    rcEnd = createClavicleGuide(info, clv, spEnd, 'R')
    lwEnd = createArmGuide(info, lcEnd, 'L')
    rwEnd = createArmGuide(info, rcEnd, 'R')
    lbEnd = createFingerBase(info, fbv, lwEnd, 'L')
    rbEnd = createFingerBase(info, fbv, rwEnd, 'R')
    lhEnd = createInhandGuide(info, lbEnd, 'L', [iht,ihi,ihm,ihr,ihp,ihe])
    rhEnd = createInhandGuide(info, rbEnd, 'R', [iht,ihi,ihm,ihr,ihp,ihe])
    # ---- finger guide
    for i, size, part in zip(lhEnd, [tfv, ifv, mfv, rfv, pfv, efv], \
                             ['thumb','index','middle','ring','pinky','extra']):
        createFingerGuide(info, size, i, 'L', part)
    for i, size, part in zip(rhEnd, [tfv, ifv, mfv, rfv, pfv, efv], \
                             ['thumb','index','middle','ring','pinky','extra']):
        createFingerGuide(info, size, i, 'R', part)
    # ---- leg guide
    laEnd = createlegGuide(info, plEnd, 'L')
    raEnd = createlegGuide(info, plEnd, 'R')
    ltEnd = createToeBase(info, tbv, laEnd, 'L')
    rtEnd = createToeBase(info, tbv, raEnd, 'R')
    lfEnd = createInfootGuide(info, ltEnd, 'L', [ift,ifi,ifm,ifr,ifp,ife])
    rfEnd = createInfootGuide(info, rtEnd, 'R', [ift,ifi,ifm,ifr,ifp,ife])
    # ---- foot guide
    for i, size, part in zip(lfEnd, [ftv, fiv, fmv, frv, fpv, fev], \
                             ['thumb','index','middle','ring','pinky','extra']):
        createFootFingerGuide(info, size, i, 'L', part)
    for i, size, part in zip(rfEnd, [ftv, fiv, fmv, frv, fpv, fev], \
                             ['thumb','index','middle','ring','pinky','extra']):
        createFootFingerGuide(info, size, i, 'R', part)
    # ---- parent
    bsEnd.setParent(gList[1])
    # ---- Link Curve
    for k, v in sorted(info.items()):
        src = '_{0}_guide'.format(v[1][1])
        tgt = '_{0}_guide'.format(v[1][0])
        if pm.objExists(src) and pm.objExists(tgt):
            crv = createLinkCurve(src, tgt)
            crv.setParent(gList[4])
            # ---- reverse connection
            if 'R_' in tgt:
                lg = tgt.replace('R_', 'L_')
                rg = tgt
                reverseConnection(lg, rg)


# ------------------------------------------------------------------------------
# Guide arrangement
# ------------------------------------------------------------------------------
def fitToSkeleton(dfDict={}):
    gList = [i[1:].replace('_guide', '') for i in mc.ls('_root_guide', dag=True)]
    mLog  = ''
    oLog  = ''
    for i in gList:
        for k, v in dfDict.items():
            if v[1][0] == i:
                if pm.objExists(v[0]):
                    p = pm.xform(v[0], ws=True, t=True, q=True)
                    pm.move(p[0], p[1], p[2], '_{0}_guide'.format(i), a=True, pcp=True)
                    mLog += 'move: {0} --> {1}\n'.format(i, v[0])
                oLog += '{0} doesn\'t find source joint.\n'.format(i)
    print (mLog)
    print (oLog)


def fitToMesh(g='', side=0, vtx=[]):
    # -- symmetry modeling : off
    pm.symmetricModelling(s=False, e=True)
    pm.mel.eval('reflectionSetMode none;')
    if vtx:
        if side == 0: # -- center
            d = command.getCenterPostion(vtx)
            pos = (0, d[1], d[2])
            pm.move(pos[0], pos[1], pos[2], g, a=True, pcp=True)
        elif side == 1: # -- Left
            pos = command.getCenterPostion(vtx)
            pm.move(pos[0], pos[1], pos[2], g, a=True, pcp=True)


# ------------------------------------------------------------------------------
# align guide
# ------------------------------------------------------------------------------
def alignFingerGuide():
    side = 'L_'
    for part in ['index', 'middle', 'ring', 'pinky']:
        f1g, f2g, f3g, f4g  = ['_{0}{1}{2}_guide'.format(side, part, i) for i in range(1,5)]
        f1l, f2l, f3l, f4l = [pm.spaceLocator(n='_{0}{1}{2}_alignLocator'.format(side, part, i)) for i in range(4)]
        pm.parent(f2l, f3l, f4l, f1l)
        pm.delete(pm.parentConstraint(f1g, f1l, mo=False))
        # -- aim constraint
        v = [(0,0,0),(1,0,0),(0,1,0),'object','_{0}{1}_upGuide'.format(side, part)]
        pm.delete(pm.aimConstraint(f4g, f1l, 
                                   w = 1.0,
                                   o = v[0],
                                 aim = v[1],
                                   u = v[2],
                                 wut = v[3], 
                                 wuo = v[4]))
        pm.delete(pm.pointConstraint(f2g, f2l, w=1, sk=['z']))
        pm.delete(pm.pointConstraint(f3g, f3l, w=1, sk=['z']))
        pm.delete(pm.pointConstraint(f4g, f4l, w=1, sk=['z']))
        pm.delete(pm.pointConstraint(f2l, f2g, w=1))
        pm.delete(pm.pointConstraint(f3l, f3g, w=1))
        pm.delete(pm.pointConstraint(f4l, f4g, w=1))
        pm.delete(f1l)

    part = 'thumb'
    f2g, f3g, f4g = ['_{0}{1}{2}_guide'.format(side, part, i) for i in range(2,5)]
    f2l, f3l, f4l = [pm.spaceLocator(n='_{0}{1}{2}_alignLocator'.format(side, part, i)) for i in range(1,4)]
    pm.parent(f3l, f4l, f2l)
    pm.delete(pm.parentConstraint(f2g, f2l, mo=False))
    # -- aim constraint
    v = [(0,0,0),(1,0,0),(0,0,1),'object','_{0}{1}_upGuide'.format(side, part)]
    pm.delete(pm.aimConstraint(f4g, f2l, 
                               w = 1.0,
                               o = v[0],
                             aim = v[1],
                               u = v[2],
                             wut = v[3], 
                             wuo = v[4]))
    pm.delete(pm.pointConstraint(f3g, f3l, w=1, sk=['y']))
    pm.delete(pm.pointConstraint(f4g, f4l, w=1, sk=['y']))
    pm.delete(pm.pointConstraint(f3l, f3g, w=1))
    pm.delete(pm.pointConstraint(f4l, f4g, w=1))
    pm.delete(f2l)


def alignFootGuide():
    h  = '_L_hip_guide'
    k  = '_L_knee_guide'
    b  = '_L_ball_guide'
    t  = '_L_toe_guide'
    hl = pm.spaceLocator(n='_L_hip_alignLocator')
    bl = pm.spaceLocator(n='_L_ball_alignLocator')
    tl = pm.spaceLocator(n='_L_toe_alignLocator')
    pm.parent(bl, tl, hl)
    pm.delete(pm.parentConstraint(h, hl, mo=False))
    v = [(0,0,0),(0,-1,0),(0,0,-1),'object','_L_ankle_guide']
    pm.delete(pm.aimConstraint(k, hl,
                              sk = 'x',
                               w = 1.0,
                               o = v[0],
                             aim = v[1],
                               u = v[2],
                             wut = v[3], 
                             wuo = v[4]))
    pm.delete(pm.pointConstraint(b, bl, w=1, sk=['x']))
    pm.delete(pm.pointConstraint(t, tl, w=1, sk=['x']))
    pm.delete(pm.pointConstraint(bl, b, w=1))
    pm.delete(pm.pointConstraint(tl, t, w=1))
    pm.delete(hl)


# ------------------------------------------------------------------------------
# edit guide
# ------------------------------------------------------------------------------
def editHipTransGuide(val=[], htv=True):
    rtg = pm.PyNode('_root_guide')
    htg = pm.PyNode('_hipsTranslation_guide')
    pvg = pm.PyNode('_pelvis_guide')
    if htv == True:
        command.worldDisconnect(htg)
        htg.t.set(val[3][0], val[3][1], val[3][2])
        htg.setParent(rtg)
        pvg.setParent(htg)
    elif htv == False:
        pvg.setParent(rtg)
        htg.setParent('_guideHidden_GP')
        command.worldConnection(pvg, htg)
    pm.select(d=True)


def editSpineGuide(info={}, uiv=3):
    idList = ['008','023','024','025','026','027','028','029','030','031']
    gList  = [pm.PyNode('_{0}_guide'.format(info[i][1][0])) for i in idList]
    vList  = [info[i] for i in idList]
    pList  = [gList[0]]
    upg    = []
    # ---- for all spine guide
    for g in gList:
        ch = pm.listRelatives(g, c=True)
        if len(ch) > 1:
            upg = ch
        command.worldDisconnect(g)
    # ---- for 1 - uiv spine
    for g, v in zip(gList[1:uiv], vList[1:uiv]):
        command.extractHierarchy(g)
        pList.append(g)
        g.t.set(v[3][0], v[3][1], v[3][2])
    # ---- for uic - end spine
    for g in gList[uiv:]:
        command.extractHierarchy(g)
        g.setParent('_guideHidden_GP')
        command.worldConnection(gList[uiv-1], g)
    # ---- parent
    command.chainParent(pList[::-1])
    for i in upg:
        i.setParent(gList[uiv-1])
    pm.select(d=True)


def editNeckGuide(info={}, uiv=1):
    idList = ['020','032','033','034','035','036','037','038','039','040']
    gList  = [pm.PyNode('_{0}_guide'.format(info[i][1][0])) for i in idList]
    vList  = [info[i] for i in idList]
    pList  = [gList[0]]
    # ---- for all spine guide
    for g in gList:
        command.worldDisconnect(g)
    # ---- for 1 - uiv spine
    for g, v in zip(gList[1:uiv], vList[1:uiv]):
        command.extractHierarchy(g)
        pList.append(g)
        g.t.set(v[3][0], v[3][1], v[3][2])
    # ---- for uic - end spine
    for g in gList[uiv:]:
        command.extractHierarchy(g)
        g.setParent('_guideHidden_GP')
        command.worldConnection(gList[uiv-1], g)
    # ---- parent
    command.chainParent(pList[::-1])
    pm.parent('_head_guide', gList[uiv-1])
    pm.select(d=True)


def editClavicleGuide(info={}, uiv=1, side='L'):
    if side == 'L':
        idList = ['018','170']
    else:
        idList = ['019','171']
    gList = [pm.PyNode('_{0}_guide'.format(info[i][1][0])) for i in idList]
    vList = [info[i] for i in idList]
    pList = []
    # ---- end spine guide
    n0g = pm.PyNode('_neck0_guide')
    spg = n0g.getParent()
    shg = pm.PyNode('_{0}_shoulder_guide'.format(side))
    if uiv > 0:
        for g in gList:
            command.worldDisconnect(g)
        # ---- for 0 - uiv spine
        for g, v in zip(gList[0:uiv], vList[0:uiv]):
            command.extractHierarchy(g)
            pList.append(g)
            if side == 'L':
                g.t.set(v[3][0], v[3][1], v[3][2])
        # ---- for uic - end spine
        for g in gList[uiv:]:
            command.extractHierarchy(g)
            g.setParent('_guideHidden_GP')
            if side == 'L':
                command.worldConnection(gList[uiv-1], g)
        # ---- parent
        command.chainParent(pList[::-1])
        pList[0].setParent(spg)
        shg.setParent(gList[uiv-1])
    # ---- uiv == 0
    else:
        for g in gList:
            command.extractHierarchy(g)
            g.setParent('_guideHidden_GP')
            if side == 'L':
                command.worldConnection(spg, g)
        shg.setParent(spg)
    pm.select(d=True)


def editFingerBaseGuide(val=[], side='L', fbv=True):
    wtg = pm.PyNode('_{0}_wrist_guide'.format(side))
    fbg = pm.PyNode('_{0}_fingerBase_guide'.format(side))
    if fbv == True:
        command.worldDisconnect(fbg)
        fbg.t.set(val[3][0], val[3][1], val[3][2])
        ifgList = wtg.getChildren()
        if ifgList:
            for ifg in ifgList:
                ifg.setParent(fbg) 
        fbg.setParent(wtg)
    elif fbv == False:
        ifgList = fbg.getChildren()
        if ifgList:
            for ifg in ifgList:
                ifg.setParent(wtg)
        fbg.setParent('_guideHidden_GP')
        command.worldConnection(wtg, fbg)
    pm.select(d=True)


def editInHandGuide(val=[], side='L', finger='thumb', uiv=True):
    wtg = pm.PyNode('_{0}_wrist_guide'.format(side))
    fbg = pm.PyNode('_{0}_fingerBase_guide'.format(side))
    fgg = pm.PyNode('_{0}_{1}0_guide'.format(side, finger))
    chg = pm.PyNode('_{0}_{1}1_guide'.format(side, finger))
    # ---- parent
    if fbg in wtg.getChildren():
        pag = fbg
    else:
        pag = wtg
    # ---- child
    if chg in wtg.getChildren(ad=True):
        ch = True
    else:
        ch = False
    if uiv == True:
        command.worldDisconnect(fgg)
        fgg.t.set(val[3][0], val[3][1], val[3][2])
        fgg.setParent(pag)
        if ch:
            chg.setParent(fgg)
    elif uiv == False:
        if ch:
            chg.setParent(pag)
        fgg.setParent('_guideHidden_GP')
        command.worldConnection(pag, fgg)
    pm.select(d=True)


def editFinderGuide(info={}, idList=['050','051','052','053'], uiv=4):
    fgList = [pm.PyNode('_{0}_guide'.format(info[i][1][0])) for i in idList]
    if uiv > 0:
        for i, fg in enumerate(fgList[1:uiv:1]):
            val = info[idList[i]]
            command.worldDisconnect(fg)
            fg.t.set(val[3][0], val[3][1], val[3][2])
            fg.setParent(fgList[i-1])
    else:
        for i, fg in enumerate(fgList[uiv:]):
            fg.setParent('_guideHidden_GP')
            command.worldConnection(fg, fgList[uiv])
    pm.select(d=True)


def editToeBaseGuide(val=[], side='L', tbv=True):
    akg = pm.PyNode('_{0}_ankle_guide'.format(side))
    tbg = pm.PyNode('_{0}_ball_guide'.format(side))
    if tbv == True:
        command.worldDisconnect(tbg)
        tbg.t.set(val[3][0], val[3][1], val[3][2])
        ifgList = akg.getChildren()
        if ifgList:
            for ifg in ifgList:
                ifg.setParent(tbg) 
        tbg.setParent(akg)
    elif tbv == False:
        ifgList = tbg.getChildren()
        if ifgList:
            for ifg in ifgList:
                ifg.setParent(akg)
        tbg.setParent('_guideHidden_GP')
        command.worldConnection(akg, tbg)
    pm.select(d=True)


def editInFootGuide(val=[], side='L', finger='footThumb', uiv=True):
    akg = pm.PyNode('_{0}_ankle_guide'.format(side))
    tbg = pm.PyNode('_{0}_ball_guide'.format(side))
    fgg = pm.PyNode('_{0}_{1}0_guide'.format(side, finger))
    chg = pm.PyNode('_{0}_{1}1_guide'.format(side, finger))
    # ---- parent
    if tbg in akg.getChildren():
        pag = tbg
    else:
        pag = akg
    # ---- child
    if chg in akg.getChildren(ad=True):
        ch = True
    else:
        ch = False
    if uiv == True:
        command.worldDisconnect(fgg)
        fgg.t.set(val[3][0], val[3][1], val[3][2])
        fgg.setParent(pag)
        if ch:
            chg.setParent(fgg)
    elif uiv == False:
        if ch:
            chg.setParent(pag)
        fgg.setParent('_guideHidden_GP')
        command.worldConnection(pag, fgg)
    pm.select(d=True)


#def editFootFinderGuide():



'''
iftg = pm.PyNode('_L_footThumb0_guide')
ifig = pm.PyNode('_L_footIndex0_guide') 
ifmg = pm.PyNode('_L_footMiddle0_guide') 
ifrg = pm.PyNode('_L_footRing0_guide') 
ifpg = pm.PyNode('_L_footPinky0_guide') 
ifeg = pm.PyNode('_L_footExtra0_guide') 

iftg = pm.PyNode('_R_footThumb0_guide') 
ifig = pm.PyNode('_R_footIndex0_guide') 
ifmg = pm.PyNode('_R_footMiddle0_guide') 
ifrg = pm.PyNode('_R_footRing0_guide') 
ifpg = pm.PyNode('_R_footPinky0_guide') 
ifeg = pm.PyNode('_R_footExtra0_guide')
'''

def editRightToeBaseGUide(val=[], tbv=True):
    rtbg = pm.PyNode('_R_ball_guide')
    rakg = pm.PyNode('_R_ankle_guide')
    rchList = rtbg.getCChildren()
    if tbv == True:
        command.worldDisconnect(rtbg)




def editInhandRing(val=True):
    l  = pm.PyNode('_L_ring0_guide')
    r  = pm.PyNode('_R_ring0_guide')
    lp = pm.PyNode('_L_wrist_guide') 
    rp = pm.PyNode('_R_wrist_guide')
    lc = pm.PyNode('_L_ring1_guide')
    rc = pm.PyNode('_R_ring1_guide')

    for i, p, c in zip([l, r], [lp, rp], [lc, rc]):
        if val == True:
            i.setParent(p)
            if not c.getParent().name() == '_guideHidden_GP':
                c.setParent(i)
        elif val == False:
            c.setParent(p)
            i.setParent('_guideHidden_GP')


def editInhandPinky(val=True):
    l  = pm.PyNode('_L_pinky0_guide')
    r  = pm.PyNode('_R_pinky0_guide')
    lp = pm.PyNode('_L_wrist_guide') 
    rp = pm.PyNode('_R_wrist_guide')
    lc = pm.PyNode('_L_pinky1_guide')
    rc = pm.PyNode('_R_pinky1_guide')

    for i, p, c in zip([l, r], [lp, rp], [lc, rc]):
        if val == True:
            i.setParent(p)
            if not c.getParent().name() == '_guideHidden_GP':
                c.setParent(i)
        elif val == False:
            c.setParent(p)
            i.setParent('_guideHidden_GP')







'''
# ---- parent ------------------------------***************
def setGuideParent(k='', v=[]):
    p = None
    if v[3]:
        g = pm.PyNode('_{0}_guide'.format(k))
        p = pm.PyNode('_{0}_guide'.format(v[3]))
        g.setParent(p)
    return p


# ---- fit ------------------------------***************
def fitGuide(k='', v=[]):
    g = '_{0}_guide'.format(k)
    if pm.objExists(v[-1]):
        pos = pm.xform(v[-1], ws=True, t=True, q=True)
    else:
        pos = v[-2]
    pm.move(pos[0],pos[1],pos[2], g, a=True)
        


# ---- create guide ------------------------------***************
def createGuideFromUI(info={}):
    gList = []
    pList = []
    for k, v in info.items():
        if v[0]:
            g = createGuide(v[1][0])
            g.radius.set(v[2][3]*2)
            pm.move(v[3][0], v[3][1], v[3][2], g, a=True)
            gList.append(g)
            pList.append('_{0}_guide'.format(v[1][1]))

    # -- parenting
    for g, p in zip(gList, pList):
        if pm.objExists(p):
            g.setParent(p)
'''