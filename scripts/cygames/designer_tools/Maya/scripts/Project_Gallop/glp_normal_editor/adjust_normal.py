# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

from __future__ import division

try:
    # Maya 2022-
    from past.utils import old_div
    from importlib import reload
    from builtins import object
except Exception:
    pass

import sys
import maya.cmds as cmds

from . import utility

reload(utility)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class AdjustNormal(object):

    # ==================================================
    def __init__(self):

        self.raw_vtx_list = None
        self.raw_edge_list = None

        self.target_vtx_list = None
        self.edge_info_list = None
        self.edge_chain_list = None

        self.ready_src_type = None
        self.is_positive = False
        self.set_normal_index = 0

        self.should_keep_end_normal = False

    # ==================================================
    def set_target(self):

        self.ready_src_type = ''

        select_component_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_component_list:
            return

        self.raw_vtx_list = []
        self.raw_edge_list = []

        self.raw_vtx_list = cmds.ls(cmds.polyListComponentConversion(select_component_list, tv=True), l=True, fl=True)
        self.raw_edge_list = cmds.ls(cmds.polyListComponentConversion(select_component_list, te=True, internal=True), l=True, fl=True)

        self.edge_info_list = []
        self.target_vtx_list = []
        self.edge_chain_list = []

        # エッジ選択に変換可能
        if self.raw_edge_list:

            for edge in self.raw_edge_list:
                this_edge_info = EdgeInfo()
                this_edge_info.create_info(edge)
                self.edge_info_list.append(this_edge_info)

                for vtx in this_edge_info.vtx_list:
                    if vtx not in self.target_vtx_list:
                        self.target_vtx_list.append(vtx)

            self.edge_chain_list = self.__get_edge_chain_list(self.target_vtx_list, self.edge_info_list)

            if not self.edge_chain_list:
                cmds.warning('invalid edge selection')
                return

            self.ready_src_type = 'edge'

        # 単頂点選択
        elif self.raw_vtx_list:

            if not len(self.raw_vtx_list) == 1:
                cmds.warning('invalid vtx selection')
                return

            self.target_vtx_list = self.raw_vtx_list
            edge_around_vtx_list = cmds.ls(cmds.polyListComponentConversion(self.target_vtx_list, te=True), l=True, fl=True)

            for edge in edge_around_vtx_list:

                this_edge_info = EdgeInfo()
                this_edge_info.create_info(edge)
                this_single_edge_chain = self.__get_edge_chain_list(self.target_vtx_list, [this_edge_info])

                if not this_single_edge_chain:
                    continue

                self.edge_chain_list.extend(this_single_edge_chain)

            if not self.edge_chain_list:
                return

            self.ready_src_type = 'single_vtx'

    # ==================================================
    def __get_edge_chain_list(self, target_vtx_list, all_edge_info_list):

        result_edge_chain_list = []
        end_vtx_list = []
        mid_vtx_list = []

        for vtx in target_vtx_list:

            # この頂点をもつ選択エッジのリスト
            # 長さ1ならその頂点は端点
            edge_info_list = []

            for edge_info in all_edge_info_list:
                if edge_info.has_vtx(vtx):
                    edge_info_list.append(edge_info)

            if not edge_info_list:
                continue
            elif len(edge_info_list) == 1:
                end_vtx_list.append(vtx)
            elif len(edge_info_list) == 2:
                mid_vtx_list.append(vtx)
            elif len(edge_info_list) > 2:
                # 枝分かれしたエッジ選択がある
                return

        # 端の頂点からエッジリストを探索
        for end_vtx in end_vtx_list:
            is_used = False

            for edge_chain in result_edge_chain_list:

                if end_vtx in edge_chain.vtx_list:
                    is_used = True

                    break

            if is_used:
                continue

            this_chain = EdgeChainInfo()
            this_chain.create_info(end_vtx, all_edge_info_list)
            result_edge_chain_list.append(this_chain)

        # ループエッジがないかmid_vtxを探索
        for mid_vtx in mid_vtx_list:
            is_used = False

            for edge_chain in result_edge_chain_list:

                if mid_vtx in edge_chain.vtx_list:
                    is_used = True

                    break

            if is_used:
                continue

            this_chain = EdgeChainInfo()
            this_chain.create_info(mid_vtx, all_edge_info_list)
            result_edge_chain_list.append(this_chain)

        return result_edge_chain_list

    # ==================================================
    def adjust_normal_along_face(self):

        if self.ready_src_type == 'edge':
            self.__adjust_normal_from_edge_src()
        elif self.ready_src_type == 'single_vtx':
            self.__adjust_normal_from_single_vtx_src()

    # ==================================================
    def __adjust_normal_from_edge_src(self):

        set_normal_vtx_list = []
        set_normal_list = []

        for edge_chain in self.edge_chain_list:

            for vtx in edge_chain.vtx_list:

                if vtx not in self.target_vtx_list:
                    continue

                if self.should_keep_end_normal and not edge_chain.is_circle:
                    if vtx == edge_chain.start_vtx or vtx == edge_chain.end_vtx:
                        continue

                normal_list = []
                edge_face_info_pair_list = []
                edge_info_list = edge_chain.get_edge_info_list_from_vtx(vtx)

                for edge_info in edge_info_list:

                    face_info_list = edge_chain.get_face_info_list_from_edge_info(edge_info)

                    for face_info in face_info_list:

                        if self.is_positive and face_info.is_positive_pos_face:
                            normal_list.append(face_info.calc_normal)
                        elif not self.is_positive and not face_info.is_positive_pos_face:
                            normal_list.append(face_info.calc_normal)

                if not normal_list:
                    continue

                avarage_vector = utility.get_avarage_vector(normal_list)

                set_normal_vtx_list.append(vtx)
                set_normal_list.append(
                    utility.normalize_vector(avarage_vector))

        if self.is_positive:
            self.is_positive = False
        else:
            self.is_positive = True

        if not set_normal_vtx_list:
            return

        cmds.polyNormalPerVertex(set_normal_vtx_list, xyz=set_normal_list)

    # ==================================================
    def __adjust_normal_from_single_vtx_src(self):

        target_vtx = self.target_vtx_list[0]
        set_normal_list = []

        for edge_chain in self.edge_chain_list:

            edge_info_list = edge_chain.get_edge_info_list_from_vtx(target_vtx)
            face_info_list = edge_chain.get_face_info_list_from_edge_info(edge_info_list[0])

            for face_info in face_info_list:
                set_normal_list.append([target_vtx, face_info.calc_normal])

        if not set_normal_list:
            return

        if self.set_normal_index + 1 > len(set_normal_list):
            self.set_normal_index = 0

        cmds.polyNormalPerVertex(set_normal_list[self.set_normal_index][0], xyz=set_normal_list[self.set_normal_index][1])

        self.set_normal_index += 1


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EdgeInfo(object):

    # ==================================================
    def __init__(self):

        self.name = None
        self.vtx_list = None

        self.edge_vector = None
        self.cg_pos = None

        self.exists = False

    # ==================================================
    def create_info(self, name):

        self.exists = False

        self.name = name

        if not cmds.objExists(name):
            return

        self.vtx_list = cmds.ls(cmds.polyListComponentConversion(self.name, tv=True), l=True, fl=True)

        self.edge_vector = self.__get_edge_vector()
        self.cg_pos = self.__get_cg_pos()

        self.exists = True

    # ==================================================
    def __get_edge_vector(self):

        if not self.vtx_list:
            return

        vtx1_pos = cmds.xform(self.vtx_list[0], q=True, ws=True, t=True)
        vtx2_pos = cmds.xform(self.vtx_list[1], q=True, ws=True, t=True)

        tmp_vector = [0, 0, 0]
        tmp_vector[0] = vtx2_pos[0] - vtx1_pos[0]
        tmp_vector[1] = vtx2_pos[1] - vtx1_pos[1]
        tmp_vector[2] = vtx2_pos[2] - vtx1_pos[2]

        return utility.normalize_vector(tmp_vector)

    # ==================================================
    def __get_cg_pos(self):

        if not self.vtx_list:
            return

        vtx1_pos = cmds.xform(self.vtx_list[0], q=True, ws=True, t=True)
        vtx2_pos = cmds.xform(self.vtx_list[1], q=True, ws=True, t=True)

        cg_pos = [0, 0, 0]
        if sys.version_info.major == 2:
            cg_pos[0] = (vtx1_pos[0] + vtx2_pos[0]) / 2
            cg_pos[1] = (vtx1_pos[1] + vtx2_pos[1]) / 2
            cg_pos[2] = (vtx1_pos[2] + vtx2_pos[2]) / 2
        else:
            # for Maya 2022-
            cg_pos[0] = old_div((vtx1_pos[0] + vtx2_pos[0]), 2)
            cg_pos[1] = old_div((vtx1_pos[1] + vtx2_pos[1]), 2)
            cg_pos[2] = old_div((vtx1_pos[2] + vtx2_pos[2]), 2)

        return cg_pos

    # ==================================================
    def has_vtx(self, vtx):

        result = False

        if not self.vtx_list:
            return result

        if vtx in self.vtx_list:
            result = True

        return result

    # ==================================================
    def get_the_other_vtx(self, vtx):

        if not self.has_vtx(vtx):
            return

        if self.vtx_list[0] == vtx:
            return self.vtx_list[1]
        else:
            return self.vtx_list[0]

    # ==================================================
    def update_edge_direction(self, vtx, is_start):

        if not self.has_vtx(vtx):
            return

        if is_start:
            if self.vtx_list[0] == vtx:
                return
        else:
            if self.vtx_list[1] == vtx:
                return

        new_vtx_list = [self.vtx_list[1], self.vtx_list[0]]
        self.vtx_list = new_vtx_list
        self.edge_vector = self.__get_edge_vector()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EdgeChainInfo(object):

    # ==================================================
    def __init__(self):

        self.start_vtx = None
        self.end_vtx = None
        self.is_circle = False

        self.vtx_list = None
        self.edge_info_list = None
        self.face_info_list = None

    # ==================================================
    def create_info(self, start_vtx, all_edge_info_list):

        self.start_vtx = start_vtx
        self.vtx_list = []
        self.edge_info_list = []
        self.face_info_list = []

        for edge_info in all_edge_info_list:
            if edge_info.has_vtx(start_vtx):
                edge_info.update_edge_direction(start_vtx, True)
                self.vtx_list.append(self.start_vtx)
                self.edge_info_list.append(edge_info)
                break

        current_vtx = self.start_vtx
        current_edge_info = self.edge_info_list[0]

        if all_edge_info_list:

            while True:
                next_vtx = current_edge_info.get_the_other_vtx(current_vtx)
                next_edge_info = None

                for edge_info in all_edge_info_list:

                    if not edge_info.has_vtx(next_vtx):
                        continue

                    if edge_info.name == current_edge_info.name:
                        continue

                    next_edge_info = edge_info
                    next_edge_info.update_edge_direction(next_vtx, True)
                    break

                if not next_edge_info:
                    self.end_vtx = next_vtx
                    self.vtx_list.append(next_vtx)
                    break
                elif next_vtx in self.vtx_list:
                    self.end_vtx = next_vtx
                    self.is_circle = True
                    break

                self.vtx_list.append(next_vtx)
                self.edge_info_list.append(next_edge_info)

                current_vtx = next_vtx
                current_edge_info = next_edge_info

        for edge_info in self.edge_info_list:
            this_face_list = cmds.ls(cmds.polyListComponentConversion(edge_info.name, tf=True), l=True, fl=True)

            for face in this_face_list:
                this_face_info = FaceInfo()
                this_face_info.create_info(face, edge_info)

                if this_face_info.exists:
                    self.face_info_list.append(this_face_info)

    # ==================================================
    def get_edge_info_list_from_vtx(self, vtx):

        result_list = []

        for edge_info in self.edge_info_list:
            if edge_info.has_vtx(vtx):
                result_list.append(edge_info)

        return result_list

    # ==================================================
    def get_face_info_list_from_vtx(self, vtx):

        result_list = []

        for face_info in self.face_info_list:
            if face_info.has_vtx(vtx):
                result_list.append(face_info)

        return result_list

    # ==================================================
    def get_face_info_list_from_edge_info(self, edge_info):

        result_list = []

        for face_info in self.face_info_list:
            if face_info.target_edge_info.name == edge_info.name:
                result_list.append(face_info)

        return result_list


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FaceInfo(object):

    # ==================================================
    def __init__(self):

        self.name = None

        self.edge_list = None
        self.target_edge_info = None
        self.vtx_list = None

        self.cg_pos = None
        self.face_normal = None
        self.calc_normal = None
        self.is_positive_pos_face = True

        self.exists = False

    # ==================================================
    def create_info(self, name, edge_info):

        self.exists = False

        self.name = name

        if not cmds.objExists(name):
            return

        self.target_edge_info = edge_info
        self.face_normal = self.__get_face_normals(self.name)

        self.edge_list = cmds.ls(cmds.polyListComponentConversion(self.name, te=True), l=True, fl=True)
        self.vtx_list = cmds.ls(cmds.polyListComponentConversion(self.name, tv=True), l=True, fl=True)

        self.cg_pos = self.__get_cg_pos()

        cross_vector = utility.get_cross_vector(self.face_normal, self.target_edge_info.edge_vector)
        cross_vector = utility.normalize_vector(cross_vector)

        cg_vector = utility.get_directional_vector(self.cg_pos, self.target_edge_info.cg_pos)
        cg_vector = utility.normalize_vector(cg_vector)

        if utility.get_dot_value(cross_vector, cg_vector) >= 0:
            self.is_positive_pos_face = True
            self.calc_normal = cross_vector
        else:
            self.is_positive_pos_face = False
            self.calc_normal = [-cross_vector[0], -cross_vector[1], -cross_vector[2]]

        self.exists = True

    # ==================================================
    def __get_face_normals(self, face):
        temp_info = cmds.polyInfo(face, fn=True)[0]
        temp_info_list = temp_info.split(' ')
        return [float(temp_info_list[-3]), float(temp_info_list[-2]), float(temp_info_list[-1])]

    # ==================================================
    def __get_cg_pos(self):

        if not self.vtx_list:
            return

        sum_pos = [0, 0, 0]
        vtx_count = len(self.vtx_list)

        for vtx in self.vtx_list:
            vtx_pos = cmds.xform(vtx, q=True, ws=True, t=True)
            sum_pos[0] += vtx_pos[0]
            sum_pos[1] += vtx_pos[1]
            sum_pos[2] += vtx_pos[2]
        if sys.version_info.major == 2:
            return [sum_pos[0] / vtx_count, sum_pos[1] / vtx_count, sum_pos[2] / vtx_count]
        else:
            # for Maya 2022-
            return [old_div(sum_pos[0], vtx_count), old_div(sum_pos[1], vtx_count), old_div(sum_pos[2], vtx_count)]

    # ==================================================
    def has_edge(self, edge):

        result = False

        if not self.edge_list:
            return result

        if edge in self.edge_list:
            result = True

        return result

    # ==================================================
    def has_vtx(self, vtx):

        result = False

        if not self.vtx_list:
            return result

        if vtx in self.vtx_list:
            result = True

        return result
