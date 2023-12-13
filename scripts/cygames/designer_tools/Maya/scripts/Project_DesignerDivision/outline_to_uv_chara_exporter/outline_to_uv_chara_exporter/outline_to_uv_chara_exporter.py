# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from . import outline_to_uv_chara_exporter_item as exporter_item
from ..base_common import utility as base_utility
from . import create_full_body

try:
    from builtins import object
except Exception:
    pass


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class OutlineToUVCharaExporter(object):

    # ===============================================
    def __init__(self, target_file_path, logger, is_ascii=False, keep_temp_file=False, show_in_exprorer=False, root_node_prefix='', mesh_prefix='', is_combine_export=False):

        self.target_file_path = target_file_path

        self.logger = logger
        self.is_ascii = is_ascii
        self.keep_temp_file = keep_temp_file
        self.show_in_explorer = show_in_exprorer
        self.is_combine_export = is_combine_export

        self.root_node = None

        self.fix_export_target_list = None

        self.base_skin_info_list = None

        self.exporter_item_list = None

        self.temp_file_path = None

        # ルートノードの接頭辞
        self.root_node_prefix = root_node_prefix
        # ルートノード以下の対象メッシュ名の接頭辞
        self.mesh_prefix = mesh_prefix
        self.target_transform_list = []

    # ===============================================
    def initialize(self):

        self.root_node = self.get_root_node()
        if not self.root_node:
            self.logger.write_error(u'ルートノードが取得できませんでした')
            return False

        return True

    # ===============================================
    def get_root_node(self):

        root_node_list = []

        if not self.root_node_prefix:
            return None

        top_level_transform_node_list = cmds.ls(assemblies=True, l=True)
        for top_level_transform_node in top_level_transform_node_list:
            if top_level_transform_node.split('|')[-1].startswith(self.root_node_prefix):
                root_node_list.append(top_level_transform_node)

        if len(root_node_list) == 1:
            return root_node_list[0]

        return None

    # ===============================================
    def export(self):

        self.logger.write_log()
        self.logger.write_log('*****')
        self.logger.write_log(u'エクスポート')
        self.logger.write_log(u'{0}'.format(self.target_file_path))
        self.logger.write_log('*****')
        self.logger.write_log()

        self.logger.write_log()
        self.logger.write_log('++++')
        self.logger.write_log(u'一時ファイルを作成')
        self.logger.write_log('++++')
        self.logger.write_log()

        # tempファイル作成後、開く
        temp_file_path = \
            base_utility.file.open_temp(
                self.target_file_path,
                '____temp000_base_' + os.path.basename(self.target_file_path)
            )

        if temp_file_path is None:
            return

        # 頭部と身体一体化してデータチェックに回す
        if self.is_combine_export:
            if not create_full_body.create_full_body_scene():
                self.logger.write_error(u'頭部と身体の一体化に失敗しました')
                return

        # tempファイル読み込み後にイニシャライズ
        if not self.initialize():
            return

        # データチェック
        if not self.check_data():
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            return

        base_utility.file.save()

        if not self.keep_temp_file:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        export_item = exporter_item.OutlineToUVCharaExporterItem(
            self.target_file_path, self.target_transform_list, self.root_node, self.logger, self.is_ascii, self.keep_temp_file, self.show_in_explorer, self.is_combine_export)
        export_item.export()

        if self.show_in_explorer:
            # 一体化したデータはキャラのルートフォルダに出力される
            if self.is_combine_export:
                scene_dir = os.path.dirname(self.target_file_path)
                root_dir = os.path.dirname(os.path.dirname(scene_dir))
                base_utility.io.open_directory(root_dir)
            else:
                base_utility.io.open_directory(self.target_file_path)

    # ===============================================
    def check_data(self):

        is_export = self.initialize()
        if not is_export:
            self.logger.write_error(u'キャラの情報が取得できませんでした')
            return False

        self.logger.write_log()
        self.logger.write_log('++++')
        self.logger.write_log(u'エクスポートデータチェック')
        self.logger.write_log('++++')
        self.logger.write_log()

        if not os.path.isfile(self.target_file_path):
            self.logger.write_error(u'ファイルが見つかりません')
            return False

        self.fix_export_target_list = []
        self.fix_export_target_list.append(self.root_node)

        if len(self.fix_export_target_list) == 0:
            self.logger.write_error(u'エクスポート対象が見つかりません')
            return False

        self.target_transform_list = []

        for target in self.fix_export_target_list:

            transform_list = cmds.listRelatives(target, ad=True, ni=True, type='transform', f=True)

            for transform in transform_list:

                shape = cmds.listRelatives(transform, c=True, ni=True, s=True, typ='mesh', f=True)
                if not shape:
                    continue

                if not self.mesh_prefix or transform.split('|')[-1].startswith(self.mesh_prefix):
                    self.target_transform_list.append(transform)

        if not self.target_transform_list:
            self.logger.write_error(u'対象のメッシュが見つかりません')
            return False

        # マテリアルチェック
        for target_transform in self.target_transform_list:

            material_list = base_utility.material.get_material_list(target_transform)

            if not material_list:
                self.logger.write_error(u'{}にマテリアルが割りあたっていません'.format(target_transform))
                return False

            for material in material_list:
                if not cmds.objectType(material, i='lambert'):
                    self.logger.write_error(u'{}のマテリアルが正しくありません'.format(target_transform))
                    return False

        target_file_list = []

        if self.is_combine_export:
            part_path_dict = create_full_body.get_part_path_dict(create_full_body.get_part(os.path.basename(cmds.file(q=True, sn=True))))
            target_file_list = [os.path.basename(part_path_dict[key]) for key in part_path_dict]
        else:
            target_file_list = [os.path.basename(self.target_file_path)]

        self.logger.write_log(u'対象ファイル: {0}'.format(', '.join(target_file_list)))
        self.logger.write_log(u'対象オブジェクト: {0}'.format(self.fix_export_target_list))

        output_file_name = '{}.fbx'.format(os.path.splitext(os.path.basename(self.target_file_path))[0])
        if self.is_combine_export:
            output_file_name = '{}.fbx'.format(create_full_body.get_full_body_scene_name())

        self.logger.write_log(u'出力ファイル名: {0}'.format(output_file_name))

        transform_list = self.target_transform_list[:]
        if self.is_combine_export:
            transform_list.append(u'+ 他パーツのメッシュ')
        self.logger.write_log(u'\r\n処理対象メッシュ名:\r\n{0}'.format(',\r\n'.join(transform_list)))

        return True
