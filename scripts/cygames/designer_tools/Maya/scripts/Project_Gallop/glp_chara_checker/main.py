# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import os

import maya.cmds as cmds

from .. import base_common
from ..base_common import classes as base_class

from .. import glp_common
from ..glp_common import classes as glp_class

from . import checker_param_root
from . import checker_param_item
from . import checker_param_list
from . import checker_method
from . import checker_info
from . import checker_info_window

reload(base_common)
reload(glp_common)

reload(checker_param_root)
reload(checker_param_item)
reload(checker_method)
reload(checker_info_window)
reload(checker_param_list)
reload(checker_info)


# ==================================================
def main():

    this_main = Main()
    this_main.create_ui()


# ==================================================
def export_csv():

    this_main = Main()
    this_main.export_csv()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ==================================================
    def __init__(self):

        self.tool_version = '23031301'

        self.tool_name = 'GallopCharaChecker'

        self.window_name = self.tool_name + 'Win'

        self.setting = \
            base_class.setting.Setting(self.tool_name)

        self.chara_info = None
        self.checker_param_root = None

        # UI関連
        self.ui_updating = False

        self.ui_update_count = 0

        self.logger = base_class.logger.Logger()

        self.each_info_logger = base_class.logger.Logger()

        # 初期化フラグ
        self.is_init = False

        # ユーザー作成のchara_data.csvを使用しているかどうか
        self.is_use_user_create_chara_data_csv = False

    # ==================================================
    def initialize(self):

        self.is_init = False

        self.chara_info = glp_class.info.chara_info.CharaInfo()

        self.checker_param_root = checker_param_root.CheckerParamRoot(self)
        self.checker_param_root.initialize()

        self.is_init = True

    # ==================================================
    def create_ui(self):

        self.initialize()

        if not self.is_init:
            return

        self.checker_param_root.create_ui()

    # ==================================================
    def update_chara_info(self):

        self.is_use_user_create_chara_data_csv = False

        self.chara_info.create_info(is_create_all_info=True)
        if self.chara_info.exists is False:
            return

        # maと同じフォルダにchara_data.csvがあり
        # id, height, bust, scale 情報が揃っていたらそちらを優先する
        chara_data_csv_path = self.chara_info.file_dir + '/chara_data.csv'
        chara_data_dict = self.get_chara_dict_by_id(self.chara_info.data_main_id, chara_data_csv_path)
        if chara_data_dict:

            checker_data_info = CheckerDataInfo()
            checker_data_info.set_data(chara_data_dict)
            if checker_data_info.exists:

                self.chara_info.data_info.height_id = checker_data_info.height_id
                self.chara_info.data_info.bust_id = checker_data_info.bust_id
                self.chara_info.data_info.shape_id = checker_data_info.shape_id
                self.chara_info.data_info.exists = checker_data_info.exists
                self.is_use_user_create_chara_data_csv = True

        if not self.chara_info.data_info.exists:
            if self.chara_info.is_unique_chara:
                cmds.warning('キャラクターのデータ取得に失敗しました。キャラIDの入ったchara_data.csvがあるか確認してください。')

    # ===============================================
    def get_chara_dict_by_id(self, data_main_id, chara_data_csv_path):
        """
        chara_data.csvを読み指定したID列のディクショナリを返す
        Args:
            chara_id (str): キャラID
            chara_data_csv_path (str): chara_data.csvのパス
        Returns:
            dict: base_class.csv_reader.CsvReaderで読み取ったディクショナリ
        """

        if data_main_id is None or not os.path.exists(chara_data_csv_path):
            return None

        chara_data_csv_reader = base_class.csv_reader.CsvReader()
        chara_data_csv_reader.read(chara_data_csv_path, 'utf-8')
        chara_data_csv_reader.update('id', '')
        chara_data_dicts = chara_data_csv_reader.get_value_dict_list()
        # キャラのidがマッチするcsvの行のディクショナリを探す
        for chara_data_dict in chara_data_dicts:
            chara_id = chara_data_dict.get('id')
            if chara_id is not None and str(chara_id).startswith(data_main_id):
                return chara_data_dict

        return None

    # ==================================================
    def export_csv(self):

        self.initialize()

        if not self.is_init:
            return

        self.checker_param_root.export_csv()


class CheckerDataInfo(object):
    """
    CharaDataの持つDataInfoは glp_common/_resource/chara_info内のcsvから読み込む仕様になっている
    Mayaシーンのプロジェクトフォルダ内に置いたcsvがあったらそちらを先に読み込ませる仕様を追加する際
    本家を変更せずにキャラチェッカー内で対応する必要が出たので作られたクラス
    chara_data.csvの列はid, height, bust, shapeだけあれば動作するようにする
    """
    def __init__(self):
        self.height_id = None
        self.bust_id = None
        self.shape_id = None
        self.exists = False

    def set_data(self, chara_data_dict):
        """
        data_infoの代替用変数をインスタンス変数に設定する
        必須変数は全てNoneか''以外の値が入っているかチェックし、問題なければExistsをTrueにする
        Args:
            data (dict): ユーザーフォルダcsvから取得したディクショナリ
        """
        self.height_id = chara_data_dict.get('height')
        self.bust_id = chara_data_dict.get('bust')
        self.shape_id = chara_data_dict.get('shape')
        # 必須要素が満たされているかの判定 全てに値が入っていればexists = Trueになる
        if not [v for v in [self.height_id, self.shape_id, self.bust_id] if v is None or v == '']:
            self.exists = True
