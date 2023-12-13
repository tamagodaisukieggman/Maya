# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import os
import subprocess
import datetime

import maya.cmds as cmds
import maya.mel as mel


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BatchRenderManager(object):

    # ===========================================
    def __init__(self):

        self.root_dir_path = None

        self.delete_file_after_render = False

        self.render_exe_file_path = None

        self.render_item_num = 3
        self.render_item_list = None

        self.__create_render_item_list()

    # ===========================================
    def __create_render_item_list(self):

        self.render_item_list = []

        for p in range(0, self.render_item_num):

            new_render_item = BatchRenderItem(self, p)

            self.render_item_list.append(new_render_item)

    # ===========================================
    def add_target(self, target_file_path, target_file_option):

        target_render_item = self.__get_render_item_with_min_list()

        if target_render_item is None:
            return False

        if not target_render_item.add_target(target_file_path, target_file_option):
            return False

        return True

    # ===========================================
    def __get_render_item_with_min_list(self):

        max_target_count = 1000
        target_render_item = None

        for render_item in self.render_item_list:

            if len(render_item.target_file_path_list) < max_target_count:

                max_target_count = len(
                    render_item.target_file_path_list)

                target_render_item = render_item

        return target_render_item

    # ===========================================
    def execute_batch_render(self):

        if not self.__check():
            return False

        for render_item in self.render_item_list:
            render_item.execute_batch_render()

        return True

    # ===========================================
    def __check(self):

        if self.root_dir_path is None:
            return False

        if not os.path.isdir(self.root_dir_path):
            return False

        maya_version = cmds.about(v=True)

        self.render_exe_file_path = 'C:/Program Files/Autodesk/Maya{0}/bin/Render.exe'.format(
            maya_version
        )

        if not os.path.isfile(self.render_exe_file_path):
            return False

        return True

    # ===========================================
    def clear_all_target(self):

        for render_item in self.render_item_list:
            render_item.clear_all_target()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BatchRenderItem(object):

    # ===========================================
    def __init__(self, main, index):

        self.main = main

        self.index = index

        self.batch_file_name = None
        self.batch_file_path = None

        self.target_file_path_list = []
        self.target_file_option_list = []

    # ===========================================
    def add_target(self, target_file_path, target_file_option):

        if not os.path.isfile(target_file_path):
            return False

        fix_file_option = ''
        if target_file_option is not None:
            fix_file_option = target_file_option

        self.target_file_path_list.append(target_file_path)
        self.target_file_option_list.append(fix_file_option)

        return True

    # ===========================================
    def clear_all_target(self):

        self.target_file_path_list = []
        self.target_file_option_list = []

    # ===========================================
    def __check(self):

        if self.target_file_path_list is None:
            return False

        if len(self.target_file_path_list) == 0:
            return False

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

        self.batch_file_name = '____batch_render{0:02d}_{1}.bat'.format(
            self.index,
            today_info
        )

        self.batch_file_path = self.main.root_dir_path + '/' + self.batch_file_name

        return True

    # ===========================================
    def __create_batch_file(self):

        whole_content = ''

        target_path_content = ''

        for p in range(0, len(self.target_file_path_list)):

            target_file_path = self.target_file_path_list[p]
            target_file_option = self.target_file_option_list[p]

            if not os.path.isfile(target_file_path):
                continue

            if target_file_option is None:
                target_file_option = ''

            target_file_path = target_file_path.replace('/', '\\')

            this_content = '"{0}" {1} "{2}"\r\n'.format(
                self.main.render_exe_file_path.replace('/', '\\'),
                target_file_option,
                target_file_path
            )

            if self.main.delete_file_after_render:
                this_content += 'del "{0}"\r\n'.format(target_file_path)

            whole_content += this_content + '\r\n'

            target_path_content += 'echo ' + target_file_path + '\r\n'

            if target_file_option != '':
                target_path_content += \
                    'echo     ({0})\r\n'.format(target_file_option)

        if os.path.isfile(self.batch_file_path):
            os.remove(self.batch_file_path)

        if whole_content == '':
            return False

        fix_batch_file_path = self.batch_file_path.replace('/', '\\')

        header_content = ''
        header_content += '@echo off\r\n'
        header_content += 'echo *******************************************\r\n'
        header_content += 'echo Batch Render Start\r\n'
        header_content += 'echo;\r\n'
        header_content += 'echo Batch File:\r\n'
        header_content += 'echo {0}\r\n'.format(fix_batch_file_path)
        header_content += 'echo;\r\n'
        header_content += 'echo Target File List:\r\n'
        header_content += target_path_content
        header_content += 'echo;\r\n'
        header_content += 'echo *******************************************\r\n'
        header_content += 'echo;\r\n'

        footer_content = ''
        footer_content += 'echo;\r\n'
        footer_content += 'echo *******************************************\r\n'
        footer_content += 'echo;\r\n'
        footer_content += 'echo Batch Render End\r\n'
        footer_content += 'echo;\r\n'
        footer_content += 'echo *******************************************\r\n'
        footer_content += 'del "{0}"\r\n'.format(fix_batch_file_path)

        whole_content = header_content + whole_content + footer_content

        output_file = open(self.batch_file_path, 'w')

        output_file.write(whole_content)

        output_file.close()

        if not os.path.isfile(self.batch_file_path):
            return False

        return True

    # ===========================================
    def execute_batch_render(self):

        if not self.__check():
            return False

        if not self.__create_batch_file():
            return False

        if not os.path.isfile(self.batch_file_path):
            return False

        subprocess.Popen(self.batch_file_path)

        return True
