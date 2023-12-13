# -*- coding: utf-8 -*-
from __future__ import print_function
try:
    import maya.cmds as cmds
    from workfile_manager_maya import assetutils_maya

except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase):
    def application(self):
        return Application.Maya

    def apps_executable_on(self):
        return (
            Application.Maya,
            Application.MotionBuilder,
            Application.Standalone,
        )

    def is_asset_eligible(self, asset):
        return True

    def order(self):
        return 1000

    def is_namespace_linked(self, rfn):
        try:
            ns = cmds.referenceQuery(rfn, ns=True)
            return ns
        except:
            return None


    def execute(self, args):
        try:
            sel = args['global_args']['selection']
        except:
            sel = []
        print('sel:', sel)
        export_nodes = assetutils_maya.get_nodes_to_export_selection(sel=sel)
        #print('export_nodes:', export_nodes) # Too much information to print.
        selected_ns = []
        for n in export_nodes:
            if '|' in n:
                n = n[n.rindex('|')+1:]
            if ':' in n:
                ns = n[:n.rindex(':')]
            else:
                ns = None
            if ns is None:
                continue
            if ns not in selected_ns:
                selected_ns.append(ns)
        for ns in selected_ns:
            print('Selected namespace:', ns)


        valid, _ = self.is_valid()
        if not valid:
            return False

        ns_from_refs = [cmds.referenceQuery(x, ns=True) for x in cmds.ls(type='reference') if self.is_namespace_linked(x) is not None]

        for ns in cmds.namespaceInfo(lon=True, an=True):
            print('ns:', ns)
            if sel is not None and sel != []:
                if ns.strip(':') not in selected_ns:
                    print('skip:', ns)
                    continue
            print('Check deletable: ', ns)
            if ns in ns_from_refs:
                if 'deletable_ns' not in args or ns not in args['deletable_ns']:
                    continue
            if ns=='UI' or ns=='shared':
                continue
            try:
                cmds.namespace(mergeNamespaceWithRoot=True, removeNamespace=ns)
                print('Namespace deleted:', ns)
            except:
                pass
        return True

    def getlabel(self):
        return 'Delete Namespaces'

    def default_checked(self):
        return True

    def is_valid(self):
        return True, ''

    def is_editable(self):
        return False