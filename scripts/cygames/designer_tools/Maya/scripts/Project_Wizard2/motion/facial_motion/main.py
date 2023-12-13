import os
import subprocess
from importlib import reload
from functools import partial
try:
    import json
except Exception as ex:
    print(ex)

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

import maya.cmds as cmds

from . import facial
reload(facial)

g_tool_name = 'W2FacialEvent'
g_version = '2023.12.11'

CURRENT_PATH = os.path.dirname(__file__)


class FacialMotionWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """
    ツールのメインウィンドウ
    """
    # マテリアル切り替えトグルボタンラベル
    btn_tgl_edit_mat_text = '作業用マテリアルに切り替え'
    btn_tgl_orig_mat_text = 'マテリアルを元に戻す'
    cur_keynode_eye = 0  # インデックス
    cur_keynode_mouth = 0  # インデックス
    eyebrow_sliders = {}
    current_eyebrow_size = 'M'  # 眉のデフォルトサイズ
    eyebrow_sizes = ['S', 'M', 'L']

    def __init__(self, parent=None):
        super(FacialMotionWindow, self).__init__(parent=parent)
        loader = QUiLoader()
        ui_file_path = os.path.join(CURRENT_PATH, 'window.ui')
        self.UI = loader.load(ui_file_path)  # QMainWindow
        self.setCentralWidget(self.UI)
        self.setWindowTitle(g_tool_name + ' ' + g_version)
        self.setObjectName(g_tool_name)
        self.create_action()
        self.create_menu()
        # ツールリロード
        self.UI.btn_reload_window.clicked.connect(main)
        # 顔リロード
        self.UI.btn_reload_face.clicked.connect(self.reload_face)
        # 眉リロード
        self.UI.btn_reload_eyebrow.clicked.connect(self.reload_eyebrow)
        # マテリアル切り替えボタン
        self.UI.btn_tgl_edit_orig_mat.clicked.connect(self.switch_material)
        # キーオブジェクトを選択
        self.UI.btn_select_keynode.clicked.connect(self.on_select_key_node)
        # 目　キークリア
        self.UI.btn_clear_eye_keys.clicked.connect(partial(self.on_clear_facial_key, 'eye'))
        # 口　キークリア
        self.UI.btn_clear_mouth_keys.clicked.connect(partial(self.on_clear_facial_key, 'mouth'))
        # 出力フォルダ「選択」
        self.UI.btn_out_dir.clicked.connect(self.on_out_dir)
        self.load_settings()
        scene_path = cmds.file(q=True, sn=True)
        if scene_path:
            scene_name = os.path.basename(scene_path).split('.')[0]
            # 出力ファイル名
            self.UI.txt_out_file_name.setText(scene_name)
        # Unity用にエクスポート
        self.UI.btn_export_motion.clicked.connect(self.on_export_facial_data)
        self.csv_rows = facial.read_csv(os.path.join(CURRENT_PATH, 'csv', 'facial_uv.csv'))
        chara_root = facial.find_chara_root_from_selection()
        if not chara_root:
            chara_root = facial.try_find_chara_root()
        if chara_root:
            cmds.select(chara_root)
        self.reload_face()
        if chara_root:
            cmds.select(chara_root)
        self.reload_eyebrow()

    def reload(self):
        if cmds.window(g_tool_name, exists=True):
            cmds.deleteUI(g_tool_name)
        ui = FacialMotionWindow()
        ui.show()

    def create_action(self):
        self.show_manual_action = QtWidgets.QAction('マニュアル', self,
                                                    statusTip='マニュアルページを開きます',
                                                    triggered=self.show_manual)

        self.show_about_action = QtWidgets.QAction('&About', self,
                                                   statusTip='このツールについて',
                                                   triggered=self.show_about)

    def create_menu(self):
        self.helpMenu = self.menuBar().addMenu('Help')
        self.helpMenu.addAction(self.show_about_action)
        self.helpMenu.addAction(self.show_manual_action)

    def show_about(self):
        cmds.confirmDialog(title='FacialMotionTool', message='表情モーション作成ツールです')

    def show_manual(self):
        import webbrowser
        try:
            webbrowser.open('https://wisdom.cygames.jp/pages/viewpage.action?pageId=741538008')
        except Exception:
            cmds.confirmDialog(title='FacialMotionTool', message='マニュアルのURLが開けませんでした')

    def closeEvent(self, event):
        try:
            self.save_settings()
        except Exception:
            pass

    def reload_face(self):
        """
        シーン内の選択からキャラの目、口周りのUIを更新する
        Returns:
            str: 顔メッシュ
        """
        cur_face = self.UI.txt_face_model.toPlainText()
        self.UI.txt_face_model.setText('')
        face_mesh = facial.find_face_mesh_from_selection()
        if face_mesh:
            self.UI.txt_face_model.setText(face_mesh)
        else:
            cmds.confirmDialog(title='Usage', message='顔メッシュが見つかりませんでした')
            return
        if facial.is_edit_mat(cur_face, 'eye'):
            facial.switch_to_orig_mat(cur_face, 'eye', False, True)
        if facial.is_edit_mat(cur_face, 'mouth'):
            facial.switch_to_orig_mat(cur_face, 'mouth', False, True)
        cmds.select(face_mesh)
        eye_mats = facial.list_materials_from_selecion('eye')
        no_eye_mat = False
        if not eye_mats:
            cmds.confirmDialog(title='Usage', message='eyeマテリアルがありません')
            no_eye_mat = True
        mouth_mats = facial.list_materials_from_selecion('mouth')
        if not mouth_mats:
            if no_eye_mat:
                return
            cmds.confirmDialog(title='Usage', message='mouthマテリアルがありません')
        self.load_facial_buttons(self.UI.layout_eye, self.csv_rows, 'eye', os.path.join(CURRENT_PATH, 'images'), face_mesh)
        self.load_facial_buttons(self.UI.layout_mouth, self.csv_rows, 'mouth', os.path.join(CURRENT_PATH, 'images'), face_mesh)
        # マテリアル切り替えボタンのテキスト
        if facial.is_edit_mat(face_mesh, 'eye'):
            self.UI.btn_tgl_edit_orig_mat.setText(self.btn_tgl_orig_mat_text)
        else:
            self.UI.btn_tgl_edit_orig_mat.setText(self.btn_tgl_edit_mat_text)
        return face_mesh

    def reload_eyebrow(self):
        """
        シーン内の選択からキャラの眉周りのUIを更新する
        Returns:
            str: 眉メッシュ
        """
        self.UI.txt_eyebrow_model.setText('')
        eyebrow_mesh = facial.find_eyebrow_mesh_from_selection(with_blendshape=True)
        if not eyebrow_mesh:
            eyebrow_mesh = facial.find_eyebrow_brendshape_mesh_in_scene()
        if eyebrow_mesh:
            self.UI.txt_eyebrow_model.setText(eyebrow_mesh)
        else:
            user_choice = cmds.confirmDialog(title='Import?',
                                             message='P4リポジトリから自動でブレンドシェイプ付き眉のインポートを試みますか?\n' +
                                             '(P4Vのtoolsとteam/3dcg/chr/plyを最新にしておくことをお勧めします)',
                                             button=['OK', 'Cancel'])
            if user_choice == 'OK':
                self.import_eyebrow()
            else:
                return
        self.load_eyebrow_bars(self.UI.layout_eyebrow, eyebrow_mesh)
        return eyebrow_mesh
    
    def update_script_timeslider_job(self, eyebrow_mesh):
        jobs = cmds.scriptJob(listJobs=True)
        for job in jobs:
            if job.find('FacialMotionWindow.time_change_callback') > -1:
                try:
                    jobId = int(job.split(':')[0])
                    cmds.scriptJob(kill=jobId)
                except Exception as ex:
                    print(ex)
        if eyebrow_mesh and cmds.objExists(eyebrow_mesh):
            cmds.scriptJob(e=('timeChanged', partial(self.time_change_callback, eyebrow_mesh)))

    def import_eyebrow(self):
        # rig班が作っているツールの設定json
        p4_tool_json_path = 'C:/cygames/wiz2/tools/maya/scripts/rig/avatarReferenceTool/data/avatar_collection.json'
        if not os.path.exists(p4_tool_json_path):
            p4_tool_json_path = cmds.fileDialog2(caption='アバターリファレンスツールのavatar_collection.jsonを選択してください',
                                                 fileFilter='*.json', dialogStyle=2, fileMode=1)
            if not p4_tool_json_path:
                return
        f = open(p4_tool_json_path, 'r')
        json_dict = json.load(f)
        eyebrow_dict = json_dict['eyebrow']
        import_window = ImportWindow(eyebrow_dict, '眉を選択', self)
        import_window.show()

    def set_eyebrow_key(self, blendshape, shape, lbl_has_key):
        """
        指定したshapeにキーフレームをセットする
        Args:
            blendshape (str): ブレンドシェイプ名
            shape (str): ブレンドシェイプのシェイプ名
            lbl_has_key (QtWidgets.QLabel): 更新するUI要素 キーがあるかないかを示す〇/●のラベル
        """
        try:
            weight = cmds.getAttr('{0}.{1}'.format(blendshape, shape))
        except Exception:
            return
        if not cmds.setKeyframe('{0}.{1}'.format(blendshape, shape), value=weight, outTangentType='step'):
            cmds.warning('セットキー失敗')
            return
        # ダメ押しでステップカーブ
        cmds.keyTangent('{0}.{1}'.format(blendshape, shape), ott='step')
        lbl_has_key.setText('●')

    def clear_current_eyebrow_key(self, blendshape, shape, lbl_has_key):
        """
        指定したshapeの現在のキーフレームを削除
        Args:
            blendshape (str): ブレンドシェイプ名
            shape (str): ブレンドシェイプのシェイプ名
            spin (QtWidgets.QSpinBox): 更新するUI要素 数値入力のスピンボックス
            slider (QtWidgets.QSlider): 更新するUI要素 数値のスライダーバー
            lbl_has_key (QtWidgets.QLabel): 更新するUI要素 キーがあるかないかを示す〇/●のラベル
        """
        cmds.currentTime(query=True)
        cmds.cutKey('{0}.{1}'.format(blendshape, shape))
        if facial.has_keyframe(blendshape, shape):
            lbl_has_key.setText('●')
        else:
            lbl_has_key.setText('○')

    def clear_all_eyebrow_key(self, blendshape, shape, spin, slider, lbl_has_key):
        """
        指定したshapeのキーフレームをすべて削除
        Args:
            blendshape (str): ブレンドシェイプ名
            shape (str): ブレンドシェイプのシェイプ名
            spin (QtWidgets.QSpinBox): 更新するUI要素 数値入力のスピンボックス
            slider (QtWidgets.QSlider): 更新するUI要素 数値のスライダーバー
            lbl_has_key (QtWidgets.QLabel): 更新するUI要素 キーがあるかないかを示す〇/●のラベル
        """
        spin.setValue(0)
        slider.setValue(0)
        cmds.cutKey('{0}.{1}'.format(blendshape, shape))
        lbl_has_key.setText('○')

    def load_eyebrow_bars(self, layout, eyebrow_mesh):
        """シーン内の選択からキャラの眉のUIを更新する
        Args:
            layout (QVBoxLayout): UIを追加するレイアウト(layout_eyebrow)
            eyebrow_mesh (str): 眉メッシュ名
        """
        self.clear_layout(layout)
        if not eyebrow_mesh:
            cmds.warning('眉メッシュがありません')
            return
        if not cmds.objExists(eyebrow_mesh):
            cmds.warning('眉メッシュがありません: ' + eyebrow_mesh)
            return
        if facial.has_blendshapes_with_sml(eyebrow_mesh):
            self.on_switch_size(layout, eyebrow_mesh, self.current_eyebrow_size)
        else:
            self.clear_layout(layout)
            lbl = QtWidgets.QLabel('ブレンドシェイプの仕様が想定外です')
            layout.addWidget(lbl)
            self.UI.scroll_eyebrow.setMinimumSize(QtCore.QSize(self.UI.scroll_eyebrow.width(), 70))

    def draw_sliders(self, layout, eyebrow_mesh, blendshape, target_shapes, clear=False):
        """
        target_shapesの中のターゲットシェイプ名のスピンボックス、スライダー、セットキー等のボタンを描画する
        Args:
            layout (_type_): _description_
            eyebrow_mesh (_type_): _description_
            blendshape (_type_): _description_
            target_shapes (str[]): スライダーを表示するターゲットシェイプ名
            clear (bool, optional): _description_. Defaults to False.
        """
        self.eyebrow_sliders = {}
        if clear:
            self.clear_layout(layout)
        for shape in target_shapes:
            # sizeはスライダー表示しない
            if shape.endswith('_size'):
                continue
            horizontal_layout = QtWidgets.QHBoxLayout()
            lbl = QtWidgets.QLabel(shape)
            lbl.setFixedWidth(80)
            spin = QtWidgets.QSpinBox()
            spin.setMaximum(100)
            slider = QtWidgets.QSlider(self, orientation=QtCore.Qt.Orientation.Horizontal)
            slider.setMaximum(100)
            btn_add_key = QtWidgets.QPushButton('セットキー')
            btn_remove_key = QtWidgets.QPushButton('キークリア')
            btn_clear_all = QtWidgets.QPushButton('全キークリア')
            lbl_has_key = QtWidgets.QLabel('○')
            if facial.has_keyframe(blendshape, shape):
                lbl_has_key = QtWidgets.QLabel('●')
            btn_add_key.clicked.connect(partial(self.set_eyebrow_key, blendshape, shape, lbl_has_key))
            btn_remove_key.clicked.connect(partial(self.clear_current_eyebrow_key, blendshape, shape, lbl_has_key))
            btn_clear_all.clicked.connect(partial(self.clear_all_eyebrow_key, blendshape, shape, spin, slider, lbl_has_key))
            # getAttrする前に現在のフレーム更新
            cur_time = cmds.currentTime(query=True)
            cmds.currentTime(cur_time, update=True)
            blend_value = cmds.getAttr('{0}.{1}'.format(blendshape, shape))
            blend_value = blend_value * 100
            spin.setValue(blend_value)
            spin.valueChanged.connect(partial(self.on_spin_value_changed, self.eyebrow_sliders, shape))
            slider.setValue(blend_value)
            if not shape in self.eyebrow_sliders:
                self.eyebrow_sliders[shape] = {'slider': slider, 'spin': spin, 'has_key': lbl_has_key}
            slider.valueChanged.connect(partial(self.on_slider_value_change, eyebrow_mesh, self.eyebrow_sliders, shape))
            horizontal_layout.addWidget(lbl)
            horizontal_layout.addWidget(spin)
            horizontal_layout.addWidget(slider)
            horizontal_layout.addWidget(btn_add_key)
            horizontal_layout.addWidget(btn_remove_key)
            horizontal_layout.addWidget(btn_clear_all)
            horizontal_layout.addWidget(lbl_has_key)
            layout.addLayout(horizontal_layout)
        self.UI.scroll_eyebrow.setMinimumSize(QtCore.QSize(self.UI.scroll_eyebrow.width(), 70 + (40 * len(target_shapes))))
        # タイムスライダー移動時イベント更新
        self.update_script_timeslider_job(eyebrow_mesh)

    def draw_eyebrow_sliders_by_size(self, layout, eyebrow_mesh, current_size):
        """サイズ切替のS, M, Lボタンと現在のサイズの眉スライダーを描画する
        Args:
            layout (QVBoxLayout): S, M, L 切替ボタンとスライダーを追加するレイアウト
            eyebrow_mesh (str): 眉メッシュ
            current_size (str): S, M, Lのどれか
        """
        if not eyebrow_mesh:
            cmds.warning('眉メッシュがありません')
            return
        if not cmds.objExists(eyebrow_mesh):
            cmds.warning('眉メッシュがありません: ' + eyebrow_mesh)
            return
        self.clear_layout(layout)
        # スライダーとして描画するターゲットシェイプ
        shapes_for_sliders = facial.get_facial_shapes_by_size(eyebrow_mesh, current_size, True)
        if not shapes_for_sliders:
            cmds.warning('ブレンドシェイプのターゲットメッシュがありません')
            return
        history = cmds.listHistory(eyebrow_mesh)
        blendshapes = cmds.ls(history, type='blendShape')
        if not blendshapes:
            cmds.warning('ブレンドシェイプがありません')
            return
        # S, M, Lボタン
        horizontal_layout = QtWidgets.QHBoxLayout()
        for button_size in self.eyebrow_sizes:
            btn = QtWidgets.QPushButton(button_size)
            btn.clicked.connect(partial(self.on_switch_size, layout, eyebrow_mesh, button_size))
            if button_size == current_size:
                pal = btn.palette()
                pal.setColor(QtGui.QPalette.Button, QtGui.QColor('DarkRed'))
                btn.setAutoFillBackground(True)
                btn.setPalette(pal)
                btn.update()
            horizontal_layout.addWidget(btn)
            layout.addLayout(horizontal_layout)
        # スライダー
        self.draw_sliders(layout, eyebrow_mesh, blendshapes[0], shapes_for_sliders)

    def on_switch_size(self, layout, eyebrow_mesh, size):
        """S, M, L ボタン切替時、ロード時
        眉モデルのベースサイズ切替、表情キーの移動、スライダーの切替, 現在の眉サイズ更新
        Args:
            layout (QVBoxLayout): _description_
            eyebrow_mesh (_type_): _description_
            size (_type_): _description_
        """
        # 眉モデルのベースサイズ切替
        facial.switch_base_size(eyebrow_mesh, size, self.eyebrow_sizes)
        # 表情キーの移動
        facial.replace_facial_keys_to_another_size(eyebrow_mesh, self.current_eyebrow_size, size)
        # キーを打っていない現在のシェイプウェイトを反映
        facial.switch_weight_to_another_size(eyebrow_mesh, self.current_eyebrow_size, size)
        # スライダーの切替
        self.draw_eyebrow_sliders_by_size(layout, eyebrow_mesh, size)
        self.current_eyebrow_size = size  # 現在の眉サイズ更新

    def on_slider_value_change(self, eyebrow_mesh, eyebrow_sliders, slider_shape, value):
        """眉のブレンドシェイプスライダーが動いた時
        Args:
        """
        for shape in eyebrow_sliders:
            spin = eyebrow_sliders[shape]['spin']
            slider = eyebrow_sliders[shape]['slider']
            if shape == slider_shape:
                spin = eyebrow_sliders[shape]['spin']
                try:
                    spin.setValue(value)
                except Exception:
                    cmds.warning('スピンボックス更新失敗')
                lbl_has_key = eyebrow_sliders[shape]['has_key']
                history = cmds.listHistory(eyebrow_mesh)
                blendshapes = cmds.ls(history, type='blendShape')
                if blendshapes:
                    blend_value = value/100.0
                    prev_value = cmds.getAttr('{0}.{1}'.format(blendshapes[0], shape))
                    if blend_value != prev_value:
                        cmds.setAttr('{0}.{1}'.format(blendshapes[0], shape), blend_value)
                    lbl_has_key.setText('○')
                    if facial.has_keyframe(blendshapes[0], shape):
                        lbl_has_key.setText('●')

    def on_spin_value_changed(self, eyebrow_sliders, spin_shape, value):
        for shape in eyebrow_sliders:
            if shape == spin_shape:
                slider = eyebrow_sliders[shape]['slider']
                try:
                    slider.setValue(value)
                except Exception:
                    cmds.warning('スライダー更新失敗')

    def time_change_callback(self, eyebrow_mesh):
        """MayaのTimeSliderが動かされたら表情ツール側の眉のスライダーも更新する
        """
        if not eyebrow_mesh:
            return
        if not cmds.objExists(eyebrow_mesh):
            return
        history = cmds.listHistory(eyebrow_mesh)
        blendshapes = cmds.ls(history, type='blendShape')
        if not blendshapes:
            cmds.warning('ブレンドシェイプがありません')
            return
        try:
            target_shapes = cmds.blendShape(eyebrow_mesh, q=True, target=True)
        except Exception:
            cmds.warning('メッシュのブレンドシェイプがありません: ' + eyebrow_mesh)
            return
        target_shapes = facial.remove_namespace(target_shapes)
        for shape in target_shapes:
            if self.eyebrow_sliders.get(shape):
                spin = self.eyebrow_sliders[shape]['spin']
                slider = self.eyebrow_sliders[shape]['slider']
                cur_value = cmds.getAttr('{0}.{1}'.format(blendshapes[0], shape))
                slider_value = int(cur_value * 100.0)
                try:
                    slider.setValue(slider_value)
                    spin.setValue(slider_value)
                except Exception:
                    print('timesliderのイベントでの更新失敗')
                    pass


    def load_facial_buttons(self, layout, csv_rows, face_part, btn_img_folder, face_mesh):
        """
        csvを元にテクスチャーfileノード事に表情のUVスイッチボタンを作る
        :param csv_rows: 最初のアイテムがテクスチャーfile名
        :return: QHBoxLayout.
        """
        if not csv_rows:
            cmds.warning('Error: csvListが読み込めていません。')
            return
        self.clear_layout(layout)
        label_index_dict = {}
        for i, csv_row in enumerate(csv_rows):
            if i == 0:
                for index, label in enumerate(csv_row):
                    label_index_dict[label] = index
            else:
                try:
                    rowPart = csv_row[label_index_dict['Face Part']]
                    if face_part == rowPart:
                        btn_img_path = os.path.join(btn_img_folder, csv_row[label_index_dict['Default Icon Image']])
                        face_index = int(csv_row[label_index_dict['Face ID']])
                        u = 0
                        v = 0
                        try:
                            u = float(csv_row[int(label_index_dict['Translate Frame U'])])
                            v = float(csv_row[int(label_index_dict['Translate Frame V'])])
                        except Exception:
                            cmds.warning('Error: UV値の読み込みに失敗しました。')
                        if os.path.exists(btn_img_path):
                            row = int(csv_row[int(label_index_dict['Row'])])
                            col = int(csv_row[int(label_index_dict['Col'])])
                            top_x = int(csv_row[int(label_index_dict['Top X'])])
                            top_y = int(csv_row[int(label_index_dict['Top Y'])])
                            width = int(csv_row[int(label_index_dict['Button Image Width'])])
                            height = int(csv_row[int(label_index_dict['Button Image Height'])])
                            lbl = csv_row[int(label_index_dict['Face ID'])]
                            btn_facial = facial.PicButton(btn_img_path,
                                                          top_x,
                                                          top_y,
                                                          width,
                                                          height,
                                                          lbl, self, partial(facial.set_uv, face_mesh, face_part, face_index, u, v, self.UI.chk_set_key))
                            layout.addWidget(btn_facial, row, col)
                        else:
                            btn_facial = QtWidgets.QPushButton(str(i))
                            btn_facial.clicked.connect(partial(facial.set_uv, face_mesh, face_part, face_index, u, v, self.UI.chk_set_key))
                except Exception:
                    pass

    def clear_layout(self, root_layout):
        """
        layoutを空にします
        :return:
        """
        def deleteItems(layout):
            if layout is not None:
                try:
                    while layout.count():
                        item = layout.takeAt(0)
                        widget = item.widget()
                        if widget is not None:
                            widget.deleteLater()
                        else:
                            deleteItems(item.layout())
                except Exception as ex:
                    cmds.confirmDialog(title='Error', message=str(ex))
                    self.reload()
                    return
        deleteItems(root_layout)

    def switch_material(self):
        """作業用マテリアル <> オリジナルマテリアル切り替え
        """
        if not self.UI.txt_face_model.toPlainText():
            cmds.confirmDialog(title='Usage', message='キャラのシーンを開き「顔リロード」をしてください')
            return
        if self.UI.btn_tgl_edit_orig_mat.text() == self.btn_tgl_edit_mat_text:
            self.UI.btn_tgl_edit_orig_mat.setText(self.btn_tgl_orig_mat_text)
            # 作業用マテリアルに切り替える
            facial.switch_to_edit_mat(self.UI.txt_face_model.toPlainText(), 'eye', True)
            facial.switch_to_edit_mat(self.UI.txt_face_model.toPlainText(), 'mouth', False)
        else:
            self.UI.btn_tgl_edit_orig_mat.setText(self.btn_tgl_edit_mat_text)
            # マテリアルを元に戻す
            userChoise = cmds.confirmDialog(title='Warning',
                                            message='表情アニメーションをつけた作業用マテリアルを削除しますか?',
                                            button=['切り替えるだけ', '切り替えて作業用マテリアルを削除', 'Cancel'],
                                            defaultButton='切り替えるだけ',
                                            cancelButton='Cancel',
                                            dismissString='Cancel')
            if userChoise == 'Cancel':
                return
            delete_edit_mat = True
            if userChoise == '切り替えるだけ':
                delete_edit_mat = False
            facial.switch_to_orig_mat(self.UI.txt_face_model.toPlainText(), 'eye', delete_edit_mat, True)
            facial.switch_to_orig_mat(self.UI.txt_face_model.toPlainText(), 'mouth', delete_edit_mat, True)

    def on_select_key_node(self):
        if (self.UI.chk_select_keynode_eye.checkState() == QtCore.Qt.CheckState.Unchecked and 
            self.UI.chk_select_keynode_mouth.checkState() == QtCore.Qt.CheckState.Unchecked and
            self.UI.chk_select_keynode_eyebrow.checkState() == QtCore.Qt.CheckState.Unchecked):
            cmds.confirmDialog(title='Warning',
                        message='選択したいキーオブジェクトにチェックを入れてください',
                        button=['OK'])
            return
        cmds.select(clear=True)
        if self.UI.chk_select_keynode_eye.checkState() == QtCore.Qt.CheckState.Checked:
            if not facial.select_key_node(self.UI.txt_face_model.toPlainText(), 'eye', self.cur_keynode_eye, True):
                return
            if self.cur_keynode_eye < 3:
                self.cur_keynode_eye += 1
            else:
                self.cur_keynode_eye = 0
        if self.UI.chk_select_keynode_mouth.checkState() == QtCore.Qt.CheckState.Checked:
            if not facial.select_key_node(self.UI.txt_face_model.toPlainText(), 'mouth', self.cur_keynode_mouth, True):
                return
            if self.cur_keynode_mouth < 3:
                self.cur_keynode_mouth += 1
            else:
                self.cur_keynode_mouth = 0
        if self.UI.chk_select_keynode_eyebrow.checkState() == QtCore.Qt.CheckState.Checked:
            eyebrow_mesh = self.UI.txt_eyebrow_model.toPlainText()
            if not cmds.objExists(eyebrow_mesh):
                cmds.confirmDialog(title='Warning',
                           message='まずは眉リロードを試してみてください',
                           button=['OK'])
                return
            if facial.has_blendshapes(eyebrow_mesh):
                cmds.select(eyebrow_mesh, add=True)
            else:
                cmds.confirmDialog(title='Warning',
                           message='Blendshapeを持ったメッシュではありません: ' + eyebrow_mesh,
                           button=['OK'])

    def on_clear_facial_key(self, face_part):
        facial.clear_facial_key(self.UI.txt_face_model.toPlainText(), face_part)

    def on_export_facial_data(self):
        out_dir = self.UI.txt_out_dir.toPlainText()
        out_dir.replace('\\', '/')
        if not os.path.exists(out_dir):
            cmds.confirmDialog(title='Usage', message='出力フォルダがありません')
            return
        out_file_name = self.UI.txt_out_file_name.toPlainText()
        if not out_file_name.endswith('.json'):
            out_file_name += '.json'
        export_path = os.path.join(out_dir, out_file_name).replace('\\', '/')
        face_mesh = self.UI.txt_face_model.toPlainText()
        no_face_mesh = False
        if not cmds.ls(face_mesh):
            no_face_mesh = True
            user_choice = cmds.confirmDialog(title='確認',
                                             message='顔メッシュがありません\n' +
                                             '続行しますか?',
                                             button=['OK', 'Cancel'])
            if user_choice != 'OK':
                return
        eyebrow_mesh = self.UI.txt_eyebrow_model.toPlainText()
        if not cmds.ls(eyebrow_mesh):
            if no_face_mesh:
                cmds.confirmDialog(title='Usage', message='エクスポート対象がありません')
                return
            else:
                user_choice = cmds.confirmDialog(title='確認',
                                                 message='眉メッシュがありません\n' +
                                                 '続行しますか?',
                                                 button=['OK', 'Cancel'])
                if user_choice != 'OK':
                    return
        fps = 30
        fps_dict = {'game': 15.0, 'film': 24.0, 'ntsc': 30.0, 'show': 48.0, 'palf': 50.0, 'ntscf': 60.0}
        if cmds.currentUnit(q=True, time=True) != 'ntsc':
            user_choice = cmds.confirmDialog(title='確認',
                                             message='FPSが30ではありません\n' +
                                             '30fpsに設定してもよろしいですか?',
                                             button=['OK', 'NO', 'Cancel'],
                                             defaultButton='OK',
                                             cancelButton='Cancel',
                                             dismissString='Cancel')
            if user_choice == 'OK':
                cmds.currentUnit(time='ntsc')
            elif user_choice == 'Cancel':
                return
            else:
                fps = fps_dict[cmds.currentUnit(q=True, time=True)]
        eye_facial_list = facial.get_facial_list(face_mesh, 'eye', self.csv_rows, fps)
        mouth_facial_list = facial.get_facial_list(face_mesh, 'mouth', self.csv_rows, fps)
        eyebrow_facial_list = facial.get_eyebrow_list(eyebrow_mesh, fps)
        facials = {}
        if eye_facial_list:
            facials['eye'] = eye_facial_list
        if mouth_facial_list:
            facials['mouth'] = mouth_facial_list
        if eyebrow_facial_list:
            facials['eyebrow'] = eyebrow_facial_list
        if not facials:
            cmds.confirmDialog(title='Usage', message='表情のキーフレームがありません')
            return
        try:
            json_file = open(export_path, mode='w')
            json.dump(facials, json_file)
            json_file.close()
            print('出力しました: ' + export_path)
            if os.path.exists(out_dir):
                subprocess.Popen('explorer "{}"'.format(os.path.normpath(out_dir)))
        except Exception:
            cmds.confirmDialog(title='Error', message='出力失敗')

    def save_setting(self, key_name, value):
        """
        optionVarに設定を保存する
        Args:
            key_name (str): UIパーツ名
            value (any): 保存する値
        """
        if isinstance(value, str):
            cmds.optionVar(stringValue=('g_tool_name_{0}'.format(key_name), value))
        elif isinstance(value, int):
            cmds.optionVar(intValue=('g_tool_name_{0}'.format(key_name), value))
        elif isinstance(value, float):
            cmds.optionVar(floatValue=('g_tool_name_{0}'.format(key_name), value))
        elif isinstance(value, bool):
            cmds.optionVar(stringValue=('g_tool_name_{0}'.format(key_name), int(value)))
        else:
            cmds.optionVar(stringValue=('g_tool_name_{0}'.format(key_name), str(value)))

    def load_setting(self, key_name, default_value=''):
        """
        optionVarから保存した設定を読み込む
        Args:
            key_name (str): UIパーツ名
            default_value (any): 保存データがないの場合デフォルトを指定
        """
        if not cmds.optionVar(exists='g_tool_name_{0}'.format(key_name)):
            return default_value
        result = cmds.optionVar(query='g_tool_name_{0}'.format(key_name))
        return result

    def save_settings(self):
        """
        Window init時に設定を読み込む
        """
        self.save_setting('txt_out_dir', self.UI.txt_out_dir.toPlainText())
        self.save_setting('width', self.width())
        self.save_setting('height', self.height())
        self.save_setting('current_eyebrow_size', self.current_eyebrow_size)
        # 目キーオブジェクト　チェックボックス
        if self.UI.chk_select_keynode_eye.checkState() == QtCore.Qt.CheckState.Checked:
            self.save_setting('chk_select_keynode_eye', True)
        else:
            self.save_setting('chk_select_keynode_eye', False)
        # 口キーオブジェクト　チェックボックス
        if self.UI.chk_select_keynode_mouth.checkState() == QtCore.Qt.CheckState.Checked:
            self.save_setting('chk_select_keynode_mouth', True)
        else:
            self.save_setting('chk_select_keynode_mouth', False)
        # 眉キーオブジェクト　チェックボックス
        if self.UI.chk_select_keynode_eyebrow.checkState() == QtCore.Qt.CheckState.Checked:
            self.save_setting('chk_select_keynode_eyebrow', True)
        else:
            self.save_setting('chk_select_keynode_eyebrow', False)
        # 目、口ボタンでアニメーションキーを付ける
        if self.UI.chk_set_key.checkState() == QtCore.Qt.CheckState.Checked:
            self.save_setting('chk_set_key', True)
        else:
            self.save_setting('chk_set_key', False)

    def load_settings(self):
        """
        Windowクローズ時に設定を保存
        """
        desktop_dir = os.path.abspath(os.path.join(os.path.expanduser('~'), '..', 'Desktop'))
        out_dir = self.load_setting('txt_out_dir', desktop_dir)
        if out_dir:
            self.UI.txt_out_dir.setText(out_dir)
        width = int(self.load_setting('width', 600))
        height = int(self.load_setting('height', 1000))
        self.resize(width, height)
        self.current_eyebrow_size = self.load_setting('current_eyebrow_size', 'M')
        # 目キーオブジェクト　チェックボックス
        chk_select_keynode_eye = self.load_setting('chk_select_keynode_eye', False)
        if chk_select_keynode_eye:
            self.UI.chk_select_keynode_eye.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.UI.chk_select_keynode_eye.setCheckState(QtCore.Qt.CheckState.Unchecked)
        # 口キーオブジェクト　チェックボックス
        chk_select_keynode_mouth = self.load_setting('chk_select_keynode_mouth', False)
        if chk_select_keynode_mouth:
            self.UI.chk_select_keynode_mouth.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.UI.chk_select_keynode_mouth.setCheckState(QtCore.Qt.CheckState.Unchecked)
        # 眉キーオブジェクト　チェックボックス
        chk_select_keynode_eyebrow = self.load_setting('chk_select_keynode_eyebrow', False)
        if chk_select_keynode_eyebrow:
            self.UI.chk_select_keynode_eyebrow.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.UI.chk_select_keynode_eyebrow.setCheckState(QtCore.Qt.CheckState.Unchecked)
        # 目、口ボタンでアニメーションキーを付ける
        chk_set_key = self.load_setting('chk_set_key', False)
        if chk_set_key:
            self.UI.chk_set_key.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.UI.chk_set_key.setCheckState(QtCore.Qt.CheckState.Unchecked)

    def on_out_dir(self):
        """
        出力フォルダ「選択」ボタン実行
        """
        start_dir = self.UI.txt_out_dir.toPlainText()
        if not start_dir.strip():
            start_dir = os.path.abspath(os.path.join(os.path.expanduser('~'), '..', 'Desktop'))
        paths = cmds.fileDialog2(fileMode=3, dialogStyle=2, okc='選択', dir=start_dir)
        if paths:
            self.UI.txt_out_dir.setText(paths[0])



class ImportWindow(QtWidgets.QDialog):
    def __init__(self, menu_dict, title='Select to Import', parent=None):
        super(ImportWindow, self).__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.resize(300, 100)
        # Validation
        if not isinstance(menu_dict, dict) or not menu_dict:
            print('Error ImportWindow')
            return
        self.setWindowTitle(title)
        self.menu_dict = menu_dict
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(list(menu_dict.keys()))
        btn_import = QtWidgets.QPushButton('インポート')
        btn_import.clicked.connect(self.import_item)
        layout.addWidget(self.combobox)
        layout.addWidget(btn_import)

    def import_item(self):
        reference_path = self.menu_dict[self.combobox.currentText()]
        if not reference_path or not os.path.exists(reference_path):
            cmds.confirmDialog(title='Warning', message='ファイルがありませんでした(P4更新?): ' + str(reference_path))
            return
        try:
            # P4 rig/avatarReferenceToolに準拠
            if cmds.namespace(exists='eyebrow'):
                cmds.file(
                    reference_path,
                    loadReference='eyebrowRN',
                    type='FBX',
                    f=True
                )
            else:
                cmds.file(
                    reference_path,
                    namespace='eyebrow',
                    r=True,
                    type='FBX',
                    ignoreVersion=True,
                    gl=True,
                    mergeNamespacesOnClash=False,
                )
        except Exception:
            cmds.warning('インポート失敗')
        self.parent.reload()


def main():
    """Windowの起動
    """
    if cmds.window(g_tool_name, exists=True):
        cmds.deleteUI(g_tool_name)
    ui = FacialMotionWindow()
    ui.show()
