"""Maya機能のCallback。外からはconnectとdisconnectのみ。"""
from __future__ import annotations

import typing as tp
from typing import TYPE_CHECKING

from cy.ed.timeline import utility
from maya import cmds, mel
from maya.api import OpenMaya as om
from maya.api import OpenMayaAnim as oa
from shr.cutscene.sequencer import const

from . import model
from .api import ClipStatus, Sequencer, SequencerClipData
from .maya_reference_controller import MayaReferenceController

if TYPE_CHECKING:
    from .controller import SequencerController


class MayaCallbackController(object):
    def __init__(self, sequencer: SequencerController) -> None:
        self.time_changed_callback = None
        self.keyframe_event = None
        self.playback_play_time_range_slider_callback = None
        self._sequencer = sequencer

    def connect(self):
        self._override_playback()
        self._connect_time_slider_mouse_moved()
        self._connect_maya_time_slider_changed()
        self._connect_maya_anim_keyframe_event()
        self._connect_maya_time_range_changed()

    def disconnect(self):
        om.MMessage.removeCallback(self.time_changed_callback)
        om.MMessage.removeCallback(self.keyframe_event)
        om.MMessage.removeCallback(self.playback_play_time_range_slider_callback)
        om.MMessage.removeCallback(self.playback_max_range_callback)

        self._disconnect_time_slider_mouse_moved()
        # self._disable_override_playback()

    # ======================================================================
    # カレントフレーム同期
    # ======================================================================
    def _connect_time_slider_mouse_moved(self):
        """シーケンサーのTimeSliderマウス移動イベント
        """
        ...
        self._sequencer._signals.time_slider_mouse_moved.connect(self._time_slider_mouse_moved)

    def _time_slider_mouse_moved(self, frame, *args):
        cmds.currentTime(frame, edit=True)

    def _disconnect_time_slider_mouse_moved(self):
        """シーケンサーのTimeSliderマウス移動イベント解除
        """
        ...
        self._sequencer._signals.time_slider_mouse_moved.disconnect(self._time_slider_mouse_moved)

    def _connect_maya_time_slider_changed(self):
        """Mayaの時間変更イベント
        """
        self.time_changed_callback = om.MEventMessage.addEventCallback("timeChanged", self._set_current_frame)

    def _set_current_frame(self, *args):
        """カレントフレームの同期
        """
        current_frame = model.MayaTimeConfig.get_current_time()
        self._sequencer.set_maya_time_slider(current_frame)

    # ======================================================================
    # Keyframe同期
    # ======================================================================
    def _connect_maya_anim_keyframe_event(self):
        """KeyFrame変更イベント
        """
        self.keyframe_event = oa.MAnimMessage.addAnimKeyframeEditedCallback(self._keyframe_event)

    def _keyframe_event(self, *args):
        """Keyframeを入力した時のCallback通知
        """
        ref_node_list = MayaReferenceController().get_ref_path_from_selected_node()
        if not ref_node_list:
            return

        clips: tp.List[SequencerClipData] = self._sequencer.get_all_clips()

        for ref_node in ref_node_list:
            for clip in clips:
                clip_property = clip.get_clip_property()
                reference_path = clip_property[const.Event.EVENT_REFERENCE_PATH]
                if ref_node == reference_path:
                    clip.set_status(ClipStatus.Edit)

    # ======================================================================
    # TimeRange同期
    # ======================================================================
    def _connect_maya_time_range_changed(self):
        """MayaのTimeLine変更イベント
        """
        self.playback_play_time_range_slider_callback = om.MEventMessage.addEventCallback("playbackRangeChanged", self._update_min_max_time)

        self.playback_max_range_callback = om.MEventMessage.addEventCallback("playbackRangeSliderChanged", self._update_animation_time)

    def _update_min_max_time(self, *args):
        """minTime, maxTimeの変更イベント
        """
        controller = self._sequencer._timeline_view.get_controller()
        min_time = cmds.playbackOptions(query=True, minTime=True)
        max_time = cmds.playbackOptions(query=True, maxTime=True)

        seq_play_time = controller.play_range_in_frame
        if min_time != seq_play_time[0] or max_time != seq_play_time[1]:
            controller.set_track_play_bounds(utility.frame_to_sec(min_time),
                                             utility.frame_to_sec(max_time))

    def _update_animation_time(self, *args):
        """animationStartTime, animationEndTimeの更新イベント
        """
        controller = self._sequencer._timeline_view.get_controller()
        animation_min_time = cmds.playbackOptions(query=True, animationStartTime=True)
        animation_max_time = cmds.playbackOptions(query=True, animationEndTime=True)

        seq_length_time = controller.timeline_length

        if animation_max_time != seq_length_time:
            controller.set_timeline_length(animation_max_time)

    # ======================================================================
    # Playback
    # ======================================================================
    def _override_playback(self):
        """プレイバックウィジェットを上書きする
        TODO: 本来はPlaybackWidgetが取り外し可能になっていて、それを差し替える事で実現できる方が良い。
        しかし、現状厳しいので、生成後に上書きする。
        """
        # self._disable_playback_signal() コントローラー側でシグナル切断済み
        self._override_playback_signal()
        ...

    def _override_playback_signal(self):
        timeline_view = self._sequencer._timeline_view
        playback_panel = timeline_view._playback_panel
        playback_panel.play_button.toggled.connect(self._push_maya_play_button)
        playback_panel.forward_button.clicked.connect(self._override_maya_forward_time)
        playback_panel.backward_button.clicked.connect(self._override_maya_backward_time)
        playback_panel.skip_forward_button.clicked.connect(self._push_maya_forward_button)
        playback_panel.skip_backward_button.clicked.connect(self._push_maya_backward_button)

        timeline_view.get_controller().track_play_bounds_changed.connect(self._update_maya_playrange)

    def _push_maya_play_button(self, is_checked, *args):
        cmds.play(state=is_checked)

    def _override_maya_forward_time(self, *args):
        max_time = cmds.playbackOptions(query=True, maxTime=True)
        cmds.currentTime(max_time, edit=True)
        self._sequencer._time_ctrl.set_current_frame(max_time)

    def _override_maya_backward_time(self, *args):
        min_time = cmds.playbackOptions(query=True, minTime=True)
        cmds.currentTime(min_time, edit=True)
        self._sequencer._time_ctrl.set_current_frame(min_time)

    def _push_maya_forward_button(self, *args):
        mel.eval("NextFrame;")

    def _push_maya_backward_button(self, *args):
        mel.eval("playButtonStepBackward")

    def _update_maya_playrange(self, *args):
        play_range = self._sequencer._timeline_view.get_controller().play_range_in_frame

        cmds.playbackOptions(edit=True, minTime=play_range[0])
        cmds.playbackOptions(edit=True, maxTime=play_range[1])

        maya_animation_max_time = cmds.playbackOptions(query=True, animationEndTime=True)

        if play_range[1] >= maya_animation_max_time:
            ...
        else:
            max_frame = self._sequencer._timeline_view.get_controller().timeline_length_by_frame
            cmds.playbackOptions(edit=True, animationEndTime=max_frame)
