# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import re

import maya.cmds as cmds

from .. import utility as base_utility

try:
    from builtins import str
    from builtins import range
except Exception:
    pass

__g_all_node_dict = None
__g_all_node_dict_job_enable = False
__g_all_node_dict_update_flag = False


# ===============================================
def exists(target_node, node_type=None):
    """
    ノードが存在するかどうか

    :param target_node: 対象ノード
    :param node_type: タイプ

    :return: 存在する場合はTrue
    """

    if not target_node:
        return False

    if not cmds.objExists(target_node):
        return False

    if not node_type:
        return True

    hit_node_list = cmds.ls(target_node, typ=node_type, l=True)

    if hit_node_list:
        return True

    return False


# ===============================================
def search(
    short_node_name,
    long_name_filter=None,
    node_type=None
):
    """
    ノード検索

    :param short_node_name: 対象ノード名 正規表現
    :param long_name_filter: ロング名フィルター 正規表現
    :param node_type: タイプ
    """

    hit_node_list = \
        search_list(short_node_name, long_name_filter, node_type)

    if not hit_node_list:
        return

    return hit_node_list[0]


# ===============================================
def search_list(
    short_node_name,
    long_name_filter=None,
    node_type=None
):
    """
    ノードをリスト検索

    :param short_node_name: 対象ノード名 正規表現
    :param long_name_filter: ロング名フィルター 正規表現
    :param node_type: タイプ
    """

    global __g_all_node_dict_update_flag

    __update_all_node_dict()

    hit_node_list = \
        __search_list_base(short_node_name, long_name_filter, node_type)

    if hit_node_list:
        return hit_node_list

    __g_all_node_dict_update_flag = True

    __update_all_node_dict()

    hit_node_list = \
        __search_list_base(short_node_name, long_name_filter, node_type)

    return hit_node_list


# ===============================================
def __search_list_base(
    short_node_name,
    long_name_filter,
    node_type
):
    """
    ノードをリスト検索

    :param target_node_name: 対象ノード名 正規表現
    :param long_name_filter: ロング名フィルター 正規表現
    :param node_type: タイプ
    """

    global __g_all_node_dict_update_flag

    if not short_node_name:
        return

    __update_all_node_dict()

    if not __g_all_node_dict:
        return

    fix_short_node_name = short_node_name

    if fix_short_node_name.find(':') >= 0:
        fix_short_node_name = fix_short_node_name.split(':')[-1]

    hit_name_list = None

    for p in range(2):

        hit_name_list = []

        if fix_short_node_name in __g_all_node_dict:

            hit_name_list = __g_all_node_dict[fix_short_node_name]

        else:

            node_name_re_object = re.compile(fix_short_node_name)

            for this_key in __g_all_node_dict:

                if not node_name_re_object.search(this_key):
                    continue

                this_node_list = __g_all_node_dict[this_key]

                if not this_node_list:
                    continue

                hit_name_list.extend(this_node_list)

        if not hit_name_list:
            return

        all_exists = True
        for hit_name in hit_name_list:

            if cmds.objExists(hit_name):
                continue

            all_exists = False
            break

        if all_exists:
            break

        force_update_all_node_dict()

    if not hit_name_list:
        return

    fix_hit_name_list = None

    if long_name_filter:

        fix_hit_name_list = []

        long_name_re_object = re.compile(long_name_filter)

        for hit_name in hit_name_list:

            if not long_name_re_object.search(hit_name):
                continue

            fix_hit_name_list.append(hit_name)

    else:

        fix_hit_name_list = hit_name_list

    if not fix_hit_name_list:
        return

    if node_type:

        fix_hit_name_list = cmds.ls(
            fix_hit_name_list, typ=node_type, l=True)

    return fix_hit_name_list


# ===============================================
def delete(target_node_list):
    """
    ノードを削除

    :param target_node_list: 対象ノードリスト
    """

    if not target_node_list:
        return

    for target_node in target_node_list:

        if not target_node:
            continue

        if not exists(target_node):
            continue

        cmds.delete(target_node)


# ==================================================
def duplicate(target_node, duplicate_name=None):
    """
    ノード複製
    """

    if not base_utility.node.exists(target_node):
        return

    target_node_name = base_utility.name.get_short_name(target_node)

    if duplicate_name is None:
        duplicate_name = target_node_name + "_copy"

    if base_utility.node.exists(duplicate_name):
        return

    target_shape_node = base_utility.mesh.get_mesh_shape(target_node)

    if target_shape_node is not None:

        target_shape_node_name = \
            base_utility.name.get_short_name(target_shape_node)

        if target_node_name.lower() == target_shape_node_name.lower():
            cmds.rename(target_shape_node, target_shape_node_name + 'Shape')

    duplicated_node = cmds.ls(
        cmds.duplicate(target_node, rr=True, name=duplicate_name), l=True
    )[0]

    return duplicated_node


# ===============================================
def __update_all_node_dict():

    global __g_all_node_dict_update_flag

    __boot_job_for_all_node_dict()

    if not __g_all_node_dict_update_flag:
        return

    __g_all_node_dict_update_flag = False

    force_update_all_node_dict()


# ===============================================
def force_update_all_node_dict():

    global __g_all_node_dict

    if not __g_all_node_dict:
        __g_all_node_dict = {}

    __g_all_node_dict.clear()

    all_node_list = cmds.ls('*', l=True, r=True)

    if not all_node_list:
        return

    for node in all_node_list:

        this_short_name = node.split('|')[-1]
        this_short_name = this_short_name.split(':')[-1]

        if this_short_name not in __g_all_node_dict:
            __g_all_node_dict[this_short_name] = []

        __g_all_node_dict[this_short_name].append(node)


# ===============================================
def __boot_job_for_all_node_dict():

    global __g_all_node_dict_job_enable
    global __g_all_node_dict_update_flag

    if __g_all_node_dict_job_enable:
        return

    __kill_job_for_all_node_dict()

    cmds.scriptJob(conditionTrue=['delete', __execute_job_for_all_node_dict])

    cmds.scriptJob(event=['NameChanged', __execute_job_for_all_node_dict])

    cmds.scriptJob(event=['DagObjectCreated', __execute_job_for_all_node_dict])

    cmds.scriptJob(event=['NewSceneOpened', __execute_job_for_all_node_dict])
    cmds.scriptJob(event=['SceneOpened', __execute_job_for_all_node_dict])
    cmds.scriptJob(event=['SceneImported', __execute_job_for_all_node_dict])

    __g_all_node_dict_job_enable = True
    __g_all_node_dict_update_flag = True


# ===============================================
def __kill_job_for_all_node_dict():

    job_list = cmds.scriptJob(listJobs=True)

    if not job_list:
        return

    kill_job_index_list = []

    for job in job_list:

        job_str = str(job)

        if job_str.find('__execute_job_for_all_node_dict') < 0:
            continue

        this_index = base_utility.string.get_string_by_regex(job_str, '.*:')

        if this_index is None:
            continue

        try:
            this_index = int(this_index.replace(':', ''))
        except Exception:
            continue

        kill_job_index_list.append(int(this_index))

    if not kill_job_index_list:
        return

    for kill_job_index in kill_job_index_list:
        cmds.scriptJob(kill=kill_job_index)


# ===============================================
def __execute_job_for_all_node_dict():

    global __g_all_node_dict_update_flag

    __g_all_node_dict_update_flag = True
