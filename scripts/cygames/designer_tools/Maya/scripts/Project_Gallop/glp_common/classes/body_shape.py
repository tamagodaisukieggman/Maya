# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import csv
import os

resource_dir_path = os.path.abspath(os.path.join(__file__, '../../_resource'))


class BodyShape(object):
    """体型差分データクラス

    Attributes:
        enabled (bool): 体型差分が有効か
        suffix (str): ファイル出力時のサフィックス
        scale (float): モデルのスケール
        targets (dict[str, float]): 体型差分を構成するターゲットとウェイトのリスト
    """

    def __init__(self, enabled, suffix, scale, targets):
        self.enabled = enabled
        self.suffix = suffix
        self.scale = scale
        self.targets = targets

    def has(self, target):
        """この体型差分が指定されたターゲットを含むかを返す

        Args:
            target (str): チェックするターゲット名

        Returns:
            bool: 指定されたターゲットを含むか
        """

        if not isinstance(self.targets, dict):
            return None

        return target in self.targets


class BodyShapeInfo(object):
    """体型差分と、関連するブレンドシェイプターゲットをまとめたクラス

    Attributes:
        targets (list[str]): 体型差分で使用しているブレンドシェイプターゲットのリスト
        shapes (list[BodyShape]): 体型差分のリスト
    """

    def __init__(self, targets, shapes):
        self.targets = targets
        self.shapes = shapes


class BodyShapeInfoParser(object):
    """体型差分の読み込みと作成を行うクラス

    Attributes:
        ENABLE_KEY (str): Enableのキー
        SUFFIX_KEY (str): サフィックスのキー
        SCALE_KEY (str): スケールのキー
        REQUIRED_KEYS (list[str]): 体型差分読み込み時にファイル内に必要な項目
        FILTER_TARGETS (list[str]): フィルタ用のターゲットリスト
    """

    ENABLE_KEY = 'Enable'
    SUFFIX_KEY = '____FileSuffix'
    SCALE_KEY = '____Scale'
    REQUIRED_KEYS = [ENABLE_KEY, SUFFIX_KEY, SCALE_KEY]
    FILTER_TARGETS = ['_Bust_L', '_Bust_LL']

    @classmethod
    def create_from_chara_info(cls, chara_info, check_enabled=True):
        """CharaInfoから体型差分情報を作成する

        Args:
            chara_info (CharaInfo): 作成元のCharaInfo
            check_enabled (bool): 体型差分のenabled属性をチェックするか

        Returns:
            BodyShapeInfo: 体型差分情報
        """

        if chara_info is None:
            return None

        if not chara_info.exists:
            return None

        if not chara_info.is_common_body and chara_info.data_id != 'bdy0000_00':
            return None

        path = cls.__get_csv_path(chara_info)

        if path is None:
            return None

        targets_and_shapes = cls.__read_csv(path)

        if targets_and_shapes is None:
            return None

        targets, shapes = targets_and_shapes

        if check_enabled:
            shapes = [shape for shape in shapes if shape.enabled]

        if '_BustL' in chara_info.file_name:
            shapes = [shape for shape in shapes if cls.__filter_shape(shape, True)]

        if '_BustM' in chara_info.file_name:
            shapes = [shape for shape in shapes if cls.__filter_shape(shape, False)]

        return BodyShapeInfo(targets, shapes)

    @classmethod
    def __read_csv(cls, path):
        """CSVから体型差分情報を読み込む

        Args:
            path (str): CSVのパス

        Returns:
            tuple[list[str], list[BodyShape]]: ターゲットのリスト、体型差分のリストのタプル
        """

        if not os.path.isfile(path):
            return None

        try:
            with open(path) as f:
                csv_reader = csv.reader(f)
                headings = next(csv_reader)
                rows = list(csv_reader)

        except Exception:
            return None

        if not cls.__validate_keys(headings):
            return None

        targets = cls.__exclude_required_keys(headings)

        if not targets:
            return None

        shapes = [shape for shape in (cls.__create_body_shape(headings, row) for row in rows) if shape]

        if not shapes:
            return None

        return targets, shapes

    @classmethod
    def __create_body_shape(cls, keys, values):
        """キー、値リストから体型差分情報を作成する

        Args:
            keys (list[str]): キーリスト
            values (list[str]): 値リスト

        Returns:
            BodyShape: 体型差分
        """

        if not cls.__validate_keys(keys):
            return None

        if len(values) != len(keys):
            return None

        args = dict(zip(keys, values))
        target_keys = cls.__exclude_required_keys(keys)

        try:
            enabled = bool(int(args[cls.ENABLE_KEY]))
            suffix = args[cls.SUFFIX_KEY]
            scale = float(args[cls.SCALE_KEY])
            targets = {key: value for key, value in ((key, float(args[key])) for key in target_keys) if value}

        except Exception:
            return None

        return BodyShape(enabled, suffix, scale, targets)

    @classmethod
    def __get_csv_path(cls, chara_info):
        """CharaInfoから体型差分のCSVパスを取得する

        Args:
            chara_info (CharaInfo): 取得元のCharaInfo

        Returns:
            str: 体型差分のCSVパス
        """

        if not chara_info.exists:
            return None

        path = chara_info.part_info.maya_root_dir_path + '/common_body_info.csv'

        if os.path.isfile(path):
            return path

        if chara_info.part_info.is_mini:
            path = resource_dir_path + '/mini_common_body_info.csv'
        else:
            path = resource_dir_path + '/common_body_info.csv'

        if os.path.isfile(path):
            return path

        return None

    @classmethod
    def __validate_keys(cls, keys):
        """キーリストが想定されたフォーマットかチェックする

        Args:
            keys (list[str]): チェックするキーリスト

        Returns:
            bool: キーリストが想定されたフォーマットか
        """

        return all(key in keys for key in cls.REQUIRED_KEYS)

    @classmethod
    def __exclude_required_keys(cls, keys):
        """キーリストから必須キーを除外する

        Args:
            keys (list[str]): キーリスト

        Returns:
            list[str]: 必須キーを除外したキーリスト
        """

        return [key for key in keys if key not in cls.REQUIRED_KEYS]

    @classmethod
    def __filter_shape(cls, shape, include):
        """体型差分が特定のブレンドシェイプを含む、あるいは含まないかをチェックする

        Args:
            shape (BodyShape): チェックする体型差分
            include (bool): チェック条件を指定する。Trueなら『含む』、Falseなら『含まない』

        Returns:
            bool: 特定のブレンドシェイプを含む、あるいは含まないか
        """

        result = any(shape.has(target) for target in cls.FILTER_TARGETS)

        return result if include else not result
