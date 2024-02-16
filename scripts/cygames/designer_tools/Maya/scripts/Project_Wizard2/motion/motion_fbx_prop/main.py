# -*- coding: utf-8 -*-
import os
import subprocess
import maya.cmds as cmds
import maya.mel as mel
import webbrowser
import time
import tempfile

try:
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtUiTools import QUiLoader
    from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
except Exception:
    pass
g_tool_name = 'Wiz2PropMotionFBX'
g_tool_version = '2023.10.31'
CURRENT_PATH = os.path.dirname(__file__)


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
        uiFilePath = os.path.join(CURRENT_PATH, 'wiz2_prop_motion_fbx.ui')
        self.UI = loader.load(uiFilePath)  # QMainWindow
        self.setCentralWidget(self.UI)
        self.setWindowTitle(g_tool_name + ' ' + g_tool_version)
        self.setObjectName(g_tool_name)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.UI.action_manual.triggered.connect(self.show_manual)
        scene_path = cmds.file(q=True, sn=True)
        if scene_path:
            # 現在のシーンを元にデフォルト値を設定
            file_dir = os.path.dirname(scene_path)
            self.UI.txt_out_folder.textCursor().insertText(file_dir)
        # 選択しているノード名で出力ファイル名デフォルト値を設定
        selection = cmds.ls(sl=True)
        if len(selection) == 0:
            selection = ''
        else:
            selection = selection[0]
            # namespaceの方で名付けたいっぽい(proが複数ある場合があるので)
            selection = selection.split(':')[0]
        self.UI.txt_file_name.textCursor().insertText(selection)
        # フォルダ選択
        self.UI.btn_browse_out_folder.clicked.connect(self.update_out_folder)
        # FBXエクスポート
        self.UI.btn_export_fbx.clicked.connect(self.on_export_motion_fbx)
        # 保存した設定があればセット
        self.load_settings()

    def save_setting(self, key_name, value):
        """
        optionVarに設定を保存する
        Args: 
            key_name (str): UIパーツ名
            value (any): 保存する値
        """
        cmds.optionVar(stringValue=('g_tool_name_{0}'.format(key_name), str(value)))

    def load_setting(self, key_name, default_value=''):
        """
        optionVarから保存した設定を読み込む
        Args:
            key_name (str): UIパーツ名
            default_value (any): 保存データがないの場合デフォルトを指定
        """
        result = default_value
        if not cmds.optionVar(exists='g_tool_name_{0}'.format(key_name)):
            return result
        result = cmds.optionVar(query='g_tool_name_{0}'.format(key_name))
        return result

    def save_settings(self):
        """
        Window init時に設定を読み込む
        """
        self.save_setting('txt_out_folder', self.UI.txt_out_folder.toPlainText())
        self.save_setting('chk_open_out_folder', self.UI.chk_open_out_folder.checkState())
        self.save_setting('chk_keep_edited_scene_open', self.UI.chk_keep_edited_scene_open.checkState())

    def load_settings(self):
        """
        Windowクローズ時に設定を保存
        """
        # 「出力フォルダ」テキストフィールド
        desktop_dir = os.path.abspath(os.path.join(os.path.expanduser('~'), '..', 'Desktop'))
        out_dir = self.load_setting('txt_out_folder', desktop_dir)
        if out_dir:
            self.UI.txt_out_folder.setText(out_dir)
        # 「エクスポート後フォルダを開く」チェックボックス
        open_out_folder = self.load_setting('chk_open_out_folder', QtCore.Qt.CheckState.Checked)
        if open_out_folder:
            if open_out_folder == str(QtCore.Qt.CheckState.Checked):
                self.UI.chk_open_out_folder.setChecked(QtCore.Qt.CheckState.Checked)
            else:
                self.UI.chk_open_out_folder.setChecked(QtCore.Qt.CheckState.Unchecked)
        else:
            self.UI.chk_open_out_folder.setChecked(True)
        # 「エクスポート後のシーンをそのまま開いておく」チェックボックス
        keep_edited_scene_open = self.load_setting('chk_keep_edited_scene_open', QtCore.Qt.CheckState.Unchecked)
        if keep_edited_scene_open == str(QtCore.Qt.CheckState.Checked):
            self.UI.chk_keep_edited_scene_open.setChecked(True)
        else:
            self.UI.chk_keep_edited_scene_open.setChecked(False)

    def validate_prop_export(self):
        """Prop FBXエクスポートValidation
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
        # FPSチェック
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
        selection = cmds.ls(sl=True)
        if len(selection) != 1:
            cmds.confirmDialog(title='Usage', message='propを一つ選択して実行してください',
                               button=['OK'])
            return False
        return True

    def on_export_motion_fbx(self):
        """「FBXエクスポート」ボタン実行
        """
        if not self.validate_prop_export():
            return
        txt_out_folder = self.UI.txt_out_folder.toPlainText()
        txt_out_folder = txt_out_folder.replace('\\', '/')
        txt_file_name = self.UI.txt_file_name.toPlainText()
        error_msg_dict = {}
        exported = export_motion_fbx(txt_out_folder,
                                     txt_file_name,
                                     show_popup=True,
                                     error_msg_dict=error_msg_dict)
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

    def show_manual(self):
        """コンフルのツールマニュアルページを開く
        """
        try:
            webbrowser.open('https://wisdom.cygames.jp/pages/viewpage.action?pageId=513849649#id-%E3%80%90Motion%E3%80%91FBX%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%9D%E3%83%BC%E3%82%BF%E3%83%BC-Prop%E3%81%AEFBX%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%9D%E3%83%BC%E3%83%88')
        except Exception:
            cmds.warning('マニュアルページがみつかりませんでした')

    def closeEvent(self, event):
        try:
            self.save_settings()
        except Exception:
            pass


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


def export_motion_fbx(out_folder, fbx_name,
                      show_popup=True, error_msg_dict={}):
    """ 現在選択しているノード（propを想定）のScaleモーションのfbxをエクスポートします。
    propリファレンスをインポート、ネームスペース削除、キーをベイク、
    エクスポートのプリセットはモーション班提供の以下を仕様
     - wizard2_motion.fbxexportpreset (インゲーム用fbx)
    Args:
        out_folder (str): 出力フォルダのパス
        fbx_name (str): 書き出すfbxファイル名
        show_popup (bool, optional): ポップアップを表示するか. Defaults to True.
        error_msg_dict (dict, optional): 詳細のWarning/Errorメッセージを受け取りたい場合に渡す. Defaults to {}.
    Returns:
        bool: 最後までエクスポートできたらTrueを返す
    """
    scene_path = cmds.file(q=True, sn=True)
    selection = cmds.ls(sl=True)
    if not selection:
        return
    # ネームスペース削除
    if not pre_remove_namespace(selection):
        return
    selection = remove_namespace(selection)  # 1個のはず
    print('ネームスペース削除')
    if not selection:
        if show_popup:
            cmds.confirmDialog(title='エラー', message='Propのネームスペースの削除ができませんでした\n' +
                               'File > Reference Editor で propのリファレンスをリロード、もしくは\n' +
                               'シーンを一旦保存し、シーンを開きなおしてから実行してください\n' +
                               'キャンセルします', button=['OK'])
        return False
    # 選択の中のRootジョイント
    cmds.select(selection, hierarchy=True)
    root_joints = cmds.ls('Root', selection=True, type='joint', long=True)
    if not root_joints:
        add_to_dict(scene_path, 'Error: Rootジョイントが見つかりませんでした', error_msg_dict)
        return False
    if not root_joints:
        if show_popup:
            cmds.confirmDialog(title='確認', message='「Root」ジョイントが選択内にありません\n' +
                               '（ロードされたリファレンスがない? ネームスペースがある?）\n' +
                               'キャンセルします', button=['OK'])
        # エラーログ用
        add_to_dict(scene_path, 'Error:「Root」ジョイントが選択内にありません' +
                    '(ロードされたリファレンスがない? ネームスペースがある?)', error_msg_dict)
        return False
    print('選択の中のRootジョイント: ' + ', '.join(root_joints))
    # Handattach_L/R_ctrl以外のものはpropLocalSpaceをworld_ctr(0)にセット
    hand_attach_ctrl = find_ctrl_hand_attatch(root_joints)
    if not hand_attach_ctrl:
        print('ハンドアタッチではない')
        ctrl = find_ctrl_with_prop_local_space(root_joints)
        if ctrl:
            cmds.setAttr('{}.propLocalSpace'.format(ctrl), 0)
            print('Prop Local Spaceをworld_ctrlに: ' + ctrl)
        else:
            cmds.warning('PropAttachのctrlが見つかりませんでした')
    else:
        print('ハンドアタッチ: ' + hand_attach_ctrl)
    # Rootジョイント配下を選択してベイク
    attrs_to_bake = ['rotateX', 'rotateY', 'rotateZ',
                     'translateX', 'translateY', 'translateZ',
                     'scaleX', 'scaleY', 'scaleZ']
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
    print('Rootジョイント配下を選択してベイク')
    # RootのScale 以外のキーを削除
    attrs = cmds.listAttr(root_joints, keyable=True)
    attrs.remove('scaleX')
    attrs.remove('scaleY')
    attrs.remove('scaleZ')
    # キーを削除したあと値を0にするアトリビュート
    zero_attrs = ['rotateX', 'rotateY', 'rotateZ',
                  'translateX', 'translateY', 'translateZ']
    if hand_attach_ctrl:
        # RootのScale以外を0に
        for sel in root_joints:
            for attr in attrs:
                cmds.cutKey(sel, attribute=attr, time=(), option='keys')
                # Translate, Rotateは0
                if attr in zero_attrs:
                    cmds.setAttr('{}.{}'.format(sel, attr), 0)
        print('ハンドアタッチなのでRootのScale以外を0に')
    # リファレンスで消せないもの以外を削除（コンストレイントを削除する目的）
    try:
        cmds.SelectAll()
        cmds.SelectHierarchy()
        for_delete = cmds.ls(sl=True)
        cmds.delete(for_delete)
    except Exception:
        pass
    print('リファレンスで消せないもの以外を削除（コンストレイントを削除する目的）')
    # レイヤーが削除できないのでリファレンスをdefaultLayerに移動
    selection = update_list(selection)
    all = cmds.listRelatives(selection, ad=True, fullPath=True)
    belong_layers = cmds.listConnections(all, type='displayLayer')
    if belong_layers:
        belong_layers = list(set(belong_layers))
        for layer in belong_layers:
            member = cmds.editDisplayLayerMembers(layer, query=True, fullNames=True)
            cmds.editDisplayLayerMembers('defaultLayer', member)
    print('レイヤーが削除できないのでリファレンスをdefaultLayerに移動')
    # ディスプレイレイヤーを削除
    displayLayers = cmds.ls(type='displayLayer')
    for layer in displayLayers:
        if layer.find('defaultLayer') == -1:
            cmds.delete(layer)
    print('ディスプレイレイヤーを削除')
    # 念のためジョイント表示
    root_joints = update_list(root_joints)
    cmds.showHidden(root_joints, below=True)
    print('念のためジョイント表示')
    # RootのScaleが完全に0だと法線がおかしくなるかもしれないのでチェック
    for root in root_joints:
        check_scale(root)
    # Outlineを消す
    child_meshes = list_child_mesh_transforms(selection)
    for mesh in child_meshes:
        if mesh.endswith('_Outline'):
            # 参照情報が削除されコピー先の情報もなくなることがあるので念のためヒストリー削除
            cmds.delete(mesh, constructionHistory=True)
            cmds.delete(mesh)
    print('Outlineを消す')
    try:
        # この処理でのFBXプリセットを設定する（Maya本体のプリセットは変わらない）
        preset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.',
                                      'wizard2_motion.fbxexportpreset')).replace('\\', '/')
        mel.eval('FBXLoadExportPresetFile -f "{}"'.format(preset_path))
        cmds.select(selection, hierarchy=True)
        export_path = out_folder + '/' + fbx_name + '.fbx'
        mel.eval('FBXExport -f "{0}" -s'.format(export_path))
    except Exception as ex:
        print(str(ex))
        return
    print('エクスポート完了（Embed Mediaなし）: ' + export_path)
    return True


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


def pre_remove_namespace(selection):
    """remove_namespaceの前に、ネームスペースを取ったオブジェクトがバッティングしないかチェック
    バッティングするオブジェクトがある場合、ReferenceならUnload, そうでなければDeleteして良いかユーザーに聞く
    Args:
        selection (bool): remove_namespaceを実行して大丈夫ならTrue
    """
    if isinstance(selection, str):
        selection = [selection]
    for sel in selection:
        if sel.find(':') > -1:
            name = sel.split(':')[-1]
            if cmds.ls(name):
                if cmds.referenceQuery(name, isNodeReferenced=True):
                    top_ref = cmds.referenceQuery(name, referenceNode=True, topReference=True)
                    if not top_ref:
                        return False
                    file_name = cmds.referenceQuery(top_ref, filename=True)
                    if not file_name:
                        return False
                    user_choice = cmds.confirmDialog(title='確認',
                                                    message='ネームスペースを取った後の名前と同名のReferenceがあります\n' +
                                                    'Unloadして続行しますか?\n\n' +
                                                    '先に別のpropをエクスポートしている場合シーン内のコンストレイントが削除されて結果が変わっているかもしれません\n' +
                                                    'propエクスポートごとにシーンを開きなおしてエクスポートすることをおすすめします',
                                                    button=['OK', 'Cancel'],
                                                    defaultButton='OK',
                                                    cancelButton='Cancel',
                                                    dismissString='Cancel')
                    if user_choice == 'OK':
                        cmds.file(file_name, unloadReference=True)
                        return True
                    else:
                        return False
                else:
                    try:
                        cmds.delete(name)
                        return True
                    except Exception:
                        return False
    return True

def remove_namespace(selection):
    """ネームスペースを削除
    Args:
        selection (str[]): ネームスペースを削除したい選択アイテム
    Returns:
        str[]: ネームスペース削除後の選択アイテム名の配列
    """
    if not selection:
        return
    if isinstance(selection, str):
        selection = [selection]
    results = []
    remove_namespace = []
    # ネームスペース削除後のノード名を返すための配列を作成
    for sel in selection:
        name = sel.split(':')[0]
        if name == sel:
            results.append(sel)
        else:
            if not name in remove_namespace:
                remove_namespace.append(name)
            # 入れ子のネームスペースは未対応
            name_without_namespace = sel.split(':')[-1]
            results.append(name_without_namespace)
    try:
        for name in remove_namespace:
            cmds.namespace(removeNamespace=name, mergeNamespaceWithRoot=True)
    except Exception as ex:
        cmds.warning(ex)
        return []
    return results


def import_prop_reference(selection):
    """選択アイテムがリファレンスだったらインポートする
    Memo: リファレンスインポートしなくてもfbxをエクスポートできるっぽいのでいらないかも?
    Returns:
        bool: 問題がなければTrueを返す
    """
    try:
        if len(selection) != 1:
            cmds.confirmDialog(title='Usage', message='propのRootを一つ選択して実行してください',
                               button=['OK'])
            return False
        top_ref = cmds.referenceQuery(selection[0], referenceNode=True, topReference=True)
        ref_file = cmds.referenceQuery(top_ref, filename=True)
        cmds.file(ref_file, importReference=True)
    except Exception as ex:
        if len(selection) != 1:
            cmds.confirmDialog(title='Error', message=ex, button=['OK'])
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
    if scene_items:
        for item in scene_items:
            if cmds.ls(item):
                updated_list.append(item)
    else:
        print('update_list no items to update')
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


def find_ctrl_hand_attatch(sel, visited=[]):
    """
    再帰的にpropLocalSpaceアトリビュートのあるctrlを探す
        Args: 
            sel (str): 検索オブジェクト
            visited (str[]): 一度探した場所は探さないようにするために使う
    """
    hand_attatch_ctrls = ['Handattach_L_ctrl', 'Handattach_R_ctrl']
    if type(sel) == list:
        sel = sel[0]
    if not cmds.objExists(sel):
        return
    if cmds.objectType(sel) == 'transform' or cmds.objectType(sel) == 'joint':
        rels = cmds.listRelatives(sel, ad=True, fullPath=True)
        if not rels:
            return
        for rel in rels:
            if rel in visited:
                continue
            if not rel in visited:
                visited.append(rel)
            if rel.lower().find('constraint') > -1:
                conns = cmds.listConnections(rel)
                if conns:
                    conns = list(set(conns))
                for con in conns:
                    if con in visited:
                        continue
                    if not con in visited:
                        visited.append(con)
                    if con.lower().find('_ctrl') > -1:
                        for hand_attatch_ctrl in hand_attatch_ctrls:
                            if con.find(hand_attatch_ctrl) > -1:
                                return con
                        else:
                            return find_ctrl_hand_attatch(con, visited)
                break
        # 一階層上がって探す
        p = cmds.listRelatives(sel, parent=True, fullPath=True)
        if p:
            return find_ctrl_hand_attatch(p[0], visited)
    elif sel.lower().find('constraint') > -1:
        conns = cmds.listConnections(sel)
        if not conns:
            return
        conns = list(set(conns))
        for con in conns:
            if con in visited:
                continue
            if not con in visited:
                visited.append(con)
            if con.lower().find('_ctrl') > -1:
                for hand_attatch_ctrl in hand_attatch_ctrls:
                    if con.find(hand_attatch_ctrl) > -1:
                        return con
                    else:
                        result = find_ctrl_hand_attatch(con, visited)
                        if result:
                            return result
                        else:
                            p = cmds.listRelatives(con, parent=True, fullPath=True)
                            if p:
                                return find_ctrl_hand_attatch(p[0], visited)


def find_ctrl_with_prop_local_space(sel, visited=[]):
    """
    再帰的にpropLocalSpaceアトリビュートのあるctrlを探す
        Args: 
            sel (str): 検索オブジェクト
            visited (str[]): 一度探した場所は探さないようにするために使う
    """
    if type(sel) == list:
        sel = sel[0]
    if not cmds.objExists(sel):
        return
    if cmds.objectType(sel) == 'transform' or cmds.objectType(sel) == 'joint':
        rels = cmds.listRelatives(sel, ad=True, fullPath=True)
        if not rels:
            return
        for rel in rels:
            if rel in visited:
                continue
            if not rel in visited:
                visited.append(rel)
            if rel.lower().find('constraint') > -1:
                conns = cmds.listConnections(rel)
                if conns:
                    conns = list(set(conns))
                for con in conns:
                    if con in visited:
                        continue
                    if not con in visited:
                        visited.append(con)
                    if con.lower().find('_ctrl') > -1:
                        if cmds.attributeQuery('propLocalSpace', node=con, ex=True):
                            return con
                        else:
                            return find_ctrl_with_prop_local_space(con, visited)
                break
        # 一階層上がって探す
        p = cmds.listRelatives(sel, parent=True, fullPath=True)
        if p:
            return find_ctrl_with_prop_local_space(p[0], visited)
    elif sel.lower().find('constraint') > -1:
        conns = cmds.listConnections(sel)
        if not conns:
            return
        conns = list(set(conns))
        for con in conns:
            if con in visited:
                continue
            if not con in visited:
                visited.append(con)
            if con.lower().find('_ctrl') > -1:
                if cmds.attributeQuery('propLocalSpace', node=con, ex=True):
                    return con
                else:
                    result = find_ctrl_with_prop_local_space(con, visited)
                    if result:
                        return result
                    else:
                        parents = cmds.listRelatives(con, allParents=True, fullPath=True)
                        for p in parents:
                            return find_ctrl_with_prop_local_space(p, visited)

def check_scale(root):
    scale_attrs = ['scaleX', 'scaleY', 'scaleZ']
    found_zero_scale = False
    for attr in scale_attrs:
        if found_zero_scale:
            break
        times = cmds.keyframe('{0}.{1}'.format(root, attr), query=True)
        for time in times:
            vals = cmds.keyframe('{0}.{1}'.format(root, 'scale'), query=True, t=(time,time), valueChange=True)
            for val in vals:
                if val == 0:
                    found_zero_scale = True
                    break
    if found_zero_scale:
        # ワーニングのみ
        cmds.confirmDialog(title='Warning',
                           message='スケール値が0のキーがありました\n' +
                           '法線に問題が出るかもしれないので0にはしないでください')
        return False
    return True


def set_zero_scale_key_to_val(root, replace_to):
    scale_attrs = ['scaleX', 'scaleY', 'scaleZ']
    for attr in scale_attrs:
        times = cmds.keyframe('{0}.{1}'.format(root, attr), query=True)
        for time in times:
            vals = cmds.keyframe('{0}.{1}'.format(root, 'scale'), query=True, t=(time,time), valueChange=True)
            for val in vals:
                if val == 0:
                    cmds.setKeyframe('{0}.{1}'.format(root, 'scale'), time=(time), value=replace_to)
