# -*- coding: utf-8 -*-
"""facial_target.maからfacial_target.fbxを出力する
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds
import maya.mel as mel

from . import util, facial_rig_head_attach, fbx_exporter, target_info, reference

# Python3-
try:
    from importlib import reload
    from builtins import object
except Exception:
    pass

reload(util)
reload(facial_rig_head_attach)
reload(fbx_exporter)
reload(target_info)
reload(reference)


class FacialTargetExport(object):

    def __init__(self):

        self.target_file_path = ''
        self.target_file_name = ''
        self.target_file_name_without_ext = ''
        self.target_dir_path = ''
        self.model_ma_path = ''

        # ルートノード
        self.model_root_node = ''

        self.facial_target_suffix = '_facial_target'

        self.exporter = fbx_exporter.FbxExporter()

    def export(self, target_file_path):
        """フェイシャルターゲットのエクスポート実行

        Args:
            target_file_path (String): 出力対象のfacial_target.maのパス

        Returns:
            bool: fbxエクスポートが成功したかどうか
        """

        if not self.__check_data_path(target_file_path):
            return False

        # ファイルを開く前に一度new scene
        cmds.file(new=True, force=True)

        # ファイルを開く
        cmds.file(target_file_path, o=True, f=True)

        if not self.__set_scene_model_root_node():
            return False

        if not self.__export_facial_target():
            return False

        if not self.__export_eye_animation():
            return False

        return True

    def __check_data_path(self, target_file_path):
        """Export前に対象データかチェックし、変数にパスをセット

        Args:
            target_file_path (String): 出力対象のfacial_target.maのパス

        Returns:
            bool: 対象データかどうか
        """

        self.target_file_path = target_file_path.replace(os.path.sep, '/')
        if not os.path.exists(self.target_file_path):
            return False

        # facial_target以外は対象としない
        if self.target_file_path.find(self.facial_target_suffix) < 0:
            return False

        # facial_targetのファイル名
        self.target_file_name = os.path.basename(self.target_file_path)

        # facial_targetのファイル名拡張子抜き
        self.target_file_name_without_ext = os.path.splitext(self.target_file_name)[0]

        # ディレクトリパス
        self.target_dir_path = os.path.dirname(self.target_file_path)

        # 元モデルのパス
        self.model_ma_path = self.target_file_path.replace(self.facial_target_suffix, '')
        if not os.path.exists(self.model_ma_path):
            return False

        return True

    def __set_scene_model_root_node(self):
        """開いているシーンの対象モデルのルートノードを変数にセット

        Returns:
            bool: ルートノードがあったかどうか
        """

        # ルートノード名
        self.model_root_node = self.target_file_name_without_ext.replace(self.facial_target_suffix, '')
        # リファレンス環境で見つからなかったらFalse
        if not cmds.ls(self.model_root_node, l=True, r=True):
            return False

        return True

    def __export_facial_target(self):
        """フェイシャルターゲットを出力する
        """

        rig_attach = facial_rig_head_attach.FacialRigHeadAttach()
        rig_attach.detach_rig()

        model_root_node_list = cmds.ls(self.model_root_node, l=True, r=True)
        if model_root_node_list:
            cmds.dagPose(model_root_node_list[0], restore=True, g=True, bindPose=True)

        self.__transfer_local_pivot_to_translate()

        rig_attach.attach_rig()

        # フェイシャル情報の取得
        this_target_info = target_info.TargetInfo()
        this_target_info.create_info_from_csv('facial_target_info', 'facial_controller_info')
        this_target_info.target_controller_info.controller_root_name = 'Rig_head|Rig_eye_high'
        this_target_info.target_controller_info.target_root_name = self.model_root_node
        this_target_info.update_info(False, True)

        if not this_target_info.is_created:
            return False

        # 元モデルファイルを開く
        cmds.file(self.model_ma_path, o=True, f=True)

        # fbxが正しく出力されるようにベイク先にもトランス値の修正を入れる
        self.__transfer_local_pivot_to_translate()

        # Controllerに接続されている骨にindexframeでControllerの値をbake
        this_target_info.bake_transform(False, True, False)

        # Unityで値を取得する用のロケーターの作成
        this_target_info.create_info_locator('FacialInfo', self.model_root_node)

        # オイラー角がフリップしていることがあったのでフィルターをかける
        util.apply_euler_filter()

        # fbx出力
        return self.__export_facial_target_fbx()

    def __export_facial_target_fbx(self):
        """facial_target.fbxを出力する

        Returns:
            bool: fbxが正常に出力できたか
        """

        self.exporter.reset()
        self.exporter.target_node_list = [self.model_root_node]
        self.exporter.fbx_file_path = os.path.join(self.target_dir_path, '{}.fbx'.format(self.target_file_name_without_ext)).replace(os.path.sep, '/')
        return self.exporter.export()

    def __export_eye_animation(self):
        """目のアニメーションを出力する

        Returns:
            bool: 全てのFBXが出力できたか
        """

        cmds.file(self.target_file_path, open=True, f=True)

        cmds.currentTime(-1)
        cmds.currentTime(0)

        this_namespace = self.model_root_node
        reference_path = self.model_ma_path

        reference.change_reference_file_path_by_namespace(this_namespace, reference_path)
        reference.import_reference_by_namespace(this_namespace)

        cmds.namespace(rm=this_namespace, mergeNamespaceWithRoot=True)

        cmds.delete('Rig_head')

        meshes = cmds.listRelatives(self.model_root_node, ad=True, type='mesh')
        meshes = [cmds.listRelatives(mesh, p=True)[0] for mesh in meshes if cmds.listRelatives(mesh, p=True) is not None]

        for mesh in meshes:

            cmds.select(mesh, r=True)
            mel.eval('gotoBindPose;')

        frame_list = [[600, 634, 0], [700, 740, 1]]

        target_list = [
            'Eye_base_info_L',
            'Eye_base_info_R',
            'Eye_big_info_L',
            'Eye_big_info_R',
            'Eye_small_info_L',
            'Eye_small_info_R',
            'Eye_kira_info'
        ]

        cmds.bakeResults(
            target_list,
            simulation=True,
            time=(600, 800),
            sampleBy=1,
            oversamplingRate=1,
            disableImplicitControl=True,
            preserveOutsideKeys=True,
            sparseAnimCurveBake=False,
            removeBakedAttributeFromLayer=False,
            removeBakedAnimFromLayer=False,
            bakeOnOverrideLayer=False,
            minimizeRotation=True,
            controlPoints=False,
            shape=True
        )

        self.exporter.reset()
        self.exporter.target_node_list = [self.model_root_node]
        self.exporter.is_ascii = False

        was_export = True
        for frame in frame_list:

            cmds.playbackOptions(min=frame[0], max=frame[1], ast=frame[0], aet=frame[1])
            export_file_name = '{}_facial_eye0{}.fbx'.format(self.model_root_node.replace('mdl_', 'anm_'), frame[2])
            self.exporter.fbx_file_path = os.path.join(self.target_dir_path, export_file_name).replace(os.path.sep, '/')

            result = self.exporter.export()
            if not result:
                was_export = False

        return was_export

    def __transfer_local_pivot_to_translate(self):
        """ローカルピボットとtranslateから原点からのベクトルと原点へのベクトルを計算して
        translateをフリーズ後ローカルピボットのtranslateをセットする
        """

        neck_node_list = cmds.ls('{}|Neck'.format(self.model_root_node), r=True)
        if not neck_node_list:
            return

        neck_node = neck_node_list[0]
        all_trans_list = cmds.listRelatives(neck_node, ad=True, type='transform', f=True)
        all_trans_list = cmds.ls(all_trans_list, et='transform', r=True)

        for trans in all_trans_list:
            util.transfer_local_pivot_to_translate(trans)
