# -*- coding: utf-8 -*-
from typing import List

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

mel.eval("eST3start")

import eST3


class eSTRigTools:
    def __init__(self, namespace: str):
        """
        Args:
            namespace (str): リグのnamespaceを指定
        """
        self.ns = namespace

    def extended_rig(self):
        return eST3.mCmds.ExtendedRig(self.ns)

    def get_anim_plugs(self):
        """外部リグのanimPlugsを取得取得

        Args:
            namespace (_type_): 対象となるrigのnamespace

        Returns:
            _type_: _description_
        """
        external_rigs = []
        for lp in eST3.mCmds.AnimPlugs(
            "{}:animPlugs".format(self.ns)
        ).listChildAnimPlugs(r=True):
            if lp.getAnimPlugsType() == "externalRig":
                external_rigs.append(lp)
        return external_rigs

    def get_nb_unitnodes(self):
        return self.extended_rig().listUnitNodes(nb=True, asm=True)

    def get_unitnodes(self):
        return self.extended_rig().listUnitNodes(asm=True)

    def convert_animjoint_to_baseskel(self):
        parts = []
        for lp in self.get_nb_unitnodes():
            parts_dict_value = {
                "ebc": "rigConnector",
                "s": None,
            }
            parts_dict_value["t"] = lp

        parts.append(parts_dict_value)
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
            removeStaticKeys=False,
            eulerFilter=False,
            simplify=False,
        )

    def convert_baseskel_to_ctl(self):
        parts = []
        for lp in self.get_unitnodes():
            parts_dict_value = {"bcc": "baseToCtrl"}
            parts_dict_value["t"] = lp
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
            removeStaticKeys=False,
            eulerFilter=False,
            simplify=False,
        )

    def connect_controller(self, is_connect: bool):
        eST3.rCmds.ConnectController(
            connect=is_connect, rig=self.extended_rig(), unit="*"
        )


class eSTRigDisonnector:
    """fbxの骨アニメーションをeSTのリグアニメーションにコンバート。
    現在shenronの仕様に決め打ち"""

    @classmethod
    def _get_joint_from_externalrig(cls, ctrl):
        ctrl_dist = cmds.listConnections(ctrl, d=True)
        for parent_const in ctrl_dist:
            obj_type = cmds.objectType(parent_const)
            if obj_type == "parentConstraint" or obj_type == "aimConstraint":
                for parent_const_dist in cmds.listConnections(parent_const, d=True):
                    if cmds.objectType(parent_const_dist) == "joint":
                        return parent_const_dist

    @classmethod
    def _get_external_ctrl(cls, ns):
        animatables = []
        anim_plugs = "{}:animPlugs".format(ns)
        for lp in eST3.mCmds.AnimPlugs(anim_plugs).listChildAnimPlugs(r=True):
            if lp.getAnimPlugsType() == "externalRig":
                animatables.extend(lp.listAnimatables(nodesOnly=True))
        return animatables

    @classmethod
    def exec_est_disconnect(cls, namespace: str):
        ns = namespace
        rig_tools = eSTRigTools(ns)
        external_ctrls = cls._get_external_ctrl(ns)

        ctrl_and_joint = {}
        for lp in external_ctrls:
            if lp == "Asset_ctrl":
                continue
            if cls._get_joint_from_externalrig(str(lp)) == None:
                continue
            ctrl_and_joint[str(lp)] = cls._get_joint_from_externalrig(str(lp))

        eST3.rCmds.DisconnectExternalRig(
            rig=eST3.mCmds.ExtendedRig(ns),
            units=rig_tools.get_nb_unitnodes(),
            animPlugs=rig_tools.get_anim_plugs(),
            bake=False,
            echo=True,
        )

        # disconnect est controller
        rig_tools.connect_controller(False)
