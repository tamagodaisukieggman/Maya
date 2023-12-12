# -*- coding: utf-8 -*-
import re
try:
    import maya.cmds as cmds
except:
    pass

from workfile_manager.plugin_utils import Application, PluginType
from workfile_manager_maya.export.preproc.preproc_maya_base import MayaPreprocBase

class Plugin(MayaPreprocBase):
    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        return True

    def execute(self, args):
        from postproc_set_editor_maya import ui_maya
        from postproc_set_editor import ui_main
        dcc_cmds = ui_maya.DccCmds()
        sel = cmds.ls(sl=True)
        grp = []

        for node in sel:
            nodes = [node]
            nodes += self._get_parents(node)
            
            grp.append(nodes)

        sets = cmds.ls(type='objectSet')
        sets = [x for x in sets if cmds.attributeQuery('postproc_edit_set__name', ex=True, n=x)]
        result_sets = []

        for set_ in sets:
            print('checking...', set_)
            if cmds.attributeQuery('execute_on_normal_publish', ex=True, n=set_):
                v = cmds.getAttr(set_+'.execute_on_normal_publish')
                if not v:
                    continue

            try:
                tg_set = ui_main.get_target_set(dcc_cmds, set_)
                if tg_set is None:
                    continue
            except:
                continue
            
            buf = cmds.sets(tg_set, q=True)
            if buf is None:
                buf = []
            for n in buf:
                for nodes in grp:
                    if n in nodes:
                        break
                else:
                    # not match.
                    break
            else:
                result_sets.append(set_)
                
        cmds.select(result_sets, ne=True, add=True)

        return True, None
        

    def get_label(self):
        return 'Select post-process edit sets'

    def order(self):
        return 1000000

    def is_editable(self):
        return False

    def default_checked(self):
        return True

    def _get_parents(self, node):
        import copy

        if type(node) is list:
            parents = []
            for n in node:
                parents += self._get_parents(n)
            return parents
        else:
            if cmds.objectType(node) == 'objectSet':
                return []

            parents = cmds.listRelatives(node, p=True, pa=True)
            if parents is None:
                parents = []

            for p in copy.deepcopy(parents):
                parents += self._get_parents(p)

            return parents
