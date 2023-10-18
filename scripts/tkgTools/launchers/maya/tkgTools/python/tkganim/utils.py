# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import pymel.core as pm

import importlib
from imp import reload
import math
import os
import pprint
import sys
import traceback

import tkgfile.window as tkgfilewin
import tkgfile.utils as tkgfileutls

reload(tkgfilewin)
reload(tkgfileutls)

tfw=tkgfilewin.TkgDialogs()
tfu=tkgfileutls.TkgUtils()

if cmds.pluginInfo('fbxmaya', q=True, l=True) == False:
    cmds.loadPlugin("fbxmaya")

class TkgUtils(object):
    def __init__(self):
        pass

    def export_fbx(self):
        save_path=tfw.fileDialog2_dir()
        fname=tfu.get_currentSceneInfo()[2] or None
        if not fname:
            fname='NewScene'
        sel=cmds.ls(os=1)
        if sel:
            root_jnt=sel[0]
        else:
            cmds.warning(u'rootジョイントを選択してください。')
            return
        try:
            cmds.parent(root_jnt, w=1)
        except:
            pass
        cmds.select(root_jnt)
        cmds.bakeResults([root_jnt],
                         sparseAnimCurveBake=False,
                         minimizeRotation=False,
                         removeBakedAttributeFromLayer=False,
                         hierarchy='below',
                         removeBakedAnimFromLayer=False,
                         oversamplingRate=1,
                         bakeOnOverrideLayer=False,
                         preserveOutsideKeys=True,
                         simulation=True,
                         sampleBy=1,
                         shape=False,
                         t=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
                         disableImplicitControl=True,
                         controlPoints=False)

        connections=cmds.listConnections(s=1, type='displayLayer') or None
        if connections:
            [cmds.delete(obj) for obj in connections]

        mel.eval('FBXExportInAscii -v true;FBXExport -f "{0}/{1}.fbx" -s;'.format(save_path, fname))

        print('Saved:{0}/{1}.fbx'.format(save_path, fname))

    def correctkeys(self, objects=None):
        if not objects:
            objects=cmds.ls(os=1)

        [self.quaternionToEuler(obj=obj) for obj in objects]

    def quaternionToEuler(self, obj=None):
        rot = cmds.xform(obj, q=1, ro=1, os=1)
        rotOrder = cmds.getAttr('{}.rotateOrder'.format(obj))
        euler = om2.MEulerRotation(math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]), rotOrder)
        quat = euler.asQuaternion()
        euler = quat.asEulerRotation()
        r = euler.reorder(rotOrder)

        cmds.xform(obj, ro=[math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)], os=1, a=1)

        cmds.setKeyframe(obj, at='rotate')

        return math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)

    def bake(self, playbackSlider=None, correctAnimKeys=None):
        u"""フレーム毎にベイク"""
        #check and save current autokey state
        cur_time=cmds.currentTime(q=1)
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = 1
        else:
            autoKeyState = 0

        cmds.autoKeyframe(st=0)

        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

        start = playmin
        end = playmax-1

        if playbackSlider:
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            if gPlayBackSlider:
                if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
                    frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
                    start = frameRange[0]
                    end = frameRange[1]-1
                else:
                    frameRange = cmds.currentTime(q=1)
                    start = frameRange
                    end = frameRange-1

        for i in range (int(start-1), int(end+2)):
            cmds.currentTime(i, e=True)
            if correctAnimKeys:
                self.correctkeys()
        cmds.currentTime(cur_time)
        cmds.autoKeyframe(state=autoKeyState)


    def remove_nss(self, obj):
        nss = ':'.join(obj.split(':')[:-1:])
        if not ':' in nss:
            nss = nss + ':'
            replace_char = []
            replace_char.append(nss)
            replace_char.append('')

        return obj.replace(replace_char[0], replace_char[1])


    def copy_anim(self):
        objects = cmds.ls(os=1)

        if objects:
            for obj in objects:
                animCrvs = cmds.listConnections(obj, t='animCurve', scn=1)

                if animCrvs:
                    for ac in animCrvs:
                        plugs = cmds.listConnections(ac, d=1, p=1)
                        dup_ac = cmds.duplicate(ac)

                        if plugs:
                            for plg in plugs:
                                ac_out = cmds.listConnections(plg, d=1, p=1)

                                dst_repl_out = self.remove_nss(ac_out[0])
                                dst_repl_in = self.remove_nss(plg)

                                cmds.connectAttr(dst_repl_out, dst_repl_in, f=1)
                                print(dst_repl_out, dst_repl_in)

                else:
                    print('animCurves are not exist')

        else:
            print('selected objects are not exist')
