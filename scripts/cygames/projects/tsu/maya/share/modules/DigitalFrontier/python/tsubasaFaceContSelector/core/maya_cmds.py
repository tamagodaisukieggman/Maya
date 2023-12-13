# -*- coding: utf-8 -*-
"""
Copyright (C) 2021 Digital Frontier Inc.
"""
import os
import maya.cmds as cmds
from . import logger


def get_namespace_list():
    return ['EMPTY'] + [ns for ns in cmds.namespaceInfo(listOnlyNamespaces=True) if ns not in ['UI', 'shared']]


def select_node(node_list, add_select):
    sel_targets = cmds.ls(node_list)
    cmds.select(sel_targets, add=add_select)
    logger.get_logger().info('Select: ' + ', '.join(sel_targets))


def view_fit(node_list):
    sel_targets = cmds.ls(node_list)
    cmds.select(sel_targets)
    cmds.viewFit(fitFactor=0.15)
    cmds.select(clear=True)
