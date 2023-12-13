# -*- coding: utf-8 -*-
# ---- import modules
import pymel.core as pm
import maya.cmds as mc

__label__    = 'Vertex Color'
__info__     = 'Check Vertex Color in current scene.' 
__label_jp__ = u'頂点カラー'
__info_jp__  = u'不要な頂点カラーを削除します。' 


def check():
    '''
check vertex color

Parameters:
  - : 

Returns:
  - str: mesh node has vertex color 

Error:
  - :
    '''
    log = ''
    for mesh in pm.ls(typ='mesh'):
        csList = pm.polyColorSet(mesh, acs=True, q=True)
        if csList:
            log += 'vertex color : {0} \n'.format(mesh.name())
    #print  resList
    return log


def execute():
    '''
check Animation Keys

Parameters:
  - : 

Returns:
  - str: animation key 

Error:
  - :
    '''
    log = ''
    for mesh in pm.ls(typ='mesh'):
        csList = pm.polyColorSet(mesh, acs=True, q=True)
        if csList:
            for cs in csList:
                pm.polyColorSet(mesh, cs=cs, d=True)
                log += 'delete color set: {0}'.format(mesh.name()) 
    #print  log
    return log
