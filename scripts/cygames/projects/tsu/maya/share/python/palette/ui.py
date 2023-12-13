# -*- coding: utf-8 -*-
from __future__ import absolute_import

#----- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import json


from . import command
from . import data
from . import setup
from . import name
from . import _string as _str


#from . import command
#reload(command)
#from . import data
#reload(data)
#from . import setup
#reload(setup)
#from . import name
#reload(name)
#from . import _string as _str
#reload(_str)


class paletteUI(object):
    def __init__(self):
        self.__ver__          = '0.3.0'
        self.windowManageName = 'Palette'
        self.windowTitle      = '{0} v{1}'.format(self.windowManageName, self.__ver__)
        self.windowSize       = [400, 850]
        self._mayaHelp_url    = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._toolHelp_url    = r'https://wisdom.cygames.jp/display/tsubasa/%5BMaya%5D+Palette'
        #-- current script path ------------------------------------
        self.__dir = os.path.dirname(os.path.abspath(__file__))
        self._icon = r'{0}/_icon/'.format(self.__dir)
        #-- image path ---------------------------------------------
        self._mdir = r'{0}/{1}/'.format(self.__dir, '_img/main')
        #-- color --------------------------------------------------
        self.btnBgc = (0.37, 0.37, 0.37)
        self.frmBgc = (0.00, 0.30, 0.60)
        self.bgaBgc = (0.27, 0.27, 0.27)
        self.bgbBgc = (0.24, 0.24, 0.24)


    def checkWindowOverlap(self):
        if pm.window(self.windowManageName, ex=True):
            pm.deleteUI(self.windowManageName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)


    #---------------------------------------------------------------------------
    #-- init function ----------------------------------------------------------
    def _setID(self, *args):
        idStr  = data.getIDFromRoot()
        if idStr:
            res = idStr
            print('Asset ID : {0}'.format(idStr))
            print('Type     : {0}'.format(idStr[:2]))
            print('Number   : {0}'.format(idStr[-4:]))
        else:
            res = ''
        #-- set string ID
        pm.textFieldButtonGrp(self._txg0, tx=res, e=True)
        self.setP4VDir()
        self.setLclDir()


    #---------------------------------------------------------------------------
    #-- import text file -------------------------------------------------------
    #def _importLabel(self, tab, *args):
    #    res = command.importJson('{0}/_json/{1}.json'.format(self.__dir, tab))
    #    return res


    def _importAnnotation(self, v='', *args):
        res = command.importJson('{0}/_json/_ann_{1}.json'.format(self.__dir, v))
        return res


    def _importMenu(self, v='', *args):
        res = command.importJson('{0}/_json/_mi_{1}.json'.format(self.__dir, v))
        return res


    #---------------------------------------------------------------------------
    #-- directory --------------------------------------------------------------
    def setP4VDir(self, *args):
        path = data.P4VDirectory()
        if os.path.exists(path):
            pm.textFieldButtonGrp(self._txgP4, tx=data.P4VDirectory(), pht='', e=True)
        else:
            pm.textFieldButtonGrp(self._txgP4, tx='', pht=data.P4VDirectory(), e=True)
            log = 'P4V Directory doesn\'t exist.\n'
            self._addLog(log)
            print(log)


    def setLclDir(self, *arg):
        path = data.LclDirectory()
        if os.path.exists(path):
            pm.textFieldButtonGrp(self._txgLc, tx=data.LclDirectory(), pht='', e=True)
        else:
            pm.textFieldButtonGrp(self._txgLc, tx='', pht=data.LclDirectory(), e=True)
            log = 'Local Directory doesn\'t exist.\n'
            self._addLog(log)
            print(log)


    def createP4VDir(self, *arg):
        log = data.createP4VDirectory()
        self._addLog()
        self._addLog(log)
        self.setP4VDir()


    def openP4VDir(self, *arg):
        path = pm.textFieldButtonGrp(self._txgP4, tx=True, q=True)
        if os.path.exists(path):
            data.openDir(path)
        else:
            log = 'P4V Directory doesn\'t exist.\n'
            self._addLog(log)
            print(log)


    def createLclDir(self, *arg):
        log = data.createLclDirectory()
        self._addLog()
        self._addLog(log)
        self.setLclDir()


    def openLclDir(self, *arg):
        path = pm.textFieldButtonGrp(self._txgLc, tx=True, q=True)
        if os.path.exists(path):
            data.openDir(path)
        else:
            log = 'Local Directory doesn\'t exist.\n'
            self._addLog(log)
            print(log)


    def workScenePath(self, *arg):
        a = data.getIDFromRoot()
        p = pm.workspace(q=True, rd=True)
        if a:
            c = a[:2]
            n = a[-4:]
            p = r'{0}scenes/{1}/{2}/maya'.format(p, c, a)
        return p


    def workSceneFile(self, *arg):
        a = data.getIDFromRoot()
        s = self.workScenePath()

        if a and os.path.exists(s):
            fl = [i for i in os.listdir(s) if '.mb' in i]
            #if len(i.split('_')) == 3
            if fl:
                sorted(fl)
                return fl[-1]
            else:
                return ''
        else:
            return ''


    #---------------------------------------------------------------------------
    #--- functions cleanup -----------------------------------------------------
    def _setUnit(self, *args):
        self._addLog(command.setDefaultUnitEnv())
        self._toggleCheckUI('setUnit', 1)


    def _delAnimKey(self, *args):
        self._addLog(data.deleteAnimKey())
        self._toggleCheckUI('delAnimKey', 1)


    def _deleteSkin(self, *args):
        self._addLog(data.cleanSkin())
        self._toggleCheckUI('delSkin', 1)


    def _delJoint(self, *args): 
        self._addLog(data.deleteSkeleton())
        self._toggleCheckUI('delJoint', 1)


    def _resetDisplay(self, *args): 
        n = pm.textFieldButtonGrp(self._txg0, tx=True, q=True)
        self._addLog(data.resetMeshDispaly(n))
        self._toggleCheckUI('resetDisplay', 1)


    def _freezeObj(self, *args): 
        self._addLog(data.freezeObj())
        self._toggleCheckUI('freezeMesh', 1)


    def _shapeCheck(self, *args):
        self._addLog(data.checkUnnecessaryMesh())
        self._toggleCheckUI('checkShape', 1)


    def _nameCheck(self, *args):
        self._addLog(data.checkSameNameNode())
        self._toggleCheckUI('checkName', 1)


    def _checkTexture(self, *args):
        self._addLog(data.checkTextureExist())
        self._toggleCheckUI('checkTexture', 1)


    def _cleanData(self, *args):
        path = r'{0}/maya'.format(data.LclDirectory())
        if os.path.exists(path):
            self._addLog(data.cleanupData(path))
            self._addLog(command.setDefaultUnitEnv())
            self._toggleCheckUI('dataCleaning', 1)
        else:
            log = '------------------- Export Scene Cleanup -------------------------\n'
            log += 'Local Directory doesn\'t exist.\n'
            self._addLog(log)
            print(log)


    def _changeCleanupTarget(self, *args):
        ubv = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        kbv = [1, 1, 0, 0, 1, 0, 1, 1, 1, 1]

        tgt    = pm.radioButtonGrp(self.curg, sl=True, q=True)
        cbList = [i.replace('_rl', '_cb') for i in pm.columnLayout(self._rcL0, ca=True, q=True)]
        if tgt == 1:
            for i, cb in enumerate(cbList):
                pm.checkBox(cb, v=ubv[i], e=True)
                self._toggleCheckUI(cb.replace('_cb', ''), d=0)
        elif tgt == 2:
            for i, cb in enumerate(cbList):
                pm.checkBox(cb, v=kbv[i], e=True)
                self._toggleCheckUI(cb.replace('_cb', ''), d=0)


    #-- run all functions ------------------------------------------------------
    def _runAllCleaning(self, func, *args):
        for i in func:
            if pm.checkBox(i[0], v=True, q=True):
                exec('self.{0}()'.format(i[1].__name__))


    #-- create rig info set ------------------------------------------------------
    def _createRigInfoSet(self, add_log=True):
        rig_info_dict = data.getRigInformation('{0}/_json/_rig_info.json'.format(self.__dir))
        rig_info_set_name = rig_info_dict[0]
        fase_set_name = rig_info_dict[1]
        exp_pose_at_name = rig_info_dict[2]

        # rename old face set
        old_face_set_list = data.getFaceSetList()
        if old_face_set_list:
            pm.rename(old_face_set_list[0], fase_set_name)

        # ---------------------
        if not pm.objExists(rig_info_set_name):
            rig_info_set = pm.sets(em=True, n=rig_info_set_name)
            if add_log:
                self._addLog('{0} Created.\n'.format(rig_info_set_name))
        else:
            rig_info_set = pm.PyNode(rig_info_set_name)

        # ---------------------
        if not pm.objExists(fase_set_name):
            fase_set = pm.sets(em=True, n=fase_set_name)
            if add_log:
                self._addLog('{0} Created.\n'.format(fase_set_name))
        else:
            fase_set = pm.PyNode(fase_set_name)

        # ---------------------
        try:
            pm.sets(rig_info_set, e=True, fe=fase_set)
        except:
            pass

        # ---------------------
        if not pm.objExists(rig_info_set + '.' + exp_pose_at_name):
            pm.addAttr(rig_info_set, ln=exp_pose_at_name, dv=0)
            if add_log:
                self._addLog('{0} created.\n'.format(rig_info_set.name() + '.' + exp_pose_at_name))

        # ---------------------
        if pm.objExists('Face_LOD0'):
            pm.sets(fase_set, e=True, fe='Face_LOD0')


    #---------------------------------------------------------------------------
    #--- functions Export ------------------------------------------------------
    def _collectBindPose(self, *args):
        self._addLog(data.collectSingleBindPose())
        self._toggleCheckUI('singleBindPose', 1)


    def _checkSSC(self, *args):
        self._addLog(data.checkSSC())
        self._toggleCheckUI('checkSegmentScale', 1)


    def _checkJO(self, *args):
        self._addLog(data.checkJO())
        self._toggleCheckUI('checkJointOrient', 1)


    def _deleteUnusedMaterial(self, *args):
        self._addLog(data.deleteUnusedMaterial())
        self._toggleCheckUI('deleteUnusedNode', 1)


    def _deleteDisplayLayer(self, *args):
        self._addLog(data.deleteDisplayLayer())
        self._toggleCheckUI('deleteDisplayLayer', 1)


    def _deleteRig(self, *args):
        self._addLog(data.deleteRigGroup())
        self._toggleCheckUI('deleteRig', 1)


    def _deleteFace(self, *args):
        self._addLog(data.deleteFaceGroup())
        self._toggleCheckUI('deleteFace', 1)


    def _deleteAnim(self, *args):
        self._addLog(data.deleteAnimAtExportFrame())
        self._toggleCheckUI('deleteAnim', 1)


    '''
    def _replaceLowMaterial(self, *args):
        log = data.runReplaceLowMT()
        log += data.deleteVertexColor()
        self._addLog('------------------- Replace Texture ------------------\n')
        self._addLog(log)


    def _replaceTexturePath(self, *args):
        log = data.replaceResizedTxPath()
        self._addLog('------------------- Replace Texture Path -------------\n')
        self._addLog(log)
    '''


    def _changeExportTarget(self, *args):
        gmv = [1, 1, 1, 1, 1, 1, 1, 1]
        mbv = [1, 1, 1, 1, 1, 0, 0, 0]

        #-- get target
        tgt    = pm.iconTextRadioCollection(self.irb, sl=True, q=True)
        cbList = [i.replace('_rl', '_cb') for i in pm.columnLayout(self._rcL1, ca=True, q=True)]

        if tgt == 'toGM':
            for i, cb in enumerate(cbList):
                pm.checkBox(cb, v=gmv[i], e=True)
                self._toggleCheckUI(cb.replace('_cb', ''), d=0)
                pm.frameLayout(self._frTx, en=False, e=True)
            del_face_cb_val = True if pm.objExists('Face_LOD0') or data.getFaceSetList() else False
        elif tgt == 'toMB':
            for i, cb in enumerate(cbList):
                pm.checkBox(cb, v=mbv[i], e=True)
                self._toggleCheckUI(cb.replace('_cb', ''), d=0)
                pm.frameLayout(self._frTx, en=True, e=True)
            del_face_cb_val = False

        #-- Face LOD
        #pm.checkBox('deleteFace_cb', v=pm.objExists('Face_LOD0'), e=True)
        pm.checkBox('deleteFace_cb', e=True, v=del_face_cb_val)
        self._toggleCheckUI('deleteFace', d=0)


    def _runAllExport(self, func, *args):
        for i in func:
            if pm.checkBox(i[0], v=True, q=True):
                exec('self.{0}()'.format(i[1].__name__))


    def _checkTools(self, *args):
        import tsubasa.maya.tools.checktool.gui as ctgui#;reload(ctgui)
        ctgui.main()


    def _exporter(self, *args):
        pm.mel.eval('ExportModel;')


    def _replaceMaterial(self, *args):
        v= pm.confirmDialog(t='Confirm', m='Replace Material for MB?', 
                            b=['Yes','No'], db='No', cb='No', ds='No')
        if v:
            self._addLog(data.runReplaceLowMT())
            self._addLog(data.deleteVertexColor())
            self._addLog(data.normalUnlock())


    #---------------------------------------------------------------------------
    #--- functions Setup -------------------------------------------------------
    def _createWld(self, *args):
        tgt = mc.ls(sl=True)
        log = setup.wldMatrix(tgt)
        self._addLog('------------------- Create wld matrix group ----------\n')
        self._addLog(log)


    #---------------------------------------------------------------------------
    #--- Name ------------------------------------------------------------------
    def _searchAndReplace(self, *args):
        src = pm.textFieldGrp(self._tgSr, tx=True, q=True)
        tgt = pm.textFieldGrp(self._tgRp, tx=True, q=True)
        log = name.SearchAndReplace(src, tgt)
        self._addLog(log)


    def _clearField(self, v=0, *args):
        if v == 0:   #-- search field
            pm.textFieldGrp(self._tgSr, tx='', e=True)
        elif v == 1: #-- Replace field
            pm.textFieldGrp(self._tgRp, tx='', e=True)
        elif v == 2:
            pm.textFieldGrp(self._tgPr, tx='', e=True)
        elif v == 3:
            pm.textFieldGrp(self._tgSf, tx='', e=True)


    def _getFirst(self, v=0, *args):
        obj = pm.selected()
        if obj:
            n = obj[0].longName().split('|')[-1]
            if v == 0:   #-- search field
                pm.textFieldGrp(self._tgSr, tx=n, e=True)
            elif v == 1: #-- Replace field
                pm.textFieldGrp(self._tgRp, tx=n, e=True)


    def _getLast(self, v=0, *args):
        obj = pm.selected()
        if obj:
            n = obj[-1].longName().split('|')[-1]
            if v == 0:   #-- search field
                pm.textFieldGrp(self._tgSr, tx=n, e=True)
            elif v == 1: #-- Replace field
                pm.textFieldGrp(self._tgRp, tx=n, e=True)


    def _addMenu(self, typ='', tgt='', *args):
        # typ = name
        # tgt = prefix / suffix
        m = self._importMenu(typ)

        if typ == 'name' and tgt == 'prefix':   
            for i, v in enumerate(m[tgt]):
                mc.menuItem('_miPt{0}'.format(i), l='{0}'.format(v), 
                c=pm.Callback(self._addPrefixString, v))

        elif typ == 'name' and tgt == 'suffix':  
            for i, v in enumerate(m[tgt]):
                mc.menuItem('_miPt{0}'.format(i), l='{0}'.format(v), 
                c=pm.Callback(self._addSuffixString, v))


    def _addPrefixString(self, v='', *args):
        pm.textFieldGrp(self._tgPr, tx=v, e=True)


    def _addSuffixString(self, v='', *args):
        pm.textFieldGrp(self._tgSf, tx=v, e=True)


    def _addPrefix(self, *args):
        pre = pm.textFieldGrp(self._tgPr, tx=True, q=True)
        log = name.addPrefix(pre)
        self._addLog(log)


    def _addSuffix(self, *args):
        suf = pm.textFieldGrp(self._tgSf, tx=True, q=True)
        log = name.addSuffix(suf)
        self._addLog(log)


    def _countRename(self, *args):
        nn  = pm.textFieldGrp(self._tgCr, tx=True, q=True)
        st  = pm.intFieldGrp(self._ifSt, v1=True, q=True)
        stx = pm.textFieldGrp(self._tgSt, tx=True, q=True)
        sp  = pm.intFieldGrp(self._ifSp, v1=True, q=True)
        ba  = pm.optionMenuGrp(self._meBa, v=True, q=True)
        if ba == '10':
            log = name.countAndRename(nn, st, sp)
        elif ba == '16':
            log = name.countAndRenameHex(nn, stx, sp)
        self._addLog(log)


    def _changeBase(self, *args):
        ba = pm.optionMenuGrp(self._meBa, v=True, q=True)
        if ba == '10':
            pm.intFieldGrp(self._ifSt, vis=True, e=True)   #-- base10
            pm.textFieldGrp(self._tgSt, vis=False, e=True) #-- base16
        elif ba == '16':
            pm.intFieldGrp(self._ifSt, vis=False, e=True)  #-- base10
            pm.textFieldGrp(self._tgSt, vis=True, e=True)  #-- base16


    def _countJoint(self, *args):
        log = name.jointCount()
        self._addLog(log)


    def _getJointName(self, v='_0', *args):
        tgt = pm.radioButtonGrp(self._rgCt, sl=True, q=True)
        log = name.getJointList(v, tgt-1)
        self._addLog(log)


    #---------------------------------------------------------------------------
    #--- edit UI ---------------------------------------------------------------
    def _tabLayout(self, *args):
        v = pm.menuItem(self._lb0, rb=True, q=True)
        if v:
            pm.tabLayout(self.tbL0, bs='none', cr=True, tp='west', e=True)
        else:
            pm.tabLayout(self.tbL0, bs='none', cr=True, tp='north', e=True)


    def _paneLayout(self, v=1, *args):
        ww = self.windowSize[0]
        if v:
            pm.paneLayout(self.pnL0, cn='horizontal2', ps=(1, 100, 70), e=True)
            pm.menuItem(self._lb2, rb=True, e=True)
            pm.iconTextRadioCollection(self._rclg, sl=self._btst, e=True)
            pm.window(self.windowManageName, w=ww, e=True)

        else:
            pm.paneLayout(self.pnL0, cn='vertical2', ps=(2, 90, 100), e=True)
            pm.menuItem(self._lb3, rb=True, e=True)
            pm.iconTextRadioCollection(self._rclg, sl=self._btss, e=True)
            pm.window(self.windowManageName, w=ww*2, e=True)


    def _addLog(self, tx='', *args):
        #ctx = pm.scrollField(self._scf, tx=True, q=True)
        #ctx += tx
        pm.scrollField(self._scf, it=tx, ip=0, e=True)


    def _clearLog(self, tx='', *args):
        pm.scrollField(self._scf, tx='', e=True)


    def _addCheckUI(self, _name, _func, _typ, *args):
        col = [self.bgaBgc, self.bgbBgc]
        ltx = _str._convertCtoL(_name)

        pm.rowLayout('{0}_rl'.format(_name), nc=2, adj=1, bgc=col[_typ], 
                     cw2=(200, 100), cat=[(1, 'left', 20), (2, 'right', 20)])
        pm.checkBox('{0}_cb'.format(_name), l=ltx, v=True, h=36, w=200,
                    cc=pm.Callback(self._toggleCheckUI, _name, 0))
        pm.iconTextButton('{0}_itb'.format(_name), l='Run', 
                          c=pm.Callback(_func), st='iconAndTextHorizontal', 
                          i1='{0}play.png'.format(self._icon), 
                          h=22, w=66, mw=7, mh=0, bgc=self.btnBgc)
        pm.setParent('..') #-- end of rowLayout
        return ['{0}_cb'.format(_name), _func]


    def _toggleCheckUI(self, _name, d=0, *args):
        if pm.checkBox('{0}_cb'.format(_name), ex=True, q=True):
            val = d - pm.checkBox('{0}_cb'.format(_name), v=True, q=True)
            pm.checkBox('{0}_cb'.format(_name), v=val, e=True)
            pm.iconTextButton('{0}_itb'.format(_name), en=val, e=True)


    def _getSelectedRadioMenuItem(self, mi=[], typ=0, *args):
        for i, ui in enumerate(mi):
            if pm.menuItem(ui, rb=True, q=True):
                if typ == 0:   #-- return ui class
                    return ui
                elif typ == 1: #-- return ui number
                    return i


    def _changeUI(self, *args):
        #ll = [self._lbl0, self._lbl1]
        al = [self._lba0, self._lba1]
        #lv = self._getSelectedRadioMenuItem(ll, typ=1)
        av = self._getSelectedRadioMenuItem(al, typ=1)

        for i in ['cleanup', 'export']:
            #-- label
            '''
            ldict = self._importLabel('cleanup')
            for k, v in ldict.items():
                pm.checkBox('{0}_cb'.format(k), l=v[lv], e=True)
            '''

            #-- annotation
            adict = self._importAnnotation(i)
            for k, v in adict.items():
                pm.checkBox('{0}_cb'.format(k), ann=v[av], e=True)
                pm.iconTextButton('{0}_itb'.format(k), ann=v[av], e=True)


    #---------------------------------------------------------------------------
    #--- main UI ---------------------------------------------------------------
    def main(self, *args):
        self.checkWindowOverlap()
        window = pm.window(self.windowManageName,
                           t  = self.windowTitle,
                           w  = self.windowSize[0],
                           h  = self.windowSize[1],
                           mb = True)

        #--- menu --------------------------------------------------------------
        #--- menu: Tools
        pm.menu(l='Tools', to=False)
        pm.menuItem(d=True, dl='Log')
        pm.menuItem(l='Clear Log', i='clearCanvas.png',
                    c=pm.Callback(self._clearLog))
        pm.menuItem(d=True, dl='Tab Layout')
        pm.radioMenuItemCollection()
        self._lb0 = pm.menuItem(l='Vertical', rb=True)
        self._lb1 = pm.menuItem(l='Horizontal', rb=False)
        pm.menuItem(d=True, dl='Panel Layout')
        pm.radioMenuItemCollection()
        self._lb2 = pm.menuItem(l='Stacked', rb=True)
        self._lb3 = pm.menuItem(l='Side by Side', rb=False)

        #--- menu: Language
        pm.menu(l='Language', to=False)
        '''
        pm.menuItem(d=True, dl='Label')
        pm.radioMenuItemCollection()
        self._lbl0 = pm.menuItem(l='English', rb=True)
        self._lbl1 = pm.menuItem(l='Japanese', rb=False)
        #self._lbl2 = pm.menuItem(l='Chinese', rb=False)
        '''
        pm.menuItem(d=True, dl='Annotation')
        pm.radioMenuItemCollection()
        self._lba0 = pm.menuItem(l='English', rb=False)
        self._lba1 = pm.menuItem(l='Japanese', rb=True)
        #self._lba2 = pm.menuItem(l='Chinese', rb=False)

        #--- menu: Help
        pm.menu(l='Help', hm=True)
        pm.menuItem(l='Maya 2019 HELP', c=self.show_mayaHelp)
        pm.menuItem(d=True)
        pm.menuItem(l='Tool HELP', c=self.show_toolHelp)


        #--- base form layout
        self._fm   = pm.formLayout(nd=100, w=415)
        self.sep0  = pm.separator()


        #-- TOP : ID -----------------------------------------------------------
        self._fmID = pm.formLayout(nd=100, w=340)
        self._txg0 = pm.textFieldButtonGrp(l=' Asset ID : ')
        self._spID = pm.separator(st='none')
        self._btID = pm.iconTextButton(l='')
        pm.setParent('..') #-- End of self._fmID

        self.pnL0  = pm.paneLayout(cn='horizontal2')


        #-- Tab Layout: --------------------------------------------------------
        self.tbL0  = pm.tabLayout(cr=True)


        #-----------------------------------------------------------------------
        #-- TAB0 : Directory ---------------------------------------------------
        self._scDr = pm.scrollLayout(cr=True)
        self._clDr = pm.columnLayout(adj=True)


        self._fr0   = pm.frameLayout(l='Work Directory')
        self._fm0   = pm.formLayout(nd=100, w=340)

        self._txgP4 = pm.textFieldButtonGrp(l='P4V Path ')
        self._btP4c = pm.iconTextButton(l=' Create')
        self._btP4o = pm.iconTextButton(l=' Open')
        self._txgLc = pm.textFieldButtonGrp(l='Local Path ')
        self._btLcc = pm.iconTextButton(l=' Create')
        self._btLco = pm.iconTextButton(l=' Open')
        self._sep0a = pm.separator(st='in')

        pm.setParent('..') #-- End of self._fm0
        pm.setParent('..') #-- End of self._fr0

        '''
        self._fmDir = pm.formLayout(nd=100)
        #-- P4V
        self._frP4V = pm.frameLayout(l='P4V')
        self._fmP4V = pm.formLayout(nd=100, w=185)

        self._txP4V = pm.text(l='_data/scenes/maya')
        self._tfP4V = pm.textField(tx='', pht='pl0000_v001_20210101.mb')
        self._spP4V = pm.separator(st='in')
        self._boP4V = pm.iconTextButton(l='') 
        self._bsP4V = pm.iconTextButton(l='') 
        self._bsP4V = pm.iconTextButton(l='') 

        pm.setParent('..') #-- End of self._fmP4V
        pm.setParent('..') #-- End of self._frP4V


        self._spDir = pm.separator(st='in', hr=False)

        #-- Local
        self._frLcl = pm.frameLayout(l='Local')
        self._fmLcl = pm.formLayout(nd=100, w=185)

        self._txLcl = pm.text(l='/maya')
        self._tfLcl = pm.textField(tx='', pht='pl0000_v001_20210101.mb')
        self._spLcl = pm.separator(st='in')

        pm.setParent('..') #-- End of self._fmLcl
        pm.setParent('..') #-- End of self._frLcl
        pm.setParent('..') #-- End of self._fmDir
        '''

        pm.setParent('..') #-- End of self._clDr
        pm.setParent('..') #-- End of self._scDr


        #-- TAB1 : CleanUP -----------------------------------------------------
        self._sc0  = pm.scrollLayout(cr=True)
        self._c0   = pm.columnLayout(adj=True)
        self._fr0a = pm.frameLayout(l='Data Cleaning')
        self._rcL0 = pm.columnLayout(adj=True, cat=('both', 0))

        cuFunc = []
        cuFunc.append(self._addCheckUI('setUnit', self._setUnit, 0))
        cuFunc.append(self._addCheckUI('delAnimKey', self._delAnimKey, 1))
        cuFunc.append(self._addCheckUI('delSkin', self._deleteSkin, 0))
        cuFunc.append(self._addCheckUI('delJoint', self._delJoint, 1))
        cuFunc.append(self._addCheckUI('resetDisplay', self._resetDisplay, 0))
        cuFunc.append(self._addCheckUI('freezeMesh', self._freezeObj, 1))
        cuFunc.append(self._addCheckUI('checkShape', self._shapeCheck, 0))
        cuFunc.append(self._addCheckUI('checkName', self._nameCheck, 1))
        cuFunc.append(self._addCheckUI('checkTexture', self._checkTexture, 0))
        cuFunc.append(self._addCheckUI('dataCleaning', self._cleanData, 1))

        pm.setParent('..') #-- End of self._rcL0

        self._fm0a = pm.formLayout(nd=100)
        self.sep1  = pm.separator(st='in')

        self.curg  = pm.radioButtonGrp(l='', la2=['Unbind', 'Keep Bind'], nrb=2)
        self.btn8  = pm.iconTextButton(l=' Run All ')

        self.sep2 = pm.separator(st='in')
        self.tx_ris = pm.text(l='Rig Information Set')
        self.itb_ris = pm.iconTextButton(l=' Create ')

        pm.setParent('..') #-- End of self._fm0a
        pm.setParent('..') #-- End of self._fr0a
        pm.setParent('..') #-- End of self._c0
        pm.setParent('..') #-- End of self._sc0


        #-- TAB1 : Export ------------------------------------------------------
        self._sc1  = pm.scrollLayout(cr=True)
        self._c1   = pm.columnLayout(adj=True)
        self._fr0b = pm.frameLayout(l='Data Export')
        self._rcL1 = pm.columnLayout(adj=True, cat=('both', 0))

        exFunc = []
        exFunc.append(self._addCheckUI('singleBindPose', self._collectBindPose, 0))
        exFunc.append(self._addCheckUI('checkSegmentScale', self._checkSSC, 1))
        exFunc.append(self._addCheckUI('checkJointOrient', self._checkJO, 0))
        exFunc.append(self._addCheckUI('deleteUnusedNode', self._deleteUnusedMaterial, 1))
        exFunc.append(self._addCheckUI('deleteDisplayLayer', self._deleteDisplayLayer, 0))
        exFunc.append(self._addCheckUI('deleteRig', self._deleteRig, 1))
        exFunc.append(self._addCheckUI('deleteFace', self._deleteFace, 0))
        exFunc.append(self._addCheckUI('deleteAnim', self._deleteAnim, 1))

        pm.setParent('..') #-- End of self._rcL1
        pm.setParent('..') #-- End of self._fm0b
        pm.setParent('..') #-- End of self._fr0b

        self._spTx = pm.separator(st='in')
        self._frTx = pm.frameLayout(l='Texture Convert')
        self._clTx = pm.columnLayout(adj=True, cat=('both', 0))

        self._btTx = pm.button(l='Convert')

        pm.setParent('..') #-- End of self._frTx
        pm.setParent('..') #-- End of self._clTx


        self._fm0b = pm.formLayout(nd=100)
        self.sep1b = pm.separator(st='in')
        self.irb   = pm.iconTextRadioCollection()
        self.irba  = pm.iconTextRadioButton('toGM', l='Game')
        self.irbb  = pm.iconTextRadioButton('toMB', l='MotionBuilder')
        self._btnb = pm.iconTextButton(l='Run All')
        self._btCk = pm.button(l='Check Tool')
        self._btEp = pm.button(l='Exporter')


        pm.setParent('..') #-- End of self._c1
        pm.setParent('..') #-- End of self._sc1


        #-----------------------------------------------------------------------
        #-- TAB2 : SETUP -------------------------------------------------------
        '''
        self._c1 = pm.columnLayout(adj=True) 
        self._fr1a = pm.frameLayout(l='Setup Tools')
        self._fm1a = pm.formLayout(nd=100)

        self.btn10a = pm.iconTextButton(l='Create Wld matrix group', c=pm.Callback(self._createWld))

        pm.setParent('..') #-- End of self._fm1a
        pm.setParent('..') #-- End of self._fr1a
        pm.setParent('..') #-- End of self._c1
        '''

        #-----------------------------------------------------------------------
        #-- TAB3 : NAME --------------------------------------------------------
        self._scNa = pm.scrollLayout(cr=True)
        self._c2   = pm.columnLayout(adj=True)
        self._fr2a = pm.frameLayout(l='Rename')
        self._c1Na = pm.columnLayout(adj=True)

        #-- Rename
        self._fmNa = pm.formLayout(nd=100)
        self._tgSr = pm.textFieldGrp(l='Search   ')
        self._pmSr = mc.popupMenu(b=3)
        self._miSc = mc.menuItem(l='Clear')
        self._miSp = mc.menuItem(d=True)
        self._miSf = mc.menuItem(l='get First')
        self._miSl = mc.menuItem(l='get Last')

        self._tgRp = pm.textFieldGrp(l='Replace   ')
        self._pmRr = mc.popupMenu(b=3)
        self._miRc = mc.menuItem(l='Clear')
        self._miRp = mc.menuItem(d=True)
        self._miRf = mc.menuItem(l='get First')
        self._miRl = mc.menuItem(l='get Last')

        self._btSR = pm.button(l='Search && Replace')
        self._spSR = pm.separator(st='in')
        pm.setParent('..') #-- End of self._fmNa

        self._fmNb = pm.formLayout(nd=100)
        self._tgPr = pm.textFieldGrp(l='Prefix   ')
        self._pmPr = mc.popupMenu(b=3)
        self._miPc = mc.menuItem(l='Clear')
        self._miPp = mc.menuItem(d=True)
        self._addMenu('name', 'prefix')
        self._btPr = pm.button(l='Add')

        self._tgSf = pm.textFieldGrp(l='Suffix   ')
        self._pmFr = mc.popupMenu(b=3)
        self._miFc = mc.menuItem(l='Clear')
        self._miFp = mc.menuItem(d=True)
        self._addMenu('name', 'suffix')
        self._btSf = pm.button(l='Add')
        self._spPS = pm.separator(st='in')
        pm.setParent('..') #-- End of self._fmNb

        self._fmNc = pm.formLayout(nd=100)
        self._tgCr = pm.textFieldGrp(l='Rename   ')
        self._ifSt = pm.intFieldGrp(nf=1, l='Start   ')  #-- base10
        self._tgSt = pm.textFieldGrp(l='Start   ')       #-- base16
        self._ifSp = pm.intFieldGrp(nf=1, l='Step   ')
        self._meBa = pm.optionMenuGrp(l='Base   ')
        self._meBb = pm.menuItem(l='10')
        self._meBh = pm.menuItem(l='16')
        self._btCr = pm.button(l='Count && Rename')
        self._spCr = pm.separator(st='in')
        pm.setParent('..') #-- End of self._fmNb

        pm.setParent('..') #-- End of self._c1Na
        pm.setParent('..') #-- End of self._fr2a

        #-- Counter
        self._fr2b = pm.frameLayout(l='Counter')
        self._c1Ct = pm.columnLayout(adj=True)

        self._fmCt = pm.formLayout(nd=100)
        self._btAc = pm.button(l='All Joint Count')

        self._rgCt = pm.radioButtonGrp(l='', la3=['Unused', 'Used', 'Select'], nrb=3)

        self._rcCt = pm.rowColumnLayout(nc=8)
        self._btC0 = pm.button(l='_0**')
        self._btC1 = pm.button(l='_1**')
        self._btC2 = pm.button(l='_2**')
        self._btC3 = pm.button(l='_3**')
        self._btC4 = pm.button(l='_4**')
        self._btC5 = pm.button(l='_5**')
        self._btC6 = pm.button(l='_6**')
        self._btC7 = pm.button(l='_7**')
        self._btC8 = pm.button(l='_8**')
        self._btC9 = pm.button(l='_9**')
        self._btCa = pm.button(l='_a**')
        self._btCb = pm.button(l='_b**')
        self._btCc = pm.button(l='_c**')
        self._btCd = pm.button(l='_d**')
        self._btCe = pm.button(l='_e**')
        self._btCf = pm.button(l='_f**')
        pm.setParent('..') #-- End of self._rcCt
        self._spCt = pm.separator(st='in')
        pm.setParent('..') #-- End of self._fmCt

        pm.setParent('..') #-- End of self._c1Ct
        pm.setParent('..') #-- End of self._fr2a


        pm.setParent('..') #-- End of self._c2
        pm.setParent('..') #-- End of self._scNa

        pm.setParent('..') #-- End of self.tbL0


        #-----------------------------------------------------------------------
        #-- Help Line | Log ---------------------------------------------------
        self._fmlg = pm.formLayout(nd=100)
        self._rllg = pm.rowLayout(nc=5)
        self._splg = pm.separator(st='none')
        self._rclg = pm.iconTextRadioCollection()
        self._btst = pm.iconTextRadioButton('logStc', l='')
        self._btss = pm.iconTextRadioButton('logSbS', l='')
        self._sph1 = pm.separator(st='single')
        self._btcl = pm.iconTextButton()
        pm.setParent('..') #-- End of self._rll
        self._scf = pm.scrollField(ed=False, ww=False, tx='', h=20, w=100)
        self._pm0 = pm.popupMenu(b=3)
        self._mi0 = pm.menuItem(l='Clear Log')
        self._hpl = pm.helpLine(h=20, w=100, bgc=(0.15, 0.15, 0.15))
        pm.setParent('..') #-- End of self._fmlg
        pm.setParent('..') #-- End of self.pnL0



        #-----------------------------------------------------------------------
        #-- Edit Controller ----------------------------------------------------
        #-- Menu
        pm.menuItem(self._lb0, c=pm.Callback(self._tabLayout), e=True)
        pm.menuItem(self._lb1, c=pm.Callback(self._tabLayout), cb=True, e=True)
        pm.menuItem(self._lb2, c=pm.Callback(self._paneLayout, 1), e=True)
        pm.menuItem(self._lb3, c=pm.Callback(self._paneLayout, 0), e=True)

        #pm.menuItem(self._lbl0, c=pm.Callback(self._changeUI), e=True)
        #pm.menuItem(self._lbl1, c=pm.Callback(self._changeUI), e=True)

        pm.menuItem(self._lba0, c=pm.Callback(self._changeUI), e=True)
        pm.menuItem(self._lba1, c=pm.Callback(self._changeUI), e=True)


        #-- Asset ID -----------------------------------------------------------
        pm.textFieldButtonGrp(self._txg0, bl=' << ', pht='pl0000', tx='', h=50,
        bc=pm.Callback(self._setID), adj=2, cw=[(1,80), (2,80), (2,30)], e=True)

        pm.iconTextButton(self._btID, st='iconOnly',
        i1='{0}/reload.png'.format(self._icon), h=24, w=30, mw=0, mh=0,
        bgc=self.btnBgc, c=pm.Callback(self._setID), e=True)


        #-- Directory ----------------------------------------------------------
        pm.frameLayout(self._fr0, bgc=(0.03, 0.20, 0.25), cll=True, e=True)

        pm.textFieldButtonGrp(self._txgP4, bl=' ... ', h=50,
        bc=pm.Callback(self.setP4VDir), adj=2, cw=[(1,70), (2,100), (2,30)], e=True)
        pm.iconTextButton(self._btP4c, st='iconAndTextHorizontal',
        i1='{0}/createP4VDir.png'.format(self._icon), h=26, w=110, mw=7, mh=2,
        bgc=self.btnBgc, c=pm.Callback(self.createP4VDir), e=True)
        pm.iconTextButton(self._btP4o, st='iconAndTextHorizontal',
        i1='{0}/openP4VDir.png'.format(self._icon), h=26, w=110, mw=7, mh=2,
        bgc=self.btnBgc, c=pm.Callback(self.openP4VDir), e=True)

        pm.textFieldButtonGrp(self._txgLc, bl=' ... ', h=50,
        bc=pm.Callback(self.setLclDir), adj=2, cw=[(1,70), (2,100), (2,30)], e=True)
        pm.iconTextButton(self._btLcc, st='iconAndTextHorizontal',
        i1='{0}/createDir.png'.format(self._icon), h=26, w=110, mw=7, mh=2,
        bgc=self.btnBgc, c=pm.Callback(self.createLclDir), e=True)
        pm.iconTextButton(self._btLco, st='iconAndTextHorizontal',
        i1='{0}/openDir.png'.format(self._icon), h=26, w=110, mw=7, mh=2,
        bgc=self.btnBgc, c=pm.Callback(self.openLclDir), e=True)

        '''
        #-- P4V ----------------------------------------------------------------
        pm.frameLayout(self._frP4V, bgc=(0.05, 0.3, 0.35), cll=True, e=True)
        pm.text(self._txP4V, al='right', e=True)
        pm.textField(self._tfP4V, tx='{0}'.format(self.workSceneFile()), h=24, e=True)


        #-- Local --------------------------------------------------------------
        pm.frameLayout(self._frLcl, bgc=(0.35, 0.3, 0.07), cll=True, e=True)
        pm.text(self._txLcl, al='right', e=True)
        pm.textField(self._tfLcl, tx='{0}'.format(self.workSceneFile()), h=24, e=True)
        '''

        #-- Cleanup ------------------------------------------------------------
        pm.frameLayout(self._fr0a, bgc=(0.35, 0.15, 0.05), cll=True, e=True)

        pm.radioButtonGrp(self.curg, cw3=[20, 90, 90], sl=1,
        cc=pm.Callback(self._changeCleanupTarget), e=True)

        pm.iconTextButton(self.btn8, st='iconAndTextHorizontal',
        c=pm.Callback(self._runAllCleaning, cuFunc), i1='execute.png',
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, e=True)

        pm.iconTextButton(self.itb_ris, st='iconAndTextHorizontal',
        c=pm.Callback(self._createRigInfoSet), i1='out_objectSet.png',
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, e=True)


        #-- Export -------------------------------------------------------------
        pm.frameLayout(self._fr0b, bgc=(0.20, 0.15, 0.35), cll=True, e=True)
        pm.frameLayout(self._frTx, bgc=(0.20, 0.15, 0.35), cll=True, en=False, e=True)
        pm.separator(self._spTx, h=20, e=True)
        pm.button(self._btTx, c=pm.Callback(self._replaceMaterial), e=True)

        pm.iconTextRadioCollection(self.irb, sl=self.irba, e=True)

        pm.iconTextRadioButton(self.irba, st='iconAndTextHorizontal',
        i='{0}tsubasa.png'.format(self._icon), h=24, w=115, mw=7, mh=2,
        bgc=self.btnBgc, onc=pm.Callback(self._changeExportTarget), e=True)

        pm.iconTextRadioButton(self.irbb, st='iconAndTextHorizontal',
        i='{0}motionbuilder.png'.format(self._icon), h=24, w=115, mw=7, mh=2,
        bgc=self.btnBgc, onc=pm.Callback(self._changeExportTarget), e=True)

        pm.iconTextButton(self._btnb, st='iconAndTextHorizontal',
        c=pm.Callback(self._runAllExport, exFunc), i1='execute.png',
        h=24, w=100, mw=7, mh=2, bgc=self.btnBgc, e=True)

        pm.button(self._btCk, c=pm.Callback(self._checkTools), h=24, w=100, e=True)
        pm.button(self._btEp, c=pm.Callback(self._exporter), h=24, w=100, e=True)


        #-- Rename ---------------------------------------------------------------
        #-- Search and Replace
        pm.frameLayout(self._fr2a, bgc=(0.2, 0.2, 0.2), cll=True, w=400, e=True)

        pm.textFieldGrp(self._tgSr, adj=2, cw2=[100, 100], e=True)
        pm.textFieldGrp(self._tgRp, adj=2, cw2=[100, 100], e=True)

        mc.menuItem(self._miSc, c=pm.Callback(self._clearField, 0), e=True)
        mc.menuItem(self._miSf, c=pm.Callback(self._getFirst, 0), e=True)
        mc.menuItem(self._miSl, c=pm.Callback(self._getLast, 0), e=True)

        mc.menuItem(self._miRc, c=pm.Callback(self._clearField, 1), e=True)
        mc.menuItem(self._miRf, c=pm.Callback(self._getFirst, 1), e=True)
        mc.menuItem(self._miRl, c=pm.Callback(self._getLast, 1), e=True)

        pm.button(self._btSR, bgc=(0.8, 0.8, 0.8), h=24,
        c=pm.Callback(self._searchAndReplace), e=True)

        #-- Prefix, Suffix
        pm.textFieldGrp(self._tgPr, adj=2, cw2=[100, 100], e=True)
        pm.textFieldGrp(self._tgSf, adj=2, cw2=[100, 100], e=True)

        mc.menuItem(self._miPc, c=pm.Callback(self._clearField, 2), e=True)
        mc.menuItem(self._miFc, c=pm.Callback(self._clearField, 3), e=True)

        pm.button(self._btPr, bgc=(0.8, 0.8, 0.8), w=50, h=18,
        c=pm.Callback(self._addPrefix), e=True)
        pm.button(self._btSf, bgc=(0.8, 0.8, 0.8), w=50, h=18,
        c=pm.Callback(self._addSuffix), e=True)

        pm.textFieldGrp(self._tgCr, adj=2, cw2=[100, 100], pht='_###', e=True)
        pm.intFieldGrp(self._ifSt, cw2=[100, 40], vis=True, e=True)
        pm.textFieldGrp(self._tgSt, cw2=[100, 40], vis=False, e=True)
        pm.intFieldGrp(self._ifSp, cw2=[40, 40], v1=1, e=True)
        pm.optionMenuGrp(self._meBa, cw2=[40, 40],
        cc=pm.Callback(self._changeBase), e=True)
        pm.button(self._btCr, bgc=(0.8, 0.8, 0.8), h=24,
        c=pm.Callback(self._countRename), e=True)

        #-- Counter
        pm.frameLayout(self._fr2b, bgc=(0.2, 0.2, 0.2), cll=True, e=True)
        pm.button(self._btAc, bgc=(0.8, 0.8, 0.8), h=22,
                  c=pm.Callback(self._countJoint), e=True)

        pm.radioButtonGrp(self._rgCt, cw4=[20, 90, 90, 90], sl=1,
        cc=pm.Callback(self._changeCleanupTarget), e=True)

        pm.button(self._btC0, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_0'), e=True)
        pm.button(self._btC1, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_1'), e=True)
        pm.button(self._btC2, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_2'), e=True)
        pm.button(self._btC3, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_3'), e=True)
        pm.button(self._btC4, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_4'), e=True)
        pm.button(self._btC5, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_5'), e=True)
        pm.button(self._btC6, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_6'), e=True)
        pm.button(self._btC7, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_7'), e=True)

        pm.button(self._btC8, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_8'), e=True)
        pm.button(self._btC9, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_9'), e=True)
        pm.button(self._btCa, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_a'), e=True)
        pm.button(self._btCb, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_b'), e=True)
        pm.button(self._btCc, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_c'), e=True)
        pm.button(self._btCd, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_d'), e=True)
        pm.button(self._btCe, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_e'), e=True)
        pm.button(self._btCf, bgc=(0.8, 0.8, 0.8), w=41, h=22,
        c=pm.Callback(self._getJointName, '_f'), e=True)


        #-- log ----------------------------------------------------------------
        pm.rowLayout(self._rllg, adj=1, cal=[(i, 'center') for i in range(1, 6)], e=True)

        pm.iconTextRadioCollection(self._rclg, sl=self._btst, e=True)
        pm.iconTextRadioButton(self._btst, st='iconAndTextHorizontal',
        i='{0}stacked.png'.format(self._icon), h=20, w=20, mw=2, mh=2,
        bgc=self.btnBgc, onc=pm.Callback(self._paneLayout, 1), e=True)
        pm.iconTextRadioButton(self._btss, st='iconAndTextHorizontal',
        i='{0}sideBySide.png'.format(self._icon), h=20, w=20, mw=2, mh=2,
        bgc=self.btnBgc, onc=pm.Callback(self._paneLayout, 0), e=True)

        pm.separator(self._sph1, w=10, h=24, e=True)
        pm.iconTextButton(self._btcl, st='iconAndTextHorizontal',
        c=pm.Callback(self._clearLog), i1='{0}clear.png'.format(self._icon),
        h=20, w=20, mw=2, mh=2, bgc=self.btnBgc, e=True)

        pm.menuItem(self._mi0, i='clearCanvas.png',
        c=pm.Callback(self._clearLog), e=True)


        #-- setup --------------------------------------------------------------
        #pm.iconTextButton(self.btn10a, st='iconAndTextHorizontal',
        #i1='showDepend.png', h=24, w=80, mw=7, mh=2, bgc=self.btnBgc, e=True)


        #-----------------------------------------------------------------------
        #-- Edit Layout --------------------------------------------------------
        t, b, l, r = 'top', 'bottom', 'left', 'right'

        pm.tabLayout(self.tbL0, bs='none', cr=True, tp='north', w=400, e=True)
        pm.paneLayout(self.pnL0, ps=(1, 100, 75), e=True)

        #-- base
        pm.formLayout(self._fm, e=True,
        af = [(self.sep0,  t,   0), (self.sep0,  l, 0), (self.sep0,  r, 0),
              (self._fmID, t,   0), (self._fmID, l, 0), (self._fmID, r, 0), (self._fmID, b, 0),
              (self.pnL0,  t,  70), (self.pnL0,  l, 0), (self.pnL0,  r, 0), (self.pnL0, b, 0)
              ])

        #-- Asset ID
        pm.formLayout(self._fmID, e=True,
        af = [(self._txg0, t, 10), (self._txg0, l, 0), (self._txg0, r, 50),
              (self._btID, t, 23), (self._btID, r, 20),
              (self._spID, t, 70), (self._spID, l, 0), (self._spID, r,  0),
              ])

        #-- Directory
        pm.formLayout(self._fm0, e=True,
        af = [(self._txgP4, t,   5), (self._txgP4, l,   0), (self._txgP4, r, 10),
              (self._btP4c, t,  45), (self._btP4c, r, 130),
              (self._btP4o, t,  45), (self._btP4o, r,  15),
              (self._txgLc, t,  80), (self._txgLc, l,   0), (self._txgLc, r, 10),
              (self._btLcc, t, 120), (self._btLcc, r, 130),
              (self._btLco, t, 120), (self._btLco, r,  15),
              (self._sep0a, t, 170), (self._sep0a, l,   0), (self._sep0a, r,  0), (self._sep0a, b,  10),
              ])
        '''
        pm.formLayout(self._fmP4V, e=True,
        af = [(self._txP4V, t,  15), (self._txP4V, l,  15), (self._txP4V, r,   5), 
              (self._tfP4V, t,  35), (self._tfP4V, l,   0), (self._tfP4V, r,   0), 
              (self._spP4V, t, 100), (self._spP4V, l,   0), (self._spP4V, r,   0), (self._spP4V, b,  15), 
              ])

        pm.formLayout(self._fmLcl, e=True,
        af = [(self._txLcl, t,  15), (self._txLcl, l,  15), (self._txLcl, r,   5), 
              (self._tfLcl, t,  35), (self._tfLcl, l,   0), (self._tfLcl, r,   0), 
              (self._spLcl, t, 100), (self._spLcl, l,   0), (self._spLcl, r,   0), (self._spLcl, b,  15), 
              ])


        pm.formLayout(self._fmDir, e=True,
        af = [(self._frP4V, t,   0), (self._frP4V, l,   0), 
              (self._frLcl, t,   0), (self._frLcl, r,   0), 
              (self._spDir, t,   0), (self._spDir, b,   0), 
              ],
        ap = [(self._frP4V, 'right', 10, 50), (self._frLcl, 'left', 5, 51),
              (self._spDir, 'right', 0, 50), 
             ])
        '''

        #-- Cleanup
        pm.formLayout(self._fm0a, e=True,
        af = [(self.sep1, t,  10), (self.sep1, l,   5), (self.sep1, r,  5),
              (self.curg, t,  30), (self.curg, l,   0),
              (self.btn8, t,  30), (self.btn8, r,  20),
              (self.sep2, t,  70), (self.sep2, l,   5), (self.sep2, r,  5),
              (self.tx_ris, t, 88), (self.tx_ris, l, 25),
              (self.itb_ris, t, 84), (self.itb_ris, r, 20),
              ])

        #-- Export
        pm.formLayout(self._fm0b, e=True,
        af = [(self.sep1b, t, 10), (self.sep1b, l,   5), (self.sep1b, r,  5),
              (self.irba,  t, 30), (self.irba,  l,  20),
              (self.irbb,  t, 30), (self.irbb,  l, 140),
              (self._btnb, t, 30), (self._btnb, r,  20),
              (self._btCk, t, 60), (self._btCk, r,  20),
              (self._btEp, t, 90), (self._btEp, r,  20),
              ])

        #-- Setup
        #pm.formLayout(self._fm1a, e=True,
        #af = [(self.btn10a, t,  20), (self.btn10a, l, 20), (self.btn10a, r, 20),
        #      ])

        #-- name
        pm.formLayout(self._fmNa, e=True,
        af = [(self._tgSr, t,  15), (self._tgSr, l, 20), (self._tgSr, r, 30),
              (self._tgRp, t,  35), (self._tgRp, l, 20), (self._tgRp, r, 30),
              (self._btSR, t,  60), (self._btSR, l, 35), (self._btSR, r, 35),
              (self._spSR, t, 100), (self._spSR, l, 10), (self._spSR, r, 10), (self._spSR, b,  5),
              ])

        pm.formLayout(self._fmNb, e=True,
        af = [(self._tgPr, t,  10), (self._tgPr, l, 20), (self._tgPr, r, 85),
              (self._btPr, t,  11), (self._btPr, r, 35),
              (self._tgSf, t,  30), (self._tgSf, l, 20), (self._tgSf, r, 85),
              (self._btSf, t,  31), (self._btSf, r, 35),
              (self._spPS, t,  65), (self._spPS, l, 10), (self._spPS, r, 10), (self._spPS, b,  5),
              ])

        pm.formLayout(self._fmNc, e=True,
        af = [(self._tgCr, t,  10), (self._tgCr, l,  20), (self._tgCr, r, 30),
              (self._ifSt, t,  35), (self._ifSt, l,  20),
              (self._tgSt, t,  35), (self._tgSt, l,  20),
              (self._ifSp, t,  35), (self._ifSp, l, 170),
              (self._meBa, t,  35), (self._meBa, l, 260),
              (self._btCr, t,  65), (self._btCr, l,  35), (self._btCr, r, 35),
              (self._spCr, t, 105), (self._spCr, l,  10), (self._spCr, r, 10), (self._spCr, b, 15),
              ])

        #-- Counter
        pm.formLayout(self._fmCt, e=True,
        af = [(self._btAc, t,  15), (self._btAc, l, 35), (self._btAc, r, 35),
              (self._rgCt, t,  50), (self._rgCt, l, 20),
              (self._rcCt, t,  80), (self._rcCt, l, 34),
              (self._spCt, t, 140), (self._spCt, l, 10), (self._spCt, r, 10),
              ])


        #-- Log
        pm.formLayout(self._fmlg, e=True,
        af = [(self._rllg, t,  0), (self._rllg, l, 5), (self._rllg, r, 5),
              (self._scf, t,  30), (self._scf, l,  5), (self._scf, r,  5), (self._scf, b,  30),
              (self._hpl, b,  5), (self._hpl, l,  5), (self._hpl, r,  5),
              ])


        #-----------------------------------------------------------------------
        # -- Tab label edit ----------------------------------------------------
        pm.tabLayout(self.tbL0, tl=[(self._scDr, 'Directory')], e=True)
        pm.tabLayout(self.tbL0, tl=[(self._sc0, 'Cleanup')], e=True)
        pm.tabLayout(self.tbL0, tl=[(self._sc1, 'Export')], e=True)
        #pm.tabLayout(self.tbL0, tl=[(self._c1, 'Setup')], e=True)
        pm.tabLayout(self.tbL0, tl=[(self._scNa, 'Name')], e=True)


        #-----------------------------------------------------------------------
        #-- UI Language --------------------------------------------------------
        self._changeUI()


        pm.window(self.windowManageName, w=self.windowSize[0], h=self.windowSize[1], e=True)
        window.show()



        #-----------------------------------------------------------------------
        #-- init command -------------------------------------------------------
        self._setID()
        #self.setP4VDir()
        #self.setLclDir()


def showUI():
    testIns = paletteUI()
    testIns.main()