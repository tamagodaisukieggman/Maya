# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import str
except:
    pass

import re
import os
import subprocess

import maya.cmds as cmds

from .. import utility as base_utility

_g_param_prefix = 'SBATCH__'
_g_param_type_format = '__<TYP>{0}</TYP>'
_g_param_devide_format = '__<VER>{0:02d}</VER>'
_g_list_divider = '||||'
_g_dict_divider = '++++'
_g_is_cyclecheck = False


# ===============================================
def execute(command, wait, **batch_param):

    batch_file_path = __search_batch_file_path()

    if not batch_file_path:
        return

    # --------------------
    # 環境変数に値を割り当て

    if batch_param:

        for param in list(batch_param.items()):

            this_key = param[0]
            this_value = param[1]
            this_type = type(this_value)
            this_type_str = \
                base_utility.string.get_string_by_regex(this_type, '\'.*\'')
            this_type_str = this_type_str.replace('\'', '')

            __delete_env_value(this_key)

            this_env_key = (_g_param_prefix + this_key +
                            _g_param_type_format.format(this_type_str)).upper()

            if this_type == list or this_type == tuple or this_type == dict:

                temp_env_key_dict = {}

                count = -1
                for temp_value in this_value:
                    count += 1

                    this_index = int(count / 50)

                    temp_env_key = this_env_key + \
                        _g_param_devide_format.format(this_index)

                    if temp_env_key not in temp_env_key_dict:
                        temp_env_key_dict[temp_env_key] = []

                    if this_type == dict:

                        temp_dict_key = temp_value
                        temp_dict_value = str(this_value[temp_dict_key])

                        temp_env_key_dict[temp_env_key].append(
                            temp_dict_key + _g_dict_divider + temp_dict_value)

                    else:
                        temp_env_key_dict[temp_env_key].append(temp_value)

                for temp_env_key in temp_env_key_dict:

                    temp_value_list = temp_env_key_dict[temp_env_key]

                    os.environ[temp_env_key] = ''

                    count = -1
                    for temp_value in temp_value_list:
                        count += 1

                        os.environ[temp_env_key] += str(temp_value)

                        if count < len(temp_value_list) - 1:
                            os.environ[temp_env_key] += _g_list_divider

            else:

                os.environ[this_env_key] = str(this_value)

    # --------------------
    # 起動時のコマンドの生成

    fix_command = 'import os;import maya.cmds as cmds;'

    if _g_is_cyclecheck:
        fix_command += 'cmds.cycleCheck(e=True);'
    else:
        fix_command += 'cmds.cycleCheck(e=False);'

    if command:
        fix_command += command

    fix_command = fix_command.replace('"', '\"')
    fix_command = fix_command.replace(' ', '__space__')

    # --------------------
    # バッチ起動

    if wait:
        subprocess.call([batch_file_path, '"' + fix_command + '"'])
    else:
        subprocess.Popen([batch_file_path, '"' + fix_command + '"'])


# ===============================================
def get_param_value(param_name):

    env_key_prefix = (_g_param_prefix + param_name).upper()

    # --------------------
    # タイプの取得と該当する値の取得

    param_value_list = []
    param_type_str = None

    for env_key in os.environ:

        if env_key.upper().find(env_key_prefix) < 0:
            continue

        if not param_type_str:
        
            param_type_str = base_utility.string.get_string_by_regex(
                env_key, _g_param_type_format.format('.*'))
            param_type_str = base_utility.string.get_string_by_regex(
                param_type_str, '>.*<')
            param_type_str = param_type_str.replace('>', '').replace('<', '')

        param_value_list.append(os.environ[env_key])

    if not param_value_list:
        return

    # --------------------
    # タイプからデフォルト値の設定

    param_type = None
    result_value = None

    if param_type_str == 'LIST':
        param_type = list
        result_value = []
    elif param_type_str == 'TUPLE':
        param_type = tuple
        result_value = ()
    elif param_type_str == 'DICT':
        param_type = dict
        result_value = {}
    elif param_type_str == 'BOOL':
        param_type = bool
        result_value = False
    elif param_type_str == 'INT':
        param_type = int
        result_value = 0
    elif param_type_str == 'FLOAT':
        param_type = float
        result_value = 0.0
    elif param_type_str == 'LONG':
        param_type = long
        result_value = long(0.0)
    elif param_type_str == 'UNICODE':
        param_type = str
        result_value = ''
    elif param_type_str == 'STR':
        param_type = str
        result_value = ''
    elif param_type_str == 'NONETYPE':
        param_type = None
        result_value = None
    else:
        param_type = str
        result_value = ''

    # --------------------
    # 環境変数から値の取得

    for param_value in param_value_list:

        if param_type == list:

            this_value_list = \
                param_value.split(_g_list_divider)
            result_value.extend(this_value_list)

        elif param_type == tuple:

            this_value_list = \
                param_value.split(_g_list_divider)
            result_value = result_value + tuple(this_value_list)

        elif param_type == dict:

            this_value_list = \
                param_value.split(_g_list_divider)

            for this_value in this_value_list:

                if this_value.find(_g_dict_divider) < 0:
                    continue

                this_dict_key = this_value.split(_g_dict_divider)[0]
                this_dict_value = this_value.split(_g_dict_divider)[1]

                result_value[this_dict_key] = this_dict_value

        elif param_type == bool:
            if param_value == 'True':
                result_value = True
        elif param_type == int:
            result_value = int(param_value)
        elif param_type == float:
            result_value = float(param_value)
        elif param_type == long:
            result_value = long(param_value)
        elif param_type == str:
            result_value = str(param_value)
        elif param_type == str:
            result_value = str(param_value)
        elif param_type == None:
            result_value = None
        else:
            result_value = param_value

    return result_value


# ===============================================
def __delete_env_value(param_name):

    env_key_prefix = (_g_param_prefix + param_name).upper()

    target_env_key_list = []

    for env_key in os.environ:

        if env_key.upper().find(env_key_prefix) < 0:
            continue

        target_env_key_list.append(env_key)

    for env_key in target_env_key_list:

        if env_key not in os.environ:
            continue

        del os.environ[env_key]


# ===============================================
def __search_batch_file_path():

    script_file_path = os.path.abspath(__file__).replace('\\', '/')

    if not os.path.isfile(script_file_path):
        return

    script_dir_path = os.path.dirname(script_file_path)

    if not os.path.isdir(script_dir_path):
        return

    resource_dir_path = script_dir_path + '/_resource/simple_batch'

    if not os.path.isdir(resource_dir_path):
        return

    maya_version = cmds.about(v=True)

    batch_file_path = None

    if maya_version == '2015':
        batch_file_path = resource_dir_path + \
            '/mayabatch2015.bat'

    elif maya_version == '2013 x64':
        batch_file_path = resource_dir_path + \
            '/mayabatch2013.5.bat'

    elif maya_version == '2016':
        batch_file_path = resource_dir_path + \
            '/mayabatch2016.bat'

    elif maya_version == '2017':
        batch_file_path = resource_dir_path + \
            '/mayabatch2017.bat'

    elif maya_version == '2018':
        batch_file_path = resource_dir_path + \
            '/mayabatch2018.bat'

    elif maya_version == '2019':
        batch_file_path = resource_dir_path + \
            '/mayabatch2019.bat'

    elif maya_version == '2022':
        batch_file_path = resource_dir_path + \
            '/mayabatch2022.bat'

    elif maya_version == '2023':
        batch_file_path = resource_dir_path + \
            '/mayabatch2023.bat'

    if not batch_file_path:
        return

    if not os.path.isfile(batch_file_path):
        return

    return batch_file_path


# ===============================================
def set_cyclecheck(enable):

    global _g_is_cyclecheck

    _g_is_cyclecheck = enable
