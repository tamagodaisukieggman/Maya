# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import re

import maya.cmds as cmds


# ==================================================
def get_namespace_list():
    """
    ネームスペースリスト取得

    :return: ネームスペースの配列
    """

    namespace_list = cmds.namespaceInfo(lon=True)

    if not namespace_list:
        return

    result_namespace_list = []

    for namespace in namespace_list:

        result_namespace_list.append(namespace)

    return result_namespace_list


# ==================================================
def exists(target_namespace):
    """
    ネームスペースが存在するかどうか

    :param target_namespace: 対象ネームスペース名
    """

    namespace_list = get_namespace_list()

    if not namespace_list:
        return False

    for namespace in namespace_list:

        if namespace != target_namespace:
            continue

        return True

    return False


# ==================================================
def search(target_namespace):
    """
    ネームスペースを検索

    :param target_namespace: 対象ネームスペース名
    :return: ネームスペース名
    """

    namespace_list = get_namespace_list()

    if not namespace_list:
        return

    for namespace in namespace_list:

        if namespace != target_namespace:
            continue

        return namespace

    for namespace in namespace_list:

        if not re.search(target_namespace, namespace):
            continue

        return namespace

    return


# ===============================================
def get_nonamespace_name(name):
    """
    ネームスペースの無い名前を取得

    :param name: 対象名
    :return: ネームスペースを無くした名前
    """

    if name.find(':') < 0:
        return name

    namespace = name.split(':')[0]
    namespace = namespace.replace('|', '') + ':'

    nonamespace_name = name.replace(namespace, '')

    return nonamespace_name


# ===============================================
def remove(target_namespace):
    """
    ネームスペースの削除

    :param target_namespace: 対象ネームスペース名
    """

    if not exists(target_namespace):
        return

    cmds.namespace(rm=target_namespace, mergeNamespaceWithRoot=True)
