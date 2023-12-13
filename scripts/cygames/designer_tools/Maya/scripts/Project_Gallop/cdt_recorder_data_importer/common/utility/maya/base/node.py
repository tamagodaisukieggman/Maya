# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds


# ===============================================
def delete_node(target_node_list):

    if not target_node_list:
        return

    for target_node in target_node_list:

        if not target_node:
            continue

        if not cmds.objExists(target_node):
            continue

        cmds.delete(target_node)
