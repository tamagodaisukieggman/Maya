# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    import maya.cmds as cmds
    
except:
    pass

from workfile_manager import p4utils
from cylibassetdbutils import assetdbutils
from workfile_manager.plugin_utils import Application
from workman_world_custom.asset_actions.all import publish_parts_base

import cgkit.mayaascii

from Qt import QtWidgets, QtCore, QtGui
import re, os

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()


class MAReader(cgkit.mayaascii.DefaultMAReader, object):
    def __init__(self):
        super(MAReader, self).__init__()
        self.sets = {}
        self.currentNode = None
        self.roots = {}
        
    def onCreateNode(self, nodetype, opts):
        if nodetype == 'objectSet':
            name = opts['name'][0]
            self.currentNode = name
            self.sets[name] = {}
            
    def onSetAttr(self, attr, vals, opts):
        if self.currentNode in self.sets:
            attrname = attr.strip('"')[1:]
            if attrname in self.sets[self.currentNode]:
                #print('Attr already set: ', self.currentNode, attrname)
                return
            self.sets[self.currentNode][attrname] = vals
            if attrname == 'postproc_edit_set__name':
                self.roots[self.currentNode] = {}
            
            
    def onConnectAttr(self, srcattr, dstattr, opts):
        buf  = dstattr.strip('"').split('.')
        nodename = buf[0]
        attrname = buf[1]

        if attrname == 'dnsm' or attrname == 'dsm':
            if nodename in self.roots:
                v = self.roots[nodename]
                if 'children' not in v:
                    v['children'] = []
                buf = srcattr.strip('"').split('.')
                v['children'].append(buf[0])

            if nodename in self.sets:
                v = self.sets[nodename]
                if 'member' not in v:
                    v['member'] = []
                buf = srcattr.strip('"').split('.')
                v['member'].append(buf[0])


    def get_sets(self):
        res = []
        for k in self.roots:
            try:
                partname = self.sets[k]['postproc_edit_set__name'][0].strip('"')
            except:
                continue
            res.append((k, partname))
        
        return res

    def get_set_attribute(self, setname, pname, ptype=None):
        from postproc_set_editor import operator
        try:
            dic = self.sets[setname]
            v = dic[pname]
        except:
            return None

        try:
            if ptype is None:
                if len(v) > 1:
                    return v
                else:
                    return v[0].strip('"')
            else:
                if ptype == operator.ParamType.String:
                    return v[0].strip('"')
                elif ptype == operator.ParamType.Boolean:
                    vstr = v[0].strip('"')
                    if vstr == 'yes':
                        return True
                    else:
                        return False

                elif ptype == operator.ParamType.Float:
                    try:
                        return float(v[0])
                    except:
                        return 0.0
                elif ptype == operator.ParamType.Int:
                    try:
                        return int(v[0])
                    except:
                        return 0
                elif ptype == operator.ParamType.Enum:
                    return int(v[0])
                elif ptype == operator.ParamType.Vector3D:
                    return v
        except:
            return None


    def get_operators(self, partnames):
        ops = []
        from postproc_set_editor import operator

        for k in self.roots:
            try:
                partname = self.sets[k]['postproc_edit_set__name'][0].strip('"')
            except:
                continue

            if partnames is not None and partname not in partnames:
                continue

            root = self.roots[k]
            
            for ch in root['children']:
                if ch not in self.sets:
                    continue
                op_set_attrs = self.sets[ch]
                if 'postproc_edit_set__operator_name' not in op_set_attrs:
                    continue
                
                op_type = op_set_attrs['postproc_edit_set__operator_name'][0].strip('"')
                op = operator.get_operator_from_typename(op_type)
                ops.append((ch, op))

        return ops

    def get_set_members(self, setname):
        if setname in self.sets:
            if 'member' in self.sets[setname]:
                return self.sets[setname]['member']
        return []

    def get_linked_objects(self, partname):
        def get_partname(k):
            try:
                return self.sets[k]['postproc_edit_set__name'][0].strip('"')
            except:
                pass
            return None

        #
        from postproc_set_editor import operator
        buf = [self.roots[k] for k in self.roots if get_partname(k) == partname]
        if len(buf) > 0:
            root = buf[0]
        else:
            return []

        for ch in root['children']:
            if ch not in self.sets:
                continue
            if not ch.endswith('_target'):
                continue

            if 'member' in self.sets[ch]:
                return self.sets[ch]['member']
            

        return []


    def calc_total_publish_cnts(self, parts, operators):
        from postproc_set_editor import operator
        n_publish = 0
        for k in self.roots:
            try:
                partname = self.sets[k]['postproc_edit_set__name'][0].strip('"')
            except:
                continue

            if partname not in parts:
                continue

            root = self.roots[k]
            n = 0

            for ch in root['children']:
                if ch not in self.sets:
                    continue
                if operators is not None and ch not in operators:
                    continue

                op_set_attrs = self.sets[ch]
                
                if 'postproc_edit_set__operator_name' not in op_set_attrs:
                    continue
                op_type = op_set_attrs['postproc_edit_set__operator_name'][0].strip('"')

                op = operator.get_operator_from_typename(op_type)
                if op.is_publish_operator():
                    n += 1
            
            if n == 0:
                n = 1
            n_publish += n

        return n_publish

    


def convert_ma_to_cgkit_readable(source_filename):
    import tempfile
    tmpdir = tempfile.gettempdir()
    tmpfile = os.path.join(tmpdir, assetdbutils.datetime_to_str(msec=True, for_filename=True)+'.ma')
    with open(source_filename, 'r') as rfh:
        with open(tmpfile, 'w') as wfh:
            expr1 = re.compile('-ignoreVersion')
            expr2 = re.compile('-typ\s+"[^"]+"')
            expr3 = re.compile('(.*)-ch [^\s]+(.*)')
            expr4 = re.compile('(.*)-dcb [^\s]+(.*)')
            expr5 = re.compile('-iv ')
            
            lines = rfh.readlines()
            ctx = None
            file_ctx = None
            file_st = ''
            for i in range(len(lines)):
                line = lines[i]
                if ' ' in line:
                    if not line.startswith('\t'):
                        idx = line.index(' ')
                        st = line[:idx].strip()
                        if st != '':
                            ctx = st
                            #if ctx != 'file' and file_ctx:
                            #    break
                
                if ctx == 'file':
                    file_ctx = True
                    if not line.endswith(';\n'):
                        file_st += line
                        lines[i] = ''
                    else:
                        if file_st != '':
                            line = file_st + line
                            file_st = ''

                        line = expr1.sub('', line)
                        line = expr2.sub('', line)
                        line = expr5.sub(' ', line)
                        lines[i] = line
                elif ctx == 'requires':
                    lines[i] = ''
                elif ctx == 'createNode':
                    if line.startswith('createNode objectSet'):
                        ctx = 'createNode objectSet'
                    else:
                        lines[i] = ''

                elif ctx == 'otherNodeType':
                    lines[i] = ''


                elif ctx == 'instanceable':
                    lines[i] = ''

                

            wfh.writelines(lines)
    return tmpfile
    
class BasePlugin(publish_parts_base.BasePlugin):
    def application(self):
        return Application.Maya

    def get_reader(self, filename):
        reader = MAReader()
        tmpfile = convert_ma_to_cgkit_readable(filename)
        print('convert_ma_to_cgkit_readable tmpfile: ', tmpfile)
        reader.read(tmpfile)
        os.remove(tmpfile)
        return reader

    def is_open_valid(self):
        return True

    def open(self, filename):
        cmds.file(filename, ignoreVersion=True, o=True, f=True)

    def get_postprocs(self, all_postprocs):
        child_postprocs = all_postprocs
        print('child_postprocs: ', child_postprocs)

        idx = [x['module_name'][x['module_name'].rfind('.')+1:] for x in child_postprocs].index(self.postproc_name())
        pp = child_postprocs.pop(idx)

        from workfile_manager import postproc_utils, plugin_utils
        imp_pp = postproc_utils.find_proc_by_name('maya.all.import_postproc_set', plugin_type=plugin_utils.PluginType.PublishPostProcess)

        postprocs = [imp_pp, pp]

        return postprocs, child_postprocs
    







    