# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import os
import re

import maya.cmds as cmds

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility
from ..glp_chara_body_difference import body_difference

from .. import glp_common
from ..glp_common.classes.info import chara_info

reload(base_common)
reload(glp_common)


# ==================================================
def main():
    exporter = Main()
    exporter.create_ui()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ==================================================
    def __init__(self):

        # ------------------------------
        # 定数

        # ツール全般
        self.tool_version = '20060901'
        self.tool_name = 'GallopAttachUtility'

        # fbxリファレンス取得
        self.body_root_dir = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/body'
        self.mini_body_root_dir = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/mini/body'

        # 基本骨取得
        self.base_body_scene_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/body/bdy0000_00/scenes/mdl_bdy0000_00.ma'
        self.mini_base_body_scene_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/mini/body/mbdy0002_00/scenes/mdl_mbdy0002_00_00.ma'

        self.base_root_node = 'mdl_bdy0000_00'
        self.mini_base_root_node = 'mdl_mbdy0002_00_00'

        self.base_body_name_space = '__base_body__'

        self.bust_suffix_list = ['_Bust_SS', '_Bust_S', '', '_Bust_L', '_Bust_LL']
        self.mini_bust_suffix_list = ['_Bust_S', '', '_Bust_L']

        # フェイスセット作成
        self.set_prefix = 'set_'
        self.base_set_id = 'bdy0000_00'
        self.mini_base_set_id = 'mbdy0000_00'

        # ------------------------------
        # 変数

        # ツール全般
        self.window_name = self.tool_name + 'Win'

        self.target_general_body_id = None
        self.target_base_set_id = None

        self.is_attach_scene = None
        self.is_mini = None

        # fbxリファレンス取得
        self.target_body_root_dir = None

        # 基本骨取得
        self.target_base_body_scene_path = None
        self.target_base_root_node = None
        self.target_bust_suffix = None

        # chara_info関連
        self.chara_info = None
        self.data_info_text = None
        self.chara_height_id = None
        self.chara_shape_id = None
        self.chara_bust_id = None
        self.chara_mini_bust_id = None
        self.chara_sex_id = None
        self.general_body_id_list = []

    # ==================================================
    def initialize(self):

        self.is_attach_scene = False
        self.is_mini = False

        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info()
        self.chara_info.create_all_info()

        if not self.chara_info.exists:
            return

        if self.chara_info.is_mini:
            self.is_mini = True

        if self.chara_info.part_info.data_type.find('attach') >= 0:
            self.is_attach_scene = True

        if self.chara_info.data_info.exists:
            self.data_info_text = 'CSVからキャラの情報を取得しました'
            self.chara_height_id = self.chara_info.data_info.height_id
            self.chara_shape_id = self.chara_info.data_info.shape_id
            self.chara_bust_id = self.chara_info.data_info.bust_id
            self.chara_mini_bust_id = self.chara_info.data_info.mini_bust_id
            self.chara_sex_id = self.chara_info.data_info.sex_id
        else:
            self.data_info_text = 'CSVからキャラの情報を取得出来ませんでした（デフォルト値が適用されます）'
            self.chara_height_id = 1
            self.chara_shape_id = 0
            self.chara_bust_id = 2
            self.chara_mini_bust_id = 1
            self.chara_sex_id = 1

        if self.is_mini:
            self.data_info_text = 'CSVからミニキャラの情報を取得しました'
            self.target_body_root_dir = self.mini_body_root_dir
            self.target_base_set_id = self.mini_base_set_id
            self.target_base_body_scene_path = self.mini_base_body_scene_path
            self.target_base_root_node = self.mini_base_root_node
            self.target_bust_suffix = self.mini_bust_suffix_list[int(self.chara_mini_bust_id)]
        else:
            self.target_body_root_dir = self.body_root_dir
            self.target_base_set_id = self.base_set_id
            self.target_base_body_scene_path = self.base_body_scene_path
            self.target_base_root_node = self.base_root_node
            self.target_bust_suffix = self.bust_suffix_list[int(self.chara_bust_id)]

        attach_model_list = self.chara_info.part_info.model_list

        if not attach_model_list:
            return

        self.general_body_id_list = []

        for model in attach_model_list:

            match = re.search(r'(\d{4}_\d{2}).fbx', model)

            if not match:
                continue

            body_prefix = 'bdy'

            if self.is_mini:
                body_prefix = 'mbdy'

            self.general_body_id_list.append(body_prefix + match.group(1))

    # ==================================================
    def create_ui(self):
        '''ui作成
        '''

        self.initialize()

        self.ui_window = base_class.ui.window.Window(
            self.window_name,
            self.tool_name + '  ' + self.tool_version,
            width=400,
            height=600
        )

        self.ui_window.set_job('SceneOpened', self.__change_scene)

        cmds.columnLayout(adjustableColumn=True, p=self.ui_window.ui_body_layout_id, rs=10)

        # ---------------------------------

        if self.is_attach_scene:
            cmds.text(l=self.data_info_text, al='left', fn='boldLabelFont')
        else:
            cmds.text(l='アタッチモデルのシーンが開かれていません', al='left', fn='boldLabelFont')

        cmds.separator()

        # ---------------------------------

        cmds.frameLayout(l='基本骨のインポート', cll=0, cl=0, bv=1, mw=10, mh=10)
        cmds.columnLayout(adjustableColumn=True, rs=4)

        ui_base_import_button = base_class.ui.button.Button(
            '基本骨のインポート',
            self.import_base_bone, height=50, en=self.is_attach_scene
        )

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.separator()

        # ---------------------------------

        cmds.frameLayout(l='基準セット({})'.format(self.target_base_set_id), cll=0, cl=0, bv=1, mw=10, mh=10)
        cmds.columnLayout(adjustableColumn=True, rs=4)

        ui_update_set_base_button = base_class.ui.button.Button(
            '選択フェースからセットを作成・更新',
            self.update_set_base, self.target_base_set_id, height=50, en=self.is_attach_scene
        )

        cmds.separator()

        ui_select_set_base_button = base_class.ui.button.Button(
            'セットのメンバーを選択',
            self.select_set_member, self.target_base_set_id, en=self.is_attach_scene
        )

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.separator()

        # ---------------------------------

        cmds.frameLayout(l='汎用衣装セット', cll=0, cl=0, bv=1, mw=10, mh=10)
        cmds.columnLayout(adjustableColumn=True, rs=4)

        self.ui_body_pull_down = cmds.optionMenu(label='汎用衣装選択', cc=self.__update_target_general_body_from_ui)

        for general_body_id in self.general_body_id_list:
            cmds.menuItem(label=general_body_id)

        self.__update_target_general_body_from_ui('')

        cmds.separator()

        ui_update_set_general_button = base_class.ui.button.Button(
            '選択フェースからセットを作成・更新',
            self.update_set_base, height=50, en=self.is_attach_scene
        )

        cmds.separator()

        ui_select_set_general_button = base_class.ui.button.Button(
            'セットのメンバーを選択',
            self.select_set_member, en=self.is_attach_scene
        )

        cmds.separator()

        ui_update_reference_general_button = base_class.ui.button.Button(
            '汎用衣装fbxをリファレンス読み込み・削除',
            self.update_reference, en=self.is_attach_scene
        )

        ui_delete_all_reference_button = base_class.ui.button.Button(
            '汎用衣装fbxのリファレンスを一括削除',
            self.unload_all_references, en=self.is_attach_scene
        )

        cmds.setParent('..')
        cmds.setParent('..')

        # ---------------------------------s

        cmds.setParent('..')
        self.ui_window.show()

    # ==================================================
    def __change_scene(self):

        self.create_ui()

    # ==================================================
    def __update_target_general_body_from_ui(self, arg):

        self.update_target_general_body(cmds.optionMenu(self.ui_body_pull_down, q=True, v=True))

    # ==================================================
    def update_target_general_body(self, target_body_id):

        self.target_general_body_id = target_body_id

    # ==================================================
    def import_base_bone(self):

        if cmds.objExists(self.chara_info.part_info.root_node):
            cmds.warning('base set already exists')
            return

        base_body = self.__import_base_body()

        if not base_body:
            cmds.warning('cannot load base body')
            return
        else:
            print('Base body : {}'.format(base_body))

        self.__create_base_bone_from_base_body(base_body)

    # ==================================================
    def __import_base_body(self):
        '''胸骨の位置が違うので胸idでロード
        '''

        base_body_name_space = self.base_body_name_space

        while cmds.namespace(ex=base_body_name_space):
            base_body_name_space += base_body_name_space

        if not os.path.exists(self.target_base_body_scene_path):
            cmds.warning('base body scene not exists')
            return

        # 素体をインポート
        base_utility.reference.load(self.target_base_body_scene_path, base_body_name_space)
        base_utility.reference.import_reference_by_namespace(base_body_name_space)
        base_utility.reference.unload(self.target_base_body_scene_path, base_body_name_space)
        import_obj_list = cmds.ls('{}:{}*'.format(base_body_name_space, self.target_base_root_node))

        # 全体型インポートされるので、必要な胸体型以外を削除
        del_list = []
        for import_obj in import_obj_list:
            if not import_obj.endswith(self.target_base_root_node + self.target_bust_suffix):
                del_list.append(import_obj)
        cmds.delete(del_list)

        # ネームスペース除去
        cmds.namespace(removeNamespace=base_body_name_space, mergeNamespaceWithRoot=True)

        root_node_list = cmds.ls(self.target_base_root_node + self.target_bust_suffix, l=True, typ='transform')
        if root_node_list:
            return root_node_list[0]

    # ==================================================
    def __create_base_bone_from_base_body(self, base_body):

        if not cmds.objExists(base_body):
            return

        this_root = cmds.rename(base_body, self.chara_info.part_info.root_node)

        # 骨以外削除
        child_list = cmds.listRelatives(this_root, c=True, f=True)
        joint_root = None
        for child in child_list:
            if child.find('Position') >= 0:
                joint_root = child
            else:
                cmds.delete(child)

        # 規定骨以外の削除
        del_list = []

        if joint_root:

            joint_list = cmds.listRelatives(joint_root, ad=True, f=True, typ='transform')
            base_obj_list = self.chara_info.part_info.joint_list[:]
            base_obj_list.extend(self.chara_info.part_info.locator_list)

            for joint in joint_list:
                if joint == joint_root:
                    continue
                if joint not in base_obj_list:
                    del_list.append(joint)

        cmds.delete(del_list)

    # ==================================================
    def update_set_base(self, target_body_id=None):
        '''セットがあれば更新、なければ作成
        '''

        if not target_body_id:
            target_body_id = self.target_general_body_id

        if not target_body_id:
            return

        set_name = self.set_prefix + target_body_id
        upadate_type = ''

        if not cmds.objExists(set_name):
            upadate_type = 'create'
        else:
            upadate_type = 'update'

        target_face_list = []
        selection_list = cmds.ls(sl=True, l=True, fl=True)

        for selection in selection_list:

            if selection.find('.f[') >= 0:
                target_face_list.append(selection)

        if upadate_type == 'create':
            self.__create_attach_set(set_name, target_face_list)
        elif upadate_type == 'update':
            self.__update_attach_set(set_name, target_face_list)

    # ==================================================
    def __create_attach_set(self, set_name, face_list):

        cmds.sets(name=set_name)
        cmds.sets(face_list, add=set_name)

    # ==================================================
    def __update_attach_set(self, set_name, face_list):

        cmds.sets(cl=set_name)
        cmds.sets(face_list, add=set_name)

    # ==================================================
    def select_set_member(self, target_body_id=None):

        if not target_body_id:
            target_body_id = self.target_general_body_id

        if not target_body_id:
            return

        set_name = self.set_prefix + target_body_id

        if not cmds.objExists(set_name):
            return

        member_list = cmds.sets(set_name, q=True)
        cmds.select(member_list, r=True)

    # ==================================================
    def update_reference(self, target_body_id=None):
        '''レファレンスがあれば削除、なければ追加
        '''

        if not target_body_id:
            target_body_id = self.target_general_body_id

        if not target_body_id:
            return

        body_scenes_path = '{0}/{1}/scenes'.format(self.target_body_root_dir, target_body_id)

        if self.is_mini:
            file_name_with_sex = 'mdl_{0}_0{1}_{2}.fbx'.format(
                target_body_id, self.chara_sex_id, self.chara_mini_bust_id
            )

            file_name_no_sex = 'mdl_{0}_00_{1}.fbx'.format(
                target_body_id, self.chara_mini_bust_id
            )
        else:
            file_name_with_sex = 'mdl_{0}_0{1}_{2}_{3}_{4}.fbx'.format(
                target_body_id, self.chara_sex_id, self.chara_height_id,
                self.chara_shape_id, self.chara_bust_id
            )

            file_name_no_sex = 'mdl_{0}_00_{1}_{2}_{3}.fbx'.format(
                target_body_id, self.chara_height_id,
                self.chara_shape_id, self.chara_bust_id
            )

        target_file_path = ''

        if os.path.isfile(body_scenes_path + '/' + file_name_with_sex):
            target_file_path = body_scenes_path + '/' + file_name_with_sex
        elif os.path.isfile(body_scenes_path + '/' + file_name_no_sex):
            target_file_path = body_scenes_path + '/' + file_name_no_sex

        if not target_file_path:
            return

        if base_utility.reference.exist_reference_file_path(target_file_path):
            self.__unload_reference(target_file_path)

        else:
            base_utility.reference.load(target_file_path, target_body_id)

    # ==================================================
    def unload_all_references(self):

        reference_file_path_list = base_utility.reference.get_reference_file_path_list()

        if not reference_file_path_list:
            return

        for path in reference_file_path_list:
            self.__unload_reference(path)

    # ==================================================
    def __unload_reference(self, target_file_path):

        reference_namespace = cmds.file(target_file_path, q=True, ns=True)
        base_utility.reference.unload(target_file_path, reference_namespace)
