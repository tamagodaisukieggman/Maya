# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from builtins import str
except Exception:
    pass

import os

import maya.cmds as cmds
import maya.mel as mel

from ....base_common import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TransferNormal(object):
    """
    頭部へのトゥーン用法線をテンプレートから転写してスムースなシェーディングにします。
    顔のメッシュは複雑な形状をしているため、ソフトエッジだけでは十分にスムースなシェーディングになりません。
    法線の情報を整えるために、シンプルな形状のモデルから法線情報を移植します。
    """
    # ===============================================
    def __init__(self):

        self.template_path = 'W:\\gallop\\svn\\svn_gallop\\80_3D\\01_character\\01_model\\common\\bake_face\\scenes\\bake_face.ma'
        self.template_mesh_suffix = '_normal_template'
        self.tmplate_name_space = '__normal_tmp__'

    # ===============================================
    def create_mesh_template_dict(self, selection):
        """
        法線テンプレートと対応するメッシュのペアのディクショナリを作る。
        選択しているメッシュ名をテンプレートのフォーマットのメッシュ名に変換するので
        存在しないテンプレートメッシュ名がkeyになる場合もある。
        逆にbake_face.maの中に命名規則通りのテンプレートさえ増やせばコードは変えなくても対応できる作り。
        Returns:
            {ネームスペース付きテンプレートメッシュ名, メッシュ名}
        """
        src_dst_mesh_pair_dict = {}  # key: ネームスペース付きテンプレートメッシュ名, value: モデルのメッシュ名
        for mesh in selection:
            # メッシュ名をテンプレートのフォーマットのメッシュ名に変換
            # 例 |mdl_chr1010_00|M_Face のテンプレートは __normal_tmp__:M_Face_normal_template
            src_mesh_name = '{0}:{1}{2}'.format(self.tmplate_name_space, mesh.split('|')[-1], self.template_mesh_suffix)
            if src_mesh_name in list(src_dst_mesh_pair_dict.keys()):
                cmds.warning('同名のメッシュを選択しないでください')
                return {}
            else:
                src_dst_mesh_pair_dict[src_mesh_name] = mesh
        return src_dst_mesh_pair_dict

    # ===============================================
    def import_template_mesh(self):
        """
        「テンプレートのインポート」実行
        選択しているメッシュの対応テンプレートメッシュのみ複製してシーン内に残し、リファレンスは削除。
        """
        # 指定したWドライブ配下のSVNにbake_face.maがあるかチェック
        if not os.path.exists(self.template_path):
            cmds.warning('テンプレートが見つかりませんでした(Wドライブの設定でSVNをチェックアウトしていますか?): ' + str(self.template_path))
            return

        selection = cmds.ls(sl=True, l=True, et='transform')
        if not selection:
            cmds.confirmDialog(title='Usage',
                               message='テンプレートのあるメッシュ(例:M_Face, M_Hair)を選択して実行してください',
                               button=['OK'])
            return

        # 選択中のメッシュで想定できるメッシュテンプレート名のディクショナリを作る
        src_dst_mesh_pair_dict = self.create_mesh_template_dict(selection)

        # 既存のテンプレートのリファレンスがシーン内になければリファレンス読み込み
        base_utility.reference.load(self.template_path, self.tmplate_name_space)
        # 選択中のメッシュのテンプレートメッシュだけ複製してシーンに残す
        for template_mesh in list(src_dst_mesh_pair_dict.keys()):
            if cmds.objExists(template_mesh):
                cmds.duplicate(template_mesh)
        # 指定したネームスペースのリファレンスを全て削除
        base_utility.reference.unload(self.template_path, self.tmplate_name_space)

    # ===============================================
    def tarnsfer_normal(self):
        """
        「テンプレートから転写」
        選択しているメッシュの対応テンプレートメッシュから近接頂点へ法線の値をコピーする。
        テンプレートメッシュはリファレンスで読み込み、実行後はシーン内から削除する。
        """
        # 指定したWドライブ配下のSVNにbake_face.maがあるかチェック
        if not os.path.exists(self.template_path):
            cmds.warning('テンプレートが見つかりませんでした(Wドライブの設定でSVNをチェックアウトしていますか?): ' + str(self.template_path))
            return

        selection = cmds.ls(sl=True, l=True, et='transform')
        if not selection:
            cmds.confirmDialog(title='Usage',
                               message='テンプレートのあるメッシュ(例:M_Face, M_Hair)を選択して実行してください',
                               button=['OK'])
            return

        # 選択中のメッシュで想定できるメッシュテンプレート名のディクショナリを作る
        src_dst_mesh_pair_dict = self.create_mesh_template_dict(selection)

        # テンプレートのリファレンスが指定したネームスペースでシーン内になければインポート
        base_utility.reference.load(self.template_path, self.tmplate_name_space)

        # ユーザーが選択したメッシュ(dst_mesh)にテンプレートメッシュ(src_mesh)の法線を反映させる
        for src_mesh, dst_mesh in list(src_dst_mesh_pair_dict.items()):
            if cmds.objExists(src_mesh):
                # 一番近い頂点のテンプレートの法線の値をメッシュに設定
                cmds.transferAttributes(src_mesh, dst_mesh, pos=0, nml=1, uvs=0, col=0, spa=0, sm=3, fuv=0, clb=0)
                # メッシュのヒストリ削除
                cmds.delete(dst_mesh, constructionHistory=True)
                # バーテックスカラーを表示しようとしているが上手くいっていない?
                cmds.select(dst_mesh)
                mel.eval('ToggleDisplayColorsAttr')
        # リファレンスを削除
        base_utility.reference.unload(self.template_path, self.tmplate_name_space)
