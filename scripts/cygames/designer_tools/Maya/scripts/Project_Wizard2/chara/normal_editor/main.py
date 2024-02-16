# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass


import os
import shiboken2
from PySide2 import QtGui, QtWidgets, QtCore

import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI
import pymel.core as pm
from maya.api import OpenMaya as om2

from . import setting

from . import poly_info
from . import utility
from . import blend_normal
from . import copy_normal
from . import adjust_normal
from . import view
from . import drag_normal

reload(poly_info)
reload(utility)
reload(blend_normal)
reload(copy_normal)
reload(adjust_normal)
reload(view)
reload(drag_normal)

# ===============================================
# ツールマニュアル: https://wisdom.cygames.jp/pages/viewpage.action?pageId=495099672
# ===============================================
def main():
    main = Main()
    main.create_ui()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ==================================================
    def __init__(self):

        self.tool_version = '2023/03/31'
        self.tool_name = 'Wiz2NormalEditor'

        self.window_name = self.tool_name + 'Win'

        # スクリプトのパス関連
        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        # 設定関連
        self.setting = setting.Setting(self.tool_name)  # base_class.setting

        # メンバ変数
        self.copy_normal_instance = None
        self.adjust_normal_instance = None
        self.grp_list = []
        self.setup_flg = False

        # ツールインスタンス
        self.vertex_normal_dragger = drag_normal.VertexNormalDragger()

        # ビュー周りの設定
        self.view = view.View()
        self.view.save_func = self.save_setting

    # ==================================================
    def deleteOverlappingWindow(self, target):
        '''Windowの重複削除処理
        '''

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        try:
            main_window = shiboken2.wrapInstance(
                long(main_window), QtWidgets.QMainWindow)
        except Exception:
            # Maya 2022-
            main_window = shiboken2.wrapInstance(
                int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            # str必須（reloadでViewクラス(QMainWindow)の内部のtypeが変わるため）
            if str(type(target)) == str(type(widget)):
                widget.deleteLater()

    # ==================================================
    def create_ui(self):

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)

        self.setup_flg = True

        self.grp_list = [
                    {
                        'key': 'General',
                        'widget': self.view.ui.General,
                        'button': self.view.ui.basicNormToolGrpBtn
                    },

                    {
                        'key': 'NumericEdit',
                        'widget': self.view.ui.NumericEdit,
                        'button': self.view.ui.inputNumGrpBtn
                    },

                    {
                        'key': 'ShiftNormal',
                        'widget': self.view.ui.ShiftNormal,
                        'button': self.view.ui.slideNormGrpBtn
                    },

                    {
                        'key': 'SmoothNormal',
                        'widget': self.view.ui.SmoothNormal,
                        'button': self.view.ui.normSmothGrpBtn
                    },

                    {
                        'key': 'BlendNormal',
                        'widget': self.view.ui.BlendNormal,
                        'button': self.view.ui.normBlendGrpBtn
                    },

                    {
                        'key': 'CopyNormal',
                        'widget': self.view.ui.CopyNormal,
                        'button': self.view.ui.normCopyGrpBtn
                    },

                    {
                        'key': 'AdjustVtxNormal',
                        'widget': self.view.ui.AdjustVtxNormal,
                        'button': self.view.ui.AdjustVtxNormalGrpBtn
                    },

                    {
                        'key': 'SetVtxNormalFromEdge',
                        'widget': self.view.ui.SetVtxNormalFromEdge,
                        'button': self.view.ui.setNormWithSelectEdgeGrpBtn
                    }
                ]

        self.setup_view_event()

        self.load_setting()

        self.setup_flg = False

        self.view.show()

        # 何も操作しないで再度シェルフから呼ばれるとlayout設定が飛ぶためここでセーブを挟む
        self.save_setting()

    # ==================================================
    def setup_view_event(self):

        self.setup_toggle_btn_event()

        self.setup_general_event()

        self.setup_numeric_event()

        self.setup_edit_normal_event()

        self.setup_smooth_normal_event()

        self.setup_blend_normal_event()

        self.setup_copy_normal_event()

        self.setup_adjust_vtx_normal_event()

        self.setup_vtx_normal_from_edge_event()

    # ==================================================
    def setup_toggle_btn_event(self):

        for layout_info in self.grp_list:
            this_btn = layout_info['button']
            this_widget = layout_info['widget']

            this_btn.clicked.connect(lambda x=this_widget, y=this_btn: self.change_wgt_visibility(x, y))

            self.open_toggle(this_widget, this_btn)

    # =================================================
    def change_wgt_visibility(self, target_widget, clicked_button):

        sender = clicked_button
        this_widget = target_widget

        if this_widget.isVisible():
            self.close_toggle(this_widget, sender)
        else:
            self.open_toggle(this_widget, sender)

    # =================================================
    def setup_general_event(self):

        self.view.ui.openManual.triggered.connect(self.open_manual)

        # ------------------------------

        self.view.ui.showNormalHideBtn.clicked.connect(lambda: self.display_normal_from_ui('none'))
        self.view.ui.showNormalVtxBtn.clicked.connect(lambda: self.display_normal_from_ui('vertex'))
        self.view.ui.showNormalFaceBtn.clicked.connect(lambda: self.display_normal_from_ui('face'))
        self.view.ui.showNormalBothBtn.clicked.connect(lambda: self.display_normal_from_ui('both'))

        # ------------------------------

        self.view.ui.normalSizeDownBtn.clicked.connect(lambda: self.set_normal_size_from_ui(-0.5))
        self.view.ui.normalSizeUpBtn.clicked.connect(lambda: self.set_normal_size_from_ui(0.5))

        # ------------------------------

        self.view.ui.normalLockLockBtn.clicked.connect(lambda: self.lock_normal_from_ui(True))
        self.view.ui.normalLockUnlockBtn.clicked.connect(lambda: self.lock_normal_from_ui(False))

        # ------------------------------

        self.view.ui.EdgeHardBtn.clicked.connect(lambda: self.set_edge_from_ui(True))
        self.view.ui.edgeSoftBtn.clicked.connect(lambda: self.set_edge_from_ui(False))

        # ------------------------------

        self.view.ui.showEdgeBasicBtn.clicked.connect(lambda: self.display_edge_from_ui('standard'))
        self.view.ui.showEdgeHardAndSoftBtn.clicked.connect(lambda: self.display_edge_from_ui('hardAndSoft'))
        self.view.ui.showEdgeColoredHardBtn.clicked.connect(lambda: self.display_edge_from_ui('hard'))
        self.view.ui.showEdgeOnlyHardBtn.clicked.connect(lambda: self.display_edge_from_ui('hardOnly'))

        # 法線ツール------------------------------
        # 起動
        self.view.ui.normToolActBtn.clicked.connect(lambda: self.boot_normal_edit_tool_from_ui(True))
        # 解除
        self.view.ui.normToolDisableBtn.clicked.connect(lambda: self.boot_normal_edit_tool_from_ui(False))
        # ドラッグ起動
        self.view.ui.normToolActBtn2.clicked.connect(self.vertex_normal_dragger.begin_drag_normal)
        # ドラッグ解除
        self.view.ui.normToolDisableBtn2.clicked.connect(self.vertex_normal_dragger.end_drag_normal)

    # ==================================================
    def setup_numeric_event(self):
        """
        数値入力 UIイベント設定
        """
        # X, Y, Z 方向のスライダーバー
        self.connect_slider_and_spinbox(self.view.ui.inputNumXSpin, self.view.ui.inputNumXHSlider)
        self.connect_slider_and_spinbox(self.view.ui.inputNumYSpin, self.view.ui.inputNumYHSlider)
        self.connect_slider_and_spinbox(self.view.ui.inputNumZSpin, self.view.ui.inputNumZHSlider)

        # 「絶対値で指定」「加算で設定」ボタンイベント
        self.view.ui.inputNumAbsBtn.clicked.connect(lambda: self.edit_by_numeric_value_from_ui(False))
        self.view.ui.inputNumRelBtn.clicked.connect(lambda: self.edit_by_numeric_value_from_ui(True))

    # ==================================================
    def setup_edit_normal_event(self):

        # ------ 法線ずらし　加算値入力(SpinBox)とスライダーバー
        self.connect_slider_and_spinbox(self.view.ui.slideNormSliderSpin, self.view.ui.slideNormSlider)

        # ------ 法線ずらし 水平方向「-」「+」 (UIの加算値はshift_normal_from_uiの中で反映させている)
        self.view.ui.slideNormHGrpDec.clicked.connect(lambda: self.shift_normal_from_ui([-1, 0, 0]))
        self.view.ui.slideNormHGrpAdd.clicked.connect(lambda: self.shift_normal_from_ui([1, 0, 0]))

        # ------ 法線ずらし 垂直方向「-」「+」 (UIの加算値はshift_normal_from_uiの中で反映させている)
        self.view.ui.slideNormVGrpDec.clicked.connect(lambda: self.shift_normal_from_ui([0, -1, 0]))
        self.view.ui.slideNormVGrpAdd.clicked.connect(lambda: self.shift_normal_from_ui([0, 1, 0]))

    # ==================================================
    def setup_smooth_normal_event(self):
        """
        法線スムース
        """
        # 「元の法線とのブレンド値」「ブレンド法線の検索範囲」スライダーバー
        self.connect_slider_and_spinbox(self.view.ui.normSmothGrpBlendSldSpin, self.view.ui.normSmothGrpBlendSlider)
        self.connect_slider_and_spinbox(self.view.ui.normSmothGrpRangeSldSpin, self.view.ui.normSmothGrpRangeSlider)

        # 「フェイス法線の平均とブレンド」「頂点法線の平均とブレンド」ボタン
        self.view.ui.normSmothFaceAvgBtn.clicked.connect(self.on_average_by_face_normal)
        self.view.ui.normSmothVtxAvgBtn.clicked.connect(self.on_average_by_vertex_normal)

    # ==================================================
    def setup_blend_normal_event(self):

        self.connect_slider_and_spinbox(self.view.ui.normBlendSliderSpin, self.view.ui.normBlendSlider)

        self.view.ui.normBlendEdgBtn.clicked.connect(lambda: self.blend_normal_from_ui())

    # ==================================================
    def setup_copy_normal_event(self):
        """
        法線コピー
        """
        self.view.ui.normCopyBtn.clicked.connect(lambda: self.copy_normal_from_ui())
        self.view.ui.pasteWithSelectionBtn.clicked.connect(self.on_paste_normal_by_list_order)
        self.view.ui.pasteWithIndexBtn.clicked.connect(self.on_paste_normal_by_vertex_index)
        self.view.ui.pasteWithPositionBtn.clicked.connect(self.on_paste_normal_by_vertex_position)

    # ==================================================
    def setup_adjust_vtx_normal_event(self):
        self.view.ui.normSPBtn.clicked.connect(lambda: self.adjust_normal_along_face_from_ui())

    # ==================================================
    def setup_vtx_normal_from_edge_event(self):
        self.view.ui.setNormWithSelectEdgeBtn.clicked.connect(lambda: self.set_normal_from_edge_from_ui())

    # ==================================================
    def connect_slider_and_spinbox(self, spinbox, slider):
        spinbox.valueChanged.connect(lambda v: self.spin_to_slider_val_change(slider, v, spinbox))
        slider.valueChanged.connect(lambda v: self.slider_to_spin_val_change(spinbox, v))

        # sliderがホイールで誤操作されないよう無効化
        slider.wheelEvent = self.disable_wheel
        spinbox.wheelEvent = self.disable_wheel

    # ==================================================
    def disable_wheel(self, e):
        return

    # ==================================================
    def spin_to_slider_val_change(self, slider, value, sender):
        """
        スライダーバー左横のSpinBox(入力フィールド)の値が変わった時に実行される
        Args:
            slider (PySide2.QtWidgets.QSlider): QSlider object
            value (float): 値
            sender (QDoubleSpinBox): QDoubleSpinBox object
        """
        slider.blockSignals(True)
        slider.setValue(value * (10 ** sender.decimals()))
        self.save_setting()
        slider.blockSignals(False)

    # ==================================================
    def slider_to_spin_val_change(self, spinbox, value):
        """
        スライダーバーの値が変わった時に実行される
        Args:
            spinbox (PySide2.QtWidgets.QDoubleSpinBox): QDoubleSpinBox object
            value (int): 加算値 (0.34 なら 34) spinbox.decimalsで小数点何位か決める
        """
        spinbox.blockSignals(True)
        spinbox.setValue(value / (10 ** spinbox.decimals()))
        self.save_setting()
        spinbox.blockSignals(False)

    def open_manual(self):
        import webbrowser
        try:
            webbrowser.open(
                'https://wisdom.cygames.jp/pages/viewpage.action?pageId=495099672')
        except Exception:
            print('マニュアルページがみつかりませんでした。')

    # ==================================================
    def display_normal_from_ui(self, show_type):

        select_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_list:
            return

        transform_list = utility.get_transform_list(select_list)

        if not transform_list:
            return

        for transform in transform_list:

            this_shape = cmds.listRelatives(transform, shapes=True)

            if not this_shape:
                continue

            this_shape = this_shape[0]

            if show_type == 'none':
                cmds.setAttr('{0}.{1}'.format(this_shape, 'displayNormal'), 0)
            else:
                cmds.setAttr('{0}.{1}'.format(this_shape, 'displayNormal'), 1)

            if show_type == 'face':
                cmds.setAttr('{0}.{1}'.format(this_shape, 'normalType'), 1)
            elif show_type == 'vertex':
                cmds.setAttr('{0}.{1}'.format(this_shape, 'normalType'), 2)
            elif show_type == 'both':
                cmds.setAttr('{0}.{1}'.format(this_shape, 'normalType'), 3)

    # ==================================================
    def set_normal_size_from_ui(self, add_value):

        select_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_list:
            return

        transform_list = utility.get_transform_list(select_list)

        if not transform_list:
            return

        for transform in transform_list:

            this_shape = cmds.listRelatives(transform, shapes=True)

            if not this_shape:
                continue

            this_shape = this_shape[0]

            this_value = \
                cmds.getAttr('{0}.{1}'.format(this_shape, 'normalSize'))

            fix_value = this_value + add_value
            fix_value = max(fix_value, 0.0)

            cmds.setAttr('{0}.{1}'.format(this_shape, 'normalSize'), fix_value)

    # ==================================================
    def lock_normal_from_ui(self, is_lock):

        select_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_list:
            return

        contain_vertex_face = False
        for select in select_list:

            if select.find('.vtxFace') > 0:
                contain_vertex_face = True
                break

        fix_target_list = None

        if contain_vertex_face:
            fix_target_list = \
                cmds.polyListComponentConversion(select_list, tvf=True)
        else:
            fix_target_list = \
                cmds.polyListComponentConversion(select_list, tv=True)

        if not fix_target_list:
            return

        if is_lock:
            cmds.polyNormalPerVertex(fix_target_list, fn=True)
        else:
            cmds.polyNormalPerVertex(fix_target_list, ufn=True)

    # ==================================================
    def set_edge_from_ui(self, is_hard):

        select_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_list:
            return

        fix_target_list = \
            cmds.polyListComponentConversion(select_list, te=True)

        if not fix_target_list:
            return

        if is_hard:
            cmds.polySoftEdge(fix_target_list, a=0)
        else:
            cmds.polySoftEdge(fix_target_list, a=180)

    # ==================================================
    def display_edge_from_ui(self, show_type):

        select_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_list:
            return

        transform_list = utility.get_transform_list(select_list)

        if not transform_list:
            return

        for transform in transform_list:

            this_shape = cmds.listRelatives(transform, shapes=True)

            if not this_shape:
                continue

            this_shape = this_shape[0]

            if show_type == 'standard':
                cmds.setAttr('{0}.{1}'.format(this_shape, 'displayEdges'), 0)
            elif show_type == 'hardAndSoft':
                cmds.setAttr('{0}.{1}'.format(this_shape, 'displayEdges'), 1)
            elif show_type == 'hard':
                cmds.setAttr('{0}.{1}'.format(this_shape, 'displayEdges'), 2)
            elif show_type == 'hardOnly':
                cmds.setAttr('{0}.{1}'.format(this_shape, 'displayEdges'), 3)

    # ==================================================
    def blend_normal_from_ui(self):

        blend_value = self.view.ui.normBlendSliderSpin.value()

        blend_normal_cls = blend_normal.BlendNormal()

        blend_normal_cls.execute(blend_value)

    # ==================================================
    def copy_normal_from_ui(self):

        self.copy_normal_instance = copy_normal.CopyNormal()

        current_selection = om2.MGlobal.getActiveSelectionList(True)
        self.copy_normal_instance.copy_normal(current_selection)

    # ==================================================
    def on_paste_normal_by_list_order(self):
        """
        「選択順でペースト」実行
        """

        if not self.copy_normal_instance:
            cmds.warning('ペーストする前に「法線をコピー」を実行してください')
            return
        current_selection = om2.MGlobal.getActiveSelectionList(True)
        self.copy_normal_instance.paste_normal_by_list_order(
            current_selection,
            self.view.ui.normCopySetingOnlyLock.isChecked(),
            self.view.ui.normCopySetingkeepOrgEdge.isChecked())

    # ==================================================
    def on_paste_normal_by_vertex_index(self):
        """
        「頂点インデックスでペースト」実行
        """

        if not self.copy_normal_instance:
            cmds.warning('ペーストする前に「法線をコピー」を実行してください')
            return
        current_selection = om2.MGlobal.getActiveSelectionList(True)
        self.copy_normal_instance.paste_normal_by_vertex_index(
            current_selection,
            self.view.ui.normCopySetingOnlyLock.isChecked(),
            self.view.ui.normCopySetingkeepOrgEdge.isChecked())

    # ==================================================
    def on_paste_normal_by_vertex_position(self):
        """
        「頂点位置でペースト」実行
        """

        if not self.copy_normal_instance:
            cmds.warning('ペーストする前に「法線をコピー」を実行してください')
            return
        mirror_index = None  # ミラーなし
        if self.view.ui.normCopyMirrorRadioXMirror.isChecked():
            mirror_index = 0  # Xミラー
        elif self.view.ui.normCopyMirrorRadioYMirror.isChecked():
            mirror_index = 1  # Yミラー
        elif self.view.ui.normCopyMirrorRadioZMirror.isChecked():
            mirror_index = 2  # Zミラー
        current_selection = om2.MGlobal.getActiveSelectionList(True)
        # dst_target_list, is_locked_vtx_only, keep_soft_edge, is_world_space, mirror_index
        self.copy_normal_instance.paste_normal_by_vertex_position(
            current_selection,
            self.view.ui.normCopySetingOnlyLock.isChecked(),
            self.view.ui.normCopySetingkeepOrgEdge.isChecked(),
            self.view.ui.pasteByWorldRadio.isChecked(),
            mirror_index,
            self.view.ui.normCopyMirrorNormal.isChecked())

    # ==================================================
    def adjust_normal_along_face_from_ui(self):

        if not self.adjust_normal_instance:
            self.adjust_normal_instance = adjust_normal.AdjustNormal()

        self.adjust_normal_instance.should_keep_end_normal = (self.view.ui.normSPCheck.isChecked())

        self.adjust_normal_instance.set_target()
        self.adjust_normal_instance.adjust_normal_along_face()

    # ==================================================
    def set_normal_from_edge_from_ui(self):

        edge_list = cmds.ls('*.e[*]', sl=True, fl=True)

        if not edge_list:
            cmds.warning('select at least one edge')

        all_vtx_list = []
        internal_vtx_list = []
        end_vtx_list = []

        for edge in edge_list:
            this_vtx_list = cmds.polyListComponentConversion(edge, tv=True)
            this_vtx_list = cmds.ls(this_vtx_list, fl=True)
            all_vtx_list.extend(this_vtx_list)

        for vtx in all_vtx_list:
            if all_vtx_list.count(vtx) == 1:
                end_vtx_list.append(vtx)
            else:
                if vtx not in internal_vtx_list:
                    internal_vtx_list.append(vtx)

        use_vtx_list = None
        if self.view.ui.setNormWithSelectEdgeCB.isChecked():
            use_vtx_list = internal_vtx_list
        else:
            use_vtx_list = internal_vtx_list + end_vtx_list

        if not use_vtx_list:
            return

        normal_list = []
        for vtx in use_vtx_list:
            normal_list.append(utility.get_vertex_normal_from_edge(vtx, edge_list))

        cmds.polyNormalPerVertex(use_vtx_list, xyz=normal_list)

    # ==================================================
    def boot_normal_edit_tool_from_ui(self, is_boot):
        """
        法線ツール
        is_boot がTrueなら「起動」
        is_boot がFalseなら「終了」
        """
        if is_boot:
            mel.eval('PolygonNormalEditTool;toolPropertyWindow;')
        else:
            mel.eval('TranslateToolWithSnapMarkingMenu;')
            mel.eval('TranslateToolWithSnapMarkingMenuPopDown;')

    # ==================================================
    def load_setting(self):

        self.load_window(self.setting, 'MainWindow')

        self.load_lo(self.setting, 'RootLayout')

        # ------------------------------

        self.load_value(self.setting, 'NumericEditXValue', self.view.ui.inputNumXSpin)

        self.load_value(self.setting, 'NumericEditYValue', self.view.ui.inputNumYSpin)

        self.load_value(self.setting, 'NumericEditZValue', self.view.ui.inputNumZSpin)

        # ------------------------------

        self.load_value(self.setting, 'ShiftNormalAddValue', self.view.ui.slideNormSliderSpin)

        # ------------------------------

        self.load_value(self.setting, 'SmoothBlendValue', self.view.ui.normSmothGrpBlendSldSpin)

        self.load_value(self.setting, 'SmoothBlendRange', self.view.ui.normSmothGrpRangeSldSpin)

        # ------------------------------

        self.load_value(self.setting, 'BlendValue', self.view.ui.normBlendSliderSpin)

    # ==================================================
    def save_setting(self):

        # setup中は.ui側の初期値を引っ張ってきてしまうため、実行されないようにする
        if not self.setup_flg:

            self.save_window(self.setting, 'MainWindow')

            self.save_lo(self.setting, 'RootLayout')

            # ------------------------------

            self.save_value(self.setting, 'NumericEditXValue', self.view.ui.inputNumXSpin)

            self.save_value(self.setting, 'NumericEditYValue', self.view.ui.inputNumYSpin)

            self.save_value(self.setting, 'NumericEditZValue', self.view.ui.inputNumZSpin)

            # ------------------------------

            self.save_value(self.setting, 'ShiftNormalAddValue', self.view.ui.slideNormSliderSpin)

            # ------------------------------

            self.save_value(self.setting, 'SmoothBlendValue', self.view.ui.normSmothGrpBlendSldSpin)

            self.save_value(self.setting, 'SmoothBlendRange', self.view.ui.normSmothGrpRangeSldSpin)

            # ------------------------------

            self.save_value(self.setting, 'BlendValue', self.view.ui.normBlendSliderSpin)

    # ==================================================
    def load_window(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_width = setting.load(setting_key + '_Width', int)
        this_height = setting.load(setting_key + '_Height', int)
        this_left = setting.load(setting_key + '_Left', int)
        this_top = setting.load(setting_key + '_Top', int)

        if this_width and this_height:
            self.view.resize(this_width, this_height)
        if this_left and this_top:
            self.view.move(QtCore.QPoint(this_left, this_top))

    # ==================================================
    def load_lo(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        for layout_info in self.grp_list:

            this_key = None
            this_widget = None
            this_button = None

            if 'key' in layout_info:
                this_key = layout_info['key']

            if not this_key:
                continue

            if 'widget' in layout_info:
                this_widget = layout_info['widget']

            if not this_widget:
                continue

            if 'button' in layout_info:
                this_button = layout_info['button']

            if not this_button:
                continue

            this_close_default = False

            if 'close' in layout_info:
                this_close_default = layout_info['close']

            this_close = setting.load(setting_key + '_' + this_key + '_close', bool, this_close_default)

            if this_close:
                self.close_toggle(this_widget, this_button)

    # ==================================================
    def load_value(self, setting, setting_key, target_obj):

        if not setting:
            return

        if not setting_key:
            return

        if not target_obj:
            return

        # uiデータ側に初期値は入っているため上書きされる前にとっておく
        default_value = target_obj.value()

        this_value = setting.load(
            setting_key + '_Value', float, default_value)

        target_obj.setValue(this_value)

    # ==================================================
    def save_window(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_width = self.view.size().width()
        this_height = self.view.size().height()
        this_left = self.view.pos().x()
        this_top = self.view.pos().y()

        setting.save(setting_key + '_Width', this_width)
        setting.save(setting_key + '_Height', this_height)
        setting.save(setting_key + '_Left', this_left)
        setting.save(setting_key + '_Top', this_top)

    # ==================================================
    def save_lo(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        for layout_info in self.grp_list:

            this_key = None
            this_widget = None

            if 'key' in layout_info:
                this_key = layout_info['key']

            if not this_key:
                continue

            if 'widget' in layout_info:
                this_widget = layout_info['widget']

            if not this_widget:
                continue

            # isVisibleがFalseの時が閉じている時なので反転
            this_close = not this_widget.isVisible()

            setting.save(setting_key + '_' + this_key + '_close', this_close)

    # ==================================================
    def save_value(self, setting, setting_key, target_obj):

        if not setting:
            return

        if not setting_key:
            return

        if not target_obj:
            return

        this_value = target_obj.value()
        setting.save(setting_key + '_Value', this_value)

    # ==================================================
    def close_toggle(self, widget, btn):
        """
        トグルを閉じる
        バグ防止のため、トグル開閉時は必ずこれを使うこと
        """
        widget.hide()
        btn.setIcon(QtGui.QIcon(':arrowRight.png'))

        self.save_setting()

    # ==================================================
    def open_toggle(self, widget, btn):
        """
        トグルを開く
        バグ防止のため、トグル開閉時は必ずこれを使うこと
        """
        widget.show()
        btn.setIcon(QtGui.QIcon(':arrowDown.png'))

        self.save_setting()

    # ==================================================
    def list_adjacent_faces(self, component, affect_range=1):
        """
        隣接するフェイスのリストを返す。
        pymelのconnectedFacesがcmdsのpolyListComponentConversionを使うより結果が良いのでpymelを使っています。
        Args:
            component (str): このコンポーネントに隣接するフェイスを返す
            affect_range (int): 頂点からのいくつ先までのフェイスを選択するか(影響範囲)
        Returns:
            list(str): フェイスのリスト long, flatten
        """
        original_selection = cmds.ls(sl=True)
        faces = []
        pm.select(component)
        for i in range(affect_range):
            vtxs = pm.polyListComponentConversion(pm.ls(sl=True), toVertex=True)
            vtxs = pm.ls(vtxs, fl=True)
            for vtx in vtxs:
                faces.extend(vtx.connectedFaces())
                pm.select(vtx.connectedFaces(), add=True)
        faces = pm.polyListComponentConversion(faces, toFace=True)
        faces = cmds.ls(faces, l=True, fl=True)
        # 元の選択状態に戻す
        cmds.select(original_selection)
        return faces

    # ==================================================
    def list_adjacent_vertices(self, component, affect_range=1):
        """
        隣接する頂点のリストを返す
        pymelのconnectedFacesがcmdsのpolyListComponentConversionを使うより結果が良いのでpymelを使っています。
        Args:
            component (str): このコンポーネントに隣接する頂点を返す
            affect_range (int): 頂点からのいくつ先までのフェイスを選択するか(影響範囲)
        Returns:
            list[str]: 頂点リスト long, flatten
        """
        original_selection = cmds.ls(sl=True)
        vertices = []
        pm.select(component)
        for i in range(affect_range):
            vtxs = pm.polyListComponentConversion(
                pm.ls(sl=True), toVertex=True)
            vtxs = pm.ls(vtxs, fl=True)
            for vtx in vtxs:
                vertices.extend(vtx.connectedVertices())
                pm.select(vtx.connectedVertices(), add=True)
        vertices = pm.polyListComponentConversion(vertices, toVertex=True)
        vertices = cmds.ls(vertices, l=True, fl=True)
        # 元の選択状態に戻す
        cmds.select(original_selection)
        return vertices

    # ==================================================
    def on_average_by_face_normal(self):
        """法線スムース
        「フェイス法線の平均とブレンド」クリック実行
        """
        # 「元の法線とのブレンド値」
        blend_value = self.view.ui.normSmothGrpBlendSldSpin.value()
        # 「ブレンド法線の検索範囲」
        blend_range = self.view.ui.normSmothGrpRangeSlider.value()
        # 「範囲を確認」
        show_range = self.view.ui.checkSmothGrpRangeChk.isChecked()
        # 「ロック法線のみ」
        apply_only_locked = self.view.ui.applyOnlyLockedVertexFaceNormalChk1.isChecked()
        # Undo一回で元に戻せるように
        cmds.undoInfo(openChunk=True)
        self.average_by_face_normal(
            blend_value, blend_range, show_range, apply_only_locked)
        cmds.undoInfo(closeChunk=True)

    # ==================================================
    def on_average_by_vertex_normal(self):
        """法線スムース
        「頂点法線の平均とブレンド」クリック実行
        """
        # 「元の法線とのブレンド値」
        blend_value = self.view.ui.normSmothGrpBlendSldSpin.value()
        # 「ブレンド法線の検索範囲」
        blend_range = self.view.ui.normSmothGrpRangeSlider.value()
        # 「範囲を確認」
        show_range = self.view.ui.checkSmothGrpRangeChk.isChecked()
        # 「ロック法線のみ」
        apply_only_locked = self.view.ui.applyOnlyLockedVertexFaceNormalChk2.isChecked()
        # Undo一回で元に戻せるようにtarget_faces
        cmds.undoInfo(openChunk=True)
        self.average_by_vertex_normal(
            blend_value, blend_range, show_range, apply_only_locked)
        cmds.undoInfo(closeChunk=True)

    # ==================================================
    def average_by_face_normal(self, blend_value, blend_range, show_range, apply_only_locked):
        """「フェイス法線の平均とブレンド」
        選択中のコンポーネントの周辺(ブレンド法線の検索範囲)のフェイス法線の平均値をブレンドする。
        cmds.polyAverageNormalとの違い > 距離ではなく隣接する何個先のフェイスで平均を求めるかを指定。
        平均値を取る対象がフェイス法線。
        ブレンドは選択中のコンポーネントを法線ロックをかけられる最小単位のVertexFaceに変換して実行。
        Args:
            blend_value (float): 「元の法線とのブレンド値」元の法線に対し平均値を何パーセント反映させるか。0なら変更なし。
            blend_range (int): 「ブレンド法線の検索範囲」いくつ先までの周辺頂点の平均値を取るか
            show_range (bool): 「範囲を確認」Trueなら実行前に平均値を取る範囲を目視で確認して実行するか決められる。
            apply_only_locked (bool): 「ロック法線のみ」TrueならLock Normalsされている法線にのみ実行する。
        Returns:
            bool: フェイス法線の平均ブレンドができたらTrueを返す
        """
        cmds.selectMode(component=True)
        selection = cmds.ls(sl=True, l=True, fl=True)
        # 法線ロックをかけられる最小単位はVertexFaceなので選択を変換
        target_vf = cmds.polyListComponentConversion(selection, toVertexFace=True)
        if not target_vf:
            cmds.confirmDialog(title='Usage',
                               message='スムースをかけたいコンポーネントを選択して実行してください',
                               button='OK')
            return False
        # それぞれのフェイスを個別に識別できるようにリストし直し
        target_vf = cmds.ls(target_vf, l=True, flatten=True)
        # 「ロック法線のみ」にチェックが入っていたら対象をフィルター（ロックをかけられる最小単位はVertexFace）
        if apply_only_locked:
            filtered_target = []
            for vf in target_vf:
                if True in cmds.polyNormalPerVertex(vf, q=True, freezeNormal=True):
                    filtered_target.append(vf)
            target_vf = filtered_target
            if not target_vf:
                cmds.confirmDialog(title='Usage',
                                   message='「ロック法線のみ」にチェックを入れていますがロックされた頂点が選択されていません',
                                   button='OK')
                return False
        # 平均値を求める周辺フェイスをリスト
        sample_faces = self.list_adjacent_faces(target_vf, blend_range)
        # 重複削除
        sample_faces = list(set(sample_faces))
        # 「範囲を確認」にチェックが入っていたら
        if show_range:
            cmds.select(sample_faces)
            cmds.refresh()  # 選択状態を反映
            user_choice = cmds.confirmDialog(title='Confirm',
                                             message='この範囲の平均値を最初に選択していた頂点に反映させますか?',
                                             button=['Yes', 'Cancel'], defaultButton='Yes',
                                             cancelButton='Cancel', dismissString='Cancel')
            if user_choice == 'Cancel':
                cmds.select(selection)
                return False
        # 範囲内の頂点のVertexFace単位の頂点法線の平均値をもとめる
        sum_normal_x = 0
        sum_normal_y = 0
        sum_normal_z = 0
        for adjacent_face in sample_faces:
            # フェイス単位の法線
            face_normal_info = cmds.polyInfo(adjacent_face, fn=True)[0]
            temp_split = face_normal_info[0:-2].split(' ')
            xNormal = float(temp_split[-3])  # x
            yNormal = float(temp_split[-2])  # y
            zNormal = float(temp_split[-1])  # z
            sum_normal_x += xNormal
            sum_normal_y += yNormal
            sum_normal_z += zNormal
        average_normal_x = sum_normal_x / len(sample_faces)
        average_normal_y = sum_normal_y / len(sample_faces)
        average_normal_z = sum_normal_z / len(sample_faces)
        # ユーザーの選択に平均値をブレンドする
        self.blend_vertex_face_normal(target_vf, average_normal_x, average_normal_y, average_normal_z, blend_value)
        # 選択状態を戻す
        cmds.select(selection)
        return True

    # ==================================================
    def average_by_vertex_normal(self, blend_value, blend_range, show_range, apply_only_locked):
        """法線スムース
        「頂点法線の平均とブレンド」
        選択中の頂点法線に周辺(ブレンド法線の検索範囲)の頂点法線の平均値をブレンドする。
        cmds.polyAverageNormalとの違い > 距離ではなく隣接する何個先の頂点で平均を求めるかを指定。
        平均値を取る対象が頂点法線（正確にはVertef Face Normal）。
        ブレンドは選択中のコンポーネントを法線ロックをかけられる最小単位のVertexFaceに変換して実行。
        Args:
            blend_value (float): 「元の法線とのブレンド値」元の法線に対し平均値を何パーセント反映させるか。0なら変更なし。
            blend_range (int): 「ブレンド法線の検索範囲」いくつ先までの周辺頂点の平均値を取るか
            show_range (bool): 「範囲を確認」Trueなら実行前に平均値を取る範囲を目視で確認して実行するか決められる。
            apply_only_locked (bool): 「ロック法線のみ」TrueならLock Normalsされている法線にのみ実行する。
        Returns:
            bool: 頂点法線の平均ブレンドができたらTrueを返す
        """
        cmds.selectMode(component=True)
        selection = cmds.ls(sl=True, l=True, fl=True)
        target_vf = cmds.polyListComponentConversion(selection, toVertexFace=True)
        if not target_vf:
            cmds.confirmDialog(title='Usage',
                               message='スムースをかけたいコンポーネントを選択して実行してください',
                               button='OK')
            return False
        # それぞれの頂点を個別に識別できるようにリストし直し
        target_vf = cmds.ls(target_vf, l=True, flatten=True)
        # 「ロック法線のみ」にチェックが入っていたら対象をフィルター（ロックをかけられる最小単位はVertexFace）
        if apply_only_locked:
            filtered_target = []
            for vf in target_vf:
                # vertex face 単位で法線ロックの状態のリストが返る
                if True in cmds.polyNormalPerVertex(vf, q=True, freezeNormal=True):
                    filtered_target.append(vf)
            target_vf = filtered_target
            if not target_vf:
                cmds.confirmDialog(title='Usage',
                                   message='「ロック法線のみ」にチェックを入れていますがロックされた頂点が選択されていません',
                                   button='OK')
                return False
        # 平均値を求める周辺頂点をリスト
        sample_verts = self.list_adjacent_vertices(target_vf, blend_range)
        # 重複削除
        sample_verts = list(set(sample_verts))
        # 「範囲を確認」にチェックが入っていたら
        if show_range:
            cmds.select(sample_verts)
            cmds.refresh()  # 選択状態を反映
            user_choice = cmds.confirmDialog(title='Confirm',
                                             message='この範囲の平均値を最初に選択していた頂点に反映させますか?',
                                             button=['Yes', 'Cancel'], defaultButton='Yes',
                                             cancelButton='Cancel', dismissString='Cancel')
            if user_choice == 'Cancel':
                cmds.select(selection)
                return False
        # 範囲内の頂点のVertexFace単位の頂点法線の平均値をもとめる
        sum_normal_x = 0
        sum_normal_y = 0
        sum_normal_z = 0
        for adjacent_vertice in sample_verts:
            # vertex face 単位の法線リストが返る
            xNormals = cmds.polyNormalPerVertex(
                adjacent_vertice, q=True, normalX=True)
            yNormals = cmds.polyNormalPerVertex(
                adjacent_vertice, q=True, normalY=True)
            zNormals = cmds.polyNormalPerVertex(
                adjacent_vertice, q=True, normalZ=True)
            sum_normal_x += sum(xNormals) / len(xNormals)
            sum_normal_y += sum(yNormals) / len(yNormals)
            sum_normal_z += sum(zNormals) / len(zNormals)
        average_normal_x = sum_normal_x / len(sample_verts)
        average_normal_y = sum_normal_y / len(sample_verts)
        average_normal_z = sum_normal_z / len(sample_verts)
        # ユーザーの選択に平均値をブレンドする
        self.blend_vertex_face_normal(target_vf, average_normal_x, average_normal_y, average_normal_z, blend_value)
        # 選択状態を戻す
        cmds.select(selection)
        return True

    # ==================================================
    def blend_vertex_face_normal(self, component, blend_value_x, blend_value_y, blend_value_z, blend_amount):
        """コンポーネントの頂点法線の値をブレンドする。
        Args:
            component (str): vertexやface, vertex faceなどのコンポーネント
            blend_value_x (float): コンポーネントの法線にブレンドしたいx値
            blend_value_y (float): コンポーネントの法線にブレンドしたいy値
            blend_value_z (float): コンポーネントの法線にブレンドしたいz値
            blend_amount (float): 元々の法線とブレンドする割合。0～1。0ならブレンドしない。
        """
        if blend_amount == 0.0:
            return
        vertexFaces = cmds.polyListComponentConversion(component, toVertexFace=True)
        # それぞれの頂点を個別に識別できるようにリストし直し
        vertexFaces = cmds.ls(vertexFaces, l=True, flatten=True)
        for vtxFace in vertexFaces:
            normal_x = cmds.polyNormalPerVertex(vtxFace, q=True, normalX=True)[0]
            normal_y = cmds.polyNormalPerVertex(vtxFace, q=True, normalY=True)[0]
            normal_z = cmds.polyNormalPerVertex(vtxFace, q=True, normalZ=True)[0]
            normal_x = (normal_x * (1 - blend_amount)) + (blend_value_x * blend_amount)
            normal_y = (normal_y * (1 - blend_amount)) + (blend_value_y * blend_amount)
            normal_z = (normal_z * (1 - blend_amount)) + (blend_value_z * blend_amount)
            cmds.polyNormalPerVertex(vtxFace, xyz=[normal_x, normal_y, normal_z])

    # ==================================================
    def fix_vertex_normal(self, target_list):
        """
        fixとは？ コメントがなかったので本来の意図をコードから汲みとれた範囲で記載します。
        target_listを含んでいるメッシュの「全て」の「同じ方向を向いているロック済み頂点（法線のドット積がほぼ1）」
        の法線に対し同じ方向を向くようにダメ押ししている。
        「同じ方向を向いているロック済み頂点」とはVertex Normalが黄色で一本になっているもの。
        Args:
            target_list (list[str]): vtxリスト
        """
        if not target_list:
            return

        this_poly_info = poly_info.PolyInfo(target_list)

        if not this_poly_info.exists:
            return

        all_poly_info = poly_info.PolyInfo(this_poly_info.transform_list)

        if not all_poly_info.exists:
            return

        # ------------------------------

        all_vertex_face_normal_list = \
            cmds.polyNormalPerVertex(
                all_poly_info.vertex_face_list, q=True, xyz=True)

        all_vertex_face_normal_freeze_list = \
            cmds.polyNormalPerVertex(
                all_poly_info.vertex_face_list, q=True, freezeNormal=True)

        # ロックされた法線でないと編集できないのはツールの仕様
        if True not in all_vertex_face_normal_freeze_list:
            cmds.warning('ロックした法線のみ編集できます')
            return

        # ------------------------------

        fix_vertex_list = []
        fix_normal_list = []

        for vertex in all_poly_info.vertex_list:

            this_vertex_face_list = \
                all_poly_info.vertex_with_vertex_face_dict[vertex]

            if len(this_vertex_face_list) <= 1:
                continue

            this_normal_list = []

            for vertex_face in this_vertex_face_list:

                vertex_face_index = \
                    all_poly_info.vertex_face_list.index(vertex_face)

                this_freeze = \
                    all_vertex_face_normal_freeze_list[vertex_face_index]

                if not this_freeze:
                    this_normal_list = None
                    break

                this_normal = [0] * 3

                this_normal[0] = all_vertex_face_normal_list[vertex_face_index * 3]
                this_normal[1] = all_vertex_face_normal_list[vertex_face_index * 3 + 1]
                this_normal[2] = all_vertex_face_normal_list[vertex_face_index * 3 + 2]

                this_normal_list.append(this_normal)

            if not this_normal_list:
                continue

            first_normal = this_normal_list[0]

            same_normal = True
            for this_normal in this_normal_list:

                this_dot = \
                    first_normal[0] * this_normal[0] + \
                    first_normal[1] * this_normal[1] + \
                    first_normal[2] * this_normal[2]

                if abs(1.0 - this_dot) > 0.001:
                    same_normal = False
                    break

            if not same_normal:
                continue

            fix_vertex_list.append(vertex)
            fix_normal_list.append(first_normal)

        if not fix_vertex_list:
            return

        cmds.polyNormalPerVertex(fix_vertex_list, xyz=fix_normal_list)

    # ==================================================
    def edit_by_numeric_value_from_ui(self, is_relative):
        """
        数値入力　「絶対値で指定」「加算で設定」
        Args:
            is_relative (bool): 加算値で設定ならTrue
        """
        add_vector = [0] * 3

        add_vector[0] = \
            self.view.ui.inputNumXSpin.value()
        add_vector[1] = \
            self.view.ui.inputNumYSpin.value()
        add_vector[2] = \
            self.view.ui.inputNumZSpin.value()

        self.edit_normal(add_vector, is_relative)

    # ==================================================
    def edit_normal(self, add_vector, is_relative):
        """選択中のVertex もしくは Vertex Face の法線の向きを設定する。
        Args:
            add_vector (list[float, float, float]): 絶対値設定もしくは加算するベクトル
            is_relative (bool): 加算ならTrue
        """
        target_list = cmds.ls(sl=True, l=True, fl=True)

        contain_vertex_face = False
        for target in target_list:

            if target.find('.vtxFace') > 0:
                contain_vertex_face = True
                break

        fix_target_list = None

        if contain_vertex_face:
            fix_target_list = \
                cmds.polyListComponentConversion(target_list, tvf=True)
        else:
            fix_target_list = \
                cmds.polyListComponentConversion(target_list, tv=True)

        if not fix_target_list:
            cmds.warning('法線を編集したい頂点を選択してください')
            return

        this_poly_info = poly_info.PolyInfo(fix_target_list)

        if not this_poly_info:
            cmds.warning('PolyInfoの取得に失敗しました')
            return

        # ------------------------------

        vertex_face_normal_list = \
            cmds.polyNormalPerVertex(
                this_poly_info.vertex_face_list, q=True, xyz=True)

        vertex_face_normal_freeze_list = \
            cmds.polyNormalPerVertex(
                this_poly_info.vertex_face_list, q=True, freezeNormal=True)

        # ロックされた法線でないと編集できないのはツールの仕様
        if True not in vertex_face_normal_freeze_list:
            cmds.warning('ロックした法線のみ編集できます')
            return

        # ------------------------------

        fix_vertex_face_list = []
        fix_normal_list = []

        for vertex_face in this_poly_info.vertex_face_list:

            this_index = this_poly_info.vertex_face_list.index(vertex_face)

            this_freeze = vertex_face_normal_freeze_list[this_index]

            if not this_freeze:
                continue

            this_normal = [0] * 3

            this_normal[0] = vertex_face_normal_list[this_index * 3]
            this_normal[1] = vertex_face_normal_list[this_index * 3 + 1]
            this_normal[2] = vertex_face_normal_list[this_index * 3 + 2]

            this_fix_normal = [0] * 3

            for p in range(3):

                if is_relative:
                    this_fix_normal[p] = this_normal[p] + add_vector[p]
                else:
                    this_fix_normal[p] = add_vector[p]

            this_fix_normal = utility.normalize_vector(this_fix_normal)

            fix_vertex_face_list.append(vertex_face)
            fix_normal_list.append(this_fix_normal)

        if not fix_vertex_face_list:
            return

        cmds.polyNormalPerVertex(
            fix_vertex_face_list, xyz=fix_normal_list)

    # ==================================================
    def shift_normal_from_ui(self, add_vector):
        """
        法線ずらし
        Vertex もしくは Vertex Face の選択に対して実行する
        x値に * 3 している理由等は不明
        Args:
            add_vector list[]: 例: [1.0, 0, 0] 移動するNormalベクター(加算値はまだ反映されていない)
        """
        # Objectモードで全頂点取得されるととても時間がかかる為選択をチェック(bodyだと20秒くらいかかる)
        if not cmds.selectMode(q=True, component=True):
            cmds.selectMode(component=True)
            cmds.warning('コンポーネントモードでVertexもしくはVertex Faceを選択してください')

        select_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_list:
            cmds.warning('VertexもしくはVertex Faceを選択して実行してください')
            return

        # ここで加算値を取得
        add_value = self.view.ui.slideNormSliderSpin.value()

        fix_add_vector = [0] * 3

        fix_add_vector[0] = add_vector[0] * add_value
        fix_add_vector[1] = add_vector[1] * add_value
        fix_add_vector[2] = add_vector[2] * add_value

        self.shift_normal(select_list, fix_add_vector)

    # ==================================================
    def shift_normal(self, target_list, add_vector):

        if not target_list:
            return

        contain_vertex_face = False
        for target in target_list:

            if target.find('.vtxFace') > 0:
                contain_vertex_face = True
                break

        fix_target_list = None

        if contain_vertex_face:
            fix_target_list = \
                cmds.polyListComponentConversion(target_list, tvf=True)
        else:
            fix_target_list = \
                cmds.polyListComponentConversion(target_list, tv=True)

        if not fix_target_list:
            cmds.warning('法線を編集したい頂点を選択してください')
            return

        this_poly_info = poly_info.PolyInfo(fix_target_list)

        if not this_poly_info:
            cmds.warning('PolyInfoの取得に失敗しました')
            return

        # ------------------------------

        vertex_face_normal_list = \
            cmds.polyNormalPerVertex(
                this_poly_info.vertex_face_list, q=True, xyz=True)

        vertex_face_normal_freeze_list = \
            cmds.polyNormalPerVertex(
                this_poly_info.vertex_face_list, q=True, freezeNormal=True)

        # ロックされた法線でないと編集できないのはツールの仕様
        if True not in vertex_face_normal_freeze_list:
            cmds.warning('ロックした法線のみ編集できます')
            return

        # ------------------------------

        fix_vertex_face_list = []
        fix_normal_list = []

        up_vector = [0, 1, 0]
        up_sub_vector = [0, 0, -1]

        for vertex_face in this_poly_info.vertex_face_list:

            this_index = this_poly_info.vertex_face_list.index(vertex_face)

            this_freeze = vertex_face_normal_freeze_list[this_index]

            if not this_freeze:
                continue

            this_vertex = this_poly_info.vertex_face_with_vertex_dict[vertex_face][0]

            this_average_normal = \
                utility.get_vertex_normal_from_face(this_vertex)

            this_normal = [0] * 3

            this_normal[0] = vertex_face_normal_list[this_index * 3]
            this_normal[1] = vertex_face_normal_list[this_index * 3 + 1]
            this_normal[2] = vertex_face_normal_list[this_index * 3 + 2]

            this_dot = \
                utility.get_dot_value(up_vector, this_average_normal)

            if this_dot < 0.99:
                this_x_vector = \
                    utility.get_cross_vector(
                        up_vector, this_average_normal)
            else:
                this_x_vector = \
                    utility.get_cross_vector(
                        up_sub_vector, this_average_normal)

            this_y_vector = \
                utility.get_cross_vector(
                    this_average_normal, this_x_vector)

            this_fix_normal = [0] * 3

            for p in range(3):

                this_fix_normal[p] = \
                    this_normal[p] + \
                    this_x_vector[p] * add_vector[0] + \
                    this_y_vector[p] * add_vector[1]

            this_fix_normal = utility.normalize_vector(this_fix_normal)

            fix_vertex_face_list.append(vertex_face)
            fix_normal_list.append(this_fix_normal)

        if not fix_vertex_face_list:
            return

        cmds.polyNormalPerVertex(
            fix_vertex_face_list, xyz=fix_normal_list)
