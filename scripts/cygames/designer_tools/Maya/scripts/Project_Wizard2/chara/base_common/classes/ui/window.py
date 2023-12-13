# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from functools import partial

import maya.cmds as cmds

from ... import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Window(object):

    # ===============================================
    def __init__(self, ui_window_id, title, tab_list=None, menu_list=[], **window_edit_param):

        self.ui_window_id = ui_window_id

        self.__ui_tab_list = tab_list
        self.__ui_tab_count = 0
        self.ui_tab_id = None

        self.__ui_menu_list = menu_list
        self.__is_menu_bar = True if len(self.__ui_menu_list) > 0 else False
        self.ui_menu_id = None

        self.__ui_header_pane_layout_id = None
        self.__ui_footer_pane_layout_id = None
        self.__ui_side_l_pane_layout_id = None
        self.__ui_side_r_pane_layout_id = None

        self.ui_header_layout_id = None
        self.ui_footer_layout_id = None
        self.ui_side_l_layout_id = None
        self.ui_side_r_layout_id = None

        self.ui_body_header_layout_id_list = None
        self.ui_body_footer_layout_id_list = None
        self.ui_body_side_l_layout_id_list = None
        self.ui_body_side_r_layout_id_list = None
        self.ui_body_layout_id_list = None
        self.__ui_body_scroll_layout_id_list = None
        self.__ui_body_header_pane_layout_id_list = None
        self.__ui_body_footer_pane_layout_id_list = None
        self.__ui_body_side_l_pane_layout_id_list = None
        self.__ui_body_side_r_pane_layout_id_list = None

        self.ui_body_header_layout_id_dict = None
        self.ui_body_footer_layout_id_dict = None
        self.ui_body_side_l_layout_id_dict = None
        self.ui_body_side_r_layout_id_dict = None
        self.ui_body_layout_id_dict = None

        self.ui_body_header_layout_id = None
        self.ui_body_footer_layout_id = None
        self.ui_body_side_l_layout_id = None
        self.ui_body_side_r_layout_id = None
        self.ui_body_layout_id = None
        self.__ui_body_scroll_layout_id = None

        self.__show_function = None
        self.__show_function_arg = None

        self.__close_function = None
        self.__close_function_arg = None

        self.__job_list = None
        self.__job_function_list = None
        self.__job_function_arg_list = None

        self.__draw()

        if window_edit_param:
            window_edit_param['edit'] = True
            self.apply_window_param(**window_edit_param)

        self.apply_window_param(e=True, title=title)

    # ===============================================
    def __draw(self):

        base_utility.ui.window.remove_same_id_window(self.ui_window_id)

        if not self.__ui_tab_list:
            self.__ui_tab_list = ['']

        self.__ui_tab_count = len(self.__ui_tab_list)

        self.ui_body_header_layout_id_list = [''] * self.__ui_tab_count
        self.ui_body_footer_layout_id_list = [''] * self.__ui_tab_count
        self.ui_body_side_l_layout_id_list = [''] * self.__ui_tab_count
        self.ui_body_side_r_layout_id_list = [''] * self.__ui_tab_count
        self.ui_body_layout_id_list = [''] * self.__ui_tab_count

        self.__ui_body_scroll_layout_id_list = [''] * self.__ui_tab_count

        self.__ui_body_header_pane_layout_id_list = [''] * self.__ui_tab_count
        self.__ui_body_footer_pane_layout_id_list = [''] * self.__ui_tab_count
        self.__ui_body_side_l_pane_layout_id_list = [''] * self.__ui_tab_count
        self.__ui_body_side_r_pane_layout_id_list = [''] * self.__ui_tab_count

        self.ui_body_header_layout_id_dict = {}
        self.ui_body_footer_layout_id_dict = {}
        self.ui_body_side_l_layout_id_dict = {}
        self.ui_body_side_r_layout_id_dict = {}
        self.ui_body_layout_id_dict = {}

        cmds.window(
            self.ui_window_id,
            s=1,
            mnb=True,
            mxb=True,
            rtf=True,
            cc=self.__execute_close_function,
            menuBar=self.__is_menu_bar
        )

        self.__draw_menu()

        cmds.frameLayout(lv=False, mw=5, mh=5)

        self.__ui_header_pane_layout_id = cmds.paneLayout(
            configuration='horizontal2', ps=[2, 100, 100], shp=1, st=1)

        self.__draw_header()

        self.__ui_footer_pane_layout_id = cmds.paneLayout(
            configuration='horizontal2', ps=[1, 100, 100], shp=2, st=1)

        self.__ui_side_l_pane_layout_id = cmds.paneLayout(
            configuration='vertical2', ps=[2, 100, 100], swp=1, st=1)

        self.__draw_side_l()

        self.__ui_side_r_pane_layout_id = cmds.paneLayout(
            configuration='vertical2', ps=[1, 100, 100], swp=2, st=1)

        self.__draw_body()

        self.__draw_side_r()

        cmds.setParent('..')

        cmds.setParent('..')

        self.__draw_footer()

        cmds.setParent('..')

        cmds.setParent('..')

        cmds.setParent('..')

    # ===============================================
    def __draw_menu(self):

        if not self.__ui_menu_list:
            return

        for menu_param in self.__ui_menu_list:

            menu_item_param_list = menu_param['item_param_list']

            cmds.menu(label=menu_param['label'], tearOff=True)

            for menu_item_param in menu_item_param_list:

                if 'command' in menu_item_param:
                    cmds.menuItem(label=menu_item_param['label'], c=menu_item_param['command'])
                else:
                    cmds.menuItem(label=menu_item_param['label'])

    # ===============================================
    def __draw_header(self):

        self.ui_header_layout_id = cmds.frameLayout(lv=False)
        cmds.setParent('..')

    # ===============================================
    def __draw_side_l(self):

        self.ui_side_l_layout_id = cmds.frameLayout(lv=False)
        cmds.setParent('..')

    # ===============================================
    def __draw_side_r(self):

        self.ui_side_r_layout_id = cmds.frameLayout(lv=False)
        cmds.setParent('..')

    # ===============================================
    def __draw_footer(self):

        self.ui_footer_layout_id = cmds.frameLayout(lv=False)
        cmds.setParent('..')

    # ===============================================
    def __draw_body(self):

        self.ui_tab_id = cmds.tabLayout(bs='none')

        if self.__ui_tab_count <= 1:
            cmds.tabLayout(self.ui_tab_id, e=True, tv=False)

        for cnt in range(self.__ui_tab_count):
            self.__draw_body_main(cnt)

        self.ui_body_header_layout_id = self.ui_body_header_layout_id_list[0]
        self.ui_body_footer_layout_id = self.ui_body_footer_layout_id_list[0]
        self.ui_body_side_l_layout_id = self.ui_body_side_l_layout_id_list[0]
        self.ui_body_side_r_layout_id = self.ui_body_side_r_layout_id_list[0]
        self.ui_body_layout_id = self.ui_body_layout_id_list[0]
        self.__ui_body_scroll_layout_id = self.__ui_body_scroll_layout_id_list[0]

        cmds.setParent('..')

    # ===============================================
    def __draw_body_main(self, index):

        this_frame_layout_id = cmds.frameLayout(lv=False)

        self.__ui_body_header_pane_layout_id_list[index] = cmds.paneLayout(
            configuration='horizontal2', ps=[2, 100, 100], shp=1, st=1)

        self.ui_body_header_layout_id_list[index] = cmds.frameLayout(lv=False)
        cmds.setParent('..')

        self.__ui_body_footer_pane_layout_id_list[index] = cmds.paneLayout(
            configuration='horizontal2', ps=[1, 100, 100], shp=2, st=1)

        self.__ui_body_side_l_pane_layout_id_list[index] = cmds.paneLayout(
            configuration='vertical2', ps=[2, 100, 100], swp=1, st=1)

        self.ui_body_side_l_layout_id_list[index] = cmds.frameLayout(lv=False)
        cmds.setParent('..')

        self.__ui_body_side_r_pane_layout_id_list[index] = cmds.paneLayout(
            configuration='vertical2', ps=[1, 100, 100], swp=2, st=1)

        self.__ui_body_scroll_layout_id_list[index] = \
            cmds.scrollLayout(cr=True)

        self.ui_body_layout_id_list[index] = cmds.frameLayout(lv=False)

        cmds.setParent('..')
        cmds.setParent('..')

        self.ui_body_side_r_layout_id_list[index] = cmds.frameLayout(lv=False)
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.setParent('..')

        self.ui_body_footer_layout_id_list[index] = cmds.frameLayout(lv=False)
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.setParent('..')

        cmds.setParent('..')

        this_tab_name = self.__ui_tab_list[index]

        cmds.tabLayout(self.ui_tab_id, e=True, tl=[
            this_frame_layout_id, this_tab_name])

        self.ui_body_header_layout_id_dict[this_tab_name] = \
            self.ui_body_header_layout_id_list[index]

        self.ui_body_footer_layout_id_dict[this_tab_name] = \
            self.ui_body_footer_layout_id_list[index]

        self.ui_body_side_l_layout_id_dict[this_tab_name] = \
            self.ui_body_side_l_layout_id_list[index]

        self.ui_body_side_r_layout_id_dict[this_tab_name] = \
            self.ui_body_side_r_layout_id_list[index]

        self.ui_body_layout_id_dict[this_tab_name] = \
            self.ui_body_layout_id_list[index]

    # ===============================================
    def show(self):

        if not base_utility.ui.window.exists(self.ui_window_id):
            self.__draw()

        if self.__check_frame_layout(self.ui_header_layout_id):

            cmds.paneLayout(
                self.__ui_header_pane_layout_id, e=True, ps=[2, 100, 99])

        if self.__check_frame_layout(self.ui_footer_layout_id):

            cmds.paneLayout(
                self.__ui_footer_pane_layout_id, e=True, ps=[1, 100, 99])

        if self.__check_frame_layout(self.ui_side_l_layout_id):

            cmds.paneLayout(
                self.__ui_side_l_pane_layout_id, e=True, ps=[2, 99, 100])

        if self.__check_frame_layout(self.ui_side_r_layout_id):

            cmds.paneLayout(
                self.__ui_side_r_pane_layout_id, e=True, ps=[1, 99, 100])

        for cnt in range(self.__ui_tab_count):

            this_header_layout_id = self.ui_body_header_layout_id_list[cnt]
            this_footer_layout_id = self.ui_body_footer_layout_id_list[cnt]
            this_side_l_layout_id = self.ui_body_side_l_layout_id_list[cnt]
            this_side_r_layout_id = self.ui_body_side_r_layout_id_list[cnt]

            this_body_layout_id = self.ui_body_layout_id_list[cnt]
            this_scroll_layout_id = self.__ui_body_scroll_layout_id_list[cnt]

            this_header_pane_layout_id = self.__ui_body_header_pane_layout_id_list[cnt]
            this_footer_pane_layout_id = self.__ui_body_footer_pane_layout_id_list[cnt]
            this_side_l_pane_layout_id = self.__ui_body_side_l_pane_layout_id_list[cnt]
            this_side_r_pane_layout_id = self.__ui_body_side_r_pane_layout_id_list[cnt]

            if self.__check_frame_layout(this_header_layout_id):

                cmds.paneLayout(
                    this_header_pane_layout_id, e=True, ps=[2, 100, 99])

            if self.__check_frame_layout(this_footer_layout_id):

                cmds.paneLayout(
                    this_footer_pane_layout_id, e=True, ps=[1, 100, 99])

            if self.__check_frame_layout(this_side_l_layout_id):

                cmds.paneLayout(
                    this_side_l_pane_layout_id, e=True, ps=[2, 99, 100])

            if self.__check_frame_layout(this_side_r_layout_id):

                cmds.paneLayout(
                    this_side_r_pane_layout_id, e=True, ps=[1, 99, 100])

            if not self.__check_frame_layout(this_body_layout_id):

                cmds.scrollLayout(
                    this_scroll_layout_id, e=True, vis=False)

                if not self.__check_frame_layout(this_side_l_layout_id) and not self.__check_frame_layout(this_side_r_layout_id):

                    cmds.paneLayout(
                        this_side_l_pane_layout_id, e=True, vis=False)

                    cmds.paneLayout(
                        this_side_r_pane_layout_id, e=True, vis=False)

        self.__execute_show_function()

        cmds.showWindow(self.ui_window_id)

    # ===============================================
    def close(self):

        base_utility.ui.window.remove_same_id_window(self.ui_window_id)

    # ===============================================
    def __check_frame_layout(self, ui_id):

        if not ui_id:
            return False

        if cmds.frameLayout(ui_id, q=True, nch=True) != 0:
            return True

        cmds.frameLayout(ui_id, e=True, vis=False)

        return False

    # ===============================================
    def __execute_show_function(self):

        if not self.__show_function:
            return

        self.__show_function(*self.__show_function_arg)

    # ===============================================
    def set_show_function(self, function, *arg):

        self.__show_function = function
        self.__show_function_arg = arg

    # ===============================================
    def __execute_close_function(self):

        self.__kill_all_job()

        if not self.__close_function:
            return

        self.__close_function(*self.__close_function_arg)

    # ===============================================
    def set_close_function(self, function, *arg):

        self.__close_function = function
        self.__close_function_arg = arg

    # ===============================================
    def set_job(self, event_or_conditon_name, function, *arg):

        if not event_or_conditon_name:
            return

        # EventなのかConditonなのかの割り出し
        name_exist = False
        is_event = False

        event_list = cmds.scriptJob(listEvents=True)

        if event_or_conditon_name in event_list:
            is_event = True
            name_exist = True

        contidion_list = cmds.scriptJob(listConditions=True)

        if event_or_conditon_name in contidion_list:
            is_event = False
            name_exist = True

        if not name_exist:
            return

        if not function:
            return

        # ジョブメソッドの登録
        if not self.__job_function_list:
            self.__job_function_list = []
            self.__job_function_arg_list = []

        self.__job_function_list.append(function)
        self.__job_function_arg_list.append(arg)

        # ScriptJobへの登録
        this_index = len(self.__job_function_list) - 1
        this_job = None

        if is_event:
            this_job = cmds.scriptJob(
                event=[event_or_conditon_name, partial(self.__execute_job_function, this_index)], protected=True)
        else:
            this_job = cmds.scriptJob(
                conditionTrue=[event_or_conditon_name, partial(self.__execute_job_function, this_index)], protected=True)

        if not this_job:
            return

        if not self.__job_list:
            self.__job_list = []

        self.__job_list.append(this_job)

    # ===============================================
    def __kill_all_job(self):

        if not self.__job_list:
            return

        for job in self.__job_list:

            cmds.scriptJob(kill=job, force=True)

    # ===============================================
    def __execute_job_function(self, index):

        if not self.__job_function_list:
            return

        if index >= len(self.__job_function_list):
            return

        if not self.__job_function_list[index]:
            return

        self.__job_function_list[index](*self.__job_function_arg_list[index])

    # ===============================================
    def apply_window_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'window', self.ui_window_id, **param)

        return return_value

    # ===============================================
    def load_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_width = setting.load(setting_key + '_Width', int)
        this_height = setting.load(setting_key + '_Height', int)
        this_left = setting.load(setting_key + '_Left', int)
        this_top = setting.load(setting_key + '_Top', int)

        if this_width and this_width > 10:
            self.apply_window_param(e=True, width=this_width)

        if this_height and this_height > 10:
            self.apply_window_param(e=True, height=this_height)

        if this_left and this_left > 10:
            self.apply_window_param(e=True, leftEdge=this_left)

        if this_top and this_top > 10:
            self.apply_window_param(e=True, topEdge=this_top)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_width = self.apply_window_param(q=True, width=True)
        this_height = self.apply_window_param(q=True, height=True)
        this_left = self.apply_window_param(q=True, leftEdge=True)
        this_top = self.apply_window_param(q=True, topEdge=True)

        setting.save(setting_key + '_Width', this_width)
        setting.save(setting_key + '_Height', this_height)
        setting.save(setting_key + '_Left', this_left)
        setting.save(setting_key + '_Top', this_top)
