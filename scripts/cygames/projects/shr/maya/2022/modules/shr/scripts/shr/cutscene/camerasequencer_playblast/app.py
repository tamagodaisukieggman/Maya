# -*- coding: utf-8 -*-
"""CameraSequencerのプレイブラスト機能"""
from __future__ import absolute_import as _absolute_import
# from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os
import glob

from maya import cmds, mel

from shr.cutscene import utility
from shr.cutscene import custom_maya_headsupdisplay


class CutScenePlayBlastExecutor(object):
    def __init__(self, target_viewport_name, setting_dict):
        self.camera_settings = {}
        self.viewport_settings = {}
        self.target_viewport = target_viewport_name
        self.setting_dict = setting_dict

        self.collect_camera_setting()

    def collect_camera_setting(self):
        self.camera_settings = {}

        camera_list = cmds.ls(type="camera")

        for camera in camera_list:
            self.camera_settings[camera] = {
                "displayResolution": cmds.camera(camera, query=True, displayResolution=True),
                "displayGateMask": cmds.camera(camera, query=True, displayGateMask=True)
            }

        self.viewport_settings["CinematicViewPortView"] = {"headsUpDisplay": cmds.modelEditor(self.target_viewport, query=True, headsUpDisplay=False)}

    def set_settings(self):
        """プレイブラスト設定を設定する

        :param settings: プレイブラスト時に設定して欲しい設定
        :type settings: dict
        """
        override_setting = {}
        override_setting["edit"] = True
        override_setting["displayResolution"] = False
        override_setting["displayGateMask"] = False

        for camera_name in self.camera_settings:
            cmds.camera(camera_name, **override_setting)

    def reset_settings(self):
        """設定をリセットする
        """
        for camera_name, camera_setting in self.camera_settings.items():
            reset_setting = camera_setting.copy()
            reset_setting["edit"] = True
            cmds.camera(camera_name, **reset_setting)

        for view_name, view_settings in self.viewport_settings.items():
            reset_setting = view_settings.copy()
            reset_setting["edit"] = True
            cmds.modelEditor(view_name, **reset_setting)

    def start(self):
        cmds.setFocus(self.target_viewport)

        try:
            playblast_settings_formater = PlayBlastSettingsFormater(self.setting_dict)
            playblast_parameter = playblast_settings_formater.create()
            if self.setting_dict["IsOrnaments"]:
                custom_maya_headsupdisplay.create()

        except ValueError as e:
            show_error(e)
        else:
            cmds.playblast(**playblast_parameter)
            custom_maya_headsupdisplay.delete_all()

    def start_playblast(self):
        self.set_settings()
        self.start()
        self.reset_settings()


class PlayBlastSettingsFormater(object):
    def __init__(self, settings_dict):
        self.tool_settings_dict = settings_dict

    def create(self):

        setting_dict = self.tool_settings_dict

        user_viewer = setting_dict["IsView"]

        format_list = get_playblast_format()
        playblast_format = format_list[setting_dict["formatType"]]

        compression_list = get_playblast_compression(format_list[setting_dict["formatType"]])
        compression = compression_list[setting_dict["encodingType"]]

        quality = setting_dict["quality"]
        offscreen = setting_dict["IsOffscreen"]
        resolution_size = (setting_dict["resolutionWidth"], setting_dict["resolutionHeight"])

        is_ornament = setting_dict["IsOrnaments"]
        start_time, end_time = self.__collect_sequencer_time()

        full_file_path = self.create_file_full_path()

        playblast_parameter = {
            "fmt": playblast_format,
            "startTime": start_time,
            "endTime": end_time,
            "sequenceTime": True,
            "forceOverwrite": True,
            "filename": full_file_path,
            "clearCache": True,
            "showOrnaments": is_ornament,
            "percent": 100,
            "wh": resolution_size,
            "viewer": user_viewer,
            "useTraxSounds": True,
            "offScreen": offscreen
        }

        if compression != "" and compression != "global":
            # 圧縮がかかっていた場合のみ圧縮用の設定を追加。
            # ない場合は、グローバルの設定になる
            playblast_parameter["compression"] = compression
            playblast_parameter["quality"] = quality

        playblast_mode = setting_dict["modeType"]
        if playblast_mode == 1:
            target_time_range = get_shotnode_time_range()
            playblast_parameter["startTime"] = target_time_range[0]
            playblast_parameter["endTime"] = target_time_range[1]

        if playblast_mode == 2:
            playblast_parameter["startTime"] = setting_dict["startTime"]
            playblast_parameter["endTime"] = setting_dict["endTime"]

        return playblast_parameter

    def __collect_sequencer_time(self):
        sequencer_object = cmds.sequenceManager(query=True, writableSequencer=True)
        start_time = cmds.getAttr(sequencer_object + ".minFrame")
        end_time = cmds.getAttr(sequencer_object + ".maxFrame")

        return start_time, end_time

    def create_file_full_path(self):
        format_index = self.tool_settings_dict["formatType"]
        target_path = self.tool_settings_dict["directory"]
        file_name = self.tool_settings_dict["fileName"]
        file_number = self.tool_settings_dict["fileNumber"]
        is_file_override = self.tool_settings_dict["IsFileOverride"]

        format_list = cmds.playblast(query=True, format=True)

        target_extension = None
        if format_list[format_index] == "avi":
            target_extension = ".avi"
        elif format_list[format_index] == "qt":
            target_extension = ".mov"

        if not is_file_override:
            # convert_utf = target_path.encode('shift-jis')
            convert_utf = target_path.encode("shift-jis")
            hit_file_list = glob.glob("{directory}/*{extension}".format(directory=convert_utf, extension=target_extension))
            file_name_list = [os.path.basename(os.path.splitext(_)[0]) for _ in hit_file_list]

            number_identifier = utility.NumberIdentifyer(file_name, file_number)
            file_name += number_identifier.identify__max_number_from_file_name(file_name_list)
        else:
            file_name = file_name + file_number

        if os.path.splitext(file_name)[0] != ".avi" and os.path.splitext(file_name)[0] != ".AVI" and os.path.splitext(file_name)[0] != ".mov" and os.path.splitext(file_name)[0] != ".MOV":
            file_name += target_extension

        full_file_path = os.path.abspath(os.path.join(target_path, file_name)).replace("\\", "/")
        return full_file_path


def get_playblast_format():
    return cmds.playblast(query=True, format=True)


def get_playblast_compression(target_format):
    result = mel.eval('playblast -format "{}" -q -compression'.format(target_format))

    return result


def get_shotnode_time_range():
    """Shotノードの時間範囲を取得する

    :return: （最小時間, 最大時間）
    :rtype: tuple
    """
    selection_list = cmds.ls(selection=True)

    extracted_selection_list = utility.extract_data_types(selection_list, "shot")

    if extracted_selection_list == []:
        raise ValueError(u"現在SelectClipModeですが、選択範囲にクリップが存在しません。\nCameraSequencerのクリップを選択してください。")

    time_list = []
    for shot_node in extracted_selection_list:
        time_list.append(cmds.shot(shot_node, query=True, startTime=True))
        time_list.append(cmds.shot(shot_node, query=True, endTime=True))

    return (min(time_list), max(time_list))


def show_error(error):
    """エラーダイアログを表示する

    Args:
        error (Exception): Exceptionクラス
    """
    message = u"{}\n{}".format(type(error), error.message)
    cmds.confirmDialog(title="Error", button="OK", message=message)
