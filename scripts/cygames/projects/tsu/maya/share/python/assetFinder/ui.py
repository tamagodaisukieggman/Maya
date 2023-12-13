# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Common
# Name    : Asset Finder
# Author  : rkanda
# Version : 0.0.2
# Updata  : 2019/12/02 12:38:26
# ----------------------------------
# ---- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import subprocess
import datetime
import shutil

 
class assetFinderUI(object):
    def __init__(self):
        self.__ver__          = '0.0.3'
        self.windowManageName = 'assetFinder'
        self.windowTitle      = 'Asset Finder v{0}'.format(self.__ver__)
        self.windowSize       = [300, 200]
        self._mayaHelp_url    = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._toolHelp_url    = r'https://wisdom.cygames.jp/display/tsubasa/%5BMaya%5D+Asset+Finder'
        self._default_path    = r'D:/cygames/tsubasa/work/chara'


    def checkWindowOverlap(self):
        if pm.window(self.windowManageName, ex=True):
            pm.deleteUI(self.windowManageName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)


    # -- functions -------------------------------------------------------
    def getDialog(self):
        jsonFilter = 'chara Directory'
        stPath     = self.txf0.getText()
        if not stPath:
            stPath = self._default_path
        filePath   = pm.fileDialog2(ff  = jsonFilter, 
                                    ds  = 2, 
                                    spe = False, 
                                    dir = stPath, 
                                    fm  = 3)[0]
        self.txf0.setText(filePath)
        pm.textScrollList(self.tsl0, 
                         ra = True, 
                          e = True)
        pm.textScrollList(self.tsl0, 
                          a = self.getStartDir(),
                          e = True)        

    def getStartDir(self):
        stPath  = self.txf0.getText()
        dirList = []
        if os.path.exists(stPath):
            dirList = [i for i in os.listdir(stPath)]
        return dirList

    def getDirList(self):
        stPath  = self.txf0.getText()
        try:
            dirType = self.tsl0.getSelectItem()[0]
        except:
            dirType = None

        # -- edit list
        pm.textScrollList(self.tsl1, ra=True, e=True)
        pm.textScrollList(self.tsl2, ra=True, e=True)
        pm.textScrollList(self.tsl3, ra=True, e=True)
        self.resetFileInfo()
        if dirType:
            astList = [i for i in os.listdir(r'{0}/{1}'.format(stPath, dirType))]
            pm.textScrollList(self.tsl1, a=astList, e=True)

    def getAssetType(self):
        stPath  = self.txf0.getText()
        dirType = self.tsl0.getSelectItem()[0]
        try:
            astName = self.tsl1.getSelectItem()[0]
        except:
            astName = None
        # -- edit list
        pm.textScrollList(self.tsl2, ra=True, e=True)
        pm.textScrollList(self.tsl3, ra=True, e=True)
        self.resetFileInfo()
        if astName:
            typList = [i for i in os.listdir(r'{0}/{1}/{2}'.format(stPath, dirType, astName))]
            pm.textScrollList(self.tsl2, a=typList, e=True)

    def getAssetData(self):
        extList = ['mb', 'fbx']
        stPath  = self.txf0.getText()
        dirType = self.tsl0.getSelectItem()[0]
        astName = self.tsl1.getSelectItem()[0]
        try:
            pubType = self.tsl2.getSelectItem()[0]
        except:
            pubType = None
        # -- edit list
        pm.textScrollList(self.tsl3, ra=True, e=True)
        self.resetFileInfo()
        if pubType:
            if pubType == 'model' or pubType == 'rig':
                pubType = '{0}/maya/scenes'.format(pubType)  
            resPath = r'{0}/{1}/{2}/{3}'.format(stPath, dirType, astName, pubType)
            if os.path.exists(resPath):
                dataList = [i for i in os.listdir(resPath) if i.split('.')[-1] in extList]
                pm.textScrollList(self.tsl3, a=dataList, e=True)

    def getDataPath(self):
        stPath  = self.txf0.getText()
        dirType = self.tsl0.getSelectItem()[0]
        astName = self.tsl1.getSelectItem()[0]
        pubType = self.tsl2.getSelectItem()[0]
        try:
            astData = self.tsl3.getSelectItem()[0]
        except:
            astData = None
        # -- edit list
        self.resetFileInfo()
        if astData:
            if pubType == 'model' or pubType == 'rig':
                pubType = '{0}/maya/scenes'.format(pubType)
            resPath = r'{0}/{1}/{2}/{3}/{4}'.format(stPath, dirType, astName, pubType, astData)
            pm.text(self.txt1b, l=resPath, e=True)
            self.getFileSize(resPath)
            self.getFileTime(resPath)
            self.getFileExt(resPath)
            self.getThumb(resPath)
            self.rbc0.setEnable(True)

    def openFolder(self):
        path = self.txt1b.getLabel()
        if path:
            resPath, file = os.path.split(path)
            print("subprocess.call('explorer {0}')".format(resPath.replace('/', '\\')))
            subprocess.call('explorer {0}'.format(resPath.replace('/', '\\')))
    
    def openFile(self):
        path = self.txt1b.getLabel()
        if path:
            root, fileName = os.path.split(path)
            con = mc.confirmDialog(t = 'Confirm Open File', 
                                   m = 'Do you open {0} File?'.format(fileName), 
                                   b = ['Open','Cancel'], 
                                  db = 'Cancel', 
                                  cb = 'Cancel',
                                  ds = 'Cancel')
            if con == 'Open' and '.mb' in fileName:
                mc.file(path, 
                        f = True, 
                       op = 'v=0;',
                       iv = True,
                      typ = 'mayaBinary',
                        o = True)
            elif con == 'Open' and '.fbx' in fileName:
                mc.file(path, 
                        f = True, 
                       op = 'fbx',
                       iv = True,
                      typ = 'FBX',
                        o = True)

    def importFile(self):
        path = self.txt1b.getLabel()
        ns   = self.txf1.getText()
        if path:
            root, fileName = os.path.split(path)
            con = mc.confirmDialog(t = 'Confirm Import File', 
                                   m = 'Do you import {0} File?'.format(fileName), 
                                   b = ['Import','Cancel'], 
                                  db = 'Cancel', 
                                  cb = 'Cancel',
                                  ds = 'Cancel')
            if ns:
                if con == 'Import' and '.mb' in fileName:
                    mc.file(path,
                            i = True, 
                          typ = 'mayaBinary',
                           iv = True,
                           ra = True,
                          mnc = False,
                           ns = ns,
                           op = 'v=0;',
                           pr = True,
                          ifr = False,
                          itr = 'keep') 
                elif con == 'Import' and '.fbx' in fileName:
                    mc.file(path,
                            i = True, 
                          typ = 'FBX',
                           iv = True,
                           ra = True,
                          mnc = False,
                           ns = ns,
                           op = 'fbx',
                           pr = True,
                          ifr = False,
                          itr = 'keep') 
            else:
                if con == 'Import' and '.mb' in fileName:
                    mc.file(path,
                            i = True, 
                          typ = 'mayaBinary',
                           iv = True,
                          mnc = True,
                          rpr = ns,
                           op = 'v=0;',
                           pr = True,
                          ifr = False,
                          itr = 'keep')
                elif con == 'Import' and '.fbx' in fileName:
                    mc.file(path,
                            i = True, 
                          typ = 'FBX',
                           iv = True,
                          mnc = True,
                          rpr = ns,
                           op = 'fbx',
                           pr = True,
                          ifr = False,
                          itr = 'keep')


    def referenceFile(self):
        path = self.txt1b.getLabel()
        ns   = self.txf1.getText()
        if path:
            root, fileName = os.path.split(path)
            con = mc.confirmDialog(t = 'Confirm Reference File', 
                                   m = 'Do you reference {0} File?'.format(fileName), 
                                   b = ['Reference','Cancel'], 
                                  db = 'Cancel', 
                                  cb = 'Cancel',
                                  ds = 'Cancel')
            if con == 'Reference' and '.mb' in fileName:
                mc.file(path,
                        r = True,
                      typ = 'mayaBinary',
                       iv = True, 
                       gl = True,
                      mnc = False, 
                       ns = ns,
                       op = 'v=0;')
            elif con == 'Reference' and '.fbx' in fileName:
                mc.file(path,
                        r = True,
                      typ = 'FBX',
                       iv = True, 
                       gl = True,
                      mnc = False, 
                       ns = ns,
                       op = 'fbx',)


    def getFileSize(self, path=r''):
        if path:
            size = os.path.getsize(path)
            pm.text(self.txt2b, l='', e=True)
            self.txt2b.setLabel('{0:,} KB'.format(int(size*0.001)))


    def getFileTime(self, path=r''):
        if path:
            stat = os.stat(path)
            last_modified = stat.st_mtime
            dt = datetime.datetime.fromtimestamp(last_modified)
            pm.text(self.txt3b, l='', e=True)
            self.txt3b.setLabel(dt.strftime("%Y-%m-%d %H:%M:%S"))


    def getFileExt(self, path=r''):
        if path:
            root, ext = os.path.splitext(path)
            fileType  = pm.system.Path(path).getTypeName()[0]
            pm.text(self.txt4b, l='', e=True)
            self.txt4b.setLabel('{0} ({1})'.format(fileType, ext))


    def openType(self):
        typ = self.rbc0.getSelect()
        if typ == 1:
            print('Opne scene')
            pm.textField(self.txf1, 
                          tx = '',
                         pht = 'namespace', 
                          en = False, 
                           e = True)
            pm.button(self.btn0, 
                      l = 'Open Scene File',
                      c = pm.Callback(self.openFile),
                      e = True)
        elif typ == 2:
            print('import scene')
            astName = self.tsl1.getSelectItem()[0]
            pm.textField(self.txf1, 
                          tx = astName, 
                          en = True, 
                           e = True)
            pm.button(self.btn0, 
                      l = 'Import Scene File',
                      c = pm.Callback(self.importFile),
                      e = True)
        elif typ == 3:
            print('reference scene')
            astName = self.tsl1.getSelectItem()[0]
            pm.textField(self.txf1, 
                          tx = astName,
                          en = True, 
                           e = True)
            pm.button(self.btn0, 
                      l = 'Reference Scene File',
                      c = pm.Callback(self.referenceFile),
                      e = True)


    def getThumb(self, path=r''):
        if path:
            root, fileName = os.path.split(path)
            thumbPngPath   = '{0}/_thumbnail/_{1}_thumb.png'.format(root, os.path.splitext(fileName)[0])
            thumbJpgPath   = '{0}/_thumbnail/_{1}_thumb.jpg'.format(root, os.path.splitext(fileName)[0])
            png = os.path.exists(thumbPngPath)
            jpg = os.path.exists(thumbJpgPath)
            if png:
                pm.nodeIconButton(self.img0, i=thumbPngPath, en=True, e=True)
            elif not png and jpg:
                pm.nodeIconButton(self.img0, i=thumbJpgPath, en=True, e=True)
            else:
                pm.nodeIconButton(self.img0, i='goToBindPose.png', en=True, e=True)


    def saveThumb(self):
        path = self.txt1b.getLabel()
        if path:
            imgFilter      = 'image file (*.jpg *.png *.cin *.iff *.pix *.bmp *.dds *.gif *.eps *.yuv *.rgb *.pic *.tim *.tga *.tif *.rla *.xpm *.hdr)'
            root, fileName = os.path.split(path)
            srcPath        = pm.fileDialog2(ff = imgFilter, 
                                            ds = 2, 
                                            fm = 1,
                                           cap = 'Save {0} Thumbnail Image'.format(fileName),
                                           okc = 'Save')
            if srcPath:
                self.checkThumbDir()
                pm.nodeIconButton(self.img0, i='goToBindPose.png', en=True, e=True)
                imgDir, ext = os.path.splitext(srcPath[0])
                img = os.path.splitext(fileName)[0]
                if ext in ['.jpg', '.jpeg', '.JPG']:
                    tgtPath = '{0}/_thumbnail/_{1}_thumb.jpg'.format(root, img)
                    shutil.copyfile(srcPath[0], tgtPath)
                    pm.nodeIconButton(self.img0, i=tgtPath, en=True, e=True)
                elif ext in ['.png', '.PNG']:
                    tgtPath = '{0}/_thumbnail/_{1}_thumb.png'.format(root, img)
                    shutil.copyfile(srcPath[0], tgtPath)
                    pm.nodeIconButton(self.img0, i=tgtPath, en=True, e=True)
                else:
                    tgtPath = '{0}/_thumbnail/_{1}_thumb.jpg'.format(root, img)
                    self.convertThumb(srcPath[0], tgt=tgtPath, out='jpg')
                    pm.nodeIconButton(self.img0, i=tgtPath, en=True, e=True)


    def removeThumb(self):
        imgName = pm.nodeIconButton(self.img0, i=True, q=True)
        if not imgName == 'goToBindPose.png':
            path = self.txt1b.getLabel()
            if path:
                root, fileName = os.path.split(path)
                con = mc.confirmDialog(t = 'Confirm Delete Thumbnail', 
                                       m = 'Do you delete {0} Thumbnail Image?'.format(fileName), 
                                       b = ['Delete','Cancel'], 
                                      db = 'Cancel', 
                                      cb = 'Cancel',
                                      ds = 'Cancel')
                if con == 'Delete':
                    imgName = pm.nodeIconButton(self.img0, i=True, q=True)
                    os.remove(imgName)
                    pm.nodeIconButton(self.img0, i='goToBindPose.png', en=True, e=True)


    def checkThumbDir(self):
        path = self.txt1b.getLabel()
        root, fileName = os.path.split(path)
        thumbPath = r'{0}/_thumbnail'.format(root)
        if not os.path.exists(thumbPath):
            os.makedirs(thumbPath)
            print('create directory: {0}'.format(thumbPath))


    def captureThumb(self):
        path = self.txt1b.getLabel()
        root, fileName = os.path.split(path)
        imgPath = r'{0}/{1}'.format(root, os.path.splitext(fileName)[0])
        pbPath  = pm.playblast(f = imgPath,
                              st = 0,
                              et = 0,
                             fmt = 'image',
                             sqt = 0,
                              cc = True,
                               v = False,
                             orn = False,
                              fp = 4,
                              fo = True,
                               p = 100,
                               c = 'jpg',
                             qlt = 100,
                              wh = (256, 256))
        if pbPath:
            srcPath = r'{0}.0000.jpg'.format(imgPath)
            tgtPath = '{0}/_thumbnail/_{1}_thumb.jpg'.format(root, os.path.splitext(fileName)[0])
            shutil.copyfile(srcPath, tgtPath)
            pm.nodeIconButton(self.img0, i='goToBindPose.png', en=True, e=True)
            pm.nodeIconButton(self.img0, i=tgtPath, en=True, e=True)
            os.remove(srcPath)


    def convertThumb(self, src=r'', tgt=r'', out='jpg'):
        icv = r'{0}\bin\imgcvt.exe'.format(pm.Env.envVars['MAYA_LOCATION'])
        root, ext = os.path.splitext(src)
        subprocess.call('"{0}" -f {1} -t {2} {3} {4}'.format(icv, ext.replace('.', ''), out, src, tgt))


    # -- edit UI ----------------------------------------
    def reset_UI(self):
        pm.textField(self.txf0,
                     tx = self._default_path,
                      e = True)
        pm.textScrollList(self.tsl0, 
                         ra = True, 
                          e = True)
        pm.textScrollList(self.tsl0, 
                          a = self.getStartDir(),
                          e = True)
        self.getDirList()

    def resetFileInfo(self):
        self.txt1b.setLabel('')
        self.txt2b.setLabel('')
        self.txt3b.setLabel('')
        self.txt4b.setLabel('')
        self.txt5b.setLabel('')
        self.txt6b.setLabel('')
        pm.radioButtonGrp(self.rbc0,
                          sl = 1,
                          en = False,
                           e = True) 
        pm.textField(self.txf1,
                     tx = '',
                    pht = 'namespace',
                     en = False,
                      e = True)
        pm.nodeIconButton(self.img0, i='goToBindPose.png', en=False, e=True)
        pm.button(self.btn0, 
                  l = 'Open Scene File',
                  c = pm.Callback(self.openFile),
                  e = True)


    # -- main UI ----------------------------------------
    def main(self):
        self.checkWindowOverlap()
        window = pm.window(self.windowManageName,
                           t  = self.windowTitle,
                           w  = self.windowSize[0],
                           h  = self.windowSize[1],
                           mb = True)

        # -- menu
        pm.menu(l  = 'Tools', 
                to = False)
        pm.menuItem(l = 'Reset UI',
                    i = 'redrawPaintEffects.png',
                    c = pm.Callback(self.reset_UI))
        pm.menu(l  = 'Help', 
                hm = True)
        pm.menuItem(l = 'Maya 2019 HELP',
                    c = self.show_mayaHelp)
        pm.menuItem(d = True)
        pm.menuItem(l = 'Tool HELP',
                    c = self.show_toolHelp)

        # -- base form layout
        self.fmL0 = pm.formLayout(nd=100)
        with self.fmL0:
            self.sep0 = pm.separator()
            self.txt0 = pm.text(l = ' Path: ',
                               al = 'right',
                                w = 60,
                                h = 24)
            self.txf0 = pm.textField(tx = self._default_path,
                                     h  = 24)
            self.itb0 = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                          i   = 'navButtonBrowse.png', 
                                          bgc = (0.4, 0.4, 0.4),
                                          l   = 'browse', 
                                          c   = pm.Callback(self.getDialog), 
                                          h   = 24,
                                          w   = 75,
                                          mw  = 2
                                          )
            self.tsl0 = pm.textScrollList(ams = False,
                                            a = self.getStartDir(),
                                           sc = pm.Callback(self.getDirList)
                                           )
            self.tsl1 = pm.textScrollList(ams = True, 
                                            a = [],
                                           sc = pm.Callback(self.getAssetType)
                                           )
            self.tsl2 = pm.textScrollList(ams = True,
                                            a = [],
                                           sc = pm.Callback(self.getAssetData)
                                           )
            self.tsl3 = pm.textScrollList(ams = True,
                                            a = [],
                                           sc = pm.Callback(self.getDataPath)
                                           )
            self.txt1a = pm.text(l = ' File Path: ',
                                al = 'right',
                                 w = 60,
                                 h = 24)
            self.txt1b = pm.text(l = '',
                               bgc = (0.25, 0.25, 0.25),
                                al = 'left',
                                 w = 200, 
                                 h = 24)
            # -- popup menu
            self.popm0 = pm.popupMenu(b=0)
            self.pmi0a = pm.menuItem(l = 'Open Directory', 
                                     i = 'navButtonBrowse.png',
                                     c = pm.Callback(self.openFolder))
            # --
            self.txt2a = pm.text(l = ' Size: ',
                                al = 'right',
                                 w = 60,
                                 h = 24)
            self.txt2b = pm.text(l = '',
                               bgc = (0.25, 0.25, 0.25),
                                al = 'left',
                                 h = 24)
            self.txt3a = pm.text(l = ' Update: ',
                                al = 'right',
                                 w = 60,
                                 h = 24)
            self.txt3b = pm.text(l = '',
                               bgc = (0.25, 0.25, 0.25),
                                al = 'left',
                                 h = 24)
            self.txt4a = pm.text(l = ' Ext.: ',
                                al = 'right',
                                 w = 60,
                                 h = 24)
            self.txt4b = pm.text(l = '',
                               bgc = (0.25, 0.25, 0.25),
                                al = 'left',
                                 h = 24)
            self.txt5a = pm.text(l = ' User: ',
                                al = 'right',
                                 w = 60,
                                 h = 24)
            self.txt5b = pm.text(l = '',
                               bgc = (0.25, 0.25, 0.25),
                                al = 'left',
                                 h = 24)
            self.txt6a = pm.text(l = 'Comment: ',
                                al = 'right',
                                 w = 60,
                                 h = 24)
            self.txt6b = pm.text(l = '',
                               bgc = (0.25, 0.25, 0.25),
                                al = 'left',
                                 h = 24)
            self.rbc0 = pm.radioButtonGrp(l = 'File: ', 
                                        la3 = ['Open', 'Import', 'Reference'], 
                                        cw4 = [60, 80, 80, 80],
                                        nrb = 3, 
                                         sl = 1,
                                         en = False,
                                         cc = pm.Callback(self.openType))
            self.txf1 = pm.textField(tx = '',
                                    pht = 'namespace',
                                      w = 140,
                                      h = 24,
                                     en = False)
            self.img0 = pm.nodeIconButton(i = 'goToBindPose.png',
                                          w = 180,
                                          h = 180,
                                         en = False,
                                        bgc = (0.25, 0.25, 0.25),
                                          c = pm.Callback(self.captureThumb))
            # -- popup menu
            self.popm1 = pm.popupMenu(b=0)
            self.pmi1a = pm.menuItem(l = 'Open Directory', 
                                     i = 'navButtonBrowse.png',
                                     c = pm.Callback(self.openFolder))
            pm.menuItem(d=True)
            self.pmi1b = pm.menuItem(l = 'Capture Thumbnail',
                                     i = 'Camera.png',
                                     c = pm.Callback(self.captureThumb))
            self.pmi1c = pm.menuItem(l = 'Select Thumbnail', 
                                     i = 'rvKeepIt.png',
                                     c = pm.Callback(self.saveThumb))
            self.pmi1d = pm.menuItem(l = 'Remove Thumbnail', 
                                     i = 'rvRemoveIt.png',
                                     c = pm.Callback(self.removeThumb))
            self.pmi1e = pm.menuItem(l = 'create thumbnail directory',
                                     c = pm.Callback(self.checkThumbDir))
            # --
            self.btn0 = pm.button(l = 'Open Scene File', 
                                bgc = (0.4, 0.4, 0.4),
                                  c = pm.Callback(self.openFile), 
                                  h = 30,
                                  )            
        # -- Edit UI Layout
        pm.formLayout(self.fmL0, e=True,
               af = [(self.sep0, 'top', 0),  (self.sep0, 'left', 0),  (self.sep0, 'right', 0), 
                     (self.txt0, 'top', 10), (self.txt0, 'left', 10), 
                     (self.txf0, 'top', 10), (self.txf0, 'left', 70), (self.txf0, 'right', 95),
                     (self.itb0, 'top', 10), (self.itb0, 'right', 10),
                     (self.tsl0, 'top', 40), (self.tsl0, 'left', 5),  (self.tsl0, 'bottom', 230),
                     (self.tsl1, 'top', 40),                          (self.tsl1, 'bottom', 230),
                     (self.tsl2, 'top', 40),                          (self.tsl2, 'bottom', 230),
                     (self.tsl3, 'top', 40), (self.tsl3, 'right', 5), (self.tsl3, 'bottom', 230),
                     (self.txt1a, 'left', 5),                             (self.txt1a, 'bottom', 200), 
                     (self.txt1b, 'left', 70),(self.txt1b, 'right', 190), (self.txt1b, 'bottom', 200), 
                     (self.txt2a, 'left', 5),                             (self.txt2a, 'bottom', 175), 
                     (self.txt2b, 'left', 70),(self.txt2b, 'right', 190), (self.txt2b, 'bottom', 175), 
                     (self.txt3a, 'left', 5),                             (self.txt3a, 'bottom', 150), 
                     (self.txt3b, 'left', 70),(self.txt3b, 'right', 190), (self.txt3b, 'bottom', 150), 
                     (self.txt4a, 'left', 5),                             (self.txt4a, 'bottom', 125), 
                     (self.txt4b, 'left', 70),(self.txt4b, 'right', 190), (self.txt4b, 'bottom', 125), 
                     (self.txt5a, 'left', 5),                             (self.txt5a, 'bottom', 100), 
                     (self.txt5b, 'left', 70),(self.txt5b, 'right', 190), (self.txt5b, 'bottom', 100), 
                     (self.txt6a, 'left', 5),                             (self.txt6a, 'bottom',  75), 
                     (self.txt6b, 'left', 70),(self.txt6b, 'right', 190), (self.txt6b, 'bottom',  75),
                     (self.rbc0,  'left', 5), (self.rbc0, 'right', 190), (self.rbc0, 'bottom',  50),
                     (self.txf1,  'left', 330),                          (self.txf1, 'bottom',  46),
                     (self.img0, 'right', 5), (self.img0, 'bottom',  45),
                     (self.btn0, 'left', 5), (self.btn0, 'right', 5), (self.btn0, 'bottom', 5),
                    ],
               ap = [(self.tsl0, 'right', 5, 25), 
                     (self.tsl1, 'left',  0, 25), (self.tsl1, 'right',  5, 50),
                     (self.tsl2, 'left',  0, 50), (self.tsl2, 'right',  5, 75),
                     (self.tsl3, 'left',  0, 75)
                    ])
        window.show()


def showUI():
    testIns = assetFinderUI()
    testIns.main()

