# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import os

import maya.cmds as cmds
import maya.mel as mel

from . import utility as cmn_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ExportObject(object):

    # ===============================================
    def __init__(self, main):

        self.main = main

        self.export_setting_group = '____export_setting'
        self.export_setting_current_material_attr = 'current_material'

        self.current_material_name_attr = 'lmm_current_material_name'

        self.target_transform = None
        self.export_name = None

        self.export_dir_path = None

        self.fbx_exporter = None

        self.temp_colorset = '____temp_colorset'
        self.uvset_index_list = [['lmm_lightmap', 1], ['lightmap', 2]]

        self.material_replace_name_key_list = []
        self.material_replace_name_value_list = []

        self.transform_replace_name_key_list = []
        self.transform_replace_name_value_list = []

        self.export_object_item_list = []

        self.start_frame = 0
        self.end_frame = 0
        self.anim_start_frame = 0
        self.anim_end_fram = 0

        self.is_init = False

    # ===============================================
    def initialize(self):

        self.is_init = False

        if not cmn_utility.node.Method.exist_node(self.target_transform):
            return

        if not cmn_utility.list.Method.exist_list(
                self.export_object_item_list):
            return

        if self.export_dir_path is None:

            current_scene = cmds.file(q=True, sn=True)

            if current_scene is not None:

                if current_scene != '':

                    if os.path.isfile(current_scene):

                        parent_dir_path = os.path.abspath(
                            os.path.dirname(current_scene))

                        self.export_dir_path = parent_dir_path

            else:

                project_dir_path = cmds.workspace(q=True, rootDirectory=True)
                self.export_dir_path = project_dir_path + '/scenes'

                if not os.path.isdir(self.export_dir_path):
                    self.export_dir_path = project_dir_path

        if not os.path.exists(self.export_dir_path):
            self.export_dir_path = None

        if self.export_dir_path is None:
            return

        self.fbx_exporter = cmn_utility.fbx_exporter.FbxExporter()

        self.is_init = True

    # ===============================================
    def create_export_setting(self):

        if not cmds.objExists(self.export_setting_group):
            cmds.group(name=self.export_setting_group, em=True)

        cmn_utility.attribute.Method.add_attr(
            self.export_setting_group,
            self.export_setting_current_material_attr,
            self.export_setting_current_material_attr,
            'message',
            None
        )

    # ===============================================
    def delete_export_setting(self):

        if not cmds.objExists(self.export_setting_group):
            return

        cmds.delete(name=self.export_setting_group)

    # ===============================================
    def export(self):

        self.initialize()

        if not self.is_init:
            return

        self.save_timeline_frame()
        self.save_material()

        self.delete_non_skin_transform_history()

        this_name = \
            cmn_utility.name.Method.get_short_name(self.target_transform)

        this_temp_name = this_name + '____'
        this_temp_name = cmds.rename(self.target_transform, this_temp_name)

        duplicate_transform = \
            cmds.duplicate(
                this_temp_name, rr=True, un=True, n=this_name)[0]

        cmds.select(duplicate_transform, r=True)
        cmds.select(hi=True)

        child_transform_list = cmds.ls(sl=True, l=True, typ='transform')

        for child_transform in child_transform_list:
            self.optimize_colorset(child_transform)
            self.optimize_uvset(child_transform)

        for child_transform in child_transform_list:
            self.optimize_transform(child_transform)

        self.optimize_material()

        self.export_object_item(duplicate_transform)

        cmds.delete(duplicate_transform)

        cmds.rename(this_temp_name, this_name)

        self.revert_timeline_frame()
        self.revert_material()

    # ===============================================
    def delete_non_skin_transform_history(self):

        all_transform_list = cmds.listRelatives(self.target_transform, c=True, ad=True, f=True, typ='transform')

        if not all_transform_list:
            return

        non_skin_transform_list = []

        for transform in all_transform_list:

            this_skin_cluster = self.get_skin_cluster(transform)

            if this_skin_cluster:
                continue

            non_skin_transform_list.append(transform)

        cmds.delete(non_skin_transform_list, ch=True)

    # ===============================================
    def get_skin_cluster(self, target_transform):

        shape_list = cmds.listRelatives(target_transform, shapes=True, f=True, ad=True)

        if not shape_list:
            return

        for shape in shape_list:

            skin_cluster_list = cmds.listConnections(shape, type='skinCluster')

            if not skin_cluster_list:
                continue

            return skin_cluster_list[0]

    # ===============================================
    def optimize_transform(self, target_transform):

        if not cmn_utility.node.Method.exist_transform(target_transform):
            return

        transform_name = \
            cmn_utility.name.Method.get_short_name(target_transform)

        if transform_name.find('__') <= 0:
            return

        parent_transform = None

        parent_list = cmds.listRelatives(target_transform, p=True, f=True)

        if cmn_utility.list.Method.exist_list(parent_list):
            parent_transform = parent_list[0]

        rotate_center_position = \
            cmds.xform(target_transform, q=True, ws=True, rp=True)

        scale_center_position = \
            cmds.xform(target_transform, q=True, ws=True, sp=True)

        name_split = transform_name.split('__')

        this_name = name_split[0]

        this_frag = name_split[1]
        this_frag = this_frag.lower()

        is_keep_center = True

        is_combine = False
        if this_frag.find('combine') >= 0 or this_frag.find('cmb') >= 0:
            is_combine = True

        is_freeze = False
        if this_frag.find('freeze') >= 0 or this_frag.find('frz') >= 0:
            is_freeze = True
            is_keep_center = False

        is_bbox_center = False
        if this_frag.find('boundingbox') >= 0 or this_frag.find('bbox') >= 0:
            is_bbox_center = True
            is_keep_center = False

        is_merge = False
        if this_frag.find('merge') >= 0 or this_frag.find('mrg') >= 0:
            is_merge = True

        current_transform = target_transform

        if is_combine:

            current_transform = \
                cmn_utility.mesh.Method.combine_mesh(
                    [current_transform], transform_name)

        if is_freeze:

            cmds.select(current_transform, r=True)

            cmds.makeIdentity(
                current_transform,
                apply=True, t=True, r=True, s=True, n=False, pn=True)

            cmds.makeIdentity(
                current_transform,
                apply=False, t=True, r=True, s=True)

        if is_merge:

            cmds.select(current_transform, r=True)
            cmds.polyMergeVertex(current_transform, d=0.001, ch=False, am=True)

        if is_bbox_center:

            cmds.select(current_transform, r=True)
            cmds.xform(current_transform, cpc=True)

        if current_transform != target_transform:

            if cmn_utility.node.Method.exist_node(target_transform):
                cmds.delete(target_transform)

        if parent_transform is not None:
            current_transform = \
                cmds.parent(current_transform, parent_transform)[0]

        if is_keep_center:

            cmds.xform(current_transform, ws=True, rp=rotate_center_position)
            cmds.xform(current_transform, ws=True, sp=scale_center_position)

        first_colorset = \
            cmn_utility.colorset.Method.get_colorset_from_index(
                current_transform, 0)

        cmn_utility.colorset.Method.set_current_colorset(
            current_transform, first_colorset)

        cmn_utility.uvset.Method.set_current_uvset_from_index(
            current_transform, 0)

        cmds.rename(current_transform, this_name)

    # ===============================================
    def optimize_colorset(self, target_transform):

        if not cmn_utility.node.Method.exist_transform(target_transform):
            return

        current_colorset = \
            cmn_utility.colorset.Method.get_current_colorset(target_transform)

        # カラーセットがない場合はtempカラーセットを作成
        if current_colorset is None:
            cmn_utility.colorset.Method.create_new_colorset(
                target_transform, self.temp_colorset)
            cmn_utility.colorset.Method.set_current_colorset(
                target_transform, self.temp_colorset)
            return

        # カレントカラーセット以外を削除
        colorset_list = \
            cmn_utility.colorset.Method.get_colorset_list(target_transform)

        for colorset in colorset_list:

            if current_colorset == colorset:
                continue

            cmn_utility.colorset.Method.delete_colorset(
                target_transform, colorset)

        # カレントをtempカラーセットに名前変更しカレント設定
        cmn_utility.colorset.Method.rename_colorset(
            target_transform, current_colorset, self.temp_colorset)

        cmn_utility.colorset.Method.set_current_colorset(
            target_transform, self.temp_colorset)

    # ===============================================
    def optimize_uvset(self, target_transform):

        if not cmn_utility.node.Method.exist_transform(target_transform):
            return

        for uvset_index in self.uvset_index_list:

            this_uv_name = uvset_index[0]
            this_uv_index = uvset_index[1]

            current_index = \
                cmn_utility.uvset.Method.get_uvset_index(
                    target_transform, this_uv_name)

            if current_index == this_uv_index:
                continue

            cmn_utility.uvset.Method.change_uvset_index(
                target_transform, this_uv_name, this_uv_index)

    # ===============================================
    def save_material(self):

        material_list = cmds.ls(typ='lambert', l=True)

        if not cmn_utility.list.Method.exist_list(material_list):
            return

        for material in material_list:

            self.save_material_name(material)

    # ===============================================
    def revert_material(self):

        material_list = cmds.ls(typ='lambert', l=True)

        if not cmn_utility.list.Method.exist_list(material_list):
            return

        for material in material_list:

            self.revert_material_name(material)

    # ===============================================
    def optimize_material(self):

        material_list = cmds.ls(typ='lambert', l=True)

        if not cmn_utility.list.Method.exist_list(material_list):
            return

        for material in material_list:

            self.rename_material(material)

    # ===============================================
    def save_material_name(self, target_material):

        cmn_utility.attribute.Method.add_attr(
            target_material,
            self.current_material_name_attr,
            self.current_material_name_attr,
            'string',
            target_material
        )

    # ===============================================
    def rename_material(self, target_material):

        if not cmn_utility.list.Method.exist_list(
                self.material_replace_name_key_list):
            return

        if not cmn_utility.list.Method.exist_list(
                self.material_replace_name_value_list):
            return

        if len(self.material_replace_name_key_list) != \
                len(self.material_replace_name_value_list):
            return

        for p in range(len(self.material_replace_name_key_list)):

            replace_name_key = self.material_replace_name_key_list[p]
            replace_name_value = self.material_replace_name_value_list[p]

            if target_material.find(replace_name_key) < 0:
                continue

            new_name = target_material.replace(
                replace_name_key, replace_name_value)

            try:
                cmds.rename(target_material, new_name)
            except Exception:
                pass

    # ===============================================
    def revert_material_name(self, target_material):

        prev_material_name = cmn_utility.attribute.Method.get_attr(
            target_material,
            self.current_material_name_attr,
            'string'
        )

        if prev_material_name == '':
            return

        if target_material == prev_material_name:
            return

        try:
            cmds.rename(target_material, prev_material_name)
        except Exception:
            pass

    # ==================================================
    def add_export_object_item(self, enable, name, start_frame, end_frame):

        if self.export_object_item_list is None:
            self.export_object_item_list = []

        new_export_animation = ExportObjectItem(self)

        new_export_animation.enable = enable
        new_export_animation.export_name = name
        new_export_animation.start_frame = start_frame
        new_export_animation.end_frame = end_frame

        self.export_object_item_list.append(new_export_animation)

    # ==================================================
    def export_object_item(self, target_transform):

        if self.export_object_item_list is None:
            return

        if not cmn_utility.node.Method.exist_transform(target_transform):
            return

        for export_animation in self.export_object_item_list:

            if not export_animation.enable:
                continue

            export_name = export_animation.export_name

            if export_name is None:
                export_name = self.export_name

            if export_name == '':
                export_name = self.export_name

            if export_name is None:
                continue

            if export_name == '':
                continue

            self.fbx_exporter.fbx_file_path = \
                self.export_dir_path + '/' + export_name + '.fbx'

            start_frame = export_animation.start_frame
            end_frame = export_animation.end_frame

            if start_frame < 0:
                start_frame = cmds.playbackOptions(q=True, min=True)

            if end_frame < 0:
                end_frame = cmds.playbackOptions(q=True, max=True)

            cmds.playbackOptions(ast=start_frame)
            cmds.playbackOptions(aet=end_frame)

            cmds.playbackOptions(min=start_frame)
            cmds.playbackOptions(max=end_frame)

            self.fbx_exporter.target_list = [target_transform]

            self.fbx_exporter.export()

    # ==================================================
    def save_timeline_frame(self):

        self.start_frame = cmds.playbackOptions(q=True, min=True)
        self.end_frame = cmds.playbackOptions(q=True, max=True)
        self.anim_start_frame = cmds.playbackOptions(q=True, ast=True)
        self.anim_end_frame = cmds.playbackOptions(q=True, aet=True)

    # ==================================================
    def revert_timeline_frame(self):

        cmds.playbackOptions(ast=self.anim_start_frame)
        cmds.playbackOptions(aet=self.anim_end_frame)

        cmds.playbackOptions(min=self.start_frame)
        cmds.playbackOptions(max=self.end_frame)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ExportObjectItem(object):

    # ==================================================
    def __init__(self, export_object):

        self.export_object = export_object

        self.enable = False

        self.export_name = None

        self.start_frame = -1
        self.end_frame = -1
