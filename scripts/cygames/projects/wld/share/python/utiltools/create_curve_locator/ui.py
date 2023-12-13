import os
import re

import apiutils
from apiutils import uiutils
import cypyapiutils
from cypyapiutils import pyside as psutils



import pymel.core as pm
from maya import cmds
import importlib


class CreateCustomLocator(uiutils.OptionWindow):
    def filepath(self):
        return __file__

    def content(self, **args):
        self.mc = args['column']
        pm.setParent(self.mc)

        pm.columnLayout(adj=True, rs=10)
        self.ifg = ifg = pm.intFieldGrp(l='Division:', v1=24, cw2=(150, 80))
        pm.intFieldGrp(ifg, e=True)

        pm.rowLayout(nc=2, cw2=(150, 300))
        pm.text('')
        self.cb = cb = pm.checkBox(l='Keep control points', v=False)
        pm.checkBox(cb, e=True, cc=pm.Callback(self.cb_changed, cb))

        self.register_item(ifg, 'division')
        self.register_item(cb, 'keepControlPoints')

    def postfunc(self):
        self.cb_changed(self.cb)

    
    def cb_changed(self, cb):
        pm.intFieldGrp(self.ifg, e=True, en=not pm.checkBox(cb, q=True, v=True))


    def execute(self):
        from utiltools.create_curve_locator import cmds as lctcmds
        importlib.reload(lctcmds)
        lctcmds.convert()

    def apply_button_label(self):
        return 'Create'

    def reset_optvar(self):
        #toolopt = apiutils.ToolOpt(self.id)
        pass
        
    def is_desc_enabled(self):
        return False

def show():
    w = CreateCustomLocator('Create CurveLocator', w=500, h=250)
    w.show()