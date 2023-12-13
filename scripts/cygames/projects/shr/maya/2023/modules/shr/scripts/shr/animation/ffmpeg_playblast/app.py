# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
# from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os

import ffmpeg

from maya import cmds
from maya import mel

FFMPEG_PATH = "C:/cygames/shrdev/shr/tools/tp/sta/ffmpeg/5.0/bin"


class MP4PlayblastExecutor(object):
    def __init__(self):

        self.avi_path = None
        self.mp4_path = None

        EnvironPathAdder.add(FFMPEG_PATH)

    def start_playblast(self):
        # TODO: 設定は現行の設定に変更する
        frame_padding = cmds.optionVar(query="playblastPadding")

        playblast_offscreen = cmds.optionVar(query="playblastOffscreen")
        sequence_time = cmds.optionVar(query="playblastUseSequenceTime")
        show_ornaments = cmds.optionVar(query="playblastShowOrnaments")
        size_source = cmds.optionVar(query="playblastDisplaySizeSource")

        percent = 100 * cmds.optionVar(query="playblastScale")

        quality = cmds.optionVar(query="playblastQuality")

        clear_cache = cmds.optionVar(query="playblastClearCache")

        playblast_setting = {"fp": frame_padding,
                             "offScreen": playblast_offscreen,
                             "clearCache": clear_cache,
                             "format": "avi",
                             "sequenceTime": sequence_time,
                             "showOrnaments": show_ornaments,
                             "percent": percent,
                             "viewer": 0,
                             "compression": "none",
                             "quality": quality}

        if size_source == 1:
            # 何もしない
            pass
        elif size_source == 2:
            connections = cmds.listConnections(cmds.ls(type="renderGlobals")[0])
            resolution_node = None
            for connect in connections:
                if(cmds.nodeType(connect) == "resolution"):
                    resolution_node = connect

            width = cmds.getAttr(resolution_node + ".width")
            height = cmds.getAttr(resolution_node + ".height")

            playblast_setting["widthHeight"] = (width, height)
        elif size_source == 3:
            width = cmds.optionVar(query="playblastWidth")
            height = cmds.optionVar(query="playblastHeight")

            playblast_setting["widthHeight"] = (width, height)

        save_to_file = cmds.optionVar(query="playblastSaveToFile")

        if save_to_file == 1:
            target_file_path = cmds.optionVar(query="playblastFile")
            target_file_path = self.__convert_avi_path(target_file_path)

            playblast_setting["filename"] = target_file_path
            playblast_setting["forceOverwrite"] = 1

        timeslider = mel.eval("$gPlayBackSlider=$gPlayBackSlider")
        if cmds.timeControl(timeslider, query=True, rangeVisible=True):
            select_time_range = cmds.timeControl(timeslider, query=True, rangeArray=True)
            playblast_setting["startTime"] = select_time_range[0]
            playblast_setting["endTime"] = select_time_range[1]
        
        print(cmds.playblast(**playblast_setting))
        self.avi_path = cmds.playblast(**playblast_setting)

        self.mp4_path = self.avi_path.replace("avi", "mp4")

    def convert_mp4(self):
        print(self.avi_path)
        video_info = ffmpeg.probe(self.avi_path)
        stream = ffmpeg.input(self.avi_path)

        is_crop = False
        height = video_info["streams"][0]["coded_height"]
        if height % 2 != 0:
            height = height - 1
            is_crop = True

        width = video_info["streams"][0]["coded_width"]
        if width % 2 != 0:
            width = width - 1
            is_crop = True

        if is_crop:
            stream = ffmpeg.crop(stream, 0, 0, width, height)

        stream = ffmpeg.output(stream, self.mp4_path, pix_fmt='yuv420p', vcodec='libx264')
        stream = ffmpeg.overwrite_output(stream)

        ffmpeg.run(stream)

    def show_move(self):
        viewer = cmds.optionVar(query="playblastViewerOn")

        if (viewer):
            os.startfile(self.mp4_path)

    def show_explorer(self):
        target_dir = os.path.dirname(self.mp4_path)
        os.startfile(target_dir)

    def delete_avi_file(self):
        os.remove(self.avi_path)

    def __convert_avi_path(self, path):
        split_path = os.path.splitext(path)
        if split_path[1] == "":
            path += ".avi"

        if split_path[1] != ".avi":
            path = split_path[0] + ".avi"

        return path


class EnvironPathAdder(object):
    """Path環境変数にffmpegのパスを追加する必要があるので、用意

    追加する時に重複があった場合は何もしない状態にしてあるので、Add実行するのみ
    """
    @classmethod
    def add(cls, target_dir):
        target_dir = os.path.abspath(target_dir)
        if cls.__check_no_overlap(target_dir):
            os.environ["path"] += os.pathsep + target_dir

    @classmethod
    def __check_no_overlap(cls, target_dir):
        path_list = os.environ["Path"].split(';')

        hit = 0
        for path in path_list:
            if target_dir in path:
                hit += 1

        if hit == 0:
            return True
        else:
            return False


def main():
    ins = MP4PlayblastExecutor()
    ins.start_playblast()

    ins.convert_mp4()

    ins.show_move()
    ins.show_explorer()
    ins.delete_avi_file()


if __name__ == "__main__":
    """デバック用
    """
    main()
