# -*- coding: utf-8 -*-

# ---------------------------------------------
# ======= author : honda_satoshi
#                  yoshida_yutaka
# ---------------------------------------------

import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mm

from functools import partial

from . import myUtilities as utils

class MyUtilitiesGUI():
    def __init__(self):
        self.sel = []


    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------
    # yoshida -------------------------------------------------------------------------------------

    def _selectHierarchyByType_ui(self):
        mu = utils.MyUtilities()

        if cmds.window('selectHierarchyByTypeUI', ex=1):
            cmds.deleteUI('selectHierarchyByTypeUI')

        window = cmds.window('selectHierarchyByTypeUI', t='SHBT', s=0, tlc=[200, 200], wh=(240, 190))
        cmds.columnLayout()
        cmds.text(l='Select Hierarchy by Type', fn='boldLabelFont', w=240, h=30, bgc=(0.5, 0, 0.5))

        cmds.gridLayout(nc=3, cwh=(80, 40))
        cmds.button(l='Polygon', c=partial(mu._selectHierarchyByType, typ="mesh"))
        cmds.button(l='nurbsSurface', c=partial(mu._selectHierarchyByType, typ="nurbsSurface"))
        cmds.button(l='nurbsCurve', c=partial(mu._selectHierarchyByType, typ="nurbsCurve"))

        cmds.button(l='nucleus', c=partial(mu._selectHierarchyByType, typ="nucleus"))
        cmds.button(l='nCloth', c=partial(mu._selectHierarchyByType, typ="nCloth"))
        cmds.button(l='nRigid', c=partial(mu._selectHierarchyByType, typ="nRigid"))

        cmds.button(l='Locator', c=partial(mu._selectHierarchyByType, typ="locator"))
        cmds.button(l='Joint', c=partial(mu._selectHierarchyByType, typ="joint"))
        cmds.button(l='Camera', c=partial(mu._selectHierarchyByType, typ="camera"))

        cmds.button(l='Group', c=partial(mu._selectHierarchyByType, typ="transform"))
        cmds.button(l='Light', c=partial(mu._selectHierarchyByType, typ="light"))

        cmds.showWindow(window)


    def _selectCVs_ui(self):
        mu = utils.MyUtilities()

        if cmds.window('selectCVsUI', ex=1):
            cmds.deleteUI('selectCVsUI')

        window = cmds.window('selectCVsUI', t='selCVs', s=0, tlc=[200, 200], wh=(300, 30))
        cmds.columnLayout()
        cmds.rowLayout(nc=3)
        cmds.textFieldButtonGrp('cvNumberButton', l='CV Number', tx='2',
            bl='Set', cw3=[100,50,80], bc=mu._selectCVsNum)
        cmds.button(l='First', w=50, c=partial(mu._selectCVs, num=0))
        cmds.button(l='Last', w=50, c=partial(mu._selectCVs, num=1))
        cmds.showWindow(window)
