# -*- coding: utf-8 -*-
u"""オブジェクトを等間隔に配置した時の情報を出力する
実際にオブジェクトの等間隔配置も行える
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import random
import os
import math
import sys

import shiboken2

from PySide2 import QtWidgets
from maya import OpenMayaUI
import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.mel as mel

from . import view


class Main(object):

    def __init__(self):

        self.parent = self.__get_parent()

        # windowの重複削除処理
        self.__delete_overlapping_window([view.View()])

        self.view = view.View()

        self.place_object = ''
        self.placement_object_list = []
        self.placement_object_group = '|placement_object_group'
        self.should_placement_object = False
        self.should_not_export_json = False

        self.target_mesh_list = []
        self.should_add_random_id_to_info = False
        self.should_add_quaternion_to_info = False

        self.search_distance = 10000
        self.itervels = 500
        self.min_rand_range = 0
        self.max_rand_range = 6

    def __get_parent(self):

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return None

        if sys.version_info.major == 2:
            parent = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            parent = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)
        if parent is None:
            return None

        return parent

    def __delete_overlapping_window(self, target_list):
        """Windowの重複削除処理
        """

        if self.parent is None:
            return

        for widget in self.parent.children():
            for target in target_list:
                if type(target) == type(widget):
                    widget.deleteLater()

    def show_ui(self):

        self.setup_event()

        self.view.show()

    def setup_event(self):

        self.view.ui.set_place_target_object_button.clicked.connect(lambda: self.set_place_target_object())
        self.view.ui.clear_place_target_object_button.clicked.connect(lambda: self.clear_place_target_object())

        self.view.ui.add_place_target_mesh_list_button.clicked.connect(lambda: self.add_place_target_mesh_list())
        self.view.ui.remove_place_target_mesh_list_button.clicked.connect(lambda: self.remove_place_target_mesh_list())

        self.view.ui.exec_command_button.clicked.connect(lambda: self.exec_cmd())

    def set_place_target_object(self):

        selections = cmds.ls(sl=True, l=True, type='transform')
        if not selections:
            return

        self.view.ui.place_target_object_line.setText(selections[0])

    def clear_place_target_object(self):

        self.view.ui.place_target_object_line.clear()

    def add_place_target_mesh_list(self):

        add_obj_list = []
        for sel in cmds.ls(sl=True, l=True, type='transform'):
            if cmds.listRelatives(sel, c=True, f=True, type='mesh'):
                add_obj_list.append(sel)

        for add_obj in add_obj_list:
            for mesh_name in self.get_place_target_mesh_name_list():
                if add_obj == mesh_name:
                    break
            else:
                if add_obj == self.view.ui.place_target_object_line.text():
                    continue
                self.view.ui.place_target_mesh_list_widget.addItem(add_obj)

    def remove_place_target_mesh_list(self):

        select_items = self.view.ui.place_target_mesh_list_widget.selectedItems()
        for select_item in select_items:
            model_index = self.view.ui.place_target_mesh_list_widget.indexFromItem(select_item)
            self.view.ui.place_target_mesh_list_widget.takeItem(model_index.row())

    def get_place_target_mesh_name_list(self):

        mesh_name_list = []
        for i in range(self.view.ui.place_target_mesh_list_widget.count()):
            mesh_name_list.append(self.view.ui.place_target_mesh_list_widget.item(i).text())

        return mesh_name_list

    def exec_initialze(self):

        self.placement_object_list = []

        self.place_object = self.view.ui.place_target_object_line.text()
        self.should_placement_object = self.view.ui.place_target_object_check_box.isChecked()
        self.should_not_export_json = self.view.ui.not_export_json_check_box.isChecked()
        if self.should_placement_object and not self.place_object:
            cmds.confirmDialog(title=u'注意', message=u'配置オブジェクトが空です', messageAlign='left')
            return False

        self.target_mesh_list = self.get_place_target_mesh_name_list()
        if not self.target_mesh_list:
            cmds.confirmDialog(title=u'注意', message=u'配置対象メッシュリストが空です', messageAlign='left')
            return False

        self.should_add_random_id_to_info = self.view.ui.add_random_id_info_check_box.isChecked()
        self.should_add_quaternion_to_info = self.view.ui.add_quaternion_info_check_box.isChecked()
        self.max_rand_range = self.view.ui.random_id_range_spinbox.value()
        self.search_distance = self.view.ui.search_distance_spinbox.value()
        self.itervels = self.view.ui.place_iterverls_spinbox.value()

        return True

    def exec_cmd(self):

        if not self.exec_initialze():
            return

        target_info_dict = {'info_list': []}

        for target_mesh in self.target_mesh_list:

            # 対象となる等間隔配置を行うメッシュのMFnMeshを取得
            target_mfn_mesh = self.__get_fn_mesh_by_name(target_mesh)

            # バウンディングボックスを取得し端の座標位置取得
            bbox = om.MBoundingBox()
            for point in target_mfn_mesh.getPoints(om.MSpace.kWorld):
                bbox.expand(point)

            # バウンディングボックスの大きさが配置間隔より小さかったら処理しない
            if (bbox.max.x - bbox.min.x) < self.itervels or (bbox.max.z - bbox.min.z) < self.itervels:
                print(u'BoundingBoxがitervalより小さいため処理を中断 >>> {}'.format(target_mfn_mesh.name))
                continue

            x_distance = (bbox.max.x - (self.itervels / 2)) - (bbox.min.x + (self.itervels / 2))
            z_distance = (bbox.max.z - (self.itervels / 2)) - (bbox.min.z + (self.itervels / 2))
            x_range = int((x_distance // 100)) + 1

            gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
            cmds.progressBar(
                gMainProgressBar,
                edit=True,
                beginProgress=True,
                isInterruptable=True,
                status='"Example Calculation ...',
                maxValue=x_range)

            for i in range(int((x_distance // self.itervels)) + 1):

                if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True):
                    break

                x_pos = (bbox.min.x + (self.itervels / 2)) + (i * self.itervels)
                if x_pos > bbox.max.x - (self.itervels / 2):
                    break

                for j in range(int((z_distance // self.itervels)) + 1):

                    z_pos = (bbox.min.z + (self.itervels / 2)) + (j * self.itervels)
                    if z_pos > bbox.max.z - (self.itervels / 2):
                        break

                    pos_point = om.MFloatPoint(x_pos, -100, z_pos)

                    # 端の座標位置から順番に指定ベクトルの衝突判定を行う
                    result = target_mfn_mesh.allIntersections(
                        pos_point,  # 始点
                        om.MFloatVector(0, 1, 0),  # 方向
                        om.MSpace.kWorld,  # 座標空間
                        self.search_distance,  # 距離
                        True  # 裏の取得有無
                    )

                    if not result:
                        continue

                    hitPoints = result[0]
                    # hitRayParams = result[1]
                    hitFaces = result[2]
                    # hitTriangles = result[3]
                    # hitBary1s = result[4]
                    # hitBary2s = result[5]

                    if not hitPoints:
                        continue

                    hitFace = hitFaces[0]
                    face_normal_mvector = target_mfn_mesh.getPolygonNormal(hitFace, om.MSpace.kWorld)
                    face_quet = om.MQuaternion(om.MVector.kYaxisVector, face_normal_mvector)

                    data = {
                        'pos': [round(hitPoints[0].x, 2) * -1, math.ceil(hitPoints[0].y), round(hitPoints[0].z, 2)],
                    }
                    if self.should_add_quaternion_to_info:
                        data.update({'quaternion': [face_quet.x * -1.0, face_quet.y, face_quet.z * -1.0, face_quet.w]})  # 右手系から左手系へ変更
                    if self.should_add_random_id_to_info:
                        data.update({"group": random.randint(self.min_rand_range, self.max_rand_range)})

                    target_info_dict['info_list'].append(data)

                    if self.should_placement_object:
                        # 配置オブジェクトをまとめるグループノードが存在しなければ作成する
                        if not cmds.objExists(self.placement_object_group):
                            cmds.group(em=True, n=self.placement_object_group)
                        self.__placement_object(self.place_object, hitPoints[0], face_quet)

                cmds.progressBar(gMainProgressBar, edit=True, step=1)

            cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)

        if not target_info_dict['info_list']:
            cmds.confirmDialog(title=u'完了', message=u'配置情報が存在しないため処理終了しました', messageAlign='left')
            return

        if self.should_placement_object:
            if self.placement_object_list:
                self.__parent_placement_object_list()
            if self.should_not_export_json:
                cmds.confirmDialog(title=u'完了', message=u'オブジェクト配置が完了しました', messageAlign='left')
                return

        self.__export_json(target_info_dict)

    def __export_json(self, target_info_dict):

        # 現在開いているシーンを取得
        root_dir = ''
        file_name_without_ext = 'default_scene'
        scene_file_path = cmds.file(q=True, sn=True)
        if scene_file_path:
            file_name_without_ext = os.path.splitext(os.path.basename(scene_file_path))[0]
            open_scene_dir = os.path.dirname(scene_file_path)
            root_dir = os.path.dirname(open_scene_dir)
        # シーン取得出来なかったらデスクトップにjsonを出力
        else:
            root_dir = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop"

        json_export_full_path = os.path.join(root_dir, '{}_pos_info.json'.format(file_name_without_ext))

        confirm_title = u'エラー'
        confirm_message = u'出力できませんでした'
        with open(json_export_full_path, 'w') as f:
            json.dump(target_info_dict, f, indent=4)
            confirm_title = u'完了'
            confirm_message = u'出力が完了しました\n出力先:\n{}'.format(json_export_full_path)

        cmds.confirmDialog(title=confirm_title, message=confirm_message, messageAlign='left')

    def __placement_object(self, target_obj, pos, quat):

        dup_target_obj = cmds.duplicate(target_obj)
        dup_target_obj_name = dup_target_obj[0]

        cmds.setAttr(dup_target_obj_name + ".translate", pos.x, pos.y, pos.z)
        fn_transform = self.__get_fn_transform(dup_target_obj_name)
        fn_transform.rotateBy(quat, om.MSpace.kTransform)

        self.placement_object_list.append(dup_target_obj_name)

    def __parent_placement_object_list(self):

        cmds.parent(self.placement_object_list, self.placement_object_group)

    def __get_fn_mesh_by_name(self, target_mesh_name):

        sel_list = om.MGlobal.getSelectionListByName(target_mesh_name)
        dag_path = sel_list.getDagPath(0)
        fn_mesh = om.MFnMesh(dag_path)

        return fn_mesh

    def __get_fn_transform(self, target_name):

        selection = om.MSelectionList()
        selection.add(target_name)
        depend_node = selection.getDependNode(0)
        fn_transform = om.MFnTransform(depend_node)

        return fn_transform


if __name__ == '__main__':

    main = Main()
    main.show_ui()
