# -*- coding: utf-8 -*-

from __future__ import absolute_import

import codecs

# import cPickle as pickle
import _pickle as cPickle
import pickle
import glob
import json
import os
import traceback


class JsonFile(object):
    """jsonファイルの読み込み、書き出し機能の提供"""

    @classmethod
    def read(cls, file_path):
        if not file_path:
            return {}

        if not os.path.isfile(file_path):
            return {}

        with codecs.open(file_path, "r", "utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
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

        with codecs.open(file_path, "w", "utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                # ensure_ascii=False,
                # sort_keys=True,
                separators=(",", ": "),
            )
            f.flush()
            os.fsync(f.fileno())


class PickleFile(object):
    """cPickleファイルの読み込み、書き出し機能の提供"""

    @classmethod
    def read(cls, file_path):
        if not file_path:
            return {}

        if not os.path.isfile(file_path):
            return {}

        with open(file_path, "rb") as f:
            try:
                data = pickle.load(f)
            except Exception:
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

        with open(file_path, "wb") as f:
            pickle.dump(data, f)
            f.flush()
            os.fsync(f.fileno())


def find_items(root_dir, name="*", depth=1, find_type="all"):
    """指定ディレクトリ階層化のファイルを取得

    :param str root_dir: jsonファイルを探すルートディレクトリ
    :param str name: 取得ファイル名
    :param int depth: jsonファイルを探すサブディレクトリの深さ
    :param str find_type: 対象データタイプ, 'all' or 'file' or 'directory'
    :return: jsonファイルを辞書で取得 {filename: filepath, ...}
    :rtype: dict
    """

    _valid_find_types = ["all", "file", "directory"]

    depth = depth if depth > 0 else 1

    find_type = find_type or "all"
    if find_type not in _valid_find_types:
        return {}

    search_dirs = [os.path.join(root_dir, *(["*"] * i + [name])) for i in range(depth)]

    ret = {}
    for search_dir in search_dirs:
        match_list = glob.glob(search_dir)
        for match_item in match_list:
            if find_type == "file" and not os.path.isfile(match_item):
                continue

            elif find_type == "directory" and not os.path.isdir(match_item):
                continue

            basename = os.path.basename(match_item)
            basename, ext = os.path.splitext(basename)
            ret[basename] = match_item.replace(os.sep, "/")

    return ret
