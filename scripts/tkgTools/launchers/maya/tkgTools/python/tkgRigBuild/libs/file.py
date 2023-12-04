# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload
import os
import traceback

def import_hierarchy(path, namespace="imoprt_hierarchy_nss"):
    if not os.path.isfile(path):
        cmds.error('{} is not found.'.format(path))
        print(format_exc)
        return

    cmds.file(path, i=True, namespace=namespace, ignoreVersion=True, mergeNamespacesOnClash=False,
              options="v=0;", pr=True)
    root_list = cmds.ls(namespace + ":|*")
    root_nodes = []
    for root in root_list:
        root_nodes.append(root.split(":")[-1])
    cmds.namespace(moveNamespace=(namespace, ":"), f=True)
    cmds.namespace(removeNamespace=namespace)
    return root_nodes

def reference_model(path, namespace="chr"):
    if not os.path.isfile(path):
        cmds.error('{} is not found.'.format(path))
        print(format_exc)
        return

    cmds.file(path, r=True, namespace=namespace, ignoreVersion=True, mergeNamespacesOnClash=False,
              options="v=0;", gl=True)
    root_nodes = cmds.ls(namespace + ":|*", rn=True, assemblies=True)

    return root_nodes

def get_reference_info(excludes):
    """
    リファレンス情報の取得
    """
    ret = []
    refNodes = cmds.ls(references=True)
    for RNnode in refNodes:
        if not RNnode in excludes:
            ref = {}
            ref.update({
                'namespace' : cmds.referenceQuery(RNnode, namespace=True),
                'filename'   : cmds.referenceQuery(RNnode, filename=True),
                'w_filenam' : cmds.referenceQuery(RNnode, filename=True, withoutCopyNumber=True),
                'isLoaded'  : cmds.referenceQuery(RNnode, isLoaded=True),
                'nodes'     : cmds.referenceQuery(RNnode, nodes=True),
                'node'      : cmds.referenceQuery(RNnode, nodes=True)[0],
                })
            ret.append(ref)

    return ret
