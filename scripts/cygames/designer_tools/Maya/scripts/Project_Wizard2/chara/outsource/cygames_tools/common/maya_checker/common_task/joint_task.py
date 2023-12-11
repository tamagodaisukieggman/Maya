# -*- coding: utf-8 -*-
import functools
import typing as tp

from ..task import CheckTaskBase
from ..scene_data import MayaSceneDataBase
from ..data import ErrorType

import maya.cmds as cmds
from .. import utility as util


class JointSegmentScale(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "セグメントスケール"

    def exec_task_method(self):
        segment_scale_joints = self.get_joints_with_segment_scale_on()
        if len(self.get_joints_with_segment_scale_on()) > 0:
            self.set_error_data(
                "joint_segment_scale", segment_scale_joints, "セグメントスケールがONのjoint"
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        error_objects = self.get_debug_target_objects("joint_segment_scale")
        JointSegmentScale.set_segmentScaleCompensate_off(error_objects)

    @staticmethod
    def set_segmentScaleCompensate_off(joint_nodes: tp.List[str]) -> None:
        """
        対象のジョイントのsegmentScaleCompensateをOFFにする関数
        Args:
            joint_nodes (List[str]): 対象のジョイントノードのリスト
        Returns: なし
        """
        for node in joint_nodes:
            if cmds.nodeType(node) == "joint":
                cmds.setAttr(node + ".segmentScaleCompensate", 0)

    @staticmethod
    def get_joints_with_segment_scale_on() -> tp.List[str]:
        """全てのjointを取得し、segment scaleがONの物を返す関数

        Returns:
            tp.List[str]: セグメントスケールがONになっているジョイント名のリスト
        """
        all_joints = cmds.ls(type="joint")
        joints_with_segment_scale_on = []
        for joint in all_joints:
            segment_scale = cmds.getAttr(joint + ".segmentScaleCompensate")
            if segment_scale:
                joints_with_segment_scale_on.append(joint)
        return joints_with_segment_scale_on


class HasKeyframeJoints(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "キーフレーム"

    def exec_task_method(self):
        current_func = functools.partial(self.check_keyframe_joints)
        self.register_error_info_to_mesh_descendants(
            current_func,
            "has_key_frame_joints",
            "キーフレームが設定されているjoint",
        )

    @staticmethod
    def get_objects_with_keyframes(obj_list: tp.List[str]) -> tp.List[str]:
        """対象のオブジェクトにキーフレームが存在しているかどうかを確認し、キーフレームが存在しているオブジェクトをすべて返す関数

        Args:
            obj_list (tp.List[str]): オブジェクト名のリスト

        Returns:
            tp.List[str]: キーフレームが存在しているオブジェクト名のリスト
        """
        objects_with_keyframes = []
        for obj in obj_list:
            keyframes = cmds.keyframe(obj, query=True, keyframeCount=True)
            if keyframes:
                objects_with_keyframes.append(obj)
        return objects_with_keyframes

    def check_keyframe_joints(self, obejcts: tp.List[str]) -> tp.List[str]:
        """キーフレームを保有しているかどうか確認する

        Args:
            obejcts (tp.List[str]): 対象のオブジェクト

        Returns:
            tp.List[str]: キーフレームを保有しているジョイント
        """
        joints = util.get_bound_joints(obejcts)
        has_keyframe_joints = self.get_objects_with_keyframes(joints)
        return has_keyframe_joints


# 汎用関数
class JointCount(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ジョイント総数"

    def exec_task_method(self):
        max_count = self._get_max_count()

        all_joints = []
        for root in self.maya_scene_data.root_nodes:
            all_joints.extend(util.get_bound_joints(root.get_all_mesh_transform()))

        all_joints = list(set(all_joints))
        if JointCount.is_joint_below_limit(all_joints, max_count):
            self.set_error_type(ErrorType.NOERROR)
        else:
            self.set_error_data(
                "joint_count",
                [f"現在のジョイント数 >> {len(all_joints)} 本"],
                f"ジョイント数が {max_count} 本を超えています",
            )

    def _get_max_count(self) -> int:
        """骨数の最大値の取得
        override用に関数で分ける

        Returns:
            int: 骨数の最大値
        """
        return self.extra_data["max_count"]

    @staticmethod
    def is_joint_below_limit(obj_list: tp.List[str], max_count: int) -> tp.List[str]:
        """対象のオブジェクトにキーフレームが存在しているかどうかを確認し、キーフレームが存在しているオブジェクトをすべて返す関数

        Args:
            obj_list (tp.List[str]): オブジェクト名のリスト

        Returns:
            tp.List[str]: キーフレームが存在しているオブジェクト名のリスト
        """
        return len(obj_list) <= max_count
