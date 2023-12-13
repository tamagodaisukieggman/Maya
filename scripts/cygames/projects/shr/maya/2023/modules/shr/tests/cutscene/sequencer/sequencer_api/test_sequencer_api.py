
from unittest import mock

import mtk.cutscene.sequencer.api as seq
import pytest
from cy.ed import qtex
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt


@pytest.fixture()
def set_up_empty_data():
    sequencer = seq.Sequencer.get_instance()
    sequencer.clear_model()
    # sequencer.set_application_type(seq.ApplicationType.Maya)
    yield sequencer


@pytest.fixture()
def set_up_data(set_up_empty_data):
    """データの個数や順番などでテストに影響を与えるので、変更する時はテストの結果が変わるのを考慮してテスト内容を変更するように。"""
    sequencer = set_up_empty_data

    camera_track = seq.CameraTrack("Camera")
    sequencer.add_track(camera_track)
    camera_track.add_sequencer_clip((0, 44), "Camera 1")
    camera_track.add_sequencer_clip((40, 60), "Camera 2")

    track1 = seq.MotionTrack("Player")
    player_track = sequencer.add_track(track1)
    player_track.add_sequencer_clip((0, 20, 10), "battle", seq.ClipStatus.Check)
    player_track.add_sequencer_clip((0, 15, 40), "fight", seq.ClipStatus.Disable)

    npc_group = sequencer.add_group_track("my_event_type", "NPC Group")
    npc_group2 = sequencer.add_group_track("hoge_event", "NPC Group2")
    npc_group3 = sequencer.add_group_track("empty_event", "NPC Group2",)  # 重複グループは登録できない
    npc_group3 = sequencer.add_group_track("empty_event", "NPC Group2",)  # 重複グループは登録できない

    group_data = npc_group.track_data()
    group_data.add_or_edit_property("my property1", "foo bar")
    group_data.add_or_edit_property("my property2", "hoge hoge")
    group_data.add_or_edit_property("my property3", "35677")
    group_data.add_or_edit_property("my property4", "iasdf;jgkanrgea")
    group_data.add_or_edit_property("my property1", "fxied")

    track = seq.MotionTrack("NPC1")
    npc_track = sequencer.add_track(track, npc_group)
    npc_track.add_sequencer_clip((0, 10, 5), "hoge", seq.ClipStatus.Edit)
    npc_track.add_sequencer_clip((0, 15, 20), "foo", seq.ClipStatus.Check)

    track = seq.MotionTrack("NPC2")
    npc_track = sequencer.add_track(track, npc_group)
    npc_track.add_sequencer_clip((0, 20, 10), "walk")

    track = seq.MotionTrack("NPC3")
    npc_track = sequencer.add_track(track, npc_group)
    npc_track.add_sequencer_clip((0, 20, 5), "dash")

    track = seq.MotionTrack("NPC4")
    npc_track = sequencer.add_track(track, npc_group2)
    npc_track.add_sequencer_clip((0, 20, 0), "run")
    npc_track.add_sequencer_clip((0, 15, 42), "talk")
    clip_parm = seq.ClipParameters(0, 10, 25, 2, 9)
    npc_track.add_sequencer_clip(clip_parm, "sick")

    track = seq.MotionTrack("NPC5")
    npc_track = sequencer.add_track(track, npc_group2)
    npc_track.add_sequencer_clip((0, 20, 10), "skip")
    npc_track.add_sequencer_clip((0, 15, 35), "talk")

    se_group = sequencer.add_group_track("cyllista_event", "SE Group")
    track = seq.SoundTrack("Sound Track1")
    track = sequencer.add_track(track, se_group)
    track.add_sequencer_clip((15, 32), "explosion", seq.ClipStatus.Edit)
    track.add_sequencer_clip((34, 46), "rain", seq.ClipStatus.Check)

    track = seq.SoundTrack("Sound Track2")
    track = sequencer.add_track(track, se_group)
    track.add_sequencer_clip((16, 38), "beep", seq.ClipStatus.Edit)

    # 無名グループ。名前重複チェックは行われない
    empty_group1 = sequencer.add_group_track("my_event_type")
    empty_group2 = sequencer.add_group_track("my_event_type2")

    sequencer.rebuild()
    sequencer.set_timeline_length(120)
    # sequencer.set_frame_range(0, 120, 0, 80)

    yield sequencer


class TestSequencerApi(object):
    def test_get_instance(self):
        instance = seq.Sequencer.get_instance()
        instance2 = seq.Sequencer.get_instance()
        assert instance == instance2

    def test_add_group_track(self, set_up_empty_data):
        sequencer = set_up_empty_data
        group_track = sequencer.add_group_track("my_event", "Test Group")
        assert group_track is not None

        # 同名グループの追加は None が返る
        group_track2 = sequencer.add_group_track("my_event2", "Test Group")
        assert group_track2 is None

    def test_evaluate_current_frame(self, set_up_data, mocker: mock):
        # evaluate後のcalculateは不要なので、mockでかぶせる
        evaluate_mock = mocker.patch("mtk.cutscene.sequencer.model.MayaAnimationClipCalculator.calculate", retrun_value=True)

        def assert_func(data):
            assert len(data) == 3
            walk_clip = sequencer.find_clips('walk')[0]
            run_clip = sequencer.find_clips('run')[0]
            explosion_clip = sequencer.find_clips('explosion')[0]
            beep_clip = sequencer.find_clips('beep')[0]
            npc_group = walk_clip.get_parent_track()
            npc_group2 = run_clip.get_parent_track()
            se_group = explosion_clip.get_parent_track()
            assert walk_clip == data[npc_group][0].clip
            assert run_clip == data[npc_group2][0].clip
            assert explosion_clip == data[se_group][0].clip
            assert beep_clip == data[se_group][1].clip

        sequencer = set_up_data
        sequencer._signals.motion_clip_evaluated.connect(assert_func)
        sequencer.set_curernt_frame(18)
        sequencer.evaluate_current_frame()
        sequencer._signals.motion_clip_evaluated.disconnect(assert_func)
        # evaluate_mock.assert_called_once()

    def test_filter_evaluated_clip_data1(self, set_up_data, mocker: mock):
        # evaluate後のcalculateは不要なので、mockでかぶせる
        evaluate_mock = mocker.patch("mtk.cutscene.sequencer.model.MayaAnimationClipCalculator.calculate", retrun_value=True)

        def assert_func(data):
            assert len(data) == 3
            data = sequencer.filter_evaluated_clip_data(data, seq.ApplicationType.Maya)
            assert len(data) == 2  # Cyllistaのグループトラックが削除されて一つ減る

        sequencer = set_up_data
        sequencer._signals.motion_clip_evaluated.connect(assert_func)
        sequencer.set_curernt_frame(18)
        sequencer.evaluate_current_frame()
        sequencer._signals.motion_clip_evaluated.disconnect(assert_func)

    def test_filter_evaluated_clip_data2(self, set_up_data, mocker: mock):
        # evaluate後のcalculateは不要なので、mockでかぶせる
        evaluate_mock = mocker.patch("mtk.cutscene.sequencer.model.MayaAnimationClipCalculator.calculate", retrun_value=True)

        def assert_func(data):
            assert len(data) == 3
            data = sequencer.filter_evaluated_clip_data(data, seq.ApplicationType.Cyllista)
            assert len(data) == 3

        sequencer = set_up_data
        sequencer._signals.motion_clip_evaluated.connect(assert_func)
        sequencer.set_curernt_frame(18)
        sequencer.evaluate_current_frame()
        sequencer._signals.motion_clip_evaluated.disconnect(assert_func)

    def test_find_clips_and_tracks(self, set_up_data):
        sequencer = set_up_data
        track = sequencer.find_tracks("NPC3")[0]
        assert len(track.clips()) == 1
        dash_clip = track.clips()[0]

        result = sequencer.find_clips('dash')[0]
        assert dash_clip == result

    def test_find_group(self, set_up_empty_data):
        sequencer = set_up_empty_data
        group_track1 = sequencer.add_group_track("my_event1", "Test Group")
        group_track2 = sequencer.add_group_track("my_event2", "Hoge Group")
        group_track3 = sequencer.add_group_track("my_event3", "Camera")
        group_track4 = sequencer.add_group_track("my_event4", "Player")
        assert group_track1
        assert group_track2
        assert group_track3
        assert group_track4

        found_group = sequencer.find_group('Camera')
        assert found_group == group_track3

    def test_get_all_groups(self, set_up_data):
        sequencer = set_up_data
        # 既存の Group 5個に対して4個グループ追加
        group_track1 = sequencer.add_group_track("my_event", "Test Group")
        group_track2 = sequencer.add_group_track("my_event", "Hoge Group")
        group_track3 = sequencer.add_group_track("my_event", "Hoge Group")  # 重複なのでカウントしない
        group_track4 = sequencer.add_group_track("my_event", "Player2 Group")
        group_track5 = sequencer.add_group_track("my_event", "NPC2 Group")

        all_groups = sequencer.get_all_groups()
        assert len(all_groups) == 9

    def test_get_all_groups2(self, set_up_empty_data):
        # グループが一つもなければ [] が返ってくる
        sequencer = set_up_empty_data
        all_groups = sequencer.get_all_groups()
        assert len(all_groups) == 0

    def test_get_all_tracks(self, set_up_data):
        sequencer = set_up_data
        tracks = sequencer.get_all_tracks()
        assert len(tracks) == 9

    def test_get_all_tracks2(self, set_up_empty_data):
        # トラックが一つもなければ [] が返ってくる
        sequencer = set_up_empty_data
        tracks = sequencer.get_all_tracks()
        assert len(tracks) == 0

    def test_get_all_clips(self, set_up_data):
        sequencer = set_up_data
        clips = sequencer.get_all_clips()
        assert len(clips) == 16

    def test_get_all_clips2(self, set_up_empty_data):
        # クリップが一つもなければ [] が返ってくる
        sequencer = set_up_empty_data
        clips = sequencer.get_all_clips()
        assert len(clips) == 0

    def test_get_selected_track_data(self, set_up_data):
        sequencer = set_up_data

        # プログラム的に Player1 トラックを選択
        index = sequencer._model.index(1, 0)
        selection_model = sequencer._timeline_view._treeview.selectionModel()
        selection_model.clear()
        selection_model.setCurrentIndex(index, QtCore.QItemSelectionModel.Select)

        track_data = sequencer._model.itemFromIndex(index).track_data()
        result = sequencer.get_selected_track_data()
        assert track_data == result

    def test_get_selected_track_item(self, set_up_data):
        sequencer = set_up_data

        # プログラム的に Player1 トラックを選択
        index = sequencer._model.index(1, 0)
        selection_model = sequencer._timeline_view._treeview.selectionModel()
        selection_model.clear()
        selection_model.setCurrentIndex(index, QtCore.QItemSelectionModel.Select)

        item = sequencer._model.itemFromIndex(index)
        result = sequencer.get_selected_track_item()
        assert item == result

    def test_get_selected_clips(self, set_up_data):
        sequencer = set_up_data
        track_view = sequencer._timeline_view.get_track_view()

        # Row1の最初のrectを選ぶ
        index = sequencer._model.index(0, 0)
        widget = track_view.indexWidget(index)
        widget._selected_rect_indexes.add(0)
        track_data = widget.get_track_data()
        clip1 = track_data.clips()[0]
        clip_ = track_data.clips()[1]

        # Row2のrectを2つ選ぶ
        index = sequencer._model.index(1, 0)
        widget = track_view.indexWidget(index)
        widget._selected_rect_indexes.add(0)
        widget._selected_rect_indexes.add(1)
        track_data = widget.get_track_data()
        clip2 = track_data.clips()[0]
        clip3 = track_data.clips()[1]

        clips = sequencer.get_selected_clips()
        assert len(clips) == 3
        assert clip1 in clips
        assert clip2 in clips
        assert clip3 in clips
        assert clip_ not in clips

    def test_notify_clip_delete(self, set_up_data):
        sequencer = set_up_data
        track = sequencer.find_tracks("NPC3")[0]
        assert len(track.clips()) == 1
        dash_clip = track.clips()[0]
        sequencer.notify_clip_delete(dash_clip)
        assert len(track.clips()) == 0

    def test_notify_track_delete(self, set_up_data):
        sequencer = set_up_data
        all_tracks = sequencer.get_all_tracks()
        assert len(all_tracks) == 9
        track = sequencer.find_tracks("NPC3")[0]
        sequencer.notify_track_delete(track)
        all_tracks = sequencer.get_all_tracks()
        assert len(all_tracks) == 8

    def test_remove_sequencer_clip(self, set_up_data):
        sequencer = set_up_data
        track = sequencer.find_tracks("NPC3")[0]
        assert len(track.clips()) == 1
        dash_clip = track.clips()[0]
        sequencer.remove_sequencer_clip(dash_clip)
        assert len(track.clips()) == 0

    def test_remove_sequencer_track(self, set_up_data):
        sequencer = set_up_data
        track = sequencer.find_tracks("NPC3")[0]
        all_tracks = sequencer.get_all_tracks()
        assert len(all_tracks) == 9
        sequencer.remove_sequencer_track(track)
        all_tracks = sequencer.get_all_tracks()
        assert len(all_tracks) == 8

    def test_remove_selected_sequencer_clip(self, set_up_data):
        sequencer = set_up_data

        # track view を get
        track_view = sequencer._timeline_view.get_track_view()

        # Row2のrectを選ぶ
        index = sequencer._model.index(1, 0)
        widget = track_view.indexWidget(index)

        # プログラム的にClipを選択
        widget._selected_rect_indexes.add(0)
        widget._selected_rect_indexes.add(1)

        track_data = widget._track_data
        assert len(track_data.clips()) == 2
        sequencer.remove_selected_sequencer_clip()
        assert len(track_data.clips()) == 0

    def test_remove_selected_track_item(self, set_up_data):
        sequencer = set_up_data

        # プログラム的に Player トラックを選択
        index = sequencer._model.index(1, 0)
        selection_model = sequencer._timeline_view._treeview.selectionModel()
        selection_model.clear()
        selection_model.setCurrentIndex(index, QtCore.QItemSelectionModel.Select)

        # 削除前はトラックを見つけられる
        track = sequencer.find_tracks("Player")
        assert len(track) == 1

        # 選択削除
        tracks = sequencer.get_all_tracks()
        assert len(tracks) == 9
        sequencer.remove_selected_track_item()
        tracks = sequencer.get_all_tracks()
        assert len(tracks) == 8

        # 削除後はトラックの取得ができない
        track = sequencer.find_tracks("Player")
        assert track == []

    def test_remove_track(self, set_up_data):
        sequencer = set_up_data
        tracks = sequencer.get_all_tracks()
        assert len(tracks) == 9

        track = sequencer.find_tracks("NPC3")[0]
        sequencer.remove_track(track)

        tracks = sequencer.get_all_tracks()
        assert len(tracks) == 8
        track = sequencer.find_tracks("NPC3")
        assert track == []

    def test_remove_track_item(self, set_up_data):
        sequencer = set_up_data
        tracks = sequencer.get_all_tracks()
        assert len(tracks) == 9

        track = sequencer.find_tracks("NPC3")[0]
        item = track.get_track_item()
        assert item
        sequencer.remove_track_item(item)

        tracks = sequencer.get_all_tracks()
        assert len(tracks) == 8
        track = sequencer.find_tracks("NPC3")
        assert track == []

    def test_set_frame_range(self, set_up_empty_data):
        sequencer = set_up_empty_data
        sequencer.set_timeline_length(200)
        view_start = 10
        view_end = 120
        play_start = 40
        play_end = 80
        sequencer.set_frame_range(view_start, view_end, play_start, play_end)

        view_range = sequencer._controller.get_view_range_in_frame()
        assert view_range[0] == view_start
        assert view_range[1] == view_end
        play_range = sequencer._controller.play_range_in_frame
        assert play_range[0] == play_start
        assert play_range[1] == play_end

    # @pytest.mark.skip
    # def test_gui(self, qtbot, set_up_data):
    #     sequencer = set_up_data
    #     w = sequencer.get_timeline_view_widget()
    #     # qtbot.addWidget(w)  # これをするとClip表示がバグる
    #     w.show()
    #     # qtbot.wait(2000)  # wait すると addWidget() をしていなくてもClip表示がバグる
    #     w.close()
