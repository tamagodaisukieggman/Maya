# -*- coding: utf-8 -*-
u"""mtk用 FBX Export

..
    END__CYGAMES_DESCRIPTION
"""
import os

import maya.cmds as cmds
import maya.mel as mel

import mtku.maya.utils.plugin as plugin
from mtku.maya.utils.node import MtkNode
from mtku.maya.log import MtkDBLog
from mtku.maya.utils.perforce import MtkP4


logger = MtkDBLog(__name__)

plugin.load('fbxmaya.mll')


class MtkFbx(object):

    prj_flag = os.getenv('WORLD_TOOL')  # 1 world, それ以外 mutsunokami

    if str(prj_flag) == '1':
        prefix_skeletal_mesh = ''
        prefix_static_mesh = ''
        prefix_texture = ''
    else:
        prefix_skeletal_mesh = 'skm_'
        prefix_static_mesh = 'stm_'
        prefix_texture = 'tex_'

    # ----------------------------------------
    #  FBX option
    # ----------------------------------------
    @classmethod
    def _set_options(cls, command_string):
        u"""FBXのオプションの設定

        :param command_string: melコマンドの文字列
        """
        logger.debug(command_string)
        mel.eval(command_string)

    @classmethod
    def _common_export_options(cls):
        u"""出力オプション"""
        cls._set_options('FBXExportFileVersion -v FBX201400;')

    @classmethod
    def _set_mesh_export_options(cls):
        u"""メッシュの出力オプション

        スケルタルメッシュ、スタティックメッシュ共通
        """
        cls._common_export_options()

        cls._set_options('FBXExportSmoothingGroups -v true')  # Smooting Groups
        cls._set_options('FBXExportTangents -v true')  # Tangents and Binormals
        cls._set_options('FBXExportSmoothMesh -v true')  # Smooth Mesh
        # cls._set_options('FBXExportTriangulate -v true')  # Triangulate
        cls._set_options('FBXExportTriangulate -v false')  # Triangulate

    @classmethod
    def set_skeletal_mesh_export_options(cls):
        u"""スケルタルメッシュの出力オプションを設定"""
        cls._set_mesh_export_options()

    @classmethod
    def set_static_mesh_export_options(cls):
        u"""スタティックメッシュの出力オプションを設定"""
        cls._set_mesh_export_options()

    @classmethod
    def set_motion_export_options(cls):
        u"""モーションの出力オプションを設定"""
        cls._common_export_options()

        # MayaでBakeするのでFBXのオプションでBakeはしないようにする
        cls._set_options('FBXExportBakeComplexAnimation -v false')

    # ----------------------------------------
    #  UE4とFBXの都合で必要な処理
    # ----------------------------------------
    @classmethod
    def _get_order(cls, node):
        u"""階層構造で何番目か取得

        :param node: ノード
        :return: 順序
        """
        order = 0
        target_node = cmds.ls(node, long=True)[0]
        parent = cmds.ls(cmds.pickWalk(target_node, d='up', typ='nodes'), long=True)[0]
        if target_node == parent:
            return -1

        pick_node = cmds.ls(cmds.pickWalk(parent, d='down', typ='nodes'), long=True)[0]

        while pick_node != target_node:
            pick_node = cmds.ls(cmds.pickWalk(pick_node, d='right', typ='nodes'), long=True)[0]
            order += 1
            if order > 1000:
                logger.error('_get_order: ERROR')
                return

        return order

    @classmethod
    def _set_order(cls, node, order):
        u"""階層構造の位置を指定した位置に移動

        :param node: ノード
        :param order: 順序
        """
        cmds.reorder(node, f=True)
        cmds.reorder(node, r=order)

    # ----------------------------------------
    #  Export
    # ----------------------------------------
    @classmethod
    def export(cls, nodes, fbx_path, fmt='Binary', verbose=False):
        u"""基本出力

        :param nodes: 出力ノードのリスト
        :param fbx_path: fbx_pathのパス
        :param fmt: "Binary" or "ASCII"
        :param verbose: 詳細を表示するか
        :return: bool
        """
        cls._set_options('FBXProperty Export|AdvOptGrp|Fbx|AsciiFbx -v "{}";'.format(fmt))

        # 出力先のディレクトリの生成
        if not os.path.exists(os.path.dirname(fbx_path)):
            os.makedirs(os.path.dirname(fbx_path))

        # 出力オプションの確認
        if verbose:
            logger.info('{}'.format(mel.eval('FBXProperties;')))

        try:
            cmds.select(nodes)
            command = 'FBXExport -f "{filename}" -s'.format(filename=fbx_path)
            logger.debug(command)
            mel.eval(command)
            logger.info(u'EXPORT: {}'.format(fbx_path))
            return True

        except Exception:
            # logger.error(e)
            logger.error(u'FBXの出力エラー: {}'.format(fbx_path))
            return False

    @classmethod
    def _checkout_and_export(cls, nodes, fbx_path, fmt='Binary', verbose=False):
        u"""チェックアウトしてFBXを出力

        :param nodes: 出力ノードのリスト
        :param fbx_path: fbx_pathのパス
        :param fmt: "Binary" or "ASCII"
        :param verbose: 詳細を表示するか
        :return: bool
        """
        try:
            # チェックアウト
            if os.path.exists(fbx_path):
                MtkP4.edit(fbx_path)

            # FBXの出力
            cls.export(nodes, fbx_path, fmt, verbose)

            # 新規作成の場合はchangelistに追加
            MtkP4.add(fbx_path)
            return True

        except Exception:
            # logger.error(e)
            logger.error(u'FBXの出力エラー: {}'.format(fbx_path))
            logger.error(u'出力失敗: チェックアウトされているか確認してください')
            return False

    @classmethod
    def _convert_fbx_path(cls, root_node, dir_path, is_skeletal):
        u"""ルートノードからFBXファイルのパスの取得

        ルートノードがスケルタルメッシュかどうか判定して、prefixを決める

        :param dir_path: 出力先のディレクトリのパス
        :param root_node: ルートノード
        :param is_skeletal: スケルタルメッシュかどうか
        :return: FBXファイルのパス
        """
        filename = root_node.split('|')[-1]
        if is_skeletal:
            fbx_path = '{}/{}{}.fbx'.format(dir_path, cls.prefix_skeletal_mesh, filename)
        else:
            fbx_path = '{}/{}{}.fbx'.format(dir_path, cls.prefix_static_mesh, filename)
        return fbx_path

    @classmethod
    def _convert_texture_path(cls, texture_path, dir_path):
        u"""UE4用にテクスチャパスを変更

        :param texture_path: 元のテクスチャのパス
        :param dir_path: 出力先のディレクトリのパス
        :return: テクスチャのパス
        """
        basename = '{}{}'.format(cls.prefix_texture, os.path.basename(texture_path))
        ue4_texture_path = '{}/{}'.format(dir_path, basename)
        return ue4_texture_path

    @classmethod
    def _dummy_command(cls, root_node):
        u"""Maya2015のTriangulateのバグ回避のためのダミーコマンド"""
        logger.debug('Exec DummyCommand')
        cmds.polyMoveVertex(root_node, ch=False)

    @classmethod
    def export_mesh(cls, dir_path, can_checkout, root_node, fmt='Binary', verbose=False):
        u"""モデルのFBXを出力

        * FBX出力時に階層構造を変更して, root_node, root_jointをワールドにペアレント
        * UE4用にテクスチャパスを変更

        :param dir_path: 出力先のディレクトリのパス
        :param can_checkout: FBXをチェックアウトするか
        :param root_node: ルートノード
        :param fmt: "Binary" or "ASCII"
        :param verbose: 詳細を表示するか
        :return: bool
        """
        logger.debug('Project Flag: {}'.format(cls.prj_flag))

        root_joint = None
        root_joints = MtkNode.get_binding_root_joints(root_node)

        if len(root_joints) == 1:
            # logger.warning(u'ルートジョイントの探索が失敗したので処理を中止しました')
            root_joint = root_joints[0]
        elif len(root_joints) > 1:
            logger.warning(u'ルートジョイントの探索が失敗したので処理を中止しました')
            logger.debug(root_joints)
            return

        logger.debug(u'ルートジョイント: {}'.format(root_joint))
        if root_joint:
            logger.debug(u'モード: Skeletal Mesh')
            is_skeletal = True
        else:
            logger.debug(u'モード: Static Mesh')
            is_skeletal = False
        fbx_path = cls._convert_fbx_path(root_node, dir_path, is_skeletal)

        # UE4用にテクスチャパスを変更
        filenodes = MtkNode.get_filenodes(root_node)
        texture_paths = [cmds.getAttr('{}.ftn'.format(filenode)) for filenode in filenodes]

        for filenode, texture_path in zip(filenodes, texture_paths):
            ue4_texture_path = cls._convert_texture_path(texture_path, dir_path)
            cmds.setAttr('{}.fileTextureName'.format(filenode), ue4_texture_path, typ='string')

        if str(cls.prj_flag) == '1':
            logger.info('wolrd_tool')
            # FBXの出力設定
            if is_skeletal:
                cls.set_skeletal_mesh_export_options()
            else:
                cls.set_static_mesh_export_options()
            # FBX出力
            if can_checkout:
                result = cls._checkout_and_export([root_node, root_joint], fbx_path, fmt, verbose)
            else:
                result = cls.export([root_node, root_joint], fbx_path, fmt, verbose)
        else:
            logger.info('mutunokami_tool')
            # 階層構造を変更
            parent_of_node = cmds.listRelatives(root_node, p=True, f=True)
            parent_of_joint = cmds.listRelatives(root_joint, p=True, f=True)
            order = cls._get_order(root_node)

            # ルートノード、ルートジョイントをワールドにペアレント
            root_node_ = cmds.parent(root_node, w=True)[0] if parent_of_node else root_node
            root_joint_ = cmds.parent(root_joint, w=True)[0] if parent_of_joint else root_joint

            # FBXの出力設定
            if is_skeletal:
                cls.set_skeletal_mesh_export_options()
            else:
                cls.set_static_mesh_export_options()
            # Maya2015のTriangulateのバグ回避のためのダミーコマンドを実行
            if not is_skeletal:
                cls._dummy_command(root_node)
            # FBX出力
            if can_checkout:
                result = cls._checkout_and_export([root_node_, root_joint_], fbx_path, fmt, verbose)
            else:
                result = cls.export([root_node_, root_joint_], fbx_path, fmt, verbose)
            cmds.parent(root_node_, parent_of_node[0]) if parent_of_node else None
            cmds.parent(root_joint_, parent_of_joint[0]) if parent_of_joint else None
            if order != -1:
                cls._set_order(root_node, order)

        # テクスチャパスを戻す
        for filenode, texture_path in zip(filenodes, texture_paths):
            cmds.setAttr('{}.fileTextureName'.format(filenode), texture_path, typ='string')

        return result

    @classmethod
    def export_motion(cls, fbx_path, can_checkout, joint, fmt='Binary', verbose=False):
        u"""モーションを出力 (UE4用)

        :param fbx_path: fbx_pathのパス
        :param can_checkout: FBXをチェックアウトするか
        :param joint: ルートジョイント
        :param fmt: "Binary" or "ASCII"
        :param verbose: 詳細を表示するか
        :return: bool
        """
        cls.set_motion_export_options()
        if can_checkout:
            return cls._checkout_and_export([joint], fbx_path, fmt, verbose)
        else:
            return cls.export([joint], fbx_path, fmt, verbose)
