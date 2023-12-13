# -*- coding: utf-8 -*-
from __future__ import absolute_import

#----- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import json


from . import _command
from . import _json


#from . import _command
#reload(_command)
#from . import _json
#reload(_json)

import tsubasa.maya.tools.skinweight as skinweight
import tsubasa.maya.tools.skinweighteditor.gui as skinWeightEditor 
import studiolibrary


class facialGuideUI(object):
    def __init__(self):
        self.__ver__     = '0.0.5'
        self.windowName  = 'FacialGuide'
        self.windowTitle = '{0} v{1}'.format(self.windowName, self.__ver__)
        self.windowSize  = [400, 260]
        self._maya_url   = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._help_url   = r'https://wisdom.cygames.jp/display/tsubasa/%5BMaya%5D+Facial+Guide'
        self._pl_url     = r'https://wisdom.cygames.jp/pages/viewpage.action?pageId=132198409'
        self._np_url     = r'https://wisdom.cygames.jp/pages/viewpage.action?pageId=158226586'
        #-- current script path ------------------------------------------------
        self.__dir = os.path.dirname(os.path.abspath(__file__))
        #-- image path ---------------------------------------------------------
        self._icon = r'{0}/_data/_icon'.format(self.__dir)
        #-- color
        self.btnBgc = (0.37, 0.37, 0.37)


    def checkWindowOverlap(self):
        if pm.window(self.windowName, ex=True):
            pm.deleteUI(self.windowName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._maya_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._help_url)


    def show_url(self, _url=r'', *args):
        webbrowser.open_new_tab(_url)

    #---------------------------------------------------------------------------
    #--- functions -------------------------------------------------------------
    def _checkMeshes(self, *args):
        if pm.objExists('msh_head'): 
            pm.textFieldGrp(self._um1, tx='msh_head', e=True)
        if pm.objExists('msh_face'): 
            pm.textFieldGrp(self._um1, tx='msh_face', e=True)
        if pm.objExists('msh_eye'): 
            pm.textFieldGrp(self._um2, tx='msh_eye', e=True)
        if pm.objExists('msh_teeth_top'): 
            pm.textFieldGrp(self._um3, tx='msh_teeth_top', e=True)
        if pm.objExists('msh_teeth_bottom'): 
            pm.textFieldGrp(self._um4, tx='msh_teeth_bottom', e=True)
        if pm.objExists('msh_tongue'): 
            pm.textFieldGrp(self._um5, tx='msh_tongue', e=True)
        if pm.objExists('msh_eyebrows'): 
            pm.textFieldGrp(self._um6, tx='msh_eyebrows', e=True)
        if pm.objExists('msh_eyelashes'): 
            pm.textFieldGrp(self._um7, tx='msh_eyelashes', e=True)


    def setFacialJoint(self, fcDict={}, *args):
        log = ''
        pos = (0,0,0)
        um1 = pm.textFieldGrp(self._um1, tx=True, q=True)
        um2 = pm.textFieldGrp(self._um2, tx=True, q=True)
        um3 = pm.textFieldGrp(self._um3, tx=True, q=True)
        um4 = pm.textFieldGrp(self._um4, tx=True, q=True)
        um5 = pm.textFieldGrp(self._um5, tx=True, q=True)
        # -- UM1 : msh_head
        # -- UM2 : msh_eye
        # -- UM3 : msh_teeth_top
        # -- UM4 : msh_teeth_bottom
        # -- UM5 : msh_tongue

        for k, v in fcDict.items():
            if v[0]:
                fcDict[k][0] = [i.replace('UM1', um1).replace('UM2', um2).replace('UM3', um3).replace('UM4', um4).replace('UM5', um5) for i in v[0]]

        for k, v in fcDict.items():
            if v[0]:
                try:
                    pm.select(v[0], r=True)
                    cp  = pm.selected()
                    pos = _command.getCenterPostion(cp)
                    pm.move(pos[0], pos[1], pos[2], k, a=True)
                    pm.move(v[1][0], v[1][1], v[1][2], k, r=True)
                except:
                    log += '{0} doesn\'t exist in this scene.\n'.format(v[0])
            else:
                pm.move(v[1][0], v[1][1], v[1][2], k, r=True)                
        print(log)


    def _importUM(self, _file_, *args):
        _path = r'{0}/_data/_mesh'.format(self.__dir)
        _command.importFile(_path, _file_, '.mb')


    def importJoint(self, *args):
        _path = r'{0}/_data/_joint'.format(self.__dir)

        tl = ['', 'pl', 'npc']
        tv = pm.radioButtonGrp(self._tp0, sl=True, q=True)

        _file = '_fc_joint_{0}'.format(tl[tv])
        _command.importFile(_path, _file, '.mb')


    def setJoint(self, *args):
        tl = ['', 'pl', 'npc']
        tv = pm.radioButtonGrp(self._tp0, sl=True, q=True)
        gl = ['', 'm', 'f']
        gv = pm.radioButtonGrp(self._tp1, sl=True, q=True)

        _file  = '_{0}_fc_{1}.json'.format(gl[gv], tl[tv])
        _path  = r'{0}/_data/_json/{1}'.format(self.__dir, _file)
        print(_path)
        fcDict = _json.importJson(_path)
        self.setFacialJoint(fcDict)


    def launchSkinWeight(self, *args):
        skinweight.main()


    def launchSkinWeightEditor(self, *args):
        skinWeightEditor.main()


    def launchStudioLibrary(self, *args):
        studiolibrary.main()


    def importFcWeight(self, *args):
        log = ''
        um1 = pm.textFieldGrp(self._um1, tx=True, q=True)
        um2 = pm.textFieldGrp(self._um2, tx=True, q=True)
        um3 = pm.textFieldGrp(self._um3, tx=True, q=True)
        um4 = pm.textFieldGrp(self._um4, tx=True, q=True)
        um5 = pm.textFieldGrp(self._um5, tx=True, q=True)
        um6 = pm.textFieldGrp(self._um6, tx=True, q=True)
        um7 = pm.textFieldGrp(self._um7, tx=True, q=True)

        tl = ['', 'pl', 'npc']
        tv = pm.radioButtonGrp(self._tp0, sl=True, q=True)
        gl = ['', 'm', 'f']
        gv = pm.radioButtonGrp(self._tp1, sl=True, q=True)

        _path = r'{0}/_data/_weightdata/_{1}_{2}'.format(self.__dir, tl[tv], gl[gv])
        _bw1  = r'{0}/msh_body.weightdata'.format(_path)
        _bw2  = r'{0}/msh_eye.weightdata'.format(_path)
        _bw3  = r'{0}/msh_teeth_top.weightdata'.format(_path)
        _bw4  = r'{0}/msh_teeth_bottom.weightdata'.format(_path)
        _bw5  = r'{0}/msh_tongue.weightdata'.format(_path)

        if skinweight.command.import_skinCluster_weights(um1, _bw1, 'index', True):
            log += 'weight copy {0} : {1}\n'.format(um1, _bw1)
        if skinweight.command.import_skinCluster_weights(um2, _bw2, 'index', True):
            log += 'weight copy {0} : {1}\n'.format(um1, _bw2)
        if skinweight.command.import_skinCluster_weights(um3, _bw3, 'index', True):
            log += 'weight copy {0} : {1}\n'.format(um1, _bw3)
        if skinweight.command.import_skinCluster_weights(um4, _bw4, 'index', True):
            log += 'weight copy {0} : {1}\n'.format(um1, _bw4)
        if skinweight.command.import_skinCluster_weights(um5, _bw5, 'index', True):
            log += 'weight copy {0} : {1}\n'.format(um1, _bw5)
        print(log)

        if tv == 1:
            #-- eyebrows
            if um6 and pm.objExists(um6):
                ebj = ['_830', '_831', '_832', '_833', '_838', '_839', '_83a', '_83b']
                pm.select(ebj, r=True)
                pm.select(um6, add=True)
                pm.skinCluster(tsb=True, bm=0, sm=0, nw=1, wd=0)

            #-- eyelashes
            if um7 and pm.objExists(um7):
                rlj = ['_8a0', '_843', '_842', '_841', '_840', '_84f', '_848', 
                       '_849', '_84a', '_837', '_8a1', '_852', '_853', '_858', 
                       '_851', '_850', '_859', '_85f', '_85a', '_83f', '_005']
                pm.select(rlj, r=True)
                pm.select(um7, add=True)
                tScl = pm.skinCluster(tsb=True, bm=0, sm=0, nw=1, wd=0)
                # -- weight copy
                sCls = pm.mel.eval('findRelatedSkinCluster {0};'.format(um1))
                mc.select(um1, r=True)
                mc.select(um7, add=True)
                mc.copySkinWeights(ss=sCls, ds=tScl.name(), sa='closestPoint', ia=['label', 'closestJoint'], nm=True)
        elif tv == 2:
            #-- eyebrows
            if um6 and pm.objExists(um6):
                ebj = ['_830', '_838']
                pm.select(ebj, r=True)
                pm.select(um6, add=True)
                pm.skinCluster(tsb=True, bm=0, sm=0, nw=1, wd=0)

            #-- eyelashes
            if um7 and pm.objExists(um7):
                rlj = ['_841', '_848', '_851', '_858', '_005']
                pm.select(rlj, r=True)
                pm.select(um7, add=True)
                tScl = pm.skinCluster(tsb=True, bm=0, sm=0, nw=1, wd=0)
                # -- weight copy
                sCls = pm.mel.eval('findRelatedSkinCluster {0};'.format(um1))
                mc.select(um1, r=True)
                mc.select(um7, add=True)
                mc.copySkinWeights(ss=sCls, ds=tScl.name(), sa='closestPoint', ia=['label', 'closestJoint'], nm=True)


    def setFcJointParent(self, *args):
        jtList = pm.ls('_fc_joint_GP', dag=True, typ='joint')
        for i in jtList:
            pa = i.getParent()
            pj = pa.name().replace('_fc_', '')
            if pm.objExists(pj):
                i.setParent(pj)
            else:
                pm.warning('{0} doesn\'t exist in this scene.'.format(pj))
        #-- _9ff
        if pm.objExists('_9ff') and pm.objExists('_005'):
            try:
                pm.parent('_9ff', '_005')
            except:
                pass
        #-- delete group
        pm.delete('_fc_joint_GP')


    def setJointLabel(self, v=1, *args):
        jtList = pm.ls('_8*', typ='joint')
        for i in jtList:
            i.drawLabel.set(v)


    #--- edit UI ---------------------------------------------------------------
    def _setMeshName(self, v=0, *args):
        sl = pm.selected()
        if sl:
            if v == 1:
                pm.textFieldGrp(self._um1, tx=sl[-1].name(), e=True)
            elif v == 2:
                pm.textFieldGrp(self._um2, tx=sl[-1].name(), e=True)
            elif v == 3:
                pm.textFieldGrp(self._um3, tx=sl[-1].name(), e=True)
            elif v == 4:
                pm.textFieldGrp(self._um4, tx=sl[-1].name(), e=True)
            elif v == 5:
                pm.textFieldGrp(self._um5, tx=sl[-1].name(), e=True)
            elif v == 6:
                pm.textFieldGrp(self._um6, tx=sl[-1].name(), e=True)
            elif v == 7:
                pm.textFieldGrp(self._um7, tx=sl[-1].name(), e=True)
        else:
            pm.warning('Please select one of universal mesh to be target.')


    def resetUI(self, *args):
        pm.radioButtonGrp(self._tp0, sl=1, e=True)
        pm.radioButtonGrp(self._tp1, sl=1, e=True)
        self._checkMeshes()


    #---------------------------------------------------------------------------
    #--- main UI ---------------------------------------------------------------
    def main(self):               
        self.checkWindowOverlap()
        window = pm.window(self.windowName,
                           t  = self.windowTitle,
                           w  = self.windowSize[0],
                           h  = self.windowSize[1],
                           mb = True)

        #--- menu
        pm.menu(l='Edit', to=False)
        pm.menuItem(l='Reset UI',
                    c=pm.Callback(self.resetUI))
        pm.menuItem(d=True, dl='Tools')
        pm.menuItem(l='Skin Weight',
                    c=pm.Callback(self.launchSkinWeight))
        pm.menuItem(l='Skin Weight Editor',
                    c=pm.Callback(self.launchSkinWeightEditor))
        pm.menuItem(l='Studio Library',
                    c=pm.Callback(self.launchStudioLibrary))
        pm.menuItem(d=True, dl='Universal Mesh')
        pm.menuItem(l='PL Male', c=pm.Callback(self._importUM, 'dbumpl_m'))        
        pm.menuItem(l='PL Female', c=pm.Callback(self._importUM, 'dbumpl_f'))  
        pm.menuItem(l='NPC Male', c=pm.Callback(self._importUM, 'dbumnp_m'))        
        pm.menuItem(l='NPC Female', c=pm.Callback(self._importUM, 'dbumnp_f'))  
        pm.menuItem(d=True, dl='Facial Joint')
        pm.menuItem(l='Joint Label : ON',
                    c=pm.Callback(self.setJointLabel, v=1))        
        pm.menuItem(l='Joint Label : OFF',
                    c=pm.Callback(self.setJointLabel, v=0))    
        pm.menu(l='Help', hm=True)
        pm.menuItem(l='Maya 2019 HELP', c=pm.Callback(self.show_mayaHelp))
        pm.menuItem(l='Tool HELP', c=pm.Callback(self.show_toolHelp))
        pm.menuItem(d=True)
        pm.menuItem(l='Facial Joint Nmae (PL)',
                    c=pm.Callback(self.show_url, self._pl_url))
        pm.menuItem(l='Facial Joint Nmae (NPC)',
                    c=pm.Callback(self.show_url, self._np_url))

        #--- base form layout
        self.fmL0 = pm.formLayout(nd=100)
        self.sep0 = pm.separator(w=230)

        self.fmL1 = pm.formLayout(nd=100)
        self._tp0 = pm.radioButtonGrp(l='Asset Type : ', nrb=2, la2=['PL', 'NPC'])
        self._tp1 = pm.radioButtonGrp(l='Gender : ', nrb=2, la2=['Male', 'Female'])
        #-- Universal mesh name-------------------------------------------------
        self._sp0 = pm.separator(st='in', w=230, h=30)
        pm.setParent('..') #-- End of self.fmL1

        self.fmL2 = pm.formLayout(nd=100)
        self._um1 = pm.textFieldGrp(l='head : ')
        self._ib1 = pm.iconTextButton(l='')
        self._um2 = pm.textFieldGrp(l='eye : ')
        self._ib2 = pm.iconTextButton(l='')
        self._um3 = pm.textFieldGrp(l='teeth top : ')
        self._ib3 = pm.iconTextButton(l='')
        self._um4 = pm.textFieldGrp(l='teeth bottom : ')
        self._ib4 = pm.iconTextButton(l='')
        self._um5 = pm.textFieldGrp(l='tongue : ')
        self._ib5 = pm.iconTextButton(l='')
        self._sp1 = pm.separator(st='in', w=230, h=20)
        pm.setParent('..') #-- End of self.fmL2

        self.fmL3 = pm.formLayout(nd=100)
        self._um6 = pm.textFieldGrp(l='eyebrows : ')
        self._ib6 = pm.iconTextButton(l='')
        self._um7 = pm.textFieldGrp(l='eyelashes : ')
        self._ib7 = pm.iconTextButton(l='')
        self._sp2 = pm.separator(st='in', w=230, h=30)
        pm.setParent('..') #-- End of self.fmL3

        #-- Function bottons ---------------------------------------------------
        self.fmL4 = pm.formLayout(nd=100)
        self._ijb = pm.iconTextButton(l='Import Joint')
        self._fmb = pm.iconTextButton(l='Fit to Model')
        self._iwb = pm.iconTextButton(l='Import Weight')
        self._spb = pm.iconTextButton(l='Set Parent')
        pm.setParent('..') #-- End of self.fmL4

        self.sepe = pm.separator(st='none', w=190, h=20)


        #-----------------------------------------------------------------------
        #--- Edit UI elements --------------------------------------------------
        pm.radioButtonGrp(self._tp0, 
        sl=1, cw3=(80, 70, 70), e=True)
        pm.radioButtonGrp(self._tp1,  
        sl=1, cw3=(80, 70, 70), e=True)

        pm.textFieldGrp(self._um1, tx='', cw2=(80, 140), h=24, e=True)
        pm.iconTextButton(self._ib1, c=pm.Callback(self._setMeshName, v=1),
        st='iconOnly', i1='{0}/add.png'.format(self._icon), h=16, w=16, e=True)

        pm.textFieldGrp(self._um2, tx='', cw2=(80, 140), h=24, e=True)
        pm.iconTextButton(self._ib2, c=pm.Callback(self._setMeshName, v=2),
        st='iconOnly', i1='{0}/add.png'.format(self._icon), h=16, w=16, e=True)

        pm.textFieldGrp(self._um3, tx='', cw2=(80, 140), h=24, e=True)
        pm.iconTextButton(self._ib3, c=pm.Callback(self._setMeshName, v=3),
        st='iconOnly', i1='{0}/add.png'.format(self._icon), h=16, w=16, e=True)

        pm.textFieldGrp(self._um4, tx='', cw2=(80, 140), h=24, e=True)
        pm.iconTextButton(self._ib4, c=pm.Callback(self._setMeshName, v=4),
        st='iconOnly', i1='{0}/add.png'.format(self._icon), h=16, w=16, e=True)

        pm.textFieldGrp(self._um5, tx='', cw2=(80, 140), h=24, e=True)
        pm.iconTextButton(self._ib5, c=pm.Callback(self._setMeshName, v=5),
        st='iconOnly', i1='{0}/add.png'.format(self._icon), h=16, w=16, e=True)

        pm.textFieldGrp(self._um6, tx='', cw2=(80, 140), h=24, e=True)
        pm.iconTextButton(self._ib6, c=pm.Callback(self._setMeshName, v=6),
        st='iconOnly', i1='{0}/add.png'.format(self._icon), h=16, w=16, e=True)

        pm.textFieldGrp(self._um7, tx='', cw2=(80, 140), h=24, e=True)
        pm.iconTextButton(self._ib7, c=pm.Callback(self._setMeshName, v=7),
        st='iconOnly', i1='{0}/add.png'.format(self._icon), h=16, w=16, e=True)


        #-- Function bottons ---------------------------------------------------
        pm.iconTextButton(self._ijb, c=pm.Callback(self.importJoint),
        st='iconAndTextHorizontal', i1='{0}/joint.png'.format(self._icon), 
        h=24, w=120, mw=7, bgc=self.btnBgc, e=True)

        pm.iconTextButton(self._fmb, c=pm.Callback(self.setJoint),
        st='iconAndTextHorizontal', i1='{0}/connect.png'.format(self._icon), 
        h=24, w=120, mw=7, bgc=self.btnBgc, e=True)

        pm.iconTextButton(self._iwb, c=pm.Callback(self.importFcWeight),
        st='iconAndTextHorizontal', i1='p-head.png'.format(self._icon), 
        h=24, w=120, mw=7, bgc=self.btnBgc, e=True)

        pm.iconTextButton(self._spb, c=pm.Callback(self.setFcJointParent),
        st='iconAndTextHorizontal', i1='selectObj.png'.format(self._icon), 
        h=24, w=120, mw=7, bgc=self.btnBgc, e=True)


        #-----------------------------------------------------------------------
        #--- Edit UI Layout ----------------------------------------------------
        t, b , l, r = ['top', 'bottom', 'left', 'right']

        pm.formLayout(self.fmL0, e=True,
               af = [(self.sep0, t,   0), (self.sep0, l, 0), (self.sep0, r, 0), 
                     (self.fmL1, t,  15), (self.fmL1, l, 0), (self.fmL1, r, 0), 
                     (self.fmL2, t,  90), (self.fmL2, l, 0), (self.fmL2, r, 0), 
                     (self.fmL3, t, 235), (self.fmL3, l, 0), (self.fmL3, r, 0), 
                     (self.fmL4, t, 320), (self.fmL4, l, 0), (self.fmL4, r, 0), 
                     (self.sepe, b,   0), (self.sepe, l, 0), (self.sepe, r, 0), 
                    ])

        pm.formLayout(self.fmL1, e=True,
               af = [(self._tp0, t,   0), (self._tp0, l,  10),
                     (self._tp1, t,  25), (self._tp1, l,  10),
                     (self._sp0, b,   0), (self._sp0, l,   5), (self._sp0, r,  5),
                    ])

        pm.formLayout(self.fmL2, e=True,   
               af = [(self._um1, t,   0), (self._um1, l,  10), (self._um1, r, 30),
                     (self._um2, t,  25), (self._um2, l,  10), (self._um2, r, 30),
                     (self._um3, t,  50), (self._um3, l,  10), (self._um3, r, 30),
                     (self._um4, t,  75), (self._um4, l,  10), (self._um4, r, 30),
                     (self._um5, t, 100), (self._um5, l,  10), (self._um5, r, 30),
                     (self._ib1, t,   5), (self._ib1, l, 240),
                     (self._ib2, t,  30), (self._ib2, l, 240),
                     (self._ib3, t,  55), (self._ib3, l, 240),
                     (self._ib4, t,  80), (self._ib4, l, 240),
                     (self._ib5, t, 105), (self._ib5, l, 240),
                     (self._sp1, b,   0), (self._sp1, l,   5), (self._sp1, r,  5),
                    ])

        pm.formLayout(self.fmL3, e=True,   
               af = [(self._um6, t,   0), (self._um6, l,  10), (self._um6, r, 30),
                     (self._um7, t,  25), (self._um7, l,  10), (self._um7, r, 30),
                     (self._ib6, t,   5), (self._ib6, l, 240),
                     (self._ib7, t,  30), (self._ib7, l, 240),
                     (self._sp2, b,   0), (self._sp2, l,   5), (self._sp2, r,  5),
                    ])

        pm.formLayout(self.fmL4, e=True,  
               af = [(self._ijb, t,   0), (self._ijb, l,  10),
                     (self._fmb, t,   0), (self._fmb, l, 140),
                     (self._iwb, t,  30), (self._iwb, l,  10),
                     (self._spb, t,  30), (self._spb, l, 140),
                    ])


        window.show()


        #-- init command -------------------------------------------------------
        self._checkMeshes()


def showUI():
    testIns = facialGuideUI()
    testIns.main()
