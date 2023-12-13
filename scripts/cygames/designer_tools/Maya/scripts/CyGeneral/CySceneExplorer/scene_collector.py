# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import json
import uuid

import maya.cmds as cmds

from . import utility
from . import const

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

reload(utility)
reload(const)


class SceneCollector(object):

    def __init__(self):

        self.collection_dict = {}
        self.json_path = ''

    def reset(self):

        self.__init__()

    def initialize(self, json_path=None):

        """
        self.collection_dictの構造は以下の通り

        self.collection_dict = {
            '(UUID)': {
                'Name': 'aaa',
                'UiOrder': 0,
                'Color': {'r': 128, 'g': 64, 'b': 64},
                'Items': {
                    '(UUID)': {
                        'Path': 'path/path/path_a0.ma',
                        'Desc': 'desc_a_0',
                        'UiOrder': 0,
                    },
                }
            },
            '(UUID)': {
                'Name': 'bbb',
                'UiOrder': 1,
                'Color': {'r': 64, 'g': 128, 'b': 64},
                'Items': {
                    '(UUID)': {
                        'Path': 'path/path/path_b0.ma',
                        'Desc': 'desc_b_0',
                        'UiOrder': 0,
                    },
                    '(UUID)': {
                        'Path': 'path/path/path_b1.ma',
                        'Desc': 'desc_b_1',
                        'UiOrder': 1,
                    },
                }
            },
        }
        """

        if json_path is None:
            self.reset()
            return True

        load_result = self.load_collection(json_path)

        if load_result:
            print('loaded: ' + json_path)
            return True
        else:
            cmds.confirmDialog(m='{}\nコレクションデータを読み取れませんでした'.format(json_path))
            self.reset()
            return False

    def get_collection_order(self, col_id):
        """コレクションのUIオーダーを取得
        """

        col = self.get_collection(col_id)
        if col:
            return col['UiOrder']

    def set_collection_order(self, col_id, order):
        """コレクションのUIオーダーを設定
        """

        col_ids = self.get_collection_ids_by_order()

        if col_id not in col_ids:
            return

        col = self.get_collection(col_id)
        col['UiOrder'] = order

        col_ids.remove(col_id)
        for id in col_ids:
            if self.get_collection_order(id) >= order:
                this_col = self.get_collection(id)
                this_col['UiOrder'] += 1

    def get_colletion_item_paths(self, col_ids):
        """コレクションからアイテムのパスを取得

        Args:
            col_ids (list): コレクションのIDリスト

        Returns:
            list: アイテムのパスリスト
        """

        item_ids = []

        for col_id in col_ids:
            this_item_ids = self.get_child_collection_item_ids(col_id)
            if this_item_ids:
                item_ids.extend(this_item_ids)

        return [self.get_collection_item_path(x) for x in item_ids]

    def get_collection_item_order(self, col_item_id):
        """コレクションアイテムのUIオーダーを取得
        """

        col_item = self.get_collection_item(col_item_id)
        if col_item:
            return col_item['UiOrder']

    def set_collection_item_order(self, col_item_id, order):
        """コレクションアイテムのUIオーダーを指定
        """

        col_item_ids = self.get_all_collection_item_ids_by_order()

        if col_item_id not in col_item_ids:
            return

        col_item = self.get_collection_item(col_item_id)
        col_item['UiOrder'] = order

        col_item_ids.remove(col_item_id)
        for id in col_item_ids:
            if self.get_collection_item_order(id) >= order:
                this_col = self.get_collection_item(id)
                this_col['UiOrder'] += 1

    def get_collection_ids_by_order(self):
        """全コレクションIDをオーダー順で取得
        """

        col_info_dicts = []

        for k, v in self.collection_dict.items():
            this_dict = {'Id': k, 'UiOrder': v['UiOrder']}
            col_info_dicts.append(this_dict)

        col_info_dicts.sort(key=lambda x: x['UiOrder'])
        return [x['Id'] for x in col_info_dicts]

    def get_sorted_collection_item_ids(self, col_ids):
        """コレクションアイテムIDリストをオーダー順に並び替え
        """

        return sorted(col_ids, key=lambda x: self.get_collection_item(x)['UiOrder'])

    def get_child_collection_item_ids(self, col_id):
        """指定したコレクションの子のコレクションアイテムIDリストを取得
        """

        col = self.get_collection(col_id)
        if col:
            return col['Items'].keys()

    def get_all_collection_item_ids_by_order(self):
        """全コレクションアイテムIDをオーダー順に取得
        """

        col_item_ids = []
        for col in self.collection_dict.values():
            col_item_ids.extend(col['Items'].keys())

        return sorted(col_item_ids, key=lambda x: self.get_collection_item_order(x))

    def optimize_collection_order(self):
        """コレクションのオーダーを最適化
        """

        ordered_ids = self.get_collection_ids_by_order()

        for i, id in enumerate(ordered_ids):
            self.set_collection_order(id, i)

    def optimize_collection_item_order(self):
        """コレクションアイテムのオーダーを最適化
        """

        ordered_ids = self.get_all_collection_item_ids_by_order()

        for i, id in enumerate(ordered_ids):
            self.set_collection_item_order(id, i)

    def direct_reorder_collection(self, col_ids, new_orders):
        """複数のコレクションのオーダー値を直指定
        オーダー値の重複や飛びが発生する可能性がある点に注意

        Args:
            col_ids (list): 操作するIDのリスト
            new_orders (list): 指定するオーダーのリスト
        """

        for id, order in zip(col_ids, new_orders):

            col_dict = self.get_collection(id)

            if col_dict:
                col_dict['UiOrder'] = order

    def direct_reorder_collection_item(self, col_item_ids, new_orders):
        """複数のコレクションアイテムのオーダー値を直指定
        オーダー値の重複や飛びが発生する可能性がある点に注意

        Args:
            col_ids (list): 操作するIDのリスト
            new_orders (list): 指定するオーダーのリスト
        """

        for id, order in zip(col_item_ids, new_orders):

            col_dict = self.get_collection_item(id)

            if col_dict:
                col_dict['UiOrder'] = order

    def get_collection_name(self, col_id):
        """コレクション名を取得

        Args:
            col_id (str): コレクションのID

        Returns:
            str: コレクション名
        """

        col = self.get_collection(col_id)

        if col:
            return col['Name']

    def set_collection_name(self, col_id, name):
        """コレクション名を設定

        Args:
            col_id (str): コレクションのID
            name (str): コレクション名
        """

        col = self.get_collection(col_id)

        if col:
            col['Name'] = name

    def set_collection_color(self, col_id, rgb):
        """コレクションのカラーを設定

        Args:
            col_id (str): コレクションのID
            rgb (list): カラー
        """

        col = self.get_collection(col_id)

        if col:
            col['Color'] = {'r': rgb[0], 'g': rgb[1], 'b': rgb[2]}

    def get_collection_item_path(self, col_item_id):
        """コレクションアイテムのパスを取得

        Args:
            col_item_id (str): コレクションアイテムのID

        Returns:
            str: アイテムのパス
        """

        col_item = self.get_collection_item(col_item_id)

        if col_item:
            return col_item['Path']

    def get_collection_item_desc(self, col_item_id):
        """コレクションアイテムの説明を取得

        Args:
            col_item_id (str): コレクションアイテムのID

        Returns:
            str: アイテムの説明
        """

        col_item = self.get_collection_item(col_item_id)

        if col_item:
            return col_item['Desc']

    def set_collection_item_desc(self, col_item_id, desc):
        """コレクションアイテムの説明をセット

        Args:
            col_item_id (str): コレクションアイテムのID
            desc (str): アイテムの説明
        """

        col_item = self.get_collection_item(col_item_id)

        if col_item:
            col_item['Desc'] = desc

    def get_collections(self):
        """全コレクションdictを取得

        Returns:
            [dict]: 全コレクションdictのリスト
        """

        if not self.collection_dict:
            return []
        else:
            return self.collection_dict.values()

    def get_collection(self, col_id):
        """コレクションのdictを取得

        Args:
            col_id (str): コレクションのID

        Returns:
            dict: コレクションのdict
        """

        if not self.collection_dict:
            return

        return self.collection_dict.get(col_id)

    def get_collection_item(self, item_id):
        """コレクションアイテムのdictを取得

        Args:
            item_id (str): コレクションアイテムのID

        Returns:
            dict: コレクションアイテムのdict
        """

        for col_dict in self.collection_dict.values():
            item_dict = col_dict['Items']
            item = item_dict.get(item_id)
            if item:
                return item

    def get_parent_collection(self, item_id):
        """コレクションアイテムから親のコレクションを取得

        Args:
            item_id (str): コレクションアイテムのID

        Returns:
            str, dict: 親コレクションのIDとdict
        """

        for id, col_dict in self.collection_dict.items():
            item_dict = col_dict['Items']
            item = item_dict.get(item_id)
            if item:
                return id, col_dict

    def add_collection(self, name):
        """コレクションの追加

        Args:
            name (str): 追加するコレクション名

        Returns:
            str: 追加したコレクションのUUID
        """

        new_collection_dict = {
            'Name': name,
            'UiOrder': 0,
            'Color': {'r': 64, 'g': 64, 'b': 64},
            'Items': {}
        }

        this_id = uuid.uuid4()
        all_orders = self.get_collection_ids_by_order()
        new_collection_dict['UiOrder'] = len(all_orders)
        self.collection_dict[str(this_id)] = new_collection_dict
        return str(this_id)

    def del_collection(self, del_col_id):
        """コレクションの削除

        Args:
            del_col_id (str): コレクションのID
        """

        self.collection_dict.pop(del_col_id, None)

    def add_collection_item(self, col_id, paths):
        """コレクションアイテムの追加

        Args:
            col_id (str): 追加するコレクションのID
            paths (list): 追加するパスリスト

        Returns:
            str: 追加したコレクションアイテムのUUID
        """

        col_dict = self.collection_dict.get(col_id)

        if not col_dict:
            return

        results = []
        for path in paths:

            # 同じパスのアイテムがあったらスキップ
            if self.has_same_item(col_id, path):
                continue

            new_item_dict = {
                'Path': path,
                'Desc': '説明を追加',
                'UiOrder': 0,
            }

            this_id = uuid.uuid4()
            all_orders = self.get_all_collection_item_ids_by_order()
            new_item_dict['UiOrder'] = len(all_orders)
            col_dict['Items'][str(this_id)] = new_item_dict
            results.append(str(this_id))

        return results

    def del_collection_item(self, col_item_id):
        """コレクションアイテムの削除

        Args:
            col_item_id (str): コレクションアイテムのUUID
        """

        col_id, dict = self.get_parent_collection(col_item_id)
        col_dict = self.collection_dict.get(col_id)

        if not col_dict:
            return

        col_dict['Items'].pop(col_item_id, None)

    def has_same_item(self, col_id, path):
        """コレクション内に該当のパスを持つアイテムがあるか

        Args:
            col_id (str): コレクションのID
            path (str): パス

        Returns:
            bool: コレクション内に該当のパスを持つアイテムがあるか
        """

        col_dict = self.collection_dict.get(col_id)

        if not col_dict:
            return False

        for item in col_dict['Items'].values():
            if item['Path'] == path:
                return True
        return False

    def save_collection(self, path=None):
        """コレクションを保存
        パスが指定されなければself.json_pathに保存

        Args:
            path (str, optional): 保存パス. Defaults to None.
        """

        if path:
            self.json_path = path
        if not self.json_path:
            return

        # UIオーダーの重複や飛びを解消
        self.optimize_collection_order()
        self.optimize_collection_item_order()

        save_dict = {
            'Label': const.TOOL_COLLECTION_LABEL,
            'Version': const.TOOL_COLLECTION_VERSION,
            'Data': self.collection_dict
        }

        try:
            with open(self.json_path, 'w') as file:
                json.dump(save_dict, file)
        except Exception:
            cmds.confirmDialog(m='{}\n保存に失敗しました\nファイルが書き込み可能な状態か確認してください'.format(self.json_path))

    def load_collection(self, json_path):
        """コレクションをロード

        Args:
            json_path (str): jsonパス

        Returns:
            bool: ロードできたか
        """

        if not json_path:
            return False
        load_dict = None

        # TOOLのjsonか判定
        if os.path.exists(json_path):
            try:
                with open(json_path) as file:
                    load_dict = json.load(file)
            except Exception:
                pass

        if not load_dict:
            cmds.warning('cannot load collection json')
            return False

        tool_label = load_dict.get('Label')
        tool_version = load_dict.get('Version')

        if tool_label != const.TOOL_COLLECTION_LABEL or not tool_version:
            cmds.warning('invalid json')
            return False

        if tool_version < const.TOOL_MIN_VALID_COLLECTION_VERSION:
            cmds.warning('invalid json version')
            return False

        self.collection_dict = load_dict.get('Data')
        self.json_path = json_path
        return True
