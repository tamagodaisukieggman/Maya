from maya import cmds

from . import app, view


class LivelinkUtilityController(object):
    def __init__(self):
        self.ui = view.View()

        self.setup_event()

    def setup_event(self):
        ...
        self.ui.gui.closeButton.clicked.connect(self.close_option)
        self.ui.gui.syncButton.clicked.connect(self.clicked_sync_button)
        self.ui.gui.applyButton.clicked.connect(self.clicked_apply_button)
        self.ui.gui.syncTimeSliderButton.clicked.connect(self.clicked_sync_time_slider_button)

    def show_option(self):
        self.ui.show()

    def close_option(self):
        self.ui.close()

    def clicked_apply_button(self):
        try:
            self.ui.save()

            live_link_utility = app.LivelinkUtility(self.ui.load_in_dict())
            result = live_link_utility.sync_keyframe()

            if result == app.SyncStatus.COMPLETE:
                cmds.confirmDialog(title="完了", message="キーフレームの移動とタイムスライダーの同期が完了しました")

            elif result == app.SyncStatus.CANCEL:
                cmds.confirmDialog(title="完了", message="同期をキャンセルしました")

            elif result == app.SyncStatus.FAILURE:
                cmds.confirmDialog(title="失敗", message="同期に失敗しました。\nUEを起動し、サブシーケンサーを開いてる必要があります。")
        except Exception as e:
            cmds.confirmDialog(title="不明なエラー", message=f"不明なエラーが発生しました。TAに確認してください\n{e}")

    def clicked_sync_button(self):
        self.clicked_apply_button()
        self.close_option()

    def clicked_sync_time_slider_button(self):
        live_link_utility = app.LivelinkUtility(self.ui.load_in_dict())
        result = live_link_utility.sync_time_slider_only()
        if result == app.SyncStatus.COMPLETE:
            cmds.confirmDialog(title="完了", message="タイムスライダーの同期が完了しました")
        elif result == app.SyncStatus.FAILURE:
            cmds.confirmDialog(title="失敗", message="同期に失敗しました。\nUEを起動し、サブシーケンサーを開いてる必要があります。")
