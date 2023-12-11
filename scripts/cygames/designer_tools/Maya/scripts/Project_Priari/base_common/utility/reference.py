# -*- coding: utf-8 -*-F

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import range
except:
    pass

import os

import maya.cmds as cmds


# ================================================
def exists(target_file_path, target_namespace):

    if not exist_reference_namespace(target_namespace):
        return False

    if not exist_reference_file_path(target_file_path):
        return False

    return True


# ================================================
def load(target_file_path, target_namespace):

    if exists(target_file_path, target_namespace):
        return

    cmds.file(
        target_file_path,
        ignoreVersion=True,
        ns=target_namespace,
        r=True,
        mergeNamespacesOnClash=False
    )


# ================================================
def unload(target_file_path, target_namespace):

    if not exists(target_file_path, target_namespace):
        return

    ref_file_path = \
        get_reference_file_path_by_namespace(target_namespace)

    cmds.file(ref_file_path, rr=True)


# ================================================
def get_reference_file_path_list():

    reference_file_list = cmds.file(q=True, r=True)

    if not reference_file_list:
        return

    return reference_file_list


# ================================================
def exist_reference_file_path(target_file_path):

    if not target_file_path:
        return False

    if not os.path.isfile(target_file_path):
        return False

    reference_file_path_list = get_reference_file_path_list()

    if not reference_file_path_list:
        return False

    target_file_path = target_file_path.replace('\\', '/')
    target_file_path = target_file_path.lower()

    for reference_file_path in reference_file_path_list:

        reference_file_path = reference_file_path.replace('\\', '/')
        reference_file_path = reference_file_path.lower()

        if reference_file_path.find(target_file_path) >= 0:
            return True

    return False


# ================================================
def get_reference_namespace_list():

    reference_file_list = get_reference_file_path_list()

    if not reference_file_list:
        return

    reference_namespace_list = []

    for reference_file in reference_file_list:

        reference_namespace = cmds.file(reference_file, q=True, ns=True)

        reference_namespace_list.append(reference_namespace)

    return reference_namespace_list


# ================================================
def exist_reference_namespace(target_namespace):

    if not target_namespace:
        return False

    reference_namespace_list = get_reference_namespace_list()

    if not reference_namespace_list:
        return False

    target_namespace = target_namespace.lower()

    for reference_namespace in reference_namespace_list:

        reference_namespace = reference_namespace.lower()

        if reference_namespace == target_namespace:
            return True

    return False


# ================================================
def get_reference_file_path_by_namespace(target_namespace):

    namespace_list = get_reference_namespace_list()
    file_list = get_reference_file_path_list()

    if not namespace_list:
        return

    target_index = -1

    for p in range(len(namespace_list)):

        if namespace_list[p] == target_namespace:
            target_index = p
            break

    if target_index < 0:
        return

    reference_file = file_list[target_index]

    return reference_file


# ================================================
def change_reference_file_path_by_namespace(target_namespace, target_file_path):

    if not os.path.isfile(target_file_path):
        return

    reference_file_path = \
        get_reference_file_path_by_namespace(target_namespace)

    if not reference_file_path:
        return

    reference_node = cmds.file(reference_file_path, q=True, rfn=True)

    cmds.file(target_file_path, lrd='asPrefs', lr=reference_node)


# ================================================
def import_reference_by_namespace(target_namespace):

    reference_file_path = get_reference_file_path_by_namespace(
        target_namespace)

    if not reference_file_path:
        return

    cmds.file(reference_file_path, ir=True)
