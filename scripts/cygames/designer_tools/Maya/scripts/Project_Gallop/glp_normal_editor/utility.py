# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
except Exception:
    pass

import math
import itertools
import operator

import maya.cmds as cmds


# ==================================================
def get_vertex_normal_from_face(vertex):

    face_list = \
        cmds.polyListComponentConversion(vertex, tf=True)

    face_list = cmds.ls(face_list, fl=True, l=True)

    average_normal = [0] * 3
    average_count = 0

    for face in face_list:

        this_face_normal = get_face_normal(face)

        average_normal[0] += this_face_normal[0]
        average_normal[1] += this_face_normal[1]
        average_normal[2] += this_face_normal[2]

        average_count += 1

    average_normal[0] /= average_count
    average_normal[1] /= average_count
    average_normal[2] /= average_count

    return average_normal


# ==================================================
def get_vertex_normal_from_edge(vertex, target_edge_list):

    edge_list = cmds.polyListComponentConversion(vertex, te=True)

    edge_list = cmds.ls(edge_list, fl=True, l=True)
    target_edge_list = cmds.ls(target_edge_list, fl=True, l=True)
    use_edge_list = []

    for edge in edge_list:
        if edge in target_edge_list:
            use_edge_list.append(edge)

    use_face_list = cmds.polyListComponentConversion(use_edge_list, tf=True)
    use_face_list = cmds.ls(use_face_list, fl=True, l=True)

    average_normal = [0] * 3
    average_count = 0

    for face in use_face_list:

        this_face_normal = get_face_normal(face)

        average_normal[0] += this_face_normal[0]
        average_normal[1] += this_face_normal[1]
        average_normal[2] += this_face_normal[2]

        average_count += 1

    average_normal[0] /= average_count
    average_normal[1] /= average_count
    average_normal[2] /= average_count

    average_normal = normalize_vector(average_normal)

    return average_normal


# ==================================================
def get_face_normal(face):

    face_normal = [0] * 3

    face_normal_info = cmds.polyInfo(face, fn=True)[0]

    temp_split = face_normal_info[0:-2].split(' ')

    face_normal[0] = float(temp_split[-3])
    face_normal[1] = float(temp_split[-2])
    face_normal[2] = float(temp_split[-1])

    return face_normal


# ==================================================
def get_cross_vector(src_vector, dst_vector):

    cross_vector = [0] * 3

    cross_vector[0] = \
        src_vector[1] * dst_vector[2] - \
        src_vector[2] * dst_vector[1]

    cross_vector[1] = \
        src_vector[2] * dst_vector[0] - \
        src_vector[0] * dst_vector[2]

    cross_vector[2] = \
        src_vector[0] * dst_vector[1] - \
        src_vector[1] * dst_vector[0]

    cross_length = \
        cross_vector[0] * cross_vector[0] + \
        cross_vector[1] * cross_vector[1] + \
        cross_vector[2] * cross_vector[2]

    cross_vector[0] /= cross_length
    cross_vector[1] /= cross_length
    cross_vector[2] /= cross_length

    return cross_vector


# ==================================================
def get_dot_value(src_vector, dst_vector):

    dot_value = \
        src_vector[0] * dst_vector[0] + \
        src_vector[1] * dst_vector[1] + \
        src_vector[2] * dst_vector[2]

    return dot_value


# ==================================================
def get_transform_list(target_list):

    if not target_list:
        return

    transform_list = []

    for target in target_list:

        this_transform = target

        if target.find('.') > 0:
            this_transform = target.split('.')[0]

        if cmds.objectType(this_transform) != 'transform':
            continue

        if this_transform in transform_list:
            continue

        transform_list.append(this_transform)

    return transform_list


# ==================================================
def normalize_vector(vector):

    raw_length = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

    if raw_length == 0:
        return vector

    return [vector[0] / raw_length, vector[1] / raw_length, vector[2] / raw_length]


# ==================================================
def get_avarage_vector(normal_ist):

    if not normal_ist:
        return

    sum_normal = [0, 0, 0]
    count = len(normal_ist)

    for normal in normal_ist:
        sum_normal[0] += normal[0]
        sum_normal[1] += normal[1]
        sum_normal[2] += normal[2]

    return [sum_normal[0] / count, sum_normal[1] / count, sum_normal[2] / count]


# ==================================================
def get_directional_vector(pos1, pos2):

    result_vector = [0, 0, 0]

    if not pos1 or not pos2:
        return result_vector

    if not len(pos1) == 3 or not len(pos2) == 3:
        return result_vector

    result_vector[0] = pos2[0] - pos1[0]
    result_vector[1] = pos2[1] - pos1[1]
    result_vector[2] = pos2[2] - pos1[2]

    return result_vector


# ==================================================
def get_info_pair_list_by_index(src_info_list, dst_info_list):

    get_index = operator.attrgetter('index')

    all_vert_list = src_info_list + dst_info_list
    key_group_list = itertools.groupby(sorted(all_vert_list, key=get_index), key=get_index)
    group_list = (list(group) for _, group in key_group_list)
    pair_list = (pair for pair in group_list if len(pair) == 2)

    return list(zip(*pair_list))


# ==================================================
def get_info_pair_list_by_position(src_info_list, dst_info_list, is_world_space, mirror_index, mirror_normal):

    get_pos = operator.attrgetter('world_position') if is_world_space else operator.attrgetter('local_position')

    mirrored_src_info_list = [vert_info.mirror(mirror_index, mirror_normal) for vert_info in src_info_list]

    tree = get_tree(mirrored_src_info_list, get_pos)

    pair_list = []

    for dst_vert_info in dst_info_list:
        dst_pos = get_pos(dst_vert_info)
        closest_info = search_tree(tree, get_pos, dst_pos)
        pair_list.append((closest_info[0], dst_vert_info))

    return list(zip(*pair_list))


def get_tree(info_list, get_pos, depth=0):
    """
    近傍探索用kd木を作成
    """

    if not info_list:
        return None

    axis = depth % 3

    info_list.sort(key=lambda x: get_pos(x)[axis])
    index = len(info_list) // 2

    info = info_list[index]
    left = get_tree(info_list[:index], get_pos, depth + 1)
    right = get_tree(info_list[index + 1:], get_pos, depth + 1)

    return (info, left, right)


def search_tree(tree, get_pos, point, depth=0):
    """
    kd木を使用した近傍探索
    """

    if tree is None:
        return None

    axis = depth % 3

    pos = get_pos(tree[0])

    best = (tree[0], pos.distanceTo(point))

    first, second = (tree[1], tree[2]) if pos[axis] > point[axis] else (tree[2], tree[1])

    first_best = search_tree(first, get_pos, point, depth + 1)

    if first_best and first_best[1] < best[1]:
        best = first_best

    if best[1] > abs(point[axis] - pos[axis]):
        second_best = search_tree(second, get_pos, point, depth + 1)

        if second_best and second_best[1] < best[1]:
            best = second_best

    return best
