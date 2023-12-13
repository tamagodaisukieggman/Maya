# -*- coding: utf-8 -*-
u"""FBX Exporter (Command)

.. END__CYGAMES_DESCRIPTION
"""
import os
import traceback

import maya.cmds as cmds

# Maya2022対応: MtkDBLog無効化
import logging
# from mtku.maya.log import MtkDBLog
from mtk.utils.perforce import MtkP4
from .fbx import MtkFbx
from mtk.utils import getCurrentSceneFilePath


# logger = MtkDBLog(__name__)
logger = logging.getLogger(__name__)


class BaseExportCmd(object):

    @classmethod
    def pre_export(cls, *args, **kwargs):
        u"""出力時の前処理"""
        dryrun = kwargs.setdefault('dryrun', False)
        can_checkout_ma = kwargs.setdefault('can_checkout_ma', False)
        if dryrun:
            return True

        # Mayaシーンのチェックアウト
        if can_checkout_ma:
            cls.checkout_current_scene()

        return True

    @classmethod
    def post_export(cls, *args, **kwargs):
        u"""出力時の後処理"""
        return True

    @classmethod
    def export(cls, *args, **kwargs):
        u"""出力"""
        return True

    @classmethod
    def exec_(cls, *args, **kwargs):
        u"""Export実行コマンド"""
        dryrun = kwargs.setdefault('dryrun', False)
        if dryrun:
            logger.warning(u'Dry Runで実行')
            if args:
                logger.info(u'\n可変引数')
                logger.info(u'{:-<79}'.format(''))
                for i, arg in enumerate(args):
                    logger.info(u'{}: {}'.format(i, arg))
                logger.info(u'{:-<79}'.format(''))
            if kwargs:
                logger.info(u'\nキーワード引数')
                logger.info(u'{:-<79}'.format(''))
                for k, v in kwargs.items():
                    logger.info(u'{}: {}'.format(k, v))
                logger.info(u'{:-<79}'.format(''))
            return False
        try:
            logger.info('Pre-Export')
            cls.pre_export(*args, **kwargs)  # 前処理
            logger.info('Export')
            cls.export(*args, **kwargs)   # Export
            logger.info('Post-Export')
            cls.post_export(*args, **kwargs)  # 後処理

            if not dryrun:
                logger.info(u'出力しました')
            return True

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return False

    # ########################################
    #  UE4 or Cyllista Command
    # ########################################
    @classmethod
    def export_mesh(cls, output_dir, can_checkout, root_node, fmt='Binary'):
        u"""モデルの出力

        * キャラ、モデル出力用のコマンド
        * UE4からCyllistaに移行する際はここの中身を入れ替える

        :param output_dir: 出力先のディレクトリのパス
        :param can_checkout: FBXをチェックアウトするか
        :param root_node: ルートノード
        :param fmt: "Binary" or "ASCII"
        """
        MtkFbx.export_mesh(output_dir, can_checkout, root_node, fmt)

    @classmethod
    def export_motion(cls, fbx_path, can_checkout, joint, fmt='Binary'):
        u"""モーションの出力

        * モーション出力用のコマンド
        * UE4からCyllistaに移行する際はここの中身を入れ替える

        :param fbx_path: fbx_pathのパス
        :param can_checkout: FBXをチェックアウトするか
        :param joint: ルートジョイント
        :param fmt: "Binary" or "ASCII"
        """
        MtkFbx.export_motion(fbx_path, can_checkout, joint, fmt)

    # ########################################
    #  Perforce
    # ########################################
    @classmethod
    def checkout_current_scene(cls):
        u"""現在のMayaシーンをチェックアウト

        :return: bool (成功した場合はTrue)
        """
        maya_scene_path = getCurrentSceneFilePath()
        if not maya_scene_path:
            return False
        return MtkP4.edit(maya_scene_path)

    # ########################################
    #  Utility
    # ########################################
    @classmethod
    def create_dir(cls, output_path):
        u"""ディレクトリ生成

        :param output_path: 生成するディレクトリのパス
        """
        if not os.path.exists(output_path):
            os.makedirs(output_path)
