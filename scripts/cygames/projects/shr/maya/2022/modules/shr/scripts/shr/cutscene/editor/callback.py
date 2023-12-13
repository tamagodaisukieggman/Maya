# -*- coding: utf-8 -*-
"""Callbackまとめ。Callbackは色々な所に入れるとバグの温床になりそうなので、まとめる"""
from __future__ import absolute_import as _absolute_import
from __future__ import division as _division
from __future__ import print_function as _print_function
from __future__ import unicode_literals as _unicode_literals

import abc

import six
from maya import cmds

from . import viewport

CUSTOM_VIEWPORT_CALLBACK = "CustomViewportCallback"
CUSTOM_VIEWPORT_CAMERA_ATTRIBUTE_CALLBACK = "CustomViewportCameraAttributeCallback"


@six.add_metaclass(abc.ABCMeta)
class BaseCallBackRegister(object):
    def __init__(self):
        pass

    @abc.abstractmethod
    def register(self):
        pass

    @abc.abstractmethod
    def unregister(self):
        pass


class ViewPortCallBackRegister(BaseCallBackRegister):

    camera_change_callback_id = None

    @classmethod
    def register(cls):
        cmds.condition(CUSTOM_VIEWPORT_CALLBACK, dependency="playingBack", script="python(\"import mtk; shr.cutscene.editor.callback.ViewPortCallBackRegister.set_focus()\")")

        cls.camera_change_callback_id = cmds.scriptJob(event=["modelEditorChanged", "import mtk; shr.cutscene.editor.callback.ViewPortCallBackRegister.save_viewport_camera()"])

        cmds.condition(CUSTOM_VIEWPORT_CAMERA_ATTRIBUTE_CALLBACK, dependency="cameraDisplayAttributesChange", script="python(\"import mtk;shr.cutscene.editor.CutsceneEditorRegister.viewport_controller.view_grid_drawermanager.refresh_grid_all()\")")

    @classmethod
    def unregister(cls):
        try:
            cmds.condition(CUSTOM_VIEWPORT_CALLBACK, delete=True)
        except Exception:
            pass

        if cls.camera_change_callback_id is None:
            return

        if cmds.scriptJob(exists=cls.camera_change_callback_id):
            cmds.scriptJob(kill=cls.camera_change_callback_id)

        try:
            cmds.condition(CUSTOM_VIEWPORT_CAMERA_ATTRIBUTE_CALLBACK, delete=True)
        except Exception:
            pass

    @classmethod
    def set_focus(cls, *args, **kwags):
        cmds.setFocus(viewport.CINEMATIC_VIEWPORT_VIEW)
        cmds.setFocus(cmds.getPanel(withLabel="Camera Sequencer"))

        if (viewport.edit_view_camera):
            cmds.modelEditor(viewport.EDIT_VIEWPORT_VIEW, edit=True, camera=viewport.edit_view_camera)

        if (viewport.camera_view_camera):
            cmds.modelEditor(viewport.CAMERA_VIEWPORT_VIEW, edit=True, camera=viewport.camera_view_camera)
        if (viewport.camera_view_camera):
            cmds.modelEditor(cmds.getPanel(withLabel="Persp View"), edit=True, camera=viewport.default_view_camera)

    @classmethod
    def save_viewport_camera(cls, *args, **kwargs):
        """ビューポートのカメラ状態をセーブする
        """
        viewport.edit_view_camera = cmds.modelEditor(viewport.EDIT_VIEWPORT_VIEW, query=True, camera=True)
        viewport.camera_view_camera = cmds.modelEditor(viewport.CAMERA_VIEWPORT_VIEW, query=True, camera=True)

        default_model_panel_camera = cmds.modelPanel(cmds.getPanel(withLabel="Persp View"), query=True, camera=True)
        viewport.default_view_camera = default_model_panel_camera
