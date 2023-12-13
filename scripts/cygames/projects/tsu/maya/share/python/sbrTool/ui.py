# -*- coding: utf-8 -*-
from __future__ import absolute_import

#----- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import json


from . import core

#from . import core
#reload(core)
#from . import adn
#reload(adn)
#from . import setup
#reload(setup)



class multiConnectionUI(object):
    def __init__(self):
        self.__ver__     = '0.0.2'
        self.windowName  = 'simulationBlendRateTool'
        self.windowTitle = 'Simulation Blend Rate Tool v{0}'.format(self.__ver__)
        self.windowSize  = [300, 300]
        self._maya_url   = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._help_url   = r'https://wisdom.cygames.jp/x/ZjEJDw'
        #--- current script path -----------------------------------------------
        self.__dir = os.path.dirname(os.path.abspath(__file__))
        #-- image path ---------------------------------------------------------
        self._idir = r'{0}/_data/_icon'.format(self.__dir)
        #-- color --------------------------------------------------------------
        self.btnBgc = (0.37, 0.37, 0.37)
        #-- initial variables --------------------------------------------------
        self._an_ibt = u''

    #-- initial funsionts ------------------------------------------------------
    def checkWindowOverlap(self):
        if pm.window(self.windowName, ex=True):
            pm.deleteUI(self.windowName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)


    #--- functions -------------------------------------------------------------
    def _getNamespace(self, *args):
        nsl = core.getNameSpace()
        pm.optionMenu(self._opm0, dai=True, e=True)
        pm.menuItem(l='All', p=self._opm0)
        for i in nsl:
            pm.menuItem(l=i, p=self._opm0)   


    def _addJtList(self, *args):
        jtl = core.getSBRJointlist()
        pm.textScrollList(self._tsl0, ra=True, e=True)
        pm.textScrollList(self._tsl0, a=jtl, e=True)


    def _selJt(self, *args):
        si = pm.textScrollList(self._tsl0, si=True, q=True)
        pm.select(si, r=True)


    def _addSBRAttr(self, *args):
        core.addSBRAttr()
        self._refresh()


    def _delSBRAttr(self, *args):
        core.deleteSBRAttr()
        self._refresh()


    def _refresh(self, *args):
        self._getNamespace()
        self._addJtList()


    def _setKey(self, *args):
        core.setKey()


    def _setKeyValue(self, v=1, *args):
        core.setKeyValue(v)


    #--- edit UI ---------------------------------------------------------------
    def _sort(self, *args):
        lsti = pm.textScrollList(self._tsl0, ai=True, q=True)
        ns   = pm.optionMenu(self._opm0, v=True, q=True)
        if not ns == 'All':
            resl = core.listSort(lsti, ns)
            pm.textScrollList(self._tsl0, ra=True, e=True)
            pm.textScrollList(self._tsl0, a=resl, e=True)
        else:
            self._addJtList()



    #--- main UI ---------------------------------------------------------------
    def main(self):
        self.checkWindowOverlap()
        window = pm.window(self.windowName, mb = True,
                           t = self.windowTitle,
                           w = self.windowSize[0],
                           h = self.windowSize[1])

        #-- menu ---------------------------------------------------------------
        pm.menu(l='Help', hm=True)
        pm.menuItem(l='Maya 2019 HELP', c=self.show_mayaHelp)
        pm.menuItem(d=True)
        pm.menuItem(l='Tool HELP', c=self.show_toolHelp)


        #-- layout -------------------------------------------------------------
        #-- Pane Layout
        self._fmL0 = pm.formLayout(nd=100)
        self._sep0 = pm.separator()

        self._opm0 = pm.optionMenu(l='')
        pm.menuItem(l='All')
        self._tsl0 = pm.textScrollList(ams=True)

        self._ibt1 = pm.iconTextButton(l='Add')
        self._ibt2 = pm.iconTextButton(l='Delete')
        self._ibt3 = pm.iconTextButton(l='Reflesh')

        self._sep1 = pm.separator()

        self._ibt4 = pm.iconTextButton(l='Set Key')
        self._ibt5 = pm.iconTextButton(l='0 Key')
        self._ibt6 = pm.iconTextButton(l='1 key')

        self._sep2 = pm.separator()

        #-----------------------------------------------------------------------
        #--- Edit UI elements --------------------------------------------------
        pm.optionMenu(self._opm0, h=24, cc=pm.Callback(self._sort), e=True)

        pm.textScrollList(self._tsl0, sc=pm.Callback(self._selJt), e=True)

        pm.iconTextButton(self._ibt1, c=pm.Callback(self._addSBRAttr),
        st='iconAndTextHorizontal', i1='{0}/adnCreate.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibt2, c=pm.Callback(self._delSBRAttr),
        st='iconAndTextHorizontal', i1='{0}/delete.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibt3, c=pm.Callback(self._refresh),
        st='iconAndTextHorizontal', i1='{0}/update.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.separator(self._sep1, st='in', w=100, e=True)

        pm.iconTextButton(self._ibt4, c=pm.Callback(self._setKey),
        st='iconAndTextHorizontal', i1='{0}/key.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibt5, c=pm.Callback(self._setKeyValue, 0),
        st='iconAndTextHorizontal', i1='{0}/key0.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibt6, c=pm.Callback(self._setKeyValue, 1),
        st='iconAndTextHorizontal', i1='{0}/key1.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.separator(self._sep2, st='none', w=100, e=True)

        #-----------------------------------------------------------------------
        #--- Edit UI Layout ----------------------------------------------------
        t, b, l, r = ['top', 'bottom', 'left', 'right']

        pm.formLayout(self._fmL0, e=True,
        af = [(self._sep0, t,   0), (self._sep0, l,   0), (self._sep0, r,   0), 
              (self._opm0, t,  10), (self._opm0, l,  10), (self._opm0, r, 120),
              (self._tsl0, t,  40), (self._tsl0, l,  10), (self._tsl0, r, 120), (self._tsl0, b,  10), 
              (self._ibt1, t,  40), (self._ibt1, r,  10),
              (self._ibt2, t,  70), (self._ibt2, r,  10), 
              (self._ibt3, t, 100), (self._ibt3, r,  10), 
              (self._sep1, t, 135), (self._sep1, r,  10), 
              (self._ibt4, t, 150), (self._ibt4, r,  10),
              (self._ibt5, t, 180), (self._ibt5, r,  10), 
              (self._ibt6, t, 210), (self._ibt6, r,  10), 
              (self._sep2, t, 250), (self._sep2, r,  10), 
             ])


        window.show()

        #-- init command -------------------------------------------------------
        self._refresh()

        pm.window(self.windowName, e=True,
                  w = self.windowSize[0], 
                  h = self.windowSize[1])


def showUI():
    testIns = multiConnectionUI()
    testIns.main()

