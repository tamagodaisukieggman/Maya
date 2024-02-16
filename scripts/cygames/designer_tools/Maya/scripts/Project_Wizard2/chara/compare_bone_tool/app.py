from .data import BoneCheckedData, CheckState
import maya.cmds as cmds

ATTRIBUTES = [
    "translateX",
    "translateY",
    "translateZ",
    "rotateX",
    "rotateY",
    "rotateZ",
    "scaleX",
    "scaleY",
    "scaleZ",
    "rotateAxisX",
    "rotateAxisY",
    "rotateAxisZ",
    "jointOrientX",
    "jointOrientY",
    "jointOrientZ",
    "stiffnessX",
    "stiffnessY",
    "stiffnessZ",
    "preferredAngleX",
    "preferredAngleY",
    "preferredAngleZ",
]


class BoneCompare(object):
    def __init__(self, source_bone: str, target_bone: str):
        self.source_bone = source_bone
        self.target_bone = target_bone
        self.checked_data = BoneCheckedData()

    def get_checked_data(self) -> BoneCheckedData:
        """チェックを行った後のデータを取得

        Returns:
            BoneCheckedData: _description_
        """
        return self.checked_data

    def exec_compare(self):
        """骨の比較の実行
        実行結果はchecked_dataに格納
        """
        result = self.compare_joint_attributes(
            self.source_bone, self.target_bone, ATTRIBUTES
        )
        self.set_check_data(result)

    def set_check_data(self, check_result: dict):
        """チェックしたデータをcheck_dataに格納

        Args:
            check_result (dict): チェックした結果を格納した辞書
        """
        if check_result:
            for attribute_name in check_result:
                if check_result[attribute_name]["has_error"]:
                    self.checked_data.check_state = CheckState.HAS_ERROR
                    break
            else:
                self.checked_data.check_state = CheckState.NO_ERROR
        else:
            return

        self.checked_data.result = check_result

    def compare_joint_attributes(
        self, joint_a: str, joint_b: str, attributes: list, tolerance: float = 0.001
    ) -> dict:
        """
        指定された属性の値を比較します。浮動小数点数の比較は指定された許容範囲内にあります。
        Args:
            joint_a (str): 比較したい最初の骨関節の名前
            joint_b (str): 比較したい2番目の骨関節の名前
            attributes (list): 比較したい属性のリスト
            tolerance (float): 浮動小数点数の比較の許容誤差
        Returns:
            dict: 各属性について、その値が同じかどうかを示す辞書
        """
        results = {}
        for attribute in attributes:
            value_a = cmds.getAttr(joint_a + "." + attribute)
            value_b = cmds.getAttr(joint_b + "." + attribute)

            is_success = True
            if isinstance(value_a, float) and isinstance(value_b, float):
                is_success = abs(value_a - value_b) <= tolerance

            else:
                is_success = value_a == value_b

            result = {
                "has_error": not is_success,
                "source_value": value_a,
                "target_value": value_b,
            }
            results[attribute] = result
        return results
