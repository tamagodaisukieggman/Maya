# -*- coding: utf-8 -*-
import os
import subprocess
import maya.cmds as cmds
import maya.mel as mel
import webbrowser
import glob
import time
import tempfile
import sys
from importlib import reload

try:
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtUiTools import QUiLoader
    from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
    import P4
except Exception:
    pass

try:
    from ..common import common
    reload(common)
except Exception as ex:
    print(ex)

g_tool_name = 'Wiz2MotionFBX'
g_tool_version = '2023.12.27'
CURRENT_PATH = os.path.dirname(__file__)
g_default_namespaces = ['UI', 'shared']  # ユーザー指定に関係ないデフォルトネームスペース
g_chara_prefixes = ['p1', 'p2', 'chr']  # 優先順
# ネームスペースがbottomsだったら、キャラのグループの p1:chr:p1_b_sotai01 を非表示にする時などに使うdict
# costumeの場合はt, b, h, (o)非表示。 oは常に非表示。
g_namespace_parts_dict = {'bottoms': 'b', 'hair': 'h', 'shoes': 's', 'tops': 't', 'costume': ''}
# Wizard2のモーション用でシーン内にあるtiming_boxノードのscaleZに
# モーション分割用に入っているIN,LOOP,OUT用のキーフレームがある場合は分割アニメーションをエクスポートする
g_ws_root = 'C:/tkgpublic/wiz2'  # Perforceのワークスペース


def main():
    """Windowの起動
    Returns:
        MotionFBXWindow: ツールウィンドウのインスタンス
    """
    if cmds.window(g_tool_name, exists=True):
        cmds.deleteUI(g_tool_name)
    ui = MotionFBXWindow()
    ui.show()
    return ui


class MotionFBXWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """モーションFBXWindow
    """
    def __init__(self, parent=None):
        super(MotionFBXWindow, self).__init__(parent=parent)
        loader = QUiLoader()
        uiFilePath = os.path.join(CURRENT_PATH, 'wiz2_motion_fbx.ui')
        self.UI = loader.load(uiFilePath)  # QMainWindow
        self.setCentralWidget(self.UI)
        self.setWindowTitle(g_tool_name + '' + g_tool_version)
        self.setObjectName(g_tool_name)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.UI.action_manual.triggered.connect(show_manual)
        scene_path = cmds.file(q=True, sn=True)
        if scene_path:
            # 現在のシーンを元にデフォルト値を設定
            file_dir = os.path.dirname(scene_path)
            self.UI.txt_out_folder.textCursor().insertText(file_dir)
            file_name_without_ext = os.path.splitext(os.path.basename(scene_path))[0]
            self.UI.txt_file_name.textCursor().insertText(file_name_without_ext)
        # リグとキャラのバージョンを記録
        self.UI.btn_add_rig_chr_ver.clicked.connect(self.on_add_rig_chr_ver)
        # リグとキャラのバージョンをチェック
        self.UI.btn_check_rig_chr_ver.clicked.connect(self.on_check_rig_chr_ver)
        # timing_box作成
        self.UI.btn_create_timing_box.clicked.connect(create_timing_box)
        # timing_box更新
        self.UI.btn_update_timing_box.clicked.connect(update_timing_box)
        # フォルダ選択
        self.UI.btn_browse_out_folder.clicked.connect(self.update_out_folder)
        # FBXエクスポート
        self.UI.btn_export_fbx.clicked.connect(self.on_export_motion_fbx)
        # FBXエクスポート（衣装）廃止予定
        self.UI.btn_export_fbx_w_dress.clicked.connect(self.on_export_motion_fbx_w_dress)
        # FBXエクスポート（シーン）廃止予定
        self.UI.btn_export_fbx_scene.clicked.connect(self.on_export_motion_fbx_scene)
        # FBXエクスポート（シーン）New
        self.UI.btn_export_fbx_scene_2.clicked.connect(self.on_export_motion_fbx_scene2)
        # === FBXエクスポート（一括）===
        # 対象フォルダ選択
        self.UI.btn_browse_input_folder.clicked.connect(self.update_input_folder)
        # 対象ファイルフィルタ
        self.UI.chk_filter.toggled.connect(self.on_toggle_check_filter)
        self.UI.txt_file_filter_batch.setText('*_ALL.ma')
        if not self.UI.chk_filter.isChecked():
            self.UI.txt_file_filter_batch.setEnabled(False)
        # 出力先ラジオボタン
        self.UI.rad_in_scene_folder.toggled.connect(self.on_toggle_same_as_scene_radio)
        # 出力フォルダ選択
        self.UI.btn_browse_out_folder_batch.clicked.connect(self.update_out_folder_batch)
        # FBXエクスポート（一括）
        self.frameLayout1 = FrameLayout(self.UI.expand_fbx_export_batch,
                                        self.UI.frame_fbx_export_batch)
        self.UI.btn_export_fbx_batch.clicked.connect(self.on_export_motion_fbx_batch)
        # FBXエクスポート（衣装・一括）
        self.UI.btn_export_fbx_batch_w_dress.clicked.connect(self.on_export_motion_fbx_w_dress_batch)

    def on_add_rig_chr_ver(self):
        """リグとキャラのバージョンを記録
        """
        reference_rig_path = get_reference_rig_path()
        reference_chr_path = get_reference_chr_path()
        if reference_rig_path:
            rig_ver_result = add_rig_ver()
            if not rig_ver_result:
                return
        else:
            rig_ver_result = True  # リファレンスないならそれはそれでOK
        if reference_chr_path:
            chr_ver_result = add_chr_ver()
            if not chr_ver_result:
                return
        else:
            chr_ver_result = True  # リファレンスないならそれはそれでOK
        if rig_ver_result and chr_ver_result:
            cmds.confirmDialog(title='OK',
                               message='リグとキャラの情報をExtra Attrubuteに記載しました',
                               button=['OK'])
        elif rig_ver_result:
            cmds.confirmDialog(title='OK',
                               message='リグの情報をExtra Attrubuteに記載しました',
                               button=['OK'])
        elif chr_ver_result:
            cmds.confirmDialog(title='OK',
                               message='キャラの情報をExtra Attrubuteに記載しました',
                               button=['OK'])

    def on_check_rig_chr_ver(self):
        """リグとキャラのバージョンをチェック
        """
        rig_ver_result = check_rig_ver()
        chr_ver_result = check_chr_ver()
        if rig_ver_result and chr_ver_result:
            cmds.confirmDialog(title='OK',
                               message='リファレンスのリグとキャラのバージョンはシーン内の記録と同じです',
                               button=['OK'])
        elif rig_ver_result:
            cmds.confirmDialog(title='OK',
                               message='リファレンスのリグのバージョンはシーン内の記録と同じです',
                               button=['OK'])
        elif chr_ver_result:
            cmds.confirmDialog(title='OK',
                               message='リファレンスのキャラのバージョンはシーン内の記録と同じです',
                               button=['OK'])

    def validate_scene_export(self):
        """現在のシーン「FBXエクスポート」用Validation
        """
        txt_out_folder = self.UI.txt_out_folder.toPlainText()
        txt_out_folder = txt_out_folder.replace('\\', '/')
        txt_file_name = self.UI.txt_file_name.toPlainText()
        if not os.path.isdir(txt_out_folder):
            cmds.confirmDialog(title='Warning', message='出力フォルダが存在しません\n' +
                               txt_out_folder,
                               button=['OK'])
            return False
        if not txt_file_name:
            cmds.confirmDialog(title='Warning', message='出力ファイル名を指定してください\n' +
                               txt_out_folder,
                               button=['OK'])
            return False
        # 保存状態
        not_saved = cmds.file(q=True, modified=True)
        if not_saved:
            user_choice = cmds.confirmDialog(title='Confirm',
                                             message='シーンは保存されていません\n' +
                                             '実行するとシーンは大きく変更されます\n' +
                                             'エクスポート実行前にシーンを保存しますか?',
                                             button=['保存', '保存しないで続行', 'Cancel'],
                                             defaultButton='保存',
                                             cancelButton='Cancel',
                                             dismissString='Cancel')
            if user_choice == 'Cancel':
                return False
            elif user_choice == '保存':
                secene_path = cmds.file(q=True, sn=True)
                is_writable = os.access(secene_path, os.W_OK)
                if not is_writable:
                    cmds.confirmDialog(title=u'確認',
                                       message='シーンが読み取り専用です\n' +
                                       'Perforceでチェックアウトしていますか?\n' +
                                       'シーンが保存できないのでキャンセルします',
                                       button=['OK'])
                    return False
                cmds.file(save=True)
        return True

    def on_export_motion_fbx(self):
        """「FBXエクスポート」ボタン実行
        """
        if not self.validate_scene_export():
            return
        txt_out_folder = self.UI.txt_out_folder.toPlainText()
        txt_out_folder = txt_out_folder.replace('\\', '/')
        txt_file_name = self.UI.txt_file_name.toPlainText()
        is_fix_root_to_origin = self.UI.chk_fix_root_to_origin.isChecked()
        error_msg_dict = {}
        exported = export_motion_fbx(txt_out_folder,
                                     txt_file_name,
                                     remove_all=False,
                                     is_fix_root_to_origin=is_fix_root_to_origin,
                                     check_version=False,
                                     show_popup=True,
                                     error_msg_dict=error_msg_dict,
                                     is_with_dress=False,
                                     is_scene=False,
                                     is_embed_media=False)
        self.close()
        # エクスポート後フォルダを開く
        if exported and self.UI.chk_open_out_folder.isChecked():
            if os.path.exists(txt_out_folder):
                subprocess.Popen('explorer "{}"'.format(os.path.normpath(txt_out_folder)))
        # エクスポート後のシーンをそのまま開いておく　のチェックがオフなら空のシーンを開く（上書き防止）
        if exported and not self.UI.chk_keep_edited_scene_open.isChecked():
            cmds.file(new=True, f=True)
        # ErrorやWarning等があったら知らせる
        if error_msg_dict:
            now = time.localtime()
            timestamp = time.strftime('%Y%m%d%H%M', now)
            log_file_path = os.path.join(tempfile.gettempdir(), 'MotionFBXExportErrorLog_' + timestamp + '.csv')
            with open(log_file_path, mode='w+') as f:
                f.write(time.strftime('%Y/%m/%d', now) + '\n')
                for scene_path in error_msg_dict:
                    f.write(scene_path + ',' + ','.join(error_msg_dict[scene_path]) + '\n')
            webbrowser.open(log_file_path)

    def on_export_motion_fbx_batch(self):
        """「FBXエクスポート（一括）」ボタン実行
        """
        print("「FBXエクスポート（一括）」ボタン実行")
        is_in_scene_folder = self.UI.rad_in_scene_folder.isChecked()
        is_check_version = self.UI.rad_check_version.isChecked()
        is_fix_root_to_origin = self.UI.chk_fix_root_to_origin_batch.isChecked()
        input_folder = self.UI.txt_input_folder.toPlainText()
        is_filter = self.UI.chk_filter.isChecked()
        search_str = self.UI.txt_file_filter_batch.toPlainText()
        is_open_out_folder_batch = self.UI.chk_open_out_folder_batch.isChecked()
        show_popup = False
        is_with_dress = False
        is_scene = False
        is_embed_media = False
        if is_check_version:
            if not validate_p4(show_popup=True):
                return
        # 対象フォルダ確認
        if not os.path.exists(input_folder):
            if not self.update_input_folder():
                return
            input_folder = self.UI.txt_input_folder.toPlainText()
        input_folder = input_folder.replace('\\', '/')
        # 対象ファイルフィルタ
        if is_filter:
            if not search_str:
                search_str = '*.ma'
            elif not search_str.endswith('.ma'):
                search_str += '.ma'
        else:
            search_str = '*.ma'
        try:
            # Validation用にマヤシーンをリスト
            # ここでのリストの仕方とexport_motion_fbx_batchでのリストの仕方は同じであること
            # （パラメータで長い文字列約8000字以上を渡せない為）
            ma_files = [os.path.join(dir, f) for dir, dn, filenames in os.walk(input_folder) for f in glob.glob(dir + '/' + search_str)]
        except Exception:
            cmds.warning('フィルタは正規表現にしてください')
            return
        if not ma_files:
            cmds.confirmDialog(title='Info',
                               message='対象の.maシーンを見つけられませんでした',
                               button=['OK'])
            return
        # パスのスラッシュ修正
        fixed_slashes = []
        for file_path in ma_files:
            fixed_slashes.append(file_path.replace('\\', '/'))
        ma_files = fixed_slashes
        # 出力先フォルダを指定にチェックが入っている場合は出力先フォルダ確認
        out_folder = ''
        if not is_in_scene_folder:
            out_folder = self.UI.txt_out_folder_batch.toPlainText()
            if not os.path.isdir(out_folder):
                if not self.update_out_folder_batch():
                    return False
                out_folder = self.UI.txt_out_folder_batch.toPlainText()
        # 対象ファイルを表示してユーザーにこれで良いか確認する
        user_choice = cmds.confirmDialog(title='Confirm',
                                         message='以下のシーンをFBXエクスポートします\n' +
                                         'よろしいですか?\n' + '\n'.join(ma_files),
                                         button=['OK', 'Cancel'],
                                         defaultButton='OK',
                                         cancelButton='Cancel',
                                         dismissString='Cancel')
        if user_choice == 'Cancel':
            return
        # _ALLを取るかどうか
        remove_all = False
        if found_all_in_paths(ma_files):
            user_choice = cmds.confirmDialog(title='Confirm',
                                             message='「_ALL」で終わっているシーンがありました\n' +
                                             'シーン名でFBXを書き出しますが、_ALLを取りますか?',
                                             button=['_ALLを取る', 'そのまま', 'Cancel'],
                                             defaultButton='_ALLを取る',
                                             cancelButton='Cancel',
                                             dismissString='Cancel')
            if user_choice == 'Cancel':
                return
            elif user_choice == '_ALLを取る':
                remove_all = True
        if ma_files:
            try:
                import subprocess
                # Note: batch mode escapes single back slash!
                input_folder = input_folder.replace("\\", "/")
                out_folder = out_folder.replace("\\", "/")
                search_str = search_str.replace("\\", "/")
                module_root = os.path.dirname(os.path.dirname(__file__))
                os.chdir(module_root)
                params = [("\'" + input_folder + "\'"),
                          ("\'" + search_str + "\'"),
                          ("\'" + str(is_in_scene_folder) + "\'"),
                          ("\'" + out_folder + "\'"),
                          ("\'" + str(remove_all) + "\'"),
                          ("\'" + str(is_fix_root_to_origin) + "\'"),
                          ("\'" + str(is_check_version) + "\'"),
                          ("\'" + str(is_open_out_folder_batch) + "\'"),
                          ("\'" + str(show_popup) + "\'"),
                          ("\'" + str(is_with_dress) + "\'"),
                          ("\'" + str(is_scene) + "\'"),
                          ("\'" + str(is_embed_media) + "\'")]
                params = list(map(str, params))
                paramStr = ','.join(params)
                commandStr = '\"C:\\Program Files\\Autodesk\\Maya2022\\bin\\mayabatch.exe\" ' \
                             '-command \"python(\"\"import motion_fbx.main;' \
                             'motion_fbx.main.export_motion_fbx_batch(' + paramStr + ')\"\")\" '
                subprocess.Popen(commandStr, start_new_session=True)
            except Exception as e:
                print("Error " + __file__ + " line 225: " + str(e))
        self.close()
        cmds.warning('コマンドプロンプトは処理が終わってからクローズしてください')

    def on_export_motion_fbx_w_dress(self):
        """「FBXエクスポート(衣装)」ボタン実行
        衣装込みでexport_motion_fbxする
        ユーザーが指定した出力フォルダの中に「DressPreview」フォルダを作りエクスポートする
        衣装書き出しの時はEmbed MediaオプションをONにする
        """
        if not self.validate_scene_export():
            return
        txt_out_folder = self.UI.txt_out_folder.toPlainText()
        txt_out_folder = txt_out_folder.replace('\\', '/')
        if os.path.exists(txt_out_folder):
            txt_out_folder += '/DressPreview'
            if not os.path.exists(txt_out_folder):
                os.makedirs(txt_out_folder)
        txt_file_name = self.UI.txt_file_name.toPlainText()
        is_fix_root_to_origin = self.UI.chk_fix_root_to_origin.isChecked()
        error_msg_dict = {}
        exported = export_motion_fbx(txt_out_folder,
                                     txt_file_name,
                                     remove_all=False,
                                     is_fix_root_to_origin=is_fix_root_to_origin,
                                     check_version=False,
                                     show_popup=True,
                                     error_msg_dict=error_msg_dict,
                                     is_with_dress=True,
                                     is_scene=False,
                                     is_embed_media=True)
        self.close()
        # エクスポート後フォルダを開く
        if exported and self.UI.chk_open_out_folder.isChecked():
            if os.path.exists(txt_out_folder):
                subprocess.Popen('explorer "{}"'.format(os.path.normpath(txt_out_folder)))
        # エクスポート後のシーンをそのまま開いておく　のチェックがオフなら空のシーンを開く（上書き防止）
        if exported and not self.UI.chk_keep_edited_scene_open.isChecked():
            cmds.file(new=True, f=True)
        # ErrorやWarning等があったら知らせる
        if error_msg_dict:
            now = time.localtime()
            timestamp = time.strftime('%Y%m%d%H%M', now)
            log_file_path = os.path.join(tempfile.gettempdir(), 'MotionFBXExportErrorLog_' + timestamp + '.csv')
            with open(log_file_path, mode='w+') as f:
                f.write(time.strftime('%Y/%m/%d', now) + '\n')
                for scene_path in error_msg_dict:
                    f.write(scene_path + ',' + ','.join(error_msg_dict[scene_path]) + '\n')
            webbrowser.open(log_file_path)

    def on_export_motion_fbx_scene(self):
        """「FBXエクスポート(シーン)」ボタン実行
        衣装込みでexport_motion_fbxする
        ユーザーが指定した出力フォルダの中に「ScenePreview」フォルダを作りエクスポートする
        Embed MediaオプションをONにする
        """
        if not self.validate_scene_export():
            return
        txt_out_folder = self.UI.txt_out_folder.toPlainText()
        txt_out_folder = txt_out_folder.replace('\\', '/')
        if os.path.exists(txt_out_folder):
            txt_out_folder += '/ScenePreview'
            if not os.path.exists(txt_out_folder):
                os.makedirs(txt_out_folder)
        txt_file_name = self.UI.txt_file_name.toPlainText()
        is_fix_root_to_origin = self.UI.chk_fix_root_to_origin.isChecked()
        error_msg_dict = {}
        exported = export_motion_fbx(txt_out_folder,
                                     txt_file_name,
                                     remove_all=False,
                                     is_fix_root_to_origin=is_fix_root_to_origin,
                                     check_version=False,
                                     show_popup=True,
                                     error_msg_dict=error_msg_dict,
                                     is_with_dress=True,
                                     is_scene=True,
                                     is_embed_media=True)
        self.close()
        # エクスポート後フォルダを開く
        if exported and self.UI.chk_open_out_folder.isChecked():
            if os.path.exists(txt_out_folder):
                subprocess.Popen('explorer "{}"'.format(os.path.normpath(txt_out_folder)))
        # エクスポート後のシーンをそのまま開いておく　のチェックがオフなら空のシーンを開く（上書き防止）
        if exported and not self.UI.chk_keep_edited_scene_open.isChecked():
            cmds.file(new=True, f=True)
        # ErrorやWarning等があったら知らせる
        if error_msg_dict:
            now = time.localtime()
            timestamp = time.strftime('%Y%m%d%H%M', now)
            log_file_path = os.path.join(tempfile.gettempdir(), 'MotionFBXExportErrorLog_' + timestamp + '.csv')
            with open(log_file_path, mode='w+') as f:
                f.write(time.strftime('%Y/%m/%d', now) + '\n')
                for scene_path in error_msg_dict:
                    f.write(scene_path + ',' + ','.join(error_msg_dict[scene_path]) + '\n')
            webbrowser.open(log_file_path)

    def on_export_motion_fbx_scene2(self):
        """「FBXエクスポート(シーン)2」ボタン実行
        ①素体のメッシュの不要部分t,b,oをハイド
        ②embed_mediaにチェックを入れてテクスチャ込みのfbxを出力
        ・シーン内の全てをベイク
        ・小数フレームカット
        ・オイラーフィルター
        https://cg415.slack.com/archives/C03CKCB1KRC/p1697549062256139
        ユーザーが指定した出力フォルダの中に「ScenePreview」フォルダを作りエクスポートする
        """
        if not self.validate_scene_export():
            return
        scene_path = cmds.file(q=True, sn=True)
        error_msg_dict = {}
        txt_out_folder = self.UI.txt_out_folder.toPlainText()
        txt_out_folder = txt_out_folder.replace('\\', '/')
        if os.path.exists(txt_out_folder):
            txt_out_folder += '/ScenePreview'
            if not os.path.exists(txt_out_folder):
                os.makedirs(txt_out_folder)
        txt_file_name = self.UI.txt_file_name.toPlainText()
        # t, b, oを非表示にする
        export_root = get_export_chara_root()
        if not export_root:
            add_to_dict(scene_path, 'Warning: エクスポートルートのキャラが見つかりませんでした', error_msg_dict)
        else:
            export_root_children = cmds.listRelatives(export_root, children=True, fullPath=True)
            for child in export_root_children:
                for part in ['t', 'b', 'o']:
                    hide_part = '{0}_{1}_'.format(export_root, part)
                    if child.find(hide_part) > -1:
                        cmds.hide(child)
        # ベイクする
        attrs_to_bake = ['rotateX', 'rotateY', 'rotateZ',
                        'translateX', 'translateY', 'translateZ',
                        'scaleX', 'scaleY', 'scaleZ']
        # アーティストさん指定の選択方法なのでなるべく変更しない
        cmds.SelectAll()
        cmds.SelectHierarchy()
        all_objects = cmds.ls(sl=True)
        if not all_objects:
            cmds.confirmDialog(title='Usage', message='エクスポートするモデルがありません (エクスポートするモデルが非表示になっていませんか?)', button=['OK'])
            return
        else:
            time_range_start = cmds.playbackOptions(q=True, minTime=True)
            time_range_end = cmds.playbackOptions(q=True, maxTime=True)
            cmds.bakeResults(all_objects, simulation=True, t=(time_range_start,time_range_end), sampleBy=1, oversamplingRate=1,
                            disableImplicitControl=True, preserveOutsideKeys=True, sparseAnimCurveBake=False,
                            removeBakedAttributeFromLayer=False, removeBakedAnimFromLayer=False, bakeOnOverrideLayer=False,
                            minimizeRotation=True, controlPoints=False, attribute=attrs_to_bake)
            # 中間のキーをクリア
            cmds.selectKey(unsnappedKeys=True, time=(time_range_start,time_range_end), hierarchy='none', controlPoints=False)
            cmds.cutKey(animation='keys', clear=True)
            # Euler Filterをかける
            cmds.filterCurve(all_objects)
        # コンストレイントを削除
        if self.UI.chk_is_model_reference.isChecked():
            # アーティスト指定の方法
            # リファレンスでないもの全削除(コンストレイントを消す目的)
            cmds.select(all_objects)
            cmds.delete()
            all_objects = update_list(all_objects)
            if not all_objects and self.UI.chk_keep_edited_scene_open.isChecked():
                cmds.confirmDialog(title='Usage', message='シーンを開きなおし「モデルはリファレンス」のチェックを外して実行してみてください', button=['OK'])
        else:
            # リファレンスでない場合の対応
            delete_constraints(delete_handle_obj=True)
            # スキンのないjointがあると3Dビューアでプレビューがでないっぽい
            root_joints = get_root_joints_in_scene()
            for rootj in root_joints:
                if not joint_has_skin(rootj):
                    cmds.delete(rootj)
        # キャラモデルのリファレンスをインポート
        if not import_main_chara_reference():
            add_to_dict(scene_path, 'Error: キャラモデルのリファレンスのインポートに失敗しました', error_msg_dict)
        # geo_grpをグループから出す
        try:
            geo_grp = cmds.ls('*:geo_grp')
        except Exception:
            geo_grp = cmds.ls('geo_grp')
        if geo_grp:
            try:
                cmds.parent(geo_grp, world=True)
            except Exception as ex:
                print(ex)
        # rigを削除
        rig_node = cmds.ls('*:rig')
        if rig_node:
            cmds.delete(rig_node)
        # getaなし
        if self.UI.chk_no_geta.isChecked():
            geta_nodes = cmds.ls('*:geta_grp')
            cmds.select(geta_nodes, hi=True)
            geta_nodes = cmds.ls(sl=True)
            for geta_node in geta_nodes:
                cmds.setAttr('{}.visibility'.format(geta_node), lock=False)
                cmds.setAttr('{}.visibility'.format(geta_node), False)
        # レイヤーが削除できないのでリファレンスをdefaultLayerに移動
        all_objects = update_list(all_objects)
        all = cmds.listRelatives(all_objects, ad=True, fullPath=True)
        belong_layers = cmds.listConnections(all, type='displayLayer')
        if belong_layers:
            belong_layers = list(set(belong_layers))
            for layer in belong_layers:
                member = cmds.editDisplayLayerMembers(layer, query=True, fullNames=True)
                cmds.editDisplayLayerMembers('defaultLayer', member)
        # ディスプレイレイヤーを削除
        displayLayers = cmds.ls(type='displayLayer')
        for layer in displayLayers:
            if layer.find('defaultLayer') == -1:
                cmds.delete(layer)
        cmds.SelectAll()
        roots = cmds.ls(sl=True)
        export_selection = []
        for root in roots:
            if root.find('hair_sim') == -1:
                export_selection.append(root)
        if not export_selection:
            add_to_dict(scene_path, 'Warning: エクスポートするモデルがありません', error_msg_dict)
        else:
            cmds.select(export_selection)
            try:
                # この処理でのFBXプリセットを設定する（Maya本体のプリセットは変わらない）
                # Embed Mediaでエクスポート
                preset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.',
                                            'wizard2_motion_embed_media.fbxexportpreset')).replace('\\', '/')
                mel.eval('FBXLoadExportPresetFile -f "{}"'.format(preset_path))
                cmds.select(export_selection, hierarchy=True)
                export_path = txt_out_folder + "/" + txt_file_name + ".fbx"
                mel.eval('FBXExport -f "{0}" -s'.format(export_path))
            except Exception as ex:
                error_msg_dict[scene_path] = str(ex)
            print('FBXを出力しました: ' + export_path)
            # エクスポート後フォルダを開く
            if self.UI.chk_open_out_folder.isChecked():
                if os.path.exists(txt_out_folder):
                    subprocess.Popen('explorer "{}"'.format(os.path.normpath(txt_out_folder)))
        self.close()
        # エクスポート後のシーンをそのまま開いておく　のチェックがオフなら空のシーンを開く（上書き防止）
        if not self.UI.chk_keep_edited_scene_open.isChecked():
            cmds.file(new=True, f=True)
        # ErrorやWarning等があったら知らせる
        if error_msg_dict:
            now = time.localtime()
            timestamp = time.strftime('%Y%m%d%H%M', now)
            log_file_path = os.path.join(tempfile.gettempdir(), 'MotionFBXExportErrorLog_' + timestamp + '.csv')
            with open(log_file_path, mode='w+') as f:
                f.write(time.strftime('%Y/%m/%d', now) + '\n')
                for scene_path in error_msg_dict:
                    f.write(scene_path + ',' + ','.join(error_msg_dict[scene_path]) + '\n')
            webbrowser.open(log_file_path)

    def on_export_motion_fbx_w_dress_batch(self):
        """「FBXエクスポート（衣装・一括）」ボタン実行
        """
        is_in_scene_folder = self.UI.rad_in_scene_folder.isChecked()
        is_check_version = self.UI.rad_check_version.isChecked()
        is_fix_root_to_origin = self.UI.chk_fix_root_to_origin_batch.isChecked()
        input_folder = self.UI.txt_input_folder.toPlainText()
        is_filter = self.UI.chk_filter.isChecked()
        search_str = self.UI.txt_file_filter_batch.toPlainText()
        is_open_out_folder_batch = self.UI.chk_open_out_folder_batch.isChecked()
        show_popup = False
        is_with_dress = True
        is_scene = False
        is_embed_media = True
        if is_check_version:
            if not validate_p4(show_popup=True):
                return
        # 対象フォルダ確認
        if not os.path.exists(input_folder):
            if not self.update_input_folder():
                return
            input_folder = self.UI.txt_input_folder.toPlainText()
        input_folder = input_folder.replace('\\', '/')
        # 対象ファイルフィルタ
        if is_filter:
            if not search_str:
                search_str = '*.ma'
            elif not search_str.endswith('.ma'):
                search_str += '.ma'
        else:
            search_str = '*.ma'
        try:
            # Validation用にマヤシーンをリスト
            # ここでのリストの仕方とexport_motion_fbx_batchでのリストの仕方は同じであること
            # （パラメータで長い文字列約8000字以上を渡せない為）
            ma_files = [os.path.join(dir, f) for dir, dn, filenames in os.walk(input_folder) for f in glob.glob(dir + '/' + search_str)]
        except Exception:
            cmds.warning('フィルタは正規表現にしてください')
            return
        if not ma_files:
            cmds.confirmDialog(title='Info',
                               message='対象の.maシーンを見つけられませんでした',
                               button=['OK'])
            return
        # パスのスラッシュ修正
        fixed_slashes = []
        for file_path in ma_files:
            fixed_slashes.append(file_path.replace('\\', '/'))
        ma_files = fixed_slashes
        # 出力先フォルダを指定にチェックが入っている場合は出力先フォルダ確認
        out_folder = ''
        if not is_in_scene_folder:
            out_folder = self.UI.txt_out_folder_batch.toPlainText()
            if not os.path.isdir(out_folder):
                if not self.update_out_folder_batch():
                    return False
                out_folder = self.UI.txt_out_folder_batch.toPlainText()
        # 対象ファイルを表示してユーザーにこれで良いか確認する
        user_choice = cmds.confirmDialog(title='Confirm',
                                         message='以下のシーンをFBXエクスポートします\n' +
                                         'よろしいですか?\n' + '\n'.join(ma_files),
                                         button=['OK', 'Cancel'],
                                         defaultButton='OK',
                                         cancelButton='Cancel',
                                         dismissString='Cancel')
        if user_choice == 'Cancel':
            return
        # _ALLを取るかどうか
        remove_all = False
        if found_all_in_paths(ma_files):
            user_choice = cmds.confirmDialog(title='Confirm',
                                             message='「_ALL」で終わっているシーンがありました\n' +
                                             'シーン名でFBXを書き出しますが、_ALLを取りますか?',
                                             button=['_ALLを取る', 'そのまま', 'Cancel'],
                                             defaultButton='_ALLを取る',
                                             cancelButton='Cancel',
                                             dismissString='Cancel')
            if user_choice == 'Cancel':
                return
            elif user_choice == '_ALLを取る':
                remove_all = True
        if ma_files:
            try:
                import subprocess
                # Note: batch mode escapes single back slash!
                out_folder = out_folder.replace("\\", "/")
                search_str = search_str.replace("\\", "/")
                module_root = os.path.dirname(os.path.dirname(__file__))
                os.chdir(module_root)
                params = [("\'" + input_folder + "\'"),
                          ("\'" + search_str + "\'"),
                          ("\'" + str(is_in_scene_folder) + "\'"),
                          ("\'" + out_folder + "\'"),
                          ("\'" + str(remove_all) + "\'"),
                          ("\'" + str(is_fix_root_to_origin) + "\'"),
                          ("\'" + str(is_check_version) + "\'"),
                          ("\'" + str(is_open_out_folder_batch) + "\'"),
                          ("\'" + str(show_popup) + "\'"),
                          ("\'" + str(is_with_dress) + "\'"),
                          ("\'" + str(is_scene) + "\'"),
                          ("\'" + str(is_embed_media) + "\'")]
                params = list(map(str, params))
                paramStr = ','.join(params)
                commandStr = '\"C:\\Program Files\\Autodesk\\Maya2022\\bin\\mayabatch.exe\" ' \
                             '-command \"python(\"\"import motion_fbx.main;' \
                             'motion_fbx.main.export_motion_fbx_batch(' + paramStr + ')\"\")\" '
                subprocess.Popen(commandStr, start_new_session=True)
            except Exception as e:
                print("Error " + __file__ + " line 225: " + str(e))
        self.close()
        cmds.warning('コマンドプロンプトは処理が終わってからクローズしてください')

    def update_out_folder(self):
        """出力先の「フォルダ選択」ボタン実行
        フォルダ選択ダイアログを出し、出力フォルダフィールドにパスを設定
        """
        scene_path = cmds.file(q=True, sn=True)
        file_dir = ''
        if scene_path:
            file_dir = os.path.dirname(scene_path)
        export_folder = cmds.fileDialog2(caption='出力先のフォルダを選択してください',
                                         fileMode=3, dialogStyle=2,
                                         okCaption='選択', dir=file_dir)
        if export_folder:
            self.UI.txt_out_folder.clear()
            self.UI.txt_out_folder.textCursor().insertText(export_folder[0])
            # TODO: カーソルを最後に移動したいが何故かできない
            self.UI.txt_out_folder.textCursor().movePosition(QtGui.QTextCursor.End)
            return True
        return False

    def update_out_folder_batch(self):
        """バッチの出力先の「フォルダ選択」ボタン実行
        フォルダ選択ダイアログを出し、出力フォルダフィールドにパスを設定
        """
        scene_path = cmds.file(q=True, sn=True)
        file_dir = ''
        if scene_path:
            file_dir = os.path.dirname(scene_path)
        export_folder = cmds.fileDialog2(caption='出力先のフォルダを選択してください',
                                         fileMode=3, dialogStyle=2,
                                         okCaption='選択', dir=file_dir)
        if export_folder:
            self.UI.txt_out_folder_batch.clear()
            self.UI.txt_out_folder_batch.textCursor().insertText(export_folder[0])
            # TODO: カーソルを最後に移動したいが何故かできない
            self.UI.txt_out_folder_batch.textCursor().movePosition(QtGui.QTextCursor.End)
            return True
        return False

    def update_input_folder(self):
        """対象フォルダの「フォルダ選択」ボタン実行
        フォルダ選択ダイアログを出し、対象フォルダフィールドにパスを設定
        """
        scene_path = cmds.file(q=True, sn=True)
        file_dir = ''
        if scene_path:
            file_dir = os.path.dirname(scene_path)
        input_folder = cmds.fileDialog2(caption='Mayaシーンの入っている対象フォルダを選択してください',
                                        fileMode=3, dialogStyle=2,
                                        okCaption='選択', dir=file_dir)
        if input_folder:
            self.UI.txt_input_folder.clear()
            self.UI.txt_input_folder.textCursor().insertText(input_folder[0])
            # TODO: カーソルを最後に移動したいが何故かできない
            self.UI.txt_input_folder.textCursor().movePosition(QtGui.QTextCursor.End)
            return True
        return False

    def on_toggle_check_filter(self, *args):
        is_check_filter = args[0]
        if is_check_filter:
            self.UI.txt_file_filter_batch.setEnabled(True)
        else:
            self.UI.txt_file_filter_batch.setEnabled(False)

    def on_toggle_same_as_scene_radio(self, *args):
        """「シーンと同じフォルダ」ラジオボタンがONなら一括の出力フォルダをグレーアウトし
        OFFなら一括の出力フォルダを有効にする。
        """
        is_same_as_scene = args[0]
        if is_same_as_scene:
            self.UI.lbl_out_folder_batch.setEnabled(False)
            self.UI.txt_out_folder_batch.setEnabled(False)
            self.UI.btn_browse_out_folder_batch.setEnabled(False)
        else:
            self.UI.lbl_out_folder_batch.setEnabled(True)
            self.UI.txt_out_folder_batch.setEnabled(True)
            self.UI.btn_browse_out_folder_batch.setEnabled(True)


class FrameLayout(object):
    """QTDesignerでFrameLayoutを作るクラス
    """
    def __init__(self, titleBar, frame):
        self.titleBar = titleBar    # 開閉ボタン
        self.frame = frame          # 開閉するウィジェット
        self.collapse = False       # 開閉している状態フラグ
        self.setSignals()           # シグナルをセット

    def setSignals(self):
        """シグナルを設定する
        """
        self.titleBar.clicked.connect(self.setCollapse)

    def setCollapse(self):
        """フレームを開閉するアクション
        """
        # 現在のステータスを反転する
        self.collapse = not self.collapse
        # フレームのビジビリティを変更する
        self.frame.setHidden(self.collapse)

        # 開閉状況に合わせてアロータイプを変更する
        if self.collapse:
            # 閉じている時は右に向ける
            self.titleBar.setArrowType(QtCore.Qt.RightArrow)
        else:
            # 開いている時は下へ向ける
            self.titleBar.setArrowType(QtCore.Qt.DownArrow)


def found_all_in_paths(paths):
    for path in paths:
        file_name_without_ext = os.path.splitext(os.path.basename(path))[0]
        if file_name_without_ext.endswith('_ALL'):
            return True
    else:
        return False


def add_rig_ver():
    """シーン内のリファレンスのリグのP4の日付をエクスポートRootの
    Extra AttrubuteのRig_P4_Timestampアトリビュートに書き込む
    Returns:
        bool: 追加・更新できたらTrue
    """
    export_root = get_export_chara_root()
    if not export_root:
        cmds.warning('モデルグループを見つけられませんでした')
        return False
    reference_rig_path = get_reference_rig_path()
    if not reference_rig_path:
        cmds.confirmDialog(title='Info',
                           message='リグのリファレンスを見つけられませんでした',
                           button=['OK'])
        cmds.warning('リグのリファレンスを見つけられませんでした')
        return False
    p4_filelog = get_p4_filelog(reference_rig_path, True)
    if not p4_filelog:
        return False
    try:
        time = p4_filelog['rev_time']
    except Exception as ex:
        cmds.warning(ex)
        return False
    extra_attrs = get_rig_chr_info()
    p4_filelog = get_p4_filelog(reference_rig_path, show_popup=True)
    if not p4_filelog:
        cmds.confirmDialog(title='Info',
                           message='リグのリファレンスの日付の取得ができませんでした',
                           button=['OK'])
        return False
    cmds.select(export_root)
    if extra_attrs.get('rig_rev_time') and p4_filelog:
        if str(extra_attrs['rig_rev_time']) == str(p4_filelog['rev_time']):
            # 前回と同じならあえて更新しない
            return True
        user_choice = cmds.confirmDialog(title='Confirm',
                                         message='リファレンスのリグのバージョンはシーン内の記録と違いました\n' +
                                         '前回: ' + str(extra_attrs['rig_rev_time']) +
                                         '\n今回: ' + str(p4_filelog['rev_time']) +
                                         '\n更新しますか？',
                                         button=['OK', 'Cancel'],
                                         defaultButton='OK',
                                         cancelButton='Cancel',
                                         dismissString='Cancel')
        if user_choice == 'Cancel':
            return False
    # ====== Extra Attrubuteがない場合は用意する ======
    try:
        cmds.getAttr('{}.Rig_P4_Timestamp'.format(export_root))
    except Exception:
        cmds.addAttr(export_root, ln='Rig_P4_Timestamp', dt='string')
    # ====== アトリビュート記載 ======
    cmds.setAttr('{}.Rig_P4_Timestamp'.format(export_root), time, type='string')
    return True


def add_chr_ver():
    """シーン内のリファレンスのキャラのP4の日付をエクスポートRootの
    Extra AttrubuteのChr_P4_Timestampアトリビュートに書き込む
    Returns:
        bool: 追加・更新できたらTrue
    """
    export_root = get_export_chara_root()
    if not export_root:
        cmds.warning('モデルグループを見つけられませんでした')
        return False
    reference_chr_path = get_reference_chr_path()
    if not reference_chr_path:
        cmds.confirmDialog(title='Info',
                           message='キャラのリファレンスを見つけられませんでした',
                           button=['OK'])
        cmds.warning('キャラのリファレンスを見つけられませんでした')
        return False
    p4_filelog = get_p4_filelog(reference_chr_path, True)
    if not p4_filelog:
        return False
    try:
        time = p4_filelog['rev_time']
    except Exception as ex:
        cmds.warning(ex)
        return False
    extra_attrs = get_rig_chr_info()
    if not reference_chr_path:
        cmds.confirmDialog(title='Info',
                           message='キャラのリファレンスがありません',
                           button=['OK'])
    p4_filelog = get_p4_filelog(reference_chr_path, show_popup=True)
    if not p4_filelog:
        cmds.confirmDialog(title='Info',
                           message='キャラのリファレンスの日付の取得ができませんでした',
                           button=['OK'])
        return False
    cmds.select(export_root)
    if extra_attrs.get('chr_rev_time') and p4_filelog:
        if str(extra_attrs['chr_rev_time']) == str(p4_filelog['rev_time']):
            # 前回と同じならあえて更新しない
            return True
        user_choice = cmds.confirmDialog(title='Confirm',
                                         message='リファレンスのキャラのバージョンはシーン内の記録と違いました\n' +
                                         '前回: ' + str(extra_attrs['chr_rev_time']) +
                                         '\n今回: ' + str(p4_filelog['rev_time']) +
                                         '\n更新しますか？',
                                         button=['OK', 'Cancel'],
                                         defaultButton='OK',
                                         cancelButton='Cancel',
                                         dismissString='Cancel')
        if user_choice == 'Cancel':
            return False
    # ====== Extra Attrubuteがない場合は用意する ======
    try:
        cmds.getAttr('{}.Chr_P4_Timestamp'.format(export_root))
    except Exception:
        cmds.addAttr(export_root, ln='Chr_P4_Timestamp', dt='string')
    # ====== アトリビュート記載 ======
    cmds.setAttr('{}.Chr_P4_Timestamp'.format(export_root), time, type='string')
    return True


def has_rig_ver_in_scene():
    """シーン内のエクスポートRootがリグのタイムスタンプ情報を持っているかどうか
    タイムスタンプのP4との整合性まではチェックしない
    Returns:
        bool: リグのタイムスタンプがあればTrue
    """
    export_root = get_export_chara_root()
    if export_root:
        cmds.select(export_root)
    extra_attrs = get_rig_chr_info()
    if not extra_attrs.get('rig_rev_time'):
        return False
    return True


def has_chr_ver_in_scene():
    """シーン内のエクスポートRootがキャラのタイムスタンプ情報を持っているかどうか
    タイムスタンプのP4との整合性まではチェックしない
    Returns:
        bool: キャラのタイムスタンプがあればTrue
    """
    export_root = get_export_chara_root()
    if export_root:
        cmds.select(export_root)
    extra_attrs = get_rig_chr_info()
    if not extra_attrs.get('chr_rev_time'):
        return False
    return True


def check_rig_ver(show_popup=True):
    """エクスポートRootのExtra AttrubuteのRig_P4_Timestampの日付と
    シーン内のリファレンスのリグのP4の日付が同じかチェックする
    エラーがある時だけポップアップ出す
    Returns:
        bool: リグのバージョンがあっていればTrue
    """
    export_root = get_export_chara_root()
    if export_root:
        cmds.select(export_root)
    extra_attrs = get_rig_chr_info()
    if not extra_attrs or not extra_attrs.get('rig_rev_time'):
        if show_popup:
            cmds.confirmDialog(title='Info',
                               message='シーンにリグのバージョンの記録がありません\n' +
                               '「リグとキャラのバージョンを記録」をお勧めします',
                               button=['OK'])
        return False
    reference_rig_path = get_reference_rig_path()
    if not reference_rig_path:
        if show_popup:
            cmds.confirmDialog(title='Info',
                               message='リグのリファレンスがありません',
                               button=['OK'])
        return False
    p4_filelog = get_p4_filelog(reference_rig_path, show_popup=show_popup)
    if not p4_filelog:
        if show_popup:
            cmds.confirmDialog(title='Info',
                               message='リグのリファレンスの日付の取得ができませんでした',
                               button=['OK'])
        return False
    if extra_attrs and p4_filelog:
        if extra_attrs['rig_rev_time'] and str(extra_attrs['rig_rev_time']) == str(p4_filelog['rev_time']):
            return True
    if show_popup:
        cmds.confirmDialog(title='NG',
                           message='以前使っていたリグとバージョンが違います',
                           button=['OK'])
    return False


def check_chr_ver(show_popup=True):
    """エクスポートRootのExtra AttrubuteのRig_P4_Timestampの日付と
    シーン内のリファレンスのキャラのP4の日付が同じかチェックする
    エラーがある時だけポップアップ出す
    Returns:
        bool: キャラのバージョンがあっていればTrue
    """
    export_root = get_export_chara_root()
    if export_root:
        cmds.select(export_root)
    extra_attrs = get_rig_chr_info()
    if not extra_attrs or not extra_attrs.get('chr_rev_time'):
        if show_popup:
            cmds.confirmDialog(title='Info',
                               message='シーンにキャラのバージョンの記録がありません\n' +
                               '「リグとキャラのバージョンを記録」をお勧めします',
                               button=['OK'])
        return False
    reference_chr_path = get_reference_chr_path()
    if not reference_chr_path:
        if show_popup:
            cmds.confirmDialog(title='Info',
                               message='キャラのリファレンスがありません',
                               button=['OK'])
        return False
    p4_filelog = get_p4_filelog(reference_chr_path, show_popup=show_popup)
    if not p4_filelog:
        if show_popup:
            cmds.confirmDialog(title='Info',
                               message='キャラのリファレンスの日付の取得ができませんでした',
                               button=['OK'])
        return False
    if extra_attrs and p4_filelog:
        if extra_attrs['chr_rev_time'] and str(extra_attrs['chr_rev_time']) == str(p4_filelog['rev_time']):
            return True
    if show_popup:
        cmds.confirmDialog(title='NG',
                           message='以前使っていたキャラとバージョンが違います',
                           button=['OK'])
    return False


def get_reference_rig_path():
    refs = cmds.ls(type='reference')
    if not refs:
        return False
    for ref in refs:
        # sharedReferenceNodeはファイルがないのでRuntimeErrorになるのでスルー
        if ref == 'sharedReferenceNode':
            continue
        ref_file = cmds.referenceQuery(ref, f=True)
        try:
            if cmds.referenceQuery(ref_file, isLoaded=True):
                # 読み込まれているリファレンスでrigがあれば最初に見つけたものを返す
                if ref_file.find('/3dcg/rig/') >= 0:
                    return ref_file
        except Exception:
            pass
    return False


def get_reference_chr_path():
    refs = cmds.ls(type='reference')
    if not refs:
        return False
    for ref in refs:
        # sharedReferenceNodeはファイルがないのでRuntimeErrorになるのでスルー
        if ref == 'sharedReferenceNode':
            continue
        ref_file = cmds.referenceQuery(ref, f=True)
        try:
            if cmds.referenceQuery(ref_file, isLoaded=True):
                # 読み込まれているリファレンスでchrがあれば最初に見つけたものを返す
                if ref_file.find('/3dcg/chr/') >= 0:
                    return ref_file
        except Exception:
            pass
    return False


def get_rig_chr_info():
    extra_attrs = {}
    export_root = get_export_chara_root()
    if not export_root:
        cmds.warning('モデルグループを見つけられませんでした')
        return
    try:
        rig_rev_time = cmds.getAttr('{}.Rig_P4_Timestamp'.format(export_root))
        extra_attrs['rig_rev_time'] = rig_rev_time
    except Exception:
        pass
    try:
        chr_rev_time = cmds.getAttr('{}.Chr_P4_Timestamp'.format(export_root))
        extra_attrs['chr_rev_time'] = chr_rev_time
    except Exception:
        pass
    return extra_attrs


def validate_p4(show_popup):
    """PerforceのバージョンチェックができるかどうかValidateする
    """
    sitepackage_path = os.path.abspath(os.path.join(CURRENT_PATH, '../../',
                                       'local-packages/Python37/Lib/site-packages')).replace('\\', '/')
    if sitepackage_path not in sys.path:
        sys.path.append(sitepackage_path)
    try:
        import psutil
        import P4
    except Exception:
        if show_popup:
            cmds.confirmDialog(title='Error',
                               message='psutilとP4モジュールが読み込めませんでした\nTAにご連絡ください',
                               button=['OK'])
        cmds.warning('Error: psutilとP4モジュールが読み込めませんでした\nTAにご連絡ください')
        return False
    is_p4_started = False
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'p4v.exe':
            is_p4_started = True
            break
    if not is_p4_started:
        if show_popup:
            cmds.confirmDialog(title='Usage',
                               message='「バージョンをチェック」が選択されています\n' +
                               'P4Vから情報を取得するのでP4Vを起動してから実行してください',
                               button=['OK'])
        cmds.warning('「バージョンをチェック」が選択されています。P4Vから情報を取得するのでP4Vを起動してから実行してください。')
        return False
    if not os.path.exists(g_ws_root):
        if show_popup:
            cmds.confirmDialog(title='Usage',
                               message='Perforceのリポジトリがありません\n' +
                               g_ws_root + '\nリポジトリの設定をしてください',
                               button=['OK'])
        cmds.warning('Perforceのリポジトリがありません\n' +
                     g_ws_root + '\nリポジトリの設定をしてください',)
        return False
    try:
        p4 = P4.P4()  # .p4configでurl等設定しているのでここで指定しない
        p4.cwd = g_ws_root
        p4.connect()
        p4.disconnect() 
    except Exception as ex:
        if show_popup:
            cmds.confirmDialog(title='Error',
                               message=str(ex),
                               button=['OK'])
        cmds.warning(ex)
        return False
    return True


def get_p4_filelog(file_path, show_popup):
    try:
        p4 = P4.P4()  # .p4configでurl等設定しているのでここで指定しない
        p4.cwd = g_ws_root
        p4.connect()
    except Exception as ex:
        if show_popup:
            cmds.confirmDialog(title='Error',
                               message=str(ex),
                               button=['OK'])
        cmds.warning(ex)
        return
    try:
        logs = p4.run_filelog('{}#have,#head'.format(file_path))
    except Exception as ex:
        cmds.warning(ex)
        # TODO: ログインもここで済ます？
        if show_popup:
            cmds.confirmDialog(title='Usage',
                               message='Perforceにログインしてください',
                               button=['OK'])
        cmds.warning('Perforceにログインしてください')
        return
    file_log_dict = {}
    if logs:
        rev = logs[0].revisions[0].rev
        rev_time = logs[0].revisions[0].time
        rev_user = logs[0].revisions[0].user
        file_log_dict['rev'] = rev
        file_log_dict['rev_time'] = rev_time
        file_log_dict['rev_user'] = rev_user
    try:
        p4.disconnect()
    except Exception:
        pass
    return file_log_dict


def show_manual():
    """コンフルのツールマニュアルページを開く
    """
    try:
        webbrowser.open('https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=513849649')
    except Exception:
        cmds.warning('マニュアルページがみつかりませんでした')


def add_to_dict(key, value, dict):
    if not key:
        key = 'ProgramError'
    if not value:
        value = 'ProgramError add_to_dictのValueがありません'
    if dict is None:
        cmds.warning('add_to_dict ディクショナリがありません' + str(value))
        return
    if key in dict:
        dict[key].append(value)
    else:
        dict[key] = [value]


def export_motion_fbx(out_folder, fbx_name, remove_all,
                      is_fix_root_to_origin=False, check_version=True,
                      show_popup=True, error_msg_dict={},
                      is_with_dress=False,
                      is_scene=False,
                      is_embed_media=False):
    """ 現在開いているシーンのgeo_grp配下のchr*ノードをエクスポートします。
    リファレンスをインポート、ネームスペース削除、Rootジョイントにモーションをベイク、
    Euler Filterをかける等。 詳細はコンフルもしくはコメント参照。
    エクスポートのプリセットはモーション班提供の以下を仕様
     - wizard2_motion.fbxexportpreset (インゲーム用fbx)
     - wizard2_motion_embed_media.fbxexportpreset (レビュー用 衣装・コスチュームfbx)
    Args:
        out_folder (str): 出力フォルダのパス
        fbx_name (str): 書き出すfbxファイル名
        remove_all (bool): シーン名の後ろの_ALLをfbx名から取るならTrue(バッチの時必要)
        is_fix_root_to_origin (bool, optional): _description_. Defaults to False.
        check_version (bool, optional): リグとキャラのリファレンスの日付をP4の最新版と比較するならTrue. Defaults to True.
        show_popup (bool, optional): ポップアップを表示するか. Defaults to True.
        error_msg_dict (dict, optional): 詳細のWarning/Errorメッセージを受け取りたい場合に渡す. Defaults to {}.
        is_with_dress (bool, optional): 衣装(tops, bottoms等)の出力. レビュー用. Defaults to False.
        is_scene (bool, optional): 衣装以外のメッシュのrootも出力. レビュー用. Defaults to False.
        is_embed_media (bool, optional): FBXにテクスチャ等を入れる場合はTrue. 
                                         衣装もしくはコスチュームの時Trueの想定. Defaults to False.
    Returns:
        bool: 最後までエクスポートできたらTrueを返す
    """
    # ======= Begin Validation =====================================
    scene_path = cmds.file(q=True, sn=True)
    if not os.path.exists(out_folder):
        cmds.warning('出力フォルダが存在しません: ' + str(out_folder))
        return False
    if check_version:
        # シーン内のタイムスタンプ情報を確認
        reference_rig_path = get_reference_rig_path()
        reference_chr_path = get_reference_chr_path()
        if reference_rig_path:
            rig_ver_result = check_rig_ver(show_popup=False)
        else:
            rig_ver_result = True  # リファレンスないならそれはそれでOK
        if reference_chr_path:
            chr_ver_result = check_chr_ver(show_popup=False)
        else:
            chr_ver_result = True  # リファレンスないならそれはそれでOK
        # タイムスタンプ情報を追加
        add_rig_chr_ver_result = True  # リグバージョン追加しない場合はTrue
        if not rig_ver_result and not chr_ver_result:
            if show_popup:
                user_choice = cmds.confirmDialog(title='Confirm',
                                                 message='リグとキャラのバージョンの整合性が確認できませんでした\n' +
                                                 '本当に続行しますか?',
                                                 button=['続行', 'リグとキャラバージョンを更新して続行', 'Cancel'],
                                                 defaultButton='Cancel',
                                                 cancelButton='Cancel',
                                                 dismissString='Cancel')
                if user_choice == 'Cancel':
                    return False
                elif user_choice == 'リグとキャラバージョンを更新して続行':
                    rig_result = add_rig_ver()
                    # リグバージョンが追加できないならおそらくキャラバージョンも追加できないので余計なポップアップ回避
                    if rig_result:
                        chr_result = add_chr_ver()
                    else:
                        chr_result = False
                    if not rig_result or not chr_result:
                        add_rig_chr_ver_result = False
            # エラーログ用
            add_to_dict(scene_path, 'Warning: リグとキャラのバージョンの整合性が確認できませんでした', error_msg_dict)
        elif not rig_ver_result:
            if show_popup:
                user_choice = cmds.confirmDialog(title='Confirm',
                                                 message='リグのバージョン情報がシーン内にない為、整合性が確認できませんでした\n' +
                                                 '本当に続行しますか?',
                                                 button=['続行', 'リグバージョンを更新して続行', 'Cancel'],
                                                 defaultButton='Cancel',
                                                 cancelButton='Cancel',
                                                 dismissString='Cancel')
                if user_choice == 'Cancel':
                    return False
                elif user_choice == 'リグバージョンを更新して続行':
                    add_rig_chr_ver_result = add_rig_ver()
            # エラーログ用
            add_to_dict(scene_path, 'Warning: リグのバージョン情報がシーン内にない為、整合性が確認できませんでした', error_msg_dict)
        elif not chr_ver_result:
            if show_popup:
                user_choice = cmds.confirmDialog(title='Confirm',
                                                 message='キャラのバージョン情報がシーン内にない為、整合性が確認できませんでした\n' +
                                                 '本当に続行しますか?',
                                                 button=['続行', 'fbxにキャラバージョンを追加して続行', 'Cancel'],
                                                 defaultButton='Cancel',
                                                 cancelButton='Cancel',
                                                 dismissString='Cancel')
                if user_choice == 'Cancel':
                    return False
                elif user_choice == 'fbxにキャラバージョンを追加して続行':
                    add_rig_chr_ver_result = add_chr_ver()
            # エラーログ用
            add_to_dict(scene_path, 'Warning: キャラのバージョン情報がシーン内にない為、整合性が確認できませんでした', error_msg_dict)
        if not add_rig_chr_ver_result:
            if show_popup:
                user_choice = cmds.confirmDialog(title='Confirm',
                                                 message='リグもしくはキャラ情報を更新できませんでした\n' +
                                                 'このまま続行しますか?',
                                                 button=['続行', 'Cancel'],
                                                 defaultButton='Cancel',
                                                 cancelButton='Cancel',
                                                 dismissString='Cancel')
                if user_choice == 'Cancel':
                    return False
    # FPSチェック
    if show_popup:
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
                return False
    else:
        # バッチの時は効かずに30fpsで処理続行
        if cmds.currentUnit(q=True, time=True) != 'ntsc':
            cmds.currentUnit(time='ntsc')
            # エラーログ用
            add_to_dict(scene_path, 'Warning: FPSが30ではありません', error_msg_dict)
    # キャラモデルのリファレンスをインポート
    if not import_main_chara_reference():
        if show_popup:
            cmds.confirmDialog(title='Error', message='リファレンスのインポートに失敗しました\n中止します',
                               button=['OK'])
        # エラーログ用
        add_to_dict(scene_path, 'Error: リファレンスのインポートに失敗しました', error_msg_dict)
        return False
    # キャラのネームスペース削除
    ignore_namespaces = g_default_namespaces.copy()  # 再帰で使うパラメータのためcopyにする(mayabatch複数処理対応)
    remove_chara_namespace(ignore_namespaces)
    # 必要なグループ名をチェック
    # まずはgeo_grp配下のchrを探す
    export_root = get_export_chara_root()
    if not export_root:
        cmds.warning('キャラルートが見つかりませんでした')
        add_to_dict(scene_path, 'Error: エクスポートルートのキャラが見つかりませんでした', error_msg_dict)
        return False
    # インゲーム用fbxだったら素体表示
    if not is_with_dress and not is_scene:
        show_sotai_parts(export_root)
    export_roots = [export_root]
    dress_roots = []
    if is_with_dress:
        dress_roots = get_dress_roots(export_root)
        if dress_roots:
            hide_parts_for_dress(export_root, dress_roots)
            export_roots.extend(dress_roots)
    if is_scene:
        mesh_roots = list_mesh_roots()
        for root in mesh_roots:
            if root not in export_roots:
                export_roots.append(root)
    if not export_roots:
        if show_popup:
            cmds.confirmDialog(title='Error', message='モデルグループを見つけられませんでした\n中止します',
                               button=['OK'])
        add_to_dict(scene_path, 'Error: モデルグループを見つけられませんでした', error_msg_dict)
        return False
    # Rootジョイント
    root_joint = get_chara_root_joint()
    if not root_joint:
        add_to_dict(scene_path, 'Error: Rootジョイントが見つかりませんでした', error_msg_dict)
        return False
    root_joints = [root_joint]
    if is_with_dress:
        dress_root_joints = get_dress_root_joints(export_root)
        root_joints.extend(dress_root_joints)
    if not root_joints:
        if show_popup:
            cmds.confirmDialog(title='確認', message='「Root」ジョイントがシーン内にありません\n' +
                               '（ロードされたリファレンスがない? ネームスペースがある?）\n' +
                               'キャンセルします', button=['OK'])
        # エラーログ用
        add_to_dict(scene_path, 'Error:「Root」ジョイントがシーン内にありません' +
                    '(ロードされたリファレンスがない? ネームスペースがある?)', error_msg_dict)
        return False

    # ======= End Validation =====================================
    # Rootジョイント配下を選択してベイク
    attrs_to_bake = ['rotateX', 'rotateY', 'rotateZ']
    cmds.select(root_joints, hierarchy=True)
    model_joints = cmds.ls(sl=True, exactType='joint')
    time_range_start = cmds.playbackOptions(q=True, minTime=True)
    time_range_end = cmds.playbackOptions(q=True, maxTime=True)
    cmds.bakeResults(model_joints, t=(time_range_start, time_range_end),
                     simulation=True, sampleBy=1, oversamplingRate=1,
                     disableImplicitControl=True, preserveOutsideKeys=True,
                     sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False,
                     removeBakedAnimFromLayer=False, bakeOnOverrideLayer=False,
                     minimizeRotation=True, attribute=attrs_to_bake)
    # Root, Hip, Handattach_L, Handattach_R のみtranslateもベイクする
    attrs_to_bake = ['translateX', 'translateY', 'translateZ',
                     'scaleX', 'scaleY', 'scaleZ']
    bake_trans_list = ['Root', 'Hip', 'Handattach_L', 'Handattach_R']
    bake_trans_joints = []
    for jnt in model_joints:
        for jnt_to_bake_trans in bake_trans_list:
            if jnt.find(jnt_to_bake_trans) > -1:
                bake_trans_joints.append(jnt)
    if not bake_trans_joints:
        add_to_dict(scene_path, 'Warning: ジョイントの選択に失敗', error_msg_dict)
        return False
    cmds.bakeResults(bake_trans_joints, t=(time_range_start, time_range_end),
                     simulation=True, sampleBy=1, oversamplingRate=1,
                     disableImplicitControl=True, preserveOutsideKeys=True,
                     sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False,
                     removeBakedAnimFromLayer=False, bakeOnOverrideLayer=False,
                     minimizeRotation=True, attribute=attrs_to_bake)
    # Hipはscaleはいらない（ベイク分けるより早いので消す）
    hip_joint = cmds.ls('Hip', type='joint')
    if not hip_joint:
        hip_joint2 = cmds.ls('Hip', recursive=True, type='joint')
        if hip_joint2:
            hip_joint = hip_joint2
            add_to_dict(scene_path, 'Warning: ネームスペースが上手く削除できていません', error_msg_dict)
        else:
            add_to_dict(scene_path, 'Warning: Hipジョイントが見つかりませんでした(リファレンスがない?)', error_msg_dict)
            return False
    try:
        # cmds.cutKey(hip_joint, attribute='scale')  # メッシュが消えることがある?
        all_scale = cmds.listConnections(hip_joint, s=True, type="animCurveTU")
        cmds.delete(all_scale)
    except Exception as ex:
        add_to_dict(scene_path, str(ex), error_msg_dict)
        return False
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
            add_to_dict(scene_path, 'Warning: timing_boxはありましたが想定する値のキーが入っていません', error_msg_dict)
    else:
        scene_name = cmds.file(q=True, sn=True)
        if scene_name.endswith('_ALL.ma'):
            # エラーログ用
            add_to_dict(scene_path, 'Warning: シーン名は_ALLですがtiming_boxがありませんでした', error_msg_dict)
    # 中間のキーをクリア
    cmds.selectKey(unsnappedKeys=True, time=(time_range_start,time_range_end), hierarchy='none', controlPoints=False)
    cmds.cutKey(animation='keys', clear=True)
    # Euler Filterをかける前に最初のキーの一つ前に0値のキーを打つ(無理な回転がつかないように)
    first_key = cmds.findKeyframe(which='first')
    add_zero_key(model_joints, bake_trans_joints, first_key-1)
    # Euler Filterをかける
    cmds.filterCurve(model_joints)
    # Euler Filterをかける前に打ったキーを削除
    remove_key_before_start(model_joints, bake_trans_joints, first_key-1)
    # chrxxxx_xxをグループから出す
    try:
        cmds.parent(export_roots, world=True)
    except Exception as ex:
        print(ex)
        pass
    # rigを削除
    rig_node = cmds.ls('rig', recursive=True, dag=True)
    if rig_node:
        cmds.delete(rig_node)
    # コンストレイントの入っているfosterParentを削除
    # ベイクしているしコンストレイントは選択せずエクスポートするが
    # Mayaのポップアップが出てアーティストさんを不安にさせるので消す
    fosterParents = cmds.ls(type='fosterParent')
    if fosterParents:
        cmds.delete(fosterParents)
    # レイヤーが削除できないのでリファレンスをdefaultLayerに移動
    export_roots = update_list(export_roots)
    all = cmds.listRelatives(export_roots, ad=True, fullPath=True)
    belong_layers = cmds.listConnections(all, type='displayLayer')
    if belong_layers:
        belong_layers = list(set(belong_layers))
        for layer in belong_layers:
            member = cmds.editDisplayLayerMembers(layer, query=True, fullNames=True)
            cmds.editDisplayLayerMembers('defaultLayer', member)
    # ディスプレイレイヤーを削除
    displayLayers = cmds.ls(type='displayLayer')
    for layer in displayLayers:
        if layer.find('defaultLayer') == -1:
            cmds.delete(layer)
    # Rootジョイントの原点固定（デフォルトは原点開始）
    if is_fix_root_to_origin and not is_with_dress:
        for root_joint in root_joints:
            times = cmds.keyframe(root_joint + '.translateX', query=True)
            cmds.setKeyframe(root_joint, t=times, at='tx', v=0)
            cmds.setKeyframe(root_joint, t=times, at='ty', v=0)
            cmds.setKeyframe(root_joint, t=times, at='tz', v=0)
            cmds.setKeyframe(root_joint, t=times, at='rx', v=0)
            cmds.setKeyframe(root_joint, t=times, at='ry', v=0)
            cmds.setKeyframe(root_joint, t=times, at='rz', v=0)
    # 念のためジョイント表示
    root_joints = update_list(root_joints)
    cmds.showHidden(root_joints, below=True)
    # 情報を入れ終わったら_Outlineを消す
    child_meshes = list_child_mesh_transforms(export_roots)
    for mesh in child_meshes:
        if mesh.endswith('_Outline'):
            # 参照情報が削除されコピー先の情報もなくなることがあるので念のためヒストリー削除
            cmds.delete(mesh, constructionHistory=True)
            cmds.delete(mesh)
    # バッチの時ファイル名から_ALLを取るか
    if remove_all:
        if len(fbx_name) > 4 and fbx_name.endswith('_ALL'):
            fbx_name = fbx_name[0:-4]
    exported_files = []
    if is_separate_export:
        cmds.select(export_roots)
        exported_files = export_split_animation(out_folder,
                                                fbx_name,
                                                model_joints,
                                                bake_trans_joints,
                                                error_msg_dict,
                                                is_with_dress)
    else:
        try:
            # この処理でのFBXプリセットを設定する（Maya本体のプリセットは変わらない）
            preset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.',
                                          'wizard2_motion.fbxexportpreset')).replace('\\', '/')
            if is_embed_media:
                preset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.',
                                              'wizard2_motion_embed_media.fbxexportpreset')).replace('\\', '/')
            mel.eval('FBXLoadExportPresetFile -f "{}"'.format(preset_path))
            cmds.select(export_roots, hierarchy=True)
            export_path = out_folder + "/" + fbx_name + ".fbx"
            mel.eval('FBXExport -f "{0}" -s'.format(export_path))
            exported_files.append(export_path)
        except Exception as ex:
            print(ex)
    # 原点固定ではなかったら出力後のfbxに原点開始の再処理（デフォルトは原点開始）
    if not is_fix_root_to_origin and not is_with_dress:
        anim_origin_start(exported_files, is_with_dress)
    if exported_files:
        re_export_for_3dviwer(exported_files, is_with_dress, is_scene)
        print('FBXを出力しました: \n' + '\n'.join(exported_files))
    return True


def anim_origin_start(maya_scene_paths, is_with_dress):
    """原点開始
    export_motion_fbxでエクスポート後のfbxに再度実行する想定
    衣装のエクスポートには対応していない
    Args:
        maya_scene_paths (string[]): export_motion_fbxでエクスポートされたfbxパス配列
    """
    if not maya_scene_paths:
        return False
    if type(maya_scene_paths) is str:
        maya_scene_paths = [maya_scene_paths]
    for scene_path in maya_scene_paths:
        cmds.file(scene_path, open=True, force=True)
        root_joint = get_chara_root_joint()
        if not root_joint:
            cmds.warning('「Root」ジョイントがシーン内にありません')
            return
        export_root = get_export_chara_root()
        if not export_root:
            cmds.warning('キャラルートが見つかりませんでした')
            return
        export_roots = [export_root]
        if is_with_dress:
            dress_roots = get_dress_roots(export_root)
            if dress_roots:
                # 衣装のjointsはキャラのと同じはず
                export_roots.extend(dress_roots)
        time_range_start = cmds.playbackOptions(q=True, minTime=True)
        time_range_end = cmds.playbackOptions(q=True, maxTime=True)
        loc_rot = cmds.spaceLocator(name='rot')[0]
        loc_trans = cmds.spaceLocator(name='trans')[0]
        cmds.parent(loc_trans, loc_rot)
        loc_rot_point_constraint = cmds.pointConstraint(root_joint, loc_rot)[0]
        cmds.setKeyframe(loc_rot, time=time_range_start)
        cmds.delete(loc_rot_point_constraint)
        loc_rot_rot_constraint = cmds.orientConstraint(root_joint, loc_rot)[0]
        loc_trans_point_constraint = cmds.pointConstraint(root_joint, loc_trans)[0]
        cmds.bakeResults(loc_rot,
                         t=(time_range_start, time_range_end),
                         simulation=True, sampleBy=1, oversamplingRate=1,
                         disableImplicitControl=True, preserveOutsideKeys=True,
                         sparseAnimCurveBake=False,
                         removeBakedAttributeFromLayer=False,
                         removeBakedAnimFromLayer=False,
                         bakeOnOverrideLayer=False,
                         minimizeRotation=True,
                         attribute=['rotateX', 'rotateY', 'rotateZ'])
        cmds.bakeResults(loc_trans,
                         t=(time_range_start, time_range_end),
                         simulation=True, sampleBy=1, oversamplingRate=1,
                         disableImplicitControl=True, preserveOutsideKeys=True,
                         sparseAnimCurveBake=False,
                         removeBakedAttributeFromLayer=False,
                         removeBakedAnimFromLayer=False,
                         bakeOnOverrideLayer=False,
                         minimizeRotation=True,
                         attribute=['translateX', 'translateY', 'translateZ'])
        cmds.delete(loc_rot_rot_constraint)
        cmds.delete(loc_trans_point_constraint)
        joint_rot_constraint = cmds.orientConstraint(loc_trans, root_joint)[0]
        joint_trans_constraint = cmds.pointConstraint(loc_trans, root_joint)[0]
        cmds.select(loc_rot)
        anim_layer = cmds.animLayer(addSelectedObjects=True)
        cmds.setAttr('{0}.rotationAccumulationMode'.format(anim_layer), False)
        cmds.setAttr('{0}.scaleAccumulationMode'.format(anim_layer), True)
        cmds.makeIdentity(loc_rot, t=True, r=True)
        cmds.setKeyframe(loc_rot, time=time_range_start)
        cmds.select(root_joint, hierarchy=True)
        model_joints = cmds.ls(sl=True, exactType='joint')
        cmds.bakeResults(model_joints, t=(time_range_start, time_range_end),
                         simulation=True, sampleBy=1, oversamplingRate=1,
                         disableImplicitControl=True, preserveOutsideKeys=True,
                         sparseAnimCurveBake=False,
                         removeBakedAttributeFromLayer=False,
                         removeBakedAnimFromLayer=False,
                         bakeOnOverrideLayer=False,
                         minimizeRotation=True,
                         attribute=['rotateX', 'rotateY', 'rotateZ',
                                    'translateX', 'translateY', 'translateZ'])
        cmds.delete(joint_rot_constraint)
        cmds.delete(joint_trans_constraint)
        scene_path = cmds.file(q=True, sn=True)
        if scene_path:
            out_folder = os.path.dirname(scene_path)
            fbx_name = os.path.splitext(os.path.basename(scene_path))[0]
            preset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.',
                                          'wizard2_motion.fbxexportpreset')).replace('\\', '/')
            mel.eval('FBXLoadExportPresetFile -f "{}"'.format(preset_path))
            cmds.select(export_roots, hierarchy=True)
            export_path = out_folder + "/" + fbx_name + ".fbx"
            try:
                mel.eval('FBXExport -f "{0}" -s'.format(export_path))
            except Exception as ex:
                print(ex)
    return [maya_scene_paths]


def export_motion_fbx_batch(input_folder, search_str, is_same_as_scene_folder,
                            out_folder, remove_all, is_fix_root_to_origin,
                            check_version, is_open_out_folder_batch,
                            show_popup, is_with_dress, is_scene,
                            is_embed_media):
    try:
        # on_export_motion_fbx_batchのValidation時と同じようにリストすること
        # （コマンドプロンプトで渡せる文字数上限が8000くらいな為リストパラメータで渡せない）
        ma_files = [os.path.join(dir, f) for dir, dn, filenames in os.walk(input_folder) for f in glob.glob(dir + '/' + search_str)]
    except Exception:
        return
    try:
        sitepackage_path = os.path.abspath(os.path.join(CURRENT_PATH, '../../',
                                           'local-packages/Python37/Lib/site-packages')).replace('\\', '/')
        sys.path.append(sitepackage_path)
    except Exception as ex:
        print(ex)
        return
    if type(is_same_as_scene_folder) is str:
        is_same_as_scene_folder = False if is_same_as_scene_folder == 'False' else True
    if type(remove_all) is str:
        remove_all = False if remove_all == 'False' else True
    if type(is_fix_root_to_origin) is str:
        is_fix_root_to_origin = False if is_fix_root_to_origin == 'False' else True
    if type(check_version) is str:
        check_version = False if check_version == 'False' else True
    if type(is_open_out_folder_batch) is str:
        is_open_out_folder_batch = False if is_open_out_folder_batch == 'False' else True
    if type(show_popup) is str:
        show_popup = False if show_popup == 'False' else True
    if type(is_with_dress) is str:
        is_with_dress = False if is_with_dress == 'False' else True
    if type(is_scene) is str:
        is_scene = False if is_scene == 'False' else True
    if type(is_embed_media) is str:
        is_embed_media = False if is_embed_media == 'False' else True
    if not is_same_as_scene_folder and (is_with_dress):
        if os.path.exists(out_folder):
            out_folder += '/DressPreview'
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)
    # パスのスラッシュ修正
    fixed_slashes = []
    for file_path in ma_files:
        fixed_slashes.append(file_path.replace('\\', '/'))
    ma_files = fixed_slashes
    if ma_files:
        start = time.time()
        error_msg_dict = {}
        for scene_path in ma_files:
            cmds.file(scene_path, open=True, force=True)
            file_name_without_ext = os.path.splitext(os.path.basename(scene_path))[0]
            if is_same_as_scene_folder:
                out_folder = os.path.dirname(scene_path)
                if is_with_dress:
                    out_folder += '/DressPreview'
                    if not os.path.exists(out_folder):
                        os.makedirs(out_folder)
            try:
                export_motion_fbx(out_folder,
                                  file_name_without_ext,
                                  remove_all,
                                  is_fix_root_to_origin,
                                  check_version,
                                  show_popup,
                                  error_msg_dict,
                                  is_with_dress,
                                  is_scene,
                                  is_embed_media)
            except Exception:
                add_to_dict(scene_path, 'エクスポート中に予期せぬエラーが置きました', error_msg_dict)
        time_took = time.time() - start
        # ErrorやWarning等があったら知らせる
        if error_msg_dict:
            now = time.localtime()
            timestamp = time.strftime('%Y%m%d%H%M', now)
            log_file_path = os.path.join(tempfile.gettempdir(), 'MotionFBXExportErrorLog_' + timestamp + '.csv')
            with open(log_file_path, mode='w+') as f:
                f.write(time.strftime('%Y/%m/%d', now) + '\n')
                for scene_path in error_msg_dict:
                    try:
                        f.write(scene_path + ',' + ','.join(error_msg_dict[scene_path]) + '\n')
                    except Exception:
                        f.write('ログの書き出し中にエラーが置きました\n')
                f.write('かかった時間:{0}'.format(round(time_took)) + '秒')
            webbrowser.open(log_file_path)
        # エクスポート後フォルダを開く
        if is_open_out_folder_batch:
            if os.path.exists(out_folder):
                subprocess.Popen('explorer "{}"'.format(os.path.normpath(out_folder)))


def list_child_mesh_transforms(root_node, except_outline=False):
    """root_node配下のmeshのtransformのリスト(fullPath)を返す
    Args:
        root_node (str): 例：chr0004_00
    Returns:
        str[]: root_node配下のメッシュtransformのリスト
    """
    orig_selection = cmds.ls(sl=True)
    mesh_transforms = []
    if root_node:
        children = cmds.listRelatives(root_node, children=True, fullPath=True)
        cmds.select(children, hierarchy=True)
        meshes = cmds.ls(sl=True, long=True, type='mesh')
        if not meshes:
            return []
        for mesh in meshes:
            transforms = cmds.listRelatives(mesh, p=True, fullPath=True)
            if transforms:
                transform = transforms[0]
                if except_outline:
                    if transform.endswith('_Outline'):
                        continue
                mesh_transforms.append(transform)
        mesh_transforms = list(set(mesh_transforms))
    cmds.select(orig_selection)  # 選択状態を元に戻す
    return mesh_transforms


def get_export_chara_root():
    scene_path = cmds.file(q=True, sn=True)
    # エクスポート済みfbxの場合
    if scene_path.endswith('.fbx'):
        top_nodes = cmds.ls(assemblies=True)
        # ネームスペースがない方優先
        for node in top_nodes:
            if node in g_chara_prefixes:
                return node
        # ネームスペースがある
        for node in top_nodes:
            for prefix in g_chara_prefixes:
                if node.find(prefix):
                    return node
    try:
        # モーション用の.maシーンの場合 geo_grpの下にモデルがある
        try:
            children = cmds.listRelatives('*:geo_grp')
        except Exception:
            children = cmds.listRelatives('geo_grp')
        for child in children:
            for prefix in g_chara_prefixes:
                name_wo_namespace = child.split(':')[-1]
                if name_wo_namespace.find(prefix) > -1:
                    return child
    except Exception:
        # p1またはp2グループがgeo_grpの下以外だった場合、なんとかchrを探す
        for prefix in g_chara_prefixes:
            export_roots = cmds.ls(prefix, recursive=True, dag=True)
            if export_roots:
                return export_roots[0]


def get_dress_roots(export_root):
    """
    エクスポートキャラのタイプの衣装ノードを返す
    Args:
        export_root (str): 現在のメインキャラのルートノード(p1, p2, chrのどれか)
    Returns:
        str[]: キャラタイプのTransformの配列（ネームスペース対応）
    """
    if export_root.find(':') > -1:
        export_root = export_root.split(':')[-1]
    dress_roots = []
    roots = cmds.ls(export_root, recursive=True, exactType='transform')
    found_hair = False
    for root in roots:
        if root.find('hair') > -1:
            found_hair = True
            break
    # このキャラタイプのhairがない場合はシーン内にp0(男女共通)のhairがあるか探す
    if not found_hair:
        roots_p0 = cmds.ls('p0', recursive=True, exactType='transform')
        for root in roots_p0:
            if root.find('hair') > -1:
                roots.append(root)
    for root in roots:
        for name_space in g_namespace_parts_dict.keys():
            if root.find(name_space) > -1:
                dress_roots.append(root)
    return dress_roots


def show_sotai_parts(export_root):
    show_parts = []
    show_parts.append('{0}_{1}_'.format(export_root, 'h'))
    show_parts.append('{0}_{1}_'.format(export_root, 'f'))
    show_parts.append('{0}_{1}_'.format(export_root, 'e'))
    show_parts.append('{0}_{1}_'.format(export_root, 't'))
    show_parts.append('{0}_{1}_'.format(export_root, 'b'))
    # show_parts.append('{0}_{1}_'.format(export_root, 'o'))
    export_root_children = cmds.listRelatives(export_root, children=True, fullPath=True)
    for child in export_root_children:
        for part in show_parts:
            if child.find(part) > -1:
                cmds.showHidden(child)


def hide_parts_for_dress(export_root, found_dress_roots):
    """衣装と被ったexport_root配下の素体を非表示にする
    なりきりセットの時はt, b , o, hの素体を非表示
    素体のoは常に非表示
    Args:
        export_root (str): _description_
        found_dress_roots (str[]): シーン内でリストされた衣装のrootリスト
    """
    is_costume = False
    for dress_root in found_dress_roots:
        if dress_root.find('|') > -1:
            dress_root = dress_root.split('|')[-1]
        if dress_root.startswith('costume:'):
            is_costume = True
            break
    export_root_children = cmds.listRelatives(export_root, children=True, fullPath=True)
    hide_parts = []
    # oはオーバーオールもしくはワンピースの意味。oの素体は常に非表示。
    hide_parts.append('{0}_{1}_'.format(export_root, 'o'))
    if is_costume:
        hide_parts.append('{0}_{1}_'.format(export_root, 't'))
        hide_parts.append('{0}_{1}_'.format(export_root, 'b'))
        hide_parts.append('{0}_{1}_'.format(export_root, 'h'))
    else:
        for dress in found_dress_roots:
            if dress.find(':') > -1:
                dress = dress.split(':')[0]
            part_letter = g_namespace_parts_dict.get(dress, None)
            if part_letter:
                hide_parts.append('{0}_{1}_'.format(export_root, part_letter))
    for child in export_root_children:
        for hide_part in hide_parts:
            if child.find(hide_part) > -1:
                cmds.hide(child)


def create_timing_box():
    """IN,LOOP,OUTにアニメーションのFBXを分けてエクスポートする際のフレームを
    指定するノード。　「timing_box」という名前のピンク色のキューブをキャラの頭上に作ります。
    ScaleZにキーを打って指定する。 INの開始位置には値1のキー、LOOPの開始の開始位置には値2のキー、
    OUTの開始位置には値3のキーを打つ想定。
    """
    # ネームスペース付きにも対応するためrecursive
    timing_boxes = cmds.ls('timing_box', recursive=True)
    if timing_boxes:
        cmds.select(timing_boxes)
        cmds.confirmDialog(title='Info',
                           message='既にあります',
                           button=['OK'])
        return
    timing_box = cmds.polyCube(sx=1, sy=1, sz=1, h=15, w=15, d=15, name='timing_box')
    timing_box = timing_box[0]
    cmds.move(0, 200, 0, timing_box)
    cmds.move(0, 0, 0, timing_box+".scalePivot", timing_box+".rotatePivot", absolute=True)
    shd = cmds.ls('timing_box_lambert', type='lambert')
    if shd:
        shd = shd[0]
        shdSG = cmds.ls('%sSG' % shd)[0]
    else:
        shd = cmds.shadingNode('lambert', name="timing_box_lambert", asShader=True)
        shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
        cmds.setAttr(shd + ".color", 1, 0, 1, type="double3")
    cmds.sets(timing_box, e=True, forceElement=shdSG)
    # デフォルトで1, 2, 3のキーフレームを打つ
    cmds.setKeyframe(timing_box, attribute='scaleZ', t=[0], itt='stepnext', ott='step', value=1)
    cmds.setKeyframe(timing_box, attribute='scaleZ', t=[20], itt='stepnext', ott='step', value=2)
    cmds.setKeyframe(timing_box, attribute='scaleZ', t=[80], itt='stepnext', ott='step', value=3)
    cmds.setKeyframe(timing_box, attribute='scaleZ', t=[100], itt='stepnext', ott='step', value=3)
    # timing_boxに必要ないアトリビュートをLock and Hideする
    cmds.setAttr('{}.tx'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.ty'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.tz'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.rx'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.ry'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.rz'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.sx'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.sy'.format(timing_box), lock=True, keyable=False, channelBox=False)
    # IN, LOOP, OUT Extra Attrubuteを作成 (追加仕様 2023/05/30)
    cmds.addAttr(timing_box, ln='IN', at='bool', defaultValue=True, keyable=True)
    cmds.setAttr('{}.IN'.format(timing_box), keyable=False, channelBox=True)
    cmds.addAttr(timing_box, ln='LOOP', at='bool', defaultValue=True, keyable=True)
    cmds.setAttr('{}.LOOP'.format(timing_box), keyable=False, channelBox=True)
    cmds.addAttr(timing_box, ln='OUT', at='bool', defaultValue=True, keyable=True)
    cmds.setAttr('{}.OUT'.format(timing_box), keyable=False, channelBox=True)
    cmds.addAttr(timing_box, ln='IsJump', at='bool', defaultValue=False, keyable=True)
    cmds.setAttr('{}.IsJump'.format(timing_box), keyable=False, channelBox=True)


def update_timing_box():
    """timing_boxのExtraAttributeにboolのIN,LOOP,OUTを追加した為
    既存のtiming_boxがある場合は追加する。 2023/05/30~
    """
    # ネームスペース付きで複数ある場合の対応
    timing_boxes = cmds.ls('timing_box', recursive=True)
    if len(timing_boxes) > 1:
        cmds.confirmDialog(title='Usage',
                           message='timing_boxが複数ありました\n' +
                           '一つにしてください\n' + '\n'.join(timing_boxes),
                           button=['OK'])
        return
    if not timing_boxes:
        user_choice = cmds.confirmDialog(title='Confirm',
                                         message='既存のtiming_boxがありません\n' +
                                         '新規で作りますか?',
                                         button=['OK', 'Cancel'],
                                         defaultButton='OK',
                                         cancelButton='Cancel',
                                         dismissString='Cancel')
        if user_choice == 'Cancel':
            return
        create_timing_box()
        return
    timing_box = timing_boxes[0]
    # timing_boxに必要ないアトリビュートをLock and Hideする
    cmds.setAttr('{}.tx'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.ty'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.tz'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.rx'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.ry'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.rz'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.sx'.format(timing_box), lock=True, keyable=False, channelBox=False)
    cmds.setAttr('{}.sy'.format(timing_box), lock=True, keyable=False, channelBox=False)
    # IN, LOOP, OUT Extra Attrubuteを作成 (追加仕様 2023/05/30)
    try:
        cmds.getAttr('{}.IN'.format(timing_box))
    except Exception:
        cmds.addAttr(timing_box, ln='IN', at='bool', defaultValue=True, keyable=True)
        cmds.setAttr('{}.IN'.format(timing_box), keyable=False, channelBox=True)
    try:
        cmds.getAttr('{}.LOOP'.format(timing_box))
    except Exception:
        cmds.addAttr(timing_box, ln='LOOP', at='bool', defaultValue=True, keyable=True)
        cmds.setAttr('{}.LOOP'.format(timing_box), keyable=False, channelBox=True)
    try:
        cmds.getAttr('{}.OUT'.format(timing_box))
    except Exception:
        cmds.addAttr(timing_box, ln='OUT', at='bool', defaultValue=True, keyable=True)
        cmds.setAttr('{}.OUT'.format(timing_box), keyable=False, channelBox=True)
    try:
        cmds.getAttr('{}.IsJump'.format(timing_box))
    except Exception:
        cmds.addAttr(timing_box, ln='IsJump', at='bool', defaultValue=False, keyable=True)
        cmds.setAttr('{}.IsJump'.format(timing_box), keyable=False, channelBox=True)
    cmds.select(timing_box)


def add_zero_key(joints_to_key_rot, joints_to_key_trans, frame):
    """
    Euler Filterをかける前に最初のキーの一つ前に値0のキーフレームを打つ。
    RotYだけの回転で良いのにEular FilterでRotX, RotXで無理やり回転がついてしまうケースの対応
    Args:
        joints_to_key_rot (str[]): ローテーションをベイクしているジョイントのリスト
        start_frame (str[]): トランスレーションをベイクしているジョイントのリスト
    """
    # Rootジョイント配下のRotationにキーを打つ
    attrs_to_key = ['rotateX', 'rotateY', 'rotateZ']
    cmds.setKeyframe(joints_to_key_rot, attribute=attrs_to_key, t=[frame],  value=0)
    # Root, Hip, Handattach_L, Handattach_R translateにもキーを打つ
    attrs_to_key = ['translateX', 'translateY', 'translateZ']
    cmds.setKeyframe(joints_to_key_trans, attribute=attrs_to_key, t=[frame],  value=0)


def remove_key_before_start(joints_to_key_rot, joints_to_key_trans, frame):
    """add_zero_key で追加したキーを削除
    """
    attrs_to_remove_key = ['rotateX', 'rotateY', 'rotateZ']
    cmds.cutKey(joints_to_key_rot, time=(frame, frame), attribute=attrs_to_remove_key, option="keys")
    attrs_to_remove_key = ['translateX', 'translateY', 'translateZ']
    cmds.cutKey(joints_to_key_trans, time=(frame, frame), attribute=attrs_to_remove_key, option="keys")


def export_into_takes(out_folder, file_name_as, start_frame, end_frame,
                      joints_to_key_rot, joints_to_key_trans):
    export_path = out_folder + '/' + file_name_as
    # Euler Filterをかける
    add_zero_key(joints_to_key_rot, joints_to_key_trans, start_frame-1)
    cmds.filterCurve(joints_to_key_rot)
    # Euler Filterかける前に打ったキーを削除
    remove_key_before_start(joints_to_key_rot, joints_to_key_trans, start_frame-1)
    # 分割アニメーションのタイムレンジは0スタートにはしない
    cmds.playbackOptions(animationStartTime=start_frame,
                         animationEndTime=end_frame,
                         min=start_frame,
                         max=end_frame)
    try:
        mel.eval("FBXExportSplitAnimationIntoTakes -clear;")
        preset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.',
                                      'wizard2_motion.fbxexportpreset')).replace('\\', '/')
        mel.eval('FBXLoadExportPresetFile -f "{}"'.format(preset_path))
        mel.eval('FBXExportSplitAnimationIntoTakes -v "{0}" {1} {2}'.format(export_path, start_frame, end_frame))
        mel.eval('FBXExport -f "{0}" -s'.format(export_path))
        mel.eval("FBXExportSplitAnimationIntoTakes -clear;")  # お掃除しておかないと次のFBXExportに支障が出る
    except Exception as ex:
        print(ex)
        return
    return export_path


def re_export_for_3dviwer(scene_paths, is_with_dress, is_scene):
    """3Dビューワでも分割再生されるよう再エクスポート
    FBXExportSplitAnimationIntoTakesでエクスポートしたままだとプレビューがフルフレームのままなので再エクスポート
    プレビューだけフルフレームでもUnity上では問題ないが、ADレビューの時に3Dビューワで再生するためプレビュー大事
    Args:
        scene_paths (string[]): 分割エクスポート済みのシーンパス
    """
    for scene_path in scene_paths:
        cmds.file(scene_path, open=True, force=True)
        export_root = get_export_chara_root()
        if not export_root:
            return False
        export_roots = [export_root]
        if is_with_dress:
            dress_roots = get_dress_roots(export_root)
            if dress_roots:
                export_roots.extend(dress_roots)
        if is_scene:
            mesh_roots = list_mesh_roots()
            for root in mesh_roots:
                if root not in export_roots:
                    export_roots.append(root)
        cmds.select(export_roots, hierarchy=True)
        try:
            mel.eval('FBXExport -f "{0}" -s'.format(scene_path))
        except Exception as ex:
            print(ex)
    return True


def export_split_animation(out_folder, base_file_name, joints_to_key_rot,
                           joints_to_key_trans, error_msg_dict,
                           is_with_dress):
    """
    timing_boxのscaleZに指定されているキーでIN, LOOP, OUT部分に分けたアニメーションfbxをエクスポートします。
    出力ファイル名はbase_file_name にそれぞれ _IN, _LOOP, _OUT がつきます。
    0スタートにはせず、シーンのキーフレームそのままで出す。
    シーン内のtiming_boxのExtraAttrubuteにIN,LOOP,OUTがついている場合はTrueのものだけエクスポートする。
    ExtraAttrubuteのLOOPがTrueでLOOPのキーがない場合はINとOUTの境目の1フレームをLOOPとしてエクスポートする(jumpなど)。
    wizard2_motion.fbxexportpreset プリセットを使ってエクスポートする。
    Args:
        out_folder (str): 出力フォルダパス
        base_file_name (str): ベースファイル名
    Returns:
        str[] 分割出力したシーンファイルパスの列
    """
    timing_box = cmds.ls('timing_box', recursive=True)
    if timing_box:
        timing_box = timing_box[0]
    # ExtraAttributeにIN,LOOP,OUTがない場合はキーがあれば全部エクスポートする
    is_export_IN = True
    is_export_LOOP = True
    is_export_OUT = True
    is_jump = False
    try:
        is_export_IN = cmds.getAttr('{}.IN'.format(timing_box))
    except Exception:
        pass
    try:
        is_export_LOOP = cmds.getAttr('{}.LOOP'.format(timing_box))
    except Exception:
        pass
    try:
        is_export_OUT = cmds.getAttr('{}.OUT'.format(timing_box))
    except Exception:
        pass
    try:
        is_jump = cmds.getAttr('{}.IsJump'.format(timing_box))
    except Exception:
        pass
    exported_files = []
    # 同じモーションタイプが複数存在する場合用
    num_in = 0
    num_loop = 0
    num_out = 0
    start_split_frame_value = common.get_first_split_frame()
    if not start_split_frame_value:
        return
    # ベイクは整数のキーフレームに打たれるため、アニメーションのキーフレームが整数でない場合分割した際ズレるのでチェック
    # timing_boxの開始フレームチェック
    if round(start_split_frame_value[0]) != start_split_frame_value[0]:
        add_to_dict(base_file_name, 'Warning: timing_boxの開始フレームが整数ではないため分割のポーズがズレているかもしれません', error_msg_dict)
        print('Warning: timing_boxの開始フレームが整数ではないため分割のポーズがズレているかもしれません')
    # モデルのジョイント1つの開始フレームチェック
    keyframes = cmds.keyframe(joints_to_key_rot[0] + '.scaleZ', q=True, time=())
    if round(keyframes[0]) != keyframes[0]:
        add_to_dict(base_file_name, 'Warning: 開始フレームが整数ではないため分割のポーズがズレているかもしれません', error_msg_dict)
        print('Warning: 開始フレームが整数ではないため分割のポーズがズレているかもしれません')
    end_split_frame_value = common.get_last_split_frame()
    end_split_frame = end_split_frame_value[0]
    next_split_frame_value = common.get_next_split_frame(start_split_frame_value)
    prev_motion_type = None
    while True:
        if not start_split_frame_value:
            break
        from_frame = start_split_frame_value[0]
        motion_type = start_split_frame_value[1]
        if next_split_frame_value:
            to_frame = next_split_frame_value[0]
        else:
            # 最後に1フレームだけ別のモーションがある場合は1フレームだけ出力
            if prev_motion_type != motion_type and from_frame == end_split_frame:
                to_frame = end_split_frame
            else:
                break
        file_name = ''
        do_export = True
        if motion_type == 1:
            if not is_export_IN:
                do_export = False
            else:
                if num_in > 0:
                    file_name = base_file_name + '_IN' + str(num_in+1) + '.fbx'
                else:
                    file_name = base_file_name + '_IN.fbx'
                num_in += 1
        elif motion_type == 2:
            if not is_export_LOOP:
                do_export = False
            else:
                if num_loop > 0:
                    file_name = base_file_name + '_LOOP' + str(num_loop+1) + '.fbx'
                else:
                    file_name = base_file_name + '_LOOP.fbx'
                num_loop += 1
        elif motion_type == 3:
            if not is_export_OUT:
                do_export = False
            else:
                if num_out > 0:
                    file_name = base_file_name + '_OUT' + str(num_out+1) + '.fbx'
                else:
                    file_name = base_file_name + '_OUT.fbx'
                num_out += 1
            # ユーザーがExtraAttrubuteのIs Jumpにチェックを入れていて、timing_boxにLOOPのキーが打っていないようなら
            # 別途OUTの開始1フレームをLOOPとしてエクスポートする
            if is_jump:
                if common.has_loop_split_frame():
                    add_to_dict(base_file_name, 'Warning: 「Is Jump」はLOOPキーがない時OUTの最初のフレームを' +
                                'LOOPとして出力しますが、LOOPキーがある為LOOPキーを優先します', error_msg_dict)
                    print('Warning: 「Is Jump」はLOOPキーがない時OUTの最初のフレームを' +
                          'LOOPとして出力しますが、LOOPキーがある為LOOPキーを優先します')
                elif not is_export_LOOP:
                    # Is JumpがonでもLOOPがoffなら出力しない
                    pass
                else:
                    # Jumpの時ににLOOPのキーはないので連番はつかない
                    num_loop += 1
                    exported_path = export_into_takes(out_folder, base_file_name + '_LOOP.fbx', from_frame, from_frame, joints_to_key_rot, joints_to_key_trans)
                    if exported_path:
                        exported_files.append(exported_path)
                    else:
                        add_to_dict(base_file_name, 'Warning: JumpのLOOPエクスポートに失敗しました', error_msg_dict)
                        print('Warning: JumpのLOOPエクスポートに失敗しました')
        if do_export:
            exported_path = export_into_takes(out_folder, file_name, from_frame, to_frame, joints_to_key_rot, joints_to_key_trans)
            if exported_path:
                exported_files.append(exported_path)
            else:
                add_to_dict(base_file_name, 'Warning: 分割エクスポートに失敗しました', error_msg_dict)
                print('Warning: 分割エクスポートに失敗しました')
        prev_motion_type = motion_type
        start_split_frame_value = next_split_frame_value
        next_split_frame_value = common.get_next_split_frame(start_split_frame_value)
    # FBXExportSplitAnimationIntoTakesのバグ?で3Dビューワでプレビューが分割されない為再エクスポートで修正
    is_scene = False
    result = re_export_for_3dviwer(exported_files,
                                   is_with_dress, is_scene)
    if not result:
        add_to_dict(base_file_name, 'Warning: 3Dビューワ向けの再エクスポート中に問題がありました', error_msg_dict)
    return exported_files


def remove_namespaces():
    """デフォルトネームスペース以外のネームスペースを削除します。
    子階層になっているネームスペースにも対応。
    削除の際のオプションはMerge With Rootです。
    """
    default_namespaces = ['UI', 'shared']
    cmds.namespace(setNamespace=':')
    namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
    non_default_namespaces = [n for n in namespaces if n not in default_namespaces]
    if non_default_namespaces:
        for name in non_default_namespaces:
            cmds.namespace(removeNamespace=name, mergeNamespaceWithRoot=True)
        remove_namespaces()
    else:
        return


def remove_chara_namespace(except_namespaces):
    """p1, p2, chrのネームスペースを削除します。
    削除の際のオプションはMerge With Rootです。
    """
    cmds.namespace(setNamespace=':')
    namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
    namespaces = [n for n in namespaces if n not in except_namespaces]
    if namespaces:
        for name in namespaces:
            # ネームスペースは基本p1, p2, chrのはずだが「chr0006_00」というのもある
            for prefix in g_chara_prefixes:
                if name == g_chara_prefixes or name.startswith(prefix):
                    cmds.namespace(removeNamespace=name, mergeNamespaceWithRoot=True)
                else:
                    except_namespaces.append(name)
        remove_chara_namespace(except_namespaces)


def get_chara_root_joint():
    """キャラのRootジョイントを返す。
    リファレンスのキャラが複数シーン内にある場合、3dcg/rigのモデルのRootジョイントを優先する。
    リファレンスのキャラがp1, p2, chr(旧仕様)とある場合はp1, p2, chrの順で優先して返す。
    Returns:
        str: Rootジョイントの名前
    """
    # 単純にRootジョイントがシーン内に1つならそれを返す
    roots = cmds.ls('Root', exactType='joint')
    if len(roots) == 1:
        return roots[0]
    chara_model_candidates = {}  # キャラモデルの候補を絞り込むのに使う　key prefix, value リファレンス名の配列
    roots = cmds.ls('Root', recursive=True, exactType='joint')
    # キャラモデルはリファレンス名ではなくprefixごとにまとめる
    for prefix in g_chara_prefixes:
        # 同一で複数ある場合があるので配列（例：p1_xxx.maが複数）
        chara_model_candidates[prefix] = []
    for root in roots:
        # キャラモデルは候補をあとで絞るので一旦chara_model_candidatesディクショナリの配列に格納
        for prefix in g_chara_prefixes:
            if root.startswith(prefix):
                chara_model_candidates[prefix].append(root)
                break
    # キャラモデルを絞り込む。prefxのkeyは優先順になっているはず
    chara_prefix_to_import = ''  # インポートすることになったキャラモデルのprefix
    for prefix, roots in list(chara_model_candidates.items()):
        roots = list(set(roots))
        if prefix in g_chara_prefixes:
            # 優先外のキャラモデルがあればアンロード＆ディクショナリから削除
            if chara_prefix_to_import:
                chara_model_candidates.pop(prefix)
            # 優先モデルのprefix決定
            if roots:
                chara_prefix_to_import = prefix
            else:
                # 見つからなかったprefxはディクショナリから削除
                if prefix in chara_model_candidates:
                    chara_model_candidates.pop(prefix)
    # 同じ優先prefxで複数のキャラモデルがある場合はパスが3dcg/rigのものを優先して1つ選ぶ
    roots = chara_model_candidates.get(chara_prefix_to_import)
    rig_ref_root = None
    if roots:
        roots = list(set(roots))
        for top_ref in roots:
            try:
                ref_file = cmds.referenceQuery(top_ref, filename=True)
                if ref_file.replace('\\', '/').find('/3dcg/rig/') != -1:
                    rig_ref_root = top_ref
                    break
            except Exception:
                continue
    # もし同じprefxで複数のトップノードがシーン内にあり/3dcg/rig/のものが見つからなかったら最初にみつかったものにする
    chara_node_to_use = None
    if rig_ref_root:
        chara_node_to_use = rig_ref_root
    else:
        if roots:
            chara_node_to_use = roots[0]
    # p1, p2, chrの順で優先させたキャラのリファレンス1つとそれ以外のリファレンスのリスト
    return chara_node_to_use


def get_dress_root_joints(export_root):
    root_joints = []
    dress_roots = get_dress_roots(export_root)
    for root in dress_roots:
        try:
            joints = cmds.skinCluster(root, inf=True, q=True)
            if joints:
                root_joints.append(joints[0])
        except Exception:
            pass
    root_joints = list(set(root_joints))
    return root_joints


def list_top_refs_and_filter_character():
    """キャラモデルのroot名が開発途中でchr_xxxxからp1_xxxx(男)、p2_xxxx(女)に変わった
    リファレンスがシーン内に両方混在している場合があるため、
    Mayaシーン名がchrで始まるp1またはp2で始まるものが複数ある場合、
    p1もしくはp2を優先的に1つだけ残し、あとはフィルター(アンロード)する。
    優先したキャラモデルのトップノード(例：p1_xxx)が複数ある場合、パスが3dcg/rigのものを優先して1つ選ぶ。
    読み込まれていないトップリファレンスはスルー
    Returns:
        list: キャラを1体のみにフィルターしたトップリファレンスのリスト
    """
    filtered_top_refs = []
    chara_model_candidates = {}  # キャラモデルの候補を絞り込むのに使う　key prefix, value リファレンス名の配列
    refs = cmds.ls(type='reference')
    if not refs:
        return []
    # キャラモデルはリファレンス名ではなくprefixごとにまとめる
    for prefix in g_chara_prefixes:
        # 同一で複数ある場合があるので配列（例：p1_xxx.maが複数）
        chara_model_candidates[prefix] = []
    # sharedReferenceやアンロードされているリファレンス以外のトップリファレンスをリスト
    for ref in refs:
        if ref.endswith('sharedReferenceNode'):
            continue
        top_ref = cmds.referenceQuery(ref, referenceNode=True, topReference=True)
        ref_file = cmds.referenceQuery(top_ref, filename=True, shortName=True)
        if not cmds.referenceQuery(top_ref, isLoaded=True):
            continue
        was_chara = False
        # キャラモデルは候補をあとで絞るので一旦chara_model_candidatesディクショナリの配列に格納
        for prefix in g_chara_prefixes:
            if ref_file.startswith(prefix):
                was_chara = True
                chara_model_candidates[prefix].append(top_ref)
                break
        # キャラモデル以外はtop_ref_dictに登録
        if not was_chara:
            if top_ref not in filtered_top_refs:
                filtered_top_refs.append(top_ref)
    # キャラモデルを絞り込む。prefxのkeyは優先順になっているはず
    chara_prefix_to_import = ''  # インポートすることになったキャラモデルのprefix
    for prefix, top_model_refs in list(chara_model_candidates.items()):
        top_model_refs = list(set(top_model_refs))
        if prefix in g_chara_prefixes:
            # 優先外のキャラモデルがあればアンロード＆ディクショナリから削除
            if chara_prefix_to_import:
                if top_model_refs:
                    for top_ref in top_model_refs:
                        cmds.file(unloadReference=top_ref)
                chara_model_candidates.pop(prefix)
            # 優先モデルのprefix決定
            if top_model_refs:
                chara_prefix_to_import = prefix
            else:
                # 見つからなかったprefxはディクショナリから削除
                if prefix in chara_model_candidates:
                    chara_model_candidates.pop(prefix)
    # キャラモデルがシーン内になければその他だけ返す
    if not chara_prefix_to_import:
        return filtered_top_refs
    # 同じ優先prefxで複数のキャラモデルがある場合はパスが3dcg/rigのものを優先して1つ選ぶ
    top_model_refs = chara_model_candidates.get(chara_prefix_to_import)
    found_rig_ref = ""
    if top_model_refs:
        top_model_refs = list(set(top_model_refs))
        for top_ref in top_model_refs:
            ref_file = cmds.referenceQuery(top_ref, filename=True)
            if ref_file.replace('\\', '/').find('/3dcg/rig/') != -1:
                found_rig_ref = top_ref
                break
    # もし同じprefxで複数のトップノードがシーン内にあり/3dcg/rig/のものが見つからなかったら最初にみつかったものにする
    # それ以外のモデルリファレンスはアンロードする
    if found_rig_ref:
        filtered_top_refs.append(found_rig_ref)
        for top_ref in top_model_refs:
            if top_ref != found_rig_ref:
                cmds.file(unloadReference=top_ref)
    else:
        if top_model_refs:
            for i, top_ref in enumerate(top_model_refs):
                if i == 0:
                    filtered_top_refs.append(top_ref)
                else:
                    if top_ref not in filtered_top_refs:
                        cmds.file(unloadReference=top_ref)
    # p1, p2, chrの順で優先させたキャラのリファレンス1つとそれ以外のリファレンスのリスト
    return filtered_top_refs


def import_main_chara_reference():
    """メインキャラのリファレンスをインポートする
    リファレンスインポート後のリファレンスがある
    Memo: リファレンスインポートしなくてもfbxをエクスポートできるっぽいのでいらないかも?
    Returns:
        bool: 問題がなければTrueを返す
    """
    root = get_chara_root_joint()
    if root:
        try:
            top_ref = cmds.referenceQuery(root, referenceNode=True, topReference=True)
        except Exception:
            # リファレンスじゃないのでOK
            return True
        try:
            ref_file = cmds.referenceQuery(top_ref, filename=True)
            if cmds.referenceQuery(ref_file, isLoaded=True):
                cmds.file(ref_file, importReference=True)
        except Exception:
            return False
    root = get_chara_root_joint()
    if root:
        try:
            top_ref = cmds.referenceQuery(root, referenceNode=True, topReference=True)
            if not top_ref:
                return True
            ref_file = cmds.referenceQuery(top_ref, filename=True)
            if cmds.referenceQuery(ref_file, isLoaded=True):
                cmds.file(ref_file, importReference=True)
        except Exception as ex:
            print(ex)
            return False
    return True


def update_list(scene_items):
    """シーンにあるアイテムだけのリストに更新
    Args:
        scene_items (string[]): 既存のアイテムリスト
    Returns:
        string[]: シーンにあるものだけにしたリスト
    """
    updated_list = []
    for item in scene_items:
        if cmds.ls(item):
            updated_list.append(item)
    return updated_list


def get_root_node(node):
    if not node:
        return
    parents = cmds.listRelatives(node, parent=True, fullPath=True)
    if not parents:
        return node
    else:
        for p in parents:
            return get_root_node(p)


def get_root_joints_in_scene():
    joints = cmds.ls(type='joint')
    root_joints = []
    for j in joints:
        p = cmds.listRelatives(j, parent=True, type='joint')
        if not p:
            if p not in root_joints:
                root_joints.append(j)
    return root_joints


def joint_has_skin(joints):
    if not isinstance(joints, list):
        joints = [joints]
    for joint in joints:
        cmds.select(joint, hierarchy=True)
        joint_all = cmds.ls(sl=True)
        conns = cmds.listConnections(joint_all)
        for con in conns:
            if cmds.objectType(con) == 'skinCluster':
                return True
    return False


def list_mesh_roots():
    all_top_nodes = cmds.ls(assemblies=True)
    all_cameras = cmds.listCameras()
    non_camera_roots = [x for x in all_top_nodes if x not in all_cameras]
    cmds.select(non_camera_roots, hi=True)
    meshes = cmds.ls(sl=True, long=True, type='mesh')
    mesh_roots = []
    for mesh in meshes:
        root = get_root_node(mesh)
        if root not in mesh_roots:
            mesh_roots.append(root)
    return mesh_roots


def get_roots_except_camera():
    result = []
    roots = cmds.ls(assemblies=True)
    for root in roots:
        rels = cmds.listRelatives(root, fullPath=True)
        if rels:
            for rel in rels:
                if cmds.nodeType(rel) != 'camera':
                    result.append(root)
        else:
            result.append(root)
    return result


def delete_constraint_locator(constraint, constraint_type):
    all_transforms = cmds.ls(type='transform', long=True)
    if not all_transforms:
        return
    for t in all_transforms:
        conns = cmds.listConnections(t, d=True)
        rels = cmds.listRelatives(t, fullPath=True)
        locator_transforms = []  # closestPointOnMeshのように1つのコンストレイントに2つのロケータが作成される場合もある
        if conns:
            for con in conns:
                if cmds.objectType(con) == constraint_type:
                    try:
                        if con == constraint:
                            is_locator = False
                            for rel in rels:
                                if cmds.objectType(rel) == 'locator':
                                    is_locator = True
                            if is_locator:
                                locator_transforms.append(t)
                                # Locatorの場合、子がついている場合もありそうなのでlocator削除前に移動
                                locator_children = cmds.listRelatives(t, children=True, type='transform', fullPath=True)
                                if locator_children:
                                    locator_parent = cmds.listRelatives(t, parent=True, fullPath=True)
                                    if locator_parent:
                                        cmds.parent(locator_children, locator_parent[0])
                    except Exception:
                        continue
            if locator_transforms:
                for loc in locator_transforms:
                    cmds.delete(loc)


def delete_constraint_path(constraint, constraint_type):
    # End Testing
    all_transforms = cmds.ls(type='transform', long=True)
    if not all_transforms:
        return
    for t in all_transforms:
        conns = cmds.listConnections(t, d=True)
        if conns:
            for con in conns:
                if cmds.objectType(con) == constraint_type:
                    if con == constraint:
                        try:
                            path_conns = cmds.listConnections(con)
                            cmds.select(path_conns, hi=True)
                            nurbs_curve = cmds.ls(sl=True, type='nurbsCurve')
                            if nurbs_curve:
                                for c in nurbs_curve:
                                    try:
                                        path_transform = cmds.listRelatives(c, parent=True, type='transform', fullPath=True)
                                        if path_transform:
                                            cmds.delete(path_transform)
                                    except Exception:
                                        continue
                        except Exception:
                            continue


def delete_uvpin_constraint(objects, delete_locator):
    if not objects:
        return
    for obj in objects:
        try:
            meshes = cmds.listRelatives(obj, type='mesh', fullPath=True)
            if not meshes:
                continue
            for mesh in meshes:
                conns = cmds.listConnections(mesh)
                if conns:
                    for con in conns:
                        if cmds.objectType(con) == 'uvPin':
                            if delete_locator:
                                delete_constraint_locator(con, 'uvPin')
                            cmds.delete(con)
        except Exception as ex:
            continue


def delete_proximity_pin_constraint(objects, delete_locator):
    if not objects:
        return
    for obj in objects:
        try:
            meshes = cmds.listRelatives(obj, type='mesh', fullPath=True)
            if not meshes:
                continue
            for mesh in meshes:
                conns = cmds.listConnections(mesh, d=True)
                if conns:
                    for con in conns:
                        if cmds.objectType(con) == 'proximityPin':
                            if delete_locator:
                                delete_constraint_locator(con, 'proximityPin')
                            cmds.delete(con)
        except Exception:
            continue


def delete_motion_path_constraint(objects, delete_path):
    if not objects:
        return
    for obj in objects:
        try:
            conns = cmds.listConnections(obj, source=True)
            if conns:
                for con in conns:
                    if cmds.objectType(con) == 'motionPath':
                        if delete_path:
                            delete_constraint_path(con, 'motionPath')
                        cmds.delete(con)
        except Exception as ex:
            continue


def delete_point_on_poly_constraint(objects):
    if not objects:
        return
    for obj in objects:
        try:
            meshes = cmds.listRelatives(obj, type='mesh', fullPath=True)
            if not meshes:
                continue
            for mesh in meshes:
                conns = cmds.listConnections(mesh, d=True)
                if conns:
                    for con in conns:
                        if cmds.objectType(con) == 'pointOnPolyConstraint':
                            cmds.delete(con)
        except Exception:
            continue


def delete_closest_point_on_mesh_constraint(objects, delete_locator):
    if not objects:
        return
    for obj in objects:
        try:
            meshes = cmds.listRelatives(obj, type='mesh', fullPath=True)
            if not meshes:
                continue
            for mesh in meshes:
                conns = cmds.listConnections(mesh, d=True)
                if conns:
                    for con in conns:
                        if cmds.objectType(con) == 'closestPointOnMesh':
                            if delete_locator:
                                delete_constraint_locator(con, 'closestPointOnMesh')
                            cmds.delete(con)
        except Exception as ex:
            continue


def delete_pole_vector_constraint_constraint(objects, delete_path):
    if not objects:
        return
    for obj in objects:
        try:
            if cmds.objectType(obj) == 'ikHandle':
                conns = cmds.listConnections(obj, d=True)
                if conns:
                    for con in conns:
                        if cmds.objectType(con) == 'poleVectorConstraint':
                            if delete_path:
                                delete_constraint_path(con, 'poleVectorConstraint')
                            cmds.delete(con)
        except Exception as ex:
            continue
    # 念ためikHandleから辿れない場合
    pole_vector_constraint = cmds.ls(sl=True, type='poleVectorConstraint')
    if pole_vector_constraint:
        cmds.delete(pole_vector_constraint)


def delete_constraints(delete_handle_obj):
    """
    シーン内のコンストレイントを削除
    """
    roots = get_roots_except_camera()
    cmds.select(roots, hi=True)
    all_objects = cmds.ls(sl=True)
    parent_constraints = cmds.ls(sl=True, type='parentConstraint')
    cmds.delete(parent_constraints)
    orient_constraints = cmds.ls(sl=True, type='orientConstraint')
    cmds.delete(orient_constraints)
    scale_constraints = cmds.ls(sl=True, type='scaleConstraint')
    cmds.delete(scale_constraints)
    aim_constraint = cmds.ls(sl=True, type='aimConstraint')
    cmds.delete(aim_constraint)
    geometry_constraint = cmds.ls(sl=True, type='geometryConstraint')
    cmds.delete(geometry_constraint)
    normal_constraint = cmds.ls(sl=True, type='normalConstraint')
    cmds.delete(normal_constraint)
    # tangentコンストレイントの場合はカーブを消したいとは限らない
    tangent_constraint = cmds.ls(sl=True, type='tangentConstraint')
    cmds.delete(tangent_constraint)
    delete_uvpin_constraint(all_objects, delete_handle_obj)
    delete_proximity_pin_constraint(all_objects, delete_handle_obj)
    delete_motion_path_constraint(all_objects, delete_handle_obj)
    delete_point_on_poly_constraint(all_objects)
    delete_closest_point_on_mesh_constraint(all_objects, delete_handle_obj)
    delete_pole_vector_constraint_constraint(all_objects, delete_handle_obj)
    # pointConstraintを削除すると何故かpoleVectorConstraintも消える
    # poleVectorConstraintのパスの削除上、pointConstraintは後
    cmds.select(roots, hi=True)
    point_constraints = cmds.ls(sl=True, type='pointConstraint')
    cmds.delete(point_constraints)
    print('コンストレイントを削除')
    # ikHandleも一種のコンストレイントとみなす (3Dビューワでモデル表示されなくなるので)
    iks = cmds.ls(type='ikHandle')
    if iks:
        cmds.delete(iks)
    ikeffs = cmds.ls(type='ikEffector')
    if ikeffs:
        cmds.delete(ikeffs)
    



