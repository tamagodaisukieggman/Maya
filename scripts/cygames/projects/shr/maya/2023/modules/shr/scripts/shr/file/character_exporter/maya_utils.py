# -*- coding: utf-8 -*-
import os
import re
import typing as tp
import maya.cmds as cmds
import maya.mel as mel



class MayaUtil:
    @classmethod
    def create_and_bind_temp_joint(cls, target_objects: list) -> None:
        """もしバインドされていなければ骨を作成し、バインド

        Args:
            target_objects (list): バインド対象のオブジェクトのリストを渡す
        """
        joint_name = "root_jnt"
        if not cmds.objExists(joint_name):
            root = cmds.createNode("joint", n=joint_name)

        for target_object in target_objects:
            if cls.check_if_already_bound(target_object) == False:
                cmds.skinCluster([joint_name, target_object], tsb=True)

    @classmethod
    def check_if_already_bound(cls, target_object: str) -> bool:
        """target_objectがバインド済みかどうかをboolで返す

        Args:
            target_object (str): メッシュのトランスフォーム

        Returns:
            bool: arget_objectがバインド済みかどうか
        """
        for lp in cmds.listHistory(target_object):
            if "skinCluster" in lp:

                return True
        return False

    @classmethod
    def copy_and_rebind(cls, src_obj: str, parent_grp="") -> str:
        """src_objをコピーしてバインドする

        Args:
            src_obj (str): コピー元となるオブジェクト名
            parent_grp (str, optional): 親グループ。指定されていればバインド後親子付け. Defaults to "".

        Returns:
            str: コピーした先のオブジェクト名
        """
        skincluster_node = mel.eval('findRelatedSkinCluster "{}"'.format(src_obj))
        if len(skincluster_node) == 0:
            return 0
        max_inf = cmds.skinCluster(skincluster_node, q=True, mi=True)
        connection_joint = cmds.listConnections(
            skincluster_node + ".matrix", type="joint"
        )
        duplicate_buff = ""
        if parent_grp != "":
            duplicate_buff = cmds.duplicate(src_obj, rr=True, p=parent_grp)[0]
        else:
            duplicate_buff = cmds.duplicate(src_obj, rr=True)[0]
        cmds.skinCluster(
            connection_joint,
            duplicate_buff,
            removeUnusedInfluence=False,
            tsb=True,
            mi=max_inf,
        )
        cmds.copySkinWeights(
            src_obj, duplicate_buff, nm=True, sa="closestPoint", ia=["oneToOne", "name"]
        )
        return duplicate_buff

    @classmethod
    def copy_skincluster(cls, src_obj, tgt_obj) -> None:
        """src_objのスキン情報をコピーしてtgt_objにバインドする

        Args:
            src_obj (str): コピー元となるオブジェクト名
            tgt_obj (str): バインド対象のオブジェクト
        """

        skincluster_node = mel.eval('findRelatedSkinCluster "{}"'.format(src_obj))
        if len(skincluster_node) == 0:
            return None
        max_inf = cmds.skinCluster(skincluster_node, q=True, mi=True)
        connection_joint = cmds.listConnections(
            skincluster_node + ".matrix", type="joint"
        )
        cmds.skinCluster(
            connection_joint, tgt_obj, removeUnusedInfluence=False, tsb=True, mi=max_inf
        )
        cmds.copySkinWeights(
            src_obj, tgt_obj, nm=True, sa="closestPoint", ia=["oneToOne", "name"]
        )

    @classmethod
    def get_short_name(cls, longName: str) -> str:
        """longNameからshortnameを取得する

        Args:
            longName (str): 変換対象のオブジェクトのロングネーム

        Returns:
            str: ショートネーム
        """
        if "|" in longName:
            sn = longName.rsplit("|")[-1]
        else:
            sn = longName
        return sn

    @classmethod
    def replace_group_to_transform(cls, grp: str):
        """
        groupをtransformに置き換える
        groupにはlodgroupが入る想定

        Args:
            grp (str): 置き換える対象のnode名
        """
        mesh_grp = grp
        new_grp = cmds.group(em=True, w=True, n="mesh")
        for lp in cmds.listRelatives(mesh_grp, c=True) or []:
            cmds.parent(lp, new_grp)

        parent = cmds.listRelatives(mesh_grp, p=True)[0]
        cmds.delete(mesh_grp)
        grp = cmds.parent(new_grp, parent)
        cmds.reorder(grp, front=True)

    @classmethod
    def create_lod_grp(cls, grp_name: str, parent_grp: str) -> str:
        """lod_groupの作成
        cameraとのコネクションを設定しないとshowの設定が反映されない

        Args:
            grp_name (str): 作成されるlod grpの名前
            parent_grp (str): 親となる階層

        Returns:
            str: lod group名
        """
        lod_grp = cmds.createNode("lodGroup", name="mesh", parent=parent_grp)
        camera = cmds.ls("perspShape", type="camera")[0]

        # cameraとのコネクションをしないとshowが効かない
        cmds.connectAttr(
            "{}.worldMatrix".format(camera), "{}.cameraMatrix".format(lod_grp)
        )
        cmds.connectAttr(
            "{}.focalLength".format(camera), "{}.focalLength".format(lod_grp)
        )
        return lod_grp

    @classmethod
    def replace_transform_to_lodgroup(cls, tf: str) -> None:
        """
        transformをlodグループに置き換える
        lodグループに置き換えるtransform

        Args:
            tf (str): 置き換える対象のtransform名
        """
        # リネームするためのショートネームを取得
        sn_mesh_grp = cls.get_short_name(tf)
        # 最終的な親階層の取得
        parent_grp = cmds.listRelatives(tf, p=True)[0]

        lods = cmds.listRelatives(tf, c=True, pa=True)
        # worldにペアレント
        w_lods = cmds.parent(lods, w=True)

        cmds.delete(tf)

        # 選択状態をクリア
        lod_grp = MayaUtil.create_lod_grp(sn_mesh_grp, parent_grp)
        # 元に戻す
        cmds.parent(w_lods, lod_grp)
        cmds.reorder(lod_grp, front=True)

    @classmethod
    def bake_animation(cls, joints):
        """アニメーションをベイク

        Args:
            joints (strings): アニメーションのベイクターゲットとなるジョイントの文字列の配列

        Returns:
            joints (strings): ベイクされたジョイント
        """
        # Get Character joints
        start = cmds.playbackOptions(q=True, minTime=True)
        end = cmds.playbackOptions(q=True, maxTime=True)
        # Bake Animation
        cmds.bakeResults(
            joints,
            simulation=True,
            t=(start, end),
            sampleBy=1,
            disableImplicitControl=True,
            preserveOutsideKeys=True,
            sparseAnimCurveBake=False,
            removeBakedAttributeFromLayer=False,
            bakeOnOverrideLayer=False,
            minimizeRotation=False,
            # shape=True
            # at=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
        )
        # Return Result
        return joints

    @classmethod
    def get_hierarchy_root_joint(cls, joint=""):
        """引数jointのrootに当たる骨の取得

        Args:
            joint (str, optional): joint名

        Returns:
            string: 親骨名
        """
        rootJoint = joint

        # 再帰処理
        while True:
            parent = cmds.listRelatives(rootJoint, parent=True, type="joint")
            if not parent:
                break
            rootJoint = parent[0]
        return rootJoint

    @staticmethod
    def delete_namespace(cls, root):
        """
        namespaceの削除
        """
        target_assets = cmds.listRelatives(root, ad=True) or []
        nss = []

        # 削除する必要のあるnamespaceを検索
        for lp in target_assets:
            ns = lp.split(":")[0]
            # namespaceがついている and 既にリストに入っていない
            if ":" in lp and ns not in nss:
                nss.append(ns)

        rtn = 0
        for ns in nss:
            cmds.namespace(mergeNamespaceWithRoot=True, removeNamespace=ns)
            try:
                cmds.namespace(mergeNamespaceWithRoot=True, removeNamespace=ns)
                print("Namespace deleted:", ns)
                rtn = 1
            except:
                pass
        return rtn

    @classmethod
    def recreate_bindpose(cls, joints: list) -> None:
        """現在のフレームでバインドポーズを作成

        Args:
            root_joint (list): rootのjoint名
        """
        # バインドポーズ全削除
        cmds.delete(cmds.ls(type="dagPose"))
        # バインドポーズの作成
        pose_name = cmds.dagPose(joints, bp=True, s=True, n="bindPose1")
        print("create bindpose : {}".format(pose_name))

    @classmethod
    def re_open_cdrive(cls) -> bool:
        """Cdriveで開きなおす

        Returns:
            bool: 開きなおしたかどうか
        """
        if "C:/cygames/shrdev/" not in cmds.file(q=True, sn=True):
            selected = cmds.ls(sl=True)
            current_path = cmds.file(q=True, sn=True)
            search = re.compile(".*(shr_art/.*)")
            path = re.search(search, current_path).group(1)
            cmds.file("C:/cygames/shrdev/" + path, o=True, f=True)
            cmds.select(selected, r=True)
            return True
        else:
            return False

    # @classmethod
    # def get_filepath_dialog(
    #     cls,
    # ) -> tp.List[str]:
    #     cmds.fileDialog2()

    class MH_Command:
        @classmethod
        def create_custom_attribute(cls, root: str):
            """custom attributeの作製

            Args:
                root (str): 作製する対象となるルートの骨を選択
            """
            expressions_node = cmds.ls("*:CTRL_expressions")[0]
            root_bone = root

            attr_list = cmds.listAttr(expressions_node, userDefined=True)
            sn_expressions_node = expressions_node.split(":")[-1]
            for attr in attr_list:
                alias_attr_name = sn_expressions_node + "_" + attr

                try:
                    cmds.addAttr(
                        root_bone,
                        longName=f"{alias_attr_name}",
                        attributeType="float",
                        keyable=True,
                    )
                except:
                    continue

                dst_attr = f"{expressions_node}.{attr}"
                src_attr = f"{root_bone}.{alias_attr_name}"
                cmds.connectAttr(dst_attr, src_attr)

            frm = cmds.ls("*:FRM_WMmultipliers")[0]
            frm_attr_list = cmds.listAttr(frm, userDefined=True)

            for attr in frm_attr_list:
                try:
                    cmds.addAttr(
                        root_bone, longName=f"{attr}", attributeType="float", keyable=True
                    )
                    dst_attr = f"{frm}.{attr}"
                    src_attr = f"{root_bone}.{attr}"
                except:
                    continue
                cmds.connectAttr(dst_attr, src_attr)
