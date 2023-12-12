# -*- coding: utf-8 -*-
u"""perforce

..
    END__CYGAMES_DESCRIPTION

"""
import re
import os
import types
from collections import OrderedDict
import importlib

import P4
importlib.reload(P4)

from P4 import P4

from P4 import P4Exception
from functools import wraps

# from mtku.maya.log import MtkDBLog
#
#
# logger = MtkDBLog(__name__)

from logging import getLogger
logger = getLogger(__name__)

p4 = P4()


def p4wrapper(func):
    u"""p4コマンドのdecorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        u"""wrapper

        :param args: args[0] function, args[1] ファイルパスまたはファイルパスのリスト
        :param kwargs:
        :return:
        """
        result = None
        try:
            p4.exception_level = 1
            p4.charset = 'utf8'
            p4.connect()

            result = func(*args, **kwargs)

        except P4Exception:
            for e in p4.errors:
                logger.error(e)
        finally:
            p4.disconnect()

        return result
    return wrapper


class MtkP4(object):

    @classmethod
    def _is_under_client(cls, file_path):
        u"""指定したファイルがクライアント下のものか

        :param file_path: ファイルのパス
        :return: bool
        """
        if not os.path.exists(file_path):
            return False

        drive, _ = os.path.splitdrive(file_path)
        if drive.upper() != 'Z:':
            logger.debug(u'{} is not under client'.format(file_path))
            return False

        return True

    @classmethod
    def _convert_argument(cls, argument):
        u"""引数を変換

        str, list, tuple -> list
        generator -> generator
        それ以外 -> []

        :param argument: 引数
        :return: list
        """
        if isinstance(argument, str):
            return [argument]
        elif isinstance(argument, list) or isinstance(argument, tuple):
            return argument
        elif isinstance(argument, types.GeneratorType):
            return argument
        else:
            return []

    @classmethod
    def _filter(cls, file_paths):
        u"""指定した引数をperforce管理下のファイルのみ取得してリストして返す

        :param file_paths: ファイルパスのリスト
        :return: list
        """
        return [file_path.encode('utf-8') for file_path in cls._convert_argument(file_paths) if cls._is_under_client(file_path)]

    @classmethod
    @p4wrapper
    def add(cls, file_paths):
        u"""追加

        :param file_paths: ファイルパスまたはファイルパスのリスト
        """
        filter_file_paths = cls._filter(file_paths)
        if filter_file_paths:
            p4.run_add(filter_file_paths)

    @classmethod
    @p4wrapper
    def edit(cls, file_paths):
        u"""チェックアウト

        :param file_paths: ファイルパスまたはファイルパスのリスト
        """
        filter_file_paths = cls._filter(file_paths)
        if filter_file_paths:
            p4.run_add(filter_file_paths)
            p4.run_edit(filter_file_paths)

    @classmethod
    @p4wrapper
    def revert(cls, file_paths, *args):
        u"""元に戻す

        :param file_paths: ファイルパスまたはファイルパスのリスト
        """
        filter_file_paths = cls._filter(file_paths)
        if filter_file_paths:
            if args:
                arguments = list(args) + filter_file_paths
                p4.run_revert(arguments)
            else:
                p4.run_revert(filter_file_paths)

    @classmethod
    @p4wrapper
    def sync(cls, file_paths, *args):
        u"""最新版を取得

        :param file_paths: ファイルパスまたはファイルパスのリスト
        """
        filter_file_paths = cls._filter(file_paths)
        if filter_file_paths:
            files = []
            for file_path in filter_file_paths:
                if os.path.isdir(file_path):
                    files.append('{}\\...'.format(re.sub(r'\\\\', r'\\', file_path)))
                else:
                    files.append('{}'.format(re.sub(r'\\\\', r'\\', file_path)))
            p4.run_sync(files)

    @classmethod
    @p4wrapper
    def submit(cls, file_paths, description):
        u"""サブミット

        :param file_paths: ファイルパスまたはファイルパスのリスト
        :param description: description
        """

        filter_file_paths = cls._filter(file_paths)

        if filter_file_paths:
            change = p4.fetch_change()
            change['Files'] = filter_file_paths
            change['Description'] = description

            new_change_list = p4.save_change(change)
            number = int(new_change_list[0].split()[1])

            for file_path in file_paths:
                p4.run_reopen('-c', number, file_path)

            p4.run_submit('-c', number)

    @classmethod
    @p4wrapper
    def fstat(cls, file_paths):
        u"""fstat

        :param file_paths: ファイルパスまたはファイルパスのリスト
        :return: fstat
        """
        filter_file_paths = cls._filter(file_paths)
        if filter_file_paths:
            stats = p4.run_fstat(filter_file_paths)
            return stats
        else:
            return []

    @classmethod
    def _get_action(cls, stat):
        u"""ファイルの状態

        :param stat: fstat
        :return: mode
        """
        if not stat:
            return 'none'

        if 'otherOpen' in stat:
            return 'other'
        elif 'haveRev'not in stat:
            return 'add'
        elif 'actionOwner' in stat:
            return 'checkout'
        else:
            have_rev = int(stat['haveRev'])
            head_rev = int(stat['headRev'])
            if have_rev < head_rev:
                return 'stale'
            else:
                return 'latest'

    @classmethod
    def _get_file_users(cls, stat):
        u"""ファイルのユーザー名

                :param stat: fstat
                :return: list
                """
        user_list = []

        if not stat:
            return user_list

        # collect name of current user
        if 'actionOwner' in stat:
            user_name = stat['actionOwner']
            user_list.append(user_name)

        # collect names of other users
        if 'otherOpens' in stat:
            otherOpens = stat['otherOpens']
            numOther = int(otherOpens)
            if numOther > 0:
                otherOpenList = stat['otherOpen']
                for p4_user_string in otherOpenList:
                    p4_user_tuple_list = re.findall(r'(.+)@(.+)', p4_user_string)
                    p4_user_tuple = p4_user_tuple_list[0]
                    user_name = p4_user_tuple[0]  # [0] is the p4 user name, [1] is the p4 workspace
                    user_list.append(user_name)

        return user_list

    @classmethod
    @p4wrapper
    def status(cls, file_paths):
        u"""ファイルの編集モードの取得

        :param file_path: ファイルパス
        :return:
        """
        file_status = OrderedDict({})

        stats = p4.run_fstat(file_paths)
        for file_path in file_paths:
            action = None
            have_rev = 0
            head_rev = 0
            for stat in stats:
                client_file = re.sub(r'\\', '/', stat['clientFile'])
                if file_path == client_file:
                    action = cls._get_action(stat)
                    have_rev = int(stat['haveRev']) if 'haveRev' in stat else 0
                    head_rev = int(stat['headRev']) if 'headRev' in stat else 0
                    stats.remove(stat)
                    break

            file_status[file_path] = {'action': action, 'haveRev': have_rev, 'headRev': head_rev}
        return file_status

    @classmethod
    @p4wrapper
    def status_ext(cls, file_paths):
        u"""ファイルの編集モードの取得, ファイルのユーザー名の取得

        :param file_path: ファイルパス
        :return:
        """
        user_list = []
        file_status = OrderedDict({})
        stats = p4.run_fstat(file_paths)

        for file_path in file_paths:
            action = None
            have_rev = 0
            head_rev = 0
            for stat in stats:
                client_file = re.sub(r'\\', '/', stat['clientFile'])
                if file_path == client_file:
                    action = cls._get_action(stat)
                    have_rev = int(stat['haveRev']) if 'haveRev' in stat else 0
                    head_rev = int(stat['headRev']) if 'headRev' in stat else 0
                    user_list = cls._get_file_users(stat)
                    stats.remove(stat)
                    break

            file_status[file_path] = {'action': action, 'haveRev': have_rev, 'headRev': head_rev, 'users': user_list}

        return file_status
