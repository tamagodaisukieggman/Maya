# -*- coding: utf-8 -*-
u"""PlayBlastを実行する
カメラ指定と表示されているパネルの設定保持の為に
パネルを新規で作成→パネルのカメラ変更→PlayBlast撮影→パネル削除の流れを行っている
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os

import maya.cmds as cmds

# movie_compresserはmaya_boot_bat依存モジュール
from ...glp_compress_playblast import movie_compresser

DEFAULT_CAMERA = 'persp'

try:
    # Maya2022-
    from builtins import object
except Exception:
    pass


class ExecPlayblast(object):

    def __init__(self):

        self.movie_compresser = movie_compresser.MovieCompresser()

        self.window = None
        self.panel = None

    def exec_playblast(
            self, dir_path='', width=256, height=256,
            remove_org_avi=False, should_view_mp4=False, target_panel=''):
        u"""PlayBlastの実行
        """

        if not os.path.exists(dir_path):
            return False

        # 実行中のmaファイルパスを取得
        scene_name = cmds.file(q=True, sceneName=True)
        if not scene_name:
            return False

        scene_short_name_without_ext = os.path.splitext(os.path.basename(scene_name))[0]

        avi_path = os.path.join(dir_path, '{}.avi'.format(scene_short_name_without_ext))
        mp4_path = os.path.join(dir_path, '{}.mp4'.format(scene_short_name_without_ext))

        # PlayBlastの実行
        cmds.playblast(
            format='avi',
            filename=avi_path,
            forceOverwrite=True,
            sequenceTime=0,
            clearCache=0,
            viewer=0,
            showOrnaments=0,
            fp=4,
            percent=95,
            compression='none',
            quality=95,
            width=width,
            height=height,
            editorPanelName=target_panel
        )

        # AVIをmp4形式に圧縮
        self.movie_compresser.compress_avi_to_mp4(avi_path, mp4_path, remove_org_avi, should_view_mp4)

        return True
