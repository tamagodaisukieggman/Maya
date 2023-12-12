# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import functools


from maya import cmds

from . import app
from . import view, list_item_view, render
from mtk.cutscene.utility.dialog import select_folder


class ViewController(object):

    def __init__(self):
        self.storyboard_render = app.StorybardRender()

        self.ui = view.View(self.storyboard_render.get_scene_name())

        self.first_clip_list_checkbox_widgets = None
        self.custom_clip_list_checkbox_widgets = None

        self.setup_event()

    def setup_event(self):
        self.ui.gui.AddcustomClipListButton.clicked.connect(self.add_custom_clip_list_button)
        self.ui.gui.removeCustomClipListButton.clicked.connect(self.remove_custom_clip_list_button)
        self.ui.gui.updateButton.clicked.connect(self.clicked_update_button)
        self.ui.gui.applyButton.clicked.connect(self.clicked_apply_button)
        self.ui.gui.startCurrentFrameRendering.clicked.connect(self.start_render_from_current_frame_button)
        self.ui.gui.closeButton.clicked.connect(self.close_option)
        self.ui.gui.startRenderButton.clicked.connect(self.start_render_button)
        self.ui.gui.openFolderButton.clicked.connect(self.open_folder_button)

        self.add_checkbox_event_from_first_clip_list()
        self.add_checkbox_event_from_custom_clip_list()

    def add_checkbox_event_from_first_clip_list(self):
        self.first_clip_list_checkbox_widgets = self.ui.insert_item_to_list_widget(self.ui.gui.firstClipList, list_item_view.ListWigetItemCheckABoxView())

        self.first_clip_list_checkbox_widgets.gui.checkBox.stateChanged.connect(functools.partial(self.change_check_box_event,
                                                                                                  self.first_clip_list_checkbox_widgets.gui.checkBox,
                                                                                                  self.ui.gui.firstClipList))

    def add_checkbox_event_from_custom_clip_list(self):
        self.custom_clip_list_checkbox_widgets = self.ui.insert_item_to_list_widget(self.ui.gui.customClipList, list_item_view.ListWigetItemCheckABoxView())

        self.custom_clip_list_checkbox_widgets.gui.checkBox.stateChanged.connect(functools.partial(self.change_check_box_event,
                                                                                                   self.custom_clip_list_checkbox_widgets.gui.checkBox,
                                                                                                   self.ui.gui.customClipList))

    def show_option(self):
        self.ui.show()

    def close_option(self):
        self.ui.close()

    def start_render_button(self):
        self.clicked_apply_button()

        self.close_option()

    def clicked_apply_button(self):
        """アプライボタンイベント
        """
        self.ui.save()

        render_frame_list = self.__correct_render_list()
        max_count = len(render_frame_list)
        current_time = cmds.sequenceManager(query=True, currentTime=True)
        for i, render_frame in enumerate(render_frame_list):
            settings = self.ui.load_in_dict()

            cmds.sequenceManager(currentTime=render_frame)

            if max_count - 1 == i:
                settings["isOpenExplorer"] = True
            else:
                settings["isOpenExplorer"] = False

            render.ArnoldDebugRender.render(settings)

        cmds.sequenceManager(currentTime=current_time)

    def clicked_update_button(self):
        """アップデートボタンイベント
        """
        self.ui.gui.firstClipList.clear()

        self.add_checkbox_event_from_first_clip_list()

        clip_info_list = self.storyboard_render.collect_clip_info_from_camerasequencer()
        for clip_info in clip_info_list:
            insert_view = self.ui.insert_item_to_list_widget(self.ui.gui.firstClipList, list_item_view.ListWigetItemView())
            insert_view.gui.clipName.setText(clip_info["name"])
            insert_view.gui.frame.setValue(clip_info["startTime"])

    def change_check_box_event(self, check_box, list_view, *args):
        """チェックボックス変更イベント
        """
        check = check_box.isChecked()
        clip_count = list_view.count()

        for _ in list(reversed(range(1, clip_count))):
            item = list_view.item(_)

            item_widgets = list_view.itemWidget(item)
            item_widgets.gui.isRender.setChecked(check)

    def add_custom_clip_list_button(self):
        """カスタムクリップリストに追加ボタン
        """
        clip_info = self.storyboard_render.collect_clip_info_from_camerasequencer_current_frame()

        if not clip_info:
            return

        insert_view = self.ui.insert_item_to_list_widget(self.ui.gui.customClipList, list_item_view.ListWigetItemView())
        insert_view.gui.clipName.setText(clip_info["name"])
        insert_view.gui.frame.setValue(clip_info["startTime"])

    def remove_custom_clip_list_button(self):
        """カスタムクリップリストの削除ボタン
        """
        selected_index = self.ui.gui.customClipList.currentRow()
        if selected_index == 0 or selected_index is None:
            return

        item = self.ui.gui.customClipList.takeItem(selected_index)
        del item

    def __correct_render_list(self):
        """レンダリングする対象を収集する

        :return: レンダリングする時間リスト
        :rtype: list
        """
        render_list = []
        first_clip_list_count = self.ui.gui.firstClipList.count()
        for count in range(1, first_clip_list_count):
            item = self.ui.gui.firstClipList.item(count)
            widgets = self.ui.gui.firstClipList.itemWidget(item)
            if widgets.gui.isRender.isChecked():
                render_list.append(widgets.gui.frame.text())

        custom_clip_list_count = self.ui.gui.customClipList.count()
        for count in range(1, custom_clip_list_count):
            item = self.ui.gui.customClipList.item(count)
            widgets = self.ui.gui.customClipList.itemWidget(item)
            if widgets.gui.isRender.isChecked():
                render_list.append(widgets.gui.frame.text())

        return render_list

    def start_render_from_current_frame_button(self):
        """カレントフレームのレンダリングボタン
        """
        self.ui.save()
        settings = self.ui.load_in_dict()
        render.ArnoldDebugRender.render(settings)

    def open_folder_button(self):
        target_path = select_folder()
        if target_path != "":
            self.ui.gui.directory.setText(target_path)
