# -*- coding: utf-8 -*-
from __future__ import absolute_import

#----- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import json
import socket


#-- import bootstrap
#import bootstrap
#import bootstrap.core as mbc

#-- shr3d.rig
import shr3d.rig.bootstrap as bootstrap
import shr3d.rig.bootstrap.core as mbc


from . import core as stc


import importlib
importlib.reload(mbc)
importlib.reload(stc)


class startupUI(object):
    def __init__(self):
        self.__ver__     = '0.0.4'
        self.windowName  = 'startup'
        self.windowTitle = 'Startup v{0}'.format(self.__ver__)
        self.windowSize  = [400, 400]
        self._maya_url   = r'https://help.autodesk.com/view/MAYAUL/2022/JPN/'
        self._help_url   = r'https://help.autodesk.com/view/MAYAUL/2022/JPN/'
        #--- current script path -----------------------------------------------
        self._dir = os.path.dirname(os.path.abspath(__file__))
        self._mbc = bootstrap.__path__[0].replace('\\', '/') #-- bootstrap path
        #-- image path ---------------------------------------------------------
        self._ico = os.path.join(self._dir, r'_data/_icon').replace(os.sep, '/')
        self._bic = os.path.join(self._mbc, r'_icon').replace(os.sep, '/')
        #-- color --------------------------------------------------------------
        self.btnBgc = (0.37, 0.37, 0.37)
        self.frmBgc = (0.169, 0.169, 0.169)
        self.frmBsa = (0.11, 0.11, 0.20)
        self.frmBnw = (0.11, 0.20, 0.11)
        self.frmBer = (0.20, 0.11, 0.11)
        self.fomBgc = (0.25, 0.25, 0.25)
        self.txfBgc = (0.15, 0.15, 0.15)
        #-- initial variables --------------------------------------------------
        self.p4Rig  = stc.astP['p4vRig']
        self.p4Chr  = stc.astP['p4vCh']
        self.WmRig  = stc.astP['workman']
        self.DcRig  = stc.astP['user']
        self.user = stc.user
        self.ctgr = stc.aCtg
        self._aID = stc.getIDFromRoot()
        #-- asset info ---------------------------------------------------------
        self.aAll = ''
        self.aID  = ''
        self.aTyp = ''
        self.aStr = ''
        self.aCtg = ''


    #---------------------------------------------------------------------------
    #-- initial funsionts ------------------------------------------------------
    def checkWindowOverlap(self):
        if pm.window(self.windowName, ex=True):
            pm.deleteUI(self.windowName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)


    #---------------------------------------------------------------------------
    #--- functions -------------------------------------------------------------
    def check(self, *args):
        print (True)


    #-- set default unit environment -------------------------------------------
    def setDefaultUnitEnv(self, *args):
        print('------------------- Set Unit Log ------------------------------')
        mbc.setGrid(200.0, 50.0, 5)
        mbc.setCam(50)
        mbc.setJointSize(1.0)
        mbc.setSceneUnit('cm', 'deg', '60fps')
        mbc.setTimeRange(0, 10)
        #-- load plugin
        pList = ['matrixNodes', 'mayaHIK', 'mayaCharacterization', 'OneClick']
        for i in pList:
            mbc.checkLoadPlugin(i)
        #-- unload turtle
        stc.turtleKiller()


    #---------------------------------------------------------------------------
    #-- Get Asset Infomation ---------------------------------------------------
    def setInitAssetInfo(self, rootID='', *args):
        aAll, aID, aTyp, aStr, aCtg = [None, None, None, None, None]
        if rootID:
            aAll, aID, aTyp, aStr, aCtg = stc.getAssetInfo(rootID)
            self.aAll = aAll
            self.aID  = aID
            self.aTyp = aTyp
            self.aStr = aStr
            self.aCtg = aCtg
        infoTxt = f'all string  :  {self.aAll} \n' \
                  f'asset ID    :  {self.aID} \n' \
                  f'type        :  {self.aTyp} \n' \
                  f'name        :  {self.aStr} \n' \
                  f'category    :  {self.aCtg} '
        pm.text(self.txAti, l=infoTxt, e=True)
        return [aAll, aID, aTyp, aStr, aCtg]


    def resetInitAssetInfo(self, *args):
        self.aAll = ''
        self.aID  = ''
        self.aTyp = ''
        self.aStr = ''
        self.aCtg = ''
        infoTxt = f'all string  :  {self.aAll} \n' \
                  f'asset ID    :  {self.aID} \n' \
                  f'type        :  {self.aTyp} \n' \
                  f'name        :  {self.aStr} \n' \
                  f'category    :  {self.aCtg} '
        pm.text(self.txAti, l=infoTxt, e=True)


    def setAssetInfo(self, *args):
        rootID = stc.getIDFromRoot()
        if rootID:
            aAll, aID, aTyp, aStr, aCtg = stc.getAssetInfo(rootID)
        else:
            res = pm.promptDialog(t='Asset ID', m='Enter Name: ', 
                                  b=['Set', 'Cancel'], db='Set', 
                                  cb='Cancel', ds='Cancel')
            if res == 'Set':
                rootID = pm.promptDialog(tx=True, q=True)
                if rootID:
                    aAll, aID, aTyp, aStr, aCtg = stc.getAssetInfo(rootID)

        if aID and aStr:
            self.refleshAssetInfo(rootID) #-- Reflesh Asset Information


    def refleshAssetInfo(self, rootID='', *args):
        aAll, aID, aTyp, aStr, aCtg = stc.getAssetInfo(rootID)
        if aID and aStr:
            #-- Set Asset String
            self.setInitAssetInfo(rootID)
            #-- Set Asset Info
            pm.optionMenu(self.omAst, v=aCtg, e=True)
            pm.textField(self.tfAID, tx=aID, e=True)
            pm.textField(self.tfANA, tx=aStr, e=True)
            #-- asset path
            lv = stc.midPathExists(aCtg, aID, aStr)
            if lv[0]:
                pm.textField(self.tfWkp, tx=lv[1], e=True)
            else:
                pm.textField(self.tfWkp, pht=lv[1], e=True)
            #-- file name
            self.setFileName()
            self.setFileNamePopupMenu()
        else:
            pm.warning(f'{rootID} is doesn\'t exsit in P4V path. please check asset ID.')


    def getAssetList(self, cat='', *args):
        allList = []
        res = []
        for fd_path, sb_folder, sb_file in os.walk(self.p4Chr):
            for f in sb_folder:
                if '_' in f.split(os.sep)[-1]:
                    allList.append(f)
        if cat == '--':
            return allList
        else:
            res = [i for i in allList for pre in self.ctgr[cat] if pre in i]
            return res


    def createAssetDir(self, *args):
        cta, aID, aSt = self.getAssetValues()
        if aID and aSt:
            stc.createDirectory(cta, aID, aSt)
            self.getCurrentWorkspace()
        else:
            pm.warning('Please Fill in Asset Type, ID, and Dev Name.')


    #---------------------------------------------------------------------------
    #-- Local Path -------------------------------------------------------------
    def getCurrentWorkspace(self, *args):
        crp = pm.workspace(rd=True, q=True).replace(os.sep, '/')
        pm.textField(self.tfLcp, tx=crp, e=True)


    def setCurrentWorkspace(self, *args):
        pm.mel.eval('SetProject;')
        crp = pm.workspace(rd=True, q=True).replace(os.sep, '/')
        pm.textField(self.tfLcp, tx=crp, e=True)
        self.setAssetInfo()


    def setFileName(self, *args):
        #-- set File Name -> self.tfFln
        cta, aID, aSt = self.getAssetValues()
        path  = stc.getWorkPath(cta, aID, aSt)
        fList = stc.getFileList(path, 1, aID)
        if fList:
            pm.textField(self.tfFln, tx=fList[-1], e=True)
        else:
            pm.textField(self.tfFln, tx='', e=True)


    def replaceFileName(self, fName='', *args):
        pm.textField(self.tfFln, tx=fName, e=True)
        self.checkData()


    def newFile(self, *args):
        pm.mel.eval('file -f -new;')
        self.resetAssetValues()
        self.resetPathValues()
        self.resetInitAssetInfo()
        self.checkData()
        self.resetP4VPath()


    def openFile(self, *args):
        prj, atp, fna = self.getPathValues()
        fPath = os.path.join(prj, atp, fna).replace(os.sep, '/')
        stc.openFile(fPath)


    def saveFile(self, *args):
        prj, atp, fna = self.getPathValues()
        fPath = os.path.join(prj, atp, fna).replace(os.sep, '/')
        stc.saveFile(fPath)
        self.setFileNamePopupMenu()
        self.checkData()


    def openDir(self, *args):
        prj, atp, fna = self.getPathValues()
        fPath = os.path.join(prj, atp).replace(os.sep, '/')
        if os.path.isdir(fPath):
            os.startfile(fPath)


    def openProject(self, *args):
        prj, atp, fna = self.getPathValues()
        fPath = prj.replace(os.sep, '/')
        if os.path.isdir(fPath):
            os.startfile(fPath)


    def updateFileName(self, val=1, *args):
        #-- update file ver feature
        fileName = pm.textField(self.tfFln, tx=True, q=True)
        fName    = stc.updateFileName(name=fileName, v=val)
        pm.textField(self.tfFln, tx=fName, e=True)
        self.checkData()
        print(f'Set File Name: {fileName} -> {fName}')


    def updateDate(self, *args):
        #-- update file data feature
        fileName = pm.textField(self.tfFln, tx=True, q=True)
        fName = stc.updateDate(name=fileName)
        pm.textField(self.tfFln, tx=fName, e=True)
        self.checkData()
        print(f'Set File Data: {fileName} -> {fName}')


    def checkData(self, *args):
        prj, atp, fna = self.getPathValues()
        if os.path.isdir(os.path.join(prj, atp)):
            path  = os.path.join(prj, atp)
            fPath = os.path.join(prj, atp, fna)
            aID   = pm.textField(self.tfAID, tx=True, q=True)
            val   = stc.checkVer(path, aID, fna)

            if val == 0:   #-- v020 == v020 -- same ver
                pm.textField(self.tfFln, tx=fna, pht='FileName.mb...', 
                    bgc=self.frmBsa, e=True)

            elif val == 1:  #-- v021 > v020 -- new ver
                pm.textField(self.tfFln, tx=fna, pht='FileName.mb...',
                    bgc=self.frmBnw, e=True)

            elif val == -1:  #-- v019 < v020 -- error
                pm.textField(self.tfFln, tx=fna, pht='FileName.mb...', 
                    bgc=self.frmBer, e=True)

            else: #-- not exists
                pm.textField(self.tfFln, tx=fna, pht='FileName.mb...', 
                    bgc=self.frmBgc, e=True)

        else:
            pm.textField(self.tfFln, tx=fna, pht='FileName.mb...', 
                bgc=self.frmBgc, e=True)


    def resetAssetValues(self, *args):
        pm.optionMenu(self.omAst, v='--', e=True)
        pm.textField(self.tfAID, tx='', pht='xxx0000', e=True)
        pm.textField(self.tfANA, tx='', pht='devname', e=True)


    def resetPathValues(self, *args):
        pm.textField(self.tfWkp, tx='', pht='scenes/...', e=True)
        pm.textField(self.tfFln, tx='', pht='FileName.mb...', e=True)
        self.setFileNamePopupMenu()


    def setFileNamePopupMenu(self, typ=1, *args):
        fList = []
        cta, aID, aSt = self.getAssetValues()
        path  = stc.getWorkPath(cta, aID, aSt)
        if os.path.isdir(path):
            fList = stc.getFileList(path, typ, aID)
        #-- check UI
        if pm.popupMenu('filePopup', ex=True):
            pm.deleteUI('filePopup')

        #-- directory
        pm.popupMenu('filePopup', b=1, p=self.ibFll)
        pm.menuItem(l='Open Directory', c=pm.Callback(self.openDir))    
        pm.menuItem(d=True)

        #-- add data
        if fList:
            for fName in fList:
                pm.menuItem(l=fName, c=pm.Callback(self.replaceFileName, fName))
        else:
            pass


    #---------------------------------------------------------------------------
    #-- P4V Path ---------------------------------------------------------------
    def setP4VPath(self, *args):
        #-- P4V path
        pm.textField(self.tfP4p, tx=self.p4Rig, e=True) 
        #-- P4V mid path
        self.setP4VMidPath()
        #-- File list
        self.setP4vFileName()
        self.setP4VFileNamePopupMenu()
        #-- Outsource file list
        self.setP4VOutsourceFile()
        self.setP4VOutsourceFileNamePopupMenu()
        

    def resetP4VPath(self, *args):
        pm.textField(self.tfP4m, tx='', e=True)
        pm.textField(self.tfP4f, tx='', e=True)
        pm.textField(self.tfP4O, tx='', e=True)
        self.setP4VFileNamePopupMenu()
        self.setP4VOutsourceFileNamePopupMenu()


    def getP4VPath(self, *args):
        P4p = pm.textField(self.tfP4p, tx=True, q=True) 
        P4m = pm.textField(self.tfP4m, tx=True, q=True)
        path = os.path.join(P4p, P4m).replace(os.sep, '/')
        return path


    def setP4VMidPath(self, *args):
        if self.aID:
            aAll, aID, aTyp, aStr, aCtg = stc.getAssetInfo(self.aID)
            mid = stc.midP4VPathExists(self.p4Rig, aCtg, aID, aStr)
            if mid[0]:
                pm.textField(self.tfP4m, tx=mid[1], e=True) 
            else:
                pm.textField(self.tfP4m, pht=mid[1], e=True)
        else:
            pm.textField(self.tfP4m, tx='', pht='asset/...', e=True) 


    def openP4VPath(self, *args):
        P4p = pm.textField(self.tfP4p, tx=True, q=True) 
        if os.path.isdir(P4p):
            os.startfile(P4p)


    def openP4VFilePath(self, *args):
        path = self.getP4VPath()
        if os.path.isdir(path):
            os.startfile(path)


    def setP4VPopupMenu(self, *args):
        pm.popupMenu(b=1, p=self.ibP4p)
        pm.menuItem(l='Open P4V Directory', c=pm.Callback(self.openP4VPath))


    def setP4VFileNamePopupMenu(self, *args):
        fList = []
        ctg, aID, aStr = self.getAssetValues()
        path = self.getP4VPath()
        if os.path.isdir(path):
            fList = stc.getFileList(path, 1, aID)

        #-- check UI
        if pm.popupMenu('P4vPopup', ex=True):
            pm.deleteUI('P4vPopup')

        #-- directory
        pm.popupMenu('P4vPopup', b=1, p=self.ibP4f)
        pm.menuItem(l='Open Directory', c=pm.Callback(self.openP4VFilePath))    
        pm.menuItem(d=True)

        #-- add data
        if fList:
            for fName in fList:
                pm.menuItem(l=fName, c=pm.Callback(self.replaceP4VFileName, fName))
        else:
            pass


    def setP4vFileName(self, *args):
        fList = []
        ctg, aID, aStr = self.getAssetValues()
        path = self.getP4VPath()
        if os.path.isdir(path):
            fList = stc.getFileList(path, 1, aID)
        if fList:
            pm.textField(self.tfP4f, tx=fList[-1], e=True)
        else:
            pm.textField(self.tfP4f, tx='', e=True)


    def replaceP4VFileName(self, fName='', *args):
        pm.textField(self.tfP4f, tx=fName, e=True)


    def openP4VFile(self, typ=0, *args):
        p4v = self.getP4VPath()
        p4f = pm.textField(self.tfP4f, tx=True, q=True)
        p4o = pm.textField(self.tfP4O, tx=True, q=True)
        if typ == 0: #-- work file
            fPath = os.path.join(p4v, p4f).replace(os.sep, '/')
        elif typ == 1: #-- outsource file
            p4v = p4v.replace('/work/maya', '/outsource')
            fPath = os.path.join(p4v, p4o).replace(os.sep, '/')
        stc.openFile(fPath)


    #-- Outsource
    def setP4VOutsourceFile(self, *args):
        fList = []
        ctg, aID, aStr = self.getAssetValues()
        path = self.getP4VPath()
        path = path.replace('/work/maya', '/outsource')
        if os.path.isdir(path):
            fList = stc.getFileList(path, 1, aID)
        if fList:
            pm.textField(self.tfP4O, tx=fList[-1], e=True)
        else:
            pm.textField(self.tfP4O, tx='', e=True)


    def openP4VOutsource(self, *args):
        path = self.getP4VPath()
        path = path.replace('/work/maya', '/outsource')
        if os.path.isdir(path):
            os.startfile(path)


    def setP4VOutsourceFileNamePopupMenu(self, *args):
        fList = []
        ctg, aID, aStr = self.getAssetValues()
        path = self.getP4VPath()
        path = path.replace('work/maya', 'outsource')
        if os.path.isdir(path):
            fList = stc.getFileList(path, 1, aID)

        #-- check UI
        if pm.popupMenu('P4vOutsourcePopup', ex=True):
            pm.deleteUI('P4vOutsourcePopup')

        #-- directory
        pm.popupMenu('P4vOutsourcePopup', b=1, p=self.ibP4O)
        pm.menuItem(l='Open Outsource Directory', 
                    c=pm.Callback(self.openP4VOutsourceFilePath))    
        pm.menuItem(d=True)

        #-- add data
        if fList:
            for fName in fList:
                pm.menuItem(l=fName, c=pm.Callback(self.replaceP4VOutsourceFileName, fName))
        else:
            pass


    def openP4VOutsourceFilePath(self, *args):
        path = self.getP4VPath()
        path = path.replace('work/maya', 'outsource')
        if os.path.isdir(path):
            os.startfile(path)


    def replaceP4VOutsourceFileName(self, fName='', *args):
        pm.textField(self.tfP4O, tx=fName, e=True)


    #---------------------------------------------------------------------------
    #-- Workman Path -----------------------------------------------------------
    def setWorkmanPath(self, *args):
        pm.textField(self.tfWmp, tx=self.WmRig, e=True)
        self.setWorkmanMidPath()
        self.setWorkmanFileName()
        self.setWorkmanFileNamePopupMenu()


    def resetP4VPath(self, *args):
        pm.textField(self.tfWmm, tx='', e=True)
        pm.textField(self.tfWmf, tx='', e=True)
        self.setWorkmanFileNamePopupMenu()


    def getWorkmanPath(self, *args):
        wmp = pm.textField(self.tfWmp, tx=True, q=True) 
        wmm = pm.textField(self.tfWmm, tx=True, q=True)
        path = os.path.join(wmp, wmm).replace(os.sep, '/')
        return path


    def setWorkmanMidPath(self, *args): 
        if self.aID:
            aAll, aID, aTyp, aStr, aCtg = stc.getAssetInfo(self.aID)
            mid = stc.midWorkmanPathExists(self.WmRig, aCtg, aID, aStr)
            if mid[0]:
                pm.textField(self.tfWmm, tx=mid[1], e=True) 
            else:
                pm.textField(self.tfWmm, pht=mid[1], e=True) 
        else:
            pm.textField(self.tfWmm, tx='', pht='asset/...', e=True) 


    def openWorkmanPath(self, typ=0, *args):
        wmp  = pm.textField(self.tfWmp, tx=True, q=True)
        wmm  = pm.textField(self.tfWmm, tx=True, q=True)
        wmf  = pm.textField(self.tfWmf, tx=True, q=True)
        path = os.path.join(wmp, wmm).replace(os.sep, '/')
        if typ == 0: #-- open workman project
            os.startfile(wmp)
        elif typ == 1: #-- open workman file path
            os.startfile(path)


    def setWorkmanPopupMenu(self, *args):
        pm.popupMenu(b=1, p=self.ibWmp)
        pm.menuItem(l='Open Workman Directory', 
                    c=pm.Callback(self.openWorkmanPath, 0))


    def setWorkmanFileNamePopupMenu(self, *args):
        fList = []
        cta, aID, aSt = self.getAssetValues()
        path = self.getWorkmanPath()

        if os.path.isdir(path):
            fList = stc.getFileList(path, 1, aID)

        #-- check UI
        if pm.popupMenu('workmanPopup', ex=True):
            pm.deleteUI('workmanPopup')

        #-- directory
        pm.popupMenu('workmanPopup', b=1, p=self.ibWmf)
        pm.menuItem(l='Open Workman File Directory', 
                    c=pm.Callback(self.openWorkmanPath, 1))
        pm.menuItem(d=True)

        #-- add data
        if fList:
            for fName in fList:
                pm.menuItem(l=fName, 
                            c=pm.Callback(self.replaceWorkmanFileName, fName))
        else:
            pass


    def setWorkmanFileName(self, *args):
        fList = []
        cta, aID, aSt = self.getAssetValues()
        path = self.getWorkmanPath()
        if os.path.isdir(path):
            fList = stc.getFileList(path, 1, aID)
        if fList:
            pm.textField(self.tfWmf, tx=fList[-1], e=True)
        else:
            pm.textField(self.tfWmf, tx='', e=True)


    def replaceWorkmanFileName(self, fName='', *args):
        pm.textField(self.tfWmf, tx=fName, e=True)


    def openWorkmanFile(self, typ=0, *args):
        wmp = self.getWorkmanPath()
        wmf = pm.textField(self.tfWmf, tx=True, q=True)
        fPath = os.path.join(wmp, wmf).replace(os.sep, '/')
        stc.openFile(fPath)


    #---------------------------------------------------------------------------
    #-- Data Check Path --------------------------------------------------------
    def setDataCheckPath(self, *args):
        pm.textField(self.tfDcp, tx=self.DcRig, e=True)#---------------------------------------------------------------------------
        self.getUserList()
        self.setDataCheckMidPath()
        #self.setWorkmanFileName()
        #self.setDataCheckFileNamePopupMenu()


    def resetDataCheckPath(self, *args):
        pm.textField(self.tfDcm, tx='', e=True)
        pm.textField(self.tfDcf, tx='', e=True)
        self.setDataCheckPopupMenu()


    def getDataCheckPath(self, *args):
        dcp = pm.textField(self.tfDcp, tx=True, q=True) 
        usr = pm.optionMenu(self.omDcu, v=True, q=True)
        dcm = pm.textField(self.tfDcm, tx=True, q=True)
        path = os.path.join(dcp, usr, dcm)
        return path


    def setDataCheckMidPath(self, *args):
        if self.aID:
            aAll, aID, aTyp, aStr, aCtg = stc.getAssetInfo(self.aID)
            usr = pm.optionMenu(self.omDcu, v=True, q=True)
            mid = stc.midDataCheckPathExists(self.DcRig, aCtg, aID, usr)
            if mid[0]:
                pm.textField(self.tfDcm, tx=mid[1], e=True) 
            else:
                pm.textField(self.tfDcm, pht=mid[1], e=True) 
        else:
            pm.textField(self.tfDcm, tx='', pht='asset/...', e=True) 
        #-- change user directory
        self.setDataCheckFileName()
        self.setDataCheckFileNamePopupMenu()


    def openDataCheckPath(self, typ=0, *args):
        dcp  = pm.textField(self.tfDcp, tx=True, q=True)
        usr  = pm.optionMenu(self.omDcu, v=True, q=True)
        dcm  = pm.textField(self.tfDcm, tx=True, q=True)
        dcf  = pm.textField(self.tfDcf, tx=True, q=True)
        path = os.path.join(dcp, usr, dcm)
        if typ == 0: #-- open workman project
            os.startfile(dcp)
        elif typ == 1: #-- open workman file path
            os.startfile(path)


    def setDataCheckPopupMenu(self, *args):
        pm.popupMenu(b=1, p=self.ibDcp)
        pm.menuItem(l='Open Data Check Directory', 
                    c=pm.Callback(self.openDataCheckPath, 0))


    def getUserList(self, *args):
        #-- delete all items
        pm.optionMenu(self.omDcu, dai=True, e=True)
        #-- user directory list
        users = os.listdir(self.DcRig)
        for i in users:
            pm.menuItem(l=i, p=self.omDcu)

        #-- get user PC Name
        host = socket.gethostname()
        if host in self.user.keys():
            userDir = self.user[host]
            pm.optionMenu(self.omDcu, v=userDir, e=True)


    def setDataCheckFileNamePopupMenu(self, *args):
        fList = []
        cta, aID, aSt = self.getAssetValues()
        path = self.getDataCheckPath()
        
        if os.path.isdir(path):
            fList = stc.getFileList(path, 1, aID)

        #-- check UI
        if pm.popupMenu('dataCheckPopup', ex=True):
            pm.deleteUI('dataCheckPopup')

        #-- directory
        pm.popupMenu('dataCheckPopup', b=1, p=self.ibDcf)
        pm.menuItem(l='Open Data Check File Directory', 
                    c=pm.Callback(self.openDataCheckPath, 1))
        pm.menuItem(d=True)

        #-- add data
        if fList:
            for fName in fList:
                pm.menuItem(l=fName, 
                            c=pm.Callback(self.replaceDataCheckFileName, fName))
        else:
            pass


    def setDataCheckFileName(self, *args):
        fList = []
        cta, aID, aSt = self.getAssetValues()
        path = self.getDataCheckPath()
        if os.path.isdir(path):
            fList = stc.getFileList(path, 1, aID)
        if fList:
            pm.textField(self.tfDcf, tx=fList[-1], e=True)
        else:
            pm.textField(self.tfDcf, tx='', e=True)


    def replaceDataCheckFileName(self, fName='', *args):
        pm.textField(self.tfDcf, tx=fName, e=True)
        self.checkData()


    #---------------------------------------------------------------------------
    #-- Convert Texture --------------------------------------------------------
    def getP4VMtPath(self, v=0, *args):
        ctg, aID, aSt = self.getAssetValues()
        mid  = stc.getMidPath(ctg, aID, aSt)
        pPath = os.path.join(self.p4Rig, mid).replace(os.sep, '/')
        mPath = fr'{pPath}/_data/_material/{aID}_mt.mb'
        if v == 0:
            return pPath
        elif v == 1:
            return mPath


    def openMaterialDir(self, *args):
        mPath = self.getP4VMtPath(1)
        if os.path.isfile(mPath):
            dirPath = os.path.dirname(mPath)
            os.startfile(dirPath, operation='explore')


    def createMaterialData(self, *args):
        #-- low material
        mt = stc.createLowMTPlanes()
        pm.select(mt, r=True)

        #-- export to material path
        mPath = self.getP4VMtPath(1) 
        mc.file(mPath, f=True, op='v=0;', typ='mayaBinary', pr=True, es=True)

        #-- set text field and log
        self.setMaterialPath()
        print(f'Export Material Data: {mPath}')


    def importMaterialData(self, *args):
        #-- export to material path
        mPath = self.getP4VMtPath(1)
        #-- delete _mtMesh_grp
        if pm.objExists('_mtMesh_grp'):
            pm.delete('_mtMesh_grp')
        #-- import material data
        mc.file(mPath, i=True, typ='mayaBinary', iv=True, ra=True,
                mnc=True, ns=':', op='v=0;', pr=True)


    def resetMaterial(self, *args):
        stc.setDefaultMaterial()


    def assignMaterialFromData(self, *args):
        stc.assignMaterialFromData()


    def convertLowMaterial(self, *args):
        #-- assign preview materials
        stc.assignLowMaterial()

        #-- convert preview texture
        pPath = self.getP4VMtPath(0)
        tPath = rf'{pPath}/texture'
        stc.convertLowTexture(tPath)


    def hypershadeWindow(self, *args):
        pm.mel.eval('HypershadeWindow;')


    def randomAssignMaterial(self, *args):
        stc.randAssignMT()


    #-- Create Hierarchy -------------------------------------------------------
    def createHierarchy(self, *args):
        stc.createBaseHierarchy()


    def importCtrl(self, *args):
        path = rf'{self._dir}/_data/_scenes/_ctrl.mb'
        mc.file(path, i=True, typ='mayaBinary', iv=True, ra=True,
               mnc=True, ns=':', op='v=0;', pr=True)


    #---------------------------------------------------------------------------
    #-- edit UI ----------------------------------------------------------------
    def setCategoryOption(self, *args):
        pm.menuItem(l='--')
        for i in self.ctgr.keys():
            pm.menuItem(l=i)


    def setAssetIDPopupMenu(self, cat='', *args):
        astList = self.getAssetList(cat)
        #-- check UI
        if pm.popupMenu('AssetIDPopup', ex=True):
            pm.deleteUI('AssetIDPopup')

        pm.popupMenu('AssetIDPopup', b=1, p=self.tfAID)
        #-- add data
        for i in astList:
            astID = i.split('_')[0]
            pm.menuItem(l=i, c=pm.Callback(self.refleshAssetInfo, astID))


    def resetAssetIDPopupMenu(self, *args): 
        cat = pm.optionMenu(self.omAst, v=True, q=True)
        self.setAssetIDPopupMenu(cat)
        

    def setProjectPopupMenu(self, *args):
        #-- check UI
        if pm.popupMenu('projectPopup', ex=True):
            pm.deleteUI('projectPopup')

        pm.popupMenu('projectPopup', b=1, p=self.ibLcp)
        pm.menuItem(l='Open Project Directory', c=pm.Callback(self.openProject))
        pm.menuItem(d=True)  
        pm.menuItem(l='Set Project...', c=pm.Callback(self.setCurrentWorkspace))


    def setMaterialPopupMenu(self, *args):
        #-- check UI
        if pm.popupMenu('materialPopup', ex=True):
            pm.deleteUI('materialPopup')

        pm.popupMenu('projectPopup', b=1, p=self.ibMtd)
        pm.menuItem(l='Open Directory', c=pm.Callback(self.openMaterialDir))
        pm.menuItem(l='Reload...', i='{0}/reload.png'.format(self._ico),
                    c=pm.Callback(self.setMaterialPath)) 
        pm.menuItem(d=True)  
        pm.menuItem(l='Hypershade', i='{0}/hypershade.png'.format(self._ico),
                    c=pm.Callback(self.hypershadeWindow)) 


    def getAssetValues(self, *args):
        cta = pm.optionMenu(self.omAst, v=True, q=True)
        aID = pm.textField(self.tfAID, tx=True, q=True)
        aSt = pm.textField(self.tfANA, tx=True, q=True)
        return [cta, aID, aSt]


    def getPathValues(self, *args):
        prj = pm.textField(self.tfLcp, tx=True, q=True)
        atp = pm.textField(self.tfWkp, tx=True, q=True)
        fna = pm.textField(self.tfFln, tx=True, q=True)
        return [prj, atp, fna]


    def setMaterialPath(self, *args):
        mPath = self.getP4VMtPath(1)
        if os.path.isfile(mPath):
            pm.textField(self.tfMtd, tx=mPath, e=True)
        else:
            pm.textField(self.tfMtd, tx='', e=True)          


    #--- main UI ---------------------------------------------------------------
    def main(self):
        self.checkWindowOverlap()
        window = pm.window(self.windowName, mb = True,
                           t = self.windowTitle,
                           w = self.windowSize[0],
                           h = self.windowSize[1])

        #-----------------------------------------------------------------------
        #-- menu ---------------------------------------------------------------
        pm.menu(l='Help', hm=True)
        pm.menuItem(l='Maya 2022 HELP', c=self.show_mayaHelp)
        pm.menuItem(d=True)
        pm.menuItem(l='Tool HELP', c=self.show_toolHelp)


        #-----------------------------------------------------------------------
        #-- layout -------------------------------------------------------------
        self.clL = pm.columnLayout(adj=True)

        #-- Start Environment --------------------------------------------------
        self.fmLSte = pm.formLayout(nd=100)
        self.spSta = pm.separator(st='in', h=2)
        self.ibSte = pm.iconTextButton(l='Set Start Environment')
        self.spSte = pm.separator(st='in', h=2)
        self.omAst = pm.optionMenu(l=' Type :')
        self.setCategoryOption()
        self.ibGid = pm.iconTextButton(l='Get Asset ID')

        self.txAid = pm.text(l=' ID :')
        self.tfAID = pm.textField(pht='xxx0000')
        self.setAssetIDPopupMenu('--')
        self.txAun = pm.text(l='_')
        self.tfANA = pm.textField(pht='devname')

        self.spAti = pm.separator(st='in', h=2)
        self.txAti = pm.text(l='')
        self.ibChe = pm.iconTextButton(l='Create Asset Hierarchy')
        self.spCah = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.fmLSte


        self.tbLFil = pm.tabLayout()
        #-- Local File ---------------------------------------------------------
        self.fmLSvf = pm.formLayout(nd=100)
        self.txLcp = pm.text(l=' Local Directory :')
        self.tfLcp = pm.textField(pht='Project...')
        self.ibLcp = pm.iconTextButton(l='Set Project')
        self.setProjectPopupMenu()
        self.tfWkp = pm.textField(pht='scenes/...')
        self.tfFln = pm.textField(pht='FileName.mb...')
        self.ibFll = pm.iconTextButton(l='...')
        self.setFileNamePopupMenu()

        self.ibDup = pm.iconTextButton(l='Up')
        self.ibDdw = pm.iconTextButton(l='Down')
        self.ibDat = pm.iconTextButton(l='Date')
        #self.ibRld = pm.iconTextButton(l='Reload')

        self.spNwf = pm.separator(st='in', h=2)
        self.ibNwf = pm.iconTextButton(l='New')
        self.ibOpf = pm.iconTextButton(l='Open')
        self.ibSvf = pm.iconTextButton(l='Save')
        self.spSvf = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.fmLSvf


        #-- P4V ----------------------------------------------------------------
        self.fmLP4V = pm.formLayout(nd=100)
        self.txP4V = pm.text(l=' P4V Directory :')
        self.tfP4p = pm.textField(pht='P4V/...')
        self.ibP4p = pm.iconTextButton(l='P4V Path')
        self.setP4VPopupMenu()
        self.tfP4m = pm.textField(pht='asset/...')
        self.tfP4f = pm.textField(pht='FileName.mb...')
        self.ibP4f = pm.iconTextButton(l='...')
        self.setP4VFileNamePopupMenu()
        self.txP4O = pm.text(l=' Outsource :')
        self.tfP4O = pm.textField(pht='FileName.mb...')
        self.ibP4O = pm.iconTextButton(l='...')
        self.setP4VOutsourceFileNamePopupMenu()

        self.spNwO = pm.separator(st='in', h=2)
        self.ibOpO = pm.iconTextButton(l='Open Work File')
        self.ibSvO = pm.iconTextButton(l='Open Outsource File')
        self.spP4V = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.fmLP4V


        #-- Workman ------------------------------------------------------------
        self.fmLWkm = pm.formLayout(nd=100)
        self.txWkm = pm.text(l=' Workman Directory :')

        self.tfWmp = pm.textField(pht='Workman/...')
        self.ibWmp = pm.iconTextButton(l='Workman Path')
        self.setWorkmanPopupMenu()
        self.tfWmm = pm.textField(pht='asset/...')
        self.tfWmf = pm.textField(pht='FileName.mb...')
        self.ibWmf = pm.iconTextButton(l='...')
        self.setWorkmanFileNamePopupMenu()
        self.spWmO = pm.separator(st='in', h=2)
        self.ibWmO = pm.iconTextButton(l='Open Work File')
        self.spWkm = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.fmLWkm


        #-- Data Check ---------------------------------------------------------
        self.fmLDtc = pm.formLayout(nd=100)
        self.txDtc = pm.text(l=' Data Check Directory :')

        self.tfDcp = pm.textField(pht='Data Check Path/...')
        self.ibDcp = pm.iconTextButton(l='Data Check Path')
        self.setDataCheckPopupMenu()
        self.omDcu = pm.optionMenu(l='') #-- User Directoris
        self.tfDcm = pm.textField(pht='asset/...')
        self.tfDcf = pm.textField(pht='FileName.mb...')
        self.ibDcf = pm.iconTextButton(l='...')
        #self.setDataCheckFileNamePopupMenu()

        self.spDcs = pm.separator(st='in', h=2)
        self.ibDco = pm.iconTextButton(l='Open')
        self.ibDcs = pm.iconTextButton(l='Save')
        self.spDtc = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.fmLDtc
        pm.setParent('..') #-- end of self.tbLFil


        #-- Convert Texture ----------------------------------------------------
        self.fmLCvT = pm.formLayout(nd=100)
        self.txCvT = pm.text(l=' Material Data :')
        self.tfMtd = pm.textField(pht='material data...')
        self.ibMtd = pm.iconTextButton(l='...')
        self.setMaterialPopupMenu()
        self.ibExm = pm.iconTextButton(l='Export')
        self.ibImm = pm.iconTextButton(l='Import')
        self.ibRtm = pm.iconTextButton(l='Assign Lambert1 to All Meshes.')
        self.ibAmt = pm.iconTextButton(l='Assign Materials from Data')
        self.ibLot = pm.iconTextButton(l='Convert Low Materials')
        self.ibRam = pm.iconTextButton(l='Random Assign Materials')
        self.spCvT = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.fmLCvT


        #-- Create Hierarchy ---------------------------------------------------
        self.fmLChe = pm.formLayout(nd=100)
        self.ibCbh = pm.iconTextButton(l='Create Base Hierarchy')
        self.ibCct = pm.iconTextButton(l='Import Controllers')
        self.spChe = pm.separator(st='in', h=2)
        pm.setParent('..') #-- end of self.fmLChe


        #-----------------------------------------------------------------------
        #--- Edit UI elements --------------------------------------------------
        io,  to, = ['iconOnly', 'textOnly']
        ith, itv = ['iconAndTextHorizontal', 'iconAndTextVertical']

        #-- Start Environment --------------------------------------------------
        pm.iconTextButton(self.ibSte, st=ith, h=30, mw=7, mh=2,  
            i='{0}/prefs.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.setDefaultUnitEnv), e=True)

        pm.optionMenu(self.omAst, w=120, h=26, e=True,
            cc=pm.Callback(self.resetAssetIDPopupMenu)) 
        pm.iconTextButton(self.ibGid, st=ith, w=100, h=26, mw=7, mh=2,  
            i='{0}/getID.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.setAssetInfo), e=True)

        pm.text(self.txAid, h=24, w=35, al='right', e=True)
        pm.text(self.txAun, h=24, w=10, al='right', e=True)
        pm.textField(self.tfAID, w=73, h=24, e=True)
        pm.textField(self.tfANA, h=24, e=True)

        pm.iconTextButton(self.ibChe, st=ith, w=160, h=30, mw=7, mh=2,  
            i='{0}/folderNew.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.createAssetDir), e=True)

        pm.text(self.txAti, al='left', fn='fixedWidthFont', e=True)

        #-- Save File ----------------------------------------------------------
        pm.text(self.txLcp, al='left', e=True)
        pm.textField(self.tfLcp, h=24, e=True)

        pm.iconTextButton(self.ibLcp, st=io, w=24, h=22, mw=0, mh=0,  
            i='{0}/open.png'.format(self._ico), bgc=self.btnBgc, e=True)

        pm.textField(self.tfWkp, h=24, e=True)
        pm.textField(self.tfFln, bgc=self.frmBgc,
            tcc=pm.Callback(self.checkData), h=24, e=True) 

        pm.iconTextButton(self.ibFll, st=to, w=24, h=22, mw=0, mh=0,
            bgc=self.btnBgc, e=True)


        pm.iconTextButton(self.ibDup, st=io, w=24, h=22, mw=7, mh=2,  
            i='{0}/up.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.updateFileName, 1), e=True)

        pm.iconTextButton(self.ibDdw, st=io, w=24, h=22, mw=7, mh=2,  
            i='{0}/down.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.updateFileName, -1), e=True)

        pm.iconTextButton(self.ibDat, st=io, w=24, h=22, mw=7, mh=2,  
            i='{0}/time.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.updateDate), e=True)

        #pm.iconTextButton(self.ibRld, st=io, w=24, h=22, mw=7, mh=2,  
        #    i='{0}/reload.png'.format(self._ico), bgc=self.btnBgc, 
        #    c=pm.Callback(self.checkData), e=True)


        pm.iconTextButton(self.ibNwf, st=ith, w=85, h=26, mw=7, mh=2,  
            i='{0}/fileNew.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.newFile), e=True)

        pm.iconTextButton(self.ibOpf, st=ith, w=100, h=26, mw=7, mh=2,  
            i='{0}/openFile.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.openFile), e=True)

        pm.iconTextButton(self.ibSvf, st=ith, w=100, h=26, mw=7, mh=2,  
            i='{0}/save.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.saveFile), e=True)

        #-- P4V ----------------------------------------------------------------
        pm.text(self.txP4V, al='left', e=True)

        pm.textField(self.tfP4p, h=24, e=True)

        pm.iconTextButton(self.ibP4p, st=io, w=24, h=22, mw=0, mh=0,  
            i='{0}/open.png'.format(self._ico), bgc=self.btnBgc, e=True)

        pm.textField(self.tfP4m, h=24, e=True)
        pm.textField(self.tfP4f, h=24, e=True)

        pm.iconTextButton(self.ibP4f, st=to, w=24, h=22, mw=0, mh=0,
            bgc=self.btnBgc, e=True)

        pm.text(self.txP4O, al='left', e=True)
        pm.textField(self.tfP4O, h=24, e=True)
        pm.iconTextButton(self.ibP4O, st=to, w=24, h=22, mw=0, mh=0,
            bgc=self.btnBgc, e=True)

        pm.iconTextButton(self.ibOpO, st=ith, w=100, h=26, mw=7, mh=2,  
            i='{0}/openFile.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.openP4VFile, 0), e=True)

        pm.iconTextButton(self.ibSvO, st=ith, w=100, h=26, mw=7, mh=2,  
            i='{0}/openFile.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.openP4VFile, 1), e=True)


        #-- Workman ------------------------------------------------------------
        pm.text(self.txWkm, al='left', e=True)

        pm.textField(self.tfWmp, h=24, e=True)

        pm.iconTextButton(self.ibWmp, st=io, w=24, h=22, mw=0, mh=0,  
            i='{0}/open.png'.format(self._ico), bgc=self.btnBgc, e=True)

        pm.textField(self.tfWmm, h=24, e=True)
        pm.textField(self.tfWmf, h=24, e=True)

        pm.iconTextButton(self.ibWmf, st=to, w=24, h=22, mw=0, mh=0,
            bgc=self.btnBgc, e=True)

        pm.iconTextButton(self.ibWmO, st=ith, w=100, h=26, mw=7, mh=2,  
            i='{0}/openFile.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.openWorkmanFile, 0), e=True)


        #-- Data Check Path ----------------------------------------------------
        pm.text(self.txDtc, al='left', e=True)

        pm.textField(self.tfDcp, h=24, e=True)

        pm.iconTextButton(self.ibDcp, st=io, w=24, h=22, mw=0, mh=0,  
            i='{0}/open.png'.format(self._ico), bgc=self.btnBgc, e=True)

        pm.optionMenu(self.omDcu, w=120, h=24, e=True,
            cc=pm.Callback(self.setDataCheckMidPath)) 

        pm.textField(self.tfDcm, h=24, e=True)
        pm.textField(self.tfDcf, h=24, e=True)

        pm.iconTextButton(self.ibDcf, st=to, w=24, h=22, mw=0, mh=0,
            bgc=self.btnBgc, e=True)

        pm.iconTextButton(self.ibDco, st=ith, w=100, h=26, mw=7, mh=2,  
            i='{0}/openFile.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.openFile), e=True)

        pm.iconTextButton(self.ibDcs, st=ith, w=100, h=26, mw=7, mh=2,  
            i='{0}/save.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.saveFile), e=True)


        #-- Convert Texture ----------------------------------------------------
        pm.text(self.txCvT, al='left', e=True)

        pm.textField(self.tfMtd, h=24, e=True)
        pm.iconTextButton(self.ibMtd, st=to, w=24, h=22, mw=0, mh=0,  
            bgc=self.btnBgc, e=True)

        pm.iconTextButton(self.ibExm, st=ith, h=30, mw=7, mh=2,  
            i='{0}/out.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.createMaterialData), e=True)

        pm.iconTextButton(self.ibImm, st=ith, h=30, mw=7, mh=2,  
            i='{0}/in.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.importMaterialData), e=True)

        pm.iconTextButton(self.ibRtm, st=ith, h=30, mw=7, mh=2,  
            i='{0}/lambert.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.resetMaterial), e=True)

        pm.iconTextButton(self.ibAmt, st=ith, h=30, mw=7, mh=2,  
            i='{0}/Textured.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.assignMaterialFromData), e=True)

        pm.iconTextButton(self.ibLot, st=ith, h=30, mw=7, mh=2,  
            i='{0}/lowMaterial.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.convertLowMaterial), e=True)

        pm.iconTextButton(self.ibRam, st=ith, h=30, mw=7, mh=2,  
            i='{0}/random.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.randomAssignMaterial), e=True)

        #-- Create Hierarchy ---------------------------------------------------
        pm.iconTextButton(self.ibCbh, st=ith, h=30, mw=7, mh=2,  
            i='{0}/hierarchy.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.createHierarchy), e=True)

        pm.iconTextButton(self.ibCct, st=ith, h=30, mw=7, mh=2,  
            i='{0}/ctrl.png'.format(self._ico), bgc=self.btnBgc, 
            c=pm.Callback(self.importCtrl), e=True)



        #-----------------------------------------------------------------------
        #--- Edit UI Layout ----------------------------------------------------
        t, b, l, r = ['top', 'bottom', 'left', 'right']


        pm.formLayout(self.fmLSte, e=True, af=[
        (self.spSta, t,   0), (self.spSta, l,   0), (self.spSta, r,   0), 
        (self.ibSte, t,  15), (self.ibSte, l,  10), (self.ibSte, r,  10), 
        (self.spSte, t,  60), (self.spSte, l,   0), (self.spSte, r,   0), 
        (self.omAst, t,  76), (self.omAst, l,  10), 
        (self.ibGid, t,  75), (self.ibGid, l, 140), (self.ibGid, r,  10), 
        (self.txAid, t, 110), (self.txAid, l,   9), 
        (self.tfAID, t, 110), (self.tfAID, l,  49), 
        (self.txAun, t, 110), (self.txAun, l, 123), 
        (self.tfANA, t, 110), (self.tfANA, l, 139), (self.tfANA, r,   9), 

        (self.spAti, t, 145), (self.spAti, l,   0), (self.spAti, r,   0), 
        (self.txAti, t, 155), (self.txAti, l,  40), (self.txAti, r,  10),
        (self.ibChe, t, 240), (self.ibChe, l,  10), (self.ibChe, r,  10),
        (self.spCah, t, 280), (self.spCah, l,   0), (self.spCah, r,   0), 
        ])


        #-- Save File ----------------------------------------------------------
        pm.formLayout(self.fmLSvf, e=True, w=380, af=[
        (self.txLcp, t,  10), (self.txLcp, l,  10), (self.txLcp, r,  10), 
        (self.tfLcp, t,  30), (self.tfLcp, l,   9), (self.tfLcp, r,  40), 
        (self.ibLcp, t,  31),                       (self.ibLcp, r,  10), 
        (self.tfWkp, t,  60), (self.tfWkp, l,   9), (self.tfWkp, r,   9), 
        (self.tfFln, t,  90), (self.tfFln, l,   9), (self.tfFln, r,  40), 
        (self.ibFll, t,  91),                       (self.ibFll, r,  10), 

        (self.ibDup, t, 120),                       (self.ibDup, r,  70), 
        (self.ibDdw, t, 120),                       (self.ibDdw, r,  40), 
        (self.ibDat, t, 120),                       (self.ibDat, r,  10),                      
        #(self.ibRld, t, 120),                       (self.ibRld, r,  10), 
        (self.spNwf, t, 195), (self.spNwf, l,   0), (self.spNwf, r,   0),
        (self.ibNwf, t, 210), (self.ibNwf, l,  10), 
        (self.ibOpf, t, 210), (self.ibOpf, l, 100), 
        (self.ibSvf, t, 210),                       (self.ibSvf, r,  10),
        (self.spSvf, t, 250), (self.spSvf, l,   0), (self.spSvf, r,   0),
        ],
        ap=[
        (self.ibOpf, r,  5, 60), 
        (self.ibSvf, l,  0, 60),
        ])


        #-- P4V Path -----------------------------------------------------------
        pm.formLayout(self.fmLP4V, e=True, af=[
        (self.txP4V, t,  10), (self.txP4V, l,  10), (self.txP4V, r,  10), 
        (self.tfP4p, t,  30), (self.tfP4p, l,   9), (self.tfP4p, r,  40), 
        (self.ibP4p, t,  31),                       (self.ibP4p, r,  10), 
        (self.tfP4m, t,  60), (self.tfP4m, l,   9), (self.tfP4m, r,   9), 
        (self.tfP4f, t,  90), (self.tfP4f, l,   9), (self.tfP4f, r,  40), 
        (self.ibP4f, t,  91),                       (self.ibP4f, r,  10), 
        (self.txP4O, t, 130), (self.txP4O, l,  10), (self.txP4O, r,  10), 
        (self.tfP4O, t, 150), (self.tfP4O, l,   9), (self.tfP4O, r,  40), 
        (self.ibP4O, t, 151),                       (self.ibP4O, r,  10), 

        (self.spNwO, t, 195), (self.spNwO, l,   0), (self.spNwO, r,   0),
        (self.ibOpO, t, 210), (self.ibOpO, l,  10), 
        (self.ibSvO, t, 210),                       (self.ibSvO, r,  10),

        (self.spP4V, t, 250), (self.spP4V, l,   0), (self.spP4V, r,   0),
        ],
        ap=[
        (self.ibOpO, r,  5, 50), 
        (self.ibSvO, l,  0, 50),
        ])


        #-- Workman Path -------------------------------------------------------
        pm.formLayout(self.fmLWkm, e=True, af=[
        (self.txWkm, t,  10), (self.txWkm, l,  10), (self.txWkm, r,  10), 
        (self.tfWmp, t,  30), (self.tfWmp, l,   9), (self.tfWmp, r,  40), 
        (self.ibWmp, t,  31),                       (self.ibWmp, r,  10), 
        (self.tfWmm, t,  60), (self.tfWmm, l,   9), (self.tfWmm, r,   9), 
        (self.tfWmf, t,  90), (self.tfWmf, l,   9), (self.tfWmf, r,  40), 
        (self.ibWmf, t,  91),                       (self.ibWmf, r,  10), 

        (self.spWmO, t, 195), (self.spWmO, l,   0), (self.spWmO, r,   0),
        (self.ibWmO, t, 210), (self.ibWmO, l,  10), (self.ibWmO, r,  10), 
        (self.spWkm, t, 250), (self.spWkm, l,   0), (self.spWkm, r,   0),
        ])


        #-- Data Check Path ----------------------------------------------------
        pm.formLayout(self.fmLDtc, e=True, af=[
        (self.txDtc, t,  10), (self.txDtc, l,  10), (self.txDtc, r,  10), 
        (self.tfDcp, t,  30), (self.tfDcp, l,   9), (self.tfDcp, r,  40), 
        (self.ibDcp, t,  31),                       (self.ibDcp, r,  10),
        (self.omDcu, t,  60), (self.omDcu, l,   9),  
        (self.tfDcm, t,  60), (self.tfDcm, l, 140), (self.tfDcm, r,   9), 
        (self.tfDcf, t,  90), (self.tfDcf, l,   9), (self.tfDcf, r,  40), 
        (self.ibDcf, t,  91),                       (self.ibDcf, r,  10), 

        (self.spDcs, t, 195), (self.spDcs, l,   0), (self.spDcs, r,   0),
        (self.ibDco, t, 210), (self.ibDco, l,  10), 
        (self.ibDcs, t, 210),                       (self.ibDcs, r,  10),
        (self.spDtc, t, 250), (self.spDtc, l,   0), (self.spDtc, r,   0),
        ],
        ap=[
        (self.ibDco, r,  5, 50), 
        (self.ibDcs, l,  0, 50),
        ])



        pm.tabLayout(self.tbLFil, imw=5, imh=5, e=True, 
            tl=((self.fmLSvf, ' Local Path '), (self.fmLP4V, '  P4V Path  '), 
            (self.fmLWkm, ' Workman '), (self.fmLDtc, ' Data Check ')) )


        #-- Convert Texture ----------------------------------------------------
        pm.formLayout(self.fmLCvT, e=True, af=[
        (self.txCvT, t,  10), (self.txCvT, l,  10), (self.txCvT, r,  10), 
        (self.tfMtd, t,  30), (self.tfMtd, l,   9), (self.tfMtd, r,  40), 
        (self.ibMtd, t,  31),                       (self.ibMtd, r,  10), 
        (self.ibExm, t,  60), (self.ibExm, l,  10),  
        (self.ibImm, t,  60),                       (self.ibImm, r,  10), 
        (self.ibRtm, t,  95), (self.ibRtm, l,  10), (self.ibRtm, r,  10), 
        (self.ibAmt, t, 130), (self.ibAmt, l,  10), (self.ibAmt, r,  10), 
        (self.ibLot, t, 165), (self.ibLot, l,  10), (self.ibLot, r,  10), 
        (self.ibRam, t, 200), (self.ibRam, l,  10), (self.ibRam, r,  10), 
        (self.spCvT, t, 300), (self.spCvT, l,   0), (self.spCvT, r,   0), 
        ],
        ap=[
        (self.ibExm, r,  5, 50),
        (self.ibImm, l,  0, 50), 
        ])


        #-- Create Hierarchy ---------------------------------------------------
        pm.formLayout(self.fmLChe, e=True, af=[
        (self.ibCbh, t,  10), (self.ibCbh, l,  10), (self.ibCbh, r,  10), 
        (self.ibCct, t,  45), (self.ibCct, l,  10), (self.ibCct, r,  10), 
        (self.spChe, t, 100), (self.spChe, l,   0), (self.spChe, r,   0), 
        ])



        #-- Show UI Command ----------------------------------------------------
        window.show()

        #-- init command -------------------------------------------------------
        pm.window(self.windowName, e=True,
                  w = self.windowSize[0], 
                  h = self.windowSize[1])
        self.getCurrentWorkspace()

        self.setInitAssetInfo(self._aID) #-- get info from root node
        self.setAssetInfo() #-- get info from root node
        self.setP4VPath()
        self.setWorkmanPath()
        self.setDataCheckPath()

        self.setMaterialPath()
        self.checkData()


def showUI():
    testIns = startupUI()
    testIns.main()
