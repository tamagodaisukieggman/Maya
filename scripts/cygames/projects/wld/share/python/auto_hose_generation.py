import pymel.core as pm

import maya.mel as mel



def run():    

    if not pm.pluginInfo('houdiniEngine', query=True, loaded=True ):

        pm.loadPlugin('houdiniEngine')



    nodes = pm.ls(selection=True)



    hda = pm.createNode('houdiniAsset')

    hda.assetName.set('Sop/world_auto_hose')

    hda.otlFilePath.set(r'W:\production\tools\projects\world\inhouse\win\extension\houdini\share\otls\world_auto_hose.hda')



    obj1 = nodes[0]

    obj2 = nodes[1]



    cmd = 'houdiniEngine_setAssetInput %s.input[0].inputNodeId {"%s"}' % (hda, obj1)

    mel.eval(cmd)

    cmd = 'houdiniEngine_setAssetInput %s.input[1].inputNodeId {"%s"}' % (hda, obj2)

    mel.eval(cmd)

    

    pm.connectAttr('time1.outTime', '{}.inTime'.format(hda))



    cmd = 'houdiniEngine_syncAsset {}'.format(hda)

    mel.eval(cmd)



    







