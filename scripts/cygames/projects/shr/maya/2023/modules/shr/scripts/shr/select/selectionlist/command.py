# -*- coding: utf-8 -*-

from __future__ import absolute_import

import _pickle as pickle
import datetime
import os
import re
import tempfile
import traceback

import maya.cmds as cmds

from tatool.config import Config

class PickleFile(object):
    """cPickleファイルの読み込み、書き出し機能の提供
    """

    @classmethod
    def read(cls, file_path):
        if not file_path:
            return {}

        if not os.path.isfile(file_path):
            return {}

        with open(file_path, 'r') as f:
            try:
                data = pickle.load(f)
            except Exception as e:
                cmds.warning('{}'.format(e))
                traceback.print_exc()
                data = {}

        return data

    @classmethod
    def write(cls, file_path, data):
        if not file_path:
            return

        dirname, basename = os.path.split(file_path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        with open(file_path, 'w') as f:
            pickle.dump(data, f)
            f.flush()
            os.fsync(f.fileno())


def get_utcnow(format_str='%Y-%m-%d %H:%M:%S'):
    """現在のutcを取得
    :param str format_str: strftimeフォーマットテキスト
    :return: 現在のutc
    :rtype: str
    """

    return datetime.datetime.utcnow().strftime(format_str)


def get_tempdir():
    """tempディレクトリパスを取得
    :return: tempディレクトリパス
    :rtype: str
    """

    return tempfile.gettempdir().replace(os.sep, '/')


def get_icon(icon_name):
    """アイコンパスの取得
    :param str icon_name: アイコン名
    :return: アイコンパス
    :rtype: str
    """

    icon_path = os.path.join(os.path.dirname(__file__), 'icons', icon_name).replace(os.sep, '/')
    return icon_path if os.path.isfile(icon_path) else ''


def get_object_namespace(node):
    """ノード名からネームスペースを取得

    :param str node: ノード名
    :return: ネームスペース名
    :rtype: str
    """

    node = node.rsplit('|', 1)[-1].split('.')[0]
    p = node.rfind(':')

    if p >= 0:
        return ':%s' % node[:p]
    else:
        return ':'


def get_object_name(node):
    """ノード名からオブジェクト名(ネームスペース無しのノード名)を取得
    :param str node: ノード名
    :return: オブジェクト名
    :rtype: str
    """

    node = node.rsplit('|', 1)[-1].split('.')[0]
    p = node.rfind(':')

    if p >= 0:
        return node[p + 1:]
    else:
        return node


def get_object_uniquename(object_name):
    """ノード名からオブジェクト名(ネームスペース無しのノード名)を取得

    get_object_name の ノード名重複対応版

    :param str object_name: ノード名
    :return: オブジェクト名
    :rtype: str
    """

    namespace = get_object_namespace(object_name).strip(':')
    return re.sub(':+', ':', '|'.join([
        p.replace(namespace, '', 1).strip(':') for p in object_name.split('|') if p
    ])).strip('|').split('.')[0]


def add_namespace(object_name, namespace=':'):
    """オブジェクトにネームスペースを追加した名前を取得
    dagNodeの場合は全階層にネームスペースを追加する
    :param str object_name: オブジェクト名
    :param str namespace: 追加ネームスペース名
    :return: object_name に namespaceを追加した名前
    :rtype: str
    """

    return '|'.join([
        '{}:{}'.format(namespace, p).strip(':') for p in object_name.split('|') if p
    ]).strip('|')


def replace_namespace(object_name, namespace=':'):
    """オブジェクトのネームスペースを入れ替えた名前を取得
    dagNodeの場合は全ての階層のネームスペースを入れ替える
    :param str object_name: オブジェクト名
    :param str namespace: 入れ替えるネームスペース名
    :return: ネームスペースを入れ替えたオブジェクト名
    :rtype: str
    """

    ret = re.sub(':+', ':', add_namespace(get_object_uniquename(object_name), namespace=namespace))
    if '.' in object_name:
        return ret + '.' + object_name.split('.', 1)[-1]
    else:
        return ret


def list_namespaces(root_namespace=':', recurse=False):
    """シーン内のネームスペースのリストを取得
    :param str root_namespace: ルートネームスペース
    :param bool recurse: 再帰的にネームスペースを取得
    :return: ネームスペースのリスト
    :rtype: list
    """

    exclude_list = ['UI', 'shared']
    root_namespace = root_namespace or ':'

    current = cmds.namespaceInfo(cur=True)
    cmds.namespace(set=root_namespace)
    namespaces = [':{}'.format(ns) for ns in cmds.namespaceInfo(lon=True, recurse=recurse) if ns not in exclude_list]
    cmds.namespace(set=current)

    return namespaces
