# -*- coding: utf-8 -*-
from __future__ import absolute_import

#----- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import json

from . import core as mrc

import importlib
importlib.reload(mrc)

class mirrorUI(object):
    def __init__(self):
        self.__ver__     = '0.0.1'
        self.windowName  = 'mirror'
        self.windowTitle = 'Mirror v{0}'.format(self.__ver__)
        self.windowSize  = [300, 200]
        self._maya_url   = r'https://help.autodesk.com/view/MAYAUL/2023/JPN/'
        self._help_url   = r'https://wisdom.cygames.jp/display/shenron/Rig%3A+Tools%3A+Maya%3A+Mirror'
        #--- current script path -----------------------------------------------
        self.__dir = os.path.dirname(os.path.abspath(__file__))
        #-- image path ---------------------------------------------------------
        self._icon = fr'{self.__dir}/_data/_icon'
        #-- color --------------------------------------------------------------
        self.btnBgc = (0.37, 0.37, 0.37)
        #-- initial variables --------------------------------------------------


    #-- initial funsionts ------------------------------------------------------
    def checkWindowOverlap(self):
        if pm.window(self.windowName, ex=True):
            pm.deleteUI(self.windowName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._maya_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._help_url)


    #--- functions -------------------------------------------------------------
    def runMirror(self, typ=1, *args):
        objs = pm.selected()
        size = len(objs)

        if size >= 2: #-- run mirror
            src = objs[:int(size/2)]
            tgt = objs[int(size/2):]

            for s, t in zip(src, tgt):
                if typ ==   1: #-- basic
                    mrc.setMirror(s, t)
                elif typ == 2: #-- behavior
                    mrc.setBehavior(s, t)
                elif typ == 3: #-- swing
                    mrc.setSwing(s, t)

        else: #-- warning
            pm.warning('Please select more than 2 objects.')


    def runDuplicateMirror(self, typ=1, *args):
        s = pm.textField(self.tfDpL, tx=True, q=True)
        t = pm.textField(self.tfDpR, tx=True, q=True)
        v = pm.checkBox(self.cbJsd, v=True, q=True)

        if typ ==   1: #-- basic
            mrc.duplicateMirror(s, t, v)
        elif typ == 2: #-- behavior
            mrc.duplicateBehavior(s, t, v)
        elif typ == 3: #-- swing
            mrc.duplicateSwing(s, t, v)


    #--- edit UI ---------------------------------------------------------------
    def switchType(self, *args):
        t = pm.radioButtonGrp(self.rbTyp, sl=True, q=True)
        if t == 1: #-- Basic
            pm.iconTextButton(self.ibMir, l='Mirror Selected ( Basic )',
                c=pm.Callback(self.runMirror, typ=1), e=True)

            pm.iconTextButton(self.ibDpl, l='Mirror Duplicate ( Basic )',
                c=pm.Callback(self.runDuplicateMirror, typ=1), e=True)

        elif t == 2: #-- Behavior
            pm.iconTextButton(self.ibMir, l='Mirror Selected ( Behavior )',
                c=pm.Callback(self.runMirror, typ=2), e=True)

            pm.iconTextButton(self.ibDpl, l='Mirror Duplicate ( Behavior )',
                c=pm.Callback(self.runDuplicateMirror, typ=2), e=True)

        elif t == 3: #-- Swing
            pm.iconTextButton(self.ibMir, l='Mirror Selected ( Swing )',
                c=pm.Callback(self.runMirror, typ=3), e=True)

            pm.iconTextButton(self.ibDpl, l='Mirror Duplicate ( Swing )',
                c=pm.Callback(self.runDuplicateMirror, typ=3), e=True)


    #--- main UI ---------------------------------------------------------------
    def main(self):
        self.checkWindowOverlap()
        window = pm.window(self.windowName, mb = True,
                           t = self.windowTitle,
                           w = self.windowSize[0],
                           h = self.windowSize[1])

        #-- menu ---------------------------------------------------------------
        pm.menu(l='Help', hm=True)
        pm.menuItem(l='Maya HELP', c=self.show_mayaHelp)
        pm.menuItem(d=True)
        pm.menuItem(l='Tool HELP', c=self.show_toolHelp)


        #-- layout -------------------------------------------------------------
        #-- Pane Layout
        self._fmL = pm.formLayout(nd=100, h=200)
        self._sep = pm.separator()

        self.rbTyp = pm.radioButtonGrp(l='Type :   ', 
                     la3=['Basic', 'Behavior', 'Swing'], nrb=3)

        self.ibMir = pm.iconTextButton(l='Mirror Selected ( Basic )')
        self._spMr = pm.separator(st='in')
        self.tfDpL = pm.textField(tx='L_')
        self.tfDpR = pm.textField(tx='R_')
        self.cbJsd = pm.checkBox(l='Joint Side')
        self.ibDpl = pm.iconTextButton(l='Mirror Duplicate ( Basic )')
        self._spDp = pm.separator(st='in')

        #-----------------------------------------------------------------------
        #--- Edit UI elements --------------------------------------------------
        io,  to, = ['iconOnly', 'textOnly']
        ith, itv = ['iconAndTextHorizontal', 'iconAndTextVertical']

        pm.radioButtonGrp(self.rbTyp, cw4=(50, 60, 80, 80), sl=1, 
            cc=pm.Callback(self.switchType), e=True)

        pm.iconTextButton(self.ibMir, st=ith, w=140, h=26, mw=7, mh=2,  
            i=f'{self._icon}/toLeft.png', bgc=self.btnBgc, 
            c=pm.Callback(self.runMirror), e=True)

        pm.textField(self.tfDpL, tx='L_', h=28, e=True)

        pm.textField(self.tfDpR, tx='R_', h=28, e=True)

        pm.checkBox(self.cbJsd, h=30, v=True, e=True)

        pm.iconTextButton(self.ibDpl, st=ith, w=140, h=26, mw=7, mh=2,  
            i=f'{self._icon}/toLeft.png', bgc=self.btnBgc, 
            c=pm.Callback(self.runDuplicateMirror), e=True)


        #-----------------------------------------------------------------------
        #--- Edit UI Layout ----------------------------------------------------
        t, b, l, r = ['top', 'bottom', 'left', 'right']


        pm.formLayout(self._fmL, e=True, af=[
        (self._sep,  t,   0), (self._sep,   l,  0), (self._sep,   r,  0), 
        (self.rbTyp, t,  15), (self.rbTyp,  l, 10), (self.rbTyp,  r, 10),
        (self.ibMir, t,  60), (self.ibMir,  l, 10), (self.ibMir,  r, 10), 
        (self._spMr, t,  95), (self._spMr,  l,  5), (self._spMr,  r,  5), 
        (self.tfDpL, t, 105), (self.tfDpL,  l, 10), 
        (self.tfDpR, t, 105),                       
        (self.cbJsd, t, 105),                       (self.cbJsd,  r, 10), 
        (self.ibDpl, t, 140), (self.ibDpl,  l, 10), (self.ibDpl,  r, 10), 
        (self._spDp, t, 175), (self._spDp,  l,  5), (self._spDp,  r,  5), 
        ], ap=[
        (self.tfDpL, r,  5, 35), 
        (self.tfDpR, l,  0, 35), (self.tfDpR, r,  5, 65),
        (self.cbJsd, l,  5, 65), 
        ])


        window.show()

        #-- init command -------------------------------------------------------
        pm.window(self.windowName, e=True,
                  w = self.windowSize[0], 
                  h = self.windowSize[1])


def showUI():
    testIns = mirrorUI()
    testIns.main()

