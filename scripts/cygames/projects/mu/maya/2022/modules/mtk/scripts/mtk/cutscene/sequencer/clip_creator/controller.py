from __future__ import annotations

import typing as tp

from mtk.cutscene.sequencer import const
from mtk.cutscene.sequencer.controller import SequencerController
from mtk.cutscene.utility.dialog import show_error_dialog

from ..api import sequencer_api
from ..config import ActorConfig
from ..lib.time import fetch_file_updated_time
from ..maya_clip_editor import MayaMotionClipEditor
from ..maya_reference_controller import MayaReferenceController
from . import app, view


class InsertAnimationController(object):
    def __init__(self):
        self.ui = view.View()
        self._sequencer = SequencerController.get_instance()

        self._track_data = None
        self._group_item = None
        self._group_data = None
        self._actor_config = None

        self._track_type = None

        self.setup_event()
        self.update_selected_track()
        self.change_ui()

    def setup_event(self):
        self.ui.gui.close_button.clicked.connect(self.close_option)
        self.ui.gui.ok_button.clicked.connect(self.clicked_ok_button)
        self.ui.gui.apply_button.clicked.connect(self.clicked_apply_button)
        self.ui.gui.dialog_button.clicked.connect(self.clicked_dialog_button)

    def update_selected_track(self):
        self._track_data: sequencer_api.SequencerTrack = self._sequencer.get_selected_track_data()
        self._group_item: sequencer_api.TimelineGroupItem = self._sequencer.get_selected_track_item().parent()
        self._group_data: sequencer_api.SequencerGroupTrackData = self._group_item.track_data()

        group_property = self._group_data.get_property()
        self._actor_config_path = group_property[const.Event.GROUP_ACTOR_CONFIG_PATH]
        self._screen_writer = group_property[const.Event.GROUP_SCREEN_WRITER_PATH]
        self._reference_node = group_property[const.Event.GROUP_REFERENCE_PATH]

        self._actor_config = ActorConfig(self._actor_config_path)

        self._track_type = self._track_data.track_type()

    def show_option(self):
        self.change_clip_name("")
        self.ui.show()

    def close_option(self):
        self.ui.close()

    def change_ui(self):
        self.ui.gui.camera_type_widget.setHidden(False)
        self.ui.gui.time_widget.setHidden(False)
        self.ui.gui.import_file_widget.setHidden(False)

        if self._track_type == sequencer_api.TrackType.Motion:
            self.ui.gui.camera_type_widget.setHidden(True)
            self.ui.gui.time_widget.setHidden(True)
        elif self._track_type == sequencer_api.TrackType.Camera:
            self.ui.gui.import_file_widget.setHidden(True)
            self.update_camera_type()

        self.ui.adjustSize()
        ...

    def update_camera_type(self):
        self.ui.gui.camera_type_combo_box.clear()
        path = self._actor_config.data.recommended_animation_path
        file_list = app.collect_files(path)
        name_list = app.collect_file_basenames(file_list)
        self.ui.gui.camera_type_combo_box.addItems(name_list)

    def clicked_ok_button(self):
        self.clicked_apply_button()
        self.close_option()

    def clicked_apply_button(self):
        self.update_selected_track()
        if not isinstance(self._group_data, sequencer_api.GroupTrackData):
            return

        clip_name = self.ui.gui.clip_name.text()
        path = self.collect_import_path()
        try:
            insert_animator = app.InsertAnimator(self._actor_config.data, self._screen_writer)
            motion_ref_name, index = insert_animator.connect_animation(clip_name, path)

        except ValueError as e:
            show_error_dialog("重複エラー", f"{e}\n{clip_name}が重複しています。\n別のクリップ名を利用してください。")
            return

        # 整合性取れなかったらダイアログ出して終了させる
        if not self.check_consistency(self._reference_node, motion_ref_name, insert_animator):
            return

        frame_range = self.collect_frame_range(motion_ref_name)

        MayaMotionClipEditor.move_clip(motion_ref_name, frame_range[2])
        updated = fetch_file_updated_time(motion_ref_name)
        self._sequencer._maya_signals.created_event_motion.emit(self._track_data,
                                                                frame_range,
                                                                clip_name,
                                                                index,
                                                                motion_ref_name,
                                                                updated)

    def clicked_dialog_button(self):
        path = app.open_dialog(self._actor_config.data.recommended_animation_path)

        if path:
            self.ui.gui.file_path.setText(path[0])

    def change_clip_name(self, clip_name=""):
        if clip_name == "":
            self.ui.gui.clip_name.setText(self._actor_config.data.recommended_name)
        else:
            self.ui.gui.clip_name.setText(clip_name)

    def collect_import_path(self) -> str:
        if self._track_type == sequencer_api.TrackType.Camera:
            select_camera_type_index = self.ui.gui.camera_type_combo_box.currentIndex()
            dir_path = self._actor_config.data.recommended_animation_path
            file_list = app.collect_files(dir_path)
            path = file_list[select_camera_type_index]

        elif self._track_type == sequencer_api.TrackType.Motion:
            path = self.ui.gui.file_path.text()

        return path

    def collect_frame_range(self, motion_ref_name) -> tp.Tuple[float, float, float] | tp.Tuple[float, float, float, float, float]:
        if self._track_type == sequencer_api.TrackType.Camera:
            frame_range = (self.ui.gui.startTime.value(), self.ui.gui.endTime.value(), 0)
        elif self._track_type == sequencer_api.TrackType.Motion:
            frame_range = MayaMotionClipEditor.get_clip_range(motion_ref_name)

        return frame_range

    def check_consistency(self, actor_ref, motion_ref, insert_animator: app.InsertAnimator):
        """整合性確認
        整合性取れなかったらダイアログを表示する

        Returns:
            bool: 整合性が取れるかどうか
        """

        if not insert_animator.compare_actor_and_motion(actor_ref, motion_ref):
            MayaReferenceController().delete(motion_ref)
            show_error_dialog("整合性チェックエラー", f"{motion_ref}がアクターと整合性が取れない為、読み込みに失敗しました。")
            return False

        return True
