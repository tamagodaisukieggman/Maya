import re
import os

import pymel.core as pm
import pymel.core.uitypes as ui

from Qt import QtWidgets

try:
    import shiboken2
except ImportError:
    from Qt import shiboken2

import maya.OpenMayaUI as omUI

import yaml

print('apiutils.uiutils loaded.')

def maya_to_qt(name, toType=QtWidgets.QWidget):
    ptr = omUI.MQtUtil.findControl(name)
    if not ptr:
        ptr = omUI.MQtUtil.findLayout(name)    
    if not ptr:
        ptr = omUI.MQtUtil.findMenuItem(name)
    if not ptr:
        return None

    return shiboken2.wrapInstance(int(ptr), toType)

class OptionWindow:
    def __init__(self, title, w=None, h=None):
        self.title = title
        self.items = []
        self.id = re.sub('[\\s-]', '_', self.title)
        self.sizeargs = dict()
        self.sizeargs['w'] = 400 if not w else w
        self.sizeargs['h'] = 300 if not h else h

    def show(self):
        if pm.window(self.id, q=True, ex=True):
            pm.deleteUI(self.id, window=True)
        self.win = w = pm.window(self.id, t=self.title, menuBar=True, **self.sizeargs)
        maya_to_qt(w).setStyleSheet('QWidget {font-size:14px} QListWidget {font-size:17px}')
        pm.window(self.win, e=True, cc=pm.Callback(self.__save_optionvar))
        self.edit_menu = edit_menu = pm.menu(l='Edit')

        print('menu:', maya_to_qt(edit_menu))
        maya_to_qt(edit_menu).setStyleSheet('QMenu::item {padding: 4px 25px 4px 20px;}')

        if not self.is_editmenu_enabled():
            pm.menu(edit_menu, e=True, en=False)
        rmi = pm.menuItem(l='Reset Settings', c=pm.Callback(self.__reset_settings))
        if not self.is_reset_optvar_enabled():
            pm.menuItem(rmi, e=True, en=False)
        help_menu = pm.menu(l='Help', helpMenu=True)
        pm.menuItem(l='About ...')
        pm.menu(help_menu, e=True, enable=self.is_help_enabled())

        #
        mform = pm.formLayout()
        tb = pm.frameLayout(lv=False)
        self.content(column=tb)

        pm.setParent(mform)
        if self.is_desc_enabled():
            pm.text('', h=5)
            self.fr_desc = fr = pm.frameLayout(l='Description', mh=10, cll=True, cl=False)
            pm.text(al='left', l=self.__description())
        else:
            self.fr_desc = fr = pm.text('')
        
        pm.setParent(mform)

        c2 = pm.columnLayout(adj=True, co=('both', 2))
        f = pm.formLayout(numberOfDivisions=100)

        b1 = pm.button(l='%s and Close' % self.apply_button_label(), c=pm.Callback(self.__execute))
        b2 = pm.button(l=self.apply_button_label(), c=pm.Callback(self.__apply))
        b3 = pm.button(l='Close', c=pm.Callback(self.close))
        pm.formLayout(f, e=True, 
                            attachForm=[
                                (b1, 'left', 0),
                                (b3, 'right', 0),
                            ],
                            attachPosition=[
                                (b1, 'right', 2, 33), 
                                (b2, 'left', 2, 33),
                                (b2, 'right', 2, 66),
                                (b3, 'left', 2, 66), 
                            ],
                        )

        pm.formLayout(mform, e=True, attachForm=[
                        (tb, 'top', 10), (tb, 'left', 10), (tb, 'right', 10),
                        (fr, 'left', 10), (fr, 'right', 10),
                        (c2, 'bottom', 20), (c2, 'left', 10), (c2, 'right', 10)
                    ],

                attachControl=[
                        (tb, 'bottom', 10, self.fr_desc), 
                        (self.fr_desc, 'bottom', 10, c2)
                    ])

        #pm.setParent('..')
        #pm.text('', h=5);
        if self.is_desc_enabled():
            self.register_item(self.fr_desc, 'DescriptionFrame')

        print('window.id: ', self.id)
        pm.showWindow(self.id)

        self.__load_optionvar()
        self.postfunc()
        if pm.window(self.win, q=True, w=True) < self.sizeargs['w']:
            pm.window(self.win, e=True, w=self.sizeargs['w'])
        if pm.window(self.win, q=True, h=True) < self.sizeargs['h']:
            pm.window(self.win, e=True, h=self.sizeargs['h'])

    def register_item(self, w, name):
        self.items.append({ 'object' : w, 'name' : name})

    def close(self):
        self.__save_optionvar()
        if self.win:
            pm.deleteUI(self.win, window=True)

    

    # virtual methods.
    def content(self, **args):
        pass

    def execute(self):
        pass

    def is_help_enabled(self):
        return False
    def is_editmenu_enabled(self):
        return True
    def is_desc_enabled(self):
        return True

    def apply_button_label(self):
        return 'Apply'

    def postfunc(self):
        pass

    def reset_optvar(self):
        raise Exception('default options not set:', self.id)
    
    def is_reset_optvar_enabled(self):
        return True

    def filepath(self):
        return None
    

    # private.
    def __apply(self):
        self.__save_optionvar()
        self.execute()

    def __execute(self):
        self.__apply()
        pm.deleteUI(self.win, window=True)

    def __optname(self, name):
        return '%s__%s' % (self.id, name)

    def __save_optionvar(self):
        for item in self.items:
            w = item['object']
            optname = self.__optname(item['name'])
            if type(w) == ui.RadioCollection:
                v = pm.radioCollection(w, q=True, select=True)
                label = ui.RadioButton(v).getLabel()
                pm.optionVar(sv=(optname, label))
            elif type(w) == ui.CheckBoxGrp:
                pm.optionVar(iv=(optname, pm.checkBoxGrp(w, q=True, v1=True)))
            elif type(w) == ui.CheckBox:
                pm.optionVar(iv=(optname, pm.checkBox(w, q=True, v=True)))
            elif type(w) == ui.IntFieldGrp:
                pm.optionVar(iv=(optname, pm.intFieldGrp(w, q=True, v1=True)))
            elif type(w) == ui.FrameLayout:
                pm.optionVar(iv=(optname, pm.frameLayout(w, q=True, cl=True)))
            else:
                pm.warning('Not supported widget type:', w)


    def __load_optionvar(self):
        for item in self.items:
            optname =self.__optname(item['name'])
            if not pm.optionVar(ex=optname):
                continue
            v = pm.optionVar(q=optname)
            w = item['object']
            if type(w) == ui.RadioCollection:
                buf = pm.radioCollection(w, q=True, cia=True)
                for r in buf:
                    if pm.radioButton(r, q=True, label=True) == v:
                        pm.radioCollection(w, e=True, select=r)
                        break
            elif type(w) == ui.CheckBoxGrp:
                pm.checkBoxGrp(w, e=True, v1=True if v>0 else False)
            elif type(w) == ui.CheckBox:
                pm.checkBox(w, e=True, v=True if v>0 else False)
            elif type(w) == ui.IntFieldGrp:
                pm.intFieldGrp(w, e=True, v1=v)
            elif type(w) == ui.FrameLayout:
                pm.frameLayout(w, e=True, cl=True if v>0 else False)
            else:
                pm.warning('Not supported widget type:', w)

    
    def __reset_settings(self):
        self.reset_optvar()
        self.__load_optionvar()
        self.postfunc()

    
    def __description(self):
        path = self.filepath()
        res = None
        if path:
            dscfile = os.path.join(os.path.dirname(path), 'desc.yaml')
            with open(dscfile, encoding='utf-8') as f:
                dsc = None
                try:
                    yaml.UnsafeLoader
                except:
                    dsc = yaml.load(f)
                else:
                    dsc = yaml.load(f, Loader=yaml.UnsafeLoader)
                if dsc is None:
                    print('Failed in loading desc.yaml.')
                    return res 

            if self.id in dsc and dsc[self.id]['Description']:
                res = dsc[self.id]['Description']


        if not res:
            pm.frameLayout(self.fr_desc, e=True, cl=False)
            return 'No description file available.'
        return res