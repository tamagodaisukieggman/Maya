# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import sys


# ===============================================
def exec_maya_command(command, *header_param, **value_param):
    """
    Mayaコマンドの実行

    :param command: Mayaコマンド
    :param header_param: 可変長引数
    :param value_param: 可変長引数

    :return: 存在する場合はTrue
    """

    if not command:
        return

    script_str = ''

    if header_param:

        count = -1
        for header_param_value in header_param:
            count += 1

            if not header_param_value:
                continue

            this_type = type(header_param_value)

            if sys.version_info.major == 2:
                if this_type == str or this_type == unicode:
                    script_str += '\'{0}\''.format(header_param_value)
                else:
                    script_str += '{0}'.format(header_param_value)
            else:
                if this_type == str or this_type == bytes:
                    script_str += '\'{0}\''.format(header_param_value)
                else:
                    script_str += '{0}'.format(header_param_value)

            if count < len(header_param) - 1:
                script_str += ','

    if value_param:

        if script_str != '':
            script_str += ','

        count = -1
        for value_param_key in value_param:
            count += 1

            value = value_param[value_param_key]
            this_type = type(value)

            if sys.version_info.major == 2:
                if this_type == str or this_type == unicode:
                    script_str += '{0}=\'{1}\''.format(value_param_key, value)
                else:
                    script_str += '{0}={1}'.format(value_param_key, value)
            else:
                if this_type == str or this_type == bytes:
                    script_str += '{0}=\'{1}\''.format(value_param_key, value)
                else:
                    script_str += '{0}={1}'.format(value_param_key, value)

            if count < len(value_param) - 1:
                script_str += ','

    locals_obj = locals()
    script_str = 'import maya.cmds as cmds; result_value = cmds.{0}({1})'.format(command, script_str)
    exec(script_str, {}, locals_obj)

    return locals_obj.get('result_value')
