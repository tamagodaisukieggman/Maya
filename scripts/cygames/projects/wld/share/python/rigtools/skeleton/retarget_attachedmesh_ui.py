import pymel.core as pm
import pymel.core.uitypes as ui

from apiutils import uiutils
import apiutils

class RetargetAttachedMeshOpt(uiutils.OptionWindow):
    def content(self, **args):
        tb = pm.tabLayout(tv=False, scr=True, cr=True)
        pm.tabLayout(tb, e=True, tv=True, innerMarginHeight=50)
        
        cl = pm.columnLayout(adj=True)

        pm.tabLayout(tb, e=True, tl=(cl, 'Basic'))

        # Basic Tab
        pm.separator(style='none')
        pm.rowLayout(nc=2, cat=(1, 'both',10), cw2=(200, 200), rat=(1, 'top', 3))
        pm.text(l='Surface Association:', al='right')
        pm.columnLayout()
        rc = pm.radioCollection()
        mmlabel = ('UV', 'VertexID', 'Position')
        rb = list()
        for l in mmlabel:
            rb.append(pm.radioButton(l=l))
        pm.radioCollection(rc, e=True, select=rb[0])
        
        #
        pm.setParent(cl)
        pm.rowLayout(nc=2, cat=(1, 'both',10), cw2=(200, 200), rat=(1, 'top', 3))
        pm.text(l='Object Match Mode:', al='right')
        pm.columnLayout()
        rc_mm = pm.radioCollection()
        mmlabel = ('Object Name', 'Mesh Topology')
        rb = list()
        for l in mmlabel:
            rb.append(pm.radioButton(l=l, enable=False))
        pm.radioCollection(rc_mm, e=True, select=rb[0])

        #
        pm.setParent(cl)
        cbg = pm.checkBoxGrp(l='Construction History:', ncb=1, v1=False, cw2=(200, 200), 
                ct2=('both', 'both'), co2=(10, 0), en=False)



        # Advance Tab
        pm.setParent(tb)
        cl2 = pm.columnLayout(rs=10, adj=True)
        pm.separator(style='none')
        pm.tabLayout(tb, e=True, tl=(cl2, 'Advanced'))
        args = {'cw2':(200, 50), 'co2':(10, 0), 'ct2':('both', 'both')}
        ifg_iter = pm.intFieldGrp(l='Iterations:', v1=3, **args)
        self.cb_sm = pm.checkBoxGrp(l='Enable Smoothing:', ncb=1, v1=True, **args) 
        self.ifg_sm = pm.intFieldGrp(l='Smoothness:', v1=1, **args)
        pm.checkBoxGrp(self.cb_sm, e=True, cc=pm.Callback(self.cb_changed, self.cb_sm, self.ifg_sm))
        pm.separator(style='none', h=10)
        self.cb_av = pm.checkBoxGrp(l='Enable Averaging:', ncb=1, v1=False, **args) 
        self.ifg_av = pm.intFieldGrp(l='Iterations:', v1=10, **args)
        pm.checkBoxGrp(self.cb_av, e=True, cc=pm.Callback(self.cb_changed, self.cb_av, self.ifg_av))



        self.register_item(rc, 'matchMode')
        self.register_item(rc_mm, 'objMatchMode')
        self.register_item(cbg, 'history')
        self.register_item(self.cb_sm, 'preSmoothEnabled')
        self.register_item(self.ifg_sm, 'preSmoothValue')
        self.register_item(self.cb_av, 'preAverageEnabled')
        self.register_item(self.ifg_av, 'preAverageValue')
        self.register_item(ifg_iter, 'numIterations')

    def execute(self):
        from . import retarget_attachedmesh_cmds
        retarget_attachedmesh_cmds.exe()

        
    def postfunc(self):
        self.cb_changed(self.cb_sm, self.ifg_sm)
        self.cb_changed(self.cb_av, self.ifg_av)

    def apply_button_label(self):
        return 'Retarget'

    def cb_changed(self, cb, ifg):
        v = pm.checkBoxGrp(cb, q=True, v1=True)
        pm.intFieldGrp(ifg, e=True, en=v)

    def reset_optvar(self):
        print('reset_optvar:', self.id)
        toolopt = apiutils.ToolOpt(self.id)
        toolopt.savevalue('matchMode', 'UV')
        toolopt.savevalue('objMatchMode', 'Object Name')
        toolopt.savevalue('history', False)
        toolopt.savevalue('preSmoothEnabled', True)
        toolopt.savevalue('preSmoothValue', 1)
        toolopt.savevalue('preAverageEnabled', False)
        toolopt.savevalue('preAverageValue', 10)
        toolopt.savevalue('numIterations', 3)

    def filepath(self):
        return __file__
        
def show():
    w = RetargetAttachedMeshOpt('Retarget Attached Meshes')
    w.show()

