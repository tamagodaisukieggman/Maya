# -*- coding: utf-8 -*-
from __future__ import absolute_import

#----- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import json


from . import _textScrollList as _tsl
from . import _setup as _su
from . import _json


#from . import _textScrollList as _tsl
#reload(_tsl)
#from . import _setup as _su
#reload(_su)
#from . import _json
#reload(_json)



class multiConnectionUI(object):
    def __init__(self):
        self.__ver__     = '0.0.2'
        self.windowName  = 'multiConnection'
        self.windowTitle = 'Multi Connection v{0}'.format(self.__ver__)
        self.windowSize  = [420, 500]
        self._maya_url   = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._help_url   = r'https://wisdom.cygames.jp/x/M_qaDQ'
        self.__project__ = pm.workspace(q=True, rd=True)
        #--- current script path -----------------------------------------------
        self.__dir = os.path.dirname(os.path.abspath(__file__))
        #-- image path ---------------------------------------------------------
        self._icon = r'{0}/_data/_icon'.format(self.__dir)
        #-- color --------------------------------------------------------------
        self.btnBgc = (0.37, 0.37, 0.37)
        #-- initial variables --------------------------------------------------
        self._jext = '*.json'


    #-- initial funsionts ------------------------------------------------------
    def checkWindowOverlap(self):
        if pm.window(self.windowName, ex=True):
            pm.deleteUI(self.windowName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._maya_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._help_url)


    #--- functions -------------------------------------------------------------
    def _importJson(self, *arg):
        strt = pm.textFieldGrp(self._txPt, tx=True, q=True)
        path = pm.fileDialog2(dir=strt, ff=self._jext, ds=2, fm=1)
        ock  = pm.checkBox(self._ckoc, v=True, q=True)

        if path:
            pm.textFieldGrp(self._txPt, tx=path[0], e=True)
            jsn = _json.importJson(path[0])
            if ock:
                src = [i for i in jsn.keys() if pm.objExists(i)]
                tgt = [i for i in jsn.values() if pm.objExists(i)]
                _tsl.reset(self._tsls, src)
                _tsl.reset(self._tslt, tgt)
                print('import successfully {0} : Object Checked.'.format(path))
            else:
                _tsl.reset(self._tsls, jsn.keys())
                _tsl.reset(self._tslt, jsn.values())
                print('import successfully {0} : Object Unchecked.'.format(path))
        pm.text(self._txSn, l='{0}'.format(_tsl.count(self._tsls)), e=True)
        pm.text(self._txTn, l='{0}'.format(_tsl.count(self._tslt)), e=True)
        return path


    def _exportJson(self, *arg):
        path = pm.fileDialog2(ff=self._jext, ds=2, okc='Export', bbo=1)
        if path:
            pm.textFieldGrp(self._txPt, tx=path[0], e=True)
            jsn = _json.zipJson(pm.textScrollList(self._tsls, ai=True, q=True),
                                pm.textScrollList(self._tslt, ai=True, q=True))
            print(jsn)
            _json.exportJson(path[0], jsn)
        return path


    def _getNode(self, _list_, _num_, *args):
        obj = [i.name() for i in pm.ls(sl=True, typ='transform')]
        _tsl.add(_list_, obj)
        pm.text(_num_, l='{0}'.format(_tsl.count(_list_)), e=True)


    def _moveUP(self, _list_, *args):
        _tsl.moveUp(_list_)


    def _moveDown(self, _list_, *args):
        _tsl.moveDown(_list_)


    def _remove(self, _list_, _num_, *args):
        _tsl.remove(_list_)
        pm.text(_num_, l='{0}'.format(_tsl.count(_list_)), e=True)


    def _clearList(self, _list_, _num_, *args):
        pm.textScrollList(_list_, ra=True, e=True)
        pm.text(_num_, l='0', e=True)


    def _sort(self, _list_, *args):
        _tsl.sort(_list_)


    def _reverse(self, _list_, *args):
        _tsl.reverse(_list_)


    def _replace(self, _list_, *args):
        _tsl.replaceText(_list_, s, t)


    def _select(self, _list_, *args):
        _tsl.select(_list_)


    def _replacePrompt(self, *args):
        #-- Get the dialog's Layout.
        #self._rpFmL = pm.setParent(q=True)_rpFmL
        #-- Layout
        self._rpFmL = pm.formLayout(nd=100)
        self._rptxt = pm.text(l='Enter Text')
        self._rptf1 = pm.textFieldGrp(l='', tx='', pht='Search...', 
                                      adj=2, h=26, cw2=[0,100])
        self._rptf2 = pm.textFieldGrp(l='', tx='', pht='Replace...', 
                                      adj=2, h=26, cw2=[0,100])
        self._rpbt1 = pm.button(l='Replace', w=100, 
                                c=pm.Callback(self._dismiss))
        self._rpbt2 = pm.button(l='Cancel', w=100, 
                                c='pm.layoutDialog(dis="Cancel")')

        #-- edit
        t, b, l, r = ['top', 'bottom', 'left', 'right']

        pm.formLayout(self._rpFmL, e=True,
        af = [(self._rptxt, t, 10), (self._rptxt, l,  10), 
              (self._rptf1, t, 30), (self._rptf1, l,   5), (self._rptf1, r, 0), 
              (self._rptf2, t, 55), (self._rptf2, l,   5), (self._rptf2, r, 0), 
              (self._rpbt1, t, 90), (self._rpbt1, r, 110), (self._rpbt1, b, 5), 
              (self._rpbt2, t, 90), (self._rpbt2, r,   5), (self._rpbt2, b, 5), 
              ])

    def _dismiss(self, *args):
        s = pm.textFieldGrp(self._rptf1, tx=True, q=True)
        t = pm.textFieldGrp(self._rptf2, tx=True, q=True)
        pm.layoutDialog(dis='Replace,{0},{1}'.format(s, t))


    def _replaceText(self,  _list_, *args):
        res = pm.layoutDialog(ui=self._replacePrompt)
        if 'Replace' in res:
            s = res.split(',')[1]
            t = res.split(',')[0]
            _tsl.replaceText(_list_, s, t)


    def _addPrefix(self, _list_, *args):
        res = pm.promptDialog(t='Add Prefix', m='Enter Name:',
                              b=['Add', 'Cancel'], db='Cancel', 
                              cb='Cancel', ds='Cancel', st='text')
        if res == 'Add':
            pre = pm.promptDialog(tx=True, q=True)
            _tsl.addPrefix(_list_, pre)


    def _addSuffix(self, _list_, *args):
        res = pm.promptDialog(t='Add Suffix', m='Enter Name:',
                              b=['Add', 'Cancel'], db='Cancel', 
                              cb='Cancel', ds='Cancel', st='text')
        if res == 'Add':
            suf = pm.promptDialog(tx=True, q=True)
            _tsl.addSuffix(_list_, suf)


    def _connect(self, *args):
        src = pm.textScrollList(self._tsls, ai=True, q=True)
        tgt = pm.textScrollList(self._tslt, ai=True, q=True)
        siz = min(len(src), len(tgt))

        t = pm.checkBox(self._ckbT, v=True, q=True)
        r = pm.checkBox(self._ckbR, v=True, q=True)
        s = pm.checkBox(self._ckbS, v=True, q=True)

        for i in range(siz):
            _su.multiConstraint(src[i], tgt[i], t, r, s)
            #_su.worldConnection(src[i], tgt[i])


    #--- edit UI ---------------------------------------------------------------
    def _addListMenu(self, *args):
        m0  = pm.menuItem(d=True, l='Edit')
        m1  = pm.menuItem(l='Add Selected')
        m2  = pm.menuItem(l='Remove')
        m3  = pm.menuItem(l='Clear List')
        m4  = pm.menuItem(d=True, l='Order')
        m5  = pm.menuItem(l='Sort')
        m6  = pm.menuItem(l='Reverse')
        m7  = pm.menuItem(d=True, l='Text')
        m8  = pm.menuItem(l='Add Prefix')
        m9  = pm.menuItem(l='Add Suffix')
        m10 = pm.menuItem(l='Replace Text')
        return [m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10]


    def _editListMenu(self, uil, _list_, _num_, *args):
        pm.menuItem(uil[1], e=True, c=pm.Callback(self._getNode, _list_, _num_),
                    i='{0}/plus2.png'.format(self._icon))
        pm.menuItem(uil[2], e=True, c=pm.Callback(self._remove, _list_, _num_),
                    i='{0}/delete.png'.format(self._icon))
        pm.menuItem(uil[3], e=True, c=pm.Callback(self._clearList, _list_, _num_),
                    i='{0}/clear.png'.format(self._icon))

        pm.menuItem(uil[5], e=True, c=pm.Callback(self._sort, _list_),
                    i='{0}/sort.png'.format(self._icon))
        pm.menuItem(uil[6], e=True, c=pm.Callback(self._reverse, _list_),
                    i='{0}/reverse.png'.format(self._icon))

        pm.menuItem(uil[8], e=True, c=pm.Callback(self._addPrefix, _list_),
                    i='{0}/add.png'.format(self._icon))
        pm.menuItem(uil[9], e=True, c=pm.Callback(self._addSuffix, _list_),
                    i='{0}/add.png'.format(self._icon))
        pm.menuItem(uil[10], e=True, c=pm.Callback(self._replaceText, _list_),
                    i='{0}/replace.png'.format(self._icon))


    #--- main UI ---------------------------------------------------------------
    def main(self):
        self.checkWindowOverlap()
        window = pm.window(self.windowName, mb = True,
                           t = self.windowTitle,
                           w = self.windowSize[0],
                           h = self.windowSize[1])

        #-- menu ---------------------------------------------------------------
        pm.menu(l='Source')
        self._mSrc = self._addListMenu()
        pm.menu(l='Target')
        self._mTgt = self._addListMenu()
        pm.menu(l='Help', hm=True)
        pm.menuItem(l='Maya 2019 HELP', c=self.show_mayaHelp)
        pm.menuItem(d=True)
        pm.menuItem(l='Tool HELP', c=self.show_toolHelp)


        #-- layout -------------------------------------------------------------
        #-- Pane Layout
        self._fmL_ = pm.formLayout(nd=100)
        self._sep_ = pm.separator()

        self._txPt = pm.textFieldGrp(l='', tx=self.__project__, pht='Path...')
        self._ibti = pm.iconTextButton(l='')
        self._ibto = pm.iconTextButton(l='')
        self._ckoc = pm.checkBox(l='Object Check')
        self._sep0 = pm.separator(st='in')

        self._pnL0 = pm.paneLayout(cn='vertical2')

        self._fmLL = pm.formLayout(nd=100, w=160)
        self._txSr = pm.text(l='Source:')
        self._txSn = pm.text(l='0')
        self._rwLs = pm.rowLayout(nc=5, h=30)
        self._ibo0 = pm.iconTextButton(l='')
        self._ibo1 = pm.iconTextButton(l='')
        self._ibo2 = pm.iconTextButton(l='')
        self._ibo3 = pm.iconTextButton(l='')
        self._ibo4 = pm.iconTextButton(l='')
        pm.setParent('..') #-- End of self._rwLs
        self._tsls = pm.textScrollList()
        self._pmSr = pm.popupMenu(b=3)
        self._meSr = self._addListMenu()
        pm.setParent('..') #-- End of self._fmLL

        self._fmLR = pm.formLayout(nd=100, w=160)
        self._txTg = pm.text(l='Target:')
        self._txTn = pm.text(l='0')
        self._rwLt = pm.rowLayout(nc=5, h=30)
        self._ibi0 = pm.iconTextButton(l='')
        self._ibi1 = pm.iconTextButton(l='')
        self._ibi2 = pm.iconTextButton(l='')
        self._ibi3 = pm.iconTextButton(l='')
        self._ibi4 = pm.iconTextButton(l='')
        pm.setParent('..') #-- End of self._rwLt
        self._tslt = pm.textScrollList()
        self._pmTg = pm.popupMenu(b=3)
        self._meTg = self._addListMenu()
        pm.setParent('..') #-- End of self._fmLR

        pm.setParent('..') #-- End of self._pnL0

        self._sep1 = pm.separator(st='in')
        self._fmLC = pm.formLayout(nd=100)
        self._ckbT = pm.checkBox(l='T')
        self._ckbR = pm.checkBox(l='R')
        self._ckbS = pm.checkBox(l='S')
        self._ibRn = pm.button(l='Run')
        pm.setParent('..') #-- End of self._fmLC


        #-----------------------------------------------------------------------
        #--- Edit UI elements --------------------------------------------------
        pm.textFieldGrp(self._txPt, adj=2, h=26, cw2=[0,100], e=True)

        pm.iconTextButton(self._ibti, c=pm.Callback(self._importJson),
        st='iconAndTextHorizontal', i1='{0}/import.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.iconTextButton(self._ibto, c=pm.Callback(self._exportJson),
        st='iconAndTextHorizontal', i1='{0}/export.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.checkBox(self._ckoc, al='right', v=True, e=True)

        pm.iconTextButton(self._ibo0, 
        c=pm.Callback(self._getNode, self._tsls, self._txSn),
        st='iconAndTextHorizontal', i1='{0}/addSel.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.iconTextButton(self._ibo1, 
        c=pm.Callback(self._moveUP, self._tsls),
        st='iconAndTextHorizontal', i1='{0}/moveUp.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.iconTextButton(self._ibo2, 
        c=pm.Callback(self._moveDown, self._tsls),
        st='iconAndTextHorizontal', i1='{0}/moveDown.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.iconTextButton(self._ibo3, 
        c=pm.Callback(self._remove, self._tsls, self._txSn),
        st='iconAndTextHorizontal', i1='{0}/delete.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.iconTextButton(self._ibo4, 
        c=pm.Callback(self._clearList, self._tsls, self._txSn),
        st='iconAndTextHorizontal', i1='{0}/clear.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.textScrollList(self._tsls, ams=True, 
        dcc=pm.Callback(self._select, self._tsls), e=True)


        pm.iconTextButton(self._ibi0, 
        c=pm.Callback(self._getNode, self._tslt, self._txTn),
        st='iconAndTextHorizontal', i1='{0}/addSel.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.iconTextButton(self._ibi1, 
        c=pm.Callback(self._moveUP, self._tslt),
        st='iconAndTextHorizontal', i1='{0}/moveUp.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.iconTextButton(self._ibi2, 
        c=pm.Callback(self._moveDown, self._tslt),
        st='iconAndTextHorizontal', i1='{0}/moveDown.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.iconTextButton(self._ibi3,
        c=pm.Callback(self._remove, self._tslt, self._txTn),
        st='iconAndTextHorizontal', i1='{0}/delete.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.iconTextButton(self._ibi4, 
        c=pm.Callback(self._clearList, self._tslt, self._txTn),
        st='iconAndTextHorizontal', i1='{0}/clear.png'.format(self._icon),
        h=24, w=24, mw=2, mh=2, bgc=self.btnBgc, fla=False, e=True)

        pm.textScrollList(self._tslt, ams=True, 
        dcc=pm.Callback(self._select, self._tslt), e=True)


        pm.checkBox(self._ckbT, w=50, v=True, e=True)
        pm.checkBox(self._ckbR, w=50, v=True, e=True)
        pm.checkBox(self._ckbS, w=50, v=True, e=True)


        pm.button(self._ibRn, c=pm.Callback(self._connect), e=True)

        self._editListMenu(self._mSrc, self._tsls, self._txSn)
        self._editListMenu(self._mTgt, self._tslt, self._txTn)
        self._editListMenu(self._meSr, self._tsls, self._txSn)
        self._editListMenu(self._meTg, self._tslt, self._txTn)


        #-----------------------------------------------------------------------
        #--- Edit UI Layout ----------------------------------------------------
        t, b, l, r = ['top', 'bottom', 'left', 'right']

        pm.formLayout(self._fmL_, e=True,
               af = [(self._sep_, t,   0), (self._sep_, l,   0), (self._sep_, r,  0), 
                     (self._txPt, t,  20), (self._txPt, l,  10), (self._txPt, r, 65), 
                     (self._ibti, t,  20), (self._ibti, r,  40), 
                     (self._ibto, t,  20), (self._ibto, r,  10), 
                     (self._ckoc, t,  50), (self._ckoc, r,  65), 
                     (self._sep0, t,  75), (self._sep0, l,   5), (self._sep0, r,  5), 
                     (self._pnL0, t,  80), (self._pnL0, l,   5), (self._pnL0, r,  5), (self._pnL0, b, 50), 
                     (self._sep1, l,   5), (self._sep1, r,   5), (self._sep1, b, 45), 
                     (self._fmLC, l,   5), (self._fmLC, r,   5), (self._fmLC, b, 10), 
                    ])

        pm.formLayout(self._fmLL, e=True,
               af = [(self._txSr, t,  8), (self._txSr, l,  5),
                     (self._txSn, t,  8), (self._txSn, l, 60),
                     (self._rwLs, t,  0), (self._rwLs, r,  0),
                     (self._tsls, t, 35), (self._tsls, l,  0), (self._tsls, r, 0), (self._tsls, b, 5), 
                    ])

        pm.formLayout(self._fmLR, e=True,
               af = [(self._txTg, t,  8), (self._txTg, l,  5),
                     (self._txTn, t,  8), (self._txTn, l, 60),
                     (self._rwLt, t,  0), (self._rwLt, r,  0),
                     (self._tslt, t, 35), (self._tslt, l,  0), (self._tslt, r, 0), (self._tslt, b, 5), 
                    ])

        pm.formLayout(self._fmLC, e=True,
               af = [(self._ckbT, t,  2), (self._ckbT, l,  10),
                     (self._ckbR, t,  2), (self._ckbR, l,  50),
                     (self._ckbS, t,  2), (self._ckbS, l,  90),
                     (self._ibRn, t,  0), (self._ibRn, l, 140), (self._ibRn, r, 5),
                    ])


        window.show()

        #-- init command -------------------------------------------------------
        pm.window(self.windowName, e=True,
                  w = self.windowSize[0], 
                  h = self.windowSize[1])


def showUI():
    testIns = multiConnectionUI()
    testIns.main()

