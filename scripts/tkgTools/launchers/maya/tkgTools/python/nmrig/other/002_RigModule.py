import maya.cmds as cmds

class RigModule(RigBase):
    def __init__(self, model_path=None):
        self.model_path = model_path

rig_object = RigModule(model_path="cylinder")
rig_object.create_module()

class RigModule(RigBase):
    def __init__(self, side=None, part=None, model_path=None):
        self.side = side
        self.part = part
        self.model_path = model_path

        if not self.side:
            self.side = "Cn"
        if not self.part:
            self.part = "default"
        self.base_name = self.side + "_" + self.part

    def create_module(self):
        super(RigModule, self).create_module()
        self.part_hierarchy()

    def part_hierarchy(self):
        self.part_grp = self.rig_group(name=self.base_name, parent=self.rig)
        self.module_grp = self.rig_group(name=self.base_name + "_MODULE", parent=self.part_grp)
        self.control_grp = self.rig_group(name=self.base_name + "_CONTROL", parent=self.part_grp)

rig_object = RigModule(model_path="cylinder")
rig_object.create_module()
