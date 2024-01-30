from maya import cmds, mel
import maya.api.OpenMaya as OpenMaya

import codecs
from collections import OrderedDict
import json
import math

class FacialExpressions:
    def __init__(self,
                 bs_node=None,
                 target=None,
                 tmp_joints=None,
                 forehead_center_jnt=None,
                 brow_center_jnt=None):

        self.bs_node = bs_node
        self.bs_targets = self.get_bs_targets()
        self.target = target
        self.tmp_joints = tmp_joints

        self.pre_post_joint_values = OrderedDict()
        self.pre_post_percentage = OrderedDict()
        self.pre_post_targets = OrderedDict()

        self.forehead_center_jnt = forehead_center_jnt
        self.brow_center_jnt = brow_center_jnt

    def get_pos(self, obj=None):
        if obj: return cmds.xform(obj, q=True, t=True, ws=True)

    def get_distance(self, objA=None, objB=None):
        gObjA = self.get_pos(objA)
        gObjB = self.get_pos(objB)

        return math.sqrt(math.pow(gObjA[0]-gObjB[0],2)+math.pow(gObjA[1]-gObjB[1],2)+math.pow(gObjA[2]-gObjB[2],2))

    def get_mid_point(self, pos1, pos2, percentage=0.5):
        mid_point = [pos1[0] + (pos2[0] - pos1[0]) * percentage,
                     pos1[1] + (pos2[1] - pos1[1]) * percentage,
                     pos1[2] + (pos2[2] - pos1[2]) * percentage]
        return mid_point

    def get_bs_targets(self):
        return cmds.blendShape(self.bs_node, q=True, t=True)

    def mid_point(self, objA=None, objB=None, percentage=0.5):
        pos1 = self.get_pos(objA)
        pos2 = self.get_pos(objB)
        return self.get_mid_point(pos1, pos2, percentage)

    def get_pre_post_joint_values(self):
        cmds.setAttr(self.bs_node+'.'+self.target, 0)
        for jnt in self.tmp_joints:
            self.pre_post_joint_values[jnt] = {}
            self.pre_post_joint_values[jnt]['pre'] = cmds.xform(jnt, q=True, t=True, ws=True)

        cmds.setAttr(self.bs_node+'.'+self.target, 1)
        for jnt in self.tmp_joints:
            self.pre_post_joint_values[jnt]['post'] = cmds.xform(jnt, q=True, t=True, ws=True)

        cmds.setAttr(self.bs_node+'.'+self.target, 0)

        return self.pre_post_joint_values

    def get_percentage(self, valA=None, valB=None):
        result = []
        for va, vb in zip(valA, valB):
            try:
                result.append(va/vb)
            except ZeroDivisionError:
                result.append(0.0)
        return result

    def get_percentage_from_values(self):
        self.get_pre_post_joint_values()
        self.pre_post_percentage = OrderedDict()
        for jnt, values in self.pre_post_joint_values.items():
            pre_val = values['pre']
            post_val = values['post']
            if not pre_val == post_val:
                self.pre_post_percentage[jnt] = self.get_percentage(post_val, pre_val)

    def get_joint_percentage_from_bs(self):
        self.pre_post_targets = OrderedDict()
        for bs_target in self.bs_targets:
            self.target = bs_target
            self.get_percentage_from_values()
            if self.pre_post_percentage:
                self.pre_post_targets[bs_target] = self.pre_post_percentage

def json_transfer(file_name=None, operation=None, export_values=None):
    if operation == 'export':
        try:
            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)
        except:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

    elif operation == 'import':
        try:
            with codecs.open(file_name, 'r', encoding='utf-8') as f:
                return json.load(f, 'utf-8', object_pairs_hook=OrderedDict)
        except:
            with open(file_name, 'r', encoding="utf-8") as f:
                return json.load(f, object_pairs_hook=OrderedDict)


facial_exp = FacialExpressions(
    bs_node='shapes',
    tmp_joints=cmds.ls(os=True)
)


# facial_exp.get_pre_post_joint_values()
# facial_exp.get_percentage_from_values()
facial_exp.get_joint_percentage_from_bs()

path = 'F:/myTechData/Maya/scripts/tkgTools/launchers/maya/tkgTools/python/facial/joint_percentages/facial_exp_joints.json'
json_transfer(file_name=path, operation='export', export_values=facial_exp.pre_post_targets)

for joint, value in facial_exp.pre_post_targets['jawForward'].items():
    neutral_pos = cmds.xform(joint, q=True, t=True, ws=True)
    mult_pos = [va*vb for va, vb in zip(neutral_pos, value)]
    cmds.xform(joint, t=mult_pos, ws=True, a=True)