# -*- coding: utf-8 -*-
from __future__ import absolute_import

#----- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import json

from . import command
from . import build
from . import guide
from . import setup

import importlib

importlib.reload(command)
importlib.reload(build)
importlib.reload(guide)
importlib.reload(setup)

def exportJson(path=r'', dict={}):
    f = open(path, 'w')
    json.dump(dict, f, indent=4)
    f.close()


def importJson(path=r''):
    f = open(path, 'r')
    tmp = f.read()
    res = json.loads(tmp)
    f.close()
    return res


class baseBodyBuilderUI(object):
    def __init__(self):
        self.__ver__       = '0.0.8'
        self.windowName    = 'baseBodyBuilder'
        self.windowTitle   = 'BBB v{0}'.format(self.__ver__)
        self.windowSize    = [200, 300]
        self._mayaHelp_url = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._toolHelp_url = r'https://wisdom.cygames.jp/x/SOB_C'
        #--- current script path -----------------------------------------------
        self.__dir = os.path.dirname(os.path.abspath(__file__))
        #-- image path ---------------------------------------------------------
        self._idir = os.path.join(self.__dir, r'_data/_icon').replace('\\', '/')
        #-- color --------------------------------------------------------------
        self.btnBgc = (0.37, 0.37, 0.37)
        self.frmBgc = (0.11, 0.11, 0.11)
        self.fomBgc = (0.25, 0.25, 0.25)
        self.txfBgc = (0.15, 0.15, 0.15)
        #-- annotation ---------------------------------------------------------
        self._an_ibt = u'ガイドをインポートします。'
        self._an_imb = u'Jointにガイドをスナップします。'
        self._an_ckb = u'移動ツール階層保持オプション'
        self._an_afg = u'手の指のガイドを揃えます。'
        self._an_aft = u'足のガイドを揃えます。'
        self._an_cbt = u'Biped(二足)の設定でビルド'
        self._an_nbt = u'Quadruped(四足)の設定でビルド'

        self._an_smb = u'スキンのインポート'
        self._an_ftb = u'スキンをJointにスナップします。'

        self._an_tpt = u'0～10fでTポーズを設定します。'
        self._an_chb = u'キャラクターノードの作成とマッピング'

        self._an_ict = u'基本コントローラーのインポート'
        self._an_ctw = u'選択したオブジェクトにwldを作成'
        self._an_cnw = u'2つ選択したノード間にwldコネクションを作成'

        self._an_rfm = u'チェックモーションデータのリファレンス'
        self._an_imm = u'チェックモーションデータのインポート'


    def checkWindowOverlap(self):
        if pm.window(self.windowName, ex=True):
            pm.deleteUI(self.windowName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)


    #--- functions -------------------------------------------------------
    def importFile(self, path=r'', f='', ext='.mb'):
        path = os.path.join(path, f'{f}.{ext}')
        mc.file(path, i=True, typ='mayaBinary', iv=True, ra=True, mnc=True, 
                ns=':', op='v=0;', pr=True, ifr=False, itr='keep')


    def importGuide(self, *args):
        std  = os.path.join(self.__dir, '_data/_guide')
        path = mc.fileDialog2(ff='*.mb', fm=1, ds=2, cap='Import Guide Data',
                              dir=std, okc='Import', cc='Cancel')
        if path: #-- import guide
            mc.file(path[0], i=True, typ='mayaBinary', iv=True, mnc=False, 
                    rpr='_guide', op='v=0;', pr=True, itr='keep')


    def saveGuide(self, *args):
        std  = os.path.join(self.__dir, '_data/_guide')
        path = mc.fileDialog2(ff='*.mb', ds=2, cap='Save Guide Data', 
                              dir=std, okc='Save', cc='Cancel')
        if path: #-- Export guide
            mc.select('_guide_GP', r=True)
            mc.file(path, f=True, op='v=0;', typ='mayaBinary', pr=True, es=True) 


    def fitGuideToSkeleton(self, *args):
        info = self.getHikDefinition(typ='pl')
        guide.fitToSkeleton(info)


    def importMesh(self, *args):
        path = os.path.join(self.__dir, r'_data/_mesh')
        self.importFile(path, '_basebody', '.mb')


    def importSkinMesh(self, typ='', *args):
        if typ: typ = '_{0}'.format(typ)
        path = os.path.join(self.__dir, r'_data/_mesh')
        self.importFile(path, '_basebody_bind{0}'.format(typ), '.mb')


    def importDammy(self, *args):
        path = os.path.join(self.__dir, r'_data/_dammy')
        self.importFile(path, '_dammy_joint', '.mb')


    def setMoveToolOption(self, *args):
        val = pm.checkBox(self._ckb, v=True, q=True)
        command.setPreserveChildren(val)


    def getHikDefinition(self, typ='pl', *args):
        p = self.__dir
        f = r'_data/_json/_hik_{0}.json'.format(typ)
        _path = os.path.join(p, f)
        print (_path)
        info  = command.importJson(_path)
        return info


    #-- skeleton builde function
    def skeletonBuild(self, typ='biped', *args):
        info = self.getHikDefinition(typ=typ)
        pm.delete(pm.ls('*', typ='joint'))
        if typ == 'biped':
            build.testBuild(info)
        elif typ == 'quad':
            build.quadBuild(info)


    def testBuild(self, typ='pl', *args):
        info = self.getHikDefinition(typ=typ)
        if not pm.objExists('null'):
            build.testBuild(info)
        else:
            build.rebuild(info)


    def alignFinger(self, *args):
        guide.alignFingerGuide()


    def alignFoot(self, *args):
        guide.alignFootGuide()


    def fitToGuide(self, *args):
        info = self.getHikDefinition()
        log  = ''
        for k, v in info.items():
            if v[0]:
                pos = '{0}_pos'.format(v[0])
                if pm.objExists(pos):
                    if pm.objExists(v[0]):
                        #---- skeleton
                        tgt = v[0]
                        #--- fit 
                        pm.delete(pm.parentConstraint(tgt, pos, mo=False, w=1))
                    else:
                        g = '_{0}_guide'.format(v[1][0])
                        if pm.objExists(g):
                            tgt = g
                            #--- fit 
                            pm.delete(pm.pointConstraint(tgt, pos, mo=False, w=1))

                    log += 'skin fit : {0} -> {1} \n'.format(pos, tgt)
                else:
                    log += 'skin fit skip: {0} \n'.format(pos)
        print (log)


    #-- caracterize ------------------------------------------------------------
    def setPose(self, *args):
        info = self.getHikDefinition()
        command.setTimeSlider(info)


    def setDefinition(self, *args):
        info  = self.getHikDefinition()
        asset = ['_default']
        command.createCharacterDefinition(asset[0])
        chara = '{0}_character'.format(asset[0])
        if pm.objExists(chara):
            command.setCharacterDefinition(chara, info)


    def deleteAnimCurve(self, *args):
        command.deleteAnimKey()


    def importCtrl(self, *args):
        path = os.path.join(self.__dir, r'_data/_guide')
        if path:
            self.importFile(path, '_ctrl', 'mb')


    def _createWld(self, *args):
        tgt = mc.ls(sl=True)
        log = setup.wldMatrix(tgt)


    def _connectWld(self, *args):
        sel = mc.ls(sl=True)
        if len(sel) == 2:
            src = sel[0]
            tgt = sel[1]
            setup.worldConnection(src, tgt)
        else:
            pm.warning('Please select 2 objects as soruce and target.')


    def referenceMotion(self, *args):
        exf  = '*.mb'
        std  = os.path.join(self.__dir, r'_data/_motion/_mb')
        path = mc.fileDialog2(ff=exf, fm=1, ds=2, cap='Reference Motion Data',
                              dir=std, okc='Reference', cc='Cancel')
        if path:
            mc.file(path[0], r=True, typ='mayaBinary', iv=True, gl=False,
                    mnc=False, ns='_motion', op='v=0;')


    def importMotion(self, *args):
        #--- check keep motion
        val = pm.confirmDialog(t='Keep Root Position',
                               m='Does Root Joint "_000" keep position?', 
                               b=['Keep', 'As Motion', 'Cancel'], 
                               db='Yes', cb='Cancel', ds='Cancel')
        exf = '*.fbx'
        std = os.path.join(self.__dir, r'_data/_motion/_fbx')
        path = mc.fileDialog2(ff=exf, fm=1, ds=2,  cap='Import Motion Data',
                              dir=std, okc='Import', cc='Cancel')
        if path:
            mc.file(path[0], i=True,typ='FBX', iv=True, gl=False,
                    mnc=False, op='fbx', pr=True, itr='combine')


    #--- edit UI ----------------------------------------



    #--- main UI ----------------------------------------
    def main(self):               
        self.checkWindowOverlap()
        window = pm.window(self.windowName,
                           t  = self.windowTitle,
                           w  = self.windowSize[0],
                           h  = self.windowSize[1],
                           mb = True)

        #--- menu
        pm.menu(l='Tools', to=False)
        pm.menuItem(d=True, dl='Import')
        pm.menuItem(l='guide', i='{0}/p-add.png'.format(self._idir),
                    c=self.importGuide)
        pm.menuItem(l='low mesh', i='{0}/np-head.png'.format(self._idir),
                    c=self.importMesh)
        pm.menuItem(l='Import controller', i='{0}/ctrl.png'.format(self._idir),
                    c=self.importCtrl)
        pm.menuItem(l='dammy joint', i='{0}/joint.png'.format(self._idir),
                    c=self.importDammy)

        pm.menuItem(d=True, dl='Import Skin')
        pm.menuItem(l='Skin Mesh', i='{0}/np-head.png'.format(self._idir),
                    c=pm.Callback(self.importSkinMesh, typ=''))
        pm.menuItem(l='PL skin', i='{0}/np-head.png'.format(self._idir),
                    c=pm.Callback(self.importSkinMesh, typ='pl'))
        pm.menuItem(l='NPC skin', i='{0}/np-head.png'.format(self._idir),
                    c=pm.Callback(self.importSkinMesh, typ='npc'))
        
        pm.menu(l='Help', hm=True)
        pm.menuItem(l='Maya 2019 HELP', c=self.show_mayaHelp)
        pm.menuItem(d=True)
        pm.menuItem(l='Tool HELP', c=self.show_toolHelp)


        #-- base form layout 
        self.fmL0 = pm.formLayout(nd=100)
        self.sep0 = pm.separator(w=275)
        self.cmL0 = pm.columnLayout()


        #-----------------------------------------------------------------------
        #-- Guide --------------------------------------------------------------
        self.rLGd = pm.frameLayout(l='Guide')
        self.fLGd = pm.formLayout(nd=100)
        self._ibt = pm.iconTextButton(l='Import Guide')
        self.btsv = pm.iconTextButton(l='Save Guide')
        self._imb = pm.iconTextButton(l='Fit to Skeleton')
        self._ckb = pm.checkBox(l='Preserve Children')
        self._afg = pm.iconTextButton(l='Align finger')
        self._aft = pm.iconTextButton(l='Align foot')
        self._cbt = pm.iconTextButton(l='Build ( Biped )')
        self._nbt = pm.iconTextButton(l='Build ( Quad )')
        self.sep1 = pm.separator(st='none')
        pm.setParent('..') #-- end of self.fLGd
        pm.setParent('..') #-- end of self.rLGd


        #-----------------------------------------------------------------------
        #-- Edit ---------------------------------------------------------------
        self.rLEd = pm.frameLayout(l='Edit')
        self.fLEd = pm.formLayout(nd=100)
        self._smb = pm.iconTextButton(l='Import skin')
        self._ftb = pm.iconTextButton(l='Fit to Skeleton')
        self.sep2 = pm.separator(st='none')
        pm.setParent('..') #-- end of self.fLEd
        pm.setParent('..') #-- end of self.rLEd


        #-----------------------------------------------------------------------
        #-- Characterize ------------------------------------------------------- 
        self.rLCh = pm.frameLayout(l='Characterize')
        self.fLCh = pm.formLayout(nd=100)
        self._tpt = pm.iconTextButton(l='T-pose')
        self._chb = pm.iconTextButton(l='character')
        self._dac = pm.iconTextButton(l='delete Anim')
        self.sep3 = pm.separator(st='none')
        pm.setParent('..') #-- end of self.fLCh
        pm.setParent('..') #-- end of self.rLCh


        #-----------------------------------------------------------------------
        #-- Controller --------------------------------------------------------- 
        self.rLCt = pm.frameLayout(l='Controller')
        self.fLCt = pm.formLayout(nd=100)
        self._ict = pm.iconTextButton(l='Import ctrl')
        self._ctw = pm.iconTextButton(l='Create wld')
        self._cnw = pm.iconTextButton(l='Connect wld')
        self.sep4 = pm.separator(st='none')
        pm.setParent('..') #-- end of self.fLCt
        pm.setParent('..') #-- end of self.rLCt


        #-----------------------------------------------------------------------
        #-- Motion ------------------------------------------------------------- 
        self.rLMo = pm.frameLayout(l='Motion')
        self.fLMo = pm.formLayout(nd=100)
        self._rfm = pm.iconTextButton(l='Ref Motion')
        self._imm = pm.iconTextButton(l='Import Motion')
        self.sep5 = pm.separator(st='none')
        pm.setParent('..') #-- End of self.fmL1
        pm.setParent('..') #-- End of self.rLMo
        pm.setParent('..') #-- end of self.cmL0

        self.spEd = pm.separator(st='none', w=275, h=20)
        self._hpl = pm.helpLine(h=20, w=100, bgc=(0.15, 0.15, 0.15))
        pm.setParent('..') #-- End of self.fLMo


        #-----------------------------------------------------------------------
        #-- Edit UI Layout -----------------------------------------------------
        pm.columnLayout(self.cmL0, adj=True, rs=0, e=True)
        pm.frameLayout(self.rLGd, cll=True, bgc=self.frmBgc, e=True)
        pm.frameLayout(self.rLEd, cll=True, bgc=self.frmBgc, e=True)
        pm.frameLayout(self.rLCh, cll=True, bgc=self.frmBgc, e=True)
        pm.frameLayout(self.rLCt, cll=True, bgc=self.frmBgc, e=True)
        pm.frameLayout(self.rLMo, cll=True, bgc=self.frmBgc, e=True)


        #-----------------------------------------------------------------------
        #-- Guide --------------------------------------------------------------
        io,  to  = ['iconOnly', 'textOnly']
        ith, itv = ['iconAndTextHorizontal', 'iconAndTextVertical']

        pm.iconTextButton(self._ibt, st=ith, h=30, w=125, mw=7, e=True,
            c=pm.Callback(self.importGuide), ann=self._an_ibt, 
            i='{0}/p-add.png'.format(self._idir), bgc=self.btnBgc)

        pm.iconTextButton(self.btsv, st=ith, h=30, w=125, mw=7, e=True,
            c=pm.Callback(self.saveGuide), ann=self._an_ibt,
            i='{0}/exportGuide.png'.format(self._idir), bgc=self.btnBgc)

        pm.iconTextButton(self._imb, st=ith, h=30, w=125, mw=7, e=True,
            c=pm.Callback(self.fitGuideToSkeleton), ann=self._an_imb, 
            i='{0}/pi-head.png'.format(self._idir), bgc=self.btnBgc)

        pm.checkBox(self._ckb, h=30, w=125, ann=self._an_ckb, e=True,
            cc=pm.Callback(self.setMoveToolOption))

        pm.iconTextButton(self._afg, st=ith, h=30, w=125, mw=7, e=True,
            i='{0}/align.png'.format(self._idir), bgc=self.btnBgc, 
            c=pm.Callback(self.alignFinger), ann=self._an_afg)

        pm.iconTextButton(self._aft, st=ith, h=30, w=125, mw=7, e=True,
            i='{0}/align.png'.format(self._idir), bgc=self.btnBgc,
            c=pm.Callback(self.alignFoot), ann=self._an_aft)

        pm.iconTextButton(self._cbt, st=ith, h=30, w=125, mw=7, e=True,
            i='{0}/build.png'.format(self._idir), bgc=self.btnBgc,
            c=pm.Callback(self.skeletonBuild, typ='biped'), ann=self._an_cbt)

        pm.iconTextButton(self._nbt, st=ith, h=30, w=125, mw=7, e=True,
            i='{0}/build.png'.format(self._idir), bgc=self.btnBgc, 
            c=pm.Callback(self.skeletonBuild, typ='quad'), ann=self._an_nbt)


        #-----------------------------------------------------------------------
        #-- import functions ---------------------------------------------------
        pm.iconTextButton(self._smb, c=pm.Callback(self.importSkinMesh, typ=''), 
            st=ith, i1='{0}/np-head.png'.format(self._idir),
            h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_smb, e=True)

        pm.iconTextButton(self._ftb, c=pm.Callback(self.fitToGuide), 
            st=ith, i1='{0}/p-head.png'.format(self._idir),
            h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_ftb, e=True)


        #-----------------------------------------------------------------------
        #-- Characterize functions ---------------------------------------------
        pm.iconTextButton(self._tpt, st=ith, h=30, w=125, mw=7, ann=self._an_tpt,
            i1='{0}/text.png'.format(self._idir), bgc=self.btnBgc, 
            c=pm.Callback(self.setPose), e=True)
        pm.iconTextButton(self._chb, st=ith, h=30, w=125, mw=7, ann=self._an_chb, 
            i1='{0}/build.png'.format(self._idir), bgc=self.btnBgc, 
            c=pm.Callback(self.setDefinition), e=True)
        pm.iconTextButton(self._dac, st=ith, h=30, w=125, mw=7, ann=self._an_chb, 
            i1='{0}/delete.png'.format(self._idir), bgc=self.btnBgc, 
            c=pm.Callback(self.deleteAnimCurve), e=True)


        #-----------------------------------------------------------------------
        #-- Controller functions -----------------------------------------------
        pm.iconTextButton(self._ict, c=pm.Callback(self.importCtrl), 
            st=ith, i1='{0}/ctrl.png'.format(self._idir),
            h=30, w=255, mw=7, bgc=self.btnBgc, ann=self._an_ict, e=True)
        pm.iconTextButton(self._ctw, c=pm.Callback(self._createWld), 
            st=ith, i1='{0}/create.png'.format(self._idir),
            h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_ctw, e=True)
        pm.iconTextButton(self._cnw, c=pm.Callback(self._connectWld),
            st=ith, i1='{0}/connect.png'.format(self._idir),
            h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_cnw, e=True)


        #-----------------------------------------------------------------------
        #-- Motion functions ---------------------------------------------------
        pm.iconTextButton(self._rfm, c=pm.Callback(self.referenceMotion), 
            st=ith, i1='{0}/motion.png'.format(self._idir), 
            h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_rfm, e=True)
        pm.iconTextButton(self._imm, c=pm.Callback(self.importMotion), 
            st=ith, i1='{0}/motion.png'.format(self._idir), 
            h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_imm, e=True)


        #-- Edit UI Layout -----------------------------------------------------
        t, b, l, r = ['top', 'bottom', 'left', 'right']

        pm.formLayout(self.fmL0, e=True,
        af=[(self.sep0, t,   0), (self.sep0, l, 0), (self.sep0, r, 0), 
            (self.cmL0, t,   0), (self.cmL0, l, 0), (self.cmL0, r, 0), 
                                 (self.spEd, l, 0), (self.spEd, r, 0), (self.spEd, b, 15), 
                                 (self._hpl, l, 5), (self._hpl, r, 5), (self._hpl, b,  5), 
            ])

        pm.formLayout(self.fLGd, bgc=self.fomBgc, e=True,
        af=[(self._ibt, t,  10), (self._ibt, l,  10),
            (self.btsv, t,  10), (self.btsv, l, 140),
            (self._ckb, t,  45), (self._ckb, l,  15), 
            (self._imb, t,  45), (self._imb, l, 140), #-- fit

            (self._afg, t,  80), (self._afg, l,  10), #-- align
            (self._aft, t,  80), (self._aft, l, 140),

            (self._cbt, t, 115), (self._cbt, l,  10), #-- build
            (self._nbt, t, 115), (self._nbt, l, 140),
            (self.sep1, t, 160), (self.sep1, l,   0), (self.sep1, r,  0),
            ])

        pm.formLayout(self.fLEd, bgc=self.fomBgc, e=True,
        af=[(self._smb, t,  10), (self._smb, l,  10),
            (self._ftb, t,  10), (self._ftb, l, 140),
            (self.sep2, t,  55), (self.sep2, l,   0), (self.sep2, r,  0),
            ])

        pm.formLayout(self.fLCh, bgc=self.fomBgc, e=True,
        af=[(self._tpt, t,  10), (self._tpt, l,  10),
            (self._chb, t,  10), (self._chb, l, 140),
            (self._dac, t,  45), (self._dac, l,  10),
            (self.sep3, t, 100), (self.sep3, l,   0), (self.sep3, r,  0),
            ])

        pm.formLayout(self.fLCt, bgc=self.fomBgc, e=True,
        af=[(self._ict, t,  10), (self._ict, l,  10),
            (self._ctw, t,  45), (self._ctw, l,  10),
            (self._cnw, t,  45), (self._cnw, l, 140),
            (self.sep4, t,  90), (self.sep4, l,   0), (self.sep4, r,  0),
            ])

        pm.formLayout(self.fLMo, bgc=self.fomBgc, e=True,
        af=[(self._rfm, t,  10), (self._rfm, l,  10),
            (self._imm, t,  10), (self._imm, l, 140),
            (self.sep5, t,  55), (self.sep5, l,   0), (self.sep5, r,  0),
            ])

        window.show()


        #-- init command -------------------------------------------------------
        pm.window(self.windowName, e=True,
                  w = self.windowSize[0], 
                  h = self.windowSize[1])


def showUI():
    testIns = baseBodyBuilderUI()
    testIns.main()
