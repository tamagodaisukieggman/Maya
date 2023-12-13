# -*- coding: utf-8 -*-

import os
import re

from apiutils import uiutils
from cypyapiutils import pyside as psutils

import pymel.core as pm
from maya import cmds

PRESET_WINDOW_NAME = 'Post-process Set Editor - Preset'
INPUT_NAME_WINDOW = 'Post-process Set Editor - Input set name'
SETNAME_ATTR = 'postproc_edit_set__name'

def is_unique(base_set_name, silent=False):
    for set_ in cmds.ls(type='objectSet'):
        if not cmds.attributeQuery(SETNAME_ATTR, ex=True, n=set_):
            continue
        _setname = cmds.getAttr(set_+'.'+SETNAME_ATTR)
        if _setname == base_set_name:
            if not silent:
                d = psutils.PromptDialog2('Error', btns=['OK'])
                d.show(m='The given name is already used.', modal=True)
            return False
    return True

def icon_button(label, image, callback, style='iconAndTextHorizontal'):
    iconpath = os.path.join(os.path.dirname(__file__), 'icons', image).replace('\\', '/')
    return pm.iconTextButton(h=30, l=label+' ', style=style, image1=iconpath, bgc=(0.4, 0.4, 0.4), c=callback)

class InputSetName(uiutils.OptionWindow):
    def content(self, **args):
        self.mc = args['column']
        pm.setParent(self.mc)

        pm.columnLayout()
        self.tfg = pm.textFieldGrp(l='Set Name:')

    def is_desc_enabled(self):
        return False

    def is_editmenu_enabled(self):
        return False

    def execute(self):
        name_ = pm.textFieldGrp(self.tfg, q=True, text=True)
        self._prostproc_set_editor_mwin._add_item(name_)


class Set():
    def __init__(self, pm_nodes=[], set_name=None, new=False):
        tgsetname = self.get_unique('plset%02d_target')

        if new:
            newname = self.get_unique('plset%02d_' + set_name )
            self.pm_link_set = pm.sets([x.name() for x in pm_nodes], name=tgsetname)
            self.pm_set = pm.sets([self.pm_link_set.name()], name=newname)
            self.addattr(set_name)
        else:
            self.pm_set = pm.PyNode(set_name)
            ms = cmds.sets(self.pm_set.name(), q=True)
            if ms is None:
                ms = []
            try:
                tg_setname = [x for x in ms if cmds.objectType(x)=='objectSet' and re.search(r'^plset\d{2}_target', x)][0]
                
                self.pm_link_set = pm.PyNode(tg_setname)
            except:
                self.pm_link_set = pm.sets([x.name() for x in pm_nodes], name=tgsetname)
                pm.sets(self.pm_set, add=self.pm_link_set)

        if not pm.attributeQuery('postproc_edit_set', ex=True, n=self.pm_set):
            pm.addAttr(self.pm_set, ln='postproc_edit_set', at='bool')
            pm.setAttr(self.pm_set+'.postproc_edit_set', True)

        self.pm_nodes = pm_nodes
        

    def get_unique(self, ptn):
        i = 1
        while True:
            res = ptn % i
            if not cmds.objExists(res):
                break
            i += 1
        return res

    def get_op_setname(self, opname):
        try:
            ms = cmds.sets(self.pm_set.name(), q=True)
        except:
            ms = []

        if ms is None:
            ms = []

        buf = [x for x in ms \
                    if cmds.objectType(x)=='objectSet' and \
                        re.search(r'^plset\d{2}_', x) and \
                        not re.search(r'^plset\d{2}_target', x)]

        for set_ in buf:
            m = re.search(r'^plset\d{2}_(.*)', set_)
            _opname = m.group(1)
            if _opname.lower() == opname.lower():
                return set_

        return None

    def get_targets(self, set_):
        buf = cmds.sets(set_, q=True)
        if buf is None:
            buf = []
        
        return buf

    def get_operators(self):
        buf = cmds.sets(self.pm_set.name(), q=True)
        buf = [x for x in buf if cmds.attributeQuery('postproc_edit_set__operator_name', ex=True, n=x)]

        buf = [x for x in cmds.ls(type='objectSet') if x in buf]

        return buf

    def get_setname(self):
        if not cmds.objExists(self.pm_set.name()):
            return
        attrname = SETNAME_ATTR
        if not cmds.attributeQuery(attrname, ex=True, n=self.pm_set.name()):
            self.addattr(self.pm_set.name())
        
        return cmds.getAttr(self.pm_set+'.'+attrname)

        
    def addattr(self, setname):
        attrname = SETNAME_ATTR
        if not cmds.attributeQuery(attrname, ex=True, n=self.pm_set.name()):
            cmds.addAttr(self.pm_set.name(), ln=attrname, dt='string')
            
        cmds.setAttr(self.pm_set+'.'+attrname, setname, type='string')


def is_root_set(set_):
    def is_object_set(x):
        try:
            return True if cmds.objectType(x) == 'objectSet' else False
        except:
            return False
            

    for _set in cmds.ls(type='objectSet'):
        ms = cmds.sets(_set, q=True)
        if ms is None:
            ms = []

        for m in [x for x in ms if is_object_set(x)]:
            if m==set_:
                return False
        
    return True

def clear_set(set_):
    if not cmds.objExists(set_):
        return
    ms = cmds.sets(set_, q=True)
    if ms is None:
        ms = []
    for s in [x for x in ms if cmds.objectType(x)=='objectSet']:
        clear_set(s)
    if cmds.objExists(set_):
        cmds.delete(set_)


def textScrollList(**args):
    tsl = pm.textScrollList(**args)
    pm.textScrollList(tsl, e=True, dcc=pm.Callback(select_all, tsl))
    return tsl

def select_all(tsl):
    pm.textScrollList(tsl, e=True, si=pm.textScrollList(tsl, q=True, ai=True))

