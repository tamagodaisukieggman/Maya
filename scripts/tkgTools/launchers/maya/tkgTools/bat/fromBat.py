# -*- coding: utf-8 -*-
import base64
from collections import OrderedDict
from datetime import datetime
from imp import reload
import json
import os
import pickle
import pprint
import traceback

from maya import cmds, mel

try:
    import tkgrig.tkg_skinCluster as tkgScn
    reload(tkgScn)
except:
    print(traceback.format_exc())


dir = '{}'.format(os.path.split(os.path.abspath(__file__))[0])
dir_path = dir.replace('\\', '/')

class BatFunc():
    def __init__(self):
        # Error Stack
        self.errors = []

        # Cameras
        self.default_cameras = ['persp', 'top', 'front', 'side']

        # Dirs
        self.check_dir = '{}/check'.format(dir_path)
        self.joints_dir = '{}/joints'.format(dir_path)
        self.meshes_dir = '{}/meshes'.format(dir_path)
        self.values_dir = '{}/values'.format(dir_path)
        self.skinWeights_dir = '{}/skinWeights'.format(dir_path)
        self.export_files_dir = '{}/exports'.format(dir_path)
        make_path = [self.check_dir,
                     self.joints_dir,
                     self.meshes_dir,
                     self.values_dir,
                     self.skinWeights_dir,
                     self.export_files_dir]
        for mkp in make_path:
            if not os.path.isdir(mkp):
                os.makedirs(mkp)

        date = u'{0}{1:4d}'.format(datetime.now().strftime("%Y%m%d_%H%M%S"), datetime.now().microsecond) # 時間は%H%M%S
        self.check_json = '{}/{}_nodeCheck.json'.format(self.check_dir, date)

        # Checks
        self.file_check_list = OrderedDict()

        # Check the same object names
        self.check_samename = None

        # Get Object Values
        self.check_object_values = None

        # Save Values:
        self.save_values = None

        # Export SkinWeights
        self.export_skinweights = None

        # Export MayaBinary
        self.export_mb_file = None

        # Detach Joints And Save
        self.detach_joints = None

        # Detach Meshes And Save
        self.detach_meshes = None

    def error_stack(func):
        def wrapper(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
            except:
                print(traceback.format_exc())
                self.errors.append(traceback.format_exc())
        return wrapper

    def file_open(func):
        def wrapper(self, *args, **kwargs):
            cur_path = cmds.file(q=1, sn=1)
            if not cur_path == self.file_path:
                cmds.file(self.file_path, o=1, iv=1, f=1)
            func(self, *args, **kwargs)
        return wrapper

    def create_primitive(self):
        mel.eval("""
        CreatePolygonSphere;
        CreatePolygonCube;
        CreatePolygonCylinder;
        """)

        bat_file = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/fromPython.bat'.format(os.getenv('USER'))

        cmds.file(rn="{}/bat_test.ma".format(os.path.dirname(bat_file)))
        file_type = "mayaAscii"
        cmds.file(f=1, save=1, options='v=0', type=file_type)

    def run_files(self, paths):
        print('PATHS', paths)
        listFiles = paths.split(' ')
        maya_openable_files = [file for file in listFiles if (file.endswith('.fbx') or file.endswith('.ma') or file.endswith('.mb'))]
        maya_command_files = [file for file in listFiles if (file.endswith('.py') or file.endswith('.mel'))]
        other_files = [file for file in listFiles if not (file.endswith('.py') or file.endswith('.mel') or file.endswith('.fbx') or file.endswith('.ma') or file.endswith('.mb'))]

        print('List Files:\n',maya_openable_files)
        print('List Commands:\n',maya_command_files)
        print('List Other Files:\n',other_files)

        for o_file in maya_openable_files:
            cur_path = cmds.file(q=1, sn=1)
            if not cur_path == o_file:
                cmds.file(o_file, o=1, iv=1, f=1)
            if self.check_samename:
                self.file_check_list[o_file] = OrderedDict()
                samenames_dict = OrderedDict()
                samenames_dict['Samename'] = self.get_samename()
                self.file_check_list[o_file] = samenames_dict
            if self.check_object_values:
                self.file_check_list[o_file] = OrderedDict()
                object_values_dict = OrderedDict()
                object_values_dict['ObjectValues'] = self.get_object_values()
                self.file_check_list[o_file] = object_values_dict
            if self.save_values:
                split_path = os.path.split(o_file)
                json_transfer('{}/{}.json'.format(self.values_dir, split_path[1]), operation='export', export_values=self.get_object_values())
            if self.export_skinweights:
                split_path = os.path.split(o_file)
                self.export_skinweights_from_tkg('{}/{}.json'.format(self.skinWeights_dir, split_path[1]))
            if self.export_mb_file:
                self.export_selected_file()
            if self.detach_joints:
                self.detach_joints_and_save()
            if self.detach_meshes:
                cmds.file(o_file, o=1, iv=1, f=1)
                self.detach_meshes_and_save()

        json_transfer(self.check_json, operation='export', export_values=self.file_check_list)

    def get_samename(self):
        return [node for node in cmds.ls(type='transform') if '|' in node]

    def get_node_values(self, node=None, node_values=None):
        node_values[node] = OrderedDict()

        node_parent = cmds.listRelatives(node, p=1) or None
        if node_parent:
            node_parent = node_parent[0]
        else:
            node_parent = None
        node_values[node]['Parent'] = node_parent

        node_shape = cmds.listRelatives(node, s=1) or None
        if node_shape:
            node_shape = cmds.objectType(node_shape[0])
        elif not node_shape:
            node_shape = None
        else:
            node_shape = node_shape[0]

        if cmds.objectType(node) == 'joint':
            node_shape = 'joint'
        elif 'Constraint' in cmds.objectType(node):
            node_shape = 'constraint'

        node_values[node]['Type'] = node_shape

        node_values[node]['Attributes'] = OrderedDict()
        attrsList = []
        node_listAttrs = cmds.listAttr(node, k=1)
        if node_listAttrs:
            if node_shape == 'joint':
                node_listAttrs += ['jointOrientX',
                                   'jointOrientY',
                                   'jointOrientZ',
                                   'side',
                                   'type',
                                   'otherType',
                                   'radius']
            for at in node_listAttrs:
                node_at = '{}.{}'.format(node, at)
                if len(node_at.split('.')) > 1:
                    node_at = '.'.join(node_at.split('.')[0:2])
                attrsList.append(node_at)

            attrsList.sort()

            for node_at in attrsList:
                try:
                    node_values[node]['Attributes'][node_at.split('.')[-1]] = cmds.getAttr(node_at)
                except RuntimeError:
                    pass

        node_values[node]['WorldSpace'] = {'translate':cmds.xform(node, q=1, t=1, ws=1),
                                           'rotate':cmds.xform(node, q=1, ro=1, ws=1)}

    def get_object_values(self):
        node_values=OrderedDict()
        allNodes = cmds.ls(type='transform')
        for node in allNodes:
            self.get_node_values(node, node_values)

        return node_values

    def set_object_values(self, path=None, type=None):
        node_values = json_transfer(path, operation='import')
        sel = cmds.ls(os=1)
        for node, values in node_values.items():
            if node in sel:
                for key, types in values.items():
                    if key == type:
                        if 'Attributes' == type:
                            for at, val in types.items():
                                try:
                                    if at == "otherType":
                                        cmds.setAttr('{}.{}'.format(node, at), str(val), type='string')
                                    else:
                                        cmds.setAttr('{}.{}'.format(node, at), val)

                                except Exception:
                                    print(traceback.format_exc())


    def detach_joints_and_save(self):
        allNodes = cmds.ls(type='transform')
        joints = cmds.ls(type='joint')
        if not joints:
            return
        [cmds.lockNode(jt, l=1) for jt in joints]
        [cmds.lockNode(cam, l=1) for cam in self.default_cameras]

        for node in allNodes:
            try:
                cmds.delete(node)
            except:
                pass

        [cmds.lockNode(jt, l=0) for jt in joints]
        [cmds.lockNode(cam, l=0) for cam in self.default_cameras]

        mel.eval('cleanUpScene 3;')

        cur_path = cmds.file(q=1, sn=1)
        split_path = os.path.split(cur_path)

        if split_path[1].endswith('.mb'):
            file_type = 'mayaBinary'
        elif split_path[1].endswith('.ma'):
            file_type = 'mayaAscii'

        cmds.file(rn='{}/{}'.format(self.joints_dir, split_path[1]))
        cmds.file(f=1, save=1, options='v=0', type=file_type)

        return

    def detach_meshes_and_save(self):
        allNodes = cmds.ls(type='transform')
        meshShapes = cmds.ls(exactType='mesh')
        meshes = list(set([mesh for mesh in cmds.listRelatives(meshShapes, p=1) if meshShapes]))

        if not meshShapes or not meshes:
            return

        [cmds.lockNode(ms, l=1) for ms in meshes]
        [cmds.lockNode(cam, l=1) for cam in self.default_cameras]

        for node in allNodes:
            try:
                cmds.delete(node)
            except:
                pass

        [cmds.lockNode(ms, l=0) for ms in meshes]
        [cmds.lockNode(cam, l=0) for cam in self.default_cameras]

        mel.eval('cleanUpScene 3;')

        cur_path = cmds.file(q=1, sn=1)
        split_path = os.path.split(cur_path)

        if split_path[1].endswith('.mb'):
            file_type = 'mayaBinary'
        elif split_path[1].endswith('.ma'):
            file_type = 'mayaAscii'

        cmds.file(rn='{}/{}'.format(self.meshes_dir, split_path[1]))
        cmds.file(f=1, save=1, options='v=0', type=file_type)

        return

    def export_skinweights_from_tkg(self, fileName=None):
        skinClusters, skinedGeos = tkgScn.get_geometories_from_skinClusters()
        if not skinedGeos:
            return

        tkgSkinCluster = tkgScn.TKGSkinWeights()
        tkgSkinCluster.export_file = True
        getWeightsValues = tkgSkinCluster.get_objects_weights(skinedGeos)
        tkgScn.json_transfer(fileName, 'export', export_values=getWeightsValues)

        # s = base64.b64encode(pickle.dumps(getWeightsValues)).decode("utf-8")
        # d = {"pickle": s}
        # with open(fileName, "w") as f:
        #     json.dump(d, f)


    def export_selected_file(self):
        top_nodes = cmds.ls(assemblies=True)
        export_nodes = [exnode for exnode in top_nodes if not exnode in self.default_cameras]
        cmds.select(export_nodes, r=1)

        cur_path = cmds.file(q=1, sn=1)
        split_path = os.path.split(cur_path)

        cmds.file('{}/{}'.format(self.export_files_dir, split_path[1]), f=1, typ='mayaBinary', pr=1, es=1, options="v=0;")


def json_transfer(fileName=None, operation=None, export_values=None):
    if operation == 'export':
        try:
            with codecs.open(fileName, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

        except:
            with open(fileName, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

    elif operation == 'import':
        try:
            with codecs.open(fileName, 'r', encoding='utf-8') as f:
                return json.load(f, 'utf-8', object_pairs_hook=OrderedDict)

        except:
            with open(fileName, 'r', encoding="utf-8") as f:
                return json.load(f, object_pairs_hook=OrderedDict)
