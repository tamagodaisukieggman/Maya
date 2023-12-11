# -*- coding: utf-8 -*-
"""facial/ear_targetからBlendShapeモデルを作成する
BlendShapeの順番はリストの並び順でセットされる
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from . import util, reference, fbx_exporter, target_info

# Python3-
try:
    from importlib import reload
    from builtins import object
except Exception:
    pass

reload(util)
reload(reference)
reload(fbx_exporter)
reload(target_info)


class BlendShapeTargetExport(object):

    def __init__(self):

        self.facial_target_suffix = '_facial_target'
        self.ear_target_suffix = '_ear_target'

    def export(self, target_file_path, facial_blend_target_mesh_name, ear_blend_target_mesh_name):
        """facial/ear_targetからBlendShapeモデルを作成する
        BlendShapeの順番はリストの並び順でセットされる

        Args:
            target_file_path (String): 実行対象のパス
            facial_blend_target_mesh_name (String): 顔用のblendshape作成対象メッシュ名
            ear_blend_target (_type_): 耳用のblendshape作成対象メッシュ名
        """

        if not self.__check_data_path(target_file_path):
            return

        # 新規シーンを開いてリセット
        cmds.file(new=True, force=True)
        # 新規シーンは30fps固定
        # TODO: 2022/4/7 facial_targetシーンのfps値を取得して入れこむ処理にした方が汎用性が増えるが、一時対応
        cmds.currentUnit(time='30fps')

        # facial_target Load
        reference.load(self.facial_target_ma_path, self.model_ma_name_without_ext)

        # 顔のblandShape情報取得
        facial_blend_shape_target_info = self.__create_blend_shape_target_info('facial_blend_shape_target_info', 'facial_controller_info')
        if facial_blend_shape_target_info is None:
            return

        # blendShape用mesh複製
        result = self.__create_bland_shape_meshes(facial_blend_target_mesh_name, facial_blend_shape_target_info)
        # facial_target Unload
        reference.unload(self.facial_target_ma_path, self.model_ma_name_without_ext)

        if result is None:
            return

        facial_blend_target_group = result.get('group')
        facial_blend_target_name_list = result.get('list')

        # ear_target Load
        reference.load(self.ear_target_ma_path, self.model_ma_name_without_ext)

        ear_blend_shape_target_info = self.__create_blend_shape_target_info('ear_blend_shape_target_info', 'ear_controller_info')
        if ear_blend_shape_target_info is None:
            return

        # blendShape用mesh複製
        result = self.__create_bland_shape_meshes(ear_blend_target_mesh_name, ear_blend_shape_target_info)
        # Unload
        reference.unload(self.ear_target_ma_path, self.model_ma_name_without_ext)

        if result is None:
            return

        ear_blend_target_group = result.get('group')
        ear_blend_target_name_list = result.get('list')

        # ファイル一時保存
        tmp_file_path = os.path.join(self.target_dir_path, '{}_blend_shape_target.mb'.format(self.model_ma_name_without_ext))
        cmds.file(rename=tmp_file_path)
        cmds.file(s=True, type='mayaBinary')

        # maファイルを開く
        cmds.file(new=True, force=True)
        cmds.file(self.target_model_ma_path, o=True, force=True)

        # import
        cmds.file(tmp_file_path, i=True, importTimeRange='combine')

        # ノード検索
        facial_blend_target_node = util.find_node(facial_blend_target_mesh_name)
        ear_blend_target_node = util.find_node(ear_blend_target_mesh_name)
        if not facial_blend_target_node or not ear_blend_target_node:
            return False

        # blendShape作成
        cmds.blendShape(facial_blend_target_name_list + [facial_blend_target_node])
        cmds.blendShape(ear_blend_target_name_list + [ear_blend_target_node])

        # 元ノード削除
        cmds.delete(facial_blend_target_group)
        cmds.delete(ear_blend_target_group)

        # maファイルをセーブ
        blend_shape_target_ma_path = os.path.join(self.target_dir_path, '{}_blend_shape_target.ma'.format(self.model_ma_name_without_ext))
        cmds.file(rename=blend_shape_target_ma_path)
        cmds.file(s=True, type='mayaAscii')

        # fbxを出力
        exporter = fbx_exporter.FbxExporter()
        exporter.reset()
        exporter.target_node_list = [self.model_ma_name_without_ext]
        exporter.is_ascii = False
        exporter.fbx_file_path = os.path.join(self.target_dir_path, '{}_blend_shape_target.fbx').format(self.model_ma_name_without_ext).replace(os.path.sep, '/')

        exporter.export()

        # tmpファイルの削除
        os.remove(tmp_file_path)

    def __check_data_path(self, target_file_path):
        """blendShpae作成に必要な元モデルのパスやfacial/ear_targetのパス等を取得してセット
        パスに問題があれば処理途中で返す

        Args:
            target_file_path (String): 開いたファイルのフルパス

        Returns:
            bool: パス生成に成功したかどうか
        """

        target_file_path = target_file_path.replace(os.path.sep, '/')
        if not os.path.exists(target_file_path):
            return False

        # 元モデルのパス
        self.target_model_ma_path = target_file_path.replace(self.ear_target_suffix, '').replace(self.facial_target_suffix, '')
        if not os.path.exists(self.target_model_ma_path):
            return False

        # ディレクトリパス
        self.target_dir_path = os.path.dirname(self.target_model_ma_path)

        # 元モデルの名前拡張子ありと抜き
        self.model_ma_name = os.path.basename(self.target_model_ma_path)
        self.model_ma_name_without_ext = os.path.splitext(self.model_ma_name)[0]

        # facial_targetのパス
        self.facial_target_ma_path = os.path.join(self.target_dir_path, '{}{}.ma'.format(self.model_ma_name_without_ext, self.facial_target_suffix))
        if not os.path.exists(self.facial_target_ma_path):
            return False

        # ear_targetのパス
        self.ear_target_ma_path = os.path.join(self.target_dir_path, '{}{}.ma'.format(self.model_ma_name_without_ext, self.ear_target_suffix))
        if not os.path.exists(self.ear_target_ma_path):
            return False

        return True

    def __create_blend_shape_target_info(self, blend_shape_target_csv_name, controller_csv_name):
        """顔・耳のblendShape情報クラスを取得

        Args:
            blend_shape_target_csv_name (String): blendShpae情報が記載されたCSV名
            controller_csv_name (String): 顔・耳のコントローラー情報が記載されたＣＳＶ名

        Returns:
            TargetInfo or None
        """

        # ネームスペース取得
        target_namespace = ''
        for _namespace in cmds.namespaceInfo(lon=True):
            if _namespace.startswith(self.model_ma_name_without_ext):
                target_namespace = _namespace
                break

        blend_shape_target_info = target_info.TargetInfo()
        blend_shape_target_info.create_info_from_csv(blend_shape_target_csv_name, controller_csv_name, namespace=target_namespace)
        blend_shape_target_info.update_info(True, False)
        if blend_shape_target_info.is_created:
            return blend_shape_target_info

        return None

    def __create_bland_shape_meshes(self, blend_target_name, target_info):
        """顔・耳のblendShapeを作成する

        Args:
            blend_target_name (String): _description_
            target_info (TargetInfo): blendShape情報が入ったクラスobject

        Returns:
            None or 作成したblendShapeのgroup名と複製したメッシュ名(blendShape名)のリストが入った辞書型
            ({'group': グループ名, 'list': 複製したメッシュ名(blendShape名)のリスト})
        """

        # ノード検索
        blend_target_node = util.find_node(blend_target_name)
        if not blend_target_node:
            return None

        # BASEフレームに移動
        cmds.currentTime(0)

        duplicate_mesh_list = []
        duplicate_node_name_list = []

        # BASEから特定フレームの値を取得してコントローラーにセット、duplicate後にリセット
        for target_info_item in target_info.info_item_list:

            # Base設定用オブジェクトは利用しない
            if target_info_item.part == 'Base':
                continue

            for controller_info_item in target_info_item.controller_info_item_list:
                if controller_info_item.part.startswith(target_info_item.part):
                    controller_info_item.set_transform(True, None, False, 1.0)

            duplicate_node_name = target_info_item.label
            duplicate_node_name_list.append(duplicate_node_name)
            # ここでduplicate
            duplicate_mesh = cmds.duplicate(blend_target_node, n=duplicate_node_name)[0]
            # lambert1をセット
            cmds.sets(duplicate_mesh, e=True, forceElement='initialShadingGroup')

            # attrを元の値に戻す
            for controller_info_item in target_info_item.controller_info_item_list:
                if controller_info_item.part.startswith(target_info_item.part):
                    controller_info_item.set_transform(True, None, True, 1.0)

            duplicate_mesh_list.append(duplicate_mesh)

        # メッシュを1つのグループにまとめる
        meshes_group = cmds.group(duplicate_mesh_list)
        meshes_group = cmds.parent(meshes_group, w=True)[0]

        return {'group': meshes_group, 'list': duplicate_node_name_list}
