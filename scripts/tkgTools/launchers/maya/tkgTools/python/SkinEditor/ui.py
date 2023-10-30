# coding: utf-8

from __future__ import absolute_import

import datetime
import functools
import os
import re
import traceback
from collections import OrderedDict

import maya.cmds as cmds
import maya.mel as mel

from . import lib


Tool_Name_Prefix = 'SkinEditor'
Tool_Title_Prefix = 'Skin Editor'


def save_optionvar(key, value, force=True):
    """optionVarに保存

    :param str key: キー名
    :param mixin value: 値
    :param bool force: 強制的に上書きするかのブール値

    :return: 保存できたかどうかのブール値
    :rtype: bool
    """

    vStr = str(value)
    if force:
        cmds.optionVar(sv=[key, vStr])
        return True
    else:
        if not cmds.optionVar(ex=key):
            cmds.optionVar(sv=[key, vStr])
            return True
        else:
            return False


def load_optionvar(key):
    """optionVarを取得

    :param str key: キー名
    :return: 保存された値, キーが見つからない場合は None
    :rtype: value or None
    """

    if cmds.optionVar(ex=key):
        return eval(cmds.optionVar(q=key))
    else:
        return None


def remove_optionvar(key):
    """optionVarを削除

    :param str key: キー名
    :return: 削除成功したかのブール値
    :rtype: bool
    """

    if cmds.optionVar(ex=key):
        cmds.optionVar(rm=key)
        return True
    else:
        return False


def get_icon(icon_name):
    u"""パッケージ内のアイコンのパスを取得
    """

    icon_path = os.path.join(os.path.dirname(__file__), 'icons', icon_name).replace(os.sep, '/')
    return icon_path if os.path.isfile(icon_path) else ''


def refresh_componentEditors():
    u"""コンポーネントエディターの表示を更新
    componentEditorを全て更新します。
    """

    editors = cmds.lsUI(editors=1)
    for editor in editors:
        try:
            if cmds.componentEditor(editor, ex=True):
                li = cmds.componentEditor(editor, q=True, li=1)
                cmds.componentEditor(editor, e=True, li=not li)
                cmds.componentEditor(editor, e=True, li=li)
        except:
            pass


def refresh_skinInfluenceList():
    """ArtPaintSkinWeightsToolのinfluenceListの更新
    """

    try:
        if '$gArtSkinInfluencesList' in mel.eval('env'):
            mel.eval('''
if((`treeView -q -exists $gArtSkinInfluencesList`) && (currentCtx() == "artAttrSkinContext")){
    artAttrSkinJointMenuRebuild( "artAttrSkinPaintCtx" );
}''')
    except:
        pass


class CopyWeightsUI(object):
    u"""
    """

    WINDOW_NAME = '{}_copyWeights'.format(Tool_Name_Prefix)
    WINDOW_TITLE = '{} Copy Weights'.format(Tool_Title_Prefix)

    def __init__(self, *args, **kwargs):
        self._win = None
        self._width = 450
        self._height = 250

        self._methodLabels = [
            'Index',
            'Nearest Component',
            'Closest Point',
        ]
        self._methods = [
            'index',
            'nearestcomponent',
            'closestpoint',
        ]

        self._src_nonselect_msg = 'Please select source skinned object.'
        self._dst_nonselect_msg = 'Please select destination skinned object.'

    def save_settings(self, *args, **kwargs):
        options = self.get_options()
        save_optionvar('{}__ui_options'.format(self.WINDOW_NAME), options)

    def load_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        loadValue = load_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        if loadValue:
            try:
                if 'method' in loadValue:
                    methodSelectIndex = self._methods.index(loadValue['method']) + 1
                    cmds.optionMenuGrp(self.method, e=True, sl=methodSelectIndex)

                if 'keepLock' in loadValue:
                    cmds.checkBoxGrp(self.keepLock, e=True, v1=loadValue['keepLock'])

                if 'useBlend' in loadValue:
                    cmds.checkBoxGrp(self.useBlend, e=True, v1=loadValue['useBlend'])

                if 'blend' in loadValue:
                    cmds.floatFieldGrp(self.blend, e=True, v1=loadValue['blend'])

            except Exception as e:
                cmds.error(e)
                self.reset_settings()

        if update_ui:
            self.update_ui()

    def reset_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        cmds.optionMenuGrp(self.method, e=True, sl=1)
        cmds.checkBoxGrp(self.keepLock, e=True, v1=False)
        cmds.checkBoxGrp(self.useBlend, e=True, v1=False)
        cmds.floatFieldGrp(self.blend, e=True, v1=0.5)

        if update_ui:
            self.update_ui()

    def remove_settings(self, *args, **kwargs):
        remove_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        self.reset_settings()

    def get_options(self, *args, **kwargs):
        return {
            'method': self._methods[cmds.optionMenuGrp(self.method, q=True, sl=True) - 1],
            'keepLock': cmds.checkBoxGrp(self.keepLock, q=True, v1=True),
            'useBlend': cmds.checkBoxGrp(self.useBlend, q=True, v1=True),
            'blend': cmds.floatFieldGrp(self.blend, q=True, v1=True)
        }

    def close(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

    def show(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

        self._win = cmds.window(self.WINDOW_NAME, title=self.WINDOW_TITLE, mb=True, w=self._width, h=self._height)

        cw1 = 120
        cw2 = 100
        cw3 = 50
        h = 24
        margin = 2

        # Menu
        editMenu = cmds.menu(l='Edit', p=self._win)
        cmds.menuItem(l='Save Settings', p=editMenu, c=self.save_settings)
        cmds.menuItem(l='Reset Settings', p=editMenu, c=self.reset_settings)
        cmds.menuItem(l='Remove Settings', p=editMenu, c=self.remove_settings)

        mainLay = cmds.formLayout(p=self._win, nd=100)

        # Labels
        labelsLay = cmds.columnLayout(adj=True, p=mainLay, rs=2)
        srcLay = cmds.rowLayout(nc=2, cw2=(cw1, cw2), cl2=['center', 'left'], ct2=['right', 'left'], p=labelsLay, h=h)
        cmds.text(l='Source :', p=srcLay)
        self.src = cmds.text(l=self._src_nonselect_msg, p=srcLay, fn='boldLabelFont')

        cmds.separator(style='in', p=labelsLay)

        dstLay = cmds.rowLayout(nc=2, cw2=(cw1, cw2), cl2=['center', 'left'], ct2=['right', 'left'], p=labelsLay, h=h)
        cmds.text(l='Destination :', p=dstLay)
        self.dst = cmds.text(l=self._dst_nonselect_msg, p=dstLay, fn='boldLabelFont')

        # Options
        optionLay = cmds.frameLayout(l='Options', lv=True, mw=2, mh=2, cll=False, p=mainLay)
        optionColumn = cmds.columnLayout(adj=True, p=optionLay, rs=2)

        self.method = cmds.optionMenuGrp(label='Copy Method : ', cw2=[cw1, cw2], p=optionColumn, h=h)
        for label in self._methodLabels:
            cmds.menuItem(label=label)

        self.useBlend = cmds.checkBoxGrp(label='Weight Blend : ', cw2=[cw1, cw2], v1=False, h=h, p=optionColumn, cc1=self.update_ui)
        self.blend = cmds.floatFieldGrp(label='blend : ', cw2=[cw1, cw3], v1=0.5, pre=2, h=h, p=optionColumn)
        self.keepLock = cmds.checkBoxGrp(label='Keep Lock : ', cw2=[cw1, cw2], v1=False, h=h, p=optionColumn)

        buttonLay = cmds.formLayout(p=mainLay)
        self.applyAndCloseBtn = cmds.button(l='Apply and Close', c=self.apply_and_close, p=buttonLay)
        self.applyBtn = cmds.button(l='Apply', c=self.apply, p=buttonLay)
        closeBtn = cmds.button(l='Close', c=self.close, bgc=[0.3, 0.3, 0.3], p=buttonLay)

        cmds.formLayout(buttonLay, e=True,
                        af=[[self.applyAndCloseBtn, 'left', margin],
                            [self.applyAndCloseBtn, 'top', margin],
                            [self.applyAndCloseBtn, 'bottom', margin],
                            [self.applyBtn, 'top', margin],
                            [self.applyBtn, 'bottom', margin],
                            [closeBtn, 'right', margin],
                            [closeBtn, 'top', margin],
                            [closeBtn, 'bottom', margin],
                            ],
                        ac=[[self.applyBtn, 'left', margin, self.applyAndCloseBtn],
                            [self.applyBtn, 'right', margin, closeBtn],
                            ],
                        ap=[[self.applyAndCloseBtn, 'right', margin, 35],
                            [closeBtn, 'left', margin, 75],
                            ],
                        )
        cmds.formLayout(mainLay, e=True,
                        af=[[labelsLay, 'top', margin],
                            [labelsLay, 'left', margin],
                            [labelsLay, 'right', margin],
                            [optionLay, 'left', margin],
                            [optionLay, 'right', margin],
                            [buttonLay, 'left', margin],
                            [buttonLay, 'right', margin],
                            [buttonLay, 'bottom', margin],
                            ],
                        ac=[[optionLay, 'top', margin, labelsLay],
                            [optionLay, 'bottom', margin, buttonLay],
                            ],
                        an=[[labelsLay, 'bottom'],
                            [buttonLay, 'top'],
                            ]
                        )

        cmds.showWindow(self._win)
        cmds.scriptJob(e=['SelectionChanged', self.selection_changed], p=self._win, rp=True)

        self.reset_settings(update_ui=False)
        self.load_settings()

    def update_ui(self, *args, **kwargs):
        options = self.get_options()

        cmds.floatFieldGrp(self.blend, e=True, en=options.get('useBlend', False))
        self.selection_changed()

    def apply(self, *args, **kwargs):
        options = self.get_options()

        opt = {
            'showProgress': True,
            'method': options['method'],
            'blend': options['blend'] if options.get('useBlend', False) else 1.0,
            'keepLock': options['keepLock'],
        }

        lib.transfer_weights(**opt)

        refresh_componentEditors()

        self.save_settings()

    def apply_and_close(self, *args, **kwargs):
        self.apply()
        self.close()

    def selection_changed(self, *args, **kwargs):
        cmds.text(self.src, e=True, l=self._src_nonselect_msg)
        cmds.text(self.dst, e=True, l=self._dst_nonselect_msg)

        cmds.button(self.applyBtn, e=True, en=False)
        cmds.button(self.applyAndCloseBtn, e=True, en=False)

        sels = cmds.ls(os=True, fl=True)
        selObjects = lib.get_objects(sels)
        if not selObjects:
            return

        histories = cmds.listHistory(selObjects, interestLevel=1) or []
        geos = cmds.ls(histories, type='controlPoint', ni=1)
        geos = sorted(set(geos), key=geos.index)
        nGeos = len(geos)
        if nGeos == 0:
            return

        src = geos[0]
        src_clst = lib.list_related_skinClusters(src)
        src = cmds.listRelatives(src, p=True, pa=True)[0]
        cmds.text(self.src, e=True, l=src)

        if nGeos < 2:
            return

        dst = geos[1]
        dst_clst = lib.list_related_skinClusters(dst)
        dst = cmds.listRelatives(dst, p=True, pa=True)[0]
        cmds.text(self.dst, e=True, l=dst)

        src_infls = lib.list_skinCluster_influences(src_clst)
        dst_infls = lib.list_skinCluster_influences(dst_clst)
        diff = list(set(src_infls).difference(dst_infls))
        if diff:
            cmds.text(self.dst, e=True, l='Found {} uncontained influences.'.format(len(diff)))
            print('Uncontained influences : {}'.format(diff))
            return

        if not all([src, dst, src_clst, dst_clst]):
            return

        cmds.button(self.applyBtn, e=True, en=True)
        cmds.button(self.applyAndCloseBtn, e=True, en=True)


class SmoothWeightsUI(object):
    u"""
    """

    WINDOW_NAME = '{}_smoothWeights'.format(Tool_Name_Prefix)
    WINDOW_TITLE = '{} Smooth Weights'.format(Tool_Title_Prefix)

    def __init__(self, *args, **kwargs):
        self._win = None
        self._width = 250
        self._height = 170

    def save_settings(self, *args, **kwargs):
        options = self.get_options()
        save_optionvar('{}__ui_options'.format(self.WINDOW_NAME), options)

    def load_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        loadValue = load_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        if loadValue:
            try:
                if 'keepLock' in loadValue:
                    cmds.checkBoxGrp(self.keepLock, e=True, v1=loadValue['keepLock'])

                if 'blend' in loadValue:
                    cmds.floatFieldGrp(self.blend, e=True, v1=loadValue['blend'])

                if 'useMeshUV' in loadValue:
                    cmds.checkBoxGrp(self.useMeshUV, e=True, v1=loadValue['useMeshUV'])

                if 'meshUV' in loadValue:
                    cmds.checkBoxGrp(self.meshUV, e=True, v1=loadValue['meshUV'][0], v2=loadValue['meshUV'][1])

            except Exception as e:
                cmds.error(e)
                self.reset_settings()

        if update_ui:
            self.update_ui()

    def reset_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        cmds.floatFieldGrp(self.blend, e=True, v1=0.5)
        cmds.checkBoxGrp(self.keepLock, e=True, v1=False)
        cmds.checkBoxGrp(self.useMeshUV, e=True, v1=False)
        cmds.checkBoxGrp(self.meshUV, e=True, v1=True, v2=True)

        if update_ui:
            self.update_ui()

    def remove_settings(self, *args, **kwargs):
        remove_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        self.reset_settings()

    def get_options(self, *args, **kwargs):
        return {
            'keepLock': cmds.checkBoxGrp(self.keepLock, q=True, v1=True),
            'blend': cmds.floatFieldGrp(self.blend, q=True, v1=True),
            'useMeshUV': cmds.checkBoxGrp(self.useMeshUV, q=True, v1=True),
            'meshUV': [cmds.checkBoxGrp(self.meshUV, q=True, v1=True), cmds.checkBoxGrp(self.meshUV, q=True, v2=True)]
        }

    def close(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

    def show(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

        self._win = cmds.window(self.WINDOW_NAME, title=self.WINDOW_TITLE, mb=True, w=self._width, h=self._height)

        cw1 = 100
        cw2 = 100
        cw3 = 50
        h = 24
        margin = 2

        # Menu
        editMenu = cmds.menu(l='Edit', p=self._win)
        cmds.menuItem(l='Save Settings', p=editMenu, c=self.save_settings)
        cmds.menuItem(l='Reset Settings', p=editMenu, c=self.reset_settings)
        cmds.menuItem(l='Remove Settings', p=editMenu, c=self.remove_settings)

        mainLay = cmds.formLayout(p=self._win, nd=100)

        # Options
        optionLay = cmds.frameLayout(l='Options', lv=False, mw=2, mh=2, cll=False, p=mainLay)
        optionColumn = cmds.columnLayout(adj=True, p=optionLay, rs=2)

        self.blend = cmds.floatFieldGrp(label='Blend : ', cw2=[cw1, cw3], v1=0.5, pre=2, h=h, p=optionColumn)
        self.keepLock = cmds.checkBoxGrp(label='Keep Lock : ', cw2=[cw1, cw2], v1=False, h=h, p=optionColumn)
        self.useMeshUV = cmds.checkBoxGrp(label='Use Mesh UV : ', cw2=[cw1, cw3], v1=False, h=h, p=optionColumn, cc=self.update_ui)
        self.meshUV = cmds.checkBoxGrp(label='   ', ncb=2, cw3=[cw1, cw3, cw3], h=h, p=optionColumn, v1=False, l1='U', v2=False, l2='V')

        self.applyBtn = cmds.iconTextButton(l='Apply', c=self.apply, p=mainLay, rpt=True, style='textOnly', fn='boldLabelFont', bgc=[0.4, 0.4, 0.4])

        cmds.formLayout(mainLay, e=True,
                        af=[[optionLay, 'top', margin],
                            [optionLay, 'left', margin],
                            [optionLay, 'right', margin],
                            [self.applyBtn, 'left', margin],
                            [self.applyBtn, 'right', margin],
                            [self.applyBtn, 'bottom', margin],
                            ],
                        ac=[[optionLay, 'bottom', margin * 2, self.applyBtn],
                            ],
                        an=[[self.applyBtn, 'top'],
                            ]
                        )

        cmds.showWindow(self._win)
        cmds.scriptJob(e=['SelectionChanged', self.selection_changed], p=self._win, rp=True)

        self.reset_settings(update_ui=False)
        self.load_settings()

    def update_ui(self, *args, **kwargs):
        options = self.get_options()

        cmds.checkBoxGrp(self.meshUV, e=True, en=options['useMeshUV'])

        self.selection_changed()

    def apply(self, *args, **kwargs):
        options = self.get_options()

        opt = {
            'showProgress': False,
            'blend': options['blend'],
            'keepLock': options['keepLock'],
            'neighbourMethod': 'connected_vertices',
            'useMeshUV': options['useMeshUV'],
            'meshU': options['meshUV'][0],
            'meshV': options['meshUV'][1],
            'thresholdAngle': 30,
        }

        lib.smooth_weights(**opt)
        refresh_componentEditors()

        self.save_settings()

    def selection_changed(self, *args, **kwargs):
        cmds.iconTextButton(self.applyBtn, e=True, en=False)

        sels = cmds.ls(os=True, fl=True)
        selObjects = lib.get_objects(sels)
        if not selObjects:
            return

        histories = cmds.listHistory(selObjects, interestLevel=1) or []
        geos = cmds.ls(histories, type='controlPoint', ni=1)
        geos = sorted(set(geos), key=geos.index)
        if len(geos) < 1:
            return

        src = geos[0]
        src_clst = lib.list_related_skinClusters(src)
        if not (src and src_clst):
            return

        cmds.iconTextButton(self.applyBtn, e=True, en=True)


class SwapMoveWeightsUI(object):
    u"""Swap or Move Weights
    """

    WINDOW_NAME = '{}_swapMoveWeights'.format(Tool_Name_Prefix)
    WINDOW_TITLE = '{} Swap Move Weights'.format(Tool_Title_Prefix)

    def __init__(self, mode, *args, **kwargs):
        self._win = None
        self._window_name = '{}_{}Weights'.format(Tool_Name_Prefix, 'swap' if mode == 'swap' else 'move')
        self._window_title = '{} {} Weights'.format(Tool_Title_Prefix, 'Swap' if mode == 'swap' else 'Move')

        self._width = 300
        self._height = 80

        self._mode = mode

    def save_settings(self, *args, **kwargs):
        options = self.get_options()
        save_optionvar('{}__ui_options'.format(self._window_name), options)

    def load_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        loadValue = load_optionvar('{}__ui_options'.format(self._window_name))
        if loadValue:
            try:
                if 'move_weight' in loadValue:
                    cmds.floatFieldGrp(self.move_weight, e=True, v1=loadValue['move_weight'])

            except Exception as e:
                cmds.error(e)
                self.reset_settings()

        if update_ui:
            self.update_ui()

    def reset_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        cmds.floatFieldGrp(self.move_weight, e=True, v1=1.0)

        if update_ui:
            self.update_ui()

    def remove_settings(self, *args, **kwargs):
        remove_optionvar('{}__ui_options'.format(self._window_name))
        self.reset_settings()

    def get_options(self, *args, **kwargs):
        return {
            'move_weight': cmds.floatFieldGrp(self.move_weight, q=True, v1=True),
        }

    def close(self, *args, **kwargs):
        if cmds.window(self._window_name, q=True, ex=True):
            cmds.deleteUI(self._window_name)

    def show(self, *args, **kwargs):
        if cmds.window(self._window_name, q=True, ex=True):
            cmds.deleteUI(self._window_name)

        self._win = cmds.window(self._window_name, title=self._window_title, mb=True, w=self._width, h=self._height)

        cw1 = 100
        h = 24
        margin = 2

        # Menu
        editMenu = cmds.menu(l='Edit', p=self._win)
        cmds.menuItem(l='Save Settings', p=editMenu, c=self.save_settings)
        cmds.menuItem(l='Reset Settings', p=editMenu, c=self.reset_settings)
        cmds.menuItem(l='Remove Settings', p=editMenu, c=self.remove_settings)

        mainLay = cmds.formLayout(p=self._win, nd=100)

        # Options
        optionLay = cmds.frameLayout(l='Options', lv=False, mw=2, mh=2, cll=False, p=mainLay)
        optionColumn = cmds.columnLayout(adj=True, p=optionLay, rs=2)

        targetLay = cmds.formLayout(nd=100, p=optionColumn)
        self.src_infl = cmds.text(label='----------', p=targetLay, h=h, fn='fixedWidthFont', bgc=[0.8, 0.8, 0.8], al='center')
        self.src_infl_menu = cmds.popupMenu(b=1, pmc=functools.partial(self.populate_infl_menu, 'src'))

        self.infixText = cmds.iconTextButton(l=' >>> ' if self._mode == 'move' else ' <-> ',
                                             p=targetLay, style='textOnly', fn='boldLabelFont', al='center')
        if self._mode == 'move':
            cmds.iconTextButton(self.infixText, e=True, dtg='left_to_right', c=self.change_direction)

        self.dst_infl = cmds.text(label='----------', p=targetLay, h=h, fn='fixedWidthFont', bgc=[0.8, 0.8, 0.8], al='center')
        self.dst_infl_menu = cmds.popupMenu(b=1, pmc=functools.partial(self.populate_infl_menu, 'dst'))

        cmds.formLayout(targetLay, e=True,
                        af=[[self.src_infl, 'left', margin],
                            [self.src_infl, 'top', margin],
                            [self.src_infl, 'bottom', margin],
                            [self.infixText, 'top', margin],
                            [self.infixText, 'bottom', margin],
                            [self.dst_infl, 'right', margin],
                            [self.dst_infl, 'top', margin],
                            [self.dst_infl, 'bottom', margin],
                            ],
                        ap=[[self.src_infl, 'right', margin, 45],
                            [self.dst_infl, 'left', margin, 55],
                            ],
                        ac=[[self.infixText, 'left', 0, self.src_infl],
                            [self.infixText, 'right', 0, self.dst_infl],
                            ],
                        )
        self.move_weight = cmds.floatFieldGrp(label='move_weight : ', cw2=[cw1, 50], v1=0.5, pre=2, h=h, p=optionColumn)

        self.swapBtn = cmds.iconTextButton(l='Swap Influence Weights', c=self.on_swap, p=mainLay, rpt=True, style='textOnly', fn='boldLabelFont', bgc=[0.4, 0.4, 0.4])
        self.moveBtn = cmds.iconTextButton(l='Move Influence Weights', c=self.on_move, p=mainLay, rpt=True, style='textOnly', fn='boldLabelFont', bgc=[0.4, 0.4, 0.4])
        cmds.iconTextButton(self.swapBtn if self._mode != 'swap' else self.moveBtn, e=True, vis=False)

        cmds.formLayout(mainLay, e=True,
                        af=[[optionLay, 'top', margin],
                            [optionLay, 'left', margin],
                            [optionLay, 'right', margin],
                            [self.swapBtn, 'left', margin],
                            [self.swapBtn, 'bottom', margin],
                            [self.swapBtn, 'right', margin],
                            [self.moveBtn, 'left', margin],
                            [self.moveBtn, 'bottom', margin],
                            [self.moveBtn, 'right', margin],
                            ],
                        ac=[[optionLay, 'bottom', margin * 2, self.swapBtn],
                            ],
                        an=[[self.swapBtn, 'top'],
                            [self.moveBtn, 'top'],
                            ]
                        )

        cmds.showWindow(self._win)
        cmds.scriptJob(e=['SelectionChanged', self.selection_changed], p=self._win, rp=True)

        self.reset_settings(update_ui=False)
        self.load_settings()

    def update_ui(self, *args, **kwargs):
        self.get_options()

        self.selection_changed()

    def on_swap(self, *args, **kwargs):
        self.get_options()
        clst = self._get_clst()
        if not clst:
            return

        src = cmds.text(self.src_infl, q=True, l=True)
        if not cmds.objExists(src):
            return
        dst = cmds.text(self.dst_infl, q=True, l=True)
        if not cmds.objExists(dst):
            return

        opt = {
            'mode': 'swap',
            'src': src,
            'dst': dst,
            'components': cmds.ls(sl=True, fl=True),
        }

        lib.swap_or_move_weights([clst], **opt)

        refresh_componentEditors()

        self.save_settings()

    def on_move(self, *args, **kwargs):
        options = self.get_options()
        clst = self._get_clst()
        if not clst:
            return

        src = cmds.text(self.src_infl, q=True, l=True)
        if not cmds.objExists(src):
            return
        dst = cmds.text(self.dst_infl, q=True, l=True)
        if not cmds.objExists(dst):
            return

        dir_ = cmds.iconTextButton(self.infixText, q=True, dtg=True)
        if dir_ == 'right_to_left':
            src, dst = dst, src

        opt = {
            'mode': 'move',
            'src': src,
            'dst': dst,
            'components': cmds.ls(sl=True, fl=True),
            'weight': options.get('move_weight', 1.0)
        }

        lib.swap_or_move_weights([clst], **opt)

        refresh_componentEditors()

        self.save_settings()

    def change_direction(self, *args, **kwargs):
        dir_ = cmds.iconTextButton(self.infixText, q=True, dtg=True)
        if dir_ == 'left_to_right':
            cmds.iconTextButton(self.infixText, e=True, l=' <<< ', dtg='right_to_left')
        else:
            cmds.iconTextButton(self.infixText, e=True, l=' >>> ', dtg='left_to_right')

    @staticmethod
    def _get_clst():
        sels = cmds.ls(os=True, fl=True)
        selObjects = lib.get_objects(sels)
        if not selObjects:
            return

        histories = cmds.listHistory(selObjects, interestLevel=1) or []
        geos = cmds.ls(histories, type='controlPoint', ni=1)
        geos = sorted(set(geos), key=geos.index)
        if len(geos) < 1:
            return

        clst = lib.list_related_skinClusters(geos[0])
        return clst[0]

    def selection_changed(self, *args, **kwargs):
        cmds.iconTextButton(self.swapBtn, e=True, en=False)
        cmds.iconTextButton(self.moveBtn, e=True, en=False)

        clst = self._get_clst()
        if not clst:
            return

        cmds.iconTextButton(self.swapBtn, e=True, en=self._mode == 'swap')
        cmds.iconTextButton(self.moveBtn, e=True, en=self._mode == 'move')
        cmds.floatFieldGrp(self.move_weight, e=True, vis=self._mode == 'move')

        influenceIndexList, influenceList = lib.list_influences(clst, longName=False)
        src = cmds.text(self.src_infl, q=True, l=True)
        if src not in influenceList:
            cmds.text(self.src_infl, e=True, l='----------')

        dst = cmds.text(self.dst_infl, q=True, l=True)
        if dst not in influenceList:
            cmds.text(self.dst_infl, e=True, l='----------')

    def populate_infl_menu(self, side, *args, **kwargs):
        popup = self.src_infl_menu if side == 'src' else self.dst_infl_menu
        cmds.popupMenu(popup, e=True, dai=True)

        clst = self._get_clst()
        if not clst:
            return

        influenceIndexList, influenceList = lib.list_influences(clst, longName=False)

        for infl in influenceList:
            cmds.menuItem(p=popup, l=infl,
                          c=functools.partial(self.update_target_infl, side, infl))

    def update_target_infl(self, side, infl, *args, **kwargs):
        cmds.text(self.src_infl if side == 'src' else self.dst_infl, e=True, l=infl)


class WeightClipboardUI(object):
    u"""
    """

    WINDOW_NAME = '{}_weightClipboard'.format(Tool_Name_Prefix)
    WINDOW_TITLE = '{} Weight Clipboard'.format(Tool_Title_Prefix)

    def __init__(self, *args, **kwargs):
        self._win = None
        self._width = 260
        self._height = 190

    def save_settings(self, *args, **kwargs):
        options = self.get_options()
        save_optionvar('{}__ui_options'.format(self.WINDOW_NAME), options)

    def load_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        loadValue = load_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        if loadValue:
            try:
                if 'blend' in loadValue:
                    cmds.floatField(self.blend, e=True, v=loadValue['blend'])

                if 'keepLock' in loadValue:
                    cmds.checkBoxGrp(self.optionCheck, e=True, v1=loadValue['keepLock'])

                if 'average' in loadValue:
                    cmds.checkBoxGrp(self.optionCheck, e=True, v2=loadValue['average'])

                if 'useFirst' in loadValue:
                    cmds.checkBoxGrp(self.optionCheck, e=True, v3=loadValue['useFirst'])

            except Exception as e:
                cmds.error(e)
                self.reset_settings()

        if update_ui:
            self.update_ui()

    def reset_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        cmds.floatField(self.blend, e=True, v=0.5)
        cmds.checkBoxGrp(self.optionCheck, e=True, v1=False)
        cmds.checkBoxGrp(self.optionCheck, e=True, v2=False)
        cmds.checkBoxGrp(self.optionCheck, e=True, v3=False)

        if update_ui:
            self.update_ui()

    def remove_settings(self, *args, **kwargs):
        remove_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        self.reset_settings()

    def get_options(self, *args, **kwargs):
        return {
            'blend': cmds.floatField(self.blend, q=True, v=True),
            'keepLock': cmds.checkBoxGrp(self.optionCheck, q=True, v1=True),
            'average': cmds.checkBoxGrp(self.optionCheck, q=True, v2=True),
            'useFirst': cmds.checkBoxGrp(self.optionCheck, q=True, v3=True),
        }

    def close(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

    def show(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

        self._win = cmds.window(self.WINDOW_NAME, title=self.WINDOW_TITLE, mb=True, w=self._width, h=self._height)

        cw1 = 100
        cw2 = 100
        cw3 = 40
        h = 24
        margin = 2

        # Menu
        editMenu = cmds.menu(l='Edit', p=self._win)
        cmds.menuItem(l='Save Settings', p=editMenu, c=self.save_settings)
        cmds.menuItem(l='Reset Settings', p=editMenu, c=self.reset_settings)
        cmds.menuItem(l='Remove Settings', p=editMenu, c=self.remove_settings)

        mainLay = cmds.formLayout(p=self._win, nd=100)

        # Main Buttons
        mainButtonLay = cmds.columnLayout(adj=True, p=mainLay, rs=True)
        copyBtnLay = cmds.rowLayout(adj=1, nc=2, cw2=(cw1, cw3), cl2=['center', 'left'], ct2=['right', 'left'], p=mainButtonLay, h=h)
        self.copyBtn = cmds.iconTextButton(l='Copy', style='textOnly', fn='boldLabelFont', dtg='-1', p=copyBtnLay, h=h, bgc=[0.8, 0.6, 0.6], c=self.on_copy_btn)
        cmds.text(l='', p=copyBtnLay, w=cw3)
        self.copyBtnLay = copyBtnLay

        pasteBtnLay = cmds.rowLayout(adj=1, nc=2, cw2=(cw1, cw3), cl2=['center', 'left'], ct2=['right', 'left'], p=mainButtonLay, h=h)
        self.pasteBtn = cmds.iconTextButton(l='Paste', style='textOnly', fn='boldLabelFont', p=pasteBtnLay, h=h, bgc=[0.4, 0.4, 0.4], rpt=True, c=self.on_paste_btn)
        cmds.text(l='', p=pasteBtnLay, w=cw3)
        self.pasteBtnLay = pasteBtnLay

        blendBtnLay = cmds.rowLayout(adj=1, nc=2, cw2=(cw1, cw3), cl2=['center', 'left'], ct2=['right', 'left'], p=mainButtonLay, h=h)
        self.blendBtn = cmds.iconTextButton(l='blend', style='textOnly', fn='boldLabelFont', p=blendBtnLay, bgc=[0.4, 0.4, 0.4], rpt=True, c=self.on_blend_btn)
        self.blend = cmds.floatField(v=0.5, pre=2, min=0.0, max=1.0, step=0.01, p=blendBtnLay, h=h, w=cw3)
        self.blendBtnLay = blendBtnLay

        # Options
        optionLay = cmds.frameLayout(l='Options', lv=False, mw=2, mh=2, cll=False, p=mainLay)
        optionColumn = cmds.columnLayout(adj=True, p=optionLay, rs=2)

        clipLay = cmds.rowLayout(adj=2, nc=2, cw2=(cw1, cw2), cl2=['center', 'left'], ct2=['right', 'left'], p=optionColumn, h=h)
        cmds.text(l='num clips : ', al='right', p=clipLay)
        self.clipCounts = cmds.text(l='0', al='left', fn='boldLabelFont', dtg=str({}), p=clipLay)
        self.chooseClipMenu = cmds.popupMenu(p=self.clipCounts, pmc=self.populate_clip_menu, mm=True)

        copyInfoLay = cmds.rowLayout(adj=2, nc=2, cw2=(cw1, cw2), cl2=['center', 'left'], ct2=['right', 'left'], p=optionColumn, h=h)
        cmds.text(l='copy components : ', al='right', p=copyInfoLay)
        self.copyCounts = cmds.text(l='0', al='left', fn='boldLabelFont', p=copyInfoLay)

        self.optionCheck = cmds.checkBoxGrp(l='', cw4=[0, 80, 80, 80],
                                            l1=': keepLock', l2=': average', l3=': useFirst', v1=False, v2=False, v3=False, adj=1, h=h, p=optionColumn, ncb=3)

        cmds.formLayout(mainLay, e=True,
                        af=[[mainButtonLay, 'top', margin],
                            [mainButtonLay, 'left', margin],
                            [mainButtonLay, 'right', margin],
                            [optionLay, 'left', margin],
                            [optionLay, 'right', margin],
                            [optionLay, 'bottom', margin],
                            ],
                        ac=[[mainButtonLay, 'bottom', margin, optionLay],
                            ],
                        an=[[optionLay, 'top'],
                            ]
                        )

        cmds.showWindow(self._win)
        cmds.scriptJob(e=['SelectionChanged', self.selection_changed], p=self._win, rp=True)

        # コンポーネントの選択順を維持するため、trackSelectionOrderを有効にする
        # scriptJobでＵＩ削除時に元の状態に戻す。
        cmds.scriptJob(uiDeleted=[self._win, 'import maya.cmds;maya.cmds.selectPref(trackSelectionOrder={})'.format(cmds.selectPref(q=True, trackSelectionOrder=True))])
        cmds.selectPref(trackSelectionOrder=True)

        self.reset_settings(update_ui=False)
        self.load_settings()
        self.update_ui()

    def update_ui(self, *args, **kwargs):
        self.get_options()
        self.selection_changed()

    def on_copy_btn(self, *args, **kwargs):
        geos = cmds.ls(sl=True, o=True)
        if not geos:
            return

        skinClusters = lib.list_related_skinClusters(geos[0])
        if not skinClusters:
            return

        comps = lib.flatten_components(cmds.ls(os=True, fl=True))
        if not comps:
            comps = cmds.ls('{}.cp[*]'.format(geos[0]), fl=True)

        data = lib.get_skinCluster_weights(skinClusters[0], comps)
        if data:
            data_dict = data.asDict()
            data_dict['copy_time'] = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
            clip_dtg = cmds.text(self.clipCounts, q=True, dtg=True)
            clips = eval(clip_dtg) if clip_dtg else OrderedDict()
            clips[len(clips)] = data_dict
            cmds.text(self.clipCounts, e=True, l=len(clips), dtg=str(clips))
            cmds.control(self.copyBtn, e=True, dtg=str(len(clips) - 1))
            cmds.text(self.copyCounts, l='{}'.format(len(comps)), e=True)

        self.update_ui()

    def on_paste_btn(self, *args, **kwargs):
        geos = cmds.ls(sl=True, o=True)
        if not geos:
            return

        skinClusters = lib.list_related_skinClusters(geos[0])
        if not skinClusters:
            return

        comps = lib.flatten_components(cmds.ls(os=True, fl=True))
        if not comps:
            comps = cmds.ls('{}.cp[*]'.format(geos[0]), fl=True)

        options = self.get_options()

        clip_dtg = cmds.text(self.clipCounts, q=True, dtg=True)
        clips = eval(clip_dtg) if clip_dtg else OrderedDict()
        data_index = eval(cmds.control(self.copyBtn, q=True, dtg=True))
        data = clips[data_index]
        w_data = lib.SkinClusterWeightData()
        w_data.setDict(data)

        opt = {
            'keepLock': options.get('keepLock', False),
            'average': options.get('average', False),
            'useFirst': options.get('useFirst', False),
            'blend': 1.0,
        }

        lib.set_component_weights(
            skinClusters[0],
            comps,
            w_data,
            **opt)

        refresh_componentEditors()
        self.save_settings()

    def on_blend_btn(self, *args, **kwargs):
        geos = cmds.ls(sl=True, o=True)
        if not geos:
            return

        skinClusters = lib.list_related_skinClusters(geos[0])
        if not skinClusters:
            return

        comps = lib.flatten_components(cmds.ls(os=True, fl=True))
        if not comps:
            comps = cmds.ls('{}.cp[*]'.format(geos[0]), fl=True)

        options = self.get_options()

        clip_dtg = cmds.text(self.clipCounts, q=True, dtg=True)
        clips = eval(clip_dtg) if clip_dtg else OrderedDict()
        data_index = eval(cmds.control(self.copyBtn, q=True, dtg=True))
        data = clips[data_index]
        w_data = lib.SkinClusterWeightData()
        w_data.setDict(data)

        opt = {
            'keepLock': options.get('keepLock', False),
            'average': options.get('average', False),
            'useFirst': options.get('useFirst', False),
            'blend': options.get('blend', 0.5),
        }

        lib.set_component_weights(
            skinClusters[0],
            comps,
            w_data,
            **opt)

        refresh_componentEditors()
        self.save_settings()

    def selection_changed(self, *args, **kwargs):
        cmds.layout(self.copyBtnLay, e=True, en=False)
        cmds.layout(self.pasteBtnLay, e=True, en=False)
        cmds.layout(self.blendBtnLay, e=True, en=False)

        sels = cmds.ls(os=True, fl=True)
        if not sels:
            return

        selObjects = lib.get_objects(sels)
        if not selObjects:
            return

        histories = cmds.listHistory(selObjects, interestLevel=1) or []
        geos = cmds.ls(histories, type='controlPoint', ni=1)
        geos = sorted(set(geos), key=geos.index)
        if len(geos) < 1:
            return

        src = geos[0]
        src_clst = lib.list_related_skinClusters(src)
        if not (src and src_clst):
            return

        cmds.layout(self.copyBtnLay, e=True, en=True)

        data_index = eval(cmds.control(self.copyBtn, q=True, dtg=True))
        if data_index < 0:
            return

        cmds.layout(self.pasteBtnLay, e=True, en=True)
        cmds.layout(self.blendBtnLay, e=True, en=True)

    def populate_clip_menu(self, *args, **kwargs):
        # numMenus = cmds.popupMenu(self.chooseClipMenu, q=True, ni=True)
        cmds.popupMenu(self.chooseClipMenu, e=True, dai=True)
        clip_dtg = cmds.text(self.clipCounts, q=True, dtg=True)
        clips = eval(clip_dtg) if clip_dtg else OrderedDict()
        for i in reversed(clips.keys()):
            data = clips[i]
            cmds.menuItem(p=self.chooseClipMenu,
                          l='{} : {} - {}'.format(i, data['copy_time'], data['components'][:5]),
                          c=functools.partial(self.update_paste_data_index, i, data['numComponents']))

        cmds.menuItem(p=self.chooseClipMenu, rp='N', l='Clear Clipboard', c=self.clear_clipboard_data)

    def update_paste_data_index(self, index, numComps, *args, **kwargs):
        cmds.control(self.copyBtn, e=True, dtg=str(index))
        cmds.text(self.copyCounts, l='{}'.format(numComps), e=True)

    def clear_clipboard_data(self, *args, **kwargs):
        cmds.control(self.copyBtn, e=True, dtg='-1')
        cmds.text(self.clipCounts, e=True, l='0', dtg=str({}))
        cmds.text(self.copyCounts, e=True, l='0')

        self.selection_changed()


class PruneWeightsUI(object):
    u"""
    """

    WINDOW_NAME = '{}_pruneWeights'.format(Tool_Name_Prefix)
    WINDOW_TITLE = '{} Prune Small Weights'.format(Tool_Title_Prefix)

    def __init__(self, *args, **kwargs):
        self._win = None
        self._width = 250
        self._height = 80

    def save_settings(self, *args, **kwargs):
        options = self.get_options()
        save_optionvar('{}__ui_options'.format(self.WINDOW_NAME), options)

    def load_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        loadValue = load_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        if loadValue:
            try:
                if 'pruneValue' in loadValue:
                    cmds.floatFieldGrp(self.pruneValue, e=True, v1=loadValue['pruneValue'])

            except Exception as e:
                cmds.error(e)
                self.reset_settings()

        if update_ui:
            self.update_ui()

    def reset_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        cmds.floatFieldGrp(self.pruneValue, e=True, v1=0.01)

        if update_ui:
            self.update_ui()

    def remove_settings(self, *args, **kwargs):
        remove_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        self.reset_settings()

    def get_options(self, *args, **kwargs):
        return {
            'pruneValue': cmds.floatFieldGrp(self.pruneValue, q=True, v1=True),
        }

    def close(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

    def show(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

        self._win = cmds.window(self.WINDOW_NAME, title=self.WINDOW_TITLE, mb=True, w=self._width, h=self._height)

        cw1 = 100
        cw3 = 50
        h = 24
        margin = 2

        # Menu
        editMenu = cmds.menu(l='Edit', p=self._win)
        cmds.menuItem(l='Save Settings', p=editMenu, c=self.save_settings)
        cmds.menuItem(l='Reset Settings', p=editMenu, c=self.reset_settings)
        cmds.menuItem(l='Remove Settings', p=editMenu, c=self.remove_settings)

        mainLay = cmds.formLayout(p=self._win, nd=100)

        # Options
        optionLay = cmds.frameLayout(l='Options', lv=False, mw=2, mh=2, cll=False, p=mainLay)
        optionColumn = cmds.columnLayout(adj=True, p=optionLay, rs=2)

        self.pruneValue = cmds.floatFieldGrp(label='Prune Value : ', cw2=[cw1, cw3], v1=0.01, pre=2, h=h, p=optionColumn)

        self.applyBtn = cmds.iconTextButton(l='Apply', c=self.apply, p=mainLay, rpt=True, style='textOnly', fn='boldLabelFont', bgc=[0.4, 0.4, 0.4])

        cmds.formLayout(mainLay, e=True,
                        af=[[optionLay, 'top', margin],
                            [optionLay, 'left', margin],
                            [optionLay, 'right', margin],
                            [self.applyBtn, 'left', margin],
                            [self.applyBtn, 'right', margin],
                            [self.applyBtn, 'bottom', margin],
                            ],
                        ac=[[optionLay, 'bottom', margin * 2, self.applyBtn],
                            ],
                        an=[[self.applyBtn, 'top'],
                            ]
                        )

        cmds.showWindow(self._win)
        cmds.scriptJob(e=['SelectionChanged', self.selection_changed], p=self._win, rp=True)

        self.reset_settings(update_ui=False)
        self.load_settings()

    def update_ui(self, *args, **kwargs):
        self.get_options()

        self.selection_changed()

    def apply(self, *args, **kwargs):
        options = self.get_options()

        opt = {
            'pruneWeights': options['pruneValue'],
        }

        clst_and_comps = lib.get_selected_clst_and_components()
        if not clst_and_comps:
            return

        clst, comps = clst_and_comps
        lib.prune_weights(clst, comps, **opt)

        refresh_componentEditors()

        self.save_settings()

    def selection_changed(self, *args, **kwargs):
        cmds.iconTextButton(self.applyBtn, e=True, en=False)

        sels = cmds.ls(os=True, fl=True)
        selObjects = lib.get_objects(sels)
        if not selObjects:
            return

        histories = cmds.listHistory(selObjects, interestLevel=1) or []
        geos = cmds.ls(histories, type='controlPoint', ni=1)
        geos = sorted(set(geos), key=geos.index)
        if len(geos) < 1:
            return

        src = geos[0]
        src_clst = lib.list_related_skinClusters(src)
        if not (src and src_clst):
            return

        cmds.iconTextButton(self.applyBtn, e=True, en=True)


class RoundWeightsUI(object):
    u"""
    """

    WINDOW_NAME = '{}_roundWeights'.format(Tool_Name_Prefix)
    WINDOW_TITLE = '{} Round Weights'.format(Tool_Title_Prefix)

    def __init__(self, *args, **kwargs):
        self._win = None
        self._width = 250
        self._height = 80

    def save_settings(self, *args, **kwargs):
        options = self.get_options()
        save_optionvar('{}__ui_options'.format(self.WINDOW_NAME), options)

    def load_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        loadValue = load_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        if loadValue:
            try:
                if 'roundDigits' in loadValue:
                    cmds.intFieldGrp(self.roundDigits, e=True, v1=loadValue['roundDigits'])

            except Exception as e:
                cmds.error(e)
                self.reset_settings()

        if update_ui:
            self.update_ui()

    def reset_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        cmds.intFieldGrp(self.roundDigits, e=True, v1=3)

        if update_ui:
            self.update_ui()

    def remove_settings(self, *args, **kwargs):
        remove_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        self.reset_settings()

    def get_options(self, *args, **kwargs):
        return {
            'roundDigits': cmds.intFieldGrp(self.roundDigits, q=True, v1=True),
        }

    def close(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

    def show(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

        self._win = cmds.window(self.WINDOW_NAME, title=self.WINDOW_TITLE, mb=True, w=self._width, h=self._height)

        cw1 = 100
        h = 24
        margin = 2

        # Menu
        editMenu = cmds.menu(l='Edit', p=self._win)
        cmds.menuItem(l='Save Settings', p=editMenu, c=self.save_settings)
        cmds.menuItem(l='Reset Settings', p=editMenu, c=self.reset_settings)
        cmds.menuItem(l='Remove Settings', p=editMenu, c=self.remove_settings)

        mainLay = cmds.formLayout(p=self._win, nd=100)

        # Options
        optionLay = cmds.frameLayout(l='Options', lv=False, mw=2, mh=2, cll=False, p=mainLay)
        optionColumn = cmds.columnLayout(adj=True, p=optionLay, rs=2)

        self.roundDigits = cmds.intFieldGrp(label='Round Digits : ', cw2=[cw1, 50], v1=3, h=h, p=optionColumn)

        self.applyBtn = cmds.iconTextButton(l='Apply', c=self.apply, p=mainLay, rpt=True, style='textOnly', fn='boldLabelFont', bgc=[0.4, 0.4, 0.4])

        cmds.formLayout(mainLay, e=True,
                        af=[[optionLay, 'top', margin],
                            [optionLay, 'left', margin],
                            [optionLay, 'right', margin],
                            [self.applyBtn, 'left', margin],
                            [self.applyBtn, 'right', margin],
                            [self.applyBtn, 'bottom', margin],
                            ],
                        ac=[[optionLay, 'bottom', margin * 2, self.applyBtn],
                            ],
                        an=[[self.applyBtn, 'top'],
                            ]
                        )

        cmds.showWindow(self._win)
        cmds.scriptJob(e=['SelectionChanged', self.selection_changed], p=self._win, rp=True)

        self.reset_settings(update_ui=False)
        self.load_settings()

    def update_ui(self, *args, **kwargs):
        self.get_options()

        self.selection_changed()

    def apply(self, *args, **kwargs):
        options = self.get_options()

        opt = {
            'roundDigits': options['roundDigits'],
        }

        clst_and_comps = lib.get_selected_clst_and_components()
        if not clst_and_comps:
            return

        clst, comps = clst_and_comps
        lib.round_weights(clst, comps, **opt)

        refresh_componentEditors()

        self.save_settings()

    def selection_changed(self, *args, **kwargs):
        cmds.iconTextButton(self.applyBtn, e=True, en=False)

        sels = cmds.ls(os=True, fl=True)
        selObjects = lib.get_objects(sels)
        if not selObjects:
            return

        histories = cmds.listHistory(selObjects, interestLevel=1) or []
        geos = cmds.ls(histories, type='controlPoint', ni=1)
        geos = sorted(set(geos), key=geos.index)
        if len(geos) < 1:
            return

        src = geos[0]
        src_clst = lib.list_related_skinClusters(src)
        if not (src and src_clst):
            return

        cmds.iconTextButton(self.applyBtn, e=True, en=True)


class EditSkinUI(object):
    u"""
    """

    WINDOW_NAME = '{}'.format(Tool_Name_Prefix)
    WINDOW_TITLE = '{}'.format(Tool_Title_Prefix)

    def __init__(self, *args, **kwargs):
        self._win = None
        self._width = 300
        self._height = 600

        self._nonselect_msg = '-' * 20

        self.rootDir = None

    def close(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

    def show(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

        self._win = cmds.window(self.WINDOW_NAME, title=self.WINDOW_TITLE, mb=True, w=self._width, h=self._height)

        cw1 = 80
        cw2 = 100
        h = 24
        btnSize = 36
        margin = 2

        # Menu
        editMenu = cmds.menu(l='Edit', p=self._win)
        cmds.menuItem(l='Save Settings', p=editMenu, c=self.save_settings)
        cmds.menuItem(l='Reset Settings', p=editMenu, c=self.reset_settings)
        cmds.menuItem(l='Remove Settings', p=editMenu, c=self.remove_settings)

        # File
        fileMenu = cmds.menu(l='File', p=self._win, tearOff=True)
        cmds.menuItem(d=True, dl='Single')
        cmds.menuItem(l='Export', p=fileMenu, c=self.export_skinCluster_weight)
        cmds.menuItem(l='Import', p=fileMenu, c=self.import_skinCluster_weight)
        cmds.menuItem(d=True, dl='Multi')
        cmds.menuItem(l='Export (multi)', p=fileMenu, c=self.export_skinCluster_weights)
        cmds.menuItem(l='Import (multi)', p=fileMenu, c=self.import_skinCluster_weights)

        # Influence
        influenceMenu = cmds.menu(l='Influence', p=self._win, tearOff=True)
        cmds.menuItem(l='Add Influences', p=influenceMenu, c=self.add_influences)
        cmds.menuItem(l='Remove Unused Influences', p=influenceMenu, c=self.remove_unused_influences)
        cmds.menuItem(d=True)
        cmds.menuItem(l='Select Related Influences', p=influenceMenu, c=self.select_related_influences)

        # Modify
        editWeightMenu = cmds.menu(l='Edit Weight', p=self._win, tearOff=True)
        cmds.menuItem(d=True, dl='Maya Default')
        cmds.menuItem(l='Copy Skin Weights...', p=editWeightMenu, c='CopySkinWeightsOptions;', stp='mel')
        cmds.menuItem(l='Mirror Skin Weights...', p=editWeightMenu, c='MirrorSkinWeightsOptions;', stp='mel')
        cmds.menuItem(d=True, dl='Original')
        cmds.menuItem(l='Copy Weights...', p=editWeightMenu, c=self.copyweights_ui)
        cmds.menuItem(l='Smooth Weights...', p=editWeightMenu, c=self.smoothweights_ui)
        cmds.menuItem(l='Clipboard...', p=editWeightMenu, c=self.clipboard_ui)
        cmds.menuItem(l='Normalize', p=editWeightMenu, c=self.normalize_weights)
        cmds.menuItem(l='Prune...', p=editWeightMenu, c=self.pruneweights_ui)
        cmds.menuItem(l='Round...', p=editWeightMenu, c=self.roundweights_ui)
        cmds.menuItem(l='Move...', p=editWeightMenu, c=functools.partial(self.swap_move_weights_ui, 'move'))
        cmds.menuItem(l='Swap...', p=editWeightMenu, c=functools.partial(self.swap_move_weights_ui, 'swap'))

        mainLay = cmds.formLayout(p=self._win, nd=100)

        # Labels
        topLay = cmds.columnLayout(adj=True, p=mainLay, rs=2)
        cmds.separator(style='in', p=topLay)
        geoLay = cmds.rowLayout(nc=2, cw2=(cw1, cw2), cl2=['center', 'left'], ct2=['right', 'left'], adj=2, p=topLay, h=h)
        cmds.text(l='Geometry :', p=geoLay)
        self.geo = cmds.iconTextButton(l=self._nonselect_msg, p=geoLay, fn='boldLabelFont', style='textOnly', align='left', c=self.select_geometry)

        clstLay = cmds.rowLayout(nc=2, cw2=(cw1, cw2), cl2=['center', 'left'], ct2=['right', 'left'], adj=2, p=topLay, h=h)
        cmds.text(l='SkinCluster :', p=clstLay)
        self.clst = cmds.iconTextButton(l=self._nonselect_msg, p=clstLay, fn='boldLabelFont', style='textOnly', align='left', c=self.select_skinCluster)

        cmds.separator(style='in', p=topLay)

        # Tool
        toolLay = cmds.rowColumnLayout(nr=1, p=topLay, h=40)

        # paint
        cmds.iconTextButton(
            ann='paint skin weights',
            c='ArtPaintSkinWeightsToolOptions', stp='mel',
            image1=get_icon('ic_brush_white_36dp_1x.png'),
            iol='Paint', olc=[0.2, 0.2, 0.2], olb=[0.8, 0.8, 0.8, 0.3],
            w=btnSize, h=btnSize, style='iconOnly', p=toolLay)

        # component editor
        cmds.iconTextButton(
            ann='component editor',
            c=self.show_componentEditor,
            image1=get_icon('ic_view_list_white_36dp_1x.png'),
            iol='Comp', olc=[0.2, 0.2, 0.2], olb=[0.8, 0.8, 0.8, 0.3],
            w=btnSize, h=btnSize, style='iconOnly', p=toolLay)

        cmds.separator(style='in', horizontal=False, w=10, p=toolLay)

        # clipboard
        cmds.iconTextButton(
            ann='weight clip board',
            c=self.clipboard_ui,
            image1=get_icon('ic_content_copy_white_36dp_1x.png'),
            iol='Clip', olc=[0.2, 0.2, 0.2], olb=[0.8, 0.8, 0.8, 0.3],
            w=btnSize, h=btnSize, style='iconOnly', p=toolLay)

        # smooth
        cmds.iconTextButton(
            ann='smooth weight',
            c=self.smoothweights_ui,
            image1=get_icon('ic_blur_on_white_36dp_1x.png'),
            iol='Smooth', olc=[0.2, 0.2, 0.2], olb=[0.8, 0.8, 0.8, 0.3],
            w=btnSize, h=btnSize, style='iconOnly', p=toolLay)

        # copy
        cmds.iconTextButton(
            ann='copy weight',
            c=self.copyweights_ui,
            image1=get_icon('ic_transform_white_36dp_1x.png'),
            iol='Copy', olc=[0.2, 0.2, 0.2], olb=[0.8, 0.8, 0.8, 0.3],
            w=btnSize, h=btnSize, style='iconOnly', p=toolLay)

        # move
        cmds.iconTextButton(
            ann='move weight',
            c=functools.partial(self.swap_move_weights_ui, 'move'),
            image1=get_icon('ic_keyboard_arrow_right_white_36dp_1x.png'),
            iol='Move', olc=[0.2, 0.2, 0.2], olb=[0.8, 0.8, 0.8, 0.3],
            w=btnSize, h=btnSize, style='iconOnly', p=toolLay)

        # swap
        cmds.iconTextButton(
            ann='swap weight',
            c=functools.partial(self.swap_move_weights_ui, 'swap'),
            image1=get_icon('ic_swap_horiz_white_36dp_1x.png'),
            iol='Swap', olc=[0.2, 0.2, 0.2], olb=[0.8, 0.8, 0.8, 0.3],
            w=btnSize, h=btnSize, style='iconOnly', p=toolLay)

        cmds.separator(style='in', p=topLay)

        # Slider Lay
        sliderLay = cmds.columnLayout(adj=True, rs=2, p=mainLay, vis=True, en=True)
        sliderRowLay = cmds.rowLayout(adj=4, nc=5, cw5=(30, 30, 30, 100, 30), cl5=['center', 'left', 'left', 'left', 'left'], ct5=['right', 'left', 'left', 'both', 'left'], p=sliderLay, h=32)
        self.apply_collection = cmds.iconTextRadioCollection(p=sliderLay)
        self.apply_add = cmds.iconTextRadioButton('add', l='+', style='textOnly', fn='boldLabelFont', h=30, w=30, p=sliderRowLay, sl=True, onc=self.apply_type_changed, bgc=[0.4, 0.4, 0.4])
        self.apply_multiply = cmds.iconTextRadioButton('multiply', l='x', style='textOnly', fn='boldLabelFont', h=30, w=30, p=sliderRowLay, onc=self.apply_type_changed, bgc=[0.4, 0.4, 0.4])
        self.apply_replace = cmds.iconTextRadioButton('replace', l='=', style='textOnly', fn='boldLabelFont', h=30, w=30, p=sliderRowLay, onc=self.apply_type_changed, bgc=[0.4, 0.4, 0.4])
        self.apply_floatScrollBar = cmds.floatScrollBar(min=-10.0, max=10.0, value=0.0, step=0.1, largeStep=0.2, p=sliderRowLay, cc=self.floatScrollBar_changed, dtg='0.0')
        self.apply_floatField = cmds.floatField(min=-10.0, max=10.0, v=0.1, p=sliderRowLay, w=40, pre=3, cc=self.floatField_changed, ec=self.floatField_enter)
        cmds.popupMenu(mm=True, p=self.apply_floatField)
        cmds.menuItem(l='1.0', c=functools.partial(self.floatField_update, 1.0))
        cmds.menuItem(l='0.1', c=functools.partial(self.floatField_update, 0.1))
        cmds.menuItem(l='0.01', c=functools.partial(self.floatField_update, 0.01))
        cmds.menuItem(l='0.001', c=functools.partial(self.floatField_update, 0.001))

        cmds.separator(style='in', p=sliderLay)

        # Mid
        midLay = cmds.columnLayout(adj=True, rs=2, p=mainLay)

        sortLay = cmds.rowLayout(adj=3, nc=4, cw4=(30, 100, 100, 30), cl4=['center', 'left', 'left', 'right'], ct4=['right', 'left', 'left', 'right'], p=midLay, h=h)
        self.influence_sort = cmds.radioCollection()
        cmds.text(l='Sort : ', p=sortLay)
        cmds.radioButton('alphabetically', l='Alphabetically', sl=True, cl=self.influence_sort, p=sortLay, cc=self.update_influenceList)
        cmds.radioButton('connectindex', l='connectIndex', sl=False, cl=self.influence_sort, p=sortLay)
        cmds.iconTextButton(
            ann='refresh',
            c=self.update_ui,
            image1=get_icon('ic_autorenew_white_36pt.png'),
            w=h, h=h, style='iconOnly', p=sortLay)

        nameFilterLay = cmds.rowLayout(nc=2, cw2=(cw1, cw2), cl2=['center', 'left'], ct2=['right', 'left'], adj=2, p=midLay, h=h)
        self.nameFilterEnableCheck = cmds.checkBox(l='Name Filter : ', v=False, p=nameFilterLay, cc=self.nameFilterEnable_changed)
        self.nameFilterTextField = cmds.textField(tx='.*', fn='fixedWidthFont', en=False, ec=self.nameFilterText_changed, cc=self.nameFilterText_changed, p=nameFilterLay)

        self.affectInflFilterCheck = cmds.checkBox(l='Show Affect Influences Only', v=False, p=midLay, cc=self.affectInflFilterCheck_chenged)

        self.influenceList = cmds.textScrollList(ams=True, fn='plainLabelFont', en=True, h=200, p=mainLay)

        cmds.popupMenu(mm=True, p=self.influenceList)
        cmds.menuItem(l='Lock', en=True, rp='W', c=self.hold_highlight_influences)
        cmds.menuItem(l='Unlock', en=True, rp='E', c=self.unhold_highlight_influences)
        cmds.menuItem(l='Lock (All)', en=True, c=self.hold_all_influences)
        cmds.menuItem(l='Unlock (All)', en=True, c=self.unhold_all_influences)
        # cmds.menuItem(l='Toggle Lock', en=True, c=self.togglehold_highlight_influences)
        cmds.menuItem(l='Toggle Lock (All)', en=True, c=self.togglehold_all_influences)
        cmds.menuItem(d=True)
        cmds.menuItem(l='Select List Items', en=True, rp='N', c=self.select_list_items)
        cmds.menuItem(d=True)
        cmds.menuItem(l='Select Influences', en=True, c=self.select_highlight_influences)
        cmds.menuItem(l='Select Influences (All)', en=True, c=self.select_all_influences)
        cmds.menuItem(d=True)
        cmds.menuItem(l='Select Affected Components', en=True, c=self.select_affected_components)

        bottomLay = cmds.columnLayout(adj=True, p=mainLay, rs=2)
        cmds.separator(style='in', p=bottomLay)
        self.info = cmds.text(l='num components : {} / num influences : {} / {}'.format(0, 0, 0), fn='boldLabelFont', p=bottomLay)

        cmds.formLayout(mainLay, e=True,
                        af=[[topLay, 'top', margin],
                            [topLay, 'left', margin],
                            [topLay, 'right', margin],
                            [midLay, 'left', margin],
                            [midLay, 'right', margin],
                            [sliderLay, 'left', margin],
                            [sliderLay, 'right', margin],
                            [self.influenceList, 'left', margin],
                            [self.influenceList, 'right', margin],
                            [bottomLay, 'left', margin],
                            [bottomLay, 'right', margin],
                            [bottomLay, 'bottom', margin],
                            ],
                        ac=[[sliderLay, 'top', margin, topLay],
                            [midLay, 'top', margin, sliderLay],
                            [self.influenceList, 'top', margin, midLay],
                            [self.influenceList, 'bottom', margin, bottomLay],
                            ],
                        an=[[sliderLay, 'bottom'],
                            [midLay, 'bottom'],
                            [topLay, 'bottom'],
                            [bottomLay, 'top'],
                            ]
                        )

        cmds.showWindow(self._win)
        cmds.scriptJob(e=['SelectionChanged', self.selection_changed], p=self._win, rp=True)

        self.reset_settings(update_ui=False)
        self.load_settings()

    def save_settings(self, *args, **kwargs):
        options = self.get_options()
        save_optionvar('{}__ui_options'.format(self.WINDOW_NAME), options)

    def load_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        loadValue = load_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        if loadValue:
            try:
                pass

            except Exception as e:
                cmds.error(str(e))
                self.reset_settings()

        if update_ui:
            self.update_ui()

    def reset_settings(self, *args, **kwargs):
        update_ui = kwargs.get('update_ui', True)

        cmds.checkBox(self.nameFilterEnableCheck, e=True, v=False)
        cmds.textField(self.nameFilterTextField, e=True, tx='.*', en=False)

        if update_ui:
            self.update_ui()

    def remove_settings(self, *args, **kwargs):
        remove_optionvar('{}__ui_options'.format(self.WINDOW_NAME))
        self.reset_settings()

    def update_ui(self, *args, **kwargs):
        self.selection_changed()
        self.apply_type_changed()

    def apply_type_changed(self, *args, **kwargs):
        apply_type = cmds.radioCollection(self.apply_collection, q=True, sl=True)
        cmds.floatScrollBar(self.apply_floatScrollBar, e=True, en=False)

        col = [[0.4, 0.4, 0.4], [0.9, 0.9, 0.9]]
        cmds.iconTextRadioButton(self.apply_add, e=True, bgc=col[apply_type == 'add'])
        cmds.iconTextRadioButton(self.apply_multiply, e=True, bgc=col[apply_type == 'multiply'])
        cmds.iconTextRadioButton(self.apply_replace, e=True, bgc=col[apply_type == 'replace'])

        if apply_type == 'add':
            cmds.floatField(self.apply_floatField, e=True, v=0.1)
            cmds.floatScrollBar(self.apply_floatScrollBar, e=True, en=True)

        elif apply_type == 'multiply':
            cmds.floatField(self.apply_floatField, e=True, v=1.1)
            cmds.floatScrollBar(self.apply_floatScrollBar, e=True, en=True)

        elif apply_type == 'replace':
            cmds.floatField(self.apply_floatField, e=True, v=0.5)

        self.floatField_changed()

    def floatScrollBar_changed(self, *args, **kwargs):
        v = cmds.floatScrollBar(self.apply_floatScrollBar, q=True, v=True)
        self.apply_weights()
        cmds.floatScrollBar(self.apply_floatScrollBar, e=True, dtg=str(v))

        apply_type = cmds.radioCollection(self.apply_collection, q=True, sl=True)
        if apply_type == 'multiply':
            cmds.floatScrollBar(self.apply_floatScrollBar, e=True, v=1.0, dtg=str(1.0))

    def floatField_update(self, value, *args, **kwargs):
        mode = kwargs.get('mode', 'absolute')
        if mode == 'absolute':
            cmds.floatField(self.apply_floatField, e=True, v=value)
        else:
            cmds.floatField(self.apply_floatField, e=True, v=cmds.floatField(self.apply_floatField, q=True, v=True) + value)

        self.floatField_changed()

    def floatField_changed(self, *args, **kwargs):
        v = cmds.floatField(self.apply_floatField, q=True, v=True)
        step = max(0.001, abs(lib.clamp(-1.0, 1.0, v)))

        apply_type = cmds.radioCollection(self.apply_collection, q=True, sl=True)
        if apply_type == 'add':
            cmds.floatScrollBar(self.apply_floatScrollBar, e=True, v=0.0, step=step, largeStep=step * 2, dtg='0.0')

        elif apply_type == 'multiply':
            cmds.floatScrollBar(self.apply_floatScrollBar, e=True, v=1.0, step=step, largeStep=step * 2, dtg='1.0')

        elif apply_type == 'replace':
            pass

    def floatField_enter(self, *args, **kwargs):
        apply_type = cmds.radioCollection(self.apply_collection, q=True, sl=True)
        if apply_type == 'replace':
            self.apply_weights()

    def apply_weights(self, *args, **kwargs):
        pv = float(cmds.floatScrollBar(self.apply_floatScrollBar, q=True, dtg=True))
        v = cmds.floatScrollBar(self.apply_floatScrollBar, q=True, v=True)
        fv = cmds.floatField(self.apply_floatField, q=True, v=True)

        influences = cmds.textScrollList(self.influenceList, q=True, si=True)
        if not influences:
            return

        comps = cmds.ls(sl=True, fl=True)
        if not comps:
            return

        apply_type = cmds.radioCollection(self.apply_collection, q=True, sl=True)
        apply_value = 1.0
        if apply_type == 'replace':
            apply_value = fv

        elif apply_type == 'add':
            apply_value = v - pv

        elif apply_type == 'multiply':
            apply_value = fv if v - pv > 0.0 else 1 / fv

        lib.update_weights(apply_value, influences, comps, method=apply_type)

        refresh_componentEditors()

    def selection_changed(self, *args, **kwargs):
        cmds.iconTextButton(self.geo, e=True, l=self._nonselect_msg, dtg='')
        cmds.iconTextButton(self.clst, e=True, l=self._nonselect_msg, dtg='')
        cmds.textScrollList(self.influenceList, e=True, dtg='', en=False)
        cmds.text(self.info, l='num components : {} / num influences : {} / {}'.format(0, 0, 0), e=True)

        sels = cmds.ls(os=True, fl=True)
        selObjects = lib.get_objects(sels)
        if selObjects:
            histories = cmds.listHistory(selObjects, interestLevel=1) or []
            geos = cmds.ls(histories, type='controlPoint', ni=1)
            geos = sorted(set(geos), key=geos.index)
            nGeos = len(geos)
            if nGeos != 0:
                geo = cmds.listRelatives(geos[0], p=True, pa=True)[0]
                cmds.iconTextButton(self.geo, e=True, l=geo, dtg=geo)

                clst = lib.list_related_skinClusters(geo)
                if clst:
                    clst = clst[0]
                    cmds.iconTextButton(self.clst, e=True, l=clst, dtg=clst)

                    influenceIndexList, influenceList = lib.list_influences(clst, longName=False)
                    cmds.textScrollList(self.influenceList, e=True, dtg=str(influenceList), en=True)

        self.update_influenceList()

    def update_influenceList(self, *args, **kwargs):
        prev_select_items = cmds.textScrollList(self.influenceList, q=True, si=True)
        cmds.textScrollList(self.influenceList, e=True, ra=True)
        nameFilterEnabled = cmds.checkBox(self.nameFilterEnableCheck, q=True, v=True)
        affectInflFilterEnabled = cmds.checkBox(self.affectInflFilterCheck, q=True, v=True)
        dtg = cmds.textScrollList(self.influenceList, q=True, dtg=True)
        all_items = eval(dtg) if dtg else []

        geo = cmds.iconTextButton(self.geo, q=True, dtg=True)
        if not geo:
            return

        clst = cmds.iconTextButton(self.clst, q=True, dtg=True)
        if not clst:
            return

        comps = lib.get_object_components(geo, cmds.ls(sl=True, fl=True))
        if not comps:
            comps = cmds.ls('{}.cp[*]'.format(geo), fl=True)

        set_items = None
        if nameFilterEnabled:
            filterText = cmds.textField(self.nameFilterTextField, q=True, tx=True)
            if filterText:
                try:
                    filter_re = re.compile(filterText, re.I)
                    if filter_re:
                        set_items = [item for item in all_items if filter_re.search(item)]
                except:
                    traceback.print_exc()
        else:
            set_items = all_items

        if affectInflFilterEnabled:
            affect_infls = lib.get_affect_influences(clst, comps)
            set_items = [item for item in set_items if item in affect_infls]

        if set_items:
            sortType = cmds.radioCollection(self.influence_sort, q=True, sl=True)
            if sortType == 'alphabetically':
                set_items.sort()

            cmds.textScrollList(self.influenceList, e=True, append=set_items)

            if prev_select_items:
                select_items = [item for item in prev_select_items if item in set_items]
                if select_items:
                    cmds.textScrollList(self.influenceList, e=True, si=select_items)

        cmds.text(self.info, l='num components : {} / num influences : {} / {}'.format(len(comps), len(set_items), len(all_items)), e=True)
        self.update_influenceList_lineFont()

    def affectInflFilterCheck_chenged(self, *args, **kwargs):
        self.update_influenceList()

    def nameFilterEnable_changed(self, *args, **kwargs):
        nameFilterEnabled = cmds.checkBox(self.nameFilterEnableCheck, q=True, v=True)
        cmds.textField(self.nameFilterTextField, e=True, en=nameFilterEnabled)
        self.update_influenceList()

    def nameFilterText_changed(self, *args, **kwargs):
        self.update_influenceList()

    def update_influenceList_lineFont(self, *args, **kwargs):
        items = cmds.textScrollList(self.influenceList, q=True, ai=True)
        if items:
            for i, item in enumerate(items, 1):
                _font = 'boldLabelFont' if lib.is_lockInfluence(item) else 'plainLabelFont'
                cmds.textScrollList(self.influenceList, e=True, lf=[i, _font])

            refresh_componentEditors()
            refresh_skinInfluenceList()

    def on_select_scrollItem(self, *args, **kwargs):
        items = cmds.textScrollList(self.influenceList, q=True, si=True)
        if items:
            cmds.hilite(items, r=True)
            cmds.floatScrollBar(self.apply_floatScrollBar, e=True,)

    def select_related_influences(self, *args, **kwargs):
        geo = cmds.iconTextButton(self.geo, q=True, dtg=True)
        if geo:
            lib.select_related_influences(geo)

    def add_influences(self, *args, **kwargs):
        all_joints = cmds.textScrollList(self.influenceList, q=True, ai=True)
        sel_joints = cmds.ls(sl=True, typ='joint')
        add_joints = [joint for joint in sel_joints if joint not in all_joints]
        clst = cmds.iconTextButton(self.clst, q=True, dtg=True)
        if add_joints and clst:
            cmds.skinCluster(clst, e=True, dr=4, lw=True, wt=0.0, addInfluence=add_joints)
            self.update_ui()

    def remove_unused_influences(self, *args, **kwargs):
        mel.eval('removeUnusedInfluences;')
        self.update_ui()

    def hold_all_influences(self, *args, **kwargs):
        items = eval(cmds.textScrollList(self.influenceList, q=True, dtg=True))
        if items:
            lib.hold_influence(items)
            self.update_influenceList_lineFont()

    def unhold_all_influences(self, *args, **kwargs):
        items = eval(cmds.textScrollList(self.influenceList, q=True, dtg=True))
        if items:
            lib.unhold_influence(items)
            self.update_influenceList_lineFont()

    def togglehold_all_influences(self, *args, **kwargs):
        items = eval(cmds.textScrollList(self.influenceList, q=True, dtg=True))
        if items:
            lib.togglehold_influence(items)
            self.update_influenceList_lineFont()

    def hold_highlight_influences(self, *args, **kwargs):
        items = cmds.textScrollList(self.influenceList, q=True, si=True)
        if items:
            lib.hold_influence(items)
            self.update_influenceList_lineFont()

    def unhold_highlight_influences(self, *args, **kwargs):
        items = cmds.textScrollList(self.influenceList, q=True, si=True)
        if items:
            lib.unhold_influence(items)
            self.update_influenceList_lineFont()

    def togglehold_highlight_influences(self, *args, **kwargs):
        items = cmds.textScrollList(self.influenceList, q=True, si=True)
        if items:
            lib.togglehold_influence(items)
            self.update_influenceList_lineFont()

    def select_all_influences(self, *args, **kwargs):
        items = eval(cmds.textScrollList(self.influenceList, q=True, dtg=True))
        if items:
            cmds.select(items, r=True)

    def on_doubleclick_scrollItem(self, *args, **kwargs):
        items = cmds.textScrollList(self.influenceList, q=True, si=True)
        if items:
            cmds.select(items, r=True)

    def select_highlight_influences(self, *args, **kwargs):
        items = cmds.textScrollList(self.influenceList, q=True, si=True)
        if items:
            cmds.select(items, r=True)

    def select_list_items(self, *args, **kwargs):
        sii = cmds.textScrollList(self.influenceList, q=True, sii=True)
        items = cmds.textScrollList(self.influenceList, q=True, ai=True)
        if items:
            idx = min(sii) if sii else 1
            cmds.textScrollList(self.influenceList, e=True, si=items, shi=idx)

    def select_geometry(self, *args, **kwargs):
        geo = cmds.iconTextButton(self.geo, q=True, dtg=True)
        if geo:
            cmds.select(geo, tgl=True)

    def select_skinCluster(self, *args, **kwargs):
        clst = cmds.iconTextButton(self.clst, q=True, dtg=True)
        if clst:
            cmds.select(clst, tgl=True)

    def select_affected_components(self, *args, **kwargs):
        clst = cmds.iconTextButton(self.clst, q=True, dtg=True)
        items = cmds.textScrollList(self.influenceList, q=True, si=True)
        if clst and items:
            cmds.skinCluster(clst, e=True, selectInfluenceVerts=items)

    def normalize(self, *args, **kwargs):
        lib.nomalize_weights()

    # Weight I/O
    def export_skinCluster_weight(self, *args, **kwargs):
        geo = cmds.iconTextButton(self.geo, q=True, dtg=True)
        clst = cmds.iconTextButton(self.clst, q=True, dtg=True)
        if not (geo and clst):
            cmds.error('[Export Weight] Please select skinned geometry.')
            return

        if not self.rootDir:
            self.rootDir = cmds.workspace(q=True, rd=True).replace(os.sep, '/')
        dirs = cmds.fileDialog2(caption='Export SkinCluster Wegiht', ds=2, fm=2, okc='Export', ff='*.json', dir=self.rootDir)
        if not dirs:
            return

        dir_ = dirs[0]
        if not os.path.isdir(dir_):
            os.makedirs(dir_)

        self.rootDir = dir_

        base_name = '{}.json'.format(geo).replace('|', '__').replace(':', '_')
        file_path = os.path.join(dir_, base_name)

        with lib.waitCursorBlock():
            lib.write_skinClusterData(geo, file_path)

    def export_skinCluster_weights(self, *args, **kwargs):
        nodes = cmds.ls(sl=True, o=True)
        skinnedNodes = [node for node in nodes if lib.list_related_skinClusters(node)]
        if not skinnedNodes:
            cmds.error('[Export Weight] Please select skinned geometry.')
            return

        if not self.rootDir:
            self.rootDir = cmds.workspace(q=True, rd=True).replace(os.sep, '/')
        dirs = cmds.fileDialog2(caption='Export SkinCluster Wegihts (multi)', ds=2, fm=3, okc='Export', ff='*.json', dir=self.rootDir)
        if not dirs:
            return

        dir_ = dirs[0]
        if not os.path.isdir(dir_):
            os.makedirs(dir_)

        self.rootDir = dir_

        with lib.waitCursorBlock():
            lib.export_skinClusterWeights(skinnedNodes, dir_)

    def import_skinCluster_weight(self, *args, **kwargs):
        geo = cmds.iconTextButton(self.geo, q=True, dtg=True)
        clst = cmds.iconTextButton(self.clst, q=True, dtg=True)
        if not (geo and clst):
            cmds.error('[Export Weight] Please select skinned geometry.')
            return

        if not self.rootDir:
            self.rootDir = cmds.workspace(q=True, rd=True).replace(os.sep, '/')
        files = cmds.fileDialog2(caption='Import SkinCluster Wegiht', ds=2, fm=1, okc='Import', ff='*.json', dir=self.rootDir)
        if not files:
            return

        file_path = files[0]

        self.rootDir = file_path

        with lib.waitCursorBlock():
            read_data = lib.read_skinClusterData(file_path)
            lib.set_skinCluster_weights(geo, read_data)

    def import_skinCluster_weights(self, *args, **kwargs):
        if not self.rootDir:
            self.rootDir = cmds.workspace(q=True, rd=True).replace(os.sep, '/')
        files = cmds.fileDialog2(caption='Import SkinCluster Wegihts (multi)', ds=2, fm=4, okc='Import', ff='*.json', dir=self.rootDir)
        if not files:
            return

        with lib.waitCursorBlock():
            lib.import_skinClusterWeights(files)

    # Skin Edit Sub UI
    def show_componentEditor(self, *args, **kwargs):
        ce = mel.eval('componentEditorWindow()')
        ctl = cmds.componentEditor(ce, q=True, p=True)
        tabLay = cmds.layout(cmds.layout(ctl, q=True, p=True), q=True, p=True) + '|compEdTab'
        labels = cmds.componentEditor(ce, q=True, operationLabels=True)
        for i, label in enumerate(labels, 1):
            if 'Smooth Skins' in label:
                cmds.tabLayout(tabLay, e=True, sti=i)
                break

    def copyweights_ui(self, *args, **kwargs):
        CopyWeightsUI().show()

    def smoothweights_ui(self, *args, **kwargs):
        SmoothWeightsUI().show()

    def clipboard_ui(self, *args, **kwargs):
        WeightClipboardUI().show()

    def normalize_weights(self, *args, **kwargs):
        lib.normalize_weights_from_selection()
        refresh_componentEditors()

    def pruneweights_ui(self, *args, **kwargs):
        PruneWeightsUI().show()

    def roundweights_ui(self, *args, **kwargs):
        RoundWeightsUI().show()

    def swap_move_weights_ui(self, mode, *args, **kwargs):
        SwapMoveWeightsUI(mode).show()


def openUI(*args, **kwargs):
    EditSkinUI().show()
