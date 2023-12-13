import pymel.core as pm

import apiutils.uiutils
from . import command

class MainWindow(apiutils.uiutils.OptionWindow):
    def content(self, **args):
        pm.columnLayout()
        cbg = pm.checkBoxGrp(l='Construction History:', ncb=1, v1=False, cw2=(200, 200), 
                ct2=('both', 'both'), co2=(10, 0))
        self.register_item(cbg, 'history')

    def execute(self):
        command.exe()        

    def is_editmenu_enabled(self):
        return False
    def filepath(self):
        return __file__

    def apply_button_label(self):
        return 'Generate'

def show():
    w = MainWindow('Eyelash Generator')
    w.show()