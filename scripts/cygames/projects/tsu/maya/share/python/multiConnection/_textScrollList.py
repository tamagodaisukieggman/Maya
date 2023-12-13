# -*- coding: utf-8 -*-
from __future__ import absolute_import


#-- import modules
import pymel.core as pm
import maya.cmds as mc



def clear(tsl):
    pm.textScrollList(tsl, ra=True, e=True)


def moveUp(tsl):
    ali = pm.textScrollList(tsl, ai=True, q=True)
    sli = pm.textScrollList(tsl, sii=True, q=True)

    if sli:
        for i in sli:
            if i > 1:
                si = i-1
                src = ali[si]   #-- source
                pm.textScrollList(tsl, ap=(i-1, src), rii=i, sii=i-1, e=True)


def moveDown(tsl):
    ali = pm.textScrollList(tsl, ai=True, q=True)
    sli = pm.textScrollList(tsl, sii=True, q=True)

    if sli:
        for i in sli[::-1]:
            if i < len(ali):
                si = i-1
                src = ali[si]   #-- source
                pm.textScrollList(tsl, ap=(i+1, src), rii=i, sii=i+1, e=True)


def add(tsl, obj):
    ali = pm.textScrollList(tsl, ai=True, q=True)
    adl = [i for i in obj if not i in ali]
    pm.textScrollList(tsl, a=adl, e=True)


def remove(tsl):
    tgt = [int(i) for i in pm.textScrollList(tsl, sii=True, q=True)]
    tgt.reverse()
    print(tgt)
    pm.textScrollList(tsl, rii=tgt, da=True, e=True)


def sort(tsl):
    obj = pm.textScrollList(tsl, ai=True, q=True)
    obj.sort()
    pm.textScrollList(tsl, ra=True, e=True)
    pm.textScrollList(tsl, a=obj, e=True)


def reverse(tsl):
    obj = pm.textScrollList(tsl, ai=True, q=True)
    obj.reverse()
    pm.textScrollList(tsl, ra=True, e=True)
    pm.textScrollList(tsl, a=obj, e=True)


def reset(tsl, obj):
    pm.textScrollList(tsl, ra=True, e=True)
    pm.textScrollList(tsl, a=obj, e=True)


def count(tsl):
    return len(pm.textScrollList(tsl, ai=True, q=True))


def addPrefix(tsl, pre):
    tgt = ['{0}{1}'.format(pre, i) for i in pm.textScrollList(tsl, ai=True, q=True)]
    pm.textScrollList(tsl, ra=True, e=True)
    pm.textScrollList(tsl, a=tgt, e=True)


def addSuffix(tsl, suf):
    tgt = ['{0}{1}'.format(i, suf) for i in pm.textScrollList(tsl, ai=True, q=True)]
    pm.textScrollList(tsl, ra=True, e=True)
    pm.textScrollList(tsl, a=tgt, e=True)


def replaceText(tsl, s, t):
    tgt = [i.replace(s, t) for i in pm.textScrollList(tsl, ai=True, q=True)]
    pm.textScrollList(tsl, ra=True, e=True)
    pm.textScrollList(tsl, a=tgt, e=True)


def select(tsl):
    sel = pm.textScrollList(tsl, si=True, q=True)
    res = []
    for i in sel:
        if pm.objExists(i):
            res.append(i)
    if res:
        pm.select(res, r=True)
        print(res)












