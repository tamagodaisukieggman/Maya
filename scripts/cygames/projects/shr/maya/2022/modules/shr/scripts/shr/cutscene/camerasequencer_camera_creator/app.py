# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from enum import Enum
import abc

from maya import cmds
from maya import mel
import six


from shr.cutscene import utility
from . import view
from . import settings
from . import sequencer


class CameraType(Enum):
    normal = 0
    aim = 1
    aim_and_up = 2


@six.add_metaclass(abc.ABCMeta)
class CameraSequencerObject(object):
    """カメラシーケンサー用のオブジェクト基底クラス

    名前や表示/非表示、トラック情報を保有する
    """

    def __init__(self, name, visibility=True):
        self.__name = name
        self.__visibility = visibility
        self.__transform = {"position": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]}

    def get_name(self):
        return self.__name

    def set_name(self, value):
        unique_name = utility.create_unique_object_name(value, "camera")

        cmds.rename(self.__name, unique_name)

        self.__name = unique_name

    def get_visibility(self):
        return self.__visibility

    def set_visibility(self, value):
        cmds.setAttr(self.__name + ".visibility", value)

        self.__visibility = value

    def get_transform(self):
        return self.__transform

    def set_transform(self, value):
        cmds.setAttr(self.__name + ".tx", value["position"][0])
        cmds.setAttr(self.__name + ".ty", value["position"][1])
        cmds.setAttr(self.__name + ".tz", value["position"][2])

        cmds.setAttr(self.__name + ".rx", value["rotation"][0])
        cmds.setAttr(self.__name + ".ry", value["rotation"][1])
        cmds.setAttr(self.__name + ".rz", value["rotation"][2])

        self.__transform = value

    @classmethod
    @abc.abstractmethod
    def create(cls):
        pass


class CutsceneCamera(CameraSequencerObject):
    """カットシーン用のカメラクラス
    """

    def __init__(self, name, visibility=True):
        super(CutsceneCamera, self).__init__(name, visibility=visibility)

    @classmethod
    def create(cls):
        create_camera = cmds.camera()
        return CutsceneCamera(create_camera[0], visibility=True)

    def set_parent(self, target_node):
        cmds.parent(self.get_name(), target_node)

    def set_attribute(self, attribute_settings):
        name = self.get_name()
        for attribute_name, value in attribute_settings.items():
            cmds.setAttr("{}.{}".format(name, attribute_name), value)

    def focus(self, model_panel):
        cmds.modelPanel(model_panel, edit=True, camera=self.get_name())

    def change_camera_type(self, parent_node, camera_type=CameraType.normal):
        mel.eval('cameraMakeNode {} "{}"'.format(camera_type.value, self.get_name()))
        if camera_type == CameraType.aim or camera_type == CameraType.aim_and_up:
            camera_name = self.get_name()
            search_parent_group_node = cmds.ls(camera_name + "_group", type="lookAt")
            if not search_parent_group_node:
                raise ValueError("internal error.")

            cmds.parent(search_parent_group_node[0], parent_node)


class CutSceneCameraCreator(object):
    CONST_CAMERA_FILM_APERTURE = {"horizontalFilmAperture": 1.4173228346456694,  # 36mm
                                  "verticalFilmAperture": 0.9448818897637796}    # 24mm

    def __init__(self, settings_dict):
        self.settings = settings_dict

        # CustomEditor作成まで、CameraSequencerを指定
        self.__sequencer = sequencer.CameraSequencerController

    def duplicate(self):
        try:
            from shr.cutscene import editor
        except Exception:
            cmds.warning("Not Editor Mode.")
        else:
            target_model_panel = editor.CutsceneEditorRegister.viewport_controller.get_cinematic_view_panel()

            prev_focus_panel_name = editor.viewport.ModelEditorFocusHolder.get_prev_focus()
        finally:
            if prev_focus_panel_name is not None:
                target_camera = utility.panel.get_camera_from_model_panel(prev_focus_panel_name)
            else:
                persp_view = cmds.getPanel(withLabel="Persp View")
                target_camera = cmds.modelPanel(persp_view, query=True, camera=True)

        source_model_transform = self.__get_transform(target_camera)

        create_camera = self.create(source_model_transform, target_model_panel)

        return create_camera

    def create(self, transform, model_panel=None):
        # CameraSequencerの仕様上、shotに適用するとコントロール奪われるので、フォーカス先をカメラが切り替わってもよい物に変更が必要
        if model_panel is not None:
            cmds.setFocus(model_panel)

        group_name = self.settings["cameraGroup"]
        if not cmds.objExists(group_name):
            group_name = self.__create_group(group_name)

        create_camera = CutsceneCamera.create()
        create_camera.set_transform(transform)
        create_camera.set_attribute(self.CONST_CAMERA_FILM_APERTURE)
        create_camera.set_parent(group_name)

        self.__set_create_after_default_settings(create_camera.get_name())

        create_shot_name = self.__sequencer.set_shot(create_camera, self.settings)

        # シーケンサーを作った後に名前が決まるので、後実行
        create_camera.set_name(create_shot_name + "_cam")

        target_camera_type = CameraType(self.settings["cameraType"])
        create_camera.change_camera_type(group_name, camera_type=target_camera_type)

        self.__set_keyframe(create_camera.get_name(), create_shot_name)

        return create_camera

    def __get_transform(self, object_name):
        transform_data = {
            "position": [cmds.getAttr(object_name + ".tx"), cmds.getAttr(object_name + ".ty"), cmds.getAttr(object_name + ".tz")],
            "rotation": [cmds.getAttr(object_name + ".rx"), cmds.getAttr(object_name + ".ry"), cmds.getAttr(object_name + ".rz")],
            "scale": [cmds.getAttr(object_name + ".sx"), cmds.getAttr(object_name + ".sy"), cmds.getAttr(object_name + ".sz")],
        }
        return transform_data

    def __create_group(self, name):
        return cmds.group(name=name, world=True, empty=True)

    def __set_keyframe(self, camera_name, shot_name):
        """キーをフレームを設定する

        shotが存在する場合は、そのshotのstartTimeに
        存在しない場合は、currentTimeへ

        :param camera_name: キーを入力するカメラ名
        :type camera_name: str
        :param shot_name: shot名
        :type shot_name: str
        """

        if not shot_name:
            # shotが存在しない時はcurrentTimeにキーを入れる
            target_frame = cmds.currentTime(query=True)
        else:
            target_frame = cmds.shot(shot_name, query=True, startTime=True)

        cmds.setKeyframe(camera_name, time=target_frame, breakdown=False, controlPoints=False, shape=False)

    def __set_create_after_default_settings(self, camera_name):
        """作成後に設定を上書きする

        ・オーバースキャンを1.0に
        ・このままだとOn/Offする事で1.3に戻るので、lock
        ・FilmGate自体をOnに
        ・Gatemaskを黒に

        :param camera_name: 設定を上書きしたいカメラ名
        :type camera_name: str
        """
        camera_shape_name = self.__get_shapes_from_transform(camera_name)

        cmds.setAttr("{}.overscan".format(camera_shape_name), 1.0)
        cmds.setAttr("{}.overscan".format(camera_shape_name), lock=True)
        cmds.setAttr("{}.displayResolution".format(camera_shape_name), True)
        cmds.setAttr("{}.displayGateMaskColor".format(camera_shape_name), 0.0, 0.0, 0.0, type="double3")

    def __get_shapes_from_transform(self, camera_name):
        return cmds.listRelatives(camera_name, shapes=True)[0]
