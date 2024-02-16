# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds

from .. import utils

reload(utils)


class TpProcessModelError(Exception):
    pass


class BaseModel(object):

    def __init__(self):

        self.__target_node = None
        self.__target_attrs = []
        self.__init_vals = []
        self.__param_data = {}
        self.__process_nodes = []

    def create_param_data_template(self):
        """モデルのパラメーターテンプレート

        Returns:
            dict: パラメーターテンプレート
        """

        # param_data = {'attr': {'value': val, 'type': type},}
        param_data = {}
        return param_data

    def target(self):
        """プロセスの操作対象（=対象のtp骨）

        Returns:
            str: プロセスの操作対象
        """
        return self.__target_node

    def target_attrs(self):
        """プロセスの操作対象となるアトリビュートリスト

        Returns:
            list: アトリビュートリスト
        """
        return self.__target_attrs

    def init_vals(self):
        """プロセススタート前の初期値
        インデックスはtarget_attrs()のアトリビュートと同じ

        Returns:
            list: プロセススタート前の初期値
        """
        return self.__init_vals

    def set_init_vals(self, vals):
        """プロセススタート前の初期値をセット
        インデックスはtarget_attrs()のアトリビュートと同じ
        """
        self.__init_vals = vals

    def process_nodes(self):
        """プロセス実行時に作成されたノードリスト

        Returns:
            list: プロセス実行時に作成されたノードリスト
        """
        return self.__process_nodes

    def param_data(self):
        """プロセスで使用されるパラメーターdict

        Returns:
            dict: プロセスで使用されるパラメーターdict. {attr_name: {'type': type, 'value': value},,,}
        """
        return self.__param_data

    def is_activated(self):
        """実行中かどうか
        プロセス実行のために作成されたノードの有無で判定

        Returns:
            bool: 実行中かどうか
        """

        return True if self.__process_nodes else False

    def __set_targets(self, target_node, target_attrs):
        """プロセスの操作対象となるアトリビュートを指定

        Args:
            target_node (str): 操作対象のノード
            target_attrs (list): 操作対象のアトリビュートリスト
        """

        self.__target_node = target_node
        self.__target_attrs = target_attrs

        if self.__target_node and self.__target_attrs and cmds.objExists(self.__target_node):
            self.set_init_vals([cmds.getAttr('{}.{}'.format(self.__target_node, x)) for x in self.__target_attrs])

    def __set_param_data(self, param_data):
        """プロセスで使用されるパラメーターを設定

        Args:
            param_data (dict): プロセスで使用されるパラメーターdict. {attr_name: {'type': type, 'value': value},,,}
        """

        self.__param_data = param_data

    def save_process_param(self, save_node):
        """プロセス用のパラメーターを記録用ノードに保存

        Args:
            save_node (str): 記録用ノード
        """

        utils.save_in_extra_attrs(save_node, self.__get_save_param())

    def __get_save_param(self):
        """記録用ノードに保存するパラメーターのdictを取得

        Returns:
            dict: セーブするパラメーターdict. {attr_name: {'type': type, 'value': value},,,}
        """

        save_param = {}
        save_param.update(
            {
                'targetNode': {
                    'type': 'string',
                    'value': self.target(),
                },
                'targetAttrs': {
                    'type': 'stringArray',
                    'value': self.target_attrs(),
                },
                'targetOrgVals': {
                    'type': 'floatArray',
                    'value': self.init_vals(),
                },
                'processNodes': {
                    'type': 'stringArray',
                    'value': self.process_nodes(),
                },
            }
        )

        save_param.update(self.param_data())

        return save_param

    def load_process_param(self, save_node):
        """記録用ノードからパラメーターをロード

        Args:
            save_node (_type_): _description_
        """

        if not cmds.objExists(save_node):
            return

        self.__target_node = utils.load_from_extra_attrs(save_node, 'targetNode')
        self.__target_attrs = utils.load_from_extra_attrs(save_node, 'targetAttrs', [])
        self.__init_vals = utils.load_from_extra_attrs(save_node, 'targetOrgVals', [])
        self.__process_nodes = utils.load_from_extra_attrs(save_node, 'processNodes', [])

        param_data = self.create_param_data_template()

        for key in param_data:

            val_type = param_data[key].get('type')
            default_val = None

            if val_type in ['long', 'short', 'double']:
                default_val = 0
            elif val_type == 'string':
                default_val = ''
            elif val_type in ['stringArray', 'floatArray']:
                default_val = []

            param_data[key].update({'value': utils.load_from_extra_attrs(save_node, key, default_val)})

        self.__param_data = param_data

    def update_model(self, target, target_attr, param_data):
        """モデルを更新

        Args:
            target (str): ターゲットノード
            target_attr (list): アトリビュートリスト
            param_data (dict): パラメーターdict
        """

        current_state = self.is_activated()

        # 再生中なら一時停止
        if current_state:
            self.stop_process()

        # モデルを更新
        self.__set_targets(target, target_attr)
        self.__set_param_data(param_data)

    def update_from_node(self, node):
        """モデルを更新

        Args:
            target (str): ターゲットノード
            target_attr (list): アトリビュートリスト
            param_data (dict): パラメーターdict
        """

        current_state = self.is_activated()

        # 再生中なら一時停止
        if current_state:
            self.stop_process()

        # モデルを更新
        self.load_process_param(node)

    def validate_targets(self):
        """ターゲットのチェック

        Returns:
            bool: ターゲットとアトリビュートが適切かどうか
        """

        for attr in self.target_attrs():

            target = '{}.{}'.format(self.target(), attr)

            if not cmds.objExists(target):
                return False, 'ターゲットが存在しません: {}'.format(target)
            if not cmds.getAttr(target, se=True):
                return False, 'ターゲットにノードをコネクトできません: {}'.format(target)
            if cmds.keyframe(self.target(), attribute=attr, query=True, keyframeCount=True):
                return False, 'ターゲットにキーフレームが打たれています: {}'.format(target)

        return True, ''

    def validate_param_data(self):
        """パラメーターのチェック

        Returns:
            bool: パラメーターが適切かどうか
        """

        return True, ''

    def start_process(self):
        """プロセスの開始
        """

        result, msg = self.validate_targets()
        if not result:
            return False, msg

        result, msg = self.validate_param_data()
        if not result:
            return False, msg

        if self.is_activated():
            return True, 'already activated'

        self.pre_start_process()
        result, nodes = self.create_process()
        self.post_start_process()

        if nodes:
            self.__process_nodes = nodes

        if not result:
            self.stop_process()
            return False, 'プロセス作成中にエラーが発生しました'

        return True, 'success!'

    def pre_start_process(self):
        """プロセスの前処理
        """
        pass

    def post_start_process(self):
        """プロセス実行直後処理
        """
        pass

    def create_process(self):
        """プロセスを実行するノードを作成

        Returns:
            bool: 実行結果
            list: 作成されたノードリスト
        """

        # # 結果と作成されたノードリストを返す
        # return True, []
        msg = 'create_processがオーバーライドされていません'
        raise TpProcessModelError(msg)

    def stop_process(self):
        """プロセスの停止
        """

        self.__remove_process_nodes()
        self.__restore_org_value()
        self.post_stop_process()

    def __remove_process_nodes(self):
        """プロセス実行用のノードを削除
        """

        delete_targets = [x for x in self.__process_nodes if x and cmds.objExists(x)]

        if delete_targets:
            cmds.delete(delete_targets)

        self.__process_nodes = []

    def __restore_org_value(self):
        """スタート時に記録されていたアトリビュート値の復元
        """

        target = self.target()
        target_attrs = self.target_attrs()
        init_vals = self.init_vals()

        if not all([target, target_attrs, init_vals]):
            return

        for attr, val in zip(target_attrs, init_vals):

            if not cmds.objExists('{}.{}'.format(target, attr)):
                continue
            if not cmds.getAttr('{}.{}'.format(target, attr), se=True):
                continue
            cmds.setAttr('{}.{}'.format(target, attr), val)

    def post_stop_process(self):
        """プロセス終了時の処理
        """
        pass













