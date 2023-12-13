# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pymel.core as pm
import maya.cmds as mc

import json

#-- json ---------------------------------------------------------------------------
def exportJson(path=r'', dict={}):
    f = open(path, 'w')
    json.dump(dict, f, indent=4)
    f.close()


def importJson(path=r''):
    f = open(path, 'r')
    tmp = f.read()
    res = json.loads(tmp)
    f.close()
    return res


def zipJson(keys=[], values=[]):
    res = {k:v for k, v in zip(keys, values)}
    return res
