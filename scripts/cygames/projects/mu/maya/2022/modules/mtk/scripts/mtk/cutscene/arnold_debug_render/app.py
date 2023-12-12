# -*- coding: utf-8 -*-
"""Arnoldのレンダリング"""
from __future__ import absolute_import as _absolute_import
# from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os
import subprocess
import shutil

from maya import cmds
from maya import mel
from mtoa.cmds.arnoldRender import arnoldRender
import mtoa.core as core

from mtk.cutscene import utility
from mtk.utils import getCurrentSceneFilePath

DEFAULT_DISPLAY_SIZE = 1920
OUTLINE_SIZE = 1
PADDING = 20
FONT_SIZE = 20

FFMPEG_PATH = "\"Z:/cyllista/tools/ffmpeg/ffmpeg.exe\""
# DEFAULT_FONT_PATH = "C\\\\:/Windows/Fonts/msgothic.ttc"
DEFAULT_FONT_PATH = "C\\\\:/Windows/Fonts/meiryob.ttc"


class ArnoldDebugRender(object):
    @classmethod
    def render(cls, view_settings):
        core.createOptions()

        mel.eval("RenderViewWindow")
        cmds.refresh()

        # ArnoldRenderViewを開く
        # cmds.arnoldRenderView(mode="open")

        arnold_render_settings = ArnoldRenderSettings()
        settings = arnold_render_settings.setup_render_settings(view_settings["camera"])

        render_size = settings["render_size"]
        cls.start_rendering(render_size, settings)

        image_path = settings["image_path"]

        create_image_name = "{}_{}{}".format(settings["image_scene_name"], settings["image_frame"], os.path.splitext(settings["image_path"])[1])

        base_folder = os.path.dirname(image_path)
        image_work_path = os.path.join(base_folder, create_image_name)

        shutil.copy2(image_path, image_work_path)
        os.remove(image_path)

        diameter = (render_size[0] / DEFAULT_DISPLAY_SIZE)
        font_size = int(diameter * FONT_SIZE)
        paddig = int(diameter * PADDING)

        outline_size = int(diameter * OUTLINE_SIZE)
        if outline_size < 1:
            outline_size = 1

        text_setting = {}
        text_setting["work_path"] = image_work_path
        text_setting["font_path"] = DEFAULT_FONT_PATH
        text_setting["font_size"] = font_size
        text_setting["padding"] = (paddig, paddig)
        text_setting["outline_size"] = outline_size
        text_setting["text"] = ""
        text_setting["outline_color"] = "black"
        text_setting["is_outline"] = view_settings["is_draw_outline"]

        if view_settings["Frame"] is True:
            frame = str(int(cmds.currentTime(query=True)))

            frame_text_setting = text_setting.copy()
            frame_text_setting["text"] = frame

            cls.draw_text_right_edge(frame_text_setting)

        if view_settings["SceneName"] is True:
            scene_name = os.path.splitext(os.path.basename(getCurrentSceneFilePath()))[0]
            if scene_name:
                scene_name_settings = text_setting.copy()
                scene_name_settings["text"] = scene_name

                cls.draw_text_left_top(scene_name_settings)

        if view_settings["CutName"] is True:
            clip_name = cmds.sequenceManager(query=True, currentShot=True)

            if clip_name:
                clip_name_settings = text_setting.copy()
                clip_name_settings["text"] = clip_name

                cls.draw_text_left_edge(clip_name_settings)

        if view_settings["FocalLength"] is True:
            focal_length = str(cmds.getAttr(utility.panel.get_camera_from_focus_model_panel() + '.focalLength')) + 'mm'

            focal_length_settings = text_setting.copy()
            focal_length_settings["text"] = focal_length

            cls.draw_text_right_top(focal_length_settings)

        arnold_render_settings.reset_settings()

        if view_settings["is_after_explorer"]:
            os.startfile(os.path.normpath(base_folder))

    @classmethod
    def start_rendering(cls, render_size, render_settings):
        arnoldRender(render_size[0], render_size[1], True, True, render_settings["render_camera"], ' -layer defaultRenderLayer')

    @classmethod
    def draw_text_right_edge(cls, setting):
        """右下にテキストを描画する

        :param setting: テキスト設定
        :type setting: dict
        """
        cls.__draw_text(setting,
                        "(w-text_w-{})",
                        "(w-text_w-{}{}{})",
                        "(h-text_h-{})",
                        "(h-text_h-{}{}{})")

    @classmethod
    def draw_text_right_top(cls, setting):
        """右上にテキストを描画する

        :param setting: テキスト設定
        :type setting: dict
        """
        cls.__draw_text(setting,
                        "(w-text_w-{})",
                        "(w-text_w-{}{}{})",
                        "({})",
                        "({}{}{})")

    @classmethod
    def draw_text_left_top(cls, setting):
        """左上にテキストを描画する

        :param setting: テキスト設定
        :type setting: dict
        """
        cls.__draw_text(setting,
                        "({})",
                        "({}{}{})",
                        "({})",
                        "({}{}{})")

    @classmethod
    def draw_text_left_edge(cls, setting):
        """左下にテキストを描画する。

        :param setting: テキスト設定
        :type setting: dict
        """
        cls.__draw_text(setting,
                        "({})",
                        "({}{}{})",
                        "(h-text_h-{})",
                        "(h-text_h-{}{}{})")

    @classmethod
    def __draw_ffmpeg_text(cls, source_image_path, draw_text, work_path):
        """ffmpegでテキストを描画する

        :param source_image_path: 参加元の画像パス
        :type source_image_path: str
        :param draw_text: テキスト描画コマンド
        :type draw_text: str
        :param work_path: 描画先の画像パス
        :type work_path: str
        """
        command = "{} {} {} {} \"{}\" {} -y".format(FFMPEG_PATH, "-i", source_image_path, "-vf", draw_text, work_path)

        # コンソール非表示
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        subprocess.check_output(command, startupinfo=startupinfo)

    @classmethod
    def __draw_text(cls, setting, width_format, width_outline_format, height_padding_format, height_outline_format):

        split_work_path = os.path.splitext(setting["work_path"])
        tempfile = split_work_path[0] + "temp" + split_work_path[1]
        shutil.copy2(setting["work_path"], tempfile)

        draw_text_command = cls.__create_draw_text_command(setting, width_format, width_outline_format, height_padding_format, height_outline_format)
        cls.__draw_ffmpeg_text(tempfile, draw_text_command, setting["work_path"])

        os.remove(tempfile)

    @classmethod
    def __create_draw_text_command(cls, setting, width_format, width_outline_format, height_padding_format, height_outline_format):
        """複数テキストの描画用コマンドを作成する。

        一つずつffmpeg実行だとかなり待たされることになるので、フィルターを連結して、一括で行う様に、描画コマンドを連結作成する。

        :param setting: テキスト設定
        :type setting: dict
        :param width_format: 横幅用のテンプレート。ffmpegの特殊な文字列を含む。
        :type width_format: str
        :param width_outline_format: 横幅用のアウトラインテンプレート。ffmpegの特殊な文字列を含む。
        :type width_outline_format: str
        :param height_padding_format: 縦幅用のテンプレート。ffmpegの特殊な文字列を含む。
        :type height_padding_format: str
        :param height_outline_format: 縦幅用のアウトラインテンプレート。ffmpegの特殊な文字列を含む。
        :type height_outline_format: str
        :return: ffmpegで実行できるdraw_textコマンド
        :rtype: str
        """
        pattern_list = [
            ("-", setting["outline_size"], "-", 0),
            ("+", setting["outline_size"], "-", 0),
            ("+", 0, "-", setting["outline_size"]),
            ("+", 0, "+", setting["outline_size"]),
            ("-", setting["outline_size"], "+", setting["outline_size"]),
            ("+", setting["outline_size"], "+", setting["outline_size"]),
            ("-", setting["outline_size"], "-", setting["outline_size"]),
            ("+", setting["outline_size"], "-", setting["outline_size"]),
        ]

        command_list = []

        if setting["is_outline"]:
            for count, pattern in enumerate(pattern_list):
                command_list.append(cls.__create_one_draw_text_command(setting["font_path"],
                                                                       width_outline_format.format(setting["padding"][0], pattern[0], pattern[1]),
                                                                       height_outline_format.format(setting["padding"][1], pattern[2], pattern[3]),
                                                                       setting["font_size"],
                                                                       setting["outline_color"],
                                                                       setting["text"]))

                if count == len(pattern_list) - 1:
                    command_list.append(cls.__create_one_draw_text_command(setting["font_path"],
                                                                           width_format.format(setting["padding"][0]),
                                                                           height_padding_format.format(setting["padding"][1]),
                                                                           setting["font_size"],
                                                                           "white",
                                                                           setting["text"]))
        else:
            # アウトラインなし
            command_list.append(cls.__create_one_draw_text_command(setting["font_path"],
                                                                   width_format.format(setting["padding"][0]),
                                                                   height_padding_format.format(setting["padding"][1]),
                                                                   setting["font_size"],
                                                                   "black",
                                                                   setting["text"]))

        # ffmpegの構文様に先頭に[in], 末尾に[out]をつける
        draw_text_command = ", ".join(command_list)
        draw_text_command = "[in]" + draw_text_command
        draw_text_command = draw_text_command + "[out]"
        return draw_text_command

    @classmethod
    def __create_one_draw_text_command(cls, font_path, x, y, font_size, font_color, text):
        """単体テキスト描画コマンドを生成する

        :param font_path: フォントの場所
        :type font_path: str
        :param x: 描画するx座標
        :type x: str
        :param y: 描画するy座標
        :type y: str
        :param font_size: フォントサイズ
        :type font_size: str
        :param font_color: フォントカラー(blackなど文字列指定)
        :type font_color: str
        :param text: 描画する文字列
        :type text: str
        :return: 描画用のコマンド
        :rtype: str
        """
        draw_text = "drawtext=fontfile=\"{font}\":x={x}:y={y}:fontsize={font_size}:fontcolor={font_color}:text=\"{text}\"".format(font=font_path, x=x, y=y, font_size=font_size, font_color=font_color, text=text)
        return draw_text


class ArnoldRenderSettings(object):
    def __init__(self):
        core.createOptions()
        self.__defult_extension = cmds.getAttr("defaultArnoldDriver.ai_translator")
        self.__exr_merge_aovs = cmds.getAttr("defaultArnoldDriver.mergeAOVs")

    def setup_render_settings(self, render_camera):
        file_name = os.path.splitext(os.path.basename(getCurrentSceneFilePath()))[0]
        if file_name == "":
            file_name = "untitled"

        image_file_prefix = cmds.getAttr("defaultRenderGlobals.imageFilePrefix")
        if not image_file_prefix:
            image_file_prefix = file_name

        cmds.setAttr("defaultArnoldDriver.ai_translator", "png", type="string")

        # 2018.5からのバグでexrフォーマットのmergeAOVsがOffだとレンダリング画像に_1が追加されるので実行時にOnにする。
        cmds.setAttr("defaultArnoldDriver.mergeAOVs", 1)

        root_workspace_folder_path = cmds.workspace(fullName=True)
        file_name = image_file_prefix
        image_directory = os.path.join(root_workspace_folder_path, "images", "tmp", file_name + ".png").replace("/", os.sep)

        settings = {}
        settings["image_path"] = image_directory
        settings["image_frame"] = str(cmds.currentTime(query=True))
        settings["image_scene_name"] = file_name
        settings["image_cut_name"] = cmds.sequenceManager(query=True, currentShot=True)

        # view_info = viewport.CinematicViewPortInfo()
        # settings["render_camera"] = view_info.get_camera()

        settings["render_camera"] = render_camera
        settings["render_size"] = self.__get_resolution_size()

        return settings

    def __get_resolution_size(self):
        r_width = cmds.getAttr("defaultResolution.width")
        r_height = cmds.getAttr("defaultResolution.height")
        return (r_width, r_height)

    def reset_settings(self):
        cmds.setAttr("defaultArnoldDriver.ai_translator", self.__defult_extension, type="string")
        cmds.setAttr("defaultArnoldDriver.mergeAOVs", self.__exr_merge_aovs)
