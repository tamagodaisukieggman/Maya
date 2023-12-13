# -*- coding: utf-8 -*-
u"""Maya用batファイル生成用の関数

※廃止予定のスクリプト
"""

import re
import os
from datetime import datetime

import maya.cmds as cmds

import logging
# from mtku.maya.log import MtkDBLog


# logger = MtkDBLog(__name__)
logger = logging.getLogger(__name__)


def get_temp_dir():
    u"""TEMPフォルダの取得

    :return: TEMPフォルダ
    """
    temp_dir = '{}/cygames_maya'.format(os.environ['TEMP'])
    temp_dir = re.sub(r'\\', '/', temp_dir)

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


def get_timestamp():
    u"""タイムスタンプの取得

    :return: タイムスタンプ
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return timestamp


def get_command_description(mel_command, name='mayabatch', suffix=0, no_load_plugins=False):
    u"""mayabatch実行用のコマンドを記述を取得

    :return: mayabatch実行用のコマンドの文字列
    """
    version = cmds.about(v=True)
    # mayabatch = r'"C:\Program Files\Autodesk\Maya{version}\bin\mayabatch.exe"'.format(
    #     version=version,
    # )
    mayabatch = r'"Z:\mtk\tools\maya\bat\Maya{version}.bat"'.format(
        version=version,
    )
    log = '{dir}/{name}_{suffix}.log'.format(
        dir=get_temp_dir(), name=name, suffix=suffix,
    )
    logger.debug('log: {}'.format(log))
    command_description = """\
call {mayabatch} -command {mel_command} -log {log}""".format(
        mayabatch=mayabatch, mel_command=mel_command, log=log,
    )
    if no_load_plugins:
        command_description += ' -noAutoloadPlugins\r\n'
    else:
        command_description += '\r\n'

    return command_description


def delete_self_description():
    u"""自分自身を削除する記述を取得

    :return: 自分自身を削除する記述
    """
    return 'del / F "%~dp0%~nx0"'


if __name__ == '__main__':
    import doctest
    import maya.standalone

    maya.standalone.initialize(name='python')
    doctest.testmod()
