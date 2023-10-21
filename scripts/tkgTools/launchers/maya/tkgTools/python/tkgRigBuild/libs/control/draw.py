# -*- coding: utf-8 -*-

import maya.cmds as cmds

from imp import reload
import json
import os
import traceback

import tkgRigBuild.libs.common as tkgCommon
reload(tkgCommon)

'''
import tkgRigBuild.libs.control.draw as tkgDraw
reload(tkgDraw)

draw_util = tkgDraw.Draw()
draw_util.write_curve(control=None, name=None, force=None)
draw_util.create_curve(name="cool_name", shape="nurbsCircle3", axis="z", scale=5)
'''

SHAPE_DIR = os.path.dirname(os.path.realpath(__file__)) + "\shapes"

class Draw(object):
    def __init__(self, curve=None):
        if curve:
            self.curve = tkgCommon.get_transform(curve)
        elif len(cmds.ls(sl=True)):
            self.curve = tkgCommon.get_transform(cmds.ls(sl=True)[0])
        else:
            self.curve = None

    def write_curve(self, control=None, name=None, force=False):
        if control:
            self.curve = tkgCommon.get_transform(control)
        elif len(cmds.ls(sl=True)):
            sel = cmds.ls(sl=True)
            self.curve = tkgCommon.get_transform(sel[0])
        elif self.curve:
            pass
        else:
            cmds.error("Please define or select a curve to write out.")

        if not name:
            name = self.curve

        curve_data = self.get_curve_info(self.curve)

        json_path = "{}/{}.json".format(SHAPE_DIR, name)
        json_dump = json.dumps(curve_data, indent=4)

        if force or os.path.isfile(json_path) == False:
            json_file = open(json_path, "w")
            json_file.write(json_dump)
            json_file.close()
        else:
            cmds.error("aaa")


    def get_curve_info(self, curve=None):
        if not curve:
            curve = self.curve

        self.curve_dict = {}
        for crv in tkgCommon.get_shapes(curve):
            min_value = cmds.getAttr(crv + ".minValue")
            max_value = cmds.getAttr(crv + ".maxValue")
            spans = cmds.getAttr(crv + ".spans")
            degree = cmds.getAttr(crv + ".degree")
            form = cmds.getAttr(crv + ".form")
            cv_len = len(cmds.ls(crv + ".cv[*]", fl=True))
            cv_pose = self.get_cv_positions(curve=crv, cv_len=cv_len)

            curve_info = {"min":min_value,
                          "max":max_value,
                          "spans":spans,
                          "degree":degree,
                          "form":form,
                          "cv_len":cv_len,
                          "cv_pose":cv_pose}
            self.curve_dict[crv] = curve_info

        return self.curve_dict

    def get_cv_positions(self, curve, cv_len):
        cv_pose = []
        for i in range(cv_len):
            pos = cmds.xform("{}.cv[{}]".format(curve, i), q=True, os=True, t=True)
            cv_pose.append(pos)

        return cv_pose

    def create_curve(self, name="default", shape="circle", axis="y", scale=1):
        file_path = "{}/{}.json".format(SHAPE_DIR, shape)
        if os.path.isfile(file_path):
            try:
                json_file = open(file_path, "r")
                json_data = json_file.read()
                curve_dict = json.loads(json_data)
            except:
                print(traceback.format_exc())
        else:
            cmds.error("Shape does not exist")

        for i, shp in enumerate(curve_dict):
            info = curve_dict[shp]
            point_info = []
            for point_list in info["cv_pose"]:
                point = [p * scale for p in point_list]
                point_info.append(point)
            if i == 0:
                self.curve = cmds.curve(point=point_info,
                                        degree=info["degree"],
                                        name=name)
                crv_shape = tkgCommon.get_shapes(self.curve)[0]
            else:
                child_crv = cmds.curve(point=point_info,
                                       degree=info["degree"])
                crv_shape = tkgCommon.get_shapes(child_crv)[0]
                cmds.parent(crv_shape, self.curve, s=True, r=True)
                cmds.delete(child_crv)

            if info["form"] >= 1:
                cmds.closeCurve(crv_shape, ch=False, ps=0, rpo=True)

        curve_shapes = tkgCommon.get_shapes(self.curve)
        for i, shp in enumerate(curve_shapes):
            cmds.setAttr('{}.lineWidth'.format(shp), 2)

            if i == 0:
                cmds.rename(shp, self.curve + "Shape")
            else:
                cmds.rename(shp, "{}Shape_{}".format(self.curve, i))

        if not axis == "y":
            self.set_axis(axis)


    def combine_curves(self, curve=None, shapes=None):
        if not curve:
            curve = self.curve
        cmds.makeIdentity(curve, apply=True)

        if not shapes:
            shapes = cmds.ls(sl=True)

        all_shapes = []
        for s in shapes:
            shape_list = tkgCommon.get_shapes(s)
            if shape_list:
                all_shapes += shape_list

        for s in all_shapes:
            transform = cmds.listRelatives(s, p=True)
            cmds.makeIdentity(transform, apply=True)
            if cmds.listRelatives(s, parent=True)[0] == self.curve:
                continue
            cmds.parent(s, curve, s=True, r=True)
            if not cmds.listRelatives(transform, ad=True):
                cmds.delete(transform)

    def set_axis(self, axis="y"):
        axis_dict = {"x":[0,0,-90],
                     "-x":[0,0,90],
                     "y":[0,0,0],
                     "-y":[0,0,180],
                     "z":[90,0,0],
                     "-z":[-90,0,0]}

        cmds.setAttr(self.curve + ".rotate", *axis_dict[axis])
        cmds.refresh()
        cmds.makeIdentity(self.curve, apply=True)
