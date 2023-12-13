# -*- coding: utf-8 -*-
from __future__ import absolute_import

#-- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os

def setEdit(typ=0, tgtSet=[]):
    '''
maya object set edit

Parameters:
  - int typ: type of set edit 

Returns:
  - : 

Error:
  - :
    '''
    if typ == 0: # -- add to target set
        if tgtSet:
            for tgt in tgtSet:
                mc.sets(mc.ls(sl=True), add=tgt)
        else:
            mc.warning('Please fill in new set name.')

    elif typ == 1: # -- remove from target set
        if tgtSet:
            for tgt in tgtSet:
                mc.sets(mc.ls(sl=True), rm=tgt)
        else:
            mc.warning('Please fill in new set name.')

    elif typ == 2: # -- simple parent set
        selectObj = mc.ls(sl=True)
        if mc.nodeType(selectObj[-1]) == 'objectSet':
            selectObj = mc.ls(sl=True)
            mc.sets(selectObj[:-1], add=selectObj[-1])
        else :
            mc.warning('Please select objectSet node at the end.')

    elif typ == 3: # -- simple unparent set
        selectObj = mc.ls(sl=True)
        if mc.nodeType(selectObj[-1]) == 'objectSet':
            mc.sets(selectObj[:-1], rm=selectObj[-1])
        else :
            mc.warning('Please select objectSet node at the end.')

    elif typ == 4: # -- add attribute
        atList  = mc.channelBox('mainChannelBox', sma=True, q=True)
        objList = mc.ls(sl=True)
        if tgtSet:
            for tgt in tgtSet:
                if objList:
                    chList = ['{0}.{1}'.format(obj, at) for obj in objList for at in atList]
                    mc.sets(chList, add=tgt)


class setEditorUI(object):
    def __init__(self):
        self.__ver__          = '0.1.0'
        self.windowManageName = 'setEditor'
        self.windowTitle      = 'Set Editor v{0}'.format(self.__ver__)
        self.windowSize       = [400, 200]
        self._mayaHelp_url    = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._toolHelp_url    = r'https://wisdom.cygames.jp/display/tsubasa/%5BMaya%5D+Set+Editor'
        #--- current script path -----------------------------------------------
        self._dir = os.path.dirname(os.path.abspath(__file__))
        #-- image path ---------------------------------------------------------
        self._ico = r'{0}/_data/_icon'.format(self._dir)

    def checkWindowOverlap(self):
        if pm.window(self.windowManageName, ex=True):
            pm.deleteUI(self.windowManageName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)


    # -- functions -------------------------------------------------------
    def run_createNewSet(self):
        nameList = self._cs_txf.getText().replace(' ', '').split(',')
        setList  = []
        if nameList:
            for name in nameList:
                if name:
                    newSet = mc.sets(n=name)
                    print('create new set: {0}'.format(name))
                    setList.append(newSet)
                else:
                    newSet = mc.sets()
                    print('create new set: {0}'.format(newSet))
                    setList.append(newSet)

            self._ts_txf.setText(','.join(setList))
            return setList


    def run_getSetName(self):
        tgtSet = mc.ls(sl=True, typ='objectSet')
        if tgtSet:
            self._ts_txf.setText(', '.join(tgtSet))
        else:
            mc.warning('Please select objectSet node.')


    def run_se_add(self):
        typ    = 0
        tgtSet = self._ts_txf.getText().replace(' ', '').split(',')
        setEdit(typ, tgtSet)


    def run_se_remove(self):
        typ    = 1
        tgtSet = self._ts_txf.getText().replace(' ', '').split(',')
        setEdit(typ, tgtSet)


    def run_se_parent(self):
        typ    = 2
        tgtSet = []
        setEdit(typ, tgtSet)


    def run_se_unparent(self):
        typ    = 3
        tgtSet = []
        setEdit(typ, tgtSet)


    def run_se_addAttr(self):
        typ    = 4
        tgtSet = self._ts_txf.getText().replace(' ', '').split(',')
        setEdit(typ, tgtSet)


    def selectAttrFromCB(self):
        atList  = mc.channelBox('mainChannelBox', sma=True, q=True)
        objList = mc.ls(sl=True)

        if objList:
            chList = ['{0}.{1}'.format(obj, at) for obj in objList for at in atList]
        mc.select(chList, r=True)


    # -- edit UI ----------------------------------------
    def reset_UI(self):
        self._cs_txf.setText('')
        self._ts_txf.setText('')


    # -- main UI ----------------------------------------
    def main(self):               
        self.checkWindowOverlap()
        window = pm.window(self.windowManageName,
                           t  = self.windowTitle,
                           w  = self.windowSize[0],
                           h  = self.windowSize[1],
                           mb = True)

        # -- menu
        pm.menu(l  = 'Tools', 
                to = False)
        pm.menuItem(l = 'Reset UI',
                    i = 'redrawPaintEffects.png',
                    c = pm.Callback(self.reset_UI))
        pm.menu(l  = 'Help', 
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
            
            # -- main form layout
            self.fmL1 = pm.formLayout(nd=100)
            with self.fmL1:
                self._cs_txt = pm.text(l='New Set : ', al='right', w=70, h=24)
                self._cs_txf = pm.textField(pht='new set name', h=24)
                self._cs_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                 i   = '{0}/create.png'.format(self._ico), 
                                                 rpt = True,
                                                 al  = 'center', 
                                                 bgc = (0.4, 0.4, 0.4),
                                                 l   = 'Create', 
                                                 c   = pm.Callback(self.run_createNewSet), 
                                                 w   = 80, 
                                                 mw  = 5
                                                 )

                self._ts_txt = pm.text(l='Target Set : ', al='right', w=70, h=24)
                self._ts_txf = pm.textField(pht='target set name', h=24)
                self._ts_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                 i   = '{0}/left.png'.format(self._ico), 
                                                 rpt = True,
                                                 al  = 'center', 
                                                 bgc = (0.4, 0.4, 0.4),
                                                 l   = 'Get', 
                                                 c   = pm.Callback(self.run_getSetName), 
                                                 w   = 80, 
                                                 mw  = 5
                                                 )

                self._ad_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                 i   = '{0}/add.png'.format(self._ico),
                                                 rpt = True, 
                                                 al  = 'center', 
                                                 bgc = (0.4, 0.4, 0.4),
                                                 l   = 'Add', 
                                                 c   = pm.Callback(self.run_se_add),
                                                 h   = 30, 
                                                 mw  = 5
                                                 )
                self._rm_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                 i1  = '{0}/remove.png'.format(self._ico),
                                                 rpt = True, 
                                                 al  = 'center', 
                                                 bgc = (0.4, 0.4, 0.4),
                                                 l   = 'Remove', 
                                                 c   = pm.Callback(self.run_se_remove),
                                                 h   = 30, 
                                                 mw  = 5
                                                 )
                self._at_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                 i   = '{0}/channels.png'.format(self._ico),
                                                 rpt = True, 
                                                 al  = 'center', 
                                                 bgc = (0.4, 0.4, 0.4),
                                                 l   = 'Add Attribute from CB', 
                                                 c   = pm.Callback(self.run_se_addAttr),
                                                 h   = 30, 
                                                 mw  = 5
                                                 )
                self._st_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                 i   = '{0}/channels.png'.format(self._ico),
                                                 rpt = True, 
                                                 al  = 'center', 
                                                 bgc = (0.4, 0.4, 0.4),
                                                 l   = 'Select Attribute from CB', 
                                                 c   = pm.Callback(self.selectAttrFromCB),
                                                 h   = 30, 
                                                 mw  = 5
                                                 )


                self.sep1    = pm.separator(st='in')

                self._sp_txt = pm.text(l=' Sets Parenting : ', al='right', w=90, h=18)
                self._pa_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                 i   = '{0}/parent.png'.format(self._ico), 
                                                 rpt = True,
                                                 al  = 'center', 
                                                 bgc = (0.4, 0.4, 0.4),
                                                 l   = 'Parent', 
                                                 c   = pm.Callback(self.run_se_parent), 
                                                 h   = 30, 
                                                 mw  = 5                                                 
                                                 )
                self._up_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                 i   = '{0}/unparent.png'.format(self._ico), 
                                                 rpt = True,
                                                 al  = 'center', 
                                                 bgc = (0.4, 0.4, 0.4),
                                                 l   = 'Unparent', 
                                                 c   = pm.Callback(self.run_se_unparent), 
                                                 h   = 30, 
                                                 mw  = 5
                                                 )
                self.sep2    = pm.separator()


        # -- Edit UI Layout
        pm.formLayout(self.fmL0, e=True,
               af = [(self.sep0, 'top', 0), (self.sep0, 'left', 0), (self.sep0, 'right', 0), 
                     (self.fmL1, 'top', 0), (self.fmL1, 'left', 0), (self.fmL1, 'right', 0), (self.fmL1, 'bottom', 0),
                    ])
                    
        pm.formLayout(self.fmL1, e=True,
               af = [(self._cs_txt, 'top', 20), (self._cs_txt, 'left', 10), 
                     (self._cs_txf, 'top', 20), (self._cs_txf, 'left', 85), (self._cs_txf, 'right', 95),
                     (self._cs_btn, 'top', 20), (self._cs_btn, 'right', 10),

                     (self._ts_txt, 'top', 50), (self._ts_txt, 'left', 10), 
                     (self._ts_txf, 'top', 50), (self._ts_txf, 'left', 85), (self._ts_txf, 'right', 95),
                     (self._ts_btn, 'top', 50), (self._ts_btn, 'right', 10),

                     (self._ad_btn, 'top',  90), (self._ad_btn, 'left', 10),
                     (self._rm_btn, 'top',  90), (self._rm_btn, 'right', 10),
                     (self._at_btn, 'top', 125), (self._at_btn, 'left', 10),
                     (self._st_btn, 'top', 125), (self._st_btn, 'right', 10),
                     
                     (self.sep1, 'top', 165), (self.sep1, 'left', 10), (self.sep1, 'right', 10),

                     (self._sp_txt, 'top', 175), (self._sp_txt, 'left', 10), 
                     (self._pa_btn, 'top', 200), (self._pa_btn, 'left', 10), 
                     (self._up_btn, 'top', 200), (self._up_btn, 'right', 10),
                     (self.sep2, 'bottom', 10),
                    ],
               ap = [(self._ad_btn, 'right', 2, 50), (self._rm_btn,  'left', 2, 50), 
                     (self._at_btn, 'right', 2, 50), (self._st_btn,  'left', 2, 50), 
                     (self._pa_btn, 'right', 2, 50), (self._up_btn,  'left', 2, 50), 
                    ])
                    
        window.show()
        

def showUI():
    testIns = setEditorUI()
    testIns.main()
