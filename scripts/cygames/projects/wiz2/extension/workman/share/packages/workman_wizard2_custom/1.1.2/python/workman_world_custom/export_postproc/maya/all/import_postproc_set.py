# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import shutil
import subprocess
import yaml

try:
    import maya.cmds as cmds
    import pymel.core as pm
except:
    pass

from workfile_manager.plugin_utils import Application
from workfile_manager_maya.export.postproc import postproc_maya_base

try:
    from postproc_set_editor import ui_preset
except:
    pass

class Plugin(postproc_maya_base.MayaPostprocBase):
    def apps_executable_on(self):
        return [
            Application.MotionBuilder,
        ]

    def is_asset_eligible(self, asset):
        return True

    def order(self):
        return 1

    def proc_preset(self, dic, preset_name):
        def includes_another_set(tg):
            for _preset in list(dic['presets'].keys()):
                if 'node_name' not in list(dic['presets'][_preset].keys()):
                    continue
                if tg == dic['presets'][_preset]['node_name']:
                    return _preset
            return None

        if preset_name in self.done:
            return
        ops = dic['presets'][preset_name]['operator']
        for op in ops:
            for tg in op['targets']:
                anset = includes_another_set(tg)
                if anset:
                    self.proc_preset(dic, anset)

        res = ui_preset.create_set_from_preset(dic['presets'], preset_name, self.dcc_cmds, use_node_name=self.use_node_name, rename_if_exist=True)
        for setobj in res:
            print('set created:', self.dcc_cmds.get_name(setobj.pm_set))
        self.done.append(preset_name)


    def execute(self, args):
        from workfile_manager import cmds as wcmds
        from postproc_set_editor_maya import ui_maya
        self.dcc_cmds = ui_maya.DccCmds()

        self.done = []

        if 'postproc_set_file' not in args:
            return
        setfile = args['postproc_set_file']
        print('setfile: ', setfile.replace('/', '\\'))

        with open(setfile, 'r') as fhd:
            dic = wcmds.yaml_load(fhd)
            print('setfile found:', dic)

        keys = list(dic['presets'].keys())
        self.use_node_name = True if 'use_node_name' in args and args['use_node_name'] else False

        for preset_name in keys:
            self.proc_preset(dic, preset_name)
        
        #if os.path.exists(setfile):
        #    os.remove(setfile)
        return True
            

    def getlabel(self):
        return 'Import Post-process Sets'

    def default_checked(self):
        return True

    def is_editable(self):
        return False