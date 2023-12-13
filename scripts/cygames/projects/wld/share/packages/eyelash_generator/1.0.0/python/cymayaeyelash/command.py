import os
import re

import maya.cmds as cmds
import maya.mel as mel

import apiutils

def exe():
    if not cmds.pluginInfo('houdiniEngine', q=True, l=True):
        cmds.loadPlugin('houdiniEngine')
    toolopt = apiutils.ToolOpt('Eyelash_Generator')
    ch = toolopt.getvalue('history', True)

    mesh = cmds.ls(sl=True)[0]
    crv = cmds.ls(sl=True)[1]

    ha = cmds.createNode('houdiniAsset')
    cmds.setAttr(ha + '.syncWhenInputConnects', False)
    dir_ = re.sub('\\\\', '/', os.path.dirname(__file__))
    
    otlpath = dir_ + '/../../otls/eyelash_generator.hda'

    mcmd = 'setAttr -type "string" %s.otlFilePath "%s"' % (ha, otlpath)
    mel.eval(mcmd)
    mcmd = 'setAttr -type "string" %s.assetName "Sop/eyelash"' % ha
    mel.eval(mcmd)

    mcmd = 'houdiniEngine_setAssetInput %s.input[0].inputNodeId {"%s"}' % (ha, mesh)
    mel.eval(mcmd)
    mcmd = 'houdiniEngine_setAssetInput %s.input[1].inputNodeId {"%s"}' % (ha, crv)
    mel.eval(mcmd)
    mcmd = 'houdiniEngine_syncAsset %s' % ha
    mel.eval(mcmd)

    if not ch:
        delete_history(ha)

def delete_history(ha):
    meshs = cmds.listRelatives(ha, ad=True, type='mesh')
    cmds.delete(meshs, ch=True)
    cmds.parent(meshs, w=True)
    cmds.delete(ha)
    
    
    