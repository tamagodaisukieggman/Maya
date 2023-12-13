import os

import pymel.core as pm

from apiutils import uiutils
import cypyapiutils

class CmdPresetUI(uiutils.OptionWindow, object):
    def __init__(self, title, lang, parent, w=None, h=None):
        super(CmdPresetUI, self).__init__(title, w=w, h=h)
        self.lang = lang # mel or python
        self.parent = parent

    def content(self, **args):
        varfile = os.path.join(os.path.dirname(__file__), 'variables.yaml')
        self.var = cypyapiutils.Variable(self.id, defaultfile=varfile)

        self.cmds = []

        self.mc = args['column']

        c1 = pm.columnLayout(adj=True)

        pm.rowLayout(nc=2, ad2=1, rat=[(1, 'top', 0), (2, 'top', 0)])
        pm.columnLayout(adj=True)
        self.tsl = pm.textScrollList()
        pm.setParent('..')
        pm.columnLayout()
        pm.button(l='Delete', w=100, c=pm.Callback(self.delete))

        pm.setParent(c1)
        pm.columnLayout(adj=True)
        pm.rowLayout(nc=2, ad2=1)
        self.tfg_name = pm.textFieldGrp(l='Name:', ad2=2, cw=(1, 70))
        pm.text(l='', w=100)
        pm.setParent('..')
        pm.rowLayout(nc=3, ad2=1)
        self.tfg_cmd = pm.textFieldGrp(l='Command:', ad2=2, cw=(1, 70))
        #pm.setParent('..')
        self.addbtn = pm.button('Mel', w=70, c=pm.Callback(self.cmdbtn_pressed, 'mel'))
        self.addpybtn = pm.button('Python', w=70, c=pm.Callback(self.cmdbtn_pressed, 'python'))

        pm.textScrollList(self.tsl, e=True, sc=pm.Callback(self.selected))
        pm.textScrollList(self.tsl, e=True, dcc=pm.Callback(self.execute))
        self.load_cmds()

    def selected(self):
        buf = pm.textScrollList(self.tsl, q=True, sii=True)
        if len(buf) > 0:
            index = buf[0] - 1
            pm.textFieldGrp(self.tfg_name, e=True, tx=self.cmds[index][0])
            pm.textFieldGrp(self.tfg_cmd, e=True, tx=self.cmds[index][1])
        else:
            pm.textFieldGrp(self.tfg_name, e=True, tx='')
            pm.textFieldGrp(self.tfg_cmd, e=True, tx='')

    def load_cmds(self):
        names = self.var.get('CommandName')
        cmds = self.var.get('CommandContent')
        langs = self.var.get('CommandLang')
        if names and cmds and langs:
            for c in zip(names, cmds, langs):
                #if c[2] != self.lang:
                #    continue
                self.__additem(c)
                self.cmds.append(c)
        
    def execute(self):
        index = pm.textScrollList(self.tsl, q=True, sii=True)[0]-1
        c = self.cmds[index]
        
        if c[2] == 'mel':
            pm.textFieldGrp(self.parent.tfg_mel, e=True, tx=c[1])
            pm.tabLayout(self.parent.tbl_cmd, e=True, sti=1)
        else:
            pm.textFieldGrp(self.parent.tfg_py, e=True, tx=c[1])
            pm.tabLayout(self.parent.tbl_cmd, e=True, sti=2)


    def apply_button_label(self):
        return 'Select'

    def is_editmenu_enabled(self):
        return False

    def delete(self):
        buf = pm.textScrollList(self.tsl, q=True, sii=True)
        if len(buf) == 0:
            return
        index = buf[0]
        self.var.removeByIndex('CommandName', index-1)
        self.var.removeByIndex('CommandContent', index-1)
        self.var.removeByIndex('CommandLang', index-1)
        pm.textScrollList(self.tsl, e=True, rii=index)
        del self.cmds[index-1]
        pm.textScrollList(self.tsl, e=True, da=True)
        

    def cmdbtn_pressed(self, lang):
        name = pm.textFieldGrp(self.tfg_name, q=True, tx=True)
        if name == '':
            return
        cmd = pm.textFieldGrp(self.tfg_cmd, q=True, tx=True)
        if cmd == '':
            return
        c = (name, cmd, lang)
        self.cmds.append(c)
        self.__additem(c)
        self.var.add('CommandName', name)
        self.var.add('CommandContent', cmd)
        self.var.add('CommandLang', lang)

    def __additem(self, c):
        #pm.textScrollList(self.tsl, e=True, a='%s:\t%s' % c)
        pm.textScrollList(self.tsl, e=True, a='%s (%s)' % (c[0], c[2]))
        pm.textScrollList(self.tsl, e=True, da=True)
        self.selected()