# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya2022-
    from builtins import range
    from importlib import reload
except Exception:
    pass

import os
import uuid
import maya.cmds as cmds

from PySide2 import QtWidgets, QtCore, QtGui

from . import define
from . import utils
from .ui import item_widget

reload(define)
reload(utils)
reload(item_widget)


class Item(QtWidgets.QWidget):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    # signal
    delete_process_item = QtCore.Signal(QtWidgets.QWidget)

    def __init__(self, parent, process_datas, save_node=None):
        """コンストラクター

        Args:
            parent (view.View): メインウィンドウ
            process_datas (list): main.tp_process_datas
            save_node (str, optional): アイテム情報をセーブしたノード.Noneの場合は新規作成. Defaults to None.
        """

        super(Item, self).__init__(parent)

        self.__is_visible = True
        self.__process_datas = process_datas
        self.__item_id = ''

        self.__item_widget = item_widget.Ui_Form()
        self.__item_widget.setupUi(self)

        self.__process_widget = None
        self.__process_model = None

        self.__save_node = save_node
        self.__block_save = False

        self.__opening_icon = None
        self.__closing_icon = None
        self.__delete_icon = None

        if os.path.exists(define.FRAME_OPEN_ICON_PATH):
            self.__opening_icon = QtGui.QIcon(define.FRAME_OPEN_ICON_PATH)
        if os.path.exists(define.FRAME_CLOSE_ICON_PATH):
            self.__closing_icon = QtGui.QIcon(define.FRAME_CLOSE_ICON_PATH)
        if os.path.exists(define.DELETE_ICON_PATH):
            self.__delete_icon = QtGui.QIcon(define.DELETE_ICON_PATH)

        self.__initialize_item()

    def __initialize_item(self):
        """アイテムの初期化
        """

        # 使用可能なプロセス一覧をプルダウンに定義
        labels = [x.get('label') for x in self.__process_datas if x.get('label')]
        self.__item_widget.expression_combo.addItems(labels)

        # セーブノードがあれば情報を復元、なければIDだけ作成
        if self.__save_node and cmds.objExists(self.__save_node):
            self.load_item(self.__save_node)
        else:
            self.__item_id = str(uuid.uuid4())

        # ウィジェットの設定
        self.__initialize_ui()
        self.__setup_widget_event()
        self.__update_frame_label()
        self.__update_enable_label_color()
        self.__update_frame_icon()

    def save_item_deco(func):
        """アイテムセーブを行うデコレーター
        """
        def inner(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.save_item()
            return result
        return inner

    def __initialize_ui(self):
        """UI初期設定
        """

        widget = self.item_widget()
        widget.frame_button.setStyleSheet('text-align: left;')

        if self.__delete_icon:
            widget.del_item_button.setText('')
            widget.del_item_button.setIcon(self.__delete_icon)

    def __setup_widget_event(self):
        """イベントを設定
        """

        self.__item_widget.expression_combo.wheelEvent = lambda event: None  # 事故防止のためマウススクロールイベントをふさぐ
        self.__item_widget.frame_button.clicked.connect(self.__toggle_visible)
        self.__item_widget.del_item_button.clicked.connect(self.__delete_item_event)
        self.__item_widget.expression_combo.currentIndexChanged.connect(self.__select_process_event)
        self.__item_widget.enable_check.stateChanged.connect(self.__enable_check_event)

    def __update_frame_label(self):
        """フレームのラベルを更新
        """

        label = '__No Target__'
        if self.__process_widget:
            target, _ = self.__process_widget.get_target_data()
            label = target or label
        else:
            label = 'New Process'

        self.__item_widget.frame_button.setText(label)

    @save_item_deco
    def __toggle_visible(self, *args):
        """フレームの表示/非表示切り替え
        """

        self.__is_visible = not self.__is_visible
        if self.__is_visible:
            self.__item_widget.frame_group.show()
        else:
            self.__item_widget.frame_group.hide()

        self.__update_frame_icon()

    def __update_frame_icon(self):
        """フレーム開閉アイコンの更新
        """

        if self.is_visible():
            if self.__opening_icon:
                self.__item_widget.frame_button.setIcon(self.__opening_icon)
        else:
            if self.__closing_icon:
                self.__item_widget.frame_button.setIcon(self.__closing_icon)

    def __delete_item_event(self):
        """アイテムの削除イベント
        """

        self.__stop_process()

        if cmds.objExists(self.save_node()):
            cmds.delete(self.save_node())

        self.delete_process_item.emit(self)

    def __select_process_event(self):
        """プロセス切り替えイベント
        """

        self.set_process(self.__item_widget.expression_combo.currentText())
        self.__update_frame_label()

    def __enable_check_event(self):
        """有効化チェックボックスイベント
        """

        self.update_process()
        self.__update_enable_label_color()

    def __process_edit_event(self):
        """プロセス更新時イベント
        """

        self.update_process()
        self.__update_enable_label_color()

    def __update_enable_label_color(self):
        """サイドフレームの背景色変更
        """

        widget = self.item_widget()

        style = '#enable_label_frame {background-color: rgb(64, 64, 64)};'
        if widget.enable_check.isChecked():
            model = self.process_model()
            if model and model.is_activated():
                style = '#enable_label_frame {background-color: rgb(72, 72, 160)};'
            else:
                style = '#enable_label_frame {background-color: rgb(160, 72, 72)};'

        widget.enable_label_frame.setStyleSheet(style)

    def item_id(self):
        """アイテムIDを取得

        Returns:
            str: アイテムID
        """

        return self.__item_id

    def item_widget(self):
        """アイテムウィジェットの取得

        Returns:
            item_widget: アイテムウィジェット
        """

        return self.__item_widget

    def process_widget(self):
        """プロセスウィジェットの取得

        Returns:
            QtWidgets.QWidget: プロセス固有のウィジェット
        """

        return self.__process_widget

    def process_model(self):
        """プロセスモデルの取得

        Returns:
            object: プロセスモデル
        """

        return self.__process_model

    def save_node(self):
        """セーブノードの取得

        Returns:
            str: アイテム情報をセーブしているノード
        """

        return self.__save_node

    def process_type(self):
        """現在このアイテムで使用しているプロセスタイプを取得

        Returns:
            str: 現在このアイテムで使用しているプロセスタイプ
        """

        return self.__item_widget.expression_combo.currentText()

    def is_visible(self):
        """プロセスウィジェットを展開表示しているか

        Returns:
            bool: プロセスウィジェットを展開表示しているか
        """

        return self.__is_visible

    def set_activated(self, is_activated):
        """有効化を設定

        Args:
            is_activated (bool): 有効/無効
        """

        self.__item_widget.enable_check.blockSignals(True)
        self.__item_widget.enable_check.setChecked(is_activated)
        self.__item_widget.enable_check.blockSignals(False)
        self.__enable_check_event()

    def is_activated(self):
        """プロセスを有効化しているか

        Returns:
            bool: プロセスを有効化しているか
        """

        return self.__item_widget.enable_check.isChecked()

    def set_save_block(self, block):
        """セーブをブロックするか
        ロード中などセーブが走らないようにするフラグ

        Args:
            block (bool): セーブをブロックするか
        """
        self.__block_save = block

    def is_save_blocking(self):
        """セーブがブロックされているか

        Returns:
            bool: セーブがブロックされているか
        """
        return self.__block_save

    @save_item_deco
    def set_process(self, process_type):
        """適用するプロセスを設定

        Args:
            process_type (str): 適用するプロセスタイプ（コンボボックスのラベル）
        """

        self.reset_process()

        for process_data in self.__process_datas:
            if process_data.get('label') == process_type:

                model = process_data.get('model')
                widget = process_data.get('widget')

                if model and widget:

                    self.__process_model = model()
                    param_data_template = self.__process_model.create_param_data_template()

                    self.__process_widget = widget(self, param_data_template)
                    self.__process_widget.create_widget()

                    if self.save_node():
                        self.__process_model.load_process_param(self.save_node())
                        self.__set_model_param_to_widget(self.__process_model, self.__process_widget)

                    self.__process_widget.expression_edit.connect(self.__process_edit_event)
                    self.__item_widget.expression_layout.addWidget(self.__process_widget)

        self.update_process()

    def __set_model_param_to_widget(self, model, widget):
        """モデルのパラメーターをウィジェットに反映

        Args:
            model (object): モデル
            widget (QtWidgets.QWidget): ウィジェット
        """

        if model and widget:
            target = model.target()
            param_data = model.param_data()
            widget.import_param_data(target, param_data)

    def __set_widget_param_to_model(self, model, widget):
        """ウィジェットのパラメーターをモデルに反映

        Args:
            model (object): モデル
            widget (QtWidgets.QWidget): ウィジェット
        """

        if model and widget:
            target, attrs = widget.get_target_data()
            param_data = widget.get_param_data()
            model.update_model(target, attrs, param_data)

    @save_item_deco
    def reset_process(self, *args):
        """アイテムの設定をすべてリセットする
        """
        # 登録しているprocessを削除
        self.__stop_process()

        # UIを削除
        count = self.__item_widget.expression_layout.count()
        if count > 0:
            for index in reversed(range(count)):
                item = self.__item_widget.expression_layout.itemAt(index)
                widget = item.widget()
                widget.deleteLater()

        # 変数を削除
        self.__process_widget = None
        self.__process_model = None

        # ラベルを更新
        self.__update_frame_label()

    def __stop_process(self):
        """プロセスを停止
        """

        # このアイテムで登録していたexpressionを削除
        model = self.process_model()
        if model:
            self.set_activated(False)
            model.stop_process()

    @save_item_deco
    def update_process(self, *args):
        """プロセスを更新する
        """

        # ラベルを更新
        self.__update_frame_label()

        # モデルかウィジェットがない場合はリセットして終了
        widget = self.process_widget()
        model = self.process_model()
        if not widget or not model:
            self.reset_process()
            return

        # ウィジェットのパラメーターをモデルに反映
        self.__set_widget_param_to_model(self.process_model(), self.process_widget())

        # 有効化
        result = True
        msg = ''

        if self.is_activated():
            if not model.is_activated():
                result, msg = model.start_process()
        else:
            model.stop_process()

        if not result:
            cmds.confirmDialog(m=msg)

    def save_item(self):
        """アイテム情報をセーブ
        """

        if self.is_save_blocking():
            return

        self.__create_save_node()

        # アイテム情報
        utils.save_in_extra_attrs(self.save_node(), self.__get_item_base_param())

        # プロセス情報
        process_model = self.process_model()
        if process_model:
            process_model.save_process_param(self.save_node())

    def load_item(self, save_node):
        """アイテム情報をロード

        Args:
            save_node (str): アイテム情報がセーブされているノード
        """

        if not cmds.objExists(save_node):
            return

        self.set_save_block(True)

        self.__save_node = save_node
        self.__item_id = save_node.split('|')[-1].replace(define.ITEM_NODE_BASE_NAME, '')

        # 保存値を取得
        process_type = utils.load_from_extra_attrs(save_node, 'processType')
        is_activated = utils.load_from_extra_attrs(save_node, 'isActivated')
        is_visible = utils.load_from_extra_attrs(save_node, 'isVisible')

        # itemをロード
        widget = self.item_widget()

        if process_type is not None:
            self.set_process(process_type)
            index = widget.expression_combo.findText(process_type)
            if index >= 0:
                widget.expression_combo.blockSignals(True)
                widget.expression_combo.setCurrentIndex(index)
                widget.expression_combo.blockSignals(False)

        if is_activated is not None:
            widget.enable_check.blockSignals(True)
            widget.enable_check.setChecked(is_activated)
            widget.enable_check.blockSignals(False)

        if is_visible is not None:
            self.__is_visible = is_visible
            if self.__is_visible:
                self.__item_widget.frame_group.show()
            else:
                self.__item_widget.frame_group.hide()

        # プロセス情報をmodelにロード
        process_model = self.process_model()
        if process_model:
            process_model.load_process_param(save_node)

        # widgetに反映
        process_widget = self.process_widget()
        self.__set_model_param_to_widget(process_model, process_widget)

        self.set_save_block(False)

        self.update_process()

    def __create_save_node(self):
        """セーブノードの作成
        """

        save_node = self.save_node()
        if save_node and cmds.objExists(save_node):
            return

        name = define.ITEM_NODE_BASE_NAME + self.item_id()
        self.__save_node = cmds.scriptNode(n=name, ire=True)

    def __get_item_base_param(self):
        """アイテムの基本情報
        セーブ用にキーにアトリビュート名、値にtypeとvalueを持つdictを持つ

        Returns:
            dicr: アイテムの基本情報
        """

        return {
            'itemOrder': {
                'type': 'long',
                'value': self.parent().get_index(self),
            },
            'processType': {
                'type': 'string',
                'value': self.process_type(),
            },
            'isActivated': {
                'type': 'bool',
                'value': self.is_activated(),
            },
            'isVisible': {
                'type': 'bool',
                'value': self.is_visible(),
            },
        }

