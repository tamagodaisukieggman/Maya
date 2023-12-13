import re

import pymel.core as pm
import pymel.core.uitypes as ui

from apiutils import uiutils
import apiutils

class NodeRenamer(uiutils.OptionWindow):
    def content(self, **args):
        pm.setParent(args['column'])
        pm.columnLayout(adj=True, rs=5)

        cw1 = 100
        tw = 200
        pm.rowLayout(nc=3, cw3=(310, 30, 40))
        self.tfg1 = pm.textFieldGrp(l='Search Pattern:', cw2=(cw1, tw), cat=(1, 'right', 10))
        pm.button(l='BS', w=30, c=pm.Callback(self.backspace, self.tfg1))
        pm.button(l='Clear', w=40, c=pm.Callback(self.fieldchange, self.tfg1, '', True))
        pm.setParent('..')
        pm.rowLayout(nc=2, cw2=(cw1, 300))
        pm.text(l='')
        pm.rowLayout(nc=5)
        pm.button(l='Namesp.', c=pm.Callback(self.fieldchange, self.tfg1, r'(^[^:]+:)', True))
        pm.button(l='Prefix', c=pm.Callback(self.fieldchange, self.tfg1, r'(^[^_]+_)', True))
        pm.button(l='Suffix', c=pm.Callback(self.fieldchange, self.tfg1, r'(_[^_]+$)', True))
        pm.button(l='Head', c=pm.Callback(self.fieldchange, self.tfg1, r'(^)', True))
        pm.button(l='Tail', c=pm.Callback(self.fieldchange, self.tfg1, r'($)', True))
        pm.setParent('..')
        pm.setParent('..')

        pm.rowLayout(nc=3, cw3=(310, 30, 40))
        self.tfg2 = pm.textFieldGrp(l='Replace:', cw2=(cw1, tw), cat=(1, 'right', 10))
        pm.button(l='BS', w=30, c=pm.Callback(self.backspace, self.tfg2))
        pm.button(l='Clear', w=40, c=pm.Callback(self.fieldchange, self.tfg2, '', True))
        pm.setParent('..')
        pm.rowLayout(nc=2, cw2=(cw1, 300))
        pm.text(l='')
        bw = 40
        pm.rowLayout(nc=3, cw3=[bw]*3)
        pm.button(l=r'\1', w=bw, c=pm.Callback(self.fieldchange, self.tfg2, r'(1)'))
        pm.button(l=r'\2', w=bw, c=pm.Callback(self.fieldchange, self.tfg2, r'(2)'))
        pm.button(l=r'\3', w=bw, c=pm.Callback(self.fieldchange, self.tfg2, r'(3)'))
        pm.setParent('..')
        pm.setParent('..')

        pm.text(l='')
        self.rbg = pm.radioButtonGrp(l='Hierarchy:', sl=1, nrb=2, la2=['Selected', 'Below'], cw3=(cw1, 80, 80), cat=(1, 'right', 10))
        #self.register_item(rc, 'matchMode')
        #self.register_item(rc_mm, 'objMatchMode')
        #self.register_item(cbg, 'history')


    def execute(self):
        pt = pm.textFieldGrp(self.tfg1, q=True, tx=True)
        rp_org = pm.textFieldGrp(self.tfg2, q=True, tx=True)
        for n in pm.selected():
            self.exec_node(n, pt, rp_org)

    def exec_node(self, n, pt, rp_org):
        rp = rp_org
        name = n.nodeName()
        m = re.search(pt, name)
        if not m:
            return
        cnt = len(m.groups())
        
        while True:
            m2 = re.search(r'\((\d+)\)', rp)
            if not m2:
                break
            i = int(m2.group(1))
            rp = re.sub(r'\(\d+\)', m.group(i), rp, 1)
        newname = re.sub(pt, rp, name, 1)
        print(name, ' ---> ', newname)
        self.addnamespace(newname)
        print(name, ' ---> ', newname)
        pm.rename(n.name(), newname)

        if pm.radioButtonGrp(self.rbg, q=True, select=True) == 2:
            cld = pm.listRelatives(n, c=True)
            for c in cld:
                self.exec_node(c, pt, rp_org)


    def addnamespace(self, newname, index=1):
        m = re.search('^([^:]*:){%d}' % index, newname)
        if not m:
            return
        ns = m.group(0)[:-1]
        if not pm.namespace(ex=ns):
            pm.namespace(add=ns)

        index += 1
        self.addnamespace(newname, index=index)

    def apply_button_label(self):
        return 'Rename'

    def reset_optvar(self):
        pass
        #toolopt = apiutils.ToolOpt(self.id)
        #toolopt.savevalue('matchMode', 'UV')
        #toolopt.savevalue('objMatchMode', 'Object Name')
        #toolopt.savevalue('history', False)
    def is_editmenu_enabled(self):
        return False
    def is_desc_enabled(self):
        return False


    def fieldchange(self, w, tx, replace=False):
        org = ''
        if not replace:
            org = pm.textFieldGrp(w, q=True, tx=True)
        pm.textFieldGrp(w, e=True, tx=org+tx)

    def backspace(self, w):
        org = pm.textFieldGrp(w, q=True, tx=True)
        tx = re.sub(r'\([^\(]*$', '', org)
        pm.textFieldGrp(w, e=True, tx=tx)        


def show():
    w = NodeRenamer('Node Renamer', w=400, h=260)
    w.show()

