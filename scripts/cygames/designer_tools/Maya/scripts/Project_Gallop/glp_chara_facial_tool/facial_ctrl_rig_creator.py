# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import os
import re
from datetime import datetime

import maya.cmds as cmds
import maya.mel as mel

from ..base_common import utility as base_utility

from . import target_info

from . import cheek_driven_key_creator

from . import blend_target_info

from . import eye_driven_key_creator


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialCtrlRigCreator(object):

    file_info_key_list = [
        'GallopFacialTool_FacialTargetLastModified',
        'GallopFacialTool_HeadModelLastModified',
        'GallopFacialTool_EarTargetLastModified',
    ]
    date_format = '%a, %b %d, %Y %I:%M:%S %p'

    # ===============================================
    def __init__(self):

        self.target_file_path = None
        self.target_file_name = None
        # 「フォルダ」テキストフィールドに入力されたフォルダパス
        self.target_dir_path = None

        # 「80_3D」フォルダへのパス(「3Dの」root)
        self.root_dir_path = None

        self.ctrl_rig_file_path = None

        self.model_file_path = None

        self.model_root_dir_path = None

        self.scenes_dir_path = None

        self.sourceimage_dir_path = None

        self.facial_target_file_path = None
        self.facial_target_xml_path = None

        self.ear_target_file_path = None
        self.ear_target_xml_path = None

        self.facial_rig_file_path = None

        self.file_id = None

        self.is_check_path = False

    @classmethod
    def get_target_update_state(cls, target_file_path, folder_path):
        """facial_targetの更新状態を返す

        Args:
            target_file_path (str): 処理対象のファイルパス（UIの「フォルダ」パス配下でmainで既に検索されたもの）
            folder_path (str): UIにユーザーが入力したフォルダパス

        Returns:
            str: 更新状態
        """

        if not folder_path:
            return 'エラー'

        if not target_file_path or not os.path.isfile(target_file_path):
            return 'エラー'

        if '_facial_target' not in target_file_path:
            return 'エラー'

        target_file_path = target_file_path.replace('\\', '/')
        target_file_name = os.path.basename(target_file_path)
        folder_path = folder_path.replace('\\', '/')

        root_dir_path = None
        root_dir_match = re.match('.*80_3D', folder_path)
        if root_dir_match:
            root_dir_path = root_dir_match.group()

        if not root_dir_path:
            return 'エラー'

        file_id = base_utility.string.get_string_by_regex(target_file_name, r'chr\d{4}_\d{2}')

        if not file_id:
            return 'エラー'

        # Ctrl_RIG
        ctrl_rig_file_name = 'md_{0}_Ctrl_RIG.ma'.format(file_id)
        ctrl_rig_dir_name = re.sub(r'\d{2}$', '00', file_id)
        ctrl_rig_file_path = root_dir_path + '/03_motion/Chara/' + ctrl_rig_dir_name + '/' + ctrl_rig_file_name

        if not os.path.isfile(ctrl_rig_file_path):
            return 'RIG未作成'

        target_dir_path = os.path.dirname(target_file_path)

        # Model
        model_file_name = 'mdl_{0}.ma'.format(file_id)
        model_file_path = target_dir_path + '/' + model_file_name

        if not os.path.isfile(model_file_path):
            return 'エラー'

        # ear_target
        ear_target_file_name = 'mdl_{0}_ear_target.ma'.format(file_id)
        ear_target_file_path = target_dir_path + '/' + ear_target_file_name

        target_modified_date = cls.get_scene_modified_date(target_file_path)
        if not target_modified_date:
            return 'エラー'

        model_modified_date = cls.get_scene_modified_date(model_file_path)
        if not model_modified_date:
            return 'エラー'

        # ear_targetは非ウマ耳キャラには存在しないためエラーにしない
        ear_target_modified_date = cls.get_scene_modified_date(ear_target_file_path)

        # file_info_key_listに合わせfacial_target、Headモデル、ear_targetの順
        current_modified_dates = [target_modified_date, model_modified_date, ear_target_modified_date]

        rig_modified_dates = cls.get_facial_target_modified_dates(ctrl_rig_file_path)
        if not rig_modified_dates:
            return '日時未保存'

        if any(cls.is_updated(current_date, rig_date) for current_date, rig_date in zip(current_modified_dates, rig_modified_dates)):
            return '更新有り'

        return '最新'

    @classmethod
    def is_updated(cls, current_date, saved_date):
        """current_dateがsaved_dateより新しい日付かどうかを返す

        Args:
            current_date (datetime): 現在の日時
            saved_date (datetime): 保存されている日時

        Returns:
            bool: current_dateがsaved_dateより新しい日付か
        """

        if current_date is None and saved_date is None:
            return False
        if (current_date is None) ^ (saved_date is None):
            return True
        return current_date > saved_date

    # ===============================================
    def create(self, target_file_path, folder_path):
        """
        target_file_path: 処理対象のファイルパス（UIの「フォルダ」パス配下でmainで既に検索されたもの）
        folder_path: UIにユーザーが入力したフォルダパス
        """
        self.target_file_path = target_file_path
        self.target_dir_path = folder_path

        self.is_check_path = self.__check_path()

        if not self.is_check_path:
            return

        self.__export_facial_target_xml()
        self.__export_ear_target_xml()

        self.__create_ctrl_rig_base()

        self.__delete_all_animation_layer()

        self.__clear_facial_key()

        self.__relink_cheek_for_maya_texture()

        self.__create_cheek_driven_key()
        self.__create_facial_target_driven_key()
        # self.__create_facial_blend_target_driven_key()  # 旧フェイシャルリグ用処理のため不要と思われるが一応コメントアウトで残しておく
        self.__create_ear_driven_key()

        self.__add_attr_to_cheek_ctrl()

        self.__set_parent_constraint()

        self.__set_visibility()

        self.__reset_mesh_display()

        self.__optimize_scene()

        self.__save_modified_date()

        base_utility.file.save(self.ctrl_rig_file_path, True)
        # 出力したフォルダを開く
        os.startfile(os.path.dirname(self.ctrl_rig_file_path))

    # ===============================================
    def __check_path(self):

        if not self.target_dir_path:
            cmds.warning("フォルダパスが取得できませんでした")
            return False

        if not self.target_file_path or not os.path.isfile(self.target_file_path):
            cmds.warning("Mayaシーンパスが取得できませんでした")
            return False

        if self.target_file_path.find('_facial_target') < 0 and \
                self.target_file_path.find('_Ctrl_RIG') < 0:
            cmds.warning("「_facial_target」か「_Ctrl_RIG」のシーンが対象です")
            return False

        self.target_file_path = self.target_file_path.replace('\\', '/')
        self.target_file_name = os.path.basename(self.target_file_path)
        self.target_dir_path = self.target_dir_path.replace('\\', '/')

        # --------------------------------
        # ルートフォルダの検索

        self.root_dir_path = None

        temp_root_dir_path = os.path.dirname(self.target_dir_path)

        for count in range(20):

            temp_root_dir_path = os.path.dirname(temp_root_dir_path)

            if temp_root_dir_path.endswith('80_3D'):
                self.root_dir_path = temp_root_dir_path
                break

        if not self.root_dir_path:
            return False

        # --------------------------------
        # ファイル名

        self.file_id = base_utility.string.get_string_by_regex(
            self.target_file_name, 'chr\d{4}_\d{2}')

        if not self.file_id:
            return False

        model_dir_name = self.file_id

        model_file_name = \
            'mdl_{0}.ma'.format(self.file_id)

        ctrl_rig_file_name = 'md_{0}_Ctrl_RIG.ma'.format(self.file_id)
        facial_target_file_name = \
            'mdl_{0}_facial_target.ma'.format(self.file_id)
        ear_target_file_name = \
            'mdl_{0}_ear_target.ma'.format(self.file_id)

        # --------------------------------
        # Model

        temp_file_list = base_utility.io.get_data_path_list(
            self.target_dir_path, False, model_file_name, None, '.ma', None, None, True
        )

        if temp_file_list:
            self.model_file_path = temp_file_list[0]

        # --------------------------------
        # Model Directory

        temp_dir_list = base_utility.io.get_data_path_list(
            self.target_dir_path, True, model_dir_name, None, None, None, None, True
        )

        if temp_dir_list:
            self.model_root_dir_path = temp_dir_list[0]
            self.scenes_dir_path = self.model_root_dir_path + '/scenes'
            self.sourceimage_dir_path = self.model_root_dir_path + '/sourceimages'

        # --------------------------------
        # Ctrl_RIG
        ctrl_rig_dir_name = re.sub(r'\d{2}$', '00', self.file_id)
        self.ctrl_rig_file_path = self.root_dir_path + '/03_motion/Chara/' + ctrl_rig_dir_name + '/' + ctrl_rig_file_name

        # --------------------------------
        # facial_target

        temp_file_list = base_utility.io.get_data_path_list(
            self.target_dir_path, False, facial_target_file_name, '', '.ma', None, None, True
        )

        if temp_file_list:
            self.facial_target_file_path = temp_file_list[0]
            self.facial_target_xml_path = \
                self.facial_target_file_path.replace('.ma', '.xml')

        # --------------------------------
        # ear_target

        temp_file_list = base_utility.io.get_data_path_list(
            self.target_dir_path, False, ear_target_file_name, '', 'ma', None, None, True
        )

        if temp_file_list:
            self.ear_target_file_path = temp_file_list[0]
            self.ear_target_xml_path = \
                self.ear_target_file_path.replace('.ma', '.xml')

        # --------------------------------
        # facial_rig

        temp_file_list = base_utility.io.get_data_path_list(
            self.root_dir_path + "/03_motion/00_scenes/RIG", False, '_faicialRig2', '', 'ma', None, None, True
        )

        if temp_file_list:
            self.facial_rig_file_path = temp_file_list[0]

        return True

    # ==================================================
    def __export_facial_target_xml(self):

        if not self.facial_target_file_path:
            return

        if not os.path.isfile(self.facial_target_file_path):
            return

        base_utility.file.open(self.facial_target_file_path)

        this_target_info = target_info.TargetInfo()

        this_target_info.create_info_from_csv(
            'facial_target_info', 'facial_controller_info')

        this_target_info.target_controller_info.controller_root_name = 'Rig_head|Rig_eye_high'
        this_target_info.target_controller_info.target_root_name = 'Neck'

        this_target_info.update_info(True, True)

        this_target_info.write_xml(
            os.path.basename(self.facial_target_xml_path), None)

    # ==================================================
    def __export_ear_target_xml(self):

        if not self.ear_target_file_path:
            return

        if not os.path.isfile(self.ear_target_file_path):
            return

        base_utility.file.open(self.ear_target_file_path)

        this_target_info = target_info.TargetInfo()

        this_target_info.create_info_from_csv(
            'ear_target_info', 'ear_controller_info')

        this_target_info.target_controller_info.controller_root_name = 'Rig_ear'
        this_target_info.target_controller_info.target_root_name = 'Neck'

        this_target_info.update_info(True, True)

        this_target_info.write_xml(
            os.path.basename(self.ear_target_xml_path), None)

    # ===============================================
    def __create_ctrl_rig_base(self):

        base_utility.file.open(self.facial_target_file_path)

        ref_namespace_list = base_utility.reference.get_reference_namespace_list()

        if ref_namespace_list:

            base_utility.reference.change_reference_file_path_by_namespace(
                ref_namespace_list[0], self.model_file_path)

            base_utility.reference.import_reference_by_namespace(
                ref_namespace_list[0]
            )

        cmds.file(self.facial_rig_file_path, i=True, f=True)

        cmds.playbackOptions(min=0, max=30, ast=0, aet=30)

    # ==================================================
    def __create_cheek_driven_key(self):

        this_cheek_driven_key_creator = \
            cheek_driven_key_creator.CheekDrivenKeyCreator()
        this_cheek_driven_key_creator.create()

    # ==================================================
    def __create_facial_target_driven_key(self):

        if not self.facial_target_xml_path:
            return

        if not os.path.isfile(self.facial_target_xml_path):
            return

        this_target_info = target_info.TargetInfo()

        this_target_info.create_info_from_csv(
            'facial_target_info', 'facial_controller_info')

        this_target_info.target_controller_info.controller_root_name = 'Rig_head|Rig_eye_high'
        this_target_info.target_controller_info.target_root_name = 'Neck'
        this_target_info.target_controller_info.driver_root_name = 'facial_Ctrl'

        this_target_info.update_info_from_xml(
            self.facial_target_xml_path)

        this_target_info.delete_driven_key()

        this_target_info.create_driven_key(True)

        # ------------------------------
        # 目のドリブンキー設定
        this_eye_driven_key_creator = \
            eye_driven_key_creator.EyeDrivenKeyCreator(
                this_target_info)
        this_eye_driven_key_creator.create_driven_key()

    # ==================================================
    def __create_facial_blend_target_driven_key(self):

        if not self.facial_target_xml_path:
            return

        if not os.path.isfile(self.facial_target_xml_path):
            return

        this_target_info = target_info.TargetInfo()

        this_target_info.create_info_from_csv(
            'facial_target_info', 'facial_controller_info')

        for info_item in this_target_info.target_controller_info.info_item_list:

            if not info_item.driver_name:
                continue

            info_item.driver_name = info_item.driver_name.replace(
                '_Base_', '_')

        this_target_info.target_controller_info.controller_root_name = 'Rig_head|Rig_eye_high'
        this_target_info.target_controller_info.target_root_name = 'Neck'
        this_target_info.target_controller_info.driver_root_name = 'facial_Ctrl'

        this_target_info.update_info_from_xml(
            self.facial_target_xml_path)

        this_blend_target_info = blend_target_info.BlendTargetInfo()
        this_blend_target_info.create_info_from_csv(
            this_target_info, 'facial_blend_info')

        this_blend_target_info.update_info(True, True)

        this_blend_target_info.delete_driven_key()

        this_blend_target_info.create_driven_key(True)

    # ==================================================
    def __create_ear_driven_key(self):

        if not self.ear_target_xml_path:
            return

        if not os.path.isfile(self.ear_target_xml_path):
            return

        this_target_info = target_info.TargetInfo()

        this_target_info.create_info_from_csv(
            'ear_target_info', 'ear_controller_info')

        this_target_info.target_controller_info.controller_root_name = 'Rig_ear'
        this_target_info.target_controller_info.target_root_name = 'Neck'
        this_target_info.target_controller_info.driver_root_name = 'facial_Ctrl'

        this_target_info.update_info_from_xml(self.ear_target_xml_path)

        this_target_info.delete_driven_key()
        this_target_info.create_driven_key(False)

    # ==================================================
    def __delete_all_animation_layer(self):

        animation_layer_list = cmds.ls(typ='animLayer', l=True, r=True)

        if not animation_layer_list:
            return

        for animation_layer in animation_layer_list:

            if animation_layer == 'BaseAnimation':
                continue

            if not cmds.animLayer(animation_layer, q=True, exists=True):
                continue

            cmds.delete(animation_layer)

    # ==================================================
    def __clear_facial_key(self):

        cmds.currentTime(0)

        cmds.select(clear=True)

        if cmds.objExists('Rig_head'):
            cmds.select('Rig_head', add=True)

        if cmds.objExists('Rig_eye_high'):
            cmds.select('Rig_eye_high', add=True)

        cmds.select(hi=True)

        target_transform_list = cmds.ls(sl=True, l=True, typ='transform')

        if not target_transform_list:
            return

        target_attr_list = [
            'tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'
        ]

        for target_transform in target_transform_list:

            for target_attr in target_attr_list:

                self.__cut_keyframe(target_transform, target_attr,
                                    0, 100000)

    # ==================================================
    def __cut_keyframe(self, target_node, target_attribute, start_frame, end_frame):

        if not target_node:
            return

        if not target_attribute:
            return

        keyframe_list = cmds.keyframe(target_node,
                                      q=True, attribute=target_attribute,
                                      timeChange=True, absolute=True)

        if not keyframe_list:
            return

        current_value = base_utility.attribute.get_value(
            target_node, target_attribute)

        cmds.cutKey(
            target_node,
            attribute=target_attribute, time=(start_frame, end_frame))

        base_utility.attribute.set_value(
            target_node, target_attribute, current_value)

    # ==================================================
    def __set_parent_constraint(self):

        this_hit_list = [
            ['Rig_head\|.*Neck_Ctrl$', '\|.*Neck$'],
            ['Rig_head\|.*Head_Ctrl$', 'Neck\|.*Head$'],
        ]

        transform_list = cmds.ls(typ='transform', l=True, r=True)

        if not transform_list:
            return

        for hit in this_hit_list:

            parent_transform = None
            child_transform = None

            for trans in transform_list:

                if re.search(hit[0], trans):
                    parent_transform = trans
                    break

            if not parent_transform:
                continue

            for trans in transform_list:

                if re.search(hit[1], trans):
                    child_transform = trans
                    break

            if not child_transform:
                continue

            cmds.parentConstraint(parent_transform, child_transform)

    # ==================================================
    def __set_visibility(self):

        visibility_info_list = [
            {'name': 'M_.*_Outline$', 'visibility': False, 'delete': True},
            {'name': 'Rig_eye_high', 'visibility': False, 'delete': False},
            {'name': 'Rig_head', 'visibility': False, 'delete': False},
            {'name': 'M_Tear_(L|R)', 'visibility': False, 'delete': False},
            {'name': 'M_Line', 'visibility': False, 'delete': False},
            {'name': 'M_Face', 'visibility': True, 'delete': False},
            {'name': 'M_Hair', 'visibility': True, 'delete': False},
            {'name': 'M_Cheek', 'visibility': True, 'delete': False},
            {'name': 'M_Mayu', 'visibility': True, 'delete': False},
        ]

        for this_info in visibility_info_list:

            this_name = this_info['name']

            hit_list = base_utility.node.search_list(
                this_name, None, None
            )

            if not hit_list:
                continue

            this_visibility = this_info['visibility']
            this_delete = this_info['delete']

            for hit in hit_list:

                if this_delete:

                    cmds.delete(hit)
                    continue

                base_utility.attribute.set_value(
                    hit, 'visibility', this_visibility
                )

    # ==================================================
    def __reset_mesh_display(self):

        this_hit_list = ['M_']

        transform_list = cmds.ls(typ='transform', l=True, r=True)

        if not transform_list:
            return

        for trans in transform_list:

            is_hit = False
            for hit in this_hit_list:

                if re.search(hit, trans):
                    is_hit = True
                    break

            if not is_hit:
                continue

            this_mesh = base_utility.mesh.get_mesh_shape(trans)

            if not this_mesh:
                continue

            cmds.select(trans, r=True)
            mel.eval('PolyDisplayReset;')

            base_utility.attribute.set_value(
                this_mesh, 'displayColors', 0
            )

    # ==================================================
    def __optimize_scene(self):

        for _ in range(3):

            # なぜ、3回もクリーンアップしているのかわからないが、何かの対処のためかもしれないので放置する
            cmds.optionVar(iv=('deformerOption', 1))
            cmds.optionVar(iv=('unknownNodesOption', 1))
            cmds.optionVar(iv=('animationCurveOption', 1))

            # 以下の値を設定しておくとクリーンアップ時にクリーンアップしますか?と聞かれずに済む
            os.environ["MAYA_TESTING_CLEANUP"] = "1"

            mel.eval('OptimizeScene;')

        del os.environ["MAYA_TESTING_CLEANUP"]

        if cmds.objExists('imagePlane*'):
            cmds.delete('imagePlane*')

        if cmds.objExists('|left'):
            cmds.delete('|left')

        # ジョイントセグメントスケール設定
        bones = cmds.ls(typ='joint')
        for bone in bones:
            cmds.setAttr('{}.segmentScaleCompensate'.format(bone), 0)

        # BaseAnimation削除
        if cmds.objExists('BaseAnimation'):
            cmds.delete('BaseAnimation')

        # workデータ削除
        if cmds.objExists('*:work'):
            cmds.delete('*:work')

        # HeadボーンのInverseScale接続を切る
        attrs = cmds.listConnections('*:Head.inverseScale', p=True)
        if attrs:
            for attr in attrs:
                cmds.disconnectAttr(attr, '*:Head.inverseScale')

        # unknownノード削除
        unknown_nodes = cmds.ls(typ=('unknown', 'unknownDag', 'unknownTransform'))
        if unknown_nodes:
            cmds.delete(unknown_nodes)

        unknown_plugins = cmds.unknownPlugin(q=True, l=True)
        if unknown_plugins:
            for unknown_plugin in unknown_plugins:
                try:
                    cmds.unknownPlugin(unknown_plugin, r=True)
                except Exception:
                    pass

        # 耳なしキャラのリグ削除
        ear_ctrl_sets = [
            ('Ear_01_R_Ctrl', 'Ear_01_R_Ctrl.Base'),
            ('Ear_02_R_Ctrl', 'Ear_02_R_Ctrl.Base'),
            ('Ear_03_R_Ctrl', 'Ear_03_R_Ctrl.Base'),
            ('Ear_01_L_Ctrl', 'Ear_01_L_Ctrl.Base'),
            ('Ear_02_L_Ctrl', 'Ear_02_L_Ctrl.Base'),
            ('Ear_03_L_Ctrl', 'Ear_03_L_Ctrl.Base'),
        ]

        for ctrl, base in ear_ctrl_sets:
            if cmds.objExists(ctrl) and not cmds.objExists(base):
                cmds.delete(ctrl)

        # スケールコンストレインする
        cmds.scaleConstraint('Rig_head', '*:Neck')

        # ポリゴン表示をデフォルトにする
        meshes = ['*:M_Face', '*:M_Cheek', '*:M_Hair', '*:M_Mayu']
        for mesh in meshes:
            if cmds.objExists(mesh):
                cmds.polyOptions(mesh, dv=False, se=True, dcv=True, duv=False, dn=False, dmb=False, dc=False)

        # 不要なノードを削除
        delete_nodes = [
            '*:NeckEdgeSet',
            '*RNfosterParent*',
            'charaLight0',
            '*:bake_model',
            '*:backup',
            'group1',
            '____charaLightRig',
            'M_Face_normal_template',
            '_faicialRig2_facial_Ctrl',
            '*:*Face_normal_template',
        ]

        for delete_node in delete_nodes:
            if cmds.objExists(delete_node):
                cmds.delete(delete_node)

        # Neckを表示する
        necks = cmds.ls('*:Neck')
        for neck in necks:
            cmds.setAttr('{}.visibility'.format(neck), 1)

        # 不要なカメラを削除
        keep_cameras = ['sideShape', 'perspShape', 'topShape', 'frontShape']
        delete_cameras = [camera for camera in cmds.ls(typ='camera') if camera not in keep_cameras]
        for delete_camera in delete_cameras:
            delete_transform = cmds.listRelatives(delete_camera, p=True)[0]
            cmds.delete(delete_transform)

        # ロケーターを非表示にする
        locator_names = [
            '*:Mouth_Root',
            '*:Cheek_offset_L',
            '*:Cheek_offset_R',
            '*:Eyebrow_offset_R',
            '*:Eyebrow_offset_L',
            '*:Eye_target_locator_L',
            '*:Eye_target_locator_R',
            '*:Head_center_offset',
            '*:Head_tube_center_offset',
            '*:Eye_tear_attach_01_L',
            '*:Eye_tear_attach_02_L',
            '*:Eye_tear_attach_03_L',
            '*:Eye_tear_attach_01_R',
            '*:Eye_tear_attach_02_R',
            '*:Eye_tear_attach_03_R',
            '*:Head_shade_start',
            '*:Head_attach_R',
            '*:Head_attach_L',
            '*:Head_attach',
            '*:Eye_locator_R',
            '*:Eye_locator_L',
        ]

        for locator_name in locator_names:
            locators = cmds.ls(locator_name)
            for locator in locators:
                cmds.setAttr('{}.visibility'.format(locator), 0)

        # LocalAxis表示オフ
        transforms = cmds.ls(typ='transform')
        for transform in transforms:
            cmds.setAttr('{}.displayLocalAxis'.format(transform), 0)

        # Head下表示、非表示（Sp_:Tp_:Ex_:Pc_ボーンは表示）
        visible_prefix = [':Sp_', ':Tp_', ':Ex_', ':Pc_']

        head_children = cmds.listRelatives('*:Head', c=True)
        for head_child in head_children:
            if 'Constraint' not in head_child:
                cmds.setAttr('{}.visibility'.format(head_child), 0)

        head_child_joints = cmds.listRelatives('*:Head', typ='joint', c=True)
        for head_child_joint in head_child_joints:
            if any(prefix in head_child_joint for prefix in visible_prefix):
                cmds.setAttr('{}.visibility'.format(head_child_joint), 1)

                if '_Ear0_' in head_child_joint and not cmds.objExists('Ear_03_R_Ctrl'):
                    cmds.setAttr('{}.visibility'.format(head_child_joint), 0)

        # 耳本体ボーンは非表示
        ear_joint_names = [
            '*:Ear_01_L',
            '*:Ear_02_L',
            '*:Ear_03_L',
            '*:Ear_01_R',
            '*:Ear_02_R',
            '*:Ear_03_R',
        ]

        for ear_joint_name in ear_joint_names:
            ear_joints = cmds.ls(ear_joint_name)
            for ear_joint in ear_joints:
                cmds.setAttr('{}.visibility'.format(ear_joint), 0)

        # Headボーンの表示 None
        heads = cmds.ls('*:Head')
        for head in heads:
            cmds.setAttr('{}.drawStyle'.format(head), 2)

        # 耳のボーンとSpボーンをplusMinusAverageノードで繋ぐ
        avg_joint_sets = [
            ('plusMinusAverageEarL1', 'Sp_He_Ear0_L_01', 'Ear_02_L'),
            ('plusMinusAverageEarL2', 'Sp_He_Ear0_L_02', 'Ear_03_L'),
            ('plusMinusAverageEarR1', 'Sp_He_Ear0_R_01', 'Ear_02_R'),
            ('plusMinusAverageEarR2', 'Sp_He_Ear0_R_02', 'Ear_03_R'),
        ]

        attr_sets = [
            ('rotateX', 'input3D[0].input3Dx'),
            ('rotateY', 'input3D[0].input3Dy'),
            ('rotateZ', 'input3D[0].input3Dz'),
        ]

        he_ear_joints = cmds.ls('mdl_chr*:Sp_He_Ear0_L_00')

        if he_ear_joints:
            head_namespace = he_ear_joints[0].split(':')[0]

            for avg, src_name, dst_name in avg_joint_sets:
                if cmds.objExists(avg):
                    continue

                long_src_name = '{}:{}'.format(head_namespace, src_name)
                long_dst_name = '{}:{}'.format(head_namespace, dst_name)

                cmds.shadingNode('plusMinusAverage', au=True, n=avg)

                for old_attr, new_attr in attr_sets:
                    long_old_attr = '{}.{}'.format(long_dst_name, old_attr)
                    long_new_attr = '{}.{}'.format(avg, new_attr)

                    rotate_nodes = cmds.listConnections(long_old_attr, d=False)

                    if rotate_nodes:
                        input_nodes = cmds.listConnections('{}.input'.format(rotate_nodes[0]), d=False)
                        if input_nodes:
                            output_attr = '{}.output'.format(input_nodes[0])
                            cmds.connectAttr(output_attr, long_new_attr, f=True)
                            cmds.disconnectAttr(output_attr, long_old_attr)

                cmds.connectAttr('{}.rotate'.format(long_src_name), '{}.input3D[1]'.format(avg), f=True)
                cmds.connectAttr('{}.output3D'.format(avg), '{}.rotate'.format(long_dst_name), f=True)

        # シーン最適化
        mel.eval('deleteUnusedDeformers()')

        # AnimSchoolPickerを削除
        file_info = cmds.fileInfo(q=True)

        if file_info:
            for i in range(0, len(file_info), 2):
                key = file_info[i]
                if key.startswith('AnimSchoolPicker'):
                    cmds.fileInfo(rm=key)

    # ==================================================
    def __relink_cheek_for_maya_texture(self):

        # ---------------
        # cheek_for_mayaテクスチャの検索

        cheek_texture_name = 'tex_{0}_cheek_for_maya0.tga'.format(self.file_id)

        cheek_texture_path = '{0}/{1}'.format(
            self.sourceimage_dir_path, cheek_texture_name
        )

        if not os.path.isfile(cheek_texture_path):
            return

        # ---------------
        # マテリアル検索

        cheek_material = base_utility.node.search(
            'mtl_chr.*_cheek', None, 'lambert')

        if not cheek_material:
            return

        # ---------------
        # ファイルノード検索

        attr_list = base_utility.attribute.get_input_attr_list(
            cheek_material, 'color'
        )

        if not attr_list:
            return

        file_node = attr_list[0].split('.')[0]

        # ---------------
        # 紐づけ

        base_utility.attribute.set_value(
            file_node, 'fileTextureName', cheek_texture_path
        )

    # ==================================================
    def __add_attr_to_cheek_ctrl(self):

        cheek_ctrl = base_utility.node.search(
            'Cheek_Ctrl$', 'facial_Ctrl', 'transform')

        if not cheek_ctrl:
            return

        # ---------------

        base_utility.attribute.add(
            cheek_ctrl, 'namida', 0.0
        )

        cmds.addAttr(
            cheek_ctrl + '.namida', e=True,
            min=0, max=1)

        cmds.setAttr(
            cheek_ctrl + '.namida',
            cb=False, k=True, l=False)

        # ---------------

        base_utility.attribute.add(
            cheek_ctrl, 'hitomi', 0.0
        )

        cmds.addAttr(
            cheek_ctrl + '.hitomi', e=True,
            min=0, max=10000)

        cmds.setAttr(
            cheek_ctrl + '.hitomi',
            cb=False, k=True, l=False)

        # ---------------

        base_utility.attribute.add(
            cheek_ctrl, 'shadeAlpha', 0.0
        )

        cmds.addAttr(
            cheek_ctrl + '.shadeAlpha', e=True,
            min=0, max=1)

        cmds.setAttr(
            cheek_ctrl + '.shadeAlpha',
            cb=False, k=True, l=False)

        # ---------------

        base_utility.attribute.add(
            cheek_ctrl, 'mangaStart', False
        )

        cmds.setAttr(
            cheek_ctrl + '.mangaStart', e=True,
            cb=False, k=True, l=False)

        # ---------------

        base_utility.attribute.add(
            cheek_ctrl, 'mangaID', 0
        )

        cmds.addAttr(
            cheek_ctrl + '.mangaID', e=True,
            min=0, max=10000)

        cmds.setAttr(
            cheek_ctrl + '.mangaID',
            cb=False, k=True, l=False)

        # ---------------

        this_tear_info_list = [
            {'alpha': 0.0, 'speed': 1.0, 'id': 1, 'LR': 0},
            {'alpha': 0.0, 'speed': 1.0, 'id': 1, 'LR': 1},
            {'alpha': 0.0, 'speed': 1.0, 'id': 0, 'LR': 0},
            {'alpha': 0.0, 'speed': 1.0, 'id': 0, 'LR': 1},
        ]

        for tear_attr_type in range(4):

            for tear_id in range(4):

                this_tear_prefix = 'tear{0}'.format(tear_id)

                this_tear_info = this_tear_info_list[tear_id]

                if tear_attr_type == 0:

                    this_tear_alpha = this_tear_info['alpha']

                    base_utility.attribute.add(
                        cheek_ctrl,
                        '{0}Alpha'.format(this_tear_prefix),
                        this_tear_alpha
                    )

                    cmds.addAttr(
                        cheek_ctrl + '.{0}Alpha'.format(this_tear_prefix), e=True,
                        min=0, max=1)

                    cmds.setAttr(
                        cheek_ctrl + '.{0}Alpha'.format(this_tear_prefix),
                        cb=False, k=True, l=False)

                elif tear_attr_type == 1:

                    this_tear_speed = this_tear_info['speed']

                    base_utility.attribute.add(
                        cheek_ctrl,
                        '{0}Speed'.format(this_tear_prefix),
                        this_tear_speed
                    )

                    cmds.addAttr(
                        cheek_ctrl + '.{0}Speed'.format(this_tear_prefix), e=True,
                        min=0, max=5)

                    cmds.setAttr(
                        cheek_ctrl + '.{0}Speed'.format(this_tear_prefix),
                        cb=False, k=True, l=False)

                elif tear_attr_type == 2:

                    this_tear_id = this_tear_info['id']

                    base_utility.attribute.add(
                        cheek_ctrl,
                        '{0}Id'.format(this_tear_prefix),
                        this_tear_id
                    )

                    cmds.addAttr(
                        cheek_ctrl + '.{0}Id'.format(this_tear_prefix), e=True,
                        min=0, max=10000)

                    cmds.setAttr(
                        cheek_ctrl + '.{0}Id'.format(this_tear_prefix),
                        cb=False, k=True, l=False)

                elif tear_attr_type == 3:

                    this_tear_lr = this_tear_info['LR']

                    base_utility.attribute.add(
                        cheek_ctrl,
                        '{0}LR'.format(this_tear_prefix),
                        ['L', 'R'],
                        'enum'
                    )

                    base_utility.attribute.set_value(
                        cheek_ctrl,
                        '{0}LR'.format(this_tear_prefix),
                        this_tear_lr
                    )

                    cmds.setAttr(
                        cheek_ctrl + '.{0}LR'.format(this_tear_prefix),
                        cb=False, k=True, l=False)

    # ==================================================
    def __set_eye_high_visibility(self):

        layered_tex_list = cmds.ls(typ='layeredTexture', l=True, r=True)

        if not layered_tex_list:
            return

        for layered_tex in layered_tex_list:

            if not re.search('_eye_(l|r)$', layered_tex):
                continue

            index_list = cmds.getAttr(layered_tex + '.inputs', mi=True)

            if not index_list:
                continue

            for index in index_list:

                base_utility.attribute.set_value(
                    layered_tex, 'inputs[{0}].isVisible'.format(index), 0
                )

                input_attr_list = \
                    base_utility.attribute.get_input_attr_list(
                        layered_tex, 'inputs[{0}].color'.format(index)
                    )

                if not input_attr_list:
                    continue

                input_node = input_attr_list[0].split('.')[0]

                this_type = cmds.objectType(input_node)

                if this_type != 'file':
                    continue

                base_utility.attribute.set_value(
                    layered_tex, 'inputs[{0}].isVisible'.format(index), 1
                )

    def __save_modified_date(self):
        """facial_targetの更新日時を保存する
        """
        target_file_path_list = [self.facial_target_file_path, self.model_file_path, self.ear_target_file_path]
        modified_dates = [self.get_scene_modified_date(path) for path in target_file_path_list]
        self.set_facial_target_modified_dates(dict(zip(self.file_info_key_list, modified_dates)))

    @classmethod
    def get_scene_modified_date(cls, path):
        """シーンの更新日時を返す

        Args:
            path (str): シーンパス

        Returns:
            datetime: 更新日時
        """

        date_pattern = '//Last modified: (.*)'

        try:
            with open(path) as f:
                data = f.read()
                match = re.search(date_pattern, data)
                if match:
                    return datetime.strptime(match.group(1), cls.date_format)
        except Exception:
            pass

        return None

    @classmethod
    def get_facial_target_modified_dates(cls, path):
        """facial_targetの更新日時を返す

        Args:
            path (str): RIGのパス

        Returns:
            list[datetime]: 更新日時
        """

        date_pattern = 'fileInfo "{}" "(.*)";'

        try:
            with open(path) as f:
                data = f.read()

            match_list = [re.search(date_pattern.format(key), data) for key in cls.file_info_key_list]

            if all(match_list):
                return [datetime.strptime(match.group(1), cls.date_format) if match.group(1) else None for match in match_list]
        except Exception:
            pass

        return None

    @classmethod
    def set_facial_target_modified_dates(cls, modified_date_dict):
        """fileInfoにfacial_targetの更新日時を保存する

        Args:
            modified_date (dict[str, datetime]): キーと更新日時の辞書
        """

        for key, modified_date in modified_date_dict.items():
            cmds.fileInfo(key, modified_date.strftime(cls.date_format) if modified_date else '')
