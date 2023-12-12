# -*- coding: utf-8 -*-
"""
Copyright (C) 2021 Digital Frontier Inc.
"""
import os
from . import logger


def get_namespace_list():
    return ['EMPTY', 'cAAA', 'cBBB']


def select_node(node_list, add_select):
    logger.get_logger().info('Select: ' + ', '.join(node_list))


def view_fit(node_list):
    logger.get_logger().info('ViewFit: ' + ', '.join(node_list))
