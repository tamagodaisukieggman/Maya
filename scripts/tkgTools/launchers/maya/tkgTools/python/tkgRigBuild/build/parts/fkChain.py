# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.build.chain as tkgChain
import tkgRigBuild.build.fk as tkgFk
import tkgRigBuild.libs.attribute as tkgAttr
reload(tkgModule)
reload(tkgChain)
reload(tkgFk)
reload(tkgAttr)

class FkChain(tkgModule.RigModule, tkgFk.Fk):
    """
    # -*- coding: utf-8 -*-
    import maya.cmds as cmds
    from imp import reload

    import tkgRigBuild.build.parts.fkChain as tkgFkChain
    import tkgRigBuild.post.finalize as tkgFinalize
    reload(tkgFkChain)
    reload(tkgFinalize)

    import traceback

    sel = cmds.ls(os=True, dag=True)
    try:
        tkgFkChain.FkChain(
                        side=None,
                         part=None,
                         guide_list=sel,
                         gimbal=True,
                         offset=True,
                         pad="auto",
                         ctrl_scale=3,
                         ctrl_color=[0.8, 0.8, 0],
                         remove_last=True,
                         fk_shape="cube",
                         gimbal_shape="circle",
                         offset_shape="square",
                         model_path=None,
                         guide_path=None)
    except:
        print(traceback.format_exc())

    tkgFinalize.add_color_attributes()
    """
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 gimbal=True,
                 offset=True,
                 pad="auto",
                 fk_ctrl_axis='x',
                 fk_ctrl_edge_axis='-x',
                 ctrl_scale=1,
                 ctrl_color=[0.1, 0.4, 0.8],
                 remove_last=True,
                 fk_shape="circle",
                 gimbal_shape="circle",
                 offset_shape="square",
                 model_path=None,
                 guide_path=None):
        super(FkChain, self).__init__(side=side,
                                      part=part,
                                      guide_list=guide_list,
                                      ctrl_scale=ctrl_scale,
                                      model_path=model_path,
                                      guide_path=guide_path)

        self.guide_list = guide_list
        self.gimbal = gimbal
        self.offset = offset
        self.pad = pad
        self.fk_ctrl_axis = fk_ctrl_axis
        self.fk_ctrl_edge_axis = fk_ctrl_edge_axis
        self.ctrl_color = ctrl_color
        self.remove_last = remove_last
        self.fk_shape = fk_shape
        self.gimbal_shape = gimbal_shape
        self.offset_shape = offset_shape

        self.part_fk_main_ctrls = []
        self.part_fk_gimbal_ctrls = []
        self.part_fk_offset_ctrls = []

        if self.pad == "auto":
            self.pad = len(str(len(self.guide_list))) + 1

        self.create_module()

    def create_module(self):
        super().create_module()

        self.control_rig()
        self.output_rig()
        self.skeleton()

    def control_rig(self):
        self.build_fk_controls()
        cmds.parent(self.fk_ctrls[0].top, self.control_grp)

    def output_rig(self):
        self.build_fk_chain()
        cmds.parent(self.fk_joints[0], self.module_grp)

    def skeleton(self):
        fk_chain = tkgChain.Chain(transform_list=self.fk_joints,
                                 prefix=self.side,
                                 suffix="JNT",
                                 name=self.part)
        fk_chain.create_from_transforms(parent=self.skel)

        if self.remove_last:
            cmds.delete(self.fk_ctrls[-1].top)
            self.bind_joints = fk_chain.joints[:-1]
        else:
            self.bind_joints = fk_chain.joints

        self.tag_bind_joints(self.bind_joints, self.part_grp)
