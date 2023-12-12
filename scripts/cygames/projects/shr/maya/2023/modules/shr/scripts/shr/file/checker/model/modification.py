# -*- coding: utf-8 -*-
u"""修正 (共通)"""

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

# from mtku.maya.mtklog import MtkLog
from mtku.maya.utils.node import MtkNode
from mtku.maya.utils.history import MtkHistory


# logger = MtkLog(__name__)


class Modification(object):

    @classmethod
    def modify_nface(cls, *args, **kwargs):
        u"""5角形以上のポリゴンを修正(3角形化)し Non-Deformer History を適用します

         :param args:
         :param kwargs: 'node' エラーノード
         :return: bool (成功したらTrue)

         """
        root_node = kwargs.setdefault('nodes', None)
        pm.select(root_node)
        mel.eval(
            'polyCleanupArgList 3 '
            '{ "0","1","1","0","1","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-1","0" };'
        )

        return

    @classmethod
    def modify_lamina_faces(cls, *args, **kwargs):
        u"""2重ポリゴンを修正

        :param args:
        :param kwargs: 'node' エラーノード

        """
        root_node = kwargs.setdefault('node', None)
        cmds.select(root_node)
        mel.eval('polyCleanupArgList 3 {"0", "1", "1", "0", "0", "0", "0", "0", "0", "1e-005",'
                 ' "0", "1e-005", "0", "1e-005", "0", "-1", "1"};')

    @classmethod
    def modify_unused_nodes(cls, *args, **kwargs):
        u"""不要なノード、マテリアルなどの修正

        :param args:
        :param kwargs: 'node' エラーノード

        """
        cmds.select(all=True)
        mel.eval('MLdeleteUnused;')

    @classmethod
    def modify_unused_history(cls, *args, **kwargs):
        u"""不要なヒストリーの修正

        :param args:
        :param kwargs: 'node' エラーノード

        """
        root_node = kwargs.setdefault('node', None)
        cmds.select(root_node)
        MtkHistory.delete_history()

    @classmethod
    def _reset_joint(cls, joint):
        u"""ジョイントの値をリセット

        :param joint: ジョイント名
        """
        pairs = (
            ('tx', 'txInitVal'), ('ty', 'tyInitVal'), ('tz', 'tzInitVal'),
            ('rx', 'rxInitVal'), ('ry', 'ryInitVal'), ('rz', 'rzInitVal'),
            ('sx', 'sxInitVal'), ('sy', 'syInitVal'), ('sz', 'szInitVal'),
            ('jox', 'jxInitVal'), ('joy', 'jyInitVal'), ('joz', 'jzInitVal'),
        )

        for attr, init_attr in pairs:
            if not cmds.attributeQuery(init_attr, ex=True, node=joint):
                continue
            if not cmds.getAttr('{node}.{attr}'.format(node=joint, attr=attr), se=True):
                continue

            value = cmds.getAttr('{node}.{attr}'.format(node=joint, attr=init_attr))
            cmds.setAttr('{node}.{attr}'.format(node=joint, attr=attr), value)

    @classmethod
    def modify_bind_pose(cls, *args, **kwargs):
        u"""バインドポーズが一つになるように修正する

        :param args:
        :param kwargs: 'node' エラーノード
        :return: bool (成功したらTrue)

        :example:
        >>> data_root = 'Z:/mtk_test/tools/maya/2017/modules/mtku/scripts/file/checker/chara/validation'
        >>> maya_scene = '{}/a_bind_pose.ma'.format(data_root)
        >>> cmds.file(maya_scene, f=True, o=True)
        u'Z:/mtk_test/tools/maya/2017/modules/mtku/scripts/file/checker/chara/validation/a_bind_pose.ma'
        >>> CharaModification.modify_bind_pose(node='false_joint')
        True
        """
        root_joint = kwargs.setdefault('node', None)
        if not root_joint:
            return

        dag_poses = cmds.listConnections(root_joint, t='dagPose')
        if not dag_poses:
            return

        # jointを初期位置にリセット
        joints = MtkNode.get_joints(root_joint)
        [cls._reset_joint(joint) for joint in joints]

        # 既存のBindPoseを削除
        cmds.delete(dag_poses)
        # BindPoseの再生成
        joints = cmds.ls(root_joint, dag=True, l=True)
        cmds.dagPose(joints, bp=True, s=True, sl=True)

        return True

    @classmethod
    def modify_many_bind(cls, *args, **kwargs):
        u"""1頂点に5ボーン以上のジョイントがバインドされているのを修正する

        :param args:
        :param kwargs: 'node' エラーノード
        """
        import mtku.modify.checkweights.command as checkweights
        this_vtx = kwargs.setdefault('node', None)

        if ".vtx" not in this_vtx:
            return
        this_shape = cmds.listRelatives(this_vtx, p=True)[0]

        skin_cluster = mel.eval('findRelatedSkinCluster ' + this_shape)
        joint_list = cmds.skinCluster(skin_cluster, q=True, wi=True)
        influences_list = checkweights.get_influences_list(this_vtx, joint_list, skin_cluster)

        checkweights.set_vtx_weights(this_vtx, influences_list, skin_cluster)
