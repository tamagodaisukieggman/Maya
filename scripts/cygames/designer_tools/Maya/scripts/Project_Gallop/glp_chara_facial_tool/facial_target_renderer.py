# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import os
import shutil

import subprocess


import maya.cmds as cmds
import maya.mel as mel

from ..base_common import utility as base_utility
from ..base_common import classes as base_class
from ..glp_common.classes.info import chara_info
from . import target_info
from . import facial_combine


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialTargetRenderer(object):

    # ===============================================
    def __init__(self):

        self.render_cam_name = '__facial_render_camera__'
        self.render_resolution = [1000, 1000]
        self.render_type = 'hardware2'
        self.render_global_node = 'defaultRenderGlobals'
        self.render_resolution_node = 'defaultResolution'
        self.hardware_render_global_node = 'hardwareRenderingGlobals'
        self.eyebrow_anim_layer_facial_label = 'Base'
        self.mouth_anim_layer_facial_label = 'WaraiD'

        self.target_part_list = ['Eyebrow_L', 'Eye_L', 'Mouth']

        self.target_file_path = None
        self.target_file_name = None
        self.target_dir_path = None

        self.model_file_path = None

        self.chara_info = None

        self.is_checked = False

    # ===============================================
    def render(self, should_output_psd):
        """
        眉、目、口パーツをレンダリングする
        should_output_psd: bool. Falseならscemesフォルダと同階層のimages/facial_target/キャラIDフォルダ内にpngを書き出し終了。
        Trueなら「xxx_facial_target_tmp.psd」をダウンロードしPhotoshopへ処理を引き渡す。
        Photoshopのスクリプトはこの _facial_target_tmp を目印に対象を割り出し、書き出したpngをpsdにまとめ、
        80_3D/01_character/02_faical_list/facialフォルダにjpgを出力し_facial_target_tmp.psd を _facial_target.psdにリネームし
        対象にならないようにして終了。
        """
        self.is_checked = self.__check_data()

        if not self.is_checked:
            cmds.warning('データに不備がありました')
            return False

        render_dir_path = self.chara_info.part_info.maya_root_dir_path + '/images/facial_target/' + self.chara_info.part_info.data_id

        render_target_dir_path = \
            render_dir_path + '/' + self.chara_info.part_info.data_id + '_target'

        # ------------------------------
        # レンダー設定

        self.set_render_setting()

        # ------------------------------
        # メッシュの表示設定

        self.__check_mesh_visibility()
        self.__offset_eyebrow()

        # ------------------------------
        # フェイシャル
        this_target_info = target_info.TargetInfo()

        this_target_info.create_info_from_csv(
            'facial_target_info', 'facial_controller_info')

        this_target_info.update_info(False, True)

        # ------------------------------
        # レンダリング

        if os.path.isdir(render_target_dir_path):
            shutil.rmtree(render_target_dir_path)

        brow_index = -1
        eye_index = -1
        mouth_index = -1

        for info_item in this_target_info.info_item_list:

            render = base_class.simple_render.SimpleRender()

            render.set_base_camera(self.render_cam_name)
            render.set_base_output_dir(render_dir_path)

            anim_layer_name = None
            label = info_item.label
            frame = info_item.frame
            index = info_item.index
            part_index = 0
            part = info_item.part
            waku = 0

            if info_item.animation_layer_name:
                anim_layer_name = info_item.animation_layer_name

            if part not in self.target_part_list:
                # パーツのディクショナリが作られていなくても構わない？
                continue

            if part == self.target_part_list[0]:
                brow_index += 1
                part_index = brow_index

            elif part == self.target_part_list[1]:
                eye_index += 1
                part_index = eye_index

            elif part == self.target_part_list[2]:
                mouth_index += 1
                part_index = mouth_index

            # ------------------------------
            # animationLayerがある場合
            if anim_layer_name:

                target_facial_label = None

                if part == 'Eyebrow_L':
                    target_facial_label = self.eyebrow_anim_layer_facial_label
                elif part == 'Mouth':
                    target_facial_label = self.mouth_anim_layer_facial_label

                if not target_facial_label:
                    return False

                for facial_info in this_target_info.info_item_list:

                    if facial_info.label == target_facial_label:
                        frame = facial_info.frame

                waku = 1

                self.__set_weight_anim_layer(anim_layer_name, 1.0)

            render_file_name = \
                '{0}__{1}__{2}__{3}F__{4}__{5}'.format(
                    index, label, part_index, frame, part, waku)

            cmds.currentTime(frame)

            render.add_item(
                file_name=render_file_name,
            )

            render.render()

            if anim_layer_name:
                self.__set_weight_anim_layer(anim_layer_name, 0.0)

        render = base_class.simple_render.SimpleRender()

        render.set_base_camera(self.render_cam_name)
        render.set_base_output_dir(render_dir_path)

        title_file_name = \
            'title__{0}'.format(
                '【 フェイシャルのターゲット一覧 {0} 】'.format(self.chara_info.part_info.data_id))

        render.add_item(file_name=title_file_name)
        cmds.currentTime(0)
        render.render()

        cmds.delete(self.render_cam_name)

        # ------------------------------
        # テンプレートのダウンロード

        if should_output_psd:

            tool_dir = os.path.dirname(__file__)
            resource_dir = os.path.join(tool_dir, 'resource')
            template_file_path = os.path.join(resource_dir, 'template_facial_target.psd')

            copy_file_path = \
                render_dir_path + '/' + self.chara_info.part_info.data_id + '_facial_target_tmp.psd'

            shutil.copy(template_file_path, copy_file_path)

            if not os.path.exists(copy_file_path):
                cmds.warning('copy_file_pathがありません: ' + copy_file_path)
                return False
        return True

    # ===============================================
    def render_face_type(self, should_output_psd):
        """
        眉、目、口パーツを組み合わせた各種「表情」をレンダリングする
        should_output_psd: bool. Falseならscemesフォルダと同階層のimages/face_type/キャラIDフォルダ内にpngを書き出し終了。
        TrueならPhotoshopへ処理を引き渡し、書き出したpngをpsdにまとめ、80_3D/01_character/02_faical_list/face_typeフォルダにjpgを出力。
        """
        self.is_checked = self.__check_data()

        if not self.is_checked:
            cmds.warning('__check_dataでエラーがありました')
            return False

        render_dir_path = self.chara_info.part_info.maya_root_dir_path + '/images/face_type/' + self.chara_info.part_info.data_id

        render_target_dir_path = \
            render_dir_path + '/' + self.chara_info.part_info.data_id + '_target'

        # ------------------------------
        # レンダー設定

        self.set_render_setting(20)

        # ------------------------------
        # メッシュの表示設定

        self.__check_mesh_visibility()
        self.__offset_eyebrow()

        # ------------------------------
        # フェイシャル
        this_target_info = facial_combine.FacialCombine()
        this_target_info.initialize_from_csv('facial_target_info', 'facial_controller_info', 'face_type_data')
        if not this_target_info.face_type_item_list:
            cmds.warning('csvの読み取りに失敗')
            return False
        # ------------------------------
        # レンダリング
        if os.path.isdir(render_target_dir_path):
            shutil.rmtree(render_target_dir_path)

        for info_item in this_target_info.face_type_item_list:

            render = base_class.simple_render.SimpleRender()

            render.set_base_camera(self.render_cam_name)
            render.set_base_output_dir(render_dir_path)

            label = info_item.label
            group_index = info_item.group_index
            group = info_item.set_face_group_index

            render_file_name = '{0}__{1}__{2}'.format(str(group), str(group_index), label)

            render.add_item(
                file_name=render_file_name,
            )

            info_item.apply_facial()

            render.render()

        render = base_class.simple_render.SimpleRender()

        render.set_base_camera(self.render_cam_name)
        render.set_base_output_dir(render_dir_path)

        title_file_name = \
            'title__{0}'.format(
                '【 フェイスタイプ一覧 {0} 】'.format(self.chara_info.part_info.data_id))

        render.add_item(file_name=title_file_name)
        cmds.currentTime(0)
        render.render()

        cmds.delete(self.render_cam_name)

        # ------------------------------
        # テンプレートのダウンロード

        if should_output_psd:

            tool_dir = os.path.dirname(__file__)
            resource_dir = os.path.join(tool_dir, 'resource')
            template_file_path = os.path.join(resource_dir, 'template_face_type_target.psd')

            copy_file_path = \
                render_dir_path + '/' + self.chara_info.part_info.data_id + '_face_type_target_tmp.psd'

            shutil.copy(template_file_path, copy_file_path)

            if not os.path.exists(copy_file_path):
                cmds.warning('copy_file_pathがありません: ' + copy_file_path)
                return False
        return True

    # ===============================================
    def __check_data(self):

        base_utility.logger.write()
        base_utility.logger.write_line()
        base_utility.logger.write('データチェック')
        base_utility.logger.write()
        self.target_file_path = cmds.file(q=True, sn=True)

        if not self.target_file_path:
            return False

        if self.target_file_path.find('_facial_target') < 0:
            return False

        self.target_file_path = \
            self.target_file_path.replace('\\', ' / ')

        self.target_file_name = os.path.basename(self.target_file_path)
        self.target_dir_path = os.path.dirname(self.target_file_path)

        model_file_name = base_utility.string.get_string_by_regex(
            self.target_file_name, 'mdl_.*_facial_target'
        )

        if not model_file_name:
            return False

        model_file_name = model_file_name.replace('_facial_target', '') + '.ma'

        self.model_file_path = \
            self.target_dir_path + '/' + model_file_name

        if not os.path.isfile(self.model_file_path):
            return False

        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info(file_path=self.model_file_path)

        if not self.chara_info.exists:
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
    def __check_mesh_visibility(self):

        data_id = self.chara_info.data_id

        invisible_target_list = ['Cheek', 'Tear', 'Line', 'Outline', 'Alpha']
        all_mesh_list = cmds.ls('::M_*', l=True, fl=True, et='transform')

        model_mesh_list = []
        invisible_mesh_list = []

        for mesh in all_mesh_list:

            if mesh.find('mdl_{}'.format(data_id)) < 0:
                continue

            model_mesh_list.append(mesh)

            for invisible_target in invisible_target_list:
                if mesh.find(invisible_target) >= 0:
                    invisible_mesh_list.append(mesh)
                    break

        for mesh in model_mesh_list:
            if mesh not in invisible_mesh_list:
                cmds.setAttr(mesh + '.visibility', 1)
            else:
                cmds.setAttr(mesh + '.visibility', 0)

    # ===============================================
    def set_render_setting(self, render_width=16):

        facial_render_camera = cmds.camera(name=self.render_cam_name)[0]

        facial_render_camera = cmds.rename(facial_render_camera, self.render_cam_name)

        base_utility.attribute.set_value(
            facial_render_camera, 'orthographic', 1)

        base_utility.attribute.set_value(
            facial_render_camera, 'orthographicWidth', render_width)

        base_utility.attribute.set_value(
            facial_render_camera, 'translate', [0, 12, 1000])

        base_utility.attribute.set_value(
            self.render_global_node,
            'currentRenderer', 'mayaHardware2'
        )

        mel.eval('loadPreferredRenderGlobalsPreset("mayaHardware2")')

        base_utility.attribute.set_value(
            self.render_resolution_node,
            'width', self.render_resolution[0]
        )

        base_utility.attribute.set_value(
            self.render_resolution_node,
            'height', self.render_resolution[1]
        )

        base_utility.attribute.set_value(
            self.render_resolution_node, 'aspectLock', 1
        )

        base_utility.attribute.set_value(
            self.hardware_render_global_node, 'lightingMode', 4
        )

        base_utility.attribute.set_value(
            self.hardware_render_global_node, 'lineAAEnable', 1
        )

        base_utility.attribute.set_value(
            self.hardware_render_global_node, 'multiSampleEnable', 1
        )

        base_utility.attribute.set_value(
            self.hardware_render_global_node, 'multiSampleCount', 16
        )

        base_utility.attribute.set_value(
            self.render_global_node, 'imageFormat', 32
        )

    # ===============================================
    def __offset_eyebrow(self):

        if cmds.objExists('Eyebrow_offset_L_g'):
            cmds.setAttr('Eyebrow_offset_L_g.translateZ', 20)

        if cmds.objExists('Eyebrow_offset_R_g'):
            cmds.setAttr('Eyebrow_offset_R_g.translateZ', 20)

    # ===============================================
    def __set_weight_anim_layer(self, animation_layer_name, weight):

        if not cmds.animLayer(animation_layer_name, q=True, exists=True):
            return

        cmds.animLayer(animation_layer_name, e=True, weight=weight, mute=False)

    # ===============================================
    def exe_subprocess(self):

        # ------------------------------
        # バッチなどのパスチェック

        script_file_path = os.path.abspath(__file__)
        script_file_path = script_file_path.replace('\\', '/')

        script_dir_path = os.path.dirname(script_file_path)

        ps_script_file_path = script_dir_path + '/batch/ps_target_maker.jsx'

        ps_exe_path = None
        if os.path.isfile('C:/Program Files/Adobe/Adobe Photoshop 2023/Photoshop.exe'):
            ps_exe_path = 'C:/Program Files/Adobe/Adobe Photoshop 2023/Photoshop.exe'
        elif os.path.isfile('C:/Program Files/Adobe/Adobe Photoshop 2022/Photoshop.exe'):
            ps_exe_path = 'C:/Program Files/Adobe/Adobe Photoshop 2022/Photoshop.exe'
        elif os.path.isfile('C:/Program Files/Adobe/Adobe Photoshop 2020/Photoshop.exe'):
            ps_exe_path = 'C:/Program Files/Adobe/Adobe Photoshop 2020/Photoshop.exe'
        elif os.path.isfile('C:/Program Files/Adobe/Adobe Photoshop CC 2019/Photoshop.exe'):
            ps_exe_path = 'C:/Program Files/Adobe/Adobe Photoshop CC 2019/Photoshop.exe'

        if ps_exe_path is None:
            return

        # ------------------------------
        # Photoshop起動
        ps_exe_dir_path = os.path.dirname(ps_exe_path)
        ps_exe_file_name = 'Photoshop.exe'
        jsx_script_path = ps_script_file_path.replace('/', '\\')

        subprocess.call(
            '{0} {1}'.format(ps_exe_file_name, jsx_script_path),
            shell=True,
            cwd=ps_exe_dir_path,
        )
