# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import math
import random

import maya.cmds as cmds
import maya.mel as mel

from ..base_common import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TearCreator:

    # ===============================================
    def __init__(self):

        self.particle_count = 10

        self.root_transform_name = 'tear_root'
        self.root_transform = None

        self.particle_root_name = 'tear_particle'
        self.particle_root = None

        self.particle_nucleus = None
        self.particle_shape = None
        self.particle_mesh = None

        self.controller_prefix = 'tear_ctrl_'
        self.controller_list = None

        self.sub_controller_prefix = 'tear_sub_ctrl_'
        self.sub_controller_list = None

        self.motion_path_list = None

        self.target_curve = None

        self.material_name = None

        self.frame_info_list = [

            {
                'frame': 0,
                'position': 0,
                'meshThreshold': 0.1,
                'meshBlobbyRadiusScale': 0,
                'meshTriangleSize': 0.25,
                'delay': 1,
                'delayPower': 1,
                'offset': [0, 0, 0],
                'offsetInterval': 2,
                'spread': [0, 0, 0],
            },
        ]

    # ===============================================
    def create(self):

        if not self.root_transform_name:
            return

        if not self.target_curve:
            return

        if not cmds.objExists(self.target_curve):
            return

        if not self.frame_info_list:
            return

        if len(self.frame_info_list) < 2:
            return

        self.__create_root()

        self.__create_particle()

        self.__create_controller()

        self.__convert_to_polygon()

        self.__set_particle_nucleus()

        self.__assign_curve()

        self.__set_controller_key()

        self.__assign_material()

    # ===============================================
    def __create_root(self):

        if cmds.objExists(self.root_transform_name):
            cmds.delete(self.root_transform_name)

        self.root_transform = cmds.group(
            name=self.root_transform_name, em=True)

    # ===============================================
    def __create_particle(self):

        position_list = [[0, 0, 0]] * self.particle_count

        this_particle_list = cmds.nParticle(
            name=self.particle_root_name, position=position_list)

        if not this_particle_list:
            return

        self.particle_root = this_particle_list[0]
        self.particle_nucleus = \
            cmds.listConnections(this_particle_list[1], type='nucleus')[0]

        cmds.parent(self.particle_root, self.root_transform)
        cmds.parent(self.particle_nucleus, self.root_transform)

        self.particle_root = self.root_transform + \
            '|' + self.particle_root.split('|')[-1]
        self.particle_nucleus = self.root_transform + \
            '|' + self.particle_nucleus.split('|')[-1]

    # ===============================================
    def __create_controller(self):

        self.controller_list = []
        self.sub_controller_list = []

        for p in range(self.particle_count):

            this_particle = '{0}.pt[{1}]'.format(self.particle_root, p)

            controler_info = cmds.circle(
                name='{0}{1:04d}'.format(self.controller_prefix, p))

            controler_transform = controler_info[0]

            sub_controler_info = cmds.circle(
                name='{0}{1:04d}'.format(self.sub_controller_prefix, p))

            sub_controler_transform = sub_controler_info[0]

            sub_controler_transform = cmds.parent(
                sub_controler_transform, controler_transform)[0]

            cmds.cluster(this_particle,
                         wn=[sub_controler_transform, sub_controler_transform]
                         )

            cmds.parent(controler_transform, self.root_transform)

            controler_transform = self.root_transform + \
                '|' + controler_transform.split('|')[-1]
            sub_controler_transform = controler_transform + \
                '|' + sub_controler_transform.split('|')[-1]

            self.controller_list.append(controler_transform)
            self.sub_controller_list.append(sub_controler_transform)

    # ===============================================
    def __convert_to_polygon(self):

        cmds.select(self.particle_root, r=True)

        mel.eval('particleToPoly;')

        particle_shape_list = cmds.listRelatives(
            self.particle_root, typ='nParticle')

        if not particle_shape_list:
            return

        for particle_shape in particle_shape_list:

            if particle_shape.find('Deformed') > 0:
                self.particle_shape = particle_shape
                break

        if not self.particle_shape:
            return

        shape_list = cmds.listConnections(
            self.particle_shape, type='mesh')

        if not shape_list:
            return

        cmds.parent(shape_list[0], self.root_transform)

        self.particle_mesh = self.root_transform + \
            '|' + shape_list[0].split('|')[-1]

        print(self.particle_mesh)

    # ===============================================
    def __assign_curve(self):

        self.motion_path_list = []

        self.start_frame = self.frame_info_list[0]['frame']
        self.end_frame = self.frame_info_list[-1]['frame']

        for controller in self.controller_list:

            this_motion_path = cmds.pathAnimation(
                controller, self.target_curve,
                startTimeU=self.start_frame, endTimeU=self.end_frame,
                fractionMode=True)

            self.motion_path_list.append(this_motion_path)

    # ===============================================
    def __set_controller_key(self):

        for motion_path in self.motion_path_list:
            cmds.cutKey(motion_path, attribute='uValue')

        count = -1
        for frame_info in self.frame_info_list:
            count += 1

            this_frame = frame_info['frame']
            this_position = frame_info['position']
            this_mesh_threshold = frame_info['meshThreshold']
            this_mesh_blobby_radius_scale = frame_info['meshBlobbyRadiusScale']
            this_mesh_triangle_size = frame_info['meshTriangleSize']
            this_delay = frame_info['delay']
            this_delay_power = frame_info['delayPower']
            this_offset = frame_info['offset']
            this_offset_interval = max(1, frame_info['offsetInterval'])

            this_next_frame = None
            if count < len(self.frame_info_list) - 1:
                this_next_frame = self.frame_info_list[count + 1]['frame']

            for p in range(0, len(self.controller_list)):

                this_controller = self.controller_list[p]
                this_motion_path = self.motion_path_list[p]
                this_sub_controller = self.sub_controller_list[p]

                bake_frame = \
                    this_frame + this_delay * math.pow(p, this_delay_power)

                bake_frame = max(bake_frame, this_frame)

                if this_next_frame:
                    bake_frame = min(bake_frame, this_next_frame)

                base_utility.attribute.set_key(
                    this_motion_path, 'uValue', this_position, bake_frame)

                if this_next_frame:

                    for frame in range(this_frame, this_next_frame):

                        if frame % this_offset_interval != 0:
                            continue

                        fix_offset = [0] * 3

                        for q in range(3):

                            fix_offset[q] = \
                                (random.random() * 2 - 1) * this_offset[q]

                        base_utility.attribute.set_key(
                            this_sub_controller, 'translate', fix_offset, frame
                        )

            base_utility.attribute.set_key(
                self.particle_shape, 'threshold',
                this_mesh_threshold, this_frame)

            base_utility.attribute.set_key(
                self.particle_shape, 'blobbyRadiusScale',
                this_mesh_blobby_radius_scale, this_frame)

            base_utility.attribute.set_key(
                self.particle_shape, 'meshTriangleSize',
                this_mesh_triangle_size, this_frame)

    # ===============================================
    def __set_particle_nucleus(self):

        if not self.particle_nucleus:
            return

        base_utility.attribute.set_value(
            self.particle_nucleus, 'gravity', 0)

    # ===============================================
    def __assign_material(self):

        if not self.particle_mesh:
            return

        if not self.material_name:
            return

        if not cmds.objExists(self.material_name):
            return

        base_utility.material.assign_material(
            self.material_name, [self.particle_mesh]
        )
