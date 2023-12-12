# -*- coding: utf-8 -*-
import os
import subprocess
import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMaya as om
import tool_log

import shr.model.rename_lod.command as cmd
from .maya_utils import MayaUtil
from .est_utils import eSTRigDisonnector


# ------------------------------------------
# 定数
# ------------------------------------------
INFO_NAMES = {"path": "{}_export_path", "name": "{}_export_name"}
PROXY_MESH_GRP_NAME = "proxy_mesh_grp"
MESH_GRP_NAME = "mesh"
RIG_GRP_NAME = "rig_grp"
HUMAN_TYPE = ["ply", "npc", "mob"]
DEV = False


class Exporter:
    def __init__(self, prep_type: str):
        self.force = False
        self.prep_type = prep_type
        self.export_target_grps = []
        self.exported_fbx_paths = []
        self.Info_path = self._get_info(INFO_NAMES["path"])
        self.Info_name = self._get_info(INFO_NAMES["name"])

    # ------------------------------------------
    # Pathの取得
    # ------------------------------------------
    @staticmethod
    def get_current_scene_path():
        """現在開いているシーンのパスを取得

        Returns:
            rtn{dict}: path,nameを返す
        """
        fullpath = cmds.file(q=True, sn=True)
        filepath = os.path.dirname(fullpath)
        filename = os.path.basename(fullpath).split(".", 1)[0]
        rtn = {"path": filepath, "name": filename}
        return rtn

    # @staticmethod
    def get_current_saved_path(self):
        """現在シーンに保存されているシーンのパスを取得

        Returns:
            rtn{dict}: path,nameを返す
        """
        filepath = cmds.fileInfo(self.Info_path, query=True)[0]
        filename = cmds.fileInfo(self.Info_name, query=True)[0]
        rtn = {"path": filepath, "name": filename}
        return rtn

    @staticmethod
    def get_current_fbx_path(prep_type: str):
        """相対的にfbxのパスを取得

        Returns:
            str: ファイルパス
        """
        if prep_type == "animation" or prep_type == "mh_animation":
            directory = "fbx"
        else:
            directory = "mesh"
        filepath = (
            Exporter.get_current_scene_path()["path"].rsplit("/", 2)[0]
            + "/"
            + directory
        )
        return filepath

    # ------------------------------------------
    # preprocess
    # ------------------------------------------
    def _get_target_joints(self, selected) -> list:
        """
        選択以下の骨を取得
        prepで使用
        """
        root = cmds.listRelatives(selected, type="joint", pa=True, c=True) or []
        target_joints = cmds.listRelatives(root, type="joint", pa=True, ad=True)
        target_joints.extend(root)
        return target_joints

    def _get_group(self, selected, group_type) -> str or None:
        """rootグループ以下の子グループの取得
        proxy_meshとmeshグループのみ対応
        prepで使用

        Args:
            selected (_type_): 選択しているtransform(rootを選択している想定)
            group_type (_type_): root以下のグループを指定

        Returns:
            str: group名を返す
        """
        groups = cmds.listRelatives(selected, c=True, type="transform", f=True) or []

        # proxy_meshのgroupを検索
        if group_type == "proxy_mesh":
            for lp in groups:
                if PROXY_MESH_GRP_NAME in lp:
                    return lp

        elif group_type == "mesh":
            for lp in groups:
                if lp.endswith(MESH_GRP_NAME):
                    return lp

        # 未使用
        elif group_type == "rig":
            for lp in groups:
                if lp.endswith(RIG_GRP_NAME):
                    return lp

    def _delete_end_joints(self, target_joints: list) -> None:
        """選択以下の骨を取得
        prepで使用

        Args:
            target_joints (list): 削除する候補のジョイントをリストで渡す
        """
        for lp in target_joints:
            if lp.endswith("end"):
                cmds.delete(lp)
                print("delete endjoint >> %s" % lp)

    def _create_shader(self, name: str, node_type="lambert") -> any:
        """
        shaderの作成
        proxymesh用に用意したものなので、基本はlambertのみで運用
        """
        mtl = cmds.shadingNode(node_type, name=name, asShader=True)

        sg = cmds.sets(
            name="%sSG" % name, empty=True, renderable=True, noSurfaceShader=True
        )
        cmds.connectAttr("%s.outColor" % mtl, "%s.surfaceShader" % sg)

        src_mtl = name.rsplit("_", 1)[0]
        color = cmds.getAttr(src_mtl + ".color")

        cmds.setAttr(mtl + ".color", *color[0], type="double3")
        return mtl, sg

    def _asign_shader(self, meshes, sg) -> None:
        """
        shaderのassign
        proxymesh用に用意したものなので、基本はlambertのみで運用
        """
        meshes = cmds.ls(meshes, dag=True, type="mesh", noIntermediate=True)
        cmds.sets(meshes, forceElement=sg)

    def _get_ns(self, selected: list) -> str:
        """選択ノードのネームスペースを取得

        Returns:
            str: ネームスペースの文字列
        """
        ns = selected[0].split(":")[0]
        return ns

    def _model_prep(self) -> bool:
        """
        skeletalmeshのエクスポート前に行うシーンのクリーンアップ
        """
        is_raise = False
        try:
            selected = cmds.ls(sl=True)
            target_joints = self._get_target_joints(selected)

            proxy_mesh_grp = self._get_group(selected, "proxy_mesh")

            mesh_grp = self._get_group(selected, "mesh")

            # エクスプレッションの削除
            cmds.delete(cmds.ls(type="expression"))

            # eST関係のConstraintとコネクションを切る
            if cmds.objExists("animPlugs"):
                eSTRigDisonnector.exec_est_disconnect("")

            # assume preferred angleをかける
            cmds.joint(target_joints, apa=True, e=True, ch=True)

            # bindposeの作り直し
            MayaUtil.recreate_bindpose(target_joints)

            # rigのグループは削除
            rig_grps = []
            if cmds.objExists("rig"):
                rig_grps.append(cmds.ls("rig")[0])
            rig_grps.append(self._get_group(selected, "rig"))
            if rig_grps != [None]:
                cmds.delete(rig_grps)
            if cmds.objExists("rig_grp"):
                cmds.delete("rig_grp")

            self._get_group(selected, "mesh")

            lod_grps = cmds.listRelatives(mesh_grp, c=True, pa=True) or []
            # meshのgroupをlodグループに置き換え
            if cmds.objectType(mesh_grp) == "transform":
                MayaUtil.replace_transform_to_lodgroup(mesh_grp)

            # proxy_mesh_grpが存在していれば
            if proxy_mesh_grp != None:
                # proxy_meshの整理
                proxy_meshes = cmds.listRelatives(
                    proxy_mesh_grp, ad=True, f=True, type="transform"
                )

                for lod_grp in lod_grps:
                    lod_proxy_mesh_grp = cmds.duplicate(proxy_mesh_grp)[0]
                    cmds.parent(lod_proxy_mesh_grp, lod_grp)

                    # 同一階層になっているハズという想定
                    for i, tgt_obj in enumerate(
                        cmds.listRelatives(
                            lod_proxy_mesh_grp, ad=True, pa=True, type="transform"
                        )
                    ):
                        src_obj = proxy_meshes[i]
                        MayaUtil.copy_skincluster(src_obj, tgt_obj)

                        # リネームとマテリアルのアサイン（lod0以外）
                        if lod_grp.endswith("lod0"):
                            continue
                        lod_sn = MayaUtil.get_short_name(lod_grp)

                        tgt_shape = cmds.listRelatives(tgt_obj, shapes=True, f=True)
                        current_sg = cmds.listConnections(
                            tgt_shape, s=False, d=True, t="shadingEngine"
                        )
                        current_mat = cmds.ls(
                            cmds.listConnections(current_sg, s=True, d=False), mat=True
                        )[0]

                        mtl, sg = self._create_shader(current_mat + "_" + lod_sn)
                        self._asign_shader(tgt_obj, sg)
                        cmds.rename(tgt_obj, tgt_obj + "_" + lod_sn)
                    cmds.rename(lod_proxy_mesh_grp, PROXY_MESH_GRP_NAME)
                cmds.delete(proxy_mesh_grp)

            cmds.select(selected, r=True)

            # 削除する前にrootとなるjointを取得

            root = MayaUtil.get_hierarchy_root_joint(target_joints[0])
            self._delete_end_joints(target_joints)
            # root骨をworldにparent
            cmds.parent(root, w=True)

            # 書き出し用のオブジェクトを選択状態へ
            cmds.select(root, r=True)
            cmds.select(selected, add=True)

        except Exception as e:
            print("例外args:", e.args)
            is_raise = True

        return is_raise

    def _sb_low_model_prep(self) -> None:
        """substance用の_lowがついたfbxを書き出す
        書き出し場所は.mesh
        """
        selected = cmds.ls(sl=True)
        # cmd.rename_lods()
        target_joints = self._get_target_joints(selected)
        root = MayaUtil.get_hierarchy_root_joint(target_joints[0])
        mesh_grp = self._get_group(selected, "mesh")
        lod_grps = cmds.listRelatives(mesh_grp, c=True, pa=True) or []
        for lod_grp in lod_grps:
            if "lod0" in lod_grp:
                cmds.parent(lod_grp, w=True)
                children = cmds.listRelatives(ad=True)
                for child in children:
                    if child.endswith("_lod0") == True:
                        new_name = child.replace("_lod0", "_low")
                        cmds.rename(child, new_name)
        # root骨をworldにparent
        cmds.parent(root, w=True)
        lod0 = cmds.ls("lod0")[0]
        cmds.select([lod0], r=True)

        return

    def _mock_model_prep(self) -> None:
        """モックモデル用のpreprocess
        SKで出力するためバインドされていなければ仮の骨を作成してバインド
        """
        selected = cmds.ls(sl=True)
        # cmd.rename_lods()
        target_joint = "root_jnt"

        mesh_grp = self._get_group(selected, "mesh")
        all_shapes = cmds.listRelatives(mesh_grp, ad=True, type="mesh") or []
        all_transform = cmds.listRelatives(all_shapes, ap=True) or []
        cmds.delete(all_transform, ch=True)
        MayaUtil.create_and_bind_temp_joint(all_transform)

        joints = [target_joint]
        children_joint = cmds.listRelatives(target_joint, ad=True, type="joint") or []
        joints.extend(children_joint)
        # バインドポーズを現在のフレームのアニメーションで作り直し
        MayaUtil.recreate_bindpose(joints)

        all_transform.append(target_joint)
        cmds.select(all_transform, r=True)

    def _mh_animation_prep(self) -> bool:
        """
        metahuman用のアニメーション削除

        Raises:
            ValueError: _description_

        Returns:
            bool: _description_
        """
        is_raise = False
        try:
            root = cmds.ls(sl=True)[0]
            if "root" not in root:
                raise ValueError("please after selecting a root joint, execute it.")
            MayaUtil.MH_Command.create_custom_attribute(root)

            # アニメーションをベイク
            MayaUtil.bake_animation(root)

            duplicated_joint = cmds.duplicate(root, ic=True, po=True)
            # 親が存在していればworldにペアレント
            if len(cmds.listRelatives(duplicated_joint, p=True) or []) >= 1:
                duplicated_joint = cmds.parent(duplicated_joint, w=True)

            duplicated_joint = cmds.rename(duplicated_joint, "root_jnt")

            # rootだけにする
            cmds.delete(cmds.listRelatives(c=True))

            # 書き出し用のオブジェクトを選択状態へ
            cmds.select(duplicated_joint, r=True)
        except Exception as e:
            print("例外args:", e.args)
            is_raise = True

        return is_raise


    def _animation_prep(self) -> bool:
        """
        animationのエクスポート前に行うシーンのクリーンアップ
        """

        is_raise = False
        target_joints = []
        try:
            selected = cmds.ls(sl=True)
            target_joints = self._get_target_joints(selected)

            # # 補助骨とモーションポイント以外をベイク
            # for lp in all_joints:
            #     if "_drv" in lp or "_mtp" in lp:
            #         continue
            #     target_joints.append(lp)

            # アニメーションをベイク
            MayaUtil.bake_animation(target_joints)
            if cmds.objExists("animPlugs"):
                eSTRigDisonnector.exec_est_disconnect(self._get_ns(selected))
            # リファレンスを複製(namespaceの除去と編集可の状態へ)

            duplicated = cmds.duplicate(target_joints, ic=True, po=True)
            root = MayaUtil.get_hierarchy_root_joint(duplicated[0])

            # root骨をworldにparent
            cmds.parent(root, w=True)

            # 不要なjointの削除
            self._delete_end_joints(cmds.listRelatives(root, ad=True, type="joint"))

            # 書き出し用のオブジェクトを選択状態へ
            cmds.select(root, r=True)

        except Exception as e:
            print("例外args:", e.args)
            is_raise = True

        return is_raise

    def _organize_sotai_prep(self) -> None:
        """
        素体用の階層整理
        """
        selected = cmds.ls(sl=True)
        target_root_node = selected[0]
        id = self.get_character_info(target_root_node)
        chr_type = id["character_type"]
        mesh_grp = self._get_group(selected, "mesh")
        lod_grps = cmds.listRelatives(mesh_grp, c=True, pa=True) or []

        fc_root = None
        fc_mesh_grp = None

        prefix = ""
        # idの一文字目がprefixになる
        for lp in HUMAN_TYPE:
            if chr_type == lp:
                prefix = lp[0]
        if prefix == "":
            return

        fc_root = cmds.group(
            em=True, w=True, name="{0}fc{1}".format(prefix, id["character_number"])
        )
        fc_mesh_grp = cmds.group(em=True, p=fc_root, name="mesh")

        for lod_grp in lod_grps:
            mesh_parts = cmds.listRelatives(lod_grp, c=True, pa=True)
            for mesh_part in mesh_parts:
                if "face" in mesh_part:
                    fc_lod_grp = cmds.group(
                        em=True, p=fc_mesh_grp, name=MayaUtil.get_short_name(lod_grp)
                    )
                    cmds.parent(mesh_part, fc_lod_grp)

        cmds.select(selected, r=True)
        self.export_target_grps.extend([fc_root])

    def warning_dialog(self):
        """export時の保存警告"""
        selected_btn = cmds.confirmDialog(
            title="Warning",
            message="エクスポートには作業データの保存が必要です\nファイルを保存します。よろしいですか?",
            button=["はい", "いいえ"],
            defaultButton="はい",
            cancelButton="いいえ",
            dismissString="いいえ",
        )
        if selected_btn == "はい":
            cmds.file(s=True, de=True)
            return 1
        else:
            return 0

    def export_result_dialog(self, exported_paths):
        """export完了時の保存先の照会"""
        message = "■export assets"
        export_path = ""
        asset_message = "\n\n  ●export_asset"
        export_message = "\n\n  ●export path"
        for lp in exported_paths:
            export_path, name = lp.rsplit("/", 1)
            export_message += "\n    " + export_path
            asset_message += "\n    " + name + ".fbx"

        message = message + export_message + asset_message
        selected_btn = cmds.confirmDialog(
            title="Result",
            message=message,
            button=["閉じる", "エクスプローラーで開く"],
            defaultButton="閉じる",
            cancelButton="閉じる",
        )
        if selected_btn == "エクスプローラーで開く":
            export_path = export_path.replace("/", "\\")
            subprocess.Popen(["explorer", export_path], shell=True)

    def exec_prep(self):
        """preprocessとしてexport前に実行
        prep系の実行管理
        """
        target_root_node = cmds.ls(sl=True)[0]
        cmds.undoInfo(openChunk=True)
        if self.prep_type == "model":
            id_dict = self.get_character_info(target_root_node)
            # 素体だったら頭と体で別に書き出し(ワークフロー上不要になったのでコメントアウト)
            # if id_dict["detail_category"] == 0:
            #     self._organize_sotai_prep()

            self._model_prep()
        elif self.prep_type == "sb_low_model":
            self._sb_low_model_prep()
        elif self.prep_type == "mock_model":
            self._mock_model_prep()
        elif self.prep_type == "animation":
            self._animation_prep()
        elif self.prep_type == "mh_animation":
            self._mh_animation_prep()
        cmds.undoInfo(closeChunk=True)

    # ------------------------------------------
    # export
    # ------------------------------------------

    def export(self, path="", file_name="") -> None:
        """ベースとなるエクスポート関数

        Args:
            path (str, optional): export先のパス. Defaults to "".
            file_name (str, optional): export先のfbx名. Defaults to "".
        """

        # exportしようとしているfolderが無ければ作成
        os.makedirs(path, exist_ok=True)

        if not DEV:
            self.send_logger()

        # exportできる状態かどうかの確認
        self.check_exportable()
        is_saved = True

        # テスト時はダイアログスキップ
        if self.force == False:
            is_saved = self.warning_dialog()

        if not is_saved:
            cmds.warning("ファイルが保存できませんでした。処理を終了します。")
            return 0

        # exportpathを合成
        exportpath = path + "/{}".format(self.get_fbx_prefix()) + file_name
        self.set_fbx_settings()

        # 整頓して選択状態を変更
        is_raise = self.exec_prep()

        if is_raise:
            cmds.file(cmds.file(q=True, sn=True), o=True, f=True)
            return 0

        try:
            selected_joint = ""
            self.exported_fbx_paths = []

            # substance用の書き出し時のみジョイントの書き出しが不要
            if len(cmds.ls(sl=True, type="joint")) > 0:
                selected_joint = cmds.ls(sl=True, type="joint")[0]

            # 書き出し
            om.MGlobal.executeCommand('FBXExport -f "{0}.fbx" -s'.format(exportpath))
            print("exported >> %s.fbx" % exportpath.replace("/", "\\"))
            self.exported_fbx_paths.append(exportpath)

        except RuntimeError:
            cmds.error(
                "fbxの書き出しができませんでした。fbxファイルが上書きできない状態の可能性があります。ご確認ください。例: 読み取り専用、パスの間違い等"
            )

        # re_open
        cmds.file(cmds.file(q=True, sn=True), o=True, f=True)
        self.export_result_dialog(self.exported_fbx_paths)

    def export_by_currently_fbx_path(self, suffix=""):
        """
        fbxの階層にエクスポート
        Args:
            suffix (str): suffixを設定。なにも入れなければそのまま出力
        """
        filepath = Exporter.get_current_fbx_path(self.prep_type)
        self.export(filepath, Exporter.get_current_scene_path()["name"] + suffix)

    def export_by_currently_scene_path(self, file_name: str) -> None:
        """現在開いているSceneの階層にエクスポート

        Args:
            file_name (str): fbxのファイル名を渡す
        """
        filepath = Exporter.get_current_scene_path()["path"]
        self.export(filepath, file_name)

    def export_by_currently_saved_path(self) -> None:
        """
        現在のinfo保存されている場所にエクスポート
        """
        if cmds.fileInfo(self.Info_path, q=True) == []:
            self.initialize_ui_info()
        paths = self.get_current_saved_path()
        self.export(paths["path"], paths["name"])

    def export_by_dialog(self) -> None:
        """
        ダイアログで指定した場所にエクスポート
        """
        path, name = cmds.fileDialog2(dialogStyle=1)[0].rsplit("/", 1)
        self.export(path, name.split(".")[0])

    # ------------------------------------------
    # command
    # ------------------------------------------

    def set_fbx_settings(self) -> None:
        """
        fbxの保存設定,presetをロードする
        """
        preset_path = os.path.dirname(__file__).replace("\\", "/") + "/presets"

        prep_type = self.prep_type
        if self.prep_type == "sb_low_model" or self.prep_type == "mock_model":
            prep_type = "model"

        elif self.prep_type == "mh_animation":
            prep_type = "animation"

        preset_name = "/" + prep_type + ".fbxexportpreset"
        preset = preset_path + preset_name
        mel.eval('FBXLoadExportPresetFile -f "{}"'.format(preset))

    def check_exportable(self) -> bool:
        # アニメーション以外は名前の整理を実行
        if self.prep_type != "animation" and self.prep_type != "mh_animation":
            cmd.rename_lods()
        if cmds.ls(sl=True) == []:
            cmds.warning("対象が選択されていません。rootとなるノードを選択して実行してください。")
            return False
        return True

    def send_logger(self) -> None:
        """ログ送信用"""
        logger_type = ""
        version = "v2022.09.02"

        if self.prep_type == "model":
            logger_type = "CharacterExporter"
        elif self.prep_type == "animation":
            logger_type = "AnimationExporter"
        elif self.prep_type == "mock_model":
            logger_type = "MockModelExporter"
        elif self.prep_type == "sb_low_model":
            logger_type = "SBLowModelExporter"
        elif self.prep_type == "mh_animation":
            logger_type = "MHAnimationExporter"

        logger = tool_log.get_logger(logger_type, version)
        logger.send_launch("")

    def get_character_info(self, name: str) -> dict:
        """キャラクターの情報の取得

        Args:
            name (str): _description_

        Returns:
            dict: _description_
            {
                detail_category  :<characterid>0***の0に当たる,
                type             :<characterid>*00*の00に当たる,
                variation        :<characterid>***0の0に当たる,
                character_type   :ply,enm等の識別子,
                character_number :<characterid>0000の0000に当たる,
            }
        """
        # scene_name = Exporter.get_current_scene_path()["name"]
        number = name[3:]
        character_id = str(number)

        rtn_info = {}
        rtn_info["detail_category"] = int(character_id[0])
        rtn_info["type"] = int(character_id[0:3])
        rtn_info["variation"] = int(character_id[2])
        rtn_info["character_type"] = name[:3]
        rtn_info["character_number"] = name[3:]

        return rtn_info

    def get_fbx_prefix(self) -> str:
        """fbxのファイル名のprefixを取得
        uasset化したときの命名規則に準拠

        Returns:
            str: prefix
        """
        prefix = ""
        if self.prep_type == "model":
            prefix = "s_"
        elif self.prep_type == "animation":
            prefix = "a_"
        elif self.prep_type == "mock_model":
            prefix = "s_"
        else:
            prefix = ""
        return prefix

    # ------------------------------------------
    # ui
    # ------------------------------------------
    # @staticmethod
    def initialize_ui_info(self):
        """
        fileInfoの初期化(現在のシーンの場所と名前を入れる)
        初めてシーンを開いた際に使用
        アニメーション用
        """
        paths = Exporter.get_current_scene_path()
        fbx_path = Exporter.get_current_fbx_path(self.prep_type)
        cmds.fileInfo(self.Info_path, fbx_path)
        cmds.fileInfo(self.Info_name, paths["name"])

    def _get_info(self, info):
        return info.format(self.prep_type)
