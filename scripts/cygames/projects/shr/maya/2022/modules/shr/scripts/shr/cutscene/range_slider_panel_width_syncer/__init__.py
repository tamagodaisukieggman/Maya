# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from functools import partial

from maya import cmds, mel

from . import app
from .. import utility

instance_syncer = None
graph_editor_event_call_back_register = None
dope_sheet_event_call_back_register = None

# 基本的に冪等性確保の為に何度Syncを実行しても問題ない様にしている。
# 拡張機能有効時に一回
# カメラシーケンサーにカーソルを合わせた時に50フレームごとに再登録している。


def start_sync():
    global instance_syncer
    global graph_editor_event_call_back_register
    global dope_sheet_event_call_back_register

    end_sync()

    if instance_syncer is None:
        instance_syncer = app.CameraSequencerRangeSliderSyncer()

        graph_editor_panel = cmds.getPanel(withLabel="Graph Editor")
        dope_sheet_panel = cmds.getPanel(withLabel="Dope Sheet")

        if graph_editor_event_call_back_register is None:
            graph_editor_event_call_back_register = utility.qt.PanelInMouseLoopEventCallbackRegister(graph_editor_panel, partial(instance_syncer.sync, graph_editor_panel, dope_sheet_panel), None, 10)
            graph_editor_event_call_back_register.set_event()

        if dope_sheet_event_call_back_register is None:
            dope_sheet_event_call_back_register = utility.qt.PanelInMouseLoopEventCallbackRegister(dope_sheet_panel, partial(instance_syncer.sync, dope_sheet_panel, graph_editor_panel), None, 10)
            dope_sheet_event_call_back_register.set_event()


def end_sync():
    global instance_syncer
    global graph_editor_event_call_back_register
    global dope_sheet_event_call_back_register

    if instance_syncer is not None:
        instance_syncer = None

    if graph_editor_event_call_back_register is not None:
        graph_editor_event_call_back_register.remove_event()
        graph_editor_event_call_back_register = None

    if dope_sheet_event_call_back_register is not None:
        dope_sheet_event_call_back_register.remove_event()
        dope_sheet_event_call_back_register = None
