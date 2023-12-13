# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
except:
    pass

import re
import math

import maya.cmds as cmds


# ===============================================
def get_neck_normal_list():
    """首の法線リストを取得

    :return: 頂点を選択した順の頂点法線リスト
    """

    select_vertex_list = cmds.ls(l=True, fl=True, os=True)
    if not select_vertex_list:
        return

    normal_list = []

    for select_vertex in select_vertex_list:

        this_normal_list = \
            cmds.polyNormalPerVertex(select_vertex, q=True, xyz=True)

        if not this_normal_list:
            continue

        if len(this_normal_list) < 3:
            continue

        this_normal = [0] * 3
        this_normal[0] = this_normal_list[0]
        this_normal[1] = this_normal_list[1]
        this_normal[2] = this_normal_list[2]

        normal_list.append(this_normal)

    return normal_list


# ===============================================
def get_neck_normal_list_string():
    """首の法線リストを変数含め文字列で取得

    :return: 頂点を選択した順の頂点法線リスト文字列
    """

    normal_list = get_neck_normal_list()
    if not normal_list:
        return

    result_string = ''

    result_string = 'self.neck_normal_list = [\n'

    for normal in normal_list:

        result_string += '    ' + str(normal) + ',\n'

    result_string += ']'

    return result_string


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NeckNormalInfo(object):

    # ===============================================
    def __init__(self):

        # region 定数

        self.set_name = 'NeckEdgeSet'
        self.mob_flag_str = 'mdl_chr0001'
        self.face_flag_str = '_face'

        self.default_normal_list = [
            [0.0, -0.9999899864196777, -0.004461305215954781],
            [0.4246300458908081, -0.9050871729850769, -0.0225040465593338],
            [0.9384597539901733, -0.30013999342918396, 0.17090685665607452],
            [0.9471073746681213, -0.07069253921508789, -0.313033789396286],
            [0.5902230143547058, -0.19881224632263184, -0.7823747992515564],
            [0.0, -0.22410105168819427, -0.974565863609314],
            [-0.5902230143547058, -0.19881224632263184, -0.7823747992515564],
            [-0.9471073746681213, -0.07069253921508789, -0.313033789396286],
            [-0.9384597539901733, -0.30013999342918396, 0.17090685665607452],
            [-0.4246300458908081, -0.9050871729850769, -0.0225040465593338],
        ]

        self.outline_normal_list = [
            [0.0, -0.9999899864196777, -0.004461305215954781],
            [0.4246300458908081, -0.9050871729850769, -0.0225040465593338],
            [0.9384597539901733, -0.30013999342918396, 0.17090685665607452],
            [0.9471073746681213, -0.07069253921508789, -0.313033789396286],
            [0.5902230143547058, -0.19881224632263184, -0.7823747992515564],
            [0.0, -0.22410105168819427, -0.974565863609314],
            [-0.5902230143547058, -0.19881224632263184, -0.7823747992515564],
            [-0.9471073746681213, -0.07069253921508789, -0.313033789396286],
            [-0.9384597539901733, -0.30013999342918396, 0.17090685665607452],
            [-0.4246300458908081, -0.9050871729850769, -0.0225040465593338],
        ]

        # endregion

        # region __init_param_by_file_nameで初期化されるメンバ

        self.neck_default_normal_list = self.default_normal_list[:]
        self.neck_outline_normal_list = self.outline_normal_list[:]

        self.neck_edge_target_count = len(self.neck_default_normal_list)
        self.is_mob = False
        self.is_mob_hair = False

        # endregion

        # region その他のメンバ

        self.neck_edge_list = None
        self.neck_vertex_info_list = None

        # endregion

    # ==================================================
    def __print_log(self, msg):

        log_msg = msg.encode('shift_jis')
        print(log_msg)

    # ==================================================
    def __init_param_by_file_name(self):

        scene_name = cmds.file(q=True, sn=True)

        if not scene_name:
            return

        if scene_name.find(self.mob_flag_str) >= 0:

            if scene_name.find(self.face_flag_str) >= 0:

                self.neck_default_normal_list = [
                    self.default_normal_list[0],
                    self.default_normal_list[1],
                    self.default_normal_list[2],
                    self.default_normal_list[3],
                    self.default_normal_list[7],
                    self.default_normal_list[8],
                    self.default_normal_list[9],
                ]

                self.neck_outline_normal_list = [
                    self.outline_normal_list[0],
                    self.outline_normal_list[1],
                    self.outline_normal_list[2],
                    self.outline_normal_list[3],
                    self.outline_normal_list[7],
                    self.outline_normal_list[8],
                    self.outline_normal_list[9],
                ]

            else:
                self.neck_default_normal_list = [
                    self.default_normal_list[3],
                    self.default_normal_list[4],
                    self.default_normal_list[5],
                    self.default_normal_list[6],
                    self.default_normal_list[7],
                ]

                self.neck_outline_normal_list = [
                    self.outline_normal_list[3],
                    self.outline_normal_list[4],
                    self.outline_normal_list[5],
                    self.outline_normal_list[6],
                    self.outline_normal_list[7],
                ]

                self.is_mob_hair = True

            self.neck_edge_target_count = len(self.neck_default_normal_list) - 1
            self.is_mob = True

        else:
            self.neck_default_normal_list = self.default_normal_list[:]
            self.neck_outline_normal_list = self.outline_normal_list[:]

            self.neck_edge_target_count = len(self.neck_default_normal_list)
            self.is_mob = False

    # ==================================================
    def exist_neck_edge_set(self):

        set_list = cmds.ls(type='objectSet')
        if self.set_name not in set_list:
            return False

        return True

    # ==================================================
    def add_neck_edge_set(self):

        self.__init_param_by_file_name()

        neck_edge_list = cmds.ls(
            (cmds.polyListComponentConversion(te=True)), l=True, fl=True)

        if not neck_edge_list:
            msg_str = '何も選択されていません'
            self.__print_log(msg_str)
            return

        if len(neck_edge_list) != self.neck_edge_target_count:

            msg_str = '選択された首の頂点数が規定数と違います 規定数 : {0} 選択数 : {1}'.format(
                str(self.neck_edge_target_count), str(len(neck_edge_list))
            )
            self.__print_log(msg_str)
            return

        if cmds.objExists(self.set_name):
            msg_str = '{0}が存在します'.format(self.set_name)
            self.__print_log(msg_str)
            return

        cmds.sets(name=self.set_name)
        cmds.sets(neck_edge_list, add=self.set_name)

        self.update_neck_edge_set()

    # ==================================================
    def update_neck_edge_set(self):

        select_list = cmds.ls(sl=True)

        self.update_neck_edge_set_base()

        if not select_list:
            return

        cmds.select(select_list, r=True)

    # ==================================================
    def update_neck_edge_set_base(self):

        if not cmds.objExists(self.set_name):
            msg_str = '{0}が存在しません'.format(self.set_name)
            self.__print_log(msg_str)
            return

        cmds.select(self.set_name, r=True)

        neck_edge_list = cmds.ls(
            (cmds.polyListComponentConversion(te=True)), l=True, fl=True)

        if not neck_edge_list:
            msg_str = '何も選択されていません'
            self.__print_log(msg_str)
            return

        default_transform_list = []
        ouline_transform_list = []
        for edge in neck_edge_list:

            this_transform = edge.split('.')[0]

            if this_transform.lower().find('outline') >= 0:
                ouline_transform_list.append(this_transform)
                continue

            default_transform_list.append(this_transform)

        self.set_neck_normal_from_neck_edge_set(
            default_transform_list, False)

        self.set_neck_normal_from_neck_edge_set(
            ouline_transform_list, True)

    # ==================================================
    def select_neck_edge_set(self):

        if not cmds.objExists(self.set_name):
            msg_str = '{0}が存在しません'.format(self.set_name)
            self.__print_log(msg_str)
            return

        cmds.select(self.set_name, r=True)

    # ==================================================
    def remove_selected_edge_from_neck_edge_set(self):

        select_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_list:
            msg_str = '何も選択されていません'
            self.__print_log(msg_str)
            return

        edge_list = cmds.polyListComponentConversion(select_list, te=True)

        if not edge_list:
            msg_str = 'エッジが取得できません'
            self.__print_log(msg_str)
            return

        edge_list = cmds.ls(edge_list, l=True, fl=True)

        if not edge_list:
            return

        if not cmds.objExists(self.set_name):
            msg_str = '{0}が存在しません'.format(self.set_name)
            self.__print_log(msg_str)
            return

        cmds.sets(edge_list, rm=self.set_name)

    # ==================================================
    def remove_edge_from_neck_edge_set_by_name(self, target_name):

        if not target_name:
            return

        if not cmds.objExists(self.set_name):
            return

        edge_list_in_set = cmds.ls(cmds.sets('NeckEdgeSet', q=True), fl=True)

        remove_edge_list = []

        for edge in edge_list_in_set:
            if edge.find(target_name) >= 0:
                remove_edge_list.append(edge)

        if not remove_edge_list:
            return

        cmds.sets(remove_edge_list, rm=self.set_name)

    # ==================================================
    def delete_neck_edge_set(self):

        if cmds.objExists(self.set_name):
            cmds.delete(self.set_name)

    # ==================================================
    def set_neck_normal_from_neck_edge_set(
            self, target_transform_list, is_outline_normal, name_prefix=None, name_suffix=None):

        self.update_neck_edge_list_from_neck_edge_set(
            target_transform_list, name_prefix, name_suffix)

        if not self.neck_edge_list:
            return

        self.update_neck_vertex_info()

        if not self.neck_vertex_info_list:
            return

        self.set_vertex_normal(is_outline_normal)

    # ==================================================
    def set_neck_normal_from_selected_edge(self, is_outline_normal):

        self.neck_edge_list = []

        self.update_neck_edge_list_from_selected_edge()

        if not self.neck_edge_list:
            msg_str = 'neck_edge_listが空です'.format(self.set_name)
            self.__print_log(msg_str)
            return

        self.update_neck_vertex_info()

        if not self.neck_vertex_info_list:
            return

        self.set_vertex_normal(is_outline_normal)

    # ==================================================
    def update_neck_edge_list_from_selected_edge(self):

        self.__init_param_by_file_name()

        self.neck_edge_list = []

        this_neck_edge_list = cmds.ls(
            (cmds.polyListComponentConversion(te=True)), l=True, fl=True)

        if not this_neck_edge_list:
            msg_str = 'neck_edge_listが空です'.format(self.set_name)
            self.__print_log(msg_str)
            return

        if len(this_neck_edge_list) != self.neck_edge_target_count:
            msg_str = '選択された首の頂点数が規定数と違います 規定数 : {0} 選択数 : {1}'.format(
                str(self.neck_edge_target_count), str(len(this_neck_edge_list))
            )
            self.__print_log(msg_str)
            return

        self.neck_edge_list = this_neck_edge_list

    # ==================================================
    def update_neck_edge_list_from_neck_edge_set(self, target_transform_list, name_prefix=None, name_suffix=None):

        self.__init_param_by_file_name()

        self.neck_edge_list = []

        if not target_transform_list:
            msg_str = '対象のトランスフォームノードリストが空です'
            self.__print_log(msg_str)
            return

        if not cmds.objExists(self.set_name):
            msg_str = '{0}が存在しません'.format(self.set_name)
            self.__print_log(msg_str)
            return

        cmds.select(self.set_name, r=True)

        this_neck_edge_list = cmds.ls(sl=True, fl=True, l=True)

        if not this_neck_edge_list:
            msg_str = 'neck_edge_listが空です'.format(self.set_name)
            self.__print_log(msg_str)
            return

        this_neck_edge_fix_list = []

        for this_neck_edge in this_neck_edge_list:

            this_transform = this_neck_edge.split('.')[0]

            match_obj = re.search(r'\[(\d*)\]', this_neck_edge)
            if not match_obj:
                continue

            this_edge_index = match_obj.group(1)

            this_transform_name = this_transform.split('|')[-1]

            for target_transform in target_transform_list:

                target_transform_name = target_transform.split('|')[-1]

                if this_transform_name != target_transform_name:
                    continue

                this_neck_edge_fix = this_neck_edge

                if name_prefix is not None or name_suffix is not None:

                    fix_transform_name = this_transform_name

                    if name_prefix is not None:
                        fix_transform_name = name_prefix + fix_transform_name

                    if name_suffix is not None:
                        fix_transform_name += name_suffix

                    this_neck_edge_fix = fix_transform_name + \
                        '.e[' + str(this_edge_index) + ']'

                if not cmds.objExists(this_neck_edge_fix):
                    continue

                this_neck_edge_fix_list.append(this_neck_edge_fix)
                break

        if len(this_neck_edge_fix_list) != self.neck_edge_target_count:
            return

        self.neck_edge_list = this_neck_edge_fix_list

    # ==================================================
    def update_neck_vertex_info(self):

        self.__init_param_by_file_name()

        self.neck_vertex_info_list = []

        if not self.neck_edge_list:
            return

        cmds.select(self.neck_edge_list, r=True)

        vertices = cmds.ls(
            (cmds.polyListComponentConversion(tv=True)), l=True, fl=True)

        center_position = [0, 0, 0]
        top_position = [0, 0, 0]
        max_z_position = -100000

        for vertex in vertices:

            this_vtx_position = cmds.pointPosition(vertex, w=True)

            if this_vtx_position[2] > max_z_position:
                max_z_position = this_vtx_position[2]
                top_position = this_vtx_position

            self.neck_vertex_info_list.append(
                [0, [0, 0, 0], vertex, this_vtx_position, 0])

            center_position[0] += this_vtx_position[0]
            center_position[1] += this_vtx_position[1]
            center_position[2] += this_vtx_position[2]

        center_position[0] /= len(vertices)
        center_position[1] /= len(vertices)
        center_position[2] /= len(vertices)

        base_vector = [0, 0, 0]

        # 重心からZ最大の頂点へのベクトルを基準ベクトルとする
        # モブ髪はZ最大の頂点が特定できないので、[0, 0, 1]を基準ベクトルとする
        if self.is_mob_hair:
            base_vector = [0, 0, 1]

        else:
            base_vector[0] = top_position[0] - center_position[0]
            base_vector[1] = top_position[1] - center_position[1]
            base_vector[2] = top_position[2] - center_position[2]

            base_length = base_vector[0] * base_vector[0] + \
                base_vector[1] * base_vector[1] + \
                base_vector[2] * base_vector[2]

            base_length = math.sqrt(base_length)

            base_vector[0] /= base_length
            base_vector[1] /= base_length
            base_vector[2] /= base_length

        for vertex_info in self.neck_vertex_info_list:

            vertex_position = vertex_info[3]

            vector_from_center = [0, 0, 0]

            vector_from_center[0] = vertex_position[0] - center_position[0]
            vector_from_center[1] = vertex_position[1] - center_position[1]
            vector_from_center[2] = vertex_position[2] - center_position[2]

            length_from_center = \
                vector_from_center[0] * vector_from_center[0] + \
                vector_from_center[1] * vector_from_center[1] + \
                vector_from_center[2] * vector_from_center[2]

            length_from_center = math.sqrt(length_from_center)

            vector_from_center[0] /= length_from_center
            vector_from_center[1] /= length_from_center
            vector_from_center[2] /= length_from_center

            vertex_info[1] = vector_from_center

            this_dot_2d = base_vector[0] * vector_from_center[0] + \
                base_vector[1] * vector_from_center[1] + \
                base_vector[2] * vector_from_center[2]

            this_degree = 0

            if this_dot_2d < 1.0 - 0.001:
                this_degree = math.degrees(math.acos(this_dot_2d))

            if vector_from_center[0] < 0 and this_degree != 0:
                this_degree = 360 - this_degree

            vertex_info[0] = this_degree

        if not self.neck_edge_list:
            self.neck_vertex_info_list = []
            return

        self.neck_vertex_info_list.sort()

        current_index = -1
        prev_degree = -100000

        for p in range(len(self.neck_vertex_info_list)):

            this_info = self.neck_vertex_info_list[p]

            this_degree = this_info[0]

            this_sub = abs(this_degree - prev_degree)

            if this_sub > 0.0001:
                current_index += 1

            self.neck_vertex_info_list[p][4] = current_index

            prev_degree = this_degree

        if self.is_mob:
            target_index = self.neck_edge_target_count
        else:
            target_index = self.neck_edge_target_count - 1

        if current_index != target_index:
            self.neck_vertex_info_list = []

    # ==================================================
    def set_vertex_normal(self, is_outline_normal):

        self.__init_param_by_file_name()

        if not self.neck_vertex_info_list:
            return

        for p in range(0, len(self.neck_vertex_info_list)):

            this_info = self.neck_vertex_info_list[p]

            this_vertex = this_info[2]
            this_index = this_info[4]

            this_fix_normal = None

            if is_outline_normal:
                this_fix_normal = self.neck_outline_normal_list[this_index]
            else:
                this_fix_normal = self.neck_default_normal_list[this_index]

            cmds.polyNormalPerVertex(this_vertex, xyz=this_fix_normal)
