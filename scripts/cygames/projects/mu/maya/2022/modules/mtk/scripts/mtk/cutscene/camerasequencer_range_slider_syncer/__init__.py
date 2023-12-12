# -*- coding: utf-8 -*-
"""カメラシーケンサーと他エディターを同期する機能"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya import cmds

from . import app

from .. import utility
from .. import range_slider_panel_width_syncer

instance_syncer = None
event_call_back_register = None


def start_sync():
    global instance_syncer
    global event_call_back_register

    end_sync()

    if instance_syncer is None:
        instance_syncer = app.CameraSequencerRangeSliderSyncer()

        camera_sequencer_panel = cmds.getPanel(withLabel="Camera Sequencer")

        if event_call_back_register is None:
            event_call_back_register = utility.qt.PanelInMouseLoopEventCallbackRegister(camera_sequencer_panel, instance_syncer.sync__time_editor_time_range__from_camera_sequencer, range_slider_panel_width_syncer.start_sync)
            event_call_back_register.set_event()


def end_sync():
    global instance_syncer
    global event_call_back_register
    if instance_syncer is not None:
        instance_syncer = None

    if event_call_back_register is not None:
        event_call_back_register.remove_event()
        event_call_back_register = None
