# -*- coding: utf-8 -*-
u"""メニュー「ttsubasa(Artist)」を追加"""

import sys
import inspect

import maya.cmds as cmds
import maya.mel as mel

from functools import partial

class TsubasaDccUserMenu(object):

    menu_name = 'tsubasa_artist'
    menu_title = 'tsubasa(Artist)'

    @classmethod
    def _add_items(cls):
        u"""メニューアイテムの追加"""
        # --------------------------------------------------
        # この下にメニューを追加する
        # cmds.menuItem(l=u'label', c='command')
        #
        #
        #
        # ここまで --------------------------------------------------
        cmds.menuItem(l=u'General', sm=True)
        cmds.menuItem(l=u'Asset Finder', 
                      c='import assetFinder.ui; assetFinder.ui.showUI()')
        cmds.menuItem(l=u'Node Finder', i='hotkeyFieldSearch.png',
                      c='from nodeFinder import nodeFinder; nodeFinder.main()')
        cmds.menuItem(l=u'Node Selecter',
                      c='from nodeSelecter import nodeSelecter; nodeSelecter.main()')
        cmds.menuItem(l=u'Attr Watcher',
                      c='from attrWatcher import attrWatcher; attrWatcher.main()')
        cmds.menuItem(l=u'Window Manager',
                      c='from windowManage import windowManage; windowManage.main()')
        cmds.setParent('..', m=True)

        cmds.menuItem(l=u'Animation', sm=True)
        cmds.menuItem(l=u'Animation Checker',
                      c='from animationChecker import animationChecker; animationChecker.main()')
        cmds.menuItem(l=u'Facial Support', 
                      c='import fcSupport.ui; fcSupport.ui.showUI()')
        cmds.menuItem(l=u'Simulation Blend Rate Tool', 
                      c='import sbrTool.ui; sbrTool.ui.showUI()')
        cmds.setParent('..', m=True)

        cmds.menuItem(l=u'Rigging', sm=True)
        cmds.menuItem(l=u'Base Body Guide',
                      i='p-add.png', 
                      c='import baseBodyGuide.ui; baseBodyGuide.ui.showUI()')
        cmds.menuItem(l=u'ADN Assistant',
                      i='pi-add.png', 
                      c='import adnAssistant.ui; adnAssistant.ui.showUI()')
        cmds.menuItem(l=u'ADN Set Val Assistant',
                      c='from adnSetValAssistant import adnSetValAssistant; adnSetValAssistant.main()')
        cmds.menuItem(l=u'Multi Connection',
                      i='out_bifrostCompound.png', 
                      c='import multiConnection.ui; multiConnection.ui.showUI()')
        cmds.menuItem(d=True)
        cmds.menuItem(l=u'Facial Guide',
                      i='QR_show.png', 
                      c='import facialGuide.ui;facialGuide.ui.showUI()')
        cmds.menuItem(l=u'Palette', 
                      i='setEdEditMode.png',
                      c='import palette.ui;palette.ui.showUI()')
        cmds.menuItem(l=u'Smear Support', 
                      i='modifyBend.png',
                      c='import smearSupport.ui;smearSupport.ui.showUI()')
        cmds.menuItem(l=u'Rig Support Other', 
                      c='from rigSupportToolsOther import ui; ui.main()')
        cmds.menuItem(l=u'Update Model Tool', 
                      c='from updateModelTool import updateModelToolUi; updateModelToolUi.main()')
        cmds.menuItem(l=u'NPC Tools', 
                      c='from rigSupportToolsOther import npcTools; npcTools.initUi()')
        cmds.menuItem(l=u'Convert Texture ForMB', 
                      i='imageDisplay.png',
                      c='from convertTex2jpgForMB import convertTex2jpgForMB; convertTex2jpgForMB.main()')
        cmds.menuItem(l=u'Save Manage RigScene', i='saveToShelf.png',
                      c='from saveManageRigScene import saveManageRigScene; saveManageRigScene.main()')
        cmds.menuItem(d=True)
        cmds.menuItem(l=u'Select Primary Joints', i='HIKCharacterToolStancePose.png',
                      c='from dccUserMayaSharePythonLib import tsubasa_dumspl; tsubasa_dumspl.selPrimaryJoints()')
        cmds.menuItem(l=u'Select Joints Without ADN', i='HIKCharacterToolStancePose.png',
                      c='from dccUserMayaSharePythonLib import tsubasa_dumspl; tsubasa_dumspl.selJointsExceptADN()')
        cmds.menuItem(d=True)
        cmds.menuItem(l=u'Joint Tools', 
                      i='joint.open.svg',
                      c='from jointTools import tsubasaJointTools; tsubasaJointTools.main()')
        cmds.menuItem(l=u'Joint Colour',
                      i='joint.open.svg',
                      c='from jointColour import jointColour; jointColour.ui()')
        cmds.menuItem(l=u'Curve Controller',
                      c='from curveController import curveController; curveController.main()')	  
        cmds.menuItem(l=u'Tail Ctrl Creator Maya Ver', 
                      i='ikSplineSolver.svg',
                      c='from tailCtrlCreatorMayaVer import tailCtrlCreatorMayaVer; tailCtrlCreatorMayaVer.main()')
        cmds.menuItem(l=u'Set Editor', 
                      c='import setEditor.ui; setEditor.ui.showUI()')
        cmds.menuItem(l=u'Copy JointLabel', 
                      c='from copyJointLabel import tsubasa_jointlabel_copy; tsubasa_jointlabel_copy.main()')
        cmds.menuItem(l=u'Reconnect Joint', 
                      c='from reconnectJoint import ui; ui.main()')
        cmds.menuItem(l=u'Drawing Override Editor',
                      c='import drawingOverrideEditor.ui; drawingOverrideEditor.ui.showUI()')
        cmds.menuItem(l=u'Duplicate Polygon With Weight',
                      c='from duplicatePolygonWithWeight import duplicatePolygonWithWeight; duplicatePolygonWithWeight.main()')
        cmds.menuItem(l=u'Bind and Copy Weight', i='rigidBind.png',
                      c='from bindAndCopyWeight import bindAndCopyWeight; bindAndCopyWeight.main()')
        cmds.menuItem(l=u'Skin Weights Simple', i='skinWeightCopy.png',
                      c='from skinWeightSimple import skinWeightSimple; skinWeightSimple.main()')
        cmds.menuItem(l=u'Various Copy Paste', 
                      c='from variousCopyPaste import variousCopyPaste; variousCopyPaste.main()')
        cmds.menuItem(l=u'Weight Copy to Vtx', 
                      c='from weightCopyToVtx import weightCopyToVtx; weightCopyToVtx.main()')
        cmds.menuItem(l=u'Weight Gradation', 
                      c='from weightGradation import weightGradation; weightGradation.main()')
        cmds.menuItem(d=True)
        cmds.menuItem(l=u'Const Viewer',
                      c='from constViewer import constViewer; constViewer.main()')
        cmds.menuItem(l=u'Icon Viewer', 
                      c='import iconViewer.ui; iconViewer.ui.showUI()')
        cmds.menuItem(l=u'LOD Viewer', 
                      c='from lodViewer import lodViewer; lodViewer.main()')
        cmds.setParent('..', m=True)

        cmds.menuItem(l=u'Houdini Engine', sm=True)
        cmds.menuItem(l=u'HDA List <ENV>',
                      c='import houdini_engine.hda_list.env.ui; houdini_engine.hda_list.env.ui.showUI()')
        cmds.menuItem(l=u'HDA List <VFX>',
                      c='import houdini_engine.hda_list.vfx.ui; houdini_engine.hda_list.vfx.ui.showUI()')
        cmds.menuItem(l=u'Shutter Tool',
                      c='import houdini_engine.shutter_tool.shutter_tool; houdini_engine.shutter_tool.shutter_tool.showUI()')
        cmds.menuItem(l=u'Ivy Tool',
                      c='import houdini_engine.ivy_tool.ivy_tool; houdini_engine.ivy_tool.ivy_tool.showUI()')
        cmds.menuItem(l=u'Pivot Painter',
                      c='import houdini_engine.pivot_painter.pivot_painter; houdini_engine.pivot_painter.pivot_painter.showUI()')
        cmds.menuItem(l=u'Houdini Reduction',
                      c='import houdini_engine.houdini_reduction.houdini_reduction; houdini_engine.houdini_reduction.houdini_reduction.showUI()')
        cmds.menuItem(l=u'Simple Collision',
                      c='import houdini_engine.simple_collision.simple_collision; houdini_engine.simple_collision.simple_collision.showUI()')
        cmds.menuItem(l=u'__ freeze all HDA in this scene __',
                      c='import houdini_engine.freeze_all; houdini_engine.freeze_all.freeze_all()')
        cmds.setParent('..', m=True)

        cmds.menuItem(l=u'DigitalFrontier', sm=True)
        cmds.menuItem(l=u'tsubasaFaceContSelector ', 
                      c='import tsubasaFaceContSelector.ui.main;tsubasaFaceContSelector.ui.main.maya()')
        cmds.setParent('..', m=True)

    @classmethod
    def main(cls):
        u"""メニュー「tsubasa(Artist)」を追加"""
        # この関数は編集禁止        
        g_main_window = mel.eval('$temp=$gMainWindow')

        if cmds.menu(cls.menu_name, q=True, ex=True):
            cls.menu = cmds.menu(cls.menu_name, e=True, dai=True, to=True)
        else:
            cls.menu = cmds.menu(cls.menu_name, l=cls.menu_title, p=g_main_window, to=True)

        cls._add_items()

        cmds.setParent('..', menu=True)
        cmds.menuItem(d=True)
        cmds.setParent('..')
        cmds.setParent(cls.menu_name, menu=True)
