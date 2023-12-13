# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import Counter
from functools import partial
import os
import webbrowser

import sys
import importlib

import maya.OpenMaya as om
import maya.cmds as cmds

from . import command
from . import TITLE
from . import NAME
from mtk.utils import getCurrentSceneFilePath


# 開発中はTrue、リリース時にFalse
DEV_MODE = False

if DEV_MODE:
    importlib.reload(command)
else:
    from . import logger


ICON_PATH = r"Z:\mtk\tools\maya\2022\modules\mtk\scripts\mtk\rig\easy_bind\icons"


class EasyBindUI(object):
    _window_width = 250

    _button_height = 40
    _window_height = (_button_height * 3) + 80

    select_mesh_btn = "{}_{}".format(NAME, "select_mesh_btn")
    select_joint_btn = "{}_{}".format(NAME, "select_joint_btn")
    select_all_btn = "{}_{}".format(NAME, "select_all_btn")
    bind_skin_btn = "{}_{}".format(NAME, "bind_skin_btn")
    unbind_skin_btn = "{}_{}".format(NAME, "unbind_skin_btn")
    goto_bind_pose_btn = "{}_{}".format(NAME, "goto_bind_pose_btn")
    select_translate_btn = "{}_{}".format(NAME, "select_translate_btn")
    lod_translate_btn = "{}_{}".format(NAME, "lod_translate_btn")
    open_directory_dialog_btn = "{}_{}".format(NAME, "directory_dialog_btn")
    save_weight_btn = "{}_{}".format(NAME, "save_weight_btn")
    load_weight_btn = "{}_{}".format(NAME, "load_weight_btn")
    _tso_flag = False

    frame_a = "{}_{}".format(NAME, "frame_a")
    frame_b = "{}_{}".format(NAME, "frame_b")
    frame_c = "{}_{}".format(NAME, "frame_c")

    rigid_body_cb = "{}_{}".format(NAME, "rigid_body_cb")
    mutsu_specification_cb = "{}_{}".format(NAME, "mutsu_specification_cb")

    column_layout = "{}_{}".format(NAME, "column_layout")

    btn_num = 0

    def __init__(self):
        self.scene_name = ""
        self.work_dir = ""
        self._trackSelectionOrder_flag()

    def create(self):
        self.get_icons()

        try:
            cmds.deleteUI(NAME)
        except:
            pass

        cmds.window(NAME,
                    title=TITLE,
                    width=self._window_width,
                    menuBar=True,
                    height=self._window_height,
                    cc=partial(self.close_event))

        cmds.menu(label='Help', helpMenu=True)
        cmds.menuItem(label=u'コンフルページにジャンプ', command=partial(self.open_confluence))

        cmds.columnLayout(adjustableColumn=True)

        cmds.checkBox(self.mutsu_specification_cb,
                      l=u"[ mutsunokami ] 仕様のジョイント限定",
                      value=True)
        cmds.setParent("..")

        cmds.columnLayout(self.column_layout,
                          adjustableColumn=True,
                          width=self._window_width,
                          height=self._window_height)

        cmds.frameLayout(self.frame_a,
                         l=u"バインド対象 の選択",
                         mh=10,
                         cll=True,
                         cc=partial(self.close_frame_cb, self.frame_a),
                         ec=partial(self.open_frame_cb, self.frame_a),
                         labelVisible=True,
                         width=self._window_width)

        cmds.iconTextButton(self.select_all_btn,
                            image1=self.nodes_with_lod_icon,
                            label=u"対象 メッシュ選択",
                            width=(self._window_width / 2) - 10,
                            height=self._button_height,
                            style='iconAndTextHorizontal',
                            bgc=(0.3, 0.3, 0.3),
                            command=partial(self.select_meshes),
                            )

        cmds.iconTextButton(
            image1=self.nodes_not_with_lod_icon,
            label=u"対象 メッシュ選択（LODは除外）",
            width=(self._window_width / 2) - 10,
            height=self._button_height,
            style='iconAndTextHorizontal',
            bgc=(0.3, 0.3, 0.3),
            command=partial(self.select_meshes_no_lod),
        )

        cmds.iconTextButton(
            image1=self.joint_icon,
            label=u"対象 ジョイント選択",
            width=(self._window_width / 2) - 10,
            height=self._button_height,
            style='iconAndTextHorizontal',
            bgc=(0.3, 0.3, 0.3),
            command=partial(self.select_joints),
        )

        cmds.iconTextButton(
            image1=self.nodes_with_joints_lod_icon,
            label=u"対象 メッシュ と 対象 ジョイント選択",
            width=(self._window_width / 2) - 10,
            height=self._button_height,
            style='iconAndTextHorizontal',
            bgc=(0.3, 0.3, 0.3),
            command=partial(self.select_all),
        )

        cmds.setParent("..")

        btn_num = cmds.frameLayout(self.frame_a, q=True, nch=True)
        all_btn_num = btn_num
        self.set_frame_height(self.frame_a, btn_num)

        cmds.frameLayout(self.frame_b,
                         l=u"スムースバインド",
                         mh=10,
                         cll=True,
                         cc=partial(self.close_frame_cb, self.frame_b),
                         ec=partial(self.open_frame_cb, self.frame_b),
                         labelVisible=True,
                         width=self._window_width)

        cmds.iconTextButton(
            image1=self.gotobind_icon,
            label=u"バインドポーズに移行",
            width=(self._window_width / 2) - 10,
            height=self._button_height,
            style='iconAndTextHorizontal',
            bgc=(0.3, 0.3, 0.3),
            command=partial(self.go_to_bind),
        )

        cmds.iconTextButton(
            image1=self.bind_auto_icon,
            label=u"自動バインド",
            width=(self._window_width / 2) - 10,
            height=self._button_height,
            style='iconAndTextHorizontal',
            bgc=(0.3, 0.3, 0.3),
            command=partial(self.bind_skin),
        )

        cmds.iconTextButton(
            image1=self.bind_select_icon,
            label=u"現在の 選択でバインド",
            width=(self._window_width / 2) - 10,
            height=self._button_height,
            style='iconAndTextHorizontal',
            bgc=(0.3, 0.3, 0.3),
            command=partial(self.bind_select_nodes),
        )

        cmds.iconTextButton(
            image1=self.unbind_icon,
            label=u"シーン全体のバインド解除",
            width=(self._window_width / 2) - 10,
            height=self._button_height,
            style='iconAndTextHorizontal',
            bgc=(0.3, 0.3, 0.3),
            command=partial(self.unbind_skin),
        )

        cmds.iconTextButton(self.select_translate_btn,
                            image1=self.copy_skin_weight,
                            label=u"選択ジオメトリ に ウェイト転送",
                            width=(self._window_width / 2) - 10,
                            height=self._button_height,
                            style='iconAndTextHorizontal',
                            bgc=(0.3, 0.3, 0.3),
                            # en=False,
                            command=partial(self.copy_weight_selection)
                            )

        cmds.rowLayout(nc=2, adj=2, cw2=[4, 10], height=self._button_height)

        cmds.text(l=u"", w=4)
        cmds.checkBox(self.rigid_body_cb,
                      l=u"リジッド（角や棘）モード ※開いたトポロジ",
                      height=self._button_height,
                      width=(self._window_width / 2))

        cmds.setParent("..")

        cmds.iconTextButton(self.lod_translate_btn,
                            image1=self.lod_icon,
                            label=u"LOD にウェイト転送",
                            width=(self._window_width / 2) - 10,
                            height=self._button_height,
                            style='iconAndTextHorizontal',
                            bgc=(0.3, 0.3, 0.3),
                            # en=False,
                            command=partial(self.copy_weight_lod_auto)
                            )

        cmds.setParent("..")

        btn_num = cmds.frameLayout(self.frame_b, q=True, nch=True)
        all_btn_num += btn_num
        self.set_frame_height(self.frame_b, btn_num)

        cmds.frameLayout(self.frame_c,
                         l=u"ウェイトデータの読み込み / 保存",
                         mh=10,
                         cll=True,
                         cc=partial(self.close_frame_cb, self.frame_c),
                         ec=partial(self.open_frame_cb, self.frame_c),
                         labelVisible=True,
                         width=self._window_width)

        cmds.iconTextButton(self.open_directory_dialog_btn,
                            image1=self.open_directory_dialog_icon,
                            label=u"ウェイトファイルの保存場所の指定",
                            width=(self._window_width / 2) - 10,
                            style='iconAndTextHorizontal',
                            height=self._button_height,
                            bgc=(0.3, 0.3, 0.3),
                            command=partial(self.open_file_dialog),
                            e=False
                            )

        cmds.iconTextButton(self.save_weight_btn,
                            image1=self.save_icon,
                            label=u"選択ジオメトリ の ウェイトの保存",
                            width=(self._window_width / 2) - 10,
                            style='iconAndTextHorizontal',
                            height=self._button_height,
                            bgc=(0.3, 0.3, 0.3),
                            command=partial(self.save_weight_data),
                            e=False
                            )

        cmds.iconTextButton(self.load_weight_btn,
                            image1=self.open_icon,
                            label=u"選択ジオメトリ に ウェイトの読み込み",
                            width=(self._window_width / 2) - 10,
                            style='iconAndTextHorizontal',
                            height=self._button_height,
                            bgc=(0.3, 0.3, 0.3),
                            command=partial(self.load_weight_data, "index"),
                            e=False
                            )

        cmds.iconTextButton(
            image1=self.open_auto_icon,
            label=u"選択ジオメトリ に ウェイトの読み込み（自動修復）",
            width=(self._window_width / 2) - 10,
            style='iconAndTextHorizontal',
            height=self._button_height,
            bgc=(0.3, 0.3, 0.3),
            command=partial(self.load_weight_data, "normalize"),
            e=False
        )

        cmds.setParent("..")

        btn_num = cmds.frameLayout(self.frame_c, q=True, nch=True)

        all_btn_num += btn_num
        self.current_btn_num = all_btn_num

        self.set_frame_height(self.frame_c, btn_num)
        self.set_window_size()

        cmds.showWindow(NAME)

        self.init_scene_data()
        cmds.scriptJob(parent=NAME, event=["SceneOpened", partial(self.init_scene_data)])
        cmds.scriptJob(parent=NAME, event=["NewSceneOpened", partial(self.init_scene_data)])

    def open_file_dialog(self, *args):
        """ディレクトリ選択ダイアログ表示
        """
        result = cmds.fileDialog2(startingDirectory=self.work_dir,
                                  fileMode=3,
                                  dialogStyle=2,
                                  okCaption=u"ディレクトリ選択",
                                  caption=u"ウェイトファイルの保存先を指定してください")
        if result:
            self.work_dir = result[0].replace(os.sep, '/')

    def open_confluence(self, *args):
        """ヘルプサイト表示
        """
        _web_site = "https://wisdom.cygames.jp/display/mutsunokami/Maya+:Easy+Bind"
        try:
            webbrowser.open(_web_site)
        except Exception as e:
            print("error--- ", e)

    def set_frame_height(self, frame_name="", btn_num=1):
        """各フレームの高さ設定

        Args:
            frame_name (str): フレームのUI 名
            btn_num (int): フレームに入るボタンの数
        """
        cmds.frameLayout(
            frame_name,
            e=True,
            h=btn_num * self._button_height + 20
        )

    def close_frame_cb(self, *args):
        """フレームを折りたたんだ時の動作
        """
        frame_name = args[0]
        btn_num = cmds.frameLayout(frame_name, q=True, nch=True)
        self.current_btn_num = self.current_btn_num - btn_num
        self.set_frame_height(frame_name, 0)
        self.set_window_size()

    def open_frame_cb(self, *args):
        """フレームを展開したときの動作
        """
        frame_name = args[0]
        btn_num = cmds.frameLayout(frame_name, q=True, nch=True)
        self.current_btn_num = self.current_btn_num + btn_num
        self.set_frame_height(frame_name, btn_num)
        self.set_window_size()

    def set_window_size(self):
        """最終的なウィンドウサイズの調整
        """
        all_size = self.current_btn_num * self._button_height + 60
        cmds.columnLayout(self.column_layout, e=True, h=all_size)
        cmds.window(NAME, e=True, h=all_size)

    def close_event(self, *args):
        """ツールウィンドウを閉じたときの動作
        選択順を記憶する設定を元に戻す
        """
        cmds.selectPref(tso=self._tso_flag)

    def _trackSelectionOrder_flag(self):
        """ウェイトコピーの際に選択順に適用するための関数
        元の設定をとっておきツール終了時に元に戻す
        Returns:
            [bool]: 元の設定のフラグ
        """
        _tso_flag = cmds.selectPref(q=True, tso=True)
        self._tso_flag = _tso_flag
        if not _tso_flag:
            cmds.selectPref(tso=True)
        return _tso_flag

    def load_weight_data(self, *args):
        """ウェイト読み込みボタンの動作
        Args:
            args (str): index, normalize
        index: デフォルト動作（読み込み前に0 書き込み）
        normalize: 読み込み時にノーマルらいず
        """

        meshes = command.get_meshes()
        if not meshes:
            return

        method = "index"
        if args:
            method = args[0]

        _flags = 0
        with command.ProgressWindowBlock(title='Load Weight', maxValue=len(meshes)) as prg:
            prg.step(1)
            for mesh in meshes:
                mesh_short_name = mesh.split("|")[-1]
                prg.step(1)
                prg.status = '{} ...'.format(mesh_short_name)
                if prg.is_cancelled():
                    break
                skin_cluster = self.get_skin_cluster(mesh)
                if not skin_cluster:
                    continue

                exchange_name = mesh.replace('|', '_').replace(':', '__')
                file_name = "{}.xml".format(exchange_name)

                weight_file_path = os.path.join(self.work_dir, file_name)

                if not os.path.exists(weight_file_path):
                    _flags += 1
                    continue

                if method != "normalize":
                    command.set_weight_zero(mesh, skin_cluster)

                command.load_weight_file_cmds(mesh, self.work_dir, file_name, self.scene_basename, "", "index")

                if method == "normalize":
                    cmds.skinCluster(skin_cluster, e=True, forceNormalizeWeights=True)
        if _flags:
            _m = u"{} 個のウェイトデータは見つかりませんでした".format(_flags)
            command._message_dialog(_m)

    def save_weight_data(self, *args):
        """ウェイトデータ保存
        """
        meshes = command.get_meshes()
        if not meshes:
            return

        with command.ProgressWindowBlock(title='Save Weight', maxValue=len(meshes)) as prg:
            prg.step(1)
            for mesh in meshes:

                mesh_short_name = mesh.split("|")[-1]
                prg.step(1)
                prg.status = '{} ...'.format(mesh_short_name)
                if prg.is_cancelled():
                    break
                skin_cluster = self.get_skin_cluster(mesh)
                if not skin_cluster:
                    continue

                exchange_name = mesh.replace('|', '_').replace(':', '__')
                file_name = "{}.xml".format(exchange_name)
                command.save_weight_file_cmds(mesh, self.work_dir, file_name, self.scene_basename)

    def go_to_bind(self, *args):
        command.go_to_bindpose()

    def get_skin_cluster(self, node):
        flag = None
        _historys = cmds.listHistory(node)
        if _historys:
            for _history in _historys:
                if cmds.nodeType(_history) == "skinCluster":
                    flag = _history
                    break
        return flag

    def bind_select_nodes(self, *args):
        sel = cmds.ls(sl=True, type="transform")

        if not sel:
            command._message_dialog(u"トランスフォームノードを選択してから実行してください")
            return

        joints = []
        meshes = []

        for node in sel:
            shapes = cmds.listRelatives(node, c=True, type="mesh", fullPath=True, ni=True)
            if shapes:
                shape = [x for x in shapes if not cmds.getAttr("{}.intermediateObject".format(x))][0]
                meshes.append(shape)
            else:
                joints.append(node)

        if not joints:
            command._message_dialog(u"選択にジョイントが含まれていません")
            return
        if not meshes:
            command._message_dialog(u"選択にメッシュが含まれていません")
            return

        command.bind_skin(meshes, joints)

    def bind_skin(self, *args):
        _mutsu_flag = cmds.checkBox(self.mutsu_specification_cb, q=True, value=True)
        joints = command.get_need_joints(_mutsu_flag)
        if not joints:
            command._message_dialog(u"必要なジョイントが見つかりません")
            return

        nodes = self.get_nodes("mesh")
        if not nodes:
            command._message_dialog(u"シーンに必要なメッシュが見つかりません")
            return
        if [x for x in cmds.listHistory(nodes)if cmds.nodeType(x) == "skinCluster"]:
            command._message_dialog(u"既にスキニングされています\n一度バインドを解除してから再度実行してください")
            return

        command.bind_skin(nodes, joints)

    def unbind_skin(self, *args):
        joints = cmds.ls(type="joint", l=True)
        if not joints:
            command._message_dialog(u"必要なジョイントが見つかりません")
            return

        nodes = cmds.ls(type="mesh", l=True)
        if not nodes:
            command._message_dialog(u"必要なメッシュが見つかりません")

        try:
            self.go_to_bind()
        except Exception as e:
            print(e)

        command.unbind_skin(nodes, joints)

    def copy_weight_lod_auto(self):
        _mutsu_flag = cmds.checkBox(self.mutsu_specification_cb, q=True, value=True)
        if not self.scene_name:
            command._message_dialog(u"シーンを開いてから実行してください")
            return

        sel = cmds.ls(sl=True, type="transform")

        if sel:
            transform_meshes = command.get_select_node_in_meshes(sel)
            if not transform_meshes:
                command._message_dialog(u"{}\n以下にメッシュがありません".format(",".join(sel)))
                return
        else:
            transform_meshes = command.get_model_node_in_meshes(self.scene_basename)

            if not transform_meshes:
                command._message_dialog(u"{} 以下の {} にメッシュがありません".format(self.scene_basename, "model"))
                return

        joints = command.get_need_joints(_mutsu_flag)
        if not joints:
            command._message_dialog(u"必要なジョイントが見つかりません")
            return

        lod_groups = command.get_lods()

        if not lod_groups:
            command._message_dialog(u"LOD が存在しません")
            return

        _flags = ""
        with command.ProgressWindowBlock(title='Copy Weight', maxValue=len(lod_groups)) as prg:
            prg.step(1)
            for lod_group in lod_groups:
                prg.step(1)
                prg.status = '{} ...'.format(lod_group)
                if prg.is_cancelled():
                    break
                lod_meshes = command.get_alldescendents_mesh_nodes(lod_group)
                if lod_meshes:
                    for lod_mesh in lod_meshes:
                        parent = cmds.listRelatives(lod_mesh, p=True, type="transform", fullPath=True)[0]
                        short_name = parent.split("|")[-1]
                        base_name = short_name.rsplit("_", 1)[0]

                        base_skin_cluster = ""
                        if base_name in transform_meshes:
                            base_mesh = transform_meshes[base_name]
                            base_skin_cluster = command.get_skincluster(base_mesh)

                        if not base_skin_cluster:
                            continue

                        skin_cluster = command.get_skincluster(lod_mesh)

                        if not skin_cluster:
                            skin_cluster = command.bind_skin_noprogress([lod_mesh], joints)
                            if not skin_cluster:
                                continue
                            skin_cluster = skin_cluster[0]

                        _flags = base_skin_cluster
                        command.weight_copy(base_skin_cluster, skin_cluster)
        if not _flags:
            command._message_dialog(u"処理できるものが見つかりませんでした")

    def copy_weight_selection(self):

        rigid_ck = cmds.checkBox(self.rigid_body_cb, q=True, v=True)

        sel = cmds.ls(os=True, type="transform")
        if not sel:
            command._message_dialog(u"トランスフォームノードを選択してください")
            return
        if len(sel) == 1:
            command._message_dialog(u"二つ以上のトランスフォームノードを選択してください")
            return
        src = sel.pop(0)

        src_mesh = command.get_mesh_shape_node(src)
        dst_meshes = command.get_mesh_shape_node(sel)

        if not src_mesh:
            command._message_dialog(u"コピー元にメッシュが見つかりませんでした")
            return

        src_mesh = src_mesh[0]

        if not dst_meshes:
            command._message_dialog(u"コピー先にメッシュが見つかりませんでした")
            return

        src_skin_cluster = self.get_skin_cluster(src_mesh)
        if not src_skin_cluster:
            command._message_dialog(u"ソースにスキンクラスタがありませんでした")
            return

        dst_skin_clusters = [self.get_skin_cluster(x) for x in dst_meshes]
        if not dst_skin_clusters:
            command._message_dialog(u"ターゲットにスキンクラスタがありませんでした")
            return

        if src_skin_cluster and dst_skin_clusters:
            for dst_skin_cluster in dst_skin_clusters:
                command.weight_copy(src_skin_cluster, dst_skin_cluster)

        if rigid_ck:
            _exsist_flag = True
            for mesh in dst_meshes:
                # [[0, 1], [2, 3]] アイランドID リスト内に FaceID リスト
                island_ids = command.get_polygon_shell(mesh)

                for face_ids in island_ids:
                    # 開いた部分の1頂点と、アイランドの全頂点、1頂点のポジション
                    _one, _island_vtx, _position = command.get_boundary_one_vtx(mesh, face_ids)
                    if not _one:
                        _exsist_flag = False
                        continue
                    _weight = command.get_weight_data_vtx(mesh, _one)
                    command.set_weight_data_vtx(mesh, _weight, _island_vtx)
            if not _exsist_flag:
                command._message_dialog(u"棘の形状は開いたトポロジにしてください")

    def get_scene_name(self, *args):
        """シーン名を取得
        cmds で取得できないシーンがあったのでOpenMayaでも取得を試みる
        ただし、OpenMayaの場合は開いていなくても文字列は空にならないので
        そのための対処
        """
        work_dir = ""
        scene_name = getCurrentSceneFilePath()
        if not scene_name:
            scene_name = om.MFileIO.currentFile()

        if len(scene_name.split(".")) < 2:
            scene_name = ""

        if scene_name:
            self.scene_name = scene_name
            path, basename = os.path.split(scene_name)
            _path, scene_dir = os.path.split(path)
            work_dir = os.path.join(_path, "workbench").replace(os.sep, '/')
            if not os.path.exists(work_dir):
                try:
                    os.makedirs(work_dir)
                except Exception as e:
                    print(e)
                    work_dir = path.replace(os.sep, '/')

            self.work_dir = work_dir
            if basename[:4] != "mdl_":
                scene_name = ""
            self.scene_basename = basename.rsplit(".")[0]

        if not scene_name:
            self.scene_name = ""

    def get_root_node(self):
        root_nodes = cmds.ls(assemblies=True)
        for node in root_nodes:
            if node.startswith("mdl_"):
                self.root_node = node
                break

    def init_scene_data(self, *args):
        # self.bind_flag = False
        # self.exists_flag = False

        self.weight_files = []

        self.scene_basename = ""
        self.root_node = ""

        self.get_scene_name()

    def get_icons(self):
        self.bind_icon = os.path.join(ICON_PATH, "bind.png")
        self.bind_mutsu_icon = os.path.join(ICON_PATH, "bind_mutsu.png")
        self.bind_auto_icon = os.path.join(ICON_PATH, "bind_auto.png")
        self.bind_select_icon = os.path.join(ICON_PATH, "bind_select.png")
        self.unbind_icon = os.path.join(ICON_PATH, "detachSkin.png")
        # self.select_icon = os.path.join(ICON_PATH, "select.png")
        # self.select_all_icon = os.path.join(ICON_PATH, "joint_object.png")
        self.gotobind_icon = os.path.join(ICON_PATH, "gotobind.png")
        self.joint_icon = os.path.join(ICON_PATH, "joint.png")
        self.open_icon = os.path.join(ICON_PATH, "open.png")
        self.open_auto_icon = os.path.join(ICON_PATH, "open_auto.png")
        self.save_icon = os.path.join(ICON_PATH, "save.png")
        self.cube_icon = os.path.join(ICON_PATH, "cube.png")
        self.lod_icon = os.path.join(ICON_PATH, "translate.png")
        self.copy_skin_weight = os.path.join(ICON_PATH, "copySkinWeight.png")
        self.nodes_with_lod_icon = os.path.join(ICON_PATH, "nodes_with_lod.png")
        self.nodes_not_with_lod_icon = os.path.join(ICON_PATH, "nodes_not_with_lod.png")
        self.nodes_with_joints_lod_icon = os.path.join(ICON_PATH, "nodes_with_joints_lod.png")
        self.open_directory_dialog_icon = os.path.join(ICON_PATH, "fileOpen.png")

    def select_joints(self, *args):
        mods = cmds.getModifiers()
        _mutsu_flag = cmds.checkBox(self.mutsu_specification_cb, q=True, value=True)

        joints = command.get_need_joints(_mutsu_flag)
        if joints:
            if mods == 4:
                cmds.select(joints, add=True)
            else:
                cmds.select(joints, r=True)
        else:
            cmds.select(clear=True)

    def select_all(self, *args):
        _mutsu_flag = cmds.checkBox(self.mutsu_specification_cb, q=True, value=True)
        joints = command.get_need_joints(_mutsu_flag)
        # nodes = self.get_bind_mesh("transform")
        nodes = self.get_nodes("transform")

        select_nodes = []
        if joints:
            select_nodes = joints
        if nodes:
            select_nodes += nodes
        if select_nodes:
            cmds.select(select_nodes, r=True)

    def select_meshes(self, *args):
        mods = cmds.getModifiers()
        # nodes = self.get_bind_mesh("transform")
        nodes = self.get_nodes("transform")
        if nodes:
            if mods == 4:
                cmds.select(nodes, add=True)
            else:
                cmds.select(nodes, r=True)

    def select_meshes_no_lod(self, *args):
        mods = cmds.getModifiers()
        # nodes = self.get_bind_mesh("transform", False)
        nodes = self.get_nodes("transform", False)
        if nodes:
            if mods == 4:
                cmds.select(nodes, add=True)
            else:
                cmds.select(nodes, r=True)

    def get_nodes(self, node_type="transform", lod=True):
        if not self.scene_name:
            command._message_dialog(u"シーンを開いてから実行してください")
            return

        node_list = []
        inside_model_group = command.get_model_node_in_meshes(self.scene_basename, True)

        if not inside_model_group:
            return
        if node_type == "transform":
            node_list = list(inside_model_group.keys())
        else:
            node_list = list(inside_model_group.values())

        if lod:
            lod_groups = command.get_lods()
            if lod_groups:
                for lod_group in lod_groups:
                    inside_group = command.get_group_in_meshes(lod_group, True)
                    if inside_group:
                        if node_type == "transform":
                            node_list.extend(list(inside_group.keys()))
                        else:
                            node_list.extend(list(inside_group.values()))

        return node_list


def main():
    if not DEV_MODE:
        logger.send_launch(u'ツール起動')
    eb = EasyBindUI()
    eb.create()
