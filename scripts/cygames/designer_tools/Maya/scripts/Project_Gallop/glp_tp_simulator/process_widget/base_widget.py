# -*- coding: utf-8 -*-
"""MVCでいうViewを担う
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets, QtCore


class TpProcessWidgetError(Exception):
    pass


class BaseWidget(QtWidgets.QWidget):

    # パラメーター編集時にemitするシグナル
    expression_edit = QtCore.Signal(QtWidgets.QWidget)

    def __init__(self, parent, param_data_template):
        super(BaseWidget, self).__init__(parent)

        self.param_data_template = param_data_template
        self.main_layout = QtWidgets.QVBoxLayout(self)

    def create_widget(self):
        """ウィジェットの作成
        """

        msg = 'create_widgetがオーバーライドされていません'
        raise TpProcessWidgetError(msg)

    def get_target_data(self):
        """UIからプロセスの制御対象となるノードとアトリビュートリストを取得

        Returns:
            str: ノード
            list: アトリビュートリスト
        """

        return None, []

    def get_param_data(self):
        """UIからプロセスで使用するパラメーターを取得

        Returns:
            dict: プロセスで使用されるパラメーターdict. {attr_name: {'type': type, 'value': value},,,}
        """

        return {}

    def import_param_data(self, target, param_data):
        """パラメーター情報の読み込み

        Args:
            target (str): ターゲットノード
            param_data (dict): プロセスで使用されるパラメーターdict. {attr_name: {'type': type, 'value': value},,,}
        """

        pass
