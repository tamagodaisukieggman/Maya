# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from . import app
from . import view


class ViewController(object):
    GROUP_SUFFIX = "_group"
    AIM_SUFFIX = "_aim"

    CAM_SUFFIX = "_cam"

    def __init__(self):
        self.ui = view.View()

        self.setup_event()

    def setup_event(self):
        self.ui.gui.closeButton.clicked.connect(self.close_option)
        self.ui.gui.startRenameButton.clicked.connect(self.clicked_start_rename_button)
        self.ui.gui.applyButton.clicked.connect(self.clicked_apply_button)

        self.ui.gui.shotName.textChanged.connect(self.changed_shot_name_and_number)
        self.ui.gui.shotNumber.textChanged.connect(self.changed_shot_name_and_number)

    def show_option(self):
        self.ui.show()

    def close_option(self):
        self.ui.close()

    def clicked_apply_button(self):
        self.ui.save()
        name_prefix = self.ui.gui.shotName.text()
        number = self.ui.gui.shotNumber.text()

        is_rename_camera = self.ui.gui.is_rename_camera.isChecked()
        self.exec_rename(name_prefix, number, is_rename_camera)

    def exec_rename(self, name_prefix, number, is_rename_camera):
        group_suffix = self.GROUP_SUFFIX
        aim_suffix = self.AIM_SUFFIX
        cam_suffix = self.CAM_SUFFIX

        app.ShotRenamer(name_prefix, number, group_suffix, aim_suffix, cam_suffix, is_rename_camera)._exec()
        self.changed_shot_name_and_number()

    def clicked_start_rename_button(self):
        self.clicked_apply_button()
        self.close_option()

    def changed_shot_name_and_number(self):
        shot_name_text = self.ui.gui.shotName.text()
        shot_number_text = self.ui.gui.shotNumber.text()

        if shot_name_text and shot_number_text:
            result = shot_name_text + shot_number_text
            self.ui.gui.previewText.setText(result)
