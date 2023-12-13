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
from . import build
from . import guide
from . import adn
from . import setup


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


class baseBodyGuideUI(object):
    def __init__(self):
        self.__ver__          = '0.4.0'
        self.windowManageName = 'baseBodyGuide'
        self.windowTitle      = 'BBG v{0}'.format(self.__ver__)
        self.windowSize       = [300, 300]
        self._mayaHelp_url    = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._toolHelp_url    = r'https://wisdom.cygames.jp/x/SOB_C'
        #--- current script path -----------------------------------------------
        self.__dir = os.path.dirname(os.path.abspath(__file__))
        #-- image path ---------------------------------------------------------
        self._idir = r'{0}/_data/_icon'.format(self.__dir)
        #-- color
        self.btnBgc = (0.37, 0.37, 0.37)
        #-- color
        self._an_ibt = u'ガイドをインポートします。'
        self._an_imb = u'Jointにガイドをスナップします。'
        self._an_ckb = u'移動ツール階層保持オプション'
        self._an_afg = u'手の指のガイドを揃えます。'
        self._an_aft = u'足のガイドを揃えます。'
        self._an_cbt = u'プレイアブルキャラクターの設定でビルド'
        self._an_nbt = u'NPCの設定でビルド'

        self._an_smb = u'スキンのインポート'
        self._an_ftb = u'スキンをJointにスナップします。'

        self._an_tpt = u'0～10fでTポーズを設定します。'
        self._an_chb = u'キャラクターノードの作成とマッピング'

        self._an_sae = u'Assist Drive Editorの起動'
        self._an_adn = u'ADN Assistantの起動'
        self._an_pad = u'プレイアブルキャラクターの設定のAssistDriveを作成'
        self._an_nad = u'NPCの設定のAssistDriveを作成'

        self._an_ict = u'基本コントローラーのインポート'
        self._an_ctw = u'選択したオブジェクトにwldを作成'
        self._an_cnw = u'2つ選択したノード間にwldコネクションを作成'

        self._an_rfm = u'チェックモーションデータのリファレンス'
        self._an_imm = u'チェックモーションデータのインポート'



    def checkWindowOverlap(self):
        if pm.window(self.windowManageName, ex=True):
            pm.deleteUI(self.windowManageName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)


    #--- functions -------------------------------------------------------
    def importGuide(self, *args):
        p = self.__dir
        f = '_data/_guide'
        #path = r'{0}/{1}'.format(p, f)
        p   = self.__dir
        exf = '*.mb'
        std = r'{0}/_data/_guide'.format(p)
        path = mc.fileDialog2(ff=exf, 
                              fm=1,
                              ds=2,
                             cap='Import Guide Data',
                             dir=std,
                             okc='Import',
                              cc='Cancel')

        importFile(path, '_guide', '.mb')


    def fitGuideToSkeleton(self, *args):
        info = self.getHikDefinition(typ='pl')
        guide.fitToSkeleton(info)


    def importMesh(self, *args):
        importFile(r'{0}/_data/_mesh'.format(self.__dir), '_basebody', '.mb')


    def importSkinMesh(self, typ='', *args):
        if typ:
            typ = '_{0}'.format(typ)
        importFile(r'{0}/_data/_mesh'.format(self.__dir), 
                   '_basebody_bind{0}'.format(typ), 
                   '.mb')


    def importDammy(self, *args):
        importFile(r'{0}/_data/_dammy'.format(self.__dir), '_dammy_joint', '.mb')


    def setMoveToolOption(self, *args):
        val = pm.checkBox(self._ckb, v=True, q=True)
        command.setPreserveChildren(val)


    def getHikDefinition(self, typ='pl', *args):
        p = self.__dir
        f = r'_data/_json/_hik_{0}.json'.format(typ)
        _path = r'{0}/{1}'.format(p, f)
        print (_path)
        info  = command.importJson(_path)
        return info


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


    def showADE(self, *args):
        adn.showADE()


    def showADN(self, *args):
        adn.showADNA()


    def addADJoint(self, *args):
        adn.addJoint_adn()


    def addADJoint_forNPC(self, *args):
        adn.addJoint_adn_npc()


    def importADN(self, typ='pl', *args):
        if typ == 'pl':
            adn.addJoint_adn()
        elif typ == 'npc':
            adn.addJoint_adn_npc()

        p = self.__dir
        f = r'_data/_assistdrive/_{0}.csv'.format(typ)
        _path = r'{0}/{1}'.format(p, f)
        adn.importDefaultADN(_path)


    def importCtrl(self, *args):
        p = self.__dir
        f = '_data/_guide'
        _path = r'{0}/{1}'.format(p, f)
        importFile(_path, '_ctrl', '.mb')


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
        p   = self.__dir
        exf = '*.mb'
        std = r'{0}/_data/_motion/_mb'.format(p)
        path = mc.fileDialog2(ff=exf, 
                              fm=1,
                              ds=2,
                             cap='Reference Motion Data',
                             dir=std,
                             okc='Reference',
                              cc='Cancel')

        #--- reference
        mc.file(path[0], r=True,
                       typ='mayaBinary',
                        iv=True,
                        gl=False,
                       mnc=False,
                        ns='_motion',
                        op='v=0;')


    def importMotion(self, *args):
        #--- check keep motion
        val = pm.confirmDialog(t='Keep Root Position',
                               m='Does Root Joint "_000" keep position?', 
                               b=['Keep', 'As Motion', 'Cancel'], 
                              db='Yes',
                              cb='Cancel', 
                              ds='Cancel' )
        #--- lock translate attr
        if val == 'Keep':
            for i in pm.ls('_000', dag=True, typ='joint'):
                if not i.name() == '_000':
                    i.t.set(l=True)

        elif val == 'As Motion':
            for i in pm.ls('_000', dag=True, typ='joint'):
                i.t.set(l=True)

        elif val == 'Cancel':
            return

        p   = self.__dir
        exf = '*.fbx'
        std = r'{0}/_data/_motion/_fbx'.format(p)
        path = mc.fileDialog2(ff=exf, 
                              fm=1,
                              ds=2,
                             cap='Import Motion Data',
                             dir=std,
                             okc='Import',
                              cc='Cancel')

        #--- import
        mc.file(path[0], i=True,
                       typ='FBX',
                        iv=True,
                        gl=False,
                       mnc=False,
                        op='fbx',
                        pr=True,
                       itr='combine')


    #--- edit UI ----------------------------------------



    #--- main UI ----------------------------------------
    def main(self):               
        self.checkWindowOverlap()
        window = pm.window(self.windowManageName,
                           t  = self.windowTitle,
                           w  = self.windowSize[0],
                           h  = self.windowSize[1],
                           mb = True)

        #--- menu
        pm.menu(l='Tools', 
               to=False)
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

        pm.menuItem(d=True, dl='Assist Drive')
        pm.menuItem(l='ADN Assistant', i='{0}/pi-add.png'.format(self._idir),
                    c=self.showADN)
        pm.menuItem(l='Assist Drive Editor', i='{0}/pi-add.png'.format(self._idir),
                    c=self.showADE)
        pm.menuItem(l='Add joint for PL', i='{0}/add.png'.format(self._idir),
                    c=self.addADJoint)
        pm.menuItem(l='Add joint for NPC', i='{0}/add.png'.format(self._idir),
                    c=self.addADJoint_forNPC)
        
        pm.menu(l  = 'Help', 
                hm = True)
        pm.menuItem(l = 'Maya 2019 HELP',
                    c = self.show_mayaHelp)
        pm.menuItem(d = True)
        pm.menuItem(l = 'Tool HELP',
                    c = self.show_toolHelp)

        #--- base form layout
        self.fmL0 = pm.formLayout(nd=100)
        with self.fmL0:
            self.sep0 = pm.separator(w=275)

            self.fmL1 = pm.formLayout(nd=100)
            with self.fmL1:
                self._ibt = pm.iconTextButton(l='Import Guide')
                self._imb = pm.iconTextButton(l='Fit to Skeleton')
                self._ckb = pm.checkBox(l='Preserve Children')
                self._afg = pm.iconTextButton(l='Align finger')
                self._aft = pm.iconTextButton(l='Align foot')
                self._cbt = pm.iconTextButton(l='Build ( PL )')
                self._nbt = pm.iconTextButton(l='Build ( NPC )')
                self.sep1 = pm.separator(st='in')

                self._smb = pm.iconTextButton(l='Import skin')
                self._ftb = pm.iconTextButton(l='Fit to Skeleton')
                self.sep2 = pm.separator(st='in')

                self._tpt = pm.iconTextButton(l='T-pose')
                self._chb = pm.iconTextButton(l='character')
                self.sep3 = pm.separator(st='in')

                self._adn = pm.iconTextButton(l='ADN Assistant')
                self._sae = pm.iconTextButton(l='Assist Drive Editor (old)')
                self._pad = pm.iconTextButton(l='Add PL ADN')
                self._nad = pm.iconTextButton(l='Add NPC ADN')
                self.sep4 = pm.separator(st='in')

                self._ict = pm.iconTextButton(l='Import ctrl')
                self._ctw = pm.iconTextButton(l='Create wld')
                self._cnw = pm.iconTextButton(l='Connect wld')
                self.sep5 = pm.separator(st='in')

                self._rfm = pm.iconTextButton(l='Ref Motion')
                self._imm = pm.iconTextButton(l='Import Motion')
            self.sepe = pm.separator(st='none', w=275, h=20)
            self._hpl = pm.helpLine(h=20, w=100, bgc=(0.15, 0.15, 0.15))


        #--- Edit UI Layout
        pm.iconTextButton(self._ibt, c=pm.Callback(self.importGuide),
        st='iconAndTextHorizontal', i1='{0}/p-add.png'.format(self._idir),
        h=30, w=255, mw=7, bgc=self.btnBgc, ann=self._an_ibt, e=True)
        pm.iconTextButton(self._imb, c=pm.Callback(self.fitGuideToSkeleton),
        st='iconAndTextHorizontal', i1='{0}/pi-head.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_imb, e=True)
        pm.checkBox(self._ckb, cc=pm.Callback(self.setMoveToolOption),
        h=30, w=125, ann=self._an_ckb, e=True)
        pm.iconTextButton(self._afg, c=pm.Callback(self.alignFinger), 
        st='iconAndTextHorizontal', i1='{0}/align.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_afg, e=True)
        pm.iconTextButton(self._aft, c=pm.Callback(self.alignFoot), 
        st='iconAndTextHorizontal', i1='{0}/align.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_aft, e=True)
        pm.iconTextButton(self._cbt, c=pm.Callback(self.testBuild, typ='pl'), 
        st='iconAndTextHorizontal', i1='{0}/build.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_cbt, e=True)
        pm.iconTextButton(self._nbt, c=pm.Callback(self.testBuild, typ='npc'), 
        st='iconAndTextHorizontal', i1='{0}/build.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_nbt, e=True)

        #-- import functions
        pm.iconTextButton(self._smb, c=pm.Callback(self.importSkinMesh, typ=''), 
        st='iconAndTextHorizontal', i1='{0}/np-head.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_smb, e=True)
        pm.iconTextButton(self._ftb, c=pm.Callback(self.fitToGuide), 
        st='iconAndTextHorizontal', i1='{0}/p-head.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_ftb, e=True)

        #-- Pose functions
        pm.iconTextButton(self._tpt, c=pm.Callback(self.setPose), 
        st='iconAndTextHorizontal', i1='{0}/text.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_tpt, e=True)
        pm.iconTextButton(self._chb, c=pm.Callback(self.setDefinition), 
        st='iconAndTextHorizontal', i1='{0}/build.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_chb, e=True)

        #-- Assist Drive functions
        pm.iconTextButton(self._adn, c=pm.Callback(self.showADN), 
        st='iconAndTextHorizontal', i1='{0}/pi-add.png'.format(self._idir),
        h=30, w=255, mw=7, bgc=self.btnBgc, ann=self._an_adn, e=True)
        pm.iconTextButton(self._sae, c=pm.Callback(self.showADE), 
        st='iconAndTextHorizontal', i1='{0}/pi-add.png'.format(self._idir),
        h=30, w=255, mw=7, bgc=self.btnBgc, ann=self._an_sae, e=True)
        pm.iconTextButton(self._pad, c=pm.Callback(self.importADN, typ='pl'), 
        st='iconAndTextHorizontal', i1='{0}/add.png'.format(self._idir), 
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_pad, e=True)
        pm.iconTextButton(self._nad, c=pm.Callback(self.importADN, typ='npc'), 
        st='iconAndTextHorizontal', i1='{0}/add.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_nad, e=True)

        #-- Controll functions
        pm.iconTextButton(self._ict, c=pm.Callback(self.importCtrl), 
        st='iconAndTextHorizontal', i1='{0}/ctrl.png'.format(self._idir),
        h=30, w=255, mw=7, bgc=self.btnBgc, ann=self._an_ict, e=True)
        pm.iconTextButton(self._ctw, c=pm.Callback(self._createWld), 
        st='iconAndTextHorizontal', i1='{0}/create.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_ctw, e=True)
        pm.iconTextButton(self._cnw, c=pm.Callback(self._connectWld),
        st='iconAndTextHorizontal', i1='{0}/connect.png'.format(self._idir),
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_cnw, e=True)

        #-- Motion functions
        pm.iconTextButton(self._rfm, c=pm.Callback(self.referenceMotion), 
        st='iconAndTextHorizontal', i1='{0}/motion.png'.format(self._idir), 
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_rfm, e=True)
        pm.iconTextButton(self._imm, c=pm.Callback(self.importMotion), 
        st='iconAndTextHorizontal', i1='{0}/motion.png'.format(self._idir), 
        h=30, w=125, mw=7, bgc=self.btnBgc, ann=self._an_imm, e=True)
        #--- Edit UI Layout
        t, b , l, r = ['top', 'bottom', 'left', 'right']

        pm.formLayout(self.fmL0, e=True,
               af = [(self.sep0, t,  0), (self.sep0, l, 0), (self.sep0, r, 0), 
                     (self.fmL1, t,  0), (self.fmL1, l, 0), (self.fmL1, r, 0), (self.fmL1, b, 0),
                     (self.sepe, b, 25), (self.sepe, l, 0), (self.sepe, r, 0), 
                     (self._hpl, b,  5), (self._hpl, l, 5), (self._hpl, r, 5), 
                    ])

        pm.formLayout(self.fmL1, e=True,
               af = [(self._ibt, t,  10), (self._ibt, l, 10),
                     (self._imb, t,  45), (self._imb, l, 140),
                     (self._ckb, t,  44), (self._ckb, l, 15),
                     (self._afg, t,  80), (self._afg, l, 10),
                     (self._aft, t,  80), (self._aft, l, 140),
                     (self._cbt, t, 115), (self._cbt, l, 10),
                     (self._nbt, t, 115), (self._nbt, l, 140),

                     (self.sep1, t, 155), (self.sep1, l, 10), (self.sep1, r, 10),
                     (self._smb, t, 165), (self._smb, l, 10),
                     (self._ftb, t, 165), (self._ftb, l, 140),

                     (self.sep2, t, 205), (self.sep2, l, 10), (self.sep2, r, 10),
                     (self._tpt, t, 215), (self._tpt, l, 10),
                     (self._chb, t, 215), (self._chb, l, 140),

                     (self.sep3, t, 255), (self.sep3, l, 10), (self.sep3, r, 10),
                     (self._adn, t, 265), (self._adn, l, 10),
                     (self._sae, t, 300), (self._sae, l, 10),
                     (self._pad, t, 335), (self._pad, l, 10),
                     (self._nad, t, 335), (self._nad, l, 140),

                     (self.sep4, t, 375), (self.sep4, l, 10), (self.sep4, r, 10),
                     (self._ict, t, 385), (self._ict, l, 10),
                     (self._ctw, t, 420), (self._ctw, l, 10),
                     (self._cnw, t, 420), (self._cnw, l, 140),

                     (self.sep5, t, 460), (self.sep5, l, 10), (self.sep5, r, 10),
                     (self._rfm, t, 470), (self._rfm, l, 10),
                     (self._imm, t, 470), (self._imm, l, 140),
                    ])

        window.show()


def showUI():
    testIns = baseBodyGuideUI()
    testIns.main()
