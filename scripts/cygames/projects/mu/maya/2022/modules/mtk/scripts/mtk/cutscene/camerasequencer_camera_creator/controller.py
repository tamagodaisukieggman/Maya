# -*- coding: utf-8 -*-
"""SettingsViewのControllerモジュール"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function
from . import view
from . import app
from . import sequencer


class SettingsViewController(object):
    def __init__(self):
        self.ui = view.View()

        self.setup_event()

    def setup_event(self):
        self.ui.gui.closeButton.clicked.connect(self.close_option)
        self.ui.gui.createCameraButton.clicked.connect(self.clicked_create_camera_button)
        self.ui.gui.applyButton.clicked.connect(self.clicked_apply_button)

        self.ui.gui.shotName.textChanged.connect(self.changed_shot_name_and_number)
        self.ui.gui.shotNumber.textChanged.connect(self.changed_shot_name_and_number)

    def show_option(self):
        self.ui.show()

        self.changed_shot_name_and_number()

    def close_option(self):
        self.ui.close()

    def clicked_apply_button(self):
        self.ui.save()
        settings_dict = self.ui.load_in_dict()
        app.CutSceneCameraCreator(settings_dict).duplicate()
        self.changed_shot_name_and_number()

    def clicked_create_camera_button(self):
        self.clicked_apply_button()
        self.close_option()

    def changed_shot_name_and_number(self):
        shot_name_text = self.ui.gui.shotName.text()
        shot_number_text = self.ui.gui.shotNumber.text()

        if shot_name_text and shot_number_text:
            result = sequencer.CameraSequencerController.create_unique_shot_name(shot_name_text, shot_number_text)
            self.ui.gui.previewText.setText(result)
