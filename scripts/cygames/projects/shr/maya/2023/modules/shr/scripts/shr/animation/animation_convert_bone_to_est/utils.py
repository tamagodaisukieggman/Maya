# -*- coding: utf-8 -*-
from typing import List

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

mel.eval("eST3start")

import tool_log

import eST3
import shr.animation.bakesimulation as bs

ROOT = "root_jnt"
PELVIS = "pelvis_jnt"
SPINE_BASE = "spine0_jnt"
COG_BASE = "baseCog"
FBX_PATH = r"C:\cygames\shrdev\shr_art\resources\animations\enemy\enm\enm2000_firedragon\fbx\a_enm2000_atk_breath_straight_f_lp1_nn_01.fbx"
SCENE_PATH = r"C:\cygames\shrdev\shr_art\resources\rigs\enemy\enm\enm2000_firedragon\work\maya\enm2000.mb"


class RigUtilTools:
    def __init__(self, namespace: str):
        """
        Args:
            namespace (str): リグのnamespaceを指定
        """
        self.ns = namespace
        self.send_logger()

    def send_logger(self) -> None:
        """ログ送信用"""
        version = "v2022.03.17"
        logger_type = "animation_convert_bone_to_est"

        logger = tool_log.get_logger(logger_type, version)
        logger.send_launch("")

    def get_root_joint(self):
        """root jointの取得

        Returns:
            str: ルートとなるジョイント名を返す
        """
        root_jnt = cmds.ls("{0}:{1}".format(self.ns, "root_jnt"))[0]
        return root_jnt

    def get_drv_joints(self):
        """補助骨を取得

        Returns:
            list: 補助骨の配列
        """
        root_jnt = self.get_root_joint()
        joints = cmds.listRelatives(root_jnt, ad=True, type="joint")
        drv_joints = []
        for lp in joints:
            if "_drv" in lp:
                drv_joints.append(lp)
        return drv_joints

    def set_lock_drv_joints(self, is_lock: bool):
        # for drv_joint in self.get_drv_joints():
        #     drv_joint
        ...

    def duplicate_main_joints(self) -> list:
        """主要な骨（補助骨以外の骨）を複製

        Returns:
            list: 複製した骨群
        """
        root = self.get_root_joint()
        children = cmds.listRelatives(root, ad=True, type="joint")
        children.append(root)
        main_joints = []
        for lp in children:
            if "_drv" not in lp:
                main_joints.append(lp)

        cmds.select(main_joints, r=True)
        cmds.duplicate(po=True)
        dup_mainjoints = cmds.ls(sl=True)

        return dup_mainjoints

    def reconnection_animcurve(self, target_joints):
        """アニメーションカーブの作成

        Args:
            target_joints (list): 骨
        """
        namespace = self.ns
        sources = []
        targets = []
        # for lp in target_joints:
        connections = cmds.listConnections(
            target_joints, c=True, d=True, s=True, p=True, type="animCurve"
        )
        max_index = len(connections)

        for i in range(max_index)[::2]:
            sources.append(connections[i])
            targets.append(connections[i + 1])

        for source, target in zip(sources, targets):
            try:
                cmds.disconnectAttr(target, source)

                source = namespace + ":" + source
                cmds.connectAttr(target, source, f=True)

            except RuntimeError:
                continue


class eSTRigTools:
    def __init__(self, namespace: str):
        """
        Args:
            namespace (str): リグのnamespaceを指定
        """
        self.ns = namespace

    def extended_rig(self):
        return eST3.mCmds.ExtendedRig(self.ns)

    def get_external_anim_plugs(self) -> List[eST3.mCmds.AnimPlugs]:
        """外部リグのanimPlugsを取得取得

        Args:
            namespace (_type_): 対象となるrigのnamespace

        Returns:
            _type_: external_rigの
        """
        external_rigs = []
        for lp in eST3.mCmds.AnimPlugs(
            "{}:animPlugs".format(self.ns)
        ).listChildAnimPlugs(r=True):
            if lp.getAnimPlugsType() == "externalRig":
                external_rigs.append(lp)
        return external_rigs

    def get_nb_unitnodes(self) -> List[eST3.mCmds.UnitNode]:
        """noBuiltInオプションをONにした外部リグ用のUnitを取得

        Returns:
            List[eST3.mCmds.UnitNode]: unitnode
        """
        return self.extended_rig().listUnitNodes(nb=True, asm=True)

    def get_unitnodes(self) -> List[eST3.mCmds.UnitNode]:
        """unitnodeの取得

        Returns:
            List[eST3.mCmds.UnitNode]: unitnode
        """
        return self.extended_rig().listUnitNodes(asm=True)

    def connect_controller(self, is_connect: bool):
        eST3.rCmds.ConnectController(
            connect=is_connect, rig=self.extended_rig(), unit="*"
        )


class eSTAnimationConverter:
    """fbxの骨アニメーションをeSTのリグアニメーションにコンバート。
    現在shenronの仕様に決め打ち"""

    def __init__(self, namespace: str):
        self.ns = namespace
        self.est_rig_tools = eSTRigTools(self.ns)
        self.rig_util_tools = RigUtilTools(self.ns)

    def _get_joint_from_externalrig(self, ctrl):
        ctrl_dist = cmds.listConnections(ctrl, d=True)
        for parent_const in ctrl_dist:
            obj_type = cmds.objectType(parent_const)
            if obj_type == "parentConstraint" or obj_type == "aimConstraint":
                for parent_const_dist in cmds.listConnections(parent_const, d=True):
                    if cmds.objectType(parent_const_dist) == "joint":
                        return parent_const_dist

    def _get_external_ctrl(self):
        animatables = []
        anim_plugs = "{}:animPlugs".format(self.ns)
        for lp in eST3.mCmds.AnimPlugs(anim_plugs).listChildAnimPlugs(r=True):
            if lp.getAnimPlugsType() == "externalRig":
                animatables.extend(lp.listAnimatables(nodesOnly=True))
        return animatables

    def _convert_animjoint_to_baseskel(self):
        parts = []
        for lp in self.est_rig_tools.get_nb_unitnodes():
            parts_dict_value = {
                "ebc": "rigConnector",
                "s": None,
            }
            parts_dict_value["t"] = lp
            parts.append(parts_dict_value)
            parts_dict_value = {"bcc": "baseToCtrl"}

            parts_dict_value["t"] = lp
            parts.append(parts_dict_value)

        # ----------
        # convert animation joint to baseSkeleton
        eST3.rCmds.ConvertAnimation(
            parts=parts,
            bake=True,
            timeRange=0,
            startFrame=1.0,
            endFrame=10.0,
            sampleBy=1.0,
            tangentType="linear",
            startMargin=0.0,
            endMargin=0.0,
            preserveOutsideKeys=True,
            removeStaticKeys=True,
            eulerFilter=False,
            simplify=False,
        )

    def _convert_baseskel_to_ctl(self):
        parts = []

        for lp in self.est_rig_tools.get_unitnodes():
            parts_dict_value = {"bcc": "baseToCtrl"}
            parts_dict_value["t"] = lp

            if lp.getUnit() in ["plntArm", "digiLeg"]:
                if lp.getUnit() == "plntArm":
                    parts_dict_value["bco"] = {"armR": 3}
                elif lp.getUnit() == "digiLeg":
                    parts_dict_value["bco"] = {"legR": 3}

            elif lp.getUnit() in ["bipedArm", "bipedLeg"]:
                if lp.getUnit() == "bipedArm":
                    parts_dict_value["bco"] = {"armR": 2}
                # elif lp.getUnit() == "bipedLeg":
                #     parts_dict_value["bco"] = {"legR": 2}

            parts.append(parts_dict_value)

        # baseSkeleton to controller
        eST3.rCmds.ConvertAnimation(
            parts=parts,
            bake=True,
            timeRange=0,
            startFrame=1.0,
            endFrame=10.0,
            sampleBy=1.0,
            tangentType="linear",
            startMargin=0.0,
            endMargin=0.0,
            preserveOutsideKeys=True,
            removeStaticKeys=True,
            eulerFilter=False,
            simplify=False,
        )

    def convert_animation(self, convert_scene_path: str, fbx_path: str):
        # ----------
        # open maya scene
        cmds.file(convert_scene_path, f=1, o=1)

        external_ctrls = self._get_external_ctrl()

        ctrl_and_joint = {}
        for lp in external_ctrls:
            if lp == "Asset_ctrl":
                continue
            if self._get_joint_from_externalrig(str(lp)) == None:
                continue
            ctrl_and_joint[str(lp)] = self._get_joint_from_externalrig(str(lp))

        attribute_connection_pair = {
            "constraintRotateX": "rotateX",
            "constraintRotateY": "rotateY",
            "constraintRotateZ": "rotateZ",
            "constraintTranslateX": "translateX",
            "constraintTranslateY": "translateY",
            "constraintTranslateZ": "translateZ",
        }

        eST3.rCmds.DisconnectExternalRig(
            rig=eST3.mCmds.ExtendedRig(self.ns),
            units=self.est_rig_tools.get_nb_unitnodes(),
            animPlugs=self.est_rig_tools.get_external_anim_plugs(),
            bake=False,
            echo=True,
        )

        # disconnect est controller
        self.est_rig_tools.connect_controller(False)

        # disconnect external rig
        constraints_delete_later = []
        constraint_and_joint = {}
        to_bake = []
        for ctrl, jnt in ctrl_and_joint.items():
            bind_jnt = jnt
            src_node = pm.listConnections("{}".format(bind_jnt), s=True, d=False)
            for s in set(src_node):
                if s.nodeType() == "parentConstraint" or "aimConstraint":
                    for src, dst in attribute_connection_pair.items():
                        try:
                            cmds.disconnectAttr(
                                "{}.{}".format(s, src), "{}.{}".format(bind_jnt, dst)
                            )
                            constraint_and_joint[
                                "{}.{}".format(s, src)
                            ] = "{}.{}".format(bind_jnt, dst)
                        except:
                            # print("pass {},{}".format(bind_jnt, dst))
                            continue

            external_ctrl = ctrl
            to_bake.append(external_ctrl)
            pcn = cmds.parentConstraint(bind_jnt, external_ctrl, mo=True)
            constraints_delete_later.append(pcn[0])

        # コンバートの際にはAsset_ctrl.root_jnt_cnstの値を0に設定しておく
        cmds.setAttr("{}:Asset_ctrl.root_jnt_cnst".format(self.ns), 0)

        # constraint baseCog from pelvis_jnt
        pcon = cmds.parentConstraint(
            "{}:pelvis_jnt".format(self.ns),
            "{}:baseCog".format(self.ns),
            mo=False,
        )

        # ----------
        # create dummly loc
        dummy_loc = cmds.spaceLocator(name="root_dummy_loc")
        cmds.parentConstraint("{}:{}".format(self.ns, ROOT), dummy_loc, mo=False)
        to_bake.append(dummy_loc[0])

        # dummy joint
        dup_main_joints = self.rig_util_tools.duplicate_main_joints()

        mel.eval("FBXImportMode -v Exmerge")

        # ----------
        # import animation to dummy joint.
        cmds.file(
            fbx_path,
            i=True,
            type="FBX",
            mergeNamespacesOnClash=False,
            ra=True,
            options="fbx",
            importTimeRange="override",
            importFrameRate=True,
        )
        cmds.namespace(set=":{}".format(self.ns))

        self.rig_util_tools.reconnection_animcurve(dup_main_joints)

        cmds.delete(dup_main_joints)

        # ----------
        cmds.delete(
            cmds.parentConstraint(
                dummy_loc, "{}:{}".format(self.ns, "layout"), mo=False
            )
        )

        # -----
        constraints_delete_later.append(
            cmds.parentConstraint(
                "{}:pelvis_jnt".format(self.ns), "{}:baseCog".format(self.ns), mo=False
            )[0]
        )
        constraints_delete_later.append(
            cmds.parentConstraint(
                "{}:root_jnt".format(self.ns), "{}:baseRoot".format(self.ns), mo=False
            )[0]
        )

        # ----------
        # bake to baseCog and externalRig
        cmds.refresh(su=True)
        sf = cmds.playbackOptions(q=True, min=True)
        ef = cmds.playbackOptions(q=True, max=True)

        mask = eST3.eST.kMsgMask.warning
        prev = eST3.eST.Printer.preserveMsgMask(mask)

        # bake objects
        to_bake.append("{}:baseCog".format(self.ns))
        # todo: baseRootのベイクを追加しました
        to_bake.append("{}:baseRoot".format(self.ns))
        try:
            cmds.select(to_bake, r=True)
            bs.main()

            eST3.eST.warning("this message is never shown.")
        finally:
            eST3.eST.Printer.preserveMsgMask(mask, prev)

        # delete parentConstraint
        cmds.delete(constraints_delete_later)

        # animjointからbaseskelへアニメーションをコンバート
        self._convert_animjoint_to_baseskel()

        # baseskelからctrlへアニメーションをコンバート
        self._convert_baseskel_to_ctl()

        # ----------
        # delete baseSkeleton animation keys
        for j in pm.listRelatives(
            "{}:globalLayout".format(self.ns), ad=True, typ="joint"
        ):
            pm.delete(pm.listConnections(j, t="animCurve"))
        pm.delete(pm.listConnections("{}:baseCog".format(self.ns), t="animCurve"))
        pm.delete(pm.listConnections("{}:baseRoot".format(self.ns), t="animCurve"))

        # ----------
        # connect eST controller to baseSkeleton
        self.est_rig_tools.connect_controller(True)

        unit_list = []

        for lp in self.est_rig_tools.get_nb_unitnodes():
            unit_list.append([lp, eST3.mCmds.Prefix(self.ns)])

        anim_plugs = []
        for lp in self.est_rig_tools.get_external_anim_plugs():
            anim_plugs.append([lp, eST3.mCmds.Prefix(self.ns)])

        # connect baseSkeleton to external rig
        eST3.rCmds.ConnectExternalRig(
            rig=eST3.mCmds.ExtendedRig(self.ns),
            units=unit_list,
            animPlugs=anim_plugs,
            echo=True,
        )

        constraints_delete_later = []
        bake_controller = [
            "{}:{}".format(self.ns, ctrl) for ctrl in ["root_jnt_ctrl", "root"]
        ]
        constraints_delete_later.append(
            cmds.parentConstraint(
                dummy_loc, "{}:{}".format(self.ns, "root_jnt_ctrl"), mo=False
            )[0]
        )
        constraints_delete_later.append(
            cmds.parentConstraint(dummy_loc, "{}:{}".format(self.ns, "root"), mo=False)[
                0
            ]
        )

        # reconnect parentConstraint to bindJoint
        for src, dct in constraint_and_joint.items():
            try:
                cmds.connectAttr(src, dct, force=True)
            except:
                # print("pass {},{}".format(src, dct))
                continue

        # bake root animation.
        cmds.bakeResults(
            bake_controller,
            simulation=True,
            t=(sf, ef),
            sampleBy=1,
            oversamplingRate=1,
            disableImplicitControl=True,
            preserveOutsideKeys=True,
            sparseAnimCurveBake=False,
            removeBakedAttributeFromLayer=False,
            removeBakedAnimFromLayer=False,
            bakeOnOverrideLayer=False,
            minimizeRotation=True,
            controlPoints=False,
            shape=True,
        )

        cmds.refresh(su=False)

        # --------
        cmds.delete(dummy_loc)
