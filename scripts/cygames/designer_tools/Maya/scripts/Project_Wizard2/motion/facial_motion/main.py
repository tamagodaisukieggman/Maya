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

from ..common import common
reload(common)


g_tool_name = 'W2FacialEvent'
g_version = '2024.01.15'
g_import_eyebrow_namespace = 'eyebrow'

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
    eyebrow_sliders = {}  # 眉のUIにアクセスする為のdict
    current_eyebrow_size = 'M'  # 眉のデフォルトサイズ

    def __init__(self, parent=None):
        super(FacialMotionWindow, self).__init__(parent=parent)
        if cmds.autoKeyframe(q=True, state=True):
            cmds.confirmDialog(title='Warning', message='AutoKeyframeをOFFにして使ってください')
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
        # Unityからインポート
        self.UI.btn_import_motion.clicked.connect(self.on_import_facial_data)
        self.csv_rows = facial.read_csv(os.path.join(CURRENT_PATH, 'csv', 'facial_uv.csv'))
        chara_root = facial.find_chara_root_from_selection()
        if not chara_root:
            chara_root = facial.try_find_chara_root_in_scene()
        if chara_root:
            cmds.select(chara_root)
        self.reload_face()
        if chara_root:
            cmds.select(chara_root)
        self.reload_eyebrow()

    def reload(self):
        """ツールウィンドウリロード
        """
        if cmds.window(g_tool_name, exists=True):
            cmds.deleteUI(g_tool_name)
        ui = FacialMotionWindow()
        ui.show()

    def create_action(self):
        """ツールウィンドウ左上メニューアクション作成
        """
        self.show_manual_action = QtWidgets.QAction('マニュアル', self,
                                                    statusTip='マニュアルページを開きます',
                                                    triggered=self.show_manual)

        self.show_about_action = QtWidgets.QAction('&About', self,
                                                   statusTip='このツールについて',
                                                   triggered=self.show_about)

    def create_menu(self):
        """ツールウィンドウ左上メニュー設定
        """
        self.helpMenu = self.menuBar().addMenu('Help')
        self.helpMenu.addAction(self.show_about_action)
        self.helpMenu.addAction(self.show_manual_action)

    def show_about(self):
        """ツールウィンドウ左上Help > Aboutクリック時
        """
        cmds.confirmDialog(title='FacialMotionTool', message='表情モーション作成ツールです')

    def show_manual(self):
        """ツールウィンドウ左上Help > マニュアルクリック時
        """
        import webbrowser
        try:
            webbrowser.open('https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=741538008')
        except Exception:
            cmds.confirmDialog(title='FacialMotionTool', message='マニュアルのURLが開けませんでした')

    def closeEvent(self, event):
        """ツールウィンドウクローズ時
        """
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
        eyebrow_to_hide = None
        eyebrow_mesh = facial.find_eyebrow_mesh_from_selection(with_blendshape=True)
        if not eyebrow_mesh:
            # ブレンドシェイプ付き眉でなくてもとりあえず眉があれば眉メッシュフィールドに設定
            eyebrow_to_hide = facial.find_eyebrow_mesh_from_selection(with_blendshape=False)
            if eyebrow_to_hide:
                self.UI.txt_eyebrow_model.setText(eyebrow_to_hide)
            eyebrow_mesh = facial.find_eyebrow_brendshape_mesh_in_scene()
        if eyebrow_mesh:
            self.UI.txt_eyebrow_model.setText(eyebrow_mesh)
        else:
            user_choice = cmds.confirmDialog(title='Import?',
                                             message='P4リポジトリから自動でブレンドシェイプ付き眉のインポートを試みますか?\n' +
                                             '(P4Vのtoolsとteam/3dcg/chr/plyを最新にしておくことをお勧めします)',
                                             button=['OK', 'Cancel'])
            if user_choice == 'OK':
                self.show_import_window(eyebrow_to_hide)
            else:
                return
        # keyのついているサイズ
        size = facial.get_keyed_eyebrow_size(eyebrow_mesh)
        if size:
            self.current_eyebrow_size = size
        self.load_eyebrow_bars(self.UI.layout_eyebrow, eyebrow_mesh)
        return eyebrow_mesh
    
    def update_script_timeslider_job(self, eyebrow_mesh):
        """Mayaのタイムスライダーが移動した時、このツールのスライダーを
        現在のフレームの表情に更新する
        Args:
            eyebrow_mesh (str): 眉メッシュ名
        """
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

    def show_import_window(self, eyebrow_mesh_to_hide):
        """眉のインポートポップアップを表示する
        Args:
            eyebrow_mesh_to_hide (str): インポート後、代わりに非表示にするメッシュ
        """
        # rig班が作っているツールの設定json
        p4_tool_json_path = 'C:/tkgpublic/wiz2/tools/maya/scripts/rig/avatarReferenceTool/data/avatar_collection.json'
        if not os.path.exists(p4_tool_json_path):
            p4_tool_json_path = cmds.fileDialog2(caption='アバターリファレンスツールのavatar_collection.jsonを選択してください',
                                                 fileFilter='*.json', dialogStyle=2, fileMode=1)
            if not p4_tool_json_path:
                return
        f = open(p4_tool_json_path, 'r')
        json_dict = json.load(f)
        eyebrow_dict = json_dict.get('eyebrow', {})
        import_window = ImportWindow(eyebrow_dict, '眉を選択', self, eyebrow_mesh_to_hide)
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
        指定したターゲットシェイプの現在のキーフレームを削除
        Args:
            blendshape (str): ブレンドシェイプ名
            shape (str): ブレンドシェイプのターゲットシェイプ名
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
        指定した眉のターゲットシェイプのキーフレームをすべて削除
        Args:
            blendshape (str): ブレンドシェイプ名
            shape (str): ブレンドシェイプのターゲットシェイプ名
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
            cmds.warning('ブレンドシェイプ付きの眉メッシュがありません')
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
            cmds.warning('main draw_eyebrow_sliders_by_size 眉メッシュがありません')
            return
        if not cmds.objExists(eyebrow_mesh):
            cmds.warning('main draw_eyebrow_sliders_by_size 眉メッシュがありません: ' + eyebrow_mesh)
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
        for button_size in facial.g_eyebrow_sizes:
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
        facial.switch_base_size(eyebrow_mesh, size, facial.g_eyebrow_sizes)
        # 表情キーの移動
        facial.replace_facial_keys_to_another_size(eyebrow_mesh, self.current_eyebrow_size, size)
        # キーを打っていない現在のシェイプウェイトを反映
        facial.switch_weight_to_another_size(eyebrow_mesh, self.current_eyebrow_size, size)
        # スライダーの切替
        self.draw_eyebrow_sliders_by_size(layout, eyebrow_mesh, size)
        self.current_eyebrow_size = size  # 現在の眉サイズ更新

    def on_slider_value_change(self, eyebrow_mesh, eyebrow_sliders, slider_shape, value):
        """眉のブレンドシェイプスライダーが動いた時、眉のブレンドシェイプ、スピンボックス、キーありなしの●印を更新
        Args:
            eyebrow_mesh (str): 眉メッシュ名
            eyebrow_sliders (dict): FacialMotionWindowのeyebrow_slidersディクショナリ
            slider_shape (str): どのターゲットシェイプのスライダーか
            value (int): UI上の表情のブレンド値 (0~100)
        """
        for shape in eyebrow_sliders:
            try:
                spin = eyebrow_sliders[shape]['spin']
                if shape == slider_shape:
                    spin = eyebrow_sliders[shape]['spin']
                    spin.setValue(value)
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
            except Exception:
                cmds.warning('スピンボックス更新失敗')

    def on_spin_value_changed(self, eyebrow_sliders, spin_shape, value):
        """眉のブレンドシェイプスピンボックス（数値入力フィールド）変更時
        Args:
            eyebrow_sliders (_type_): _description_
            spin_shape (_type_): _description_
            value (_type_): _description_
        """
        for shape in eyebrow_sliders:
            if shape == spin_shape:
                try:
                    slider = eyebrow_sliders[shape]['slider']
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
                try:
                    spin = self.eyebrow_sliders[shape]['spin']
                    slider = self.eyebrow_sliders[shape]['slider']
                    cur_value = cmds.getAttr('{0}.{1}'.format(blendshapes[0], shape))
                    slider_value = int(cur_value * 100.0)
                    slider.setValue(slider_value)
                    spin.setValue(slider_value)
                except Exception:
                    cmds.warning('スライダー更新失敗')


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
                    rowPart = csv_row[label_index_dict.get('Face Part')]
                    if face_part == rowPart:
                        btn_img_path = os.path.join(btn_img_folder, csv_row[label_index_dict['Default Icon Image']])
                        face_index = int(csv_row[label_index_dict.get('Face ID')])
                        u = 0
                        v = 0
                        try:
                            u = float(csv_row[int(label_index_dict.get('Translate Frame U'))])
                            v = float(csv_row[int(label_index_dict.get('Translate Frame V'))])
                        except Exception:
                            cmds.warning('Error: UV値の読み込みに失敗しました。')
                        if os.path.exists(btn_img_path):
                            row = int(csv_row[int(label_index_dict.get('Row'))])
                            col = int(csv_row[int(label_index_dict.get('Col'))])
                            top_x = int(csv_row[int(label_index_dict.get('Top X'))])
                            top_y = int(csv_row[int(label_index_dict.get('Top Y'))])
                            width = int(csv_row[int(label_index_dict.get('Button Image Width'))])
                            height = int(csv_row[int(label_index_dict.get('Button Image Height'))])
                            lbl = csv_row[int(label_index_dict.get('Face ID'))]
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
                    cmds.warning('csvのフォーマットが想定外です')

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
        """キーオブジェクトを選択ボタンクリック時実行
        """
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
        if self.UI.chk_select_keynode_mouth.checkState() == QtCore.Qt.CheckState.Checked:
            if not facial.select_key_node(self.UI.txt_face_model.toPlainText(), 'mouth', self.cur_keynode_mouth, True):
                return
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
        """表情横の「全キークリア」ボタン実行時
        Args:
            face_part (str): eye 又は mouth
        """
        facial.clear_facial_key(self.UI.txt_face_model.toPlainText(), face_part)

    def on_export_facial_data(self):
        out_dir = self.UI.txt_out_dir.toPlainText()
        out_dir.replace('\\', '/')
        if not os.path.exists(out_dir):
            cmds.confirmDialog(title='Usage', message='出力フォルダがありません')
            return
        out_file_name_without_ext = self.UI.txt_out_file_name.toPlainText()
        if out_file_name_without_ext.endswith('.json'):
            out_file_name_without_ext = out_file_name_without_ext[0, len(out_file_name_without_ext) - len('.json')]
        export_path = os.path.join(out_dir, out_file_name_without_ext + '.json').replace('\\', '/')
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
        # ----
        # 分割してエクスポートするかどうか
        is_separate_export = False
        first_split_frame_value = None
        # シーン内にtiming_boxがあるか
        timing_box = cmds.ls('timing_box', recursive=True)
        if timing_box:
            # timing_boxのIN, LOOP, OUTキーをチェック
            first_split_frame_value = common.get_first_split_frame()
            if first_split_frame_value:
                is_separate_export = True
            else:
                user_choice = cmds.confirmDialog(title='Warning',
                                                 message='timing_boxはありましたが想定する値のキーが入っていません\n' +
                                                 '続行しますか?',
                                                 button=['OK', 'Cancel'],
                                                 defaultButton='OK',
                                                 cancelButton='Cancel',
                                                 dismissString='Cancel')
                if user_choice == 'Cancel':
                    return
        # ----
        try:
            if is_separate_export:
                # timing_boxのキーフレームで分割する際Timeがフレームのままだとやりやすいのでfpsを1にしてある
                eye_facial_list = facial.get_facial_list(face_mesh, 'eye', self.csv_rows, fps=1)
                mouth_facial_list = facial.get_facial_list(face_mesh, 'mouth', self.csv_rows, fps=1)
                eyebrow_facial_list = facial.get_eyebrow_list(eyebrow_mesh, fps=1)
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
                facial.export_split_animation(out_dir, out_file_name_without_ext, facials, fps)
            else:
                eye_facial_list = facial.get_facial_list(face_mesh, 'eye', self.csv_rows, fps)
                mouth_facial_list = facial.get_facial_list(face_mesh, 'mouth', self.csv_rows, fps)
                eyebrow_facial_list = facial.get_eyebrow_list(eyebrow_mesh, fps)
                facials = {}
                if eye_facial_list:
                    facials['eye'] = eye_facial_list
                    if eye_facial_list[0].get('Time') != 0:
                        cmds.confirmDialog(title='Warning',
                                           message='目の開始フレームにイベントがありません')
                if mouth_facial_list:
                    facials['mouth'] = mouth_facial_list
                    if mouth_facial_list[0].get('Time') != 0:
                        cmds.confirmDialog(title='Warning',
                                           message='口の開始フレームにイベントがありません')
                if eyebrow_facial_list:
                    facials['eyebrow'] = eyebrow_facial_list
                    if eyebrow_facial_list[0].get('Time') != 0:
                        cmds.confirmDialog(title='Warning',
                                           message='眉の開始フレームにイベントがありません')
                if not facials:
                    cmds.confirmDialog(title='Usage', message='表情のキーフレームがありません')
                    return
                json_file = open(export_path, mode='w')
                json.dump(facials, json_file)
                json_file.close()
                print('出力しました: ' + export_path)
            if os.path.exists(out_dir):
                subprocess.Popen('explorer "{}"'.format(os.path.normpath(out_dir)))
        except Exception as ex:
            cmds.error(ex)
            cmds.confirmDialog(title='Error', message='出力失敗')

    def on_import_facial_data(self):
        json_filter = "*.json"
        json_file = cmds.fileDialog2(fileFilter=json_filter, dialogStyle=2, fileMode=1)
        if not json_file:
            print('jsonファイルが選択されませんでした')
            return
        json_file = json_file[0]
        json_file = json_file.replace('\\', '/')
        if not os.path.exists(json_file):
            cmds.confirmDialog(title='Usage',
                               message='UnityのAvatarViewer > 表情切替アニメーションイベント編集' +
                               ' > Json出力 で出力した.jsonファイルを選択してください')
            return
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
                cmds.confirmDialog(title='Usage', message='表情をインポートする対象がありません')
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
        user_choice = cmds.confirmDialog(title='Warning', message='既存の表情は上書きされます\n' +
                                         '続行しますか?',
                                         button=['続行', 'Cancel'])
        if user_choice == 'Cancel':
            return
        if self.UI.btn_tgl_edit_orig_mat.text() == self.btn_tgl_edit_mat_text:
            self.switch_material()
        if not self.reload_eyebrow():
            cmds.warning('眉モーションは読み込まれません')
        # 分割しているモーションには未対応
        try:
            with open(json_file) as json_str:
                json_dict = json.load(json_str)
                if not json_dict:
                    cmds.confirmDialog(title='Usage', message='表情のキーフレームがありません')
                    return
                eye_facial_list = json_dict.get('eye', {})
                mouth_facial_list = json_dict.get('mouth', {})
                eyebrow_facial_list = json_dict.get('eyebrow', {})
                facial.load_facial(face_mesh, 'eye', self.csv_rows, eye_facial_list, fps)
                facial.load_facial(face_mesh, 'mouth', self.csv_rows, mouth_facial_list, fps)
                facial.load_eyebrow_motion(eyebrow_mesh, eyebrow_facial_list, self.current_eyebrow_size, fps)
        except Exception as ex:
            cmds.error(ex)
            cmds.confirmDialog(title='Error', message='読込失敗')

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
        self.save_setting('x', self.x())
        self.save_setting('y', self.y())
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
        # Windowの位置とサイズ
        x = int(self.load_setting('x', 0))
        y = int(self.load_setting('y', 0))
        self.move(x, y)
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
    """インポートダイアログを表示し、メニューで選択したアイテムのパスをインポートするダイアログ
    シーン内の眉モデルにブレンドシェイプがない場合、ブレンドシェイプ付き眉をインポートするときに使う
    Args:
        QtWidgets (_type_): _description_
    """
    def __init__(self, menu_dict, title='Select to Import', parent=None, hide_mesh_after_import=None):
        """ダイアログ初期化
        Args:
            menu_dict (dict<string, string>): keyはメニューに表示する文字列、valueはインポートするファイルパス
            title (str, optional): ダイアログに表示するタイトル文字列. Defaults to 'Select to Import'.
            parent (QMainWindow, optional): 親ウィンドウ（モダルにするのに必要）. Defaults to None.
            hide_mesh_after_import (string, optional): インポート後に非表示にしたいアイテム. Defaults to None.
        """
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
        btn_import.clicked.connect(partial(self.import_item, hide_mesh_after_import))
        layout.addWidget(self.combobox)
        layout.addWidget(btn_import)

    def import_item(self, hide_mesh_after_import):
        reference_path = self.menu_dict[self.combobox.currentText()]
        if not reference_path or not os.path.exists(reference_path):
            cmds.confirmDialog(title='Warning', message='ファイルがありませんでした(P4更新?): ' + str(reference_path))
            return
        try:
            import rig.avatarReferenceTool.commands as avatarReferenceTool
            reload(avatarReferenceTool)
        except Exception as ex:
            # C:\tkgpublic\wiz2\tools\maya\scripts\rig\avatarReferenceTool にある想定
            print(ex)
            cmds.confirmDialog(title='Warning', 
                               message='PerforceリポジトリのavatarReferenceToolが見つかりませんでした\n' +
                               '眉のリファレンスインポートができません\n' +
                               'P4でtools更新してください',
                               button=['OK'])
        try:
            reference_path = self.menu_dict[self.combobox.currentText()]
            print(reference_path)
            # delete
            avatarReferenceTool.delete_ref(ref_name=g_import_eyebrow_namespace)
            # create
            avatarReferenceTool.create_ref(ref_name=g_import_eyebrow_namespace, path=reference_path)
            # 読み込んだ眉メッシュのディスプレイレイヤーが「R」以外のものになっていたら「R」となるように
            display_layers = cmds.ls(type = 'displayLayer')
            for layer in display_layers:
                if layer.startswith('{0}:'.format(g_import_eyebrow_namespace)):
                    cmds.setAttr('{0}.displayType'.format(layer), 2)
            # 元からあった眉の方を非表示
            if hide_mesh_after_import and cmds.objExists(hide_mesh_after_import):
                cmds.hide(hide_mesh_after_import)
            self.parent.reload()
        except Exception as ex:
            self.close()
            print(ex)
            cmds.confirmDialog(title='Error', message='リファレンスできませんでした')
            


def main():
    """Windowの起動
    """
    if cmds.window(g_tool_name, exists=True):
        cmds.deleteUI(g_tool_name)
    ui = FacialMotionWindow()
    ui.show()
