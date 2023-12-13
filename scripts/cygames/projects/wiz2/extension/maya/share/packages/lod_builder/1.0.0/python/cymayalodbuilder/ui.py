import os

import pymel.core as pm

import apiutils
from apiutils import uiutils
import cypyapiutils
import importlib

class LodBuilder(uiutils.OptionWindow):
    def filepath(self):
        return __file__

    def content(self, **args):
        self.cur = 0
        varfile = os.path.join(os.path.dirname(__file__), 'variables.yaml')
        self.var = cypyapiutils.Variable(self.id, toolgroup='Maya', defaultfile=varfile)

        self.mc = args['column']
        pm.setParent(self.mc)
        c1 = pm.columnLayout()

        pm.rowLayout(nc=3, cw3=(30, 30, 200), cat=(3, 'left', 30))
        pm.button(l='+', w=30, c=pm.Callback(self.add_item))
        pm.button(l='-', w=30, c=pm.Callback(self.remove_item))
        self.cb = pm.checkBox(l='Delete Original', v=False)

        pm.setParent(c1)
        self.selgp = pm.columnLayout(adj=True)
        self.target = []
        for i in range(self.var.size('LODs')):
            lod = self.var.get('LODs')[i]
            self.add_item(name=lod['name'], percent=lod['percent'], ui_only=True)
        pm.setParent('..')

        self.register_item(self.cb, 'deleteOriginal')
    
    def add_item(self, name=None, percent=None, ui_only=False):
        pm.setParent(self.selgp)
        if not name:
            i = self.var.size('LODs')
            name = 'LOD%d' % i
            buf = self.var.get('LODs')
            if buf:
                while len([x for x in buf if x['name']==name]) > 0:
                    name = 'LOD%d' % i
                    i += 1
            percent = 1.0
        self.target.append(OneSelection(name, percent, self.cur, parent=self))
        self.cur += 1
        lod = self.target[-1]

        if not ui_only:
            v = {'name':lod.name, 'percent':lod.percent}
            self.var.add('LODs', v)

    def remove_item(self):
        if len(self.target) <= 1:
            return
        self.target[-1].delete()
        del self.target[-1]
        self.var.pop('LODs')

    def execute(self):
        from . import command
        importlib.reload(command)
        command.exe()

    def apply_button_label(self):
        return 'Build'

    def reset_optvar(self):
        toolopt = apiutils.ToolOpt(self.id)
        toolopt.savevalue('deleteOriginal', False)
        del self.target[:]
        for n in pm.columnLayout(self.selgp, q=True, ca=True):
            pm.deleteUI(n)
        self.var.load_default()
        
        pm.setParent(self.selgp)            
        for i in range(self.var.size('LODs')):
            lod = self.var.get('LODs')[i]
            self.add_item(name=lod['name'], percent=lod['percent'], ui_only=True)

    #def is_editmenu_enabled(self):
    #    return False

class OneSelection:
    def __init__(self, name=None, percent=None, id_=None, parent=None):
        self.parent = parent
        self.id = id_
        self.name = name
        self.percent = percent
        self.build()

    def delete(self):
        pm.deleteUI(self.root)

    def delpressed(self):
        if len(self.parent.target) == 1:
            return
        if self in self.parent.target:
            pm.deleteUI(self.root)
            index = self.index()
            del self.parent.target[index]
            self.parent.var.removeByIndex('LODs', index)
        #for t in self.parent.target:
        #    print 'id:', t.id, 'name:', t.name, 'percent:', t.percent


    def index(self):
        index = None
        if self in self.parent.target:
            index = self.parent.target.index(self)
        return index

    def build(self):
        self.root = pm.rowLayout(nc=5, cw5=(30, 230, 10, 120, 200))
        pm.button(l='x', w=20, c=pm.Callback(self.delpressed))
        self.tfg_name = pm.textFieldGrp(l='Lod Name:', cw2=(80, 140), cat=(1, 'right', 10), 
                tx=self.name, cc=pm.Callback(self.changed))
        pm.text(l='')
        self.ffg_percent = pm.floatFieldGrp(l='Percent:', cw2=(50, 60), pre=3,  
                cat=(1, 'right', 10), v1=self.percent, cc=pm.Callback(self.changed))
        bw = 30
        pm.rowLayout(nc=4, cw4=(bw, bw, bw, bw))
        pm.button(l='100%', w=bw, c=pm.Callback(self.pcpressed, 1.0))
        pm.button(l='50%', w=bw, c=pm.Callback(self.pcpressed, 0.5))
        pm.button(l='20%', w=bw, c=pm.Callback(self.pcpressed, 0.2))
        pm.button(l='5%', w=bw, c=pm.Callback(self.pcpressed, 0.05))
        pm.setParent('..')
        pm.setParent('..')

    def pcpressed(self, v):
        pm.floatFieldGrp(self.ffg_percent, e=True, v1=v)
        self.changed()

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

    def get_nodes(self):
        res = []
        if pm.tabLayout(self.tl, q=True, sti=True)==1:
            res.append(pm.textFieldGrp(self.tfg_target, q=True, tx=True))
        else:
            for n in pm.textScrollList(self.tsl, q=True, ai=True):
                res.append(n)
        return res


    def changed(self):
        name = pm.textFieldGrp(self.tfg_name, q=True, tx=True)
        self.name = name
        pct = pm.floatFieldGrp(self.ffg_percent, q=True, v1=True)
        if self in self.parent.target:
            index = self.index()
            self.parent.var.get('LODs')[index]['name'] = name
            self.parent.var.get('LODs')[index]['percent'] = pct
            self.parent.var.save()


def show():
    w = LodBuilder('Lod Builder', w=550, h=400)
    w.show()

