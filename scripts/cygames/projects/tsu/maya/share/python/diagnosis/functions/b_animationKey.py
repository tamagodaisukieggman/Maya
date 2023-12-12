# -*- coding: utf-8 -*-
# ---- import modules
import pymel.core as pm
import maya.cmds as mc

__label__    = 'Animation Keys'
__info__     = 'Check Animation Keys in current scene.' 
__label_jp__ = u'アニメーション キー'
__info_jp__  = u'シーン内の不要なアニメーションを削除します。' 

def check():
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
    animList = pm.ls(typ=['animCurveTA', 'animCurveTL', 'animCurveTU'])
    #print  animList
    for i in animList:
    	log += 'animation key : {0} \n'.format(i.name())
    return log



def execute():
    '''
delete Animation Keys

Parameters:
  - : 

Returns:
  - list: joint list using object color 

Error:
  - :
    '''
    log = ''
    animList = pm.ls(typ=['animCurveTA', 'animCurveTL', 'animCurveTU'])
    pm.delete(animList)
    #print  'animation keys were deleted.'
    for i in animList:
    	log += 'delete animation key : {0} \n'.format(i.name())
    return log
