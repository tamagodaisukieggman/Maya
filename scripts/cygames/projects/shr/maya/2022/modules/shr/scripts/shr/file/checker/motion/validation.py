# -*- coding: utf-8 -*
u"""Checker (モーション)

Jenkinsでのみ実行 (今のところ)
"""
import os
import sqlite3
import codecs
import json
import traceback
from datetime import datetime

import maya.cmds as cmds

from mtku.maya.constant import MTK_TECH_SERVER_PATH
# from mtku.maya.mtklog import MtkLog
# from mtku.maya.utils.bat import MtkBat
from mtku.maya.utils.perforce import MtkP4
from mtku.maya.utils.decoration import timer
from mtku.maya.utils.node import MtkNode

from mtk.utils import getCurrentSceneName

# logger = MtkLog(__name__)


class MotionValidation(object):
    u"""Validation (モーション)

    * Jenkinsで自動で実行
    """
    latest_result = u'{}/var/maya/log/checker/motion/latest'.format(MTK_TECH_SERVER_PATH)
    log_root = u'{}//var/maya/log/checker/motion/{}'.format(MTK_TECH_SERVER_PATH, datetime.now().strftime("%Y%m%d"))

    @classmethod
    def exists_reference(cls):
        u"""リファレンスが存在するか"""
        count = cmds.file(q=True, r=True)
        if count:
            return True
        else:
            return False

    @classmethod
    def no_keyframe_of_root_joints(cls):
        u"""ルートジョイントにキーフレームがないか"""
        joints = cmds.ls(typ='joint')
        root_joints = MtkNode.get_binding_root_joints(joints)
        for root_joint in root_joints:
            if cmds.keyframe(root_joint, q=True, iv=True):
                return False
        return True

    @classmethod
    def no_keyframe_of_move_ctrl(cls):
        u"""moveCtrlにキーフレームがないか"""
        filename, _ = os.path.splitext(getCurrentSceneName())
        prefix = filename.split('_')[0]

        logger.debug(u'prefix: {}'.format(prefix))

        move_ctrl = u'{}_999_rig:moveCtrl'.format(prefix)
        if cmds.ls(move_ctrl):
            if cmds.keyframe(move_ctrl, q=True, iv=True):
                return False
            else:
                return True
        else:
            return False

    @classmethod
    def corrects_namespace(cls):
        u"""namespaceが正しいか"""
        os.path.basename()
        filename, _ = os.path.splitext(getCurrentSceneName())
        prefix = filename.split('_')[0]

        logger.debug(u'prefix: {}'.format(prefix))

        reference_file_paths = cmds.file(q=True, r=True)
        for file_path in reference_file_paths:
            ref_node = cmds.file(file_path, q=True, rfn=True)
            namespace = cmds.referenceQuery(ref_node, ns=True, shn=True)
            if namespace.find(prefix) != -1:
                logger.debug(u'prefix: {}, namespace: {}'.format(prefix, namespace))
                if namespace != u'{}_999_rig'.format(prefix):
                    return False

        return True

    @classmethod
    def check(cls, maya_file_path):
        u"""チェック

        :param maya_file_path: Mayaファイルのパス
        :return:
        """
        detail = {}
        logger.info(u'チェック開始: {}\n'.format(maya_file_path))

        # ファイルオープン
        if not MtkBat.open_file(maya_file_path):
            detail['open'] = False
            return False, detail

        # データチェック
        # --------------------------------------------
        # リファレンスのチェック
        try:
            if not cls.exists_reference():
                detail['reference'] = False
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            detail['reference'] = 'CheckError'
        # ルートジョイントにキーフレームがある
        try:
            if not cls.no_keyframe_of_root_joints():
                detail['have_keyframe_of_root_joints'] = False
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            detail['have_keyframe_of_root_joints'] = 'CheckError'
        # moveCtrlにキーフレームがある
        # try:
        #     if not cls.no_keyframe_of_move_ctrl():
        #         detail['have_keyframe_of_move_ctrl'] = False
        # except Exception as e:
        #     logger.error(e)
        #     detail['have_keyframe_of_move_ctrl'] = 'CheckError'
        # namespaceのチェック
        try:
            if not cls.corrects_namespace():
                detail['namespace'] = False
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            detail['namespace'] = 'CheckError'
        # --------------------------------------------
        logger.info(u'チェック終了: {}\n'.format(maya_file_path))

        if detail:
            print('{}:{}:{}\n'.format('CHECKER', maya_file_path, 'E'))
            return False, detail
        else:
            return True, {}

    @classmethod
    def _get_rev_from_db(cls):
        u"""DBからリビジョンを取得

        :return: ｛maya_file_path: rev}
        """
        db_revision = {}

        # DBからリビジョンを取得
        if os.path.exists(MtkBat.db_path):
            try:
                con = sqlite3.connect(MtkBat.db_path)
                c = con.cursor()
                command = 'SELECT * FROM revision;'
                for row in c.execute(command):
                    maya_file_path, rev = row
                    db_revision[maya_file_path] = rev
                con.close()
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())

        return db_revision

    @classmethod
    @timer
    def main(cls, root_path, checks_only_differences=True):
        u"""main"""
        counter = 0
        open_error = []
        results = []

        if checks_only_differences:
            logger.info(u'モード: 差分のみチェック')
        else:
            logger.info(u'モード: 全チェック')

        # DBからリビジョンを取得
        db_revision = cls._get_rev_from_db()

        # DBが存在し、かつ差分のみチェックする場合
        if db_revision and checks_only_differences:
            stats = MtkP4.fstat(MtkBat.get_maya_file_path(root_path))
            for stat in stats:
                maya_file_path = stat['clientFile']
                rev = stat['headRev']
                # リビジョン比較
                if maya_file_path not in db_revision:
                    continue
                if rev <= db_revision[maya_file_path]:
                    continue
                # チェック
                result, detail = cls.check(maya_file_path)
                if not result:
                    print('{}:{}:{}'.format('CHECKER', maya_file_path, 'E'))
                    if 'open' in detail:
                        open_error.append(maya_file_path)
                    results.append((maya_file_path, detail))
                counter += 1

        # DBが存在しない、または全チェック時
        else:
            for maya_file_path in MtkBat.get_maya_file_path(root_path):
                # チェック
                result, detail = cls.check(maya_file_path)
                if not result:
                    print('{}:{}:{}'.format('CHECKER', maya_file_path, 'E'))
                    if 'open' in detail:
                        open_error.append(maya_file_path)
                    results.append((maya_file_path, detail))
                counter += 1

        latest_summary = {
            'result': False if results else True,
            'total': counter,
            'open_error': len(open_error),
            'error': len(results),
        }

        logger.info('')
        logger.info(('{0:=<79}'.format('')))
        logger.info(u'チェック総数: {}'.format(latest_summary['total']))
        logger.info(u'ファイルオープンエラー数: {}'.format(latest_summary['open_error']))
        logger.info(u'エラー数: {}'.format(latest_summary['error']))

        # 仮処理
        if results:
            if not os.path.exists(cls.log_root):
                os.makedirs(cls.log_root)
            result_csv = '{}/result.csv'.format(cls.log_root)
            with codecs.open(result_csv, 'w', 'utf-8') as f:
                for result in results:
                    logger.info(result)
                    f.write(u'{},{}\r\n'.format(result[0], result[1]))

        with codecs.open(cls.latest_result, 'w', 'utf8') as f:
            json.dump(latest_summary, f, indent=4)
