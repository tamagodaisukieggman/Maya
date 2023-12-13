# -*- coding: utf-8 -*-


from workfile_manager import p4utils
from cylibassetdbutils import assetdbutils
from workman_world_custom.asset_actions.all import publish_parts_base
from workfile_manager.plugin_utils import Application

try:
    from workfile_manager import fbxutils
except:
    pass

from Qt import QtWidgets, QtCore, QtGui
import re, os

db = assetdbutils.DB.get_instance()


class FBXReader(fbxutils.Fbx):
    def get_sets(self):
        self.setobj = {}

        res = []
        for i in range(self.scene.GetMemberCount()):
            n = self.scene.GetMember(i)
            
            pr = fbxutils.cast_property(n.FindProperty('postproc_edit_set__name'))
            if pr is None:
                continue

            if n.GetName() not in self.setobj:
                self.setobj[n.GetName()] = n

            partname = pr.Get()
            res.append((n.GetName(), partname.Buffer()))
        return res

    def get_operators(self, partnames):
        from postproc_set_editor import operator
        ops = []
        root_sets = self.get_sets()
        for setname, partname in root_sets:
            if partnames is not None and partname not in partnames:
                continue
            setobj = self.setobj[setname]
            for ci in range(setobj.GetSrcObjectCount()):
                cn = setobj.GetSrcObject(ci)
                #print('>child:',cn.GetName())
                pr = fbxutils.cast_property(cn.FindProperty('postproc_edit_set__operator_name'))
                if pr is None:
                    continue
                op_type = pr.Get()
                op = operator.get_operator_from_typename(op_type)
                ops.append((cn.GetName(), op))
        return ops
    
    def get_linked_objects(self, partname):
        try:
            setname = [x[0] for x in self.get_sets() if x[1]==partname][0]
        except:
            return
        setobj = self.setobj[setname]
        objs = []
        for ci in range(setobj.GetSrcObjectCount()):
            cn = setobj.GetSrcObject(ci)
            if not cn.GetName().endswith('_target'):
                continue
            for i in range(cn.GetSrcObjectCount()):
                c = cn.GetSrcObject(i)
                objs.append(c.GetName())
            break
        return objs


    def get_set_attribute(self, setname, pname, ptype=None):
        import fbx
        from postproc_set_editor import operator
        for i in range(self.scene.GetMemberCount()):
            n = self.scene.GetMember(i)
            if n.GetName() == setname:
                break
        else:
            return None

        pr = fbxutils.cast_property(n.FindProperty(pname))
        if pr is None:
            return
        v = pr.Get()

        if ptype is None:
            if type(v) is fbx.FbxString:
                return v.Buffer()
            return v
        else:
            if ptype == operator.ParamType.String:
                if type(v) is fbx.FbxString:
                    return v.Buffer()
                else:
                    return str(v)
            elif ptype == operator.ParamType.Boolean:
                return v
            elif ptype == operator.ParamType.Float:
                return float(v)
            elif ptype == operator.ParamType.Int:
                return int(v)
            elif ptype == operator.ParamType.Enum:
                return v
            elif ptype == operator.ParamType.Vector3D:
                return v
        return v


    def get_set_members(self, setname):
        import fbx
        objs = []
        for i in range(self.scene.GetMemberCount()):
            n = self.scene.GetMember(i)
            if n.GetName() == setname:
                break
        else:
            return objs
            
        for i in range(n.GetSrcObjectCount()):
            c = n.GetSrcObject(i)
            objs.append(c.GetName())

        return objs




    def calc_total_publish_cnts(self, parts, operators):
        from postproc_set_editor import operator
        n_publish = 0
        for set_node_name, partname in self.get_sets():
            if partname not in parts:
                continue
            ops = self.get_operators([partname])
            n = 0
            for op_name, op in ops:
                if operators is not None and op_name not in operators:
                    continue
                if op.is_publish_operator():
                    n += 1
            
            if n == 0:
                n = 1

            n_publish += n
        
        return n_publish
            
    


class BasePlugin(publish_parts_base.BasePlugin):
    def application(self):
        return Application.MotionBuilder

    def get_reader(self, filename):
        reader = FBXReader(filename)
        return reader

    def open(self, filename):
        pass

    def get_postprocs(self, all_postprocs):
        child_postprocs = all_postprocs
        postprocs = all_postprocs

        return postprocs, child_postprocs

    

    








    