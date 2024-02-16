import os
import typing as tp
from pathlib import Path
import maya.cmds as cmds
import maya.mel as mel


IMPORT_PATH = "c:/cygames/wiz2/team/3dcg/mot/weightcheck/fbx/"
# IMPORT_PATH = f"{Path(__file__).parent.as_posix()}/fbx/"
IMPORT_NAMES = {
    "p1": ["an_p1_cmn_emote_900.fbx", "an_p1_cmn_emote_901.fbx"],
    "p2": ["an_p2_cmn_emote_900.fbx", "an_p2_cmn_emote_901.fbx"],
}
CONTROLLER_NAME = "__demo_motion_controller"
DEMO_MOTION_NAMESPACE_BASE = "__demo_motion_"


class DemoAnimationManager:
    def __init__(self):
        ...

    # animation_controller
    def flip_animation_type(self):
        if cmds.ls(CONTROLLER_NAME):
            controller = cmds.ls(CONTROLLER_NAME)[0]
            current_rot = cmds.getAttr(f"{controller}.used_rot")
            current_trans = cmds.getAttr(f"{controller}.used_trans")

            cmds.setAttr(f"{controller}.used_rot", int(not bool(current_rot)))
            cmds.setAttr(f"{controller}.used_trans", int(not bool(current_trans)))

        if not bool(current_rot) == True:
            cmds.headsUpMessage("<体操>モーションが有効になりました")
        else:
            cmds.headsUpMessage("<移動>モーションが有効になりました")

    # remove

    def remove_demo_motion(self):
        self.reset_timeline_slider()
        self.delete_controller()
        self.delete_constraints()
        self.remove_reference()
        self.go_to_bindpose_to_all_mesh()

    @staticmethod
    def reset_timeline_slider():
        cmds.currentTime(0)

    def remove_reference(self):
        self.remove_reference_by_namespace(DEMO_MOTION_NAMESPACE_BASE + "_0")
        self.remove_reference_by_namespace(DEMO_MOTION_NAMESPACE_BASE + "_1")

    def delete_controller(self):
        if self.check_exsit_controller():
            cmds.delete(CONTROLLER_NAME)

    def check_exsit_controller(self):
        return cmds.objExists(CONTROLLER_NAME)

    def delete_constraints(self):
        consts = self.get_all_demo_motion_constraint()
        if consts:
            cmds.delete(consts)

    def get_all_demo_motion_constraint(self) -> tp.List[str]:
        consts = cmds.ls(f"{DEMO_MOTION_NAMESPACE_BASE}*:", type="parentConstraint")
        return consts

    @staticmethod
    def remove_reference_by_namespace(namespace):
        reference_nodes = cmds.ls(namespace + ":*")

        for node in reference_nodes:
            try:
                ref_file = cmds.referenceQuery(node, f=True)
                cmds.file(ref_file, removeReference=True)
                break
            except RuntimeError as e:
                print(str(e))

    @staticmethod
    def go_to_bindpose_to_all_mesh():
        meshes = cmds.ls(type="mesh")
        parents = list(set(cmds.listRelatives(meshes, p=True, type="transform")))
        cmds.select(parents, r=True)
        mel.eval("GoToBindPose;")
        cmds.select(clear=True)


class DemoAnimationImporter:
    def __init__(self, import_type: str):
        self.import_type = import_type
        self.manager = DemoAnimationManager()

    def set_fbx_import_preset(self):
        """load presetの設定"""
        preset_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), ".", "chara_animation_import.fbximportpreset"
            )
        ).replace("\\", "/")
        mel.eval('FBXLoadImportPresetFile -f "{}"'.format(preset_path))

    def constraint_bones_by_namespaces(self, namespaces: str):
        """
        指定したファイルをリファレンスで読み込み、含まれる骨を同名の既存骨とparent constraintします。
        Args:
            file_path (str): リファレンスとして読み込むファイルのパス。
        """
        # Create a controlling locator
        control_locator = self.create_controll_locator()

        joints_1 = cmds.ls(namespaces[0] + ":*", type="joint")
        joints_2 = cmds.ls(namespaces[1] + ":*", type="joint")
        for joint_1, joint_2 in zip(joints_1, joints_2):
            constraint_name = joint_1.split(":")[1]
            existing_joint = cmds.ls(constraint_name, type="joint")
            exception_values = []

            ref_objects = cmds.ls("*:" + constraint_name, type="joint")

            # 今回インポートしてきたオブジェクトは対象に含めない
            for lp in ref_objects:
                if namespaces[0] in lp or namespaces[1] in lp:
                    exception_values.append(lp)

            # exception_valuesに含まれる値を取り除く
            ref_objects = [
                value for value in ref_objects if value not in exception_values
            ]

            existing_joint.extend(ref_objects)

            if existing_joint:
                for lp in existing_joint:
                    constraint = cmds.parentConstraint(joint_1, joint_2, lp, mo=False)[
                        0
                    ]
                    cmds.connectAttr(
                        control_locator + ".used_rot",
                        constraint + "." + constraint_name + "W0",
                    )
                    cmds.connectAttr(
                        control_locator + ".used_trans",
                        constraint + "." + constraint_name + "W1",
                    )

                    cmds.rename(constraint, DEMO_MOTION_NAMESPACE_BASE + constraint)

    def create_controll_locator(self) -> str:
        """コントローラー(ロケーター)の作成

        Returns:
            str: 作成したロケーター名
        """

        control_locator = cmds.spaceLocator(n=CONTROLLER_NAME)[0]
        cmds.addAttr(control_locator, ln="used_rot", at="double", min=0, max=1, dv=1)
        cmds.addAttr(control_locator, ln="used_trans", at="double", min=0, max=1, dv=0)
        cmds.setAttr(control_locator + ".used_rot", e=True, keyable=True)
        cmds.setAttr(control_locator + ".used_trans", e=True, keyable=True)
        cmds.setAttr(control_locator + ".visibility", 0)
        return control_locator

    def import_reference_and_constraint(self):
        """referenceを読み込んで、コンストレインを接続する"""

        def _reference_and_constraint(file_paths):
            namespaces = []
            namespace_base = DEMO_MOTION_NAMESPACE_BASE
            for i, file_path in enumerate(file_paths):
                namespace = namespace_base + "_" + str(i)
                # self.set_fbx_import_preset()
                cmds.file(
                    file_path,
                    r=True,
                    type="FBX",
                    ignoreVersion=True,
                    gl=True,
                    mergeNamespacesOnClash=False,
                    namespace=namespace,
                    options="v=0;p=17;f=0",
                )

                self.set_invisible_by_namespace(namespace=namespace)
                namespaces.append(namespace)
            self.constraint_bones_by_namespaces(namespaces)
            return namespace_base

        if self.import_type in ["p0", "p1"]:
            file_names = IMPORT_NAMES["p1"]
            file_paths = [IMPORT_PATH + name for name in file_names]
            _reference_and_constraint(file_paths)

        elif self.import_type in ["p2"]:
            file_names = IMPORT_NAMES["p2"]
            file_paths = [IMPORT_PATH + name for name in file_names]
            _reference_and_constraint(file_paths)

    @staticmethod
    def set_invisible_by_namespace(namespace: str):
        for lp in cmds.ls(namespace + ":*", type="transform"):
            cmds.setAttr(f"{lp}.visibility", 0)

    def execute(self):
        if not self.manager.check_exsit_controller():
            self.import_reference_and_constraint()
        else:
            cmds.warning("既にdemo motionがインポート済みです。一度削除を行ってから再度実行してください。")
