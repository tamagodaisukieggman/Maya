# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload
import os
import traceback

def import_hierarchy(path, namespace="import_hierarchy_tmp_ns"):
    if not os.path.isfile(path):
        cmds.error('{} is not found.'.format(path))
        print(format_exc)
        return

    cmds.file(path, i=True, namespace=namespace)
    root_list = cmds.ls(namespace + ":|*")
    root_nodes = []
    for root in root_list:
        root_nodes.append(root.split(":")[-1])
    cmds.namespace(moveNamespace=(namespace, ":"), f=True)
    cmds.namespace(removeNamespace=namespace)
    return root_nodes
