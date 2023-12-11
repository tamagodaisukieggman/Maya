# -*- coding=utf-8 -*-
u"""
name: autocreate_rig/constant.py
data: 2021/10/18
ussage: priari 用 Rig 自動作成ツールの定数
version: 2.72
​
"""
from __future__ import print_function
try:
    # Maya 2022-
    from builtins import object
except:
    pass

from collections import OrderedDict
import os
import traceback
import re
from logging import getLogger
import maya.api.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm
from . import const
from .utils import Utils

logger = getLogger(__name__)


class Check(object):

    @classmethod
    def _is_maya_file(cls, file_path):
        u"""Mayaファイルか

        :param file_path: ファイルパス
        :return: bool
        """
        if file_path.endswith('.ma') or file_path.endswith('.mb'):
            return True
        else:
            return False

    @classmethod
    def scene(cls, grp, ex_sik=None):
        u"""
            Rigに必要なシーンに情報のチェック
            :param str grp :
            :return: bool check_flag :チェック結果 ＯＫなら True, ＮＧなら False
            :return: error_list : [(str, PyNode)]チェック結果ログ
        """
        ns = Utils.get_namespace(grp)
        error_log = "No Group: {}".format(grp)

        if not grp or not pm.objExists(grp):
            return False, error_log

        if ex_sik is None:
            ex_sik = []
        # TODO ex_dict
        # ex_sik = [k for k, v in ex_sik.items() if v["sik"]]

        logger.info("-" * 72)
        logger.info(" >>> start check_check under {}".format(grp))
        logger.info("-" * 72)
        check_flag = True
        error_list = []

        root = Utils.get_pynode(grp, ns + const.ROOTJOINTNAME)
        grp_joint = Utils.get_pynode(grp, ns + const.GROUPJOINTNAME)
        grp_mesh = Utils.get_pynode(grp, ns + const.GROUPMESHNAME)

        # v2.1~: 決め打ちのl_mantle,r_mantle,l_sleeve,r_sleeveをOptionalに変更により不要。
        # l_mantle = Utils.get_pynode(grp, ns + L_MANTLENAME)
        # r_mantle = Utils.get_pynode(grp, ns + R_MANTLENAME)
        # l_sleeve = Utils.get_pynode(grp, ns + L_SLEEVENAME)
        # r_sleeve = Utils.get_pynode(grp, ns + R_SLEEVENAME)

        for joint in Utils.get_pyjoints(root):
            label = Utils.get_label(joint.nodeName())
            if label == 'tail':
                p_joint = joint.getParent()
                label = Utils.get_label(p_joint.nodeName())
                if not (label == 'tail' or label == 'hip'):
                    msg = u'{} の階層が正しくありません。'.format(joint)
                    logger.error(msg)
                    error_list.append((msg, joint))
                    check_flag = False  # return check_flag

            # if label in const.SECONDARYJOINTNAME_LIST and joint.nodeName().startswith("EX_"):
            if label in const.SECONDARYJOINTNAME_LIST:
                # invalid secondary joint check
                j_name = joint.nodeName()
                pa_node = joint.getParent()
                pj_name = pa_node.nodeName()

                # print("label in const.SECONDARYJOINTNAME_LIST", label, j_name)
                # 01-99の末尾の場合
                if re.match(".*_[0-9][0-9]$", j_name) and re.match(".*_[0-9][0-9]$", pj_name):
                    num = int(j_name.split("_")[-1])
                    p_num = int(pj_name.split("_")[-1])
                    if num != 0 and num - 1 != p_num:
                        print((j_name, num, p_num))
                        msg = u"Secondaryジョイント名末尾が階層と違います。"
                        error_list.append((msg, j_name))
                        check_flag = False

                if re.match(".*_00$", j_name):
                    pass

        if not grp_mesh:
            msg = u'階層内に grp_mesh ノードが見つかりません。'
            logger.error(msg)
            error_list.append((msg, ""))
            check_flag = False

        if not grp_joint:
            msg = u'階層内に grp_joint ノードが見つかりません。'
            logger.error(msg)
            error_list.append((msg, ""))
            check_flag = False

        else:
            if grp_joint.getParent() != grp:
                msg = u'grp_joint ノードの階層が正しくありません。'
                logger.error(msg)
                error_list.append((msg, grp_joint))
                check_flag = False

        if not root:
            msg = u'階層内に root ジョイントが見つかりません。'
            error_list.append((msg, ""))
            check_flag = False

        else:
            joints = pm.listRelatives(root, c=True, ad=True, type='joint', f=True) or []
            ex_joints = [j for j in joints if j.nodeName().startswith("EX_")]
            ex_endjoints = [j for j in ex_joints if not j.getChildren()]
            ex_root_joints = []

            invalid_endjoints = [j for j in ex_endjoints if not re.match('^EX_.+_(End|twistarm)$', j.nodeName())]

            # invalid ex joint check
            for j in ex_joints:
                j_name = j.nodeName()
                j_children = j.getChildren(type="joint") if j.getChildren(type="joint") else []
                is_numbered = True if re.match(".*_[0-9][0-9]$", j_name) else False
                is_ex = True if re.match("^EX_", j_name) else False
                is_multichained = True if len(j_children) > 1 else False
                if is_multichained:
                    for child in j_children:
                        if child.nodeName() in ex_sik:
                            msg = u"EXジョイントでルートが共有されたSplineIK設定が存在します。"
                            error_list.append((msg, child))
                            check_flag = False

                pa_node = j.getParent()
                if pa_node and pa_node.type() == "joint":
                    pj_name = pa_node.nodeName()
                    pj_is_numbered = True if re.match(".*_[0-9][0-9]$", pj_name) else False
                    pj_is_ex = True if re.match("^EX_", pj_name) else False

                    # first ex joint or not
                    if not pj_name.startswith("EX_"):
                        if j_name.endswith("_00"):

                            ex_root_joints.append(j)
                        else:
                            if "_bust" not in j_name:
                                msg = u"EXルートジョイント名末尾が'_00'ではありません。"
                                error_list.append((msg, j))
                                check_flag = False
                            else:
                                print(u"*_bustジョイントは末尾00ルール除外")
                else:
                    msg = u"親がジョイントではありません。"
                    error_list.append((msg, j))
                    check_flag = False

            # second ex joint or not
            for j in ex_root_joints:
                j_name = j.nodeName()
                c_joints = pm.listRelatives(j, c=True, ad=True, type='joint', f=True) or []
                # it has only one child
                if len(c_joints) == 1:
                    c_joints = [j for j in c_joints if not j.nodeName().endswith("_End")]
                    for c_j in c_joints:
                        c_j_name = c_j.nodeName()
                        num = len(c_j.longName().split(j_name)[-1].split("|")) - 1

                        if c_j_name[-2:] != "{0:02d}".format(num):
                            # print("> c_j_name[-2:] != '{0:02d}'.format(num)",  c_j_name[-2:], "{0:02d}".format(num))
                            msg = u"EXジョイント末尾の数字が階層とあっていません。"
                            error_list.append((msg, c_j))
                            check_flag = False

                        if c_j_name[:-3] != j_name[:-3]:
                            msg = u"EXジョイントのベースネームがルートネームとあっていません。"
                            error_list.append((msg, c_j))
                            check_flag = False

                # it has children
                elif len(c_joints) > 1 and j_name in ex_sik:
                    is_valid = True
                    for cj in c_joints:
                        cj_path = cj.fullPath()
                        depth_list = cj_path.replace(j.fullPath(), j.nodeName()).split("|")
                        for num, name in enumerate(depth_list):
                            suffix = name.split("_")[-1]
                            if suffix != "End" and num != int(suffix):
                                is_valid = False
                                break

                    if not is_valid:
                        check_flag = False
                        msg = u"EXジョイントで一部が共有されたSplineIK設定が存在します。"
                        error_list.append((msg, j))

                elif len(c_joints) > 1 and j_name not in ex_sik:
                    pass
                # No children
                else:
                    msg = u"EXルート以下にEXジョイントが１つも存在しません"
                    error_list.append((msg, j))
                    check_flag = False

            root_parent_node = root.getParent()
            if grp_joint != root_parent_node:
                msg = u'root ジョイントの階層が正しくありません。'
                # logger.error(u"{}:　missing [grp_joint|root]".format(msg, root_parent_node))
                error_list.append((msg, root_parent_node))
                check_flag = False

            if pm.listConnections(root, d=True, type='dagPose') is None:
                logger.warning(u'root ジョイントに Bind Pose が見つかりません。')

            for joint in cls.double(Utils.get_pyjoints(grp)):
                msg = u'名前の重複しているジョイントが見つかりました。'
                error_list.append((msg, joint))
                check_flag = False

            for joint in invalid_endjoints:
                msg = u'末端ジョイントに "_End"文字列がありません。'
                error_list.append((msg, joint))
                check_flag = False

        pm.select(grp, hi=True)
        meshes = pm.ls(sl=True, type='mesh')

        for mesh in meshes:
            tr_name = mesh.getTransform().name() or ""

            if not tr_name.endswith("_Outline"):
                # skin = get_skincluster(mesh.longName())
                # meshTransformとmeshShapeの名前が一致しない場合にmel.findSkinclusterでskinを取得できない為、pymelに変更
                skin = mesh.listHistory(type="skinCluster")[0] if mesh.listHistory(type="skinCluster") else None
                pa_node = mesh.getTransform().getParent() or ""

                if pa_node != grp_mesh:
                    msg = u'grp_mesh 階層内に {} が見つかりません。'.format(mesh.nodeName())
                    logger.error(msg)
                    error_list.append(msg)
                    check_flag = False

                if skin:
                    skin = pm.PyNode(skin)
                    skin_joint = pm.skinCluster(skin, query=True, inf=True)
                    for joint in skin_joint:
                        if not Utils.get_pynode(root, joint.nodeName()):
                            msg = u'{} 階層内に {} が見つかりません。'.format(grp, joint)
                            logger.error(msg)
                            error_list.append(msg)
                            check_flag = False
                else:
                    msg = u'{} に SkinCluster が見つかりません。'.format(mesh)
                    logger.warning(msg)
                    # skin設定が無くても動作するように変更。
                    # error_list.append(msg)
                    # check_flag = False

        if not meshes:
            msg = u'階層内にメッシュデータが見つかりません。'
            logger.warn(msg)  # error_num += 1  # error_list.append(u'{}: {}'.format(error_num, msg))

        # Rigの階層別重複名に対応していない為、シーン内にRigグループが存在する際はエラーを返す
        rig_groups = pm.ls('grp_CTRL')
        if rig_groups:
            msg = u'グループ内にRigが既に作成されている場合、正常に作成できない可能性があります。'
            logger.warn(msg)
            error_list.append(msg, "")
            check_flag = False

        pm.select(grp)

        return check_flag, error_list

    @classmethod
    def delete(cls):
        sel = pm.selected()
        # TODO: 削除に必要なチェック記載予定
        if not sel:
            return False
        # Utils.get_pynodes(sel[0], type="transform")
        return True

    @classmethod
    def double(cls, grp=None, type="transform"):
        u"""
            grp以下の重複ノードのチェック、grp指定が無ければ全体の重複チェック　
            :param  grp :PyNode
            :param  type :str
            :return: double_list :重複ノードリスト
            :rtype: list of PyNode　or []
        """
        double_list = []

        if grp is None or not isinstance(grp, pm.PyNode):
            return double_list

        # joint_list = Utils.get_pyjoints(grp)
        pynode_list = Utils.get_pynodes(grp, type=type)

        for i, node in enumerate(pynode_list):
            for x, search_name in enumerate(pynode_list):
                if i != x:
                    if Utils.get_name(node) == Utils.get_name(search_name):
                        if not Utils.get_name(node) in double_list:
                            double_list.append(node)

        return double_list