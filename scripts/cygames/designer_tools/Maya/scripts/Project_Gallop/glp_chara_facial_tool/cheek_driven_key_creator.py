# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import os

import maya.cmds as cmds

from ..base_common import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CheekDrivenKeyCreator(object):

    # ===============================================
    def __init__(self):

        self.script_file_path = None
        self.script_dir_path = None

        self.cheek_driver = None
        self.cheek_driven = None

        self.is_init = False

        self.facial_root = 'facial'

        self.driven_key_attr_list = [
            'cheek0',
            'cheek1',
        ]

    # ===============================================
    def create(self):

        self.__initialize()

        if not self.is_init:
            return

        self.__create_driven_key_attribute()

        self.__reset_driver()

        self.__create_expression()

        self.__reset_driver()

    # ===============================================
    def __initialize(self):

        self.is_init = False

        self.cheek_driver = \
            base_utility.node.search('Cheek_Ctrl$', self.facial_root)

        if not self.cheek_driver:
            return

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.is_init = True

    # ===============================================
    def __create_driven_key_attribute(self):

        if not self.is_init:
            return

        for driven_attr in self.driven_key_attr_list:

            base_utility.attribute.add(
                self.cheek_driver, driven_attr, 0.0
            )

            cmds.setAttr(
                self.cheek_driver + '.' + driven_attr,
                cb=False, k=True, l=False)

            cmds.addAttr(
                self.cheek_driver + '.' + driven_attr,
                e=True,
                minValue=0,
                maxValue=1
            )

    # ===============================================
    def __reset_driver(self):

        for driven_attr in self.driven_key_attr_list:

            cmds.setAttr(self.cheek_driver + '.' + driven_attr, 0)

    # ===============================================
    def __create_expression(self):

        expression_file_path = \
            self.script_dir_path + '/resource/cheek_expression.txt'

        if not os.path.isfile(expression_file_path):
            return

        cheek_ctrl = \
            base_utility.node.search("Cheek_Ctrl$", self.facial_root)

        if not cheek_ctrl:
            return

        cheek_material = \
            base_utility.node.search("mtl_.*_cheek", '', 'lambert')

        if not cheek_material:
            return

        file_node = cmds.listConnections(cheek_material + '.color', t='file')

        if not file_node:
            return

        file_node = file_node[0]

        base_utility.attribute.set_value(
            file_node,
            'useFrameExtension',
            1
        )

        connect_list = cmds.listConnections(file_node + ".frameExtension")

        if connect_list:
            cmds.delete(connect_list)

        fopen = open(expression_file_path)
        expression_data = fopen.read()
        fopen.close()

        expression_data = expression_data.replace("CHEEK_CTRL", cheek_ctrl)
        expression_data = expression_data.replace(
            "CHEEK_FILE_NODE", file_node)

        cmds.expression(n='cheek_expression', s=expression_data)
