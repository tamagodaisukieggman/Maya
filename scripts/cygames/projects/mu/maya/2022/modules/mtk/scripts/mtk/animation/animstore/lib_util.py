# -*- coding: utf-8 -*-

from __future__ import absolute_import

# import global modules
import datetime
import getpass
import locale
import os
import socket
import subprocess
import sys
import tempfile
import traceback
import uuid


def get_uuid():
    """uuidを取得
    :return: uuid
    :rtype: str
    """

    return str(uuid.uuid4())


def get_utcnow(format_str='%Y-%m-%d %H:%M:%S'):
    """現在のutcを取得
    :param str format_str: strftimeフォーマットテキスト
    :return: 現在のutc
    :rtype: str
    """

    return datetime.datetime.utcnow().strftime(format_str)


def get_utcdelta(format_str='%Y-%m-%d %H:%M:%S',
                 days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=9, weeks=0):
    """現在のutcに差分を加えた時間を取得
    :param str format_str: strftimeフォーマットテキスト
    :param days:
    :param seconds:
    :param microseconds:
    :param milliseconds:
    :param minutes:
    :param hours:
    :param weeks:
    :return: local時間
    :rtype: str
    """

    utc = datetime.datetime.utcnow()
    delta = datetime.timedelta(
        days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds,
        minutes=minutes, hours=hours, weeks=weeks
    )

    return (utc + delta).strftime(format_str)


def get_datetime(time_str):
    """strftime文字列からdatetimeオブジェクトを取得
    :param str time_str: strftime文字列
    :return: datetimeオブジェクト
    :rtype: datetime
    """

    return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')


def get_computername():
    """コンピューター名を取得
    :return: コンピューター名
    :rtype: str
    """

    return socket.getfqdn()


def get_username():
    """ユーザー名を取得
    :return: ユーザー名
    :rtype: str
    """

    return getpass.getuser()


def get_tempdir():
    """tempディレクトリパスを取得
    :return: tempディレクトリパス
    :rtype: str
    """

    return tempfile.gettempdir().replace(os.sep, '/')


def get_temp_dir():
    """tempディレクトリパスを取得
    :return: tempディレクトリのパス
    :rtype: str
    """

    ret = ''

    temp_dir_keys = ['TMPDIR', 'TEMP', 'TMP']
    for key in temp_dir_keys:
        ret = os.environ.get(key)
        if ret:
            break

    if not ret:
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp')

    return ret.replace(os.sep, '/')


def get_os(short_name=True):
    """
    :param bool short_name: OS省略名を返す
    :return: OS名の取得('win', 'mac', 'lnx') or ('windows', 'mac', 'linux')
    :rtype: unicode
    """

    platform = sys.platform
    if platform in ['win32']:
        return 'win' if short_name else 'windows'

    elif platform in ['darwin']:
        return 'mac'

    elif platform in ['linux2', 'linux3']:
        return 'lnx' if short_name else 'linux'

    else:
        return ''


def open_explorer(path, selected=False):
    """
    エクスプローラを開く.

    :param str path: 表示するパス
    :param bool selected: 選択をされた状態ならTrue/そうでなければFalse.
    :note: この機能はWindowsでしか利用できません.
    """

    platform = get_os()
    if platform in ['win']:
        path = os.path.realpath(path)
        option = '/select,' if selected else ''
        encoding = locale.getpreferredencoding(False)
        subprocess.Popen(('explorer %s %s' % (option, path)).encode(encoding))

    else:
        cmd = ''
        if platform == 'mac':
            option = '-R' if selected else ''
            cmd = 'open %s %s' % (option, os.path.normpath(path))
        elif platform == 'lnx':
            cmd = 'xdg-open %s' % path
        if cmd:
            try:
                os.system(cmd)
            except OSError:
                traceback.print_exc()
