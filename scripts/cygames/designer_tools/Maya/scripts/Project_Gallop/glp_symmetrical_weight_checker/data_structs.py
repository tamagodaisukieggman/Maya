# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import re

import maya.cmds as cmds


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class VtxData(object):

    # ===============================================
    def __init__(self):

        self.name = ''
        self.label = ''
        self.index = None
        self.pos = None
        self.joint_weight_list = []
        self.is_ready = None

    # ===============================================
    def create_data(self, vtx_long_name, all_joint_weight_info_list):

        self.is_ready = False

        suffix_match = re.search('\.vtx\[([0-9]+)\]', vtx_long_name)

        if not suffix_match:
            print('trying to create_data by not-vtx name: {}'.format(vtx_long_name))
            return

        if not cmds.objExists(vtx_long_name):
            print('not exists: {}'.format(vtx_long_name))
            return

        self.name = vtx_long_name
        self.label = vtx_long_name.split('|')[-1]
        self.index = suffix_match.group(1)
        self.pos = cmds.xform(self.name, q=True, t=True, ws=True)

        if not all_joint_weight_info_list:
            return

        for this_list in all_joint_weight_info_list:

            this_index = this_list[0]
            this_raw_joint_weight_list = this_list[1]

            if not str(this_list[0]) == str(self.index):
                continue

            this_joint_weight_list = []

            for raw_joint_weight_pair in this_raw_joint_weight_list:

                joint_long_name = raw_joint_weight_pair[0]
                weight = raw_joint_weight_pair[1]

                joint_data = JointData()
                joint_data.create_data(joint_long_name)

                if joint_data.is_ready:
                    this_joint_weight_list.append([joint_data, weight])

            self.joint_weight_list = this_joint_weight_list
            break

        self.is_ready = True


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class JointData(object):

    # ===============================================
    def __init__(self):

        self.name = ''
        self.label = ''
        self.pos = None
        self.is_ready = None

    # ===============================================
    def create_data(self, joint_long_name):

        self.is_ready = False

        self.name = joint_long_name
        self.label = self.name.split('|')[-1]

        if not cmds.objExists(self.name):
            print('not exists: {}'.format(self.name))
            return

        self.pos = cmds.xform(self.name, q=True, t=True, ws=True)

        self.is_ready = True
