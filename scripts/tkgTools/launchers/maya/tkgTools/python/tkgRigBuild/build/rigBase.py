# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload
import tkgRigBuild.libs.file as tkgFile
reload(tkgFile)

class RigBase(object):
    def __init__(self,
                 model_path=None,
                 model_namespace=None,
                 guide_path=None):
        self.model_path = model_path
        self.model_namespace = model_namespace
        self.guide_path = guide_path

    def create_module(self):
        self.rig_hierarchy()
        if self.model_path:
            self.load_model()
        if self.guide_path:
            self.load_guide()

    def rig_hierarchy(self):
        self.root = self.rig_group(name="CHAR")
        self.model = self.rig_group(name="MODEL", parent=self.root)
        self.rig = self.rig_group(name="RIG", parent=self.root)
        self.skel = self.rig_group(name="SKEL", parent=self.root)

    def load_model(self):
        if self.model_namespace:
            root_nodes = tkgFile.reference_model(self.model_path, self.model_namespace)
        else:
            root_nodes = tkgFile.reference_model(self.model_path)
        cmds.parent(root_nodes, self.model)

    def load_guide(self):
        self.guide_roots = tkgFile.import_hierarchy(self.guide_path)

    def rig_group(self, empty=True, name=None, **kwargs):
        if not cmds.objExists(name):
            grp = cmds.group(empty=empty, name=name, **kwargs)
        else:
            grp = name
        return grp
