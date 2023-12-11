# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
except:
    pass

from xml.dom import minidom, Node
import tempfile
import platform
import os.path
import sys

import maya.cmds as cmds


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Setting(object):
    """
    設定のロード、セーブ
    """

    # ===============================================
    def __init__(self, setting_name, is_group_transform=False):

        self.__setting_name = setting_name

        self.is_group_transform = is_group_transform

        self.setting_dir_path = None
        self.setting_file_name = None

        self.setting_file_path = None

        self.setting_group_name = None
        self.setting_group = None

        self.__initialize()

    # ===============================================
    def __initialize(self):

        temp_dir_path = tempfile.gettempdir()
        temp_dir_path = temp_dir_path.replace('\\', '/')

        if platform.system() == 'Windows':
            temp_dir_path = \
                temp_dir_path.replace(
                    'appdata/local/temp',
                    'documents/maya/scripts'
                )

        self.set_dir_path(temp_dir_path)
        self.set_file_name(self.__setting_name + '_setting.xml')

        self.set_group_name(self.__setting_name + '_setting')

    # ===============================================
    def set_file_name(self, file_name):

        if not file_name:
            return

        self.setting_file_name = file_name

        if self.setting_file_name.find('.xml') < 0:
            self.setting_file_name += '.xml'

        self.__fix_setting_file_path()

    # ===============================================
    def set_dir_path(self, dir_path):

        if not dir_path:
            return

        self.setting_dir_path = dir_path

        self.__fix_setting_file_path()

    # ===============================================
    def __fix_setting_file_path(self):

        if not self.setting_dir_path:
            return

        if not self.setting_file_name:
            return

        self.setting_file_path = \
            self.setting_dir_path + '/' + self.setting_file_name

    # ===============================================
    def set_group_name(self, group_name):

        if not group_name:
            return

        self.setting_group_name = group_name

    # ===============================================
    def save(self, key, value):

        if self.is_group_transform:

            self.__save_to_group(key, value)

        else:

            self.__save_to_xml(key, value)

    # ===============================================
    def __save_to_xml(self, key, value):

        if not self.__create_file():
            return

        doc = self.__get_xml_document(self.setting_file_path)

        if doc is None:
            return

        convert_value = self.__convert_value_to_string(value)

        root_node = doc.documentElement

        data_node = self.__get_xml_data_node(root_node, key)

        if data_node is not None:

            data_node.setAttribute('Value', convert_value)

        else:

            data_node = doc.createElement('Data')
            data_node.setAttribute('Value', convert_value)
            data_node.setAttribute('Key', key)

            root_node.appendChild(data_node)

        self.__save_xml_document(self.setting_file_path, doc)

    # ===============================================
    def __save_to_group(self, key, value):

        self.__create_setting_group()

        if not self.setting_group:
            return

        self.__set_key_attribute(key, value)

    # ===============================================
    def load(self, key, data_type=str, default_value=None):

        if self.is_group_transform:

            return self.__load_from_group(key, data_type, default_value)

        else:

            return self.__load_from_xml(key, data_type, default_value)

    # ===============================================
    def __load_from_xml(self, key, value_type, default_value):

        doc = self.__get_xml_document(self.setting_file_path)

        if not doc:
            return default_value

        root_node = doc.documentElement
        data_node = self.__get_xml_data_node(root_node, key)

        if not data_node:
            return default_value

        value = self.__get_xml_attr_value('Value', data_node)

        convert_value = \
            self.__convert_value_from_string(value, value_type, default_value)

        return convert_value

    # ===============================================
    def __load_from_group(self, key, value_type, default_value):

        self.__set_setting_group()

        if not self.setting_group:
            return default_value

        if not self.__exists_key_attribute(key):
            return default_value

        value = self.__get_key_attribute(key)

        convert_value = \
            self.__convert_value_from_string(value, value_type, default_value)

        return convert_value

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
        if sys.version_info.major == 2:
            temp_file.write(doc.toprettyxml('  ', '\n', 'utf-8'))
        else:
            temp_file.write(doc.toprettyxml('  ', '\n', 'utf-8').decode('utf-8'))
        temp_file.close()

        return doc

    # ===============================================
    def __get_xml_document(self, file_path):

        if not os.path.isfile(file_path):
            return None

        try:
            return minidom.parse(file_path)
        except:
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

        if sys.version_info.major == 2:
            temp_file.write(temp_str)
        else:
            temp_file.write(temp_str.decode('utf-8'))
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

    # ===============================================
    def __set_setting_group(self):

        self.setting_group = None

        if not cmds.objExists(self.setting_group_name):
            return

        hit_list = cmds.ls(self.setting_group_name, l=True, r=True)

        if not hit_list:
            return

        self.setting_group = hit_list[0]

    # ===============================================
    def __create_setting_group(self):

        self.__set_setting_group()

        if self.setting_group:
            return

        cmds.group(name=self.setting_group_name, em=True)

        self.__set_setting_group()

    # ===============================================
    def __exists_key_attribute(self, key):

        if not self.setting_group:
            return

        attr_list = cmds.listAttr(self.setting_group)

        if not attr_list:
            return

        for attr in attr_list:

            if attr == key:
                return attr

        return None

    # ===============================================
    def __add_key_attribute(self, key):

        if self.__exists_key_attribute(key):
            return

        cmds.addAttr(self.setting_group,
                      longName=key,
                      dataType='string',
                      niceName=key)

        cmds.setAttr(self.setting_group + '.' + key,
                      '',
                      type='string')

    # ===============================================
    def __set_key_attribute(self, key, value):

        self.__add_key_attribute(key)

        convert_value = self.__convert_value_to_string(value)

        cmds.setAttr(self.setting_group + '.' + key,
                      convert_value, type='string')

    # ===============================================
    def __get_key_attribute(self, key):

        if not self.__exists_key_attribute(key):
            return

        attr_value = cmds.getAttr(self.setting_group + '.' + key)

        return attr_value

    # ===============================================
    def __convert_value_to_string(self, value):

        value_type = type(value)
        convert_value = ''

        if sys.version_info.major == 2:
            if value_type == str or value_type == unicode:
                convert_value = eval(repr(value))
            else:
                convert_value = str(value)
        else:
            if value_type == str or value_type == bytes:
                convert_value = eval(repr(value))
            else:
                convert_value = str(value)

        return convert_value

    # ===============================================
    def __convert_value_from_string(self, value, value_type, default_value):

        if value_type == str or value_type == None:

            try:
                return eval(repr(value))
            except:

                if default_value is None:
                    return ''

                return default_value

        elif value_type == int:

            try:
                return int(value)
            except:

                if default_value is None:
                    return 0

                return default_value

        elif value_type == float:

            try:
                return float(value)
            except:

                if default_value is None:
                    return 0.0

                return default_value

        elif value_type == bool:

            try:

                if value == 'False':
                    return False
                elif value == 'True':
                    return True

                if default_value is None:
                    return False

                return default_value

            except:

                if default_value is None:
                    return False

                return default_value

        return default_value
