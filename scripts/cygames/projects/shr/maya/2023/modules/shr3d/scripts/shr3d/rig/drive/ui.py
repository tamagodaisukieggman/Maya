# -*- coding: utf-8 -*-
from __future__ import absolute_import

#----- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import json


#-- import bootstrap
from . import bootstrap as mbc
#import bootstrap.core as mbc
from . import core as dvc


import importlib
importlib.reload(mbc)
importlib.reload(dvc)


class driveUI(object):
    def __init__(self):
        self.__ver__     = '0.0.4'
        self.windowName  = 'drive'
        self.windowTitle = 'Drive v{0}'.format(self.__ver__)
        self.windowSize  = [340, 400]
        self.dockName    = 'driveDock'
        self._maya_url   = r'https://help.autodesk.com/view/MAYAUL/2022/JPN/'
        self._help_url   = r'https://help.autodesk.com/view/MAYAUL/2022/JPN/'
        #--- current script path -----------------------------------------------
        self._dir = os.path.dirname(os.path.abspath(__file__))
        #self._mbc = bootstrap.__path__[0].replace('\\', '/') #-- bootstrap path
        #-- image path ---------------------------------------------------------
        self._ico = os.path.join(self._dir, r'_data/_icon').replace('\\', '/')
        #self._bic = os.path.join(self._mbc, r'_icon').replace('\\', '/')
        #-- color --------------------------------------------------------------
        self.btnBgc = (0.37, 0.37, 0.37)
        self.frmBgc = (0.11, 0.11, 0.11)
        self.fomBgc = (0.25, 0.25, 0.25)
        self.txfBgc = (0.15, 0.15, 0.15)
        #-- initial variables --------------------------------------------------
        self.partList = ['Twist', 'Middle', 'Front', 'Back', 'Side']
        self.roList   = ['xyz','yzx','zxy','xzy','yxz','zyx']
        self.axList   = ['X','Y','Z','-X','-Y','-Z']


    #---------------------------------------------------------------------------
    #-- initial funsionts ------------------------------------------------------
    def checkWindowOverlap(self):
        if pm.window(self.windowName, ex=True):
            pm.deleteUI(self.windowName)
        if pm.dockControl(self.dockName, ex=True):
            pm.deleteUI(self.dockName)

    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)


    #---------------------------------------------------------------------------
    #--- functions -------------------------------------------------------------
    def check(self, *args):
        print (True)


    def createDriveWld(self, suf='wld', *args):
        tgt = pm.selected()
        if tgt:
            mbc.wldMatrix(tgt, suf)


    def createCustomWld(self, *args):
        suf = pm.textField(self.tfCm, tx=True, q=True)
        tgt = pm.selected()
        if tgt:
            mbc.wldMatrix(tgt, suf)


    #-- Copy Rotate
    def createCopyRotateDrv(self, *args):
        tgt  = pm.textField(self.tfCr, tx=True, q=True)
        part = pm.textField(self.tfCp, tx=True, q=True)
        CrRo = self.roList.index(pm.optionMenu(self.omCax, v=True, q=True))
        dvc.createCopyRotate(tgt, part, CrRo, suf='roll')

        
    #-- Bend Roll
    def createBendRollDrv(self, *args):
        tgt  = pm.textField(self.tfBj, tx=True, q=True)
        aim  = pm.textField(self.tfAj, tx=True, q=True)
        part = pm.textField(self.tfBp, tx=True, q=True)
        brAx = self.axList.index(pm.optionMenu(self.omBax, v=True, q=True))
        brUp = self.axList.index(pm.optionMenu(self.omBup, v=True, q=True))
        dvc.createBendRoll(tgt, aim, part, brAx, brUp, suf=['bend', 'upv', 'roll'])


    #-- YawPitchRoll
    def createYawPitchRollDrv(self, *args):
        tgt  = pm.textField(self.tfYp, tx=True, q=True)
        part = pm.textField(self.tfYt, tx=True, q=True)
        YpRo  = self.roList.index(pm.optionMenu(self.omYax, v=True, q=True))
        dvc.createYawPitchRoll(tgt, part, YpRo, suf=['yaw', 'pitch', 'roll'])


    #-- Duplicate
    def duplicateReplace(self, *args):
        s = pm.textField(self.tfDpL, tx=True, q=True)
        r = pm.textField(self.tfDpR, tx=True, q=True)
        v = pm.checkBox(self.cbDpo, v=True, q=True)
        dvc.duplicateReplaceName(s, r, v)


    def switchSelect(self, *args):
        s = pm.textField(self.tfSsL, tx=True, q=True)
        r = pm.textField(self.tfSsR, tx=True, q=True)
        dvc.switchSelection(s, r)


    #-- Hierarchy
    def createNodeAbove(self, *args):
        typ = pm.textField(self.tfANt, tx=True, q=True)
        suf = pm.textField(self.tfASf, tx=True, q=True)
        dvc.createNodeAbove(typ, suf)


    def createNodeBelow(self, *args):
        typ = pm.textField(self.tfBNt, tx=True, q=True)
        suf = pm.textField(self.tfBSf, tx=True, q=True)
        dvc.createNodeBelow(typ, suf)


    def chainParent(self, rev=False, *args):
        dvc.chainParent(rev=rev)


    def oneByOneParent(self, *args):
        dvc.oneByOneParent()


    def arrayParent(self, *args):
        dvc.arrayParent()


    def composeRotate(self, *args):
        t = pm.radioButtonGrp(self.rbMro, sl=True, q=True)
        lsObj = pm.selected(typ='joint')

        if t == 1:
            dvc.composeRotate(lsObj)
        elif t == 2:
            dvc.composeJointOrient(lsObj)

    #---------------------------------------------------------------------------
    #--- edit UI ---------------------------------------------------------------
    def expandAll(self, v=True, *args):
        fList = [self.frLWd, self.frLCd, self.frLDn, 
                 self.frLCn, self.frLDp, self.frLHe, self.frLJm]
        for i in fList:
            pm.frameLayout(i, cl=v, e=True) #-- close


    def toggleFrame(self, frL, *args):
        fList = [self.frLWd, self.frLCd, self.frLDn, 
                 self.frLCn, self.frLDp, self.frLHe, self.frLJm]
        fList.remove(frL)
        to = pm.menuItem(self.mitgo, cb=True, q=True)
        if to:
            for i in fList:
                pm.frameLayout(i, cl=True, e=True) #-- close


    def columnSize(self, v=1, *args):
        fList = [self.frLWd, self.frLCd, self.frLDn, 
                 self.frLCn, self.frLDp, self.frLHe, self.frLJm]
        clv = []
        for i in fList:
            clv.append(pm.frameLayout(i, cl=True, q=True))
        #-- relaod UI
        pm.deleteUI(self.rcL, lay=True)
        self.contents(v)
        pm.formLayout(self.fmL, w=340+(330*(v-1)), e=True)
        pm.scrollLayout(self.scL, w=(335*v)+(5*(v-1)), e=True)
        pm.window(self.windowName, e=True,
                  w = self.windowSize[0], 
                  h = self.windowSize[1])

        fList = [self.frLWd, self.frLCd, self.frLDn, 
                 self.frLCn, self.frLDp, self.frLHe, self.frLJm]
        for i, cv in zip(fList, clv):
            pm.frameLayout(i, cl=cv, e=True)

        #-- toggle check
        if v == 1:
            pm.menuItem(self.mitgo, en=True, e=True)
        else:
            pm.menuItem(self.mitgo, en=False, cb=False, e=True)


    def resizeWindow(self, *args):
        pass
        #print(True)


    def cllapseFrame(self, *args):
        pass
        #-- window size
        #pm.window(self.windowName, h=100, e=True)


    def addPartMenu(self, tf, *args):
        pm.popupMenu(b=1)
        for i, part in enumerate(self.partList):
            pm.menuItem(l=part, c=pm.Callback(self.addPartText, tf, part))


    def addPartText(self, tf, part, *args):
        org = pm.textField(tf, tx=True, q=True)
        res = f'{org}{part}'
        pm.textField(tf, tx=res, e=True)


    def getObjectName(self, tf, ptf, typ='joint', *args):
        if typ:
            tgt = [i.name() for i in pm.selected(typ=typ)]
        else:
            tgt = [i.name() for i in pm.selected()]
        if tgt:
            pm.textField(tf, tx=tgt[0], e=True)
            if ptf:
                pm.textField(ptf, tx=dvc.getPartName(tgt[0]), e=True)


    def setAxisOption(self, opList=[], *args):
        for i in opList:
            pm.menuItem(l=i)


    def clearTextField(self, tfL=[], *args):
        for tf in tfL:
            pm.textField(tf, tx='', e=True)


    def toggleDrivenType(self, *args):
        t = pm.radioButtonGrp(self.rbDvn, sl=True, q=True) - 1
        v = [(1,1,1,1,1,0,0,0,0,0,0), 
             (1,1,1,1,1,1,1,1,1,1,1), 
             (0,0,0,1,1,0,0,0,0,0,0)]

        pm.textField(self.tfDvJ, en=v[t][0], e=True)
        pm.iconTextButton(self.ibGDv, en=v[t][1], e=True)
        pm.iconTextButton(self.ibCDv, en=v[t][2], e=True)

        pm.textField(self.tfDvp,      en=v[t][3], e=True)
        pm.iconTextButton(self.ibDvp, en=v[t][4], e=True)

        pm.textField(self.tfStJ,      en=v[t][5], e=True)
        pm.iconTextButton(self.ibGSt, en=v[t][6], e=True)

        pm.textField(self.tfEdJ,      en=v[t][7], e=True)
        pm.iconTextButton(self.ibGEd, en=v[t][8], e=True)
        pm.iconTextButton(self.ibCEd, en=v[t][9], e=True)
        pm.intSliderGrp(self.isMDv,   en=v[t][10], e=True)

        if t == 2:
            pm.textField(self.tfDvp, tx='{selected}', e=True)


    def createDrivenJoint(self, *args):
        t = pm.radioButtonGrp(self.rbDvn, sl=True, q=True)
        base  = pm.textField(self.tfDvJ, tx=True, q=True)
        part  = pm.textField(self.tfDvp, tx=True, q=True)
        start = pm.textField(self.tfStJ, tx=True, q=True)
        end   = pm.textField(self.tfEdJ, tx=True, q=True)
        size  = pm.intSliderGrp(self.isMDv, v=True, q=True)

        if t == 1:
            dvc.createSingleDrivenJoint(base, part)
        elif t == 2:
            dvc.createSerialDrivenJoint(base, part, start, end, size)
        elif t == 3:
            dvc.createSelectDrivenJoint(part)


    def setDrivenJointAttr(self, *args):
        for i in pm.selected():
            dvc.setDrivenJointAttr(i)


    #-- Duplicate and Hierarchy
    def nodeListPopup(self, ui, *args):
        nodeTyp = ['transform', 'joint', 'locator']

        pm.popupMenu(b=0)
        pm.menuItem(l='Clear', c=pm.Callback(self.setText, ui, ''))
        pm.menuItem(d=True)
        for i in nodeTyp:
            pm.menuItem(l=i, c=pm.Callback(self.setText, ui, i))


    def suffixListPopup(self, ui, *args):
        sufList = ['_jnt', '_drv', '_sim', '_fce', '_mtp', '_ax', '_grp', 
                   '_mtp', '_end', '_pos', '_cnst', '_ctrl', '_old']

        pm.popupMenu(b=0)
        pm.menuItem(l='Clear', c=pm.Callback(self.setText, ui, ''))
        pm.menuItem(d=True)
        for i in sufList:
            pm.menuItem(l=i, c=pm.Callback(self.setText, ui, i))


    def selectNodePopup(self, ui, *args):
        pm.popupMenu(b=0)
        pm.menuItem(l='Clear', c=pm.Callback(self.setText, ui, ''))
        pm.menuItem(d=True)
        pm.menuItem(l='Get First', c=pm.Callback(self.getSelectNodeName, ui))
        pm.menuItem(l='Get Last', c=pm.Callback(self.getSelectNodeName, ui))


    def setText(self, ui, txt='', *args):
        pm.textField(ui, tx=txt, e=True)


    def getSelectNodeName(self, ui, v=0, *args):
        selObj = pm.selected()
        txt = ''
        if selObj:
            if v == 0: txt = selObj[0].name()
            if v == 1: txt = selObj[-1].name()
        pm.textField(ui, tx=txt, e=True)


    #---------------------------------------------------------------------------
    #--- Contents UI -----------------------------------------------------------
    def contents(self, columnSize=1, *args):
        self.rcL = pm.rowColumnLayout(nc=columnSize, p=self.scL)

        #-- Base Layout
        self.frLWd = pm.frameLayout(l='World Matrix Nodes')

        #-- World Matrix -------------------------------------------------------
        self.fmLWd = pm.formLayout(nd=100)
        self.ibWr = pm.iconTextButton(l='Create for rig')
        self.ibWd = pm.iconTextButton(l='Create for drive')
        self.tfCm = pm.textField(pht='Suffix...')
        self.ibCm = pm.iconTextButton(l='Create')
        self.spWd = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.fmLWd
        pm.setParent('..') #-- end of self.frLWd


        #-- Driven Joint -------------------------------------------------------
        self.frLDn = pm.frameLayout(l='Driven Joint')
        self.fmLDn = pm.formLayout(nd=100)
        self.rbDvn = pm.radioButtonGrp(l='type :   ', 
                     la3=['Single', 'Multi', 'Select'], nrb=3)

        self.tfDvJ = pm.textField(pht='base joint...')
        self.ibGDv = pm.iconTextButton(l='Get')
        self.ibCDv = pm.iconTextButton(l='Clear')

        self.tfDvp = pm.textField(pht='Parts Name...')
        self.ibDvp = pm.iconTextButton(l='Add Text')
        self.addPartMenu(self.tfDvp)

        self.tfStJ = pm.textField(pht='start...')
        self.ibGSt = pm.iconTextButton(l='Get')

        self.tfEdJ = pm.textField(pht='end...')
        self.ibGEd = pm.iconTextButton(l='Get')
        self.ibCEd = pm.iconTextButton(l='Clear')

        self.isMDv = pm.intSliderGrp(l='Size :   ', f=True)
        self.ibDvn = pm.iconTextButton(l='Create Driven Joint')
        self.ibDjA = pm.iconTextButton(l='Set Driven Joint Attributes')
        self.spDn  = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.fmLDn
        pm.setParent('..') #-- end of self.frLDn


        #-- Create Drive -------------------------------------------------------
        self.frLCd = pm.frameLayout(l='Drive Hierarchy')
        self.clDr = pm.columnLayout(adj=True)

        #-- Copy Rotate
        self.flCr = pm.formLayout(nd=100)
        self.ilCr = pm.iconTextStaticLabel(l='Copy Rotate')
        self.tfCr = pm.textField(pht='target joint...')
        self.ibGt = pm.iconTextButton(l='Get')
        self.ibCl = pm.iconTextButton(l='Clear')
        #-- options
        self.tfCp = pm.textField(pht='Parts Name...')
        self.ibCp = pm.iconTextButton(l='Add Text')
        self.addPartMenu(self.tfCp)
        self.omCax = pm.optionMenu(l=' Order :')
        self.setAxisOption(self.roList)
        self.ibCr = pm.iconTextButton(l='Create Drive')
        self.spCr = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.flCr
        
        #-- Bend & Roll
        self.flBr = pm.formLayout(nd=100)
        self.ilBr = pm.iconTextStaticLabel(l='Bend Roll')
        self.tfBj = pm.textField(pht='target joint...')
        self.ibGb = pm.iconTextButton(l='Get')
        self.ibCb = pm.iconTextButton(l='Clear')
        self.tfAj = pm.textField(pht='aim joint...')
        self.ibGa = pm.iconTextButton(l='Get')
        self.ibCa = pm.iconTextButton(l='Clear')
        self.tfBp = pm.textField(pht='Parts Name...')
        self.ibBp = pm.iconTextButton(l='Add Text')
        self.addPartMenu(self.tfBp)
        self.omBax = pm.optionMenu(l=' Axis :')
        self.setAxisOption(self.axList)
        self.omBup = pm.optionMenu(l='Up :')
        self.setAxisOption(self.axList)
        self.ibBr = pm.iconTextButton(l='Create Drive')
        self.spBr = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.flBr

        #-- Yaw Ptich Roll
        self.flYp = pm.formLayout(nd=100)
        self.ilYp = pm.iconTextStaticLabel(l='Yaw Ptich Roll')
        self.tfYp = pm.textField(pht='target joint...')
        self.ibGy = pm.iconTextButton(l='Get')
        self.ibCy = pm.iconTextButton(l='Clear')
        self.tfYt = pm.textField(pht='Parts Name...')
        self.ibYt = pm.iconTextButton(l='Add Text')
        self.addPartMenu(self.tfYt)
        self.omYax = pm.optionMenu(l=' Order :')
        self.setAxisOption(self.roList)
        self.ibYp = pm.iconTextButton(l='Create Drive')
        self.spYp = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.flYp
        pm.setParent('..') #-- end of self.clDr
        pm.setParent('..') #-- end of self.frLCd


        #-- Connect to Driven --------------------------------------------------
        self.frLCn = pm.frameLayout(l='Connect to Driven')
        self.fmLCn = pm.formLayout(nd=100)
        self.ibExp = pm.iconTextButton(l='Expression Editor')
        self.ibSdk = pm.iconTextButton(l='Set Driven Key')
        self.spCn  = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of connection
        pm.setParent('..') #-- end of self.frLDn


        #-- Duplicate ----------------------------------------------------------
        self.frLDp = pm.frameLayout(l='Duplicate')
        self.fmLDp = pm.formLayout(nd=100)

        self.tfDpL = pm.textField(tx='L_')
        self.selectNodePopup(self.tfDpL)
        self.tfDpR = pm.textField(tx='R_')
        self.selectNodePopup(self.tfDpR)
        self.cbDpo = pm.checkBox(l='Selected Only')
        self.ibDpl = pm.iconTextButton(l='Duplicate')

        self.tfSsL = pm.textField(tx='L_')
        self.selectNodePopup(self.tfSsL)
        self.tfSsR = pm.textField(tx='R_')
        self.selectNodePopup(self.tfSsR)
        self.ibSws = pm.iconTextButton(l='Switch Select')

        self.spDup = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.fmLDp
        pm.setParent('..') #-- end of self.frLDp


        #-- Hierarchy ----------------------------------------------------------
        self.frLHe = pm.frameLayout(l='Hierarchy')
        self.fmLHe = pm.formLayout(nd=100)

        self.tfANt = pm.textField(tx='transform')
        self.nodeListPopup(self.tfANt) #-- popup menu
        self.tfASf = pm.textField(tx='_ax')
        self.suffixListPopup(self.tfASf)
        self.ibAbv = pm.iconTextButton(l='Above')

        self.tfBNt = pm.textField(tx='transform')
        self.nodeListPopup(self.tfBNt) #-- popup menu
        self.tfBSf = pm.textField(tx='_null')
        self.suffixListPopup(self.tfBSf)
        self.ibBlw = pm.iconTextButton(l='Below')

        self.ibChP = pm.iconTextButton(l='Chain')
        self.ibRvP = pm.iconTextButton(l='Reverse')
        self.ibObP = pm.iconTextButton(l='One by One')
        self.ibAry = pm.iconTextButton(l='Array')

        self.spHie = pm.separator(st='in', h=2)

        pm.setParent('..') #-- end of self.fmLHe
        pm.setParent('..') #-- end of self.frLHe

        #-- Joint Management ---------------------------------------------------
        self.frLJm = pm.frameLayout(l='Joint Management')
        self.fmLJm = pm.formLayout(nd=100)
        self.rbMro = pm.radioButtonGrp(l='Merge to :   ', 
                     la2=['Rotation', 'Joint Orient'], nrb=2)
        self.ibMro = pm.iconTextButton(l='Merge')
        self.spMro = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of connection
        pm.setParent('..') #-- end of self.frLDn


        pm.setParent('..') #-- end of self.rcL
        

        #-----------------------------------------------------------------------
        #--- Edit UI elements --------------------------------------------------
        io, to, = ['iconOnly', 'textOnly']
        ith, itv = ['iconAndTextHorizontal', 'iconAndTextVertical']

        pm.menuItem(self.miExa, c=pm.Callback(self.expandAll, False), e=True)
        pm.menuItem(self.miCla, c=pm.Callback(self.expandAll, True), e=True)

        pm.menuItem(self.miCl1, c=pm.Callback(self.columnSize, 1), e=True)
        pm.menuItem(self.miCl2, c=pm.Callback(self.columnSize, 2), e=True)
        pm.menuItem(self.miCl3, c=pm.Callback(self.columnSize, 3), e=True)

        #-- World matrix -------------------------------------------------------
        pm.iconTextButton(self.ibWr, st=ith, w=160, h=30, mw=7, mh=2,  
            i=f'{self._ico}/createWldRig.png', bgc=self.btnBgc, 
            c=pm.Callback(self.createDriveWld, 'wld'), e=True)

        pm.iconTextButton(self.ibWd, st=ith, w=160, h=30, mw=7, mh=2,  
            i=f'{self._ico}/createWld.png', bgc=self.btnBgc, 
            c=pm.Callback(self.createDriveWld, 'dWld'), e=True)

        pm.textField(self.tfCm, tx='', w=20, h=30, e=True)
        pm.iconTextButton(self.ibCm, st=ith, w=100, h=28, mw=7, mh=2,  
            i=f'{self._ico}/createWld.png', bgc=self.btnBgc, 
            c=pm.Callback(self.createCustomWld), e=True)


        #-- Driven Joint -------------------------------------------------------
        pm.radioButtonGrp(self.rbDvn, cw4=(40, 60, 60, 60), sl=1,
            cc=pm.Callback(self.toggleDrivenType), e=True)

        pm.textField(self.tfDvJ, tx='', h=24, e=True)
        pm.iconTextButton(self.ibGDv, st=io, w=30, h=22, mw=7, mh=2, e=True,
            i=f'{self._ico}/get.png', bgc=self.btnBgc, 
            c=pm.Callback(self.getObjectName, self.tfDvJ, self.tfDvp, 'joint'))
        pm.iconTextButton(self.ibCDv, st=io, w=30, h=22, mw=7, mh=2, e=True,
            i=f'{self._ico}/clear.png', bgc=self.btnBgc, 
            c=pm.Callback(self.clearTextField, [self.tfDvJ, self.tfDvp]))

        pm.textField(self.tfDvp, tx='', h=24, e=True)
        pm.iconTextButton(self.ibDvp, st=to, w=65, h=22, mw=0, mh=0,  
            bgc=self.btnBgc, e=True)

        pm.textField(self.tfStJ, tx='', h=24, e=True)
        pm.iconTextButton(self.ibGSt, st=io, w=30, h=22, mw=7, mh=2, e=True,
            i=f'{self._ico}/get.png', bgc=self.btnBgc, 
            c=pm.Callback(self.getObjectName, self.tfStJ, None, 'transform'))

        pm.textField(self.tfEdJ, tx='', h=24, e=True)
        pm.iconTextButton(self.ibGEd, st=io, w=30, h=22, mw=7, mh=2, e=True,
            i=f'{self._ico}/get.png', bgc=self.btnBgc, 
            c=pm.Callback(self.getObjectName, self.tfEdJ, None, 'transform'))
        pm.iconTextButton(self.ibCEd, st=io, w=30, h=22, mw=7, mh=2,  
            i=f'{self._ico}/clear.png', bgc=self.btnBgc, 
            c=pm.Callback(self.clearTextField, [self.tfStJ, self.tfEdJ]), e=True)

        pm.intSliderGrp(self.isMDv, min=1, max=10, fmn=1, fmx=10, v=3,
            cw3=(40, 60, 60), e=True)

        pm.iconTextButton(self.ibDvn, st=ith, w=65, h=30, mw=10, mh=2, 
            i=f'{self._ico}/driven.png', bgc=self.btnBgc, 
            c=pm.Callback(self.createDrivenJoint), e=True)

        pm.iconTextButton(self.ibDjA, st=ith, w=65, h=30, mw=10, mh=2, 
            i='{0}/setDrv.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.setDrivenJointAttr), e=True)


        #-- Create Drive -------------------------------------------------------
        #-- copy rotate
        pm.iconTextStaticLabel(self.ilCr, st=ith, mw=5, 
            i1=f'{self._ico}/copyRotate.png', e=True)
        pm.textField(self.tfCr, tx='', h=24, e=True)
        pm.iconTextButton(self.ibGt, st=io, w=30, h=22, mw=7, mh=2, e=True,
            i=f'{self._ico}/get.png', bgc=self.btnBgc, 
            c=pm.Callback(self.getObjectName, self.tfCr, self.tfCp, 'joint'))
        pm.iconTextButton(self.ibCl, st=io, w=30, h=22, mw=7, mh=2, e=True,
            i=f'{self._ico}/clear.png', bgc=self.btnBgc, 
            c=pm.Callback(self.clearTextField, [self.tfCr, self.tfCp]))
        pm.textField(self.tfCp, tx='', h=24, e=True)
        pm.iconTextButton(self.ibCp, st=to, w=65, h=22, mw=0, mh=0,  
            bgc=self.btnBgc, e=True)

        pm.optionMenu(self.omCax, w=100, h=24, e=True)
        pm.iconTextButton(self.ibCr, st=ith, h=30, mw=10, mh=2,  
            i=f'{self._ico}/createDrive.png', bgc=self.btnBgc, 
            c=pm.Callback(self.createCopyRotateDrv), e=True)


        #-- bend roll
        pm.iconTextStaticLabel(self.ilBr, st=ith, mw=5, 
            i1=f'{self._ico}/bendRoll.png', e=True)
        pm.textField(self.tfBj, tx='', h=24, e=True)
        pm.iconTextButton(self.ibGb, st=io, w=30, h=22, mw=7, mh=2, e=True,  
            i=f'{self._ico}/get.png', bgc=self.btnBgc, 
            c=pm.Callback(self.getObjectName, self.tfBj, self.tfBp, 'joint'))
        pm.iconTextButton(self.ibCb, st=io, w=30, h=22, mw=7, mh=2,  
            i=f'{self._ico}/clear.png', bgc=self.btnBgc, 
            c=pm.Callback(self.clearTextField, [self.tfBj, self.tfBp]), e=True)

        pm.textField(self.tfAj, tx='', h=24, e=True)
        pm.iconTextButton(self.ibGa, st=io, w=30, h=22, mw=7, mh=2, e=True,
            i=f'{self._ico}/get.png', bgc=self.btnBgc, 
            c=pm.Callback(self.getObjectName, self.tfAj, None, 'transform'))
        pm.iconTextButton(self.ibCa, st=io, w=30, h=22, mw=7, mh=2,  
            i=f'{self._ico}/clear.png', bgc=self.btnBgc, 
            c=pm.Callback(self.clearTextField, [self.tfAj]), e=True)

        pm.textField(self.tfBp, tx='', h=24, e=True)
        pm.iconTextButton(self.ibBp, st=to, w=65, h=22, mw=0, mh=0,  
            bgc=self.btnBgc, e=True)

        pm.optionMenu(self.omBax, w=85, h=24, e=True)
        pm.optionMenu(self.omBup, w=75, h=24, e=True)
        pm.iconTextButton(self.ibBr, st=ith, h=30, mw=10, mh=2,  
            i=f'{self._ico}/createDrive.png', bgc=self.btnBgc, 
            c=pm.Callback(self.createBendRollDrv), e=True)


        #-- yaw pitch roll
        pm.iconTextStaticLabel(self.ilYp, st=ith, mw=5, 
            i1=f'{self._ico}/yawPitchRoll.png', e=True)
        pm.textField(self.tfYp, tx='', h=24, e=True)
        pm.iconTextButton(self.ibGy, st=io, w=30, h=24, mw=7, mh=2, e=True,
            i=f'{self._ico}/get.png', bgc=self.btnBgc, 
            c=pm.Callback(self.getObjectName, self.tfYp, self.tfYt, 'joint'))
        pm.iconTextButton(self.ibCy, st=io, w=30, h=24, mw=7, mh=2, e=True,
           i=f'{self._ico}/clear.png', bgc=self.btnBgc, 
            c=pm.Callback(self.clearTextField, [self.tfYp, self.tfYt]))

        pm.textField(self.tfYt, tx='', h=24, e=True)
        pm.iconTextButton(self.ibYt, st=to, w=65, h=22, mw=0, mh=0,  
            bgc=self.btnBgc, e=True)

        pm.optionMenu(self.omYax, w=100, h=24, e=True)
        pm.iconTextButton(self.ibYp, st=ith, h=30, mw=10, mh=2,  
            i=f'{self._ico}/createDrive.png', bgc=self.btnBgc, 
            c=pm.Callback(self.createYawPitchRollDrv), e=True)


        #-- connection ---------------------------------------------------------
        pm.iconTextButton(self.ibExp, st=ith, w=65, h=30, mw=10, mh=2, 
            i=f'{self._ico}/expression.png', bgc=self.btnBgc, 
            c='maya.mel.eval("ExpressionEditor;")', e=True)
        pm.iconTextButton(self.ibSdk, st=ith, w=65, h=30, mw=10, mh=2, 
            i=f'{self._ico}/drivenkey.png', bgc=self.btnBgc, 
            c='maya.mel.eval("setDrivenKeyWindow "" {};")', e=True)


        #-- Duplicate ----------------------------------------------------------
        pm.textField(self.tfDpL, tx='L_', h=32, e=True)
        pm.textField(self.tfDpR, tx='R_', h=32, e=True)
        pm.iconTextButton(self.ibDpl, st=ith, w=30, h=30, mw=7, mh=2, e=True,
            i=f'{self._ico}/dup_LR.png', bgc=self.btnBgc, 
            c=pm.Callback(self.duplicateReplace))

        pm.textField(self.tfSsL, tx='L_', h=32, e=True)
        pm.textField(self.tfSsR, tx='R_', h=32, e=True)
        pm.iconTextButton(self.ibSws, st=ith, w=30, h=30, mw=7, mh=2, e=True,
            i=f'{self._ico}/sel_LR.png', bgc=self.btnBgc, 
            c=pm.Callback(self.switchSelect))


        #-- Hierarchy ----------------------------------------------------------
        pm.textField(self.tfANt, tx='transform', h=32, w=30, e=True)
        pm.textField(self.tfASf, tx='_ax',       h=32, w=30, e=True)
        pm.iconTextButton(self.ibAbv, st=ith, w=30, h=30, mw=7, mh=2, e=True,
            i=f'{self._ico}/dag_above.png', bgc=self.btnBgc, 
            c=pm.Callback(self.createNodeAbove))

        pm.textField(self.tfBNt, tx='transform', h=32, w=30, e=True)
        pm.textField(self.tfBSf, tx='_null',     h=32, w=30, e=True)
        pm.iconTextButton(self.ibBlw, st=ith, w=30, h=30, mw=7, mh=2, e=True,
            i=f'{self._ico}/dag_below.png', bgc=self.btnBgc, 
            c=pm.Callback(self.createNodeBelow))

        pm.iconTextButton(self.ibChP, st=ith, w=30, h=30, mw=7, mh=2, e=True,
            i=f'{self._ico}/dag_chain.png', bgc=self.btnBgc, 
            c=pm.Callback(self.chainParent, False))

        pm.iconTextButton(self.ibRvP, st=ith, w=30, h=30, mw=7, mh=2, e=True,
            i=f'{self._ico}/dag_reverse.png', bgc=self.btnBgc, 
            c=pm.Callback(self.chainParent, True))

        pm.iconTextButton(self.ibObP, st=ith, w=30, h=30, mw=7, mh=2, e=True,
            i=f'{self._ico}/oneByOne.png', bgc=self.btnBgc, 
            c=pm.Callback(self.oneByOneParent))

        pm.iconTextButton(self.ibAry, st=ith, w=30, h=30, mw=7, mh=2, e=True,
            i=f'{self._ico}/array.png', bgc=self.btnBgc, 
            c=pm.Callback(self.arrayParent))


        #-- Joint Management ---------------------------------------------------
        pm.radioButtonGrp(self.rbMro, cw3=(80, 100, 100), sl=1, e=True)

        pm.iconTextButton(self.ibMro, st=ith, w=30, h=30, mw=7, mh=2, e=True,
            i='{0}/setDrv.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.composeRotate))



        #-----------------------------------------------------------------------
        #--- Edit UI Layout ----------------------------------------------------
        pm.rowColumnLayout(self.rcL, cw=[(1,320), (2,320), (3,320)], e=True,
            cs=[(2,5), (3,5)])

        t, b, l, r = ['top', 'bottom', 'left', 'right']

        #-- base
        pm.formLayout(self.fmL, e=True, af=[
        (self.scL, t, 0), (self.scL, l, 0), (self.scL, r, 0), (self.scL, b, 0),
        ])

        #-- world matrix
        pm.formLayout(self.fmLWd, e=True, af=[
        (self.ibWr, t,  10), (self.ibWr,  l, 10), (self.ibWr,  r,  10), 
        (self.ibWd, t,  45), (self.ibWd,  l, 10), (self.ibWd,  r,  10),  
        (self.tfCm, t,  80), (self.tfCm,  l, 10), (self.tfCm,  r, 115), 
        (self.ibCm, t,  81),                      (self.ibCm,  r,  10), 
        (self.spWd, t, 130), (self.spWd,  l,  0), (self.spWd,  r,   0),
        ])

        #-- Driven Joint 
        pm.formLayout(self.fmLDn, e=True, af=[
        (self.rbDvn, t,  10), (self.rbDvn, l,  10),  
        (self.tfDvJ, t,  40), (self.tfDvJ, l,  10), (self.tfDvJ, r,  80), 
        (self.ibGDv, t,  41),                       (self.ibGDv, r,  45), 
        (self.ibCDv, t,  41),                       (self.ibCDv, r,  10), 
        (self.tfDvp, t,  70), (self.tfDvp, l,  10), (self.tfDvp, r,  80),
        (self.ibDvp, t,  71),                       (self.ibDvp, r,  10), 
        (self.tfStJ, t, 100), (self.tfStJ, l,  10),  
        (self.ibGSt, t, 101),                        
        (self.tfEdJ, t, 100),                       (self.tfEdJ, r,  80), 
        (self.ibGEd, t, 101),                       (self.ibGEd, r,  45), 
        (self.ibCEd, t, 101),                       (self.ibCEd, r,  10), 
        (self.isMDv, t, 131), (self.isMDv, l,  10), (self.isMDv, r,  10), 
        (self.ibDvn, t, 160), (self.ibDvn, l,  10), (self.ibDvn, r,  10), 
        (self.ibDjA, t, 195), (self.ibDjA, l,  10), (self.ibDjA, r,  10),
        (self.spDn,  t, 245), (self.spDn,  l,   0), (self.spDn,  r,   0),
        ],
        ac=[
        (self.tfStJ, r, 5, self.ibGSt),
        (self.tfEdJ, r, 5, self.ibGEd),
        ],
        ap=[
        (self.ibGSt, r, 5, 47),
        (self.tfEdJ, l, 0, 47),
        ])

        #-- copy rotate
        pm.formLayout(self.flCr, e=True, af=[
        (self.ilCr, t,  10), (self.ilCr,  l, 10), (self.ilCr,  r, 10),
        (self.tfCr, t,  40), (self.tfCr,  l, 10), (self.tfCr,  r, 80), 
        (self.ibGt, t,  41),                      (self.ibGt,  r, 45), 
        (self.ibCl, t,  41),                      (self.ibCl,  r, 10), 
        (self.tfCp, t,  70), (self.tfCp,  l, 10), (self.tfCp,  r, 80),
        (self.ibCp, t,  71),                      (self.ibCp,  r, 10), 
        (self.omCax,t, 104), (self.omCax, l,  10),
        (self.ibCr, t, 100), (self.ibCr,  l, 120), (self.ibCr,  r, 10), 
        (self.spCr, t, 140), (self.spCr,  l,   0), (self.spCr,  r,  0), 
        ])

        #-- bend roll
        pm.formLayout(self.flBr, e=True, af=[
        (self.ilBr, t,  10), (self.ilBr,  l, 10), (self.ilBr,  r, 10),
        (self.tfBj, t,  40), (self.tfBj,  l, 10), (self.tfBj,  r, 80), 
        (self.ibGb, t,  41),                      (self.ibGb,  r, 45), 
        (self.ibCb, t,  41),                      (self.ibCb,  r, 10), 
        (self.tfAj, t,  70), (self.tfAj,  l, 10), (self.tfAj,  r, 80), 
        (self.ibGa, t,  71),                      (self.ibGa,  r, 45), 
        (self.ibCa, t,  71),                      (self.ibCa,  r, 10), 
        (self.tfBp, t, 100), (self.tfBp,  l, 10), (self.tfBp,  r, 80),
        (self.ibBp, t, 101),                      (self.ibBp,  r, 10), 
        (self.omBax,t, 134), (self.omBax, l,  10),
        (self.omBup,t, 134), (self.omBup, l, 105),
        (self.ibBr, t, 130), (self.ibBr,  l, 190), (self.ibBr,  r, 10), 
        (self.spBr, t, 170), (self.spBr,  l,   0), (self.spBr,  r,  0), 
        ])

        #-- yaw pitch roll
        pm.formLayout(self.flYp, e=True, af=[
        (self.ilYp, t,  10), (self.ilYp,  l, 10), (self.ilYp,  r, 10),
        (self.tfYp, t,  40), (self.tfYp,  l, 10), (self.tfYp,  r, 80), 
        (self.ibGy, t,  40),                      (self.ibGy,  r, 45), 
        (self.ibCy, t,  40),                      (self.ibCy,  r, 10), 
        (self.tfYt, t,  70), (self.tfYt,  l, 10), (self.tfYt,  r, 80),
        (self.ibYt, t,  71),                      (self.ibYt,  r, 10), 
        (self.omYax,t, 104), (self.omYax, l,  10),
        (self.ibYp, t, 100), (self.ibYp,  l, 120), (self.ibYp,  r, 10), 
        (self.spYp, t, 150), (self.spYp,  l,   0), (self.spYp,  r,  0), 
        ])

        #-- Connect
        pm.formLayout(self.fmLCn, e=True, af=[
        (self.ibExp, t,  10), (self.ibExp, l, 10), (self.ibExp, r,  10), 
        (self.ibSdk, t,  45), (self.ibSdk, l, 10), (self.ibSdk, r,  10),  
        (self.spCn,  t,  95), (self.spCn,  l,  0), (self.spCn,  r,   0),
        ])

        #-- Duplicate
        pm.formLayout(self.fmLDp, e=True, af=[
        (self.tfDpL, t,  10), (self.tfDpL, l,  10),
        (self.tfDpR, t,  10),
        (self.cbDpo, t,  18),
        (self.ibDpl, t,  45), (self.ibDpl, l,  10), (self.ibDpl, r, 10), 
        (self.tfSsL, t,  90), (self.tfSsL, l,  10),
        (self.tfSsR, t,  90),
        (self.ibSws, t,  91),                       (self.ibSws, r, 10), 
        (self.spDup, t, 135), (self.spDup, l,   0), (self.spDup, r,  0), 
        ],
        ap=[
        (self.tfDpL, r,  3, 30),
        (self.tfDpR, l,  0, 30), (self.tfDpR, r, 5, 60),
        (self.cbDpo, l, 10, 60), 
        (self.tfSsL, r,  3, 30),
        (self.tfSsR, l,  0, 30), (self.tfSsR, r, 5, 60),
        (self.ibSws, l,  0, 60), 
        ])

        #-- Hierarchy
        pm.formLayout(self.fmLHe, e=True, af=[
        (self.tfANt, t,  10), (self.tfANt, l,  10),
        (self.tfASf, t,  10),
        (self.ibAbv, t,  11),                       (self.ibAbv, r, 10), 
        (self.tfBNt, t,  45), (self.tfBNt, l,  10),
        (self.tfBSf, t,  45),
        (self.ibBlw, t,  46),                       (self.ibBlw, r, 10), 
        (self.ibChP, t,  90), (self.ibChP, l,  10),
        (self.ibRvP, t,  90),                       (self.ibRvP, r, 10),
        (self.ibObP, t, 125), (self.ibObP, l,  10),
        (self.ibAry, t, 125),                       (self.ibAry, r, 10),
        (self.spHie, t, 180), (self.spHie, l,   0), (self.spHie, r,  0), 
        ],
        ap=[
        (self.tfANt, r, 3, 40),
        (self.tfASf, l, 0, 40), (self.tfASf, r, 5, 65),
        (self.ibAbv, l, 0, 65), 
        (self.tfBNt, r, 3, 40),
        (self.tfBSf, l, 0, 40), (self.tfBSf, r, 5, 65),
        (self.ibBlw, l, 0, 65), 
        (self.ibChP, r, 5, 50),
        (self.ibRvP, l, 0, 50), 
        (self.ibObP, r, 5, 50),
        (self.ibAry, l, 0, 50), 
        ])


        #-- Joint Management
        pm.formLayout(self.fmLJm, e=True, af=[
        (self.rbMro, t,  10), (self.rbMro, l, 10), (self.rbMro, r,  10), 
        (self.ibMro, t,  45), (self.ibMro, l, 10), (self.ibMro, r,  10),  
        (self.spMro, t,  95), (self.spMro, l,  0), (self.spMro, r,   0),
        ])


        pm.frameLayout(self.frLWd, cll=True, cl=False, bgc=self.frmBgc, 
        ec=pm.Callback(self.toggleFrame, self.frLWd), 
        cc=pm.Callback(self.cllapseFrame), e=True)

        pm.frameLayout(self.frLCd, cll=True, cl=True, bgc=self.frmBgc, 
        ec=pm.Callback(self.toggleFrame, self.frLCd), 
        cc=pm.Callback(self.cllapseFrame), e=True)

        pm.frameLayout(self.frLDn, cll=True, cl=True, bgc=self.frmBgc, 
        ec=pm.Callback(self.toggleFrame, self.frLDn), 
        cc=pm.Callback(self.cllapseFrame), e=True)

        pm.frameLayout(self.frLCn, cll=True, cl=True, bgc=self.frmBgc, 
        ec=pm.Callback(self.toggleFrame, self.frLCn), 
        cc=pm.Callback(self.cllapseFrame), e=True)

        pm.frameLayout(self.frLDp, cll=True, cl=True, bgc=self.frmBgc, 
        ec=pm.Callback(self.toggleFrame, self.frLDp), 
        cc=pm.Callback(self.cllapseFrame), e=True)

        pm.frameLayout(self.frLHe, cll=True, cl=True, bgc=self.frmBgc, 
        ec=pm.Callback(self.toggleFrame, self.frLHe), 
        cc=pm.Callback(self.cllapseFrame), e=True)

        pm.frameLayout(self.frLJm, cll=True, cl=True, bgc=self.frmBgc, 
        ec=pm.Callback(self.toggleFrame, self.frLHe), 
        cc=pm.Callback(self.cllapseFrame), e=True)



    #---------------------------------------------------------------------------
    #--- main UI ---------------------------------------------------------------
    def main(self):
        self.checkWindowOverlap()
        window = pm.window(self.windowName, mb = True, dl='left', rtf=True,
                           t = self.windowTitle,
                           w = self.windowSize[0],
                           h = self.windowSize[1])

        #-----------------------------------------------------------------------
        #-- menu ---------------------------------------------------------------
        pm.menu(l='Help', hm=True)
        pm.menuItem(l='Maya 2022 HELP', c=self.show_mayaHelp)
        pm.menuItem(d=True)
        pm.menuItem(l='Tool HELP', c=self.show_toolHelp)

        pm.menu(l='Layout')
        self.miExa = pm.menuItem(l='Expand All')
        self.miCla = pm.menuItem(l='Collapse All')
        self.miDop = pm.menuItem(d=True, dl='Open')
        self.mitgo = pm.menuItem(l='Toggle', cb=False)
        self.miDop = pm.menuItem(d=True, dl='Column')
        self.mrbCl = pm.radioMenuItemCollection()
        self.miCl1 = pm.menuItem(l='1', rb=True)
        self.miCl2 = pm.menuItem(l='2', rb=False)
        self.miCl3 = pm.menuItem(l='3', rb=False)
        #-----------------------------------------------------------------------
        #-- layout -------------------------------------------------------------
        self.fmL = pm.formLayout(nd=100)
        self.scL = pm.scrollLayout()

        self.contents(columnSize=1)

        pm.setParent('..') #-- end of self.scL
        window.show()

        #-----------------------------------------------------------------------
        #-- edit ---------------------------------------------------------------
        pm.formLayout(self.fmL, w=340, e=True)
        pm.scrollLayout(self.scL, rc=pm.Callback(self.resizeWindow), w=330, e=True)

        #-- init command -------------------------------------------------------
        pm.window(self.windowName, e=True,
                  w = self.windowSize[0], 
                  h = self.windowSize[1])


        self.toggleDrivenType()

        #-- dock check
        pm.dockControl(self.dockName, a='left', con=self.windowName, 
                       aa=['left', 'right', 'bottom'], l='Main')


def showUI():
    testIns = driveUI()
    testIns.main()

