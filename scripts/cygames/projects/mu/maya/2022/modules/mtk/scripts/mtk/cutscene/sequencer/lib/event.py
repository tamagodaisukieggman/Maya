from .. import const


def is_sequencer_track(event_type):
    if event_type == const.EVENT_TYPE_CAMERA or event_type == const.EVENT_TYPE_MOTION:
        return True

    return False


def is_camera_track(event_type):
    if event_type == const.EVENT_TYPE_CAMERA:
        return True

    return False


def is_motion_track(event_type):
    if event_type == const.EVENT_TYPE_MOTION:
        return True

    return False
