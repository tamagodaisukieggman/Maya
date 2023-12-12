# -*- coding: utf-8 -*-
#=========================================================================== # noqa
# Cygames Tools # noqa
# importJSON.py # noqa
# # noqa
# Copyright 2017, Cygames Inc. # noqa
#=========================================================================== # noqa
import maya.cmds as mc
import maya.mel as mm
import json
import re


def importJSON(JPath, *args):  # noqa
    ns = mc.frameLayout('nameSpList', q=True, l=True)
    replaceSts = mc.checkBox('replaceGp', q=True, v=True)
    sts = mc.checkBox('revertPoseChk', q=True, v=True)
    tSts = mc.checkBox('lockPoseChkT', q=True, v=True)
    rSts = mc.checkBox('lockPoseChkR', q=True, v=True)
    revsel = mc.ls(sl=True)

    if mc.checkBox('tx_CB', q=True, ex=True):
        imtx = mc.checkBox('tx_CB', q=True, v=True)
    if mc.checkBox('ty_CB', q=True, ex=True):
        imty = mc.checkBox('ty_CB', q=True, v=True)
    if mc.checkBox('tz_CB', q=True, ex=True):
        imtz = mc.checkBox('tz_CB', q=True, v=True)
    if mc.checkBox('rx_CB', q=True, ex=True):
        imrx = mc.checkBox('rx_CB', q=True, v=True)
    if mc.checkBox('ry_CB', q=True, ex=True):
        imry = mc.checkBox('ry_CB', q=True, v=True)
    if mc.checkBox('rz_CB', q=True, ex=True):
        imrz = mc.checkBox('rz_CB', q=True, v=True)
    if mc.checkBox('sx_CB', q=True, ex=True):
        imsx = mc.checkBox('sx_CB', q=True, v=True)
    if mc.checkBox('sy_CB', q=True, ex=True):
        imsy = mc.checkBox('sy_CB', q=True, v=True)
    if mc.checkBox('sz_CB', q=True, ex=True):
        imsz = mc.checkBox('sz_CB', q=True, v=True)

    if mc.checkBox('tx_rCB', q=True, ex=True):
        rimtx = mc.checkBox('tx_rCB', q=True, v=True)
    if mc.checkBox('ty_rCB', q=True, ex=True):
        rimty = mc.checkBox('ty_rCB', q=True, v=True)
    if mc.checkBox('tz_rCB', q=True, ex=True):
        rimtz = mc.checkBox('tz_rCB', q=True, v=True)
    if mc.checkBox('rx_rCB', q=True, ex=True):
        rimrx = mc.checkBox('rx_rCB', q=True, v=True)
    if mc.checkBox('ry_rCB', q=True, ex=True):
        rimry = mc.checkBox('ry_rCB', q=True, v=True)
    if mc.checkBox('rz_rCB', q=True, ex=True):
        rimrz = mc.checkBox('rz_rCB', q=True, v=True)
    if mc.checkBox('sx_rCB', q=True, ex=True):
        rimsx = mc.checkBox('sx_rCB', q=True, v=True)
    if mc.checkBox('sy_rCB', q=True, ex=True):
        rimsy = mc.checkBox('sy_rCB', q=True, v=True)
    if mc.checkBox('sz_rCB', q=True, ex=True):
        rimsz = mc.checkBox('sz_rCB', q=True, v=True)

    try:
        transform = {'translateX': imtx, 'translateY': imty, 'translateZ': imtz, 'rotateX': imrx, 'rotateY': imry, 'rotateZ': imrz, 'scaleX': imsx, 'scaleY': imsy, 'scaleZ': imsz}
        retransform = {'translateX': rimtx, 'translateY': rimty, 'translateZ': rimtz, 'rotateX': rimrx, 'rotateY': rimry, 'rotateZ': rimrz}
        radioname = mc.radioCollection('RGOC', q=True, sl=True)
        option = {'adBtn': 'Add', 'sbBtn': 'Subtract', 'mtBtn': 'Multiply', 'dvBtn': 'Divide'}
        slideValue = mc.floatSliderGrp('fsg',  q=True, v=True)
    except:  # noqa
        transform = {'translateX': False, 'translateY': False, 'translateZ': False, 'rotateX': False, 'rotateY': False, 'rotateZ': False, 'scaleX': False, 'scaleY': False, 'scaleZ': False}

    getTValue = None
    getRValue = None
    nonExists = []
    nonExistsAttr = []
    attrList = []
    try:
        mc.textScrollList('changeAttrTsl', e=True, ra=True)
    except:  # noqa
        pass
    if tSts:
        getTValue = getT()
    if rSts:
        getRValue = getR()

    try:
        revSts = mc.checkBox('rev_CB', q=True, v=True)
        if revSts:
            getRevValue = createLocator()
            revSlideValue = mc.floatSliderGrp('revfsg',  q=True, v=True)
    except:  # noqa
        pass

    f = open(JPath, 'r')
    jsonData = json.load(f)
    key = jsonData['objects'].keys()
    atr = []
    for i in key:
        atr = jsonData['objects'][i]
        for j in atr:
            at = jsonData['objects'][i][j]
            n = len(at)  # noqa
            for k in at.keys():
                if re.match('.*lockInfluenceWeights.*', k):
                    continue
                else:
                    len(k)
                    p = jsonData['objects'][i][j][k]  # タイプと値
                    val = p['value']
                    a = i + '.' + k
                    if mc.objExists(i):
                        attrList.append(i)
                    try:
                        if transform[k] == True:  # noqa
                            opgetAttr = mc.getAttr(a)
                            if option[radioname] == 'Add':
                                val = opgetAttr + slideValue
                            elif option[radioname] == 'Subtract':
                                val = opgetAttr - slideValue
                            elif option[radioname] == 'Multiply':
                                val = opgetAttr * slideValue
                            elif option[radioname] == 'Divide':
                                val = opgetAttr / slideValue
                    except:  # noqa
                        pass
                    if ns is None:
                        cmds = ('setAttr ' '"' + a + '" ' + repr(val))  # noqa
                        node = i
                    elif replaceSts is False and ns is not None:
                        cmds = ('setAttr ' '"' + ns + ':' + a + '" ' + repr(val))  # noqa
                        node = '{}:{}'.format(ns, i)
                    elif replaceSts is True and ns is not None:
                        cmds = ('setAttr ' '"' + a.replace(a.split(':')[0], ns) + '" ' + repr(val))  # noqa
                        node = '{}'.format(i.replace(i.split(':')[0], ns))
                    if mc.objExists(node):
                        if mc.attributeQuery(k, node=node, exists=True):
                            mm.eval(cmds)
                        else:
                            nonExistsAttr.append(a)
                    else:
                        nonExists.append(node)
                        continue
    try:
        for ap in list(set(attrList)):
            mc.textScrollList('changeAttrTsl', e=True, append=[ap])
        svList = mc.textScrollList('changeAttrTsl', q=True, ai=True)
        mc.textFieldGrp('getImportObj', e=True, tx="{}".format(",".join(svList)))
        searchList()
    except:  # noqa
        pass
    try:
        revMain(getRevValue, revSlideValue, retransform, revsel)
    except:  # noqa
        pass

    if 0 < len(nonExists):  # noqa
        print u'以下のオブジェクトが存在しません。'  # noqa
        print u'--------------------------------------------------------'
        print '\n'.join(set(nonExists))
        print u'--------------------------------------------------------'
        print u'以上のオブジェクトが存在しません。'

    if 0 < len(nonExistsAttr):
        mc.textField('messagesTxt', e=True, text=u"存在しないアトリビュート '{}'".format("', '".join(nonExistsAttr)))
    else:
        mc.textField('messagesTxt', e=True, text='')
    if sts == True:  # noqa
        mirror()
    if getTValue:  # noqa
        setAttrLockValue(getTValue)
    if getRValue:  # noqa
        setAttrLockValue(getRValue)


def mirror(*args):
    ctrl = mc.ls(sl=True)
    for i in ctrl:  # noqa
        nams = i.split(':')
        if nams is None:  # noqa
            pass
        else:
            base_ctrl = nams[1].split(':')

        rx = mc.getAttr((i + '.rotateX'))
        ry = mc.getAttr((i + '.rotateY'))
        rz = mc.getAttr((i + '.rotateZ'))
        side = base_ctrl[0].split('_')
        if side[1] == 'L':
            ctrl = nams[0] + ':' + side[0] + '_R_' + side[2]
            if mc.objExists(ctrl) and side[0] != 'thumb':
                mc.setAttr((ctrl + '.rotateX'), rx * 1)
                mc.setAttr((ctrl + '.rotateY'), ry * -1)
                mc.setAttr((ctrl + '.rotateZ'), rz * -1)
            elif side[0] == 'thumb':
                mc.setAttr((ctrl + '.rotateX'), rx)
                mc.setAttr((ctrl + '.rotateY'), ry)
                mc.setAttr((ctrl + '.rotateZ'), rz)
        if side[1] == 'R':
            ctrl = nams[0] + ':' + side[0] + '_L_' + side[2]
            if mc.objExists(ctrl) and side[0] != 'thumb':
                mc.setAttr((ctrl + '.rotateX'), rx * 1)
                mc.setAttr((ctrl + '.rotateY'), ry * -1)
                mc.setAttr((ctrl + '.rotateZ'), rz * -1)
            elif side[0] == 'thumb':
                mc.setAttr((ctrl + '.rotateX'), rx)
                mc.setAttr((ctrl + '.rotateY'), ry)
                mc.setAttr((ctrl + '.rotateZ'), rz)


def getT():
    sel = mc.ls(sl=True)

    t = []
    t.append('translate')
    for obj in sel:
        if not mc.objectType(obj, isa='dagNode'):
            continue

        t.append(obj)
        tx = mc.getAttr('{}.translateX'.format(obj))
        t.append(tx)
        ty = mc.getAttr('{}.translateY'.format(obj))
        t.append(ty)
        tz = mc.getAttr('{}.translateZ'.format(obj))
        t.append(tz)

    return t


def getR():
    sel = mc.ls(sl=True)

    r = []
    r.append('rotate')
    for obj in sel:
        if not mc.objectType(obj, isa='dagNode'):
            continue

        r.append(obj)
        rx = mc.getAttr('{}.rotateX'.format(obj))
        r.append(rx)
        ry = mc.getAttr('{}.rotateY'.format(obj))
        r.append(ry)
        rz = mc.getAttr('{}.rotateZ'.format(obj))
        r.append(rz)

    return r


def setAttrLockValue(value):
    transform = value[0]
    ctrls = value[1::]  # noqa
    for i in range(len(ctrls) / 4):  # noqa
        if mc.getAttr('{}.{}X'.format(ctrls[4 * i], transform), lock=True) == False:  # noqa
            mc.setAttr('{}.{}X'.format(ctrls[4 * i], transform), ctrls[4 * i + 1])
        else:
            continue
        if mc.getAttr('{}.{}Y'.format(ctrls[4 * i], transform), lock=True) == False:  # noqa
            mc.setAttr('{}.{}Y'.format(ctrls[4 * i], transform), ctrls[4 * i + 2])
        else:
            continue
        if mc.getAttr('{}.{}Z'.format(ctrls[4 * i], transform), lock=True) == False:  # noqa
            mc.setAttr('{}.{}Z'.format(ctrls[4 * i], transform), ctrls[4 * i + 3])
        else:
            continue


def searchList(*args):
    fi = mc.textFieldGrp('getImportObj', q=True, tx=True)
    fis = fi.split(',')
    stext = mc.textFieldGrp('search', q=True, tx=True)
    # all = mc.textScrollList('changeAttrTsl', q=True, ai=True)
    mc.textScrollList('changeAttrTsl', e=True, ra=True)
    m = [s for s in fis if re.match(stext, s)]
    if m != []:
        m.sort()
        for name in m:
            mc.textScrollList('changeAttrTsl', e=True, a=name)
    elif m in fis:
        fis.sort()
        for name in fis:
            mc.textScrollList('changeAttrTsl', e=True, a=name)
    objectLength()


def createLocator(*args):
    sel = mc.ls(sl=True)
    locs = []
    if mc.objExists('pivotLocatorGp'):
        mc.delete('pivotLocatorGp')
    pivotLocatorGp = mc.group(em=True, n='pivotLocatorGp')
    for obj in sel:
        loc = mc.spaceLocator(n='pivotLocator_{}'.format(obj))
        mc.delete(mc.parentConstraint(obj, loc))
        locs.append(loc[0])
        mc.parent(loc, pivotLocatorGp)
    # mc.select(sel, r=True)
    return locs


def revMain(locs, revSlideValue, retransform, revsel):
    # sel = mc.ls(sl=True)
    for obj in revsel:
        for lo in locs:
            if obj == lo.split('pivotLocator_')[1]:
                wtA = mc.xform(obj, q=True, t=True, ws=True)
                wtArot = mc.xform(obj, q=True, ro=True)

                wtB = mc.xform(lo, q=True, t=True, ws=True)
                if retransform['translateX'] == True:  # noqa
                    wtA[0] = (wtB[0] - wtA[0]) * revSlideValue + wtB[0]
                if retransform['translateY'] == True:  # noqa
                    wtA[1] = (wtB[1] - wtA[1]) * revSlideValue + wtB[1]
                if retransform['translateZ'] == True:  # noqa
                    wtA[2] = (wtB[2] - wtA[2]) * revSlideValue + wtB[2]

                mc.xform(obj, t=[wtA[0], wtA[1], wtA[2]], ws=True)

                if retransform['rotateX'] == True:  # noqa
                    wtArot[0] = wtArot[0] * revSlideValue
                if retransform['rotateY'] == True:  # noqa
                    wtArot[1] = wtArot[1] * revSlideValue
                if retransform['rotateZ'] == True:  # noqa
                    wtArot[2] = wtArot[2] * revSlideValue

                mc.xform(obj, ro=[wtArot[0], wtArot[1], wtArot[2]])
    mc.select(revsel, r=True)
    if mc.objExists('pivotLocatorGp'):
        mc.delete('pivotLocatorGp')


def objectLength(*args):
    all = mc.textScrollList('changeAttrTsl', q=True, ai=True)
    mc.text("objectsTxt", e=True, l=u"オブジェクト数:{}".format(len(all)))
