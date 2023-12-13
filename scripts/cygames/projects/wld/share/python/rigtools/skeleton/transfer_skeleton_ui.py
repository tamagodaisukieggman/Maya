import pymel.core as pm
import pymel.core.uitypes as ui

from apiutils import uiutils
import apiutils

class TransferSkeletonOption(uiutils.OptionWindow):
    def content(self, **args):
        c1 = pm.columnLayout()

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
        pm.setParent(c1)
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
        pm.setParent(c1)
        cbg = pm.checkBoxGrp(l='Construction History:', ncb=1, v1=False, cw2=(200, 200), 
                ct2=('both', 'both'), co2=(10, 0), en=False)

        self.register_item(rc, 'matchMode')
        self.register_item(rc_mm, 'objMatchMode')
        self.register_item(cbg, 'history')


    def execute(self):
        from . import transfer_skeleton_cmds
        transfer_skeleton_cmds.exe()

    def apply_button_label(self):
        return 'Retarget'

    def reset_optvar(self):
        toolopt = apiutils.ToolOpt(self.id)
        toolopt.savevalue('matchMode', 'UV')
        toolopt.savevalue('objMatchMode', 'Object Name')
        toolopt.savevalue('history', False)

    def filepath(self):
        return __file__

def show():
    w = TransferSkeletonOption('Retarget Skeleton')
    w.show()

