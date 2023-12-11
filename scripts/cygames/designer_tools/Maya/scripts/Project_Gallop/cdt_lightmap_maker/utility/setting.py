# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
except Exception:
    pass

from xml.dom import minidom, Node
import tempfile
import platform
import os.path
import sys

import maya.cmds as cmds
import maya.mel as mel


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Setting(object):
    """
    設定のロード、セーブ
    """

    # ===============================================
    def __init__(self, tool_name):

        self.tool_name = tool_name

        self.setting_dir_path = None
        self.setting_file_path = None

        self.__initialize()

    # ===============================================
    def __initialize(self):

        self.setting_dir_path = tempfile.gettempdir()
        self.setting_dir_path = self.setting_dir_path.replace('\\', '/')

        if platform.system() == 'Windows':
            self.setting_dir_path = \
                self.setting_dir_path.replace(
                    'appdata/local/temp',
                    'documents/maya/scripts'
                )

        self.setting_file_path = \
            self.setting_dir_path + '/' + self.tool_name + '_setting.xml'

    # ===============================================
    def save(self, key, value):

        if not self.__create_file():
            return

        this_type = type(value)
        this_conv_value = ''

        if sys.version_info.major == 2:
            if this_type == str or this_type == unicode:
                this_conv_value = eval(repr(value))
            else:
                this_conv_value = str(value)
        else:
            # maya 2022-
            if this_type == str or this_type == bytes:
                this_conv_value = eval(repr(value))
            else:
                this_conv_value = str(value)

        doc = self.__get_xml_document(self.setting_file_path)

        if doc is None:
            return

        root_node = doc.documentElement

        data_node = self.__get_xml_data_node(root_node, key)

        if data_node is not None:
            data_node.setAttribute('Value', this_conv_value)

        else:

            data_node = doc.createElement('Data')
            data_node.setAttribute('Value', this_conv_value)
            data_node.setAttribute('Key', key)

            root_node.appendChild(data_node)

        self.__save_xml_document(self.setting_file_path, doc)

    # ===============================================
    def load(self, key, data_type='string', default_value=None):

        data_value = ''

        doc = self.__get_xml_document(self.setting_file_path)

        if doc is not None:

            root_node = doc.documentElement
            data_node = self.__get_xml_data_node(root_node, key)
            data_value = ''

            if data_node is not None:
                data_value = self.__get_xml_attr_value('Value', data_node)

        if data_type == 'string' or data_type == '':

            try:
                return eval(repr(data_value))
            except Exception:

                if default_value is None:
                    return ''

                return default_value

        elif data_type == 'int':

            try:
                return int(data_value)
            except Exception:

                if default_value is None:
                    return 0

                return default_value

        elif data_type == 'float':

            try:
                return float(data_value)
            except Exception:

                if default_value is None:
                    return 0.0

                return default_value

        elif data_type == 'bool':

            try:

                if data_value == 'False':
                    return False
                elif data_value == 'True':
                    return True

                if default_value is None:
                    return False

                return default_value

            except Exception:

                if default_value is None:
                    return 0.0

                return default_value

    # ===============================================
    def __create_file(self):

        if not os.path.isdir(self.setting_dir_path):
            return False

        if not os.path.isfile(self.setting_file_path):
            self.__create_xml_document(self.setting_file_path, 'SettingData')

        return True

    # ===============================================
    def __get_xml_data_node(self, root_node, key):

        data_node_list = self.__get_xml_node_list('', root_node)

        for node in data_node_list:

            this_key = self.__get_xml_attr_value('Key', node)

            if this_key == key:
                return node

        return None

    # ===============================================
    def __create_xml_document(self, file_path, root_node_name):

        doc = minidom.Document()

        root = doc.createElement(root_node_name)
        doc.appendChild(root)

        temp_file = open(file_path, 'w')
        temp_file.write(doc.toprettyxml('  ', '\n', 'utf-8'))
        temp_file.close()

        return doc

    # ===============================================
    def __get_xml_document(self, file_path):

        if not os.path.isfile(file_path):
            return None

        try:
            return minidom.parse(file_path)
        except Exception:
            return None

    # ===============================================
    def __save_xml_document(self, file_path, xml_doc):

        if not os.path.isfile(file_path):
            return

        temp_str = xml_doc.toprettyxml('  ', '\n', 'utf-8')
        temp_file = open(file_path, 'w')

        temp_str = temp_str.replace('  \n', '')
        temp_str = temp_str.replace('\n\n', '\n')
        temp_str = temp_str.replace('\n    ', '\n  ')

        temp_file.write(temp_str)
        temp_file.close()

    # ===============================================
    def __get_xml_node_list(self, node_name, root_node):

        result = []

        parent_nodes = []
        if node_name != '':
            parent_nodes = root_node.getElementsByTagName(node_name)
        else:
            parent_nodes.append(root_node)

        if parent_nodes is None:
            return result

        if len(parent_nodes) == 0:
            return result

        parent_node = parent_nodes[0]

        for node in parent_node.childNodes:

            if node.nodeType != node.ELEMENT_NODE:
                continue

            result.append(node)

        return result

    # ===============================================
    def __get_xml_attr_value(self, attr_name, root_node):

        for index in range(root_node.attributes.length):

            item = root_node.attributes.item(index)

            if item.name == attr_name:
                return item.value

        return ''
