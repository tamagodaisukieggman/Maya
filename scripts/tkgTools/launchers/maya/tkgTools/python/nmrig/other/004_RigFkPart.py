import maya.cmds as cmds

class RigFkPart(RigModule):
    def __init__(self, side=None, part=None, model_path=None, position_list=[]):
        super(RigFkPart, self).__init__(side=side, part=part, model_path=model_path)
        self.position_list = position_list

        self.create_module()

    def create_module(self):
        super(RigFkPart, self).create_module()
        fk_module = Fk(name=self.base_name, position_list=self.position_list)
        fk_module.build_fk()
        cmds.parent(fk_module.control_list[0], self.control_grp)
        cmds.parent(fk_module.joint_list[0], self.module_grp)

        self.bind_joints = fk_module.joint_list

fk_part = RigFkPart(model_path="cylinder", position_list=[(0,0,0), (0,1,0), (0,1,0), (0,3,0), (0,4,0), (0,5,0), (0,6,0)])
cmds.skinCluster(fk_part.bind_joints, "pCylinder1", toSelectedBones=True)
