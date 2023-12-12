# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from shr.cutscene import utility

from maya import cmds


class StoryboardRenderSettings(utility.qt.QtSettings):
    def __init__(self, file_name):
        super(StoryboardRenderSettings, self).__init__("CutsceneEditor_Storyboard", file_name)

    def save_settings(self, tool_widgets, tool_save_widgets_list):
        self.tool_setting.clear()

        first_clip_list_count = tool_widgets.gui.firstClipList.count()

        self.tool_setting.beginWriteArray(tool_widgets.gui.firstClipList.objectName())
        for count in range(1, first_clip_list_count):
            self.tool_setting.setArrayIndex(count - 1)

            item = tool_widgets.gui.firstClipList.item(count)
            item_widgets = tool_widgets.gui.firstClipList.itemWidget(item)

            self.tool_setting.setValue("frame", item_widgets.gui.frame.value())
            self.tool_setting.setValue("clipName", item_widgets.gui.clipName.text())
            self.tool_setting.setValue("isRender", item_widgets.gui.isRender.isChecked())
        self.tool_setting.endArray()

        custom_clip_list_count = tool_widgets.gui.customClipList.count()
        self.tool_setting.beginWriteArray(tool_widgets.gui.customClipList.objectName())
        for count in range(1, custom_clip_list_count):
            self.tool_setting.setArrayIndex(count - 1)

            item = tool_widgets.gui.customClipList.item(count)
            item_widgets = tool_widgets.gui.customClipList.itemWidget(item)

            self.tool_setting.setValue("frame", item_widgets.gui.frame.value())
            self.tool_setting.setValue("clipName", item_widgets.gui.clipName.text())
            self.tool_setting.setValue("isRender", item_widgets.gui.isRender.isChecked())

        self.tool_setting.endArray()

        super(StoryboardRenderSettings, self).save_settings(tool_save_widgets_list)

    def load_list_widget_value(self, list_widgets):
        size = self.tool_setting.beginReadArray(list_widgets.objectName())
        list_widgets_value_list = []
        for i in range(size):
            self.tool_setting.setArrayIndex(i)
            data = dict()
            data["name"] = self.tool_setting.value("clipName")
            data["frame"] = float(self.tool_setting.value("frame"))
            data["isRender"] = bool(self.tool_setting.value("isRender"))

            list_widgets_value_list.append(data)
        self.tool_setting.endArray()
        return list_widgets_value_list
