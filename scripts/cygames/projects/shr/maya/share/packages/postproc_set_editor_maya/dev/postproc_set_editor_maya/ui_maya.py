# -*- coding: utf-8 -*-
from __future__ import print_function
import os, re

import postproc_set_editor
from postproc_set_editor import ui_main
from maya.app.general import mayaMixin

import pymel.core as pm
from maya import cmds

class DccCmds(postproc_set_editor.DccCmdsBase):
    def dccutils(self):
        from workfile_manager_maya import assetutils_maya
        dccutils = assetutils_maya.MayaUtils.get_instance()
        return dccutils

    def open(self, filename):
        cmds.file(filename, ignoreVersion=True, o=True, f=True)

    def is_node_from_reference(self, node):
        if type(node) is not str:
            return True if cmds.reference(node.name(), q=True, inr=True) else False
        else:    
            return True if cmds.reference(node, q=True, inr=True) else False
        
    def list_nodes(self, nodes=None, **args):
        if nodes is None:
            return pm.ls(**args)
        else:
            return pm.ls(nodes, **args)

    def list_node_names(self, nodes=None, **args):
        if nodes is None:
            return [x.name() for x in self.list_nodes(**args)]
        else:
            return [x.name() for x in self.list_nodes(nodes, **args)]
    
    def select(self, nodes=None, **args):
        if nodes is None:
            pm.select(**args)
        else:
            pm.select(nodes, **args)

    def obj_exists(self, node):
        return pm.objExists(node)

    def object_type(self, node):
        return pm.objectType(node)

    def sets(self, obj=None, **args):
        if obj is None:
            return pm.sets(**args)
        else:
            return pm.sets(obj, **args)

    def get_setobj(self, setname):
        return pm.PyNode(setname)

    def add_attr(self, node, **args):
        from postproc_set_editor import operator
        if 'at' in args and args['at'] == operator.ParamType.Vector3D:
            pm.addAttr(node, ln=args['ln'], at='double3')
            for ax in 'XYZ':
                pm.addAttr(node, ln='%s%s' % (args['ln'], ax), at='double', p=args['ln'])

            pm.setAttr(node+'.'+args['ln'], e=True, keyable=True)
            for ax in 'XYZ':
                pm.setAttr(node+'.%s%s' % (args['ln'], ax), e=True, keyable=True)

        else:
            pm.addAttr(node, **args)

    def set_attr(self, attrname, value=None, **args):
        if value is None:
            pm.setAttr(attrname, **args)    
        else:
            from postproc_set_editor import operator
            if 'type' in args and args['type'] == operator.ParamType.Vector3D:
                args.pop('type')
                for idx, axis in enumerate('XYZ'):
                    pm.setAttr(attrname+axis, value[idx], **args)

            elif 'enum_string' in args and args['enum_string']:
                nodename, _attrname = attrname.split('.')
                items = cmds.attributeQuery(_attrname, le=True, n=nodename)[0].strip(':').split(':')
                if value in items:
                    idx = items.index(value)
                    args.pop('enum_string')
                    pm.setAttr(attrname, idx, **args)    
                else:
                    print('%s not found in enum list.' % value)
            else:
                pm.setAttr(attrname, value, **args)


    def get_attr(self, attrname, **args):
        if 'enum_string' in args and args['enum_string']:
            try:
                nodename, _attrname = attrname.split('.')
                items = cmds.attributeQuery(_attrname, le=True, n=nodename)[0].strip(':').split(':')
                idx = pm.getAttr(attrname)
                return items[idx]
            except Exception as e:
                print(e)
                print('Failded in getting value as enum string.')
                return None
        
        else:
            v = pm.getAttr(attrname)
            if type(v) is pm.datatypes.Vector:
                return [v[0], v[1], v[2]]
            else:
                return v

    def set_enum_list(self, node, attrname, items):
        pm.addAttr(node.name()+'.'+attrname, e=True, enumName=':'.join(items))

    def dgdirty(self, **args):
        cmds.dgdirty(**args)

    def get_name(self, obj):
        return obj.name()

    def delete(self, node):
        pm.delete(node)

    def duplicate(self, objs, **args):
        cmds.duplicate(objs, **args)

    def attribute_query(self, attrname, **args):
        return pm.attributeQuery(attrname, **args)

    def dryrun(self, main_widget, args, work_asset, wfile):
        from workfile_manager.export.postproc import postproc_edit_set as ppes
        from workfile_manager import postproc_utils
        from workfile_manager.plugin_utils import PluginType
        from workfile_manager_maya import ui_maya
        from cylibassetdbutils import assetdbutils

        mwin = ui_maya.MainWindow(toolgroup='Default', toolname='workfile_manager')

        setobjs = main_widget.get_current_setobjs()
        
        if setobjs is None:
            return

        commit = True if 'commit_to_engine' in args and args['commit_to_engine'] else False

        for setobj in setobjs:
            spc = [setobj.get_setname()]
            pp = ppes.Plugin()
            _args = {'plugin_name':'postproc_edit_set', 'specified':spc, 'dryrun':True,
                        'commit_to_engine':commit, 'submit_server':True if 'submit_server' in args and args['submit_server'] else False,
                        'deadline_batchname': re.sub('[.][^.]*', '', assetdbutils.labelpostfix()),
                    }
            
            if not args['submit_server']:
                _args['background_subprocess'] = True

            if commit:
                commit_procs = postproc_utils.get_postprocs(work_asset, mwin, only_enabled=True, plugin_type=PluginType.CommitProcess)
                _args['procs'] = commit_procs

            if 'comment' in args:
                _args['comment'] = args['comment']
            pp.execute(_args)

    def is_root_set(self, set_):
        buf = cmds.listConnections(set_+'.message', s=False, d=True, p=True)
        if buf is None:
            return True
        else:
            for c in buf:
                node, attr = c.split('.')
                if cmds.objectType(node) == 'objectSet' and 'dnSetMembers' in attr:
                    return False
            return True
        
        



class MainWindow(mayaMixin.MayaQWidgetBaseMixin, ui_main.PostprocSetEditor):
    def __init__(self, varfile, toolgroup, parent=None):
        self.dcc_cmds = DccCmds()
        super(mayaMixin.MayaQWidgetBaseMixin, self).__init__(varfile, toolgroup)
        
    def show(self):
        super(mayaMixin.MayaQWidgetBaseMixin, self).show()
    

def show():
    global mwin
    try:
        mwin.close()
    except:
        pass

    varfile = os.path.join(os.path.dirname(__file__), 'config_preset.yaml')
    toolgroup = 'Maya'
    mwin = MainWindow(varfile, toolgroup)

    mwin.resize(1000, 500)
    mwin.show()
