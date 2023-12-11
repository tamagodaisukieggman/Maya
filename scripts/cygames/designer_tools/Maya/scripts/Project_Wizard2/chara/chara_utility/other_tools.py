# -*- coding: utf-8 -*-
import typing as tp
import maya.cmds as cmds


class OtherTools:
    @classmethod
    def set_segment_scale(cls, value: bool, target_joints: tp.List["str"] = []):
        """targetsのノードのsegment scaleをオフに設定する
        targetがいなければ全てのjointに対して実行

        Args:
            targets (tp.List[&quot;str&quot;]): joint名のリスト
            value (bool): TrueならSegmentScaleがON
        """
        joints = []
        if target_joints == []:
            joints = cmds.ls(type="joint")
            print(
                "ノードが選択されていないので、シーン内全てのjointに対してsegmentScale OFFを適用しました",
            )

        else:
            for target_joint in target_joints:
                if "joint" == cmds.objectType(target_joint):
                    joints.append(target_joint)

        if len(joints) == 0:
            return False
        counter = 0
        for lp in joints:
            current_value = cmds.getAttr(lp + ".segmentScaleCompensate")
            if value != current_value:
                cmds.setAttr(lp + ".segmentScaleCompensate", value)
                print("segmentScale OFF >> {}".format(lp))
                counter += 1

        print("### {}件のノードにsegmentScale OFFを適応しました ###".format(counter))
