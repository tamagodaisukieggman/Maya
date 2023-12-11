# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds
import os
import re
import typing as tp


# ==================================================
class BindSkinCmd(object):
    @classmethod
    def joint_color_set(cls):
        # 直下にあるかどうかのフラグ
        flag_below = False
        ls_joints = cmds.ls(type="joint")

        # ワイヤーフレームカラー一覧
        color_sets = [
            (0.631, 0.416, 0.188),
            (0.62, 0.631, 0.188),
            (0.408, 0.631, 0.188),
            (0.188, 0.631, 0.365),
            (0.188, 0.631, 0.631),
            (0.188, 0.404, 0.631),
            (0.435, 0.188, 0.631),
            (0.631, 0.188, 0.416),
        ]

        # 階層数を取得しソート
        dic_joint_relatives = {}
        for ls_joint in ls_joints:
            parentNode = cmds.listRelatives(ls_joint, f=True, p=True)
            if not parentNode:
                flag_below = True
                dic_joint_relatives[ls_joint] = 0
            else:
                count_relatives = parentNode[0].count("|")
                dic_joint_relatives[ls_joint] = count_relatives

        dic_joint_sort = sorted(dic_joint_relatives.items(), key=lambda x: x[1])

        # 階層数に合わせて色付け
        for dic_joint in dic_joint_sort:
            if flag_below:
                count = dic_joint[1]
            else:
                count = dic_joint[1] - 1

            if count > 7:
                count = count - 8

            # cmds.setAttr('{}.objectColor'.format(dic_joint[0]), count)
            # cmds.setAttr('{}.useObjectColor'.format(dic_joint[0]), True)
            cmds.color(dic_joint[0], rgb=color_sets[count])

    @classmethod
    def selection(cls):
        selection = cmds.ls(sl=True, l=True)
        joint_list = []
        tra_list = []

        for sel in selection:
            if cmds.nodeType(sel) == "joint":
                joint_list.extend(
                    cmds.listRelatives(
                        sel, allDescendents=True, fullPath=True, type="joint"
                    )
                )
            elif cmds.nodeType(sel) == "transform":
                tra_list.append(sel)

        return tra_list, joint_list

    @classmethod
    def wiz2_bind(cls, mesh, joint):
        cmds.skinCluster(
            mesh,
            joint,
            obeyMaxInfluences=True,
            bindMethod=0,
            maximumInfluences=4,
            removeUnusedInfluence=False,
            skinMethod=0,
            includeHiddenSelections=False,
            dropoffRate=4.0,
            normalizeWeights=True,
            weightDistribution=0,
        )

    @classmethod
    def check_skincluster(cls, sel_set):
        flg_cluster = False

        for tra in sel_set[0]:
            oHistory = cmds.listHistory(tra)

            for oHistoryList in oHistory:
                oName = cmds.objectType(oHistoryList)
                if oName == "skinCluster":
                    flg_cluster = True
                    break

            if flg_cluster == False:
                return False

        return flg_cluster

    @classmethod
    def weights_export(cls, sel_set):
        """
        Args:
            sel_set (str[]): classmethod selectionで選択されたtransformとjointのリスト
        Returns:
            str[]: [[メッシュ名][xml名][ジョイント名]]
        """
        xml_list = []

        for tra in sel_set[0]:
            oHistory = cmds.listHistory(tra)

            for oHistoryList in oHistory:
                oName = cmds.objectType(oHistoryList)
                if oName == "skinCluster":
                    shortName = cmds.ls(tra, sn=True)
                    xml_name = "temporary_weights_" + shortName[0] + ".xml"
                    influence_names = cmds.skinCluster(oHistoryList, q=True, inf=True)
                    xml_list.append([tra, xml_name, influence_names])
                    cmds.deformerWeights(
                        xml_name,
                        export=True,
                        deformer=oHistoryList,
                        format="XML",
                        vertexConnections=True,
                        path=os.path.dirname(__file__),
                    )

        return xml_list

    @classmethod
    def weights_import(cls, xml_list):
        for xml_data in xml_list:
            oHistory = cmds.listHistory(xml_data[0])

            for oHistoryList in oHistory:
                oName = cmds.objectType(oHistoryList)
                if oName == "skinCluster":
                    cmds.deformerWeights(
                        xml_data[1],
                        im=True,
                        deformer=oHistoryList,
                        method="bilinear",
                        ignoreName=True,
                        path=os.path.dirname(__file__),
                    )

            os.remove(os.path.join(os.path.dirname(__file__), xml_data[1]))

    @classmethod
    def gotoBindPose(cls, joints):
        """ジョイントをバインドポーズに戻す。
        （現状使っていない。リバインドの際Go to Bind Poseしないで欲しいという希望あり。）
        ヒエラルキー内にexpressionがある場合はバインドポーズに戻せないので削除して良いか
        ポップアップでユーザーに聞く。
        Args:
            joints (str): ジョイント名のリスト
        Returns:
            bool: バインドポーズに戻せたらTrueを返す
        """
        joints = cmds.ls(joints, exactType="joint")
        cmds.select(joints, hi=True)
        try:
            expressions = cmds.listConnections(t="expression")
        except Exception:
            pass
        if expressions:
            joints_w_exp = []
            for exp in expressions:
                cmds.select(exp)
                bone = cmds.listConnections(t="joint")
                if bone:
                    joints_w_exp.extend(bone)
            user_choice = cmds.confirmDialog(
                title="Confirm",
                message="ジョイントにエクスプレッションがありました\n\n"
                + "\n".join(joints_w_exp)
                + "\n\nバインドポーズに戻すにはエクスプレッションを削除する必要があります。"
                + "\n削除してもよろしいですか？",
                button=["OK", "Cancel"],
                defaultButton="OK",
                cancelButton="Cancel",
                dismissString="Cancel",
            )
            if user_choice == "Cancel":
                return False
            if user_choice == "OK":
                cmds.delete(expressions)
        cmds.select(joints, hi=True)
        try:
            cmds.dagPose(bindPose=True, restore=True)
        except Exception:
            return False
        return True

    @classmethod
    def renumber_skinclusters(cls):
        """
        スキンクラスターの連番が1からになるようにリネーム
        リバインドの際にskinClusterの連番が上がっていくのが気持ち悪い為（アーティストさん要望）
        """
        clusters = cmds.ls(type="skinCluster")
        max_trailing_num = re.match(".*?([0-9]+)$", clusters[-1]).group(1)
        max_trailing_num = int(max_trailing_num)
        for i, clst in enumerate(clusters):
            trailing_num = re.match(".*?([0-9]+)$", clst).group(1)
            clst_name = clst[0 : len(clst) - len(trailing_num)]
            cmds.rename(clst, "{0}{1}".format(clst_name, max_trailing_num + i + 1))
        clusters = cmds.ls(type="skinCluster")
        for i, clst in enumerate(clusters):
            trailing_num = re.match(".*?([0-9]+)$", clst).group(1)
            clst_name = clst[0 : len(clst) - len(trailing_num)]
            cmds.rename(clst, "{0}{1}".format(clst_name, i + 1))

    @classmethod
    def renumber_bindposes(cls):
        """
        バインドポーズの連番が1からになるようにリネーム
        リバインドの際にbindPoseの連番が上がっていくのが気持ち悪い為（アーティストさん要望）
        """
        dposes_in_scene = cmds.ls(type="dagPose")
        max_trailing_num = re.match(".*?([0-9]+)$", dposes_in_scene[-1]).group(1)
        max_trailing_num = int(max_trailing_num)
        for i, dpose in enumerate(dposes_in_scene):
            trailing_num = re.match(".*?([0-9]+)$", dpose).group(1)
            dag_name = dpose[0 : len(dpose) - len(trailing_num)]
            cmds.rename(dpose, "{0}{1}".format(dag_name, max_trailing_num + i + 1))
        dposes_in_scene = cmds.ls(type="dagPose")
        for i, dpose in enumerate(dposes_in_scene):
            trailing_num = re.match(".*?([0-9]+)$", dpose).group(1)
            dag_name = dpose[0 : len(dpose) - len(trailing_num)]
            cmds.rename(dpose, "{0}{1}".format(dag_name, (i + 1)))

    # ==================================================

    @classmethod
    def project_bind(cls):
        print("Project Bind Start")

        sel = cls.selection()

        if len(sel[0]) == 0 or len(sel[1]) == 0:
            cmds.confirmDialog(
                title="Project Bind",
                message="メッシュとボーンが検出されませんでした。\n選択して実行してください。",
                button="close",
            )

        else:
            if cls.check_skincluster(sel):
                cmds.confirmDialog(
                    title="Project Bind",
                    message="既にバインドされているため処理を停止します。",
                    button="close",
                )
            else:
                for mesh in sel[0]:
                    cls.wiz2_bind(mesh, sel[1])

                cls.joint_color_set()
                cmds.confirmDialog(
                    title="Project Bind", message="処理が正常に終了しました。", button="close"
                )

        print("Project Bind End")

    @classmethod
    def rebind(cls):
        """rebindの実行関数"""
        print("Rebind Start")

        selection = cmds.ls(sl=True)
        cls.rebind_targets(selection)

        print("Rebind End")

    @classmethod
    def rebind_targets(cls, target_objects: tp.List[str], is_result=True):
        """
        2023/04/03 以下仕様追加
        ・リバインドする際はスケルトンにバインドされているすべてのメッシュに対して
        現状のポーズのスケルトンにリバインドする
        ・その際、bindPoseの連番名が上がらないようにしておく
        https://cg415.slack.com/archives/C042MMV8A48/p1680257311495809?thread_ts=1675936306.103529&cid=C042MMV8A48
        """

        # 選択ベースになっているのでtargetを選択
        cmds.select(target_objects, r=True)

        root_nodes = find_root_nodes_from_selection()
        if len(root_nodes) == 0:
            cmds.confirmDialog(
                title="Rebind", message="リバインドしたいメッシュを選択して実行してください。", button="close"
            )
            return
        if len(root_nodes) > 1:
            cmds.confirmDialog(
                title="Rebind", message="複数のキャラクターには対応していません。", button="close"
            )
            return
        root_node = root_nodes[0]
        root_joint = find_root_joint(root_node)
        meshes = get_bound_meshes_from_joint(root_joint)
        if len(meshes) == 0:
            cmds.confirmDialog(
                title="Rebind",
                message="選択にメッシュが検出されませんでした。\n選択して実行してください。",
                button="close",
            )
        else:
            if cls.check_skincluster((meshes, [])):
                xml_list = cls.weights_export((meshes, []))
                # delete history
                cmds.delete(meshes, constructionHistory=True)

                for xml_data in xml_list:
                    cls.wiz2_bind(xml_data[0], xml_data[2])

                cls.weights_import(xml_list)
                cls.joint_color_set()
                cls.renumber_skinclusters()
                # bindPose 名の番号がインクリメントされないように
                cls.renumber_bindposes()
                is_success = True
            else:
                is_success = False

            if is_result:
                if is_success:
                    cmds.confirmDialog(
                        title="Rebind", message="処理が正常に終了しました。", button="close"
                    )
                else:
                    cmds.confirmDialog(
                        title="Rebind",
                        message="選択にスキンクラスターが検出できませんでした。\n" "バインド済みメッシュを選択肢て実行してください。",
                        button="close",
                    )


def find_root_joint(root_node):
    group_members = cmds.listRelatives(root_node, ad=True)
    joints = [
        cmds.listRelatives(i, p=True)[0] for i in cmds.ls(group_members, type="joint")
    ]
    for jnt in joints:
        parents = cmds.listRelatives(jnt, p=True)
        parentobj = None
        if parents:
            parentobj = parents[0]
            if cmds.objectType(parentobj) != "joint":
                return jnt


def find_parent(obj):
    parents = cmds.listRelatives(obj, p=True)
    if not parents:
        return obj
    else:
        for p in parents:
            return find_parent(p)


def find_root_nodes_from_selection():
    found_parents = []
    selection = cmds.ls(sl=True)
    if not selection:
        return None
    parents = cmds.listRelatives(selection, p=True)
    # 選択しているもの全てが親だったら
    if not parents:
        return selection
    # 選択ごとにrootを見つける
    for sel in selection:
        parents = cmds.listRelatives(sel, p=True)
        if not parents:
            found_parents.append(sel)
        else:
            group_members = cmds.listRelatives(sel, ad=True)
            for mem in group_members:
                parents = cmds.listRelatives(mem, p=True)
            if not parents:
                found_parents.append(mem)
            else:
                found_parents.append(find_parent(mem))
    return list(set(found_parents))


def get_bound_meshes_from_joint(jnt):
    clusters = cmds.listConnections(jnt, type="skinCluster")
    clusters = list(set(clusters))
    mesh_list = []
    for clust in clusters:
        meshes = cmds.listConnections(clust, type="mesh")
        mesh_list.extend(meshes)
    mesh_list = list(set(mesh_list))
    return mesh_list
