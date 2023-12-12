from . import app, controller


def sync(*args):
    """UEの状態に合わせてSyncする
    """
    fake_controller = controller.LivelinkUtilityController()
    settings = fake_controller.ui.load_in_dict()
    app.LivelinkUtility(settings).sync_keyframe()

    # app.CutSceneCameraCreator(settings).duplicate()


def show_option(*args):
    """option起動のエントリーポイント
    """
    global facial_live_link_utility_controller

    try:
        facial_live_link_utility_controller.close_option()
    except Exception:
        pass

    facial_live_link_utility_controller = controller.LivelinkUtilityController()
    facial_live_link_utility_controller.show_option()
