# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import sys
import re
import math

import maya.cmds as cmds

from . import neck_pos

reload(neck_pos)


# ===============================================
def get_neck_normal_list():
    """首の法線リストを取得

    :return: 頂点を選択した順の頂点法線リスト
    """

    select_vertex_list = cmds.ls(l=True, fl=True, os=True)
    if not select_vertex_list:
        return

    normal_list = []

    for select_vertex in select_vertex_list:

        this_normal_list = \
            cmds.polyNormalPerVertex(select_vertex, q=True, xyz=True)

        if not this_normal_list:
            continue

        if len(this_normal_list) < 3:
            continue

        this_normal = [0] * 3
        this_normal[0] = this_normal_list[0]
        this_normal[1] = this_normal_list[1]
        this_normal[2] = this_normal_list[2]

        normal_list.append(this_normal)

    return normal_list


# ===============================================
def get_neck_normal_list_string():
    """首の法線リストを変数含め文字列で取得

    :return: 頂点を選択した順の頂点法線リスト文字列
    """

    normal_list = get_neck_normal_list()
    if not normal_list:
        return

    result_string = ''

    result_string = 'self.neck_normal_list = [\n'

    for normal in normal_list:

        result_string += '    ' + str(normal) + ',\n'

    result_string += ']'

    return result_string


class NeckNormalInfo(object):

    def __init__(self):
        """コンストラクター
        """

        # region 定数

        self.set_name = 'NeckEdgeSet'
        self.mob_flag_str = 'mdl_chr0001'
        self.face_flag_str = '_face'
        self.head_joint_search_word = '*|Head'

        # 首の法線リスト（outlineも共通）
        # 下のself.vtx_pos_reference_listと対応したindexになっている
        self.normal_list = [
            [0.0, -0.9999899864196777, -0.004461305215954781],
            [0.4246300458908081, -0.9050871729850769, -0.0225040465593338],
            [-0.4246300458908081, -0.9050871729850769, -0.0225040465593338],
            [0.9384597539901733, -0.30013999342918396, 0.17090685665607452],
            [-0.9384597539901733, -0.30013999342918396, 0.17090685665607452],
            [0.9471073746681213, -0.07069253921508789, -0.313033789396286],
            [-0.9471073746681213, -0.07069253921508789, -0.313033789396286],
            [0.5902230143547058, -0.19881224632263184, -0.7823747992515564],
            [-0.5902230143547058, -0.19881224632263184, -0.7823747992515564],
            [0.0, -0.22410105168819427, -0.974565863609314],
        ]

        # headから見た各頂点への位置ベクトルの参照値.self.normal_listと対応したindexを持つ.
        # シーンの頂点がself.normal_listのどれに対応するか判定するために用いる.
        # 体型によってリストが若干異なるが最近傍頂点の判定には影響しないためdefaultのリストを使う.
        self.vtx_pos_reference_list = neck_pos.NeckPositionInfo().default_pos_from_head_list

        # endregion

        # region __init_param_by_file_nameで初期化されるメンバ

        self.neck_normal_list = []
        self.neck_ref_pos_list = []
        self.neck_edge_target_count = None

        self.is_mob = False
        self.is_mob_hair = False

        # endregion

        # region その他のメンバ

        self.neck_edge_list = None
        self.neck_vertex_info_list = None

        # endregion

    def __print_log(self, msg):
        """メッセージをプリントする

        Args:
            msg (str): メッセージ
        """

        # python3で文字化けしてしまうため分岐させる
        if sys.version_info.major == 2:
            log_msg = msg.encode('shift_jis')
            print(log_msg)
        else:
            print(msg)

    def __init_param_by_file_name(self):
        """シーン名からパラメーターを設定
        """

        scene_name = cmds.file(q=True, sn=True)

        if not scene_name:
            return

        # MOBは顔と髪でシーンが分かれているためリストをトリミングする
        if scene_name.find(self.mob_flag_str) >= 0:

            if scene_name.find(self.face_flag_str) >= 0:

                # 前半7つが顔に該当
                self.neck_normal_list = self.normal_list[:7]
                self.neck_ref_pos_list = self.vtx_pos_reference_list[:7]

            else:

                # 後半5つが髪に該当
                self.neck_normal_list = self.normal_list[5:]
                self.neck_ref_pos_list = self.vtx_pos_reference_list[5:]

                self.is_mob_hair = True

            self.neck_edge_target_count = len(self.neck_normal_list) - 1
            self.is_mob = True

        else:

            self.neck_normal_list = self.normal_list[:]
            self.neck_ref_pos_list = self.vtx_pos_reference_list[:]

            self.neck_edge_target_count = len(self.neck_normal_list)
            self.is_mob = False

    def exist_neck_edge_set(self):
        """ネックエッジセットの存在確認

        Returns:
            bool: ネックエッジセットがあるか
        """

        set_list = cmds.ls(type='objectSet')
        if self.set_name not in set_list:
            return False

        return True

    def add_neck_edge_set(self):
        """ネックエッジセットの追加
        選択エッジからネックエッジセットを作成し法線設定も行う
        """

        self.__init_param_by_file_name()

        neck_edge_list = cmds.ls((cmds.polyListComponentConversion(te=True)), l=True, fl=True)

        if not neck_edge_list:
            msg_str = '何も選択されていません'
            self.__print_log(msg_str)
            return

        if len(neck_edge_list) != self.neck_edge_target_count:

            msg_str = '選択された首の頂点数が規定数と違います 規定数 : {0} 選択数 : {1}'.format(
                str(self.neck_edge_target_count), str(len(neck_edge_list))
            )
            self.__print_log(msg_str)
            return

        if cmds.objExists(self.set_name):
            msg_str = '{0}が存在します'.format(self.set_name)
            self.__print_log(msg_str)
            return

        cmds.sets(name=self.set_name)
        cmds.sets(neck_edge_list, add=self.set_name)

        self.update_neck_edge_set()

    def update_neck_edge_set(self):
        """ネックエッジセットの更新
        """

        if not cmds.objExists(self.set_name):
            msg_str = '{0}が存在しません'.format(self.set_name)
            self.__print_log(msg_str)
            return

        neck_edge_list = cmds.ls(cmds.sets(self.set_name, q=True), l=True, fl=True)

        if not neck_edge_list:
            msg_str = '何も選択されていません'
            self.__print_log(msg_str)
            return

        target_transform_list = []

        for edge in neck_edge_list:

            target_transform_list.append(edge.split('.')[0])

        self.set_neck_normal_from_neck_edge_set(target_transform_list)

    def select_neck_edge_set(self):
        """ネックエッジを選択
        """

        if not cmds.objExists(self.set_name):
            msg_str = '{0}が存在しません'.format(self.set_name)
            self.__print_log(msg_str)
            return

        cmds.select(self.set_name, r=True)

    def remove_selected_edge_from_neck_edge_set(self):
        """選択しているエッジをネックエッジセットから除去
        """

        select_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_list:
            msg_str = '何も選択されていません'
            self.__print_log(msg_str)
            return

        edge_list = cmds.polyListComponentConversion(select_list, te=True)

        if not edge_list:
            msg_str = 'エッジが取得できません'
            self.__print_log(msg_str)
            return

        edge_list = cmds.ls(edge_list, l=True, fl=True)

        if not edge_list:
            return

        if not cmds.objExists(self.set_name):
            msg_str = '{0}が存在しません'.format(self.set_name)
            self.__print_log(msg_str)
            return

        cmds.sets(edge_list, rm=self.set_name)

    def remove_edge_from_neck_edge_set_by_name(self, target_name):
        """名前指定でエッジをネックエッジセットから除去

        Args:
            target_name (str): 除去するエッジ
        """

        if not target_name:
            return

        if not cmds.objExists(self.set_name):
            return

        edge_list_in_set = cmds.ls(cmds.sets('NeckEdgeSet', q=True), fl=True)

        remove_edge_list = []

        for edge in edge_list_in_set:
            if edge.find(target_name) >= 0:
                remove_edge_list.append(edge)

        if not remove_edge_list:
            return

        cmds.sets(remove_edge_list, rm=self.set_name)

    def delete_neck_edge_set(self):
        """ネックエッジセットを削除
        """

        if cmds.objExists(self.set_name):
            cmds.delete(self.set_name)

    def set_neck_normal_from_neck_edge_set(self, target_transform_list, name_prefix='', name_suffix=''):
        """ネックエッジセットの情報を元に首の法線を設定する

        Args:
            target_transform_list (list): 対象とするトランスフォームリスト
            name_prefix (str, optional): トランスフォームのプレフィックス. Defaults to ''.
            name_suffix (str, optional): トランスフォームのサフィックス. Defaults to ''.
        """

        self.neck_edge_list = self.create_target_edge_list(target_transform_list, name_prefix, name_suffix)

        if not self.neck_edge_list:
            return

        self.update_neck_vertex_info()

        if not self.neck_vertex_info_list:
            return

        self.set_vertex_normal()

    def update_neck_edge_list_from_selected_edge(self):
        """選択しているエッジからネックエッジセットを更新
        """

        self.__init_param_by_file_name()

        self.neck_edge_list = []

        this_neck_edge_list = cmds.ls(
            (cmds.polyListComponentConversion(te=True)), l=True, fl=True)

        if not this_neck_edge_list:
            msg_str = 'neck_edge_listが空です'
            self.__print_log(msg_str)
            return

        if len(this_neck_edge_list) != self.neck_edge_target_count:
            msg_str = '選択された首の頂点数が規定数と違います 規定数 : {0} 選択数 : {1}'.format(
                str(self.neck_edge_target_count), str(len(this_neck_edge_list))
            )
            self.__print_log(msg_str)
            return

        self.neck_edge_list = this_neck_edge_list

    def create_target_edge_list(self, target_transform_list, name_prefix='', name_suffix=''):
        """ターゲットとなるエッジのリストを生成する
        self.set_nameに含まれるエッジから特定のトランスフォーム名を持つもののリストをつくる

        Args:
            target_transform_list (list): 検索するトランスフォーム名
            name_prefix (str, optional): トランスフォームのプレフィックス. Defaults to ''.
            name_suffix (str, optional): トランスフォームのサフィックス. Defaults to ''.

        Returns:
            list: 該当トランスフォーム内のエッジリスト
        """

        self.__init_param_by_file_name()

        if not target_transform_list:
            msg_str = '対象のトランスフォームノードリストが空です'
            self.__print_log(msg_str)
            return []

        if not cmds.objExists(self.set_name):
            msg_str = '{0}が存在しません'.format(self.set_name)
            self.__print_log(msg_str)
            return []

        this_neck_edge_list = cmds.ls(cmds.sets(self.set_name, q=True), l=True, fl=True)

        if not this_neck_edge_list:
            msg_str = 'neck_edge_listが空です'
            self.__print_log(msg_str)
            return []

        target_neck_edge_list = []

        for this_neck_edge in this_neck_edge_list:

            # edgeであることを確認
            match_obj = re.search(r'.e\[\d*\]', this_neck_edge)
            if not match_obj:
                continue

            this_transform = this_neck_edge.split('.')[0]

            if this_transform.split('|')[-1] in [x.split('|')[-1] for x in target_transform_list]:

                replace_transform_name = name_prefix + this_transform.split('|')[-1] + name_suffix
                target_edge = this_neck_edge.replace(this_transform, replace_transform_name)

                if cmds.objExists(target_edge):
                    target_neck_edge_list.append(target_edge)

        if len(target_neck_edge_list) != self.neck_edge_target_count:
            return []

        return target_neck_edge_list

    def update_neck_vertex_info(self):
        """self.neck_vertex_info_listを更新する
        {'vtx': 頂点名, 'normal': 法線} の辞書が追加される
        """

        self.__init_param_by_file_name()

        self.neck_vertex_info_list = []

        if not self.neck_edge_list:
            return

        vertices = cmds.ls((cmds.polyListComponentConversion(self.neck_edge_list, tv=True)), l=True, fl=True)
        head_joints = cmds.ls(self.head_joint_search_word, type='joint', l=True, fl=True)

        if not head_joints or not vertices:
            return

        head_pos = cmds.xform(head_joints[0], q=True, t=True, ws=True)

        # self.vtx_pos_reference_listを用いてself.normal_listから対応する法線を探す
        for vtx in vertices:

            vtx_pos = cmds.xform(vtx, q=True, t=True, ws=True)
            vtx_from_head = [
                vtx_pos[0] - head_pos[0],
                vtx_pos[1] - head_pos[1],
                vtx_pos[2] - head_pos[2],
            ]

            min_suare_distance = -1
            min_index = -1

            for i, ref_pos in enumerate(self.vtx_pos_reference_list):

                x_distance = vtx_from_head[0] - ref_pos[0]
                y_distance = vtx_from_head[1] - ref_pos[1]
                z_distance = vtx_from_head[2] - ref_pos[2]
                square_distance = x_distance**2 + y_distance**2 + z_distance**2

                if min_suare_distance == -1 or square_distance < min_suare_distance:
                    min_suare_distance = square_distance
                    min_index = i

            self.neck_vertex_info_list.append({'vtx': vtx, 'normal': self.normal_list[min_index]})

    def set_vertex_normal(self):
        """法線をセットする
        """

        if not self.neck_vertex_info_list:
            return

        for info in self.neck_vertex_info_list:
            cmds.polyNormalPerVertex(info['vtx'], xyz=info['normal'])
