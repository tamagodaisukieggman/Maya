# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from importlib import reload
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

reload(chara_info)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EarTargetRenderer(object):

    # ===============================================
    def __init__(self):

        self.render_cam_name = '__ear_render_camera__'
        self.render_resolution = [1000, 1000]
        self.render_type = 'hardware2'
        self.render_global_node = 'defaultRenderGlobals'
        self.render_resolution_node = 'defaultResolution'
        self.hardware_render_global_node = 'hardwareRenderingGlobals'

        self.target_file_path = None
        self.target_file_name = None
        self.target_dir_path = None

        self.model_file_path = None

        self.chara_info = None

        self.is_checked = False

    # ===============================================
    def render(self, should_output_psd):

        self.is_checked = self.__check_data()

        if not self.is_checked:
            base_utility.logger.write('')
            base_utility.logger.write('データに不備がありました。処理を中断します')
            base_utility.logger.write('')
            return

        render_dir_path = self.chara_info.part_info.maya_root_dir_path + '/images/ear_target/' + self.chara_info.part_info.data_id

        render_target_dir_path = \
            render_dir_path + '/' + self.chara_info.part_info.data_id + '_target'

        # ------------------------------
        # レンダー設定

        self.set_render_setting()

        # ------------------------------
        # メッシュの表示設定

        self.__check_mesh_visibility()

        # ------------------------------
        # 耳
        this_target_info = target_info.TargetInfo()

        # this_target_info.info_item_list と
        # this_target_info.target_controller_info.info_item_list が作られる
        this_target_info.create_info_from_csv(
            'ear_target_info', 'ear_controller_info')

        this_target_info.update_info(False, True)

        # ------------------------------
        # レンダリング

        if os.path.isdir(render_target_dir_path):
            shutil.rmtree(render_target_dir_path)

        render = base_class.simple_render.SimpleRender()

        render.set_base_camera(self.render_cam_name)
        render.set_base_output_dir(render_dir_path)

        # TODO: csvにはLとRで分かれているので同じ耳のポーズが
        # 2回レンダリングされているのでcsvの中身を修正する？
        for info_item in this_target_info.info_item_list:

            label = info_item.label
            frame = info_item.frame
            index = info_item.index
            part = 'Ear'
            waku = 0

            render_file_name = \
                '{0}__{1}__{2}__{3}F__{4}__{5}'.format(
                    index, label, index, frame, part, waku)

            render.add_item(
                file_name=render_file_name,
                start_frame=frame,
            )

        title_file_name = \
            'title__{0}'.format(
                '【 耳のターゲット一覧 {0} 】'.format(self.chara_info.part_info.data_id))

        render.add_item(
            file_name=title_file_name,
            start_frame=0,
        )

        render.render()

        cmds.delete(self.render_cam_name)

        # ------------------------------
        # テンプレートのダウンロード

        if should_output_psd:
            server_dir_path = \
                '//cygames-fas01/100_projects/056_designer_tools/99_other/tools/cygame_designer_tools'

            template_file_path = server_dir_path + \
                '/sample/gallop/glp_chara_facial_tool/ear_target_template.psd'

            copy_file_path = \
                render_dir_path + '/' + self.chara_info.part_info.data_id + '_ear_target_tmp.psd'

            shutil.copy(template_file_path, copy_file_path)

            if not os.path.exists(copy_file_path):
                return

    # ===============================================
    def __check_data(self):
        # Memo: ボタン押した時にreset&g_is_print=Trueした方が良いのかも。
        # 元々ここだけbase_utility.logger使われていたのでここでしてます。
        base_utility.logger.reset()
        # 処理速度が落ちるなどの理由で出力したくないならFalseにしてください
        base_utility.logger.g_is_print = True
        # Asciiエラーになるのでコンソールへの日本語出力はshift-jisでする
        base_utility.logger.g_encode_type = "shift-jis"
        base_utility.logger.write()
        base_utility.logger.write_line()
        base_utility.logger.write('データチェック')
        base_utility.logger.write()

        self.target_file_path = cmds.file(q=True, sn=True)

        if not self.target_file_path:
            base_utility.logger.write('現在のMayaシーンパスが取得できませんでした')
            return False

        if self.target_file_path.find('_ear_target') < 0:
            base_utility.logger.write(
                '_ear_targetのシーンではありません: ' + str(self.target_file_path))
            return False

        self.target_file_path = \
            self.target_file_path.replace('\\', ' / ')

        self.target_file_name = os.path.basename(self.target_file_path)
        self.target_dir_path = os.path.dirname(self.target_file_path)

        model_file_name = base_utility.string.get_string_by_regex(
            self.target_file_name, 'mdl_.*_ear_target'
        )

        if not model_file_name:
            return False

        model_file_name = model_file_name.replace('_ear_target', '') + '.ma'

        self.model_file_path = \
            self.target_dir_path + '/' + model_file_name

        if not os.path.isfile(self.model_file_path):
            base_utility.logger.write('Error モデルファイルがありません: ' + self.model_file_path)
            return False

        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info(file_path=self.model_file_path)

        if not self.chara_info.exists:
            base_utility.logger.write('Error キャラInfoがありません')
            return False

        self.exporter = base_class.fbx_exporter.FbxExporter()

        base_utility.logger.write(
            'フォルダ : {0}'.format(self.target_dir_path))
        base_utility.logger.write(
            'ターゲット : {0}'.format(self.target_file_name))
        base_utility.logger.write(
            'モデル : {0}'.format(model_file_name))

        base_utility.logger.write_line()
        base_utility.logger.write()
        return True

    # ===============================================
    def __check_mesh_visibility(self):

        data_id = self.chara_info.part_info.data_id

        invisible_target_list = ['Cheek', 'Tear', 'Line', 'Outline']
        all_mesh_list = cmds.ls('mdl_{}|M_*'.format(data_id), r=True, l=True, fl=True, typ='transform')

        for mesh in all_mesh_list:

            is_visible = True

            for invisible_target in invisible_target_list:
                if mesh.find(invisible_target) >= 0:
                    is_visible = False
                    break

            if is_visible:
                cmds.setAttr(mesh + '.visibility', 1)
            else:
                cmds.setAttr(mesh + '.visibility', 0)

    # ===============================================
    def set_render_setting(self):

        ear_render_camera = cmds.camera(name=self.render_cam_name)[0]

        ear_render_camera = cmds.rename(ear_render_camera, self.render_cam_name)

        base_utility.attribute.set_value(
            ear_render_camera, 'orthographic', 1)

        base_utility.attribute.set_value(
            ear_render_camera, 'orthographicWidth', 42)

        base_utility.attribute.set_value(
            ear_render_camera, 'translate', [0, 20, 1000])

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
