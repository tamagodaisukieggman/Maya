# -*- coding: utf-8 -*-

from utiltools.custom_locator_manager import command as clm_cmd

import os
import re

import apiutils
from apiutils import uiutils
import cypyapiutils
from cypyapiutils import pyside as psutils

import pymel.core as pm
from maya import cmds

from Qt import QtWidgets

def textScrollList(**args):
    tsl = pm.textScrollList(**args)
    pm.textScrollList(tsl, e=True, dcc=pm.Callback(select_all, tsl))
    return tsl

def select_all(tsl):
    pm.textScrollList(tsl, e=True, si=pm.textScrollList(tsl, q=True, ai=True))

def normalize_path(p):
    return p.lower().replace('\\', '/')

class CustomLocatorManager(uiutils.OptionWindow):
    def filepath(self):
        return __file__

    def content(self, **args):
        if not cmds.pluginInfo('curveLocator', q=True, l=True):
            try:
                cmds.loadPlugin('curveLocator')
            except:
                psutils.PromptDialog2('Error', btns=['OK']).show(m='Cannot load curveLocator plugin.')
                return

        varfile = os.path.join(os.path.dirname(__file__), 'variables.yaml')
        self.var = cypyapiutils.Variable(self.id, toolgroup='Maya', defaultfile=varfile)

        self.mc = args['column']
        pm.setParent(self.mc)

        fl = pm.formLayout()

        tx = pm.text(l='Custom locators:', al='left', font='boldLabelFont')
        uiutils.maya_to_qt(tx).setStyleSheet('QWidget {font-size:14px; font-weight:bold}')
        self.tsl = tsl = pm.textScrollList(ams=True)
        rl = pm.rowLayout(nc=3, co3=(5, 5, 5), ct3=('right', 'right', 'right'))
        self.btn_save = pm.button(l='Save', w=100, h=30, c=pm.Callback(self.save_clicked))
        self.btn_delete = pm.button(l='Delete', w=100, h=30, c=pm.Callback(self.delete_clicked))

        pm.formLayout(fl, e=True, af=[
                    (tx, 'top', 10),
                    (rl, 'bottom', 10),
                    (tsl, 'left', 0),
                    (tsl, 'right', 0),
                ],ac=[
                    (tsl, 'top', 10, tx), 
                    (tsl, 'bottom', 10, rl), 
                ]
                )

        pm.menuItem(divider=True, parent=self.edit_menu)
        pm.menuItem(l='Change library path...', c=pm.Callback(self.change_library_path), parent=self.edit_menu)
        self.recent_libpaths = pm.menuItem(l='Recent library paths', pmc=pm.Callback(self.refresh_recent_libpaths), parent=self.edit_menu, subMenu=True)
        self.recent_libpaths.children = []

        self.reload()


    def get_library_path(self, f=False):
        if 'LibraryPath' in self.var.var:
            res = self.var.get('LibraryPath')
            if not os.path.exists(res):
                return None
            return res
        elif 'CURVE_LOCATOR_LIBRARY_PATH' in os.environ:
            return os.environ['CURVE_LOCATOR_LIBRARY_PATH']
        else:
            if not f:
                psutils.PromptDialog2('Error', btns=['OK']).show(m=u'ライブラリのパスが定義されていません。')
            return None

    

    def reload(self):
        libpath = self.get_library_path()
        if libpath is None:
            return
        
        files = os.listdir(libpath)
        files = [x for x in files if x.endswith('.mb')]

        pm.textScrollList(self.tsl, e=True, ra=True)
        for f in files:
            item = re.sub('[.][^.]+$', '', f)
            pm.textScrollList(self.tsl, e=True, a=item)

        enabled = True
        if 'CURVE_LOCATOR_LIBRARY_PATH' in os.environ:
            if normalize_path(libpath) == normalize_path(os.environ['CURVE_LOCATOR_LIBRARY_PATH']):
                enabled = False
        pm.button(self.btn_save, e=True, en=enabled)
        pm.button(self.btn_delete, e=True, en=enabled)

    def refresh_recent_libpaths(self):
        if 'RecentLibraryPath' not in self.var.var:
            return
        paths = self.var.var['RecentLibraryPath']

        for c in self.recent_libpaths.children:
            cmds.deleteUI(c)
        self.recent_libpaths.children = []

        for p in paths:
            item = pm.menuItem(l=p, parent=self.recent_libpaths, c=pm.Callback(self._change_library_path, p))
            self.recent_libpaths.children.append(item)


    def add_recent_libpath(self, libpath):
        if 'CURVE_LOCATOR_LIBRARY_PATH' in os.environ:
            if normalize_path(libpath) == normalize_path(os.environ['CURVE_LOCATOR_LIBRARY_PATH']):
                return

        if 'RecentLibraryPath' not in self.var.var:
            self.var.var['RecentLibraryPath'] = []
        
        recents = self.var.var['RecentLibraryPath']
        if libpath in recents:
            recents.remove(libpath)
        
        recents.insert(0, libpath)

    def change_library_path(self):
        libpath = self.get_library_path(f=True)
        if libpath is None:
            libpath = ''
        libpath = QtWidgets.QFileDialog.getExistingDirectory(None, 'Change library path', libpath)
        self._change_library_path(libpath)

    def _change_library_path(self, libpath):
        if not os.path.exists(libpath):
            return
        self.var.replace('LibraryPath', libpath)

        self.add_recent_libpath(libpath)
        
        self.var.save()
        self.reload()


    def save_clicked(self):
        libpath = self.get_library_path()
        print('libpatah:', libpath)
        if libpath is None:
            return
        sel = cmds.ls(sl=True, type='curveLocator')
        dsc = cmds.listRelatives(ad=True, type='curveLocator', pa=True)
        if type(dsc) is list:
            sel += dsc

        if len(sel) == 0:
            psutils.PromptDialog2('Confirmation', btns=['OK']).show('No curveLocators selected.')
            return
        
        wd = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout(wd)
        lb = QtWidgets.QLabel('Name:')
        le = QtWidgets.QLineEdit()

        buf = pm.textScrollList(self.tsl, q=True, si=True)

        if len(buf) > 0:
            le.setText(buf[0])

        hbox.addWidget(lb)
        hbox.addWidget(le)
        d = psutils.PromptDialog2('Save locator')
        res = d.show(m=u'Input locator name:', aw=wd, modal=True)
        if res != 1:
            return

        

        import re
        res = re.sub('\W', '_', le.text()).strip()
        if res == '':
            return

        filepath = os.path.join(libpath, res+'.mb')

        if os.path.exists(filepath):
            res = psutils.PromptDialog2('Confirmation').show('Overwirte?', modal=True)
            if res != 1:
                return



        cmds.file(filepath, es=True, type='mayaBinary', f=True)

        self.reload()

    def delete_clicked(self):
        libpath = self.get_library_path()
        if libpath is None:
            return
        
        sel = pm.textScrollList(self.tsl, q=True, si=True)
        if len(sel) == 0:
            return
        
        res = psutils.PromptDialog2('Confirmation').show('Delete selected locators?', modal=True)
        if res != 1:
            return

        for item in sel:
            filepath = os.path.join(libpath, item+'.mb')
            os.remove(filepath)

        self.reload()


    def reset_optvar(self):
        d = psutils.PromptDialog2('Confirmation', btns=['Reset', 'Cancel'])
        res = d.show(m='Reset presets to default?', modal=True)
        if res == 1:
            import copy
            bk = copy.deepcopy(self.var.var)
            pm.textScrollList(self.tsl, e=True, ra=True)
            self.var.load_default()
            try:
                self.var.var['RecentLibraryPath'] = bk['RecentLibraryPath']
            except:
                pass
            self.var.save()
            self.reload()

    


    def execute(self):
        libpath = self.get_library_path()
        if not libpath:
            return

        
        
        sel = pm.textScrollList(self.tsl, q=True, si=True)
        for item in sel:
            filepath = os.path.join(libpath, item+'.mb')
            #cmds.file(filepath, i=True, f=True)
            clm_cmd.create_locator(filepath)
            

    def apply_button_label(self):
        return 'Create'

        
    def is_desc_enabled(self):
        return False


def show():
    w = CustomLocatorManager('Custom Locator Manager', w=500, h=450)
    w.show()