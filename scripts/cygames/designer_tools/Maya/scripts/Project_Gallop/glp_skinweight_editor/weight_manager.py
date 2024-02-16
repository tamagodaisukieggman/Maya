# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

import functools
import json
import math
import collections

import maya.api.OpenMaya as om
import maya.cmds as cmds

import Project_Gallop.base_common.classes.vertex as vertex
from . import joint, skincluster_data, utility
reload(vertex)
reload(joint)
reload(skincluster_data)
reload(utility)


# TODO: 将来的にUIから設定できるようにする
# (マッチするパターン, リプレース先文字列)
MIRROR_MATCH_PATTERN_LIST = [
    (r'_R$', '_L'), (r'_L$', '_R'),
    (r'_r$', '_l'), (r'_l$', '_r'),
    ('_R_', '_L_'), ('_L_', '_R_'),
    ('_r_', '_l_'), ('_l_', '_r_'),
    ('_FR_', '_FL_'), ('_FL_', '_FR_'),
    ('_FRR_', '_FLL_'), ('_FLL_', '_FRR_'),
    ('_FFR_', '_FFL_'), ('_FFL_', '_FFR_'),
    ('_BR_', '_BL_'), ('_BL_', '_BR_'),
    ('_BRR_', '_BLL_'), ('_BLL_', '_BRR_'),
    ('_BBR_', '_BBL_'), ('_BBL_', '_BBR_'),
]


class WeightManager(object):
    """ウェイト情報を扱うクラスです
    """

    def __init__(self):

        # コピー元作成時に使用
        self.src_vtxdatas = []
        self.src_skinweight_dict = {}

        # コピー実行時に使用
        self.dest_vtxdatas = []
        self.dest_skinweight_dict = {}
        self.remap_active = False
        self.remaped_joint = []

        self.om_pos_mode = om.MSpace.kWorld
        self.paste_distance = 5.0

        self.custom_post_process = None

    def src_data_initialize(self):
        """コピー元に関するデータの初期化する
        """
        self.src_vtxdatas = []
        self.src_skinweight_dict = {}

    def dest_data_initialize(self):
        """ペースト先に関するデータの初期化する
        """
        self.dest_vtxdatas = []
        self.dest_skinweight_dict = {}
        self.remap_active = False
        self.remaped_joint = []

    def create_info(self, for_distanation=False):
        """データの作成を行います

        Args:
            for_distanation (bool, optional): 作成するデータはペースト先のものか. Defaults to False.

        return:
            bool: 作成に成功したか
        """
        vtx_list = utility.get_selected_vertex_list()
        if not vtx_list:
            om.MGlobal.displayWarning('対象の頂点を取得できません')
            return False

        # 初期化処理
        if not for_distanation:
            self.src_data_initialize()
        else:
            self.dest_data_initialize()

        if for_distanation:
            self.dest_vtxdatas = vertex.get_vtx_datas(vtx_list, om_pos_space=self.om_pos_mode)
            transforms = utility.get_transform_from_vertexes(vtx_list)

            for transform in transforms:
                mfn_skincluster = utility.get_mfn_skin_clusters_by_transform(transform)
                if not mfn_skincluster:
                    om.MGlobal.displayWarning('{0}にはスキンクラスターがありません'.format(transform))
                    continue

                self.dest_skinweight_dict[transform] = skincluster_data.get_skinweight_data(mfn_skincluster, transform, self.om_pos_mode)
        else:
            self.src_vtxdatas = vertex.get_vtx_datas(vtx_list, om_pos_space=self.om_pos_mode)
            transforms = utility.get_transform_from_vertexes(vtx_list)

            for transform in transforms:
                mfn_skincluster = utility.get_mfn_skin_clusters_by_transform(transform)
                if not mfn_skincluster:
                    om.MGlobal.displayWarning('{0}にはスキンクラスターがありません'.format(transform))
                    continue

                self.src_skinweight_dict[transform] = skincluster_data.get_skinweight_data(mfn_skincluster, transform, self.om_pos_mode)

        if not for_distanation:
            om.MGlobal.displayInfo('コピー元情報取得完了')
        else:
            om.MGlobal.displayInfo('コピー先情報取得完了')

        return True

    def paste_weight_wrapper(f):
        """Paste工程の前後処理のためのwrapper

        src, destがそれぞれセットされているかの確認と、関数実行後の処理を追加するwrapper

        Args:
            f (function): 実際のペースト処理を行う関数

        Returns:
            function: wrapされた関数
        """
        @functools.wraps(f)
        def status_validation(*args, **kwargs):
            # 必要情報が含まれているか確認して、もし足りないなら実行させない
            if not args[0].src_vtxdatas or not args[0].src_skinweight_dict:
                om.MGlobal.displayWarning('コピー元の情報がありません')
                return

            if not args[0].dest_vtxdatas or not args[0].dest_skinweight_dict:
                om.MGlobal.displayWarning('ペースト先の情報がありません')
                return

            paste_func = f(*args, **kwargs)

            # 事後処理
            # スキンウェイトを更新してもdest_vtxdataなどは古いままになっているので、誤って使わないよう明示的に破棄する
            args[0].dest_data_initialize()

            # カスタム追加のポストプロセス
            if args[0].custom_post_process:
                args[0].custom_post_process()
                args[0].custom_post_process = None

            return paste_func

        return status_validation

    @paste_weight_wrapper
    def paste_weight_by_order(self):
        """選択順でウェイトのペーストを行う
        """
        if len(self.dest_vtxdatas) > len(self.src_vtxdatas):
            om.MGlobal.displayWarning('ペースト先の頂点数がコピー元の頂点数より多くなっています')
            return

        update_weight_dict = self.create_update_weight_dict(self.src_vtxdatas, self.dest_vtxdatas)
        self.apply_to_skincluster(update_weight_dict)

    @paste_weight_wrapper
    def paste_weight_by_index(self):
        """index順に応じて、ウェイトのペーストを行う
        """

        update_weight_dict = {}
        # トランスフォームごとに情報を作成する
        for dest_transform in self.dest_skinweight_dict.keys():

            this_dest_vtxdatas = []
            this_src_vtxdatas = []

            dest_transform_sn = utility.get_namespace_removed_shortname(dest_transform)
            for src_transform in self.src_skinweight_dict.keys():
                if dest_transform_sn == utility.get_namespace_removed_shortname(src_transform):
                    this_src_vtxdatas = vertex.get_transform_matched_vtx_datas(src_transform, self.src_vtxdatas)
                    break

            # src側が名前でマッチできなかった場合、とりあえずすべてのVtxDataを入れておく
            if not this_src_vtxdatas:
                this_src_vtxdatas = self.src_vtxdatas

            this_dest_vtxdatas = vertex.get_transform_matched_vtx_datas(dest_transform, self.dest_vtxdatas)

            matched_src_vtxdatas = vertex.get_index_match_vtx_datas(this_dest_vtxdatas, this_src_vtxdatas)

            update_weight_dict.update(self.create_update_weight_dict(matched_src_vtxdatas, this_dest_vtxdatas))

        self.apply_to_skincluster(update_weight_dict)

    @paste_weight_wrapper
    def paste_weight_by_position(self):
        """位置情報をもとに、ウェイトのペーストを行う
        """

        # ほぼ同一頂点となっている状況で、weightに別の値が入っているケースは考えにくいためshould_check_face_normalは利用しない（副産物として、書き出し時にface_vtxの書き出しも不要にできる）
        sorted_src_vtxdatas = vertex.get_nearest_pos_vtx_datas(self.dest_vtxdatas, self.src_vtxdatas, False)
        update_weight_dict = self.create_update_weight_dict(sorted_src_vtxdatas, self.dest_vtxdatas, check_distance=True)

        self.apply_to_skincluster(update_weight_dict)

    @paste_weight_wrapper
    def paste_weight_by_uv_position(self):
        """UV位置情報をもとにウェイトのペーストを行う
        """
        sorted_src_vtxdatas = vertex.get_nearest_uv_pos_vtx_datas(self.dest_vtxdatas, self.src_vtxdatas, tolerance=self.paste_distance)
        update_weight_dict = self.create_update_weight_dict(sorted_src_vtxdatas, self.dest_vtxdatas)
        self.apply_to_skincluster(update_weight_dict)

    @paste_weight_wrapper
    def mirror_paste_weight(self, mirror_x, mirror_y, mirror_z):
        """ミラーしたうえで、位置をもとにウェイトのペーストを行う

        Args:
            mirror_x (bool): x軸を反転するか
            mirror_y (bool): y軸を反転するか
            mirror_z (bool): z軸を反転するか
        """

        # paste側のデータのポジションを反転させて、対応する頂点を取得する
        mirror_coffient = [1, 1, 1]
        reversed_dest_vtxdatas = []
        for dest_vtxdata in self.dest_vtxdatas:
            reversed_vtxdata = dest_vtxdata
            if mirror_x:
                reversed_vtxdata.position.x *= -1
                mirror_coffient[0] = -1
            if mirror_y:
                reversed_vtxdata.position.y *= -1
                mirror_coffient[1] = -1
            if mirror_z:
                reversed_vtxdata.position.z *= -1
                mirror_coffient[2] = -1

            reversed_dest_vtxdatas.append(reversed_vtxdata)

        # positionでマッチ
        # ほぼ同一頂点となっている状況で、weightに別の値が入っているケースは考えにくいためshould_check_face_normalは利用しない（書き出し時にface_vtxの書き出しも不要にできる）
        sorted_src_vtxdatas = vertex.get_nearest_pos_vtx_datas(reversed_dest_vtxdatas, self.src_vtxdatas, should_check_face_normal=False)

        # ミラーのアップデート用の情報作成をしておく
        mirror_settings = {'coffient': mirror_coffient, 'mirror_pattern': MIRROR_MATCH_PATTERN_LIST, 'allow_distance': self.paste_distance}
        update_weight_dict = self.create_update_weight_dict(sorted_src_vtxdatas, reversed_dest_vtxdatas, mirror_settings, check_distance=True)

        self.apply_to_skincluster(update_weight_dict)

    def create_update_weight_dict(self, sorted_src_vtxdatas, dest_vtxdatas, mirror_settings=None, check_distance=False):
        """スキンウェイトの値を更新するためのデータセットを作成する

        Args:
            sorted_src_vtxdatas (list[vertex.VtxData]): dest側とペアになるようにソートされたコピー元のVtxDataのlist
            dest_vtxdatas (list[vertex.VtxData]): スキンウェイトを変更したい頂点のVtxDataのlist
            mirror_settings (dict, optional): ミラーリングを行う場合に利用する設定のdict. Defaults to None.

        Returns:
            dict: スキンウェイトの値の更新に利用するdict
        """
        INF_IDX = 0
        WEIGHT_IDX = 1
        TARGET_VTX_IDX = 2
        update_weight_dict = {}
        for i, dest_vtxdata in enumerate(dest_vtxdatas):
            dest_transform = dest_vtxdata.transform
            dest_skincluster_data = self.dest_skinweight_dict[dest_transform]

            src_vtxdata = sorted_src_vtxdatas[i]
            if not src_vtxdata:
                print('{0}のペアが見つかりません'.format(dest_vtxdata.get_name()))
                continue

            src_transform = src_vtxdata.transform
            src_skincluster_data = self.src_skinweight_dict[src_transform]

            # 距離オーバーなら飛ばす
            if check_distance and src_vtxdata.position.distanceTo(dest_vtxdata.position) > self.paste_distance:
                print('距離オーバー: コピー元{0}.vtx[{1}] -> コピー先{2}.vtx[{3}]'.format(src_vtxdata.transform, src_vtxdata.index, dest_vtxdata.transform, dest_vtxdata.index))
                continue

            # influenceのindexのリストができていない場合はここで作成
            if dest_transform not in update_weight_dict.keys():
                update_weight_dict[dest_transform] = [[], [], []]

                if mirror_settings:
                    update_weight_dict[dest_transform][INF_IDX] = dest_skincluster_data.create_mirror_influence_map(src_skincluster_data.jointdatas, mirror_settings)
                else:
                    update_weight_dict[dest_transform][INF_IDX] = dest_skincluster_data.create_influence_map(src_skincluster_data.jointdatas)

                invalid_idx_indices = [i for i, x in enumerate(update_weight_dict[dest_transform][INF_IDX]) if x == -1]  # -1は無効なインデックス
                if invalid_idx_indices:
                    for i in invalid_idx_indices:
                        cmds.warning('{} に対応するインフルエンスが見つかりませんでした.このインフルエンスに対する操作はスキップされます.'.format(src_skincluster_data.jointdatas[i].name))

            # ウェイトデータ登録
            update_weight_dict[dest_transform][WEIGHT_IDX].extend(src_skincluster_data.get_weights(src_vtxdata.index))
            update_weight_dict[dest_transform][TARGET_VTX_IDX].append(dest_vtxdata.index)

        # joint remapが必要な場合にはremap実行
        if self.remap_active:
            update_weight_dict = self.update_weight_dict_joint_remap(update_weight_dict, self.remaped_joint)

        return update_weight_dict

    def update_weight_dict_joint_remap(self, src_weight_dict, remap_list):
        """update_weight_dictのジョイントをリマップする

        Args:
            src_weight_dict (dict): もととなるupdate_weight_dict
            remap_list (list)): 各々のinfluenceをどのようにremapするかを指定するlist

        Returns:
            dict: リマップされたupdate_weight_dict
        """
        INF_IDX = 0
        WEIGHT_IDX = 1
        TARGET_VTX_IDX = 2
        remaped_weight_dict = {}

        # remapでは重複が発生しうるのでそれに応じてリストを調整する
        unique_remap_list = []
        for i in remap_list:
            if i not in unique_remap_list:
                unique_remap_list.append(i)

        for transform in src_weight_dict.keys():
            remap_unique_count = len(unique_remap_list)
            inf_count = len(src_weight_dict[transform][INF_IDX])
            vtx_count = len(src_weight_dict[transform][TARGET_VTX_IDX])

            src_weights = src_weight_dict[transform][WEIGHT_IDX]
            remaped_weights = [0] * (remap_unique_count * vtx_count)

            # influenceのindexのリストができていない場合はここで作成
            if transform not in remaped_weight_dict.keys():
                remaped_weight_dict[transform] = [[], [], []]

            # remap listはinf_countと必ず一致しなければいけない
            if len(remap_list) != inf_count:
                om.MGlobal.displayWarning('Remap元とインフルエンスの個数は一致する必要があります')

                # remap不能の場合はとりあえずremap前の値を入れておく
                remaped_weight_dict[transform][INF_IDX] = src_weight_dict[transform][INF_IDX]
                remaped_weight_dict[transform][WEIGHT_IDX] = src_weight_dict[transform][WEIGHT_IDX]
                remaped_weight_dict[transform][TARGET_VTX_IDX] = src_weight_dict[transform][TARGET_VTX_IDX]
                continue

            for vtx_idx in range(vtx_count):
                for inf_idx in range(inf_count):
                    # それぞれのindexを指定
                    src_weights_idx = vtx_idx * inf_count + inf_idx
                    remaped_weights_idx = vtx_idx * remap_unique_count + unique_remap_list.index(remap_list[inf_idx])

                    remaped_weights[remaped_weights_idx] += src_weights[src_weights_idx]

            remaped_weight_dict[transform][INF_IDX] = unique_remap_list
            remaped_weight_dict[transform][WEIGHT_IDX] = remaped_weights
            remaped_weight_dict[transform][TARGET_VTX_IDX] = src_weight_dict[transform][TARGET_VTX_IDX]

        return remaped_weight_dict

    def apply_to_skincluster(self, update_dict):
        """スキンクラスターにデータを適用する

        Args:
            update_dict (dict): create_update_weight_dictなどで作成する、更新するためのデータが格納されたdict
        """
        INF_IDX = 0
        WEIGHT_IDX = 1
        TARGET_VTX_IDX = 2
        for transform in update_dict.keys():
            sorted_weights, sorted_comps, filtered_inf = self.__coordinate_data(update_dict[transform][WEIGHT_IDX], update_dict[transform][TARGET_VTX_IDX], update_dict[transform][INF_IDX])
            if not all([sorted_weights, sorted_comps, filtered_inf]):
                continue  # インフルエンスが見つからない場合など空でかえってくることがある
            weights = om.MDoubleArray(sorted_weights)
            influence_idxs = om.MIntArray(filtered_inf)
            id_comp = om.MFnSingleIndexedComponent()
            vertex_comp = id_comp.create(om.MFn.kMeshVertComponent)
            id_comp.addElements(sorted_comps)

            sel = om.MSelectionList()
            sel.add(transform)
            geo_dag_path = sel.getDagPath(0)

            mfn_skincluster = utility.get_mfn_skin_clusters_by_transform(transform)
            mfn_skincluster.setWeights(geo_dag_path, vertex_comp, influence_idxs, weights, True)

        om.MGlobal.displayInfo('スキンウェイトの反映を完了しました')
        cmds.headsUpMessage('スキンウェイトの反映を完了しました', time=5.0)

    def round_weight(self, fraction_digits):
        """weightの丸めを実行する

        Args:
            fraction_digits (int): 小数点以下何桁で丸めを実行するか
        """
        # もととなる情報を作成
        status = self.create_info()
        if not status:
            return
        self.dest_data_initialize()
        self.dest_skinweight_dict = self.src_skinweight_dict
        self.dest_vtxdatas = self.src_vtxdatas

        for vtxdata in self.src_vtxdatas:
            current_skinweight = self.src_skinweight_dict[vtxdata.transform]
            current_index = vtxdata.index

            current_weights = current_skinweight.get_weights(current_index)
            indexed_weights = list(enumerate(current_weights))

            # 降順にソートする(同値の場合、indexが若いほうが先)
            sorted_indexed_weights = sorted(indexed_weights, key=lambda x: (x[1], x[0]), reverse=True)

            sorted_weights = [x[1] for x in sorted_indexed_weights]
            sorted_indexes = [x[0] for x in sorted_indexed_weights]

            for idx, weight in enumerate(sorted_weights):
                sorted_weights[idx] = round(weight, fraction_digits)

            sorted_weights = self.normarize(sorted_weights, 0)
            current_skinweight.set_weights(current_index, zip(sorted_indexes, sorted_weights))

        update_weight_dict = self.create_update_weight_dict(self.src_vtxdatas, self.dest_vtxdatas)
        self.apply_to_skincluster(update_weight_dict)
        self.src_data_initialize()
        self.dest_data_initialize()

    def check_round_weight(self, fraction_digits):
        """指定の桁数内で丸められているか確認する

        Args:
            fraction_digits (int): 小数何桁で丸められているか
        """
        status = self.create_info()
        if not status:
            return

        errors = []
        for vtxdata in self.src_vtxdatas:
            current_skinweight = self.src_skinweight_dict[vtxdata.transform]
            current_index = vtxdata.index

            current_weights = current_skinweight.get_weights(current_index)
            if any(not self.is_rounded(widget, fraction_digits) for widget in current_weights):
                errors.append(vtxdata.get_name())

        if errors:
            cmds.selectMode(component=True)
            cmds.selectType(vertex=True)
            cmds.select(errors)
            om.MGlobal.displayInfo('チェック完了: エラーの頂点を選択しました')
            cmds.headsUpMessage('チェック完了: エラーの頂点を選択しました')
        else:
            om.MGlobal.displayInfo('チェック完了: エラーなし')
            cmds.headsUpMessage('チェック完了: エラーなし')

        self.src_data_initialize()

    def set_max_influence(self, max_influence):
        """最大値の入っているインフルエンス数が収まるようにweightを調整する

        Args:
            max_influence (int): 値の入っているインフルエンス数の上限
        """
        status = self.create_info()
        if not status:
            return
        self.dest_data_initialize()
        self.dest_skinweight_dict = self.src_skinweight_dict
        self.dest_vtxdatas = self.src_vtxdatas

        for vtxdata in self.src_vtxdatas:
            current_skinweight = self.src_skinweight_dict[vtxdata.transform]
            current_index = vtxdata.index

            current_weights = current_skinweight.get_weights(current_index)
            indexed_weights = list(enumerate(current_weights))

            # 降順にソートする(同値の場合、indexが若いほうが先)
            sorted_indexed_weights = sorted(indexed_weights, key=lambda x: (x[1], x[0]), reverse=True)

            sorted_weights = [x[1] for x in sorted_indexed_weights]
            sorted_indexes = [x[0] for x in sorted_indexed_weights]
            for idx, weight in enumerate(sorted_weights):
                if idx < max_influence:
                    sorted_weights[idx] = weight
                else:
                    sorted_weights[idx] = 0.0

            sorted_weights = self.normarize(sorted_weights, 1)
            current_skinweight.set_weights(current_index, zip(sorted_indexes, sorted_weights))

        update_weight_dict = self.create_update_weight_dict(self.src_vtxdatas, self.dest_vtxdatas)
        self.apply_to_skincluster(update_weight_dict)
        self.src_data_initialize()
        self.dest_data_initialize()
        self.src_data_initialize()

    def check_max_influence(self, max_influence):
        """インフルエンス数が基底数以内かチェックして、問題個所を選択する

        Args:
            max_influence (int): 値の入っているインフルエンス数の上限
        """
        status = self.create_info()
        if not status:
            return

        errors = []
        for vtxdata in self.src_vtxdatas:
            current_skinweight = self.src_skinweight_dict[vtxdata.transform]
            current_index = vtxdata.index

            current_weights = current_skinweight.get_weights(current_index)
            if self.get_influence_count(current_weights) > max_influence:
                errors.append(vtxdata.get_name())

        if errors:
            cmds.selectMode(component=True)
            cmds.selectType(vertex=True)
            cmds.select(errors)
            om.MGlobal.displayInfo('チェック完了: エラーの頂点を選択しました')
            cmds.headsUpMessage('チェック完了: エラーの頂点を選択しました')
        else:
            om.MGlobal.displayInfo('チェック完了: エラーなし')
            cmds.headsUpMessage('チェック完了: エラーなし')

        self.src_data_initialize()

    def get_influence_count(self, weights):
        """値の入っているインフルエンス数を取得する

        Args:
            weights (list(float)): weightのリスト

        Returns:
            int: 値の入っているインフルエンス数
        """
        count = 0
        for weight in weights:
            if weight != 0.0:
                count += 1
        return count

    def is_rounded(self, value, fraction_digits, tolerance_digit=2):
        """特定の桁数内でまとめられているか

        Args:
            value (float): 検証したい値
            fraction_digits (int): 小数何桁で丸められているか
            tolerance_digit (int, optional): 許容誤差の桁数. Defaults to 2.

        Returns:
            bool: 特定の桁内で丸められているか
        """
        value = value * pow(10, fraction_digits)
        temp_val = math.modf(value)

        tolerance = pow(10, -tolerance_digit)
        if temp_val[0] < tolerance or temp_val[0] > 1 - tolerance:
            return True

        return False

    def normarize(self, weights, mode):
        """ウェイトの合計が1になるように調整する

        Args:
            weights (list(float)): 正規化を行いたい1頂点のウェイトのリスト
            mode (int): 1の場合は丸め誤差で生じた差分を一番大きいウェイトを調整して相殺するモード、2の場合は差分を現在有効なウェイトが振られているものの中で等分して処理する方式

        Returns:
            list(float): weightの合計値が1になるように正規化されたlist
        """
        valid_weight_count = 0
        weights_sum = 0.0
        for weight in weights:
            weights_sum += weight
            if weight != 0.0:
                valid_weight_count += 1

        diff = weights_sum - 1.0
        if diff == 0:
            return weights

        # 差分スイープ方式
        if mode == 0:
            weights[0] -= diff

        # 均等割り当て方式
        elif mode == 1:
            print(valid_weight_count)
            part_diff = diff / valid_weight_count
            print(part_diff)
            for idx, weight in enumerate(weights):
                if idx >= valid_weight_count:
                    break
                weight -= part_diff
                weights[idx] = weight

        return weights

    def export_as_json(self, export_path):
        """json形式でweightをエクスポート

        Args:
            export_path (str): 出力先パス
        """
        converted_dict = {}
        converted_dict['data_type'] = 'GlpWeightEditorData'
        converted_dict['pos_mode'] = self.om_pos_mode

        converted_dict['skin_weight_data_list'] = []
        for transform in self.src_skinweight_dict.keys():
            skinweight_dict = {}
            skinweight_dict['transform'] = transform
            # MDoubleのままでは保存できない
            # 加えて長いリストは保存時時間がかかるため文字列書き出し
            skinweight_dict['weights'] = ','.join(str(weight) for weight in self.src_skinweight_dict[transform].weights)
            skinweight_dict['joints'] = []

            for joint_data in self.src_skinweight_dict[transform].jointdatas:
                joint_dict = {}
                joint_dict['name'] = joint_data.name
                joint_dict['full_path'] = joint_data.full_path
                joint_dict['vector_from_root'] = [joint_data.vector_from_root.x, joint_data.vector_from_root.y, joint_data.vector_from_root.z]
                skinweight_dict['joints'].append(joint_dict)

            converted_dict['skin_weight_data_list'].append(skinweight_dict)

        converted_dict['VtxDataList'] = []
        for vtxdata in self.src_vtxdatas:
            vtx_dict = {}
            attr_value = {
                'transform': vtxdata.transform,
                'position': [vtxdata.position.x, vtxdata.position.y, vtxdata.position.z, vtxdata.position.w],
                'index': vtxdata.index,
                'uv_position': vtxdata.face_vtx_datas[0].uv_pos
            }
            for attr in attr_value.keys():
                vtx_dict[attr] = attr_value[attr]

            converted_dict['VtxDataList'].append(vtx_dict)

        with open(export_path, 'w') as f:
            json.dump(converted_dict, f, indent=4)

    def import_from_json(self, export_path):
        """json形式でweight infoをインポート

        Args:
            export_path (str): jsonの取り込みパス
        """
        with open(export_path) as f:
            imported_dict = json.load(f)

        if 'data_type' not in imported_dict.keys() or imported_dict['data_type'] != 'GlpWeightEditorData':
            om.MGlobal.displayWarning('このファイルはGlpWeightEditorのデータではありません。処理を中止します')
            return

        not_have_uv_pos = False

        self.src_data_initialize()
        self.om_pos_mode = imported_dict['pos_mode']

        skin_weight_dict = {}
        for skin_weight_data in imported_dict['skin_weight_data_list']:
            transform = skin_weight_data['transform']
            weights = utility.convert_str_to_float_list(skin_weight_data['weights'])
            jointdatas = []
            for jnt in skin_weight_data['joints']:
                jointdata = joint.JointData()
                jointdata.name = jnt['name']
                jointdata.full_path = jnt['full_path']
                jointdata.vector_from_root = om.MVector(jnt['vector_from_root'])
                jointdatas.append(jointdata)

            skin_weight_dict[transform] = skincluster_data.SkinClusterData()
            skin_weight_dict[transform].jointdatas = jointdatas
            skin_weight_dict[transform].weights = weights

        vtxdatas = []
        for vtx in imported_dict['VtxDataList']:
            vtxdata = vertex.VtxData()
            vtxdata.transform = vtx['transform']
            vtxdata.position = om.MPoint(vtx['position'])
            vtxdata.index = vtx['index']

            # UV positionを含まない旧データのために念のためチェックする
            if 'uv_position' in vtx.keys():
                # vertex faceの情報作成
                vtxfacedata = vertex.FaceVtxData()
                vtxfacedata.uv_pos = vtx['uv_position']
                vtxdata.face_vtx_datas = [vtxfacedata]
            else:
                not_have_uv_pos = True

            vtxdatas.append(vtxdata)

        if not_have_uv_pos:
            om.MGlobal.displayWarning('旧データのため、UV位置の情報がデータに含まれていません')

        self.src_vtxdatas = vtxdatas
        self.src_skinweight_dict = skin_weight_dict

    def __coordinate_data(self, weights, comps, inf_list):
        """Componentが順々になるようにweightsをソートする
        (setWeightsにおいてComponentの並び順は拾ってはくれない模様。ソートしてやらないといけない)

        Args:
            weights (list(float)): ウェイトのリスト
            comps (list(int)): 対象頂点番号のリスト
            inf_list (list(int)): 対象インフルエンスのIndexのリスト
        return:
            (list(float), list(int)): 頂点番号順にソートされたウェイトのリストと頂点番号のリスト
        """

        # 無効なIndexがある場合に除外する
        invalid_inf_idx = []
        filtered_inf = []

        # idxはinf_list上で何番目かを指定しており、inf_idxは実際のinfluenceのindex。(infのidxはremapなどで順番通りでない可能性がある)
        for idx, inf_idx in enumerate(inf_list):
            if inf_idx == -1:
                invalid_inf_idx.append(idx)
            else:
                filtered_inf.append(inf_idx)

        # コンポーネント(頂点)のID順に並べるためにコンポーネントごとにウェイトを収集
        comp_weight_dicts = []
        org_inf_count = len(inf_list)
        for i in range(len(comps)):

            this_dict = {
                'comp_id': comps[i],
                'weights': None,
            }

            # weightsからこのコンポーネントに必要な値を抽出
            new_weight = []
            if not invalid_inf_idx:
                new_weight = weights[org_inf_count * i:org_inf_count * i + org_inf_count]
            else:
                for idx in range(org_inf_count):
                    if idx not in invalid_inf_idx:
                        new_weight.append(weights[org_inf_count * i + idx])

            # influenceが無効の場合など、すべてのweightが0になってしまう場合はスキップする
            if not new_weight or all([x == 0 for x in new_weight]):
                continue

            this_dict['weights'] = new_weight
            comp_weight_dicts.append(this_dict)

        # ID順に並び替え
        comp_weight_dicts.sort(key=lambda x: x['comp_id'])
        sorted_weights = []
        sorted_comps = []

        for comp_weight_dict in comp_weight_dicts:
            sorted_weights.extend(comp_weight_dict['weights'])
            sorted_comps.append(comp_weight_dict['comp_id'])

        return (sorted_weights, sorted_comps, filtered_inf)

