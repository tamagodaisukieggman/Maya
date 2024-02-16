# -*- coding: utf-8 -*-
u"""指定座標位置のスクリーンショット撮影を行う
PILがmayaに入っているpipモジュール並びにpythonコンパイルだとエラーを吐くため、
PILモジュールのスクリーンショット機能をpyinstallerでexe化して実行している
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import subprocess

try:
    # Maya2022-
    from builtins import str
    from builtins import object
except Exception:
    pass


class ScreenshotCapture(object):

    def __init__(self):

        root = os.path.abspath(os.path.dirname(__file__))
        self.pil_screenshot_exe_path = os.path.join('{}\\resources'.format(root), 'PIL_ScreenShot.exe')

    def screenshot_capture(self, posx, posy, size_h, size_w, path):
        u"""ScreenShot撮影を行う
        PILがmayaに入っているpipモジュール並びにpythonコンパイルだとエラーを吐くため、
        PILモジュールをpyinstallerでexe化したアプリケーションを利用している
        将来的には(具体的にはpython3対応したmaya2022移行後)PILモジュールを利用したい

        Args:
            posx ([type]): スクリーンショットを行う左上点のX座標位置
            posy ([type]): スクリーンショットを行う左上点のY座標位置
            size_h ([type]): スクリーンショットを行う縦範囲
            size_w ([type]): スクリーンショットを行う横範囲
            path ([type]): スクリーンショット保存ファイルフルパス

        Returns:
            [type]: [description]
        """

        if not os.path.exists(self.pil_screenshot_exe_path):
            return False

        subprocess.check_call(
            [
                self.pil_screenshot_exe_path,
                str(posx),
                str(posy),
                str(size_h),
                str(size_w),
                path
            ]
        )

        if not os.path.exists(path):
            return False

        return True
