# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import range
except:
    pass

import maya.cmds as cmds

import maya.OpenMaya as om_old

from ... import utility as base_utility


# ==================================================
def get_skin_cluster(target_transform):
    """
    スキンクラスターを取得

    :param target_transform: 対象トランスフォーム

    :return: スキンクラスター
    """

    if not cmds.objExists(target_transform):
        return None
    if not cmds.objectType(target_transform, isType='transform'):
        return None

    skincluster = None

    for history in cmds.listHistory(target_transform):
        if cmds.objectType(history, isType='skinCluster'):
            skincluster = history
            break

    return skincluster


# ==================================================
def get_skin_root_joint(target_transform):
    """
    スキンルートジョイント取得

    :param target_transform: 対象トランスフォーム

    :return: ルートジョイント
    """

    if not cmds.objExists(target_transform):
        return

    skin_cluster = get_skin_cluster(target_transform)

    if skin_cluster is None:
        return

    if skin_cluster == '':
        return

    temp_list = cmds.listConnections(
        '{0}.matrix'.format(skin_cluster), t='joint')

    temp_list2 = cmds.listConnections(
        '{0}.influenceColor'.format(skin_cluster), t='joint')

    first_joint = None

    if temp_list:
        first_joint = temp_list[0]

    if first_joint is None:
        if temp_list2:
            first_joint = temp_list2[0]

    if first_joint is None:
        return

    if not first_joint:
        return first_joint

    long_name_list = cmds.ls(first_joint, l=True)

    if not long_name_list:
        return first_joint

    if len(long_name_list) == 1:
        return long_name_list[0]

    return long_name_list[0]


# ==================================================
def get_skin_joint_list(target_transform):
    """
    スキンに関わるジョイントリスト取得

    :param target_transform: 対象トランスフォーム

    :return: ジョイントリスト
    """

    if not cmds.objExists(target_transform):
        return

    skin_cluster = get_skin_cluster(target_transform)

    if not skin_cluster:
        return

    temp_joint_list = cmds.listConnections(
        '{0}.matrix'.format(skin_cluster), t='joint')

    if not temp_joint_list:

        temp_joint_list = cmds.listConnections(
            '{0}.influenceColor'.format(skin_cluster), t='joint')

        if not temp_joint_list:
            return

    fix_joint_list = []

    for joint in temp_joint_list:

        long_name = None

        if not joint:
            long_name = joint

        long_name_list = cmds.ls(joint, l=True)

        if not long_name_list:
            long_name = joint

        if len(long_name_list) == 1:
            long_name = long_name_list[0]

        if not long_name:
            continue

        fix_joint_list.append(long_name)

    if not fix_joint_list:
        return

    fix_joint_list = list(set(fix_joint_list))
    fix_joint_list.sort()

    return fix_joint_list


# ==================================================
def get_all_joint_weight_info_list(target_transform):
    """
    全てのウェイト値を取得

    :param target_transform: 対象トランスフォーム

    :return: [頂点番号,[[ジョイントA, Aのウェイト値], [ジョイントB, Bのウェイト値]]]の配列
    """

    skin_cluster = get_skin_cluster(target_transform)

    if skin_cluster is None:
        return

    om_weight_list = \
        base_utility.open_maya.get_om_old_weight_list(target_transform)

    if om_weight_list is None:
        return

    if om_weight_list.length() == 0:
        return

    om_skin_cluster = \
        base_utility.open_maya.get_om_old_skin_cluster(skin_cluster)

    if om_skin_cluster is None:
        return

    vertex_index_list = \
        base_utility.mesh.get_vertex_index_list(target_transform)

    om_joint_list = \
        base_utility.open_maya.get_om_old_joint_dag_path_list(
            om_skin_cluster)

    weight_list_length = om_weight_list.length()
    joint_list_length = om_joint_list.length()
    vertex_index_list_length = len(vertex_index_list)

    if weight_list_length != joint_list_length * vertex_index_list_length:
        return

    all_info_list = []

    for p in range(len(vertex_index_list)):

        this_vertex_index = vertex_index_list[p]

        this_joint_weight_list = []

        for q in range(joint_list_length):

            this_om_joint = om_joint_list[q]

            this_weight_index = joint_list_length * p + q

            this_weight = om_weight_list[this_weight_index]

            if base_utility.value.is_same(this_weight, 0, 0.001):
                continue

            this_joint_full_name = this_om_joint.fullPathName()

            this_joint_weight_list.append(
                [this_joint_full_name, this_weight])

        this_info = [
            this_vertex_index,
            this_joint_weight_list
        ]

        all_info_list.append(this_info)

    all_info_list.sort()

    return all_info_list


# ==================================================
def set_joint_weight_info_list(target_transform, joint_weight_info_list):
    """
    ウェイト値を設定

    :param target_transform: 対象トランスフォーム
    :param joint_weight_info_list: [頂点番号,[[ジョイントA, Aのウェイト値], [ジョイントB, Bのウェイト値]]]の配列
    """

    if not joint_weight_info_list:
        return

    mesh_shape = base_utility.mesh.get_mesh_shape(target_transform)

    if not mesh_shape:
        return

    skin_cluster = get_skin_cluster(target_transform)

    if not skin_cluster:
        return

    om_weight_list = \
        base_utility.open_maya.get_om_old_weight_list(target_transform)

    if not om_weight_list:
        return

    all_info_list = \
        get_all_joint_weight_info_list(target_transform)

    if not all_info_list:
        return

    om_object = \
        base_utility.open_maya.get_om_old_object(target_transform)

    om_shape_dag_path = \
        base_utility.open_maya.get_om_old_dag_path(mesh_shape)

    om_skin_cluster = \
        base_utility.open_maya.get_om_old_skin_cluster(skin_cluster)

    om_joint_list = \
        base_utility.open_maya.get_om_old_joint_dag_path_list(
            om_skin_cluster)

    om_joint_index_list = \
        base_utility.open_maya.get_om_old_joint_physical_index_list(
            om_skin_cluster)

    joint_dictionary = {}
    for p in range(om_joint_list.length()):

        this_joint_index = om_joint_index_list[p]
        this_joint = om_joint_list[p].fullPathName()

        this_joint_short_name = this_joint.split('|')[-1]

        this_joint_short_name = \
            base_utility.namespace.get_nonamespace_name(
                this_joint_short_name)

        if this_joint_short_name not in joint_dictionary:
            joint_dictionary[this_joint_short_name] = \
                [[this_joint, this_joint_index]]
            continue

        joint_dictionary[this_joint_short_name].append(
            [this_joint, this_joint_index])

    for p in range(len(joint_weight_info_list)):

        this_vertex_index = joint_weight_info_list[p][0]
        this_joint_weight_list = joint_weight_info_list[p][1]

        if this_vertex_index >= len(all_info_list):
            continue

        this_fix_weight_list = [0] * om_joint_list.length()

        for q in range(len(this_joint_weight_list)):

            this_joint = this_joint_weight_list[q][0]
            this_weight = this_joint_weight_list[q][1]

            this_joint_short_name = this_joint.split('|')[-1]

            this_joint_short_name = \
                base_utility.namespace.get_nonamespace_name(
                    this_joint_short_name)

            if this_joint_short_name not in joint_dictionary:
                continue

            this_joint_index = joint_dictionary[this_joint_short_name][0][1]

            this_fix_weight_list[this_joint_index] = this_weight

        count = -1
        for this_fix_weight in this_fix_weight_list:
            count += 1

            this_weight_list_index = \
                this_vertex_index * om_joint_list.length() + count

            om_weight_list[this_weight_list_index] = this_fix_weight

    single_id_comp = om_old.MFnSingleIndexedComponent()
    vertex_comp = single_id_comp.create(om_old.MFn.kMeshVertComponent)

    om_skin_cluster.setWeights(
        om_shape_dag_path,
        vertex_comp,
        om_joint_index_list,
        om_weight_list)


# ==================================================
def set_joint_weight_info_list_slow(
    target_transform,
    joint_weight_info_list
):
    """
    ウェイト値を設定 Undo可能

    :param target_transform: 対象トランスフォーム
    :param joint_weight_info_list: [頂点番号,[[ジョイントA, Aのウェイト値], [ジョイントB, Bのウェイト値]]]の配列
    """

    if not joint_weight_info_list:
        return

    mesh_shape = base_utility.mesh.get_mesh_shape(target_transform)

    if mesh_shape is None:
        return

    skin_cluster = get_skin_cluster(target_transform)

    if skin_cluster is None:
        return

    for joint_weight_info in joint_weight_info_list:

        this_vertex_name = '{0}.vtx[{1}]'.format(
            target_transform,
            joint_weight_info[0]
        )

        this_transform_value = []

        for joint_weight in joint_weight_info[1]:

            this_transform_value.append(
                [joint_weight[0], joint_weight[1]]
            )

        if not this_transform_value:
            continue

        try:
            cmds.skinPercent(
                skin_cluster,
                this_vertex_name,
                tv=this_transform_value
            )
        except:
            pass


# ==================================================
def paste_weight_by_vertex_index(src_skin_info, dst_skin_info):
    """
    ウェイトを頂点番号でペースト

    :param src_skin_info: コピー元SkinInfoクラス
    :param dst_skin_info: コピー先SkinInfoクラス
    """

    info_item_pair_list = __get_skin_info_item_pair_list(
        src_skin_info, dst_skin_info)

    if not info_item_pair_list:
        return

    for info_item_pair in info_item_pair_list:

        src_info_item = info_item_pair[0]
        dst_info_item = info_item_pair[1]

        vertex_index_pair_list = \
            base_utility.mesh.get_vertex_index_pair_list_by_index(
                src_info_item.target_vertex_index_list,
                dst_info_item.target_vertex_index_list
            )

        if not vertex_index_pair_list:
            continue

        __paste_weight_by_vertex_index_pair_list(
            src_info_item,
            dst_info_item,
            vertex_index_pair_list,
            False
        )


# ==================================================
def paste_weight_by_vertex_position(src_skin_info, dst_skin_info):
    """
    ウェイトを位置でペースト

    :param src_skin_info: コピー元SkinInfoクラス
    :param dst_skin_info: コピー先SkinInfoクラス
    """

    info_item_pair_list = __get_skin_info_item_pair_list(
        src_skin_info, dst_skin_info)

    if not info_item_pair_list:
        return

    for info_item_pair in info_item_pair_list:

        src_info_item = info_item_pair[0]
        dst_info_item = info_item_pair[1]

        vertex_index_pair_list = \
            base_utility.mesh.get_vertex_index_pair_list_by_position(
                src_info_item.target_vertex_index_list,
                src_info_item.world_vertex_position_info_list,
                dst_info_item.target_vertex_index_list,
                dst_info_item.world_vertex_position_info_list
            )

        if not vertex_index_pair_list:
            continue

        __paste_weight_by_vertex_index_pair_list(
            src_info_item,
            dst_info_item,
            vertex_index_pair_list,
            False
        )


# ==================================================
def paste_weight_by_uv_position(src_skin_info, dst_skin_info):
    """
    ウェイトをUV位置でペースト

    :param src_skin_info: コピー元SkinInfo
    :param dst_skin_info: コピー先SkinInfo
    """

    info_item_pair_list = __get_skin_info_item_pair_list(
        src_skin_info, dst_skin_info)

    if not info_item_pair_list:
        return

    for info_item_pair in info_item_pair_list:

        src_info_item = info_item_pair[0]
        dst_info_item = info_item_pair[1]

        vertex_index_pair_list = \
            base_utility.mesh.get_vertex_index_pair_list_by_uv_position(
                src_info_item.target_vertex_index_list,
                src_info_item.world_vertex_position_info_list,
                src_info_item.uv_info_list,
                dst_info_item.target_vertex_index_list,
                dst_info_item.world_vertex_position_info_list,
                dst_info_item.uv_info_list
            )

        if not vertex_index_pair_list:
            continue

        __paste_weight_by_vertex_index_pair_list(
            src_info_item,
            dst_info_item,
            vertex_index_pair_list,
            False
        )


# ==================================================
def __get_skin_info_item_pair_list(
        src_skin_info,
        dst_skin_info,
):

    if not src_skin_info:
        return

    if not dst_skin_info:
        return

    if not src_skin_info.info_item_list:
        return

    if not dst_skin_info.info_item_list:
        return

    check_transform_name = True
    if len(src_skin_info.info_item_list) == 1:
        if len(dst_skin_info.info_item_list) == 1:
            check_transform_name = False

    if not check_transform_name:

        src_info_item = src_skin_info.info_item_list[0]
        dst_info_item = dst_skin_info.info_item_list[0]

        return [[src_info_item, dst_info_item]]

    info_item_pair_list = []

    for src_info_item in src_skin_info.info_item_list:

        for dst_info_item in dst_skin_info.info_item_list:

            if dst_info_item.target_transform_name != \
                    src_info_item.target_transform_name:
                continue

            info_item_pair_list.append([src_info_item, dst_info_item])
            break

    if not info_item_pair_list:
        return

    return info_item_pair_list


# ==================================================
def __paste_weight_by_vertex_index_pair_list(
        src_skin_info_item,
        dst_skin_info_item,
        vertex_index_pair_list,
        is_slow
):

    if not src_skin_info_item:
        return

    if not dst_skin_info_item:
        return

    if not vertex_index_pair_list:
        return

    target_info_list = []

    for vertex_index_pair in vertex_index_pair_list:

        src_vertex_index = vertex_index_pair[0]
        dst_vertex_index = vertex_index_pair[1]

        src_joint_weight_info = \
            src_skin_info_item.joint_weight_info_list[src_vertex_index]

        src_joint_weight_list = src_joint_weight_info[1]

        dst_joint_weight_info = \
            dst_skin_info_item.joint_weight_info_list[dst_vertex_index]

        dst_joint_weight_list = dst_joint_weight_info[1]

        # ウェイトリストを修正
        fix_joint_weight_list = []
        total_weight = 0
        for src_joint_weight in src_joint_weight_list:

            this_joint = src_joint_weight[0]
            this_weight = src_joint_weight[1]

            this_joint_name = this_joint.split('|')[-1]

            this_joint_name = \
                base_utility.namespace.get_nonamespace_name(
                    this_joint_name)

            if this_joint_name not in dst_skin_info_item.joint_name_dict:
                continue

            fix_joint = dst_skin_info_item.joint_name_dict[this_joint_name][0]

            fix_joint_weight_list.append([fix_joint, this_weight])

            total_weight += this_weight

        # ウェイトを補正
        if total_weight > 0 and total_weight != 1:
            for fix_joint_weight in fix_joint_weight_list:
                fix_joint_weight[1] /= total_weight

        if fix_joint_weight_list:

            target_info_list.append(
                [dst_vertex_index, fix_joint_weight_list]
            )

        else:

            target_info_list.append(
                [dst_vertex_index, dst_joint_weight_list]
            )

    if is_slow:

        base_utility.mesh.skin.set_joint_weight_info_list_slow(
            dst_skin_info_item.target_transform,
            target_info_list
        )

        return

    base_utility.mesh.skin.set_joint_weight_info_list(
        dst_skin_info_item.target_transform,
        target_info_list
    )


# ==================================================
def get_vertex_list_with_over_influence(skin_info, influence_num):
    """
    インフルエンス数が超過してる頂点リストを取得

    :param skin_info: 対象SkinInfo
    :param influence_num: インフルエンス数

    :return :頂点リスト
    """

    if not skin_info:
        return

    if not skin_info.info_item_list:
        return

    target_vertex_list = []

    for info_item in skin_info.info_item_list:

        for joint_weight_info in info_item.joint_weight_info_list:

            this_info_list = joint_weight_info[1]

            if len(this_info_list) <= influence_num:
                continue

            this_vtx_index = joint_weight_info[0]

            this_vtx = \
                '{0}.vtx[{1}]'.format(
                    info_item.target_transform, this_vtx_index)

            target_vertex_list.append(this_vtx)

    if not target_vertex_list:
        return

    return target_vertex_list


# ==================================================
def get_vertex_list_with_unround_weight(skin_info, digit):
    """
    ウェイトが丸められていない頂点リストを取得

    :param skin_info: 対象SkinInfo
    :param digit: 桁数

    :return :頂点リスト
    """

    if not skin_info:
        return

    if not skin_info.info_item_list:
        return

    target_vertex_list = []

    for info_item in skin_info.info_item_list:

        for joint_weight_info in info_item.joint_weight_info_list:

            this_info_list = joint_weight_info[1]

            is_round = True

            for this_info in this_info_list:

                this_joint = this_info[0]
                this_weight = this_info[1]

                if base_utility.value.is_round(this_weight, digit):
                    continue

                is_round = False
                break

            if is_round:
                continue

            this_vtx_index = joint_weight_info[0]

            this_vtx = \
                '{0}.vtx[{1}]'.format(
                    info_item.target_transform, this_vtx_index)

            target_vertex_list.append(this_vtx)

    if not target_vertex_list:
        return

    return target_vertex_list


# ==================================================
def write_info_list_to_xml_element(parent_element, joint_weight_info_list):

    if parent_element is None:
        return

    if not joint_weight_info_list:
        return

    root_element = base_utility.xml.add_element(
        parent_element, 'JointWeightInfoList', None)

    for p in range(len(joint_weight_info_list)):

        this_info = joint_weight_info_list[p]
        this_vertex_index = this_info[0]
        this_weight_info_list = this_info[1]

        if not this_weight_info_list:
            continue

        this_info_element = this_info_element = base_utility.xml.add_element(
            root_element, 'JointWeightInfo', None)

        base_utility.xml.add_element(
            this_info_element, 'VertexIndex', this_vertex_index)

        for weight_info in this_weight_info_list:

            this_joint = weight_info[0]
            this_weight = weight_info[1]

            this_root_element = base_utility.xml.add_element(
                this_info_element, 'JointWeight', None)

            base_utility.xml.add_element(
                this_root_element, 'Joint', this_joint)

            base_utility.xml.add_element(
                this_root_element, 'Weight', this_weight)


# ==================================================
def read_info_list_from_xml_element(parent_element):

    if parent_element is None:
        return

    root_element = base_utility.xml.search_element(
        parent_element, 'JointWeightInfoList')

    if root_element is None:
        return

    info_element_list = base_utility.xml.search_element_list(
        root_element, 'JointWeightInfo')

    if not info_element_list:
        return

    joint_weight_info_list = []

    for info_element in info_element_list:

        index_element = base_utility.xml.search_element(
            info_element, 'VertexIndex')

        if index_element is None:
            continue

        weight_info_element_list = base_utility.xml.search_element_list(
            info_element, 'JointWeight')

        if not weight_info_element_list:
            continue

        weight_info_list = []

        for weight_info_element in weight_info_element_list:

            joint_element = base_utility.xml.search_element(
                weight_info_element, 'Joint')

            if joint_element is None:
                continue

            weight_element = base_utility.xml.search_element(
                weight_info_element, 'Weight')

            if weight_element is None:
                continue

            weight_info_list.append(
                [joint_element.text, float(weight_element.text)]
            )

        joint_weight_info_list.append(
            [
                int(index_element.text),
                weight_info_list
            ]
        )

    return joint_weight_info_list
