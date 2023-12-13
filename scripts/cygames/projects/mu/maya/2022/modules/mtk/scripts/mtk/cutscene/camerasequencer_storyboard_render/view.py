# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from PySide2.QtWidgets import QMainWindow, QListWidgetItem
from PySide2.QtCore import Qt, QSize

from .ui import storyBoadrdRenderOption
from . import list_item_view
from . import settings


class View(MayaQWidgetBaseMixin, QMainWindow):

    def __init__(self, setting_name, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)

        self.gui = storyBoadrdRenderOption.Ui_StoryboardPatchRenderWindow()
        self.gui.setupUi(self)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.settings = settings.StoryboardRenderSettings(setting_name)
        self.settings_save_ui_list = [
            self.gui.isOutline,
            self.gui.isOpenExplorer,
            self.gui.isSceneName,
            self.gui.isFocalLength,
            self.gui.isCutName,
            self.gui.isFrame,
            self.gui.width,
            self.gui.height,
            self.gui.directory
        ]

    def save(self):
        self.settings.save_settings(self, self.settings_save_ui_list)
        self.settings.save_geometry(self)

    def load(self):
        self.settings.load_geometry(self)

        # self.gui.firstClipList.clear()
        # self.insert_item_to_list_widget(self.gui.firstClipList, list_item_view.ListWigetItemCheckABoxView())

        first_clip_value_list = self.settings.load_list_widget_value(self.gui.firstClipList)
        if not first_clip_value_list:
            return

        for value_info in first_clip_value_list:
            insert_view = self.insert_item_to_list_widget(self.gui.firstClipList, list_item_view.ListWigetItemView())
            insert_view.gui.clipName.setText(value_info["name"])
            insert_view.gui.frame.setValue(value_info["frame"])
            insert_view.gui.isRender.setChecked(value_info["isRender"])

        # self.gui.customClipList.clear()
        # self.insert_item_to_list_widget(self.gui.customClipList, list_item_view.ListWigetItemCheckABoxView())

        custom_clip_value_list = self.settings.load_list_widget_value(self.gui.customClipList)
        if not custom_clip_value_list:
            return

        for value_info in custom_clip_value_list:
            insert_view = self.insert_item_to_list_widget(self.gui.customClipList, list_item_view.ListWigetItemView())
            insert_view.gui.clipName.setText(value_info["name"])
            insert_view.gui.frame.setValue(value_info["frame"])
            insert_view.gui.isRender.setChecked(value_info["isRender"])

        self.settings.load_settings(self.settings_save_ui_list)

    def load_in_dict(self):
        return self.settings.load_in_dict(self.settings_save_ui_list)

    def showEvent(self, event):
        self.load()
        super(View, self).showEvent(event)

    def closeEvent(self, event):
        self.save()
        super(View, self).closeEvent(event)

    def insert_item_to_list_widget(self, insert_list_widget, insert_widget):
        new_items = QListWidgetItem()
        new_items.setSizeHint(QSize(50, 28))

        insert_list_widget.addItem(new_items)

        insert_list_widget.setItemWidget(new_items, insert_widget)
        return insert_widget
