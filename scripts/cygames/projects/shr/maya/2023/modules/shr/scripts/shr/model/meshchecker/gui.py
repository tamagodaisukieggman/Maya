# -*- coding: utf-8 -*-
u"""メッシュチェッカー

"""
from functools import wraps

import maya.cmds as cmds

import command
from mtku.maya.base.window import BaseWindow
from mtku.maya.constant import MTK_MAYA_MANUAL_HELP_URL
from mtku.maya.mtklog import MtkLog

TOOL_NAME = 'meshchecker'
UI_NAME = 'CyMeshChecker'
URL = '{}/modeling/meshchecker.html'.format(MTK_MAYA_MANUAL_HELP_URL)


logger = MtkLog(__name__)


def _frame_decorator(label, color):
    u"""FrameLayoutのdecorator

    :param label: ラベル
    :param color: 色 (R(0-1), G(0-1), B(0-1))
    :return: func
    """
    def __frame_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cmds.frameLayout(l=label, cll=True, bgc=color)
            result = func(*args, **kwargs)
            cmds.setParent('..')
            return result
        return wrapper
    return __frame_decorator


def _inner_frame_decorator(label):
    u"""FrameLayout(内側)のdecorator

    :param label: ラベル
    :return: func
    """
    def __inner_frame_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            form = cmds.formLayout()
            frame = cmds.frameLayout(l=label)
            result = func(*args, **kwargs)
            cmds.setParent('..')
            cmds.formLayout(
                form, e=True,
                af=(
                    [frame, 'left', 15],
                    [frame, 'right', 0],
                    [frame, 'bottom', 2],
                ),
            )
            cmds.setParent('..')
            return result
        return wrapper
    return __inner_frame_decorator


class MeshChecker(BaseWindow):

    def __init__(self, *args, **kwargs):
        super(MeshChecker, self).__init__(*args, **kwargs)

        self._ui = None
        # Edge
        self._float_slider_grp_edge_length = None
        # Face
        self._float_slider_grp_face_angle_min = None
        self._float_slider_grp_face_angle_max = None

    def create(self):
        u"""Windowのレイアウト作成"""
        # dirpath = os.path.dirname(__file__)
        # ui_file = '{0}/{1}.ui'.format(dirpath, TOOL_NAME)
        # self._ui = self.load_file(ui_file)

        self._edge_layout()
        self._face_layout()

    # ############################################################
    # Layout
    # ############################################################
    @_frame_decorator('Edge', (0, 0.5, 0.5))
    def _edge_layout(self):
        u"""Layout (Edge)"""
        # Edge Length
        self._edge_length_layout()

    @_frame_decorator('Face', (0, 0.5, 0.5))
    def _face_layout(self):
        u"""Layout (Face)"""
        # Polygon Angle
        self._face_slope_layout()

    @_inner_frame_decorator('Length')
    def _edge_length_layout(self):
        u"""Layout(Edge - Length)"""
        form = cmds.formLayout()

        self._float_slider_grp_edge_length = self._add_float_slider_grp('Length: ', 300, 0, 1000)
        button = cmds.button(l='CHECK', w=80, c=self._check_edge_length)

        cmds.formLayout(
            form, e=True,
            af=(
                [self._float_slider_grp_edge_length, 'left', 0],
                [self._float_slider_grp_edge_length, 'right', 0],
                [button, 'right', 5],
                [button, 'bottom', 5],
            ),
            ac=(
                [button, 'top', 10, self._float_slider_grp_edge_length],
            ),
        )

        cmds.setParent('..')

    @_inner_frame_decorator('Slope')
    def _face_slope_layout(self):
        u"""Layout (Face - Slope)"""
        form = cmds.formLayout()

        self._float_slider_grp_face_angle_min = self._add_float_slider_grp('Min: ', 0, -180, 180)
        self._float_slider_grp_face_angle_max = self._add_float_slider_grp('Max: ', 90, -180, 180)
        button = cmds.button(l='CHECK', w=80, c=self._check_face_slope)

        cmds.formLayout(
            form, e=True,
            af=(
                [self._float_slider_grp_face_angle_min, 'left', 0],
                [self._float_slider_grp_face_angle_min, 'right', 0],
                [self._float_slider_grp_face_angle_max, 'left', 0],
                [self._float_slider_grp_face_angle_max, 'right', 0],
                [button, 'right', 5],
                [button, 'bottom', 5],
            ),
            ac=(
                [self._float_slider_grp_face_angle_max, 'top', 0, self._float_slider_grp_face_angle_min],
                [button, 'top', 10, self._float_slider_grp_face_angle_max],
            ),
        )

        cmds.setParent('..')

    def _add_float_slider_grp(self, label, default_value=0, min_value=0, max_value=1000):
        u"""floatSliderGrpの追加

        :param label: ラベル
        :param default_value: default value
        :param min_value: min value
        :param max_value: max value
        :return: floatSliderGrp
        """
        float_slider_grp = cmds.floatSliderGrp(
            l=label, f=True,
            v=default_value, min=min_value, max=max_value, pre=3,
            cw3=[60, 100, 100],
        )
        return float_slider_grp

    # ############################################################
    # Button Command
    # ############################################################
    def _check_edge_length(self, *args):
        u"""Edgeの長さのチェック"""
        min_length = cmds.floatSliderGrp(self._float_slider_grp_edge_length, q=True, v=True)

        selections = cmds.ls(sl=True)
        edges = cmds.ls(cmds.polyListComponentConversion(selections, te=True), fl=True)
        if not edges:
            logger.warning(u'メッシュコンポーネントを選択してください')
            return

        error_edges = []
        for edge in edges:
            length = command.get_edge_length(edge)
            if length < min_length:
                error_edges.append(edge)
                logger.info('ng -- {} = {}'.format(edge, length))
            else:
                logger.info('ok -- {} = {}'.format(edge, length))

        if error_edges:
            cmds.select(error_edges)
        else:
            cmds.select(cl=True)
        return error_edges

    def _check_face_slope(self, *args):
        min_angle = cmds.floatSliderGrp(self._float_slider_grp_face_angle_min, q=True, v=True)
        max_angle = cmds.floatSliderGrp(self._float_slider_grp_face_angle_max, q=True, v=True)

        selections = cmds.ls(sl=True)
        faces = cmds.ls(cmds.polyListComponentConversion(selections, tf=True), fl=True)
        if not faces:
            logger.warning(u'メッシュコンポーネントを選択してください')
            return

        error_faces = []
        for face in faces:
            angle = command.get_face_angle(face, 'y')
            logger.debug('{}, {}, {}'.format(type(min_angle), type(angle), type(max_angle)))
            logger.debug('{}, {}, {}'.format(min_angle, angle, max_angle))
            if min_angle <= angle <= max_angle:
                error_faces.append(face)
                logger.info('{} = {}'.format(face, angle))
            else:
                logger.info('{} = {}'.format(face, angle))

        if error_faces:
            cmds.select(error_faces)
        else:
            cmds.select(cl=True)
        return error_faces

    def help(self, *args):
        u"""help表示"""
        cmds.showHelp(URL, a=True)
