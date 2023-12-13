# -*- coding: utf-8 -*-
u"""StageCameraImporterのGallopベタ移植版
変更点はtatoolsのloggerが読めないので分離とファイルフォーマットのみ

220517: python3対応に際し、settingをgallopのbase_commonに変更 / ファイルが読めない場合の例外処理を追加
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds
import json
import math
import os

from .. import base_common
from ..base_common import classes as base_class

reload(base_common)


class CameraImporter(object):
    def __init__(self):
        u"""
        """

        self.tool_name = "GlpCameraImporter"
        self.window_name = '{}Win'.format(self.tool_name)

        self.setting = None

        self.window_width = 400
        self.window_height = 1
        self.form_width = self.window_width - 5

        self.ui_export_folder = None
        self.ui_magnification = None
        self.ui_import_chara_locator = None

    def show_ui(self):
        u"""UI
        """

        if self.setting is None:
            self.setting = base_class.setting.Setting(self.tool_name)

        self.check_window_already_open()

        cmds.window(self.window_name,
                    title=self.tool_name,
                    widthHeight=(self.window_width, self.window_height),
                    s=True,
                    mnb=True,
                    mxb=False,
                    rtf=True)
        cmds.columnLayout(adjustableColumn=True)

        self.ui_export_folder = cmds.textFieldGrp(label="LogFileFullPath",
                                                  cl2=("left", "left"),
                                                  w=self.form_width,
                                                  cw2=[100, self.form_width - 100],
                                                  text=self.setting.load("exportFolderKey0"),
                                                  tcc=lambda _, x=0, y='exportFolder': self.save_setting(x, y))
        self.ui_magnification = cmds.textFieldGrp(label=u"拡縮倍率",
                                                  cl2=("left", "left"),
                                                  ad2=2,
                                                  w=self.form_width,
                                                  cw2=[100, self.form_width - 100],
                                                  text=self.setting.load("magnificationKey0") if self.setting.load("magnificationKey0") else 100,
                                                  tcc=lambda _, x=0, y='magnification': self.save_setting(x, y))
        self.ui_import_chara_locator = cmds.checkBox(label="ImportCharaLocator", cc=lambda _, x='0', y='checkBoxChara': self.save_setting(x, y))

        this_bool = self.setting.load("checkBoxCharaKey0")
        if this_bool == "True":
            cmds.checkBox(self.ui_import_chara_locator, e=True, v=True)
        elif this_bool == "False":
            cmds.checkBox(self.ui_import_chara_locator, e=True, v=False)

        cmds.button(label="ImportCamera", w=self.form_width, command=lambda _: self.ShowConfirmation())

        cmds.showWindow(self.window_name)

    def check_window_already_open(self):
        u"""すでにウィンドウを開いていないかチェック
        """

        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name, window=True)
        else:
            if cmds.windowPref(self.window_name, exists=True):
                cmds.windowPref(self.window_name, remove=True)

    def ShowConfirmation(self):
        u"""実行確認
        """
        confirm_text = u"実行確認"
        magnification = cmds.textFieldGrp(self.ui_magnification, q=True, text=True)
        print(magnification)

        confirm = cmds.confirmDialog(title=confirm_text,
                                     message=u"実行しますか？",
                                     button=['OK', 'Cancel'],
                                     defaultButton='OK',
                                     cancelButton='Cancel',
                                     dismissString='Cancel')

        if confirm == "OK":
            self.export_root()

    def export_root(self):
        u"""実行
        """
        path = cmds.textFieldGrp(self.ui_export_folder, q=True, text=True)
        magnification = float(cmds.textFieldGrp(self.ui_magnification, q=True, text=True))

        m = self.read_json(path)

        if not m:
            cmds.warning(u'LogFileを読み取れませんでした')
            return

        totalframe = len(m["camera"])

        new_camera, new_camera_shape = cmds.camera()

        # 回転順序修正
        cmds.setAttr("{}.rotateOrder".format(new_camera), 2)
        cmds.setAttr("{}.horizontalFilmAperture".format(new_camera_shape), 1.78)
        cmds.setAttr("{}.verticalFilmAperture".format(new_camera_shape), 1)

        for i in range(0, totalframe):
            tx = -m["camera"][i][0] * magnification
            ty = m["camera"][i][1] * magnification
            tz = m["camera"][i][2] * magnification
            rx = -m["camera"][i][3]
            ry = -m["camera"][i][4] + 180
            rz = m["camera"][i][5]
            fov = float(m["camera"][i][6])
            focal_length = self.get_focal_length(new_camera_shape, fov)

            sec_str = str(i)
            cmds.setKeyframe(new_camera, at='translateX', v=tx, t=[sec_str])
            cmds.setKeyframe(new_camera, at='translateY', v=ty, t=[sec_str])
            cmds.setKeyframe(new_camera, at='translateZ', v=tz, t=[sec_str])
            cmds.setKeyframe(new_camera, at='rotateX', v=rx, t=[sec_str])
            cmds.setKeyframe(new_camera, at='rotateY', v=ry, t=[sec_str])
            cmds.setKeyframe(new_camera, at='rotateZ', v=rz, t=[sec_str])
            cmds.setKeyframe(new_camera_shape, at="focalLength", v=focal_length, t=[sec_str])

        check_box_filter = cmds.checkBox(self.ui_import_chara_locator, q=True, v=True)

        if check_box_filter is False:
            return

        for k in range(1, 6):
            this_locator = cmds.spaceLocator()[0]
            # 回転順序修正
            cmds.setAttr(str(this_locator) + ".rotateOrder", 2)
            for i in range(0, totalframe):
                tx = -m["chara" + str(k)][i][0] * magnification
                ty = m["chara" + str(k)][i][1] * magnification
                tz = m["chara" + str(k)][i][2] * magnification
                rx = -m["chara" + str(k)][i][3]
                ry = -m["chara" + str(k)][i][4]
                rz = m["chara" + str(k)][i][5]

                sec_str = str(i)
                cmds.setKeyframe(this_locator, at='translateX', v=tx, t=[sec_str])
                cmds.setKeyframe(this_locator, at='translateY', v=ty, t=[sec_str])
                cmds.setKeyframe(this_locator, at='translateZ', v=tz, t=[sec_str])
                cmds.setKeyframe(this_locator, at='rotateX', v=rx, t=[sec_str])
                cmds.setKeyframe(this_locator, at='rotateY', v=ry, t=[sec_str])
                cmds.setKeyframe(this_locator, at='rotateZ', v=rz, t=[sec_str])

        cmds.confirmDialog(title=u'完了', message=u'処理が完了しました')

    def get_focal_length(self, camera_shape, unity_fov):
        u"""GetFocalLength

        :param unityFov: unityFov
        :return: mayaのfocal_length
        """
        vfa = cmds.getAttr('{}.verticalFilmAperture'.format(camera_shape))

        focal_length = (0.5 * vfa) / math.tan(unity_fov / (2.0 * 57.29578)) / 0.03937

        return focal_length

    def save_setting(self, set_number, type_name, *args):
        u"""SaveSetting

        :param setNumber: setNumber
        :param typeName: typeName
        """

        export_value = ""

        if type_name == "exportFolder":
            export_value = cmds.textFieldGrp(self.ui_export_folder, q=True, text=True)
            xmlKey = "exportFolderKey"
        elif type_name == "magnification":
            export_value = cmds.textFieldGrp(self.ui_magnification, q=True, text=True)
            xmlKey = "magnificationKey"
        elif type_name == "checkBoxChara":
            export_value = str(cmds.checkBox(self.ui_import_chara_locator, q=True, v=True))
            xmlKey = "checkBoxCharaKey"

        self.setting.save(xmlKey + str(set_number), export_value)

    def write_json(self, path, obj):
        u"""[summary]
        """

        tmp = json.dumps(obj)
        with open(path, mode='w') as fp:
            fp.write(tmp)

    def read_json(self, path):
        u"""
        """

        result = ''

        if not os.path.exists(path):
            return result

        with open(path, mode="r") as fp:
            tmp = fp.read()
            result = json.loads(tmp)

        return result
