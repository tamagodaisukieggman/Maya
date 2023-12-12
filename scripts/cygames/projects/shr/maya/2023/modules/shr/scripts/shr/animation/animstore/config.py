# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from . import lib_util
from . import lib_maya

TOOL_NAME = 'animstore'
PREF_FILE_NAME = '{0}/pref/{0}_pref.json'.format(TOOL_NAME)
CLIPBOARD_DIR_NAME = '{0}/clipboard'.format(TOOL_NAME)
POSEDATA_DIR_NAME = '{0}/poses'.format(TOOL_NAME)
ANIMDATA_DIR_NAME = '{0}/animations'.format(TOOL_NAME)

TEMP_ANIMDATA_NAME = 'animation_temp'
TEMP_POSEDATA_NAME = 'pose_temp'
TEMP_SELECTDATA_NAME = 'select_temp'

ANIM_DATA_EXT = '.animdata'
POSE_DATA_EXT = '.posedata'
SELECT_DATA_EXT = '.seldata'


def get_pref_path():
    """プリファレンスファイルパスを取得
    :return: プリファレンスファイルパス
    :rtype: str
    """

    return os.path.join(lib_util.get_temp_dir(), PREF_FILE_NAME).replace(os.sep, '/')


def get_clipboard_dir():
    """クリップボードデータ保存ディレクトリを取得
    :return: クリップボード保存ディレクトリ
    :rtype: str
    """

    return os.path.join(lib_util.get_temp_dir(), CLIPBOARD_DIR_NAME).replace(os.sep, '/')


def get_temp_posedata_dir():
    """ポーズデータ一時保存ディレクトリを取得
    :return: ポーズデータ一時保存ディレクトリ
    :rtype: str
    """

    return os.path.join(lib_util.get_temp_dir(), POSEDATA_DIR_NAME).replace(os.sep, '/')


def get_temp_animdata_dir():
    """アニメーションデータ一時保存ディレクトリを取得
    :return: アニメーションデータ一時保存ディレクトリ
    :rtype: str
    """

    return os.path.join(lib_util.get_temp_dir(), ANIMDATA_DIR_NAME).replace(os.sep, '/')


def get_posedata_dir(root_dir):
    """ポーズデータ保存ディレクトリを取得
    :param str root_dir: ルートディレクトリ
    :return: ポーズデータ保存ディレクトリ
    :rtype: str
    """

    return os.path.join(root_dir, POSEDATA_DIR_NAME).replace(os.sep, '/')


def get_animdata_dir(root_dir):
    """アニメーションデータ保存ディレクトリを取得
    :param str root_dir: ルートディレクトリ
    :return: アニメーションデータ保存ディレクトリ
    :rtype: str
    """

    return os.path.join(root_dir, ANIMDATA_DIR_NAME).replace(os.sep, '/')


def get_workspace_posedata_dir():
    """カレントワークスペースディレクトリ下のポーズデータ保存ディレクトリを取得
    :return: カレントワークスペースディレクトリ下のポーズデータ保存ディレクトリ
    :rtype: str
    """

    return get_posedata_dir(lib_maya.get_workspace_dir())


def get_workspace_animdata_dir():
    """カレントワークスペースディレクトリ下のアニメーションデータ保存ディレクトリを取得
    :return: カレントワークスペースディレクトリ下のアニメーションデータ保存ディレクトリ
    :rtype: str
    """

    return get_animdata_dir(lib_maya.get_workspace_dir())
