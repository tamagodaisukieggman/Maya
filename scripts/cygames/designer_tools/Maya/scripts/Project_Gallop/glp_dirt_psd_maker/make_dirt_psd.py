# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import os
import re
import glob
import subprocess

import maya.cmds as cmds
import maya.mel as mel

from . import blend_image

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility
from ..glp_chara_body_difference import body_difference

from .. import glp_common
from ..glp_common.classes.info import chara_info

reload(blend_image)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MakeDirt(object):

    # ==================================================
    def __init__(self):

        self.tmp_file_prefix = '__dirt__tmp__'
        self.tmp_file_suffix = '_dirt'
        self.file_format = 'tga'
        self.default_united_dirt_tex_name = 'united_dirt'

        self.adobe_root_path = 'C:/Program Files/Adobe'
        self.ps_exe_file_name = 'Photoshop.exe'
        self.ps_script_file_name = 'overwrite_psd_by_bmp.jsx'

        self.chara_info = None
        self.output_dir_path = None

        self.default_width = 1024
        self.default_height = 1024
        self.output_width = None
        self.output_height = None

        self.is_ready = False

    # ==================================================
    def __initialize(self):
        """初期化
        """

        self.is_ready = False

        # chara_info取得
        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info()

        # 出力サイズ取得
        self.output_width, self.output_height = self.__get_output_size()

        # 出力パスを取得
        self.output_dir_path = self.__get_output_dir_path()

        if not self.output_dir_path:
            return

        self.is_ready = True

    # ==================================================
    def __get_output_size(self):
        """出力サイズの確定
        キャラインフォのoptのPSDがあればそのサイズを、無ければデフォルト値を返す
        """

        output_width = self.default_width
        output_height = self.default_height

        if not self.chara_info.exists:
            return output_width, output_height

        psd_param_list = self.chara_info.part_info.psd_param_list

        for psd_param in psd_param_list:
            if psd_param['name'].find('_opt') >= 0:
                return int(psd_param['width'][0]), int(psd_param['height'][0])

        return output_width, output_height

    # ==================================================
    def __get_output_dir_path(self):
        """出力パスの確定
        あればsourceimagesを、なければmaと同階層を返す
        """

        this_scene_path = cmds.file(q=True, sn=True)
        source_image_path = this_scene_path.split('scenes')[0] + 'sourceimages'
        is_general_body = False

        # chara_infoから汎用衣装かどうかを判定
        if self.chara_info.exists:
            if self.chara_info.part_info.data_type == 'general_body':
                is_general_body = True

        if os.path.exists(source_image_path):
            # 汎用衣装はoptを出力先に指定
            if is_general_body and os.path.exists(source_image_path + '/opt'):
                return source_image_path + '/opt'
            else:
                return source_image_path

        else:
            if this_scene_path:
                return os.path.dirname(this_scene_path)
            else:
                return None

    # ==================================================
    def make_dirt_psd(self):
        """dirtテクスチャ作成
        """

        self.__initialize()

        if not self.is_ready:
            return

        # 各パーツごとにtmpテクスチャを出力
        transfer_pair_list = self.__get_pair_list()
        output_tmp_tex_list = []

        for transfer_pair in transfer_pair_list:

            result_tmp_tex_path = self.__output_transfer_tex(transfer_pair[1], transfer_pair[0])

            if not result_tmp_tex_path:
                continue

            output_tmp_tex_list.append(result_tmp_tex_path)

        # 統合ビットマップの出力
        blend_bmp_path = self.__output_blend_image(output_tmp_tex_list)

        # tmpテクスチャを削除
        if not os.path.exists(blend_bmp_path):
            cmds.warning('bmpの出力に失敗しました')
            return
        else:
            self.__delete_files(output_tmp_tex_list)

        # ビットマップからpsdの出力
        # 19/12/13 ここでMayaから出力したデータは不完全なので、ノード接続後Photoshopで再編集する
        psd_path = self.__convertToPsd(blend_bmp_path)

        # psdに接続
        if os.path.exists(psd_path):
            for transfer_pair in transfer_pair_list:
                self.__apply_tex(transfer_pair[0], psd_path)

        # Photoshopを起動してbmpの内容をpsdに反映
        self.__apply_bmp_to_psd_by_ps(blend_bmp_path)

    # ==================================================
    def __get_pair_list(self):

        result_pair_list = []
        not_reference_transform_list = cmds.ls('*', l=True, et='transform')

        for transform in not_reference_transform_list:

            # リファレンス込みで検索
            short_name = transform.split('|')[-1]
            target_list = cmds.ls(short_name, l=True, fl=True, r=True, et='transform')

            if len(target_list) < 2:
                continue

            reference_target_list = []

            for target in target_list:
                if target not in not_reference_transform_list:
                    reference_target_list.append(target)

            if reference_target_list:
                result_pair_list.append([transform, reference_target_list[0]])

        return result_pair_list

    # ==================================================
    def __output_transfer_tex(self, src_transform, dst_transform):

        if not cmds.objExists(src_transform) or not cmds.objExists(dst_transform):
            return

        dst_short_name = dst_transform.split('|')[-1]

        file_name = self.tmp_file_prefix + dst_short_name + self.tmp_file_suffix
        file_full_path = self.output_dir_path + '/' + file_name

        cmds.surfaceSampler(
            s=src_transform,
            t=dst_transform,
            uvSet='map1',
            mapOutput='diffuseRGB',
            filename=file_full_path,
            fileFormat=self.file_format,
            mapWidth=self.output_width,
            mapHeight=self.output_height,
            searchOffset=0,
            maxSearchDistance=0,
            searchCage='',
            max=1,
            mapSpace='tangent',
            shadows=True,
            mapMaterials=True,
            superSampling=True,
            filterType=0,
            filterSize=3,
            overscan=1,
            searchMethod=0,
            useGeometryNormals=True,
            ignoreTransforms=True,
            ignoreMirroredFaces=False,
            flipU=False,
            flipV=False
        )

        return file_full_path + '.' + self.file_format

    # ==================================================
    def __output_blend_image(self, target_path_list):

        path_list = target_path_list[:]

        output_dir_path = self.output_dir_path
        file_name = self.default_united_dirt_tex_name

        if self.chara_info.exists:

            texture_param_list = self.chara_info.part_info.texture_param_list

            for tex_param in texture_param_list:
                if tex_param['name'].find('_dirt') >= 0:
                    file_name = tex_param['name']
                    file_name = file_name.split('.')[0]

        output_full_path = '{0}/{1}.bmp'.format(output_dir_path, file_name)

        blend_main = blend_image.BlendImageByQt()
        blend_main.set_all_image(path_list)
        blend_main.set_blend_mode('lighten')
        return blend_main.blend(output_full_path)

    # ==================================================
    def __convertToPsd(self, input_path):

        if not os.path.exists(input_path):
            return

        input_ext = input_path.split('.')[-1]
        output_path = input_path.replace('.{}'.format(input_ext), '.psd')

        tmp_file_node = cmds.shadingNode('file', at=True, icm=True)
        cmds.setAttr('{}.fileTextureName'.format(tmp_file_node), input_path, typ='string')

        width = int(cmds.getAttr(tmp_file_node, '{}.outSizeX'.format(tmp_file_node)))
        height = int(cmds.getAttr(tmp_file_node, '{}.outSizeY'.format(tmp_file_node)))

        cmds.psdTextureFile(
            xr=width, yr=height, ifn=(input_path, 'dirt', 0), psf=output_path
        )

        if cmds.objExists(tmp_file_node):
            cmds.delete(tmp_file_node)

        cmds.psdEditTextureFile(psf=output_path, adc='test')

        if os.path.exists(output_path):
            return output_path

    # ==================================================
    def __apply_tex(self, transform, tex_path):

        if not cmds.objExists(transform):
            return

        material_list = base_utility.material.get_material_list(transform)

        if not material_list:
            return

        for material in material_list:

            this_file_node_info = cmds.listConnections("{}.color".format(material), type="file")

            if not this_file_node_info:
                continue

            cmds.setAttr('{}.fileTextureName'.format(this_file_node_info[0]), tex_path, typ='string')

    # ==================================================
    def __apply_bmp_to_psd_by_ps(self, bmp_path):
        """psdにbmpの絵を適用

        同名のbmpでpsdを上書くjsxを起動する
        """

        script_file_path = os.path.abspath(__file__)
        script_file_path = script_file_path.replace('\\', '/')
        script_dir_path = os.path.dirname(script_file_path)

        ps_script_file_path = script_dir_path + '/' + self.ps_script_file_name

        ps_exe_path = None

        for num in (reversed(list(range(30)))):

            # Phothoshop2020以降はフォルダ名に「CC」が付かなくなっている
            if num < 20:

                this_ps_exe_path = self.adobe_root_path + '/Adobe Photoshop CC 20{}/'.format(num) + self.ps_exe_file_name
                if os.path.isfile(this_ps_exe_path):
                    ps_exe_path = this_ps_exe_path
                    break

            else:

                this_ps_exe_path = self.adobe_root_path + '/Adobe Photoshop 20{}/'.format(num) + self.ps_exe_file_name
                if os.path.isfile(this_ps_exe_path):
                    ps_exe_path = this_ps_exe_path
                    break

        if not ps_exe_path:
            cmds.warning('Photoshop.exeのパスが見つかりません')
            return

        ps_exe_dir_path = os.path.dirname(ps_exe_path)

        subprocess.Popen(
            [self.ps_exe_file_name, bmp_path, ps_script_file_path],
            shell=True,
            cwd=ps_exe_dir_path,
        )

    # ==================================================
    def __delete_files(self, file_path_list):

        if not file_path_list:
            return

        for file_path in file_path_list:

            if not os.path.exists(file_path):
                continue

            os.remove(file_path)

    # ==================================================
    def __delete_nodes(self, node_list):

        if not node_list:
            return

        for node in node_list:

            if cmds.objExists(node):
                cmds.delete(node)
