import pymel.core as pm

import maya.mel as mel

from apiutils import uiutils
import apiutils
from . import cmdpreset
import importlib

class BatchToolUI(uiutils.OptionWindow):

    def content(self, **args):
        self.mc = args['column']
        pm.setParent(self.mc)

        c1 = pm.columnLayout(adj=True)

        self.tbl_cmd = pm.tabLayout()
        tb_mel = pm.columnLayout(adj=True)
        pm.rowLayout(nc=2, ad2=1, h=50, cat=[(2, 'right', 10)])
        self.tfg_mel = pm.textFieldGrp(l='Mel Command:', cw=(1, 120), ad2=2, cat=[(1, 'right', 10)])
        pm.button('Preset', w=70, c=pm.Callback(self.open_cmdpreset, 'mel'))
        pm.setParent('..')
        pm.setParent('..')
        tb_py = pm.columnLayout(adj=True)
        pm.rowLayout(nc=2, ad2=1, h=50, cat=[(2, 'right', 10)])
        self.tfg_py = pm.textFieldGrp(l='Python Command:', cw=(1, 120), ad2=2, cat=[(1, 'right', 10)])
        pm.button('Preset', w=70, c=pm.Callback(self.open_cmdpreset, 'python'))
        pm.tabLayout(self.tbl_cmd, e=True, tabLabel=((tb_mel, 'Mel'), (tb_py, 'Python')))

        pm.setParent(c1)
        pm.rowLayout(nc=2)
        pm.button(l='+', w=30, c=pm.Callback(self.add_item))
        pm.button(l='-', w=30, c=pm.Callback(self.remove_item))

        pm.setParent(c1)
        self.selgp = pm.columnLayout(adj=True, rs=20)
        self.target = []
        self.target.append(OneSelection(label='First Selection'))
        self.target.append(OneSelection(label='Second Selection'))
        #self.target.append(OneSelection(label='Third Selection'))
        pm.setParent('..')

        deftabs = [1] * len(self.target)
        deftabs[-1] = 2

        for i, t in enumerate(self.target):
            pm.tabLayout(t.tl, e=True, sti=deftabs[i])
            t.tabchanged()
        #pm.text(l='', h=20)
    
    def open_cmdpreset(self, lang):
        from . import cmdpreset
        importlib.reload(cmdpreset)
        w = cmdpreset.CmdPresetUI('Batch Tool Command Presets', lang, self, w=500, h=350)
        w.show()

    def add_item(self):
        pm.setParent(self.selgp)
        self.target.append(OneSelection(label='#%d Selection' % (len(self.target)+1)))

    def remove_item(self):
        if len(self.target) <= 1:
            return
        self.target[-1].delete()
        del self.target[-1]

    def execute(self):
        self.loop(0)

    def loop(self, depth, sel=[]):
        for n in self.target[depth].get_nodes():
            res = sel + [n]
            if depth == len(self.target)-1:
                print('Selection: ', res)
                self.execmd(res)

            else:
                self.loop(depth+1, res)

    def execmd(self, sel):
        pm.select(sel)
        if pm.tabLayout(self.tbl_cmd, q=True, sti=True)==1:
            melcmd = pm.textFieldGrp(self.tfg_mel, q=True, tx=True)
            print('Execute(Mel): ', melcmd)
            mel.eval(melcmd)

        else:
            pycmd = pm.textFieldGrp(self.tfg_py, q=True, tx=True)
            print('Execute(Python): ', pycmd)
            exec('from maya.cmds import *;'+pycmd)


    def apply_button_label(self):
        return 'Batch'

    def reset_optvar(self):
        toolopt = apiutils.ToolOpt(self.id)
        #toolopt.savevalue('matchMode', 'UV')

    def is_editmenu_enabled(self):
        return False

class OneSelection:
    def __init__(self, label):
        self.typemaps = [('mesh','Mesh'), ('joint','Joint')]
        self.label = label
        self.build()
        self.tabchanged()

    def delete(self):
        pm.deleteUI(self.frl)

    def build(self):
        cw1 = 100
        ch = 40

        self.frl = pm.frameLayout(l=self.label)
        self.tl = tl = pm.tabLayout()
        c1 = pm.columnLayout(adj=True)
        pm.rowLayout(nc=2, ad2=1, cat=(2, 'right', 20))
        self.tfg_target = pm.textFieldGrp(l='Target:', h=ch, cw=(1, cw1), ad2=2, cat=(1, 'right', 10))
        pm.button('Load', w=60, c=pm.Callback(self.set_target, self.tfg_target))
        pm.setParent('..')
        pm.setParent('..')
        c2 = pm.columnLayout(adj=True)
        la = {}
        for i, t in enumerate(self.typemaps):
            la['label%d' % (i+1)] = t[1]
        self.rbg = pm.radioButtonGrp(nrb=2, h=ch, label='NodeType:', cw3=(cw1, 70, 70), 
                cat=(1, 'right', 10), en2=False, select=1, **la)
        pm.columnLayout(adj=True)

        loadbtn = pm.button('Load')
        self.tsl = pm.textScrollList()
        pm.button(loadbtn, e=True, c=pm.Callback(self.load_list, self.tsl, self.rbg))
        pm.setParent('..')
        pm.setParent('..')

        pm.setParent('..')
        pm.tabLayout(tl, e=True, tabLabel=((c1, 'Single'), (c2, 'Multiple')), sc=pm.Callback(self.tabchanged))

    def set_target(self, tfg):
        buf = pm.selected()
        if len(buf) == 0:
            return
        pm.textFieldGrp(tfg, e=True, tx=buf[0].name())

    def load_list(self, tsl, rbg):
        ntype = self.typemaps[pm.radioButtonGrp(rbg, q=True, select=True)-1][0]
        buf = pm.selected(type=ntype) + pm.listRelatives(ad=True, type=ntype, ni=True)
        pm.textScrollList(tsl, e=True, ra=True)
        for n in buf:
            pm.textScrollList(tsl, e=True, a=n.name())

    def tabchanged(self):
        ti = pm.tabLayout(self.tl, q=True, sti=True)
        if ti == 1:
            pm.tabLayout(self.tl, e=True, h= 60)
        else:
            pm.tabLayout(self.tl, e=True, h=200)

    def get_nodes(self):
        res = []
        if pm.tabLayout(self.tl, q=True, sti=True)==1:
            res.append(pm.textFieldGrp(self.tfg_target, q=True, tx=True))
        else:
            for n in pm.textScrollList(self.tsl, q=True, ai=True):
                res.append(n)
        return res

def show():
    w = BatchToolUI('Batch Tool', w=500, h=400)
    w.show()

