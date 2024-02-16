# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import os

import maya.cmds as cmds
import maya.mel as mel

from ..base_common import utility as base_utility
from ..base_common import classes as base_class
from ..glp_common.classes.info import chara_info
from . import target_info
from . import facial_rig_head_attach


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialTargetExporter(object):

    # ===============================================
    def __init__(self, main):

        self.main = main

        self.target_file_path = None
        self.target_file_name = None
        self.target_dir_path = None

        self.model_file_path = None

        self.chara_info = None

        self.is_checked = False

        self.exporter = None

    # ===============================================
    def export(self):

        base_utility.logger.reset()
        base_utility.logger.set_encode_type('shift-jis')
        base_utility.logger.is_print(True)

        base_utility.logger.write()
        base_utility.logger.write_line(0)
        base_utility.logger.write('フェイシャルエクスポート')
        base_utility.logger.write_line(0)
        base_utility.logger.write()

        self.is_checked = self.__check_data()

        if not self.is_checked:
            base_utility.logger.write("ファイルに問題がありました")
            return False

        if not self.__export_facial_target():
            base_utility.logger.write("facial_target.fbxの出力失敗")
            return False

        if not self.__export_eye_animation():
            base_utility.logger.write("目のハイライトアニメーションの出力失敗")
            return False

        base_utility.logger.write()
        base_utility.logger.write('完了')
        base_utility.logger.write_line(1)
        return True

    # ===============================================
    def __check_data(self):

        base_utility.logger.write()
        base_utility.logger.write_line()
        base_utility.logger.write('データチェック')
        base_utility.logger.write()

        self.target_file_path = cmds.file(q=True, sn=True)

        if not self.target_file_path:
            base_utility.logger.write("シーンが開けませんでした")
            return False

        self.target_file_name = os.path.basename(self.target_file_path)
        self.target_dir_path = os.path.dirname(self.target_file_path)

        if self.target_file_name.find("____temp_") > -1:
            self.target_file_name = self.target_file_name.split("____temp_")[1]

        # 例: mdl_chr1010_00.ma とか
        model_file_name = self.target_file_name.split("_facial_target")[0] + ".ma"

        if not model_file_name:
            return False

        self.model_file_path = \
            self.target_dir_path + '/' + model_file_name

        if not os.path.isfile(self.model_file_path):
            base_utility.logger.write("モデルファイルがありません: " + self.model_file_path)
            return False

        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info(file_path=self.model_file_path)

        if not self.chara_info.exists:
            base_utility.logger.write("キャラインフォがありません: " + self.model_file_path)
            return False

        self.exporter = base_class.fbx_exporter.FbxExporter()

        base_utility.logger.write(
            'フォルダ : {0}'.format(self.target_dir_path))
        base_utility.logger.write(
            'ターゲット : {0}'.format(self.target_file_name))
        base_utility.logger.write(
            'モデル : {0}'.format(model_file_name))
        return True

    # ===============================================
    def __export_facial_target(self):

        # -----------------------
        # Unityに正しく渡るようにベイク元のトランス値を修正

        rig_attach = facial_rig_head_attach.FacialRigHeadAttach()
        rig_attach.detach_rig()

        # フェイシャル側でベース表情を触っているものがあるので一度バインドポーズをかける
        root_list = cmds.ls(self.chara_info.part_info.root_node, l=True, r=True)
        if root_list:
            cmds.dagPose(root_list[0], restore=True, g=True, bindPose=True)

        self.__transfer_local_pivot_to_translate()

        rig_attach.attach_rig()

        # -----------------------
        # リグファイルのからフェイシャル情報を取得

        base_utility.logger.write()
        base_utility.logger.write_line()
        base_utility.logger.write('facial_targetからフェイシャル情報を取得')
        base_utility.logger.write()

        this_target_info = target_info.TargetInfo()

        this_target_info.create_info_from_csv(
            'facial_target_info', 'facial_controller_info')

        this_target_info.target_controller_info.controller_root_name = 'Rig_head|Rig_eye_high'
        this_target_info.target_controller_info.target_root_name = 'mdl_chr'

        this_target_info.update_info(False, True)

        # -----------------------
        # フェイシャルターゲットの出力

        base_utility.logger.write()
        base_utility.logger.write_line()
        base_utility.logger.write('facial_target.fbxの出力')
        base_utility.logger.write()

        base_utility.file.open(self.model_file_path)

        # fbxが正しく出力されるようにベイク先にもトランス値の修正を入れる
        self.__transfer_local_pivot_to_translate()

        this_target_info.bake_transform(False, True, False)

        this_target_info.create_info_locator(
            'FacialInfo', self.chara_info.part_info.root_node)

        # オイラー角がフリップしていることがあったのでフィルターをかける
        self.main.apply_euler_filter()

        self.exporter.reset()

        self.exporter.target_node_list = [self.chara_info.part_info.root_node]

        self.exporter.fbx_file_path = self.target_dir_path + '/'

        self.exporter.fbx_file_path += \
            'mdl_' + self.chara_info.part_info.data_id + "_facial_target.fbx"

        return self.exporter.export()

    # ===============================================
    def __export_eye_animation(self):

        base_utility.logger.write()
        base_utility.logger.write_line()
        base_utility.logger.write('目のハイライトアニメーションの出力')
        base_utility.logger.write()

        base_utility.file.open(self.target_file_path)

        cmds.currentTime(-1)
        cmds.currentTime(0)

        this_namespace = 'mdl_' + self.chara_info.part_info.data_id

        reference_path = self.chara_info.part_info.maya_scenes_dir_path + '/' + \
            'mdl_' + self.chara_info.part_info.file_id + '.ma'

        base_utility.reference.change_reference_file_path_by_namespace(
            this_namespace, reference_path
        )

        base_utility.reference.import_reference_by_namespace(
            this_namespace
        )

        base_utility.namespace.remove(
            this_namespace
        )

        cmds.delete('Rig_head')

        for mesh in self.chara_info.part_info.mesh_list:

            if not base_utility.transform.exists(mesh):
                continue

            cmds.select(mesh, r=True)
            mel.eval('gotoBindPose;')

        frame_list = [
            [600, 634, 0],
            [700, 740, 1]
        ]

        target_list = [
            'Eye_base_info_L',
            'Eye_base_info_R',
            'Eye_big_info_L',
            'Eye_big_info_R',
            'Eye_small_info_L',
            'Eye_small_info_R',
            'Eye_kira_info'
        ]
        try:
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
        except Exception as ex:
            cmds.warning(ex)
            return False
        self.exporter.reset()

        self.exporter.target_node_list = [self.chara_info.part_info.root_node]
        self.exporter.is_ascii = False
        has_error = False
        for frame in frame_list:

            cmds.playbackOptions(
                min=frame[0], max=frame[1], ast=frame[0], aet=frame[1])

            self.exporter.fbx_file_path = \
                self.chara_info.part_info.maya_scenes_dir_path + '/' + \
                'anm_' + self.chara_info.part_info.data_id + \
                "_facial_eye0{0}.fbx".format(frame[2])

            if not self.exporter.export():
                has_error = True

        if has_error:
            return False
        else:
            return True

    # ===============================================
    def __transfer_local_pivot_to_translate(self):

        root_node = self.chara_info.part_info.root_node + '|Neck'
        root_node = cmds.ls(root_node, r=True)

        if not root_node:
            return

        all_trans_list = cmds.listRelatives(root_node[0], ad=True, type='transform', f=True)
        all_trans_list = cmds.ls(all_trans_list, et='transform', r=True)

        for trans in all_trans_list:
            self.main.transfer_local_pivot_to_translate(trans)
