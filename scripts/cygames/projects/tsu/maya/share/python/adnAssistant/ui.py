# -*- coding: utf-8 -*-
from __future__ import absolute_import

#----- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import json

import tsubasa.maya.rig.assistdrive as assistdrive

from . import command
from . import adn
from . import setup


def importFile(d=r'', f='', ext='.mb'):
    path = r'{0}/{1}{2}'.format(d, f, ext)
    ns   = ''
    mc.file(path,
            i = True, 
          typ = 'mayaBinary',
           iv = True,
          mnc = False,
          rpr = f,
           op = 'v=0;',
           pr = True,
          ifr = False,
          itr = 'keep') 


class adnAssistantUI(object):
    def __init__(self):
        self.__ver__          = '1.1.0'
        self.windowManageName = 'adnAssistant'
        self.windowTitle      = 'ADN Assistant v{0}'.format(self.__ver__)
        self.windowSize       = [600, 700]
        self._mayaHelp_url    = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._toolHelp_url    = r'https://wisdom.cygames.jp/x/PTxWDQ'
        #--- current script path -----------------------------------------------
        self.__dir = os.path.dirname(os.path.abspath(__file__))
        #-- image path ---------------------------------------------------------
        self._idir = r'{0}/_data/_icon'.format(self.__dir)
        self._temp = r'{0}/_data/_assistdrive'.format(self.__dir)
        #-- color
        self.btnBgc = (0.37, 0.37, 0.37)
        #-- color
        self._an_ibt = u''
        #-- Assist drive type
        self._adnType = {'CopyRotate':'CR',
                         'AxisRoll':'AR',
                         'AxisRollBlend':'AB',
                         'AxisMove':'AM',
                         'RollMove':'RM',
                         'YawPitchRotate':'YP',
                         'RollScale':'RS'} 
        self._adnList = ['CopyRotate', 'AxisRoll', 'AxisRollBlend', 'AxisMove', 
                         'RollMove', 'YawPitchRotate', 'RollScale']
        self._side = {'Center':'', 'Left':'L_', 'Right':'R_', 'None':''}
        #-- clamp
        self.vClamp = lambda x: min(1, max(x, -1))
        self.oClamp = lambda x: min(180, max(x, -180))
        self.yClamp = lambda x: min(179, max(x, -179))


    def checkWindowOverlap(self):
        if pm.window(self.windowManageName, ex=True):
            pm.deleteUI(self.windowManageName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)


    #--- functions -------------------------------------------------------------
    def _createManipulator(self, *args):
        pm.mel.eval('AssistDriveManipulator -delete;')
        pm.mel.eval('AssistDriveManipulator -create;')


    def _deleteManipulator(self, *args):
        pm.mel.eval('AssistDriveManipulator -delete;')


    def _toggleManipulator(self, ckb, *args):
        v0 = pm.menuItem(self._cmMn, cb=True, q=True)
        v1 = pm.checkBox(self._cbMn, v=True, q=True)
        if ckb == 0:
            if v0: self._createManipulator()
            else:  self._deleteManipulator()
            pm.checkBox(self._cbMn, v=v0, e=True)
        if ckb == 1:
            if v1: self._createManipulator()
            else:  self._deleteManipulator()
            pm.menuItem(self._cmMn, cb=v1, e=True)


    def _activeManipulator(self, _adn_, *args):
        pm.mel.eval('SelectAssistDriveNode "{0}";'.format(_adn_))


    def _getADNNode(self, *args):
        adn = pm.ls(typ='AssistDriveNode')
        nl  = self._filterAdn(adn)
        #-- edit list
        self._clearList()
        pm.textScrollList(self._tsl, a=nl, e=True)
        #-- edit text
        self._countAdn()


    def _filterAdn(self, adn=[], *args):
        val = self._getDisplay()
        adL = [k for k, v in zip(self._adnList, val) if v] 
        res = []

        if adn:
            for i in adn:
                typ = pm.getAttr('{0}.DriveType'.format(i))
                if typ in adL:
                    res.append(i)
        return res


    def _countAdn(self, *args):
        nViw = pm.textScrollList(self._tsl, ni=True, q=True)
        nAll = len(pm.ls(typ='AssistDriveNode'))
        pm.text(self._txN, l='view  {0}  /  All  {1}  nodes.'.format(nViw, nAll), e=True)


    def _checkBoxAdn(self, *args):
        pin = pm.iconTextCheckBox(self._ibp, v=True, q=True)
        aln = [i.name() for i in pm.ls(typ='AssistDriveNode')]
        nl  = self._filterAdn(aln)
        if not pin:
            #-- edit list
            self._clearList()
            pm.textScrollList(self._tsl, a=nl, e=True)
            #-- edit text
            self._countAdn()


    def _getDisplay(self, *args):
        res = []
        res.append(pm.menuItem(self._cmCr, cb=True, q=True))
        res.append(pm.menuItem(self._cmAr, cb=True, q=True))
        res.append(pm.menuItem(self._cmAb, cb=True, q=True))
        res.append(pm.menuItem(self._cmAm, cb=True, q=True))
        res.append(pm.menuItem(self._cmRm, cb=True, q=True))
        res.append(pm.menuItem(self._cmYp, cb=True, q=True))
        res.append(pm.menuItem(self._cmRs, cb=True, q=True))
        return res


    def _allCheck(self, *args):
        pm.menuItem(self._cmCr, cb=True, e=True)
        pm.menuItem(self._cmAr, cb=True, e=True)
        pm.menuItem(self._cmAb, cb=True, e=True)
        pm.menuItem(self._cmAm, cb=True, e=True)
        pm.menuItem(self._cmRm, cb=True, e=True)
        pm.menuItem(self._cmYp, cb=True, e=True)
        pm.menuItem(self._cmRs, cb=True, e=True)
        self._checkBoxAdn()


    def _allOff(self, *args):
        pm.menuItem(self._cmCr, cb=False, e=True)
        pm.menuItem(self._cmAr, cb=False, e=True)
        pm.menuItem(self._cmAb, cb=False, e=True)
        pm.menuItem(self._cmAm, cb=False, e=True)
        pm.menuItem(self._cmRm, cb=False, e=True)
        pm.menuItem(self._cmYp, cb=False, e=True)
        pm.menuItem(self._cmRs, cb=False, e=True)
        self._checkBoxAdn()


    def _searchAdn(self, *args):
        n   = pm.textFieldGrp(self._tfn, tx=True, q=True)
        nl  = pm.textScrollList(self._tsl, ai=True, q=True)
        if n and nl:            
            #nl  = pm.ls(typ='AssistDriveNode')
            res = [i for i in nl if n in i]
            self._clearList()
            pm.textScrollList(self._tsl, a=res, e=True)
        else:
            self._getADNNode()


    def _selectAdn(self, *args):
        sil = pm.textScrollList(self._tsl, si=True, q=True)
        pm.select(sil, r=True)


    def _selectAllAdn(self, *args):
        sil = pm.textScrollList(self._tsl, ai=True, q=True)
        pm.textScrollList(self._tsl, si=sil, e=True)
        pm.select(sil, r=True)


    def _adnUIVis(self, typ='', *args):
        ui = [self.clL1, self.clL2, self.clL3, self.clL4, self.clL5, self.clL6, self.clL7]
        vl = adn.adn_getSelectedList(typ)
        for u, v in zip(ui, vl):
            pm.columnLayout(u, vis=v, e=True)


    def _adnUIHide(self, typ='', *args):
        ui = [self.clL1, self.clL2, self.clL3, self.clL4, self.clL5, self.clL6, self.clL7]
        for u in ui:
            pm.columnLayout(u, vis=False, e=True)
        self._adnLimitUIVis(typ='')


    def _adnLimitUIVis(self, typ='', *args):
        vl = adn.adn_getSelectedList(typ)
        if typ in ['AxisMove', 'RollMove']:
            pm.formLayout(self.fmL3, vis=True,  e=True)
            pm.formLayout(self.fmL4, vis=False, e=True)
            pm.formLayout(self.fmL5, vis=False, e=True)
        elif typ in ['CopyRotate', 'AxisRoll', 'AxisRollBlend', 'YawPitchRotate']:
            pm.formLayout(self.fmL3, vis=False, e=True)
            pm.formLayout(self.fmL4, vis=True,  e=True)
            pm.formLayout(self.fmL5, vis=False, e=True)
        elif typ in ['RollScale']:
            pm.formLayout(self.fmL3, vis=False, e=True)
            pm.formLayout(self.fmL4, vis=False, e=True)
            pm.formLayout(self.fmL5, vis=True,  e=True)
        else:
            pm.formLayout(self.fmL3, vis=False, e=True)
            pm.formLayout(self.fmL4, vis=False, e=True)
            pm.formLayout(self.fmL5, vis=False, e=True)


    def _refreshADNInfo(self, *args):
        sil = pm.textScrollList(self._tsl, si=True, q=True)
        if sil:
            tgt   = sil[0]
            env   = True
            adn_n = tgt
            adn_i = adn.adn_input(tgt)
            adn_o = adn.adn_output(tgt)
            adn_t = adn.adn_type(tgt)
            adn_c = adn.adn_commentField(tgt)

            #-- show ui
            self._adnUIVis(adn_t)
            self._adnLimitUIVis(adn_t)

            #-- insert Attr
            self._getAdnAttr(adNode=tgt)

            #-- Manipulator
            print (tgt)
            self._activeManipulator(tgt)

        else:
            tgt   = ''
            env   = False
            adn_n = ''
            adn_i = ''
            adn_o = ''
            adn_t = ''
            adn_c = ''

            #-- Hide ui
            self._adnUIHide()

        #-- edit UI
        pm.iconTextButton(self._ibt5, en=env, e=True)
        pm.iconTextButton(self._ibt6, en=env, e=True)
        pm.textFieldGrp(self._tfa, tx=adn_n, e=True)
        pm.textFieldGrp(self._tf0, tx=adn_i, e=True)
        pm.textFieldGrp(self._tf1, tx=adn_o, e=True)
        pm.textFieldGrp(self._tf2, tx=adn_t, e=True)
        pm.textFieldGrp(self._tf3, tx=adn_c, e=True)



    def _getAdnAttr(self, adNode='', *arg):
        data = assistdrive.get_assistdrive_node_data(adNode)
        dtyp = data['DriveType']
        dAtr = data['AssistDriveData']
        drvn = data['Driven']

        if dtyp == 'CopyRotate':
            pm.floatSliderGrp(self._fs1, v=dAtr['RotateRate'], e=True)
            pm.floatFieldGrp(self._ff1, 
                             v1=dAtr['RotateOffset'][0], 
                             v2=dAtr['RotateOffset'][1], 
                             v3=dAtr['RotateOffset'][2], e=True)

            pm.floatFieldGrp(self._rlf0, 
                             v1=dAtr['LimitRotateMinX'],
                             v2=pm.getAttr('{0}.rotateX'.format(drvn)),
                             v3=dAtr['LimitRotateMaxX'], e=True)
            pm.checkBox(self._rmi0, v=dAtr['EnableLimitRotateMinX'], e=True)
            pm.checkBox(self._rmx0, v=dAtr['EnableLimitRotateMaxX'], e=True)

            pm.floatFieldGrp(self._rlf1, 
                             v1=dAtr['LimitRotateMinY'],
                             v2=pm.getAttr('{0}.rotateY'.format(drvn)),
                             v3=dAtr['LimitRotateMaxY'], e=True)
            pm.checkBox(self._rmi1, v=dAtr['EnableLimitRotateMinY'], e=True)
            pm.checkBox(self._rmx1, v=dAtr['EnableLimitRotateMaxY'], e=True)

            pm.floatFieldGrp(self._rlf2, 
                             v1=dAtr['LimitRotateMinZ'],
                             v2=pm.getAttr('{0}.rotateZ'.format(drvn)),
                             v3=dAtr['LimitRotateMaxZ'], e=True)
            pm.checkBox(self._rmi2, v=dAtr['EnableLimitRotateMinZ'], e=True)
            pm.checkBox(self._rmx2, v=dAtr['EnableLimitRotateMaxZ'], e=True)

        elif dtyp == 'AxisRoll':
            pm.floatFieldGrp(self._ff2,
                             v1=dAtr['RollAxis'][0], 
                             v2=dAtr['RollAxis'][1], 
                             v3=dAtr['RollAxis'][2], e=True)
            pm.floatSliderGrp(self._fs2, v=dAtr['RollRate'], e=True)
            pm.floatFieldGrp(self._ff3, 
                             v1=dAtr['RotateOffset'][0], 
                             v2=dAtr['RotateOffset'][1], 
                             v3=dAtr['RotateOffset'][2], e=True)

            pm.floatFieldGrp(self._rlf0, 
                             v1=dAtr['LimitRotateMinX'],
                             v2=pm.getAttr('{0}.rotateX'.format(drvn)),
                             v3=dAtr['LimitRotateMaxX'], e=True)
            pm.checkBox(self._rmi0, v=dAtr['EnableLimitRotateMinX'], e=True)
            pm.checkBox(self._rmx0, v=dAtr['EnableLimitRotateMaxX'], e=True)

            pm.floatFieldGrp(self._rlf1, 
                             v1=dAtr['LimitRotateMinY'],
                             v2=pm.getAttr('{0}.rotateY'.format(drvn)),
                             v3=dAtr['LimitRotateMaxY'], e=True)
            pm.checkBox(self._rmi1, v=dAtr['EnableLimitRotateMinY'], e=True)
            pm.checkBox(self._rmx1, v=dAtr['EnableLimitRotateMaxY'], e=True)

            pm.floatFieldGrp(self._rlf2, 
                             v1=dAtr['LimitRotateMinZ'],
                             v2=pm.getAttr('{0}.rotateZ'.format(drvn)),
                             v3=dAtr['LimitRotateMaxZ'], e=True)
            pm.checkBox(self._rmi2, v=dAtr['EnableLimitRotateMinZ'], e=True)
            pm.checkBox(self._rmx2, v=dAtr['EnableLimitRotateMaxZ'], e=True)


        elif dtyp == 'AxisRollBlend':
            pm.floatFieldGrp(self._ff4,
                             v1=dAtr['RollAxis'][0], 
                             v2=dAtr['RollAxis'][1], 
                             v3=dAtr['RollAxis'][2], e=True)
            pm.floatSliderGrp(self._fs3, v=dAtr['RollRate'], e=True)
            pm.floatSliderGrp(self._fs4, v=dAtr['EtcRate'], e=True)
            pm.floatFieldGrp(self._ff5, 
                             v1=dAtr['RotateOffset'][0], 
                             v2=dAtr['RotateOffset'][1], 
                             v3=dAtr['RotateOffset'][2], e=True)

            pm.floatFieldGrp(self._rlf0, 
                             v1=dAtr['LimitRotateMinX'],
                             v2=pm.getAttr('{0}.rotateX'.format(drvn)),
                             v3=dAtr['LimitRotateMaxX'], e=True)
            pm.checkBox(self._rmi0, v=dAtr['EnableLimitRotateMinX'], e=True)
            pm.checkBox(self._rmx0, v=dAtr['EnableLimitRotateMaxX'], e=True)

            pm.floatFieldGrp(self._rlf1, 
                             v1=dAtr['LimitRotateMinY'],
                             v2=pm.getAttr('{0}.rotateY'.format(drvn)),
                             v3=dAtr['LimitRotateMaxY'], e=True)
            pm.checkBox(self._rmi1, v=dAtr['EnableLimitRotateMinY'], e=True)
            pm.checkBox(self._rmx1, v=dAtr['EnableLimitRotateMaxY'], e=True)

            pm.floatFieldGrp(self._rlf2, 
                             v1=dAtr['LimitRotateMinZ'],
                             v2=pm.getAttr('{0}.rotateZ'.format(drvn)),
                             v3=dAtr['LimitRotateMaxZ'], e=True)
            pm.checkBox(self._rmi2, v=dAtr['EnableLimitRotateMinZ'], e=True)
            pm.checkBox(self._rmx2, v=dAtr['EnableLimitRotateMaxZ'], e=True)

        elif dtyp == 'AxisMove':
            pm.floatFieldGrp(self._ff6,
                             v1=dAtr['RollAxis'][0], 
                             v2=dAtr['RollAxis'][1], 
                             v3=dAtr['RollAxis'][2], e=True)
            pm.floatFieldGrp(self._ff7,
                             v1=dAtr['MoveAxis'][0], 
                             v2=dAtr['MoveAxis'][1], 
                             v3=dAtr['MoveAxis'][2], e=True)
            pm.floatFieldGrp(self._ff8, 
                             v1=dAtr['MoveOffset'][0], 
                             v2=dAtr['MoveOffset'][1], 
                             v3=dAtr['MoveOffset'][2], e=True)
            pm.floatFieldGrp(self._ff9, 
                             v1=dAtr['MoveLength'], e=True)
            pm.floatFieldGrp(self._ff10, 
                             v1=dAtr['MoveRange'][0], 
                             v2=dAtr['MoveRange'][1], e=True)
            pm.optionMenuGrp(self._opm1, sl=dAtr['EaseType']+1, e=True)

            pm.floatFieldGrp(self._tlf0, 
                             v1=dAtr['LimitTransMinX'],
                             v2=pm.getAttr('{0}.translateX'.format(drvn)),
                             v3=dAtr['LimitTransMaxX'], e=True)
            pm.checkBox(self._tmi0, v=dAtr['EnableLimitTransMinX'], e=True)
            pm.checkBox(self._tmx0, v=dAtr['EnableLimitTransMaxX'], e=True)

            pm.floatFieldGrp(self._tlf1, 
                             v1=dAtr['LimitTransMinY'],
                             v2=pm.getAttr('{0}.translateY'.format(drvn)),
                             v3=dAtr['LimitTransMaxY'], e=True)
            pm.checkBox(self._tmi1, v=dAtr['EnableLimitTransMinY'], e=True)
            pm.checkBox(self._tmx1, v=dAtr['EnableLimitTransMaxY'], e=True)

            pm.floatFieldGrp(self._tlf2, 
                             v1=dAtr['LimitTransMinZ'],
                             v2=pm.getAttr('{0}.translateZ'.format(drvn)),
                             v3=dAtr['LimitTransMaxZ'], e=True)
            pm.checkBox(self._tmi2, v=dAtr['EnableLimitTransMinZ'], e=True)
            pm.checkBox(self._tmx2, v=dAtr['EnableLimitTransMaxZ'], e=True)

        elif dtyp == 'RollMove': 
            pm.floatFieldGrp(self._ff11,
                             v1=dAtr['RollAxis'][0], 
                             v2=dAtr['RollAxis'][1], 
                             v3=dAtr['RollAxis'][2], e=True)
            pm.floatFieldGrp(self._ff12,
                             v1=dAtr['MoveAxis'][0], 
                             v2=dAtr['MoveAxis'][1], 
                             v3=dAtr['MoveAxis'][2], e=True)
            pm.floatFieldGrp(self._ff13, 
                             v1=dAtr['MoveOffset'][0], 
                             v2=dAtr['MoveOffset'][1], 
                             v3=dAtr['MoveOffset'][2], e=True)
            pm.floatFieldGrp(self._ff14, 
                             v1=dAtr['MoveLength'], e=True)
            pm.floatFieldGrp(self._ff15, 
                             v1=dAtr['MoveRange'][0], 
                             v2=dAtr['MoveRange'][1], e=True)
            pm.optionMenuGrp(self._opm2, sl=dAtr['EaseType']+1, e=True)

            pm.floatFieldGrp(self._tlf0, 
                             v1=dAtr['LimitTransMinX'],
                             v2=pm.getAttr('{0}.translateX'.format(drvn)),
                             v3=dAtr['LimitTransMaxX'], e=True)
            pm.checkBox(self._tmi0, v=dAtr['EnableLimitTransMinX'], e=True)
            pm.checkBox(self._tmx0, v=dAtr['EnableLimitTransMaxX'], e=True)

            pm.floatFieldGrp(self._tlf1, 
                             v1=dAtr['LimitTransMinY'],
                             v2=pm.getAttr('{0}.translateY'.format(drvn)),
                             v3=dAtr['LimitTransMaxY'], e=True)
            pm.checkBox(self._tmi1, v=dAtr['EnableLimitTransMinY'], e=True)
            pm.checkBox(self._tmx1, v=dAtr['EnableLimitTransMaxY'], e=True)

            pm.floatFieldGrp(self._tlf2, 
                             v1=dAtr['LimitTransMinZ'],
                             v2=pm.getAttr('{0}.translateZ'.format(drvn)),
                             v3=dAtr['LimitTransMaxZ'], e=True)
            pm.checkBox(self._tmi2, v=dAtr['EnableLimitTransMinZ'], e=True)
            pm.checkBox(self._tmx2, v=dAtr['EnableLimitTransMaxZ'], e=True)

        elif dtyp == 'YawPitchRotate':
            pm.intSliderGrp(self._is0, v=dAtr['RollType'], e=True)
            pm.floatSliderGrp(self._fs5, v=dAtr['YawRate'], e=True)
            pm.floatFieldGrp(self._ff16, 
                             v1=dAtr['YawLimit'][0], 
                             v2=dAtr['YawLimit'][1], e=True)
            pm.floatSliderGrp(self._fs6, v=dAtr['PitchRate'], e=True)
            pm.floatFieldGrp(self._ff17, 
                             v1=dAtr['PitchLimit'][0], 
                             v2=dAtr['PitchLimit'][1], e=True)
            pm.floatFieldGrp(self._ff18, 
                             v1=dAtr['RotateOffset'][0], 
                             v2=dAtr['RotateOffset'][1], 
                             v3=dAtr['RotateOffset'][2], e=True)

            pm.floatFieldGrp(self._rlf0, 
                             v1=dAtr['LimitRotateMinX'],
                             v2=pm.getAttr('{0}.rotateX'.format(drvn)),
                             v3=dAtr['LimitRotateMaxX'], e=True)
            pm.checkBox(self._rmi0, v=dAtr['EnableLimitRotateMinX'], e=True)
            pm.checkBox(self._rmx0, v=dAtr['EnableLimitRotateMaxX'], e=True)

            pm.floatFieldGrp(self._rlf1, 
                             v1=dAtr['LimitRotateMinY'],
                             v2=pm.getAttr('{0}.rotateY'.format(drvn)),
                             v3=dAtr['LimitRotateMaxY'], e=True)
            pm.checkBox(self._rmi1, v=dAtr['EnableLimitRotateMinY'], e=True)
            pm.checkBox(self._rmx1, v=dAtr['EnableLimitRotateMaxY'], e=True)

            pm.floatFieldGrp(self._rlf2, 
                             v1=dAtr['LimitRotateMinZ'],
                             v2=pm.getAttr('{0}.rotateZ'.format(drvn)),
                             v3=dAtr['LimitRotateMaxZ'], e=True)
            pm.checkBox(self._rmi2, v=dAtr['EnableLimitRotateMinZ'], e=True)
            pm.checkBox(self._rmx2, v=dAtr['EnableLimitRotateMaxZ'], e=True)

        elif dtyp == 'RollScale': 
            pm.floatFieldGrp(self._ff19,
                             v1=dAtr['RollAxis'][0], 
                             v2=dAtr['RollAxis'][1], 
                             v3=dAtr['RollAxis'][2], e=True)
            pm.floatFieldGrp(self._ff20,
                             v1=dAtr['ScaleLength'][0], 
                             v2=dAtr['ScaleLength'][1], 
                             v3=dAtr['ScaleLength'][2], e=True)
            pm.optionMenuGrp(self._opm3, sl=dAtr['EaseType']+1, e=True)

            pm.floatFieldGrp(self._slf0, 
                             v1=dAtr['LimitScaleMinX'],
                             v2=pm.getAttr('{0}.scaleX'.format(drvn)),
                             v3=dAtr['LimitScaleMaxX'], e=True)
            pm.checkBox(self._smi0, v=dAtr['EnableLimitScaleMinX'], e=True)
            pm.checkBox(self._smx0, v=dAtr['EnableLimitScaleMaxX'], e=True)

            pm.floatFieldGrp(self._slf1, 
                             v1=dAtr['LimitScaleMinY'],
                             v2=pm.getAttr('{0}.scaleY'.format(drvn)),
                             v3=dAtr['LimitScaleMaxY'], e=True)
            pm.checkBox(self._smi1, v=dAtr['EnableLimitScaleMinY'], e=True)
            pm.checkBox(self._smx1, v=dAtr['EnableLimitScaleMaxY'], e=True)

            pm.floatFieldGrp(self._slf2, 
                             v1=dAtr['LimitScaleMinZ'],
                             v2=pm.getAttr('{0}.scaleZ'.format(drvn)),
                             v3=dAtr['LimitScaleMaxZ'], e=True)
            pm.checkBox(self._smi2, v=dAtr['EnableLimitScaleMinZ'], e=True)
            pm.checkBox(self._smx2, v=dAtr['EnableLimitScaleMaxZ'], e=True)

        else:
            pass


    def _setDD(self, *arg):
        log  = ''
        nAll = pm.ls(typ='AssistDriveNode')
        for i in nAll:
            data = assistdrive.get_assistdrive_node_data(i.name())
            drvr = data['Driver']
            drvn = data['Driven']
            v = '[{0}] -> [{1}]'.format(drvr, drvn)
            i.CommentField.set(v)
            log += 'Set Driver and Driven : {0:<30} {1}\n'.format(i.name(), v)
        self._refreshADNInfo()
        print (log)


    def _adnHideUI(self, *args):
        ui = [self.clL1, self.clL2, self.clL3, self.clL4, self.clL5, self.clL6, self.clL7]
        for u in ui:
            pm.columnLayout(u, vis=False, e=True)
        pm.formLayout(self.fmL3, vis=False, e=True)
        pm.formLayout(self.fmL4, vis=False, e=True)
        pm.formLayout(self.fmL5, vis=False, e=True)


    def _pinAdn(self, *args):
        sil = pm.textScrollList(self._tsl, si=True, q=True)
        pm.textScrollList(self._tsl, ra=True, e=True)
        pm.textScrollList(self._tsl, a=sil, e=True)
        pm.textScrollList(self._tsl, si=sil, e=True)
        self._countAdn()


    def _unpinAdn(self, *args):
        sil = pm.textScrollList(self._tsl, si=True, q=True)
        self._getADNNode()
        adn = pm.textScrollList(self._tsl, ai=True, q=True)

        pm.textScrollList(self._tsl, da=True, e=True)
        if sil:
            for i in sil:
                if i in adn:
                    pm.textScrollList(self._tsl, si=i, e=True)


    def _changeAdn(self, *args):
        typ = pm.optionMenu(self._opm, v=True, q=True)
        pre = self._adnType[typ]
        pm.text(self._ptx1, l='ADN_{0}_'.format(pre), e=True)
        if typ == 'RollScale':
            pm.checkBox(self._ckko, en=False, e=True)
        else:
            pm.checkBox(self._ckko, en=True, e=True)
        #-- change axis
        self._changeAxis()


    def _changeAxis(self, *args):
        typ = pm.optionMenu(self._opm, v=True, q=True)
        pre = self._adnType[typ]
        if typ == 'CopyRotate':
            pm.optionMenu(self._opAx, en=False, e=True)
        elif typ == 'YawPitchRotate':
            pm.menuItem(self._miax3, en=False, e=True)
            pm.menuItem(self._miax4, en=False, e=True)
            pm.menuItem(self._miax5, en=False, e=True)
        else:
            pm.optionMenu(self._opAx, en=True, e=True)
            pm.menuItem(self._miax3, en=True, e=True)
            pm.menuItem(self._miax4, en=True, e=True)
            pm.menuItem(self._miax5, en=True, e=True)


    def _changeSide(self, *args):
        typ = pm.optionMenu(self._osd, v=True, q=True)
        pm.text(self._ptx2, l=self._side[typ], e=True)


    def _createAdn(self, *args):
        oft = (0,0,0)
        kof = pm.checkBox(self._ckko, v=True, q=True)
        pax = pm.optionMenu(self._opAx, sl=True, q=True) -1
        axl = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)]
        ypl = [0, 1, 2, 0, 1, 2]

        sel = pm.selected()
        typ = pm.optionMenu(self._opm, v=True, q=True)
        sde = self._side[pm.optionMenu(self._osd, v=True, q=True)]
        sid = pm.optionMenu(self._osd, sl=True, q=True) - 1
        pre = self._adnType[typ]
        n   = pm.textFieldGrp(self._tfan, tx=True, q=True)
        if not n: n = typ

        #-- create assist drive
        if len(sel) == 2:
            src = sel[0].name()
            tgt = sel[1].name()
            anm = 'ADN_{0}_{1}{2}'.format(pre, sde, n)

            #-- get offset
            if kof:
                if typ in ['AxisMove', 'RollMove']:
                    oft = pm.getAttr('{0}.translate'.format(tgt))
                elif typ in ['CopyRotate', 'AxisRoll', 'AxisRollBlend', 'YawPitchRotate']:
                    oft = pm.getAttr('{0}.rotate'.format(tgt))

            #-- create assist drive
            res = adn.create_assistdrive_node(typ, src, tgt, anm)

            #-- set offset
            if kof:
                if typ in ['AxisMove', 'RollMove']:
                    pm.setAttr('{0}.MoveOffset'.format(res), oft)
                elif typ in ['CopyRotate', 'AxisRoll', 'AxisRollBlend', 'YawPitchRotate']:
                    pm.setAttr('{0}.RotateOffset'.format(res), oft)

            #-- set axis
            if typ in ['AxisRoll', 'AxisRollBlend', 'AxisMove', 'RollMove', 'RollScale']:
                pm.setAttr('{0}.RollAxis0'.format(res), axl[pax][0])
                pm.setAttr('{0}.RollAxis1'.format(res), axl[pax][1])
                pm.setAttr('{0}.RollAxis2'.format(res), axl[pax][2])
            elif typ in ['YawPitchRotate']:
                pm.setAttr('{0}.RollType'.format(res), ypl[pax])

            #-- label & color
            jtl = 'ADN_{0}_{1}'.format(pre, n)
            adn.setOverrideColorIndex(tgt)
            setup.setJointLabel(tgt, sid, 18, jtl)

        else:
            res = ''
            pm.warning('Please select 2 objects source and target.')

        #-- refresh
        self._getADNNode()
        if res:
            pm.textScrollList(self._tsl, si=res, e=True)
            self._refreshADNInfo()


    def _getFromSelection(self, *args):
        adnList = adn.getAdnFromDelection()
        if adnList:
            items = pm.textScrollList(self._tsl, ai=True, q=True)
            pm.textScrollList(self._tsl, da=True, e=True)
            for i in adnList:
                if i in items:
                    pm.textScrollList(self._tsl, si=i, e=True)
                else:
                    pm.textScrollList(self._tsl, a=i, e=True)
                    pm.textScrollList(self._tsl, si=i, e=True)    
        self._refreshADNInfo()


    def _addFromSelection(self, *args):
        adnList = adn.getAdnFromDelection()
        if adnList:
            items = pm.textScrollList(self._tsl, ai=True, q=True)
            for i in adnList:
                if i in items:
                    pm.textScrollList(self._tsl, si=i, e=True)
                else:
                    pm.textScrollList(self._tsl, a=i, e=True)
                    pm.textScrollList(self._tsl, si=i, e=True)    
        self._refreshADNInfo()


    def _deleteAdn(self, *args):
        sl = pm.textScrollList(self._tsl, si=True, q=True)
        for i in sl:
            if pm.objExists(i):
                pm.delete(i)
                print ('Delete Assist Drive Node : {0}'.format(i))
        self._getADNNode()
        pm.textScrollList(self._tsl, da=True, e=True)
        self._refreshADNInfo()


    def _deleteAllAdn(self, *arg):
        v = pm.confirmDialog(t='Confirm', m='Do you want Delete All Assist Drive?', 
                             b=['Delete', 'Cancel'], db='Cancel', cb='Cancel', ds='Cancel')
        if v == 'Delete':
            nl = pm.ls(typ='AssistDriveNode')
            pm.delete(nl)
            pm.textScrollList(self._tsl, ra=True, e=True)


    def _deleteErrorAdn(elf, *arg):
        v = pm.confirmDialog(t='Confirm', m='Do you want Delete Error Assist Drive?', 
                             b=['Delete', 'Cancel'], db='Cancel', cb='Cancel', ds='Cancel')
        res = []
        log = ''
        if v == 'Delete':
            nl = pm.ls(typ='AssistDriveNode')
            for i in nl:
                if not adn.adn_input(i.name()):  
                    res.append(i)
                    log += 'source error : {0}\n'.format(i.name())
                if not adn.adn_output(i.name()): 
                    res.append(i)
                    log += 'target error : {0}\n'.format(i.name())
            if res:
                res = list(set(res))
                pm.delete(res)
                print (log)


    def _importCsv(self, *arg):
        path = pm.textFieldGrp(self._tfpa, tx=True, q=True)
        bf   = '*.csv'
        path = pm.fileDialog2(dir=path, ff=bf, ds=2, fm=1)
        if path:
            assistdrive.import_assistdrive_settings(path[0], '', False, False) 
            pm.textFieldGrp(self._tfpa, tx=path[0], e=True)
            self._getADNNode()
        return path


    def _exportCsv(self, *arg):
        bf   = '*.csv'
        path = pm.fileDialog2(ff=bf, ds=2)
        if path:
            assistdrive.export_assistdrive_settings(path[0], False)
            pm.textFieldGrp(self._tfpa, tx=path[0], e=True)
            self._getADNNode()
        return path


    def _exportCsvFromSelection(self, *arg):
        tgt  = pm.textScrollList(self._tsl, si=True, q=True)
        bf   = '*.csv'
        path = pm.fileDialog2(ff=bf, ds=2)
        if path:
            assistdrive.export_assistdrive_settings(path[0], tgt)
            pm.textFieldGrp(self._tfpa, tx=path[0], e=True)
            self._getADNNode()
        return path


    def _copyAdn(self, *arg):
        adn = pm.textFieldGrp(self._tfa, tx=True, q=True)

        if pm.objExists(adn):
            data = assistdrive.get_assistdrive_node_data(adn)
            typ  = pm.getAttr('{0}.DriveType'.format(adn))
            path = r'{0}/temp.json'.format(self._temp)
            command.exportJson(path, data)

            #-- log
            pm.text(self._txCP, l='{0} | {1} copied.'.format(typ, adn), en=True, e=True)
            print ('{0} | {1} copied.'.format(typ, adn))


    def _pasteAdn(self, *arg):
        log = ''
        #-- data
        path = r'{0}/temp.json'.format(self._temp)
        if os.path.exists(path):
            data = command.importJson(path)        
            dtyp = data['DriveType']
            dAtr = data['AssistDriveData']
            dAdd = [i for i in dAtr.keys()]

            #-- target
            sl   = pm.textScrollList(self._tsl, si=True, q=True)
            tgtL = [i for i in sl if pm.getAttr('{0}.DriveType'.format(i)) == dtyp]

            for tgt in tgtL:
                for attr in dAdd:
                    pm.setAttr('{0}.{1}'.format(tgt, attr), dAtr[attr])
                log += 'Paseted Assist Drive: {0} \n'.format(tgt)

            #-- refresh
            self._refreshADNInfo()
            print (log)
        else:
            pm.warning('Please copy Assist Drive.')


    def _cleanTemp(self, *arg):
        path = r'{0}/temp.json'.format(self._temp)
        if os.path.exists(path):
            os.remove(path)
            pm.text(self._txCP, l=' ', en=False, e=True)
            print ('Delete {0}'.format(path))


    #--- set Attr --------------------------------------------------------------
    def _setName(self, *arg):
        tgid = pm.textScrollList(self._tsl, sii=True, q=True)
        tgt  = pm.textScrollList(self._tsl, si=True, q=True)
        name = pm.textFieldGrp(self._tfa, tx=True, q=True)
        if name:
            if tgt:
                if not tgt[0] == name:
                    pm.rename(tgt[0], name)
                    pm.textScrollList(self._tsl, rii=tgid[0], e=True)
                    pm.textScrollList(self._tsl, ap=(tgid[0], name), e=True)
                    pm.textScrollList(self._tsl, sii=tgid[0], e=True)
            else:
                print (tgid[0])


    def _selSrc(self, *arg):
        name = pm.textFieldGrp(self._tf0, tx=True, q=True)
        if name and pm.objExists(name):
            pm.select(name, r=True)


    def _selTgt(self, *arg):
        name = pm.textFieldGrp(self._tf1, tx=True, q=True)
        if name and pm.objExists(name):
            pm.select(name, r=True)


    def _setCommentField(self, *arg):
        tgt = pm.textFieldGrp(self._tfa, tx=True, q=True)
        val = pm.textFieldGrp(self._tf3, tx=True, q=True)
        if tgt:
            pm.setAttr('{0}.CommentField'.format(tgt), val)


    def _setDDComment(self, *arg):
        log = ''
        tgt = pm.textFieldGrp(self._tfa, tx=True, q=True)

        if tgt:
            tgt = pm.PyNode(tgt)
            data = assistdrive.get_assistdrive_node_data(tgt.name())
            drvr = data['Driver']
            drvn = data['Driven']
            v = '[{0}] -> [{1}]'.format(drvr, drvn)
            tgt.CommentField.set(v)
            log += 'Set Driver and Driven : {0:<30} {1}\n'.format(tgt.name(), v)
            self._refreshADNInfo()
            print (log)


    #--- set Attr Copy Rotate --------------------------------------------------
    def _getAdNode(self, *arg):
        name = pm.textFieldGrp(self._tfa, tx=True, q=True)
        if pm.objExists(name):
            return pm.PyNode(name)
        else:
            return None


    def _refresh(self, *arg):
        src = pm.textFieldGrp(self._tf0, tx=True, q=True)
        if pm.objExists(src):
            adn.adn_refresh(src)


    def _setCRAttr(self, *arg):
        adNode = self._getAdNode()
        rrv = pm.floatSliderGrp(self._fs1, v=True, q=True)
        rov = pm.floatFieldGrp(self._ff1, v=True, q=True)

        adNode.RotateRate.set(rrv)
        adNode.RotateOffset0.set(rov[0])
        adNode.RotateOffset1.set(rov[1])
        adNode.RotateOffset2.set(rov[2])
        self._refresh()


    #--- set Attr Axis Roll ----------------------------------------------------
    def _setARAttr(self, *arg):
        adNode = self._getAdNode()
        rav = [self.vClamp(i) for i in pm.floatFieldGrp(self._ff2, v=True, q=True)]
        rrv = pm.floatSliderGrp(self._fs2, v=True, q=True)
        rov = [self.oClamp(i) for i in pm.floatFieldGrp(self._ff3, v=True, q=True)]

        adNode.RollAxis0.set(rav[0])
        adNode.RollAxis1.set(rav[1])
        adNode.RollAxis2.set(rav[2])
        adNode.RollRate.set(rrv)
        adNode.RotateOffset0.set(rov[0])
        adNode.RotateOffset1.set(rov[1])
        adNode.RotateOffset2.set(rov[2])

        pm.floatFieldGrp(self._ff2, v1=rav[0], v2=rav[1], v3=rav[2], e=True)
        pm.floatFieldGrp(self._ff3, v1=rov[0], v2=rov[1], v3=rov[2], e=True)
        self._refresh()


    #--- set Attr Axis Roll Blend ----------------------------------------------
    def _setABAttr(self, *arg):
        adNode = self._getAdNode()
        rav = [self.vClamp(i) for i in pm.floatFieldGrp(self._ff4, v=True, q=True)]
        rrv = pm.floatSliderGrp(self._fs3, v=True, q=True)
        erv = pm.floatSliderGrp(self._fs4, v=True, q=True)
        rov = [self.oClamp(i) for i in pm.floatFieldGrp(self._ff5, v=True, q=True)]

        adNode.RollAxis0.set(rav[0])
        adNode.RollAxis1.set(rav[1])
        adNode.RollAxis2.set(rav[2])
        adNode.RollRate.set(rrv)
        adNode.EtcRate.set(erv)
        adNode.RotateOffset0.set(rov[0])
        adNode.RotateOffset1.set(rov[1])
        adNode.RotateOffset2.set(rov[2])

        pm.floatFieldGrp(self._ff4, v1=rav[0], v2=rav[1], v3=rav[2], e=True)
        pm.floatFieldGrp(self._ff5, v1=rov[0], v2=rov[1], v3=rov[2], e=True)
        self._refresh()


    #--- set Attr Axis Move ----------------------------------------------------
    def _setAMAttr(self, *arg):
        adNode = self._getAdNode()

        rav = [self.vClamp(i) for i in pm.floatFieldGrp(self._ff6, v=True, q=True)]
        mav = [self.vClamp(i) for i in pm.floatFieldGrp(self._ff7, v=True, q=True)]
        mov = pm.floatFieldGrp(self._ff8, v=True, q=True)
        mlv = pm.floatFieldGrp(self._ff9, v=True, q=True)
        mrv = pm.floatFieldGrp(self._ff10, v=True, q=True)
        etv = pm.optionMenuGrp(self._opm1, sl=True, q=True) -1

        adNode.RollAxis0.set(rav[0])
        adNode.RollAxis1.set(rav[1])
        adNode.RollAxis2.set(rav[2])
        adNode.MoveAxis0.set(mav[0])
        adNode.MoveAxis1.set(mav[1])
        adNode.MoveAxis2.set(mav[2])
        adNode.MoveOffset0.set(mov[0])
        adNode.MoveOffset1.set(mov[1])
        adNode.MoveOffset2.set(mov[2])
        adNode.MoveLength.set(mlv[0])
        adNode.MoveRange0.set(mrv[0])
        adNode.MoveRange1.set(mrv[1])
        adNode.EaseType.set(etv)

        pm.floatFieldGrp(self._ff6, v1=rav[0], v2=rav[1], v3=rav[2], e=True)
        pm.floatFieldGrp(self._ff7, v1=mav[0], v2=mav[1], v3=mav[2], e=True)
        self._refresh()



    #--- set Attr Roll Move ----------------------------------------------------
    def _setRMMttr(self, *arg):
        adNode = self._getAdNode()

        rav = [self.vClamp(i) for i in pm.floatFieldGrp(self._ff11, v=True, q=True)]
        mav = [self.vClamp(i) for i in pm.floatFieldGrp(self._ff12, v=True, q=True)]
        mov = pm.floatFieldGrp(self._ff13, v=True, q=True)
        mlv = pm.floatFieldGrp(self._ff14, v=True, q=True)
        mrv = pm.floatFieldGrp(self._ff15, v=True, q=True)
        etv = pm.optionMenuGrp(self._opm2, sl=True, q=True) -1

        adNode.RollAxis0.set(rav[0])
        adNode.RollAxis1.set(rav[1])
        adNode.RollAxis2.set(rav[2])
        adNode.MoveAxis0.set(mav[0])
        adNode.MoveAxis1.set(mav[1])
        adNode.MoveAxis2.set(mav[2])
        adNode.MoveOffset0.set(mov[0])
        adNode.MoveOffset1.set(mov[1])
        adNode.MoveOffset2.set(mov[2])
        adNode.MoveLength.set(mlv[0])
        adNode.MoveRange0.set(mrv[0])
        adNode.MoveRange1.set(mrv[1])
        adNode.EaseType.set(etv)

        pm.floatFieldGrp(self._ff11, v1=rav[0], v2=rav[1], v3=rav[2], e=True)
        pm.floatFieldGrp(self._ff12, v1=mav[0], v2=mav[1], v3=mav[2], e=True)
        self._refresh()


    #--- set Attr Yaw Pitch Roll -----------------------------------------------
    def _setYPAttr(self, *arg):
        adNode = self._getAdNode()

        rtv = pm.intSliderGrp(self._is0, v=True, q=True)
        yrv = pm.floatSliderGrp(self._fs5, v=True, q=True)
        ylv = [self.yClamp(i) for i in pm.floatFieldGrp(self._ff16, v=True, q=True)]
        prv = pm.floatSliderGrp(self._fs6, v=True, q=True)
        plv = [self.yClamp(i) for i in pm.floatFieldGrp(self._ff17, v=True, q=True)]
        rov = [self.oClamp(i) for i in pm.floatFieldGrp(self._ff18, v=True, q=True)]

        adNode.RollType.set(rtv)
        adNode.YawRate.set(yrv)
        adNode.YawLimit0.set(ylv[0])
        adNode.YawLimit1.set(ylv[1])
        adNode.PitchRate.set(prv)
        adNode.PitchLimit0.set(plv[0])
        adNode.PitchLimit1.set(plv[1])
        adNode.RotateOffset0.set(rov[0])
        adNode.RotateOffset1.set(rov[1])
        adNode.RotateOffset2.set(rov[2])

        pm.floatFieldGrp(self._ff16, v1=ylv[0], v2=ylv[1], e=True)
        pm.floatFieldGrp(self._ff17, v1=plv[0], v2=plv[1], e=True)
        pm.floatFieldGrp(self._ff18, v1=rov[0], v2=rov[1], v3=rov[2], e=True)
        self._refresh()


    #--- set Attr Roll Scale ---------------------------------------------------
    def _setRSAttr(self, *arg):
        adNode = self._getAdNode()

        rav = [self.vClamp(i) for i in pm.floatFieldGrp(self._ff19, v=True, q=True)]
        slv = pm.floatFieldGrp(self._ff20, v=True, q=True)
        etv = pm.optionMenuGrp(self._opm3, sl=True, q=True) -1

        adNode.RollAxis0.set(rav[0])
        adNode.RollAxis1.set(rav[1])
        adNode.RollAxis2.set(rav[2])
        adNode.ScaleLength0.set(slv[0])
        adNode.ScaleLength1.set(slv[1])
        adNode.ScaleLength2.set(slv[2])
        adNode.EaseType.set(etv)

        pm.floatFieldGrp(self._ff19, v1=rav[0], v2=rav[1], v3=rav[2], e=True)
        self._refresh()


    #--- Set Limit -------------------------------------------------------------
    def _setLimitTranslate(self, *arg):
        adNode = self._getAdNode()
        enMinX = pm.checkBox(self._tmi0, v=True, q=True)
        enMaxX = pm.checkBox(self._tmx0, v=True, q=True)
        enMinY = pm.checkBox(self._tmi1, v=True, q=True)
        enMaxY = pm.checkBox(self._tmx1, v=True, q=True)
        enMinZ = pm.checkBox(self._tmi2, v=True, q=True)
        enMaxZ = pm.checkBox(self._tmx2, v=True, q=True)
        limTx  = pm.floatFieldGrp(self._tlf0, v=True, q=True)
        limTy  = pm.floatFieldGrp(self._tlf1, v=True, q=True)
        limTz  = pm.floatFieldGrp(self._tlf2, v=True, q=True)

        adNode.EnableLimitTransMinX.set(enMinX)
        adNode.EnableLimitTransMaxX.set(enMaxX)
        adNode.EnableLimitTransMinY.set(enMinY)
        adNode.EnableLimitTransMaxY.set(enMaxY)
        adNode.EnableLimitTransMinZ.set(enMinZ)
        adNode.EnableLimitTransMaxZ.set(enMaxZ)

        adNode.LimitTransMinX.set(limTx[0])
        adNode.LimitTransMaxX.set(limTx[2])
        adNode.LimitTransMinY.set(limTy[0])
        adNode.LimitTransMaxY.set(limTy[2])
        adNode.LimitTransMinZ.set(limTz[0])
        adNode.LimitTransMaxZ.set(limTz[2])
        self._refresh()


    def _setLimitRotate(self, *arg):
        adNode = self._getAdNode()
        enMinX = pm.checkBox(self._rmi0, v=True, q=True)
        enMaxX = pm.checkBox(self._rmx0, v=True, q=True)
        enMinY = pm.checkBox(self._rmi1, v=True, q=True)
        enMaxY = pm.checkBox(self._rmx1, v=True, q=True)
        enMinZ = pm.checkBox(self._rmi2, v=True, q=True)
        enMaxZ = pm.checkBox(self._rmx2, v=True, q=True)
        limRx  = pm.floatFieldGrp(self._rlf0, v=True, q=True)
        limRy  = pm.floatFieldGrp(self._rlf1, v=True, q=True)
        limRz  = pm.floatFieldGrp(self._rlf2, v=True, q=True)

        adNode.EnableLimitRotateMinX.set(enMinX)
        adNode.EnableLimitRotateMaxX.set(enMaxX)
        adNode.EnableLimitRotateMinY.set(enMinY)
        adNode.EnableLimitRotateMaxY.set(enMaxY)
        adNode.EnableLimitRotateMinZ.set(enMinZ)
        adNode.EnableLimitRotateMaxZ.set(enMaxZ)

        adNode.LimitRotateMinX.set(limRx[0])
        adNode.LimitRotateMaxX.set(limRx[2])
        adNode.LimitRotateMinY.set(limRy[0])
        adNode.LimitRotateMaxY.set(limRy[2])
        adNode.LimitRotateMinZ.set(limRz[0])
        adNode.LimitRotateMaxZ.set(limRz[2])
        self._refresh()


    def _setLimitScale(self, *arg):
        adNode = self._getAdNode()
        enMinX = pm.checkBox(self._smi0, v=True, q=True)
        enMaxX = pm.checkBox(self._smx0, v=True, q=True)
        enMinY = pm.checkBox(self._smi1, v=True, q=True)
        enMaxY = pm.checkBox(self._smx1, v=True, q=True)
        enMinZ = pm.checkBox(self._smi2, v=True, q=True)
        enMaxZ = pm.checkBox(self._smx2, v=True, q=True)
        limSx  = pm.floatFieldGrp(self._slf0, v=True, q=True)
        limSy  = pm.floatFieldGrp(self._slf1, v=True, q=True)
        limSz  = pm.floatFieldGrp(self._slf2, v=True, q=True)

        adNode.EnableLimitScaleMinX.set(enMinX)
        adNode.EnableLimitScaleMaxX.set(enMaxX)
        adNode.EnableLimitScaleMinY.set(enMinY)
        adNode.EnableLimitScaleMaxY.set(enMaxY)
        adNode.EnableLimitScaleMinZ.set(enMinZ)
        adNode.EnableLimitScaleMaxZ.set(enMaxZ)

        adNode.LimitScaleMinX.set(limSx[0])
        adNode.LimitScaleMaxX.set(limSx[2])
        adNode.LimitScaleMinY.set(limSy[0])
        adNode.LimitScaleMaxY.set(limSy[2])
        adNode.LimitScaleMinZ.set(limSz[0])
        adNode.LimitScaleMaxZ.set(limSz[2])
        self._refresh()


    #--- edit UI ---------------------------------------------------------------
    def _clearList(self, *args):
        pm.textScrollList(self._tsl, ra=True, e=True)


    def _addMenuList(self, *args):
        pm.menuItem(l='Update', c=pm.Callback(self._getADNNode),
                    i='{0}/update.png'.format(self._idir))
        pm.menuItem(d=True, l='List')
        pm.menuItem(l='Select', c=pm.Callback(self._selectAdn), 
                    i='{0}/select.png'.format(self._idir))
        pm.menuItem(l='Select All', c=pm.Callback(self._selectAllAdn), 
                    i='{0}/select.png'.format(self._idir))
        pm.menuItem(l='Pin', c=pm.Callback(self._pinAdn), 
                    i='{0}/pinned.png'.format(self._idir))
        pm.menuItem(l='Unpin', c=pm.Callback(self._unpinAdn),
                    i='{0}/unpinned.png'.format(self._idir))
        pm.menuItem(l='Get from Selection', c=pm.Callback(self._getFromSelection), 
                    i='{0}/getFromSelection.png'.format(self._idir))
        pm.menuItem(l='Add from Selection', c=pm.Callback(self._addFromSelection), 
                    i='{0}/getFromSelection.png'.format(self._idir))
        pm.menuItem(d=True, l='I/O')
        pm.menuItem(l='Copy', c=pm.Callback(self._copyAdn),
                    i='{0}/copy2.png'.format(self._idir))
        pm.menuItem(l='Paste', c=pm.Callback(self._pasteAdn),
                    i='{0}/paste.png'.format(self._idir))
        pm.menuItem(l='Clear', c=pm.Callback(self._cleanTemp),
                    i='{0}/clear.png'.format(self._idir))
        pm.menuItem(l='Import', c=pm.Callback(self._importCsv),
                    i='{0}/import.png'.format(self._idir))
        pm.menuItem(l='Export All', c=pm.Callback(self._exportCsv),
                    i='{0}/export.png'.format(self._idir))
        pm.menuItem(l='Export Selection', c=pm.Callback(self._exportCsvFromSelection),
                    i='{0}/export.png'.format(self._idir))
        pm.menuItem(d=True, l='delete')
        pm.menuItem(l='Delete', c=pm.Callback(self._deleteAdn),
                    i='{0}/delete.png'.format(self._idir))
        pm.menuItem(l='Delete All', c=pm.Callback(self._deleteAllAdn),
                    i='{0}/delete.png'.format(self._idir))
        pm.menuItem(d=True, l='check')
        pm.menuItem(l='Delete error nodes.', c=pm.Callback(self._deleteErrorAdn),
                    i='{0}/delete.png'.format(self._idir))
        pm.menuItem(l='Set CommentField', c=pm.Callback(self._setDD),
                    i='{0}/copy.png'.format(self._idir))

    #--- main UI ---------------------------------------------------------------
    def main(self):               
        self.checkWindowOverlap()
        window = pm.window(self.windowManageName,
                           t  = self.windowTitle,
                           w  = self.windowSize[0],
                           h  = self.windowSize[1],
                           mb = True)

        #-- menu ---------------------------------------------------------------
        pm.menu(l='Display', to=False)
        self._cmMn = pm.menuItem(l='Manipulator', cb=True)
        pm.menuItem(d=True)
        pm.menuItem(l='All', c=pm.Callback(self._allCheck))
        pm.menuItem(l='None', c=pm.Callback(self._allOff))
        pm.menuItem(d=True)
        self._cmCr = pm.menuItem(l='CopyRotate', cb=True)
        self._cmAr = pm.menuItem(l='AxisRoll', cb=True)
        self._cmAb = pm.menuItem(l='AxisRollBlend', cb=True)
        self._cmAm = pm.menuItem(l='AxisMove', cb=True)
        self._cmRm = pm.menuItem(l='RollMove', cb=True)
        self._cmYp = pm.menuItem(l='YawPitchRotate', cb=True)
        self._cmRs = pm.menuItem(l='RollScale', cb=True)
        pm.menu(l='Tools', to=False)
        self._addMenuList()
        pm.menu(l='Help', hm=True)
        pm.menuItem(l='Maya 2019 HELP', c=self.show_mayaHelp)
        pm.menuItem(d=True)
        pm.menuItem(l='Tool HELP', c=self.show_toolHelp)

        #-- layout -------------------------------------------------------------
        #-- Pane Layout
        self._fmL = pm.formLayout(nd=100, h=600)
        self.sep0 = pm.separator()
        self.pnL0 = pm.paneLayout(cn='vertical2', h=500)

        #-- form Layout : Assist Drive node list -------------------------------
        self._fm_ = pm.formLayout(nd=100, w=200)
        self._tfn = pm.textFieldGrp(l='', tx='', pht='Search...')
        self._ibp = pm.iconTextCheckBox()
        self._tsl = pm.textScrollList(ams=True)
        self._pmADL = pm.popupMenu(b=3)
        self._addMenuList()
        self._txN = pm.text(l='view  0  /  All  0  nodes.')
        pm.setParent('..') #-- End of self._fm_

        #-----------------------------------------------------------------------
        #-- form layout : Functions --------------------------------------------
        self._scL = pm.scrollLayout(cr=True, w=400)
        self._clL = pm.columnLayout(adj=True)

        #-- create Assist drive ------------------------------------------------
        self.fmL0 = pm.formLayout(nd=100, w=340)
        self._opm = pm.optionMenu(l='Type:')
        pm.menuItem(l='CopyRotate')
        pm.menuItem(l='AxisRoll')
        pm.menuItem(l='AxisRollBlend')
        pm.menuItem(l='AxisMove')
        pm.menuItem(l='RollMove')
        pm.menuItem(l='YawPitchRotate')
        pm.menuItem(l='RollScale')
        self._osd = pm.optionMenu(l='')
        pm.menuItem(l='Center')
        pm.menuItem(l='Left')
        pm.menuItem(l='Right')
        pm.menuItem(l='None')
        self._ptx1 = pm.text(l='ADN_CR_')
        self._ptx2 = pm.text(l='')
        self._tfan = pm.textFieldGrp(l='', tx='', pht='Name...')
        self._ckko = pm.checkBox(l='Keep Offset', v=True)
        self._opAx = pm.optionMenu(l='Axis')
        self._miax0 = pm.menuItem(l='+ X')
        self._miax1 = pm.menuItem(l='+ Y')
        self._miax2 = pm.menuItem(l='+ Z')
        self._miax3 = pm.menuItem(l='- X')
        self._miax4 = pm.menuItem(l='- Y')
        self._miax5 = pm.menuItem(l='- Z')
        self._ibt0 = pm.iconTextButton(l='Create')
        pm.setParent('..') #-- End of self.fmL0

        #-- edit ---------------------------------------------------------------
        self._fmLA = pm.formLayout(nd=100, w=340)
        self._sep1 = pm.separator(st='in', h=10)
        self._ibtu = pm.iconTextButton(l='Update')
        self._ibt1 = pm.iconTextButton(l='Delete')
        self._ibt2 = pm.iconTextButton(l='Delete All')
        self._ibtg = pm.iconTextButton(l='Get')
        self._ibta = pm.iconTextButton(l='Add')
        self._ibt5 = pm.iconTextButton(l='Copy')
        self._ibt6 = pm.iconTextButton(l='paste')
        self._cbMn = pm.checkBox(l='Manipulator')
        self._txCP = pm.text(l=' ')
        self._pmCP = pm.popupMenu(b=3)
        self._miCP0 = pm.menuItem(l='Clear')
        pm.setParent('..') #-- End of self.fmLA

        #-- import / export ----------------------------------------------------
        self._fmLB = pm.formLayout(nd=100, w=340)
        self._spio = pm.separator(st='in', h=10)
        self._tfpa = pm.textFieldGrp(l='', tx=pm.workspace(q=True, rd=True))
        self._ibt3 = pm.iconTextButton(l='Import ')
        self._ibt4 = pm.iconTextButton(l='Export All')
        self._ibtE = pm.iconTextButton(l='Export Sel')
        pm.setParent('..') #-- End of self.fmLB

        #-- Assist drive info --------------------------------------------------
        self._fmLC = pm.formLayout(nd=100)
        self._sp1 = pm.separator(st='in', h=10)
        self._tfa = pm.textFieldGrp(l='Name ', tx='')
        self._tf0 = pm.textFieldGrp(l='Source ', tx='')
        self._pmSrc = pm.popupMenu(b=3)
        self._miSr0 = pm.menuItem(l='Select')
        self._tf1 = pm.textFieldGrp(l='Target ', tx='')
        self._pmTgt = pm.popupMenu(b=3)
        self._mitg0 = pm.menuItem(l='Select')
        self._tf2 = pm.textFieldGrp(l='Drive Type ', tx='', ed=False)
        self._tf3 = pm.textFieldGrp(l='Comment Field ', tx='')
        self._pmSCF = pm.popupMenu(b=3)
        self._miCF0 = pm.menuItem(l='Set CommentField')
        pm.setParent('..') #-- End of self.fmL2
        #pm.setParent('..') #-- End of self._clL

        #-----------------------------------------------------------------------
        #-- Assist Drive Attributes --------------------------------------------
        #self.clL0 = pm.columnLayout(adj=True)
        self.clL1 = pm.columnLayout(adj=True) #-- Copy Rotate ------------------
        self._sp3 = pm.separator(st='in', h=20)
        self._fs1 = pm.floatSliderGrp(l='Rotate Rate ', f=True)
        self._ff1 = pm.floatFieldGrp(l='Rotate Offset ', nf=3)
        pm.setParent('..') #-- End of self.clL1

        self.clL2 = pm.columnLayout(adj=True) #-- Axis Roll --------------------
        self._sp4 = pm.separator(st='in', h=20)
        self._ff2 = pm.floatFieldGrp(l='Roll Axis ', nf=3)
        self._fs2 = pm.floatSliderGrp(l='Roll Rate ', f=True)
        self._ff3 = pm.floatFieldGrp(l='Rotate Offset ', nf=3)
        pm.setParent('..') #-- End of self.clL2

        self.clL3 = pm.columnLayout(adj=True) #-- Axis Roll Blend --------------
        self._sp5 = pm.separator(st='in', h=20)
        self._ff4 = pm.floatFieldGrp(l='Roll Axis ', nf=3)
        self._fs3 = pm.floatSliderGrp(l='Roll Rate ', f=True)
        self._fs4 = pm.floatSliderGrp(l='Etc Rate ', f=True)
        self._ff5 = pm.floatFieldGrp(l='Rotate Offset ', nf=3)
        pm.setParent('..') #-- End of self.clL3

        self.clL4 = pm.columnLayout(adj=True) #-- Axis Move --------------------
        self._sp6 = pm.separator(st='in', h=20)
        self._ff6  = pm.floatFieldGrp(l='Roll Axis ', nf=3)
        self._ff7  = pm.floatFieldGrp(l='Move Axis ', nf=3)
        self._ff8  = pm.floatFieldGrp(l='Move Offset ', nf=3)
        self._ff9  = pm.floatFieldGrp(l='Move Length ', nf=1)
        self._ff10 = pm.floatFieldGrp(l='Move Range ', nf=2)
        self._opm1 = pm.optionMenuGrp(l='Ease Type ')
        pm.menuItem(l='Liner')
        pm.menuItem(l='EaseIn')
        pm.menuItem(l='EaseOut')
        pm.menuItem(l='EaseInOut')
        pm.setParent('..') #-- End of self.clL4

        self.clL5 = pm.columnLayout(adj=True) #-- Roll Move --------------------
        self._sp7 = pm.separator(st='in', h=20)
        self._ff11 = pm.floatFieldGrp(l='Roll Axis ', nf=3)
        self._ff12 = pm.floatFieldGrp(l='Move Axis ', nf=3)
        self._ff13 = pm.floatFieldGrp(l='Move Offset ', nf=3)
        self._ff14 = pm.floatFieldGrp(l='Move Length ', nf=1)
        self._ff15 = pm.floatFieldGrp(l='Move Range ', nf=2)
        self._opm2 = pm.optionMenuGrp(l='Ease Type ')
        pm.menuItem(l='Liner')
        pm.menuItem(l='EaseIn')
        pm.menuItem(l='EaseOut')
        pm.menuItem(l='EaseInOut')
        pm.setParent('..') #-- End of self.clL5

        self.clL6 = pm.columnLayout(adj=True) #-- Yaw Pitch Rotate -------------
        self._sp8 = pm.separator(st='in', h=20)
        self._is0  = pm.intSliderGrp(l='Roll Type ', f=True)
        self._fs5  = pm.floatSliderGrp(l='Yaw Rate ', f=True)
        self._ff16 = pm.floatFieldGrp(l='Yaw Limit ', nf=2)
        self._fs6  = pm.floatSliderGrp(l='Pitch Rate ', f=True)
        self._ff17 = pm.floatFieldGrp(l='Pitch Limit ', nf=2)
        self._ff18 = pm.floatFieldGrp(l='Rotate Offset ', nf=3)
        pm.setParent('..') #-- End of self.clL6

        self.clL7 = pm.columnLayout(adj=True) #-- Roll Scale -------------------
        self._sp9 = pm.separator(st='in', h=20)
        self._ff19 = pm.floatFieldGrp(l='Roll Axis ', nf=3)
        self._ff20 = pm.floatFieldGrp(l='Scale Length ', nf=3)
        self._opm3 = pm.optionMenuGrp(l='Ease Type ')
        pm.menuItem(l='Liner')
        pm.menuItem(l='EaseIn')
        pm.menuItem(l='EaseOut')
        pm.menuItem(l='EaseInOut')
        pm.setParent('..') #-- End of self.clL7

        #-----------------------------------------------------------------------
        #-- Limit Attributes ---------------------------------------------------
        self.fmL3  = pm.formLayout(nd=100)
        self._sp10 = pm.separator(st='in', h=10)
        self._ttx0 = pm.text('Min')
        self._ttx1 = pm.text('Current')
        self._ttx2 = pm.text('Max')
        self._ttx3 = pm.text('Min/Max')
        self._tlf0 = pm.floatFieldGrp(l='Limit Trans X ', nf=3)
        self._tmi0 = pm.checkBox(l='')
        self._tmx0 = pm.checkBox(l='')
        self._tlf1 = pm.floatFieldGrp(l='Limit Trans Y ', nf=3)
        self._tmi1 = pm.checkBox(l='')
        self._tmx1 = pm.checkBox(l='')
        self._tlf2 = pm.floatFieldGrp(l='Limit Trans Z ', nf=3)
        self._tmi2 = pm.checkBox(l='')
        self._tmx2 = pm.checkBox(l='')
        pm.setParent('..') #-- End of self.fmL3

        self.fmL4  = pm.formLayout(nd=100)
        self._sp11 = pm.separator(st='in', h=10)
        self._rtx0 = pm.text('Min')
        self._rtx1 = pm.text('Current')
        self._rtx2 = pm.text('Max')
        self._rtx3 = pm.text('Min/Max')
        self._rlf0 = pm.floatFieldGrp(l='Limit Rotate X ', nf=3)
        self._rmi0 = pm.checkBox(l='')
        self._rmx0 = pm.checkBox(l='')
        self._rlf1 = pm.floatFieldGrp(l='Limit Rotate Y ', nf=3)
        self._rmi1 = pm.checkBox(l='')
        self._rmx1 = pm.checkBox(l='')
        self._rlf2 = pm.floatFieldGrp(l='Limit Rotate Z ', nf=3)
        self._rmi2 = pm.checkBox(l='')
        self._rmx2 = pm.checkBox(l='')
        pm.setParent('..') #-- End of self.fmL4

        self.fmL5  = pm.formLayout(nd=100)
        self._sp12 = pm.separator(st='in', h=10)
        self._stx0 = pm.text('Min')
        self._stx1 = pm.text('Current')
        self._stx2 = pm.text('Max')
        self._stx3 = pm.text('Min/Max')
        self._slf0 = pm.floatFieldGrp(l='Limit Scale X ', nf=3)
        self._smi0 = pm.checkBox(l='')
        self._smx0 = pm.checkBox(l='')
        self._slf1 = pm.floatFieldGrp(l='Limit Scale Y ', nf=3)
        self._smi1 = pm.checkBox(l='')
        self._smx1 = pm.checkBox(l='')
        self._slf2 = pm.floatFieldGrp(l='Limit Scale Z ', nf=3)
        self._smi2 = pm.checkBox(l='')
        self._smx2 = pm.checkBox(l='')
        pm.setParent('..') #-- End of self.fmL5
        pm.setParent('..') #-- End of self._scL
        pm.setParent('..') #-- End of self.clL0
        pm.setParent('..') #-- End of self.pnL0
        self._hpl = pm.helpLine(h=20, w=100, bgc=(0.15, 0.15, 0.15))


        #-----------------------------------------------------------------------
        #--- Edit UI elements --------------------------------------------------
        pm.menuItem(self._cmMn, 
                    c=pm.Callback(self._toggleManipulator, ckb=0), e=True)
        pm.menuItem(self._cmCr, c=pm.Callback(self._checkBoxAdn), e=True)
        pm.menuItem(self._cmAr, c=pm.Callback(self._checkBoxAdn), e=True)
        pm.menuItem(self._cmAb, c=pm.Callback(self._checkBoxAdn), e=True)
        pm.menuItem(self._cmAm, c=pm.Callback(self._checkBoxAdn), e=True)
        pm.menuItem(self._cmRm, c=pm.Callback(self._checkBoxAdn), e=True)
        pm.menuItem(self._cmYp, c=pm.Callback(self._checkBoxAdn), e=True)
        pm.menuItem(self._cmRs, c=pm.Callback(self._checkBoxAdn), e=True)

        pm.textFieldGrp(self._tfn, adj=2, h=28, cw2=[0,100], 
                        tcc=pm.Callback(self._searchAdn), e=True)

        pm.iconTextCheckBox(self._ibp, st='iconOnly', 
                            i1='{0}/unpinned.png'.format(self._idir),
                            si='{0}/pinned.png'.format(self._idir),
                            onc=pm.Callback(self._pinAdn), 
                            ofc=pm.Callback(self._unpinAdn),
                            h=22, w=22, e=True)

        pm.textScrollList(self._tsl, sc=pm.Callback(self._refreshADNInfo), 
                          dcc=pm.Callback(self._selectAdn), e=True)

        pm.text(self._txN, al='right', e=True)

        pm.optionMenu(self._opm, h=24, cc=pm.Callback(self._changeAdn), e=True)
        pm.optionMenu(self._osd, h=24, w=102, cc=pm.Callback(self._changeSide), e=True)
        pm.textFieldGrp(self._tfan, adj=2, h=26, cw2=[0,100], e=True)
        pm.optionMenu(self._opAx, h=24, w=100, en=False, e=True)
        pm.iconTextButton(self._ibt0, c=pm.Callback(self._createAdn),
        st='iconAndTextHorizontal', i1='{0}/adnCreate.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)


        pm.iconTextButton(self._ibtu, c=pm.Callback(self._getADNNode),
        st='iconAndTextHorizontal', i1='{0}/update.png'.format(self._idir),
        h=24, w=110, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibt1, c=pm.Callback(self._deleteAdn),
        st='iconAndTextHorizontal', i1='{0}/delete.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibt2, c=pm.Callback(self._deleteAllAdn),
        st='iconAndTextHorizontal', i1='{0}/delete.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibtg, c=pm.Callback(self._getFromSelection),
        st='iconAndTextHorizontal', i1='{0}/getFromSelection.png'.format(self._idir),
        h=24, w=70, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibta, c=pm.Callback(self._addFromSelection),
        st='iconAndTextHorizontal', i1='{0}/getFromSelection.png'.format(self._idir),
        h=24, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibt5, c=pm.Callback(self._copyAdn),
        st='iconAndTextHorizontal', i1='{0}/copy2.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False, en=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibt6, c=pm.Callback(self._pasteAdn),
        st='iconAndTextHorizontal', i1='{0}/paste.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False, en=False,
        ann=self._an_ibt, e=True)

        pm.checkBox(self._cbMn, v=True, 
                    cc=pm.Callback(self._toggleManipulator, ckb=1), e=True)

        pm.text(self._txCP, al='right', en=False, e=True)
        pm.menuItem(self._miCP0, i='{0}/clear.png'.format(self._idir),
        c=pm.Callback(self._cleanTemp), e=True)


        pm.textFieldGrp(self._tfpa, adj=2, h=26, cw2=[0,100], e=True)

        pm.iconTextButton(self._ibt3, c=pm.Callback(self._importCsv),
        st='iconAndTextHorizontal', i1='{0}/import.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibt4, c=pm.Callback(self._exportCsv),
        st='iconAndTextHorizontal', i1='{0}/export.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.iconTextButton(self._ibtE, c=pm.Callback(self._exportCsvFromSelection),
        st='iconAndTextHorizontal', i1='{0}/export.png'.format(self._idir),
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, fla=False,
        ann=self._an_ibt, e=True)

        pm.textFieldGrp(self._tfa, adj=2, h=24, cw2=[80, 215], 
                        tcc=pm.Callback(self._setName), e=True)
        pm.textFieldGrp(self._tf0, adj=2, h=24, cw2=[80, 80], ed=False, e=True)
        pm.textFieldGrp(self._tf1, adj=2, h=24, cw2=[60, 80], ed=False, e=True)

        pm.menuItem(self._miSr0, c=pm.Callback(self._selSrc), e=True)
        pm.menuItem(self._mitg0, c=pm.Callback(self._selTgt), e=True)


        pm.textFieldGrp(self._tf2, adj=2, h=24, cw2=[80, 215], e=True)
        pm.textFieldGrp(self._tf3, adj=2, h=24, cw2=[80, 215],
                        tcc=pm.Callback(self._setCommentField), e=True)

        pm.menuItem(self._miCF0, c=pm.Callback(self._setDDComment), e=True)

        #-- clL1 | Copy Rotate -------------------------------------------------
        pm.floatSliderGrp(self._fs1, adj=3, h=24, cw3=[90, 70, 100], 
        min=-1.0, max=1.0, v=0.5, pre=3, cc=pm.Callback(self._setCRAttr), e=True)
        pm.floatFieldGrp(self._ff1, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setCRAttr), e=True)

        #-- clL2 | Axis Roll ---------------------------------------------------
        pm.floatFieldGrp(self._ff2, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setARAttr), e=True)
        pm.floatSliderGrp(self._fs2, adj=3, h=24, cw3=[90, 70, 110], 
        min=-1.0, max=1.0, v=0.5, pre=3, cc=pm.Callback(self._setARAttr), e=True)
        pm.floatFieldGrp(self._ff3, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setARAttr), e=True)

        #-- clL3 | Axis Roll Blend ---------------------------------------------
        pm.floatFieldGrp(self._ff4, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setABAttr), e=True)
        pm.floatSliderGrp(self._fs3, adj=3, h=24, cw3=[90, 70, 110], 
        min=-1.0, max=1.0, v=0.5, pre=3, cc=pm.Callback(self._setABAttr), e=True)
        pm.floatSliderGrp(self._fs4, adj=3, h=24, cw3=[90, 70, 110], 
        min=-1.0, max=1.0, v=0.5, pre=3, cc=pm.Callback(self._setABAttr), e=True)
        pm.floatFieldGrp(self._ff5, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setABAttr), e=True)

        #-- clL4 | Axis Move ---------------------------------------------------
        pm.floatFieldGrp(self._ff6, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setAMAttr), e=True)
        pm.floatFieldGrp(self._ff7, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setAMAttr), e=True)
        pm.floatFieldGrp(self._ff8, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setAMAttr), e=True)
        pm.floatFieldGrp(self._ff9, h=24, cw2=[90, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setAMAttr), e=True)
        pm.floatFieldGrp(self._ff10, h=24, cw3=[90, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setAMAttr), e=True)
        pm.optionMenuGrp(self._opm1, h=24, cw2=[90, 70], 
        cc=pm.Callback(self._setAMAttr), e=True)

        #-- clL5 | Roll Move ---------------------------------------------------
        pm.floatFieldGrp(self._ff11, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setRMMttr), e=True)
        pm.floatFieldGrp(self._ff12, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setRMMttr), e=True)
        pm.floatFieldGrp(self._ff13, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setRMMttr), e=True)
        pm.floatFieldGrp(self._ff14, h=24, cw2=[90, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setRMMttr), e=True)
        pm.floatFieldGrp(self._ff15, h=24, cw3=[90, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setRMMttr), e=True)
        pm.optionMenuGrp(self._opm2, h=24, cw2=[90, 70], 
        cc=pm.Callback(self._setRMMttr), e=True)

        #-- clL6 | Yaw Pitch Roll ----------------------------------------------
        pm.intSliderGrp(self._is0, adj=3, h=24, cw3=[90, 70, 110], 
        min=0, max=2, fmn=0, fmx=2, v=0, cc=pm.Callback(self._setYPAttr), e=True)
        pm.floatSliderGrp(self._fs5, adj=3, h=24, cw3=[90, 70, 110], 
        min=-1.0, max=1.0, v=0.5, pre=3, cc=pm.Callback(self._setYPAttr), e=True)
        pm.floatFieldGrp(self._ff16, h=24, cw3=[90, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setYPAttr), e=True)
        pm.floatSliderGrp(self._fs6, adj=3, h=24, cw3=[90, 70, 110], 
        min=-1.0, max=1.0, v=0.5, pre=3, cc=pm.Callback(self._setYPAttr), e=True)
        pm.floatFieldGrp(self._ff17, h=24, cw3=[90, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setYPAttr), e=True)
        pm.floatFieldGrp(self._ff18, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setYPAttr), e=True)

        #-- clL7 | Roll Scale --------------------------------------------------
        pm.floatFieldGrp(self._ff19, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setRSAttr), e=True)
        pm.floatFieldGrp(self._ff20, h=24, cw4=[90, 70, 70, 70], 
        v=[0.0, 0.0, 0.0, 0.0], pre=3, cc=pm.Callback(self._setRSAttr), e=True)
        pm.optionMenuGrp(self._opm3, h=24, cw2=[90, 70], 
        cc=pm.Callback(self._setRSAttr), e=True)

        #-- limit trans
        pm.floatFieldGrp(self._tlf0, h=24, cw4=[90, 70, 70, 70], 
        v1=0.0, v2=0.0, v3=0.0, en2=False, pre=3, cc=pm.Callback(self._setLimitTranslate), e=True)
        pm.checkBox(self._tmi0, w=18, cc=pm.Callback(self._setLimitTranslate), e=True)
        pm.checkBox(self._tmx0, w=18, cc=pm.Callback(self._setLimitTranslate), e=True)
        pm.floatFieldGrp(self._tlf1, h=24, cw4=[90, 70, 70, 70], 
        v1=0.0, v2=0.0, v3=0.0, en2=False, pre=3, cc=pm.Callback(self._setLimitTranslate), e=True)
        pm.checkBox(self._tmi1, w=18, cc=pm.Callback(self._setLimitTranslate), e=True)
        pm.checkBox(self._tmx1, w=18, cc=pm.Callback(self._setLimitTranslate), e=True)
        pm.floatFieldGrp(self._tlf2, h=24, cw4=[90, 70, 70, 70], 
        v1=0.0, v2=0.0, v3=0.0, en2=False, pre=3, cc=pm.Callback(self._setLimitTranslate), e=True)
        pm.checkBox(self._tmi2, w=18, cc=pm.Callback(self._setLimitTranslate), e=True)
        pm.checkBox(self._tmx2, w=18, cc=pm.Callback(self._setLimitTranslate), e=True)

        #-- limit rotate
        pm.floatFieldGrp(self._rlf0, h=24, cw4=[90, 70, 70, 70], 
        v1=0.0, v2=0.0, v3=0.0, en2=False, pre=3, cc=pm.Callback(self._setLimitRotate), e=True)
        pm.checkBox(self._rmi0, w=18, cc=pm.Callback(self._setLimitRotate), e=True)
        pm.checkBox(self._rmx0, w=18, cc=pm.Callback(self._setLimitRotate), e=True)
        pm.floatFieldGrp(self._rlf1, h=24, cw4=[90, 70, 70, 70], 
        v1=0.0, v2=0.0, v3=0.0, en2=False, pre=3, cc=pm.Callback(self._setLimitRotate), e=True)
        pm.checkBox(self._rmi1, w=18, cc=pm.Callback(self._setLimitRotate), e=True)
        pm.checkBox(self._rmx1, w=18, cc=pm.Callback(self._setLimitRotate), e=True)
        pm.floatFieldGrp(self._rlf2, h=24, cw4=[90, 70, 70, 70], 
        v1=0.0, v2=0.0, v3=0.0, en2=False, pre=3, cc=pm.Callback(self._setLimitRotate), e=True)
        pm.checkBox(self._rmi2, w=18, cc=pm.Callback(self._setLimitRotate), e=True)
        pm.checkBox(self._rmx2, w=18, cc=pm.Callback(self._setLimitRotate), e=True)

        #-- limit scale
        pm.floatFieldGrp(self._slf0, h=24, cw4=[90, 70, 70, 70], 
        v1=1.0, v2=1.0, v3=1.0, en2=False, pre=3, cc=pm.Callback(self._setLimitScale), e=True)
        pm.checkBox(self._smi0, w=18, cc=pm.Callback(self._setLimitScale), e=True)
        pm.checkBox(self._smx0, w=18, cc=pm.Callback(self._setLimitScale), e=True)
        pm.floatFieldGrp(self._slf1, h=24, cw4=[90, 70, 70, 70], 
        v1=1.0, v2=1.0, v3=1.0, en2=False, pre=3, cc=pm.Callback(self._setLimitScale), e=True)
        pm.checkBox(self._smi1, w=18, cc=pm.Callback(self._setLimitScale), e=True)
        pm.checkBox(self._smx1, w=18, cc=pm.Callback(self._setLimitScale), e=True)
        pm.floatFieldGrp(self._slf2, h=24, cw4=[90, 70, 70, 70], 
        v1=1.0, v2=1.0, v3=1.0, en2=False, pre=3, cc=pm.Callback(self._setLimitScale), e=True)
        pm.checkBox(self._smi2, w=18, cc=pm.Callback(self._setLimitScale), e=True)
        pm.checkBox(self._smx2, w=18, cc=pm.Callback(self._setLimitScale), e=True)

        #-----------------------------------------------------------------------
        #--- Edit UI Layout ----------------------------------------------------
        t, b , l, r = ['top', 'bottom', 'left', 'right']

        pm.formLayout(self._fmL, e=True,
               af = [(self.sep0, t,  0), (self.sep0, l, 0), (self.sep0, r, 0), 
                     (self.pnL0, t,  0), (self.pnL0, l, 0), (self.pnL0, r, 0), (self.pnL0, b, 30), 
                     (self._hpl, b,  5), (self._hpl, l, 5), (self._hpl, r, 5), 
                    ])

        pm.formLayout(self._fm_, e=True,
               af = [(self._tfn, t, 10), (self._tfn, l, 1), (self._tfn, r, 23), 
                     (self._ibp, t, 13), (self._ibp, r, 2), 
                     (self._tsl, t, 40), (self._tsl, l, 5), (self._tsl, r, 0), (self._tsl, b, 17), 
                     (self._txN, b,  0), (self._txN, r, 0), 
                    ])

        pm.formLayout(self.fmL0, e=True,
               af = [(self._opm, t,   12), (self._opm, l,   10), (self._opm, r, 115), 
                     (self._osd, t,   12), (self._osd, r,   10), 
                     (self._ptx1, t,  46), (self._ptx1, l,  10), 
                     (self._ptx2, t,  46), (self._ptx2, l,  60), 
                     (self._tfan, t,  40), (self._tfan, l,  75), (self._tfan, r,  4), 
                     (self._ckko, t,  74), (self._ckko, l,  10),
                     (self._opAx, t,  70), (self._opAx, r, 115),
                     (self._ibt0, t,  70), (self._ibt0, r,  10),
                    ])

        pm.formLayout(self._fmLA, e=True,
               af = [(self._sep1, t,  10), (self._sep1, l,   0), (self._sep1, r,  0), 
                     (self._ibtu, t,  30), (self._ibtu, l,  10), (self._ibtu, r, 220),
                     (self._ibt1, t,  30), (self._ibt1, r, 115),
                     (self._ibt2, t,  30), (self._ibt2, r,  10), 
                     (self._ibtg, t,  60), (self._ibtg, l,  10), 
                     (self._ibta, t,  60), (self._ibta, l,  85), (self._ibta, r, 220),
                     (self._ibt5, t,  60), (self._ibt5, r, 115),
                     (self._ibt6, t,  60), (self._ibt6, r,  10),
                     (self._cbMn, t,  95), (self._cbMn, l,  10), 
                     (self._txCP, t,  97), (self._txCP, r,  10),
                    ])

        pm.formLayout(self._fmLB, e=True,
               af = [(self._spio, t,  10), (self._spio, l,   0), (self._spio, r,  0), 
                     (self._tfpa, t,  20), (self._tfpa, l,   5), (self._tfpa, r,  5),
                     (self._ibt3, t,  50), (self._ibt3, l,  10), (self._ibt3, r, 220),
                     (self._ibt4, t,  50), (self._ibt4, r, 115), 
                     (self._ibtE, t,  50), (self._ibtE, r,  10), 
                    ])

        pm.formLayout(self._fmLC, e=True,
               af = [(self._sp1, t,  10), (self._sp1, l,   0), (self._sp1, r,   0), 
                     (self._tfa, t,  24), (self._tfa, l,  10), (self._tfa, r,   0), 
                     (self._tf0, t,  48), (self._tf0, l,  10), 
                     (self._tf1, t,  48), (self._tf1, r,   0), 
                     (self._tf2, t,  72), (self._tf2, l,  10), (self._tf2, r,   0), 
                     (self._tf3, t,  96), (self._tf3, l,  10), (self._tf3, r,   0), 
                    ],
               ap = [(self._tf0, r, 5, 50), (self._tf1, l, 5, 50)])

        pm.formLayout(self.fmL3, e=True,
               af = [(self._sp10, t,  10), (self._sp10, l,    0), (self._sp10, r,   0), 
                     (self._ttx0, t,  30), (self._ttx0, l,  120), 
                     (self._ttx1, t,  30), (self._ttx1, l,  180), 
                     (self._ttx2, t,  30), (self._ttx2, l,  260), 
                     (self._ttx3, t,  30), (self._ttx3, l,  310), 

                     (self._tlf0, t,  50), (self._tlf0, l,   0), 
                     (self._tmi0, t,  56), (self._tmi0, l, 315),  
                     (self._tmx0, t,  56), (self._tmx0, l, 335),  
                     (self._tlf1, t,  74), (self._tlf1, l,   0), 
                     (self._tmi1, t,  80), (self._tmi1, l, 315),  
                     (self._tmx1, t,  80), (self._tmx1, l, 335), 
                     (self._tlf2, t,  98), (self._tlf2, l,   0), 
                     (self._tmi2, t, 104), (self._tmi2, l, 315),  
                     (self._tmx2, t, 104), (self._tmx2, l, 335),  
                    ])

        pm.formLayout(self.fmL4, e=True,
               af = [(self._sp11, t,  10), (self._sp11, l,    0), (self._sp11, r,   0), 
                     (self._rtx0, t,  30), (self._rtx0, l,  120), 
                     (self._rtx1, t,  30), (self._rtx1, l,  180), 
                     (self._rtx2, t,  30), (self._rtx2, l,  260), 
                     (self._rtx3, t,  30), (self._rtx3, l,  310), 

                     (self._rlf0, t,  50), (self._rlf0, l,   0),  
                     (self._rmi0, t,  56), (self._rmi0, l, 315),  
                     (self._rmx0, t,  56), (self._rmx0, l, 335),  
                     (self._rlf1, t,  74), (self._rlf1, l,   0),  
                     (self._rmi1, t,  80), (self._rmi1, l, 315),  
                     (self._rmx1, t,  80), (self._rmx1, l, 335),  
                     (self._rlf2, t,  98), (self._rlf2, l,   0),  
                     (self._rmi2, t, 104), (self._rmi2, l, 315),  
                     (self._rmx2, t, 104), (self._rmx2, l, 335),  
                    ])

        pm.formLayout(self.fmL5, e=True,
               af = [(self._sp12, t,  10), (self._sp12, l,    0), (self._sp12, r,   0), 
                     (self._stx0, t,  30), (self._stx0, l,  120), 
                     (self._stx1, t,  30), (self._stx1, l,  170), 
                     (self._stx2, t,  30), (self._stx2, l,  260), 
                     (self._stx3, t,  30), (self._stx3, l,  310), 

                     (self._slf0, t,  50), (self._slf0, l,   0), 
                     (self._smi0, t,  56), (self._smi0, l, 315),  
                     (self._smx0, t,  56), (self._smx0, l, 335),  
                     (self._slf1, t,  74), (self._slf1, l,   0), 
                     (self._smi1, t,  80), (self._smi1, l, 315),  
                     (self._smx1, t,  80), (self._smx1, l, 335),
                     (self._slf2, t,  98), (self._slf2, l,   0), 
                     (self._smi2, t, 104), (self._smi2, l, 315),  
                     (self._smx2, t, 104), (self._smx2, l, 335),  
                    ])

        window.show()

        #-- init command -------------------------------------------------------
        self._getADNNode()
        self._adnHideUI()
        self._cleanTemp()
        self._createManipulator()
        #pm.scriptJob(uid=('adnAssistant', 'pm.mel.eval("AssistDriveManipulator -delete")'))
        pm.scriptJob(uid=('adnAssistant', pm.Callback(self._deleteManipulator)))
        
        pm.window(self.windowManageName, w=self.windowSize[0], h=self.windowSize[1], e=True)


def showUI():
    testIns = adnAssistantUI()
    testIns.main()

