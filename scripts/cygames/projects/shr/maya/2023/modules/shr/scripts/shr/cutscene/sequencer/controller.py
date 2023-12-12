# -*- coding: utf-8 -*-
"""シーケンサーのcontroller
"""
from __future__ import annotations

import os

from attr import has
from shr.cutscene.sequencer.create_camera.app import CameraCreator
from shr.cutscene.sequencer.lib.event import (is_camera_track, is_motion_track,
                                              is_sequencer_track)
from shr.utils import getCurrentSceneFilePath

from . import (clip_creator, const, create_actor, model, outliner,
               property_editor, view)
from .api import *
from .lib import reference, utility
from .lib.time import fetch_now_time
from .maya_callback import MayaCallbackController
from .maya_clip_editor import MayaMoveClipMoveDelayTimer
from .maya_reference_controller import MayaReferenceController
from .maya_reference_node_selector import ReferenceNodeSelector
from .maya_reference_visible_selector import ReferenceVisibleSelector
from .screen_writer import ScreenWriterConnector, ScreenWriterManager
from .sequencer_data import SequencerJsonDataClient


class SequencerController(Sequencer):
    __instance = None

    def __init__(self) -> None:
        self._main_window: view.MainWindow = view.MainWindow()
        self._main_window.set_sequencer_ctrl(self)
        self._main_window.init_menu_ui()
        self._maya_signals = MayaSequencerSignals.get_instance()

        super().__init__(self._main_window.timeline_view)
        self.set_time_slider_app_type(ApplicationType.Maya)
        self.get_timeline_view_widget().disable_playback_signal()

        self._animation_calculator = model.MayaAnimationClipCalculator()
        self._maya_callback = MayaCallbackController(self)
        self._maya_clip_move_timer = MayaMoveClipMoveDelayTimer()

        self._main_window.closed.connect(self.view_closed)
        self._main_window.camera_add_button.clicked.connect(self.create_camera_actor)
        self._main_window.actor_add_button.clicked.connect(self.show_create_actor)
        self._main_window.anim_add_button.clicked.connect(self.show_insert_clip)
        self._main_window.actor_only_enable_button.clicked.connect(self.show_default)
        self._main_window.show_only_selected_clip_node_button.clicked.connect(self.show_only_selected_clip_node)

        self._timeline_view.get_tree_view().set_edit_dialog_func(self.show_maya_property_editor)

        self._maya_signals.created_group_actor.connect(self.add_actor_group)
        self._maya_signals.created_event_motion.connect(self.insert_sequencer_clip_data)

        ScreenWriterManager.check_plugin()

    def show_maya_property_editor(self):
        track_data = self.get_selected_track_data()

        property_editor.main(self._controller, track_data)

    @classmethod
    def get_instance(cls) -> SequencerController:
        if cls.__instance is None:
            cls.__instance = SequencerController()
        return cls.__instance

    def show(self, auto_load=True):
        self._main_window.resize(800, 600)
        self.set_frame_from_maya_frame()

        self._maya_callback.connect()

        if not model.should_saving_scene():
            model.show_error_dialog("シーンが保存されていません。\nシーンを保存してSequencerを開いてください。")
            return

        self._main_window.show()

        if auto_load:
            scene_path = getCurrentSceneFilePath()
            if not scene_path:
                return

            scene_path_no_ext, _ = os.path.splitext(scene_path)
            seq_path = f"{scene_path_no_ext}.seq"

            if os.path.isfile(seq_path):
                self.load(seq_path)

    def close(self):
        self._main_window.close()

    def view_closed(self):
        self._maya_callback.disconnect()

    def create_track(self, name: str, event_type: str, group_item: TimelineGroupItem):

        if is_camera_track(event_type):
            track = CameraTrack(name)
            track.set_track_usage(ApplicationType.Maya)

        elif is_motion_track(event_type):
            track = MotionTrack(name)
            track.set_track_usage(ApplicationType.Maya)

        else:
            track = SoundTrack(name)
            track.set_track_usage(ApplicationType.Cyllista)

        return super().add_track(track, group_item)

    def create_sound_track(self, name: str, group=None) -> CameraTrack:
        """新規でカメラトラックを作成し、モデルに追加、そして作成されたトラックを返します。"""
        sound_track = SoundTrack(name)
        sound_track.set_track_usage(ApplicationType.Cyllista)
        return super().add_track(sound_track, group)

    def load(self, seq_file=None):
        if not seq_file:
            seq_file = model.show_import_file_dialog("seqファイルを選択してください", file_filter="*.seq")

        if not seq_file:
            return

        SequencerJsonDataClient.load(seq_file)

    def save(self, path=None):
        if not path:
            sequencer_file_path = SequencerJsonDataClient.create_default_sequencer_path()

        SequencerJsonDataClient.save(sequencer_file_path)
        print("save seq file")

        self.save_all_reference()
        print("save all reference")

        model.save_scene()
        print("save file.")

    def set_maya_time_slider(self, value):
        self._time_ctrl.set_current_frame(value)

    def set_frame_from_maya_frame(self):
        """MayaフレームからFrameを設定する"""
        min_frame = model.MayaTimeConfig.get_min_frame()
        start_frame = model.MayaTimeConfig.get_start_frame()
        max_frame = model.MayaTimeConfig.get_max_frame()
        end_frame = model.MayaTimeConfig.get_end_frame()
        self.set_timeline_length(end_frame)
        super().set_frame_range(start_frame, end_frame, min_frame, max_frame)

    def add_actor_group(self, name, event_type, screen_writer_path, actor_config_path, actor_file_path):
        if is_camera_track(event_type):
            group = self.find_group(name)
            if group:
                # 二個目以降は許可しない。
                return
            group = self.add_group_track(const.EVENT_TYPE_CAMERA, name)

        elif is_motion_track(event_type):
            group = self.add_group_track(const.EVENT_TYPE_MOTION, name)

        group_list = self.get_all_tracks()
        group_name_list = [_.display_name() for _ in group_list]
        track_name = utility.create_unique_name("track", group_name_list)

        self.create_track(track_name, event_type, group)

        group_data: SequencerGroupTrackData = group.track_data()
        group_property = group_data.get_property()
        group_property[const.Event.GROUP_SCREEN_WRITER_PATH] = screen_writer_path
        group_property[const.Event.GROUP_ACTOR_CONFIG_PATH] = actor_config_path
        group_property[const.Event.GROUP_REFERENCE_PATH] = actor_file_path

    def add_camera_group(self, name, event_type, screen_writer_path, actor_file_path):
        group = self.add_group_track(event_type, name)
        group_data: SequencerGroupTrackData = group.track_data()
        group_property = group_data.get_property()
        group_property[const.Event.GROUP_SCREEN_WRITER_PATH] = screen_writer_path
        group_property[const.Event.GROUP_REFERENCE_PATH] = actor_file_path

    def load_actor_group(self, name, event_type, screen_writer, actor_config_path, ref_path):
        group = self.add_group_track(event_type, name)
        group_data: SequencerGroupTrackData = group.track_data()
        group_property = group_data.get_property()
        group_property[const.Event.GROUP_SCREEN_WRITER_PATH] = screen_writer
        group_property[const.Event.GROUP_ACTOR_CONFIG_PATH] = actor_config_path
        group_property[const.Event.GROUP_REFERENCE_PATH] = ref_path
        return group

    def load_event_group(self, name, event_type):
        group = self.add_group_track(event_type, name)
        return group

    def insert_sequencer_clip_data(self,
                                   track: SequencerTrack,
                                   clip_parm: tp.Tuple[float, float, float, float, float],
                                   label,
                                   index,
                                   reference_path,
                                   updated):
        """
        トラックの種類を自動判別して、トラックに対応したクリップを追加
        clip_parm は次のようなタプル (start, end, start_offset, in, out), もしくは ClipParameters オブジェクトを想定。
        in, out のないカメラクリップではタプルの start, end さえあれば良いが、無駄に5つのパラメーターがあっても問題は無い。
        in, out 用のクリップのためにも、タプルを使う場合は最低 start, end, start_offset の3つの要素は必要である。
        ClipParameters オブジェクトは上記のタプルの様に[]にインデックスを付けてアクセス付けるので同等に扱える。
        """
        group = track.get_parent_group_track_data()
        event_type = group.get_event_type()
        clip = track.add_sequencer_clip(clip_parm, label, ClipStatus.Check)
        clip_property = clip.get_clip_property()
        clip.set_updated(updated)

        if is_sequencer_track(event_type):
            clip_property[const.Event.EVENT_NAME] = label
            clip_property[const.Event.EVENT_REFERENCE_PATH] = reference_path
            clip_property[const.Event.EVENT_SCREEN_WRITER_INDEX] = index
        else:
            # Eventトラックは何もプロパティを追加しない。
            ...
        return clip

    def insert_sequencer_clip_data_by_names(self, group_name, track_name, play_range, label, index, reference_node, updated):
        """
        グループ名とトラック名を指定してトラックを特定し、クリップを追加する。
        トラックの種類を自動判別して、トラックに対応したクリップを追加。
        """
        track = self._model.get_track_from_name(group_name, track_name)
        if not track:
            return

        group_data = track.get_parent_group_track_data()
        return track.add_sequencer_clip(play_range, label,
                                        index,
                                        reference_node,
                                        updated)

    def split_selected_clip(self):
        new_clips = super().split_selected_clip()

    # -----------------------------------------------------------------
    # SequencerCallback
    # -----------------------------------------------------------------

    def on_clip_double_clicked(self, data: SequencerClipData):
        """
        (override)
        トラックビューで Clip をダブルクリックされた際に呼び出される関数です。
        data にはクリックされた Clip のデータが渡されます。
        """
        if self._is_maya_clip_data(data):
            ReferenceNodeSelector(self).select(data)

    def on_motion_clip_evaluated(self, data: tp.Dict[SequencerGroupTrackData, tp.List[EvaluatedClip]]):
        """
        (override) 現在のフレームでの MotionClip と評価されたフレームがディクショナリ形式で渡されます。
        現在のフレームが変わるたびに毎回呼び出されます。
        """
        # TODO: 評価時に不要なデータをフィルタリングしてるが、少し非効率。screen_writerなどは無い物として来た方がわかりやすい。

        data = self.filter_evaluated_clip_data(data, ApplicationType.Maya)
        group_list = self.get_all_groups()
        screen_writer_list = [_.get_property()[const.Event.GROUP_SCREEN_WRITER_PATH] for _ in group_list if _.get_event_type() == "Camera" or _.get_event_type() == "Motion"]
        self._animation_calculator.calculate(screen_writer_list, data)

    def on_clip_moved(self, clip: MotionClipData, old_frame, new_frame):
        """
        (override)クリップ移動時
        # TODO: 篠島さんに移動中もイベントが飛ぶ様にできないか確認
        """
        if self._is_maya_clip_data(clip):
            self._maya_clip_move_timer.clip_moved(clip, old_frame, new_frame)

    def remove_sequencer_clip(self, clip: SequencerClipData) -> bool:
        """(override) クリップが削除された時に呼ばれる関数。"""
        track_data: SequencerTrack = clip.track_data()
        group_data = clip.get_parent_track()
        event_type = group_data.get_event_type()

        if is_sequencer_track(event_type):
            clip_property = clip.get_clip_property()
            reference_path = clip_property[const.Event.EVENT_REFERENCE_PATH]
            screen_writer = group_data.get_property()[const.Event.GROUP_SCREEN_WRITER_PATH]

            MayaReferenceController().delete(reference_path)
            ScreenWriterConnector(screen_writer).organize_input_connect()

        return track_data.remove_sequencer_clip(clip)

    def remove_sequencer_track(self, group: SequencerTrack | SequencerGroupTrackData) -> bool:
        """(override) トラックが削除されたときに呼ばれる関数。"""
        event_type = group.get_event_type()
        if isinstance(group, SequencerGroupTrackData):
            # Groupのみ、Trackは現状何もしない
            if is_sequencer_track(event_type):
                group_property = group.get_property()
                screen_writer = group_property[const.Event.GROUP_SCREEN_WRITER_PATH]
                reference_path = group_property[const.Event.GROUP_REFERENCE_PATH]
                MayaReferenceController().delete(reference_path, is_file=False)
                ScreenWriterManager.delete_node(screen_writer)

        super().remove_sequencer_track(group)

    def _is_maya_clip_data(self, clips: tp.Union[SequencerClipData, tp.List[SequencerClipData]]):
        """Mayaで評価すべきデータかどうか

        Args:
            clips (tp.Union[SequencerClipData, tp.List[SequencerClipData]]): 確認対象のClip
        """
        def is_maya_clip_data_inner(clips):
            if isinstance(clips, MotionClipData) or isinstance(clips, CameraClipData):
                return True
            else:
                return False

        if type(clips) == list:
            result = True
            for clip in clips:
                result *= is_maya_clip_data_inner(clip)

            return result

        return is_maya_clip_data_inner(clips)

    # -----------------------------------------------------------------
    # シーケンサーの基本動作。未来的には正式なアイコンに追加される。
    # -----------------------------------------------------------------
    def show_create_actor(self):
        """アクター作成
        """
        create_actor.show_actor_option(self)

    # TODO: show_insert_clipに変更する
    def show_insert_clip(self):
        """モーション追加
        """
        track_data: SequencerTrack = self.get_selected_track_data()
        if not isinstance(track_data, SequencerTrack):
            return

        clip_creator.insert_motion_show_option()

    def create_camera_actor(self):
        """カメラアクタ作成
        viewから呼ぶ用
        """
        CameraCreator(self).create_camera()

    def show_default(self):
        """通常表示
        TODO: ダブルクリック操作検討中
        """
        selector = ReferenceVisibleSelector(self)
        selector.set_all_clip_visible(False)
        selector.set_all_actor_visible(True)

    def show_only_selected_clip_node(self):
        """選択クリップのみ表示
        TODO: ダブルクリック操作検討中
        """
        clips = self.get_selected_clips()
        selector = ReferenceVisibleSelector(self)
        selector.set_all_actor_visible(False)
        selector.set_all_clip_visible(False)

        for clip in clips:
            selector.set_clip_visible(clip, True)

    def save_selected_clip_reference(self):
        clips = self.get_selected_clips()
        if not clips:
            return

        self.save_reference(clips)

    def save_reference(self, clips: tp.List[SequencerClipData]):
        """リファレンスを保存する
        """
        for clip in clips:
            event_type = clip.get_parent_track().get_event_type()
            if is_sequencer_track(event_type):
                if clip.get_status() != ClipStatus.Check:
                    clip_property = clip.get_clip_property()

                    reference.save_reference(clip_property[const.Event.EVENT_REFERENCE_PATH])
                    clip.set_status(ClipStatus.Check)

    def save_all_reference(self):
        clips = self.get_all_clips()
        if not clips:
            return

        self.save_reference(clips)

    def show_outline(self):
        outliner.main()

    # -----------------------------------------------------------------
    # 以下デバッグ用関数
    # -----------------------------------------------------------------
    def add_empty_motion_track(self):
        group = self.add_group_track("", "empty group")
        track = self.create_track("empty track", "", group)
        print(type(track))

    def add_empty_clip_to_selected_track(self):
        track_data = self.get_selected_track_data()
        self.insert_sequencer_clip_data(track_data, (0, 40, 25), "empty clip", "", "", fetch_now_time())

    def add_empty_sound_track(self):
        group = self.add_group_track("", "empty event group")
        track = self.create_sound_track("empty sound", group)

    def add_track_property(self):
        track_data = self.get_selected_track_data()
        track_data.add_or_edit_property("my data", "oh yeah")
        track_data.add_or_edit_property("property1", "my prop!")

    def print_selected_track(self):
        track = self.get_selected_track_data()
        print(track)
        print(type(track))

    def print_selected_track_property(self):
        track = self.get_selected_track_data()
        properties = track.get_property()
        print(properties)

    def print_selected_item(self):
        track_item = self.get_selected_track_item()
        print(track_item)
        print(type(track_item))

    def print_selected_clips(self):
        clips = self.get_selected_clips()
        for clip in clips:
            print(f'clip id = {id(clip)}, {clip}')

    def print_selected_clip_property(self):
        clips = self.get_selected_clips()
        for clip in clips:
            event_property = clip.get_clip_property()
            print(f"{clip}: {event_property}")

    def set_nothing_on_selected_clip(self):
        clip = self.get_selected_clips()
        clip.set_status(ClipStatus.Nothing)

    def set_check_on_selected_clip(self):
        clip = self.get_selected_clips()
        clip.set_status(ClipStatus.Check)

    def set_disable_on_selected_clip(self):
        clip = self.get_selected_clips()
        clip.set_status(ClipStatus.Disable)

    def set_edit_on_selected_clip(self):
        clip = self.get_selected_clips()
        clip.set_status(ClipStatus.Edit)

    def test(self):
        """メニューに登録するまでもない適当な関数をテストする用"""
        self.evaluate_current_frame()

    def delete_all_mseq(self):
        """デバック用

        溜まってしまっているmseqを全て削除する
        """
        import glob
        import os
        import stat

        scene_path = getCurrentSceneFilePath()
        if scene_path:
            work_folder_path = os.path.join(os.path.dirname(scene_path), "exportresources")
            files = glob.glob(f"{work_folder_path}/*.ma")

            for file in files:
                os.chmod(path=file, mode=stat.S_IWRITE)
                os.remove(file)

    def add_sub_track(self):
        group_item = self.get_selected_track_item()
        group: SequencerGroupTrackData = group_item.track_data()
        if not isinstance(group, SequencerGroupTrackData):
            print("Groupが選択されていません。")
            return

        event_type = group.get_event_type()

        if event_type == "Camera":
            self.create_track("SubTrack", "Camera", group_item)
        elif event_type == "Motion":
            self.create_track("SubTrack", "Motion", group_item)


class MayaSequencerSignals(QtCore.QObject):
    """
    Mayaアプリケーション側でもつSignalをまとめたクラス
    どこからでもアクセスできるようにシングルトンにしてある。
    """
    __instance = None
    created_group_actor = QtCore.Signal(str, str, str, str, str)
    created_event_motion = QtCore.Signal(object, tuple, str, int, str, str)
    created_event = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

    @classmethod
    def get_instance(cls):
        """
        このクラスのインスタンスを取得。
        """
        if cls.__instance is None:
            cls.__instance = MayaSequencerSignals()
        return cls.__instance
