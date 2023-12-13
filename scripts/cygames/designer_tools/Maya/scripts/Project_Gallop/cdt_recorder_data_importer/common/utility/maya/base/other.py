# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

# このcmdsはevalで使われる
import maya.cmds as cmds
import sys


# ===============================================
def exec_maya_param(command, header_param, value_param_dict):

    script_str = ''

    header_param_list = []

    if type(header_param) != list:
        header_param_list.append(header_param)
    else:
        header_param_list = header_param

    if header_param_list:

        count = -1
        for header_param in header_param_list:
            count += 1

            if not header_param:
                continue

            this_type = type(header_param)
            if sys.version_info.major == 2:
                if this_type == str or this_type == unicode:
                    script_str += '\'{0}\''.format(header_param)
                else:
                    script_str += '{0}'.format(header_param)
            else:
                # for Maya 2022-
                if this_type == str:
                    script_str += '\'{0}\''.format(header_param)
                else:
                    script_str += '{0}'.format(header_param)

            if count < len(header_param_list) - 1:
                script_str += ','

    if value_param_dict:

        if script_str != '':
            script_str += ','

        count = -1
        for value_param in value_param_dict:
            count += 1

            value = value_param_dict[value_param]
            this_type = type(value)

            if sys.version_info.major == 2:
                if this_type == str or this_type == unicode:
                    script_str += '{0}=\'{1}\''.format(value_param, value)
                else:
                    script_str += '{0}={1}'.format(value_param, value)
            else:
                # for Maya 2022-
                if this_type == str:
                    script_str += '{0}=\'{1}\''.format(value_param, value)
                else:
                    script_str += '{0}={1}'.format(value_param, value)

            if count < len(value_param_dict) - 1:
                script_str += ','

    if script_str == '':
        return

    script_str = 'cmds.{0}({1})'.format(command, script_str)

    return eval(script_str)
