from __future__ import annotations

import json
import typing as tp
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING

from maya import cmds, mel, utils
from mtk.cutscene.sequencer import const
from mtk.cutscene.sequencer.api import *
from mtk.cutscene.sequencer.lib.event import is_sequencer_track

if TYPE_CHECKING:
    from ..controller import SequencerController


class ImportType(Enum):
    Both = auto()
    Maya = auto()
    Cyllista = auto()


class ClipType(Enum):
    Clip = auto()
    ClipWithInOut = auto()


class SequencerSaveData(object):
    VERSION = "0.0.1"

    def __init__(self) -> None:
        self.version = self.VERSION
        self.fps = None
        self.min_frame = None
        self.max_frame = None
        self.ma_sync_sound = ""
        self.group_list = []
        self.track_list = []
        self.event_list = []

    def update_maya_data(self, version=None):
        from mtk.cutscene.sequencer.controller import SequencerController
        sequencer = SequencerController.get_instance()

        if not version:
            version = self.VERSION

        self.version = version
        self.fps = mel.eval('currentTimeUnitToFPS')
        self.min_frame = cmds.playbackOptions(query=True, animationStartTime=True)
        self.max_frame = cmds.playbackOptions(query=True, animationEndTime=True)
        self.group_list = [GroupData(group, {}) for group in sequencer.get_all_groups()]
        self.track_list = [TrackData(track) for track in sequencer.get_all_tracks()]
        self.event_list = [ClipData(clip, {}) for clip in sequencer.get_all_clips()]

    def set_ma_syn_sound(self, value):
        self.ma_sync_sound = value

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self, f, cls=SequencerJsonEncoder, indent=4, ensure_ascii=False)

    @classmethod
    def load(cls, path):
        from mtk.cutscene.sequencer.controller import SequencerController
        sequencer = SequencerController.get_instance()
        sequencer.clear_model()

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.loads(f.read())
                save_data = cls.decode(data)
                save_data.restore(sequencer)
        except ValueError as e:
            cmds.confirmDialog(annotation="Error", message=f"{e}\n上記エラーで読み込みに失敗しました。\n安全の為、ファイルを保存せず、終了します。")
            sequencer.clear_model()
            cmds.file(newFile=True, force=True)
            return False

        return True

    @classmethod
    def decode(cls, data):
        save_data = cls()
        save_data.version = data["version"]
        save_data.fps = data["fps"]
        save_data.min_frame = data["min_frame"]
        save_data.max_frame = data["max_frame"]
        save_data.ma_sync_sound = data["ma_sync_sound"]

        group_list = []
        for group_dict in data["group_list"]:
            group_list.append(GroupData.decode(group_dict))
        save_data.group_list = group_list

        track_list = []
        for track_dict in data["track_list"]:
            track_list.append(TrackData.decode(track_dict))
        save_data.track_list = track_list

        event_list = []
        for clip in data["event_list"]:
            event_list.append((ClipData.decode(clip)))
        save_data.event_list = event_list
        return save_data

    def restore(self, sequencer: SequencerController):

        self._override_fps(self.fps)
        self._override_min_frame(self.min_frame)
        self._override_max_frame(self.max_frame)

        self._create_group(sequencer)
        self._create_tracks(sequencer)
        self._create_clips(sequencer)

    def _override_fps(self, fps):
        unit = 'ntscf'
        if fps == 15:
            unit = 'game'
        elif fps == 24:
            unit = 'film'
        elif fps == 25:
            unit = 'pal'
        elif fps == 30:
            unit = 'ntsc'
        elif fps == 48:
            unit = 'show'
        elif fps == 50:
            unit = 'palf'
        elif fps == 60:
            unit = 'ntscf'
        elif fps == 59.94005994005994:
            unit = '59.94fps'
        else:
            unit = str(fps) + 'fps'

        cmds.currentUnit(time=unit)

    def _override_min_frame(self, min_frame: str):
        cmds.playbackOptions(edit=True, animationStartTime=float(min_frame))

    def _override_max_frame(self, max_frame: str):
        cmds.playbackOptions(edit=True, animationEndTime=float(max_frame))

    def _create_group(self, sequencer: SequencerController):
        group_list: tp.List[GroupData] = self.group_list
        for group in group_list:
            if is_sequencer_track(group.event_type):
                group_data = sequencer.load_actor_group(group.name,
                                                        group.event_type,
                                                        group.maya.screen_writer,
                                                        group.maya.actor_config_path,
                                                        group.maya.reference_path)
            else:
                group_data = sequencer.load_event_group(group.name, group.event_type)

            if group.property:
                for key, value in group.property.items():
                    group_data.track_data().add_or_edit_property(key, value)

    def _create_tracks(self, sequencer):
        for track in self.track_list:
            group = sequencer.find_group(track.target_group)
            if not group:
                raise ValueError(f"Not found Group [{group}]")

            track = sequencer.create_track(track.name, track.track_type, group)

    def _create_clips(self, sequencer: SequencerController):
        track_list = sequencer.get_all_tracks()

        for clip in self.event_list:
            target_track = None

            for track in track_list:
                if track.display_name() == clip.target_track:
                    target_track = track

            if not target_track:
                raise ValueError(f"Not found track [{clip.target_track}]")
            updated = clip.updated

            start_time = clip.data[const.Data.START]
            end_time = clip.data[const.Data.END]
            offset = clip.data[const.Data.OFFSET]
            in_time = clip.data[const.Data.IN]
            out_time = clip.data[const.Data.OUT]
            event_property = clip.property

            if is_sequencer_track(clip.event_type):
                ref_path = clip.maya.reference_path
                index = clip.maya.index
                event_property.update({const.Event.EVENT_SCREEN_WRITER_INDEX: clip.maya.index, const.Event.EVENT_REFERENCE_PATH: clip.maya.reference_path})
            else:
                ref_path = ""
                index = 0

            created_clip = sequencer.insert_sequencer_clip_data(target_track,
                                                                (start_time, end_time, offset, in_time, out_time),
                                                                clip.name,
                                                                index,
                                                                ref_path,
                                                                updated)

            created_clip.set_clip_property(event_property)


class ScreenWriterData(object):
    def __init__(self, name) -> None:
        self.name = name
        self.uuid = self.fetch_uuid(self.name)

    def fetch_uuid(self, name):
        find_objects = cmds.ls(name, uuid=True)
        if len(find_objects) != 1:
            raise ValueError(f"Invalid uuid [{name}]")

        return find_objects[0]

    @classmethod
    def decode(cls, uuid):
        find_objects = cmds.ls(uuid)
        if len(find_objects) != 1:
            raise ValueError(f"Invalid uuid [{uuid}]")

        return cls(find_objects[0])


class ReferenceData(object):
    def __init__(self, reference_path) -> None:
        self.path = self.fetch_path(reference_path)
        self.uuid = self.fetch_uuid(self.path)

    def fetch_uuid(self, ref_path):
        ref_node = cmds.referenceQuery(ref_path, referenceNode=True)
        uuid_list = cmds.ls(ref_node, uuid=True)
        if len(uuid_list) != 1:
            raise ValueError(f"Invalid uuid [{ref_path}]")

        uuid = uuid_list[0]
        return uuid

    def fetch_path(self, path):
        path = Path(path)
        if not Path(path).exists():
            raise ValueError(f"Not found path [{path}]")
        return str(path.absolute())

    @ classmethod
    def decode(cls, uuid):
        find_objects = cmds.ls(uuid)
        if len(find_objects) != 1:
            raise ValueError(f"Invalid uuid [{uuid}]")

        ref_path = cmds.referenceQuery(find_objects[0], filename=True)

        return cls(ref_path)


# -----------------------------------------------------------------
# GroupData
# -----------------------------------------------------------------
class GroupData(object):
    def __init__(self, group: tp.Optional[SequencerGroupTrackData] = None, cyllista_data=None) -> None:
        if group:
            self.name = group.display_name()
            self.event_type = group.get_event_type()
            self.cyllista = cyllista_data or {}
            self.property = group.get_property()
            if self.event_type == "Motion" or self.event_type == "Camera":
                screen_writer = self.property[const.Event.GROUP_SCREEN_WRITER_PATH]
                actor_config_path = self.property[const.Event.GROUP_ACTOR_CONFIG_PATH]
                ref_node = self.property[const.Event.GROUP_REFERENCE_PATH]
                self.maya = GroupMayaData(ScreenWriterData(screen_writer),
                                          actor_config_path,
                                          ReferenceData(ref_node))
            else:
                self.maya = {}
        else:
            self.name = None
            self.event_type = None
            self.maya = None
            self.cyllista = cyllista_data or {}
            self.property = {}

    @ classmethod
    def decode(cls, group_dict):
        save_data = cls()
        save_data.name = group_dict[const.SaveData.NAME]
        save_data.event_type = group_dict[const.SaveData.EVENT_TYPE]

        if save_data.event_type == "Motion" or save_data.event_type == "Camera":
            screen_writer = ScreenWriterData.decode(group_dict[const.SaveData.MAYA][const.Event.GROUP_SCREEN_WRITER_UUID])
            reference_data = ReferenceData.decode(group_dict[const.SaveData.MAYA][const.Event.GROUP_REFERENCE_UUID])

            save_data.maya = GroupMayaData(screen_writer, group_dict[const.SaveData.MAYA][const.Event.GROUP_ACTOR_CONFIG_PATH], reference_data)
        save_data.cyllista = group_dict.get(const.SaveData.CYLLISTA, {})
        save_data.property = group_dict.get(const.SaveData.PROPERTY, {})

        return save_data


class GroupMayaData(object):
    def __init__(self, screen_writer: ScreenWriterData, actor_config_path: str, reference: ReferenceData) -> None:
        self.screen_writer = screen_writer.name
        self.screen_writer_uuid = screen_writer.uuid
        self.actor_config_path = actor_config_path
        self.reference_path = reference.path
        self.reference_uuid = reference.uuid

    def fetch_reference_uuid(self, ref_path):
        ref_node = cmds.referenceQuery(ref_path, referenceNode=True)
        uuid = cmds.ls(ref_node, uuid=True)[0]
        return uuid


# -----------------------------------------------------------------
# TrackData
# -----------------------------------------------------------------
class TrackData(object):
    def __init__(self, track: tp.Optional[SequencerTrack] = None) -> None:
        if track:
            self.name = track.display_name()
            self.track_type = track.track_type().name
            self.target_group = track.get_parent_group_track_data().display_name()
        else:
            self.name = None
            self.track_type = None
            self.target_group = None

    @ classmethod
    def decode(cls, data):
        save_data = cls()
        save_data.name = data[const.SaveData.NAME]
        save_data.track_type = data["track_type"]
        save_data.target_group = data[const.SaveData.TARGET_GROUP]
        return save_data


# -----------------------------------------------------------------
# ClipData
# -----------------------------------------------------------------
class ClipData(object):
    def __init__(self, clip: tp.Optional[SequencerClipData] = None, cyllista_data=None) -> None:
        if clip:
            clip_parameter: ClipParameters = clip.get_clip_parameters()
            clip_data = clip_parameter.get_dict_data()
            group = clip.get_parent_track()
            self.name = clip.get_label()
            self.event_type = group.get_event_type()
            self.target_track = clip.track_data().display_name()
            self.data = clip_data
            self.updated = clip.get_updated()
            self.property = clip.get_clip_property()
            if self.event_type == "Motion" or self.event_type == "Camera":
                self.maya = ClipMayaData(ReferenceData(
                    self.property[const.Event.EVENT_REFERENCE_PATH]),
                    self.property[const.Event.EVENT_SCREEN_WRITER_INDEX])
            else:
                self.maya = {}
            self.cyllista = cyllista_data or {}

        else:
            self.name = None
            self.event_type = None
            self.target_track = None
            self.data = None
            self.maya = None
            self.cyllista = cyllista_data or {}
            self.updated = None
            self.property = None

    def fetch_data(self, clip_time_data: dict):
        return ClipTimeData(clip_time_data)

    @ classmethod
    def decode(cls, data):
        save_data = cls()
        save_data.name = data[const.SaveData.NAME]
        save_data.target_track = data[const.SaveData.TARGET_TRACK]
        save_data.updated = data[const.SaveData.UPDATED]
        save_data.data = data[const.SaveData.DATA]
        save_data.event_type = data[const.SaveData.EVENT_TYPE]
        save_data.updated = data[const.SaveData.UPDATED]

        if save_data.event_type == "Motion" or save_data.event_type == "Camera":
            ref_data = ReferenceData(data[const.SaveData.MAYA][const.Event.EVENT_REFERENCE_PATH])
            save_data.maya = ClipMayaData(ref_data, data[const.SaveData.MAYA][const.Event.EVENT_SCREEN_WRITER_INDEX])
        else:
            save_data.maya = {}

        save_data.cyllista = data[const.SaveData.CYLLISTA]
        save_data.property = data[const.SaveData.PROPERTY]

        return save_data


class ClipMayaData(object):
    def __init__(self, reference: ReferenceData, index: int) -> None:
        self.reference_uuid = reference.uuid
        self.reference_path = reference.path
        self.index = index


# class ClipTimeData(object):
#     def __init__(self, clip_time_data: tp.Optional[dict] = None) -> None:
#         if clip_time_data:
#             self.start = clip_time_data[const.DATA.START]
#             self.end = clip_time_data["end"]
#             self.in_time = clip_time_data["in"]
#             self.out_time = clip_time_data["out"]
#             self.offset = clip_time_data["offset"]

#         else:
#             self.start = None
#             self.end = None
#             self.in_time = None
#             self.out_time = None
#             self.offset = None

#     @ classmethod
#     def decode(cls, data):
#         save_data = cls()
#         save_data.start = data[const.DATA.START]
#         save_data.end = data["end"]
#         save_data.in_time = data["in"]
#         save_data.out_time = data["out"]
#         save_data.offset = data["offset"]
#         return save_data


class SequencerJsonEncoder(json.JSONEncoder):
    """シーケンサーのJsonEncoder

    上部のSaveデータ用のクラスを読み込み辞書データにシリアライズする
    """

    def default(self, o: tp.Any) -> tp.Any:
        if isinstance(o, Enum):
            return o.name

        if isinstance(o, GroupData):
            if const.Event.GROUP_SCREEN_WRITER_PATH in o.property:
                del o.property[const.Event.GROUP_SCREEN_WRITER_PATH]
            if const.Event.GROUP_ACTOR_CONFIG_PATH in o.property:
                del o.property[const.Event.GROUP_ACTOR_CONFIG_PATH]
            if const.Event.GROUP_REFERENCE_PATH in o.property:
                del o.property[const.Event.GROUP_REFERENCE_PATH]

            return {const.SaveData.NAME: o.name,
                    const.Event.EVENT_TYPE: o.event_type,
                    const.SaveData.MAYA: o.maya,
                    const.SaveData.CYLLISTA: o.cyllista,
                    const.SaveData.PROPERTY: o.property}

        if isinstance(o, GroupMayaData):
            return {const.Event.GROUP_SCREEN_WRITER_UUID: o.screen_writer_uuid,
                    const.Event.GROUP_ACTOR_CONFIG_PATH: o.actor_config_path,
                    const.Event.GROUP_REFERENCE_UUID: o.reference_uuid,
                    const.Event.GROUP_REFERENCE_PATH: o.reference_path}

        if isinstance(o, TrackData):
            return {const.SaveData.NAME: o.name,
                    const.SaveData.TRACK_TYPE: o.track_type,
                    const.SaveData.TARGET_GROUP: o.target_group}

        if isinstance(o, ClipData):
            if const.Event.EVENT_REFERENCE_UUID in o.property:
                del o.property[const.Event.EVENT_REFERENCE_UUID]

            if const.Event.EVENT_REFERENCE_PATH in o.property:
                del o.property[const.Event.EVENT_REFERENCE_PATH]

            if const.Event.EVENT_SCREEN_WRITER_INDEX in o.property:
                del o.property[const.Event.EVENT_SCREEN_WRITER_INDEX]

            return {const.SaveData.NAME: o.name,
                    const.SaveData.TARGET_TRACK: o.target_track,
                    const.SaveData.EVENT_TYPE: o.event_type,
                    const.SaveData.UPDATED: o.updated,
                    const.SaveData.DATA: o.data,
                    const.SaveData.MAYA: o.maya,
                    const.SaveData.CYLLISTA: o.cyllista,
                    const.SaveData.PROPERTY: o.property}

        # if isinstance(o, ClipTimeData):
        #     data = {const.DATA.START: o.start,
        #             "end": o.end,
        #             "in": o.in_time,
        #             "out": o.out_time,
        #             "offset": o.offset}

            return data

        if isinstance(o, ClipMayaData):
            # TODO: ここ直指定なのが気になる。とはいえMaya固有＆判別色々してるので仕方ないか
            return {const.Event.EVENT_REFERENCE_UUID: o.reference_uuid,
                    const.Event.EVENT_REFERENCE_PATH: o.reference_path,
                    const.Event.EVENT_SCREEN_WRITER_INDEX: o.index}

        if isinstance(o, SequencerSaveData):
            return o.__dict__

        return super().default(o)


if __name__ == "__main__":
    save_data = SequencerSaveData()
    save_data.update_maya_data()
    save_data.save("Z:/mtk/tools/maya/2022/modules/mtk/scripts/mtk/cutscene/sequencer/sequencer_data/sample2.seq")

    # save_data.load("Z:/mtk/tools/maya/2022/modules/mtk/scripts/mtk/cutscene/sequencer/sequencer_data/sample2.seq")
