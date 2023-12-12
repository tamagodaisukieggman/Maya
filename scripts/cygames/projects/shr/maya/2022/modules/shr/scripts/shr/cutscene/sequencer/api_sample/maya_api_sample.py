# coding=utf-8
"""
シーケンサーAPIを使ったサンプル
"""
import api
from PySide6 import QtCore, QtWidgets

from cy.ed import qtex
import api as seq


class DockWidget(QtWidgets.QDockWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.create_inner_widget()

    def create_inner_widget(self) -> None:
        # シーケンサーはDockWidget内部に入る
        self.setWidget(seq.get_sequencer().get_timeline_view_widget())


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MainWindow")
        self.setWindowTitle("Sequencer Example")
        self.setCentralWidget(None)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, DockWidget(parent=self))


def main():
    app = qtex.get_application([])
    qtex.set_style_sheet(app)

    # ユーザーの操作。 Mayaからはこんな感じで関数を使う想定
    sequencer = seq.get_sequencer()
    # sequencer.set_application_type(seq.ApplicationType.Maya)

    mw = MainWindow()
    mw.resize(1200, 600)
    mw.show()

    camera_track = seq.CameraTrack("Camera")
    sequencer.add_track(camera_track)
    camera_track.add_sequencer_clip((0, 44), "Camera 1")
    camera_track.add_sequencer_clip((40, 60), "Camera 2")

    track1 = seq.MotionTrack("Player")
    player_track = sequencer.add_track(track1)
    player_track.add_sequencer_clip((0, 20, 10), "battle", seq.ClipStatus.Check)
    player_track.add_sequencer_clip((0, 15, 40), "fight", seq.ClipStatus.Disable)

    npc_group = sequencer.add_group_track("Motion", "NPC Group")
    npc_group2 = sequencer.add_group_track("Motion", "NPC Group2")
    npc_group3 = sequencer.add_group_track("Motion", "NPC Group2",)  # 重複グループは登録できない
    npc_group3 = sequencer.add_group_track("Motion", "NPC Group2",)  # 重複グループは登録できない

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

    se_group = sequencer.add_group_track("PlaySound", "SE Group")
    track = seq.EventTrack("Sound Track1")
    track = sequencer.add_track(track, se_group)
    track.add_sequencer_clip((15, 32), "explosion", seq.ClipStatus.Edit)
    track.add_sequencer_clip((34, 46), "rain", seq.ClipStatus.Check)

    track = seq.EventTrack("Sound Track2")
    track = sequencer.add_track(track, se_group)
    track.add_sequencer_clip((16, 38), "beep", seq.ClipStatus.Edit)

    # 無名グループ。名前重複チェックは行われない
    sequencer.add_group_track("Motion")
    sequencer.add_group_track("Motion")

    sequencer.rebuild()
    sequencer.set_timeline_length(120)
    sequencer.set_frame_range(0, 60, 0, 60)

    app.exec()


if __name__ == "__main__":
    main()
