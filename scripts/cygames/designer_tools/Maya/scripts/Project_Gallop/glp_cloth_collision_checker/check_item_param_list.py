# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya2022-
    from builtins import object
except Exception:
    pass


class CheckItemParamList(object):
    """
    """

    def __init__(self):

        self.check_item_param_list = None

    def set_check_item_param_list(self, check_item_list):

        self.check_item_param_list = []

        for check_item in check_item_list:
            item_param = CheckItemParam(check_item)
            result = item_param.set_check_item_param()
            if not result:
                continue

            self.check_item_param_list.append(item_param)


class CheckItemParam(object):

    def __init__(self, item):

        self.item = item

        # ラベル名
        self.label = None
        # 説明
        self.description = None
        # 実行関数
        self.func = None
        # 引数
        self.args = []
        # ボタン表示
        self.is_log_button_view = True
        self.is_list_button_view = True
        self.is_select_button_view = True
        self.is_correction_button_view = True

        # 内製専用かどうか
        self.is_internal = False

        # ui情報
        self.ui_info = {}

        # チェック情報
        self.check_answer_info = None

        # ボタンの色
        self.ui_button_for_error_bcg = [1, 0, 0]

    def set_check_item_param(self):

        # 必須要素がなかったらはじく
        if 'label' not in self.item:
            return False
        if 'func' not in self.item:
            return False
        if 'description' not in self.item:
            return False

        self.label = self.item['label']
        self.func = self.item['func']
        self.description = self.item['description']

        # ここから任意要素
        if 'args' in self.item:
            self.args = self.item['args']
        if 'is_log_button_view' in self.item:
            self.is_log_button_view = self.item['is_log_button_view']
        if 'is_list_button_view' in self.item:
            self.is_list_button_view = self.item['is_list_button_view']
        if 'is_select_button_view' in self.item:
            self.is_select_button_view = self.item['is_select_button_view']
        if 'is_correction_button_view' in self.item:
            self.is_correction_button_view = self.item['is_correction_button_view']
        if 'is_internal' in self.item:
            self.is_internal = self.item['is_internal']
        if 'ui_button_for_error_bcg' in self.item:
            self.ui_button_for_error_bcg = self.item['ui_button_for_error_bcg']

        return True
