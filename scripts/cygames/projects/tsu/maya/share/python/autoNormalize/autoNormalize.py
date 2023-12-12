# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : autoNormalize
# Author  : toi
# Version : 0.0.3
# Update  : 2022/4/18
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import pymel.core as pm
import os
from collections import OrderedDict
import tsubasa.maya.tools.skinweighteditor.gui
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
from dccUserMayaSharePythonLib import common as cm
#from dccUserMayaSharePythonLib import pyCommon as pcm
from dccUserMayaSharePythonLib import ui


def autoNormalize(prune_=0.010, round_=3, max_influence_=4):
    tsubasa.maya.tools.skinweighteditor.gui.main()
    swe = ui.getPySideWindow('Skin Weight Editor')
    swe.hide()

    '''
    #スクリプトジョブを停止
    try:
        swe_sb = 0
        swe_sb = [x for x in cmds.scriptJob(listJobs=True) if 'SkinWeightEditor' in x]
        swe_sb = swe_sb[0].split(':')[0]
        if swe_sb:
            cmds.scriptJob(k=int(swe_sb))
    except:
        pass
    '''

    les = swe.findChildren(QLineEdit)
    les[7].setText(str(round_))
    les[8].setText(str(prune_))
    les[9].setText(str(max_influence_))
    pbs = swe.findChildren(QPushButton)
    #for pb in pbs:
    #    if pb.text() == 'Prune':
    #        cm.hum('Prune.....')
    #        pb.click()
    for pb in pbs:
        if pb.text() == 'Round':
            cm.hum('Round.....')
            pb.click()
    for pb in pbs:
        if pb.text() == 'Max Influence':
            cm.hum('Max Influence.....')
            pb.click()

    #swe.close()


def main(prune_=0.010, round_=3, max_influence_=4):
    cm.hum('Start normalize')
    sel = pm.ls(sl=True)
    if sel:
        nodes = pm.ls(sel[0], dag=True)
        #result = []
        #for node in nodes:
        #    try:
        #        if node.getShape():
        #            result.append(node)
        #    except:
        #        pass
        #pm.select(result)

        sel = pm.ls(sl=True)
        if sel:
            autoNormalize(prune_, round_, max_influence_)
            cm.hum('Finish !')
