# -*- coding: utf-8 -*-
from __future__ import absolute_import

#----- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import json


from . import core
from . import command

#from . import core
#reload(core)
#from . import command
#reload(command)
#from . import adn
#reload(adn)
#from . import setup
#reload(setup)



class smearSupportUI(object):
    def __init__(self):
        self.__ver__     = '0.0.2'
        self.windowName  = 'smearSupport'
        self.windowTitle = 'Smear Support v{0}'.format(self.__ver__)
        self.windowSize  = [300, 300]
        self._maya_url   = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._help_url   = r'https://wisdom.cygames.jp/x/AOmBEQ'
        #--- current script path -----------------------------------------------
        self.__dir = os.path.dirname(os.path.abspath(__file__))
        #-- image path ---------------------------------------------------------
        self._idir = r'{0}/_data/_icon'.format(self.__dir)
        self._wdir = r'{0}/_data/_weight'.format(self.__dir)
        #-- color --------------------------------------------------------------
        self.btnBgc = (0.37, 0.37, 0.37)
        #-- initial variables --------------------------------------------------
        self._an_ibt = u''

    #-- initial funsionts ------------------------------------------------------
    def checkWindowOverlap(self):
        if pm.window(self.windowName, ex=True):
            pm.deleteUI(self.windowName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._maya_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._help_url)


    #--- functions -------------------------------------------------------------
    def _selectJoint(self, *args):
        core.selectJoint()


    def _setLabel(self, *args):
        core.setJointLabel()


    def _createCtrl(self, *args):
        core.createCtrl()


    def _ctrlConnect(self, *args):
        core.setConstraint()


    def _getMesh(self, *args):
        mesh = core.getMesh()
        if mesh:
            pm.textField(self._tfmh, tx=mesh, e=True)


    def _createCage(self, *args):
        obj = pm.textField(self._tfmh, tx=True, q=True)
        if obj:
            bnd = core.createBendCage(obj)
            bla = core.createBlurACage(obj)
            blb = core.createBlurBCage(bla)

            pm.textField(self._tfbn, tx=bnd, e=True)
            pm.textField(self._tfba, tx=bla, e=True)
            pm.textField(self._tfbb, tx=blb, e=True)
        else:
            pm.warning('Please fill in Smear object name.')


    def _getBend(self, *args):
        mesh = core.getMesh()
        if mesh:
            pm.textField(self._tfbn, tx=mesh, e=True)

    def _getBlurA(self, *args):
        mesh = core.getMesh()
        if mesh:
            pm.textField(self._tfba, tx=mesh, e=True)

    def _getBlurB(self, *args):
        mesh = core.getMesh()
        if mesh:
            pm.textField(self._tfbb, tx=mesh, e=True)


    def _bindCage(self, *args):
        jt = pm.PyNode('_000')
        j0 = pm.PyNode('_300')
        j1 = pm.PyNode('_301')
        j2 = pm.PyNode('_302')

        bnd = pm.textField(self._tfbn, tx=True, q=True)
        if pm.objExists(bnd):
            core.bindBendCage(bnd, [jt, j0])

        bla = pm.textField(self._tfba, tx=True, q=True)
        if pm.objExists(bla):
            core.bindBendCage(bla, [jt, j0, j1])

        blb = pm.textField(self._tfbb, tx=True, q=True)
        if pm.objExists(blb):
            core.bindBendCage(blb, [jt, j0, j1, j2]) 


    def _appendInf(self, *args):
        sel = pm.selected() #-- init sel
        pm.textScrollList(self._tsif, ra=True, e=True)
        pm.text(self._txob, l='', e=True)
        pm.text(self._txif, l='', e=True) 

        if sel:
            pm.select(sel[-1], r=True)
            pm.text(self._txob, l='{0}'.format(sel[-1].name()), e=True)

            sc = core.selectSkinClusterFormSkin()
            if sc:
                pm.text(self._txif, l='{0}'.format(sc[0]), e=True) 

                jt = core.selectJointsFromSkinCluster()
                if jt:
                    pm.textScrollList(self._tsif, a=jt, e=True)

        #-- reselect
        pm.select(sel, r=True)


    def _copyWeight(self, *args):
        sel = pm.selected() #-- init sel
        wt   = {}
        pm.text(self._txst, l='', e=True) 

        mesh = pm.text(self._txob, l=True, q=True)
        sc   = pm.text(self._txif, l=True, q=True)
        jt   = pm.textScrollList(self._tsif, si=True, q=True)

        if jt:
            wt = core.copyWeight(mesh, sc, jt[0])
            path = r'{0}/_weight.json'.format(self._wdir)
            command.exportJson(path, wt)
            print('Copy weight successfully.')
            pm.text(self._txst, l='Copy:   {0}'.format(jt[0]), e=True)

            #-- reselect    
            pm.select(sel, r=True)

        else:
            pm.warning('Please select joint from list.')


    def _pasteWeight(self, *args):
        path = r'{0}/_weight.json'.format(self._wdir)
        wts  = command.importJson(path)

        mesh = pm.text(self._txob, l=True, q=True)
        sc   = pm.text(self._txif, l=True, q=True)
        tjt  = pm.textScrollList(self._tsif, si=True, q=True)

        if tjt:
            core.pasetWeight(mesh, sc, wts, tjt[0])

        else:
            pm.warning('Please select joint from list.')


    def _selSC(self, *args):
        core.selectSkinClusterFormSkin()


    def _selJt(self, *args):
        core.selectJointsFromSkin()


    def _multiCopy(self, *args):
        core.weightDistributer()


    def _bindCopy(self, *args):
        core.bindAndCopy()


    def _alignGet(self, *args):
        jwd = core.getWeight()
        if jwd:
            path = r'{0}/_vtxWeight.json'.format(self._wdir)
            command.exportJson(path, jwd)


    def _alignSet(self, *args):
        path = r'{0}/_vtxWeight.json'.format(self._wdir)
        jwd  = command.importJson(path)
        core.setWeight(jwd)


    #--- edit UI ---------------------------------------------------------------




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

        self._fLct = pm.formLayout(nd=100)
        self._btsj = pm.button(l='Select Joint')
        self._btnl = pm.button(l='Set Name && Label')
        self._btcc = pm.button(l='Create Ctrl')
        self._btcn = pm.button(l='Connect')
        self._spct = pm.separator(st='in')
        pm.setParent('..')

        self._fLca = pm.formLayout(nd=100)
        self._tfmh = pm.textField(pht='msh_sword')
        self._btmh = pm.button(l=' << ')
        self._btca = pm.button(l='Create Cage')
        self._spmh = pm.separator(st='in')
        pm.setParent('..')

        self._fLbm = pm.formLayout(nd=100)
        self._txbn = pm.text(l='Bend ')
        self._tfbn = pm.textField()
        self._btbn = pm.button(l=' << ')
        self._txba = pm.text(l='BlurA ')
        self._tfba = pm.textField()
        self._btba = pm.button(l=' << ')
        self._txbb = pm.text(l='BlurB ')
        self._tfbb = pm.textField()
        self._btbb = pm.button(l=' << ')
        self._btbd = pm.button(l='Bind')
        self._spca = pm.separator(st='in')
        pm.setParent('..')

        self._fLcw = pm.formLayout(nd=100)
        self._txol = pm.text(l='Name :   ') 
        self._txil = pm.text(l='SkinCluster :   ') 
        self._txob = pm.text(l='') 
        self._txif = pm.text(l='') 
        self._tsif = pm.textScrollList(ams=False)
        self._btcp = pm.button(l='Copy')
        self._btpa = pm.button(l='Paste')
        self._txst = pm.text(l='') 
        self._spcp = pm.separator(st='in')
        pm.setParent('..')

        self._fLfc = pm.formLayout(nd=100)
        self._btf1 = pm.button(l='Sel SkinCluster')
        self._btf2 = pm.button(l='Sel Joint')
        self._btf3 = pm.button(l='Copy Multi')
        self._btf4 = pm.button(l='Bind && Copy')
        self._btf5 = pm.button(l='Align Copy')
        self._btf6 = pm.button(l='Align Paset')
        self._spfc = pm.separator(st='none')
        pm.setParent('..')


        #-----------------------------------------------------------------------
        #--- Edit UI elements --------------------------------------------------
        pm.button(self._btsj, c=pm.Callback(self._selectJoint), h=26, e=True)
        pm.button(self._btnl, c=pm.Callback(self._setLabel), h=26, e=True)
        pm.button(self._btcc, c=pm.Callback(self._createCtrl), h=26, e=True)
        pm.button(self._btcn, c=pm.Callback(self._ctrlConnect), h=26, e=True)

        pm.textField(self._tfmh, h=25, e=True)
        pm.button(self._btmh, c=pm.Callback(self._getMesh), w=30, e=True)
        pm.button(self._btca, c=pm.Callback(self._createCage), h=28, e=True)

        pm.text(self._txbn, w=40, h=24, al='right', e=True)
        pm.textField(self._tfbn, h=25, e=True)
        pm.button(self._btbn, c=pm.Callback(self._getBend), w=30, e=True)
        pm.text(self._txba, w=40, h=24, al='right', e=True)
        pm.textField(self._tfba, h=25, e=True)
        pm.button(self._btba, c=pm.Callback(self._getBlurA), w=30, e=True)
        pm.text(self._txbb, w=40, h=24, al='right', e=True)
        pm.textField(self._tfbb, h=25, e=True)
        pm.button(self._btbb, c=pm.Callback(self._getBlurB), w=30, e=True)
        pm.button(self._btbd, c=pm.Callback(self._bindCage), h=28, e=True)

        pm.text(self._txol, al='right', w=80, e=True)
        pm.text(self._txil, al='right', w=80, e=True) 
        pm.text(self._txob, al='left', e=True)
        pm.text(self._txif, al='left', e=True) 

        pm.textScrollList(self._tsif, h=40, e=True)
        pm.button(self._btcp, c=pm.Callback(self._copyWeight), w=70, e=True)
        pm.button(self._btpa, c=pm.Callback(self._pasteWeight), w=70, e=True)
        pm.text(self._txst, al='left', w=70, e=True) 

        pm.button(self._btf1, c=pm.Callback(self._selSC), h=26, e=True)
        pm.button(self._btf2, c=pm.Callback(self._selJt), h=26, e=True)
        pm.button(self._btf3, c=pm.Callback(self._multiCopy), h=26, e=True)
        pm.button(self._btf4, c=pm.Callback(self._bindCopy), h=26, e=True)
        pm.button(self._btf5, c=pm.Callback(self._alignGet), h=26, e=True)
        pm.button(self._btf6, c=pm.Callback(self._alignSet), h=26, e=True)


        #-----------------------------------------------------------------------
        #--- Edit UI Layout ----------------------------------------------------
        t, b, l, r = ['top', 'bottom', 'left', 'right']

        pm.formLayout(self._fmL0, e=True,
        af = [
        (self._sep0, t,   0), (self._sep0, l,   0), (self._sep0, r,   0), 
        (self._fLct, t,  10), (self._fLct, l,   0), (self._fLct, r,   0), 
        (self._fLca, t, 160), (self._fLca, l,   0), (self._fLca, r,   0), 
        (self._fLbm, t, 250), (self._fLbm, l,   0), (self._fLbm, r,   0), 
        (self._fLcw, t, 410), (self._fLcw, l,   0), (self._fLcw, r,   0), (self._fLcw, b, 110), 
                              (self._fLfc, l,   0), (self._fLfc, r,   0), (self._fLfc, b,   0), 
             ])

        pm.formLayout(self._fLct, e=True,
        af = [
        (self._btsj, t,  10), (self._btsj, l,   5), (self._btsj, r,   5),
        (self._btnl, t,  40), (self._btnl, l,   5), (self._btnl, r,   5),
        (self._btcc, t,  70), (self._btcc, l,   5), (self._btcc, r,   5),
        (self._btcn, t, 100), (self._btcn, l,   5), (self._btcn, r,   5),
        (self._spct, t, 145), (self._spct, l,   5), (self._spct, r,   5),
             ])

        pm.formLayout(self._fLca, e=True,
        af = [
        (self._tfmh, t,   9), (self._tfmh, l,   5), (self._tfmh, r,  40),
        (self._btmh, t,  10),                       (self._btmh, r,   5),
        (self._btca, t,  40), (self._btca, l,   5), (self._btca, r,   5),
        (self._spmh, t,  90), (self._spmh, l,   5), (self._spmh, r,   5),
             ])

        pm.formLayout(self._fLbm, e=True,
        af = [
        (self._txbn, t,  19), (self._txbn, l,   5), 
        (self._tfbn, t,  19), (self._tfbn, l,  50), (self._tfbn, r,  40),
        (self._btbn, t,  20),                       (self._btbn, r,   5),
        (self._txba, t,  50), (self._txba, l,   5), 
        (self._tfba, t,  49), (self._tfba, l,  50), (self._tfba, r,  40),
        (self._btba, t,  50),                       (self._btba, r,   5),
        (self._txbb, t,  80), (self._txbb, l,   5), 
        (self._tfbb, t,  79), (self._tfbb, l,  50), (self._tfbb, r,  40),
        (self._btbb, t,  80),                       (self._btbb, r,   5),
        (self._btbd, t, 110), (self._btbd, l,   5), (self._btbd, r,   5),
        (self._spca, t, 155), (self._spca, l,   5), (self._spca, r,   5),
             ])

        pm.formLayout(self._fLcw, h=60, e=True,
        af = [
        (self._txol, t,  10), (self._txol, l,   5), 
        (self._txil, t,  35), (self._txil, l,   5), 
        (self._txob, t,  10), (self._txob, l,  85), (self._txob, r,   5),
        (self._txif, t,  35), (self._txif, l,  85), (self._txif, r,   5),
        (self._tsif, t,  60), (self._tsif, l,   5), (self._tsif, r,  80), (self._tsif, b,  20),
        (self._btcp, t,  60),                       (self._btcp, r,   5),
        (self._btpa, t,  90),                       (self._btpa, r,   5),
        (self._txst, t, 120),                       (self._txst, r,   5),
                              (self._spcp, l,   5), (self._spcp, r,   5), (self._spcp, b,   5),
             ])

        pm.formLayout(self._fLfc, e=True,
        af = [
        (self._btf1, t,  10), (self._btf1, l,   5), 
        (self._btf2, t,  10),                       (self._btf2, r,   5), 
        (self._btf3, t,  40), (self._btf3, l,   5), 
        (self._btf4, t,  40),                       (self._btf4, r,   5), 
        (self._btf5, t,  70), (self._btf5, l,   5), 
        (self._btf6, t,  70),                       (self._btf6, r,   5), 
        (self._spfc, t, 110), (self._spfc, l,   5), (self._spfc, r,   5),
             ],
        ap = [
        (self._btf1, r, 2, 50), (self._btf2, l, 3, 50),
        (self._btf3, r, 2, 50), (self._btf4, l, 3, 50),
        (self._btf5, r, 2, 50), (self._btf6, l, 3, 50),
             ])


        window.show()


        #-- init command -------------------------------------------------------
        sj = pm.scriptJob(e=['SelectionChanged', pm.Callback(self._appendInf)], 
                          pro=True, cu=True, p=self.windowName)

        self._appendInf()
        

        pm.window(self.windowName, e=True,
                  w = self.windowSize[0], 
                  h = self.windowSize[1])


def showUI():
    testIns = smearSupportUI()
    testIns.main()

