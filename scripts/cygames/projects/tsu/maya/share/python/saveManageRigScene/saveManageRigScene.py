# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : saveManageRigScene
# Author  : toi
# Version : 0.1.7
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
# import maya.mel as mm
import pymel.core as pm
import os
import stat
import re
import datetime
from functools import partial
from dccUserMayaSharePythonLib import common as cm
# from dccUserMayaSharePythonLib import pyCommon as pcm
from dccUserMayaSharePythonLib import file_dumspl as f
from dccUserMayaSharePythonLib import tsubasa_dumspl as tsubasa
from dccUserMayaSharePythonLib import skinning as sk
from dccUserMayaSharePythonLib import ui
from autoNormalize import autoNormalize


# reload(tsubasa)
# reload(ui)
# reload(autoNormalize)


def getDate():
    return str(datetime.date.today()).replace('-', '')


def optimiseForExport():
    id_ = tsubasa.getId(cmds.file(q=True, sn=True))
    assemblies = [x for x in cmds.ls(assemblies=True) if not pm.nodeType(pm.PyNode(x).getShape()) == 'camera']

    for assemblie in assemblies:
        if assemblie != id_:
            cmds.delete(assemblie)

    rig_groups = pm.PyNode(id_).getChildren()
    for g in rig_groups:
        if g.name() == 'rig_GP':
            pm.delete(g)


def openCurrentDir():
    os.startfile(os.path.normpath(os.path.dirname(cmds.file(q=True, sn=True))))


def savePath(path_, reverse_scene_name=False):
    """path_の名前で保存"""

    if os.path.isfile(path_):
        os.chmod(path_, stat.S_IWRITE)

    current_scene = cmds.file(q=True, sn=True)
    cmds.file(rename=path_)
    cmds.file(s=True, f=True)
    if reverse_scene_name:
        cmds.file(rename=current_scene)


def saveToExport(path_):
    """出力用に保存"""

    if os.path.isfile(path_):
        os.chmod(path_, stat.S_IWRITE)

    current_scene = cmds.file(q=True, sn=True)

    # cmds.undoInfo(openChunk=True)

    # 最適化
    # optimiseForExport()

    cmds.file(rename=path_)
    cmds.file(s=True, f=True)
    # cmds.undoInfo(closeChunk=True)

    # cmds.undo()

    cmds.file(rename=current_scene)


def exportFbxForMb(path_):
    """MB用にfbx出力"""

    if os.path.isfile(path_):
        os.chmod(path_, stat.S_IWRITE)

    cmds.undoInfo(openChunk=True)
    from rigSupportTools import ui as rstui
    rstui.rigSupportToolsUI().materialReplacement()
    cmds.undoInfo(closeChunk=True)

    f.exportFbx(path_)

    cmds.undo()


def startPalette():
    import palette.ui
    palette.ui.showUI()


def copyClipboardSubmitCommentTmp(id_):
    if not id_:
        return

    cate = id_[:2]
    id_num = id_[2:]
    cate_face = 'f' + cate[0]
    cate_wep = 'w' + cate[0]

    submit_comment_tmp = r'''@art_motion @art_cut @art_facial @art_rig @eng_battle @cygames_rig
お疲れ様です。
{0}: {1} の仮Setupデータをサブミット致しました。

更新ID
```{0} : {1}
{6}
{7}```

更新データ
```MotionBuilder：
d:\cygames\tsubasa\work\chara\{2}\{0}\rig\motionbuilder\{0}.fbx

Maya：
d:\cygames\tsubasa\work\chara\{2}\{0}\rig\maya\{0}.mb
{8}
{9}```

更新内容
```・仮Setup```

仕様書
```Rig: {0}: {1}
https://wisdom.cygames.jp/x/JEq8Bg```

Assist drive csvファイル
```d:\cygames\tsubasa\work\chara\{2}\{0}\rig\_data\_assistdrive\{0}.csv```

併せてコミット準備ができました。ローカル環境にて確認済みです。
各パートご確認の上、コミットして問題ないようでしたらステータスの変更をお願い致します。
```Rig: Commit Status: コミットステータス (社内向け)
https://wisdom.cygames.jp/pages/viewpage.action?pageId=170377659```

何かご不明な点や不備など御座いましたらご連絡下さい。
宜しくお願い致します。
'''
    face_id_comment = ''
    face_path_commect = ''
    if cate_face + id_num in tsubasa.ID:
        face_id_comment = cate_face + id_num + ' : ' + tsubasa.ID[cate_face + id_num]
        face_path_commect = r'd:\cygames\tsubasa\work\chara\{1}\{1}{0}\rig\maya\{1}{0}.mb'.format(id_num, cate_face)

    w_id_comment = ''
    w_path_comment = ''
    if cate_wep + id_num in tsubasa.ID:
        w_id_comment = cate_wep + id_num + ' : ' + tsubasa.ID[cate_wep + id_num]
        w_path_comment = r'd:\cygames\tsubasa\work\chara\{1}\{1}{0}\rig\maya\{1}{0}.mb'.format(id_num, cate_wep)

    charaname = '*' if id_ not in tsubasa.ID else tsubasa.ID[id_]
    submit_comment_tmp = submit_comment_tmp.format(
        id_, charaname, cate, id_num, cate_face, cate_wep,
        face_id_comment, w_id_comment, face_path_commect, w_path_comment)

    cm.toClip(submit_comment_tmp)


class Ui(object):
    SETTING_DIR = os.path.join(os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"), 'Documents', 'maya', 'Scripting_Files')
    SETTING_JSON = os.path.join(SETTING_DIR, 'saveManageRigScene.json')
    if not os.path.isfile(SETTING_JSON):
        f.exportJson(SETTING_JSON)

    setting_dict = f.importJson(SETTING_JSON)

    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))

        # ui初期化
        self.tx_current_dir = None
        self.tx_current_scene_name = None
        self.tf_id = None
        self.mi_ofas = None
        self.tf_versionup = None
        self.tf_to_mb = None
        self.tf_to_data = None
        self.tf_to_export = None
        self.tf_to_server = None

        # 設定辞書初期化
        server_root = '//cydrive01/100_projects/115_tsubasa/40_Artist/08_Rig/data/user'
        self.my_server_path = self.setting_dict['server_path'] if 'server_path' in self.setting_dict else server_root
        self.cb_val_ofas = self.setting_dict[
            'openFolderAfterSave'] if 'openFolderAfterSave' in self.setting_dict else False
        self.cb_val_cas = self.setting_dict['clipAfterSave'] if 'clipAfterSave' in self.setting_dict else False

    def delOverwrapWindow(self):
        if cmds.window(self.window_name, ex=True):
            pm.deleteUI(self.window_name)

    def frame(
        self, label_, ann_, command_, ofe=False,
        button_label='Save', button_col=(0.31, 0.31, 0.31), i_='fileSave.png',):
        pm.columnLayout(adj=True, bgc=(0.18, 0.23, 0.23), ann='<big>' + ann_, rs=2)

        hl = pm.horizontalLayout(ratios=(8, 1))
        pm.text(l='<big>' + label_, al='left')
        # if ofe:
        # pm.button(
        #	l='Optimise Scene', h=16, bgc=(0.31, 0.31, 0.31),
        #	ann='rig_GPは不要なので削除します。またメイン階層以外の階層も削除します',
        #	c=pm.Callback(optimiseForExport))
        # pm.iconTextButton(
        #	l='Pallet', h=16, bgc=(0.31, 0.31, 0.31), st='iconAndTextHorizontal',
        #	ann='Palletを起動します（Data Management: for Export で最適化してください）',
        #	c=pm.Callback(startPalette), i='setEdEditMode.png')
        hl.redistribute()
        pm.setParent('..')

        hl = pm.horizontalLayout(ratios=(0, 0, 0, 8, 1))
        itb = pm.iconTextButton(
            i='SP_DirClosedIcon.png', st='iconOnly', bgc=(0.31, 0.31, 0.31),
            ann='<big>パスのフォルダをエクスプローラで開きます')
        itb2 = pm.iconTextButton(
            i='folder-open.png', st='iconOnly', bgc=(0.31, 0.31, 0.31),
            ann='<big>シーンを開きます')
        bt = pm.button(
            l='C', bgc=(0.31, 0.31, 0.31),
            ann='<big>パスをクリップボードにコピーします')
        tf = pm.textField()
        pm.iconTextButton(
            l=button_label, i=i_, st='iconAndTextHorizontal',
            c=pm.Callback(command_), bgc=button_col)
        hl.redistribute()
        pm.setParent('..')

        pm.iconTextButton(itb, e=True, c=pm.Callback(self.openTfDir, tf))
        pm.iconTextButton(itb2, e=True, c=pm.Callback(self.openTfScene, tf))
        pm.button(bt, e=True, c=pm.Callback(self.copyClipTfPath, tf))
        return tf

    def collapseFrame(self, collapse=True):
        if collapse:
            pm.window(self.window_name, e=True, h=20)
        else:
            pm.window(self.window_name, e=True, h=475)

    def initUi(self):
        self.delOverwrapWindow()
        pm.window(self.window_name, t=self.window_name, w=400, mb=True)
        # fl = pm.formLayout()
        fl = pm.frameLayout(
            cll=True, l='', bgc=(0.18, 0.23, 0.23),
            cc=pm.Callback(self.collapseFrame),
            ec=pm.Callback(self.collapseFrame, False)
        )
        self.cl = pm.columnLayout(adj=True, rs=3, co=['both', 2])

        # menu
        pm.menu(l='Options')
        pm.menuItem(d=True, l='After Save')
        self.mi_ofas = pm.menuItem(
            l='Open folder', cb=self.cb_val_ofas, c=pm.Callback(self.changeCbOfas),
            ann='セーブ後に対象のフォルダを開きます')
        self.mi_cas = pm.menuItem(
            l='Copy path to Clipboard', cb=self.cb_val_cas, c=pm.Callback(self.changeCbCas),
            ann='セーブ後に対象のパスをクリップボードにコピーします')
        pm.menuItem(d=True)
        pm.menuItem(l='Regist my server path', c=pm.Callback(self.registServer))
        pm.menuItem(d=True)
        pm.menuItem(l='slack 用コメントをクリップボードにコピー', c=pm.Callback(self.runCopyClipboardSubmitCommentTmp))
        pm.menu(l='Help')
        pm.menuItem(l='Tool help', c=pm.Callback(os.startfile, 'https://wisdom.cygames.jp/x/krQrCw'))

        # ---------------------------------
        # pm.separator()
        pm.columnLayout(adj=True, co=['both', 5])
        self.tf_current_dir = pm.textField(ed=False)
        hl = pm.horizontalLayout(ratios=(0, 0.8, 0.18, 0.16, 0.2, 0.16))
        self.tx_current_scene_name = pm.text(al='left')
        pm.text(l='')
        pm.button(l='Norm Skin', c=pm.Callback(self.normMesh), ann='Prune, Round, Max Influence を最適化します')
        pm.iconTextButton(
            l='Pallet', h=16, bgc=(0.36, 0.36, 0.36), st='iconAndTextHorizontal',
            ann='Palletを起動します（Data Management: for Export で最適化してください）',
            c=pm.Callback(startPalette), i='setEdEditMode.png')
        pm.button(l='Check Tool', c=pm.Callback(self.checktool))
        pm.button(l='Exporter', c=pm.Callback(self.exporter))
        #pm.iconTextButton(
        #    l='UIリセット', h=16, bgc=(0.25, 0.33, 0.33), st='iconAndTextHorizontal',
        #    c=pm.Callback(self.sjWork), i='redrawPaintEffects.png')
        hl.redistribute()

        # ---------------------------------
        pm.setParent(self.cl)
        pm.separator()
        hl2 = pm.horizontalLayout(ratios=(0, 0, 0, 2.5, 0.5, 0.5))
        # self.tx_id = pm.text(al='right')
        pm.button(l='idList', c=pm.Callback(self.openIdList))
        self.tf_id = pm.textField(cc=pm.Callback(self.runSjWorkFromIdTf), w=60)
        self.tx_charaname = pm.textField(w=240)
        pm.text(l='')
        pm.button('Idle motion', c=pm.Callback(self.loadIdleMotion))
        pm.button('Select motion', c=pm.Callback(self._charaMotionImport))
        hl2.redistribute()

        pm.setParent(self.cl)
        pm.separator()
        hl3 = pm.horizontalLayout(ratios=(0, 0, 0, 0, 2.5, 0.5, 0.5))
        pm.text(l='Open Folder : ')
        pm.iconTextButton(
            l='Current Scene', i='SP_DirClosedIcon.png', st='iconAndTextHorizontal',
            c=pm.Callback(openCurrentDir))
        pm.iconTextButton(
            l='p4v ( Perforce )', i='SP_DirClosedIcon.png', st='iconAndTextHorizontal',
            c=pm.Callback(tsubasa.openCurrentIdDir))
        pm.iconTextButton(
            l='Server', i='SP_DirClosedIcon.png', st='iconAndTextHorizontal',
            c=pm.Callback(self.openMyServer))
        pm.text(l='')
        pm.button(l='出力の掟を読む', c=r'os.startfile("https://wisdom.cygames.jp/x/rp07Fw")')
        pm.button(l='チェックシーン', c=pm.Callback(self.sceneCheck))
        hl3.redistribute()

        pm.setParent(fl)
        sl = pm.scrollLayout(cr=True)
        cl_in_sl = pm.columnLayout(adj=True)

        # ---------------------------------
        pm.frameLayout(l='Local', cll=True, mh=2, mw=2)
        mes = 'バージョン を カウントアップして保存'
        self.tf_versionup = self.frame(
            'Save Scene Version CountUp : {0}'.format(mes), mes, self.startVersionup,
            button_col=(0.7, 0.3, 0.3))
        # pm.separator()
        # mes = 'MotionBuilder用の .fbx を出力'
        # self.tf_to_mb = self.frame(
        #	'Export Fbx : {0}'.format(mes), 'テクスチャを最適化してから出力します',
        #	self.startExportFbx, button_label='Export', i_='teGameExporter.png')

        # ---------------------------------
        pm.setParent(cl_in_sl)
        pm.frameLayout(l='p4v ( Perforce )', cll=True, mh=2, mw=2)
        mes = '「 出力用シーン 」 の保存'
        self.tf_to_export = self.frame(
            '[ rig/maya ] : {0}'.format(mes),
            '', self.startToExport, ofe=True, button_col=(0.7, 0.7, 0.3))
        pm.separator()
        mes = '「 作業用シーン 」 の保存'
        self.tf_to_data = self.frame(
            '[ rig/_data/scenes/maya ]　: {0}'.format(mes), mes, self.startToData,
            button_col=(0.3, 0.7, 0.3))

        # ---------------------------------
        pm.setParent(cl_in_sl)
        pm.frameLayout(l='Server', cll=True, mh=2, mw=2)
        mes = '受け渡し用のサーバーフォルダへ保存'
        self.tf_to_server = self.frame(
            'Save Scene to Server （ サーバへ一時保存 ）', mes, self.startToServer,
            button_col=(0.3, 0.3, 0.7))

        # レイアウト調整
        # pm.formLayout(fl, e=True, af=[(self.cl, 'top', 0), (self.cl, 'left', 5), (self.cl, 'right', 5)])
        # pm.formLayout(fl, e=True, af=[(sl, 'top', 120), (sl, 'left', 5), (sl, 'right', 5), (sl, 'bottom', 5)])

        pm.scriptJob(p=self.window_name, e=['SceneOpened', pm.Callback(self.sjWork)])
        pm.scriptJob(p=self.window_name, e=['SceneSaved', pm.Callback(self.sjWork)])
        # pm.scriptJob(p=self.window_name, e=['PostSceneRead', pm.Callback(self.sjWork)])
        pm.showWindow(self.window_name)
        self.sjWork()

    # ---------------------------------------------------------------------------------
    # 開始処理
    # ---------------------------------------------------------------------------------
    def startVersionup(self):
        path_ = self.tf_versionup.getText()
        if path_:
            if os.path.isfile(path_):
                pm.warning('既にファイルが存在するのでファイル名を見直してください')
                return

            savePath(path_)
            self.sjWork()
            self.afterSaveOption(os.path.normpath(os.path.dirname(cmds.file(q=True, sn=True))))
            pm.mel.addRecentFile(path_.replace(os.sep, '/'), 'mayaBinary')
            self.end_ivm(path_)

    def startExportFbx(self):
        path_ = self.tf_to_mb.getText()
        if path_:
            res = self.startConfirm(path_, 'テクスチャをMB用に変換してからfbxを出力します')
            if res != 2:
                self.confirmExistsDir(path_)
                exportFbxForMb(path_)
                self.afterSaveOption(path_)
                self.end_ivm(path_, 'fbx出力しました')

    def startToData(self):
        path_ = self.tf_to_data.getText()
        if path_:
            res = self.startConfirm(path_, '_data に このシーンをそのまま保存します')
            if res != 2:
                self.confirmExistsDir(path_)
                savePath(path_, True)
                self.afterSaveOption(path_)
                self.end_ivm(path_)

    def startToExport(self):
        path_ = self.tf_to_export.getText()
        if path_:
            res = self.startConfirm(path_, '現在のリグのシーンを　p4vのサブミットパスに保存します')
            if res != 2:
                self.confirmExistsDir(path_)
                saveToExport(path_)
                self.afterSaveOption(path_)
                self.end_ivm(path_)
                response = cmds.confirmDialog(
                    title='Confirm', message='保存したシーンを開きますか？\n\n' + path_,
                    button=['開く', '開かない'], dismissString='開かない', p=self.window_name)
                if response == '開く':
                    cmds.file(path_, o=True, f=True)

    def startToServer(self):
        path_ = self.tf_to_server.getText()
        if path_:
            res = self.startConfirm(path_, '現在のリグのシーンを 受け渡し用のサーバーフォルダへ保存します')
            if res != 2:
                self.confirmExistsDir(path_)
                savePath(path_, True)
                self.afterSaveOption(path_)
                self.end_ivm(path_)

    # ---------------------------------------------------------------------------------
    def startConfirm(self, path_, message_):
        ex = False
        if os.path.isfile(path_):
            ex = True

        # save = '保存してから実行'
        # no_save = '保存しないで実行'
        if ex:
            save = '上書き保存'
        else:
            save = '保存'
        cancel = '中止'
        # button_dict = {save: 0, no_save: 1, cancel: 2}
        button_dict = {save: 0, cancel: 2}
        # message_ += '\n\n※指定先に保存する前に、現在のシーンを上書き保存しますか？'
        response = cmds.confirmDialog(
            title='Confirm', message=message_, button=[save, cancel],
            defaultButton=save, cancelButton=cancel, dismissString=cancel,
            p=self.window_name)
        if response == 0:
            cmds.file(s=True, f=True)
        return button_dict[response]

    def confirmExistsDir(self, path_):
        base_dir = os.path.dirname(path_)
        if not os.path.isdir(base_dir):
            response = cmds.confirmDialog(
                title='Confirm', message='フォルダが存在しないので作成します\n\n' + base_dir,
                button=['作成', '中止'], dismissString='中止', p=self.window_name)
            if response == '作成':
                print('create_dir : ' + base_dir)
                os.makedirs(base_dir)

    def afterSaveOption(self, path_):
        if self.cb_val_ofas:
            os.startfile(os.path.dirname(path_))
        if self.cb_val_cas:
            cm.toClip(path_)

    def end_ivm(self, path_, message='保存しました'):
        dir_ = os.path.dirname(path_)
        file_name = os.path.basename(path_)
        print('save : ', path_)
        cmds.inViewMessage(
            amg='{0} : {1}{2}<font color=#FFAAFF>{3}'.format(message, dir_, os.sep, file_name), ck=True)

    # ---------------------------------------------------------------------------------
    def sjWork(self, specify_id=None):
        """シーン変更時のスクリプトジョブ：パステキストをidに対応して変更する"""
        if specify_id:
            id_ = specify_id
        else:
            exit_ = False
            scene_path = cmds.file(q=True, sn=True)
            if scene_path:
                scene_dir = os.path.dirname(scene_path)
                scene_file_name = os.path.basename(scene_path)
                id_ = tsubasa.getId(scene_path)
            else:
                id_ = tsubasa._getIdFromRoot()

            if id_ is None:
                exit_ = True

            # 初期化
            self.tf_versionup.setText('')
            # self.tf_to_mb.setText('')
            self.tf_to_data.setText('')
            self.tf_to_export.setText('')
            self.tf_to_server.setText('')

            # ID
            # self.tx_id.setLabel('')
            self.tf_id.setText('')

            # キャラ名
            self.tx_charaname.setText('')

            # シーン名
            try:
                self.tf_current_dir.setText(scene_dir)
                self.tx_current_scene_name.setLabel('<h2><b><font color=#66cdaa>' + scene_file_name)
            except:
                pass

            # 対象外の場合は終了
            if exit_:
                return
        print(id_)
        # フェイス判定（Mesh名がボディとルールが異なる）
        is_face = True if id_[0] == 'f' else False
        try:
            # self.tx_id.setLabel('<big><b>ID : ' + id_ + '  ')
            self.tf_id.setText(id_)
        except:
            pass

        try:
            self.tx_charaname.setText(' {0} '.format(tsubasa.ID[id_]))
        except:
            pass

        try:
            target_dir = tsubasa.getIdDir(scene_path)
        except:
            pass

        # バージョンアップ---------------------------------
        try:
            split_file = scene_file_name.split('_')
            if re.match('\w\d\d\d', split_file[1]):
                version = str(int(split_file[1][1:]) + 1).zfill(3)
            else:
                version = '000'
            new_scene_file_name = split_file[0] + '_v' + version + '_' + getDate() + '.mb'
            versionup_path = os.path.join(scene_dir, new_scene_file_name)
            self.tf_versionup.setText(os.path.normpath(versionup_path))
        except:
            pass
        # MotionBuilder---------------------------------
        try:
            to_mb_path = os.path.join(scene_dir, tsubasa.getId(scene_path) + '_for_MB.fbx')
            self.tf_to_mb.setText(os.path.normpath(to_mb_path))
        except:
            pass
        # Mesh---------------------------------
        try:
            rig_maya_dir = os.path.join(target_dir, 'rig', 'maya')
            if is_face:
                to_export_path = os.path.join(rig_maya_dir, tsubasa.getId(scene_path) + '_rig_export.mb')
            else:
                to_export_path = os.path.join(rig_maya_dir, tsubasa.getId(scene_path) + '.mb')
            self.tf_to_export.setText(os.path.normpath(to_export_path))
        except:
            pass
        # 作業用シーン---------------------------------
        try:
            if is_face:
                rig_data_dir = os.path.join(target_dir, 'rig', '_data', 'scenes')
            else:
                rig_data_dir = os.path.join(target_dir, 'rig', '_data', 'scenes', 'maya')
            to_data_path = os.path.join(rig_data_dir, scene_file_name)
            self.tf_to_data.setText(os.path.normpath(to_data_path))
        except:
            pass
        # Server---------------------------------
        try:
            self.tf_to_server.setText(
                os.path.normpath(os.path.join(self.my_server_path, tsubasa.getId(scene_path), scene_file_name)))
        except:
            pass

    # ---------------------------------------------------------------------------------
    def registServer(self):
        server_path = pm.fileDialog2(fileMode=3, dir=self.my_server_path)
        if server_path is not None:
            self.setting_dict['server_path'] = self.my_server_path = server_path[0]
            f.exportJson(self.SETTING_JSON, self.setting_dict)

    def openMyServer(self):
        os.startfile(os.path.normpath(self.my_server_path))

    def changeCbOfas(self):
        self.setting_dict['openFolderAfterSave'] = self.cb_val_ofas = pm.menuItem(self.mi_ofas, q=True, cb=True)
        f.exportJson(self.SETTING_JSON, self.setting_dict)

    def changeCbCas(self):
        self.setting_dict['clipAfterSave'] = self.cb_val_cas = pm.menuItem(self.mi_cas, q=True, cb=True)
        f.exportJson(self.SETTING_JSON, self.setting_dict)

    def openTfDir(self, tf):
        os.startfile(os.path.dirname((tf.getText())))

    def openTfScene(self, tf):
        scene = tf.getText()
        if not os.path.isfile(scene):
            pm.confirmDialog(message='シーンが存在しません', p=self.window_name)
            return

        response = cmds.confirmDialog(
            title='Confirm', message='シーンを開きます',
            button=['Open', 'Cancel'], dismissString='Cancel', p=self.window_name)
        if response == 'Open':
            pm.openFile(scene, f=True)
            pm.mel.addRecentFile(scene.replace(os.sep, '/'), 'mayaBinary')

    def copyClipTfPath(self, tf):
        cm.toClip(tf.getText())

    def runCopyClipboardSubmitCommentTmp(self):
        copyClipboardSubmitCommentTmp(self.tf_id.getText())

    def runSjWorkFromIdTf(self):
        self.sjWork(self.tf_id.getText())

    def openIdList(self):
        def setId():
            id = tslw.tsl.getSelectItem()[0].split(' : ')[0]
            self.tf_id.setText(id)
            self.runSjWorkFromIdTf()

        list_ = [x[0] + ' : ' + x[1] for x in tsubasa.ID.items()]
        tslw = ui.TextScrollListWindow(list_)
        tslw.window.setTitle('tsubasa Id List （ ダブルクリックでIDセット ）')
        pm.textScrollList(tslw.tsl, e=True, doubleClickCommand=pm.Callback(setId))
        tslw.init_ui()

    def checktool(self):
        import tsubasa.maya.tools.checktool.gui as ctgui
        # reload(ctgui)
        ctgui.main()
        self.selectTopNode()

    def exporter(self):
        pm.mel.eval('ExportModel')
        self.selectTopNode()

    def selectTopNode(self):
        id = self.tf_id.getText()
        if pm.objExists(id):
            pm.select(id)

    def normMesh(self):
        response = cmds.confirmDialog(
            title='Confirm',
            message='LOD0以下にある meshのskinを 以下の値で最適化します\n\nRound: 3, Max Influence: 4',
            button=['実行', '中止'], dismissString='中止', p=self.window_name)
        if response == '実行':
            lod = pm.PyNode('LOD0')
            nodes = pm.ls(lod, dag=True)
            result = []
            for node in nodes:
                try:
                    if node.getShape():
                        result.append(node)
                except:
                    pass
            pm.select(result)
            autoNormalize.main()

    # ------------------------------------------------------
    # チェックシーン
    # ------------------------------------------------------
    def sceneCheck(self):
        def uiBlock(message, result_list, text=False, fix_command=None):
            cmds.frameLayout(message, bgc=(0.18, 0.23, 0.23))
            cmds.columnLayout(adj=True, rs=2)
            if not result_list:
                cmds.text(l='<big>> OK', al='left')
            else:
                if text:
                    cmds.text(l='<font color=yellow><big>> ' + result_list, al='left')
                else:
                    for l in result_list:
                        cmds.button(l=l, c='cmds.select("{}")'.format(l), bgc=(0.6, 0.6, 0.3))
                if fix_command is not None:
                    cmds.button(l='修正する', c=fix_command)
            cmds.setParent(cl)

        window_name = 'check_scene_smrs'
        if cmds.window(window_name, ex=True):
            pm.deleteUI(window_name)
        x, y = cmds.window(self.window_name, q=True, tlc=True)
        win = cmds.window(
            window_name, t='チェックシーン', p=self.window_name,
            tlc=[x + 100, y + 400], w=400, h=600)
        cmds.scrollLayout(childResizable=True)
        cl = cmds.columnLayout(adj=True, rs=3)

        uiBlock('【 マテリアル名 】 不正', self._checkMaterialName())
        uiBlock('【 JointOrient 】 値が入っている joint', self._checkJointOrient())
        uiBlock(
            '【 SegmentScale 】 オンになっている joint',
            self._checkSegmentscale(), fix_command=partial(self._checkSegmentscale, True))
        uiBlock('【 AssistDrive 】 接続がない joint', self._checkADNConnect())
        uiBlock(
            '【 AssistDrive 】 キーが入っている joint',
            self._checkADNAnimKey(), fix_command=partial(self._checkADNAnimKey, True))
        uiBlock(
            '【 PreferredAngle 】 rotate と合致していない joint',
            self._checkPrefferdAngle(), fix_command=partial(self._checkPrefferdAngle, True))
        uiBlock(
            '【 displayHandle, displayLocalAxis 】 On になっている joint',
            self._checkJointVis(), fix_command=partial(self._checkJointVis, True))
        uiBlock(
            '【 character 】 不正',
            self._checkCharacter(), text=True, fix_command=partial(self._checkCharacter, True))
        uiBlock(
            '【 rig_info 】 不在',
            self._checkRiginfo(), text=True, fix_command=partial(self._checkRiginfo, True))
        uiBlock('【 階層 】 不正', self._checkHierarchy(), text=True)
        uiBlock('【 null, _900、del_*** 】 インフルエンスに含まれている', self._checkBind(), text=True)
        uiBlock('【 メッシュ 】 何もバインドされていない', self._checkNoBind())
        cmds.showWindow(win)

    def _checkMaterialName(self):
        dx11Shaders = cmds.ls(type='dx11Shader')
        lod_mat = [x for x in dx11Shaders if '_lod' in x]
        not_lod0_mat_list = [x for x in lod_mat if not x.endswith('_lod0')]
        return not_lod0_mat_list

    def _checkJointOrient(self):
        joints = [x for x in cmds.ls('null', dag=True, type='joint')]
        result_list = []
        for j in joints:
            if cmds.getAttr(j + '.jointOrientX') != 0.0 \
                or cmds.getAttr(j + '.jointOrientY') != 0.0 \
                    or cmds.getAttr(j + '.jointOrientZ') != 0.0:
                result_list.append(j)
        return result_list

    def _checkSegmentscale(self, *args):
        fix = True if args else False

        joints = [x for x in cmds.ls('null', dag=True, type='joint')]
        if fix:
            for j in joints:
                cmds.setAttr(j + '.segmentScaleCompensate', 0)
            cmds.evalDeferred(self.sceneCheck)
        else:
            result_list = []
            for j in joints:
                if cmds.getAttr(j + '.segmentScaleCompensate'):
                    result_list.append(j)
            return result_list

    def _checkADNConnect(self):
        adn_joints = [x for x in cmds.ls(type='joint') if x.startswith('_a')]
        result_list = []
        for j in adn_joints:
            if cmds.listConnections(j + '.t', s=True, d=False) is None \
                and cmds.listConnections(j + '.r', s=True, d=False) is None \
                    and cmds.listConnections(j + '.s', s=True, d=False) is None:
                result_list.append(j)
        return result_list

    def _checkADNAnimKey(self, *args):
        fix = True if args else False

        adn_joints = [x for x in cmds.ls(type='joint') if x.startswith('_a')]
        if fix:
            cmds.cutKey(adn_joints)
            cmds.evalDeferred(self.sceneCheck)
        else:
            keied_adn_joints = [x for x in adn_joints if cmds.keyframe(x, q=True, vc=True)]
            return keied_adn_joints

    def _checkCharacter(self, *args):
        fix = True if args else False
        chara_name = '_default_character'

        if fix:
            characters = cmds.ls(type='HIKCharacterNode')
            if len(characters) == 1:
                cmds.rename(characters[0], chara_name)
            else:
                cmds.delete(characters)
                from baseBodyGuide import command as bbg_cmd
                from baseBodyGuide import ui as bbg_ui
                tool = bbg_ui.baseBodyGuideUI()
                info = tool.getHikDefinition()
                bbg_cmd.createCharacterDefinition('_default')
                bbg_cmd.setCharacterDefinition(chara_name, info)
                cmds.evalDeferred(self.sceneCheck)
        else:
            message = ''
            characters = cmds.ls(type='HIKCharacterNode')
            if not characters:
                message += 'character がありません'
            elif len(characters) != 1:
                message += 'character が複数存在します'
            else:
                if characters[0] != chara_name:
                    message += 'character の名前が間違っています'
            return message

    def _checkPrefferdAngle(self, *args):
        fix = True if args else False

        cmds.currentTime(0, e=True)

        if fix:
            cmds.joint('null', e=True, spa=True, ch=True)
            cmds.evalDeferred(self.sceneCheck)
        else:
            joints = [x for x in cmds.ls('null', dag=True, type='joint') if not x.startswith('_a')]
            error_joints = []
            for j in joints:
                r = cmds.getAttr(j + '.rotate')
                pa = cmds.getAttr(j + '.preferredAngle')
                if not r == pa:
                    error_joints.append(j)
            return error_joints

    def _checkJointVis(self, *args):
        fix = True if args else False

        joints = [x for x in cmds.ls('null', dag=True, type='joint')]
        if fix:
            for j in joints:
                cmds.setAttr(j + '.displayHandle', False)
                cmds.setAttr(j + '.displayLocalAxis', False)
            cmds.evalDeferred(self.sceneCheck)
        else:
            error_joints = []
            for j in joints:
                if cmds.getAttr(j + '.displayHandle'):
                    error_joints.append(j)
                if cmds.getAttr(j + '.displayLocalAxis'):
                    error_joints.append(j)
            return list(set(error_joints))

    def _checkRiginfo(self, *args):
        fix = True if args else False
        from palette import ui as p_ui
        from palette import data as p_data
        obj = p_ui.paletteUI()
        rig_info_dict = p_data.getRigInformation(
            'D:/cygames/tsubasa/tools/dcc_user/maya/share/python/palette/_json/_rig_info.json')
        rig_info_set_name = rig_info_dict[0]
        fase_set_name = rig_info_dict[1]
        face_gp = 'Face_LOD0'
        if fix:
            obj._createRigInfoSet(add_log=False)
            cmds.evalDeferred(self.sceneCheck)
        else:
            message = ''
            if not cmds.objExists(rig_info_set_name):
                message += '{} がありません<br>'.format(rig_info_set_name)
            elif not cmds.objExists(fase_set_name):
                message += '{} がありません<br>'.format(fase_set_name)

            if cmds.objExists(fase_set_name) and cmds.objExists(face_gp):
                member = cmds.sets(fase_set_name, q=True)
                if member and face_gp in member:
                    pass
                else:
                    message += '{} が {} に含まれていません<br>'.format(face_gp, fase_set_name)
            return message

    def _checkHierarchy(self):
        message = ''
        id = self.tf_id.getText()
        if id:
            member = cmds.listRelatives(id, c=True)
            if len(member) == 3:
                if member[0] == 'LOD0' and member[1] == 'null' and member[2] == 'rig_GP':
                    message = ''
                else:
                    message += '{} 以下の階層の順番が不正です'.format(id)
            else:
                message += '{} 以下に足りない要素があります'.format(id)
        else:
            message += 'id が取得できないシーン名です'
        return message

    def _checkBind(self):
        message = ''
        meshs = getWithShapeNode()
        infl_list = sk.selectRelatedInfluences(meshs)
        if infl_list:
            if 'null' in infl_list:
                message += 'null がバインドされているメッシュがあります<br>'
            if '_900' in infl_list:
                message += '_900 がバインドされているメッシュがあります<br>'
            if startswith_in_stringlist('del_', infl_list):
                message += 'del_*** がバインドされているメッシュがあります'
        else:
            message = 'メッシュがバインドされていない可能性があります'
        return message

    def _checkNoBind(self):
        meshs = getWithShapeNode()

        no_bind_list = []
        for m in meshs:
            if not sk.selectRelatedInfluences(m):
                no_bind_list.append(m)
        return no_bind_list

    def loadIdleMotion(self, *args):
        response = cmds.confirmDialog(
            title='Confirm', message='HumanIK に Idle モーションを読み込みます',
            button=['Yes', 'Cancel'], dismissString='Yes', p=self.window_name)
        if response == 'Yes':
            _motion = 'D:/cygames/tsubasa/tools/dcc_user/maya/share/python/baseBodyGuide/_data/_motion/_mb/_motion_idle.mb'
            imp_nodes = cmds.file(_motion, i=True, ns='idle', returnNewNodes=True)
            for top in cmds.ls(imp_nodes, assemblies=True):
                cmds.setAttr(top + '.v', False)

            cmds.evalDeferred(self._setSouece)

    def _setSouece(self):
        cmds.currentTime(10, e=True)
        cm.changeHIKSource('_default_character', 'idle:_default_character')
        anim_curves = cm.getAnimCurves()
        cmds.select(anim_curves)
        cmds.evalDeferred('cmds.playbackOptions(e=True, maxTime=1000)')
        cm.hum('finish !')

    def _charaMotionImport(self):
        id_ = tsubasa._getIdFromRoot()
        if id_ is None:
            pm.warning('idが取得できません')
            return

        # self._pose_update = False
        project_path = tsubasa.getCharaProjectPathFromId(id_)
        anim_path = os.path.join(project_path, 'Animation/Files')
        if not os.path.isdir(anim_path):
            anim_path = project_path
        motion_path = pm.fileDialog2(fileMode=1, dir=anim_path, ff='fbx(*.fbx)')
        if motion_path is not None:
            pm.importFile(motion_path)
            anim_curves = cm.getAnimCurves()
            pm.select(anim_curves)
            cm.setAllKeyRange()

            '''
            # AssistDriveのキーを削除
            null = [x for x in cmds.ls(type='joint') if 'null' in x]
            adn_joints = cmds.ls(null[0], dag=True, type='joint')
            for adn_joint in adn_joints:
                if adn_joint.startswith('_a'):
                    cmds.cutKey(adn_joint)
            '''
        # pm.evalDeferred(pm.Callback('self._pose_update = True'))


def startswith_in_stringlist(word, string_list):
    is_startswith = False
    for s in string_list:
        if s.startswith(word):
            is_startswith = True
            return is_startswith
    else:
        return is_startswith


def getWithShapeNode(grp='LOD0'):
    nodes = pm.ls(grp, dag=True)
    result = []
    for node in nodes:
        try:
            if node.getShape():
                result.append(node.name())
        except:
            pass
    return result


def main():
    Ui().initUi()
