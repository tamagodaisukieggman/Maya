# -*- coding: utf-8 -*-
import maya.cmds as cmds

HELPER_JYOINT = "helper"

class ConstraintObject:
    type = ""
    text = ""
    error_node = ""

    name = ""
    constraint = ""
    constraints = []

    const_name = ""
    constraint_type = ""

    no_constraint = [
            "shoulder",
            "elbow",
            "thigh",
            "knee",
            "eye",
            "upperarm",
            ]
    
    # joint_category = [
    #     "move",
    #     "mtp"
    #     ]

    # need_constraint_type = [
    #     "parentConstraint",
    #     "orientConstraint",
    #     "pointConstraint",
    # ]

    # constraint_types = {
    #             "parentConstraint": [
    #                 "move",
    #                 "mtp",
    #                 "root",
    #                 "pelvis",
    #                 "hand:02",
    #                 "foot:02",
    #                 ],

    #             "orientConstraint": [
    #                 "spine",
    #                 "neck",
    #                 "head",
    #                 "jaw",
    #                 "scapula",
    #                 "hand:01",
    #                 "foot:01",
    #                 "tail",
    #                 "carpal",
    #                 "thumb",
    #                 "index",
    #                 "middle",
    #                 "metacarpal",
    #                 "ring",
    #                 "pinky",
    #                 "carpal",
    #                 "tarsal",
    #                 "footThumb",
    #                 "footIndex",
    #                 "footMiddle",
    #                 "footRing",
    #                 "metatarsal",
    #                 ],
    #             "pointConstraint":
    #             [
    #                 "hand:02",
    #                 "foot:02",
    #             ],
    #             }

    # const_names = [
    #     "main",
    #     "pelvis",
    #     ]

    error = u""

    def __init__(self, name):
        self.name = name
        self.short_name = name.split("|")[-1]
        name_split = self.short_name.split("_")
        self.name_split = name_split
        
        # 名前の確認をしてからコンストレインをチェック
        # helper などコンストレインをチェックしないジョイントがあるため
        if self.check_name():
            self.check_constraint()

        
    def check_name(self):
        """名前を確認
        jnt_mtp_root02　最低2つのアンダーバーが入る

        :return: [description]
        :rtype: bool
        """
        if len(self.name_split) < 3:
            self.error = u"名前が不正"
            return False
        return True
    
    def check_constraint(self):
        """コンストレインの種類を確認
        helper 以外のジョイント、
        "shoulder", "elbow", "thigh", "knee", "eye", "upperarm"
        以外のジョイントは全てコンストレインが入っている

        コンストレインの種類は、
        一つの場合は、ペアレント、もしくはオリエント

        二つの場合は、
        ポイント、オリエント
        :return: [description]
        :rtype: [type]
        """
        _error = ""
        constraints = []

        # Helperジョイントを抜かす
        if self.name_split[2] == HELPER_JYOINT:
            return "not check"
        
        # 特定の種類のジョイントを抜かす
        elif self.name_split[-2] in self.no_constraint:
            return "not check"

        else:
            constraints = cmds.listConnections(self.name, s=False, d=True, type="constraint")
            if not constraints:
                _error = u"コンストレインがない"
                self.error = _error
                return _error
            else:
                constraints = list(set(constraints))
                constraint_types = [cmds.nodeType(x) for x in constraints]
                if len(constraints) == 1:
                    if constraint_types[0] not in ["parentConstraint", "orientConstraint"]:
                        _error = u"既定のコンストレインではない"
                elif len(constraints) == 2:
                    for constraint_type in constraint_types:
                        _flag = False
                        
                        if constraint_type in ["pointConstraint", "orientConstraint"]:
                            _flag = constraint_type
                        else:
                            if _flag and _flag == constraint_type:
                                # _error = u"{}".format(", ".join(constraints))
                                _error = u"既定のコンストレインではない"
                else:
                    _error = u"既定のコンストレインがない"
                self.error = _error

        return _error

    # コンストレインの種類を選別しようとしていたが
    # 骨の名前とコンストレインの種類が一定ではないのでやめにした
    # 今後復活する可能性もあり

    # def check_constraint_types(self):
    #     for constraint_type in self.constraint_type_list:
    #         type_flag = ""
    #         if constraint_type not in self.need_constraint_type:
    #             self.error = u"11 constraint type error [ {} ]".format(self.short_name)
    #         else:
    #             if constraint_type == "orientConstraint":
    #                 if type_flag and type_flag != "pointConstraint":
    #                     self.error = "12 constraint type error [ {} ]".format(self.short_name)
    #                 type_flag = constraint_type
    #             if constraint_type == "parentConstraint":
    #                 if type_flag:
    #                     self.error = "13 constraint type error [ {} ]".format(self.short_name)
    #                 type_flag = constraint_type
    #             if constraint_type == "pointConstraint":
    #                 if type_flag and type_flag != "orientConstraint":
    #                     self.error = "14 constraint type error [ {} ]".format(self.short_name)
    #                 type_flag = constraint_type

    # def check_constraint_type(self):
    #     if self.constraint_type not in self.constraint_types.keys():
    #         self.error = "1 constraint type error [ {} ]".format(self.short_name)

    # def check_joint_categorys(self):
    #     for constraint_type in self.constraint_type_list:
    #         if self.name_split[1] in self.joint_category:
    #             if self.name_split[1] not in self.constraint_types[constraint_type]:
    #                 self.error = "[ {} ] constraint type error [ {} ]".format(self.name_split[1], self.short_name)
    #         else:
    #             if self.name_split[3] in ["foot", "hand"]:
    #                 name_join = "{}:{}".format(self.name_split[3], self.name_split[-1])
    #                 if name_join not in self.constraint_types[constraint_type]:
    #                     self.error = "2 constraint type error [ {} ]".format(self.short_name)
    #             elif self.name_split[3] not in self.constraint_types[constraint_type]:
    #                 self.error = "3 constraint type error [ {} ]".format(self.short_name)

    # def check_joint_category(self):
    #     if self.name_split[1] in self.joint_category:
    #         if self.name_split[1] not in self.constraint_types[self.constraint_type]:
    #             self.error = "[ {} ] constraint type error [ {} ]".format(self.name_split[1], self.short_name)
    #     else:
    #         if self.name_split[3] in ["foot", "hand"]:
    #             name_join = "{}:{}".format(self.name_split[3], self.name_split[-1])
    #             if name_join not in self.constraint_types[self.constraint_type]:
    #                 self.error = "2 constraint type error [ {} ]".format(self.short_name)
    #         elif self.name_split[3] not in self.constraint_types[self.constraint_type]:
    #             self.error = "3 constraint type error [ {} ]".format(self.short_name)

def main(scene_path):
    types = []
    texts = []
    error_nodes = []

    all_joints = cmds.ls(type="joint", l=True)

    # リファレンスとして読まれている骨は除外する
    for x in all_joints:
        if ":" in x:
            continue

        _jnt = ConstraintObject(x)
        if _jnt.error:
            texts.append(_jnt.error)
            types.append("constraint")
            error_nodes.append(x)

    return zip(texts, types, error_nodes)