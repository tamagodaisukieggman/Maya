# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    from importlib import reload
    from builtins import range
    from builtins import object
except Exception:
    pass

import os

import maya.cmds as cmds

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

reload(base_common)


# ===============================================
def main():

    main = Main()
    main.create_ui()


# ===============================================
def batch():

    main = Main()
    main.batch_export_tear()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ==================================================
    def __init__(self):

        self.tool_version = '20110501'
        self.tool_name = 'GlpTearExporter'

        self.window_name = self.tool_name + 'Win'

        # スクリプトのパス関連
        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.fbx_exporter = base_class.fbx_exporter.FbxExporter()

    # ==================================================
    def create_ui(self):

        self.ui_window = \
            base_class.ui.window.Window(
                self.window_name,
                self.tool_name + '  ' + self.tool_version,
                width=400, height=150
            )

        self.create_export_tear_ui()

        self.ui_window.show()

    # ==================================================
    def create_export_tear_ui(self):

        this_column = \
            cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            '涙モーション出力',
            self.export_tear_from_ui, False)

        cmds.frameLayout(label='涙モーション出力バッチ', cll=True, bv=True, cl=True, mw=10, mh=10)
        cmds.columnLayout(adj=True, rs=4)

        self.ui_export_tear_selector = \
            base_class.ui.data_selector.DataSelector(
                'ファイル', '', False, True)
        self.ui_export_tear_selector.set_path(
            'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/head')

        self.ui_export_tear_selector.set_file_filter(
            '_tear000_00', 'temp')
        self.ui_export_tear_selector.set_extension_filter('.ma')
        self.ui_export_tear_selector.set_contain_lower(True)

        base_class.ui.button.Button(
            '涙モーションをバッチ出力',
            self.export_tear_from_ui, True)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.separator(h=10)

        base_class.ui.button.Button(
            'ファイルリファレンス修正',
            self.fix_reference)

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True,
            parent=self.ui_window.ui_body_layout_id)

    # ==================================================
    def export_tear_from_ui(self, is_batch):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', '涙アニメーションfbxを出力しますか?',
                self.ui_window.ui_window_id):
            return

        target_file_path_list = \
            self.get_target_file_path_list_from_selector(
                self.ui_export_tear_selector, is_batch, True)

        if not target_file_path_list:
            return

        batch_command = \
            'import Project_Gallop.glp_tear_exporter.main;' + \
            'Project_Gallop.glp_tear_exporter.main.batch();'

        base_utility.simple_batch.execute(
            batch_command,
            False,
            target_file_path_list=target_file_path_list)

    # ==================================================
    def batch_export_tear(self):

        target_file_path_list = \
            base_utility.simple_batch.get_param_value(
                'target_file_path_list')

        if not target_file_path_list:
            return

        for target_file_path in target_file_path_list:

            tear_attach_position = self._get_tear_attach_position_from_mdl(target_file_path)
            if not tear_attach_position:
                continue

            base_utility.file.open(target_file_path)

            self.export_tear(tear_attach_position)

            if target_file_path.find('____temp') >= 0:

                cmds.file(save=True)
                os.remove(target_file_path)

    # ==================================================
    def _get_tear_attach_position_from_mdl(self, file_path):
        """
        """

        tear_attach_potision = []

        # 元のモデル名を抽出
        original_mdl = file_path.replace('_tear000_00', '').replace('____temp_', '')
        if os.path.exists(original_mdl):

            cmds.file(original_mdl, open=True, f=True)

            tear_attach_locator = base_utility.node.search('Eye_tear_attach_03_L', None, 'transform')
            if tear_attach_locator:
                tear_attach_potision = cmds.xform(tear_attach_locator, ws=True, t=True, q=True)

            cmds.file(new=True, f=True)

        return tear_attach_potision

    # ==================================================
    def export_tear(self, base_position):

        # パス確認

        current_path = cmds.file(q=True, sn=True)

        if not current_path:
            cmds.warning('ファイルが開かれていません')
            return

        dir_path = \
            os.path.dirname(current_path)

        file_name = \
            os.path.basename(current_path)

        file_name_noext, file_ext = \
            os.path.splitext(file_name)

        # モデル確認

        model_transform = \
            base_utility.node.search(
                'mdl_chr_tear\d{3}$', None, 'transform')

        info_transform = \
            base_utility.node.search(
                'mdl_chr_tear\d{3}_info$', None, 'transform')

        if not model_transform:
            cmds.warning('涙モデルが見つかりません')
            return

        if not info_transform:
            cmds.warning('涙情報が見つかりません')
            return

        # フレーム確認

        start_frame = \
            base_utility.attribute.get_value(
                info_transform, 'startFrame', None)
        end_frame = \
            base_utility.attribute.get_value(
                info_transform, 'endFrame', None)

        if start_frame is None:
            start_frame = \
                cmds.playbackOptions(q=True, ast=True)

        if end_frame is None:
            end_frame = \
                cmds.playbackOptions(q=True, aet=True)

        # 複製

        duplicate_name = \
            file_name_noext.replace('mdl_', 'anm_')
        duplicate_name = \
            duplicate_name.replace('____temp_', '')

        cmds.select(model_transform, r=True)
        duplicate_list = \
            cmds.duplicate(
                rr=True, instanceLeaf=True, un=True, name=duplicate_name)

        if not duplicate_list:
            cmds.warning('複製を作成できません')
            return

        # ノード確定

        duplicate_transform = \
            duplicate_list[0]

        joint_transform = \
            base_utility.node.search(
                'joint000',
                duplicate_transform.replace('|', '\|'),
                'transform')

        if not joint_transform:
            cmds.warning('ジョイントが見つかりません')
            return

        # ベイク

        cmds.bakeResults(
            [joint_transform],
            simulation=True,
            time=(start_frame, end_frame),
            hierarchy='below',
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
            shape=True)

        # コンストレイン削除

        cmds.select(joint_transform, r=True)
        cmds.select(hi=True)

        this_const_list = \
            cmds.ls(sl=True, l=True, typ='constraint')

        if this_const_list:

            unparent_list = \
                cmds.parent(this_const_list, w=True)

            if unparent_list:
                cmds.delete(unparent_list)

        # メッシュ削除

        mesh_list = \
            base_utility.node.search(
                'M_', duplicate_transform.replace('|', '\|'))

        if mesh_list:
            cmds.delete(mesh_list)

        # オフセット

        position_diff_info_list = []

        for frame in range(start_frame, end_frame + 1):

            current_position = \
                base_utility.attribute.get_value_from_frame(
                    joint_transform, 'translate', frame)

            position_diff = \
                base_utility.vector.sub(
                    current_position, base_position)

            position_diff_info_list.append([frame, position_diff])

        # オフセットでキー作成

        for position_diff_info in position_diff_info_list:

            base_utility.attribute.set_key(
                joint_transform, 'translate',
                position_diff_info[1], position_diff_info[0])

        # タイムラインの設定

        cmds.playbackOptions(ast=start_frame)
        cmds.playbackOptions(aet=end_frame)

        cmds.playbackOptions(min=start_frame)
        cmds.playbackOptions(max=end_frame)

        # FBX出力

        fbx_file_path = \
            os.path.join(dir_path, duplicate_name + '.fbx')

        fbx_file_path = \
            fbx_file_path.replace('\\', '/')

        self.fbx_exporter.reset()

        self.fbx_exporter.fbx_file_path = \
            fbx_file_path

        self.fbx_exporter.target_node_list = \
            [duplicate_transform]

        self.fbx_exporter.export()

    # ==================================================
    def get_target_file_path_list_from_selector(
            self, selector, is_batch, is_create_temp):

        target_file_path_list = None

        if is_batch:

            target_file_path_list = \
                selector.get_data_path_list()

        else:

            current_file_path = cmds.file(q=True, sn=True)

            if not current_file_path:
                return

            target_file_path = current_file_path

            if is_create_temp:

                temp_file_path = \
                    base_utility.file.create_temp(
                        current_file_path)

                if not temp_file_path:
                    return

                target_file_path = temp_file_path

            target_file_path_list = \
                [target_file_path.replace('\\', '')]

        return target_file_path_list

    # ==================================================
    def fix_reference(self):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'リファレンスを修正しますか?',
                self.ui_window.ui_window_id):
            return

        chara_dir_path = \
            'W:\\gallop\\svn\\svn_gallop\\80_3D\\01_character\\01_model'

        if not os.path.isdir(chara_dir_path):
            cmds.warning('{0} がありません'.format(chara_dir_path))
            return

        current_file_path = \
            cmds.file(q=True, sn=True)

        if not current_file_path:
            cmds.warning('ファイルが開かれていません')
            return

        current_dir_path = \
            os.path.dirname(current_file_path)

        current_file_name = \
            os.path.basename(current_file_path)

        current_file_name_noext, current_file_ext = \
            os.path.splitext(current_file_name)

        chara_face_id = \
            base_utility.string.get_string_by_regex(
                current_file_name, 'chr\d{4}_\d{2}(_face\d{3}|)')

        if not chara_face_id:
            cmds.warning('{0} からキャラIDを特定できません'.format(current_file_name))
            return

        tear_id = \
            base_utility.string.get_string_by_regex(
                current_file_name, 'tear\d{3}')

        if not tear_id:
            cmds.warning('{0} から涙IDを特定できません'.format(current_file_name))
            return

        tear_anim_file_name = \
            'mdl_chr_{}_anim'.format(tear_id)

        tear_anim_file_path = \
            '{0}\\common\\tear\\{1}\\scenes\\{2}.ma'.format(
                chara_dir_path, tear_id, tear_anim_file_name)

        if not os.path.isfile(tear_anim_file_path):
            cmds.warning('{0} がありません'.format(tear_anim_file_path))
            return

        facial_target_fbx_file_path = \
            current_dir_path + '\\mdl_{0}_facial_target.fbx'.format(chara_face_id)

        if not os.path.isfile(facial_target_fbx_file_path):
            cmds.warning('{0} がありません'.format(facial_target_fbx_file_path))
            return

        # facial_targetのリファレンスを削除

        reference_file_path_list = \
            cmds.file(q=True, r=True)

        if reference_file_path_list:

            for file_path in reference_file_path_list:

                if file_path.find('_facial_target') < 0:
                    continue

                try:
                    cmds.file(file_path, rr=True)
                except:
                    pass

        # 再度リファレンス取得

        reference_file_path_list = \
            cmds.file(q=True, r=True)

        # 涙のリファレンス

        if tear_anim_file_path.replace('\\', '/') not in reference_file_path_list:

            cmds.file(
                tear_anim_file_path,
                ignoreVersion=True,
                ns=tear_anim_file_name,
                r=True,
                mergeNamespacesOnClash=False
            )

        # facial_targetのリファレンス

        if facial_target_fbx_file_path.replace('\\', '/') not in reference_file_path_list:

            cmds.file(
                facial_target_fbx_file_path,
                ignoreVersion=True,
                ns=chara_face_id,
                r=True,
                mergeNamespacesOnClash=False
            )

        # タイムの設定

        cmds.currentUnit(time='ntsc')

        info_transform = \
            base_utility.node.search(
                'mdl_chr_tear\d{3}_info$', None, 'transform')

        start_frame = \
            base_utility.attribute.get_value(
                info_transform, 'startFrame', None)

        end_frame = \
            base_utility.attribute.get_value(
                info_transform, 'endFrame', None)

        if start_frame is None:
            start_frame = 0

        if end_frame is None:
            end_frame = 150

        cmds.playbackOptions(ast=start_frame)
        cmds.playbackOptions(aet=end_frame)

        cmds.playbackOptions(min=start_frame)
        cmds.playbackOptions(max=end_frame)

        cmds.currentTime(0)

        # メッシュなどの表示、非表示

        face_mesh = \
            base_utility.node.search(
                'M_Face', chara_face_id)

        base_utility.attribute.set_value(
            face_mesh, 'visibility', True)

        hair_mesh = \
            base_utility.node.search(
                'M_Hair', chara_face_id)

        base_utility.attribute.set_value(
            hair_mesh, 'visibility', False)

        cheek_mesh = \
            base_utility.node.search(
                'M_Cheek', chara_face_id)

        base_utility.attribute.set_value(
            cheek_mesh, 'visibility', False)

        mayu_mesh = \
            base_utility.node.search(
                'M_Mayu', chara_face_id)

        base_utility.attribute.set_value(
            mayu_mesh, 'visibility', False)

        tear_mesh_list = \
            base_utility.node.search_list(
                'M_Tear_', chara_face_id, 'transform')

        if tear_mesh_list:

            for tear_mesh in tear_mesh_list:

                base_utility.attribute.set_value(
                    tear_mesh, 'visibility', False)

        # スキンエンベロープの無効

        if face_mesh:

            face_mesh_skincluster = \
                base_utility.mesh.skin.get_skin_cluster(face_mesh)

            base_utility.attribute.set_value(
                face_mesh_skincluster, 'envelope', 0)

        # 保存
        cmds.file(save=True)

        print('{0} のリファレンスを設定'.format(current_file_path))