# -*- coding: utf-8 -*-

import maya.cmds as cmds

import traceback
from imp import reload

import tkgRigBuild.build.rigBase as tkgBase
import tkgRigBuild.libs.attribute as tkgAttr
import tkgRigBuild.libs.common as tkgCommon
reload(tkgBase)
reload(tkgAttr)
reload(tkgCommon)

class RigModule(tkgBase.RigBase):
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 ctrl_scale=None,
                 model_path=None,
                 model_namespace=None,
                 guide_path=None):
        try:
            super().__init__(model_path=model_path,
                             model_namespace=model_namespace,
                             guide_path=guide_path)
        except:
            print(traceback.format_exc())

        self.side = side
        self.part = part
        self.guide_list = guide_list
        self.ctrl_scale = ctrl_scale
        self.model_path = model_path
        self.model_namespace = model_namespace
        self.guide_path = guide_path

        if not self.side:
            self.side = "Cn"
        if not self.part:
            self.part = "default"
        self.base_name = self.side + "_" + self.part

        if self.guide_list:
            if not isinstance(self.guide_list, list):
                self.guide_list = [self.guide_list]

        # self.create_module()

    def create_module(self):
        super().create_module() # Python3のsuper()の書き方
        self.part_hierarchy()

        if not self.ctrl_scale:
            bb = tkgCommon.get_bounding_box(self.model)
            if abs(bb[0]) > abs(bb[1]):
                scale_factor = abs(bb[0])
            else:
                scale_factor = abs(bb[1])
            self.ctrl_scale = scale_factor

    def part_hierarchy(self):
        self.part_grp = self.rig_group(name=self.base_name, parent=self.rig)
        self.module_grp = self.rig_group(name=self.base_name + "_MODULE", parent=self.part_grp)
        self.control_grp = self.rig_group(name=self.base_name + "_CONTROL", parent=self.part_grp)

        if self.part != "root":
            self.global_scale = tkgAttr.Attribute(node=self.part_grp,
                                                 type="double",
                                                 value=1,
                                                 keyable=True,
                                                 name="globalScale")

    def tag_bind_joints(self, joints, part_grp):
        if not isinstance(joints, list):
            joints = [joints]
        for jnt in joints:
            tkgAttr.Attribute(node=jnt,
                             type="bool",
                             value=True,
                             keyable=False,
                             name="bindJoint")

        tkgAttr.Attribute(node=part_grp,
                         type="string",
                         value=','.join(joints),
                         keyable=False,
                         name="partJoints",
                         lock=True)

    def sort_side_list(self, side_list):
        """
        Appendix
        """
        side_list_sorted = []
        for sides in side_list:
            # sides = side_list[0]

            appendy = []
            name_replace = False
            for s in sides:
                for u in ['', '_']:
                    if name_replace:
                        for n in ['LEFTADD', 'RIGHTADD']:
                            if not n+u+s in appendy:
                                appendy.append(n+u+s)
                            if not u+s+n in appendy:
                                appendy.append(u+s+n)
                            if not n+s+u in appendy:
                                appendy.append(n+s+u)
                            if not s+u+n in appendy:
                                appendy.append(s+u+n)

                    else:
                        if not u+s in appendy:
                            appendy.append(u+s)
                        if not s+u in appendy:
                            appendy.append(s+u)

            side_list_sorted.append(appendy)

        return side_list_sorted

    def create_endJnt(self, base=None, wt=None, awt_obj=None):
        """
        Appendix
        """
        dup = cmds.duplicate(base, n=base + '_ENDJNT', po=True)[0]
        if awt_obj:
            wt = cmds.xform(awt_obj, q=True, t=True, ws=True)
            cmds.xform(dup, t=wt, ws=True, a=True)

        else:
            cmds.xform(dup, t=wt, ws=True, r=True)

        cmds.parent(dup, base)

        return dup
