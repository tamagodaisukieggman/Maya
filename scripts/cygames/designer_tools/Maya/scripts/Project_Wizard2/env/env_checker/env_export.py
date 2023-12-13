# -*- coding: utf-8 -*-

import os
import subprocess
import maya.cmds as cmds
import maya.mel as mel


def export_fbx(export_root):
    if type(export_root) == list:
        if len(export_root) != 1:
            cmds.confirmDialog(title='Usage', message='Rootを一つだけ選択し、' +
                               'targetをリセットして実行してください',
                               button=['OK'])
            return
        export_root = export_root[0]
    scene_path = cmds.file(q=True, sn=True)
    starting_dir = os.path.abspath(os.path.join(scene_path, '../..', 'fbx')).replace('\\', '/')
    out_folder = cmds.fileDialog2(caption='出力フォルダを選択してください',
                                  dialogStyle=1, fileMode=3, startingDirectory=starting_dir)
    if not out_folder:
        return
    if len(out_folder) > 1:
        cmds.confirmDialog(title='Usage', message='フォルダは一つだけ選択してください',
                           button=['OK'])
        return
    out_folder = out_folder[0]
    # 背景班にもらったプリセットを使用
    preset_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".",
                     "wizard2_env.fbxexportpreset")
                    ).replace("\\", "/")
    mel.eval('FBXLoadExportPresetFile -f "{}"'.format(preset_path))
    cmds.select(export_root)
    invalid_chars = ['\"', '<', '>', '|', ':', '*', '?', '\\', '/']
    out_file_name = export_root
    for c in invalid_chars:
        out_file_name = out_file_name.replace(c, '')
    export_path = os.path.join(out_folder,
                               out_file_name + '.fbx').replace('\\', '/')
    try:
        print("FBXを出力: " + export_path)
        mel.eval('FBXExport -f "' + export_path + '" -s')
        if os.path.exists(out_folder):
            subprocess.Popen('explorer "{}"'.format(os.path.normpath(out_folder)))
    except Exception as ex:
        cmds.error(ex)
