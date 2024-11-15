# -*- coding: utf-8 -*-

import maya.cmds as cmds
import ast
from imp import reload


import tkgRigBuild.libs.control.draw as tkgDraw
import tkgRigBuild.libs.group as tkgGroup
import tkgRigBuild.libs.common as tkgCommon
import tkgRigBuild.libs.attribute as tkgAttr
import tkgRigBuild.libs.transform as tkgXform
import tkgRigBuild.libs.maths as tkgMath
reload(tkgDraw)
reload(tkgGroup)
reload(tkgCommon)
reload(tkgAttr)
reload(tkgXform)
reload(tkgMath)

class Control(tkgDraw.Draw, tkgGroup.Group):
    def __init__(self, ctrl=None,
                parent=None,
                shape="circle",
                prefix="Lf",
                suffix="CTRL",
                name="default",
                axis="y",
                group_type="main",
                rig_type="primary",
                ctrl_scale=1,
                ctrl_color=[0.2, 0.5, 0.8],
                edge_axis=None,
                position=(0,0,0),
                rotation=(0,0,0),
                scale=(1,1,1)):

        self.group_dict = {"main": ["CNST", "MOCAP", "SDK", "OFF"],
                           "offset": ["CNST", "OFF"]}
        self.parent = parent
        self.position = position
        self.rotation = rotation
        self.scale = scale

        ctrl_color = [tkgMath.round_value(c) for c in ctrl_color]
        past_one_color_idx = [i for i, v in enumerate(ctrl_color) if 1 < v]
        if past_one_color_idx:
            for past_one in past_one_color_idx:
                ctrl_color[past_one] = 1

        self.ctrl = ctrl
        if not self.ctrl:
            self.shape = shape
            self.prefix = prefix
            self.suffix = suffix
            self.name = name
            self.axis = axis
            self.group_type = group_type
            self.rig_type = rig_type
            self.ctrl_scale = ctrl_scale
            self.ctrl_color = ctrl_color
            self.edge_axis = edge_axis

            if prefix:
                self.ctrl_name = "{}_{}_{}".format(self.prefix, self.name, self.suffix)
            else:
                self.ctrl_name = "{}_{}".format(self.name, self.suffix)
            self.create()

        else:
            self.get_control()

    def create(self):
        self.create_curve(name=self.ctrl_name,
                          shape=self.shape,
                          axis=self.axis,
                          scale=self.ctrl_scale)
        self.ctrl = self.curve

        tkgXform.move_pivot(ctrl=self.ctrl, edge_axis=self.edge_axis)

        if isinstance(self.group_type, str):
            self.group_by_list(nodes=self.ctrl,
                               pad_name_list=self.group_dict[self.group_type],
                               name=self.ctrl_name)

        elif isinstance(self.group_type, list):
            self.group_by_list(nodes=self.ctrl,
                               pad_name_list=self.group_type,
                               name=self.ctrl_name)

        elif isinstance(self.group_type, int):
            self.group_by_int(nodes=self.ctrl,
                              group_num=self.group_type,
                              name=self.ctrl_name)

        else:
            self.group_list = None
            self.top = self.ctrl_name
            self.bot = self.ctrl_name
            cmds.warning(self.ctrl + " has no group padding")

        tkgXform.match_pose(node=self.top,
                           position=self.position,
                           rotation=self.rotation,
                           scale=self.scale)

        if self.parent:
            cmds.parent(self.top, self.parent)
        self.tag_control()

    def get_control(self):
        tag_dict = cmds.getAttr(self.ctrl + ".ctrlDict")
        self.control_dict = ast.literal_eval(tag_dict)
        self.curve = self.ctrl
        self.shape = self.control_dict["shape"]
        self.prefix = self.control_dict["prefix"]
        self.suffix = self.control_dict["suffix"]
        self.name = self.control_dict["name"]
        self.axis = self.control_dict["axis"]
        self.group_list = self.control_dict["rig_groups"]
        self.rig_type = self.control_dict["rig_type"]
        self.ctrl_scale = self.control_dict["ctrl_scale"]
        self.ctrl_color = self.control_dict["ctrl_color"]
        if self.prefix:
            self.ctrl_name = "{}_{}_{}".format(self.prefix, self.name, self.suffix)

        else:
            self.ctrl_name = "{}_{}".format(self.name, self.suffix)

        if self.group_list:
            self.bot = self.group_list[0]
            self.top = self.group_list[-1]

    def tag_control(self):
        self.control_dict = {"shape": self.shape,
                             "prefix": self.prefix,
                             "suffix": self.suffix,
                             "name": self.name,
                             "axis": self.axis,
                             "rig_groups": self.group_list,
                             "rig_type": self.rig_type,
                             "ctrl_scale": self.ctrl_scale,
                             "ctrl_color": self.ctrl_color}

        tag_string = str(self.control_dict)

        tkgAttr.Attribute(type="string",
                         node=self.ctrl,
                         name="ctrlDict",
                         value=tag_string,
                         lock=True)

def create_manip_ctrl(name='manip_CTRL'):
    draw_util = tkgDraw.Draw()

    # X
    manipX = draw_util.create_curve(name="manipX", shape="manip", axis="y", scale=1)
    cmds.delete([manipX+'.cv[0:17]', manipX+'.cv[19:40]', manipX+'.cv[43:44]'])
    tkgCommon.set_rgb_color(ctrl=manipX, color=[1,0,0])

    # Y
    manipY = draw_util.create_curve(name="manipY", shape="manip", axis="y", scale=1)
    cmds.delete([manipY+'.cv[19:41]', manipY+'.cv[43:62]'])
    tkgCommon.set_rgb_color(ctrl=manipY, color=[0,1,0])

    tkgCommon.merge_curves([manipX, manipY])

    # Z
    manipZ = draw_util.create_curve(name="manipZ", shape="manip", axis="y", scale=1)
    cmds.delete([manipZ+'.cv[0:17]', manipZ+'.cv[37:41]', manipZ+'.cv[43:62]'])
    tkgCommon.set_rgb_color(ctrl=manipZ, color=[0,0,1])

    tkgCommon.merge_curves([manipY, manipZ])

    cmds.rename(manipZ, name)

    return name
