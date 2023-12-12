import maya.cmds as cmds
import maya.mel as mel

def freeze_all():
    list_hda = cmds.ls(type='houdiniAsset')
    cmds.select(list_hda)
    mel.eval('houdiniEngine_freezeSelectedAssets;')