# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : diagnosis
# Author  : rkanda
# Version : 0.0.1
# Updata  : 2019/10/07 18:38:26
# ----------------------------------
# ---- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import json

# ---- import functions
import os
path     = os.path.dirname(os.path.abspath(__file__))
exList   = ['__init__.py', '__temp__.py']
funcList = [i.replace('.py', '') for i in os.listdir(r'{0}/functions'.format(path)) if not i in exList]
# print funcList

for func in funcList:
    exec('from .functions import {0}'.format(func))
    exec('reload({0})'.format(func))


class diagnosisUI(object):
    def __init__(self):
        self.__ver__          = '0.0.1'
        self.windowManageName = 'diagnosis'
        self.windowTitle      = 'Diagnosis v{0}'.format(self.__ver__)
        self.windowSize       = [800, 600]
        self._mayaHelp_url    = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._toolHelp_url    = r'https://wisdom.cygames.jp/display/tsubasa/%5BMaya%5D+FC+Support+Tools'


    def checkWindowOverlap(self):
        if pm.window(self.windowManageName, ex=True):
            pm.deleteUI(self.windowManageName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)


    # -- run --------------------------------------------------------------------
    def run_check(self, func=''):
        exec('log = {0}.check()'.format(func))
        ctx    = pm.scrollField(self._fbl_scF, tx=True, q=True)
        sepStr = ' ------------ {0} check log ------------- \n'.format(func)
        resStr = ctx + sepStr + log 
        pm.scrollField(self._fbl_scF, tx=resStr, e=True)
        pm.button('_{0}_ch_btn'.format(func), bgc = (0.3, 0.5, 0.3), e=True)


    def run_execute(self, func=''):
        exec('log = {0}.execute()'.format(func))
        ctx    = pm.scrollField(self._fbl_scF, tx=True, q=True)
        sepStr = ' ------------ {0} execute log ------------- \n'.format(func)
        resStr = ctx + sepStr + log 
        pm.scrollField(self._fbl_scF, tx=resStr, e=True)
        pm.button('_{0}_ex_btn'.format(func), bgc = (0.3, 0.5, 0.3), e=True)


    # -- run all
    def run_checkAll(self):
        for func in funcList:
            if pm.checkBox('_{0}_ckb'.format(func), v=True, q=True):
                self.run_check(func)


    def run_executeAll(self):
        for func in funcList:
            if pm.checkBox('_{0}_ckb'.format(func), v=True, q=True):
                self.run_execute(func)


    # -- log --------------------------------------------------------------------
    def clearLog(self):
        pm.scrollField(self._fbl_scF, tx='', e=True)


    def selectListedObject(self):
        listStr = pm.scrollField(self._fbl_scF, sl=True, q=True)
        objList = [i for i in listStr.split(' ') if pm.objExists(i)]
        pm.select(objList, r=True)


    # -- edit UI ----------------------------------------------------------------
    def resetUI(self):
        pm.scrollField(self._fbl_scF, tx='', e=True)
        for func in funcList:
            pm.button('_{0}_ch_btn'.format(func), bgc = (0.3, 0.3, 0.3), e=True)
            pm.button('_{0}_ex_btn'.format(func), bgc = (0.3, 0.3, 0.3), e=True)
        self.toggleCheckAll()


    def toggleCheckAll(self):
        val = self._all_ckb.getValue()
        for func in funcList:
            pm.checkBox('_{0}_ckb'.format(func), v=val, e=True)
            self.toggleFunctionBGC(func)


    def toggleFunctionBGC(self, func=''):
        val = pm.checkBox('_{0}_ckb'.format(func), v=True, q=True)
        if val:
            pm.rowLayout('_{0}_rwL'.format(func), bgc=(0.25, 0.25, 0.25), e=True)
        else:
            pm.rowLayout('_{0}_rwL'.format(func), bgc=(0.20, 0.20, 0.20), e=True)


    # -- UI
    def main(self):               
        self.checkWindowOverlap()
        window = pm.window(self.windowManageName,
                           t  = self.windowTitle,
                           w  = self.windowSize[0],
                           h  = self.windowSize[1],
                           mb = True,
                           iconName = 'HIKmenuButton.png')

        # -- menu
        pm.menu(l  = 'Tools', 
                to = False)
        pm.menuItem(l = 'Clear Log',
                    i = 'clearCanvas.png', 
                    c = pm.Callback(self.clearLog)) 
        pm.menuItem(l = 'Reset UI',
                    i = 'redrawPaintEffects.png',
                    c = pm.Callback(self.resetUI))
        pm.menu(l  ='Help', 
                to = False, 
                hm = True)
        pm.menuItem(l = 'Maya 2019 HELP',
                    c = self.show_mayaHelp)
        pm.menuItem(d = True)
        pm.menuItem(l = 'Tool HELP',
                    c = self.show_toolHelp)

        # -- base form layout
        self.fmL0 = pm.formLayout(nd=100)
        with self.fmL0:
            self.sep0 = pm.separator()
            self.pnL0 = pm.paneLayout(cn='vertical2')
            with self.pnL0:
                # -- main form layout
                self.fmL1 = pm.formLayout(nd=100)
                with self.fmL1:
                    self._all_ckb = pm.checkBox(l  = 'All',
                                                v  = True,
                                                cc = pm.Callback(self.toggleCheckAll),
                                                h  = 28)
                    self._ack_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                      i   = 'search.png', 
                                                      bgc = (0.4, 0.4, 0.4),
                                                      l   = 'All check', 
                                                      c   = pm.Callback(self.run_checkAll), 
                                                      h   = 25,
                                                      mw  = 2
                                                      )    
                    self._aex_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                      i   = 'execute.png', 
                                                      bgc = (0.4, 0.4, 0.4),
                                                      l   = 'All execute', 
                                                      c   = pm.Callback(self.run_executeAll), 
                                                      h   = 25,
                                                      mw  = 2
                                                      )
                    #self.sep1 = pm.separator(st='in')
                    self._fnc_cmL = pm.columnLayout(adj = True,
                                                    cat = ('both', 1), 
                                                    rs  = 1, 
                                                    bgc = (0.15, 0.15, 0.15))
                    with self._fnc_cmL:
                        for func in funcList:
                            exec('funcLabel = {0}.__label__'.format(func))
                            exec('funcInfo  = {0}.__info__'.format(func))

                            pm.rowLayout('_{0}_rwL'.format(func),
                                         ann = funcInfo,
                                         nc  = 3, 
                                         cw3 = (80, 60, 60), 
                                         adj = 1, 
                                         cal = (1, 'right'), 
                                         cat = [(1, 'both', 4), (2, 'both', 0), (3, 'both', 0)],
                                         bgc = (0.25, 0.25, 0.25),
                                         h   = 28)
                            pm.checkBox('_{0}_ckb'.format(func),
                                        l  = funcLabel,
                                        v  = True,
                                        cc = pm.Callback(self.toggleFunctionBGC, func))
                            pm.button('_{0}_ch_btn'.format(func),
                                      l = 'Check', 
                                      c = pm.Callback(self.run_check, func),
                                    bgc = (0.3, 0.3, 0.3))
                            pm.button('_{0}_ex_btn'.format(func),
                                      l = 'Execute', 
                                      c = pm.Callback(self.run_execute, func),
                                    bgc = (0.3, 0.3, 0.3))
                            pm.setParent('..')

                self.fmL2 = pm.formLayout(nd=100)
                with self.fmL2:
                    self._fbl_scF = pm.scrollField(ed=True, ww=False, tx='')
                    self._fbl_pum = pm.popupMenu(b=3)
                    pm.menuItem(l = 'Clear Log', 
                                i = 'clearCanvas.png',
                                c = pm.Callback(self.clearLog)
                                )
                    pm.menuItem(l = 'Reset UI', 
                                i = 'redrawPaintEffects.png',
                                c = pm.Callback(self.resetUI)
                                )
                    pm.menuItem(d = True)
                    pm.menuItem(l = 'Select',
                                i = 'aselect.png',
                                c = pm.Callback(self.selectListedObject)
                                )
            self._hpl = pm.helpLine(bgc = (0.15, 0.15, 0.15),
                                    h   = 25)

        # -- Edit UI Layout
        pm.formLayout(self.fmL0, e=True,
               af = [(self.sep0, 'top', 0), (self.sep0, 'left', 0), (self.sep0, 'right', 0), 
                     (self.pnL0, 'top', 0), (self.pnL0, 'left', 0), (self.pnL0, 'right', 0), (self.pnL0, 'bottom', 35),
                                            (self._hpl, 'left', 5), (self._hpl, 'right', 5), (self._hpl, 'bottom', 5),
                    ])

        pm.formLayout(self.fmL1, e=True,
               af = [(self._all_ckb, 'top', 10), (self._all_ckb, 'left', 10), 
                     (self._ack_btn, 'top', 10), (self._ack_btn, 'left', 60), 
                     (self._aex_btn, 'top', 10),                              (self._aex_btn, 'right', 0),
                     #(self.sep1,     'top', 45), (self.sep1,     'left', 5), (self.sep1,     'right', 0), 
                     (self._fnc_cmL, 'top', 45), (self._fnc_cmL, 'left', 5), (self._fnc_cmL, 'right', 0), (self._fnc_cmL, 'bottom', 0),
                    ],
               ap = [(self._ack_btn, 'right', 5, 55), 
                     (self._aex_btn, 'left',  0, 55)
                    ])
        pm.formLayout(self.fmL2, e=True,
               af = [(self._fbl_scF, 'top', 0), (self._fbl_scF, 'left', 0), (self._fbl_scF, 'right', 5), (self._fbl_scF, 'bottom', 0),
                    ])

        window.show()

def showUI():
    testIns = diagnosisUI()
    testIns.main()

