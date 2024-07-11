# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import os
import sys

try:
    # gallop_maya_bootバッチから起動していれば各バージョンのサイトパッケージのパスが通っているはず
    # py2: %APPDATA%\TKG\GallopBoot\libs\python\python27\site-package
    # py3: %APPDATA%\TKG\GallopBoot\libs\python\python37\site-package
    if sys.version_info.major != 2:
        # ffmpeg
        appdata_path = os.getenv('APPDATA')
        ffmpeg_dir = os.path.join(appdata_path, 'TKG\\GallopBoot\\apps\\gpl\\ffmpeg-n5.0-latest-win64-gpl-shared-5.0\\bin')
        path_list = os.environ["Path"].split(';')
        if ffmpeg_dir not in path_list:
            os.environ["path"] += os.pathsep + ffmpeg_dir

        # ffmpeg-python
        import ffmpeg

    else:
        import cv2

except Exception:
    pass

import maya.cmds as cmds


class MovieCompresser(object):

    def __init__(self):

        self.is_module_imported = False

        if not sys.version_info.major == 2:
            # Maya 2022-
            if "ffmpeg" in sys.modules:
                self.is_module_imported = True
        else:
            if "cv2" in sys.modules:
                self.is_module_imported = True

    def compress_avi_to_mp4(self, avi_path, mp4_path, remove_org_avi=True, should_view_mp4=False):
        """aviをmp4形式に圧縮
        Maya2022以前と以降で使用モジュールを分ける

        Args:
            avi_path (str): 圧縮するaviのパス
            mp4_path (str): 出力するmp4のパス
            remove_org_avi (bool, optional): mp4出力後にaviを削除するか. Defaults to True.
            should_view_mp4 (bool, optional): mp4出力後にmp4を再生するか. Defaults to False.
        """

        if not sys.version_info.major == 2:
            # Maya 2022-
            self.compress_avi_to_mp4_with_ffmpeg(avi_path, mp4_path, remove_org_avi, should_view_mp4)
        else:
            self.compress_avi_to_mp4_with_cv2(avi_path, mp4_path, remove_org_avi, should_view_mp4)

    def compress_avi_to_mp4_with_cv2(self, avi_path, mp4_path, remove_org_avi, should_view_mp4):
        """openCVを使ってaviをmp4形式に圧縮

        Args:
            avi_path (str): 圧縮するaviのパス
            mp4_path (str): 出力するmp4のパス
            remove_org_avi (bool, optional): mp4出力後にaviを削除するか
            should_view_mp4 (bool, optional): mp4出力後にmp4を再生するか
        """

        if not self.is_module_imported:
            print('cv2のimportが失敗しています')
            return False

        if not os.path.exists(avi_path):
            return False

        # 動画ファイルを読み込む
        try:
            video = cv2.VideoCapture(avi_path)

            if not video.isOpened():
                print('読み込み失敗')
                video.release()
                return
        except Exception as e:
            print(e)
            return False

        if os.path.exists(mp4_path):

            is_skip_path = False

            # 削除出来ない場合はファイルが閉じているか確認する
            while True:
                try:
                    os.remove(mp4_path)
                    break
                except Exception:
                    ans = cmds.confirmDialog(
                        title=os.path.basename(mp4_path),
                        message='{}\n出力ファイルが閉じられているか確認してください'.format(mp4_path),
                        button=['Retry', 'Skip'],
                        defaultButton='Retry',
                        cancelButton='Skip',
                        dismissString='Skip')
                    if ans == 'Skip':
                        is_skip_path = True
                        break

            if is_skip_path:
                return False

        # 幅と高さを取得
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # 奇数だと圧縮できないので偶数に直す
        if (width % 2) > 0:
            width += 1
        if (height % 2) > 0:
            height += 1
        size = (width, height)

        # 総フレーム数を取得
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # フレームレート(1フレームの時間単位はミリ秒)の取得
        frame_rate = int(video.get(cv2.CAP_PROP_FPS))

        # 保存用
        fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')
        writer = cv2.VideoWriter(mp4_path, fmt, frame_rate, size)

        for i in range(frame_count):
            ret, frame = video.read()
            frame = cv2.resize(frame, dsize=size)
            writer.write(frame)
        writer.release()
        video.release()
        cv2.destroyAllWindows()
        if remove_org_avi:
            os.remove(avi_path)
        print('圧縮完了 >>> {}'.format(mp4_path))

        if should_view_mp4 and os.path.exists(mp4_path):
            os.startfile(mp4_path, 'open')

        return True

    def compress_avi_to_mp4_with_ffmpeg(self, avi_path, mp4_path, remove_org_avi, should_view_mp4):
        """ffmpegを使ってaviをmp4形式に圧縮

        Args:
            avi_path (str): 圧縮するaviのパス
            mp4_path (str): 出力するmp4のパス
            remove_org_avi (bool, optional): mp4出力後にaviを削除するか
            should_view_mp4 (bool, optional): mp4出力後にmp4を再生するか
        """

        if not self.is_module_imported:
            print('ffmpegのimportが失敗しています')
            return False

        if not os.path.exists(avi_path):
            return False

        # 動画ファイルを読み込む
        video = None
        stream = None
        try:
            video = ffmpeg.probe(avi_path)
            stream = ffmpeg.input(avi_path)

            if not video or not stream:
                print('読み込み失敗')
                return
        except Exception as e:
            print(e)
            return False

        if os.path.exists(mp4_path):

            is_skip_path = False

            # 削除出来ない場合はファイルが閉じているか確認する
            while True:
                try:
                    os.remove(mp4_path)
                    break
                except Exception:
                    ans = cmds.confirmDialog(
                        title=os.path.basename(mp4_path),
                        message='{}\n出力ファイルが閉じられているか確認してください'.format(mp4_path),
                        button=['Retry', 'Skip'],
                        defaultButton='Retry',
                        cancelButton='Skip',
                        dismissString='Skip')
                    if ans == 'Skip':
                        is_skip_path = True
                        break

            if is_skip_path:
                return False

        # 幅と高さを取得
        is_crop = False
        height = video["streams"][0]["coded_height"]
        if height % 2 != 0:
            height = height - 1
            is_crop = True

        width = video["streams"][0]["coded_width"]
        if width % 2 != 0:
            width = width - 1
            is_crop = True
        # 奇数だと圧縮できないので偶数に直す
        if is_crop:
            stream = ffmpeg.crop(stream, 0, 0, width, height)

        stream = ffmpeg.output(stream, mp4_path, pix_fmt='yuv420p', vcodec='libx264')
        stream = ffmpeg.overwrite_output(stream)

        ffmpeg.run(stream)

        if remove_org_avi:
            os.remove(avi_path)
        print('圧縮完了 >>> {}'.format(mp4_path))

        if should_view_mp4 and os.path.exists(mp4_path):
            os.startfile(mp4_path, 'open')

        return True
