# -*- coding: utf-8 -*-
# ---- import modules
import pymel.core as pm
import maya.cmds as mc

__label__    = 'Joint Color'
__info__     = 'Turn off use object color of binded joints' 
__label_jp__ = u'ジョイント カラー'
__info_jp__  = u'ジョイントのUse Object ColorをOFFにします。' 


def check():
    '''
check joint color

Parameters:
  - : 

Returns:
  - list: joint list using object color 

Error:
  - :
    '''
    log = ''
    for jt in pm.ls(typ='joint'):
        if jt.uoc.get():
            log += 'joint color : {0} \n'.format(jt.name())
    #print  resList
    return log


def execute():
    '''
turn off joint color

Parameters:
  - : 

Returns:
  - str: joint list 

Error:
  - :
    '''
    log = ''
    for jt in pm.ls(typ='joint'):
        if jt.uoc.get():
            jt.uoc.set(0)
            log += 'use object color off : {0} \n'.format(jt.name())
    #print  resStr
    return log
