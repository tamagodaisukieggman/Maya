# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import struct
import shutil
import math

import maya.cmds as cmds
import maya.mel as mel

from PySide2 import QtCore
from PySide2 import QtGui

import time
from ..base_common import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MeshPathCreator(object):

    # ===============================================
    def __init__(self):

        self.target_vertex_list = None

        self.root_transform_name = 'meshPath'
        self.root_transform = None

        self.path_locator_name = 'pathLocator'
        self.offset_locator_name = 'offsetLocator'
        self.up_locator_name = 'upLocator'

        self.offset_curve_name = 'offsetCurve'
        self.offset_curve = None

        self.up_curve_name = 'upCurve'
        self.up_curve = None

        self.fix_vertex_list = None
        self.position_list = None

        self.path_locator_list = None
        self.offset_locator_list = None
        self.up_locator_list = None

        self.reverse_curve = True

        self.locator_size = 0.5

        self.offset_curve_offset = 0.1
        self.up_curve_offset = 1

    # ===============================================
    def create(self):

        if not self.root_transform_name:
            return

        if not self.target_vertex_list:
            return

        self.__create_fix_vertex_list()

        if not self.fix_vertex_list:
            return

        self.__create_root()

        self.__create_locator()

        self.__create_curve()

        self.__fix_data()

    # ===============================================
    def __create_fix_vertex_list(self):

        self.fix_vertex_list = []

        for vertex in self.target_vertex_list:

            if vertex.find('.vtx') < 0:
                continue

            self.fix_vertex_list.append(vertex)

        if not self.fix_vertex_list:
            return

        self.position_list = []

        for p in range(len(self.fix_vertex_list)):

            this_vertex = self.fix_vertex_list[p]

            this_position = cmds.xform(
                this_vertex, q=True, worldSpace=True, translation=True)

            self.position_list.append(this_position)

    # ===============================================
    def __create_root(self):

        self.root_transform = cmds.group(
            name=self.root_transform_name, em=True)

    # ===============================================
    def __create_locator(self):

        self.path_locator_list = []
        self.offset_locator_list = []
        self.up_locator_list = []

        for p in range(len(self.fix_vertex_list)):

            this_vertex = self.fix_vertex_list[p]
            this_position = self.position_list[p]

            this_transform = this_vertex.split('.')[0]

            this_path_locator = self.path_locator_name + '_{:0=3}'.format(p)
            this_offset_locator = self.offset_locator_name + \
                '_{:0=3}'.format(p)
            this_up_locator = self.up_locator_name + '_{:0=3}'.format(p)

            # ------------------------------

            cmds.spaceLocator(name=this_path_locator)

            cmds.parent('|' + this_path_locator, self.root_transform)

            this_path_locator = self.root_transform + '|' + this_path_locator

            cmds.setAttr(
                this_path_locator + '.translate',
                this_position[0], this_position[1], this_position[2]
            )

            cmds.normalConstraint(this_transform, this_path_locator,
                                  weight=1, aimVector=[0, 0, 1],
                                  upVector=[0, 1, 0],
                                  worldUpType='vector', worldUpVector=[0, 1, 0]
                                  )

            cmds.geometryConstraint(
                this_transform, this_path_locator, weight=1)

            # ------------------------------

            cmds.spaceLocator(name=this_offset_locator)

            cmds.parent('|' + this_offset_locator,
                        this_path_locator, relative=True)

            this_offset_locator = this_path_locator + '|' + this_offset_locator

            # ------------------------------

            cmds.spaceLocator(name=this_up_locator)

            cmds.parent('|' + this_up_locator,
                        this_offset_locator, relative=True)

            this_up_locator = this_offset_locator + '|' + this_up_locator

            # ------------------------------

            cmds.setAttr(this_path_locator + '.overrideEnabled', 1)
            cmds.setAttr(this_path_locator + '.overrideRGBColors', 1)
            cmds.setAttr(this_path_locator + '.overrideColorRGB', 1, 0.1, 0)

            cmds.setAttr(this_path_locator + '.localScale',
                         self.locator_size, self.locator_size, 0.01)

            # ------------------------------

            cmds.setAttr(this_offset_locator + '.overrideEnabled', 1)
            cmds.setAttr(this_offset_locator + '.overrideRGBColors', 1)
            cmds.setAttr(
                this_offset_locator + '.overrideColorRGB', 0.8, 0.7, 0)

            cmds.setAttr(this_offset_locator + '.scale', lock=True)

            cmds.setAttr(this_offset_locator + '.localScale',
                         self.locator_size * 0.5, self.locator_size * 0.5, self.locator_size)

            # ------------------------------

            cmds.setAttr(this_up_locator + '.overrideEnabled', 1)
            cmds.setAttr(this_up_locator + '.overrideRGBColors', 1)
            cmds.setAttr(this_up_locator + '.overrideColorRGB', 0.0, 0.7, 0.7)

            cmds.setAttr(this_up_locator + '.translateZ', self.up_curve_offset)

            cmds.setAttr(this_up_locator + '.translate', lock=True)
            cmds.setAttr(this_up_locator + '.rotate', lock=True)
            cmds.setAttr(this_up_locator + '.scale', lock=True)

            cmds.setAttr(this_up_locator + '.localScale',
                         self.locator_size * 0.1, self.locator_size * 0.1, self.locator_size * 0.1)

            # ------------------------------

            self.path_locator_list.append(this_path_locator)
            self.offset_locator_list.append(this_offset_locator)
            self.up_locator_list.append(this_up_locator)

    # ===============================================
    def __create_curve(self):

        offset_curve_position_list = []
        up_curve_position_list = []

        for p in range(len(self.fix_vertex_list)):

            this_offset_locator = self.offset_locator_list[p]
            this_up_locator = self.up_locator_list[p]

            this_offset_locator_position = cmds.xform(
                this_offset_locator, q=True, ws=True, translation=True)

            this_up_locator_position = cmds.xform(
                this_up_locator, q=True, ws=True, translation=True)

            offset_curve_position_list.append(this_offset_locator_position)
            up_curve_position_list.append(this_up_locator_position)

        # ------------------------------

        cmds.curve(d=3, p=offset_curve_position_list,
                   name=self.offset_curve_name)
        cmds.curve(d=3, p=up_curve_position_list,
                   name=self.up_curve_name)

        cmds.parent('|' + self.offset_curve_name, self.root_transform,
                    relative=True)
        self.offset_curve = self.root_transform + '|' + self.offset_curve_name

        cmds.parent('|' + self.up_curve_name, self.root_transform,
                    relative=True)
        self.up_curve = self.root_transform + '|' + self.up_curve_name

        # ------------------------------

        cmds.setAttr(self.offset_curve + '.overrideEnabled', 1)
        cmds.setAttr(self.offset_curve + '.overrideRGBColors', 1)
        cmds.setAttr(self.offset_curve + '.overrideColorRGB', 0.0, 0.0, 1.0)

        cmds.setAttr(self.up_curve + '.overrideEnabled', 1)
        cmds.setAttr(self.up_curve + '.overrideRGBColors', 1)
        cmds.setAttr(self.up_curve + '.overrideColorRGB', 0, 1.0, 1.0)

        # ------------------------------

        for p in range(len(self.fix_vertex_list)):

            this_offset_locator = self.offset_locator_list[p]
            this_up_locator = self.up_locator_list[p]

            this_offset_curve_vertex = self.offset_curve + '.cv[{0}]'.format(p)

            cmds.cluster(this_offset_curve_vertex,
                         wn=[this_offset_locator, this_offset_locator],
                         bindState=True
                         )

            this_up_curve_vertex = self.up_curve + '.cv[{0}]'.format(p)

            cmds.cluster(this_up_curve_vertex,
                         wn=[this_up_locator, this_up_locator],
                         bindState=True
                         )

    # ===============================================
    def __fix_data(self):

        if self.reverse_curve:

            cmds.reverseCurve(self.offset_curve, rpo=True, ch=False)
            cmds.reverseCurve(self.up_curve, rpo=True, ch=False)

        for p in range(len(self.fix_vertex_list)):

            this_offset_locator = self.offset_locator_list[p]

            cmds.setAttr(
                this_offset_locator + '.tz', self.offset_curve_offset
            )

        self.__smooth_curve(self.offset_curve)
        self.__smooth_curve(self.up_curve)

    # ===============================================
    def __smooth_curve(self, target_curve):

        if not target_curve:
            return

        if not cmds.objExists(target_curve):
            return

        cmds.displaySmoothness(target_curve,
                               divisionsU=3, divisionsV=3,
                               pointsWire=16, pointsShaded=4,
                               polygonObject=3)
