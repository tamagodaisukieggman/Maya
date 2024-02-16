# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import struct
import shutil

import maya.cmds as cmds
import maya.mel as mel

from PySide2 import QtCore
from PySide2 import QtGui

import time
from ..base_common import utility as base_utility
from ..base_common import classes as base_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TextureAnimationCreator:

    # ===============================================
    def __init__(self):

        # スクリプトのパス関連
        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.target_transform_list = None
        self.fix_transform_list = None

        self.slider_start_frame = 0
        self.slider_end_frame = 0

        self.start_frame = 0
        self.end_frame = 100
        self.frame_interval = 1

        self.bound_max = None
        self.bound_min = None
        self.bound_size = None
        self.bound_offset = None
        self.bound_size_offset = 0

        self.max_bound_size = None

        self.info_list = None

        self.render_axis = 2

        self.bound_width = 0
        self.bound_height = 0
        self.camera_size = 0

        self.camera = 'cameraForTextureAnimation1'
        self.camera_shape = None

        # ------------------------------
        # Plane

        self.y_vector_index = 0
        self.z_vector_index = 0
        self.x_vector_index = 0

        self.root_group_name = 'textureAnimationRoot'
        self.root_group = None

        self.root_group_rig = None

        self.plane_y_vector = [0, -1, 0]
        self.plane_z_vector = [0, 0, 1]
        self.plane_align = [0, -1]

        self.plane_name = 'plane'

        self.plane_devide_x = 5
        self.plane_devide_y = 5

        self.plane_transform = None
        self.plane_shape = None

        self.plane_width = 0
        self.plane_height = 0

        self.plane_inner_offset = 0.1
        self.plane_x_edge_offset = 0.1
        self.plane_y_edge_offset = 0

        self.plane_joint_name_prefix = 'joint'
        self.plane_joint_list = None

        self.plane_move_name = None
        self.plane_move_root = None

        # ------------------------------
        # render path

        self.project_dir_path = None

        self.current_file_path = None
        self.current_root_dir_path = None
        self.current_scenes_dir_path = None
        self.current_sourceimages_dir_path = None
        self.render_dir_path = None
        self.render_file_name_prefix = None
        self.render_extension = '.png'

        self.temp_render_dir_path = None

        self.render_global_node = 'defaultRenderGlobals'
        self.render_resolution_node = 'defaultResolution'
        self.hardware_render_global_node = 'hardwareRenderingGlobals'

        # ------------------------------
        # Material

        self.material_name = 'mtl_textureAnimation'
        self.material = None

        self.shading_engine_name = None
        self.shading_engine = None

        self.material_file_name = None
        self.material_file = None

        self.material_p2dt_name = None
        self.material_p2dt = None

        # ------------------------------
        # Atlas

        self.atlas_file_name = 'tex_textureAnimation'
        self.atlas_file_path = None

        self.atlas_texture_width = 512
        self.atlas_texture_height = 512

        self.atlas_texture_fix_width = 0
        self.atlas_texture_fix_height = 0

        self.atlas_part_tex_width = 32
        self.atlas_part_tex_height = 64

        self.atlas_part_tex_fix_width = 0
        self.atlas_part_tex_fix_height = 0

        self.atlas_texture_multiply_value = 1

        self.atlas_current_h_index = 0
        self.atlas_current_v_index = 0

        # ------------------------------
        # Expression

        self.expression_name = None

    # ===============================================
    def create_texture(self):

        self.__check_path()

        if not self.project_dir_path:
            return

        if not self.current_file_path:
            return

        self.__check_transform()

        if not self.fix_transform_list:
            return

        self.__check_vector_index()

        if self.y_vector_index == 0 and self.z_vector_index == 0:
            return

        self.__delete_expression()

        self.__create_info_list()

        if not self.info_list:
            return

        self.__create_root_group()

        if not self.root_group:
            return

        self.__create_plane()

        self.__set_plane_uv()

        self.__offset_plane_vertex()

        self.__create_joint_for_plane()

        self.__bind_joint_to_plane()

        self.__constrain_to_move_root()

        self.__bake_to_move_root()

        self.__create_render_camera()

        self.__check_render_setting()

        self.__set_render_camera()

        self.__render_target()

        self.__create_atlas_texture()

        self.__create_material()

        self.__create_expression()

    # ===============================================
    def __check_path(self):

        if not self.root_group_name:
            return

        self.project_dir_path = cmds.workspace(q=True, fn=True)

        if not self.project_dir_path:
            return

        self.current_file_path = cmds.file(q=True, sn=True)

        if not self.current_file_path:
            return

        self.current_root_dir_path = os.path.dirname(self.current_file_path)

        if self.current_root_dir_path.find('scenes') > 0:
            self.current_root_dir_path = os.path.dirname(
                self.current_root_dir_path)

        self.current_scenes_dir_path = \
            self.current_root_dir_path + '/scenes'

        self.current_sourceimages_dir_path = \
            self.current_root_dir_path + '/sourceimages'

        self.temp_render_dir_path = \
            self.project_dir_path + '/images/tmp'

        self.render_dir_path =\
            self.current_sourceimages_dir_path + '/' + self.root_group_name

        self.atlas_file_path = \
            self.current_sourceimages_dir_path + '/' + self.atlas_file_name + '.png'

        self.render_file_name_prefix = self.root_group_name + '_'

    # ===============================================
    def __check_transform(self):

        self.fix_transform_list = []

        if not self.target_transform_list:
            return

        for target_transform in self.target_transform_list:

            if not cmds.objExists(target_transform):
                return

            if cmds.objectType(target_transform) != 'transform':
                continue

            self.fix_transform_list.append(target_transform)

    # ===============================================
    def __check_vector_index(self):

        self.y_vector_index = 0
        self.z_vector_index = 0
        self.x_vector_index = 0

        for p in range(3):

            if self.plane_y_vector[p] == 0:
                continue

            self.y_vector_index = p

            break

        for p in range(3):

            if self.plane_z_vector[p] == 0:
                continue

            self.z_vector_index = p

            break

        if self.y_vector_index == 0 and self.z_vector_index == 0:
            return

        if (self.y_vector_index == 0 and self.z_vector_index == 1) or \
                (self.y_vector_index == 1 and self.z_vector_index == 0):
            self.x_vector_index = 2

        elif (self.y_vector_index == 2 and self.z_vector_index == 0) or \
                (self.y_vector_index == 0 and self.z_vector_index == 2):
            self.x_vector_index = 1

        elif (self.y_vector_index == 1 and self.z_vector_index == 2) or \
                (self.y_vector_index == 2 and self.z_vector_index == 1):
            self.x_vector_index = 0

    # ===============================================
    def __create_info_list(self):

        self.info_list = []

        self.bound_max = [-100000] * 3
        self.bound_min = [100000] * 3
        self.max_bound_size = [-100000] * 3

        self.slider_start_frame = int(cmds.playbackOptions(q=True, min=True))
        self.slider_end_frame = int(cmds.playbackOptions(q=True, max=True))

        cmds.currentTime(self.slider_start_frame)

        for frame in range(self.slider_start_frame, self.slider_end_frame):

            cmds.currentTime(frame)

            if frame < self.start_frame:
                continue

            if frame > self.end_frame:
                break

            this_info = TextureAnimationInfo(self, self.fix_transform_list)

            this_info.index = len(self.info_list)
            this_info.frame = frame

            this_info.create()

            self.info_list.append(this_info)

            for p in range(3):

                if this_info.bound_max[p] > self.bound_max[p]:
                    self.bound_max[p] = this_info.bound_max[p]

                if this_info.bound_min[p] < self.bound_min[p]:
                    self.bound_min[p] = this_info.bound_min[p]

                if this_info.bound_size[p] > self.max_bound_size[p]:
                    self.max_bound_size[p] = this_info.bound_size[p]

        self.bound_size = [0] * 3
        self.bound_offset = [0] * 3

        for p in range(3):
            self.bound_size[p] = abs(self.bound_max[p] - self.bound_min[p])
            self.bound_offset[p] = \
                (self.bound_max[p] + self.bound_min[p]) * 0.5

    # ===============================================
    def __create_root_group(self):

        self.root_group = None
        self.root_info_group = None

        if not self.root_group_name:
            return

        self.root_group = self.root_group_name
        self.root_info_group = self.root_group + '_info'

        # ------------------------------

        if cmds.objExists(self.root_group):
            cmds.delete(self.root_group)

        if cmds.objExists(self.root_info_group):
            cmds.delete(self.root_info_group)

        cmds.group(name=self.root_group, em=True)
        self.root_group = '|' + self.root_group

        cmds.group(name=self.root_info_group, em=True)
        self.root_info_group = '|' + self.root_info_group

    # ===============================================
    def __create_plane(self):

        # ------------------------------

        self.plane_move_name = 'move_info'

        cmds.spaceLocator(name=self.plane_move_name)

        cmds.parent('|' + self.plane_move_name, self.root_info_group)

        self.plane_move_root = \
            self.root_info_group + '|' + self.plane_move_name

        # ------------------------------

        plane_axis = [0, 0, 0]
        plane_offset = [0, 0, 0]

        plane_offset[self.y_vector_index] = \
            -self.plane_y_vector[self.y_vector_index] * \
            self.max_bound_size[self.y_vector_index] * 0.5

        # ------------------------------

        cmds.polyPlane(
            name=self.plane_name,
            w=self.max_bound_size[self.x_vector_index],
            h=self.max_bound_size[self.y_vector_index],
            sx=int(self.plane_devide_x),
            sy=int(self.plane_devide_y),
            ax=self.plane_z_vector, cuv=1,
            ch=True
        )

        cmds.parent('|' + self.plane_name, self.root_group)

        self.plane_transform = self.root_group + '|' + self.plane_name

        self.plane_shape = cmds.listRelatives(
            self.plane_transform, shapes=True, f=True)[0]

        cmds.xform(self.plane_transform, ws=True, translation=plane_offset)

        cmds.setAttr(self.plane_shape + '.castsShadows', 0)
        cmds.setAttr(self.plane_shape + '.receiveShadows', 0)
        cmds.setAttr(self.plane_shape + '.primaryVisibility', 0)
        cmds.setAttr(self.plane_shape + '.visibleInReflections', 0)
        cmds.setAttr(self.plane_shape + '.visibleInRefractions', 0)

        cmds.makeIdentity(self.plane_transform,
                          t=True, r=True, s=True, n=True, pn=True, apply=True)

        cmds.makeIdentity(self.plane_transform,
                          t=True, r=True, s=True, n=True, pn=True, apply=False)

    # ===============================================
    def __set_plane_uv(self):

        plane_uv_list = cmds.polyListComponentConversion(
            self.plane_transform, toUV=True)

        if not plane_uv_list:
            return

        scale_u = self.atlas_part_tex_width / self.atlas_texture_width
        scale_v = self.atlas_part_tex_height / self.atlas_texture_height

        cmds.polyEditUV(plane_uv_list, pu=0, pv=1, su=scale_u, sv=scale_v)

    # ===============================================
    def __offset_plane_vertex(self):

        vertex_list = cmds.polyListComponentConversion(
            self.plane_transform, tv=True)

        if not vertex_list:
            return

        vertex_list = cmds.ls(vertex_list, l=True, fl=True)

        for vertex in vertex_list:

            this_position = cmds.xform(
                vertex, q=True, ws=True, translation=True)

            this_x_edge_diff = abs(
                abs(this_position[self.y_vector_index] - self.max_bound_size[self.y_vector_index] * 0.5) -
                self.max_bound_size[self.y_vector_index] * 0.5)

            this_y_edge_diff = abs(
                abs(this_position[self.x_vector_index]) -
                self.max_bound_size[self.x_vector_index] * 0.5)

            if this_x_edge_diff > 0.001 and \
                    this_y_edge_diff < 0.001:

                this_position[self.z_vector_index] += \
                    self.plane_y_edge_offset

            elif this_x_edge_diff < 0.001 and \
                    this_y_edge_diff > 0.001:

                this_position[self.z_vector_index] += \
                    self.plane_x_edge_offset

            elif this_x_edge_diff > 0.001 and \
                    this_y_edge_diff > 0.001:

                this_position[self.z_vector_index] += \
                    self.plane_inner_offset

            cmds.xform(
                vertex, ws=True, translation=this_position)

        cmds.delete(self.plane_transform, ch=True)

    # ===============================================
    def __create_joint_for_plane(self):

        self.plane_joint_list = []

        cmds.select(cl=True)

        for p in range(self.plane_devide_y + 1):

            this_offset = \
                self.max_bound_size[self.y_vector_index] / \
                self.plane_devide_y * p

            if self.plane_y_vector[self.y_vector_index] > 0:
                this_offset *= -1

            joint_position = [0, 0, 0]

            joint_position[self.y_vector_index] = this_offset

            this_joint = cmds.joint(p=joint_position, rad=0.1,
                                    name='temp_joint_000000')

            this_joint = cmds.parent(this_joint, self.root_group)[0]

            this_joint_name = \
                self.plane_joint_name_prefix + '{0:03d}'.format(p)

            this_joint = cmds.rename(this_joint, this_joint_name)
            this_joint = cmds.ls(this_joint, l=True)[0]

            if len(self.plane_joint_list) > 0:
                this_joint = cmds.parent(this_joint, self.plane_joint_list[-1])
                this_joint = cmds.ls(this_joint, l=True)[0]

            self.plane_joint_list.append(this_joint)

    # ===============================================
    def __bind_joint_to_plane(self):

        this_skincluster = \
            cmds.skinCluster(self.plane_joint_list[0],
                             self.plane_transform,
                             dropoffRate=4,
                             normalizeWeights=True,
                             weightDistribution=0,
                             obeyMaxInfluences=True,
                             removeUnusedInfluence=False,
                             bindMethod=0
                             )[0]

        vertex_list = cmds.polyListComponentConversion(
            self.plane_transform, tv=True)

        if not vertex_list:
            return

        vertex_list = cmds.ls(vertex_list, l=True, fl=True)

        for vertex in vertex_list:

            this_vtx_position = cmds.xform(
                vertex, q=True, ws=True, translation=True)

            target_joint_index = -1

            count = -1
            for joint in self.plane_joint_list:
                count += 1

                this_joint_position = cmds.xform(
                    joint, q=True, ws=True, translation=True)

                if abs(this_vtx_position[self.y_vector_index] - this_joint_position[self.y_vector_index]) < 0.001:
                    target_joint_index = count
                    break

            if target_joint_index < 0:
                continue

            target_joint0 = self.plane_joint_list[target_joint_index]
            target_joint1 = self.plane_joint_list[target_joint_index - 1]

            if target_joint_index > 0:
                cmds.skinPercent(this_skincluster, vertex,
                                 transformValue=[
                                     [target_joint0, 0.5], [target_joint1, 0.5]]
                                 )
            else:
                cmds.skinPercent(this_skincluster, vertex,
                                 transformValue=[[target_joint0, 1]]
                                 )

    # ===============================================
    def __constrain_to_move_root(self):

        if self.plane_joint_list:
            cmds.parentConstraint(
                self.plane_move_root, self.plane_joint_list[0])
        else:
            cmds.parentConstraint(
                self.plane_move_root, self.plane_transform)

    # ===============================================
    def __bake_to_move_root(self):

        info_pair_list = []

        count = -1
        for info in self.info_list:
            count += 1

            prev_info = None
            if count > 0:
                prev_info = self.info_list[count - 1]

            pair_exists = False

            if info.bound_size[0] != 0 and info.bound_size[1] != 0 and info.bound_size[2] != 0:
                info_pair_list.append([info, info])
                pair_exists = True
                continue

            if pair_exists:
                continue

            if prev_info:

                for info_pair in info_pair_list:

                    if prev_info != info_pair[0]:
                        continue

                    info_pair_list.append([info, info_pair[1]])

                    pair_exists = True

                    break

            if pair_exists:
                continue

            for this_info in self.info_list:

                if info.bound_size[0] == 0 and info.bound_size[1] == 0 and info.bound_size[2] == 0:
                    continue

                info_pair_list.append([info, this_info])
                pair_exists = True
                break

            if pair_exists:
                continue

        for info_pair in info_pair_list:

            src_info = info_pair[0]
            dst_info = info_pair[1]

            fix_position = [0] * 3
            fix_position[0] = dst_info.bound_offset[0]
            fix_position[1] = dst_info.bound_offset[1]
            fix_position[2] = dst_info.bound_offset[2]

            fix_position[self.x_vector_index] += \
                - self.plane_align[0] * \
                self.max_bound_size[self.x_vector_index] * 0.5\
                + self.plane_align[0] * \
                dst_info.bound_size[self.x_vector_index] * 0.5

            fix_position[self.y_vector_index] += \
                self.plane_y_vector[self.y_vector_index] * \
                self.max_bound_size[self.y_vector_index] * 0.5\
                - self.plane_align[1] * \
                self.max_bound_size[self.y_vector_index] * 0.5\
                + self.plane_align[1] * \
                dst_info.bound_size[self.y_vector_index] * 0.5

            print(fix_position)

            base_utility.attribute.set_key(
                self.plane_move_root, 'translate', fix_position, src_info.frame)

    # ===============================================
    def __create_render_camera(self):

        if cmds.objExists(self.camera):
            cmds.delete(self.camera)

        camera_info = cmds.camera(name=self.camera)

        self.camera_shape = camera_info[1]

        cmds.setAttr(self.camera_shape + '.orthographic', 1)
        cmds.setAttr(self.camera_shape + '.nearClipPlane', 0.1)
        cmds.setAttr(self.camera_shape + '.farClipPlane', 100000)

        cmds.setAttr(self.camera_shape + '.filmFit', 0)

        camera_offset = self.plane_z_vector[self.z_vector_index] * \
            self.bound_size[self.z_vector_index]

        if self.z_vector_index == 0:
            cmds.setAttr(self.camera + '.translateX', camera_offset)

        elif self.z_vector_index == 1:
            cmds.setAttr(self.camera + '.translateY', camera_offset)

        elif self.z_vector_index == 2:
            cmds.setAttr(self.camera + '.translateZ', camera_offset)

        self.camera_size = max(
            self.max_bound_size[self.x_vector_index],
            self.max_bound_size[self.y_vector_index])

        cmds.setAttr(
            '{0}.orthographicWidth'.format(
                self.camera_shape), self.camera_size)

    # ===============================================
    def __check_render_setting(self):

        self.camera_size = max(
            self.max_bound_size[self.x_vector_index],
            self.max_bound_size[self.y_vector_index])

        cmds.setAttr('{0}.width'.format(
            self.render_resolution_node),
            self.max_bound_size[self.x_vector_index] * 100)
        cmds.setAttr('{0}.height'.format(
            self.render_resolution_node),
            self.max_bound_size[self.y_vector_index] * 100)

        cmds.setAttr('{0}.deviceAspectRatio'.format(
            self.render_resolution_node),
            self.max_bound_size[self.x_vector_index] /
            self.max_bound_size[self.y_vector_index]
        )

        base_utility.attribute.set_value(
            self.render_global_node, 'imageFormat', 32
        )

    # ==================================================
    def __set_render_camera(self):

        camera_list = cmds.ls(l=True, typ='camera')

        if not camera_list:
            return

        for camera in camera_list:

            base_utility.attribute.set_value(
                camera, 'renderable', 0
            )

        base_utility.attribute.set_value(
            self.camera_shape, 'renderable',  1
        )

    # ===============================================
    def __render_target(self):

        self.slider_start_frame = int(cmds.playbackOptions(q=True, min=True))
        self.slider_end_frame = int(cmds.playbackOptions(q=True, max=True))

        cmds.currentTime(self.slider_start_frame)

        for frame in range(self.slider_start_frame, self.slider_end_frame):

            cmds.currentTime(frame)

            for info in self.info_list:

                if info.frame != frame:
                    continue

                info.render_target()

                break

        if cmds.objExists(self.camera):
            cmds.delete(self.camera)

    # ===============================================
    def __create_atlas_texture(self):

        self.atlas_current_h_index = 0
        self.atlas_current_v_index = 0

        self.atlas_texture_fix_width = \
            int(self.atlas_texture_width * self.atlas_texture_multiply_value)

        self.atlas_texture_fix_height = \
            int(self.atlas_texture_height * self.atlas_texture_multiply_value)

        self.atlas_part_tex_fix_width = \
            int(self.atlas_part_tex_width * self.atlas_texture_multiply_value)

        self.atlas_part_tex_fix_height = \
            int(self.atlas_part_tex_height * self.atlas_texture_multiply_value)

        qt_img = QtGui.QImage(
            self.atlas_texture_fix_width,
            self.atlas_texture_fix_height,
            QtGui.QImage.Format_ARGB32)

        fill_color = QtGui.qRgba(0.5, 0.5, 0.5, 0)

        for p in range(self.atlas_texture_fix_width):
            for q in range(self.atlas_texture_fix_height):
                qt_img.setPixel(p, q, fill_color)

        for info in self.info_list:

            info.create_atlas_texture(qt_img)

        if not os.path.isdir(self.current_sourceimages_dir_path):
            os.makedirs(self.current_sourceimages_dir_path)

        qt_img.save(
            self.atlas_file_path, 'PNG')

    # ===============================================
    def __create_material(self):

        self.material = self.material_name
        self.shading_engine = self.material + 'SG'

        self.material_file = 'file_' + self.material
        self.material_p2dt = 'p2d_' + self.material

        if cmds.objExists(self.material):
            cmds.delete(self.material)

        if cmds.objExists(self.shading_engine):
            cmds.delete(self.shading_engine)

        if cmds.objExists(self.material_file):
            cmds.delete(self.material_file)

        if cmds.objExists(self.material_p2dt):
            cmds.delete(self.material_p2dt)

        cmds.shadingNode('lambert', asShader=True, name=self.material)

        cmds.sets(renderable=True, noSurfaceShader=True,
                  empty=True, name=self.shading_engine)

        cmds.connectAttr(self.material + '.outColor',
                         self.shading_engine + '.surfaceShader', f=True)

        cmds.shadingNode('file', asTexture=True,
                         isColorManaged=True, name=self.material_file)
        cmds.shadingNode('place2dTexture', asUtility=True,
                         name=self.material_p2dt)

        cmds.connectAttr(self.material_file + '.outColor',
                         self.material + '.color', f=True)

        cmds.connectAttr(self.material_file + '.outTransparency',
                         self.material + '.transparency', f=True)

        cmds.connectAttr(self.material_p2dt + '.offset',
                         self.material_file + '.offset', f=True)
        cmds.connectAttr(self.material_p2dt + '.repeatUV',
                         self.material_file + '.repeatUV', f=True)

        cmds.connectAttr(self.material_p2dt + '.outUV',
                         self.material_file + '.uvCoord', f=True)

        cmds.setAttr(self.material_file + '.fileTextureName',
                     self.atlas_file_path, type='string')

        cmds.sets(self.plane_transform, e=True,
                  forceElement=self.shading_engine)

    # ===============================================
    def __delete_expression(self):

        self.expression_name = 'texanim_' + self.root_group_name

        if not cmds.objExists(self.expression_name):
            return

        cmds.delete(self.expression_name)

    # ===============================================
    def __create_expression(self):

        expression_file_path = \
            self.script_dir_path + '/resource/texanim_expression.txt'

        if not os.path.isfile(expression_file_path):
            return

        if not self.material:
            return

        if not self.material_p2dt:
            return

        # ------------------------------

        expression_info_uuid = cmds.ls(self.root_info_group, uuid=True)[0]

        p2dId = cmds.ls(self.material_p2dt, uuid=True)[0]

        base_utility.attribute.add(
            self.root_info_group, 'p2dId', p2dId
        )

        base_utility.attribute.add(
            self.root_info_group, 'startFrame', self.start_frame
        )

        base_utility.attribute.add(
            self.root_info_group, 'endFrame', self.end_frame
        )

        base_utility.attribute.add(
            self.root_info_group, 'atlasWidth', self.atlas_texture_width
        )

        base_utility.attribute.add(
            self.root_info_group, 'atlasHeight', self.atlas_texture_height
        )

        base_utility.attribute.add(
            self.root_info_group, 'atlasPartWidth', self.atlas_part_tex_width
        )

        base_utility.attribute.add(
            self.root_info_group, 'atlasPartHeight', self.atlas_part_tex_height
        )

        # ------------------------------

        self.__delete_expression()

        fopen = open(expression_file_path)
        expression_data = fopen.read()
        fopen.close()

        expression_data = \
            expression_data.replace(
                'INFO_NODE_ID', expression_info_uuid)

        cmds.expression(
            n=self.expression_name, s=expression_data)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TextureAnimationInfo:

    # ===============================================
    def __init__(self, parent, transform_list):

        self.parent = parent

        self.transform_list = transform_list

        self.index = 0

        self.frame = 0

        self.bound_max = None
        self.bound_min = None
        self.bound_size = None
        self.bound_offset = None

        self.temp_render_file_path = None
        self.render_file_path = None
        self.render_file_name = None

    # ===============================================
    def create(self):

        self.__calculate_bound()
        self.__set_path()

    # ===============================================
    def __calculate_bound(self):

        self.bound_min = [1000000] * 3
        self.bound_max = [-1000000] * 3

        for transform in self.transform_list:

            this_bounding_box = cmds.xform(
                transform, q=True, absolute=True, boundingBox=True)

            this_bound_min = this_bounding_box[0:3]
            this_bound_max = this_bounding_box[3:6]

            for p in range(3):

                if this_bound_min[p] < self.bound_min[p]:
                    self.bound_min[p] = this_bound_min[p]

                if this_bound_max[p] > self.bound_max[p]:
                    self.bound_max[p] = this_bound_max[p]

        for p in range(3):

            if self.bound_min[p] == self.bound_max[p]:
                continue

            self.bound_min[p] -= self.parent.bound_size_offset
            self.bound_max[p] += self.parent.bound_size_offset

        self.bound_size = [0] * 3
        self.bound_offset = [0] * 3

        for p in range(3):

            self.bound_size[p] = \
                abs(self.bound_max[p] - self.bound_min[p])

            self.bound_offset[p] = \
                (self.bound_max[p] + self.bound_min[p]) * 0.5

    # ===============================================
    def __set_path(self):

        self.render_file_name = \
            self.parent.render_file_name_prefix + \
            '_{0}'.format(self.frame)

        self.temp_render_file_path = \
            self.parent.temp_render_dir_path + '/' + \
            self.render_file_name + self.parent.render_extension

        self.render_file_path = \
            self.parent.render_dir_path + '/' + \
            self.render_file_name + self.parent.render_extension

    # ===============================================
    def create_texture(self, qt_image):

        for info_item in self.info_item_list:

            info_item.create_texture(qt_image)

    # ===============================================
    def render_target(self):

        self.__set_render_setting()

        cmds.currentTime(self.frame)

        this_position = self.bound_offset[:]

        this_position[self.parent.y_vector_index] += \
            - self.parent.max_bound_size[self.parent.y_vector_index]\
            * self.parent.plane_align[1] * 0.5\
            + self.bound_size[self.parent.y_vector_index]\
            * self.parent.plane_align[1] * 0.5

        this_position[self.parent.x_vector_index] += \
            - self.parent.max_bound_size[self.parent.x_vector_index]\
            * self.parent.plane_align[0] * 0.5\
            + self.bound_size[self.parent.x_vector_index]\
            * self.parent.plane_align[0] * 0.5

        cmds.setAttr(
            '{0}.translateX'.format(self.parent.camera), this_position[0])
        cmds.setAttr(
            '{0}.translateY'.format(self.parent.camera), this_position[1])
        cmds.setAttr(
            '{0}.translateZ'.format(self.parent.camera), this_position[2])

        if self.parent.render_axis == 0:

            cmds.setAttr(
                '{0}.translateX'.format(self.parent.camera), 30)

        elif self.parent.render_axis == 1:

            cmds.setAttr(
                '{0}.translateY'.format(self.parent.camera), 30)

        elif self.parent.render_axis == 2:

            cmds.setAttr(
                '{0}.translateZ'.format(self.parent.camera), 30)

        mel.eval('RenderViewWindow')

        mel_script = \
            'renderWindowRenderCamera render renderView {0};'.format(
                self.parent.camera
            )

        mel.eval(mel_script)

        self.__copy_render_image()

    # ===============================================
    def __set_render_setting(self):

        base_utility.attribute.set_value(
            self.parent.render_global_node,
            'imageFilePrefix', self.render_file_name
        )

    # ===============================================
    def __copy_render_image(self):

        if not os.path.isfile(self.temp_render_file_path):
            return

        if not os.path.isdir(self.parent.render_dir_path):
            os.makedirs(self.parent.render_dir_path)

        shutil.copy2(self.temp_render_file_path, self.render_file_path)

        if os.path.isfile(self.temp_render_file_path):
            os.remove(self.temp_render_file_path)

    # ===============================================
    def create_atlas_texture(self, target_qt_image):

        if not os.path.isfile(self.render_file_path):
            return

        this_qt_image = QtGui.QImage()

        if not this_qt_image.load(self.render_file_path):
            return

        this_qt_image = this_qt_image.scaled(
            self.parent.atlas_part_tex_fix_width,
            self.parent.atlas_part_tex_fix_height,
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )

        this_width = this_qt_image.width()
        this_height = this_qt_image.height()

        max_h_pixel = \
            self.parent.atlas_current_h_index * this_width + this_width
        max_v_pixel = \
            self.parent.atlas_current_v_index * this_height + this_height

        if max_h_pixel > self.parent.atlas_texture_fix_width:
            self.parent.atlas_current_h_index = 0
            self.parent.atlas_current_v_index += 1

        if max_v_pixel > self.parent.atlas_texture_fix_height:
            return

        for p in range(this_width):
            for q in range(this_height):

                this_h_pixel = \
                    self.parent.atlas_current_h_index * this_width + p
                this_v_pixel = \
                    self.parent.atlas_current_v_index * this_height + q

                this_color = this_qt_image.pixel(p, q)

                target_qt_image.setPixel(
                    this_h_pixel, this_v_pixel, this_color)

        self.parent.atlas_current_h_index += 1
