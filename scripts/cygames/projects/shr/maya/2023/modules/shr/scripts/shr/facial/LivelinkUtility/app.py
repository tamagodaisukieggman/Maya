import typing as tp
from enum import Enum, auto

from maya import cmds
from ueremoteclient import Client

FACIAL_CONTROLS_SET_NAME = "FacialControls"


class SyncStatus(Enum):
    COMPLETE = auto()
    CANCEL = auto()
    FAILURE = auto()


class LivelinkUtility:
    def __init__(self, settings: dict) -> None:
        self.settings = settings

    @classmethod
    def _get_min_and_max_frame(cls, node_list):
        keyframe_list = []
        for node in node_list:
            ref_keyframe_list = cmds.keyframe(node, query=True)
            if ref_keyframe_list is None:
                continue
            keyframe_list.extend(ref_keyframe_list)
        if keyframe_list == []:
            return (0, 0)
        else:
            return (min(keyframe_list), max(keyframe_list))

    @classmethod
    def offset_keyframe(cls, node: str, offset: int) -> None:
        node_keyframe_list = cmds.keyframe(node, query=True)
        min_frame, max_frame = cls._get_min_and_max_frame([node])

        if node_keyframe_list is None:
            return

        cmds.keyframe(node, edit=True,
                      relative=True,
                      includeUpperBound=True,
                      animation="objects",
                      option="over",
                      timeChange=offset,
                      time=(min_frame, max_frame))

    def sync_keyframe(self) -> SyncStatus:
        is_rig_animation: bool = self.settings["isRigAnimationCheckBox"]
        is_movie_file: bool = self.settings["isMovieFIleCheckBox"]
        is_wav_file: bool = self.settings["isWavFileCheckBox"]
        buffer_frame: int = self.settings["offsetFrame"]

        client = Client()
        result = client.run_file("get_current_sequnecer_frame", [])
        if result["success"] is not True:
            print(result)

        frame_info = eval(result["output"][0]["output"])

        if frame_info["end"] == 0:
            return SyncStatus.FAILURE

        min_frame: int = frame_info["start"]
        max_frame: int = frame_info["end"]

        # Mayaのスライダーを合わせる
        self.set_time_slider(min_frame, max_frame)

        maya_scene_min_frame, maya_scene_max_frame = self._get_min_and_max_frame(cmds.ls("*"))

        maya_scene_max_frame = int(maya_scene_max_frame)
        maya_scene_max_frame = int(maya_scene_max_frame)

        if maya_scene_min_frame == (min_frame - buffer_frame):
            is_execute = cmds.confirmDialog(title="警告", message="既にキーフレームが移動されてる可能性があります。\nそれでも実行しますか？", button="ok", cancelButton="cancel")

            if is_execute == "ok":
                ...
            else:
                return SyncStatus.CANCEL

        offset_frame = min_frame - maya_scene_min_frame - buffer_frame

        if is_rig_animation:
            rig_list = self.collect_rig_node()
            for rig in rig_list:
                self.offset_keyframe(rig, offset_frame)

        if is_movie_file:
            image_plane_list = cmds.ls(type="imagePlane")
            for image_plane in image_plane_list:
                former_value = cmds.getAttr(image_plane + ".frameOffset")
                cmds.setAttr(image_plane + ".frameOffset", former_value + (-1 * offset_frame))
                # cmds.refresh(force=True)
                # なぜかoffsetすると表示されなくなるので、imagePlaneの再描画を強制的にフラグ立てる
                cmds.setAttr(image_plane + ".useFrameExtension", 0)
                cmds.setAttr(image_plane + ".useFrameExtension", 1)

        if is_wav_file:
            audio_list = cmds.ls(type="audio")
            for audio in audio_list:
                former_value = cmds.getAttr(audio + ".offset")
                cmds.setAttr(audio + ".offset", former_value + offset_frame)

        cmds.refresh(force=True)
        return SyncStatus.COMPLETE

    def sync_time_slider_only(self) -> SyncStatus:
        """タイムスライダー同期単体用
        """
        client = Client()
        result = client.run_file("get_current_sequnecer_frame", [])
        if result["success"] is not True:
            return SyncStatus.FAILURE

        frame_info = eval(result["output"][0]["output"])

        if frame_info["end"] == 0:
            return SyncStatus.FAILURE

        min_frame: int = frame_info["start"]
        max_frame: int = frame_info["end"]

        # Mayaのスライダーを合わせる
        self.set_time_slider(min_frame, max_frame)

        return SyncStatus.COMPLETE

    def set_time_slider(self, min_frame: int, max_frame: int):
        cmds.playbackOptions(edit=True, maxTime=max_frame - 1)
        cmds.playbackOptions(edit=True, animationEndTime=max_frame - 1)

        cmds.playbackOptions(edit=True, minTime=min_frame)
        cmds.playbackOptions(edit=True, animationStartTime=min_frame)

    def collect_rig_node(self) -> tp.List[str]:
        # リグアニメーションをすべて取得する
        rig_sets = cmds.ls("*:FacialControls")
        if 1 != len(rig_sets):
            raise ValueError("FacialRig用のSetが複数存在します\nデータ状態を確認してください")

        if 0 == len(rig_sets):
            raise ValueError("FacialRig用のSetが取得できませんでした")

        rig_set = rig_sets[0]
        rig_list = cmds.sets(rig_set, q=True)
        return rig_list


if __name__ == "__main__":
    # リグアニメーションをすべて取得する
    rig_sets = cmds.ls("*:FacialControls")
    if 1 != len(rig_sets):
        raise ValueError("FacialRigが複数存在します")

    rig_set = rig_sets[0]

    rig_list = cmds.sets(rig_set, q=True)

    for rig in rig_list:
        LivelinkUtility.offset_keyframe(rig, 60)
