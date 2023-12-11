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
except:
    pass

import re

import maya.cmds as cmds
import maya.mel as mel

from ..bind_rebind_skin import bind_rebind_skin

from .... import base_common
from ....base_common import utility as base_utility
from ....base_common import classes as base_class

from .... import priari_common
from ....priari_common.classes.info import chara_info

reload(base_common)
reload(priari_common)


class SetJointOrient(object):
    """
    JointOrientを規定値通りに設定する
    """

    def __init__(self):
        """
        """

        self.tail_params = {
            'Tail_01': [56.651, 0.0, 0.0],
            'Tail_02': [18.349, 0.0, 0.0],
            'Tail_03': [10.0, 0.0, 0.0],
            'Tail_04': [10.0, 0.0, 0.0],
            'Tail_05': [10.0, 0.0, 0.0]
        }
        self.tail_orient = {
            'Tail_01': [0.0, 180.0, 0.0],
            'Tail_02': [0.0, 0.0, 0.0],
            'Tail_03': [0.0, 0.0, 0.0],
            'Tail_04': [0.0, 0.0, 0.0],
            'Tail_05': [0.0, 0.0, 0.0]
        }

        self.tail_expect_names = ['_BustL', '_BustM']

    def set_joint_orient(self):
        """
        ジョイントオリエントを設定する
        """

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            return

        # 揺れ骨対象
        sp_joint_name = 'Sp_'
        # メッシュ毎のジョイントウェイトの一覧
        self.mesh_joint_weight_list = {}

        # 何も選択されていなければ終了
        selected = cmds.ls(sl=True)
        if not selected:
            cmds.confirmDialog(title='Confirm', message=u'何も選択されていません', button=['OK'], defaultButton='Yes')
            return

        # シーン中のメッシュ一覧
        mesh_list = _chara_info.part_info.mesh_list
        if not mesh_list:
            print('meshのリストが見つかりません')
            return

        for mesh_node in mesh_list:
            if not cmds.objExists(mesh_node):
                continue
            # デタッチ
            if cmds.ls(cmds.listHistory(mesh_node), type="skinCluster"):
                joint_weight_info_list = base_utility.mesh.skin.get_all_joint_weight_info_list(mesh_node)
                self.mesh_joint_weight_list[mesh_node] = joint_weight_info_list
                cmds.skinCluster(mesh_node, e=True, ub=True)

        for sel in selected:

            if cmds.objectType(sel) != 'joint':
                continue

            if not sel.split('|')[-1].startswith(sp_joint_name):
                continue

            all_joint_list = cmds.listRelatives(sel, ad=True, pa=True)
            if not all_joint_list:
                print('子階層がない骨の為除外します : ' + sel)
                continue

            if sel.find('_Ear') != -1:
                print('耳骨は対象外の為除外します : ' + sel)
                continue

            all_joint_list = reversed(all_joint_list)
            target_joint_list = []
            non_sp_joint_list = []
            for joint_node in all_joint_list:
                joint_short_name = joint_node.split('|')[-1]
                if joint_short_name.startswith(sp_joint_name):
                    target_joint_list.append(joint_node)
                else:
                    non_sp_joint_list.append(joint_node)

            # Spではないjointを退避する
            # parent情報を取得
            dis_parent_joint_list = {}
            for joint_node in non_sp_joint_list:
                joint_parent = cmds.listRelatives(joint_node, parent=True, pa=True)
                dis_parent_joint_node = cmds.ls(cmds.parent(joint_node, w=True), l=True)[0]
                dis_parent_joint_list[dis_parent_joint_node] = joint_parent

            # 一括で適応する(Tail以外)
            cmds.joint(sel, e=True, orientJoint='zyx', secondaryAxisOrient='yup', children=True)

            for joint_node in target_joint_list:

                if cmds.objectType(joint_node) != 'joint':
                    continue

                joint_child = cmds.listRelatives(joint_node, children=True, pa=True)
                if joint_child:
                    continue

                joint_parent = cmds.listRelatives(
                    joint_node, parent=True, pa=True)
                if cmds.objectType(joint_parent) != 'joint':
                    continue

                # 末尾ジョイントは一つ親のジョイントをコピーしてjoint_orientを合わせる
                dup_parent_joint = cmds.duplicate(joint_parent, parentOnly=True)
                joint_child_pos = cmds.xform(joint_node, q=True, ws=True, t=True)
                cmds.xform(dup_parent_joint, ws=True, t=joint_child_pos)
                joint_short_name = cmds.ls(joint_node, l=True)[0].split('|')[-1]
                cmds.delete(joint_node)
                dup_parent_joint = cmds.rename(dup_parent_joint, joint_short_name)
                cmds.parent(dup_parent_joint, joint_parent)

            for joint_node, joint_parent in list(dis_parent_joint_list.items()):
                cmds.parent(joint_node, joint_parent)

        for mesh_node in mesh_list:
            if not cmds.objExists(mesh_node):
                continue

            if mesh_node in self.mesh_joint_weight_list:
                if not cmds.ls(cmds.listHistory(mesh_node), type="skinCluster"):
                    target_joint_list = cmds.ls(_chara_info.part_info.joint_list, l=True)
                    if not target_joint_list:
                        continue

                    cmds.skinCluster(target_joint_list, mesh_node)
                joint_weight_info_list = self.mesh_joint_weight_list[mesh_node]
                base_utility.mesh.skin.set_joint_weight_info_list(mesh_node, joint_weight_info_list)

    def set_tail_orient(self):
        """
        tailのJointOrientを設定する
        """

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            return

        topNodes = cmds.ls(assemblies=True, l=True)
        fileShortName = cmds.file(q=True, sceneName=True, shortName=True)
        fileShortNameRemoveExt = fileShortName.split('.')[0]
        for expect_name in self.tail_expect_names:
            fileShortNameRemoveExt = fileShortNameRemoveExt.replace(expect_name, '')

        for topNode in topNodes:

            weightList = None

            if not topNode.startswith('|' + fileShortNameRemoveExt):
                continue

            mbodyNode = topNode + topNode.replace(fileShortNameRemoveExt, 'mesh_body')
            positionNode = topNode + '|Position'

            if not cmds.objExists(mbodyNode) or not cmds.objExists(positionNode):
                continue

            childNodes = cmds.listRelatives(topNode, ad=True, f=True)
            tail01Node = None

            for childNode in childNodes:

                if childNode.split('|')[-1].endswith('Tail_01'):
                    tail01Node = childNode
                    break

            if not tail01Node:
                continue

            # デタッチ
            if cmds.ls(cmds.listHistory(mbodyNode), type="skinCluster"):
                joint_weight_info_list = base_utility.mesh.skin.get_all_joint_weight_info_list(mbodyNode)
                weightList = joint_weight_info_list
                cmds.skinCluster(mbodyNode, e=True, ub=True)

            target_joint_list = cmds.listRelatives(tail01Node, ad=True, pa=True)
            if not target_joint_list:
                continue
            reversed(target_joint_list)
            target_joint_list.insert(0, tail01Node)

            for joint_name, value in list(self.tail_params.items()):
                orient_value = self.tail_orient[joint_name]
                for joint_node in target_joint_list:
                    if joint_node.split('|')[-1] == joint_name:
                        cmds.joint(joint_node, e=True, o=orient_value)
                        cmds.xform(joint_node, rotation=value)
                        break

            if weightList:
                sp_joint_list = _chara_info.part_info.joint_list
                if not sp_joint_list:
                    continue

                replace_joint_list = []
                for sp_joint in sp_joint_list:
                    replace_joint = sp_joint.replace(fileShortNameRemoveExt, topNode.replace('|', ''))
                    replace_joint_list.append(replace_joint)

                cmds.skinCluster(replace_joint_list, mbodyNode)
                base_utility.mesh.skin.set_joint_weight_info_list(mbodyNode, weightList)

    def toggle_rotate_axis(self):
        """
        """

        selected = cmds.ls(sl=True)
        cmds.select(selected, hi=True)
        mel.eval("ToggleLocalRotationAxes;")


class SetEarJoint(object):
    """
    耳のjointをorient方向にセットする
    """

    def __init__(self):
        """
        """

        self.neck_joint_node = 'Neck'

        self.tmp_locator_00 = 'tmp_set_joint_loc_00'
        self.tmp_locator_01 = 'tmp_set_joint_loc_01'

    def set_ear_joint(self):
        """
        耳のjointをorient方向にセットする
        """

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            cmds.warning('chara_info not exists')
            return

        mdl_top_node = _chara_info.file_name_without_ext
        if not cmds.objExists(mdl_top_node):
            cmds.warning('mdl_top_node not exists. : {}'.format(mdl_top_node))
            return

        mdl_neck_joint_node = '{}|{}'.format(mdl_top_node, self.neck_joint_node)
        if not cmds.objExists(mdl_neck_joint_node):
            cmds.warning('mdl_neck_joint_node not exists. : {}'.format(mdl_neck_joint_node))
            return

        ear_joint_dict_list, error_message = self.__get_ear_joint_dict_list()
        if not ear_joint_dict_list:
            cmds.warning(error_message)
            return

        mesh_list = []
        for mesh_param in _chara_info.part_info.mesh_param_list:

            mesh_name = mesh_param['name']
            if 'extra' in mesh_param:
                if mesh_param['extra']:
                    continue

            if not cmds.objExists(mesh_name):
                continue

            mesh_list.append(mesh_name)

        skin_info = base_class.mesh.skin_info.SkinInfo()
        skin_info.create_info(mesh_list)

        # historyを削除してweight情報を削除
        cmds.delete(mesh_list, ch=True)

        sp_ear_00_joint_list = []

        # locatorを作成
        tmp_locator_00 = cmds.spaceLocator(name=self.tmp_locator_00)[0]
        tmp_locator_01 = cmds.spaceLocator(name=self.tmp_locator_01)[0]

        for ear_joint_dict in ear_joint_dict_list:

            ear_01_joint = ear_joint_dict['ear_01']
            ear_02_joint = ear_joint_dict['ear_02']
            ear_03_joint = ear_joint_dict['ear_03']
            sp_ear_00_joint = ear_joint_dict['sp_ear_00']
            sp_ear_01_joint = ear_joint_dict['sp_ear_01']
            sp_ear_02_joint = ear_joint_dict['sp_ear_02']

            sp_ear_00_joint_list.append(sp_ear_00_joint)

            # locatorを2番目の骨位置、3番目の骨位置にそれぞれ移動
            ear_02_joint_transform = cmds.xform(ear_02_joint, q=True, ws=True, t=True)
            cmds.xform(tmp_locator_00, ws=True, t=ear_02_joint_transform)
            ear_03_joint_transform = cmds.xform(ear_03_joint, q=True, ws=True, t=True)
            cmds.xform(tmp_locator_01, ws=True, t=ear_03_joint_transform)

            # ear_01_jointのtransformリセット
            cmds.xform(ear_01_joint, t=[0, 0, 0])

            # jointorientリセット
            for joint in [ear_01_joint, ear_02_joint, ear_03_joint, sp_ear_00_joint, sp_ear_01_joint, sp_ear_02_joint]:
                cmds.setAttr("{}.jointOrient".format(joint), 0, 0, 0)
                cmds.xform(joint, ro=(0, 0, 0))

            # 該当のロケーター方向へjointを向かせて次の骨の位置を元に戻す
            self.___set_joint_aim(sp_ear_00_joint, sp_ear_01_joint, tmp_locator_00)
            self.___set_joint_aim(sp_ear_01_joint, sp_ear_02_joint, tmp_locator_01)

            # sp骨のtransform値をアニメーション骨にコピー
            self.__copy_transform(sp_ear_01_joint, ear_02_joint)
            self.__copy_transform(sp_ear_02_joint, ear_03_joint)

        # locatorを削除
        cmds.delete([tmp_locator_00, tmp_locator_01])

        # フリーズ
        cmds.makeIdentity(sp_ear_00_joint_list, apply=True, t=False, r=True, s=False, n=False, pn=True)

        # 再バインド
        bind_skin_obj = bind_rebind_skin.BindSkin()
        bind_skin_obj.set_transform_list(mesh_list)
        bind_skin_obj.set_joint_list([mdl_neck_joint_node])
        bind_skin_obj.is_check_maximun_inf = 2
        bind_skin_obj.exec_bind()

        # 元の状態にスキニング
        target_skin_info = base_class.mesh.skin_info.SkinInfo()
        target_skin_info.create_info(mesh_list)
        base_utility.mesh.skin.paste_weight_by_vertex_index(
            skin_info, target_skin_info)

        # bindPose再設定
        bind_pose_list = cmds.dagPose(mdl_neck_joint_node, q=True, bp=True)
        if len(bind_pose_list) > 1:
            cmds.delete(bind_pose_list)
            cmds.dagPose(mdl_neck_joint_node, bp=True, save=True)

    def __get_ear_joint_dict_list(self):
        """
        左右の耳のjointリストを取得する
        """

        ear_joint_dict_list = []
        for orient in ['R', 'L']:

            ear_01_joint_name = 'Ear_01_{}'.format(orient)
            ear_01_joint = self.__get_joint_full_path(ear_01_joint_name)
            if not ear_01_joint:
                return [], 'ear_01_joint not exists. {}'.format(ear_01_joint_name)

            ear_02_joint_name = 'Ear_02_{}'.format(orient)
            ear_02_joint = self.__get_joint_full_path(ear_02_joint_name)
            if not ear_02_joint:
                return [], 'ear_02_joint not exists. {}'.format(ear_02_joint_name)

            ear_03_joint_name = 'Ear_03_{}'.format(orient)
            ear_03_joint = self.__get_joint_full_path(ear_03_joint_name)
            if not ear_03_joint:
                return [], 'ear_03_joint not exists. {}'.format(ear_03_joint_name)

            sp_ear_00_joint_name = 'Sp_He_Ear0_{}_00'.format(orient)
            sp_ear_00_joint = self.__get_joint_full_path(sp_ear_00_joint_name)
            if not sp_ear_00_joint:
                return [], 'sp_ear_00_joint not exists. {}'.format(sp_ear_00_joint_name)

            sp_ear_01_joint_name = 'Sp_He_Ear0_{}_01'.format(orient)
            sp_ear_01_joint = self.__get_joint_full_path(sp_ear_01_joint_name)
            if not sp_ear_01_joint:
                return [], 'sp_ear_01_joint not exists. {}'.format(sp_ear_01_joint_name)

            sp_ear_02_joint_name = 'Sp_He_Ear0_{}_02'.format(orient)
            sp_ear_02_joint = self.__get_joint_full_path(sp_ear_02_joint_name)
            if not sp_ear_02_joint:
                return [], 'sp_ear_02_joint not exists. {}'.format(sp_ear_02_joint_name)

            ear_joint_dict_list.append(
                {
                    'ear_01': ear_01_joint,
                    'ear_02': ear_02_joint,
                    'ear_03': ear_03_joint,
                    'sp_ear_00': sp_ear_00_joint,
                    'sp_ear_01': sp_ear_01_joint,
                    'sp_ear_02': sp_ear_02_joint
                }
            )

        return ear_joint_dict_list, ''

    def __get_joint_full_path(self, joint):
        """
        jointのfullpathを取得
        """
        joint_node_list = cmds.ls(joint, l=True)
        if len(joint_node_list) != 1:
            return None

        return joint_node_list[0]

    def ___set_joint_aim(self, target_joint, next_joint, target_loc):
        """
        jointを次のjoint方向に向け、次のjointの位置を元の位置に戻す
        """

        aimconstraint_node = cmds.aimConstraint(
            target_loc, target_joint,
            offset=[0, 0, 0], weight=1,
            aimVector=[0, 1, 0], upVector=[0, 1, 0],
            worldUpType='vector', worldUpVector=[0, 1, 0])

        cmds.delete(aimconstraint_node[0])

        # 次のジョイントの位置をlocatorと合わせる
        target_loc_transform = cmds.xform(target_loc, q=True, ws=True, t=True)
        cmds.xform(next_joint, ws=True, t=target_loc_transform)

    def __copy_transform(self, original_joint, target_joint):
        """
        originalのtransformをtargetのtransformにコピーする
        """

        original_joint_translate = cmds.xform(original_joint, q=True, t=True)
        cmds.xform(target_joint, t=original_joint_translate)


class SpMirror(object):
    """
    選択したSp骨のミラーを行う
    """

    def sp_mirror(self):
        """
        """

        joint_list = cmds.ls(sl=True, typ='joint', fl=True, l=True)

        if not joint_list:
            return

        src_base_list = self.__get_sp_base_list(joint_list)
        mirror_pair_list = self.__get_mirror_pair_list(src_base_list)

        checked_pair_list = self.__check_mirror_pair_list(mirror_pair_list)

        if not checked_pair_list:
            return

        for mirror_pair in checked_pair_list:
            self.__execute_mirror(mirror_pair[0], mirror_pair[1])

    def __execute_mirror(self, src_path, dst_path):
        """
        """

        mirror_joint_str = 'MIRRORSp_'

        if not cmds.objExists(src_path):
            return

        root_node = src_path.split('|')[1]
        origin_ws_pos = cmds.xform(root_node, q=True, ws=True, t=True)
        src_ws_pos = cmds.xform(src_path, q=True, ws=True, t=True)
        mirror_ws_pos = [origin_ws_pos[0] + (origin_ws_pos[0] - src_ws_pos[0]), src_ws_pos[1], src_ws_pos[2]]

        dst_parent = dst_path.replace('|{}'.format(dst_path.split('|')[-1]), '')

        # ミラー実行
        # オリエント修正時に親に回転値が入っていると面倒なのでワールドの子にする
        mirror_joint = cmds.mirrorJoint(src_path, mb=True, myz=True, sr=['Sp_', mirror_joint_str])[0]
        mirror_joint = cmds.parent(mirror_joint, w=True)
        mirror_joint = cmds.ls(mirror_joint, l=True)[0]

        # rotate=[180, 0, 0]にしてフリーズ
        mirror_joint = self.__apply_mirror_transform(mirror_joint)

        # ワールドで位置合わせ
        cmds.xform(mirror_joint, ws=True, t=mirror_ws_pos)

        # 階層構造の再構築
        # 存在していた場合は削除して上書き
        if cmds.objExists(dst_path):
            cmds.delete(dst_path)

        mirror_joint = cmds.parent(mirror_joint, dst_parent)[0]
        mirror_joint = cmds.ls(mirror_joint, l=True)[0]

        # リネーム
        rename_list = cmds.listRelatives(mirror_joint, ad=True, f=True)
        if rename_list:
            rename_list.append(mirror_joint)
        else:
            rename_list = [mirror_joint]

        # listRelativesは子階層から順に並ぶので、この順でリネームしていく
        for rename_item in rename_list:
            this_item_short_name = rename_item.split('|')[-1]
            this_item_short_name = this_item_short_name.replace(mirror_joint_str, 'Sp_')
            this_item_short_name = self.__get_mirror_path(this_item_short_name)
            cmds.rename(rename_item, this_item_short_name)

    def __apply_mirror_transform(self, mirrored_joint):
        """
        ミラーした骨に対する処理
        一度アンピアレントしてrotate=[180, 0, 0]した後フリーズしてピアレント
        """

        if not cmds.objExists(mirrored_joint):
            return mirrored_joint

        target_list = cmds.listRelatives(mirrored_joint, ad=True, typ='joint')
        if not target_list:
            target_list = []

        target_list.append(mirrored_joint)
        target_id_dict_list = []
        unparent_target_list = []

        for target in target_list:

            this_dict = {'id': None, 'parent_id': None}
            this_dict['id'] = cmds.ls(target, uuid=True)[0]

            parent_list = cmds.listRelatives(target, p=True)
            if parent_list:
                this_dict['parent_id'] = cmds.ls(parent_list[0], uuid=True)[0]
                unparent_target_list.append(target)

            target_id_dict_list.append(this_dict)

        cmds.parent(unparent_target_list, w=True)

        # ここに個々のjointに対する処理を記載
        for target_dict in target_id_dict_list:
            this_target = cmds.ls(target_dict['id'])[0]
            cmds.xform(this_target, ro=[180, 0, 0])
            cmds.makeIdentity(this_target, apply=True)

        for target_dict in target_id_dict_list:
            if not target_dict['parent_id']:
                continue
            this_target = cmds.ls(target_dict['id'])[0]
            this_parent = cmds.ls(target_dict['parent_id'])[0]
            cmds.parent(this_target, this_parent)

        return cmds.ls(target_id_dict_list[-1]['id'])[0]

    def __get_sp_base_list(self, joint_list):
        """
        """

        if not joint_list:
            return

        sp_base_dict = {}
        spring_flag = 'Sp_'
        ear_flag = '_Ear'
        suffix_reg = '_[0-9]{2}$'

        for joint in joint_list:

            this_short_name = joint.split('|')[-1]

            if not this_short_name.startswith(spring_flag):
                continue
            if this_short_name.find(ear_flag) >= 0:
                continue

            # Sp骨のベースネームをKey、パスをValueにして辞書を更新
            sp_root_base_name = self.__get_sp_base_name(this_short_name)

            # Keyがあるならパスを比較して親側なら更新、Keyがなければ追加
            if sp_root_base_name in sp_base_dict:
                exist_path = sp_base_dict[sp_root_base_name]
                if exist_path.find(joint) >= 0:
                    sp_base_dict[sp_root_base_name] = joint
            else:
                sp_base_dict[sp_root_base_name] = joint

        return list(sp_base_dict.values())

    def __get_sp_base_name(self, src_name):
        """
        """

        suffix_reg = '_[0-9]{2}$'
        short_name = src_name.split('|')[-1]

        return re.sub(suffix_reg, '', short_name)

    def __get_mirror_pair_list(self, src_sp_base_list):
        """
        """

        if not src_sp_base_list:
            return

        result_list = []

        for src_sp_base in src_sp_base_list:
            result_list.append([src_sp_base, self.__get_mirror_path(src_sp_base)])

        return result_list

    def __get_mirror_path(self, src_sp_path):
        """
        """

        result = ''
        pos_reg = '_[FBRL]*_'
        pos_reg2 = '_[FBRL]*$'

        path_elm_list = src_sp_path.split('|')
        mirror_path_elm_list = []

        for path_elm in path_elm_list:

            pos_match = re.search(pos_reg, path_elm)
            pos_match2 = re.search(pos_reg2, path_elm)

            if pos_match:
                this_pos = pos_match.group()
            elif pos_match2:
                this_pos = pos_match2.group()
            else:
                mirror_path_elm_list.append(path_elm)
                continue

            mirror_pos = this_pos.replace('L', '|right|')
            mirror_pos = mirror_pos.replace('R', 'L')
            mirror_pos = mirror_pos.replace('|right|', 'R')
            mirror_path_elm_list.append(path_elm.replace(this_pos, mirror_pos))

        return '|'.join(mirror_path_elm_list)

    def __check_mirror_pair_list(self, mirror_pair_list):
        """
        """

        if not mirror_pair_list:
            return False

        checked_pair_list = []
        tmp_checked_pair_list = []
        no_parent_list = []
        src_dst_conflict_list = []
        over_write_list = []

        # ミラー先の親がいるかどうかチェック
        for mirror_pair in mirror_pair_list:

            if self.__check_dst_parent_exists(mirror_pair):
                tmp_checked_pair_list.append(mirror_pair)
            else:
                no_parent_list.append(mirror_pair[0])

        # ミラー先が別のミラー元に含まれていないかチェック
        for mirror_pair in tmp_checked_pair_list:

            if self.__check_src_dst_conflict(mirror_pair, tmp_checked_pair_list):
                checked_pair_list.append(mirror_pair)
            else:
                src_dst_conflict_list.append(mirror_pair[0])

        # 上書きチェック
        for mirror_pair in checked_pair_list:
            if cmds.objExists(mirror_pair[1]) and mirror_pair[1] not in over_write_list:
                over_write_list.append(mirror_pair[1])

        if no_parent_list:

            base_utility.ui.dialog.open_ok_with_scroll(
                '確認',
                '以下のSp骨はミラー先が存在しないためスキップします',
                no_parent_list
            )

        if src_dst_conflict_list:

            base_utility.ui.dialog.open_ok_with_scroll(
                '確認',
                '以下のSp骨はミラー先が別のミラー元と被っているためスキップします',
                src_dst_conflict_list
            )

        if over_write_list:

            if not base_utility.ui.dialog.open_ok_cancel_with_scroll(
                    '確認',
                    '以下のSp骨が上書きされます。実行してよろしいですか？',
                    over_write_list
            ):
                return

        return checked_pair_list

    def __check_dst_parent_exists(self, mirror_pair):
        """
        """

        dst_short_name = mirror_pair[1].split('|')[-1]
        dst_parent = mirror_pair[1].replace('|{}'.format(dst_short_name), '')

        if cmds.objExists(dst_parent):
            return True
        else:
            return False

    def __check_src_dst_conflict(self, mirror_pair, mirror_pair_list):
        """
        """

        dst_base_name = self.__get_sp_base_name(mirror_pair[1])

        for this_mirror_pair in mirror_pair_list:

            reg = dst_base_name + '_[0-9]{2}$'
            match = re.search(reg, this_mirror_pair[0])

            if match:
                return False

        return True


class SpJointCounter(object):

    def __init__(self):
        """
        """

        self.chara_info = chara_info.CharaInfo()
        self.sp_joint_regex = re.compile(r'^Sp_')

    def sp_joint_counter(self):
        """
        """

        self.chara_info.create_info()
        if not self.chara_info.exists:
            return

        root_node = self.chara_info.part_info.root_node
        if not cmds.objExists(root_node):
            return

        child_node_list = cmds.listRelatives(root_node, ad=True, f=True)
        if not child_node_list:
            return

        sp_bone_limit = self.chara_info.part_info.sp_bone_limit

        joint_list = cmds.ls(child_node_list, type='joint', l=True)
        sp_joint_list = [_joint for _joint in joint_list if self.sp_joint_regex.search(_joint.split('|')[-1])]

        result_str = ''
        if len(sp_joint_list) > sp_bone_limit:
            result_str = '規定数オーバー'
        else:
            result_str = '規定数以内'

        info_str = '現在の本数:  {}  (  規定数:  {}  -  {}  )'.format(str(len(sp_joint_list)), str(sp_bone_limit), result_str)
        base_utility.ui.dialog.open_ok_with_scroll('Sp骨本数計測', info_str, sp_joint_list)
