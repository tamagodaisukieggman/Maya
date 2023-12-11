# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
from xml.etree import cElementTree

try:
    from builtins import str
except Exception:
    pass


# ===============================================
def read(xml_file_path):

    if not xml_file_path:
        return

    if not os.path.isfile(xml_file_path):
        return

    elementTree = cElementTree.parse(xml_file_path)

    if elementTree is None:
        return

    root_element = elementTree.getroot()

    if root_element is None:
        return

    return root_element


# ===============================================
def write(xml_file_path, root_element):

    if not xml_file_path:
        return

    if root_element is None:
        return

    element_tree = cElementTree.ElementTree(element=root_element)

    element_tree.write(xml_file_path, encoding='utf-8')


# ===============================================
def create_element(element_name, element_value):

    if not element_name:
        return

    new_element = cElementTree.Element(element_name)

    if element_value is not None:
        new_element.text = str(element_value)

    return new_element


# ===============================================
def add_element(target_element, element_name, element_value):

    if target_element is None:
        return

    if not element_name:
        return

    new_element = cElementTree.SubElement(target_element, element_name)

    if element_value is not None:
        new_element.text = str(element_value)

    return new_element


# ===============================================
def add_element_from_list(target_element, element_name, element_value_list):

    if target_element is None:
        return

    if not element_name:
        return

    if not element_value_list:
        return

    element_list = []

    for element_value in element_value_list:

        this_element = cElementTree.SubElement(
            target_element, element_name)

        if element_value is not None:
            this_element.text = str(element_value)

        element_list.append(this_element)

    return element_list


# ===============================================
def search_element(target_element, element_name):

    if target_element is None:
        return

    if not element_name:
        return

    result_element = target_element.find(element_name)

    return result_element


# ===============================================
def search_element_list(target_element, element_name):

    if target_element is None:
        return

    if not element_name:
        return

    result_element_list = target_element.findall(element_name)

    return result_element_list


# ===============================================
def exists_element(target_element, element_name):

    element = search_element(target_element, element_name)

    if element is None:
        return False

    return True


# ===============================================
def set_element_value(target_element, element_name, element_value):

    this_element = search_element(target_element, element_name)

    if this_element is None:
        return

    this_element.text = element_value


# ===============================================
def get_element_value(target_element, element_name):

    this_element = search_element(target_element, element_name)

    if this_element is None:
        return

    return this_element.text
