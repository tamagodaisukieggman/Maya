import pymel.core as pm
import apiutils.uiutils as uiutils
import apiutils


class WeightImportOpt(uiutils.OptionWindow):
    def content(self, **args):
        c1 = pm.columnLayout()

        pm.rowLayout(nc=2, cw2=(150, 200), cat=(1, 'both',10), cl2=('right', 'left'), rat=(1, 'top', 3))
        pm.text(l='Surface Association:', al='right')   
        pm.columnLayout()
        rc = pm.radioCollection()   
        rb1 = pm.radioButton(l='Closest Point')
        rb2 = pm.radioButton(l='Closest Component')
        rb3 = pm.radioButton(l='UV')
        pm.radioCollection(rc, e=True, select=rb1)

        pm.setParent(c1)
        cb = pm.checkBoxGrp(l='Delete History:', ncb=1, v1=False, cw2=(150, 200), 
                ct2=('both', 'both'), co2=(10, 0))
        

        self.register_item(rc, 'matchMode')
        self.register_item(cb, 'deleteHistory')

    def execute(self):
        import rigtools.skin
        rigtools.skin.weight_cmds.import_weight()

    def apply_button_label(self):
        if self.title.startswith('Import'):
            return 'Import'
        else:
            return 'Copy'
    
    def reset_optvar(self):
        toolopt = apiutils.ToolOpt(self.id)
        toolopt.savevalue('matchMode', 'Closest Point')
        toolopt.savevalue('deleteHistory', False)

    def filepath(self):
        return __file__

class WeightCopyOpt(WeightImportOpt):
    def execute(self):
        import rigtools.skin
        rigtools.skin.weight_cmds.copy_weight()


def show_import_opt():
    w = WeightImportOpt('Import Skin Weight')
    w.show()

def show_copy_opt():
    w = WeightCopyOpt('Copy Skin Weight')
    w.show()    