from maya import cmds
from shr.cutscene.sequencer import const
from PySide2 import QtCore

from ..api import ClipStatus, MotionClipData
from ..lib.time import fetch_now_time


class MayaMotionClipEditor(object):
    """Maya側のClip編集機能

    - 移動した時のモーションのオフセット
    - In Out時のモーション追従。(ScreenWriterでやるかも)

    Args:
        object ([type]): [description]
    """

    @classmethod
    def get_clip_range(cls, reference_node):
        min_frame, max_frame = cls.calculate_animation_range(reference_node)
        current_frame = cmds.currentTime(query=True)

        return (min_frame, max_frame, current_frame)

    @classmethod
    def calculate_animation_range(cls, ref_node):
        """キーフレームの長さを計算する
        """
        ref_bind_node_list = cmds.referenceQuery(ref_node, nodes=True)
        min_max_range = cls._get_min_and_max_frame(ref_bind_node_list)

        return min_max_range

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
    def move_clip(cls, ref_node, offset):
        """クリップ移動
        Clipのモーションを移動値に合わせてKeyframeを移動する
        """
        ref_bind_node_list = cmds.referenceQuery(ref_node, nodes=True)
        for ref_bind_node in ref_bind_node_list:
            ref_keyframe_list = cmds.keyframe(ref_bind_node, query=True)
            min_frame, max_frame = cls._get_min_and_max_frame([ref_bind_node])
            # ここから続き
            if ref_keyframe_list is None:
                continue

            cmds.keyframe(ref_bind_node, edit=True,
                          relative=True,
                          includeUpperBound=True,
                          animation="objects",
                          option="over",
                          timeChange=offset,
                          time=(min_frame, max_frame))

    @classmethod
    def cut_clip(cls):
        ...

    @classmethod
    def marge_clip(cls):
        ...


class MayaMoveClipMoveDelayTimer(object):
    """Maya用のクリップ移動の遅延タイマー

    即時実行だとレスポンスに問題があるため、QTimerで処理をまとめて実行させる。
    """
    INTERVAL_MILLISECOND = 120

    def __init__(self) -> None:
        self._move_timer = QtCore.QTimer()
        self._move_timer.setSingleShot(True)
        self._move_timer.timeout.connect(self._motion_move_event)
        self._move_frame = 0
        self._move_ref_node = None

    def clip_moved(self, clip: MotionClipData, old_frame, new_frame):
        self._move_frame += new_frame - old_frame
        self._move_timer.start(self.INTERVAL_MILLISECOND)

        clip_property = clip.get_clip_property()
        reference_path = clip_property[const.Event.EVENT_REFERENCE_PATH]

        if not self._move_ref_node:
            self._move_ref_node = reference_path

        if self._move_ref_node != reference_path:
            self._motion_move_event()
            self.clip_moved(clip, old_frame, new_frame)

        clip.set_status(ClipStatus.Edit, rebuild=False)
        clip.updated_time = fetch_now_time()

    def _motion_move_event(self):
        if self._move_ref_node:
            MayaMotionClipEditor.move_clip(self._move_ref_node, self._move_frame)
            self._move_frame = 0
            self._move_ref_node = None
