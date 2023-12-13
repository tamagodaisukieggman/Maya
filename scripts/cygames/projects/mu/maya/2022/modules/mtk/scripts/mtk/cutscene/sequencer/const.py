from cy.asset.cutscene.common.base_eventdefinition import *


class Event:
    EVENT_NAME = "event_name"
    GROUP_NAME = "group_name"
    GROUP_SCREEN_WRITER_PATH = "screen_writer_path"
    GROUP_SCREEN_WRITER_UUID = "screen_writer_uuid"
    GROUP_ACTOR_CONFIG_PATH = "actor_config_path"
    GROUP_REFERENCE_UUID = "group_reference_uuid"
    GROUP_REFERENCE_PATH = "group_reference_path"
    EVENT_REFERENCE_UUID = "event_reference_uuid"
    EVENT_REFERENCE_PATH = "event_reference_path"
    EVENT_SCREEN_WRITER_INDEX = "event_screen_writer_index"
    EVENT_TYPE = "event_type"


class SaveData:
    NAME = "name"
    EVENT_TYPE = "event_type"
    MAYA = "maya"
    CYLLISTA = "cyllista"
    PROPERTY = "property"
    TRACK_TYPE = "track_type"
    TARGET_GROUP = "target_group"
    TARGET_TRACK = "target_track"
    UPDATED = "updated"
    DATA = "data"


class Data:
    START = "start"
    END = "end"
    IN = "in"
    OUT = "out"
    OFFSET = "offset"


CATEGORY_GROUP = "group"
CATEGORY_EVENT = "group"
EVENT_TYPE_MOTION = "Motion"
EVENT_TYPE_CAMERA = "Camera"
