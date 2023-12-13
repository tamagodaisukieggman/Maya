# -*- coding: utf-8 -*-
import maya.cmds as cmds
from shr.file.character_exporter.exporter import Exporter
from shr.file.character_exporter.ue import ue_importer


def mock_model_export(import_ue=True):
    """キャラクターexport用関数"""
    exp = Exporter("mock_model")
    exp.export_by_currently_fbx_path()
    if import_ue == True:
        # filename = exp.get_current_scene_path()["name"]
        ue_importer.sk_uasset_import(False, "skel_mock", exp.exported_fbx_paths)


def sb_low_model_export():
    """キャラクターexport用関数"""
    exp = Exporter("sb_low_model")
    exp.export_by_currently_fbx_path(suffix="_low")


def character_export(import_ue=False, skeleton_name="", create_skeleton=False):
    """キャラクターexport用関数

    Args:
        import_ue (bool, optional): UEへのインポートを使用するかどうか. Defaults to False.
        skeleton_name (str, optional): Skeletonの名前を指定. Defaults to "".
        create_skeleton (bool, optional): Trueなら、スケルトンを新規作成(import_ueがTrueの場合のみ使用). Defaults to False.
    """
    exp = Exporter("model")
    exp.export_by_currently_saved_path()

    if import_ue == True:
        ue_importer.sk_uasset_import(
            create_skeleton,
            skeleton_name,
            exp.exported_fbx_paths,
        )


def ue_import_enginefile(create_skeleton, skeleton_name):
    filepath = cmds.file(q=True, sn=True)
    exp = Exporter("model")

    if not filepath.endswith(".fbx"):
        raise Exception(
            "engine files are not open.please open engine file from workman."
        )

    ue_importer.sk_uasset_import(
        create_skeleton,
        skeleton_name,
        [filepath],
    )


def character_import_ue(import_ue=False, skeleton_name="", create_skeleton=False):
    exp = Exporter("model")
    fbx_path = exp.get_current_fbx_path(exp.prep_type)
    ue_importer.sk_uasset_import(create_skeleton, skeleton_name, fbx_path)


def animation_export():
    """
    個別実行用
    アニメーションエクスポートの関数
    """
    exp = Exporter("animation")
    exp.export_by_currently_saved_path()


def mh_animation_export():
    """
    個別実行用
    metaヒューマンのアニメーションエクスポートの関数
    """
    exp = Exporter("mh_animation")
    exp.export_by_currently_saved_path()
