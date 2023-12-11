# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import shutil
import datetime

import maya.cmds as cmds
import maya.mel as mel


# ==================================================
def create_temp_file_from_current_file(temp_file_prefix, temp_file_suffix, temp_dir_name):

    current_file_path = cmds.file(q=True, sn=True)

    if current_file_path is None:
        return

    if not os.path.isfile(current_file_path):
        return

    current_file_name = os.path.basename(current_file_path)
    current_dir_path = os.path.dirname(current_file_path)

    temp_file_name = __get_temp_file_name(
        current_file_path, temp_file_prefix, temp_file_suffix)

    if temp_file_name is None:
        return

    temp_dir_path = current_dir_path

    if temp_dir_name is not None and temp_dir_name != '':
        temp_dir_path += '/' + temp_dir_name

    if not os.path.isdir(temp_dir_path):
        os.makedirs(temp_dir_path)

    temp_file_path = temp_dir_path + '/' + temp_file_name

    is_created = False

    try:

        cmds.file(rn=temp_file_path)
        cmds.file(save=True)
        cmds.file(rn=current_file_path)

        is_created = True

    except:

        is_created = False

    finally:

        cmds.file(rn=current_file_path)

    if not is_created:

        if os.path.isfile(temp_file_path):
            os.remove(temp_file_path)

        return

    return temp_file_path


# ==================================================
def __get_temp_file_name(target_file_path, prefix, suffix):

    if not os.path.isfile(target_file_path):
        return

    target_file_name = os.path.basename(target_file_path)

    target_file_name_noext, target_file_ext = os.path.splitext(
        target_file_name)

    today = datetime.date.today()
    today_detail = datetime.datetime.today()

    today_info = '{0:02d}{1:02d}{2:02d}{3:02d}{4:02d}{5:02d}'.format(
        today.year % 100,
        today.month,
        today.day,
        today_detail.hour,
        today_detail.minute,
        today_detail.second
    )

    fix_prefix = ''
    fix_suffix = ''

    if prefix is not None:
        fix_prefix = prefix

    if suffix is not None:
        fix_suffix = suffix

    temp_file_name = '____{0}{1}{2}_{3}{4}'.format(
        fix_prefix,
        target_file_name_noext,
        fix_suffix,
        today_info,
        target_file_ext
    )

    return temp_file_name
