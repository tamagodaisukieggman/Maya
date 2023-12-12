# -*- coding: utf-8 -*-
"""SettingsViewのControllerモジュール"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os
import functools

from . import view
from . import app
from mtk.cutscene.utility.dialog import select_folder


class SettingsViewController(object):
    def __init__(self, target_view):
        self.ui = view.View()
        self.__target_view = target_view

        self.setup_type_ui()
        self.setup_event()

    def setup_type_ui(self):
        setting_dict = self.ui.load_in_dict()
        default_format_index = setting_dict["formatType"]

        format_list = app.get_playblast_format()
        self.ui.gui.formatType.addItems(format_list)

        format_name = format_list[default_format_index]
        compression_list = app.get_playblast_compression(format_name)
        self.ui.gui.encodingType.addItems(compression_list)

        self.ui.load()

    def setup_event(self):
        self.ui.gui.closeButton.clicked.connect(self.close_option)
        self.ui.gui.startPlayblastButton.clicked.connect(self.clicked_create_camera_button)
        self.ui.gui.applyButton.clicked.connect(self.clicked_apply_button)
        self.ui.gui.formatType.currentIndexChanged.connect(self.current_change_format_type)

        self.ui.gui.openFolderButton.clicked.connect(self.open_folder_button)

        self.ui.gui.quality.valueChanged.connect(functools.partial(self.value_changed_callback,
                                                                   self.ui.gui.quality,
                                                                   self.ui.gui.qualitySlider))
        self.ui.gui.qualitySlider.valueChanged.connect(functools.partial(self.value_changed_callback,
                                                                         self.ui.gui.qualitySlider,
                                                                         self.ui.gui.quality))

        self.ui.gui.resolutionWidth.valueChanged.connect(functools.partial(self.value_changed_callback,
                                                                           self.ui.gui.resolutionWidth,
                                                                           self.ui.gui.resolutionWidthSlider))
        self.ui.gui.resolutionWidthSlider.valueChanged.connect(functools.partial(self.value_changed_callback,
                                                                                 self.ui.gui.resolutionWidthSlider,
                                                                                 self.ui.gui.resolutionWidth))

        self.ui.gui.resolutionHeight.valueChanged.connect(functools.partial(self.value_changed_callback,
                                                                            self.ui.gui.resolutionHeight,
                                                                            self.ui.gui.resolutionHeightSlider))
        self.ui.gui.resolutionHeightSlider.valueChanged.connect(functools.partial(self.value_changed_callback,
                                                                                  self.ui.gui.resolutionHeightSlider,
                                                                                  self.ui.gui.resolutionHeight))

        self.ui.gui.modeType.currentIndexChanged.connect(self.mode_type_changed_callback)

        self.ui.gui.fileName.textChanged.connect(self.changed_file_name_and_number)
        self.ui.gui.fileNumber.textChanged.connect(self.changed_file_name_and_number)
        self.ui.gui.IsFileOverride.stateChanged.connect(self.changed_file_name_and_number)
        self.ui.gui.directory.textChanged.connect(self.changed_file_name_and_number)
        self.ui.gui.encodingType.currentIndexChanged.connect(self.changed_file_name_and_number)

    def show_option(self):
        self.ui.show()
        self.changed_file_name_and_number()

    def close_option(self):
        self.ui.close()

    def clicked_apply_button(self):
        self.ui.save()
        setttings = self.ui.load_in_dict()
        app.CutScenePlayBlastExecutor(self.__target_view, setttings).start_playblast()

        self.changed_file_name_and_number()

    def clicked_create_camera_button(self):
        self.clicked_apply_button()
        self.close_option()

    def current_change_format_type(self):
        format_list = app.get_playblast_format()

        target_format_name = format_list[self.ui.gui.formatType.currentIndex()]
        self.ui.gui.encodingType.clear()

        self.ui.gui.encodingType.addItems(app.get_playblast_compression(target_format_name))

    def open_folder_button(self):
        target_path = select_folder()
        if target_path != "":
            self.ui.gui.directory.setText(target_path)

    def value_changed_callback(self, src, dist, *args):
        value = src.value()

        dist.blockSignals(True)

        dist.setValue(value)

        dist.blockSignals(False)

    def mode_type_changed_callback(self):
        if self.ui.gui.modeType.currentIndex() != 2:
            self.ui.gui.startTime.setEnabled(False)
            self.ui.gui.startTimeLabel.setEnabled(False)

            self.ui.gui.endTime.setEnabled(False)
            self.ui.gui.endTimeLabel.setEnabled(False)
        else:
            self.ui.gui.startTime.setEnabled(True)
            self.ui.gui.startTimeLabel.setEnabled(True)

            self.ui.gui.endTime.setEnabled(True)
            self.ui.gui.endTimeLabel.setEnabled(True)

    def changed_file_name_and_number(self):
        self.ui.save()

        file_name_text = self.ui.gui.fileName.text()
        file_number_text = self.ui.gui.fileNumber.text()

        if file_name_text and file_number_text:
            settings_dict = self.ui.load_in_dict()
            result = app.PlayBlastSettingsFormater(settings_dict).create_file_full_path()

            self.ui.gui.previewText.setText(os.path.basename(result))
